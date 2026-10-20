<!-- lesson-kind: combination -->
<!-- lesson-id: ordered-interval-state -->
## Ordered Interval State

<!-- stage: context -->
### Why The Resume Request Is So Slow

A backup client uploads a 2 TB file in chunks over eight parallel connections. Chunks arrive out of order, and a few of them fail the checksum and must be thrown away. When the network drops, the client asks the server which byte ranges of the file it still lacks, so that it can resend only those. A developer stores every chunk the server accepted as a pair of offsets in a list. To answer the question, the code sorts the whole list and sweeps it from left to right.

With 100 chunks the answer is instant. With a 64 KB chunk size the file has about 33.5 million chunks, and the status page asks the same question every few seconds while uploads continue. Each answer sorts millions of pairs again, although only a handful of byte ranges are really missing. The status request takes longer than the interval between two requests, and the server spends its time answering questions about work it already did.

The list grows with the number of chunks ever received, and the answer depends only on the few ranges that remain. This lesson asks what the server should store so that adding a chunk, discarding a corrupt chunk and reporting the received bytes each cost far less than a pass over all chunks. It also asks what changes when the offsets are so large that no array can index them.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

#### Rules For Stored Runs

The lesson Interval Unions supplied the canonical shape of the stored state. Ranges are half-open, stored in sorted order, disjoint, and never touching, so one run of covered integers has exactly one entry. It also supplied the floor lookup that finds the one stored range which can contain or touch a new range, and the rule that an add merges on equality while a removal does not.

#### A Descent That Records Predecessors

The lesson Ordered Structures supplied a descent that records the predecessor, which is the last stored key before a limit. One such search serves insertion, removal and lookup alike, and the comparison is strict for insert and erase. That lesson also showed what a layered skip list costs, which lets this lesson compare a sorted array with a skip list honestly.

#### Ranges That Nodes Own

The lesson Mutable Range Queries supplied the Fenwick tree, where each entry owns a range of positions and an update touches only the entries whose owned range contains the changed position. This lesson reuses the owned-range idea for coordinates up to 10^18. It adds a segment tree, in which each node owns a range that splits at its midpoint, and a change updates the nodes along root-to-leaf paths.

#### The Choice This Lesson Adds

The new work is the choice between two states. A sorted run array stays small while the covered set has few runs, and it cannot answer a count over a sub-range without walking runs. A tree that creates nodes only where calls touch answers both questions in logarithmic time, and it pays for that with memory per call.

<!-- stage: naive -->
### Keeping Every Chunk In A List

The direct design appends each accepted range to a list and recomputes the answer from the whole list. The method that reports the received bytes copies the list, sorts the copy by start offset, and sweeps it while it merges overlapping ranges and adds up their sizes. Ranges are half-open, so the range from `l` up to but excluding `r` holds `r - l` bytes.

```java
final class NaiveCoverage {
    private final java.util.ArrayList<long[]> chunks = new java.util.ArrayList<>(); // {start, end}

    void add(long l, long r) { chunks.add(new long[] {l, r}); }

    long received() {
        java.util.ArrayList<long[]> copy = new java.util.ArrayList<>(chunks);
        copy.sort((a, b) -> Long.compare(a[0], b[0]));           // sorts every chunk ever added
        long total = 0, reach = Long.MIN_VALUE;                  // reach is the largest end seen so far
        for (long[] c : copy) {
            long from = Math.max(c[0], reach);                   // skip bytes that an earlier chunk already counted
            if (c[1] > from) total += c[1] - from;
            reach = Math.max(reach, c[1]);
        }
        return total;
    }
}
```

With `add(0, 10)`, `add(20, 30)` and `add(5, 25)`, the call `received()` returns 30, because the three chunks merge into one range from 0 to 30. The class is correct on every small test, and it has no way to discard a corrupt chunk without finding the right entries in the list and splitting them.

```predict
A file has 33.5 million chunks and the status page calls received() once per second while chunks keep arriving. About how many comparisons does one call spend on sorting, and how many distinct byte ranges does the answer actually depend on if 99 percent of the file has arrived in order?

One sort of 33.5 million pairs needs about 33.5 million times 25, which is roughly 840 million comparisons per call. If the chunks arrived mostly in order, the merged state is a few long runs, perhaps a few dozen. The answer therefore depends on tens of ranges, while the work depends on millions of entries. Memory also grows with every chunk, because the list keeps ranges that a merge would have absorbed long ago.
```

<!-- stage: bottleneck -->
### Cost That Follows Calls, Not Runs

Let `n` be the number of calls so far and `k` the number of maximal runs of received bytes. One call to `received` costs O(n log n) time, and the list costs O(n) memory. The useful state has only `k` entries. In a healthy upload, `k` stays small while `n` reaches millions.

The repeated work has a clear shape. Each call re-derives the same merged runs from the same chunks, and every new chunk changes at most a few runs. A stored list of merged runs would avoid this, but a plain list does not search. To add a range, the code must still scan from the front to find the runs that touch it, which costs O(k) per call. For a fragmented state with 10^5 runs, that scan compares up to 10^5 entries one by one, where a binary search needs about 17 probes. A scan of that size is too slow for a call that happens thousands of times per second.

A second weakness appears when positions are huge. A sorted run list stays small while the number of runs is small, but a question such as "how many bytes in offsets 10^17 through 10^17 + 10^9 are received?" must visit every run in that window. A good design needs three things. Neighbours of a range must be found in O(log k). Updates must adjust a stored total without a rescan. A choice must exist for the workloads where counting over a sub-range matters more than keeping memory proportional to `k`.

<!-- stage: insight -->
### Search Runs And Keep The Total

#### Find Neighbours With An Explicit Search

Store the merged runs in two sorted arrays, one for starts and one for ends. Both arrays increase together, because runs are disjoint and do not touch. The routine **upper-bound search** is a binary search over the starts that returns the first index whose start is above a given offset. The runs to the left of that index are the predecessors, because each starts at or before the offset. The caller walks left from the index over the runs that reach the new range. The code names this search `firstStartAbove`. One search and a short walk replace the scan from the front.

An explicit search is worth writing when no ordered map fits. A sorted array answers the search in O(log k) with no per-entry object, and an insertion shifts the tail with one `System.arraycopy`. That shift costs O(k) per update, but it is a straight memory copy with no comparison. At 10^4 runs one shift moves at most 160 KB across the two arrays. At 10^5 runs it moves 1.6 MB, and a few thousand updates per second then move gigabytes per second. The lesson accepts the shift only because `k` stays near tens of thousands. A skip list from the lesson Ordered Structures removes the shift at the price of pointers and random levels, and a `TreeMap` hides the same search behind a library class. All three give the same answers, and the choice is a cost question.

#### Keep The Covered Length Beside The Runs

The **covered length** is the number of integers inside the stored runs, kept in a `long`. Every change to the runs also changes this number by the exact difference. An add removes the lengths of the runs it absorbs and then adds the length of the fused run. A removal subtracts the lengths of every overlapping run and adds back the surviving left and right pieces. The total is read in constant time, and a test can check it against the sum of the stored run sizes after every call.

<!-- names: upper-bound search, covered length, dynamic segment tree -->

#### Grow A Tree Only Where Calls Touch

The run arrays cannot count the integers inside a sub-range faster than they can visit the runs there. A **dynamic segment tree** answers that count in O(log D) for a coordinate domain of size D. The root owns the whole domain. A node creates its two children only when a call needs to descend below it, so memory follows the touched paths and not the domain size. A node stores how many integers it covers, and a node is full when that number equals the size of its range.

A full node needs no children. When an add covers a node completely, the node becomes full and drops its subtree, and that drop is the merge of every smaller run that the add swallowed. A node can also become full through its children, for instance after `add(0, 8)` and then `add(8, 16)`, and it then keeps them. The invariant says that a node is full exactly when its count equals its range size, that a call never descends into a full node, and that every node with children has a count equal to the sum of its two children. Dropped nodes leave their array slots behind, because the arrays never reclaim slots.

#### Choose The State From The Workload

Three facts decide the state. The domain size says whether any array over coordinates is possible. The operation set says whether a count over a sub-range is needed. The expected number of runs says whether a sorted array stays small. The sorted run state keeps memory proportional to the runs and answers the total in O(1). The tree answers every count in O(log D) and uses up to O(log D) nodes per call. When the domain is at most 64 integers, neither is needed: a single `long` used as a bitmask holds one bit per integer. An add sets a window of bits, a removal clears it, and `Long.bitCount` counts the covered bits in O(1).

<!-- stage: variables -->
### Fields Of The Two States

The sorted run state stores four fields. The arguments of each call are offsets `l` and `r` that describe the half-open range from `l` up to but excluding `r`.

- **starts** is a `long` array of run starts in increasing order, and only the first `size` slots are in use.
- **ends** is a `long` array of run ends, where `ends[i]` is greater than `starts[i]` and less than `starts[i + 1]`.
- **size** is the number of stored runs.
- **covered** is the covered length as a `long`, equal to the sum of `ends[i] - starts[i]`.

The tree state stores a root and a domain size, and each node stores two child references and a count. A node with no children is either empty or full. In the traces below, the cells are the integers 0 to 15, the pointer `l` marks the start of the call's range, and the pointer `r` marks the excluded end, so `r` can equal the number of cells.

The invariant for the run arrays is that after every call the runs are sorted, disjoint and never touch, and `covered` equals the sum of their lengths. The invariant for the tree is that every node's count equals the number of covered integers in its range.

<!-- stage: trace -->
### Tracing Runs And Tree Nodes

#### Sorted Runs With Explicit Search

Each call first runs the upper-bound search to find the index of the first run that starts above the right edge of the range. It then walks left from that index over the runs that reach the range. The first three adds build one run: the third add touches the runs on both sides of its range, so the two stored runs and the new range fuse into the single run from 2 up to but excluding 12. The removal from 4 to 10 cuts that run into two pieces, and the covered length falls from 10 to 4. The add at 14 creates a separate run. The last removal clears a stretch that spans a whole run and part of two others, and only the pieces outside it remain.

```trace
{"cells":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],"pointers":["l","r"],"steps":[{"at":{"l":2,"r":6},"vars":{"call":"add(2,6)","runs":"[2,6)","covered":4},"note":"add [2,6). The search returns index 0, and no run on its left reaches 2, so no stored run is touched. The new range becomes its own run."},{"at":{"l":9,"r":12},"vars":{"call":"add(9,12)","runs":"[2,6) [9,12)","covered":7},"note":"add [9,12). The search returns index 1, and no run on its left reaches 9, so no stored run is touched. The new range becomes its own run."},{"at":{"l":6,"r":9},"vars":{"call":"add(6,9)","runs":"[2,12)","covered":10},"note":"add [6,9). The search returns index 2, and the walk to the left stops at index 0. The 2 runs [2,6) [9,12) touch or overlap the range, so they fuse with it into [2,12)."},{"at":{"l":4,"r":10},"vars":{"call":"remove(4,10)","runs":"[2,4) [10,12)","covered":4},"note":"remove [4,10). The search returns index 1, and the walk to the left stops at index 0. The run [2,12) overlaps the cut, so the array keeps [2,4) [10,12)."},{"at":{"l":14,"r":16},"vars":{"call":"add(14,16)","runs":"[2,4) [10,12) [14,16)","covered":6},"note":"add [14,16). The search returns index 2, and no run on its left reaches 14, so no stored run is touched. The new range becomes its own run."},{"at":{"l":3,"r":15},"vars":{"call":"remove(3,15)","runs":"[2,3) [15,16)","covered":2},"note":"remove [3,15). The search returns index 3, and the walk to the left stops at index 0. The 3 runs [2,4) [10,12) [14,16) overlap the cut, so the array keeps [2,3) [15,16)."}]}
```

#### Tree Nodes Appear And Disappear

The domain is the sixteen integers 0 to 15. The first add creates nodes only on the paths to the touched leaves, and the add from 4 to 8 fills the node that owns exactly those integers. The add from 2 to 6 fills the node that owns 2 and 3, discards its two leaf children, and stops at the node for 4 to 8 because that node is already full. The add from 8 to 12 fills one more node. The final add covers the root completely, so the root becomes full and every other node disappears. The covered count reads 16 from the root alone, and the tree is back to one node.

```trace
{"cells":["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"],"pointers":["l","r"],"steps":[{"at":{"l":1,"r":3},"vars":{"call":"add(1,3)","covered":2,"nodes":11},"note":"add [1,3). [1,2) lies inside the range, so it becomes full. [2,3) lies inside the range, so it becomes full. The tree now holds 11 nodes and the covered count is 2."},{"at":{"l":4,"r":8},"vars":{"call":"add(4,8)","covered":6,"nodes":11},"note":"add [4,8). [4,8) lies inside the range, so it becomes full. The tree now holds 11 nodes and the covered count is 6."},{"at":{"l":2,"r":6},"vars":{"call":"add(2,6)","covered":7,"nodes":9},"note":"add [2,6). [2,4) lies inside the range, so it becomes full and drops 2 nodes below it. [4,8) is already full, so the call stops there. The tree now holds 9 nodes and the covered count is 7."},{"at":{"l":8,"r":12},"vars":{"call":"add(8,12)","covered":11,"nodes":11},"note":"add [8,12). [8,12) lies inside the range, so it becomes full. The tree now holds 11 nodes and the covered count is 11."},{"at":{"l":0,"r":16},"vars":{"call":"add(0,16)","covered":16,"nodes":1},"note":"add [0,16). [0,16) lies inside the range, so it becomes full and drops 10 nodes below it. The tree now holds 1 node and the covered count is 16."}]}
```

<!-- stage: code -->
### Run Arrays And A Dynamic Tree

#### The Sorted Run Arrays

The class `RunStore` keeps the starts and ends in two arrays and finds neighbours with its own binary search. The private method `splice` replaces a block of runs by at most two pieces with one array copy, so add and remove share the shifting code. The walk to the left over absorbed runs is paid for by the removal of those runs, so its cost does not add to the search.

```java
final class RunStore {
    private long[] starts = new long[4];
    private long[] ends = new long[4];
    private int size;
    private long covered;

    // Upper-bound search: returns the first index whose start is greater than x, or size when none is.
    private int firstStartAbove(long x) {
        int lo = 0, hi = size;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (starts[mid] > x) hi = mid; else lo = mid + 1;
        }
        return lo;
    }

    // Replaces runs i..j-1 by the given pieces and keeps both arrays sorted.
    private void splice(int i, int j, long[] ps, long[] pe, int count) {
        int newSize = size - (j - i) + count;
        if (newSize > starts.length) {
            starts = java.util.Arrays.copyOf(starts, newSize * 2);
            ends = java.util.Arrays.copyOf(ends, newSize * 2);
        }
        System.arraycopy(starts, j, starts, i + count, size - j);
        System.arraycopy(ends, j, ends, i + count, size - j);
        for (int k = 0; k < count; k++) { starts[i + k] = ps[k]; ends[i + k] = pe[k]; }
        size = newSize;
    }

    void add(long l, long r) {
        if (l >= r) return;                        // an empty range changes nothing
        int j = firstStartAbove(r);                // runs before j start at or before r
        int i = j;
        while (i > 0 && ends[i - 1] >= l) i--;     // walk left while the run reaches l
        long s = l, e = r;
        for (int k = i; k < j; k++) covered -= ends[k] - starts[k];
        if (i < j) { s = Math.min(s, starts[i]); e = Math.max(e, ends[j - 1]); }
        splice(i, j, new long[] {s}, new long[] {e}, 1);
        covered += e - s;
    }

    void remove(long l, long r) {
        if (l >= r) return;                        // an empty cut changes nothing
        int j = firstStartAbove(r - 1);            // runs before j start before r
        int i = j;
        while (i > 0 && ends[i - 1] > l) i--;      // walk left while the run reaches past l
        if (i == j) return;
        long[] ps = new long[2], pe = new long[2];
        int count = 0;
        if (starts[i] < l) { ps[count] = starts[i]; pe[count++] = l; }
        if (ends[j - 1] > r) { ps[count] = r; pe[count++] = ends[j - 1]; }
        for (int k = i; k < j; k++) covered -= ends[k] - starts[k];
        splice(i, j, ps, pe, count);
        for (int k = 0; k < count; k++) covered += pe[k] - ps[k];
    }

    long covered() { return covered; }
}
```

In `add`, the call `firstStartAbove(r)` gives `j`, so every run before `j` starts at or before `r` and every run from `j` on starts too far right to touch. The loop then lowers `i` while `ends[i - 1] >= l`. A run touches or overlaps the new range exactly when its end reaches `l`, so the test uses `>=` and the equal case fuses touching runs. The block `i` through `j - 1` is empty when `i == j`, and the code reads `starts[i]` and `ends[j - 1]` only when `i < j`. The fused run takes the smaller start and the larger end of the new range and that block.

In `remove`, two tests differ. The search uses `r - 1`, so `j` counts the runs that start below `r`, and a run that starts exactly at `r` stays. The loop uses `ends[i - 1] > l`, because a run that only touches the cut shares no integer with it. Only the first run of the block can leave a left piece, when `starts[i] < l`, and only the last can leave a right piece, when `ends[j - 1] > r`. Both pieces are non-empty by those tests, so the guard at the top is the only place that rejects empty input.

#### The Dynamic Segment Tree

The class `DynamicCover` stores nodes in three parallel arrays and uses index 0 for the root. A child index of 0 means no child, which is safe because the root is never a child. The three parts below show how `add`, `remove` and `countIn` behave on a domain of 16 integers, and the full class follows them.

#### Adding A Range

The method `add` ends early on a full node, and it drops the children of a node that the new range covers completely. The second trace above runs this method. Take `add(4, 8)`. The root owns 0 to 16 and is not swallowed, so it creates the children 0 to 8 and 8 to 16. Only `l < 8` holds, so the call descends left, where the node for 0 to 8 creates its own children. The node for 4 to 8 is swallowed, so its count becomes 4. The counts of its ancestors are recomputed to 4, and the tree holds 5 nodes.

#### Removing A Range

The method `remove` mirrors `add`, with one extra step. A full node without children first splits into two full halves, so a partial cut can leave one half covered. Continue with the tree after `add(4, 8)` and call `remove(5, 7)`. The full node for 4 to 8 has no children, so it splits into 4 to 6 and 6 to 8 with count 2 each. Each of those splits again, into single integers. The leaves for 5 and 6 are swallowed by the cut and drop to 0. The counts recompute upward to 2 at the root, which matches the integers 4 and 7 that remain.

#### Counting Inside A Range

The method `countIn` reads stored counts and never visits runs. It visits at most two partial nodes per level, so it costs O(log D). On the same tree, `countIn(0, 5)` skips the node for 8 to 16 because its count is 0. It also skips the node for 0 to 4 for the same reason. Inside the node for 4 to 8 it reads the count 1 of the leaf for integer 4 and ignores the leaf for integer 5, which lies outside the range. The answer is 1.

#### The Full Tree Class

```java
final class DynamicCover {
    private int[] left = new int[16], right = new int[16];
    private long[] count = new long[16];
    private int nodes = 1;                          // slot 0 is the root
    private final long limit;

    DynamicCover(long limit) { this.limit = limit; }

    private int create() {
        if (nodes == left.length) {                  // grow all three arrays together
            left = java.util.Arrays.copyOf(left, nodes * 2);
            right = java.util.Arrays.copyOf(right, nodes * 2);
            count = java.util.Arrays.copyOf(count, nodes * 2);
        }
        return nodes++;
    }

    void add(long l, long r) { add(0, 0, limit, l, r); }   // half-open [l, r) inside [0, limit)

    private void add(int node, long lo, long hi, long l, long r) {
        if (count[node] == hi - lo) return;                     // full already
        if (l <= lo && hi <= r) {                               // the range swallows the node
            count[node] = hi - lo;
            left[node] = 0;
            right[node] = 0;                                    // children are abandoned, which merges their runs; their slots are not reclaimed
            return;
        }
        long mid = lo + (hi - lo) / 2;
        if (left[node] == 0) { int a = create(); int b = create(); left[node] = a; right[node] = b; }
        if (l < mid) add(left[node], lo, mid, l, r);
        if (r > mid) add(right[node], mid, hi, l, r);
        count[node] = count[left[node]] + count[right[node]];   // recompute from the children
    }

    void remove(long l, long r) { if (l < r) remove(0, 0, limit, l, r); }

    private void remove(int node, long lo, long hi, long l, long r) {
        if (count[node] == 0) return;                           // nothing covered below
        if (l <= lo && hi <= r) {                               // the cut swallows the node
            count[node] = 0;
            left[node] = 0;
            right[node] = 0;
            return;
        }
        long mid = lo + (hi - lo) / 2;
        if (left[node] == 0) {                                  // a full node without children must split before a partial cut
            int a = create(); int b = create(); left[node] = a; right[node] = b;
            count[a] = mid - lo; count[b] = hi - mid;           // both halves inherit the full state
        }
        if (l < mid) remove(left[node], lo, mid, l, r);
        if (r > mid) remove(right[node], mid, hi, l, r);
        count[node] = count[left[node]] + count[right[node]];
    }

    // Covered integers inside [l, r), found from stored counts without visiting runs.
    long countIn(long l, long r) { return l < r ? countIn(0, 0, limit, l, r) : 0; }

    private long countIn(int node, long lo, long hi, long l, long r) {
        if (count[node] == 0 || r <= lo || hi <= l) return 0;   // empty node or disjoint range
        if (l <= lo && hi <= r) return count[node];             // the query swallows the node
        if (left[node] == 0) return Math.min(hi, r) - Math.max(lo, l); // a childless non-empty node is full
        long mid = lo + (hi - lo) / 2;
        return countIn(left[node], lo, mid, l, r) + countIn(right[node], mid, hi, l, r);
    }

    long covered() { return count[0]; }
}
```

<!-- stage: applicability -->
### When Ordered State Fits

#### Recognizing The Pattern

Use ordered interval state when public methods add or remove ranges over a large coordinate line and ask for the covered total or for neighbours of a point. Check three points before you code. Write the endpoint convention once, as half-open ranges. Estimate the number of runs, because it decides whether a sorted array shift is cheap. Ask whether any question counts the covered integers inside a sub-range, because that question moves the design toward a tree. The invariant to protect is that stored runs stay sorted, disjoint and non-touching, and that the stored total equals the sum of their lengths after every call.

#### False Friends

A boolean array over the coordinates looks like the simplest state, and it is a false friend when the domain is 10^9 or larger, because memory follows the domain and not the number of runs. A `HashSet` of covered integers has the same problem, and a range add of a million integers inserts a million entries. A third false friend is a sorted list of added ranges that is never merged. It answers search questions quickly, but its size follows the number of calls, and the covered total needs a full sweep.

#### When The Method Does Not Apply

If every range is a single point and the questions are about rank or order statistics, an order-statistic tree or a Fenwick tree over compressed coordinates fits better. If the ranges carry weights that overwrite each other, as in a paint operation that records the latest colour, a run state needs a value per run, and a lazy tree from the lesson Deferred Transforms fits better. When the whole sequence of calls is known in advance, coordinate compression and a static array can replace a dynamic tree, and the memory per call disappears.

<!-- stage: exercises -->
### Exercises

#### [Build] Gap-Tolerant Stream Summary (LeetCode 352)
<!-- id: dq39-gap-tolerant-stream -->

**Prerequisites.** The sorted run arrays and the upper-bound search from this lesson, where the last group starting at or before a value sits just left of the returned index. This exercise is a variant of LeetCode 352 and changes its contract: runs also merge across a small gap of missing values.

**Problem.** Design a class `GapSummary` whose constructor takes an `int` called `gap`. The method `addNum(v)` records the integer `v` as seen, and recording a value twice has no further effect. The method `getIntervals()` groups the seen values in sorted order. Two neighbouring seen values `a < b` belong to the same group exactly when `b - a <= gap + 1`. The method returns one closed pair `[smallest, largest]` per group, sorted by smallest value. The pair covers the missing values inside the group without marking them as seen. Search the stored groups with a hand-written binary search, not with `TreeMap`.

**Constraints.** The limits are:
- **`v`** is an `int` with `0 <= v <= 2^31 - 1`, and **`gap`** is an `int` with `0 <= gap <= 10^9`.
- **Calls** number at most `2 * 10^5`, and they arrive online, so the sequence is not known in advance.
- **Update/query ratio** is about 20 to 1.
- **Return value** is a new `int[][]`, empty for an empty stream.
- **Arithmetic** must not overflow near `2^31 - 1`.

**Example 1.** With `gap = 1`, input `addNum(1)`, `addNum(4)`, `addNum(9)`, `addNum(6)`, then `getIntervals()`, output `[[1,1],[4,6],[9,9]]`. After `addNum(2)` the output is `[[1,6],[9,9]]`, and after `addNum(7)` the output is `[[1,9]]`.

**Example 2.** With `gap = 0`, input `addNum(5)`, `addNum(5)`, `addNum(3)`, `addNum(4)`, `addNum(4)`, `addNum(9)`, then `getIntervals()`, output `[[3,5],[9,9]]`. A gap of 0 gives the original problem.

**Hint.** Store each group as its smallest and largest value in two sorted arrays. Two neighbouring groups merge when the distance `b - a` between the largest value `a` of the left group and the smallest value `b` of the right group is at most `gap + 1`. The covered length cannot be the sum of run lengths here, because a group also spans values never seen, so keep only the minimum and maximum of each group. A value inside a group changes nothing. Which two groups can a value outside every group be close enough to, and what happens when it is close to both?

**Changed decision.** The merge test compares a distance with `gap + 1` and not an equality with 1, so one new value can bridge two groups that were far apart before.

#### [Vary] Range Module With Next Gap (LeetCode 715)
<!-- id: dq39-next-gap-module -->

**Prerequisites.** The gap-tolerant exercise above and the half-open removal rules from the lesson Interval Unions. This exercise is a variant of LeetCode 715 and changes its operation set: the query asks for the first untracked integer.

**Problem.** Design a class `RangeGaps` over the integers with half-open ranges `[l, r)`. The method `addRange(l, r)` tracks every integer in the range, and `removeRange(l, r)` untracks every integer in the range. The method `nextUncovered(x)` returns the smallest untracked integer that is at least `x`. The method `trackedCount()` returns how many integers are tracked. There is no yes or no query over a range. Keep the tracked integers as sorted runs that never touch, and keep `trackedCount` in a stored field.

**Constraints.** The limits are:
- **`l` and `r`** are `long` values with `0 <= l < r <= 10^12`, and **`x`** is a `long` with `0 <= x <= 10^12`.
- **Calls** number at most `10^5`, and they arrive online.
- **Update/query ratio** is about 1 to 1.
- **Return values** are `long`, and the two update methods return nothing.

**Example 1.** Input `addRange(10,20)`, `addRange(30,40)`, `removeRange(14,33)`, then `nextUncovered(10)`, `nextUncovered(12)`, `nextUncovered(33)`, `nextUncovered(35)` and `trackedCount()`, output `14`, `14`, `40`, `40` and `11`.

**Example 2.** Input `addRange(5,8)`, `addRange(8,12)`, `addRange(1,5)`, then `nextUncovered(1)`, `nextUncovered(11)`, `nextUncovered(0)` and `trackedCount()`, output `12`, `12`, `0` and `11`.

**Hint.** If the run that contains `x` ends at `e`, why is `e` always untracked? Which property of the stored runs gives that guarantee?

**Changed decision.** The query returns the end of one run, so the non-touching property of the runs is now what makes the answer correct and not only compact.

#### [Boundary] Counting Covered Integers On A Huge Line (LeetCode 2276)
<!-- id: dq39-huge-line-coverage -->

**Prerequisites.** The dynamic segment tree from this lesson.

This exercise is a variant of LeetCode 2276. It adds a count inside a window on a line too large for an array, which a list of merged runs answers only by visiting every run in the window.

**Problem.** Design a class `CoverageTree` with a constructor that receives a `long` called `limit`, so the valid integers are `0` through `limit - 1`. The method `add(left, right)` marks every integer from `left` to `right` inclusive as covered. The method `count()` returns how many distinct integers are covered. The method `countIn(left, right)` returns how many covered integers lie from `left` to `right` inclusive. Implement the class with a dynamic segment tree whose nodes exist only along touched paths.

**Constraints.** The limits are:
- **`limit`** is a `long` with `1 <= limit <= 10^18`.
- **`left` and `right`** are `long` values with `0 <= left <= right < limit`, so `right + 1` never overflows.
- **Calls** number at most `10^5`, mixed between the three methods, and they arrive online.
- **Update/query ratio** is about 1 to 1.
- **Return values** are `long`.

**Example 1.** With `limit = 100`, input `add(10,14)`, `add(20,24)`, `add(40,44)`, `count()`, output 15. After input `add(12,41)`, `count()` outputs 35, `countIn(0,19)` outputs 10 and `countIn(42,99)` outputs 3.

**Example 2.** With `limit = 10^18`, input `add(0, 10^18 - 1)`, `count()`, output `10^18`. After input `add(5,7)`, `count()` still outputs `10^18`, and `countIn(10^18 - 10, 10^18 - 1)` outputs 10.

**Hint.** What should a node do when a new range covers it entirely, and what happens to the counts of the smaller runs that were stored below it?

**Changed decision.** One add can swallow many stored runs at once. The tree must discard the swallowed subtrees and keep every ancestor count exact, and the largest coordinate must not overflow when the range becomes half-open.

#### [Recognize] Dynamic Coverage API (Author exercise)
<!-- id: dq39-dynamic-coverage-api -->

**Prerequisites.** The three exercises above and the choice rules from this lesson.

**Problem.** Design a class `DynamicCoverage` with a constructor that receives a `long` called `domain` and a `boolean` called `rangeCounts`, where valid integers are `0` through `domain - 1` and `rangeCounts` states whether `coveredIn` will ever be called. The methods `add(l, r)` and `remove(l, r)` cover or uncover the half-open range `[l, r)`, and an empty range changes nothing. The method `total()` returns the covered count, and `coveredIn(l, r)` returns the covered count inside `[l, r)`. The method `backend()` returns the name of the stored state. The name is `"mask"`, the 64-bit bitmask from the lesson, when `domain <= 64`, otherwise `"runs"` when `rangeCounts` is false, otherwise `"tree"`. The `"runs"` state still answers `coveredIn`, by walking the stored runs that overlap the range.

**Constraints.** The limits are:
- **`domain`** is a `long` with `1 <= domain <= 10^18`.
- **`l` and `r`** are `long` values with `0 <= l <= r <= domain`, and any other range throws `IllegalArgumentException`.
- **Calls** number at most `10^5`, and they arrive online, but the constructor flag `rangeCounts` is fixed when the object is built.
- **Update/query ratio** is about 3 to 1.
- **Return values** of `total` and `coveredIn` are `long`.

**Example 1.** With `domain = 40` and `rangeCounts = true`, `backend()` returns `"mask"`. Input `add(3,10)`, `add(8,20)`, `remove(5,6)`, output `total()` is 16 and `coveredIn(0,8)` is 4. With `domain = 10^9` and `rangeCounts = false`, `backend()` returns `"runs"`. Input `add(100,200)`, `add(200,300)`, `remove(150,250)`, `add(1000,1000)`, output `total()` is 100, and `coveredIn(120,260)` is 40.

**Example 2.** With `domain = 10^12` and `rangeCounts = true`, `backend()` returns `"tree"`. Input `add(0, 5 * 10^11)`, `remove(10^11, 2 * 10^11)`, output `total()` is `4 * 10^11` and `coveredIn(0, 3 * 10^11)` is `2 * 10^11`.

**Hint.** Which state needs memory proportional to the domain, which to the number of runs, and which to the number of calls? Which of them can answer `coveredIn` without visiting runs?

**Changed decision.** The state is chosen from the coordinate domain and the expected query set, so the same public methods run on three different stored forms, and each form needs its own handling of removal.
