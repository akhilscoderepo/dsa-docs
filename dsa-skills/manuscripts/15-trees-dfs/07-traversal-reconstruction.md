<!-- lesson-kind: standard -->
<!-- lesson-id: traversal-reconstruction -->
## Traversal Reconstruction

<!-- stage: context -->
### The Flooded Shelf Plan

A flood ruined the large wall chart of a reading room's shelves, a branching plan in which every shelf had a distinct label and up to two sub-shelves, one on the left and one on the right. Two loose sheets survived. One lists the labels in the order a guide met them when walking the room, always naming a shelf before the shelves beneath it. The other lists them from the left side of the room to the right side, so that everything left of a shelf comes before it and everything right of it comes after.

The librarian wants to redraw the chart exactly as it was. She can see that the first label on the walking sheet must be the top shelf, and that the other sheet tells her something about what lies to its left. She is not sure how to continue from there without searching both sheets over and over.

<!-- stage: naive -->
### Cut The Sheets And Search Each Time

The direct method redraws one shelf at a time. The first label of the walking sheet is the top shelf. She finds that label on the left-to-right sheet by reading along it, cuts that sheet into the part before the label and the part after it, cuts the walking sheet to match, and repeats the whole job for each half.

```java
static Node redraw(int[] walk, int[] sides) {
    if (walk.length == 0) return null;
    Node top = new Node(walk[0]);
    int at = 0;
    while (sides[at] != walk[0]) at++;
    top.left = redraw(Arrays.copyOfRange(walk, 1, 1 + at), Arrays.copyOfRange(sides, 0, at));
    top.right = redraw(Arrays.copyOfRange(walk, 1 + at, walk.length), Arrays.copyOfRange(sides, at + 1, sides.length));
    return top;
}
```

Because all labels differ, the label is found at one place, and the two halves describe exactly the left and right sub-shelves.

<!-- stage: bottleneck -->
### Searching And Cutting Repeat At Every Shelf

Each call reads along a sheet to find a label and copies both sheets into smaller arrays. For a chart that is one long line of n shelves, each call hands almost the whole sheet to the next one, so the searching costs n + (n - 1) + ... steps, and the copying costs as much. The total is O(n^2), which for fifty thousand shelves means over a billion steps and a flood of temporary arrays.

Neither cost is needed. The position of a label on the left-to-right sheet never changes while the chart is redrawn, so it could be looked up in one step after a single pass that records every position. And the pieces of a sheet are always a stretch between two positions, so a pair of numbers can describe a piece without copying. What remains is to keep track of which label on the walking sheet comes next.

<!-- stage: insight -->
### One Sheet Roots, One Sheet Splits

Record the position of every label on the left-to-right sheet once, in an **index map** from label to position. Then each call owns one stretch of the left-to-right sheet, given by its two end positions, and the labels of exactly one subtree sit inside that stretch. The first unused label of the walking sheet is the root of that subtree, because the walk names a shelf before everything beneath it. The **root position** found by the map splits the stretch into the part before it, which is the left sub-shelf, and the part after it, which is the right one. The **left size**, the root position minus the start of the stretch, tells how many labels of the walking sheet belong to the left side.

That count is why one moving pointer on the walking sheet is enough. The root takes the next label, the whole left side then consumes exactly its left size labels, and what follows belongs to the right side. So the call builds the left subtree first, then the right one, and the pointer moves once for every shelf created. An empty stretch, where the start is past the end, returns null and consumes nothing.

The invariant is that every call owns one stretch of the left-to-right sheet and starts reading the walking sheet at the first label of that stretch's subtree. With the map, each shelf costs O(1), so the work is O(n) for the map and the calls together.

<!-- names: index map, root position, left size -->

Two sheets are needed. The walking sheet alone cannot tell whether a lone second label hangs on the left or the right.

<!-- stage: variables -->
### Pointer, Map And Stretch Ends

Four values describe the work. The array `pre` is the walking sheet and `inorder` the left-to-right sheet. The counter `next` is the position of the next unused label in `pre`, shared by all calls. The map `where` sends each label to its position in `inorder`. The two integers `lo` and `hi` bound the stretch owned by a call, and `lo > hi` means empty. The recursion must build the left subtree before the right one, because the shared counter follows the walking order.

<!-- stage: trace -->
### The Pointer Eats One Label Per Shelf

The first trace rebuilds the shelves from the walking sheet 3, 9, 20, 15, 7 and the left-to-right sheet 9, 3, 15, 20, 7. The cells are the walking sheet and the pointer `pre` marks the label just used as a root. Each step shows the stretch owned by that call as the two numbers `lo` and `hi`, and the root's position in the other sheet. The label 3 sits at position 1, so the left stretch has one entry and the right one has three.

```trace
{"cells":["3","9","20","15","7"],"pointers":["pre"],"steps":[{"at":{"pre":0},"vars":{"lo":0,"hi":4,"rootPos":1},"note":"The next walking label is 3, found at position 1 of the other sheet, so the stretch 0 to 4 splits into the left stretch 0 to 0 and the right stretch 2 to 4."},{"at":{"pre":1},"vars":{"lo":0,"hi":0,"rootPos":0},"note":"The next walking label is 9, found at position 0 of the other sheet, so the stretch 0 to 0 splits into the left stretch 0 to -1 and the right stretch 1 to 0."},{"at":{"pre":2},"vars":{"lo":2,"hi":4,"rootPos":3},"note":"The next walking label is 20, found at position 3 of the other sheet, so the stretch 2 to 4 splits into the left stretch 2 to 2 and the right stretch 4 to 4."},{"at":{"pre":3},"vars":{"lo":2,"hi":2,"rootPos":2},"note":"The next walking label is 15, found at position 2 of the other sheet, so the stretch 2 to 2 splits into the left stretch 2 to 1 and the right stretch 3 to 2."},{"at":{"pre":4},"vars":{"lo":4,"hi":4,"rootPos":4},"note":"The next walking label is 7, found at position 4 of the other sheet, so the stretch 4 to 4 splits into the left stretch 4 to 3 and the right stretch 5 to 4."}]}
```

The second trace uses the lopsided walking sheet 4, 3, 2, 1 with the left-to-right sheet 1, 2, 3, 4, where every shelf has only a left sub-shelf. The root position is always the end of the stretch, so each right stretch is empty and the left stretch shrinks by one. The pointer moves at each step, and no label is searched for, since the map already knows where it is.

```trace
{"cells":["4","3","2","1"],"pointers":["pre"],"steps":[{"at":{"pre":0},"vars":{"lo":0,"hi":3,"rootPos":3},"note":"The next walking label is 4, found at position 3 of the other sheet, so the stretch 0 to 3 splits into the left stretch 0 to 2 and the right stretch 4 to 3."},{"at":{"pre":1},"vars":{"lo":0,"hi":2,"rootPos":2},"note":"The next walking label is 3, found at position 2 of the other sheet, so the stretch 0 to 2 splits into the left stretch 0 to 1 and the right stretch 3 to 2."},{"at":{"pre":2},"vars":{"lo":0,"hi":1,"rootPos":1},"note":"The next walking label is 2, found at position 1 of the other sheet, so the stretch 0 to 1 splits into the left stretch 0 to 0 and the right stretch 2 to 1."},{"at":{"pre":3},"vars":{"lo":0,"hi":0,"rootPos":0},"note":"The next walking label is 1, found at position 0 of the other sheet, so the stretch 0 to 0 splits into the left stretch 0 to -1 and the right stretch 1 to 0."}]}
```

<!-- stage: code -->
### Building From Two Traversals

```java
final class Rebuild {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int next;
    static int[] pre;
    static Map<Integer, Integer> where;

    static Node build(int lo, int hi) {
        if (lo > hi) return null;
        Node node = new Node(pre[next++]);
        int mid = where.get(node.val);
        node.left = build(lo, mid - 1);
        node.right = build(mid + 1, hi);
        return node;
    }

    static Node rebuild(int[] preorder, int[] inorder) {
        pre = preorder;
        next = 0;
        where = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) where.put(inorder[i], i);
        return build(0, inorder.length - 1);
    }
}
```

The map costs O(n) to fill, and each call creates one node with constant work, so the whole rebuild is O(n) time with O(n) extra space for the map and O(h) for the stack.

<!-- stage: applicability -->
### When Two Orders Pin Down One Tree

Reach for this when two traversals of the same tree with distinct labels are given, one that names the root first, such as preorder, or last, such as postorder, and the inorder one. Typical sources are saved structures, serialized trees and checking whether two sequences could describe the same tree. The invariant is that each call owns one stretch of the inorder sequence and reads the root sequence from the first label of that stretch's subtree.

A false friend is believing that one traversal is enough. Preorder alone cannot tell whether the second label is a left or right child, so many trees share one preorder sequence, and the same holds for any single order. A second false friend is preorder with postorder, which still leaves one-child shelves ambiguous. A third is repeated labels, which make the position of a label non-unique and break the split.

In Java, fill a `HashMap<Integer, Integer>` once instead of scanning, and build the left subtree before the right, since the shared counter moves in walking order. Passing two end positions avoids the array copies that `Arrays.copyOfRange` would make.

<!-- stage: exercises -->
### Exercises

#### [Build] Split One Root (Author exercise)
<!-- id: tr-split-one-root -->

**Prerequisites.** The traversal orders lesson and the idea of an owned range.

**Problem.** Given the preorder and inorder sequences of a binary tree with distinct labels, return `[leftSize, rightSize]`, the number of nodes in the two subtrees of the root. Empty sequences give `[0, 0]`.

**Constraints.** 0 <= n <= 3000, the labels are distinct integers, and the two sequences describe the same tree.

**Example 1.** Input `preorder = [3, 9, 20, 15, 7]`, `inorder = [9, 3, 15, 20, 7]`, output `[1, 3]`.

**Example 2.** Input `preorder = [1]`, `inorder = [1]`, output `[0, 0]`.

**Hint.** Where is the first preorder label found in the inorder sequence, and what lies on each side of it?

**Changed decision.** The first preorder label is the root, and its position in the inorder sequence is what divides the remaining labels into two sides.

#### [Vary] Reconstruct By Index Ranges (Author exercise)
<!-- id: tr-rebuild-by-ranges -->

**Prerequisites.** The Split One Root rung and the position map.

**Problem.** Rebuild the tree from its preorder and inorder sequences without copying any slices, passing only the two end positions of the inorder stretch each call owns, and return the postorder sequence of the rebuilt tree.

**Constraints.** 0 <= n <= 3000, the labels are distinct integers, and the two sequences describe the same tree.

**Example 1.** Input `preorder = [3, 9, 20, 15, 7]`, `inorder = [9, 3, 15, 20, 7]`, output `[9, 15, 7, 20, 3]`.

**Example 2.** Input `preorder = [1, 2, 3]`, `inorder = [2, 1, 3]`, output `[2, 3, 1]`.

**Hint.** Which of the two child calls must run first so that the preorder pointer stays in step?

**Changed decision.** A stretch is described by two positions and never copied, and a shared counter walks the preorder sequence as nodes are created.

#### [Boundary] Empty Range And Skewed Tree (Author exercise)
<!-- id: tr-empty-range-skewed -->

**Prerequisites.** The Reconstruct By Index Ranges rung and its stopping rule.

**Problem.** Rebuild the tree as above and return `[height, emptyCalls]`, where height counts nodes on the longest root-to-leaf path and `emptyCalls` is the number of times the recursion was entered with an empty range. The empty input still makes one call.

**Constraints.** 0 <= n <= 3000, the labels are distinct integers, and the two sequences describe the same tree.

**Example 1.** Input `preorder = []`, `inorder = []`, output `[0, 1]`.

**Example 2.** Input `preorder = [1, 2, 3]`, `inorder = [3, 2, 1]`, output `[3, 4]`.

**Hint.** Each node makes two calls on its sides, and only nodes are created by non-empty calls. How do the two counts relate?

**Changed decision.** The recursion stops exactly when the owned range is empty, so a tree of n nodes makes n non-empty calls and n + 1 empty ones.

#### [Recognize] Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105)
<!-- id: tr-construct-from-pre-in -->

**Prerequisites.** The Empty Range And Skewed Tree rung and the full rebuild.

**Problem.** Rebuild the tree from its preorder and inorder sequences and return it as a level-order array, with `null` for each missing child and no trailing nulls.

**Constraints.** 1 <= n <= 3000, the labels are distinct integers between -3000 and 3000, and the sequences describe the same tree.

**Example 1.** Input `preorder = [1, 2, 4, 5, 3]`, `inorder = [4, 2, 5, 1, 3]`, output `[1, 2, 3, 4, 5]`.

**Example 2.** Input `preorder = [5, 6, 7]`, `inorder = [5, 6, 7]`, output `[5, null, 6, null, 7]`.

**Hint.** What does the index map replace, and what advances the preorder position?

**Changed decision.** The index map replaces every linear search, and a moving preorder position replaces the array slices.
