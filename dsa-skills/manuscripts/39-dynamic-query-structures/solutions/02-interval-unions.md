<!-- solutions-for: 02-interval-unions -->
### Solutions For Interval Unions

#### Solution: [Build] Data Stream as Disjoint Intervals (LeetCode 352)
<!-- id: dq39-stream-intervals -->

**Approach.** The class stores every run of seen values as a half-open entry `[start, end)` in a `TreeMap`, keyed by start. The invariant is that entries are disjoint, sorted and never touch, so each run has exactly one entry.

A new value `v` first checks the floor entry of `v`. If that entry already reaches past `v`, the value is a duplicate and the call stops. Otherwise `v` can join the entry on its left when that entry ends exactly at `v`, and it can join the entry on its right when one starts exactly at `v + 1`. The four combinations of those two tests create a fresh entry, extend one entry, or fuse two entries into one. Only one point enters per call, so at most two entries change. `getIntervals` walks the map and prints each end minus 1, which converts the half-open end back to the closed endpoint.

**Complexity.**

- **Time** is O(log n) per `addNum` for the floor lookup and at most three map writes, and O(n) per `getIntervals` for the output size, where `n` is the number of stored runs.
- **Space** is O(n) for the entries, with one entry per run of consecutive seen values.

```java run
import java.util.*;

public final class StreamIntervals {
    /** Stores runs of seen values as half-open entries [start, end) keyed by start. */
    static final class SummaryRanges {
        // Invariant: entries are disjoint, sorted by start, and no two entries touch.
        private final TreeMap<Long, Long> ends = new TreeMap<>();

        /**
         * Records v by translating the closed point v into the range [v, v + 1).
         * Time: O(log n), because one floor lookup and at most three map writes run.
         * Space: O(1) extra, because at most one entry is added per call.
         */
        void addNum(int v) {
            // Work in long so that v + 1 never overflows near the int limit.
            long s = v, e = (long) v + 1;
            // The floor entry is the only stored range that can contain or touch v from the left.
            Map.Entry<Long, Long> left = ends.floorEntry(s);
            // A floor entry reaching past v means v is already seen, so nothing changes.
            if (left != null && left.getValue() > s) return;
            // A floor entry that ends exactly at v touches the new range, so absorb it.
            if (left != null && left.getValue() == s) { s = left.getKey(); ends.remove(s); }
            // An entry that starts exactly at v + 1 touches from the right, so absorb it too.
            Long rightEnd = ends.get(e);
            if (rightEnd != null) { ends.remove(e); e = rightEnd; }
            // Store the merged run, which restores the disjoint and untouching invariant.
            ends.put(s, e);
        }

        /**
         * Returns the runs as closed pairs sorted by start.
         * Time: O(n), because each stored run produces one output pair.
         * Space: O(n), because the answer array has one row per run.
         */
        int[][] getIntervals() {
            // Allocate one row per stored run.
            int[][] out = new int[ends.size()][];
            int i = 0;
            // Iterate in key order, so the pairs come out sorted by start.
            for (Map.Entry<Long, Long> en : ends.entrySet())
                // Convert the half-open end back to the closed endpoint by subtracting 1.
                out[i++] = new int[] {(int) (long) en.getKey(), (int) (en.getValue() - 1)};
            // Return the fresh array, which the caller may modify freely.
            return out;
        }
    }

    /** Brute-force oracle: marks seen values in a boolean array and scans for runs. */
    static int[][] oracle(boolean[] seen) {
        List<int[]> runs = new ArrayList<>();
        // Scan every coordinate once.
        for (int i = 0; i < seen.length; i++) {
            // Skip unseen coordinates.
            if (!seen[i]) continue;
            int j = i;
            // Extend j to the last seen coordinate of the run.
            while (j + 1 < seen.length && seen[j + 1]) j++;
            runs.add(new int[] {i, j});
            i = j;
        }
        return runs.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // Checks Example 1: three separate points, then 2 fuses the first run.
        SummaryRanges s = new SummaryRanges();
        s.addNum(1); s.addNum(3); s.addNum(7);
        if (!Arrays.deepEquals(s.getIntervals(), new int[][] {{1, 1}, {3, 3}, {7, 7}})) throw new AssertionError("example 1 before");
        s.addNum(2);
        if (!Arrays.deepEquals(s.getIntervals(), new int[][] {{1, 3}, {7, 7}})) throw new AssertionError("example 1 after");
        // Checks Example 2: a repeated value changes nothing.
        SummaryRanges d = new SummaryRanges();
        d.addNum(5); d.addNum(5); d.addNum(4);
        if (!Arrays.deepEquals(d.getIntervals(), new int[][] {{4, 5}})) throw new AssertionError("example 2");
        // Checks the empty stream and the largest allowed value.
        if (new SummaryRanges().getIntervals().length != 0) throw new AssertionError("empty stream");
        SummaryRanges big = new SummaryRanges();
        big.addNum(Integer.MAX_VALUE);
        if (!Arrays.deepEquals(big.getIntervals(), new int[][] {{Integer.MAX_VALUE, Integer.MAX_VALUE}})) throw new AssertionError("max int");
        // Checks the map against the oracle after every call on 3,000 random streams.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            SummaryRanges sr = new SummaryRanges();
            boolean[] seen = new boolean[30];
            for (int k = 0; k < 25; k++) {
                int v = rnd.nextInt(30);
                sr.addNum(v);
                seen[v] = true;
                if (!Arrays.deepEquals(sr.getIntervals(), oracle(seen))) throw new AssertionError("stream mismatch");
            }
        }
    }
}
```

#### Solution: [Vary] Range Module (LeetCode 715)
<!-- id: dq39-range-module -->

**Approach.** The module keeps the same invariant as the stream: disjoint, sorted half-open entries in a `TreeMap`, where touching entries are merged. Every method runs a window over the map instead of a single lookup.

For `addRange`, the window starts at the floor entry of `left` when that entry reaches `left`, and ends at the last start that is at most `right`. A sub-map view holds exactly the entries to absorb. The new end is the maximum of `right` and all absorbed ends, then the view is cleared and one entry is inserted. For `removeRange`, the only entry that can stick out on the left is the one with the greatest start below `left`, and it is trimmed to end at `left`. The entries with starts inside `[left, right)` all vanish, and the largest end seen among the trimmed and vanished entries becomes a surviving tail entry `[right, end)` when it exceeds `right`. A query reads the floor entry of `left` and compares its end with `right`.

**Complexity.**

- **Time** is O(log n) plus the number of absorbed entries per call, which is amortized O(log n) because each entry is created once and deleted at most once.
- **Space** is O(n) for the entries, where `n` is the number of stored runs.

```java run
import java.util.*;

public final class RangeModuleSolution {
    /** Tracks integers as disjoint half-open ranges [start, end) keyed by start. */
    static final class RangeModule {
        // Invariant: entries are disjoint, sorted by start, and touching entries are merged.
        private final TreeMap<Long, Long> ends = new TreeMap<>();

        /**
         * Tracks every integer of [left, right).
         * Time: O(log n) plus absorbed entries, amortized O(log n) per call.
         * Space: O(1) extra, because one entry is inserted per call.
         */
        void addRange(long left, long right) {
            // An empty range tracks nothing.
            if (left >= right) return;
            long lo = left, hi = right;
            // A floor entry that reaches left (touching counts) extends the new range backward.
            Map.Entry<Long, Long> f = ends.floorEntry(left);
            if (f != null && f.getValue() >= left) lo = f.getKey();
            // The view holds every entry that starts in [lo, right], all of which overlap or touch.
            NavigableMap<Long, Long> hit = ends.subMap(lo, true, right, true);
            // The merged end is the largest end among the new range and the absorbed entries.
            for (long e : hit.values()) hi = Math.max(hi, e);
            // Clearing the view deletes the absorbed entries from the backing map.
            hit.clear();
            // One merged entry restores the invariant.
            ends.put(lo, hi);
        }

        /**
         * Untracks every integer of [left, right).
         * Time: O(log n) plus removed entries, amortized O(log n) per call.
         * Space: O(1) extra, because at most one tail entry is inserted.
         */
        void removeRange(long left, long right) {
            // An empty range untracks nothing.
            if (left >= right) return;
            long tail = -1;
            // Only the entry with the greatest start below left can stick out to the left.
            Map.Entry<Long, Long> f = ends.lowerEntry(left);
            if (f != null && f.getValue() > left) {
                // Remember its old end, because the part past right must survive.
                tail = f.getValue();
                // Trim it so that it ends at left.
                ends.put(f.getKey(), left);
            }
            // Entries starting in [left, right) lie fully or partly inside the removed range.
            NavigableMap<Long, Long> mid = ends.subMap(left, true, right, false);
            for (long e : mid.values()) tail = Math.max(tail, e);
            mid.clear();
            // A tail past right survives as one entry, because the last cut entry covers [right, tail).
            if (tail > right) ends.put(right, tail);
        }

        /**
         * Returns true when every integer of [left, right) is tracked.
         * Time: O(log n), because one floor lookup runs.
         * Space: O(1), because nothing is allocated.
         */
        boolean queryRange(long left, long right) {
            // An empty or reversed range holds no integer, so it is trivially tracked.
            if (left >= right) return true;
            // Disjoint merged entries leave the floor entry of left as the only candidate.
            Map.Entry<Long, Long> f = ends.floorEntry(left);
            // The range is tracked only when that entry reaches right (end is exclusive).
            return f != null && f.getValue() >= right;
        }
    }

    public static void main(String[] args) {
        // Checks Example 1: a removal splits the added range.
        RangeModule m = new RangeModule();
        m.addRange(10, 20); m.removeRange(14, 16);
        if (!m.queryRange(10, 14) || m.queryRange(13, 15) || !m.queryRange(16, 17)) throw new AssertionError("example 1");
        // Checks Example 2: touching ranges merge and a removal breaks them.
        RangeModule t = new RangeModule();
        t.addRange(5, 8); t.addRange(8, 10);
        if (!t.queryRange(5, 10)) throw new AssertionError("touching ranges merge");
        t.removeRange(8, 9);
        if (t.queryRange(5, 10)) throw new AssertionError("removal breaks the run");
        // Checks that an empty range is covered even on an empty module.
        if (!new RangeModule().queryRange(5, 5) || !m.queryRange(7, 7) || !m.queryRange(9, 3)) throw new AssertionError("empty range");
        // Checks coordinates near 10^9, which stay in long arithmetic.
        RangeModule b = new RangeModule();
        b.addRange(1, 1_000_000_000);
        if (!b.queryRange(5, 1_000_000_000) || b.queryRange(5, 1_000_000_001)) throw new AssertionError("large coordinates");
        // Checks every query against a boolean-array oracle after every call on random calls.
        Random rnd = new Random(3);
        for (int trial = 0; trial < 3000; trial++) {
            RangeModule rm = new RangeModule();
            boolean[] cov = new boolean[40];
            for (int k = 0; k < 30; k++) {
                int l = rnd.nextInt(39), r = l + 1 + rnd.nextInt(40 - l);
                int op = rnd.nextInt(3);
                if (op == 0) { rm.addRange(l, r); for (int x = l; x < r; x++) cov[x] = true; }
                else if (op == 1) { rm.removeRange(l, r); for (int x = l; x < r; x++) cov[x] = false; }
                else {
                    // The oracle answers by testing each coordinate of the query.
                    boolean want = true;
                    for (int x = l; x < r; x++) if (!cov[x]) want = false;
                    if (rm.queryRange(l, r) != want) throw new AssertionError("query mismatch");
                }
            }
            // After the calls, every unit query agrees with the oracle.
            for (int x = 0; x < 40; x++) if (rm.queryRange(x, x + 1) != cov[x]) throw new AssertionError("final unit query");
        }
    }
}
```

#### Solution: [Boundary] Touching And Empty Ranges (Author exercise)
<!-- id: dq39-touching-empty -->

**Approach.** The structure is the same disjoint map of half-open entries, but each operation first extracts every entry that it affects and then reinserts the result. Extraction walks downward from the greatest start that can matter and stops at the first entry that is out of reach, which is valid because disjoint sorted entries also have sorted ends.

The touching test is the only difference between the two operations. An add extracts entries with `start <= r` and `end >= l`, so equal endpoints merge. A remove extracts entries with `start < r` and `end > l`, so an entry that merely touches stays untouched. Extraction returns the union bounds `lo` and `hi` of the removed entries and the operation range. An add reinserts `[lo, hi)`. A remove reinserts `[lo, l)` when `lo < l` and `[r, hi)` when `hi > r`. An operation with `l == r` returns before extraction, which keeps empty ranges from splitting or creating entries. The answer after each operation is the map size.

**Complexity.**

- **Time** is O(m log m) for `m` operations, because each operation does one lookup and one deletion per absorbed entry, and absorbed entries are amortized against creations.
- **Space** is O(m) for the entries in the worst case, plus O(m) for the answer array.

```java run
import java.util.*;

public final class TouchingEmpty {
    /** Applies add and remove operations on half-open ranges and reports the run count after each. */
    static final class Coverage {
        // Invariant: entries [start, end) are disjoint, sorted and never touch.
        private final TreeMap<Long, Long> ends = new TreeMap<>();

        /**
         * Removes every entry that intersects [l, r) (or touches it when touching is true)
         * and returns the bounds {lo, hi} of the union of those entries with [l, r).
         * Time: O(log n) plus removed entries, amortized O(log n) per call.
         * Space: O(1) extra.
         */
        private long[] extract(long l, long r, boolean touching) {
            long lo = l, hi = r;
            while (true) {
                // The greatest start that may reach the range: at most r when touching, below r otherwise.
                Map.Entry<Long, Long> e = ends.floorEntry(touching ? r : r - 1);
                // No candidate remains, so extraction ends.
                if (e == null) break;
                // Touching ends count as a hit for add (end >= l), and not for remove (end > l).
                boolean hit = touching ? e.getValue() >= l : e.getValue() > l;
                // Ends are sorted like starts, so the first miss ends the walk.
                if (!hit) break;
                // Grow the union bounds to include the extracted entry.
                lo = Math.min(lo, e.getKey());
                hi = Math.max(hi, e.getValue());
                ends.remove(e.getKey());
            }
            return new long[] {lo, hi};
        }

        /**
         * Applies one operation and restores the invariant.
         * Time: O(log n) amortized. Space: O(1) extra.
         */
        void apply(boolean add, long l, long r) {
            // An empty range contains no integers, so the coverage cannot change.
            if (l == r) return;
            if (add) {
                // Merge on equal endpoints and store the union as one entry.
                long[] b = extract(l, r, true);
                ends.put(b[0], b[1]);
            } else {
                // Cut without merging on equal endpoints, then reinsert the surviving sides.
                long[] b = extract(l, r, false);
                if (b[0] < l) ends.put(b[0], l);
                if (b[1] > r) ends.put(r, b[1]);
            }
        }

        int runs() {
            return ends.size();
        }
    }

    /**
     * Returns the run count after each operation; each op is {type, l, r} with type 1 for add.
     * Time: O(m log m) overall. Space: O(m).
     */
    static long[] runCounts(long[][] ops) {
        Coverage c = new Coverage();
        long[] out = new long[ops.length];
        // One pass applies each operation, then records the run count (the update/query ratio is 1 to 1).
        for (int i = 0; i < ops.length; i++) {
            c.apply(ops[i][0] == 1, ops[i][1], ops[i][2]);
            out[i] = c.runs();
        }
        return out;
    }

    /** Brute-force oracle using a boolean array and a run scan after each operation. */
    static long[] oracle(long[][] ops, int n) {
        boolean[] cov = new boolean[n];
        long[] out = new long[ops.length];
        for (int i = 0; i < ops.length; i++) {
            // Set or clear each coordinate of the half-open range.
            for (int x = (int) ops[i][1]; x < (int) ops[i][2]; x++) cov[x] = ops[i][0] == 1;
            // Count the positions where a covered coordinate follows an uncovered one.
            long runs = 0;
            for (int x = 0; x < n; x++) if (cov[x] && (x == 0 || !cov[x - 1])) runs++;
            out[i] = runs;
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1: touching adds merge, and the empty remove changes nothing.
        long[][] e1 = {{1, 1, 3}, {1, 5, 7}, {1, 3, 5}, {0, 2, 2}, {0, 3, 5}};
        if (!Arrays.equals(runCounts(e1), new long[] {1, 2, 1, 1, 2})) throw new AssertionError("example 1");
        // Checks Example 2: removing everything and empty operations leave no runs.
        long[][] e2 = {{1, 0, 4}, {0, 0, 4}, {1, 2, 2}, {0, 1, 3}};
        if (!Arrays.equals(runCounts(e2), new long[] {1, 0, 0, 0})) throw new AssertionError("example 2");
        // Checks that a remove touching an entry from outside leaves it whole.
        if (!Arrays.equals(runCounts(new long[][] {{1, 5, 9}, {0, 9, 12}, {0, 0, 5}}), new long[] {1, 1, 1})) throw new AssertionError("remove touching");
        // Checks the largest allowed coordinate in long arithmetic.
        if (!Arrays.equals(runCounts(new long[][] {{1, 0, 1_000_000_000_000L}, {0, 1, 1_000_000_000_000L}}), new long[] {1, 1})) throw new AssertionError("large coordinates");
        // Compares with the oracle on 5,000 random operation lists, including empty ranges.
        Random rnd = new Random(5);
        for (int t = 0; t < 5000; t++) {
            long[][] ops = new long[25][];
            for (int i = 0; i < ops.length; i++) {
                int l = rnd.nextInt(21), r = l + rnd.nextInt(21 - l);
                ops[i] = new long[] {rnd.nextInt(2), l, r};
            }
            if (!Arrays.equals(runCounts(ops), oracle(ops, 20))) throw new AssertionError("oracle mismatch");
        }
    }
}
```

#### Solution: [Recognize] Count Integers in Intervals (LeetCode 2276)
<!-- id: dq39-count-intervals -->

**Approach.** The domain reaches 10^9, so an array is too large, and a segment tree over that domain needs dynamic nodes. A sorted map of merged half-open entries is smaller because it stores one record per run, and the workload only adds and counts. The closed pair `[left, right]` converts to `[left, right + 1)`.

The class keeps `total`, the sum of all entry lengths, and updates it during each add. An add finds the start of the merge window from the floor entry of `left` and then iterates the map forward from that start. Each visited entry whose start is at most the growing end is removed, its length is subtracted from `total`, and its end extends the window. The merged entry is inserted and its length is added. `count` returns the field in O(1). The invariant is that `total` equals the sum of `end - start` over the entries.

**Complexity.**

- **Time** is O(log n) amortized per `add`, because each entry is inserted once and removed at most once, and O(1) per `count`.
- **Space** is O(n) for the entries, where `n` is the number of stored runs, and never more than the number of `add` calls.

```java run
import java.util.*;

public final class CountIntervalsSolution {
    /** Counts covered integers with merged half-open ranges and a running total. */
    static final class CountIntervals {
        // Invariant: entries are disjoint and merged, and total is the sum of end - start.
        private final TreeMap<Long, Long> ends = new TreeMap<>();
        private long total;

        /**
         * Marks the closed pair [left, right] as covered.
         * Time: O(log n) amortized, because merged entries are deleted once.
         * Space: O(1) extra, because one entry is inserted.
         */
        void add(long left, long right) {
            // Convert the closed pair to the half-open range [lo, hi).
            long lo = left, hi = right + 1;
            // A floor entry reaching lo (touching counts) moves the window start backward.
            Map.Entry<Long, Long> f = ends.floorEntry(lo);
            long from = (f != null && f.getValue() >= lo) ? f.getKey() : lo;
            lo = Math.min(lo, from);
            // Walk forward from the window start with an iterator that can delete entries.
            Iterator<Map.Entry<Long, Long>> it = ends.tailMap(from, true).entrySet().iterator();
            while (it.hasNext()) {
                Map.Entry<Long, Long> e = it.next();
                // An entry starting beyond the window end is separated by a gap, so the walk stops.
                if (e.getKey() > hi) break;
                // Widen the window and give back the old length of the absorbed entry.
                hi = Math.max(hi, e.getValue());
                total -= e.getValue() - e.getKey();
                it.remove();
            }
            // Store the merged entry and add its full length once.
            ends.put(lo, hi);
            total += hi - lo;
        }

        /**
         * Returns the number of covered integers.
         * Time: O(1). Space: O(1).
         */
        long count() {
            // The running total is exact by the invariant, so no walk is needed.
            return total;
        }
    }

    public static void main(String[] args) {
        // Checks Example 1: a merge across two entries.
        CountIntervals c = new CountIntervals();
        c.add(2, 3); c.add(7, 10);
        if (c.count() != 6) throw new AssertionError("example 1 first count");
        c.add(5, 8);
        if (c.count() != 8) throw new AssertionError("example 1 second count");
        // Checks Example 2: the total uses long and a covered re-add changes nothing.
        CountIntervals d = new CountIntervals();
        d.add(1, 1_000_000_000);
        if (d.count() != 1_000_000_000L) throw new AssertionError("big count");
        d.add(1, 3);
        if (d.count() != 1_000_000_000L) throw new AssertionError("covered re-add");
        // Checks that totals beyond the int range are exact, by adding two disjoint huge pieces.
        CountIntervals h = new CountIntervals();
        h.add(1, 1_000_000_000); h.add(1_500_000_000L, 2_500_000_000L);
        if (h.count() != 2_000_000_001L) throw new AssertionError("long total");
        // Compares every count with a boolean-array oracle on 4,000 random call lists.
        Random rnd = new Random(17);
        for (int t = 0; t < 4000; t++) {
            CountIntervals ci = new CountIntervals();
            boolean[] cov = new boolean[50];
            for (int k = 0; k < 20; k++) {
                int l = rnd.nextInt(49), r = l + rnd.nextInt(49 - l);
                ci.add(l, r);
                for (int x = l; x <= r; x++) cov[x] = true;
                long want = 0;
                for (boolean b : cov) if (b) want++;
                if (ci.count() != want) throw new AssertionError("count mismatch");
            }
        }
    }
}
```
