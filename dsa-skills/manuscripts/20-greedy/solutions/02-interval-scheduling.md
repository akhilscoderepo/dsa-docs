<!-- solutions-for: 20-greedy -->
### Interval Scheduling

#### Solution: [Build] Choose Compatible Meetings (Author exercise)
<!-- id: gr-compatible-meetings -->

**Approach.** Copy the outer array so the caller's row order survives, sort the copy by end time, and sweep once. A meeting is accepted when its start is at or after the end of the last accepted meeting, and acceptance moves the free boundary to its end. The assertions check both examples, confirm that the input order is unchanged, and compare the answer on random small calendars with an enumeration of every subset, where a subset is valid when every pair of members is disjoint under the half-open rule.

**Complexity.** The sort costs O(n log n) and the sweep is one pass, so the sort sets the total; the copy adds O(n) references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CompatibleMeetings {
    static int mostCompatible(int[][] req) {
        int[][] sorted = req.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        int kept = 0, freeAt = Integer.MIN_VALUE;
        for (int[] r : sorted) {
            if (r[0] >= freeAt) { kept++; freeAt = r[1]; }
        }
        return kept;
    }

    static int oracle(int[][] req) {
        int n = req.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                for (int j = i + 1; j < n && ok; j++) {
                    if ((mask >> j & 1) == 0) continue;
                    if (req[i][0] < req[j][1] && req[j][0] < req[i][1]) ok = false;
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        if (mostCompatible(new int[][]{{9, 11}, {9, 10}, {10, 12}, {11, 13}, {12, 14}}) != 3) throw new AssertionError("example 1");
        if (mostCompatible(new int[][]{{1, 2}, {1, 2}, {1, 2}}) != 1) throw new AssertionError("example 2");
        if (mostCompatible(new int[0][]) != 0) throw new AssertionError("empty calendar");
        if (mostCompatible(new int[][]{{0, 10}, {1, 2}, {3, 4}}) != 2) throw new AssertionError("the long request loses to two short ones");

        int[][] rows = {{5, 6}, {1, 2}, {3, 4}};
        mostCompatible(rows);
        if (rows[0][0] != 5 || rows[1][0] != 1 || rows[2][0] != 3) throw new AssertionError("input rows were reordered");

        Random rnd = new Random(2101);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(10);
            int[][] req = new int[n][];
            for (int i = 0; i < n; i++) {
                int s = rnd.nextInt(12);
                req[i] = new int[]{s, s + 1 + rnd.nextInt(6)};
            }
            if (mostCompatible(req) != oracle(req)) throw new AssertionError("disagrees with the subset search on " + Arrays.deepToString(req));
        }
    }
}
```

#### Solution: [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gr-non-overlapping-removals -->

**Approach.** Sort a copy by end with `Long.compare` and keep a span whenever its start is at or after the end of the last kept one. The answer is the total minus the kept count, because the kept spans form a largest conflict-free set, and everything outside it must go. The assertions check both examples, then show why the comparator matters: a subtracting comparator wraps for the ends in the second example and sorts them wrongly. Random cases draw endpoints from a pool that holds both `long` limits and are checked against a subset enumeration.

**Complexity.** One sort and one sweep give O(n log n) time, with the clone holding n row references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NonOverlappingRemovals {
    static int removals(long[][] intervals) {
        long[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Long.compare(a[1], b[1]));
        int kept = 0;
        boolean any = false;
        long freeAt = 0;
        for (long[] s : sorted) {
            if (!any || s[0] >= freeAt) { kept++; freeAt = s[1]; any = true; }
        }
        return intervals.length - kept;
    }

    static int oracle(long[][] iv) {
        int n = iv.length, bestKept = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                for (int j = i + 1; j < n && ok; j++) {
                    if ((mask >> j & 1) == 0) continue;
                    if (iv[i][0] < iv[j][1] && iv[j][0] < iv[i][1]) ok = false;
                }
            }
            if (ok) bestKept = Math.max(bestKept, Integer.bitCount(mask));
        }
        return n - bestKept;
    }

    public static void main(String[] args) {
        if (removals(new long[][]{{1, 3}, {2, 5}, {4, 6}, {3, 8}, {6, 9}}) != 2) throw new AssertionError("example 1");
        long[][] wide = {
            {-8000000000000000000L, 8000000000000000000L},
            {-9000000000000000000L, -8500000000000000000L},
            {7000000000000000000L, 9000000000000000000L}};
        if (removals(wide) != 1) throw new AssertionError("example 2");
        if (removals(new long[0][]) != 0) throw new AssertionError("empty input");
        if (removals(new long[][]{{1, 2}, {2, 3}, {3, 4}}) != 0) throw new AssertionError("touching spans do not overlap");

        long smallestEnd = -8500000000000000000L;
        long diff = 8000000000000000000L - smallestEnd;
        if (diff >= 0) throw new AssertionError("the difference of two far-apart longs must wrap negative");
        if (Long.compare(8000000000000000000L, smallestEnd) <= 0) throw new AssertionError("Long.compare keeps the true order");

        long[] pool = {Long.MIN_VALUE, -9000000000000000000L, -8500000000000000000L, -1, 0, 1,
                7000000000000000000L, 8000000000000000000L, 9000000000000000000L, Long.MAX_VALUE};
        Random rnd = new Random(2102);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            long[][] iv = new long[n][];
            for (int i = 0; i < n; i++) {
                long a, b;
                do { a = pool[rnd.nextInt(pool.length)]; b = pool[rnd.nextInt(pool.length)]; } while (a == b);
                iv[i] = new long[]{Math.min(a, b), Math.max(a, b)};
            }
            if (removals(iv) != oracle(iv)) throw new AssertionError("disagrees with the subset search on " + Arrays.deepToString(iv));
        }
    }
}
```

#### Solution: [Boundary] Touching Endpoint Contract (Author exercise)
<!-- id: gr-touching-endpoint-contract -->

**Approach.** Sort by end and sweep, with the acceptance test chosen by the contract. Under the half-open model a span is accepted when its start is at or after the last end. Under the closed model the test is a strict `>`, since equal values share a point, and a point span `[a, a]` sets the boundary to `a` so that a second copy is refused. The assertions check the first example under both flags, the point-span example, and random inputs against a subset enumeration that uses an explicit pairwise overlap test for each model.

**Complexity.** The sort dominates at O(n log n); the model flag adds no cost.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TouchingEndpointContract {
    static int most(int[][] spans, boolean closed) {
        int[][] sorted = spans.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        int kept = 0;
        long freeAt = Long.MIN_VALUE;
        for (int[] s : sorted) {
            boolean fits = closed ? s[0] > freeAt : s[0] >= freeAt;
            if (fits) { kept++; freeAt = s[1]; }
        }
        return kept;
    }

    static boolean overlap(int[] a, int[] b, boolean closed) {
        if (closed) return !(a[1] < b[0] || b[1] < a[0]);
        return a[0] < b[1] && b[0] < a[1];
    }

    static int oracle(int[][] sp, boolean closed) {
        int n = sp.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                for (int j = i + 1; j < n && ok; j++) {
                    if ((mask >> j & 1) == 1 && overlap(sp[i], sp[j], closed)) ok = false;
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] chain = {{1, 3}, {3, 5}, {5, 7}};
        if (most(chain, true) != 2) throw new AssertionError("example 1, closed");
        if (most(chain, false) != 3) throw new AssertionError("example 1, half-open");
        if (most(new int[][]{{4, 4}, {4, 4}, {5, 5}}, true) != 2) throw new AssertionError("example 2");
        if (most(new int[0][], true) != 0 || most(new int[0][], false) != 0) throw new AssertionError("empty input");
        if (most(new int[][]{{0, 0}}, true) != 1) throw new AssertionError("a lone point span at zero is accepted");

        Random rnd = new Random(2103);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(9);
            boolean closed = rnd.nextBoolean();
            int[][] sp = new int[n][];
            for (int i = 0; i < n; i++) {
                int a = rnd.nextInt(9);
                sp[i] = new int[]{a, a + (closed ? rnd.nextInt(4) : 1 + rnd.nextInt(4))};
            }
            if (most(sp, closed) != oracle(sp, closed)) throw new AssertionError("disagrees with the subset search, closed=" + closed + " " + Arrays.deepToString(sp));
        }
    }
}
```

#### Solution: [Recognize] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gr-arrows-by-group -->

**Approach.** Sort a copy by start. A balloon whose start is beyond the current group end needs a new arrow, so the shot count grows and the group end becomes that balloon's end. A balloon that starts at or before the group end joins the group, and the group end drops to the smaller of the two ends, because the arrow must still land inside every member. The group end is held in a `long` for the first-balloon case. The assertions check both examples and show that a subtracting comparator misorders `Integer.MIN_VALUE` against zero. Random balloons are checked against a search over every subset of candidate points taken from the balloon ends.

**Complexity.** Sorting gives O(n log n), the sweep adds a single pass, and the extra memory is the O(n) clone of row references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ArrowsByGroup {
    static int arrows(int[][] balloons) {
        int[][] sorted = balloons.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        int shots = 0;
        long groupEnd = Long.MIN_VALUE;
        for (int[] b : sorted) {
            if (shots == 0 || b[0] > groupEnd) { shots++; groupEnd = b[1]; }
            else groupEnd = Math.min(groupEnd, b[1]);
        }
        return shots;
    }

    static int oracle(int[][] bal) {
        int n = bal.length;
        if (n == 0) return 0;
        int best = n;
        for (int mask = 1; mask < (1 << n); mask++) {
            boolean all = true;
            for (int k = 0; k < n && all; k++) {
                boolean hit = false;
                for (int c = 0; c < n && !hit; c++) {
                    if ((mask >> c & 1) == 1 && bal[k][0] <= bal[c][1] && bal[c][1] <= bal[k][1]) hit = true;
                }
                if (!hit) all = false;
            }
            if (all) best = Math.min(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        if (arrows(new int[][]{{10, 16}, {2, 8}, {1, 6}, {7, 12}}) != 2) throw new AssertionError("example 1");
        if (arrows(new int[][]{{Integer.MIN_VALUE, 0}, {0, Integer.MAX_VALUE}}) != 1) throw new AssertionError("example 2");
        if (arrows(new int[0][]) != 0) throw new AssertionError("no balloons");
        if (arrows(new int[][]{{1, 2}, {3, 4}, {5, 6}}) != 3) throw new AssertionError("disjoint balloons need one arrow each");
        if (arrows(new int[][]{{1, 2}, {2, 3}}) != 1) throw new AssertionError("a shared endpoint counts as a hit");

        int[][] pair = {{Integer.MIN_VALUE, 0}, {0, 5}};
        Arrays.sort(pair, (a, b) -> a[0] - b[0]);
        if (pair[0][0] != 0) throw new AssertionError("the subtracting comparator should misorder these two rows");
        if (0 - Integer.MIN_VALUE >= 0) throw new AssertionError("the difference must wrap negative");

        int[] pool = {Integer.MIN_VALUE, -3, 0, 4, 9, Integer.MAX_VALUE};
        Random rnd = new Random(2104);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(8);
            int[][] bal = new int[n][];
            for (int i = 0; i < n; i++) {
                int a, b;
                if (rnd.nextInt(3) == 0) { a = pool[rnd.nextInt(pool.length)]; b = pool[rnd.nextInt(pool.length)]; }
                else { a = rnd.nextInt(10); b = rnd.nextInt(10); }
                bal[i] = new int[]{Math.min(a, b), Math.max(a, b)};
            }
            if (arrows(bal) != oracle(bal)) throw new AssertionError("disagrees with the subset search on " + Arrays.deepToString(bal));
        }
    }
}
```
