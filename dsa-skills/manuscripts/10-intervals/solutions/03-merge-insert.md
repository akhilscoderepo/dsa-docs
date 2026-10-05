<!-- solutions-for: 10-intervals -->
### Solutions For Merge And Insert

#### Solution: [Build] Merge Intervals (LeetCode 56)
<!-- id: iv-merge-intervals -->

**Approach.**
The method sorts a clone by start and then scans once while it keeps the result list. The last entry of the result is the active interval, and it is the only entry that a later window can overlap, because every later start is at least the active start. A window whose start is at most the active end joins the active interval, and the active end becomes the larger of the two ends. A window that starts after the active end cannot overlap the active interval or any later window, so the active interval is final and the window opens a new one. The method copies each row before it extends it, so the caller's rows stay unchanged. The invariant is that all entries before the last are final and disjoint from all unseen windows.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds one constant-time step per window.
- **Space** is O(n), because the sorted clone and the result each hold up to `n` entries.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeIntervals {
    /**
     * Returns the merged closed intervals ordered by start.
     * Time: O(n log n), the sort plus one linear scan.
     * Space: O(n), for the sorted clone and the result.
     * Invariant: entries before the last result entry are final and disjoint from unseen windows.
     */
    static int[][] merge(int[][] windows) {
        // Sort a clone so the caller's order stays the same.
        int[][] sorted = windows.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> result = new ArrayList<>();
        // One pass: each window is tested against the end of the last result entry only.
        for (int[] w : sorted) {
            // An empty result or a start after the active end means no overlap, so open a new interval.
            if (result.isEmpty() || result.get(result.size() - 1)[1] < w[0]) {
                // Copy the row so later extensions never change the caller's row.
                result.add(new int[] {w[0], w[1]});
            } else {
                // The window overlaps the active interval, so the active end keeps the larger end.
                int[] active = result.get(result.size() - 1);
                active[1] = Math.max(active[1], w[1]);
            }
        }
        // Convert the list to the required array type; this copies row references once.
        return result.toArray(new int[result.size()][]);
    }

    /** Reference: the insertion method from the lesson, which tests every result entry for each window. */
    static int[][] oracle(int[][] windows) {
        List<int[]> result = new ArrayList<>();
        for (int[] w : windows) {
            int start = w[0], end = w[1];
            List<int[]> kept = new ArrayList<>();
            // Absorb every result entry that overlaps the growing window.
            for (int[] r : result) {
                if (r[0] <= end && start <= r[1]) { start = Math.min(start, r[0]); end = Math.max(end, r[1]); }
                else kept.add(r);
            }
            kept.add(new int[] {start, end});
            result = kept;
        }
        result.sort((a, b) -> Integer.compare(a[0], b[0]));
        return result.toArray(new int[result.size()][]);
    }

    public static void main(String[] args) {
        // Example 1: [6,7] touches the end of [2,6] and joins it.
        int[][] a = {{8, 10}, {1, 3}, {2, 6}, {6, 7}, {15, 18}};
        if (!Arrays.deepEquals(merge(a), new int[][] {{1, 7}, {8, 10}, {15, 18}})) throw new AssertionError("example 1");
        // The lesson's outage windows give three bars.
        if (!Arrays.deepEquals(merge(new int[][] {{8, 10}, {1, 3}, {2, 6}, {15, 18}}), new int[][] {{1, 6}, {8, 10}, {15, 18}})) throw new AssertionError("outage windows");
        // Example 2: touching ends merge and the single point [7,7] stays.
        if (!Arrays.deepEquals(merge(new int[][] {{3, 4}, {1, 3}, {7, 7}}), new int[][] {{1, 4}, {7, 7}})) throw new AssertionError("example 2");
        // Empty input gives an empty result.
        if (merge(new int[0][]).length != 0) throw new AssertionError("empty");
        // The input array and its rows are unchanged after the call.
        if (!Arrays.deepEquals(a, new int[][] {{8, 10}, {1, 3}, {2, 6}, {6, 7}, {15, 18}})) throw new AssertionError("input mutated");
        // Random inputs agree with the insertion reference.
        Random rnd = new Random(20);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); in[i] = new int[] {s, s + rnd.nextInt(5)}; }
            if (!Arrays.deepEquals(merge(in), oracle(in))) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Vary] Merge Already-Sorted Intervals (Author exercise)
<!-- id: iv-merge-sorted -->

**Approach.**
The input contract supplies the order that the sort provided before, so the method skips the sort and runs the same scan. Each window joins the last result entry when its start is at most that entry's end, and otherwise opens a new entry. The scan visits each window once, so the whole method runs in linear time. The invariant is the same as in the previous exercise: entries before the last are final. The method would give a wrong answer on unsorted input, so the contract carries the correctness and the code does not check it.

**Complexity.**
- **Time** is O(n), because the scan visits each window once and does constant work.
- **Space** is O(n), because the result can hold one entry per window.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeSorted {
    /**
     * Returns the merged closed intervals of an input already ordered by start.
     * Time: O(n), one pass without a sort.
     * Space: O(n), for the result.
     * Invariant: entries before the last result entry are final.
     */
    static int[][] mergeSorted(int[][] sorted) {
        List<int[]> result = new ArrayList<>();
        // One pass over the ordered input.
        for (int[] w : sorted) {
            // No overlap with the active interval: copy the row and open a new interval.
            if (result.isEmpty() || result.get(result.size() - 1)[1] < w[0]) result.add(new int[] {w[0], w[1]});
            // Overlap: the active end becomes the larger end.
            else { int[] active = result.get(result.size() - 1); active[1] = Math.max(active[1], w[1]); }
        }
        return result.toArray(new int[result.size()][]);
    }

    /** Reference: coordinate marking over a small range, valid because touching closed intervals share a coordinate. */
    static int[][] oracle(int[][] in) {
        // Two intervals chain only when they share a coordinate, so link intervals by pairwise overlap.
        int n = in.length;
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < n; i++) for (int j = 0; j < n; j++)
                if (Math.max(in[i][0], in[j][0]) <= Math.min(in[i][1], in[j][1]) && label[i] != label[j]) {
                    int from = Math.max(label[i], label[j]), to = Math.min(label[i], label[j]);
                    for (int k = 0; k < n; k++) if (label[k] == from) label[k] = to;
                    changed = true;
                }
        }
        List<int[]> out = new ArrayList<>();
        boolean[] done = new boolean[n];
        // Each label becomes one merged interval from its smallest start to its largest end.
        for (int i = 0; i < n; i++) {
            if (done[label[i]]) continue;
            done[label[i]] = true;
            int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
            for (int k = 0; k < n; k++) if (label[k] == label[i]) { lo = Math.min(lo, in[k][0]); hi = Math.max(hi, in[k][1]); }
            out.add(new int[] {lo, hi});
        }
        out.sort((a, b) -> Integer.compare(a[0], b[0]));
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        // Example 1: the point [2,2] touches [1,2], and [6,7] sits inside [5,9].
        if (!Arrays.deepEquals(mergeSorted(new int[][] {{1, 2}, {2, 2}, {5, 9}, {6, 7}}), new int[][] {{1, 2}, {5, 9}})) throw new AssertionError("example 1");
        // Example 2: no two intervals share a coordinate, so nothing merges.
        int[][] b = {{0, 0}, {1, 1}, {2, 3}};
        if (!Arrays.deepEquals(mergeSorted(b), b)) throw new AssertionError("example 2");
        // Empty input.
        if (mergeSorted(new int[0][]).length != 0) throw new AssertionError("empty");
        // Random sorted inputs agree with the reference.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); in[i] = new int[] {s, s + rnd.nextInt(5)}; }
            Arrays.sort(in, (x, y) -> Integer.compare(x[0], y[0]));
            if (!Arrays.deepEquals(mergeSorted(in), oracle(in))) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Boundary] One Interval Covers Many (Author exercise)
<!-- id: iv-one-covers-many -->

**Approach.**
The scan keeps `activeEnd`, the largest end seen in the current group, and `size`, the number of input intervals in the group. An interval whose start is at most `activeEnd` joins the group, adds one to `size`, and raises `activeEnd` only if its own end is larger. An interval that starts after `activeEnd` closes the group, so the method appends `size` to the output and starts a new group of size 1. The boundary case is a long interval followed by short ones: setting `activeEnd` to the newest end would shrink it and split the group wrongly. The invariant is that `activeEnd` never decreases within a group.

**Complexity.**
- **Time** is O(n), because the loop visits each interval once.
- **Space** is O(n) for the output in the worst case, and O(1) beyond the output.

```java run
import java.util.Arrays;
import java.util.Random;

public final class GroupSizes {
    /**
     * Returns the number of input intervals absorbed by each merged interval.
     * Time: O(n), one pass.
     * Space: O(n) for the output, O(1) beyond it.
     * Invariant: activeEnd is the largest end of the current group and never decreases within it.
     */
    static int[] groupSizes(int[][] iv) {
        int[] out = new int[iv.length];
        int k = 0, size = 0;
        int activeEnd = 0;
        // One pass over the ordered input.
        for (int i = 0; i < iv.length; i++) {
            if (i > 0 && iv[i][0] <= activeEnd) {
                // The interval joins the group; the end keeps the maximum, never the newest end.
                size++;
                activeEnd = Math.max(activeEnd, iv[i][1]);
            } else {
                // A new group begins, so the previous size is final.
                if (i > 0) out[k++] = size;
                size = 1;
                activeEnd = iv[i][1];
            }
        }
        // The last group is closed by the end of the input.
        if (iv.length > 0) out[k++] = size;
        return Arrays.copyOf(out, k);
    }

    /** Wrong variant: it takes the newest end; used only to show the failure. */
    static int[] wrongSizes(int[][] iv) {
        int[] out = new int[iv.length];
        int k = 0, size = 0, activeEnd = 0;
        for (int i = 0; i < iv.length; i++) {
            if (i > 0 && iv[i][0] <= activeEnd) { size++; activeEnd = iv[i][1]; }
            else { if (i > 0) out[k++] = size; size = 1; activeEnd = iv[i][1]; }
        }
        if (iv.length > 0) out[k++] = size;
        return Arrays.copyOf(out, k);
    }

    /** Reference: sizes by pairwise chaining of the sorted intervals through a running maximum over all earlier ends. */
    static int[] oracle(int[][] iv) {
        int n = iv.length;
        int[] out = new int[n];
        int k = 0, i = 0;
        // A group extends while the next start is within the maximum end of every earlier member.
        while (i < n) {
            int j = i, max = iv[i][1];
            while (j + 1 < n && iv[j + 1][0] <= max) { j++; max = Math.max(max, iv[j][1]); }
            out[k++] = j - i + 1;
            i = j + 1;
        }
        return Arrays.copyOf(out, k);
    }

    public static void main(String[] args) {
        // Example 1: the first interval covers both later ones.
        if (!Arrays.equals(groupSizes(new int[][] {{1, 10}, {2, 3}, {4, 5}}), new int[] {3})) throw new AssertionError("example 1");
        // The newest-end variant splits this group, so it is wrong.
        if (Arrays.equals(wrongSizes(new int[][] {{1, 10}, {2, 3}, {4, 5}}), new int[] {3})) throw new AssertionError("wrong variant should fail");
        // Example 2: [20,25] touches the end of [0,20], and [26,27] stays apart.
        if (!Arrays.equals(groupSizes(new int[][] {{0, 20}, {1, 2}, {3, 4}, {20, 25}, {26, 27}}), new int[] {4, 1})) throw new AssertionError("example 2");
        // Empty input.
        if (groupSizes(new int[0][]).length != 0) throw new AssertionError("empty");
        // Random sorted inputs: the sizes match the reference and sum to the input length.
        Random rnd = new Random(22);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); in[i] = new int[] {s, s + rnd.nextInt(8)}; }
            Arrays.sort(in, (x, y) -> Integer.compare(x[0], y[0]));
            int[] got = groupSizes(in);
            if (!Arrays.equals(got, oracle(in))) throw new AssertionError("random " + Arrays.deepToString(in));
            if (Arrays.stream(got).sum() != n) throw new AssertionError("sum");
        }
    }
}
```

#### Solution: [Recognize] Insert Interval (LeetCode 57)
<!-- id: iv-insert-interval -->

**Approach.**
The list is sorted by start and has no overlaps, so the intervals that overlap the new one form one unbroken block. The method uses one index and three loops. The first loop copies every interval whose end is below the new start, since those cannot overlap it. The second loop absorbs every interval whose start is at most the grown end, taking the smaller start and the larger end, and it stops at the first interval that starts after the grown end. The method then writes the grown interval and the third loop copies the rest. The invariant is that every interval before index `i` is either in the output or absorbed into the grown interval.

**Complexity.**
- **Time** is O(n), because the three loops share one index that moves from 0 to `n` once.
- **Space** is O(n), because the output holds up to `n + 1` intervals.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class InsertInterval {
    /**
     * Returns the intervals of a sorted disjoint list together with one new closed interval, merged.
     * Time: O(n), one index crosses the list once.
     * Space: O(n), for the output.
     * Invariant: each interval before index i is already in the output or absorbed into the grown interval.
     */
    static int[][] insert(int[][] list, int[] add) {
        List<int[]> result = new ArrayList<>();
        int i = 0, n = list.length;
        int start = add[0], end = add[1];
        // Part one: intervals that end before the new start cannot overlap it.
        while (i < n && list[i][1] < start) result.add(list[i++]);
        // Part two: intervals that start at or before the grown end overlap it, so absorb them.
        while (i < n && list[i][0] <= end) {
            start = Math.min(start, list[i][0]);
            end = Math.max(end, list[i][1]);
            i++;
        }
        // The grown interval is final here, because every later interval starts after its end.
        result.add(new int[] {start, end});
        // Part three: the rest start after the grown end and are copied unchanged.
        while (i < n) result.add(list[i++]);
        return result.toArray(new int[result.size()][]);
    }

    /** Reference: append the new interval, sort by start, then merge. */
    static int[][] oracle(int[][] list, int[] add) {
        int[][] all = Arrays.copyOf(list, list.length + 1);
        all[list.length] = add;
        Arrays.sort(all, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> out = new ArrayList<>();
        for (int[] w : all) {
            if (out.isEmpty() || out.get(out.size() - 1)[1] < w[0]) out.add(new int[] {w[0], w[1]});
            else out.get(out.size() - 1)[1] = Math.max(out.get(out.size() - 1)[1], w[1]);
        }
        return out.toArray(new int[out.size()][]);
    }

    public static void main(String[] args) {
        // Example 1: the new interval bridges [6,7] and [9,12].
        if (!Arrays.deepEquals(insert(new int[][] {{2, 4}, {6, 7}, {9, 12}}, new int[] {5, 10}), new int[][] {{2, 4}, {5, 12}})) throw new AssertionError("example 1");
        // Example 2: the new interval touches both neighbours.
        if (!Arrays.deepEquals(insert(new int[][] {{1, 2}, {3, 5}}, new int[] {2, 3}), new int[][] {{1, 5}})) throw new AssertionError("example 2");
        // The lesson trace: [4,9] absorbs three entries.
        if (!Arrays.deepEquals(insert(new int[][] {{1, 2}, {3, 5}, {6, 7}, {8, 10}, {12, 16}}, new int[] {4, 9}), new int[][] {{1, 2}, {3, 10}, {12, 16}})) throw new AssertionError("trace");
        // An empty list gives just the new interval.
        if (!Arrays.deepEquals(insert(new int[0][], new int[] {7, 7}), new int[][] {{7, 7}})) throw new AssertionError("empty");
        // A new interval between two intervals touches neither.
        if (!Arrays.deepEquals(insert(new int[][] {{1, 2}, {5, 6}}, new int[] {3, 4}), new int[][] {{1, 2}, {3, 4}, {5, 6}})) throw new AssertionError("gap");
        // Random sorted disjoint lists agree with the append-sort-merge reference.
        Random rnd = new Random(23);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(7), pos = rnd.nextInt(3);
            int[][] list = new int[n][];
            for (int i = 0; i < n; i++) { int s = pos; int e = s + rnd.nextInt(4); list[i] = new int[] {s, e}; pos = e + 1 + rnd.nextInt(3); }
            int s = rnd.nextInt(25), e = s + rnd.nextInt(8);
            int[] add = {s, e};
            if (!Arrays.deepEquals(insert(list, add), oracle(list, add))) throw new AssertionError("random " + Arrays.deepToString(list) + Arrays.toString(add));
        }
    }
}
```
