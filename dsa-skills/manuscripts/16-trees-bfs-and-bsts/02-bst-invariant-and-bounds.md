<!-- lesson-kind: standard -->
<!-- lesson-id: bst-invariant-and-bounds -->
## Carry Value Limits Down A Search Tree

<!-- stage: context -->
### Why A Valid-Looking Tree Loses A Key

A phone-book program keeps names in a binary tree and finds a name by comparing it with one node per level. A bug inserts the name "Mia" into the wrong branch three levels down. Every parent and child pair still looks sorted, because "Mia" sits below a node that holds a larger name. The program passes its quick check, and then every search for "Mia" fails, even though she is in the tree.

A **binary search tree** is a binary tree where, for every node, all keys in the left subtree are smaller and all keys in the right subtree are larger. The word "all" matters. A check that compares each node only with its parent accepts a tree that breaks the rule far below. This lesson asks what a node must be compared with, and how a program does it in one pass.

<!-- stage: naive -->
### Comparing Each Node With Its Children

The direct plan walks every node and checks the two rules that are visible at that node: the left child is smaller, and the right child is larger. The tree is valid if no node breaks them.

```java
final class ChildCheck {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static boolean looksValid(TreeNode node) {
        if (node == null) return true;                                   // an empty tree has no violation
        if (node.left != null && node.left.val >= node.val) return false;   // the left child must be smaller
        if (node.right != null && node.right.val <= node.val) return false; // the right child must be larger
        return looksValid(node.left) && looksValid(node.right);          // repeat for every node below
    }
}
```

The method accepts the tree with the root 5, a left child 1, and a right child 6 whose own children are 3 and 7. Every parent and child pair is in order, so the method returns `true`.

<!-- stage: bottleneck -->
### Finding The Missed Violation

```predict
In the tree above, the node 3 is the left child of 6, and 6 is the right child of 5. Is the tree a valid search tree? What does a search for the key 3 do, starting at the root 5?

The tree is not valid. The key 3 sits in the right subtree of 5, so it must be larger than 5. A search for 3 compares 3 with 5, goes left to the node 1, and never reaches the node 3. The search reports a missing key.
```

The method is wrong because it checks only the parent. The node 3 is smaller than its parent 6, and the check stops there. The rule says 3 must also be larger than 5, an ancestor two levels up.

A repair that compares each node with every key in its subtrees is correct. It scans the whole left subtree for a key that is too large and the whole right subtree for a key that is too small. That scan costs O(n) per node, and the total is O(n * h), which becomes O(n^2) on a chain. The program needs the ancestor information without scanning for it.

<!-- stage: insight -->
### Pass The Limits Down The Path

Every node has a range of keys that it may hold. Going left from a node with key `k` forces all keys below to be smaller than `k`. Going right forces all keys below to be larger than `k`. A path from the root to any node is a series of such turns, and each turn adds one restriction. The restrictions stack, so the allowed keys at a node are the ones that satisfy every turn on its path.

#### Two Numbers Describe Every Turn

Only the tightest restriction on each side matters. Among all the right turns on the path, the last one has the largest key, so it gives the strongest lower limit. Among all the left turns, the last one has the smallest key and gives the strongest upper limit. The two numbers form the **bounds** of the node: a lower limit and an upper limit. A key is legal at the node when it lies strictly between the two numbers, which is an **open interval** that excludes both ends.

#### Updating The Bounds At Each Child

The root starts with no restriction. For a node with key `k` and bounds `(low, high)`, the left child gets `(low, k)`, because the upper limit tightens to `k`. The right child gets `(k, high)`, because the lower limit tightens to `k`. The method checks the key against the bounds, then makes the two calls. Each node is visited once, so the check costs O(n) time.

#### Choosing What Equal Keys Mean

The words "smaller" and "larger" leave out the case of equal keys. A **duplicate policy** states where an equal key may live: nowhere, only in the left subtree, or only in the right subtree. The policy decides which end of the interval is open and which end is closed. A strict tree allows no duplicates, so both ends stay open.

<!-- names: bounds, open interval, duplicate policy -->

<!-- stage: variables -->
### The State Of The Bounds Check

- **node** is the node under test in the current call.
- **low** is the lower limit from the last right turn on the path, or no limit at the root.
- **high** is the upper limit from the last left turn on the path, or no limit at the root.
- **val** is the key of the node, which must satisfy `low < val < high`.
- **result** is `true` only when the node and both of its subtrees pass.

<!-- stage: trace -->
### Bounds Narrow Along A Path

The cells hold the keys in level order, and the pointer `node` marks the node under test.

#### Catching The Deep Violation

The tree has the root 5, the children 1 and 6, and the children 3 and 7 under the node 6. The cells hold `5, 1, 6, 3, 7`.

```trace
{"cells":[5,1,6,3,7],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"low":"no limit","high":"no limit"},"note":"The root starts with no limit. The key 5 lies inside the interval, so the walk continues."},{"at":{"node":1},"vars":{"low":"no limit","high":"5"},"note":"Left of 5: the upper limit becomes 5. The key 1 lies inside the interval, so the walk continues."},{"at":{"node":2},"vars":{"low":"5","high":"no limit"},"note":"Right of 5: the lower limit becomes 5. The key 6 lies inside the interval, so the walk continues."},{"at":{"node":3},"vars":{"low":"5","high":"6"},"note":"Left of 6: the upper limit becomes 6. The key 3 must lie between 5 and 6, and it does not, so the result is false."}]}
```

At the node 3 the bounds are 5 and 6, because the walk turned right at 5 and then left at 6. The key 3 is not larger than 5, so the walk reports `false`. The check against the parent alone would have accepted it.

#### Narrowing Bounds On A Valid Tree

The tree has the root 8, the children 4 and 12, and the children 2, 6, 10 and 14 below them. The trace follows the path to the node 6.

```trace
{"cells":[8,4,12,2,6,10,14],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"low":"no limit","high":"no limit"},"note":"The root starts with no limit. The key 8 lies inside the interval."},{"at":{"node":1},"vars":{"low":"no limit","high":"8"},"note":"Left turn at 8: the upper limit becomes 8. The key 4 lies inside the interval."},{"at":{"node":4},"vars":{"low":"4","high":"8"},"note":"Right turn at 4: the lower limit becomes 4. The key 6 lies inside the interval."}]}
```

After the left turn at 8 the upper limit is 8. After the right turn at 4 the lower limit is 4, and the upper limit stays 8. Each turn replaced exactly one limit and left the other as it was.

<!-- stage: code -->
### The Bounds Check In Code

```java
final class BoundsCheck {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static boolean isValid(TreeNode root) {
        return check(root, Long.MIN_VALUE, Long.MAX_VALUE);       // long limits sit outside every int key
    }

    private static boolean check(TreeNode node, long low, long high) {
        if (node == null) return true;                            // no node means no violation
        if (node.val <= low || node.val >= high) return false;    // strict policy: both ends are open
        return check(node.left, low, node.val)                    // left turn tightens the upper limit
            && check(node.right, node.val, high);                 // right turn tightens the lower limit
    }
}
```

The limits are `long` because an `int` key can equal `Integer.MIN_VALUE` or `Integer.MAX_VALUE`, and an `int` sentinel would reject a legal key. A `long` limit is always outside the `int` range, so the first comparison never rejects a legal root.

- **Time** is O(n), because each node is visited once and compared in constant time.
- **Space** is O(h) for the recursion stack, where `h` is the tree height.

<!-- stage: applicability -->
### Using The Bounds Rule

#### Recognizing The Cue

Use bounds when a property must hold between a node and every ancestor, or between a node and every key in a subtree. The words "valid search tree", "every key in the left subtree" and "all descendants" signal it. A local comparison cannot prove such a property.

#### Stating The Invariant

The invariant is that every call receives the exact interval allowed by all of its ancestors. A call that passes its own comparison and passes the narrowed intervals to its children proves the whole subtree. Nothing outside the subtree can change the interval of a node inside it.

#### Naming The False Friend

The false friend is the parent-child comparison, and it fails silently on deep violations. Equal keys are the second trap. A tree that allows equal keys on the right needs a closed lower end and an open upper end, and the same code with open ends rejects a legal tree. State the duplicate policy before writing the comparison.

<!-- stage: exercises -->
### Exercises

#### [Build] Validate One Root And Children (Author exercise)
<!-- id: tb-bst-root-children -->

**Prerequisites.** The open interval of a child from this lesson.

**Problem.** Given the root of a binary tree of at most three nodes, where only the root has children, return `true` if the tree is a strict binary search tree. The left child must lie in the open interval from negative infinity to the root key, and the right child must lie in the open interval from the root key to positive infinity.

**Constraints.** The limits are:
- **Nodes** number between 1 and 3, and no node below a child exists.
- **Values** are `int` values, and values may be equal.
- **Answer** is a `boolean`.
- **Mutation** does not occur.

**Example 1.** Input root 2 with children 1 and 3, output `true`.

**Example 2.** Input root 2 with children 2 and 3, output `false`, because an equal key is not allowed on the left.

**Hint.** Which interval does each child receive? What happens to a missing child?

**Changed decision.** Each child is tested against an interval and not against a bare comparison.

#### [Vary] Propagate Ancestor Bounds (Author exercise)
<!-- id: tb-bst-count-inside -->

**Prerequisites.** The exercise above.

**Problem.** The input is a binary tree. Return the number of nodes that respect all of their ancestors. A node respects its ancestors when its key is smaller than the key of every ancestor it lies to the left of, and larger than the key of every ancestor it lies to the right of. Equivalently, the key lies in the open interval between the largest right-turn key and the smallest left-turn key on its path. A node that breaks its own ancestors still passes its keys down to its children.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** satisfy `-10^9 <= val <= 10^9`, and values may repeat.
- **Answer** is an `int` between 0 and the node count.
- **Mutation** does not occur.

**Example 1.** Input root 5 with children 1 and 6, where 6 has children 3 and 7, output 4, because the node 3 lies outside the interval (5, 6).

**Example 2.** Input root 4 with a right child 4, output 1, because the right child must be larger than 4.

**Hint.** Which limit changes on a left turn, and which on a right turn? What if the node key is looser than the limit already held?

**Changed decision.** The walk counts and continues after a failure, and each child takes the tighter of the old limit and the new key.

#### [Boundary] Integer Extremes And Duplicates (Author exercise)
<!-- id: tb-bst-extremes -->

**Prerequisites.** The two exercises above.

**Problem.** For a binary tree, return `true` if every key in the left subtree of each node is strictly smaller than the node key, and every key in the right subtree is greater than or equal to the node key. Keys may be any `int`, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** cover the full `int` range.
- **Policy** places equal keys only in the right subtree.
- **Answer** is a `boolean`, and an empty tree is valid.

**Example 1.** Input root 2 with a right child 2, output `true`.

**Example 2.** Input a root `Integer.MIN_VALUE` with a left child `Integer.MIN_VALUE`, output `false`, because no `int` key is smaller than the minimum.

**Hint.** Which end of the interval is now closed? Which type holds a limit just outside the `int` range?

**Changed decision.** One end of the interval closes, and the limits widen to `long`.

#### [Recognize] Validate Binary Search Tree (LeetCode 98)
<!-- id: tb-validate-bst -->

**Prerequisites.** All three exercises above.

**Problem.** Decide whether a binary tree is a valid binary search tree, and return `true` if it is. A valid tree has, for every node, only smaller keys in its left subtree and only larger keys in its right subtree, and both subtrees are valid.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4.
- **Values** cover the full `int` range, and equal keys are not allowed in a valid tree.
- **Answer** is a `boolean`.
- **Mutation** does not occur.

**Example 1.** Input root 5 with children 1 and 4, where 4 has children 3 and 6, output `false`.

**Example 2.** Input root 2 with children 1 and 3, output `true`.

**Hint.** Which ancestor is violated at the node 3 in the first example? What does the recursion pass to the right child of the root?

**Changed decision.** Both ends of the interval are open again, and every node uses the interval of its whole path.
