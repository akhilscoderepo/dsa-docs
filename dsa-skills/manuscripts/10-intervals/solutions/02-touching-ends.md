<!-- solutions-for: 10-intervals -->
### Solutions For Touching Ends

#### Solution: [Build] Closed Interval Overlap (Author exercise)
<!-- id: iv-closed-overlap -->

**Approach.**
A coordinate lies in both closed intervals exactly when it is at least both starts and at most both ends. Such a coordinate exists when the larger start does not exceed the smaller end. The method computes `lo` as the larger start and `hi` as the smaller end, and returns `lo <= hi`. The pair `[1,3]` and `[3,5]` gives `lo = 3` and `hi = 3`, so the method returns true. The invariant is that the range from `lo` to `hi` equals the set of shared coordinates.

**Complexity.**
- **Time** is O(1), because the method makes two comparisons and one test.
- **Space** is O(1), because the method stores two integers.

```java run
import java.util.Random;

public final class ClosedOverlap {
    /**
     * Returns true when two closed intervals share an integer.
     * Time: O(1), a fixed number of comparisons.
     * Space: O(1), two local integers.
     * Invariant: [lo, hi] is the set of shared coordinates.
     */
    static boolean overlapsClosed(int[] a, int[] b) {
        // lo is the larger start, because a shared coordinate must reach both starts.
        int lo = Math.max(a[0], b[0]);
        // hi is the smaller end, because a shared coordinate must stay within both ends.
        int hi = Math.min(a[1], b[1]);
        // Both ends are included, so equal lo and hi still share one coordinate.
        return lo <= hi;
    }

    /** Reference: test every integer in a small window. */
    static boolean oracle(int[] a, int[] b) {
        // Each coordinate is tested against both intervals.
        for (int x = -2; x <= 30; x++) if (a[0] <= x && x <= a[1] && b[0] <= x && x <= b[1]) return true;
        return false;
    }

    public static void main(String[] args) {
        // Example 1: the touching pair shares the coordinate 3.
        if (!overlapsClosed(new int[] {1, 3}, new int[] {3, 5})) throw new AssertionError("example 1");
        // Example 2: a gap between 2 and 4 means no shared coordinate.
        if (overlapsClosed(new int[] {1, 2}, new int[] {4, 5})) throw new AssertionError("example 2");
        // Random pairs agree with the coordinate-by-coordinate reference.
        Random rnd = new Random(10);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(20), s2 = rnd.nextInt(20);
            int[] a = {s1, s1 + rnd.nextInt(6)}, b = {s2, s2 + rnd.nextInt(6)};
            if (overlapsClosed(a, b) != oracle(a, b)) throw new AssertionError("random");
            // The test does not depend on argument order.
            if (overlapsClosed(a, b) != overlapsClosed(b, a)) throw new AssertionError("symmetry");
        }
    }
}
```

#### Solution: [Vary] Half-Open Reservations (Author exercise)
<!-- id: iv-half-open-reservations -->

**Approach.**
A time `t` belongs to `[start, end)` when `start <= t` and `t < end`. A time belongs to both reservations when it is at least `lo` and below `hi`, which is possible exactly when `lo < hi`. So the method keeps the same two quantities as the closed test and changes only the comparison to a strict one. The pair `[1,3)` and `[3,5)` gives `lo = 3` and `hi = 3`, so the method returns false. The standard library uses the same model, which the harness confirms: `substring(begin, end)` has length `end - begin` and excludes the character at `end`.

**Complexity.**
- **Time** is O(1), because the method makes two comparisons and one test.
- **Space** is O(1), because the method stores two integers.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class HalfOpenConflict {
    /**
     * Returns true when two half-open reservations use a common integer time.
     * Time: O(1), a fixed number of comparisons.
     * Space: O(1), two local integers.
     * Invariant: the common times are the integers t with lo <= t < hi.
     */
    static boolean conflicts(int[] a, int[] b) {
        // lo is the larger start, so a common time is at least lo.
        int lo = Math.max(a[0], b[0]);
        // hi is the smaller end, so a common time is below hi.
        int hi = Math.min(a[1], b[1]);
        // The end is excluded, so lo equal to hi leaves no common time.
        return lo < hi;
    }

    /** Reference: test every integer in a small window. */
    static boolean oracle(int[] a, int[] b) {
        for (int t = -2; t <= 30; t++) if (a[0] <= t && t < a[1] && b[0] <= t && t < b[1]) return true;
        return false;
    }

    public static void main(String[] args) {
        // Example 1: the first reservation ends before time 3 begins.
        if (conflicts(new int[] {1, 3}, new int[] {3, 5})) throw new AssertionError("example 1");
        // Example 2: time 3 belongs to both reservations.
        if (!conflicts(new int[] {1, 4}, new int[] {3, 5})) throw new AssertionError("example 2");
        // Random pairs agree with the time-by-time reference.
        Random rnd = new Random(11);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(20), s2 = rnd.nextInt(20);
            int[] a = {s1, s1 + 1 + rnd.nextInt(6)}, b = {s2, s2 + 1 + rnd.nextInt(6)};
            if (conflicts(a, b) != oracle(a, b)) throw new AssertionError("random");
        }
        // Java library calls use the same model: the second argument is excluded, so the length is end - begin.
        String s = "abcdef";
        if (!s.substring(1, 3).equals("bc") || s.substring(1, 3).length() != 2) throw new AssertionError("substring");
        List<Integer> list = new ArrayList<>(List.of(0, 1, 2, 3, 4, 5));
        if (list.subList(1, 3).size() != 2 || list.subList(1, 3).get(1) != 2) throw new AssertionError("subList");
        if (!Arrays.equals(Arrays.copyOfRange(new int[] {0, 1, 2, 3, 4, 5}, 1, 3), new int[] {1, 2})) throw new AssertionError("copyOfRange");
    }
}
```

#### Solution: [Boundary] Zero-Length Range (Author exercise)
<!-- id: iv-zero-length-range -->

**Approach.**
A closed interval holds `end - start + 1` integers, and a half-open interval holds `end - start`. The empty half-open case `[x, x)` therefore gives 0, and `[x, x]` gives 1. The difference of two `int` values can exceed `Integer.MAX_VALUE`, as for `-2147483648` and `2147483647`, so the method casts one operand to `long` before it subtracts. The invariant is that every intermediate value is a `long`, so the count is exact for every legal input.

**Complexity.**
- **Time** is O(1), because the method makes one subtraction and one addition.
- **Space** is O(1), because the method stores one `long`.

```java run
import java.util.Random;

public final class CountCoordinates {
    /**
     * Returns the number of integers in the interval under the stated model.
     * Time: O(1), one subtraction and one addition.
     * Space: O(1), one long result.
     * Invariant: arithmetic runs in long, so no intermediate value wraps.
     */
    static long count(int start, int end, boolean closed) {
        // The cast widens before the subtraction, so far-apart ints do not overflow.
        long span = (long) end - start;
        // A closed interval also holds its end coordinate; a half-open one does not.
        return closed ? span + 1 : span;
    }

    public static void main(String[] args) {
        // Example 1: [4,4] holds one coordinate when closed and none when half-open.
        if (count(4, 4, true) != 1 || count(4, 4, false) != 0) throw new AssertionError("example 1");
        // Example 2: the full int range holds 2^32 integers.
        if (count(Integer.MIN_VALUE, Integer.MAX_VALUE, true) != 4294967296L) throw new AssertionError("example 2");
        // The int subtraction would have wrapped to -1 for the same pair.
        if (Integer.MAX_VALUE - Integer.MIN_VALUE != -1) throw new AssertionError("int subtraction wraps");
        // Random small intervals agree with counting the integers one by one.
        Random rnd = new Random(12);
        for (int t = 0; t < 3000; t++) {
            int s = rnd.nextInt(40) - 20, e = s + rnd.nextInt(10);
            long closed = 0, half = 0;
            for (int x = s; x <= e; x++) { closed++; if (x < e) half++; }
            if (count(s, e, true) != closed || count(s, e, false) != half) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Merge Under A Supplied Contract (Author exercise)
<!-- id: iv-group-starts-contract -->

**Approach.**
The method scans once and keeps `groupEnd`, the largest end in the current group. Input order by start means the next interval can reach only the group through that end. A new interval joins the group when its start is at most `groupEnd` in the closed model, or below `groupEnd` in the half-open model. Otherwise it opens a new group, and the method records its start. The flag changes only the one comparison, so the scan is the same code for both models. The invariant is that `groupEnd` is the largest end among the intervals of the last group.

**Complexity.**
- **Time** is O(n), because the loop visits each interval once and does constant work.
- **Space** is O(n) in the worst case, because the output holds one start per group, and O(1) beyond the output.

```java run
import java.util.Arrays;
import java.util.Random;

public final class GroupStarts {
    /**
     * Returns the start of the first interval of every group; input is ordered by start.
     * Time: O(n), one pass with constant work per interval.
     * Space: O(n) for the output, O(1) beyond it.
     * Invariant: groupEnd is the largest end in the last group.
     */
    static int[] groupStarts(int[][] iv, boolean closed) {
        // The output holds at most one entry per interval.
        int[] out = new int[iv.length];
        int k = 0;
        // groupEnd is meaningless until the first interval opens a group.
        int groupEnd = 0;
        // One pass over the sorted intervals.
        for (int i = 0; i < iv.length; i++) {
            // The only line that depends on the model: <= for closed, < for half-open.
            boolean joins = i > 0 && (closed ? iv[i][0] <= groupEnd : iv[i][0] < groupEnd);
            if (joins) {
                // The interval joins the group and may extend its end.
                groupEnd = Math.max(groupEnd, iv[i][1]);
            } else {
                // A new group starts here, so record its start.
                out[k++] = iv[i][0];
                groupEnd = iv[i][1];
            }
        }
        return Arrays.copyOf(out, k);
    }

    /** Reference: label intervals by repeated pair tests, then read off the group starts. */
    static int[] oracle(int[][] iv, boolean closed) {
        int n = iv.length;
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        // Relabel until no overlapping pair carries different labels.
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
                int lo = Math.max(iv[i][0], iv[j][0]), hi = Math.min(iv[i][1], iv[j][1]);
                boolean ov = closed ? lo <= hi : lo < hi;
                if (ov && label[i] != label[j]) {
                    int from = Math.max(label[i], label[j]), to = Math.min(label[i], label[j]);
                    for (int k = 0; k < n; k++) if (label[k] == from) label[k] = to;
                    changed = true;
                }
            }
        }
        // The first interval carrying each label gives that group's smallest start.
        int[] out = new int[n];
        int k = 0;
        boolean[] seen = new boolean[n];
        for (int i = 0; i < n; i++) if (!seen[label[i]]) { seen[label[i]] = true; out[k++] = iv[i][0]; }
        return Arrays.copyOf(out, k);
    }

    public static void main(String[] args) {
        // Example 1: touching intervals chain when closed and split when half-open.
        int[][] a = {{1, 3}, {3, 5}, {6, 8}};
        if (!Arrays.equals(groupStarts(a, true), new int[] {1, 6})) throw new AssertionError("ex1 closed");
        if (!Arrays.equals(groupStarts(a, false), new int[] {1, 3, 6})) throw new AssertionError("ex1 half-open");
        // Example 2: an inner interval does not extend the group end, so the touching start 4 decides.
        int[][] b = {{1, 4}, {2, 3}, {4, 6}};
        if (!Arrays.equals(groupStarts(b, true), new int[] {1})) throw new AssertionError("ex2 closed");
        if (!Arrays.equals(groupStarts(b, false), new int[] {1, 4})) throw new AssertionError("ex2 half-open");
        // Empty input.
        if (groupStarts(new int[0][], true).length != 0) throw new AssertionError("empty");
        // Random sorted inputs agree with the all-pairs reference under both models.
        Random rnd = new Random(13);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(12); in[i] = new int[] {s, s + 1 + rnd.nextInt(4)}; }
            Arrays.sort(in, (x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));
            for (boolean c : new boolean[] {true, false})
                if (!Arrays.equals(groupStarts(in, c), oracle(in, c))) throw new AssertionError("random " + Arrays.deepToString(in) + c);
        }
    }
}
```
