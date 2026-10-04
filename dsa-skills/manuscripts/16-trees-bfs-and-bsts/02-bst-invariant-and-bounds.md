<!-- lesson-kind: standard -->
<!-- lesson-id: bst-invariant-and-bounds -->
## BST Invariant And Bounds

<!-- stage: context -->
### The Mail Room Inspector

A mail room keeps its parcels on branching shelves. Each shelf holds one parcel with a number on it, and below it two further shelves hang, one to the left and one to the right. The house rule says that every parcel anywhere on the left side below a shelf carries a smaller number than the shelf's own parcel, and every parcel anywhere on the right side carries a larger one, so a clerk can find any number by turning left or right at each shelf.

An inspector visits each Friday and has to declare whether the rule still holds. A new clerk proposes a quick method: at every shelf, look only at the two parcels hanging directly beneath it. The head clerk is uneasy but cannot yet say why the quick method is not enough.

<!-- stage: naive -->
### Compare Each Shelf With Everything Below

The careful method takes the rule literally. For every shelf, the inspector reads every parcel on its whole left side and checks that each number is smaller, then reads every parcel on its whole right side and checks that each is larger. Only if every shelf passes both readings does she sign the form.

```java
static boolean byFullScans(Node shelf) {
    if (shelf == null) return true;
    if (!allBelow(shelf.left, shelf.val) || !allAbove(shelf.right, shelf.val)) return false;
    return byFullScans(shelf.left) && byFullScans(shelf.right);
}

static boolean allBelow(Node n, int limit) {
    if (n == null) return true;
    return n.val < limit && allBelow(n.left, limit) && allBelow(n.right, limit);
}

static boolean allAbove(Node n, int limit) {
    if (n == null) return true;
    return n.val > limit && allAbove(n.left, limit) && allAbove(n.right, limit);
}
```

This follows the rule word for word, so a pass means the rule holds, and a failure points at a real violation.

<!-- stage: bottleneck -->
### Parcels Are Reread By Every Ancestor

A parcel at depth d is read once by each of its d ancestor shelves, since each of them scans its whole side. On a tree that has become a single chain of n shelves, the shelf at the top reads n-1 parcels, the next reads n-2, and the total is about n^2/2, so the time is O(n^2). Thirty thousand shelves already cost over four hundred million reads.

The repeated reading is also redundant. The first ancestor to read a parcel learns that the parcel is below the top shelf's number, and the second ancestor learns something new about the same parcel, but all of it could have been summed up before the parcel was ever reached. Each parcel needs one comparison against a summary of what its ancestors demand, and the summary changes by one number each time we step to a child. That would give O(n) time with no rescans.

<!-- stage: insight -->
### Pass Down The Allowed Interval

Every ancestor of a shelf makes exactly one demand on it: either "smaller than my number" if the shelf is on that ancestor's left, or "larger than my number" if it is on the right. Demands from many ancestors combine into a single **allowed interval** with a lower end and an upper end, because the tightest lower end and the tightest upper end are all that matter. A shelf is acceptable when its number lies strictly inside the interval.

The interval changes in a simple way as the walk steps down. Moving to the left child keeps the lower end and replaces the upper end by the current number. Moving to the right child keeps the upper end and replaces the lower end. These are the **inherited bounds**, handed from parent to child before the child is examined, so no shelf is ever compared with a far ancestor directly. The child's check needs one comparison against two numbers.

The local method of the new clerk fails because it tests the parent number only, which is the tightest bound from one side and ignores the other side's older bound. A parcel deep in the right subtree must still exceed the top shelf, however well it fits its own parent.

The invariant is that when a call starts on a shelf, the interval passed in equals the combined demands of all of its ancestors. A **duplicate policy** must also be stated, and in this lesson equality is illegal, so both ends are exclusive.

<!-- names: allowed interval, inherited bounds, duplicate policy -->

Open ends need a value that no parcel can equal, which is why Java code uses `long` bounds for `int` numbers.

<!-- stage: variables -->
### Low, High And The Strict Test

The variables `lo` and `hi` are `long` values that start at `Long.MIN_VALUE` and `Long.MAX_VALUE`, which no `int` parcel number can equal, so the first shelf always fits. They are not changed inside a call. A call passes `(lo, node.val)` to the left child and `(node.val, hi)` to the right child, so each call owns its own copy. The test `node.val <= lo || node.val >= hi` rejects a number that touches or leaves the interval, which is how strictness shows up. The same interval can be described by `Integer` objects with `null` for an open end, but then comparisons need a null check first.

<!-- stage: trace -->
### Bounds Narrowing Down The Shelves

The first trace follows the valid shelf plan 5, 3, 8, 1, 4, 7, 9 in level order. The pointer `node` marks the shelf under inspection, and the variables `lo` and `hi` show the interval it inherited. Watch the shelf 4: it is the right child of 3, so its lower end becomes 3, but its upper end is still 5 inherited through 3 from the top shelf, which is exactly what a parent-only comparison would never know.

```trace
{"cells":["5","3","8","1","4","7","9"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"lo":"-inf","hi":"+inf"},"note":"The shelf 5 arrives with the interval (-inf, +inf) and fits strictly inside it, so its children get (-inf, 5) and (5, +inf)."},{"at":{"node":1},"vars":{"lo":"-inf","hi":"5"},"note":"The shelf 3 arrives with the interval (-inf, 5) and fits strictly inside it, so its children get (-inf, 3) and (3, 5)."},{"at":{"node":3},"vars":{"lo":"-inf","hi":"3"},"note":"The shelf 1 arrives with the interval (-inf, 3) and fits strictly inside it, so its children get (-inf, 1) and (1, 3)."},{"at":{"node":4},"vars":{"lo":"3","hi":"5"},"note":"The shelf 4 arrives with the interval (3, 5) and fits strictly inside it, so its children get (3, 4) and (4, 5)."},{"at":{"node":2},"vars":{"lo":"5","hi":"+inf"},"note":"The shelf 8 arrives with the interval (5, +inf) and fits strictly inside it, so its children get (5, 8) and (8, +inf)."},{"at":{"node":5},"vars":{"lo":"5","hi":"8"},"note":"The shelf 7 arrives with the interval (5, 8) and fits strictly inside it, so its children get (5, 7) and (7, 8)."},{"at":{"node":6},"vars":{"lo":"8","hi":"+inf"},"note":"The shelf 9 arrives with the interval (8, +inf) and fits strictly inside it, so its children get (8, 9) and (9, +inf)."}]}
```

The second trace uses the plan 10, 5, 15, null, null, 6, 20, where every shelf fits its own parent. The shelf 6 hangs on the left of 15, so it is acceptable next to its parent, yet the right side of the top shelf demands numbers above 10, and 6 is not. The pointer `node` stops moving at that shelf, because the first violated interval ends the whole inspection.

```trace
{"cells":["10","5","15","null","null","6","20"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"lo":"-inf","hi":"+inf"},"note":"The shelf 10 arrives with the interval (-inf, +inf) and fits strictly inside it, so its children get (-inf, 10) and (10, +inf)."},{"at":{"node":1},"vars":{"lo":"-inf","hi":"10"},"note":"The shelf 5 arrives with the interval (-inf, 10) and fits strictly inside it, so its children get (-inf, 5) and (5, 10)."},{"at":{"node":2},"vars":{"lo":"10","hi":"+inf"},"note":"The shelf 15 arrives with the interval (10, +inf) and fits strictly inside it, so its children get (10, 15) and (15, +inf)."},{"at":{"node":5},"vars":{"lo":"10","hi":"15"},"note":"The shelf 6 arrives with the interval (10, 15) and does not fit strictly inside it, so the plan is rejected here."}]}
```

<!-- stage: code -->
### Interval Check In One Pass

```java
final class BoundsCheck {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static boolean isValid(Node root) {
        return within(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private static boolean within(Node node, long lo, long hi) {
        if (node == null) return true;
        if (node.val <= lo || node.val >= hi) return false;
        return within(node.left, lo, node.val) && within(node.right, node.val, hi);
    }
}
```

Each shelf is examined once with two comparisons, so the time is O(n) and the extra space is the recursion depth O(h), which is n for a chain.

<!-- stage: applicability -->
### When Order Is Promised Across Levels

Use bounds whenever a property is stated about everything under a node and not only about its children: a price tree where each category's price range contains its sub-categories, a date index where each branch separates earlier from later entries, or a file index sorted by name. The invariant is that the interval received by a node is the combined demand of all of its ancestors, so one comparison against it settles the node.

The first false friend is the parent-only check, `node.left.val < node.val && node.val < node.right.val` at every node. It accepts the plan 10, 5, 15, null, null, 6, 20 and many other broken trees. A second false friend is the sorted-looking check of a single level, which has no meaning here. A third is treating the rule as true for an unordered tree: bounds can only prove a promise that was made, so on a tree that never promised order they have nothing to check.

In Java, an `int` bound cannot represent "no limit" when the data may hold `Integer.MIN_VALUE` or `Integer.MAX_VALUE`, because a shelf with that number would fail against its own sentinel. Widening to `long`, or using `null` for open ends, keeps every `int` value usable.

<!-- stage: exercises -->
### Exercises

#### [Build] Validate One Root And Children (Author exercise)
<!-- id: tb-root-and-child-intervals -->

**Prerequisites.** The tree representation lesson and the idea of an open-ended interval.

**Problem.** A shelf with number `r` receives an inherited interval, exclusive at both ends, where `lo` or `hi` may be `null` for no limit. Report the interval its left child must respect, the interval its right child must respect, and whether `r` itself fits strictly inside the inherited interval, as `[leftInterval, rightInterval, fits]` with each interval written `[low, high]`.

**Constraints.** `r`, `lo` and `hi` are integers between -1000000 and 1000000, `lo` and `hi` may be null, and strict ordering applies.

**Example 1.** Input `r = 7`, `lo = null`, `hi = 10`, output `[[null, 7], [7, 10], true]`.

**Example 2.** Input `r = 10`, `lo = 5`, `hi = 10`, output `[[5, 10], [10, 10], false]`.

**Hint.** Which end of the inherited interval survives when stepping left, and which one is replaced by `r`?

**Changed decision.** The left child keeps the lower end and takes `r` as its new upper end, while the right child does the reverse, with no scanning below.

#### [Vary] Propagate Ancestor Bounds (Author exercise)
<!-- id: tb-propagate-bounds -->

**Prerequisites.** The Validate One Root And Children rung.

**Problem.** The input is a search tree of distinct integers, stored as a level-order array with `null` for absent children. List, for every present node in level order, the pair `[lo, hi]` of exclusive bounds it inherits from its ancestors, using `null` for an end that no ancestor limits.

**Constraints.** 1 <= values.length <= 500 and the values are distinct integers between -100000 and 100000 forming a valid search tree.

**Example 1.** Input `values = [5, 3, 8, null, 4]`, output `[[null, null], [null, 5], [5, null], [3, 5]]`.

**Example 2.** Input `values = [4, 2, 6, 1, 3, 5, 7]`, output `[[null, null], [null, 4], [4, null], [null, 2], [2, 4], [4, 6], [6, null]]`.

**Hint.** When descending to the right child of 3 inside the left subtree of 5, what must remain from the older step to the left?

**Changed decision.** Instead of testing a node, the walk records the interval it arrives with and hands each child a copy that differs in one end.

#### [Boundary] Integer Extremes And Duplicates (Author exercise)
<!-- id: tb-extremes-and-equality -->

**Prerequisites.** The Propagate Ancestor Bounds rung and the `long` widening idea.

**Problem.** Given a level-order array of `int` values and a flag `equalGoesLeft`, decide whether the tree obeys the ordering where every value in a left subtree is smaller than its ancestor, or equal to it when the flag is true, and every value in a right subtree is strictly larger. Values may be any `int`, including both extremes.

**Constraints.** 0 <= values.length <= 1000, values are any 32-bit signed integers, and the flag is true or false.

**Example 1.** Input `values = [2147483647, 2147483647], equalGoesLeft = true`, output `true`.

**Example 2.** Input `values = [-2147483648, null, -2147483648], equalGoesLeft = true`, output `false`.

**Hint.** What number would a bound need to hold to say "at most this value" without overflowing at the top of the range?

**Changed decision.** Bounds are `long`, and the equal-goes-left policy turns the left upper bound into the node value plus one, an exclusive limit that cannot overflow in `long`.

#### [Recognize] Validate Binary Search Tree (LeetCode 98)
<!-- id: tb-validate-bst -->

**Prerequisites.** The Integer Extremes And Duplicates rung and the inherited interval.

**Problem.** Given the level-order array of a binary tree, decide whether it is a valid binary search tree, meaning that for every node all values in its left subtree are strictly smaller and all values in its right subtree are strictly larger.

**Constraints.** 0 <= values.length <= 10000 and values are integers between -2147483648 and 2147483647.

**Example 1.** Input `values = [5, 1, 4, null, null, 3, 6]`, output `false`.

**Example 2.** Input `values = [10, 5, 15, null, null, 6, 20]`, output `false`.

**Hint.** If every node agrees with its parent but the tree is still invalid, which older ancestor is the node disagreeing with?

**Changed decision.** Both ends of the interval travel down and each node is tested once against them, in place of comparing a node with its immediate children.
