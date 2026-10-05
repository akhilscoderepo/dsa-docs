<!-- solutions-for: 10-intervals -->
### Solutions For Keeping The Most Intervals

#### Solution: [Build] Keep Earlier Finishing Interval (Author exercise)
<!-- id: iv-keep-earlier-finish -->

**Approach.**
After one interval is kept, the next kept interval must start at or after its end. A smaller end therefore allows every later interval that a larger end allows, and possibly more. The method compares the two ends and returns 0 when the first end is at most the second, and 1 otherwise. The method ignores the starts and the lengths, because only the end limits what follows. The invariant is that the kept interval admits at least as many later intervals as the discarded one.

**Complexity.**
- **Time** is O(1), because the method makes one comparison.
- **Space** is O(1), because the method stores no extra data.

```java run
import java.util.Random;

public final class KeepEarlier {
    /**
     * Returns 0 to keep the first interval and 1 to keep the second; the interval with the smaller end is kept.
     * Time: O(1), one comparison.
     * Space: O(1), nothing is stored.
     * Invariant: the kept interval admits every later interval that the other one admits.
     */
    static int keep(int[] a, int[] b) {
        // A smaller end leaves more room to the right; a tie keeps the first interval.
        return a[1] <= b[1] ? 0 : 1;
    }

    /** Counts how many of the later half-open intervals fit after the given kept interval. */
    static int room(int[] kept, int[][] later) {
        int c = 0;
        // A later interval fits when it shares no time with the kept one, so it lies fully to its right or left.
        for (int[] x : later) if (x[0] >= kept[1] || x[1] <= kept[0]) c++;
        return c;
    }

    public static void main(String[] args) {
        // Example 1: [2,3) ends first, so keep the second interval.
        if (keep(new int[] {1, 10}, new int[] {2, 3}) != 1) throw new AssertionError("example 1");
        // Example 2: the ends tie, so the first interval stays.
        if (keep(new int[] {1, 4}, new int[] {2, 4}) != 0) throw new AssertionError("example 2");
        // The kept interval never leaves less room than the discarded one, for later intervals that start at or after both starts.
        Random rnd = new Random(40);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(10), s2 = rnd.nextInt(10);
            int[] a = {s1, s1 + 1 + rnd.nextInt(8)}, b = {s2, s2 + 1 + rnd.nextInt(8)};
            // Skip pairs that do not overlap, because the exercise guarantees an overlap.
            if (Math.max(a[0], b[0]) >= Math.min(a[1], b[1])) continue;
            int lowest = Math.max(a[0], b[0]);
            int[][] later = new int[6][];
            for (int i = 0; i < later.length; i++) { int s = lowest + rnd.nextInt(14); later[i] = new int[] {s, s + 1 + rnd.nextInt(5)}; }
            int[] kept = keep(a, b) == 0 ? a : b, dropped = keep(a, b) == 0 ? b : a;
            if (room(kept, later) < room(dropped, later)) throw new AssertionError("room " + a[0] + b[0]);
        }
    }
}
```

#### Solution: [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: iv-non-overlapping -->

**Approach.**
The method sorts a clone by end and scans once while it keeps `lastEnd`, the end of the last kept interval. An interval whose start is at least `lastEnd` shares no time with the last kept interval, so the method keeps it and updates `lastEnd`. An interval that starts earlier clashes with the kept interval, and the method skips it, which counts as one removal. Keeping the earliest-ending interval is safe because exchanging it into any best set leaves that set valid, as the lesson shows. The answer is `n` minus the number kept. The invariant is that `lastEnd` is the smallest end that a largest compatible set of the processed intervals can have.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n), because the sorted clone holds `n` references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NonOverlapping {
    /**
     * Returns the minimum number of half-open intervals to remove so the rest do not overlap.
     * Time: O(n log n), the sort plus one scan.
     * Space: O(n), for the sorted clone.
     * Invariant: lastEnd is the smallest end of a largest compatible set of the processed intervals.
     */
    static int removals(int[][] intervals) {
        // Sort a clone by end so the earliest finishing interval comes first.
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        int kept = 0;
        // lastEnd starts below every int, so the first interval always fits.
        long lastEnd = Long.MIN_VALUE;
        // One pass: each interval is compared with the end of the last kept interval only.
        for (int[] s : sorted) {
            // A start at or after lastEnd shares no time with the kept interval, so keep it.
            if (s[0] >= lastEnd) { kept++; lastEnd = s[1]; }
        }
        // Every interval that was not kept is a removal.
        return intervals.length - kept;
    }

    /** Reference: the largest compatible subset by trying every subset. */
    static int brute(int[][] in) {
        int n = in.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) for (int j = i + 1; j < n && ok; j++)
                if ((mask >> i & 1) == 1 && (mask >> j & 1) == 1 && Math.max(in[i][0], in[j][0]) < Math.min(in[i][1], in[j][1])) ok = false;
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return n - best;
    }

    public static void main(String[] args) {
        // Example 1: keep [2,3) and [3,6), remove two.
        if (removals(new int[][] {{1, 4}, {2, 3}, {3, 6}, {5, 7}}) != 2) throw new AssertionError("example 1");
        // Example 2: touching half-open intervals do not overlap.
        if (removals(new int[][] {{0, 2}, {0, 2}, {2, 5}}) != 1) throw new AssertionError("example 2");
        // Empty input.
        if (removals(new int[0][]) != 0) throw new AssertionError("empty");
        // The opening room: keeping the first request gives one event, but three fit.
        if (removals(new int[][] {{1, 10}, {2, 3}, {4, 5}, {6, 7}}) != 1) throw new AssertionError("room");
        // Keeping the shortest request is a false friend: it keeps 1 here, while 2 fit.
        int[][] trap = {{1, 6}, {5, 7}, {6, 12}};
        if (removals(trap) != 1) throw new AssertionError("trap");
        // Random inputs agree with the exhaustive count.
        Random rnd = new Random(41);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(10); in[i] = new int[] {s, s + 1 + rnd.nextInt(5)}; }
            if (removals(in) != brute(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Boundary] Remove Covered Intervals (LeetCode 1288)
<!-- id: iv-remove-covered -->

**Approach.**
The method sorts a clone by start ascending, and by end descending when starts tie. In this order a container always comes before the intervals it holds, because an interval that holds another starts no later and ends no earlier. The scan keeps `maxEnd`, the largest end among the earlier intervals. An interval whose end is at most `maxEnd` is covered by an earlier interval with a start at or before its own, so the method skips it. Any other interval is not covered, and it raises `maxEnd`. The tie rule matters: with ascending ends, `[1,2)` would come before `[1,4)` and would look uncovered. The invariant is that `maxEnd` is the largest end among all earlier intervals in the order.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n), because the sorted clone holds `n` references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RemoveCovered {
    /**
     * Returns the number of intervals not covered by any other interval.
     * Time: O(n log n), the sort plus one scan.
     * Space: O(n), for the sorted clone.
     * Invariant: maxEnd is the largest end among the earlier intervals in start order.
     */
    static int countNotCovered(int[][] intervals, boolean descendingTie) {
        int[][] sorted = intervals.clone();
        // Sort by start; on equal starts put the larger end first so containers precede what they hold.
        Arrays.sort(sorted, (a, b) -> a[0] != b[0]
                ? Integer.compare(a[0], b[0])
                : (descendingTie ? Integer.compare(b[1], a[1]) : Integer.compare(a[1], b[1])));
        int notCovered = 0;
        // maxEnd starts below every int, so the first interval is never covered.
        long maxEnd = Long.MIN_VALUE;
        for (int[] s : sorted) {
            // A larger end than every earlier end means no earlier interval covers this one.
            if (s[1] > maxEnd) { notCovered++; maxEnd = s[1]; }
        }
        return notCovered;
    }

    /** Reference: test every ordered pair, except that equal intervals cover each other and only one copy survives. */
    static int brute(int[][] in) {
        int n = in.length, count = 0;
        for (int i = 0; i < n; i++) {
            boolean covered = false;
            for (int j = 0; j < n && !covered; j++) {
                if (i == j || !(in[j][0] <= in[i][0] && in[i][1] <= in[j][1])) continue;
                // An equal interval covers this one only when it comes earlier, so one copy remains.
                boolean equal = in[j][0] == in[i][0] && in[j][1] == in[i][1];
                covered = !equal || j < i;
            }
            if (!covered) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1: [1,5) and [4,9) remain.
        int[][] a = {{1, 5}, {1, 3}, {2, 5}, {4, 9}, {6, 9}};
        if (countNotCovered(a, true) != 2) throw new AssertionError("example 1");
        // Example 2: duplicates keep one copy.
        if (countNotCovered(new int[][] {{2, 6}, {2, 4}, {2, 6}}, true) != 1) throw new AssertionError("example 2");
        // Ascending ties give the wrong answer here: [1,2) looks uncovered before [1,4).
        if (countNotCovered(new int[][] {{1, 4}, {1, 2}}, false) == 1) throw new AssertionError("ascending ties should fail");
        if (countNotCovered(new int[][] {{1, 4}, {1, 2}}, true) != 1) throw new AssertionError("descending ties");
        // Random inputs agree with the pair-by-pair reference.
        Random rnd = new Random(42);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(8); in[i] = new int[] {s, s + 1 + rnd.nextInt(6)}; }
            if (countNotCovered(in, true) != brute(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Recognize] Minimum Number Of Arrows (LeetCode 452)
<!-- id: iv-min-arrows -->

**Approach.**
The method sorts a clone by end and shoots the first arrow at the smallest end. That arrow bursts every balloon that starts at or before the arrow position, because each later balloon ends at or after that position. The scan skips balloons whose start is at most the current arrow position. A balloon that starts after the arrow position needs a new arrow, which the method places at that balloon's end for the same reason. The comparison is `start <= arrow` because a shared coordinate counts as a hit under the closed model, which differs from the half-open selection exercise where touching intervals were compatible. The invariant is that the current arrow position bursts every balloon already processed. The sort uses `Integer.compare`, so the extreme values cause no overflow.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n), because the sorted clone holds `n` references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MinArrows {
    /**
     * Returns the fewest arrows needed to burst all closed balloons.
     * Time: O(n log n), the sort plus one scan.
     * Space: O(n), for the sorted clone.
     * Invariant: the current arrow position bursts every balloon already processed.
     */
    static int minArrows(int[][] balloons) {
        // No balloons need no arrows.
        if (balloons.length == 0) return 0;
        // Sort by end with Integer.compare, which cannot overflow for extreme values.
        int[][] sorted = balloons.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        int arrows = 1;
        // The first arrow is shot at the smallest end.
        long pos = sorted[0][1];
        // One pass over the remaining balloons.
        for (int i = 1; i < sorted.length; i++) {
            // A start after the arrow position means the arrow misses this balloon, so shoot a new one at its end.
            if (sorted[i][0] > pos) { arrows++; pos = sorted[i][1]; }
        }
        return arrows;
    }

    /** Reference: try every set of arrow positions drawn from the balloon ends, smallest set first. */
    static int brute(int[][] in) {
        int n = in.length;
        if (n == 0) return 0;
        int best = n;
        // Each mask picks which balloon ends receive an arrow; an optimal arrow can sit at some end.
        for (int mask = 1; mask < (1 << n); mask++) {
            boolean all = true;
            for (int i = 0; i < n && all; i++) {
                boolean hit = false;
                for (int k = 0; k < n && !hit; k++) hit = (mask >> k & 1) == 1 && in[i][0] <= in[k][1] && in[k][1] <= in[i][1];
                all = hit;
            }
            if (all) best = Math.min(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: arrows at 4, 9 and 12.
        if (minArrows(new int[][] {{1, 4}, {3, 8}, {7, 9}, {10, 12}}) != 3) throw new AssertionError("example 1");
        // Example 2: the extreme values need one arrow at 2147483647.
        if (minArrows(new int[][] {{Integer.MIN_VALUE, Integer.MAX_VALUE}, {Integer.MAX_VALUE, Integer.MAX_VALUE}}) != 1) throw new AssertionError("example 2");
        // Touching balloons share one coordinate, so one arrow suffices.
        if (minArrows(new int[][] {{1, 2}, {2, 3}}) != 1) throw new AssertionError("touching");
        // Empty input.
        if (minArrows(new int[0][]) != 0) throw new AssertionError("empty");
        // Random inputs agree with the exhaustive search.
        Random rnd = new Random(43);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(12); in[i] = new int[] {s, s + rnd.nextInt(6)}; }
            if (minArrows(in) != brute(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```
