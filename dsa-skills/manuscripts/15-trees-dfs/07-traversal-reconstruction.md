<!-- lesson-kind: standard -->
<!-- lesson-id: traversal-reconstruction -->
## Rebuild A Tree From Two Orders

<!-- stage: context -->
### Restoring A Saved Tree From One List

A debugger saves a binary tree of values to disk before it closes. To keep the file small, the developer writes the values in the order in which a depth-first walk reaches them, as one list. After a restart the debugger must rebuild the tree from the list. It cannot. The list `1, 2` fits a tree with root 1 and left child 2, and it also fits a tree with root 1 and right child 2. The saved file does not say which one it was.

A second list in a different walk order should remove the doubt. This lesson asks how two lists determine the tree, one in preorder and one in inorder. It also asks how to read them without scanning or copying them again and again.

<!-- stage: naive -->
### Scanning And Copying For Every Node

The first version takes the root from the first value of the preorder list. It scans the inorder list for that value, cuts both lists into pieces with array copies, and repeats on each piece.

```java
import java.util.*;

final class RebuildByCopying {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(int[] pre, int[] in) {
        if (pre.length == 0) return null;                        // no values left means no node
        Node root = new Node(pre[0]);                            // the first value of the first list is the root
        int k = 0;
        while (in[k] != pre[0]) k++;                             // scan the second list for the root
        root.left = build(Arrays.copyOfRange(pre, 1, 1 + k),     // copy the left part of both lists
                          Arrays.copyOfRange(in, 0, k));
        root.right = build(Arrays.copyOfRange(pre, 1 + k, pre.length),   // copy the right part of both lists
                           Arrays.copyOfRange(in, k + 1, in.length));
        return root;
    }
}
```

For `pre = {1, 2}` and `in = {2, 1}` the method builds a root 1 with a left child 2. For `pre = {1, 2}` and `in = {1, 2}` it builds a root 1 with a right child 2. The two lists together settle what one list could not.

<!-- stage: bottleneck -->
### Counting The Scans And The Copies

```predict
The tree is a chain of n nodes where each node has only a left child, so the lists are pre = n, n-1, ..., 1 and in = 1, 2, ..., n. How many values does the method scan and copy over all calls?

The call on the lists of size m scans m values to find the root and copies about 2m values. The sizes are n, n-1, ..., 1, so the total is proportional to n + (n-1) + ... + 1, which is O(n^2).
```

The method does three kinds of repeated work. It scans the second list from the start for every root. It copies array pieces that its caller already held. It also allocates new arrays at every level, so the extra memory is O(n^2) in total because every open call holds its own pieces.

All three costs come from the same choice: each call receives its own lists. The values never move. A call only needs to know which part of each list belongs to its subtree. The position of a root in the second list also does not change between calls, so a lookup table built once can replace every scan.

<!-- stage: insight -->
### Reading A Window Of Each List

The two lists describe one tree, and each subtree occupies a contiguous window in both lists. The method passes the window boundaries as indexes and never copies a value. The method assumes that all values are distinct, so a value names exactly one node.

<!-- names: owned range, index map, left size -->

#### The First Value Names The Root

In preorder the root of a subtree comes before every other node of that subtree. The first value inside the preorder window is therefore the root of the subtree. In inorder the root sits between its left subtree and its right subtree. Every value before the root in the inorder window belongs to the left subtree, and every value after it belongs to the right subtree.

#### The Window Sizes Carry Over

The **left size** is the number of values before the root in the inorder window. Preorder visits the root, then the whole left subtree, then the whole right subtree. So the next `left size` values after the root in the preorder window are the left subtree, and all the remaining values are the right subtree. Both lists therefore give each child a window of the same length.

#### One Call Owns One Pair Of Windows

An **owned range** is the pair of windows that one call is responsible for, one in each list. The two windows hold the same set of values, and that set is exactly one subtree. When the window is empty, the call returns `null`. The invariant is that every call receives matching windows for exactly one subtree.

#### A Table Replaces The Scan

The **index map** is a `HashMap` from each value to its position in the inorder list. It is built once, in O(n) time, before the first call. Each call then finds the position of its root in O(1) time. The whole rebuild costs O(n).

<!-- stage: variables -->
### The Boundaries Of The Two Windows

- **pl** and **pr** are the first and last index of the preorder window, and the window is empty when `pl > pr`.
- **il** and **ir** are the first and last index of the inorder window, and it has the same length as the preorder window.
- **k** is the position of the root in the inorder list, taken from the index map.
- **leftSize** is `k - il`, the number of values in the left subtree.

The left child receives the preorder window `pl + 1` to `pl + leftSize` and the inorder window `il` to `k - 1`. The right child receives the preorder window `pl + leftSize + 1` to `pr` and the inorder window `k + 1` to `ir`.

<!-- stage: trace -->
### Splitting The Windows Step By Step

#### Rebuilding A Six-Node Tree

The lists are `pre = 8, 5, 2, 9, 4, 7` and `in = 2, 5, 9, 8, 7, 4`. The cells show the inorder list. The pointers `lo` and `hi` mark the inorder window, and `root` marks the position of the root. A pointer outside the cells means an empty window, and calls on empty windows return `null` and are not shown.

```trace
{"cells":["2","5","9","8","7","4"],"pointers":["lo","root","hi"],"steps":[{"at":{"lo":0,"root":3,"hi":5},"vars":{"preorder window":"0 to 5","left size":3,"right size":2},"note":"The first value of the preorder window is 8. It sits at inorder position 3, so 3 values go to the left subtree and 2 to the right subtree."},{"at":{"lo":0,"root":1,"hi":2},"vars":{"preorder window":"1 to 3","left size":1,"right size":1},"note":"The first value of the preorder window is 5. It sits at inorder position 1, so 1 value goes to the left subtree and 1 to the right subtree."},{"at":{"lo":0,"root":0,"hi":0},"vars":{"preorder window":"2 to 2","left size":0,"right size":0},"note":"The first value of the preorder window is 2. It sits at inorder position 0, so 0 values go to the left subtree and 0 to the right subtree."},{"at":{"lo":2,"root":2,"hi":2},"vars":{"preorder window":"3 to 3","left size":0,"right size":0},"note":"The first value of the preorder window is 9. It sits at inorder position 2, so 0 values go to the left subtree and 0 to the right subtree."},{"at":{"lo":4,"root":5,"hi":5},"vars":{"preorder window":"4 to 5","left size":1,"right size":0},"note":"The first value of the preorder window is 4. It sits at inorder position 5, so 1 value goes to the left subtree and 0 to the right subtree."},{"at":{"lo":4,"root":4,"hi":4},"vars":{"preorder window":"5 to 5","left size":0,"right size":0},"note":"The first value of the preorder window is 7. It sits at inorder position 4, so 0 values go to the left subtree and 0 to the right subtree."}]}
```

The first call picks 8 and finds it at inorder position 3, so three values go left and two go right. Each smaller window repeats the same step. The tree has root 8, left child 5 with children 2 and 9, and right child 4 with a left child 7.

#### Rebuilding A Chain

The lists are `pre = 5, 4, 3` and `in = 3, 4, 5`. Each root sits at the right end of its window, so the right window is empty every time.

```trace
{"cells":["3","4","5"],"pointers":["lo","root","hi"],"steps":[{"at":{"lo":0,"root":2,"hi":2},"vars":{"preorder window":"0 to 2","left size":2,"right size":0},"note":"The first value of the preorder window is 5. It sits at inorder position 2, so 2 values go to the left subtree and 0 to the right subtree."},{"at":{"lo":0,"root":1,"hi":1},"vars":{"preorder window":"1 to 2","left size":1,"right size":0},"note":"The first value of the preorder window is 4. It sits at inorder position 1, so 1 value goes to the left subtree and 0 to the right subtree."},{"at":{"lo":0,"root":0,"hi":0},"vars":{"preorder window":"2 to 2","left size":0,"right size":0},"note":"The first value of the preorder window is 3. It sits at inorder position 0, so 0 values go to the left subtree and 0 to the right subtree."}]}
```

The left size equals the window size minus one at every call, so each node has only a left child. The calls on the empty right windows return `null` at once.

<!-- stage: code -->
### The Window Method In Code

```java
import java.util.*;

final class RebuildByWindows {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(int[] pre, int[] in) {
        Map<Integer, Integer> where = new HashMap<>();
        for (int i = 0; i < in.length; i++) where.put(in[i], i);     // one pass fills the index map
        return rebuild(pre, 0, pre.length - 1, 0, in.length - 1, where);
    }

    private static Node rebuild(int[] pre, int pl, int pr, int il, int ir, Map<Integer, Integer> where) {
        if (pl > pr) return null;                                // an empty window owns no node
        Node root = new Node(pre[pl]);                           // the first preorder value is the root
        int k = where.get(pre[pl]);                              // its inorder position, found in O(1)
        int leftSize = k - il;                                   // values before the root go left
        root.left = rebuild(pre, pl + 1, pl + leftSize, il, k - 1, where);
        root.right = rebuild(pre, pl + leftSize + 1, pr, k + 1, ir, where);
        return root;
    }
}
```

The method reads the arrays and never writes to them. If a value appeared twice, the map would keep only the last position of that value, so the input must have distinct values.

- **Time** is O(n), because the map takes n steps and each node receives one call with O(1) work.
- **Space** is O(n) for the index map and the returned tree, plus a stack of pending calls as deep as the height.

<!-- stage: applicability -->
### Checking That Two Lists Are Enough

#### Naming The Owned Range

The invariant is that each call receives windows that hold the same set of values and describe exactly one subtree. The window lengths must always agree. If the lengths differ, the input is not a valid pair, and the arithmetic of `leftSize` stops matching.

#### Finding The False Friend

One list looks like enough information. That belief is the false friend of this topic. The preorder list `1, 2` fits two different trees, as the opening showed. Two lists in different orders can still fail. Preorder and postorder together do not fix a tree with one-child nodes, because a lone child could sit on either side. Inorder is the list that separates left from right.

#### No-Go Conditions

The method needs distinct values. With repeated values the root has several possible positions, and the index map gives only one. The method also needs both lists to come from the same tree. If the inputs are not trusted, the call must check that each root is found in its window before it uses `k`.

<!-- stage: exercises -->
### Exercises

#### [Build] Split One Root (Author exercise)
<!-- id: tw-split-root -->

**Prerequisites.** The windows and the left size from this lesson.

**Problem.** The arrays `pre` and `in` hold the preorder and the inorder of one binary tree with distinct values. Return an array of two integers: the number of nodes in the left subtree of the root and the number of nodes in the right subtree. Find the root in `in`, and do not rebuild the tree.

**Constraints.** The limits are:
- **Length** of each array is `n` with `1 <= n <= 3000`.
- **Values** are distinct integers between -3000 and 3000.
- **Input** is valid: both arrays hold the same values from one tree.
- **Answer** is `[left, right]` with `left + right = n - 1`.

**Example 1.** Input `pre = [8, 5, 2, 9, 4, 7]` and `in = [2, 5, 9, 8, 7, 4]`, output `[3, 2]`.

**Example 2.** Input `pre = [1]` and `in = [1]`, output `[0, 0]`.

**Hint.** Where does `pre[0]` sit in `in`? How many values lie before it, and how many after it?

**Changed decision.** The method stops after the first split and returns the two sizes.

#### [Vary] Reconstruct By Index Ranges (Author exercise)
<!-- id: tw-postorder -->

**Prerequisites.** The exercise above.

**Problem.** The arrays `pre` and `in` give the preorder and the inorder of one binary tree. All values are distinct. Return the values of the tree in postorder. Do not build any node and do not copy any array piece. Pass window boundaries as indexes.

**Constraints.** The limits are:
- **Length** of each array is `n` with `0 <= n <= 3000`.
- **Values** are distinct integers between -3000 and 3000.
- **Input** is valid, and both arrays have the same length.
- **Answer** is a list of `n` values, empty when `n` is 0.

**Example 1.** Input `pre = [8, 5, 2, 9, 4, 7]` and `in = [2, 5, 9, 8, 7, 4]`, output `2, 9, 5, 7, 4, 8`.

**Example 2.** Input `pre = [3, 1, 2]` and `in = [1, 3, 2]`, output `1, 2, 3`.

**Hint.** The root goes last in postorder. Which two windows must be written first, and in which order?

**Changed decision.** The call writes the root after both child calls and builds no node.

#### [Boundary] Empty Range And Skewed Tree (Author exercise)
<!-- id: tw-height -->

**Prerequisites.** The two exercises above.

**Problem.** Two arrays `pre` and `in` list the values of one binary tree with distinct values, in preorder and inorder. Return the height of the tree in nodes. An empty pair of arrays describes the empty tree with height 0. The recursion must stop exactly when its window is empty.

**Constraints.** The limits are:
- **Length** of each array is `n` with `0 <= n <= 3000`.
- **Values** are distinct integers between -3000 and 3000.
- **Input** is valid, and the trees may be chains of any direction.
- **Answer** is an integer between 0 and `n`.

**Example 1.** Input `pre = []` and `in = []`, output 0.

**Example 2.** Input `pre = [5, 4, 3]` and `in = [3, 4, 5]`, output 3.

**Hint.** What does a call on an empty window return? How does the height of a node use the two child heights?

**Changed decision.** The empty window is the base case, and a chain produces one empty window per node.

#### [Recognize] Construct Binary Tree From Preorder And Inorder (LeetCode 105)
<!-- id: tw-construct -->

**Prerequisites.** All three exercises above.

**Problem.** Two arrays `preorder` and `inorder` list the values of one binary tree with distinct values. Construct the tree and return its root. The index lookup for the root must take constant time per node, and the arrays must not be copied.

**Constraints.** The limits are:
- **Length** of each array is `n` with `1 <= n <= 3000`.
- **Values** are distinct integers between -3000 and 3000.
- **Input** is valid, and both arrays hold the same values.
- **Answer** is the root of a tree whose preorder and inorder equal the inputs.

**Example 1.** Input `preorder = [8, 5, 2, 9, 4, 7]` and `inorder = [2, 5, 9, 8, 7, 4]`, output a root 8. Its left child 5 has children 2 and 9, and its right child 4 has a left child 7.

**Example 2.** Input `preorder = [6]` and `inorder = [6]`, output a single node 6.

**Hint.** What does a table built once give each call? What advances when the left subtree is finished?

**Changed decision.** A table and index windows replace the scan and the array copies.
