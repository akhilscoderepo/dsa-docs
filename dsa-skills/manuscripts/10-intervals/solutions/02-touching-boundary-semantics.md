<!-- solutions-for: 10-touching-boundary-semantics -->
### Touching-Boundary Semantics

#### Solution: [Build] Closed Interval Overlap (Author exercise)
<!-- id: iv-closed-overlap -->

**Approach.** Two closed intervals share a value exactly when there is a value at least as large as both starts and at most as large as both ends. The smallest candidate is the larger of the two starts, and it works when it does not exceed the smaller of the two ends. When the larger start equals the smaller end, that single value belongs to both intervals, so the comparison is `<=`. The oracle lists the integer values of each interval and checks for a common member.

**Complexity.** O(1) time and space.

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
        if (!overlapsClosed(new int[] {-1000000000, 1000000000}, new int[] {1000000000, 1000000000})) throw new AssertionError("extreme endpoint");
        Random rnd = new Random(10201);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(12) - 6, s2 = rnd.nextInt(12) - 6;
            int[] a = {s1, s1 + rnd.nextInt(6)}, b = {s2, s2 + rnd.nextInt(6)};
            if (overlapsClosed(a, b) != oracle(a, b)) throw new AssertionError("differs for " + java.util.Arrays.toString(a) + " and " + java.util.Arrays.toString(b));
            if (overlapsClosed(a, b) != overlapsClosed(b, a)) throw new AssertionError("not symmetric");
        }
    }
}
```

#### Solution: [Vary] Half-Open Reservations (Author exercise)
<!-- id: iv-half-open-reservations -->

**Approach.** A half-open reservation holds the resource from its start up to, but not including, its end. Two reservations clash when some moment lies in both, and the earliest candidate is the larger start, which belongs to both only if it is strictly below the smaller end, since a value equal to an end is not in that interval. The predicate is therefore `<`, and reservations that meet at one moment, one ending exactly where the other starts, do not clash. The oracle lists the integer moments of each reservation and checks for a common one.

**Complexity.** O(1) time and space.

```java run
import java.util.Random;

public final class HalfOpenReservations {
    static boolean clash(int[] a, int[] b) {
        return Math.max(a[0], b[0]) < Math.min(a[1], b[1]);
    }
    static boolean oracle(int[] a, int[] b) {
        for (int v = a[0]; v < a[1]; v++) if (v >= b[0] && v < b[1]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (clash(new int[] {1, 3}, new int[] {3, 5})) throw new AssertionError("example 1");
        if (!clash(new int[] {1, 4}, new int[] {3, 6})) throw new AssertionError("example 2");
        if (!clash(new int[] {0, 10}, new int[] {3, 4})) throw new AssertionError("containment");
        Random rnd = new Random(10202);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(12) - 6, s2 = rnd.nextInt(12) - 6;
            int[] a = {s1, s1 + rnd.nextInt(6)}, b = {s2, s2 + rnd.nextInt(6)};
            if (clash(a, b) != oracle(a, b)) throw new AssertionError("differs for " + java.util.Arrays.toString(a) + " and " + java.util.Arrays.toString(b));
        }
    }
}
```

#### Solution: [Boundary] Zero-Length Range (Author exercise)
<!-- id: iv-zero-length-range -->

**Approach.** A closed interval `[x, x]` contains the single value `x`, and a half-open interval `[x, x)` contains no value at all. The two predicates need no special case for these: for closed intervals, `s <= e` holds between `[3, 3]` and `[1, 5]` because 3 is at most 3, and for half-open intervals, `s < e` fails between `[3, 3)` and `[1, 5)` because the larger start 3 is not below the smaller end 3. Two zero-length closed intervals at the same point overlap, and two zero-length half-open intervals never overlap anything, not even each other. The oracle enumerates the integer values each interval holds under its own meaning.

**Complexity.** O(1) time and space.

```java run
import java.util.Random;

public final class ZeroLengthRange {
    static boolean closed(int[] a, int[] b) { return Math.max(a[0], b[0]) <= Math.min(a[1], b[1]); }
    static boolean halfOpen(int[] a, int[] b) { return Math.max(a[0], b[0]) < Math.min(a[1], b[1]); }
    static boolean oracleClosed(int[] a, int[] b) {
        for (int v = a[0]; v <= a[1]; v++) if (v >= b[0] && v <= b[1]) return true;
        return false;
    }
    static boolean oracleHalfOpen(int[] a, int[] b) {
        for (int v = a[0]; v < a[1]; v++) if (v >= b[0] && v < b[1]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!closed(new int[] {3, 3}, new int[] {1, 5})) throw new AssertionError("example 1");
        if (halfOpen(new int[] {3, 3}, new int[] {1, 5})) throw new AssertionError("example 2");
        if (!closed(new int[] {3, 3}, new int[] {3, 3})) throw new AssertionError("two equal points");
        if (halfOpen(new int[] {3, 3}, new int[] {3, 3})) throw new AssertionError("two empty ranges");
        if (closed(new int[] {3, 3}, new int[] {4, 4})) throw new AssertionError("two different points");
        Random rnd = new Random(10203);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(8), s2 = rnd.nextInt(8);
            int[] a = {s1, s1 + rnd.nextInt(3)}, b = {s2, s2 + rnd.nextInt(3)};
            if (closed(a, b) != oracleClosed(a, b)) throw new AssertionError("closed differs");
            if (halfOpen(a, b) != oracleHalfOpen(a, b)) throw new AssertionError("half-open differs");
        }
    }
}
```

#### Solution: [Recognize] Merge Under A Supplied Contract (Author exercise)
<!-- id: iv-merge-under-contract -->

**Approach.** After sorting by start, the scan keeps the last output block and decides whether the next interval joins it. Under the closed meaning the next interval joins when its start is at most the block's end, since a shared endpoint is a shared value. Under the half-open meaning it joins only when its start is strictly below the block's end. That one comparison is the only difference between the modes, and joining takes the larger of the two ends. Each output interval is copied so the input rows are not changed, and the list is converted to an array at the end. The oracle builds groups by checking every pair with the matching predicate and joining groups transitively.

**Complexity.** O(n log n) time for the sort and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeUnderContract {
    static int[][] mergeUnder(int[][] intervals, boolean closed) {
        int[][] sorted = intervals.clone();
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
                for (int j = 0; j < n; j++) {
                    int lo = Math.max(intervals[i][0], intervals[j][0]), hi = Math.min(intervals[i][1], intervals[j][1]);
                    boolean ov = closed ? lo <= hi : lo < hi;
                    if (ov && group[i] != group[j]) {
                        int from = Math.max(group[i], group[j]), to = Math.min(group[i], group[j]);
                        for (int k = 0; k < n; k++) if (group[k] == from) group[k] = to;
                        changed = true;
                    }
                }
        }
        List<int[]> out = new ArrayList<>();
        for (int g = 0; g < n; g++) {
            int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
            boolean any = false;
            for (int i = 0; i < n; i++) if (group[i] == g) { any = true; lo = Math.min(lo, intervals[i][0]); hi = Math.max(hi, intervals[i][1]); }
            if (any) out.add(new int[] {lo, hi});
        }
        out.sort((x, y) -> Integer.compare(x[0], y[0]));
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        int[][] ex = {{1, 3}, {3, 5}, {7, 8}};
        if (!Arrays.deepEquals(mergeUnder(ex, true), new int[][] {{1, 5}, {7, 8}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(mergeUnder(ex, false), new int[][] {{1, 3}, {3, 5}, {7, 8}})) throw new AssertionError("example 2");
        if (!Arrays.deepEquals(ex, new int[][] {{1, 3}, {3, 5}, {7, 8}})) throw new AssertionError("the input must not change");
        Random rnd = new Random(10204);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(14); a[i][0] = s; a[i][1] = s + 1 + rnd.nextInt(4); }
            if (!Arrays.deepEquals(mergeUnder(a, true), oracle(a, true))) throw new AssertionError("closed differs on " + Arrays.deepToString(a));
            if (!Arrays.deepEquals(mergeUnder(a, false), oracle(a, false))) throw new AssertionError("half-open differs on " + Arrays.deepToString(a));
        }
    }
}
```
