<!-- lesson-kind: standard -->
<!-- lesson-id: balanced-tree-concepts -->
## Balanced-Tree Concepts

<!-- stage: context -->
### The Registry Clerk And The Class List

A registry clerk hangs name tags on a branching board, following the rule she was taught: each new tag goes left at every board where it is smaller and right where it is larger, until it reaches an empty hook. In her first week the names arrive in no particular order, and finding any tag takes only a handful of glances at the board, which she is proud of.

In the second week a school delivers its class list, already in alphabetical order. She hangs the tags exactly as before, and by the end of the day the board has become one long diagonal line that runs off the wall. Finding the last name on the list now takes as many glances as there are names, and she has not made any mistake in following the rule.

<!-- stage: naive -->
### Hang Each Tag By The Rule

The clerk's method is the ordinary insertion that follows one path and attaches the new tag at the first empty hook. A lookup repeats the same path. There is nothing in the method that looks at the shape of the board, and the rule alone decides every position.

```java
static Node hang(Node board, int tag) {
    if (board == null) return new Node(tag);
    Node at = board;
    while (true) {
        if (tag < at.val) {
            if (at.left == null) { at.left = new Node(tag); break; }
            at = at.left;
        } else {
            if (at.right == null) { at.right = new Node(tag); break; }
            at = at.right;
        }
    }
    return board;
}

static int lookupCost(Node board, int tag) {
    int glances = 0;
    for (Node at = board; at != null; at = tag < at.val ? at.left : at.right) {
        glances++;
        if (at.val == tag) break;
    }
    return glances;
}
```

Each hang and each lookup follows one path, so every tag ends up at a hook that obeys the rule, and the lookup always finds it.

<!-- stage: bottleneck -->
### Cost Follows Height, Not Count

Each hang and each lookup costs the length of one path, which is the height h, and the height depends on the order of arrival and not only on the number of tags. For random order the height stays near log n, but for names that arrive sorted every tag becomes the right child of the previous one, so h = n and the lookups cost O(n). Looking up all n tags once adds up to 1 + 2 + ... + n, which is O(n^2), so a class list of a hundred thousand names costs about five billion glances.

The rule of the search tree guarantees correctness but says nothing about shape, and no one controls the order in which keys arrive. A repair would need to keep the height near log n whatever the order, by changing the shape a little after each insertion, while never breaking the left-smaller, right-larger rule. The cost of a lookup would then be O(log n) in the worst case rather than only on average.

<!-- stage: insight -->
### Keep The Two Sides Near Equal Height

Add a second promise to the search rule, a **balance condition**: at every node, the heights of the left and right subtrees differ by at most 1. A tree that keeps this promise has height at most about 1.44 times log2 of n, so every search, insertion and removal costs O(log n) in the worst case. The promise does not demand a full or symmetric tree. A node may have a deeper left side than right side, and the lowest level may be partly empty, provided that no node is off by more than one.

After an insertion, a promise may be broken at some node on the path back to the root, and then the shape must be repaired locally. The repair is a **rotation**. A right rotation at a node whose left side is too deep lifts its left child to the top. The old top becomes the right child of that lifted node, and the right subtree of the lifted node, which held keys between the two, becomes the left subtree of the old top. A left rotation is the mirror image. Both are done by changing three links, so each costs O(1).

A rotation never breaks the search rule, since it keeps the left-to-right order of all keys exactly the same, and only the depths change. The invariant is that the inorder listing of the tree is the same before and after every rotation, while the height of the rotated part decreases.

<!-- names: balance condition, rotation, ordered map -->

In practice, nobody writes this by hand. A library **ordered map** such as Java's `TreeMap` keeps the promise for the programmer, and the decision is mainly about when to reach for one.

<!-- stage: variables -->
### Heights, Balance Factor And Pivot

Each node carries an int `height`, counted in nodes, with a missing subtree counting as 0. The balance factor of a node is `height(left) - height(right)`, and a value of -1, 0 or 1 is acceptable. A factor of 2 means the left side is too deep, and -2 means the right side is. In a rotation the `top` is the node whose balance has broken, the `pivot` is its child on the heavy side, and the middle subtree is the pivot's child on the side facing the top. After the links change, the heights of `top` and then of `pivot` must be recomputed, in that order, because `pivot` now sits above `top`.

<!-- stage: trace -->
### A Leaning Line And A Search Compared

The first trace repairs the line of tags 3, 2, 1, hung in that order so that each is the left child of the one before. The marker `node` is on the board where attention is focused. At 3 the heights of the two sides are 2 and 0, so the balance factor is 2 and the left side is too deep. The right rotation lifts 2 to the top, 3 becomes its right child, and the inorder listing 1 2 3 never changes.

```trace
{"cells":["3","2","null","1"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"balance":2,"inorder":"1 2 3"},"note":"At the board 3 the left side has height 2 and the right side has height 0, so the balance factor is 2 and the left side is too deep."},{"at":{"node":1},"vars":{"balance":1,"inorder":"1 2 3"},"note":"The heavy child 2 is chosen as the pivot. Its right subtree is empty, so nothing needs to move to the left of 3."},{"at":{"node":1},"vars":{"balance":0,"inorder":"1 2 3"},"note":"After the right rotation 2 is on top with 1 on its left and 3 on its right. Both sides now have height 1, and the inorder listing is still 1 2 3."}]}
```

The second trace looks up the tag 7 on a board that was hung from the tags 1 to 7 in order, so it is a right-leaning line, written here with a null cell for each empty left hook. Seven boards are visited before the tag is found, one per tag, because there is nothing to discard at any step.

```trace
{"cells":["1","null","2","null","3","null","4","null","5","null","6","null","7"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"tag":7,"visited":1},"note":"The tag 7 is larger than 1, so the walk goes right and everything on the left is dropped."},{"at":{"node":2},"vars":{"tag":7,"visited":2},"note":"The tag 7 is larger than 2, so the walk goes right and everything on the left is dropped."},{"at":{"node":4},"vars":{"tag":7,"visited":3},"note":"The tag 7 is larger than 3, so the walk goes right and everything on the left is dropped."},{"at":{"node":6},"vars":{"tag":7,"visited":4},"note":"The tag 7 is larger than 4, so the walk goes right and everything on the left is dropped."},{"at":{"node":8},"vars":{"tag":7,"visited":5},"note":"The tag 7 is larger than 5, so the walk goes right and everything on the left is dropped."},{"at":{"node":10},"vars":{"tag":7,"visited":6},"note":"The tag 7 is larger than 6, so the walk goes right and everything on the left is dropped."},{"at":{"node":12},"vars":{"tag":7,"visited":7},"note":"The board 7 holds the tag 7, found after 7 boards."}]}
```

The third trace looks up the same tag 7 on a board hung from the same seven tags in a balanced order, with 4 on top. Only three boards are visited, since each comparison drops half of what remains.

```trace
{"cells":["4","2","6","1","3","5","7"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"tag":7,"visited":1},"note":"The tag 7 is larger than 4, so the walk goes right and everything on the left is dropped."},{"at":{"node":2},"vars":{"tag":7,"visited":2},"note":"The tag 7 is larger than 6, so the walk goes right and everything on the left is dropped."},{"at":{"node":6},"vars":{"tag":7,"visited":3},"note":"The board 7 holds the tag 7, found after 3 boards."}]}
```

<!-- stage: code -->
### Height, Rotation And Rebalancing Insert

```java
final class BalancedParts {
    static final class Node {
        int val, height = 1;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int height(Node n) { return n == null ? 0 : n.height; }

    static int balance(Node n) { return height(n.left) - height(n.right); }

    static void refresh(Node n) { n.height = 1 + Math.max(height(n.left), height(n.right)); }

    static Node rotateRight(Node top) {
        Node pivot = top.left;
        top.left = pivot.right;
        pivot.right = top;
        refresh(top);
        refresh(pivot);
        return pivot;
    }

    static Node rotateLeft(Node top) {
        Node pivot = top.right;
        top.right = pivot.left;
        pivot.left = top;
        refresh(top);
        refresh(pivot);
        return pivot;
    }

    static Node insert(Node node, int key) {
        if (node == null) return new Node(key);
        if (key < node.val) node.left = insert(node.left, key);
        else if (key > node.val) node.right = insert(node.right, key);
        else return node;
        refresh(node);
        int b = balance(node);
        if (b > 1) {
            if (balance(node.left) < 0) node.left = rotateLeft(node.left);
            return rotateRight(node);
        }
        if (b < -1) {
            if (balance(node.right) > 0) node.right = rotateRight(node.right);
            return rotateLeft(node);
        }
        return node;
    }
}
```

Each rotation only rewrites links and refreshes two heights, so it takes O(1) time. An insertion walks one path and rebalances along it, so it takes O(log n) time and O(log n) recursion stack.

<!-- stage: applicability -->
### When Shape Matters More Than Rule

Think about balance whenever a search tree faces input that might arrive in sorted or nearly sorted order: timestamps, auto-incremented identifiers, alphabetical imports, and anything that has been batch-sorted upstream. The invariant is that every node keeps its two sides within one level of each other and that rotations leave the inorder order untouched.

The first false friend is the idea that a balanced tree is complete or symmetric. A tree that has a deeper left side than right side at some node is still balanced if the difference never exceeds one. A second false friend is believing that the plain search rule protects against bad shapes, because the rule decides correctness and only the order of insertion decides the height. A third is confusing a hash map with an ordered map: a `HashMap` has no sorted order, no next key and no range queries, so reaching for it when those are needed is wrong, while a `TreeMap` gives all three at O(log n) per operation.

In Java prefer `TreeMap` or `TreeSet` when ordered queries and updates are both needed, since they are balanced internally. Writing deletion for an AVL or a red-black tree by hand is outside the scope of this chapter and rarely required in practice.

<!-- stage: exercises -->
### Exercises

#### [Build] Compare Search Heights (Author exercise)
<!-- id: tb-compare-search-heights -->

**Prerequisites.** The search and insert lesson and the notion of height.

**Problem.** Take the keys 1 to n. Hang them in a plain search tree in increasing order, and also hang them in the median-first order, where the middle key is hung first and then, recursively, the middle of each remaining half. For each tree return the height in nodes, and the total number of boards visited when every key is looked up once. The answer is `[chainHeight, balancedHeight, chainTotal, balancedTotal]`.

**Constraints.** 1 <= n <= 10000, and every key is looked up once with a visit counted for each board on its path, the board holding the key included.

**Example 1.** Input `n = 7`, output `[7, 3, 28, 17]`.

**Example 2.** Input `n = 1`, output `[1, 1, 1, 1]`.

**Hint.** In the chain, how many boards lie on the path to the key k, and in the balanced tree, how many boards sit at each depth?

**Changed decision.** The only difference between the two trees is the order of insertion, and the comparison measures how that order alone changes height and lookup cost.

#### [Vary] Identify One Rotation (Author exercise)
<!-- id: tb-identify-rotation -->

**Prerequisites.** The Compare Search Heights rung and the balance factor.

**Problem.** Three distinct keys are hung in a plain search tree in the given order. Say which single repair makes the three nodes balanced: `none` if the tree is already balanced, `rotate right` for a line leaning left, `rotate left` for a line leaning right, and `double rotation` when the keys form a bend, left then right or right then left.

**Constraints.** The input has exactly three distinct integers between 1 and 1000 in any order.

**Example 1.** Input `keys = [3, 2, 1]`, output `rotate right`.

**Example 2.** Input `keys = [1, 3, 2]`, output `double rotation`.

**Hint.** Which of the six orders produce a root with two children, and which produce a line or a bend?

**Changed decision.** The case is read directly from the shape of three hung keys, so the repair is chosen by which side is too heavy and whether the heavy child leans the same way.

#### [Boundary] Preserve Inorder Through Rotation (Author exercise)
<!-- id: tb-rotation-preserves-order -->

**Prerequisites.** The Identify One Rotation rung and the three-link change.

**Problem.** Given a search tree in level order, a key naming a node, and a direction `right` or `left`, rotate at that node, which has the needed child, and return the level-order array of the whole tree afterwards, with trailing `null` entries removed. The listing of keys in sorted order must be the same before and after.

**Constraints.** 2 <= values.length <= 2000, keys are distinct integers between 0 and 100000, and the node named has a left child for `right` and a right child for `left`.

**Example 1.** Input `values = [5, 3, 8, 2, 4]`, `key = 5`, `direction = right`, output `[3, 2, 5, null, null, 4, 8]`.

**Example 2.** Input `values = [4, 2, 6, null, null, 5, 7]`, `key = 4`, `direction = left`, output `[6, 4, 7, 2, 5]`.

**Hint.** Which subtree changes parents in a rotation, and which two links of the old top and its child are rewritten?

**Changed decision.** Only three links change, so the sorted order of the keys is untouched and the answer can be checked by comparing sorted listings before and after.

#### [Recognize] Explain Library Choice (Author exercise)
<!-- id: tb-library-choice -->

**Prerequisites.** The Preserve Inorder Through Rotation rung and the idea of an ordered map.

**Problem.** A program stores integer keys and answers questions. Flags tell whether it needs ordered queries such as the next larger key, and whether keys are added or removed after the start. Return `HashMap` when order is not needed, `sorted array` when order is needed and the data never changes after the start, and `TreeMap` when order is needed and the data changes.

**Constraints.** Both flags are true or false, and there are exactly four inputs possible when the order flag is true or false and the change flag is true or false.

**Example 1.** Input `needsOrder = true`, `dataChanges = true`, output `TreeMap`.

**Example 2.** Input `needsOrder = false`, `dataChanges = true`, output `HashMap`.

**Hint.** What does a hash map lose, and what does a sorted array cost when a single key is inserted?

**Changed decision.** A hand-built unbalanced search tree is never the answer, because input that arrives sorted turns it into a line, while the library ordered map keeps its height logarithmic.
