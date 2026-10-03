<!-- solutions-for: 10-merge-and-insert -->
### Merge And Insert

#### Solution: [Build] Merge Intervals (LeetCode 56)
<!-- id: iv-merge-intervals -->

**Approach.** Sort a copy of the intervals by start, using `Integer.compare` so no subtraction can overflow. Keep the first interval as the active one. For each later interval, a start no larger than the active end touches or overlaps it, so the active end becomes the larger of the two ends. Otherwise the active interval is final, goes to the output, and the new interval becomes active. The oracle marks every covered integer point and every unit cell between points on a small line, then reads off the maximal runs, which merges intervals that share an endpoint but keeps apart intervals separated by a gap of at least one unit.

**Complexity.** O(n log n) time for the sort and O(n) space for the output.

```java run
import java.util.*;

public final class MergeIntervals {
    static int[][] merge(int[][] intervals) {
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> out = new ArrayList<>();
        int[] active = sorted[0].clone();
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i][0] <= active[1]) {
                active[1] = Math.max(active[1], sorted[i][1]);
            } else {
                out.add(active);
                active = sorted[i].clone();
            }
        }
        out.add(active);
        return out.toArray(new int[out.size()][]);
    }

    // Oracle: cover the half-unit cells [v, v+1) of each interval, then collect runs.
    // Two closed intervals that share only an endpoint share a cell boundary, so touching is
    // detected by also marking the endpoint itself as a point.
    static int[][] oracle(int[][] intervals, int limit) {
        boolean[] point = new boolean[limit + 1];
        boolean[] cell = new boolean[limit + 1];
        for (int[] iv : intervals) {
            for (int v = iv[0]; v <= iv[1]; v++) point[v] = true;
            for (int v = iv[0]; v < iv[1]; v++) cell[v] = true;
        }
        List<int[]> out = new ArrayList<>();
        int v = 0;
        while (v <= limit) {
            if (!point[v]) { v++; continue; }
            int s = v;
            while (v < limit && cell[v]) v++;
            out.add(new int[] {s, v});
            v++;
        }
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        int[][] r1 = merge(new int[][] {{1, 3}, {2, 6}, {8, 10}, {15, 18}});
        if (!Arrays.deepEquals(r1, new int[][] {{1, 6}, {8, 10}, {15, 18}})) throw new AssertionError("example 1");
        int[][] r2 = merge(new int[][] {{1, 4}, {4, 5}});
        if (!Arrays.deepEquals(r2, new int[][] {{1, 5}})) throw new AssertionError("example 2");
        Random rnd = new Random(10301);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); in[i] = new int[] {s, s + rnd.nextInt(5)}; }
            int[][] copy = new int[n][];
            for (int i = 0; i < n; i++) copy[i] = in[i].clone();
            int[][] got = merge(in);
            if (!Arrays.deepEquals(in, copy)) throw new AssertionError("input was modified");
            int[][] want = oracle(in, 25);
            if (!Arrays.deepEquals(got, want)) throw new AssertionError("differs for " + Arrays.deepToString(in) + ": " + Arrays.deepToString(got) + " vs " + Arrays.deepToString(want));
        }
    }
}
```

#### Solution: [Vary] Merge Already-Sorted Intervals (Author exercise)
<!-- id: iv-merge-already-sorted -->

**Approach.** The promise is that starts are non-decreasing, so the sort is dropped and a single scan keeps one active interval. An empty input returns an empty list before the first interval is read, because the scan starts by taking element zero. The code depends entirely on the promise: when an input is out of order, a late interval with a small start can be left unmerged with an earlier block. The solution asserts that a broken input such as `[[5, 6], [1, 2], [2, 3]]` gives a result different from the sorted oracle, which shows what the missing promise costs.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.*;

public final class MergeSorted {
    static int[][] mergeSorted(int[][] intervals) {
        if (intervals.length == 0) return new int[0][];
        List<int[]> out = new ArrayList<>();
        int[] active = intervals[0].clone();
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] <= active[1]) {
                active[1] = Math.max(active[1], intervals[i][1]);
            } else {
                out.add(active);
                active = intervals[i].clone();
            }
        }
        out.add(active);
        return out.toArray(new int[out.size()][]);
    }

    static int[][] oracle(int[][] intervals) {
        int[][] s = intervals.clone();
        Arrays.sort(s, (a, b) -> Integer.compare(a[0], b[0]));
        return mergeSorted(s);
    }

    static int[][] sortedByBruteForce(int[][] intervals, int limit) {
        boolean[] point = new boolean[limit + 1];
        boolean[] cell = new boolean[limit + 1];
        for (int[] iv : intervals) {
            for (int v = iv[0]; v <= iv[1]; v++) point[v] = true;
            for (int v = iv[0]; v < iv[1]; v++) cell[v] = true;
        }
        List<int[]> out = new ArrayList<>();
        int v = 0;
        while (v <= limit) {
            if (!point[v]) { v++; continue; }
            int s = v;
            while (v < limit && cell[v]) v++;
            out.add(new int[] {s, v});
            v++;
        }
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(mergeSorted(new int[][] {{1, 2}, {2, 3}, {5, 6}}), new int[][] {{1, 3}, {5, 6}})) throw new AssertionError("example 1");
        if (mergeSorted(new int[0][]).length != 0) throw new AssertionError("example 2");
        int[][] broken = {{5, 6}, {1, 2}, {2, 3}};
        if (Arrays.deepEquals(mergeSorted(broken), sortedByBruteForce(broken, 10))) throw new AssertionError("broken promise should change the result");
        Random rnd = new Random(10302);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); in[i] = new int[] {s, s + rnd.nextInt(5)}; }
            Arrays.sort(in, (a, b) -> Integer.compare(a[0], b[0]));
            int[][] got = mergeSorted(in);
            int[][] want = n == 0 ? new int[0][] : sortedByBruteForce(in, 25);
            if (!Arrays.deepEquals(got, want)) throw new AssertionError("differs for " + Arrays.deepToString(in));
            if (!Arrays.deepEquals(got, oracle(in))) throw new AssertionError("sorted oracle differs");
        }
    }
}
```

#### Solution: [Boundary] One Interval Covers Many (Author exercise)
<!-- id: iv-one-covers-many -->

**Approach.** The active end is the maximum end of every interval absorbed so far, written as `Math.max(active[1], next[1])`. Assigning the new end instead would shrink the block when a short interval lies inside a long one, so `[[0, 5], [1, 2], [3, 4]]` would end at 4 and then lose the span 4 to 5. The solution asserts that a faulty variant that assigns the end gives a different answer on that input, and compares the correct code with a point-marking oracle on random inputs with many nested intervals.

**Complexity.** O(n log n) time for the sort and O(n) space.

```java run
import java.util.*;

public final class OneCoversMany {
    static int[][] mergeAll(int[][] intervals, boolean useMax) {
        int[][] s = intervals.clone();
        Arrays.sort(s, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> out = new ArrayList<>();
        int[] active = s[0].clone();
        for (int i = 1; i < s.length; i++) {
            if (s[i][0] <= active[1]) {
                active[1] = useMax ? Math.max(active[1], s[i][1]) : s[i][1];
            } else {
                out.add(active);
                active = s[i].clone();
            }
        }
        out.add(active);
        return out.toArray(new int[out.size()][]);
    }

    static int[][] oracle(int[][] intervals, int limit) {
        boolean[] point = new boolean[limit + 1];
        boolean[] cell = new boolean[limit + 1];
        for (int[] iv : intervals) {
            for (int v = iv[0]; v <= iv[1]; v++) point[v] = true;
            for (int v = iv[0]; v < iv[1]; v++) cell[v] = true;
        }
        List<int[]> out = new ArrayList<>();
        int v = 0;
        while (v <= limit) {
            if (!point[v]) { v++; continue; }
            int s = v;
            while (v < limit && cell[v]) v++;
            out.add(new int[] {s, v});
            v++;
        }
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        int[][] a = {{1, 10}, {2, 3}, {4, 5}, {10, 12}, {13, 14}};
        if (!Arrays.deepEquals(mergeAll(a, true), new int[][] {{1, 12}, {13, 14}})) throw new AssertionError("example 1");
        int[][] b = {{0, 5}, {1, 2}, {3, 4}};
        if (!Arrays.deepEquals(mergeAll(b, true), new int[][] {{0, 5}})) throw new AssertionError("example 2");
        if (Arrays.deepEquals(mergeAll(b, false), new int[][] {{0, 5}})) throw new AssertionError("assigning the end should fail on example 2");
        Random rnd = new Random(10303);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) {
                int s = rnd.nextInt(10);
                int len = rnd.nextInt(4) == 0 ? 8 + rnd.nextInt(6) : rnd.nextInt(3);
                in[i] = new int[] {s, s + len};
            }
            if (!Arrays.deepEquals(mergeAll(in, true), oracle(in, 25))) throw new AssertionError("differs for " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Recognize] Insert Interval (LeetCode 57)
<!-- id: iv-insert-interval -->

**Approach.** The board is sorted and disjoint, so one scan in three regions is enough. First copy every interval whose end is below the new start. Then, while an interval's start is no larger than the new end, grow the new interval to the smaller start and the larger end. Finally copy the rest. Touching counts as overlap under the closed contract, so both region tests use strict comparisons only for the copy-before region. The oracle appends the new interval to the list and runs the sort-and-merge from the first exercise.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.*;

public final class InsertInterval {
    static int[][] insert(int[][] intervals, int[] add) {
        List<int[]> out = new ArrayList<>();
        int i = 0, n = intervals.length;
        while (i < n && intervals[i][1] < add[0]) out.add(intervals[i++].clone());
        int[] cur = add.clone();
        while (i < n && intervals[i][0] <= cur[1]) {
            cur[0] = Math.min(cur[0], intervals[i][0]);
            cur[1] = Math.max(cur[1], intervals[i][1]);
            i++;
        }
        out.add(cur);
        while (i < n) out.add(intervals[i++].clone());
        return out.toArray(new int[out.size()][]);
    }

    static int[][] oracle(int[][] intervals, int[] add) {
        int[][] all = new int[intervals.length + 1][];
        for (int i = 0; i < intervals.length; i++) all[i] = intervals[i].clone();
        all[intervals.length] = add.clone();
        Arrays.sort(all, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> out = new ArrayList<>();
        int[] active = all[0];
        for (int i = 1; i < all.length; i++) {
            if (all[i][0] <= active[1]) active = new int[] {active[0], Math.max(active[1], all[i][1])};
            else { out.add(active); active = all[i]; }
        }
        out.add(active);
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        int[][] board = {{1, 2}, {3, 5}, {6, 7}, {8, 10}, {12, 16}};
        if (!Arrays.deepEquals(insert(board, new int[] {4, 8}), new int[][] {{1, 2}, {3, 10}, {12, 16}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(insert(new int[][] {{1, 3}, {6, 9}}, new int[] {2, 5}), new int[][] {{1, 5}, {6, 9}})) throw new AssertionError("example 2");
        if (!Arrays.deepEquals(insert(new int[0][], new int[] {5, 7}), new int[][] {{5, 7}})) throw new AssertionError("empty board");
        Random rnd = new Random(10304);
        for (int t = 0; t < 4000; t++) {
            int k = rnd.nextInt(6);
            List<int[]> list = new ArrayList<>();
            int pos = rnd.nextInt(3);
            for (int i = 0; i < k; i++) {
                int s = pos, e = s + rnd.nextInt(4);
                list.add(new int[] {s, e});
                pos = e + 1 + rnd.nextInt(3);
            }
            int[][] in = list.toArray(new int[k][]);
            int s = rnd.nextInt(25), e = s + rnd.nextInt(6);
            int[] add = {s, e};
            if (!Arrays.deepEquals(insert(in, add), oracle(in, add))) throw new AssertionError("differs for " + Arrays.deepToString(in) + " + " + Arrays.toString(add));
        }
    }
}
```
