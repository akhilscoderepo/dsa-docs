<!-- solutions-for: 05-overlap-and-coverage -->
### Overlap And Coverage

#### Solution: [Build] Keep Earlier Finishing Interval (Author exercise)
<!-- id: iv-keep-earlier-finish -->

**Approach.** Compare the two ends and return the index of the smaller one, choosing the first interval on a tie. The start values never matter, because the kept interval blocks time only up to its end. The assertions test the claim directly: for every small random pair, keeping the chosen interval leaves a free tail that is at least as long as the other choice leaves, measured as the number of integer slots after its end up to a horizon, and no other interval from a small pool of later candidates fits after the rejected one but not after the chosen one.

**Complexity.** Constant time and constant space.

```java run
import java.util.Random;

public final class KeepEarlierFinish {
    static int keep(int[] a, int[] b) {
        return b[1] < a[1] ? 1 : 0;
    }

    public static void main(String[] args) {
        if (keep(new int[] {1, 9}, new int[] {3, 5}) != 1) throw new AssertionError("example 1");
        if (keep(new int[] {2, 6}, new int[] {4, 6}) != 0) throw new AssertionError("example 2");
        Random rnd = new Random(10501);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(8), e1 = s1 + 1 + rnd.nextInt(8);
            int s2 = rnd.nextInt(8), e2 = s2 + 1 + rnd.nextInt(8);
            if (!(s1 < e2 && s2 < e1)) continue;
            int[] a = {s1, e1}, b = {s2, e2};
            int chosen = keep(a, b);
            int[] kept = chosen == 0 ? a : b, dropped = chosen == 0 ? b : a;
            for (int ls = 0; ls < 20; ls++) {
                for (int le = ls + 1; le <= 20; le++) {
                    boolean fitsAfterDropped = ls >= dropped[1];
                    boolean fitsAfterKept = ls >= kept[1];
                    if (fitsAfterDropped && !fitsAfterKept) throw new AssertionError("a later request fits only after the dropped one");
                }
            }
            if (kept[1] > dropped[1]) throw new AssertionError("kept interval must end no later");
        }
    }
}
```

#### Solution: [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: iv-non-overlapping-intervals -->

**Approach.** Sort a copy by end, keep an interval when its start is at or after the last kept end, and answer with the total minus the kept count. The last end starts as a `long` minimum so the first interval always fits, and the sort uses `Integer.compare` because subtracting ends can overflow for extreme coordinates. The assertions show the overflow hazard with a pair whose subtraction flips sign, and compare against an exhaustive search over all subsets on small random inputs.

**Complexity.** O(n log n) time for the sort and O(n) space for the copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NonOverlappingIntervals {
    static int eraseOverlap(int[][] intervals) {
        int[][] sorted = new int[intervals.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = intervals[i].clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        int kept = 0;
        long lastEnd = Long.MIN_VALUE;
        for (int[] r : sorted) if (r[0] >= lastEnd) { kept++; lastEnd = r[1]; }
        return intervals.length - kept;
    }
    static int oracle(int[][] iv) {
        int n = iv.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int a = 0; a < n && ok; a++) {
                if ((mask >> a & 1) == 0) continue;
                for (int b = a + 1; b < n && ok; b++) {
                    if ((mask >> b & 1) == 0) continue;
                    if (iv[a][0] < iv[b][1] && iv[b][0] < iv[a][1]) ok = false;
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return n - best;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{0, 6}, {1, 3}, {2, 4}, {3, 5}, {5, 7}, {6, 8}};
        if (eraseOverlap(ex1) != 3) throw new AssertionError("example 1");
        if (eraseOverlap(new int[][] {{4, 5}, {4, 5}, {4, 5}}) != 2) throw new AssertionError("example 2");
        int hi = Integer.MAX_VALUE, lo = Integer.MIN_VALUE;
        if (lo - hi <= 0) throw new AssertionError("subtracting extreme ends wraps to a positive number");
        if (eraseOverlap(new int[][] {{lo, 0}, {0, hi}, {lo, hi}}) != 1) throw new AssertionError("extreme coordinates");
        int[][] original = {{3, 4}, {1, 2}};
        eraseOverlap(original);
        if (original[0][0] != 3) throw new AssertionError("the input order must survive");
        Random rnd = new Random(10502);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(10); a[i][1] = a[i][0] + 1 + rnd.nextInt(5); }
            if (eraseOverlap(a) != oracle(a)) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Boundary] Remove Covered Intervals (LeetCode 1288)
<!-- id: iv-remove-covered-intervals -->

**Approach.** Sort a copy by start ascending and, for equal starts, by end descending. Keep a running reach, the largest end among earlier intervals. An interval whose end exceeds the reach is visible and raises the reach, and every other interval is covered. The tie order makes the longer interval arrive first, so its shorter twin is already under the reach. The assertions show that sorting by start alone gives a wrong count on equal starts, and compare the scan with an all-pairs containment test on random inputs, counting duplicates as covered except for one copy.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RemoveCovered {
    static int remaining(int[][] intervals, boolean longerFirst) {
        int[][] sorted = new int[intervals.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = intervals[i].clone();
        Arrays.sort(sorted, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0])
                : (longerFirst ? Integer.compare(b[1], a[1]) : Integer.compare(a[1], b[1])));
        int visible = 0;
        long reach = Long.MIN_VALUE;
        for (int[] r : sorted) if (r[1] > reach) { visible++; reach = r[1]; }
        return visible;
    }
    static int oracle(int[][] iv) {
        int n = iv.length, count = 0;
        for (int i = 0; i < n; i++) {
            boolean covered = false;
            for (int j = 0; j < n && !covered; j++) {
                if (i == j) continue;
                boolean contains = iv[j][0] <= iv[i][0] && iv[j][1] >= iv[i][1];
                boolean same = iv[j][0] == iv[i][0] && iv[j][1] == iv[i][1];
                if (contains && (!same || j < i)) covered = true;
            }
            if (!covered) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{1, 4}, {3, 6}, {2, 8}, {2, 5}, {8, 9}, {7, 8}};
        if (remaining(ex1, true) != 3) throw new AssertionError("example 1");
        if (remaining(new int[][] {{5, 7}, {5, 7}, {5, 7}}, true) != 1) throw new AssertionError("example 2");
        if (remaining(new int[][] {{2, 5}, {2, 8}}, false) != 2) throw new AssertionError("start-only order counts the container twice");
        if (remaining(new int[][] {{2, 5}, {2, 8}}, true) != 1) throw new AssertionError("longer-first order hides the shorter twin");
        Random rnd = new Random(10503);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(6); a[i][1] = a[i][0] + 1 + rnd.nextInt(5); }
            if (remaining(a, true) != oracle(a)) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Recognize] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: iv-minimum-arrows -->

**Approach.** Sort a copy by end and shoot at the end of the first balloon. Every following balloon whose start is at or before that coordinate is burst by the same arrow, because the spans are closed. The first balloon that starts strictly after the coordinate needs a new arrow at its own end. Shooting at the smallest end reaches as far right as any single arrow can while still hitting the first balloon, so it is never worse. The assertions compare with a search over candidate shot positions, which are the end coordinates, and test extreme values where subtraction would overflow.

**Complexity.** O(n log n) time and O(n) space for the sorted copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MinimumArrows {
    static int arrows(int[][] points) {
        int[][] sorted = new int[points.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = points[i].clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
        int count = 0;
        long shot = Long.MIN_VALUE;
        for (int[] p : sorted) {
            if (count == 0 || p[0] > shot) { count++; shot = p[1]; }
        }
        return count;
    }
    static int oracle(int[][] pts) {
        int n = pts.length;
        int[] cand = new int[n];
        for (int i = 0; i < n; i++) cand[i] = pts[i][1];
        for (int k = 1; k <= n; k++) {
            if (choose(pts, cand, 0, k, new int[k], 0)) return k;
        }
        return n;
    }
    static boolean choose(int[][] pts, int[] cand, int from, int k, int[] picked, int used) {
        if (used == k) {
            for (int[] p : pts) {
                boolean hit = false;
                for (int x : picked) if (p[0] <= x && x <= p[1]) hit = true;
                if (!hit) return false;
            }
            return true;
        }
        for (int c = from; c < cand.length; c++) {
            picked[used] = cand[c];
            if (choose(pts, cand, c + 1, k, picked, used + 1)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (arrows(new int[][] {{10, 16}, {2, 8}, {1, 6}, {7, 12}}) != 2) throw new AssertionError("example 1");
        if (arrows(new int[][] {{1, 2}, {2, 3}, {3, 4}, {4, 5}}) != 2) throw new AssertionError("example 2");
        if (arrows(new int[][] {{Integer.MIN_VALUE, Integer.MAX_VALUE}, {Integer.MAX_VALUE, Integer.MAX_VALUE}}) != 1) throw new AssertionError("extreme closed spans share one point");
        if (arrows(new int[][] {{Integer.MIN_VALUE, 0}, {1, Integer.MAX_VALUE}}) != 2) throw new AssertionError("disjoint extreme spans");
        Random rnd = new Random(10504);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(10); a[i][1] = a[i][0] + rnd.nextInt(5); }
            if (arrows(a) != oracle(a)) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```
