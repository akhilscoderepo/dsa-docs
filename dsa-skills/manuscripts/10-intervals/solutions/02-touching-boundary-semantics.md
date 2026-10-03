<!-- solutions-for: 02-touching-boundary-semantics -->
### Touching-Boundary Semantics

#### Solution: [Build] Closed Interval Overlap (Author exercise)
<!-- id: iv-closed-overlap -->

**Approach.** Two closed intervals share a value exactly when the larger start does not pass the smaller end, so the test is `max(a.start, b.start) <= min(a.end, b.end)`. For `[1, 3]` and `[3, 5]` the larger start is 3 and the smaller end is 3, and the value 3 belongs to both intervals, so they overlap, which is why the comparison keeps its equality. The assertions compare the predicate with a set-based oracle that lists every integer in each interval and looks for a common one, and they check the two examples.

**Complexity.** O(1) time and O(1) space for the predicate.

```java run
import java.util.Random;

public final class ClosedOverlap {
    static boolean overlapsClosed(int[] a, int[] b) {
        return Math.max(a[0], b[0]) <= Math.min(a[1], b[1]);
    }
    static boolean oracle(int[] a, int[] b) {
        for (int v = a[0]; v <= a[1]; v++) if (v >= b[0] && v <= b[1]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!overlapsClosed(new int[] {1, 3}, new int[] {3, 5})) throw new AssertionError("example 1");
        if (overlapsClosed(new int[] {1, 2}, new int[] {4, 5})) throw new AssertionError("example 2");
        if (!overlapsClosed(new int[] {-1000000000, 1000000000}, new int[] {1000000000, 1000000000})) throw new AssertionError("extreme endpoints");
        Random rnd = new Random(10201);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(10), s2 = rnd.nextInt(10);
            int[] a = {s1, s1 + rnd.nextInt(5)};
            int[] b = {s2, s2 + rnd.nextInt(5)};
            if (overlapsClosed(a, b) != oracle(a, b)) throw new AssertionError("disagrees on " + a[0] + "," + a[1] + " " + b[0] + "," + b[1]);
            if (overlapsClosed(a, b) != overlapsClosed(b, a)) throw new AssertionError("the predicate must be symmetric");
        }
    }
}
```

#### Solution: [Vary] Half-Open Reservations (Author exercise)
<!-- id: iv-half-open-reservations -->

**Approach.** A reservation `[start, end)` holds the values from `start` up to `end - 1`. Two reservations clash when the larger start is strictly below the smaller end, so the test is `max(starts) < min(ends)`. For `[1, 3)` and `[3, 5)` the larger start 3 is not below the smaller end 3, since the first reservation does not contain 3, so they do not clash and a resource can be handed over at the moment 3. The assertions compare with an oracle that lists the integers each reservation contains, and also show that using the closed predicate on half-open data reports false clashes for touching reservations.

**Complexity.** O(1) time and O(1) space.

```java run
import java.util.Random;

public final class HalfOpenReservations {
    static boolean clashes(int[] a, int[] b) {
        return Math.max(a[0], b[0]) < Math.min(a[1], b[1]);
    }
    static boolean closedPredicate(int[] a, int[] b) {
        return Math.max(a[0], b[0]) <= Math.min(a[1], b[1]);
    }
    static boolean oracle(int[] a, int[] b) {
        for (int v = a[0]; v < a[1]; v++) if (v >= b[0] && v < b[1]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (clashes(new int[] {1, 3}, new int[] {3, 5})) throw new AssertionError("example 1");
        if (!clashes(new int[] {1, 4}, new int[] {3, 6})) throw new AssertionError("example 2");
        if (!closedPredicate(new int[] {1, 3}, new int[] {3, 5})) throw new AssertionError("the closed predicate reports a clash that does not exist");
        if (clashes(new int[] {2, 2}, new int[] {1, 5})) throw new AssertionError("an empty reservation never clashes");
        Random rnd = new Random(10202);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(10), s2 = rnd.nextInt(10);
            int[] a = {s1, s1 + rnd.nextInt(5)};
            int[] b = {s2, s2 + rnd.nextInt(5)};
            if (clashes(a, b) != oracle(a, b)) throw new AssertionError("disagrees on " + a[0] + "," + a[1] + " " + b[0] + "," + b[1]);
        }
    }
}
```

#### Solution: [Boundary] Zero-Length Range (Author exercise)
<!-- id: iv-zero-length-range -->

**Approach.** A closed `[x, x]` contains exactly one value, and a half-open `[x, x)` contains none, so the same predicates as before handle both without a special case. For a closed zero-length range inside a longer one, the larger start is `x` and the smaller end is `x`, which passes the test with equality. For a half-open zero-length range, the larger start is `x` and the smaller end is at most `x`, so the strict test fails, and an empty range overlaps nothing, even a range that surrounds it. Two zero-length ranges at the same point overlap when closed and never when half-open. The assertions compare with an oracle that counts the values each range holds, and check the sizes of zero-length ranges directly.

**Complexity.** O(1) time and O(1) space.

```java run
import java.util.Random;

public final class ZeroLengthRange {
    static boolean closedOverlap(int[] a, int[] b) {
        return Math.max(a[0], b[0]) <= Math.min(a[1], b[1]);
    }
    static boolean halfOpenOverlap(int[] a, int[] b) {
        return Math.max(a[0], b[0]) < Math.min(a[1], b[1]);
    }
    static boolean closedOracle(int[] a, int[] b) {
        for (int v = a[0]; v <= a[1]; v++) if (v >= b[0] && v <= b[1]) return true;
        return false;
    }
    static boolean halfOpenOracle(int[] a, int[] b) {
        for (int v = a[0]; v < a[1]; v++) if (v >= b[0] && v < b[1]) return true;
        return false;
    }
    static int closedSize(int[] a) { return a[1] - a[0] + 1; }
    static int halfOpenSize(int[] a) { return a[1] - a[0]; }

    public static void main(String[] args) {
        if (!closedOverlap(new int[] {3, 3}, new int[] {1, 5})) throw new AssertionError("example 1");
        if (halfOpenOverlap(new int[] {3, 3}, new int[] {1, 5})) throw new AssertionError("example 2");
        if (closedSize(new int[] {3, 3}) != 1) throw new AssertionError("a closed [x, x] is one point");
        if (halfOpenSize(new int[] {3, 3}) != 0) throw new AssertionError("a half-open [x, x) is empty");
        if (!closedOverlap(new int[] {4, 4}, new int[] {4, 4})) throw new AssertionError("equal points overlap when closed");
        if (halfOpenOverlap(new int[] {4, 4}, new int[] {4, 4})) throw new AssertionError("empty ranges never overlap");
        Random rnd = new Random(10203);
        for (int t = 0; t < 6000; t++) {
            int s1 = rnd.nextInt(8), s2 = rnd.nextInt(8);
            int[] a = {s1, s1 + (rnd.nextBoolean() ? 0 : rnd.nextInt(4))};
            int[] b = {s2, s2 + (rnd.nextBoolean() ? 0 : rnd.nextInt(4))};
            if (closedOverlap(a, b) != closedOracle(a, b)) throw new AssertionError("closed differs");
            if (halfOpenOverlap(a, b) != halfOpenOracle(a, b)) throw new AssertionError("half-open differs");
        }
    }
}
```

#### Solution: [Recognize] Merge Under A Supplied Contract (Author exercise)
<!-- id: iv-merge-under-contract -->

**Approach.** Sort by start and keep a list of finished blocks whose last entry can still grow. A new interval joins the last block when it shares a value with it, which is `cur.start <= last.end` under the closed contract and `cur.start < last.end` under the half-open one, and that single comparison is the only difference between the two modes. The block's end becomes the larger of the two ends. The oracle expands every interval into the set of integers it contains under the chosen contract, joins intervals that have a common integer until nothing changes, and reports each group by its smallest start and largest end. The assertions check both examples and compare on random inputs under both contracts.

**Complexity.** O(n log n) time for the sort and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeUnderContract {
    static int[][] mergeUnder(int[][] intervals, boolean closed) {
        int[][] sorted = new int[intervals.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = intervals[i].clone();
        Arrays.sort(sorted, (x, y) -> Integer.compare(x[0], y[0]));
        List<int[]> out = new ArrayList<>();
        for (int[] cur : sorted) {
            if (!out.isEmpty()) {
                int[] last = out.get(out.size() - 1);
                boolean joins = closed ? cur[0] <= last[1] : cur[0] < last[1];
                if (joins) {
                    last[1] = Math.max(last[1], cur[1]);
                    continue;
                }
            }
            out.add(new int[] {cur[0], cur[1]});
        }
        return out.toArray(new int[out.size()][]);
    }
    static int[][] oracle(int[][] intervals, boolean closed) {
        int n = intervals.length;
        int[] group = new int[n];
        for (int i = 0; i < n; i++) group[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++) {
                    if (group[i] == group[j]) continue;
                    boolean share = false;
                    int hiA = closed ? intervals[i][1] : intervals[i][1] - 1;
                    int hiB = closed ? intervals[j][1] : intervals[j][1] - 1;
                    for (int v = intervals[i][0]; v <= hiA; v++) if (v >= intervals[j][0] && v <= hiB) share = true;
                    if (share) {
                        int from = group[j], to = group[i];
                        for (int k = 0; k < n; k++) if (group[k] == from) group[k] = to;
                        changed = true;
                    }
                }
        }
        List<int[]> out = new ArrayList<>();
        boolean[] done = new boolean[n];
        for (int i = 0; i < n; i++) {
            if (done[i]) continue;
            int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
            for (int k = 0; k < n; k++) if (group[k] == group[i]) { done[k] = true; lo = Math.min(lo, intervals[k][0]); hi = Math.max(hi, intervals[k][1]); }
            out.add(new int[] {lo, hi});
        }
        out.sort((x, y) -> Integer.compare(x[0], y[0]));
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        int[][] in = {{1, 3}, {3, 5}, {7, 8}};
        if (!Arrays.deepEquals(mergeUnder(in, true), new int[][] {{1, 5}, {7, 8}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(mergeUnder(in, false), new int[][] {{1, 3}, {3, 5}, {7, 8}})) throw new AssertionError("example 2");
        if (!Arrays.deepEquals(in, new int[][] {{1, 3}, {3, 5}, {7, 8}})) throw new AssertionError("the input must not change");
        Random rnd = new Random(10204);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(12); a[i][0] = s; a[i][1] = s + 1 + rnd.nextInt(4); }
            for (boolean closed : new boolean[] {true, false})
                if (!Arrays.deepEquals(mergeUnder(a, closed), oracle(a, closed))) throw new AssertionError("differs for closed=" + closed + " on " + Arrays.deepToString(a));
        }
    }
}
```
