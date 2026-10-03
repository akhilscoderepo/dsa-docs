<!-- solutions-for: 03-merge-and-insert -->
### Merge And Insert

#### Solution: [Build] Merge Intervals (LeetCode 56)
<!-- id: iv-merge-intervals -->

**Approach.** Sort a copy by start, then keep one active interval at the end of the output. A new interval whose start is above the active end begins a new block, and otherwise the active end becomes the larger of the two ends, so a touching interval joins the block. Sorting by start is what guarantees that only the active interval can still overlap the next one. The oracle repeatedly joins any two intervals that share a value until no pair does, which needs no sorting, and the assertions compare the two on random inputs and check that the input array is not changed.

**Complexity.** O(n log n) time for the sort, O(n) for the scan, and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeIntervals {
    static int[][] merge(int[][] intervals) {
        int[][] sorted = new int[intervals.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = intervals[i].clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> out = new ArrayList<>();
        for (int[] cur : sorted) {
            if (out.isEmpty() || cur[0] > out.get(out.size() - 1)[1]) {
                out.add(new int[] {cur[0], cur[1]});
            } else {
                int[] last = out.get(out.size() - 1);
                last[1] = Math.max(last[1], cur[1]);
            }
        }
        return out.toArray(new int[out.size()][]);
    }
    static int[][] oracle(int[][] intervals) {
        List<int[]> pool = new ArrayList<>();
        for (int[] iv : intervals) pool.add(iv.clone());
        boolean changed = true;
        while (changed) {
            changed = false;
            outer:
            for (int i = 0; i < pool.size(); i++)
                for (int j = i + 1; j < pool.size(); j++) {
                    int[] a = pool.get(i), b = pool.get(j);
                    if (Math.max(a[0], b[0]) <= Math.min(a[1], b[1])) {
                        pool.set(i, new int[] {Math.min(a[0], b[0]), Math.max(a[1], b[1])});
                        pool.remove(j);
                        changed = true;
                        break outer;
                    }
                }
        }
        pool.sort((x, y) -> Integer.compare(x[0], y[0]));
        return pool.toArray(new int[pool.size()][]);
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(merge(new int[][] {{1, 3}, {2, 6}, {8, 10}, {15, 18}}), new int[][] {{1, 6}, {8, 10}, {15, 18}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(merge(new int[][] {{1, 4}, {4, 5}}), new int[][] {{1, 5}})) throw new AssertionError("example 2");
        int[][] in = {{5, 6}, {1, 2}};
        merge(in);
        if (!Arrays.deepEquals(in, new int[][] {{5, 6}, {1, 2}})) throw new AssertionError("the input must not change");
        Random rnd = new Random(10301);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); a[i][0] = s; a[i][1] = s + rnd.nextInt(5); }
            if (!Arrays.deepEquals(merge(a), oracle(a))) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Vary] Merge Already-Sorted Intervals (Author exercise)
<!-- id: iv-merge-already-sorted -->

**Approach.** Under the promise that the intervals are sorted by start, the sort is removed and one pass remains. The first interval always opens a block, and every later interval either starts above the active end and opens a new block, or extends the active end with the larger of the two ends. The promise is what makes this correct, because an interval that starts earlier than the active block but arrives later is treated as if it overlapped it, and the scan can then lose it. The assertions compare with a sort-then-merge oracle on sorted inputs, and show an unsorted input on which the scan returns a wrong answer.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeAlreadySorted {
    static int[][] mergeSorted(int[][] sortedByStart) {
        List<int[]> out = new ArrayList<>();
        for (int[] cur : sortedByStart) {
            if (out.isEmpty() || cur[0] > out.get(out.size() - 1)[1]) {
                out.add(new int[] {cur[0], cur[1]});
            } else {
                int[] last = out.get(out.size() - 1);
                last[1] = Math.max(last[1], cur[1]);
            }
        }
        return out.toArray(new int[out.size()][]);
    }
    static int[][] sortThenMerge(int[][] intervals) {
        int[][] copy = new int[intervals.length][];
        for (int i = 0; i < copy.length; i++) copy[i] = intervals[i].clone();
        Arrays.sort(copy, (a, b) -> Integer.compare(a[0], b[0]));
        return mergeSorted(copy);
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(mergeSorted(new int[][] {{1, 2}, {2, 3}, {5, 6}}), new int[][] {{1, 3}, {5, 6}})) throw new AssertionError("example 1");
        if (mergeSorted(new int[0][]).length != 0) throw new AssertionError("example 2");
        int[][] broken = {{5, 6}, {1, 2}, {2, 3}};
        if (Arrays.deepEquals(mergeSorted(broken), sortThenMerge(broken))) throw new AssertionError("an unsorted input must break the single pass");
        if (!Arrays.deepEquals(mergeSorted(broken), new int[][] {{5, 6}})) throw new AssertionError("the unsorted input loses the earlier intervals");
        Random rnd = new Random(10302);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); a[i][0] = s; a[i][1] = s + rnd.nextInt(5); }
            int[][] sorted = new int[n][];
            for (int i = 0; i < n; i++) sorted[i] = a[i].clone();
            Arrays.sort(sorted, (x, y) -> Integer.compare(x[0], y[0]));
            if (!Arrays.deepEquals(mergeSorted(sorted), sortThenMerge(a))) throw new AssertionError("differs on " + Arrays.deepToString(sorted));
        }
    }
}
```

#### Solution: [Boundary] One Interval Covers Many (Author exercise)
<!-- id: iv-one-covers-many -->

**Approach.** The expression that protects the active end is `last[1] = Math.max(last[1], cur[1])`. When a long interval covers several later ones, each of those ends below the active end, so assigning `cur[1]` would pull the end backwards, and a later interval that starts between the shrunk end and the true end would wrongly begin a new block. The correct scan takes the maximum. The assertions run both versions on the two examples and on a random search, check the correct scan against a brute-force union over integer points, and confirm that the end-assigning version fails on the first example.

**Complexity.** O(n log n) time for the sort and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class OneCoversMany {
    static int[][] merge(int[][] intervals, boolean useMax) {
        int[][] sorted = new int[intervals.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = intervals[i].clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> out = new ArrayList<>();
        for (int[] cur : sorted) {
            if (out.isEmpty() || cur[0] > out.get(out.size() - 1)[1]) {
                out.add(new int[] {cur[0], cur[1]});
            } else {
                int[] last = out.get(out.size() - 1);
                last[1] = useMax ? Math.max(last[1], cur[1]) : cur[1];
            }
        }
        return out.toArray(new int[out.size()][]);
    }
    static int[][] pointOracle(int[][] intervals) {
        boolean[] covered = new boolean[80];
        for (int[] iv : intervals) for (int v = 2 * iv[0]; v <= 2 * iv[1]; v++) covered[v] = true;
        List<int[]> out = new ArrayList<>();
        int v = 0;
        while (v < covered.length) {
            if (!covered[v]) { v++; continue; }
            int s = v;
            while (v + 1 < covered.length && covered[v + 1]) v++;
            out.add(new int[] {s / 2, v / 2});
            v++;
        }
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        int[][] ex1 = {{1, 10}, {2, 3}, {4, 5}, {10, 12}, {13, 14}};
        if (!Arrays.deepEquals(merge(ex1, true), new int[][] {{1, 12}, {13, 14}})) throw new AssertionError("example 1");
        int[][] ex2 = {{0, 5}, {1, 2}, {3, 4}};
        if (!Arrays.deepEquals(merge(ex2, true), new int[][] {{0, 5}})) throw new AssertionError("example 2");
        if (Arrays.deepEquals(merge(ex2, false), new int[][] {{0, 5}})) throw new AssertionError("assigning the end must shrink the block on example 2");
        if (!Arrays.deepEquals(merge(ex2, false), new int[][] {{0, 2}, {3, 4}})) throw new AssertionError("the end-assigning merge splits after the shrunk end 2");
        Random rnd = new Random(10303);
        boolean wrongVersionFailed = false;
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); a[i][0] = s; a[i][1] = s + rnd.nextInt(8); }
            int[][] expected = pointOracle(a);
            if (!Arrays.deepEquals(merge(a, true), expected)) throw new AssertionError("differs on " + Arrays.deepToString(a));
            if (!Arrays.deepEquals(merge(a, false), expected)) wrongVersionFailed = true;
        }
        if (!wrongVersionFailed) throw new AssertionError("the end-assigning version should fail on some input");
    }
}
```

#### Solution: [Recognize] Insert Interval (LeetCode 57)
<!-- id: iv-insert-interval -->

**Approach.** The list is already sorted and disjoint, so one pass in three regions is enough. First copy every interval that ends before the new interval starts. Then, while the next interval starts no later than the current end of the new interval, grow the new interval to the smaller start and the larger end and skip that interval. Emit the grown interval, and copy the rest unchanged. Because the input is disjoint, the order is preserved, and no sort is needed. The oracle inserts the new interval into the list and runs a sort-and-merge over everything, and the assertions compare on random sorted disjoint lists with gaps between neighbours, including a new interval before, after and across the list.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class InsertInterval {
    static int[][] insert(int[][] board, int[] add) {
        List<int[]> out = new ArrayList<>();
        int i = 0, n = board.length;
        while (i < n && board[i][1] < add[0]) out.add(board[i++]);
        int lo = add[0], hi = add[1];
        while (i < n && board[i][0] <= hi) {
            lo = Math.min(lo, board[i][0]);
            hi = Math.max(hi, board[i][1]);
            i++;
        }
        out.add(new int[] {lo, hi});
        while (i < n) out.add(board[i++]);
        return out.toArray(new int[out.size()][]);
    }
    static int[][] oracle(int[][] board, int[] add) {
        List<int[]> all = new ArrayList<>(Arrays.asList(board));
        all.add(add);
        all.sort((a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> out = new ArrayList<>();
        for (int[] cur : all) {
            if (out.isEmpty() || cur[0] > out.get(out.size() - 1)[1]) out.add(new int[] {cur[0], cur[1]});
            else out.get(out.size() - 1)[1] = Math.max(out.get(out.size() - 1)[1], cur[1]);
        }
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        int[][] board = {{1, 2}, {3, 5}, {6, 7}, {8, 10}, {12, 16}};
        if (!Arrays.deepEquals(insert(board, new int[] {4, 8}), new int[][] {{1, 2}, {3, 10}, {12, 16}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(insert(new int[][] {{1, 3}, {6, 9}}, new int[] {2, 5}), new int[][] {{1, 5}, {6, 9}})) throw new AssertionError("example 2");
        if (!Arrays.deepEquals(insert(new int[0][], new int[] {5, 7}), new int[][] {{5, 7}})) throw new AssertionError("empty list");
        Random rnd = new Random(10304);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(7);
            int[][] a = new int[n][2];
            int cur = rnd.nextInt(3);
            for (int i = 0; i < n; i++) {
                a[i][0] = cur;
                a[i][1] = cur + rnd.nextInt(4);
                cur = a[i][1] + 1 + rnd.nextInt(3);
            }
            int s = rnd.nextInt(30);
            int[] add = {s, s + rnd.nextInt(8)};
            if (!Arrays.deepEquals(insert(a, add), oracle(a, add))) throw new AssertionError("differs on " + Arrays.deepToString(a) + " with " + Arrays.toString(add));
        }
    }
}
```
