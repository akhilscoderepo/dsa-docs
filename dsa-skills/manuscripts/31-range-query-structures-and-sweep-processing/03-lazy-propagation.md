<!-- lesson-kind: standard -->
<!-- lesson-id: lazy-propagation -->
## Lazy Propagation

<!-- stage: context -->
### Why Range Updates Slow The Tree

A pricing service stores one price per product in a segment tree. Every night a promotion subtracts the same amount from 40,000 consecutive products. All day long, a dashboard asks for the total price of other consecutive ranges.

The segment tree from the previous lesson answers a range sum in O(log n). It also changes one position in O(log n). The nightly promotion is not a single position, though. It is a range update, where one call changes every position between two indexes by the same amount. The tree has no operation for that. The service needs one call that changes 40,000 prices and still leaves every later sum query correct and fast.

<!-- stage: naive -->
### Update Every Position One At A Time

This lesson writes ranges as half-open `[lo, hi)`, which includes `lo` and excludes `hi`, where the previous lesson used inclusive ranges. The direct approach reuses the point update. For each position in the range, it descends from the root to that leaf, adds the amount and recomputes the sums on the way back up.

```java
// tree[k] holds the sum of positions [lo, hi) for node k; node 1 is the root.
static void pointAdd(long[] tree, int k, int lo, int hi, int pos, long delta) {
    tree[k] += delta;                          // every node on the path to pos gains delta
    if (hi - lo == 1) return;                  // a leaf has no children to visit
    int mid = (lo + hi) >>> 1;
    if (pos < mid) pointAdd(tree, 2 * k, lo, mid, pos, delta);
    else pointAdd(tree, 2 * k + 1, mid, hi, pos, delta);
}

static void rangeAddByPoints(long[] tree, int n, int l, int r, long delta) {
    for (int pos = l; pos < r; pos++) {        // one full descent per changed position
        pointAdd(tree, 1, 0, n, pos, delta);
    }
}
```

Each descent visits one node per level. A range of `k` positions therefore costs `k` descents. The sums stay correct after every call, but the cost grows with the length of the range.

<!-- stage: bottleneck -->
### One Descent Per Position Costs Too Much

```predict
A segment tree covers 131,072 positions. One update adds 1 to every position. Roughly how many nodes does the one-position-at-a-time update visit?

About 2.4 million node visits for a single update. Each of the 131,072 descents visits 18 nodes. A method that stops at the root, which already covers the whole range, needs far fewer visits.
```

#### Count The Visits

The tree with 131,072 leaves has 18 levels. One descent visits 18 nodes, so the full-range update makes 131,072 times 18 visits, which is about 2.36 million. A workload of 100,000 such updates costs about 2.4 times 10^11 visits. The range update costs O(k log n) for a range of length `k`, which is O(n log n) in the worst case. A sum query still costs only O(log n), so the updates dominate everything.

#### See Why Skipped Children Are Wrong

A range query already avoids visiting every leaf. It stops at nodes whose range lies entirely inside the query range and reads their stored sums. A range update can stop at the same nodes. A node that covers positions `lo` to `hi` and lies inside the update range gains `delta * (hi - lo)` in its own sum, and the update stops there. At most about 2 log n nodes qualify, so the visit count drops to O(log n).

That shortcut leaves a problem. The children of a covered node still hold their old sums. A later query that descends below that node reads those old numbers and returns a wrong total. The structure must remember the skipped work and apply it when a query or update needs the children.

<!-- stage: insight -->
### Remember The Update On The Node

#### Store The Update As A Lazy Tag

The fix keeps a second number at each node, called the **lazy tag**. The tag stores the amount that every position under the node has gained but that the node's children do not know about yet. A covered node updates its own sum immediately and adds `delta` to its tag. It leaves the children alone.

The invariant is that a lazy tag records an update already applied to the node's sum but not yet pushed to the children. A node's stored sum is correct exactly when no ancestor holds a pending tag. A query or update that enters a node therefore clears the tags above it first.

<!-- names: lazy tag, push down, tag composition -->

#### Push Down Before You Descend

Any operation that must look inside a node first performs a **push down**. The push down moves the node's tag to both children in one step. Each child adds `tag * childLength` to its sum and adds `tag` to its own tag. The node then sets its tag to 0, so the update is passed along exactly once.

After the push down, both children hold correct sums, and the descent can continue safely. Updates and queries both push before they recurse. A fully covered node never needs a push, because it uses only its own sum. This is why every operation still visits only O(log n) nodes.

#### Combine Tags In The Right Order

Addition tags combine by adding the amounts, because adding 3 and then 4 equals adding 7 in either order. A different kind of update shows why the combination rule needs care. Suppose an update sets every position to a value `v`, and a node already holds a pending tag. The **tag composition** rule decides the result. A new assignment replaces whatever tag exists, because the old values no longer matter. A new addition applied after an assignment of `v` changes the assignment to `v + delta`. Reversing the order gives a different answer, so the order of composition is part of the data structure's contract. For example, a node of length 4 with sum 10 receives `add 3` and then `set 5`. The tag becomes `set 5`, and the sum becomes 20. In the opposite order, `set 5` and then `add 3` give the tag `set 8` and the sum 32.

<!-- stage: variables -->
### Quantities Stored At Each Node

The lazy tree keeps two arrays indexed by node number, with node 1 as the root.

- **sum[k]** holds the total of the positions under node `k`, including every tag already applied at `k`.
- **add[k]** holds the pending amount per position that node `k` has not passed to its children. This pending amount is the lazy tag.
- **lo and hi** describe the half-open range `[lo, hi)` of positions that node `k` covers. The range includes `lo` and excludes `hi`, so its length `hi - lo` scales an amount into a change of the sum.

This lesson uses half-open ranges where the previous lesson used inclusive ones, because the length `hi - lo` then needs no `+ 1`. Both arrays hold `long` values, because a delta times a length easily exceeds the `int` range. Each array needs `4 * n` slots to hold every node safely.

<!-- stage: trace -->
### Add To A Range, Then Query It

The array is 3, 1, 4, 1, 5, 9, 2, 6. The tree has node 1 as the root over `[0, 8)`. The pointers `lo` and `hi` mark the range of the node being visited.

#### Add 5 To Positions 2 Through 6

The update covers `[2, 7)`. The root and the nodes over `[0, 4)` and `[4, 8)` overlap it only in part, so each descends. Node 5 covers `[2, 4)` and lies fully inside. Its sum grows from 5 to 15, and its tag becomes 5. Node 6 covers `[4, 6)` and does the same, and its sum grows from 14 to 24.

The range `[6, 8)` is again partial. Its left child covers only position 6, and that single leaf gains 5. After the recursion returns, each ancestor recomputes its sum from its children. The root ends with 56, which is the old total 31 plus 5 times 5 positions.

The hardest step is the stop at node 5. Positions 2 and 3 now hold 9 and 6 in truth, but the leaves under node 5 still hold 4 and 1.

```trace
{"cells":[3,1,4,1,5,9,2,6],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":8},"vars":{"node":1,"sum":31,"add":0,"pushes":0},"note":"Node 1 covers [0, 8) and overlaps [2, 7) only in part, so the update descends. Its tag is 0, so nothing needs pushing."},{"at":{"lo":0,"hi":4},"vars":{"node":2,"sum":9,"add":0,"pushes":0},"note":"Node 2 covers [0, 4) and overlaps [2, 7) only in part, so the update descends. Its tag is 0, so nothing needs pushing."},{"at":{"lo":0,"hi":2},"vars":{"node":4,"sum":4,"add":0,"pushes":0},"note":"Node 4 covers [0, 2) and lies outside [2, 7), so the update skips it."},{"at":{"lo":2,"hi":4},"vars":{"node":5,"sum":15,"add":5,"pushes":0},"note":"Node 5 covers [2, 4) and lies inside [2, 7). Its sum grows by 5 times 2, and its tag becomes 5. The children stay unchanged."},{"at":{"lo":0,"hi":4},"vars":{"node":2,"sum":19,"add":0,"pushes":0},"note":"Node 2 recomputes its sum from its children as 19."},{"at":{"lo":4,"hi":8},"vars":{"node":3,"sum":22,"add":0,"pushes":0},"note":"Node 3 covers [4, 8) and overlaps [2, 7) only in part, so the update descends. Its tag is 0, so nothing needs pushing."},{"at":{"lo":4,"hi":6},"vars":{"node":6,"sum":24,"add":5,"pushes":0},"note":"Node 6 covers [4, 6) and lies inside [2, 7). Its sum grows by 5 times 2, and its tag becomes 5. The children stay unchanged."},{"at":{"lo":6,"hi":8},"vars":{"node":7,"sum":8,"add":0,"pushes":0},"note":"Node 7 covers [6, 8) and overlaps [2, 7) only in part, so the update descends. Its tag is 0, so nothing needs pushing."},{"at":{"lo":6,"hi":7},"vars":{"node":14,"sum":7,"add":5,"pushes":0},"note":"Node 14 covers [6, 7) and lies inside [2, 7). Its sum grows by 5 times 1, and its tag becomes 5. The children stay unchanged."},{"at":{"lo":7,"hi":8},"vars":{"node":15,"sum":6,"add":0,"pushes":0},"note":"Node 15 covers [7, 8) and lies outside [2, 7), so the update skips it."},{"at":{"lo":6,"hi":8},"vars":{"node":7,"sum":13,"add":0,"pushes":0},"note":"Node 7 recomputes its sum from its children as 13."},{"at":{"lo":4,"hi":8},"vars":{"node":3,"sum":37,"add":0,"pushes":0},"note":"Node 3 recomputes its sum from its children as 37."},{"at":{"lo":0,"hi":8},"vars":{"node":1,"sum":56,"add":0,"pushes":0},"note":"Node 1 recomputes its sum from its children as 56."}]}
```

#### Query The Sum Of Positions 3 To 5

The query covers `[3, 6)`. The descent reaches node 5 over `[2, 4)`, and this node overlaps the query in part, so it must look at its children. Node 5 holds the tag 5, so it pushes first. Its left child, covering position 2, becomes 9. Its right child, covering position 3, becomes 6.

The query takes the 6 from position 3. Node 6 covers `[4, 6)` and lies fully inside, so it contributes its stored sum 24 without any push. The total is 30, which equals 6 plus 10 plus 14 in the updated array.

```trace
{"cells":[3,1,4,1,5,9,2,6],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":8},"vars":{"node":1,"sum":56,"add":0,"pushes":0},"note":"Node 1 covers [0, 8) and overlaps [3, 6) only in part, so the query descends. Its tag is 0, so nothing needs pushing."},{"at":{"lo":0,"hi":4},"vars":{"node":2,"sum":19,"add":0,"pushes":0},"note":"Node 2 covers [0, 4) and overlaps [3, 6) only in part, so the query descends. Its tag is 0, so nothing needs pushing."},{"at":{"lo":0,"hi":2},"vars":{"node":4,"sum":4,"add":0,"pushes":0,"result":0},"note":"Node 4 covers [0, 2) and lies outside [3, 6), so it contributes 0."},{"at":{"lo":2,"hi":4},"vars":{"node":5,"sum":15,"add":0,"pushes":1},"note":"Node 5 covers [2, 4) and overlaps [3, 6) only in part, so the query descends. It pushes its tag first, so both children hold correct sums."},{"at":{"lo":2,"hi":3},"vars":{"node":10,"sum":9,"add":5,"pushes":1,"result":0},"note":"Node 10 covers [2, 3) and lies outside [3, 6), so it contributes 0."},{"at":{"lo":3,"hi":4},"vars":{"node":11,"sum":6,"add":5,"pushes":1,"result":6},"note":"Node 11 covers [3, 4) and lies inside [3, 6), so it contributes its sum 6. Its own tag has been applied to that sum already."},{"at":{"lo":4,"hi":8},"vars":{"node":3,"sum":37,"add":0,"pushes":1},"note":"Node 3 covers [4, 8) and overlaps [3, 6) only in part, so the query descends. Its tag is 0, so nothing needs pushing."},{"at":{"lo":4,"hi":6},"vars":{"node":6,"sum":24,"add":5,"pushes":1,"result":24},"note":"Node 6 covers [4, 6) and lies inside [3, 6), so it contributes its sum 24. Its own tag has been applied to that sum already."},{"at":{"lo":6,"hi":8},"vars":{"node":7,"sum":13,"add":0,"pushes":1,"result":0},"note":"Node 7 covers [6, 8) and lies outside [3, 6), so it contributes 0."},{"at":{"lo":3,"hi":6},"vars":{"result":30,"pushes":1},"note":"The two fully covered nodes, leaf 11 with 6 and node 6 with 24, add up to 30, which equals the sum of positions 3, 4 and 5 of the updated array."}]}
```

<!-- stage: code -->
### Implement The Lazy Sum Tree

```java
final class LazySumTree {
    private final int n;
    private final long[] sum;   // sum[k]: total of node k's range, with its own tag applied
    private final long[] add;   // add[k]: amount per position not yet passed to the children

    LazySumTree(int[] a) {
        n = a.length;
        sum = new long[4 * n];
        add = new long[4 * n];
        build(1, 0, n, a);
    }

    private void build(int k, int lo, int hi, int[] a) {
        if (hi - lo == 1) { sum[k] = a[lo]; return; }
        int mid = (lo + hi) >>> 1;
        build(2 * k, lo, mid, a);
        build(2 * k + 1, mid, hi, a);
        sum[k] = sum[2 * k] + sum[2 * k + 1];
    }

    private void applyTag(int k, int lo, int hi, long delta) {
        sum[k] += delta * (hi - lo);      // the sum changes by the amount times the length
        add[k] += delta;                  // the children learn about it only at push time
    }

    private void pushDown(int k, int lo, int hi) {
        if (add[k] == 0) return;          // nothing is pending, so the children are current
        int mid = (lo + hi) >>> 1;
        applyTag(2 * k, lo, mid, add[k]);
        applyTag(2 * k + 1, mid, hi, add[k]);
        add[k] = 0;                       // the pending amount is passed along exactly once
    }

    void rangeAdd(int l, int r, long delta) { rangeAdd(1, 0, n, l, r, delta); }

    private void rangeAdd(int k, int lo, int hi, int l, int r, long delta) {
        if (r <= lo || hi <= l) return;                        // no overlap
        if (l <= lo && hi <= r) { applyTag(k, lo, hi, delta); return; }  // full cover
        pushDown(k, lo, hi);                                   // partial overlap: children must be current
        int mid = (lo + hi) >>> 1;
        rangeAdd(2 * k, lo, mid, l, r, delta);
        rangeAdd(2 * k + 1, mid, hi, l, r, delta);
        sum[k] = sum[2 * k] + sum[2 * k + 1];                  // recompute from the updated children
    }

    long rangeSum(int l, int r) { return rangeSum(1, 0, n, l, r); }

    private long rangeSum(int k, int lo, int hi, int l, int r) {
        if (r <= lo || hi <= l) return 0;
        if (l <= lo && hi <= r) return sum[k];
        pushDown(k, lo, hi);
        int mid = (lo + hi) >>> 1;
        return rangeSum(2 * k, lo, mid, l, r) + rangeSum(2 * k + 1, mid, hi, l, r);
    }
}
```

The two public methods take half-open ranges `[l, r)` with zero-based positions. Both operations share the same three cases: no overlap, full cover and partial overlap. Only the partial case descends, and it pushes first. Both methods run in O(log n) time on a tree built in O(n).

<!-- stage: applicability -->
### When Lazy Propagation Applies

#### Recognize The Pattern

Use lazy propagation when updates affect whole ranges and queries ask for range aggregates, with both mixed in any order. Immediate descent to every leaf would cost too much. The recognition cue is a range update and a range query on the same array.

The state invariant is that each tag is already part of its node's sum and is not yet part of its children's sums. Every operation that descends below a node must push that node's tag first. Forgetting one push breaks the invariant silently, and the first symptom is a wrong sum much later.

#### Reject The False Friends

A difference array supports range addition in O(1), but it answers a range sum only after a rebuild. It is a false friend when updates and queries interleave. A plain segment tree is another false friend, because it handles point updates only.

Lazy tags also require that an update can be applied to a node's aggregate from the node's length alone. Addition to a sum has that property. Adding to a maximum needs no length at all. Some aggregates have no such formula and cannot use a tag.

#### Watch The Java Hazards

Multiply a delta by the range length in `long`. An `int` product of 10^9 and 10^5 overflows silently. Size the arrays at `4 * n`, because a tree over a length that is not a power of two can need nodes beyond `2 * n`. Keep the half-open convention in every comparison. A mix of inclusive and half-open bounds produces off-by-one errors that tests with small ranges often miss.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Add One Node (Author exercise)
<!-- id: rq31-range-add-one-node -->

**Prerequisites.** The `sum` and `add` arrays from this lesson.

**Problem.** A single tree node covers `len` positions and holds a sum `S` of those positions. Its pending tag starts at 0. Apply a sequence of deltas to the whole node, in order. Applying delta `d` adds `d * len` to the node's sum and adds `d` to its pending tag. Return the final sum and the final pending tag.

**Constraints.** The limits are:
- **`len`** is an `int` with `1 <= len <= 10^5`.
- **`S`** is a `long` with absolute value at most `10^15`.
- **Deltas** are `long` values with absolute value at most `10^9`, and the list has at most `10^3` entries.
- **Empty list** returns `S` and a tag of 0.

**Example 1.** Input `len = 4`, `S = 10`, deltas 3, -1, 2. Output sum 26 and tag 4.

**Example 2.** Input `len = 100000`, `S = 0`, deltas 10^9, 10^9, 10^9. Output sum 300000000000000 and tag 3000000000, so both values exceed the `int` range.

**Hint.** Does the sum change by the delta or by the delta times the length? Which type holds the tag?

**Changed decision.** Baseline case: one node absorbs an update by length and stores the remainder as a pending amount.

#### [Vary] Push Before Descent (Author exercise)
<!-- id: rq31-push-before-descent -->

**Prerequisites.** The previous exercise.

**Problem.** A parent node has a left child covering `a` positions and a right child covering `b` positions. Each of the three nodes has a stored sum and a pending tag, and the parent's sum already includes the parent's tag. Perform one push down from the parent. Each child adds `tag * childLength` to its sum and adds `tag` to its own tag, and the parent's tag becomes 0. Return the parent tag, then the sum and tag of the left child, then the sum and tag of the right child. A second push down must change nothing.

**Constraints.** The limits are:
- **`a` and `b`** are `int` values with `1 <= a, b <= 10^5`.
- **Sums and tags** are `long` values with absolute value at most `10^12`.
- **Parent tag** may be 0, positive or negative.
- **Return value** is the five numbers in the order stated above.

**Example 1.** Input `a = 2`, `b = 3`, parent tag 4, left sum 10 and tag 1, right sum 30 and tag 0. Output parent tag 0, left sum 18 and tag 5, right sum 42 and tag 4.

**Example 2.** Input `a = 1`, `b = 4`, parent tag -3, left sum 5 and tag 0, right sum -2 and tag 2. Output parent tag 0, left sum 2 and tag -3, right sum -14 and tag -1.

**Hint.** Does the push scale the tag by the length of the parent or by the length of each child? What happens on a second call?

**Changed decision.** The tag moves from the parent to two children, and the code must hand it over exactly once.

#### [Boundary] Assignment Versus Addition Tags (Author exercise)
<!-- id: rq31-assignment-versus-addition -->

**Prerequisites.** The two exercises above.

**Problem.** A node covers `len` positions with current sum `S` and no tag. A tag is empty, an addition of `d` or an assignment of `v`. Apply a list of whole-node operations in order, each either `add d` or `set v`. Compose each new operation with the existing tag: a `set v` replaces any tag, an `add d` on an empty or addition tag adds the amounts, and an `add d` on an assignment of `v` gives an assignment of `v + d`. Then push the final tag to a child of length `c` whose stored sum is `sc`. Return the node's final sum, the final tag and the child's new sum.

**Constraints.** The limits are:
- **`len` and `c`** are `int` values with `1 <= c <= len <= 10^5`.
- **`S` and `sc`** are `long` values with absolute value at most `10^12`.
- **Operations** number at most `10^3`, with amounts of absolute value at most `10^9`.
- **Tag output** is `none`, `add d` or `set v`.

**Example 1.** Input `len = 4`, `S = 10`, operations add 3, set 5, add 2, child `c = 2`, `sc = 6`. Output sum 28, tag `set 7` and child sum 14.

**Example 2.** Input the same sizes with operations add 2, set 5, and then with set 5, add 2. The first order outputs tag `set 5`, node sum 20 and child sum 10. The second order outputs tag `set 7`, node sum 28 and child sum 14.

**Hint.** Does the old sum of the child matter after an assignment? Which operation wins when both are pending?

**Changed decision.** The tag has two kinds, and the order in which they compose changes the answer.

#### [Recognize] Range Add Range Sum (Author exercise)
<!-- id: rq31-range-add-range-sum -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `a` of length `n`, process a list of operations in order. Operation `(1, l, r, d)` adds `d` to every `a[i]` with `l <= i < r`. Operation `(2, l, r)` asks for the sum of `a[i]` with `l <= i < r`. Return the answers to the sum operations in the order they appear.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 10^5`, and `a[i]` is an `int` with absolute value at most `10^9`.
- **Operations** number at most `10^5`, and each range satisfies `0 <= l < r <= n`.
- **Added value `d`** is an `int` with absolute value at most `10^4`.
- **Answers** are `long` values.

**Example 1.** Input `a = [3, 1, 4, 1, 5]` and operations: sum `[0, 5)`, add 10 on `[1, 4)`, sum `[0, 3)`, add -2 on `[0, 5)`, sum `[2, 5)`, sum `[3, 4)`. Output 14, 28, 24, 9.

**Example 2.** Input `a = [7]` and operations: add -10000 on `[0, 1)`, sum `[0, 1)`, add 10000 on `[0, 1)`, sum `[0, 1)`. Output -9993, 7.

**Hint.** Which operation needs the children to be current? What do you do with a node that lies entirely inside the range?

**Changed decision.** The earlier pieces combine into one structure that supports both operations in O(log n).
