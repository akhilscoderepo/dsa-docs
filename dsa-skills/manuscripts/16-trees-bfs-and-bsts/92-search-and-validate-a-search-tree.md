<!-- lesson-kind: combination -->
<!-- lesson-id: search-and-validate-a-search-tree -->
## Search And Validate A Search Tree

<!-- stage: context -->
### Why The Nightly Check Takes Hours

A billing system keeps invoice numbers in a binary search tree, and a nightly job confirms that the tree is still valid after the day's inserts and deletes. The first version of the job asks a natural question about each node: if a customer looked up this invoice number, would the lookup find this node? On a test tree the job finishes in a blink. On the production tree with fifty million invoices it runs past the morning, because each of the fifty million questions starts a fresh lookup from the top.

A tree is valid when every lookup finds its key. This lesson asks whether the job can answer all the questions in one pass, and what the lookups and the validity check share.

<!-- stage: contributions -->
### What Search And Limits Each Add

Two earlier ideas meet here. The one-path search supplies the rule that a comparison with a node key discards a whole side. A lookup follows a single line from the root and ignores everything else. The search alone says nothing about whether the rest of the tree obeys the same rule, because it only looks at the nodes on its own line.

The value limits from the lesson on carrying limits down a search tree supply the memory. Each node carries the strictest lower and upper limit that the nodes above it impose. The limits alone do not say what the limits mean for a lookup. Together the two ideas show that the interval of a node is exactly the set of keys whose lookups pass through that node, so a valid tree is one where every node lies in its own interval.

<!-- stage: naive -->
### Looking Up Every Key From The Root

The direct plan tests each node with a lookup. For a node with key `k`, the method walks from the root by comparisons and checks that the walk ends at that very node. If any lookup ends elsewhere, or ends at an empty slot, the tree is invalid.

```java
final class ValidateByLookup {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static TreeNode find(TreeNode root, int key) {
        TreeNode node = root;
        while (node != null && node.val != key) {
            node = key < node.val ? node.left : node.right;      // one branch per comparison
        }
        return node;
    }

    static boolean check(TreeNode root, TreeNode node) {
        if (node == null) return true;
        if (find(root, node.val) != node) return false;          // a lookup must land on this very node
        return check(root, node.left) && check(root, node.right);
    }
}
```

On the tree with the root 20, the children 10 and 30, and the children 5 and 25 under the node 10, the lookup of 25 goes right at 20, goes left at 30, and ends at an empty slot. The method reports the tree as invalid, which is correct.

<!-- stage: bottleneck -->
### Counting The Repeated Lookups

```predict
The tree is a chain of n nodes, where each node has only a right child and the keys increase. How many comparisons do all the lookups need together, and what is the cost in big-O terms?

The lookup for the node at depth d makes d comparisons, so the total is 1 + 2 + ... + n, which is about n squared over 2. The cost is O(n^2) on a chain, and O(n * h) in general.
```

Every lookup replays the comparisons of the lookups before it, because the lookup for a node begins at the root and passes through every ancestor of that node. The ancestors of a node are the same nodes that the check at its parent already compared. The program needs to keep the result of those comparisons while it moves down, and then it can test each node once.

<!-- stage: insight -->
### Each Slot Owns An Interval Of Keys

Think of every empty child slot of a valid tree as a place where a key could be inserted. The comparisons of a lookup from the root to a slot are fixed, so the keys that reach that slot form one open interval. The **slot interval** of a node is the open interval between the largest key on a right turn and the smallest key on a left turn along the path to the node. A key can be inserted at a slot exactly when it lies in the slot interval, and the key then keeps every earlier lookup correct.

#### One Pass Replaces All The Lookups

The lookup for a node reaches that node if and only if the node's key lies inside the slot interval of its position. The **bounds** of the interval are the two numbers carried down the recursion. A left child receives the node key as its upper bound, and a right child receives the node key as its lower bound. A single pass checks every node against its bounds, so the check costs O(n) in place of O(n * h).

#### Using The Same Interval For Updates

The interval also tells where an operation is legal. A delete that moves a key into a node must keep the key inside the interval of that node. The key moved from a right subtree lies in the interval of the removed node because it is larger than every key on the left and smaller than the remaining keys on the right. The **search path** to a node gives its interval, and a check of the new key against the interval after each update confirms the change was legal.

<!-- names: slot interval, bounds, search path -->

<!-- stage: variables -->
### The State Of The Combined Check

- **node** is the node whose slot interval the two limits describe.
- **low** is the strictest lower limit from the right turns on the path, with no limit at the root.
- **high** is the strictest upper limit from the left turns on the path, with no limit at the root.
- **key** is the value of the node, which must satisfy `low < key < high`.

<!-- stage: trace -->
### One Lookup Fails, One Pass Finds Why

#### Looking Up A Key That Cannot Be Reached

The tree has the root 20, the children 10 and 30, and the children 5 and 25 under the node 10. The cells hold `20, 10, 30, 5, 25`, and the pointer `node` marks the node compared at each step, with -1 for an empty slot. The lookup is for the key 25.

```trace
{"cells":[20,10,30,5,25],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"key":25},"note":"The key 25 is larger than 20, so the lookup goes right."},{"at":{"node":2},"vars":{"key":25},"note":"The key 25 is smaller than 30, so the lookup goes left."},{"at":{"node":-1},"vars":{"key":25},"note":"The lookup reaches an empty slot without meeting a node that holds 25, so the node 25 is not where its key belongs."}]}
```

The lookup ends at an empty slot and never reaches the node that holds 25.

#### Finding The Same Fault In One Pass

The same tree is checked once, with the limits carried down. The variable `low` and the variable `high` show the limits at each node.

```trace
{"cells":[20,10,30,5,25],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"low":"none","high":"none"},"note":"The root starts with no limit. The key 20 lies between none and none."},{"at":{"node":1},"vars":{"low":"none","high":20},"note":"Left of 20: the upper bound becomes 20. The key 10 lies between none and 20."},{"at":{"node":3},"vars":{"low":"none","high":10},"note":"Left of 10: the upper bound becomes 10. The key 5 lies between none and 10."},{"at":{"node":4},"vars":{"low":10,"high":20},"note":"Right of 10: the lower bound becomes 10. The key 25 is not between 10 and 20, so the pass reports the fault."}]}
```

At the node 25 the limits are 10 and 20, since the path turned right at 10 and left at 20. The key 25 is not below 20, so the pass reports the fault after four nodes. The slot interval explains the failed lookup: the key 25 belongs to a different slot than the one it occupies.

<!-- stage: code -->
### The Interval Check In Code

```java
final class IntervalTools {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static boolean validInside(TreeNode node, long low, long high) {
        if (node == null) return true;
        if (node.val <= low || node.val >= high) return false;   // outside the slot interval of this position
        return validInside(node.left, low, node.val)             // a left turn tightens the upper bound
            && validInside(node.right, node.val, high);          // a right turn tightens the lower bound
    }

    static int depthOf(TreeNode root, int key) {
        int depth = 1;
        for (TreeNode node = root; node != null; node = key < node.val ? node.left : node.right) {
            if (node.val == key) return depth;                   // the key is found at this depth
            depth++;
        }
        return 0;                                                // the walk reached an empty slot
    }
}
```

The check uses `long` limits so that the extreme `int` keys are legal at the root.

- **Time** is O(n) for the check and O(h) for the depth.
- **Space** is O(h) for the recursion of the check and O(1) for the depth loop.

<!-- stage: applicability -->
### Using Search And Limits Together

#### Recognizing The Cue

Use the combination when a problem asks for a check of the whole tree and a lookup of one key in the same breath, or when an update must keep the tree valid. The words "still a valid search tree after the change" and "legal position for this key" point here.

#### Stating The Invariant

The invariant is that every call knows the slot interval of its node, and the keys that reach the node by lookup are exactly the keys inside that interval. A node passes when its key is in the interval, and a subtree passes when its root passes and both children pass under the narrowed intervals.

#### Avoiding The False Friend

The false friend is the repeated lookup from the root. It tests the right property and replays the same comparisons many times. Another false friend is a rank question. The kth smallest key follows the sorted order of the keys and uses no interval at all, so a bounds check cannot answer it.

<!-- stage: exercises -->
### Exercises

#### [Build] Depth Of A Key In A Search Tree (LeetCode 700)
<!-- id: tbc-key-depth -->

**Prerequisites.** The one-path search and the slot interval from this lesson.

**Problem.** Given the root of a binary search tree and a key, return the depth of the node that holds the key, where the root has depth 1. Return 0 if no node holds the key. Take one branch per comparison.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4, and all keys are distinct.
- **Values** satisfy `-10^9 <= val <= 10^9`, and the key has the same range.
- **Answer** is an `int` between 0 and the node count.
- **Mutation** does not occur.

**Example 1.** Input root 20 with children 10 and 30, where 10 has children 5 and 15 and 30 has children 25 and 40, and key 15, output 3.

**Example 2.** Input the same tree and key 17, output 0.

**Hint.** What does the counter hold when the walk reaches an empty slot? When does it increase?

**Changed decision.** The method returns a depth counter and does not return a node.

#### [Vary] Validate A Subtree Against Outer Limits (LeetCode 98)
<!-- id: tbc-validate-limits -->

**Prerequisites.** The exercise above.

**Problem.** A binary tree and two integers `low` and `high` with `low < high` are supplied. Return `true` if the tree is a valid binary search tree and every key lies strictly between `low` and `high`. The limits describe the interval of the slot where the subtree hangs in a larger tree.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and keys are distinct in a valid tree.
- **Values** and the two limits cover the full `int` range.
- **Answer** is a `boolean`, and an empty tree is valid.
- **Mutation** does not occur.

**Example 1.** Input root 10 with children 5 and 15, `low = 0` and `high = 20`, output `true`.

**Example 2.** Input the same tree, `low = 5` and `high = 20`, output `false`, because the key 5 is not above 5.

**Hint.** What do the outer limits do to the limits of the root? What happens to the limit of a child when the caller's limit is `Integer.MIN_VALUE` or `Integer.MAX_VALUE`?

**Changed decision.** The first call starts with limits from the caller, and not with no limits.

#### [Boundary] Kth Largest Element In A BST (LeetCode 230)
<!-- id: tbc-kth-largest -->

**Prerequisites.** The two exercises above.

**Problem.** Given the root of a binary search tree and an integer `k`, return the kth largest key, where the largest key has rank 1. The answer follows the sorted order of the keys, and no numeric interval helps here.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4, and all keys are distinct.
- **K** satisfies `1 <= k <= n`.
- **Values** satisfy `-10^9 <= val <= 10^9`.
- **Mutation** does not occur.

**Example 1.** Input root 20 with children 10 and 30, where 10 has children 5 and 15 and 30 has children 25 and 40, and `k = 1`, output 40.

**Example 2.** Input the same tree and `k = 3`, output 25.

**Hint.** Which child does the stack walk visit first if the largest key must come first? What does the counter do at each pop?

**Changed decision.** The walk is mirrored, and the answer comes from the order and not from an interval.

#### [Recognize] Delete A Node With Predecessor Replacement (LeetCode 450)
<!-- id: tbc-delete-predecessor -->

**Prerequisites.** All three exercises above.

**Problem.** A binary search tree and a key are supplied. Remove the node with that key and return the new root. A node that lacks a left child gives way to its right child, and a node that lacks a right child gives way to its left child. A node with two children takes the largest key of its left subtree, after which that largest node is removed from the left subtree. An absent key leaves the tree unchanged.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and all keys are distinct.
- **Values** satisfy `-10^5 <= val <= 10^5`.
- **Answer** is the new root, which may be `null`.
- **Mutation** rewires child references.

**Example 1.** Input root 20 with children 10 and 30, where 10 has children 5 and 15 and 30 has children 25 and 40, and key 20, output a tree with the root 15, where 10 keeps only the child 5 on its left, and the right side is unchanged.

**Example 2.** Input the same tree and key 5, output a tree where 10 has only the right child 15.

**Hint.** Which node holds the largest key of the left subtree? How many children can that node have?

**Changed decision.** The predecessor replaces the removed key, and the left subtree gives the new key.
