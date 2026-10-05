<!-- solutions-for: 10-intervals -->
### Solutions For Sorting Then Scanning Intervals

#### Solution: [Build] Covered Length After Merging (LeetCode 56)
<!-- id: iv-comb-covered-length -->

**Approach.**
The method sorts a clone by start and scans once while it keeps the growing interval as two `long` values, `from` and `to`. An interval whose start is at most `to` overlaps the growing interval under the closed model, so `to` becomes the larger of the two ends. An interval that starts after `to` cannot overlap it or any later interval, so the growing interval is finished and adds `to - from + 1` integers to the total. The last growing interval adds its length after the loop. The arithmetic uses `long`, because one interval can span the whole `int` range. The invariant is that `total` equals the integers covered by all finished intervals, which are disjoint.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n), because the sorted clone holds `n` references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CoveredLength {
    /**
     * Returns the number of integers that lie in at least one closed interval.
     * Time: O(n log n), the sort plus one scan.
     * Space: O(n), for the sorted clone.
     * Invariant: total counts the integers of all finished disjoint intervals.
     */
    static long covered(int[][] intervals) {
        // No intervals cover nothing.
        if (intervals.length == 0) return 0;
        // Sort a clone by start so the growing interval is the only one that can still extend.
        int[][] s = intervals.clone();
        Arrays.sort(s, (a, b) -> Integer.compare(a[0], b[0]));
        long total = 0;
        // The growing interval is stored in long values so its length cannot overflow.
        long from = s[0][0], to = s[0][1];
        // One pass over the remaining intervals.
        for (int i = 1; i < s.length; i++) {
            if (s[i][0] <= to) {
                // Overlap under the closed model: keep the larger end.
                to = Math.max(to, s[i][1]);
            } else {
                // A gap: the growing interval is final, so add its length and start a new one.
                total += to - from + 1;
                from = s[i][0];
                to = s[i][1];
            }
        }
        // The last growing interval is still unfinished, so add it.
        return total + (to - from + 1);
    }

    /** Reference: mark every integer in a small range. */
    static long marking(int[][] in) {
        boolean[] m = new boolean[64];
        for (int[] w : in) for (int x = w[0]; x <= w[1]; x++) m[x + 10] = true;
        long c = 0;
        for (boolean b : m) if (b) c++;
        return c;
    }

    public static void main(String[] args) {
        // Example 1: hours 1 to 7 and hour 9 give 8.
        int[][] a = {{5, 7}, {1, 4}, {3, 6}, {9, 9}};
        if (covered(a) != 8) throw new AssertionError("example 1");
        // The input order is unchanged.
        if (a[0][0] != 5 || a[1][0] != 1) throw new AssertionError("input mutated");
        // Example 2: the whole int range holds 2^32 integers.
        if (covered(new int[][] {{Integer.MIN_VALUE, Integer.MAX_VALUE}}) != 4294967296L) throw new AssertionError("example 2");
        // Empty input.
        if (covered(new int[0][]) != 0) throw new AssertionError("empty");
        // Random inputs agree with marking each integer.
        Random rnd = new Random(60);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(30); in[i] = new int[] {s, s + rnd.nextInt(8)}; }
            if (covered(in) != marking(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Vary] Insert Interval Under A Half-Open Rule (LeetCode 57)
<!-- id: iv-comb-insert-half-open -->

**Approach.**
The list is sorted and its intervals do not overlap, so the intervals that overlap the new one form an unbroken block. The method uses one index and three loops. The first loop copies every interval whose end is at most the new start, because under the half-open rule an end at the new start only touches it. The second loop absorbs every interval whose start is below the grown end, so a start equal to the grown end stops the block. The method then writes the grown interval and copies the rest. Compared with the closed version, the comparisons `<` and `<=` swap places. The invariant is that every interval before index `i` is already in the output or absorbed into the grown interval.

**Complexity.**
- **Time** is O(n), because the three loops share one index that crosses the list once.
- **Space** is O(n), because the output holds up to `n + 1` intervals.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class InsertHalfOpen {
    /**
     * Returns the half-open list with the new interval inserted and overlapping groups merged.
     * Time: O(n), one index crosses the list once.
     * Space: O(n), for the output.
     * Invariant: each interval before index i is already in the output or absorbed into the grown interval.
     */
    static int[][] insert(int[][] list, int[] add) {
        List<int[]> result = new ArrayList<>();
        int i = 0, n = list.length;
        int start = add[0], end = add[1];
        // Part one: an end at or below the new start only touches it, so the interval stays separate.
        while (i < n && list[i][1] <= start) result.add(list[i++]);
        // Part two: a start strictly below the grown end overlaps it, so absorb the interval.
        while (i < n && list[i][0] < end) {
            start = Math.min(start, list[i][0]);
            end = Math.max(end, list[i][1]);
            i++;
        }
        // Write the grown interval, then copy the rest, which starts at or after its end.
        result.add(new int[] {start, end});
        while (i < n) result.add(list[i++]);
        return result.toArray(new int[result.size()][]);
    }

    /** Reference: append, sort by start, then merge only intervals that overlap strictly. */
    static int[][] oracle(int[][] list, int[] add) {
        int[][] all = Arrays.copyOf(list, list.length + 1);
        all[list.length] = add;
        Arrays.sort(all, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        List<int[]> out = new ArrayList<>();
        for (int[] w : all) {
            if (out.isEmpty() || out.get(out.size() - 1)[1] <= w[0]) out.add(new int[] {w[0], w[1]});
            else out.get(out.size() - 1)[1] = Math.max(out.get(out.size() - 1)[1], w[1]);
        }
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        // Example 1: [4,8) absorbs [3,5) and [7,9), and [1,3) only touches the result.
        if (!Arrays.deepEquals(insert(new int[][] {{1, 3}, {3, 5}, {7, 9}}, new int[] {4, 8}), new int[][] {{1, 3}, {3, 9}})) throw new AssertionError("example 1");
        // Example 2: [3,5) touches both neighbours and merges with neither.
        if (!Arrays.deepEquals(insert(new int[][] {{1, 3}, {5, 6}}, new int[] {3, 5}), new int[][] {{1, 3}, {3, 5}, {5, 6}})) throw new AssertionError("example 2");
        // Empty list.
        if (!Arrays.deepEquals(insert(new int[0][], new int[] {2, 4}), new int[][] {{2, 4}})) throw new AssertionError("empty");
        // Random sorted lists, whose half-open intervals may touch, agree with the reference.
        Random rnd = new Random(61);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(7), pos = rnd.nextInt(3);
            int[][] list = new int[n][];
            for (int i = 0; i < n; i++) { int e = pos + 1 + rnd.nextInt(4); list[i] = new int[] {pos, e}; pos = e + rnd.nextInt(3); }
            int s = rnd.nextInt(25);
            int[] add = {s, s + 1 + rnd.nextInt(8)};
            if (!Arrays.deepEquals(insert(list, add), oracle(list, add))) throw new AssertionError("random " + Arrays.deepToString(list) + Arrays.toString(add));
        }
    }
}
```

#### Solution: [Boundary] Closed Schedule Size (LeetCode 435)
<!-- id: iv-comb-closed-schedule -->

**Approach.**
The method sorts a clone by end and keeps `lastEnd`, the end of the last kept interval. Two closed intervals conflict when they share an integer, so a later interval fits only when its start is strictly greater than `lastEnd`. The method keeps such an interval and updates `lastEnd`, and it skips any other. Choosing the smallest end first is safe by the exchange argument of the fifth lesson, and that argument does not depend on the touching rule. The only change from the half-open version is the strict comparison. The invariant is that `lastEnd` is the smallest end that a largest conflict-free set of the processed intervals can have.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n), because the sorted clone holds `n` references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ClosedSchedule {
    /**
     * Returns the largest number of closed intervals that share no integer.
     * Time: O(n log n), the sort plus one scan.
     * Space: O(n), for the sorted clone.
     * Invariant: lastEnd is the smallest end of a largest conflict-free set of the processed intervals.
     */
    static int maxKept(int[][] intervals) {
        // Sort a clone by end with a safe comparison.
        int[][] s = intervals.clone();
        Arrays.sort(s, (a, b) -> Integer.compare(a[1], b[1]));
        int kept = 0;
        // lastEnd starts below every int, so the first interval is kept.
        long lastEnd = Long.MIN_VALUE;
        for (int[] x : s) {
            // A start strictly above lastEnd shares no integer with the last kept interval.
            if (x[0] > lastEnd) { kept++; lastEnd = x[1]; }
        }
        return kept;
    }

    /** Reference: the largest conflict-free subset by trying every subset. */
    static int brute(int[][] in) {
        int n = in.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) for (int j = i + 1; j < n && ok; j++)
                if ((mask >> i & 1) == 1 && (mask >> j & 1) == 1 && Math.max(in[i][0], in[j][0]) <= Math.min(in[i][1], in[j][1])) ok = false;
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: [1,3] and [3,5] conflict, so only one of them is kept.
        if (maxKept(new int[][] {{1, 3}, {3, 5}, {6, 8}}) != 2) throw new AssertionError("example 1");
        // Example 2: [2,3], [4,5] and [6,7] fit; [3,4] conflicts with two of them.
        if (maxKept(new int[][] {{1, 10}, {2, 3}, {4, 5}, {6, 7}, {3, 4}}) != 3) throw new AssertionError("example 2");
        // Extreme values do not overflow in the comparator.
        if (maxKept(new int[][] {{Integer.MIN_VALUE, Integer.MIN_VALUE}, {Integer.MAX_VALUE, Integer.MAX_VALUE}}) != 2) throw new AssertionError("extremes");
        // Empty input.
        if (maxKept(new int[0][]) != 0) throw new AssertionError("empty");
        // Random inputs agree with the exhaustive search.
        Random rnd = new Random(62);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(10); in[i] = new int[] {s, s + rnd.nextInt(5)}; }
            if (maxKept(in) != brute(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Recognize] List The Arrow Positions (LeetCode 452)
<!-- id: iv-comb-arrow-positions -->

**Approach.**
The method sorts a clone by end and places the first arrow at the smallest end. That arrow bursts every balloon that starts at or before it, because every later balloon ends at or after the arrow. When a balloon starts after the current arrow, the arrow misses it and every balloon after it that starts later, so the method records a new arrow at that balloon's end. The recorded positions are the answer, copied into an array of the right length. The positions come out in increasing order, because ends are processed in sorted order. The invariant is that the last recorded arrow bursts every balloon already processed, and no smaller set of arrows does.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n), because the sorted clone and the output array each hold up to `n` entries.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ArrowPositions {
    /**
     * Returns the positions of a smallest set of arrows that burst every closed balloon.
     * Time: O(n log n), the sort plus one scan.
     * Space: O(n), for the clone and the output.
     * Invariant: the last arrow bursts every processed balloon.
     */
    static int[] positions(int[][] balloons) {
        // No balloons need no arrows.
        if (balloons.length == 0) return new int[0];
        int[][] s = balloons.clone();
        // Sort by end with a safe comparison.
        Arrays.sort(s, (a, b) -> Integer.compare(a[1], b[1]));
        int[] out = new int[s.length];
        int k = 0;
        // The first arrow goes to the smallest end.
        int arrow = s[0][1];
        out[k++] = arrow;
        for (int i = 1; i < s.length; i++) {
            // A start past the arrow means the arrow misses this balloon, so shoot a new arrow at its end.
            if (s[i][0] > arrow) { arrow = s[i][1]; out[k++] = arrow; }
        }
        return Arrays.copyOf(out, k);
    }

    /** Checks that every balloon holds at least one arrow position. */
    static boolean bursts(int[][] balloons, int[] arrows) {
        for (int[] b : balloons) {
            boolean hit = false;
            for (int x : arrows) if (b[0] <= x && x <= b[1]) { hit = true; break; }
            if (!hit) return false;
        }
        return true;
    }

    /** Reference: the smallest arrow count by trying every set of balloon ends. */
    static int bruteSize(int[][] in) {
        int n = in.length;
        if (n == 0) return 0;
        int best = n;
        for (int mask = 1; mask < (1 << n); mask++) {
            int[] arrows = new int[Integer.bitCount(mask)];
            int k = 0;
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) arrows[k++] = in[i][1];
            if (bursts(in, arrows)) best = Math.min(best, arrows.length);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: arrows at 6 and 12.
        if (!Arrays.equals(positions(new int[][] {{10, 16}, {2, 8}, {1, 6}, {7, 12}}), new int[] {6, 12})) throw new AssertionError("example 1");
        // Example 2: arrows at 2 and 4 burst the three touching balloons.
        if (!Arrays.equals(positions(new int[][] {{1, 2}, {2, 3}, {3, 4}}), new int[] {2, 4})) throw new AssertionError("example 2");
        // Empty input.
        if (positions(new int[0][]).length != 0) throw new AssertionError("empty");
        // Random inputs: the positions burst every balloon, increase strictly, and have the smallest possible size.
        Random rnd = new Random(63);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(12); in[i] = new int[] {s, s + rnd.nextInt(6)}; }
            int[] p = positions(in);
            if (!bursts(in, p)) throw new AssertionError("misses " + Arrays.deepToString(in));
            for (int i = 1; i < p.length; i++) if (p[i - 1] >= p[i]) throw new AssertionError("order");
            if (p.length != bruteSize(in)) throw new AssertionError("size " + Arrays.deepToString(in));
        }
    }
}
```
