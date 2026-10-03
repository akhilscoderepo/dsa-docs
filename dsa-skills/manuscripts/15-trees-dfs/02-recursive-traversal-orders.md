<!-- lesson-kind: standard -->
<!-- lesson-id: recursive-traversal-orders -->
## Recursive Traversal Orders

<!-- stage: context -->
### The Shelf Index Of A Reading Room

A reading room keeps its shelves in a branching index. Each shelf has a label, and under it at most two sub-shelves, one on the left and one on the right. The head librarian needs three different sheets from this one index. The first is a copy sheet, written so that a new reading room can be set up from it by building each shelf before any shelf beneath it. The second is a sheet for a room where smaller labels sit on the left of a shelf and larger labels on the right, which should read from the smallest label to the largest. The third is a clearing sheet, where a shelf may be emptied only after everything beneath it has gone.

All three sheets list every shelf exactly once. She notices that the shelves are the same each time and only the moment of writing a label down seems to change.

<!-- stage: naive -->
### Build A New List At Each Shelf

The direct method treats each shelf as a small job that returns its own sheet. A shelf starts a fresh list, writes its label, and then glues on the sheet returned for the left sub-shelf and the sheet returned for the right one. An empty sub-shelf returns an empty list.

```java
static List<Integer> sheetFrom(Node shelf) {
    if (shelf == null) return new ArrayList<>();
    List<Integer> sheet = new ArrayList<>();
    sheet.add(shelf.val);
    sheet.addAll(sheetFrom(shelf.left));
    sheet.addAll(sheetFrom(shelf.right));
    return sheet;
}
```

The sheet it returns is right for the copy job, because each label is written ahead of everything below it, and it lists every shelf once.

<!-- stage: bottleneck -->
### Gluing Lists Copies The Same Labels Again

Every shelf copies the whole sheet of each sub-shelf into its own new list, so a label is copied once for every shelf above it. On a chain of n shelves, each hanging off the one before, the bottom label is copied n - 1 times, the next one n - 2 times, and so on, and the total is O(n^2) copies. One hundred thousand shelves in a line would need about five billion list copies, and a fresh list is also created for every call.

A second weakness is that the moment of writing the label is hidden inside the gluing code. The clearing sheet needs the label written last and the sorted sheet needs it written between the two glued parts. Changing the order by rearranging three lines of list-building is easy to get wrong, and each variant still pays the copying cost. What is needed is one sheet shared by all the calls, where each call only appends, so that the total work is O(n) and the order depends on a single visible choice.

<!-- stage: insight -->
### Where The Label Gets Written

Pass one shared output list down every call. A call on a shelf does three things: it makes the call on the left sub-shelf, it makes the call on the right sub-shelf, and it appends its own label to the shared list. The only freedom is where the append sits among those two calls, and that placement alone decides the order of the sheet. Appending before both calls gives **preorder**, appending between the two calls gives **inorder**, and appending after both calls gives **postorder**. Each order is one program with the same three lines rearranged.

Why the order holds follows from one fact. A call on a subtree appends exactly the labels of that subtree, and it appends them as one unbroken block, because nothing outside the subtree runs while the call is active. So in preorder the block of a shelf is its label, then the whole left block, then the whole right block. In inorder the left block comes first, then the label, then the right block. In postorder both blocks come first and the label ends the block. A null sub-shelf makes a call that returns at once and appends nothing, which is why one-sided shelves need no special code.

The invariant is that every call adds one contiguous block to the end of the list and leaves everything already written untouched. Calls are never repeated on the same subtree, so the work is O(n).

<!-- names: preorder, inorder, postorder -->

The orders are not labels for the same sheet. A sheet written in one of them usually cannot be turned into another without the tree.

<!-- stage: variables -->
### Output List And Append Position

Three things matter in the code. The parameter `node` is the shelf whose subtree the call owns, and the base case returns when it is `null`. The parameter `out` is the one list shared by every call, created by the caller and never inside the recursion. The position of `out.add(node.val)` relative to the two recursive calls is the whole design decision. Passing the list as an argument keeps separate runs from mixing their output, which a shared static field would not.

<!-- stage: trace -->
### Three Moments At Every Shelf

The first trace follows the shelf index 4, 2, 7, 1, 3 given in level-order form, where the cells hold that array and the pointer `node` marks the shelf whose call is acting. Each shelf passes through three moments in order: its call has just started, its left call has just returned, and both calls have returned. Preorder writes a label at the first moment, inorder at the second, and postorder at the third, so one walk grows all three sheets together. Watch the leaf 1, where the left call returns at once and the three moments follow each other with nothing between them.

```trace
{"cells":["4","2","7","1","3"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"pre":"4","in":"","post":""},"note":"The call on the shelf 4 has just started, so preorder writes 4."},{"at":{"node":1},"vars":{"pre":"4 2","in":"","post":""},"note":"The call on the shelf 2 has just started, so preorder writes 2."},{"at":{"node":3},"vars":{"pre":"4 2 1","in":"","post":""},"note":"The call on the shelf 1 has just started, so preorder writes 1."},{"at":{"node":3},"vars":{"pre":"4 2 1","in":"1","post":""},"note":"The left call of the shelf 1 has returned, so inorder writes 1."},{"at":{"node":3},"vars":{"pre":"4 2 1","in":"1","post":"1"},"note":"Both calls of the shelf 1 have returned, so postorder writes 1."},{"at":{"node":1},"vars":{"pre":"4 2 1","in":"1 2","post":"1"},"note":"The left call of the shelf 2 has returned, so inorder writes 2."},{"at":{"node":4},"vars":{"pre":"4 2 1 3","in":"1 2","post":"1"},"note":"The call on the shelf 3 has just started, so preorder writes 3."},{"at":{"node":4},"vars":{"pre":"4 2 1 3","in":"1 2 3","post":"1"},"note":"The left call of the shelf 3 has returned, so inorder writes 3."},{"at":{"node":4},"vars":{"pre":"4 2 1 3","in":"1 2 3","post":"1 3"},"note":"Both calls of the shelf 3 have returned, so postorder writes 3."},{"at":{"node":1},"vars":{"pre":"4 2 1 3","in":"1 2 3","post":"1 3 2"},"note":"Both calls of the shelf 2 have returned, so postorder writes 2."},{"at":{"node":0},"vars":{"pre":"4 2 1 3","in":"1 2 3 4","post":"1 3 2"},"note":"The left call of the shelf 4 has returned, so inorder writes 4."},{"at":{"node":2},"vars":{"pre":"4 2 1 3 7","in":"1 2 3 4","post":"1 3 2"},"note":"The call on the shelf 7 has just started, so preorder writes 7."},{"at":{"node":2},"vars":{"pre":"4 2 1 3 7","in":"1 2 3 4 7","post":"1 3 2"},"note":"The left call of the shelf 7 has returned, so inorder writes 7."},{"at":{"node":2},"vars":{"pre":"4 2 1 3 7","in":"1 2 3 4 7","post":"1 3 2 7"},"note":"Both calls of the shelf 7 have returned, so postorder writes 7."},{"at":{"node":0},"vars":{"pre":"4 2 1 3 7","in":"1 2 3 4 7","post":"1 3 2 7 4"},"note":"Both calls of the shelf 4 have returned, so postorder writes 4."}]}
```

The second trace uses a one-sided index 6, 2, null, null, 4, where the shelf 6 has only a left sub-shelf and the shelf 2 has only a right one. It records the sheet that writes a label between the two calls. Each empty sub-shelf shows up as a call that returns immediately and writes nothing, so the walk simply moves on to the next step in the recipe.

```trace
{"cells":["6","2","null","null","4"],"pointers":["node"],"steps":[{"at":{"node":1},"vars":{"sheet":""},"note":"The left sub-shelf of 2 is empty, so that call returns at once and writes nothing."},{"at":{"node":1},"vars":{"sheet":"2"},"note":"The left call of the shelf 2 is done, so the label 2 joins the sheet."},{"at":{"node":4},"vars":{"sheet":"2"},"note":"The left sub-shelf of 4 is empty, so that call returns at once and writes nothing."},{"at":{"node":4},"vars":{"sheet":"2 4"},"note":"The left call of the shelf 4 is done, so the label 4 joins the sheet."},{"at":{"node":4},"vars":{"sheet":"2 4"},"note":"The right sub-shelf of 4 is empty, so that call returns at once and writes nothing."},{"at":{"node":0},"vars":{"sheet":"2 4 6"},"note":"The left call of the shelf 6 is done, so the label 6 joins the sheet."},{"at":{"node":0},"vars":{"sheet":"2 4 6"},"note":"The right sub-shelf of 6 is empty, so that call returns at once and writes nothing."}]}
```

<!-- stage: code -->
### One Walk Three Placements

```java
final class OrderWalks {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static void pre(Node node, List<Integer> out) {
        if (node == null) return;
        out.add(node.val);
        pre(node.left, out);
        pre(node.right, out);
    }

    static void in(Node node, List<Integer> out) {
        if (node == null) return;
        in(node.left, out);
        out.add(node.val);
        in(node.right, out);
    }

    static void post(Node node, List<Integer> out) {
        if (node == null) return;
        post(node.left, out);
        post(node.right, out);
        out.add(node.val);
    }
}
```

Every node is entered once and appends once, so each walk takes O(n) time. The extra space apart from the output is the call stack, which is O(h) for height h and reaches O(n) on a chain.

<!-- stage: applicability -->
### When Order Carries The Meaning

Choose a recursive walk when every node must be handled once and the moment of handling matters. Copying and saving a structure wants the parent before its children. Reading a binary search tree in sorted order wants the parent between the two sides. Deleting, summing up or freeing a structure wants the children done first. The invariant to hold on to is that each call appends one contiguous block and never disturbs earlier output.

The nearest false friend is treating the three orders as interchangeable ways to list the same nodes, when a different order produces a different sheet and only some pairs of sheets rebuild a unique tree. Another false friend is the level-order array of the input itself, which looks like a listing but is a layer-by-layer layout and matches none of the three. A third is the return-a-list style, which hides the append position and copies repeatedly.

In Java, create the output list once and pass it down, because a static list keeps old results between test cases. Check for `null` before reading `node.val`, and remember that a deep chain can exhaust the call stack.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Tree Preorder Traversal (LeetCode 144)
<!-- id: tr-preorder-walk -->

**Prerequisites.** The Tree Representation lesson and its null convention.

**Problem.** A binary tree is given as a level-order array where `null` marks a missing child and the children of a missing node are not listed. Return the values in the order node, then left subtree, then right subtree.

**Constraints.** 0 <= values.length <= 100 and every value is an integer between -100 and 100.

**Example 1.** Input `values = [1, null, 2, 3]`, output `[1, 2, 3]`.

**Example 2.** Input `values = [5, 3, 8, 1]`, output `[5, 3, 1, 8]`.

**Hint.** Where does the append go relative to the two calls, and what does a call on null do?

**Changed decision.** The label is written before either child call, so each subtree contributes one block that begins with its own root.

#### [Vary] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: tr-inorder-walk -->

**Prerequisites.** The Binary Tree Preorder Traversal rung above.

**Problem.** For the same level-order input, return the values in the order left subtree, then node, then right subtree.

**Constraints.** 0 <= values.length <= 100 and every value is an integer between -100 and 100.

**Example 1.** Input `values = [1, null, 2, 3]`, output `[1, 3, 2]`.

**Example 2.** Input `values = [5, 3, 8, 1]`, output `[1, 3, 5, 8]`.

**Hint.** Which single line moves when preorder becomes this order?

**Changed decision.** The append moves between the two calls, so the whole left block is written before the node and the right block after it.

#### [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: tr-one-sided-orders -->

**Prerequisites.** The inorder rung and the preorder rung above it.

**Problem.** Given a level-order array, return the three sheets as `[pre, in, post]`, each a list of values, where the third writes a node after both of its subtrees. A tree with no nodes gives three empty lists, and a chain that only goes left or only goes right must still be handled by the same code.

**Constraints.** 0 <= values.length <= 200 and values are integers between -1000 and 1000.

**Example 1.** Input `values = []`, output `[[], [], []]`.

**Example 2.** Input `values = [1, 2, null, 3]`, output `[[1, 2, 3], [3, 2, 1], [3, 2, 1]]`.

**Hint.** What does a call on an empty side append? Does the code ever ask whether a side is the left one?

**Changed decision.** No branch checks for a missing side, because the call on null returns at once and the three placements stay the only difference between the walks.

#### [Recognize] Binary Tree Postorder Traversal (LeetCode 145)
<!-- id: tr-postorder-walk -->

**Prerequisites.** The one-sided boundary rung and both earlier walks.

**Problem.** For the same level-order input, return the values in the order left subtree, right subtree, then node.

**Constraints.** 0 <= values.length <= 100 and every value is an integer between -100 and 100.

**Example 1.** Input `values = [1, null, 2, 3]`, output `[3, 2, 1]`.

**Example 2.** Input `values = [5, 3, 8, 1]`, output `[1, 3, 8, 5]`.

**Hint.** When is it safe to write the label of a node, and what must have finished first?

**Changed decision.** The append is delayed until both child calls return, so a node appears only after everything it owns has been written.
