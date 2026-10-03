<!-- solutions-for: 10-two-list-intersection -->
### Two-List Intersection

#### Solution: [Build] Intersect One Pair (Author exercise)
<!-- id: iv-intersect-one-pair -->

**Approach.** The earliest value that both closed intervals contain is the larger of the two starts, and the latest is the smaller of the two ends. A shared value exists exactly when the larger start does not pass the smaller end, so the code returns that pair, or an empty array otherwise. The oracle lists the integer values of the first interval and keeps those inside the second, then reads off the smallest and largest kept value.

**Complexity.** O(1) time and space.

```java run
import java.util.*;

public final class IntersectOnePair {
    static int[] intersect(int[] a, int[] b) {
        int lo = Math.max(a[0], b[0]);
        int hi = Math.min(a[1], b[1]);
        return lo <= hi ? new int[] {lo, hi} : new int[0];
    }
    static int[] oracle(int[] a, int[] b) {
        int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
        for (int v = a[0]; v <= a[1]; v++) {
            if (v >= b[0] && v <= b[1]) { lo = Math.min(lo, v); hi = Math.max(hi, v); }
        }
        return lo == Integer.MAX_VALUE ? new int[0] : new int[] {lo, hi};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(intersect(new int[] {1, 5}, new int[] {3, 8}), new int[] {3, 5})) throw new AssertionError("example 1");
        if (intersect(new int[] {1, 2}, new int[] {4, 6}).length != 0) throw new AssertionError("example 2");
        if (!Arrays.equals(intersect(new int[] {-1000000000, 0}, new int[] {0, 1000000000}), new int[] {0, 0})) throw new AssertionError("extreme endpoints");
        Random rnd = new Random(10401);
        for (int t = 0; t < 5000; t++) {
            int s1 = rnd.nextInt(14) - 7, s2 = rnd.nextInt(14) - 7;
            int[] a = {s1, s1 + rnd.nextInt(7)}, b = {s2, s2 + rnd.nextInt(7)};
            if (!Arrays.equals(intersect(a, b), oracle(a, b))) throw new AssertionError("differs for " + Arrays.toString(a) + " and " + Arrays.toString(b));
        }
    }
}
```

#### Solution: [Vary] One Interval Against A Sorted List (Author exercise)
<!-- id: iv-one-against-list -->

**Approach.** Skip the list intervals whose end is below the fixed start, since they finish before the fixed interval begins. From there, take each list interval while its start does not pass the fixed end, record the overlap with the fixed interval, and stop at the first interval that starts after the fixed end, because every later one starts later still. The oracle tests every list interval against the fixed one with the pair rule.

**Complexity.** O(b) time for a list of b intervals, and O(1) extra space apart from the output.

```java run
import java.util.*;

public final class OneAgainstList {
    static List<int[]> againstList(int[] fixed, int[][] list) {
        List<int[]> out = new ArrayList<>();
        int j = 0;
        while (j < list.length && list[j][1] < fixed[0]) j++;
        while (j < list.length && list[j][0] <= fixed[1]) {
            out.add(new int[] {Math.max(fixed[0], list[j][0]), Math.min(fixed[1], list[j][1])});
            j++;
        }
        return out;
    }
    static List<int[]> oracle(int[] fixed, int[][] list) {
        List<int[]> out = new ArrayList<>();
        for (int[] x : list) {
            int lo = Math.max(fixed[0], x[0]), hi = Math.min(fixed[1], x[1]);
            if (lo <= hi) out.add(new int[] {lo, hi});
        }
        return out;
    }
    static boolean same(List<int[]> a, List<int[]> b) {
        return Arrays.deepEquals(a.toArray(new int[0][]), b.toArray(new int[0][]));
    }

    public static void main(String[] args) {
        int[][] list = {{1, 2}, {3, 5}, {6, 7}, {8, 12}};
        if (!same(againstList(new int[] {4, 9}, list), Arrays.asList(new int[] {4, 5}, new int[] {6, 7}, new int[] {8, 9}))) throw new AssertionError("example 1");
        if (!againstList(new int[] {3, 4}, new int[][] {{5, 6}, {7, 8}}).isEmpty()) throw new AssertionError("example 2");
        if (!againstList(new int[] {0, 5}, new int[0][]).isEmpty()) throw new AssertionError("empty list");
        Random rnd = new Random(10402);
        for (int t = 0; t < 4000; t++) {
            int k = rnd.nextInt(7);
            int[][] in = new int[k][];
            int pos = rnd.nextInt(3);
            for (int i = 0; i < k; i++) {
                int e = pos + rnd.nextInt(4);
                in[i] = new int[] {pos, e};
                pos = e + 1 + rnd.nextInt(3);
            }
            int s = rnd.nextInt(25), e = s + rnd.nextInt(8);
            int[] fixed = {s, e};
            if (!same(againstList(fixed, in), oracle(fixed, in))) throw new AssertionError("differs for " + Arrays.toString(fixed) + " against " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Boundary] Touching Intersections (Author exercise)
<!-- id: iv-touching-intersections -->

**Approach.** Walk both lists with one cursor each. For the current pair, the overlap exists when the larger start is at most the smaller end under the closed contract, and strictly below it under the half-open contract. Then advance the cursor whose end is smaller, and when the ends tie advance the second cursor. Only the nonempty test depends on the flag. The oracle expands each interval into the integer points it contains, which are `start..end` when closed and `start..end-1` when half-open, intersects the point sets, and groups consecutive points into runs. A run of consecutive points is one interval, which matches the walk because the lists are disjoint within themselves.

**Complexity.** O(a + b) time and O(1) extra space apart from the output.

```java run
import java.util.*;

public final class TouchingIntersections {
    static int[][] intersect(int[][] a, int[][] b, boolean closed) {
        List<int[]> out = new ArrayList<>();
        int i = 0, j = 0;
        while (i < a.length && j < b.length) {
            int lo = Math.max(a[i][0], b[j][0]);
            int hi = Math.min(a[i][1], b[j][1]);
            if (closed ? lo <= hi : lo < hi) out.add(new int[] {lo, hi});
            if (a[i][1] < b[j][1]) i++; else j++;
        }
        return out.toArray(new int[out.size()][]);
    }

    static boolean[] points(int[][] list, boolean closed, int limit) {
        boolean[] p = new boolean[limit + 1];
        for (int[] iv : list) {
            int end = closed ? iv[1] : iv[1] - 1;
            for (int v = iv[0]; v <= end; v++) p[v] = true;
        }
        return p;
    }
    // Oracle result uses the same shape as the walk: closed gives [start,end] of runs of shared points,
    // half-open gives [start,end) where end is the last shared point plus one.
    static int[][] oracle(int[][] a, int[][] b, boolean closed, int limit) {
        boolean[] pa = points(a, closed, limit), pb = points(b, closed, limit);
        List<int[]> out = new ArrayList<>();
        int v = 0;
        while (v <= limit) {
            if (!(pa[v] && pb[v])) { v++; continue; }
            int s = v;
            while (v + 1 <= limit && pa[v + 1] && pb[v + 1]) v++;
            out.add(new int[] {s, closed ? v : v + 1});
            v++;
        }
        return out.toArray(new int[out.size()][]);
    }

    static int[][] randomList(Random rnd, boolean closed) {
        int k = rnd.nextInt(5);
        int[][] in = new int[k][];
        int pos = rnd.nextInt(3);
        for (int i = 0; i < k; i++) {
            int len = closed ? rnd.nextInt(5) : 1 + rnd.nextInt(5);
            in[i] = new int[] {pos, pos + len};
            pos = pos + len + (closed ? 1 + rnd.nextInt(3) : rnd.nextInt(3));
        }
        return in;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 3}}, b = {{3, 5}};
        if (!Arrays.deepEquals(intersect(a, b, true), new int[][] {{3, 3}})) throw new AssertionError("example 1");
        if (intersect(a, b, false).length != 0) throw new AssertionError("example 2");
        Random rnd = new Random(10403);
        for (int t = 0; t < 4000; t++) {
            boolean closed = rnd.nextBoolean();
            int[][] x = randomList(rnd, closed), y = randomList(rnd, closed);
            int[][] got = intersect(x, y, closed);
            int[][] want = oracle(x, y, closed, 60);
            if (closed) {
                // closed oracle merges consecutive shared points into one run, so compare as covered point sets
                boolean[] g = new boolean[61], w = new boolean[61];
                for (int[] iv : got) for (int v = iv[0]; v <= iv[1]; v++) g[v] = true;
                for (int[] iv : want) for (int v = iv[0]; v <= iv[1]; v++) w[v] = true;
                if (!Arrays.equals(g, w)) throw new AssertionError("closed differs for " + Arrays.deepToString(x) + " and " + Arrays.deepToString(y));
            } else {
                boolean[] g = new boolean[61], w = new boolean[61];
                for (int[] iv : got) for (int v = iv[0]; v < iv[1]; v++) g[v] = true;
                for (int[] iv : want) for (int v = iv[0]; v < iv[1]; v++) w[v] = true;
                if (!Arrays.equals(g, w)) throw new AssertionError("half-open differs for " + Arrays.deepToString(x) + " and " + Arrays.deepToString(y));
            }
        }
    }
}
```

#### Solution: [Recognize] Interval List Intersections (LeetCode 986)
<!-- id: iv-interval-list-intersections -->

**Approach.** Keep a cursor in each list. When the larger start does not pass the smaller end, write that pair as an overlap. Then move the cursor whose interval ends first, because it cannot meet any later interval of the other list, and the other interval may still do so. The oracle tests every pair of intervals with the same overlap rule, and since the lists are each sorted and disjoint, its output is sorted once its pairs are sorted by start.

**Complexity.** O(a + b) time and O(1) extra space apart from the output.

```java run
import java.util.*;

public final class IntervalListIntersections {
    static int[][] intersectionLists(int[][] first, int[][] second) {
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
    static int[][] randomList(Random rnd) {
        int k = rnd.nextInt(6);
        int[][] in = new int[k][];
        int pos = rnd.nextInt(3);
        for (int i = 0; i < k; i++) {
            int e = pos + rnd.nextInt(5);
            in[i] = new int[] {pos, e};
            pos = e + 1 + rnd.nextInt(3);
        }
        return in;
    }

    public static void main(String[] args) {
        int[][] f = {{0, 2}, {5, 10}, {13, 23}, {24, 25}}, s = {{1, 5}, {8, 12}, {15, 24}, {25, 26}};
        if (!Arrays.deepEquals(intersectionLists(f, s), new int[][] {{1, 2}, {5, 5}, {8, 10}, {15, 23}, {24, 24}, {25, 25}})) throw new AssertionError("example 1");
        if (intersectionLists(new int[][] {{1, 3}, {5, 9}}, new int[0][]).length != 0) throw new AssertionError("example 2");
        Random rnd = new Random(10404);
        for (int t = 0; t < 4000; t++) {
            int[][] x = randomList(rnd), y = randomList(rnd);
            if (!Arrays.deepEquals(intersectionLists(x, y), oracle(x, y))) throw new AssertionError("differs for " + Arrays.deepToString(x) + " and " + Arrays.deepToString(y));
        }
    }
}
```
