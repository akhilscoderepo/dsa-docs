<!-- lesson-kind: standard -->
<!-- lesson-id: balance-sentinels -->
## Balance Sentinels

<!-- stage: context -->
### The Mobile Inspector

An art studio hangs mobiles from its ceiling. Each mobile is a rod with a hanging part on each end, and each hanging part is either a small weight or another rod with two hanging parts of its own. A mobile is called steady when, at every rod, the two hanging parts reach down by amounts that differ by no more than one level. A mobile that fails this at any single rod swings badly, and the studio will not display it.

The inspector must check hundreds of mobiles, some of them very tall and thin. For each she writes only steady or not steady, though measuring the reach of a part is the natural way to decide. She is looking for a way of working where a bad rod found low down is not forgotten, and where she does not keep re-measuring parts she has already measured.

<!-- stage: naive -->
### Measure Each Rod From Scratch

The direct method checks one rod at a time. For a rod she measures how far its left part reaches and how far its right part reaches, compares the two numbers, and then repeats the same check on both parts, each of which again measures its own two parts from scratch.

```java
static int reach(Node rod) {
    if (rod == null) return 0;
    return 1 + Math.max(reach(rod.left), reach(rod.right));
}

static boolean steady(Node rod) {
    if (rod == null) return true;
    if (Math.abs(reach(rod.left) - reach(rod.right)) > 1) return false;
    return steady(rod.left) && steady(rod.right);
}
```

A mobile is steady exactly when every rod passes the level test, so the check visits every rod and tests it.

<!-- stage: bottleneck -->
### Every Rod Measures Everything Below It

The reach helper walks the whole hanging part each time it is called, and it is called at every rod that gets checked. A rod is therefore measured once by every rod above it. In a steady mobile the reaches differ by at most one at every rod, which keeps the height close to log n, so each rod is measured by about log n rods above it and the total is O(n log n) steps instead of O(n). A million rods would cost around twenty million steps in place of one million, and every one of those measurements repeats work that the descent has already done.

A second waste is that the measuring happens on the way down, before anything is known about the parts. A failure low down is found only after the rods above it have each paid for their own measuring, and the answer is decided by the first failure alone. A report that carries both the reach and a failure mark would let each rod use the numbers its parts have already produced, in one pass of O(n), and would pass a failure straight up without any more measuring.

<!-- stage: insight -->
### One Number Can Carry Two Meanings

Let the walk return a single integer that is either a real height or a **failure sentinel**. A height is never negative, so the value -1 can safely mean failed. The call on a rod first asks both of its parts. If either returns the failure sentinel, the rod returns the sentinel at once without comparing anything, which is the **early exit**: the failure travels upward untouched, and no rod above it measures again. Only when both parts return a **valid height** does the rod compare them, and if they differ by more than one it returns the sentinel, and otherwise it returns one plus the larger.

The order of the steps matters. The comparison happens after both calls are finished and only with valid numbers, because a sentinel treated as a height would produce a difference that means nothing. A null part returns 0, which is a valid height and consistent with the rule that a leaf has height 1 and sits next to an empty side with a difference of exactly 1.

The invariant is that every call returns either the true height of its subtree, when the whole subtree is steady, or the sentinel, and it returns the sentinel only when some rod inside is out of balance. Each rod is visited once with O(1) work, so the total is O(n), with a stack of the tree height.

<!-- names: failure sentinel, early exit, valid height -->

The sentinel must lie outside the set of valid heights, or a good result will be mistaken for a failure.

<!-- stage: variables -->
### Height, Sentinel And Comparison

Each call has two child results, `l` and `r`. The constant -1 plays the part of the sentinel, and the helper's contract is written beside it: a non-negative number is a height of a steady subtree, and -1 is failure. A null child returns 0. The comparison `Math.abs(l - r) > 1` is made only after the two tests `l == -1` and `r == -1` have both been answered. The public method turns the helper into a boolean by checking that the final result is not -1.

<!-- stage: trace -->
### A Failure Rides Up Untouched

The first trace checks the mobile 3, 9, 20, null, null, 15, 7 in level-order form. The pointer `node` marks the rod that has just received both reports. Every rod here is steady, so each report is a real height: the three small weights report 1, the rod 20 compares two equal reaches and reports 2, and the top rod compares 1 with 2, a difference of one, and reports 3.

```trace
{"cells":["3","9","20","null","null","15","7"],"pointers":["node"],"steps":[{"at":{"node":1},"vars":{"returns":1},"note":"The rod 9 has reaches 0 and 0, a difference within one, so it reports the height 1."},{"at":{"node":5},"vars":{"returns":1},"note":"The rod 15 has reaches 0 and 0, a difference within one, so it reports the height 1."},{"at":{"node":6},"vars":{"returns":1},"note":"The rod 7 has reaches 0 and 0, a difference within one, so it reports the height 1."},{"at":{"node":2},"vars":{"returns":2},"note":"The rod 20 has reaches 1 and 1, a difference within one, so it reports the height 2."},{"at":{"node":0},"vars":{"returns":3},"note":"The rod 3 has reaches 1 and 2, a difference within one, so it reports the height 3."}]}
```

The second trace uses the mobile 1, 2, 3, 4, null, null, null, 5, where the left side is a thin chain. The rod 2 has a reach of 2 on one side and nothing on the other, which is a difference of two, so it reports the failure value. Look at the top rod. One of its reports is already the failure value, so it returns failure without comparing and without looking at the lighter right side again.

```trace
{"cells":["1","2","3","4","null","null","null","5"],"pointers":["node"],"steps":[{"at":{"node":7},"vars":{"returns":1},"note":"The rod 5 has reaches 0 and 0, a difference within one, so it reports the height 1."},{"at":{"node":3},"vars":{"returns":2},"note":"The rod 4 has reaches 1 and 0, a difference within one, so it reports the height 2."},{"at":{"node":1},"vars":{"returns":-1},"note":"The rod 2 has reaches 2 and 0, which differ by more than one, so it reports failure."},{"at":{"node":0},"vars":{"returns":-1},"note":"The left report of the rod 1 is the failure value, so it returns failure at once without asking the right side."}]}
```

<!-- stage: code -->
### Height Or Failure In One Pass

```java
final class BalanceCheck {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static final int FAILED = -1;

    static int heightOrFailed(Node node) {
        if (node == null) return 0;
        int l = heightOrFailed(node.left);
        if (l == FAILED) return FAILED;
        int r = heightOrFailed(node.right);
        if (r == FAILED) return FAILED;
        if (Math.abs(l - r) > 1) return FAILED;
        return 1 + Math.max(l, r);
    }

    static boolean isBalanced(Node root) {
        return heightOrFailed(root) != FAILED;
    }
}
```

Each node is entered at most once with constant work, so the time is O(n) and the stack is O(h). Returning early on the left failure even skips the right subtree entirely.

<!-- stage: applicability -->
### When A Helper Reports Success Or Failure

Use a sentinel when a recursive helper normally returns a number but a failure anywhere below must cancel the whole answer: balance checks, validity tests that also need a size, and measurements that stop at the first bad input. The invariant is that the value is either the true result for a fully good subtree or the one distinguished failure value, and a failure is passed up unchanged.

A false friend is calling a separate height function at every node, which gives the right answer but repeats every measurement, so a steady tree costs an extra factor of its height. A second false friend is a sentinel that overlaps real results: with the edge-count convention, where an empty tree has height -1, the value -1 is a valid height and cannot also mean failure. A third is comparing before checking the failure value, which produces nonsense differences.

In Java, a sentinel such as `Integer.MIN_VALUE` is dangerous inside `Math.abs`, because the absolute value of the smallest int is still negative. Prefer a small negative constant that is outside the valid range and check it before doing any arithmetic.

<!-- stage: exercises -->
### Exercises

#### [Build] Height Or Failure (Author exercise)
<!-- id: tr-height-or-failure -->

**Prerequisites.** The Diameter And Subtree Returns lesson and its return values.

**Problem.** Given a level-order tree, return its height in nodes if at every node the two child heights differ by at most one, and return -1 otherwise. The empty tree has height 0. If a child has already failed, return -1 at once.

**Constraints.** 0 <= values.length <= 5000 and values are integers between 0 and 1000.

**Example 1.** Input `values = [3, 9, 20, null, null, 15, 7]`, output `3`.

**Example 2.** Input `values = [1, 2, null, 3]`, output `-1`.

**Hint.** Which return value can never be a real height, and when is the comparison allowed?

**Changed decision.** The helper's return value doubles as a failure signal, and a failed child ends the call before any comparison is made.

#### [Vary] Detect Local Imbalance (Author exercise)
<!-- id: tr-local-imbalance -->

**Prerequisites.** The Height Or Failure rung and its comparison order.

**Problem.** For a level-order tree, return the label of the first node, in postorder, whose left and right heights differ by more than one, or -1 when there is none. Compare the heights only after both sides are known to be valid.

**Constraints.** 0 <= values.length <= 5000 and values are integers between 0 and 1000.

**Example 1.** Input `values = [1, 2, null, 3]`, output `1`.

**Example 2.** Input `values = [1, 2, 3, 4, null, null, null, 5]`, output `2`.

**Hint.** Once one node has been reported, what should every node above it do?

**Changed decision.** The helper records the culprit the first time a comparison fails and then lets the failure value carry the rest of the walk.

#### [Boundary] Empty Tree Height (Author exercise)
<!-- id: tr-empty-tree-height -->

**Prerequisites.** The Detect Local Imbalance rung and the sentinel rule.

**Problem.** Measure height in edges, so the empty tree has height -1 and a single node has height 0. Return the edge height when the tree is balanced, and -2 when it is not. The sentinel must differ from every valid height, including the height of an empty subtree.

**Constraints.** 0 <= values.length <= 5000 and values are integers between 0 and 1000.

**Example 1.** Input `values = []`, output `-1`.

**Example 2.** Input `values = [1, 2, null, 3]`, output `-2`.

**Hint.** What does a null subtree return, and which value must therefore be kept free?

**Changed decision.** The base height moves from 0 to -1, so the failure value moves to -2 to stay outside the set of valid results.

#### [Recognize] Balanced Binary Tree (LeetCode 110)
<!-- id: tr-balanced-tree -->

**Prerequisites.** The Empty Tree Height rung and the one-pass helper.

**Problem.** For a level-order tree, return whether it is height-balanced, meaning that at every node the heights of the two subtrees differ by at most one.

**Constraints.** 0 <= values.length <= 5000 and values are integers between -1000 and 1000.

**Example 1.** Input `values = [2, 1, 3, 0, 7]`, output `true`.

**Example 2.** Input `values = [1, null, 2, null, 3]`, output `false`.

**Hint.** Can one pass produce the height and the verdict together?

**Changed decision.** Detection and measurement are merged into one postorder pass, so no node asks for a height that was already computed.
