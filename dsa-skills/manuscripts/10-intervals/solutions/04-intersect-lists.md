<!-- solutions-for: 10-intervals -->
### Solutions For Intersecting Lists

#### Solution: [Build] Intersect One Pair (Author exercise)
<!-- id: iv-intersect-pair -->

**Approach.**
An integer lies in both closed intervals exactly when it is at least both starts and at most both ends. The method takes `lo` as the larger start and `hi` as the smaller end. When `lo <= hi`, the integers from `lo` to `hi` are exactly the shared ones, so the method returns `[lo, hi]`. Otherwise no integer lies in both and the method returns an empty array. Touching intervals give `lo == hi`, so the result is one coordinate. The invariant is that the returned range equals the set of shared integers.

**Complexity.**
- **Time** is O(1), because the method makes two comparisons and one test.
- **Space** is O(1), because the method allocates one array of at most two integers.

```java run
import java.util.Arrays;
import java.util.Random;

public final class IntersectPair {
    /**
     * Returns the intersection of two closed intervals, or an empty array.
     * Time: O(1), a fixed number of comparisons.
     * Space: O(1), one array of length at most 2.
     * Invariant: the result holds exactly the integers that lie in both intervals.
     */
    static int[] intersect(int[] x, int[] y) {
        // The shared range starts at the larger start.
        int lo = Math.max(x[0], y[0]);
        // The shared range ends at the smaller end.
        int hi = Math.min(x[1], y[1]);
        // A non-empty range needs lo <= hi in the closed model.
        return lo <= hi ? new int[] {lo, hi} : new int[0];
    }

    public static void main(String[] args) {
        // Example 1: overlapping intervals.
        if (!Arrays.equals(intersect(new int[] {2, 6}, new int[] {4, 9}), new int[] {4, 6})) throw new AssertionError("example 1");
        // Example 2: a gap between 3 and 4.
        if (intersect(new int[] {1, 3}, new int[] {4, 5}).length != 0) throw new AssertionError("example 2");
        // Touching intervals share exactly one coordinate.
        if (!Arrays.equals(intersect(new int[] {1, 3}, new int[] {3, 5}), new int[] {3, 3})) throw new AssertionError("touching");
        // Random pairs agree with a coordinate-by-coordinate reference.
        Random rnd = new Random(30);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(15), s2 = rnd.nextInt(15);
            int[] x = {s1, s1 + rnd.nextInt(6)}, y = {s2, s2 + rnd.nextInt(6)};
            int first = -1, last = -1;
            for (int c = 0; c <= 25; c++) if (x[0] <= c && c <= x[1] && y[0] <= c && c <= y[1]) { if (first < 0) first = c; last = c; }
            int[] expect = first < 0 ? new int[0] : new int[] {first, last};
            if (!Arrays.equals(intersect(x, y), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] One Interval Against A Sorted List (Author exercise)
<!-- id: iv-interval-vs-list -->

**Approach.**
The list is sorted and has no overlaps, so the list intervals that meet `q` form one unbroken block. The method skips the leading intervals whose end is below the start of `q`, because they lie entirely to the left. It then walks the block while the list interval starts at or before the end of `q`, and it records the intersection of each one. The first interval that starts after the end of `q` stops the walk, because every later interval starts even later. The invariant is that every interval before index `i` has either been skipped or recorded.

**Complexity.**
- **Time** is O(n), because the single index crosses the list once.
- **Space** is O(k) for the `k` recorded intersections, and O(1) beyond the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class OneAgainstList {
    /**
     * Returns the intersections of q with every list interval that meets it.
     * Time: O(n), one index crosses the list once.
     * Space: O(k) for the output.
     * Invariant: each interval before index i was skipped or recorded.
     */
    static int[][] intersectWith(int[] q, int[][] list) {
        List<int[]> out = new ArrayList<>();
        int i = 0;
        // Skip intervals that end before q starts; they cannot meet q.
        while (i < list.length && list[i][1] < q[0]) i++;
        // Walk the block of intervals that start at or before the end of q.
        while (i < list.length && list[i][0] <= q[1]) {
            // Each interval in the block meets q, so record the larger start and smaller end.
            out.add(new int[] {Math.max(q[0], list[i][0]), Math.min(q[1], list[i][1])});
            i++;
        }
        // Convert the list to the required array type.
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        // Example 1: three list intervals meet q, and the last is cut at 12.
        int[][] l1 = {{1, 3}, {5, 6}, {8, 10}, {11, 15}, {20, 22}};
        if (!Arrays.deepEquals(intersectWith(new int[] {4, 12}, l1), new int[][] {{5, 6}, {8, 10}, {11, 12}})) throw new AssertionError("example 1");
        // Example 2: q is a single coordinate that only [3,5] holds.
        if (!Arrays.deepEquals(intersectWith(new int[] {3, 3}, new int[][] {{1, 2}, {3, 5}}), new int[][] {{3, 3}})) throw new AssertionError("example 2");
        // Empty list and a query that meets nothing.
        if (intersectWith(new int[] {1, 2}, new int[0][]).length != 0) throw new AssertionError("empty");
        if (intersectWith(new int[] {100, 200}, l1).length != 0) throw new AssertionError("far right");
        // Random sorted disjoint lists agree with testing every list interval.
        Random rnd = new Random(31);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(7), pos = rnd.nextInt(3);
            int[][] list = new int[n][];
            for (int i = 0; i < n; i++) { int e = pos + rnd.nextInt(4); list[i] = new int[] {pos, e}; pos = e + 1 + rnd.nextInt(3); }
            int s = rnd.nextInt(25);
            int[] q = {s, s + rnd.nextInt(8)};
            List<int[]> expect = new ArrayList<>();
            for (int[] iv : list) {
                int lo = Math.max(q[0], iv[0]), hi = Math.min(q[1], iv[1]);
                if (lo <= hi) expect.add(new int[] {lo, hi});
            }
            if (!Arrays.deepEquals(intersectWith(q, list), expect.toArray(new int[0][]))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Touching Intersections (Author exercise)
<!-- id: iv-touching-intersections -->

**Approach.**
The method runs the two-cursor pass and counts a pair when the shared range is non-empty. Under the closed model the test is `lo <= hi`, so a pair that touches at one coordinate counts. Under the half-open model the test is `lo < hi`, so a pair that touches at an end does not count, and an empty interval with `start == end` never produces `lo < hi`. The cursor rule does not depend on the model: the interval with the smaller end advances, because the next interval of the other list starts after its own previous end. The invariant is that no finished interval can meet an unfinished interval of the other list.

**Complexity.**
- **Time** is O(n + m), because each iteration advances one cursor.
- **Space** is O(1), because the method stores two indexes and a counter.

```java run
import java.util.Random;

public final class TouchingCount {
    /**
     * Counts the non-empty intersections of two sorted lists under the chosen model.
     * Time: O(n + m), each iteration advances a cursor.
     * Space: O(1), two cursors and a counter.
     * Invariant: no finished interval meets an unfinished interval of the other list.
     */
    static int count(int[][] a, int[][] b, boolean closed) {
        int i = 0, j = 0, found = 0;
        // The loop ends when either cursor leaves its list.
        while (i < a.length && j < b.length) {
            int lo = Math.max(a[i][0], b[j][0]);
            int hi = Math.min(a[i][1], b[j][1]);
            // The model decides whether touching or zero-length ranges count.
            if (closed ? lo <= hi : lo < hi) found++;
            // Advance the interval with the smaller end; on a tie either choice is safe.
            if (a[i][1] < b[j][1]) i++; else j++;
        }
        return found;
    }

    /** Reference: test every pair. */
    static int brute(int[][] a, int[][] b, boolean closed) {
        int found = 0;
        for (int[] x : a) for (int[] y : b) {
            int lo = Math.max(x[0], y[0]), hi = Math.min(x[1], y[1]);
            if (closed ? lo <= hi : lo < hi) found++;
        }
        return found;
    }

    /** Builds a list that is sorted and has no overlaps under the model. */
    static int[][] randomList(Random rnd, boolean closed) {
        int n = rnd.nextInt(6), pos = rnd.nextInt(3);
        int[][] list = new int[n][];
        for (int i = 0; i < n; i++) {
            int e = pos + rnd.nextInt(4);
            list[i] = new int[] {pos, e};
            // Closed intervals need the next start above the end; half-open intervals may start at the end.
            pos = e + (closed ? 1 : 0) + rnd.nextInt(3);
        }
        return list;
    }

    public static void main(String[] args) {
        // Example 1: three single-coordinate meetings when closed, none when half-open.
        int[][] a = {{1, 3}, {5, 7}}, b = {{3, 5}, {7, 9}};
        if (count(a, b, true) != 3 || count(a, b, false) != 0) throw new AssertionError("example 1");
        // Example 2: a zero-length interval inside a long one.
        int[][] c = {{1, 5}}, d = {{2, 2}};
        if (count(c, d, true) != 1 || count(c, d, false) != 0) throw new AssertionError("example 2");
        // Empty lists.
        if (count(new int[0][], a, true) != 0) throw new AssertionError("empty");
        // Random lists agree with the pair-by-pair reference under both models.
        Random rnd = new Random(32);
        for (int t = 0; t < 4000; t++) {
            for (boolean closed : new boolean[] {true, false}) {
                int[][] x = randomList(rnd, closed), y = randomList(rnd, closed);
                if (count(x, y, closed) != brute(x, y, closed)) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Recognize] Interval List Intersections (LeetCode 986)
<!-- id: iv-interval-list-intersections -->

**Approach.**
The method keeps one cursor in each list and compares the two current intervals. It records their intersection when the larger start does not exceed the smaller end. It then advances the cursor whose interval has the smaller end. That interval cannot meet any later interval of the other list, because those start after the other current interval ends, and the other current interval ends at or after this one. The pass moves a cursor on every iteration, so it ends after at most `n + m - 1` iterations, and it records at most one intersection per iteration. The invariant is that all finished intervals have already contributed every intersection they can make.

**Complexity.**
- **Time** is O(n + m), because each iteration advances a cursor and there are at most `n + m` advances.
- **Space** is O(n + m) for the output in the worst case, and O(1) beyond the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ListIntersections {
    /**
     * Returns all non-empty intersections of two sorted disjoint lists of closed intervals.
     * Time: O(n + m), each iteration advances a cursor.
     * Space: O(n + m) for the output.
     * Invariant: finished intervals have already produced all their intersections.
     */
    static int[][] intersections(int[][] a, int[][] b) {
        List<int[]> out = new ArrayList<>();
        int i = 0, j = 0;
        // Stop when either list is used up; leftover intervals have nothing to meet.
        while (i < a.length && j < b.length) {
            int lo = Math.max(a[i][0], b[j][0]);
            int hi = Math.min(a[i][1], b[j][1]);
            // Record the shared range when it is non-empty under the closed model.
            if (lo <= hi) out.add(new int[] {lo, hi});
            // The interval with the smaller end cannot meet anything later, so move past it.
            if (a[i][1] < b[j][1]) i++; else j++;
        }
        return out.toArray(new int[out.size()][]);
    }

    /** Reference: test every pair, then order by start. */
    static int[][] brute(int[][] a, int[][] b) {
        List<int[]> out = new ArrayList<>();
        for (int[] x : a) for (int[] y : b) {
            int lo = Math.max(x[0], y[0]), hi = Math.min(x[1], y[1]);
            if (lo <= hi) out.add(new int[] {lo, hi});
        }
        out.sort((p, q) -> Integer.compare(p[0], q[0]));
        return out.toArray(new int[out.size()][]);
    }

    static int[][] randomList(Random rnd) {
        int n = rnd.nextInt(6), pos = rnd.nextInt(3);
        int[][] list = new int[n][];
        for (int i = 0; i < n; i++) { int e = pos + rnd.nextInt(5); list[i] = new int[] {pos, e}; pos = e + 1 + rnd.nextInt(3); }
        return list;
    }

    public static void main(String[] args) {
        // Example 1: one long interval of B meets two intervals of A.
        if (!Arrays.deepEquals(intersections(new int[][] {{0, 3}, {7, 9}}, new int[][] {{2, 8}}), new int[][] {{2, 3}, {7, 8}})) throw new AssertionError("example 1");
        // Example 2: equal ends at 4 and a touch at 8.
        if (!Arrays.deepEquals(intersections(new int[][] {{4, 4}, {6, 8}}, new int[][] {{1, 4}, {8, 9}}), new int[][] {{4, 4}, {8, 8}})) throw new AssertionError("example 2");
        // The lesson's session lists give six shared windows.
        int[][] r = intersections(new int[][] {{1, 4}, {6, 9}, {12, 15}, {18, 20}}, new int[][] {{3, 7}, {8, 13}, {14, 19}});
        if (!Arrays.deepEquals(r, new int[][] {{3, 4}, {6, 7}, {8, 9}, {12, 13}, {14, 15}, {18, 19}})) throw new AssertionError("sessions");
        // Empty lists.
        if (intersections(new int[0][], new int[][] {{1, 2}}).length != 0) throw new AssertionError("empty");
        // Random lists agree with the brute force, and the output never exceeds n + m - 1 entries.
        Random rnd = new Random(33);
        for (int t = 0; t < 4000; t++) {
            int[][] x = randomList(rnd), y = randomList(rnd);
            int[][] got = intersections(x, y);
            if (!Arrays.deepEquals(got, brute(x, y))) throw new AssertionError("random");
            if (x.length > 0 && y.length > 0 && got.length > x.length + y.length - 1) throw new AssertionError("bound");
        }
    }
}
```
