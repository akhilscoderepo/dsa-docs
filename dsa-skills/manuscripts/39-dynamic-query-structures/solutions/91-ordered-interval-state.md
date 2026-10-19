<!-- solutions-for: 91-ordered-interval-state -->
### Solutions For Ordered Interval State

#### Solution: [Build] Gap-Tolerant Stream Summary (LeetCode 352)
<!-- id: dq39-gap-tolerant-stream -->

**Approach.** The class keeps each group of seen values as a closed pair of smallest and largest value, in two parallel arrays sorted by smallest value. The invariant is that groups are disjoint and that the distance from one group's largest value to the next group's smallest value exceeds `gap + 1`, so each group is maximal.

A new value `v` first runs a hand-written predecessor search that returns the last group starting at or before `v`. If that group's largest value reaches `v`, the value lies inside the group, and nothing changes because neither the smallest nor the largest value moves. Otherwise `v` is compared with two neighbours only: the found group on its left and the next group on its right. When both are within `gap + 1`, the value bridges them, and the left group takes over the right group's largest value. When only one is close enough, that group stretches to include `v`. When neither is close, `v` opens a new group. Distances are computed in `long`, so values near `2^31 - 1` and gaps up to `10^9` cannot overflow.

**Complexity.**

- **Time** is O(log n) for the search plus an O(n) array shift when a group is inserted or two groups fuse, where `n` is the number of groups. The shift is a single block copy, and `getIntervals` costs O(n).
- **Space** is O(n) for the two arrays, because the number of groups never exceeds the number of distinct values.

```java run
import java.util.*;

public final class GapStream {
    /** Keeps seen values as clusters [lo, hi] (closed) in two parallel sorted arrays. */
    static final class GapSummary {
        // Invariant: clusters are sorted, disjoint, and the distance from one cluster's hi to the next lo exceeds step.
        private final long step;                 // two seen values merge when they differ by at most step
        private long[] lo = new long[4];         // lo[i] is the smallest seen value of cluster i
        private long[] hi = new long[4];         // hi[i] is the largest seen value of cluster i
        private int n;                           // number of clusters in use

        GapSummary(int gap) {
            // A gap of g missing values between neighbours is tolerated, so the largest merged distance is g + 1.
            if (gap < 0) throw new IllegalArgumentException("gap must be at least 0");
            this.step = (long) gap + 1;
        }

        /**
         * Predecessor search: the index of the last cluster whose lo is at most v, or -1 when none exists.
         * Time: O(log n) because each probe halves the candidate range.
         * Space: O(1).
         */
        private int lastStartAtMost(long v) {
            int a = 0, b = n;                                // the answer lies in positions a - 1 .. b - 1
            while (a < b) {                                  // each pass halves b - a
                int m = (a + b) >>> 1;                       // unsigned shift avoids int overflow of a + b
                if (lo[m] <= v) a = m + 1;                   // cluster m starts at or before v, so look right of it
                else b = m;                                  // cluster m starts after v, so look left of it
            }
            return a - 1;                                    // a is the first cluster that starts after v
        }

        /** Opens a slot at position i by shifting the tail right. Time: O(n) copy, Space: amortized O(1). */
        private void openSlot(int i) {
            if (n == lo.length) {                            // grow by doubling so growth costs O(1) amortized
                lo = Arrays.copyOf(lo, n * 2);
                hi = Arrays.copyOf(hi, n * 2);
            }
            System.arraycopy(lo, i, lo, i + 1, n - i);       // shift starts right by one
            System.arraycopy(hi, i, hi, i + 1, n - i);       // shift ends right by one
            n++;                                             // the slot count grows by one
        }

        /**
         * Records v. Time: O(log n) search plus an O(n) array shift in the worst case. Space: O(1) extra.
         * Invariant: after the call every pair of neighbouring clusters is more than step apart.
         */
        void addNum(int v) {
            int p = lastStartAtMost(v);                      // cluster p is the only one that can contain v or lie just left of it
            if (p >= 0 && hi[p] >= v) return;                // v lies inside cluster p, so min and max do not change
            boolean joinLeft = p >= 0 && v - hi[p] <= step;  // cluster p ends close enough to v
            boolean joinRight = p + 1 < n && lo[p + 1] - v <= step; // the next cluster starts close enough to v
            if (joinLeft && joinRight) {                     // v bridges two clusters into one
                hi[p] = hi[p + 1];                           // the left cluster now ends where the right one ended
                System.arraycopy(lo, p + 2, lo, p + 1, n - p - 2); // close the hole left by the right cluster
                System.arraycopy(hi, p + 2, hi, p + 1, n - p - 2);
                n--;                                         // one cluster fewer
            } else if (joinLeft) {
                hi[p] = v;                                   // v extends the left cluster to the right
            } else if (joinRight) {
                lo[p + 1] = v;                               // v extends the right cluster to the left
            } else {
                openSlot(p + 1);                             // v starts a new cluster after cluster p
                lo[p + 1] = v;
                hi[p + 1] = v;
            }
        }

        /** Returns the clusters as closed pairs. Time: O(n). Space: O(n) for the returned array. */
        int[][] getIntervals() {
            int[][] out = new int[n][];                      // a fresh array, so callers may modify it
            for (int i = 0; i < n; i++) out[i] = new int[] {(int) lo[i], (int) hi[i]}; // values came from ints
            return out;
        }
    }

    /** Oracle: keeps every seen value and groups the sorted values on demand. */
    static int[][] oracle(TreeSet<Integer> seen, int gap) {
        List<int[]> out = new ArrayList<>();
        for (int v : seen) {                                 // sorted ascending
            if (!out.isEmpty() && (long) v - out.get(out.size() - 1)[1] <= (long) gap + 1) out.get(out.size() - 1)[1] = v;
            else out.add(new int[] {v, v});
        }
        return out.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // Example 1: gap 1 bridges one missing value but not two.
        GapSummary a = new GapSummary(1);
        for (int v : new int[] {1, 4, 9, 6}) a.addNum(v);
        if (!Arrays.deepEquals(a.getIntervals(), new int[][] {{1, 1}, {4, 6}, {9, 9}})) throw new AssertionError("example 1a");
        a.addNum(2);
        if (!Arrays.deepEquals(a.getIntervals(), new int[][] {{1, 6}, {9, 9}})) throw new AssertionError("example 1b");
        a.addNum(7);
        if (!Arrays.deepEquals(a.getIntervals(), new int[][] {{1, 9}})) throw new AssertionError("example 1c");
        // Example 2: gap 0 matches the original problem, and repeated or inside values change nothing.
        GapSummary b = new GapSummary(0);
        for (int v : new int[] {5, 5, 3, 4, 4, 9}) b.addNum(v);
        if (!Arrays.deepEquals(b.getIntervals(), new int[][] {{3, 5}, {9, 9}})) throw new AssertionError("example 2");
        // Empty stream returns an empty array, and int extremes do not overflow.
        if (new GapSummary(2).getIntervals().length != 0) throw new AssertionError("empty");
        GapSummary c = new GapSummary(5);
        c.addNum(Integer.MAX_VALUE); c.addNum(0); c.addNum(Integer.MAX_VALUE - 3);
        if (!Arrays.deepEquals(c.getIntervals(), new int[][] {{0, 0}, {Integer.MAX_VALUE - 3, Integer.MAX_VALUE}})) throw new AssertionError("extremes");
        // Random streams against the oracle, with small value ranges so merges and bridges are frequent.
        Random rnd = new Random(3901);
        for (int trial = 0; trial < 6000; trial++) {
            int gap = rnd.nextInt(4), range = 5 + rnd.nextInt(60);
            GapSummary s = new GapSummary(gap);
            TreeSet<Integer> seen = new TreeSet<>();
            for (int step = 0; step < 40; step++) {
                int v = rnd.nextInt(range);
                s.addNum(v);
                seen.add(v);
                if (!Arrays.deepEquals(s.getIntervals(), oracle(seen, gap))) throw new AssertionError("trial " + trial);
            }
        }
    }
}
```

#### Solution: [Vary] Range Module With Next Gap (LeetCode 715)
<!-- id: dq39-next-gap-module -->

**Approach.** Tracked integers live in a list of half-open runs sorted by start, with a stored count. The invariant is that runs are disjoint and never touch, so the end of every run is an untracked integer, and the count equals the sum of run lengths.

One lower-bound routine serves both ends of the run, because starts and ends both increase. For an add, the first run whose end reaches `l` and the first run whose start is beyond `r` bound the block of runs that overlap or touch the new range. That block collapses into one run that spans the smallest start and the largest end, and the count changes by the new length minus the absorbed lengths. For a removal, the bounds use strict overlap, so a run that only touches the cut stays untouched. Only the first and last overlapping runs can leave a surviving piece, one on each side of the cut. The query `nextUncovered(x)` finds the last run starting at or before `x`. If that run ends beyond `x`, its end is the answer, and the non-touching invariant guarantees that the end is untracked. Otherwise `x` itself is the answer.

**Complexity.**

- **Time** is O(log n) per search plus an O(n) list shift on update, where `n` is the number of runs. Each absorbed run is removed once, so the work of the loop over absorbed runs is charged to their creation.
- **Space** is O(n) for the run list, independent of the coordinate range.

```java run
import java.util.*;
import java.util.function.ToLongFunction;

public final class GapModule {
    /** Tracks half-open runs [start, end) in an ArrayList sorted by start. */
    static final class RangeGaps {
        // Invariant: runs are sorted, disjoint and never touch, so every run end is an untracked integer.
        private final ArrayList<long[]> runs = new ArrayList<>();   // each entry is {start, end}
        private long tracked;                                       // number of tracked integers, always the sum of end - start

        private static final ToLongFunction<long[]> START = r -> r[0];
        private static final ToLongFunction<long[]> END = r -> r[1];

        /**
         * Lower bound: the first index whose key is at least x, or runs.size() when none is.
         * Starts and ends are both increasing, so one search routine serves both.
         * Time: O(log n). Space: O(1).
         */
        private int firstAtLeast(ToLongFunction<long[]> key, long x) {
            int a = 0, b = runs.size();                             // the answer lies in a .. b
            while (a < b) {                                         // each pass halves the range
                int m = (a + b) >>> 1;                              // midpoint without overflow
                if (key.applyAsLong(runs.get(m)) < x) a = m + 1;    // key too small, so the answer is right of m
                else b = m;                                         // key large enough, so m may be the answer
            }
            return a;
        }

        /**
         * Tracks [l, r). Time: O(log n) search plus O(n) list shift. Space: O(1) extra.
         * Invariant: runs touching or overlapping [l, r) collapse into one run.
         */
        void addRange(long l, long r) {
            int i = firstAtLeast(END, l);                           // first run whose end reaches l, so it overlaps or touches
            int j = firstAtLeast(START, r + 1);                     // first run that starts after r, so runs i..j-1 touch [l, r)
            long s = l, e = r;                                      // the merged run begins as the new range
            if (i < j) {                                            // at least one stored run is absorbed
                s = Math.min(s, runs.get(i)[0]);                    // the leftmost absorbed run may start earlier
                e = Math.max(e, runs.get(j - 1)[1]);                // the rightmost absorbed run may end later
                for (int k = i; k < j; k++) tracked -= runs.get(k)[1] - runs.get(k)[0]; // take back absorbed lengths
            }
            runs.subList(i, j).clear();                             // delete the absorbed runs in one shift
            runs.add(i, new long[] {s, e});                         // insert the merged run at the same position
            tracked += e - s;                                       // add the merged length once
        }

        /**
         * Untracks [l, r). Time: O(log n) search plus O(n) list shift. Space: O(1) extra.
         * Invariant: only the first and last overlapping runs can leave a surviving piece.
         */
        void removeRange(long l, long r) {
            int i = firstAtLeast(END, l + 1);                       // first run whose end is beyond l, so it overlaps [l, r)
            int j = firstAtLeast(START, r);                         // first run that starts at or after r, so runs i..j-1 overlap
            if (i >= j) return;                                     // nothing overlaps
            long[] first = runs.get(i), last = runs.get(j - 1);     // only these two can survive in part
            List<long[]> keep = new ArrayList<>(2);
            if (first[0] < l) keep.add(new long[] {first[0], l});   // left piece survives before the cut
            if (last[1] > r) keep.add(new long[] {r, last[1]});     // right piece survives after the cut
            for (int k = i; k < j; k++) tracked -= runs.get(k)[1] - runs.get(k)[0]; // remove every overlapping length
            for (long[] p : keep) tracked += p[1] - p[0];           // add back the surviving pieces
            runs.subList(i, j).clear();                             // drop the overlapping runs
            runs.addAll(i, keep);                                   // reinsert the pieces in order
        }

        /**
         * Smallest untracked integer that is at least x. Time: O(log n). Space: O(1).
         * Invariant: the run containing x ends at an untracked integer because runs never touch.
         */
        long nextUncovered(long x) {
            int p = firstAtLeast(START, x + 1) - 1;                 // last run that starts at or before x
            return p >= 0 && runs.get(p)[1] > x ? runs.get(p)[1] : x; // inside a run jump to its end, else x itself
        }

        /** Number of tracked integers. Time: O(1). Space: O(1). */
        long trackedCount() { return tracked; }
    }

    public static void main(String[] args) {
        // Example 1.
        RangeGaps a = new RangeGaps();
        a.addRange(10, 20); a.addRange(30, 40); a.removeRange(14, 33);
        long[] r1 = {a.nextUncovered(10), a.nextUncovered(12), a.nextUncovered(33), a.nextUncovered(35), a.trackedCount()};
        if (!Arrays.equals(r1, new long[] {14, 14, 40, 40, 11})) throw new AssertionError("example 1 " + Arrays.toString(r1));
        // Example 2.
        RangeGaps b = new RangeGaps();
        b.addRange(5, 8); b.addRange(8, 12); b.addRange(1, 5);
        long[] r2 = {b.nextUncovered(1), b.nextUncovered(11), b.nextUncovered(0), b.trackedCount()};
        if (!Arrays.equals(r2, new long[] {12, 12, 0, 11})) throw new AssertionError("example 2 " + Arrays.toString(r2));
        // Random operations against a boolean array.
        Random rnd = new Random(7155);
        for (int trial = 0; trial < 5000; trial++) {
            RangeGaps m = new RangeGaps();
            boolean[] on = new boolean[70];
            for (int step = 0; step < 50; step++) {
                int l = 1 + rnd.nextInt(55), r = l + 1 + rnd.nextInt(12), kind = rnd.nextInt(3);
                if (kind == 0) { m.addRange(l, r); for (int x = l; x < r; x++) on[x] = true; }
                else if (kind == 1) { m.removeRange(l, r); for (int x = l; x < r; x++) on[x] = false; }
                else {
                    long expect = l;                                // oracle: scan upward to the first untracked integer
                    while (on[(int) expect]) expect++;
                    if (m.nextUncovered(l) != expect) throw new AssertionError("next, trial " + trial);
                }
                int count = 0;
                for (boolean x : on) if (x) count++;
                if (m.trackedCount() != count) throw new AssertionError("count, trial " + trial);
            }
        }
    }
}
```

#### Solution: [Boundary] Counting Covered Integers On A Huge Line (LeetCode 2276)
<!-- id: dq39-huge-line-coverage -->

**Approach.** The class uses a dynamic segment tree whose root owns the half-open range from 0 up to `limit`. Each node stores how many integers of its range are covered. The invariant is that a node is full exactly when its count equals its range size, that a full node has no children, and that every other node's count is the sum of its two children.

An add converts the closed pair into the half-open range from `left` to `right + 1`, which cannot overflow because `right` is below `limit`. A node that is already full returns immediately. A node inside the new range becomes full and drops both children, and that drop is the multi-interval merge: every smaller covered run below the node is swallowed in constant time, and the count stays exact because the node's own count is set to its size. A node that only overlaps creates its two children on first use, recurses into the halves that the range reaches, and recomputes its count from them. The midpoint is `lo + (hi - lo) / 2`, which stays correct for ranges up to `10^18`. A window count adds the stored count of every node inside the window and, for a full node that only overlaps, the size of the overlap.

**Complexity.**

- **Time** is O(log limit) per call, because at each level at most two nodes are partial and every other visited node stops at once.
- **Space** is O(log limit) new nodes per add and O(calls * log limit) in total, and swallowed subtrees return their nodes to the garbage collector.

```java run
import java.util.*;

public final class HugeLine {
    /** Counts covered integers on [0, limit) with a dynamic segment tree that only grows along touched paths. */
    static final class CoverageTree {
        /** A node owns a half-open coordinate range and stores how many of its integers are covered. */
        private static final class Node {
            Node left, right;                    // both null for an untouched or fully covered node, both set otherwise
            long covered;                        // covered integers inside the owned range
        }

        private final long limit;                // coordinates are 0 .. limit - 1
        private final Node root = new Node();
        private int nodes = 1;                   // nodes ever created, kept to show the memory bound

        CoverageTree(long limit) {
            if (limit < 1 || limit > 1_000_000_000_000_000_000L) throw new IllegalArgumentException("limit");
            this.limit = limit;
        }

        /**
         * Covers the closed range [left, right]. Time: O(log limit), because every level visits at most two partial nodes.
         * Space: O(log limit) new nodes per call, and fully covered nodes drop their subtrees.
         * Invariant: a node is full exactly when covered equals its size, and a full node has no children.
         */
        void add(long left, long right) {
            if (left < 0 || right >= limit || left > right) throw new IllegalArgumentException("range");
            add(root, 0, limit, left, right + 1);   // convert the closed pair to the half-open range [left, right + 1)
        }

        private void add(Node node, long lo, long hi, long l, long r) {
            long size = hi - lo;                                  // size of the range this node owns
            if (node.covered == size) return;                     // already full, so nothing below can change
            if (l <= lo && hi <= r) {                             // the new range swallows this whole node
                node.covered = size;                              // the node becomes full
                node.left = null;                                 // drop every smaller run that the merge swallowed
                node.right = null;
                return;
            }
            long mid = lo + (hi - lo) / 2;                        // split point, written to avoid overflow
            if (node.left == null) {                              // first visit below this node
                node.left = new Node();
                node.right = new Node();
                nodes += 2;
            }
            if (l < mid) add(node.left, lo, mid, l, r);           // the range reaches the left half
            if (r > mid) add(node.right, mid, hi, l, r);          // the range reaches the right half
            node.covered = node.left.covered + node.right.covered; // recompute from the children, no double counting
        }

        /** Total covered integers. Time: O(1). Space: O(1). */
        long count() { return root.covered; }

        /**
         * Covered integers inside the closed range [left, right]. Time: O(log limit). Space: O(log limit) stack.
         */
        long countIn(long left, long right) {
            if (left < 0 || right >= limit || left > right) throw new IllegalArgumentException("range");
            return countIn(root, 0, limit, left, right + 1);
        }

        private long countIn(Node node, long lo, long hi, long l, long r) {
            if (node.covered == 0 || r <= lo || hi <= l) return 0;     // empty node or disjoint range
            if (l <= lo && hi <= r) return node.covered;               // node lies inside the query, take its stored count
            if (node.left == null) return Math.min(hi, r) - Math.max(lo, l); // full node: every overlapping integer is covered
            long mid = lo + (hi - lo) / 2;
            return countIn(node.left, lo, mid, l, r) + countIn(node.right, mid, hi, l, r); // add both halves
        }

        int nodeCount() { return nodes; }
    }

    public static void main(String[] args) {
        // Example 1: a later add swallows two stored runs and overlaps a third.
        CoverageTree a = new CoverageTree(100);
        a.add(10, 14); a.add(20, 24); a.add(40, 44);
        long c1 = a.count();
        a.add(12, 41);
        long c2 = a.count(), c3 = a.countIn(0, 19), c4 = a.countIn(42, 99);
        if (c1 != 15 || c2 != 35 || c3 != 10 || c4 != 3) throw new AssertionError("example 1 " + c1 + " " + c2 + " " + c3 + " " + c4);
        // Example 2: the largest coordinate and the largest limit.
        long big = 1_000_000_000_000_000_000L;
        CoverageTree b = new CoverageTree(big);
        b.add(0, big - 1);
        long d1 = b.count();
        b.add(5, 7);
        long d2 = b.count(), d3 = b.countIn(big - 10, big - 1);
        if (d1 != big || d2 != big || d3 != 10) throw new AssertionError("example 2");
        // A single add on the huge line creates only O(log limit) nodes.
        CoverageTree c = new CoverageTree(big);
        c.add(123456789012345678L, 987654321098765432L);
        if (c.nodeCount() > 4 * 61) throw new AssertionError("node bound " + c.nodeCount());
        // Random closed ranges against a boolean array, for several limits including powers of two and odd sizes.
        Random rnd = new Random(2276);
        for (int trial = 0; trial < 5000; trial++) {
            int limit = 1 + rnd.nextInt(70);
            CoverageTree t = new CoverageTree(limit);
            boolean[] on = new boolean[limit];
            for (int step = 0; step < 30; step++) {
                int l = rnd.nextInt(limit), r = l + rnd.nextInt(Math.min(12, limit - l));
                t.add(l, r);
                for (int x = l; x <= r; x++) on[x] = true;
                int ql = rnd.nextInt(limit), qr = ql + rnd.nextInt(limit - ql), total = 0, part = 0;
                for (int x = 0; x < limit; x++) {
                    if (on[x]) total++;
                    if (on[x] && x >= ql && x <= qr) part++;
                }
                if (t.count() != total || t.countIn(ql, qr) != part) throw new AssertionError("trial " + trial);
            }
            if (t.nodeCount() > 1 + 30 * 2 * 2 * 8) throw new AssertionError("nodes");
        }
    }
}
```

#### Solution: [Recognize] Dynamic Coverage API (Author exercise)
<!-- id: dq39-dynamic-coverage-api -->

**Approach.** The public class holds one internal state and picks it in the constructor from the two facts the caller knows: the domain size and whether sub-range counts will be asked. A domain of at most 64 integers fits in one `long`, where a range is a bit window and a count is a population count. Any larger domain with no sub-range counts uses an ordered map of runs, whose memory follows the number of runs and whose total is a stored field. A larger domain with sub-range counts uses the dynamic segment tree, because the map cannot count inside a window without visiting every run there.

Each state keeps its own invariant through removal. The mask clears a window with a bitwise complement. The map first cuts the range out of every overlapping run, keeps the left and right pieces, and only then fuses a new range with touching neighbours when the call is an add. The tree assigns a uniform value to a node that the range covers completely, and when a partial change reaches a uniform node, it splits the node into two children that inherit the uniform value. After the recursion, a node whose count is zero or its full size collapses back to a childless node, which keeps the tree in one canonical shape. The shift by 64 in the mask case is handled separately, because Java reduces a long shift distance modulo 64.

**Complexity.**

- **Time** is O(1) for the mask, O(log n) plus the number of runs cut for the map, and O(log domain) for the tree, per call.
- **Space** is O(1) for the mask, O(n) for the map with `n` runs, and O(calls * log domain) nodes for the tree in the worst case.

```java run
import java.util.*;

public final class DynamicCoverageApi {
    /** One state behind the public API; every range is half-open [l, r) with 0 <= l < r <= domain. */
    interface State {
        void set(long l, long r, boolean on);   // covers or uncovers every integer in [l, r)
        long covered(long l, long r);           // covered integers inside [l, r)
        long total();                           // covered integers overall
    }

    /**
     * Domain of at most 64 integers: one bit per integer.
     * Time: O(1) per call. Space: O(1), one long.
     * Invariant: bit x is set exactly when integer x is covered.
     */
    static final class MaskState implements State {
        private long bits;                                       // the whole state fits in one word

        private long window(long l, long r) {                    // bits l .. r - 1
            long len = r - l;                                    // number of bits in the window
            return len == 64 ? -1L : ((1L << len) - 1) << l;     // a shift by 64 would wrap, so the full window is special
        }

        public void set(long l, long r, boolean on) {
            long w = window(l, r);
            bits = on ? bits | w : bits & ~w;                    // set or clear the window with one operation
        }

        public long covered(long l, long r) { return Long.bitCount(bits & window(l, r)); } // popcount of the masked window

        public long total() { return Long.bitCount(bits); }
    }

    /**
     * Ordered map of disjoint, non-touching runs.
     * Time: O(log n) per call plus O(runs removed). Space: O(n) for n runs, independent of the domain size.
     * Invariant: runs are sorted, disjoint and never touch, and total equals the sum of end - start.
     */
    static final class RunState implements State {
        private final TreeMap<Long, Long> runs = new TreeMap<>();   // start -> end, with end exclusive
        private long total;                                         // covered integers, maintained by every write

        public void set(long l, long r, boolean on) {
            // Step 1: cut [l, r) out of the map so every overlapping run keeps only the pieces outside it.
            Map.Entry<Long, Long> e = runs.lowerEntry(r);           // the last run that starts before r
            while (e != null && e.getValue() > l) {                 // that run reaches into [l, r)
                long s = e.getKey(), t = e.getValue();
                runs.remove(s);                                     // take the whole run out
                total -= t - s;                                     // and take back its length
                if (s < l) { runs.put(s, l); total += l - s; }      // the piece left of the cut survives
                if (t > r) { runs.put(r, t); total += t - r; }      // the piece right of the cut survives
                e = runs.lowerEntry(r);                             // the next candidate; surviving pieces no longer qualify
            }
            if (!on) return;                                        // an uncover is finished after the cut
            // Step 2: insert [l, r) and fuse it with runs that touch either end.
            long s = l, t = r;
            Map.Entry<Long, Long> left = runs.floorEntry(l);        // a run starting at or before l
            if (left != null && left.getValue() == l) {             // it ends exactly at l, so the two touch
                s = left.getKey();
                runs.remove(s);
                total -= l - s;
            }
            Long right = runs.get(r);                               // a run starting exactly at r touches on the right
            if (right != null) {
                t = right;
                runs.remove(r);
                total -= right - r;
            }
            runs.put(s, t);                                         // one fused run replaces up to three
            total += t - s;
        }

        public long covered(long l, long r) {
            throw new UnsupportedOperationException("range counts need the tree state"); // a map walk would cost O(runs)
        }

        public long total() { return total; }
    }

    /**
     * Dynamic segment tree with assign-cover and assign-uncover.
     * Time: O(log domain) per call. Space: O(operations * log domain) nodes in the worst case.
     * Invariant: a node with no children is uniform (all covered or none), and covered is the sum over its range.
     */
    static final class TreeState implements State {
        private static final class Node { Node left, right; long covered; }
        private final long domain;
        private final Node root = new Node();

        TreeState(long domain) { this.domain = domain; }

        public void set(long l, long r, boolean on) { assign(root, 0, domain, l, r, on); }

        private void assign(Node n, long lo, long hi, long l, long r, boolean on) {
            long size = hi - lo;
            if (l <= lo && hi <= r) {                               // the change covers this node completely
                n.covered = on ? size : 0;                          // the node becomes uniform
                n.left = n.right = null;                            // children are no longer needed
                return;
            }
            long mid = lo + size / 2;                               // split point, overflow-safe
            if (n.left == null) {                                   // a uniform node meets a partial change
                if (n.covered == (on ? size : 0)) return;           // it already equals the target, so nothing changes
                n.left = new Node();
                n.right = new Node();
                if (n.covered == size) {                            // push the full state down to both halves
                    n.left.covered = mid - lo;
                    n.right.covered = hi - mid;
                }
            }
            if (l < mid) assign(n.left, lo, mid, l, r, on);        // the range reaches the left half
            if (r > mid) assign(n.right, mid, hi, l, r, on);        // the range reaches the right half
            n.covered = n.left.covered + n.right.covered;          // recompute from the children
            if (n.covered == 0 || n.covered == size) n.left = n.right = null; // collapse back to a uniform node
        }

        public long covered(long l, long r) { return count(root, 0, domain, l, r); }

        private long count(Node n, long lo, long hi, long l, long r) {
            if (n.covered == 0 || r <= lo || hi <= l) return 0;     // empty node or disjoint range
            if (l <= lo && hi <= r) return n.covered;               // node inside the query
            if (n.left == null) return Math.min(hi, r) - Math.max(lo, l); // uniform full node: count the overlap
            long mid = lo + (hi - lo) / 2;
            return count(n.left, lo, mid, l, r) + count(n.right, mid, hi, l, r);
        }

        public long total() { return root.covered; }
    }

    /** The public API; it picks one state at construction from the domain size and the query set. */
    static final class DynamicCoverage {
        private final long domain;
        private final State state;
        private final String backend;

        DynamicCoverage(long domain, boolean rangeCounts) {
            if (domain < 1 || domain > 1_000_000_000_000_000_000L) throw new IllegalArgumentException("domain");
            this.domain = domain;
            if (domain <= 64) { state = new MaskState(); backend = "mask"; }              // one word holds every integer
            else if (!rangeCounts) { state = new RunState(); backend = "runs"; }          // no sub-range counts, so runs suffice
            else { state = new TreeState(domain); backend = "tree"; }                     // sub-range counts over a large domain
        }

        String backend() { return backend; }

        private void check(long l, long r) { if (l < 0 || r > domain || l > r) throw new IllegalArgumentException("range"); }

        void add(long l, long r) { check(l, r); if (l < r) state.set(l, r, true); }      // an empty range changes nothing

        void remove(long l, long r) { check(l, r); if (l < r) state.set(l, r, false); }

        long total() { return state.total(); }

        long coveredIn(long l, long r) { check(l, r); return l == r ? 0 : state.covered(l, r); }
    }

    public static void main(String[] args) {
        // Example 1a: a tiny domain uses the mask, and a removal splits a covered stretch.
        DynamicCoverage a = new DynamicCoverage(40, true);
        a.add(3, 10); a.add(8, 20); a.remove(5, 6);
        if (!a.backend().equals("mask") || a.total() != 16 || a.coveredIn(0, 8) != 4) throw new AssertionError("example 1a");
        // Example 1b: no range counts on a large domain uses runs, and a range count is rejected.
        DynamicCoverage b = new DynamicCoverage(1_000_000_000L, false);
        b.add(100, 200); b.add(200, 300); b.remove(150, 250); b.add(1000, 1000);
        boolean threw = false;
        try { b.coveredIn(0, 10); } catch (UnsupportedOperationException ex) { threw = true; }
        if (!b.backend().equals("runs") || b.total() != 100 || !threw) throw new AssertionError("example 1b");
        // Example 2: range counts on a huge domain use the tree.
        long t12 = 1_000_000_000_000L;
        DynamicCoverage c = new DynamicCoverage(t12, true);
        c.add(0, t12 / 2); c.remove(t12 / 10, t12 / 5);
        if (!c.backend().equals("tree") || c.total() != 4 * (t12 / 10) || c.coveredIn(0, 3 * (t12 / 10)) != 2 * (t12 / 10))
            throw new AssertionError("example 2");
        // The boundary of a full 64-integer domain must not wrap the shift.
        DynamicCoverage full = new DynamicCoverage(64, true);
        full.add(0, 64);
        if (full.total() != 64 || full.coveredIn(0, 64) != 64) throw new AssertionError("64-bit window");
        // Random operations against a boolean array for all three states.
        Random rnd = new Random(2603);
        for (int trial = 0; trial < 6000; trial++) {
            int domain = 1 + rnd.nextInt(trial % 3 == 0 ? 64 : 150);
            boolean counts = rnd.nextBoolean();
            DynamicCoverage d = new DynamicCoverage(domain, counts);
            boolean[] on = new boolean[domain];
            for (int step = 0; step < 40; step++) {
                int l = rnd.nextInt(domain + 1), r = l + rnd.nextInt(domain - l + 1);
                boolean add = rnd.nextBoolean();
                if (add) d.add(l, r); else d.remove(l, r);
                for (int x = l; x < r; x++) on[x] = add;
                int total = 0;
                for (boolean x : on) if (x) total++;
                if (d.total() != total) throw new AssertionError("total, trial " + trial);
                if (!d.backend().equals("runs")) {
                    int ql = rnd.nextInt(domain + 1), qr = ql + rnd.nextInt(domain - ql + 1), part = 0;
                    for (int x = ql; x < qr; x++) if (on[x]) part++;
                    if (d.coveredIn(ql, qr) != part) throw new AssertionError("coveredIn, trial " + trial);
                }
            }
        }
    }
}
```
