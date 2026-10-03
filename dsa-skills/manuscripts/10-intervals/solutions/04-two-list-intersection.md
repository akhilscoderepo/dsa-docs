<!-- solutions-for: 04-two-list-intersection -->
### Two-List Intersection

#### Solution: [Build] Intersect One Pair (Author exercise)
<!-- id: iv-intersect-one-pair -->

**Approach.** Two closed intervals share a value exactly when the larger start does not pass the smaller end. So compute `lo = max(a[0], b[0])` and `hi = min(a[1], b[1])`, return `{lo, hi}` when `lo <= hi`, and return an empty array otherwise. The empty array is the contract's way of saying no shared value, so the caller can test `length == 0`. The assertions compare against a set of shared integer points on small random pairs, and check the touching case, where the pair shares exactly one value.

**Complexity.** Constant time and constant space, since only four numbers are read.

```java run
import java.util.Random;

public final class IntersectOnePair {
    static int[] intersect(int[] a, int[] b) {
        int lo = Math.max(a[0], b[0]);
        int hi = Math.min(a[1], b[1]);
        return lo <= hi ? new int[] {lo, hi} : new int[0];
    }

    public static void main(String[] args) {
        int[] e1 = intersect(new int[] {1, 5}, new int[] {3, 8});
        if (e1.length != 2 || e1[0] != 3 || e1[1] != 5) throw new AssertionError("example 1");
        if (intersect(new int[] {1, 2}, new int[] {4, 6}).length != 0) throw new AssertionError("example 2");
        int[] touch = intersect(new int[] {1, 3}, new int[] {3, 9});
        if (touch.length != 2 || touch[0] != 3 || touch[1] != 3) throw new AssertionError("touching closed pair shares one value");
        Random rnd = new Random(10401);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(12), e1b = s1 + rnd.nextInt(6);
            int s2 = rnd.nextInt(12), e2b = s2 + rnd.nextInt(6);
            int first = -1, last = -1;
            for (int v = 0; v < 30; v++) {
                if (v >= s1 && v <= e1b && v >= s2 && v <= e2b) { if (first < 0) first = v; last = v; }
            }
            int[] got = intersect(new int[] {s1, e1b}, new int[] {s2, e2b});
            if (first < 0) { if (got.length != 0) throw new AssertionError("expected empty"); }
            else if (got.length != 2 || got[0] != first || got[1] != last) throw new AssertionError("differs from the point set");
        }
    }
}
```

#### Solution: [Vary] One Interval Against A Sorted List (Author exercise)
<!-- id: iv-one-against-list -->

**Approach.** Keep one cursor on the list. Advance it past every list interval whose end is below the fixed start, because none of those can meet the fixed interval. Then, while the current list interval starts at or before the fixed end, emit its overlap with the fixed interval and move on. The first list interval that starts after the fixed end ends the loop, since the list is sorted and every later one starts even later. The assertions compare with a test of every list interval, which costs one check per interval, on random sorted disjoint lists.

**Complexity.** O(n) time in the worst case, where n is the list length, and O(k) space for the k reported pieces.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class OneAgainstList {
    static int[][] clip(int[] fixed, int[][] list) {
        List<int[]> out = new ArrayList<>();
        int i = 0;
        while (i < list.length && list[i][1] < fixed[0]) i++;
        while (i < list.length && list[i][0] <= fixed[1]) {
            out.add(new int[] {Math.max(fixed[0], list[i][0]), Math.min(fixed[1], list[i][1])});
            i++;
        }
        return out.toArray(new int[out.size()][]);
    }
    static int[][] oracle(int[] fixed, int[][] list) {
        List<int[]> out = new ArrayList<>();
        for (int[] iv : list) {
            int lo = Math.max(fixed[0], iv[0]), hi = Math.min(fixed[1], iv[1]);
            if (lo <= hi) out.add(new int[] {lo, hi});
        }
        return out.toArray(new int[out.size()][]);
    }
    static int[][] randomDisjoint(Random rnd) {
        int n = rnd.nextInt(7);
        int[][] a = new int[n][2];
        int cur = rnd.nextInt(3);
        for (int i = 0; i < n; i++) {
            a[i][0] = cur;
            a[i][1] = cur + rnd.nextInt(4);
            cur = a[i][1] + 1 + rnd.nextInt(3);
        }
        return a;
    }

    public static void main(String[] args) {
        int[][] l1 = {{1, 2}, {3, 5}, {6, 7}, {8, 12}};
        if (!Arrays.deepEquals(clip(new int[] {4, 9}, l1), new int[][] {{4, 5}, {6, 7}, {8, 9}})) throw new AssertionError("example 1");
        if (clip(new int[] {3, 4}, new int[][] {{5, 6}, {7, 8}}).length != 0) throw new AssertionError("example 2");
        if (clip(new int[] {0, 9}, new int[0][]).length != 0) throw new AssertionError("empty list");
        Random rnd = new Random(10402);
        for (int t = 0; t < 5000; t++) {
            int[][] list = randomDisjoint(rnd);
            int s = rnd.nextInt(25);
            int[] fixed = {s, s + rnd.nextInt(10)};
            if (!Arrays.deepEquals(clip(fixed, list), oracle(fixed, list))) throw new AssertionError("differs on " + Arrays.deepToString(list));
        }
    }
}
```

#### Solution: [Boundary] Touching Intersections (Author exercise)
<!-- id: iv-touching-intersections -->

**Approach.** Run two cursors, one per list. For the current pair, compute `lo = max(starts)` and `hi = min(ends)`. A closed pair is nonempty when `lo <= hi`, and a half-open pair is nonempty only when `lo < hi`, because a half-open pair that meets at one value shares nothing. Then advance the cursor whose interval ends first, and advance both when the ends are equal. Advancing the earlier end is safe under either contract, since that interval cannot meet anything later in the other list. The assertions compare against a point-set oracle, with each closed interval covering the integers from start to end and each half-open one covering start up to end minus one.

**Complexity.** O(n + m) time for lists of lengths n and m, and O(k) space for the k reported pieces.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class TouchingIntersections {
    static int[][] intersect(int[][] a, int[][] b, boolean closed) {
        List<int[]> out = new ArrayList<>();
        int i = 0, j = 0;
        while (i < a.length && j < b.length) {
            int lo = Math.max(a[i][0], b[j][0]);
            int hi = Math.min(a[i][1], b[j][1]);
            if (closed ? lo <= hi : lo < hi) out.add(new int[] {lo, hi});
            if (a[i][1] < b[j][1]) i++;
            else if (a[i][1] > b[j][1]) j++;
            else { i++; j++; }
        }
        return out.toArray(new int[out.size()][]);
    }
    static boolean[] points(int[][] list, boolean closed) {
        boolean[] p = new boolean[60];
        for (int[] iv : list) for (int v = iv[0]; v < iv[1] + (closed ? 1 : 0); v++) p[v] = true;
        return p;
    }
    static boolean[] pointsOfResult(int[][] list, boolean closed) { return points(list, closed); }
    static int[][] randomDisjoint(Random rnd, boolean closed) {
        int n = rnd.nextInt(6);
        int[][] a = new int[n][2];
        int cur = rnd.nextInt(3);
        for (int i = 0; i < n; i++) {
            a[i][0] = cur;
            a[i][1] = cur + (closed ? rnd.nextInt(4) : 1 + rnd.nextInt(4));
            cur = a[i][1] + (closed ? 1 : 0) + rnd.nextInt(3);
        }
        return a;
    }

    public static void main(String[] args) {
        int[][] g = intersect(new int[][] {{1, 3}}, new int[][] {{3, 5}}, true);
        if (!Arrays.deepEquals(g, new int[][] {{3, 3}})) throw new AssertionError("example 1");
        if (intersect(new int[][] {{1, 3}}, new int[][] {{3, 5}}, false).length != 0) throw new AssertionError("example 2");
        Random rnd = new Random(10403);
        for (int t = 0; t < 6000; t++) {
            boolean closed = rnd.nextBoolean();
            int[][] a = randomDisjoint(rnd, closed), b = randomDisjoint(rnd, closed);
            int[][] got = intersect(a, b, closed);
            boolean[] pa = points(a, closed), pb = points(b, closed);
            boolean[] expected = new boolean[60];
            for (int v = 0; v < 60; v++) expected[v] = pa[v] && pb[v];
            if (!Arrays.equals(pointsOfResult(got, closed), expected)) throw new AssertionError("point sets differ on " + Arrays.deepToString(a) + " " + Arrays.deepToString(b) + " closed=" + closed);
            for (int[] iv : got) if (closed ? iv[0] > iv[1] : iv[0] >= iv[1]) throw new AssertionError("empty piece reported");
        }
    }
}
```

#### Solution: [Recognize] Interval List Intersections (LeetCode 986)
<!-- id: iv-interval-list-intersections -->

**Approach.** Both lists are sorted and disjoint, so one cursor per list is enough. Emit the overlap of the current pair when its start does not pass its end, then advance the interval with the smaller end, since it cannot meet any later interval of the other list. When both ends are equal, either choice is safe, because the next step discards the stale pair with an empty overlap. The oracle tests every pair of intervals with the max-start and min-end rule and sorts the results by start. The assertions compare on random sorted disjoint lists, including empty lists and touching ends.

**Complexity.** O(n + m) time against O(n * m) for the all-pairs oracle, and O(k) space for the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class IntervalListIntersections {
    static int[][] intersection(int[][] first, int[][] second) {
        List<int[]> out = new ArrayList<>();
        int i = 0, j = 0;
        while (i < first.length && j < second.length) {
            int lo = Math.max(first[i][0], second[j][0]);
            int hi = Math.min(first[i][1], second[j][1]);
            if (lo <= hi) out.add(new int[] {lo, hi});
            if (first[i][1] < second[j][1]) i++; else j++;
        }
        return out.toArray(new int[out.size()][]);
    }
    static int[][] oracle(int[][] first, int[][] second) {
        List<int[]> out = new ArrayList<>();
        for (int[] x : first) for (int[] y : second) {
            int lo = Math.max(x[0], y[0]), hi = Math.min(x[1], y[1]);
            if (lo <= hi) out.add(new int[] {lo, hi});
        }
        out.sort((p, q) -> Integer.compare(p[0], q[0]));
        return out.toArray(new int[out.size()][]);
    }
    static int[][] randomDisjoint(Random rnd) {
        int n = rnd.nextInt(7);
        int[][] a = new int[n][2];
        int cur = rnd.nextInt(3);
        for (int i = 0; i < n; i++) {
            a[i][0] = cur;
            a[i][1] = cur + rnd.nextInt(4);
            cur = a[i][1] + 1 + rnd.nextInt(3);
        }
        return a;
    }

    public static void main(String[] args) {
        int[][] f = {{0, 2}, {5, 10}, {13, 23}, {24, 25}};
        int[][] s = {{1, 5}, {8, 12}, {15, 24}, {25, 26}};
        int[][] want = {{1, 2}, {5, 5}, {8, 10}, {15, 23}, {24, 24}, {25, 25}};
        if (!Arrays.deepEquals(intersection(f, s), want)) throw new AssertionError("example 1");
        if (intersection(new int[][] {{1, 3}, {5, 9}}, new int[0][]).length != 0) throw new AssertionError("example 2");
        Random rnd = new Random(10404);
        for (int t = 0; t < 6000; t++) {
            int[][] a = randomDisjoint(rnd), b = randomDisjoint(rnd);
            if (!Arrays.deepEquals(intersection(a, b), oracle(a, b))) throw new AssertionError("differs on " + Arrays.deepToString(a) + " " + Arrays.deepToString(b));
        }
    }
}
```
