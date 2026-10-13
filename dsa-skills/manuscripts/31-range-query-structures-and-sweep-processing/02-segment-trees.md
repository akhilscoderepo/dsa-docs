<!-- lesson-kind: standard -->
<!-- lesson-id: segment-trees -->
## Segment Trees

<!-- stage: context -->
### Why Minimum Queries Break Prefix Sums

A monitoring service keeps one response time per request in an array. Operators ask for the lowest response time between request `l` and request `r`. Between questions, a late measurement overwrites one stored value, and the next question must see it.

The Fenwick tree from the previous lesson answers a range sum as the difference of two prefix sums. That subtraction works because addition has an inverse. Minimum has no inverse. Knowing the lowest value of the first seven requests and of the first four requests does not reveal the lowest value of requests 4 to 6. A structure for range minimum with updates needs a different design.

<!-- stage: naive -->
### Scanning The Range On Every Query

The direct approach keeps the plain array. An update overwrites one cell, and a query scans every cell from `l` to `r`.

```java
static long rangeMin(long[] a, int l, int r) {
    long best = Long.MAX_VALUE;        // larger than every stored value
    for (int i = l; i <= r; i++) {
        best = Math.min(best, a[i]);   // one comparison per scanned cell
    }
    return best;
}

static void overwrite(long[] a, int pos, long value) {
    a[pos] = value;                    // the update itself costs one write
}
```

Each update is cheap and each query is correct. The query cost grows with the length of the range, so a query over the whole array reads every cell.

<!-- stage: bottleneck -->
### Every Query Pays For The Full Range

```predict
The array holds 100,000 response times, and 100,000 queries each ask about a range of about 50,000 requests. Roughly how many cell reads happen, and what would a stored summary have to provide to avoid them?

About five billion cell reads, because each query reads half the array. To avoid them, the structure must keep minima of many ranges in advance, so a query combines a few stored minima and never reads the cells one by one.
```

#### Count The Cell Reads

A query over `k` cells costs O(k), so `q` queries over ranges of length up to `n` cost O(n * q) in total. With `n = q = 100,000`, the worst case is 10^10 reads. The update costs O(1), so the scan is balanced in the wrong place. All the cost sits in the queries, and queries are the common operation.

#### Rule Out Prefix Subtraction

Storing the minimum of every prefix does not help. When one value changes, many prefix minima change with it, so an update becomes O(n). Subtracting two prefix minima also fails. In the array `[5, 2, 7, 1, 4, 3, 6, 8]`, the first seven cells and the first four cells both have minimum 1. The range from position 4 to 6 has minimum 3. The structure needs stored answers for ranges that are not prefixes.

<!-- stage: insight -->
### Store One Aggregate Per Node Range

#### Split The Array Into Halves

A **segment tree** is a binary tree in which each node owns one **node range** of positions. The root owns positions 0 to `n - 1`. A node that owns positions `lo` to `hi` splits at `mid`, which is `(lo + hi) / 2`. Its left child owns `lo` to `mid`, and its right child owns `mid + 1` to `hi`. A leaf owns one position. Every node stores the aggregate of its node range, which is the minimum or the sum of the values at those positions.

The aggregate of a parent comes from its children alone. For a minimum, the parent stores the smaller of the two child values. For a sum, it stores their total. This works for any operator that is associative, meaning the grouping of three values does not change the result. Subtraction is never needed.

#### Answer A Query From Few Nodes

A query for positions `l` to `r` starts at the root and compares the node range with the query. Three cases cover everything. If the two ranges do not overlap, the node contributes the **identity element**, a value that leaves any result unchanged. That value is `Long.MAX_VALUE` for a minimum and 0 for a sum. If the node range lies fully inside the query, the node returns its stored aggregate without looking at its children. If the ranges partly overlap, the query recurses into both children and combines their answers.

<!-- names: segment tree, node range, identity element -->

At each depth, at most two nodes partly overlap the query. Every other visited node is a no-overlap or full-cover stop. A query therefore visits O(log n) nodes, since the tree has about log n levels.

#### Update By Recomputing Ancestors

A point assignment walks from the root to the leaf that owns the position. It writes the new value into the leaf. On the way back up, each ancestor recomputes its aggregate from its two children. Only the nodes on that one path change, so an update touches O(log n) nodes.

The invariant is that every node always stores the aggregate of exactly its node range. Build, query and update each preserve it, and the query depends on it.

<!-- stage: variables -->
### Quantities To Track In The Tree

Track these items for each recursive call.

- **node** is the index of the current tree node, with node 1 as the root and children `2 * node` and `2 * node + 1`.
- **lo and hi** bound the node range of the current node, both inclusive.
- **mid** splits the node range into the left half `lo` to `mid` and the right half `mid + 1` to `hi`.
- **l and r** bound the query range, both inclusive.
- **tree[node]** holds the aggregate of the node range.

The tree array needs about `4 * n` entries so that every node index of an unbalanced split stays inside it. In the trace below, the cells are that array, and cell 0 stays unused.

<!-- stage: trace -->
### Build And Query On Eight Values

The trace uses the array `[5, 2, 7, 1, 4, 3, 6, 8]` and sums, so each stored value can be checked by hand. Node 1 owns positions 0 to 7, and the leaves are nodes 8 to 15.

#### Build Combines Children After Recursing

Construction visits each leaf first and writes the array value. Each parent is written only after both children return, so its value is the total of two finished nodes. The last write is node 1, which holds the total of the whole array.

```trace
{"cells":[0,36,15,21,7,8,7,14,5,2,7,1,4,3,6,8],"pointers":["node"],"steps":[{"at":{"node":8},"vars":{"lo":0,"hi":0,"stored":5},"note":"Leaf 8 owns position 0 and stores 5."},{"at":{"node":9},"vars":{"lo":1,"hi":1,"stored":2},"note":"Leaf 9 owns position 1 and stores 2."},{"at":{"node":4},"vars":{"lo":0,"hi":1,"stored":7},"note":"Node 4 owns positions 0 to 1. It adds 5 and 2 from its children and stores 7."},{"at":{"node":10},"vars":{"lo":2,"hi":2,"stored":7},"note":"Leaf 10 owns position 2 and stores 7."},{"at":{"node":11},"vars":{"lo":3,"hi":3,"stored":1},"note":"Leaf 11 owns position 3 and stores 1."},{"at":{"node":5},"vars":{"lo":2,"hi":3,"stored":8},"note":"Node 5 owns positions 2 to 3. It adds 7 and 1 from its children and stores 8."},{"at":{"node":2},"vars":{"lo":0,"hi":3,"stored":15},"note":"Node 2 owns positions 0 to 3. It adds 7 and 8 from its children and stores 15."},{"at":{"node":12},"vars":{"lo":4,"hi":4,"stored":4},"note":"Leaf 12 owns position 4 and stores 4."},{"at":{"node":13},"vars":{"lo":5,"hi":5,"stored":3},"note":"Leaf 13 owns position 5 and stores 3."},{"at":{"node":6},"vars":{"lo":4,"hi":5,"stored":7},"note":"Node 6 owns positions 4 to 5. It adds 4 and 3 from its children and stores 7."},{"at":{"node":14},"vars":{"lo":6,"hi":6,"stored":6},"note":"Leaf 14 owns position 6 and stores 6."},{"at":{"node":15},"vars":{"lo":7,"hi":7,"stored":8},"note":"Leaf 15 owns position 7 and stores 8."},{"at":{"node":7},"vars":{"lo":6,"hi":7,"stored":14},"note":"Node 7 owns positions 6 to 7. It adds 6 and 8 from its children and stores 14."},{"at":{"node":3},"vars":{"lo":4,"hi":7,"stored":21},"note":"Node 3 owns positions 4 to 7. It adds 7 and 14 from its children and stores 21."},{"at":{"node":1},"vars":{"lo":0,"hi":7,"stored":36},"note":"Node 1 owns positions 0 to 7. It adds 15 and 21 from its children and stores 36."}]}
```

#### Query Stops At Full Cover

The query asks for the sum of positions 2 to 6. The root partly overlaps the query, so it recurses. Node 4 owns positions 0 and 1, which lie outside the query, so it returns the identity 0. The hardest step is node 7, which owns positions 6 and 7. It overlaps only in position 6, so it recurses again and picks up leaf 14 while leaf 15 returns the identity.

The answer combines three stored values from nodes 5, 6 and 14. Five array cells were covered, but only three stored values were added.

```trace
{"cells":[0,36,15,21,7,8,7,14,5,2,7,1,4,3,6,8],"pointers":["node"],"steps":[{"at":{"node":1},"vars":{"lo":0,"hi":7,"added":0,"total":0},"note":"Node 1 owns positions 0 to 7 and overlaps the query in part, so it visits both children."},{"at":{"node":2},"vars":{"lo":0,"hi":3,"added":0,"total":0},"note":"Node 2 owns positions 0 to 3 and overlaps the query in part, so it visits both children."},{"at":{"node":4},"vars":{"lo":0,"hi":1,"added":0,"total":0},"note":"Node 4 owns positions 0 to 1, outside the query, so it returns the identity 0."},{"at":{"node":5},"vars":{"lo":2,"hi":3,"added":8,"total":8},"note":"Node 5 owns positions 2 to 3, fully inside the query, so it returns its stored 8. The running total is 8."},{"at":{"node":3},"vars":{"lo":4,"hi":7,"added":0,"total":8},"note":"Node 3 owns positions 4 to 7 and overlaps the query in part, so it visits both children."},{"at":{"node":6},"vars":{"lo":4,"hi":5,"added":7,"total":15},"note":"Node 6 owns positions 4 to 5, fully inside the query, so it returns its stored 7. The running total is 15."},{"at":{"node":7},"vars":{"lo":6,"hi":7,"added":0,"total":15},"note":"Node 7 owns positions 6 to 7 and overlaps the query in part, so it visits both children."},{"at":{"node":14},"vars":{"lo":6,"hi":6,"added":6,"total":21},"note":"Node 14 owns positions 6 to 6, fully inside the query, so it returns its stored 6. The running total is 21."},{"at":{"node":15},"vars":{"lo":7,"hi":7,"added":0,"total":21},"note":"Node 15 owns positions 7 to 7, outside the query, so it returns the identity 0."}]}
```

<!-- stage: code -->
### Build, Assign And Query

```java
final class SegmentTree {
    private final int n;
    private final long[] tree;

    SegmentTree(long[] values) {
        n = values.length;
        tree = new long[4 * n];                        // enough room for every node index
        build(values, 1, 0, n - 1);
    }

    private void build(long[] v, int node, int lo, int hi) {
        if (lo == hi) { tree[node] = v[lo]; return; }  // a leaf stores one value
        int mid = (lo + hi) / 2;
        build(v, 2 * node, lo, mid);
        build(v, 2 * node + 1, mid + 1, hi);
        tree[node] = tree[2 * node] + tree[2 * node + 1];  // parent combines its children
    }

    void assign(int pos, long value) { assign(1, 0, n - 1, pos, value); }

    private void assign(int node, int lo, int hi, int pos, long value) {
        if (lo == hi) { tree[node] = value; return; }  // reached the leaf of pos
        int mid = (lo + hi) / 2;
        if (pos <= mid) assign(2 * node, lo, mid, pos, value);
        else assign(2 * node + 1, mid + 1, hi, pos, value);
        tree[node] = tree[2 * node] + tree[2 * node + 1];  // recompute on the way back up
    }

    long query(int l, int r) { return query(1, 0, n - 1, l, r); }

    private long query(int node, int lo, int hi, int l, int r) {
        if (r < lo || hi < l) return 0;                // no overlap: identity of addition
        if (l <= lo && hi <= r) return tree[node];     // full cover: stored aggregate
        int mid = (lo + hi) / 2;
        return query(2 * node, lo, mid, l, r)
             + query(2 * node + 1, mid + 1, hi, l, r); // partial overlap: combine both halves
    }
}
```

The class uses sums, so the identity is 0 and the combine is `+`. A minimum tree changes exactly two things. The identity becomes `Long.MAX_VALUE`, and `Math.min` replaces each `+`. The three query cases and the recompute on the way back up stay the same.

Build visits each of the O(n) nodes once. Assign and query each visit O(log n) nodes.

<!-- stage: applicability -->
### When A Segment Tree Fits

#### Recognize The Pattern

Reach for a segment tree when an array receives point updates and range queries mix in any order. The operator must be associative, so the aggregate of a node range comes from its two children. It does not need an inverse. Range minimum, range maximum, range greatest common divisor and range sum all qualify.

The invariant is that each node stores the aggregate of exactly its node range, and every update restores it along one path. When a problem needs that guarantee and cannot subtract prefixes, the tree fits.

#### Choose Between A Fenwick Tree And This Tree

A Fenwick tree is shorter and faster by a constant factor, but it needs a sum-like operator with an inverse and answers prefixes. A segment tree answers any range directly for any associative operator. A static array with no updates is a false friend for this tree, because a prefix-sum array or a sparse table answers it with less machinery. A plain Fenwick tree is a false friend in the other direction, since it cannot hold a minimum under point assignment.

#### Avoid The Java Hazards

The tree array needs `4 * n` entries for a recursive layout with arbitrary `n`, and a smaller array fails with `ArrayIndexOutOfBoundsException` on some sizes. Sums need `long`, because 100,000 values near 10^9 overflow `int`. The identity of a minimum must be `Long.MAX_VALUE`, and adding to it overflows, so combine minima only with `Math.min`. Recursion depth stays near log n, so the call stack is safe.

<!-- stage: exercises -->
### Exercises

#### [Build] Build Range Sums (Author exercise)
<!-- id: rq31-segment-build-sums -->

**Prerequisites.** The node range, the children split and the combine step from this lesson.

**Problem.** Given an array `nums` of `n` integers, build the sum tree. Node 1 owns positions 0 to `n - 1`. Let `mid = (lo + hi) / 2`. A node `k` that owns `lo` to `hi` with `lo < hi` has child `2k` for `lo` to `mid` and child `2k + 1` for `mid + 1` to `hi`. Return the stored sums of all created nodes, in increasing node number.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 1000`.
- **Values** are `int` values with absolute value at most `10^6`.
- **Result** is a `long[]` that lists only nodes that exist, so it skips unused node numbers.
- **Input** is not modified.

**Example 1.** Input `[5, 2, 7, 1]`, output `[15, 7, 8, 5, 2, 7, 1]`.

**Example 2.** Input `[4, -1, 6]`, output `[9, 3, 6, 4, -1]`, which skips node 6 and node 7 because they are never created.

**Hint.** Which finishes first, a parent or its children? What does each parent read?

**Changed decision.** Baseline case: one recursive split and one combine over a whole array.

#### [Vary] Point Assignment (Author exercise)
<!-- id: rq31-segment-point-assign -->

**Prerequisites.** The first exercise above.

**Problem.** Use the sum tree from the first exercise. Process a list of assignments `(pos, value)` in order. Each assignment overwrites `nums[pos]` with `value` and recomputes every affected ancestor. For each assignment, return the number of nodes whose stored sum is rewritten, including the leaf, and the root sum afterwards.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 1000`.
- **Assignments** number at most 1000, and each `pos` satisfies `0 <= pos < n`.
- **Values** are `int` values with absolute value at most `10^6`.
- **Result** is a `long[][]` with one pair `{rewritten, rootSum}` per assignment.

**Example 1.** Input `[5, 2, 7, 1]` with assignments `(2, 0)` and `(0, 10)`, output `{3, 8}` and `{3, 13}`.

**Example 2.** Input `[1, 1, 1, 1, 1]` with assignments `(4, 6)` and `(0, 0)`, output `{3, 10}` and `{4, 9}`, because the tree for five values is uneven. The path to position 4 is shorter.

**Hint.** Which nodes own the assigned position? Do the other nodes change?

**Changed decision.** Only the leaf changes, so the exercise recomputes aggregates along one root-to-leaf path and nowhere else.

#### [Boundary] No Overlap And Full Cover (Author exercise)
<!-- id: rq31-segment-no-overlap-full-cover -->

**Prerequisites.** The three query cases from this lesson.

**Problem.** Given `n` and a query range `l` to `r`, run the query on the tree for `n` positions, using the node numbering from the first exercise. Return two lists of node numbers, each in the order the recursion reaches them. The first list holds the nodes that return their stored sum because their node range lies fully inside the query. The second list holds the nodes that return the identity 0 because their node range does not overlap the query.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 1000`.
- **Query** satisfies `0 <= l <= r < n`, and both ends are inclusive.
- **Recursion** stops at a node as soon as it is a full cover or a no-overlap node.
- **Result** is two `int` lists, first the full-cover nodes, then the no-overlap nodes.

**Example 1.** Input `n = 8`, query 2 to 6, output full cover `[5, 6, 14]` and no overlap `[4, 15]`.

**Example 2.** Input `n = 5`, query 1 to 1, output full cover `[9]` and no overlap `[8, 5, 3]`, so three nodes off the path return the identity.

**Hint.** Which test comes first, no overlap or full cover? Which nodes does a partly overlapping node still visit?

**Changed decision.** The question moves from the sum to the stopping rule, so each node returns the identity or its stored value and never recurses further.

#### [Recognize] Mutable Range Sum (LeetCode 307)
<!-- id: rq31-segment-mutable-sum -->

**Prerequisites.** All three exercises above.

**Problem.** Design a class `NumArray` built from an integer array `nums`. The method `update(index, val)` sets `nums[index]` to `val`. The method `sumRange(left, right)` returns the sum of `nums[left]` through `nums[right]`, both inclusive. Support calls in any order, and let each call see all earlier updates.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 30000`.
- **Values** are `int` values with absolute value at most `100`.
- **Calls** number at most 30000, in any order.
- **Indexes** satisfy `0 <= left <= right < n` and `0 <= index < n`.

**Example 1.** Input `[3, -2, 5, 1, 4]`, then `sumRange(1, 3)`, `update(2, 9)`, `sumRange(1, 3)`, `sumRange(0, 4)`, output `4`, `8`, `15`.

**Example 2.** Input `[7]`, then `sumRange(0, 0)`, `update(0, -3)`, `sumRange(0, 0)`, output `7`, `-3`.

**Hint.** Which operator combines two node ranges? Does a sum need a tree, or would prefix sums be enough here?

**Changed decision.** The array now changes between queries, so a fixed prefix-sum array fails and the tree repairs one path per update.
