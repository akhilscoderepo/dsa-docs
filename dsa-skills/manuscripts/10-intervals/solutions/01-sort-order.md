<!-- solutions-for: 10-intervals -->
### Solutions For Sorting Intervals

#### Solution: [Build] Order By Start Then End (Author exercise)
<!-- id: iv-order-start-end -->

**Approach.**
The method clones the outer array so the caller's order survives, then sorts the clone with a comparator. The comparator compares starts first and falls back to ends only when the starts are equal, so every pair has a defined order. The invariant is that after the sort, `sorted[i]` never follows `sorted[i + 1]` under this comparator, and the clone leaves `intervals` untouched. The clone copies row references, so both arrays share the same rows.

**Complexity.**
- **Time** is O(n log n), because the sort makes about `n log n` comparator calls and each call takes constant time.
- **Space** is O(n), because the clone holds one reference per interval.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortStartEnd {
    /**
     * Returns the intervals ordered by start, then by end, without changing the input order.
     * Time: O(n log n), from the comparison sort.
     * Space: O(n), for the cloned array of row references.
     * Invariant: for every adjacent pair in the result, the first does not follow the second.
     */
    static int[][] sortByStart(int[][] intervals) {
        // Clone the outer array so the caller's order stays as given.
        int[][] sorted = intervals.clone();
        // The comparator decides by start, and by end only when the starts tie.
        Arrays.sort(sorted, (a, b) -> a[0] != b[0]
                ? Integer.compare(a[0], b[0])
                : Integer.compare(a[1], b[1]));
        // The sorted clone is the answer.
        return sorted;
    }

    /** Reference order by insertion sort with long keys, used only to check the method. */
    static int[][] oracle(int[][] in) {
        int[][] r = in.clone();
        // Insertion sort moves each element left past every larger element.
        for (int i = 1; i < r.length; i++) {
            int[] cur = r[i];
            int j = i - 1;
            // A pair is out of order when the start is larger, or the starts tie and the end is larger.
            while (j >= 0 && (r[j][0] > cur[0] || (r[j][0] == cur[0] && r[j][1] > cur[1]))) { r[j + 1] = r[j]; j--; }
            r[j + 1] = cur;
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1: the tie at start 1 is settled by the ends.
        int[][] a = {{5, 8}, {1, 4}, {1, 2}, {3, 6}};
        int[][] expect = {{1, 2}, {1, 4}, {3, 6}, {5, 8}};
        if (!Arrays.deepEquals(sortByStart(a), expect)) throw new AssertionError("example 1");
        // The input order is unchanged, which the clone guarantees.
        if (!Arrays.deepEquals(a, new int[][] {{5, 8}, {1, 4}, {1, 2}, {3, 6}})) throw new AssertionError("input mutated");
        // The clone shares the row objects with the input, so a changed row shows in both arrays.
        int[][] r = sortByStart(a);
        r[0][0] = 99;
        if (a[2][0] != 99) throw new AssertionError("rows are shared");
        a[2][0] = 1;
        // Example 2: equal intervals and an empty input.
        if (!Arrays.deepEquals(sortByStart(new int[][] {{2, 2}, {2, 2}, {1, 3}}), new int[][] {{1, 3}, {2, 2}, {2, 2}})) throw new AssertionError("example 2");
        if (sortByStart(new int[0][]).length != 0) throw new AssertionError("empty");
        // The object sort is stable: rows equal under the comparator keep their input order.
        int[] first = {4, 4}, second = {4, 4};
        int[][] tie = sortByStart(new int[][] {first, second});
        if (tie[0] != first || tie[1] != second) throw new AssertionError("stable");
        // Random inputs agree with the insertion-sort reference.
        Random rnd = new Random(1);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(7), e = s + rnd.nextInt(4); in[i] = new int[] {s, e}; }
            if (!Arrays.deepEquals(sortByStart(in), oracle(in))) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Vary] Order By End Then Start (Author exercise)
<!-- id: iv-order-end-start -->

**Approach.**
The comparator swaps the key positions, so the end decides first and the start breaks ties. After this sort the first interval has the smallest end of all. A choice of the first interval therefore leaves the largest remaining range to its right, so any set of pairwise disjoint intervals can swap its first member for it without losing a member. That is the decision this order enables: take the earliest finishing interval, discard the ones that overlap it, and repeat. The invariant is that every interval before position `i` has an end no larger than the end at `i`.

**Complexity.**
- **Time** is O(n log n), because the comparison sort dominates and the comparator takes constant time.
- **Space** is O(n), because the clone holds one reference per interval.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortEndStart {
    /**
     * Returns the intervals ordered by end, then by start, without changing the input order.
     * Time: O(n log n), from the comparison sort.
     * Space: O(n), for the cloned array of row references.
     * Invariant: ends never decrease from one position to the next.
     */
    static int[][] sortByEnd(int[][] intervals) {
        // Clone so the caller's array keeps its order.
        int[][] sorted = intervals.clone();
        // The end decides first, and the start breaks a tie.
        Arrays.sort(sorted, (a, b) -> a[1] != b[1]
                ? Integer.compare(a[1], b[1])
                : Integer.compare(a[0], b[0]));
        // The sorted clone is the answer.
        return sorted;
    }

    /** Largest set of pairwise disjoint closed intervals by trying all subsets; used only as a reference. */
    static int bruteMaxDisjoint(int[][] in) {
        int best = 0, n = in.length;
        // Each bitmask picks one subset of the intervals.
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            int size = 0;
            for (int i = 0; i < n && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                size++;
                // A chosen pair must not share a point.
                for (int j = i + 1; j < n; j++)
                    if ((mask >> j & 1) == 1 && in[i][0] <= in[j][1] && in[j][0] <= in[i][1]) { ok = false; break; }
            }
            if (ok) best = Math.max(best, size);
        }
        return best;
    }

    /** Greedy count over the end order: keep an interval when it starts after the last kept end. */
    static int greedyMaxDisjoint(int[][] in) {
        int[][] s = sortByEnd(in);
        int count = 0;
        // lastEnd starts below every value, so the first interval is always kept.
        long lastEnd = Long.MIN_VALUE;
        for (int[] iv : s) {
            // Keep the interval only when it shares no point with the last kept one.
            if (iv[0] > lastEnd) { count++; lastEnd = iv[1]; }
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1: the short interval [2,3] comes before the long interval [1,10].
        if (!Arrays.deepEquals(sortByEnd(new int[][] {{1, 10}, {2, 3}, {4, 5}}), new int[][] {{2, 3}, {4, 5}, {1, 10}})) throw new AssertionError("example 1");
        // Example 2: equal ends order by start.
        if (!Arrays.deepEquals(sortByEnd(new int[][] {{3, 6}, {1, 6}, {2, 4}}), new int[][] {{2, 4}, {1, 6}, {3, 6}})) throw new AssertionError("example 2");
        // The input stays in its original order.
        int[][] in = {{3, 6}, {1, 6}, {2, 4}};
        sortByEnd(in);
        if (in[0][0] != 3 || in[2][0] != 2) throw new AssertionError("input mutated");
        // The earliest finishing interval leads the order, and the greedy count matches the exhaustive count.
        Random rnd = new Random(2);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(9);
            int[][] a = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(9), e = s + rnd.nextInt(5); a[i] = new int[] {s, e}; }
            int[][] s = sortByEnd(a);
            for (int i = 1; i < n; i++) if (s[i - 1][1] > s[i][1]) throw new AssertionError("end order");
            if (greedyMaxDisjoint(a) != bruteMaxDisjoint(a)) throw new AssertionError("greedy " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Boundary] Equal And Extreme Endpoints (Author exercise)
<!-- id: iv-extreme-endpoints -->

**Approach.**
The comparator calls `Integer.compare`, which answers from the two values directly and never forms their difference. A subtraction comparator fails because `a - b` can leave the `int` range and wrap to the opposite sign. For starts `-2,000,000,000` and `2,000,000,000` the wrapped value is negative, so the subtraction version places the larger start first. The invariant is that the sign of the comparator result equals the sign of the true comparison for every pair of `int` values, including both extremes.

**Complexity.**
- **Time** is O(n log n), because the comparison sort dominates and each comparison takes constant time.
- **Space** is O(n), because the clone holds one reference per interval.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortExtreme {
    /**
     * Returns the intervals ordered by start, then end, for any int values.
     * Time: O(n log n), from the comparison sort.
     * Space: O(n), for the cloned array.
     * Invariant: the comparator sign matches the true comparison, because it never subtracts.
     */
    static int[][] sortSafe(int[][] intervals) {
        // Clone so the caller's order survives.
        int[][] sorted = intervals.clone();
        // Integer.compare reads both values and returns -1, 0 or 1 without any arithmetic.
        Arrays.sort(sorted, (a, b) -> a[0] != b[0]
                ? Integer.compare(a[0], b[0])
                : Integer.compare(a[1], b[1]));
        return sorted;
    }

    /** The unsafe comparator the lesson warns about; used only to show the failure. */
    static int[][] sortBySubtraction(int[][] intervals) {
        int[][] sorted = intervals.clone();
        // The subtraction can wrap, so the sign may be wrong for far-apart starts.
        Arrays.sort(sorted, (a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
        return sorted;
    }

    public static void main(String[] args) {
        // Example 1: both extremes and a tie at start 0.
        int[][] a = {{Integer.MAX_VALUE, Integer.MAX_VALUE}, {Integer.MIN_VALUE, 0}, {0, 5}, {0, 3}};
        int[][] expect = {{Integer.MIN_VALUE, 0}, {0, 3}, {0, 5}, {Integer.MAX_VALUE, Integer.MAX_VALUE}};
        if (!Arrays.deepEquals(sortSafe(a), expect)) throw new AssertionError("example 1");
        // Example 2: the true order puts -2,000,000,000 first.
        int[][] b = {{2000000000, 2000000000}, {-2000000000, 1}};
        if (!Arrays.deepEquals(sortSafe(b), new int[][] {{-2000000000, 1}, {2000000000, 2000000000}})) throw new AssertionError("example 2");
        // The wrapped difference is negative although the true difference is positive.
        if (2000000000 - (-2000000000) >= 0) throw new AssertionError("difference should wrap negative");
        // The subtraction comparator therefore sorts the same pair into the wrong order.

        if (sortBySubtraction(b)[0][0] != 2000000000) throw new AssertionError("subtraction puts the larger start first");
        // Random extreme values: the safe order is non-decreasing by the long-valued key.
        Random rnd = new Random(3);
        int[] pool = {Integer.MIN_VALUE, Integer.MIN_VALUE + 1, -1, 0, 1, Integer.MAX_VALUE - 1, Integer.MAX_VALUE};
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) {
                int s = pool[rnd.nextInt(pool.length)], e = pool[rnd.nextInt(pool.length)];
                in[i] = new int[] {Math.min(s, e), Math.max(s, e)};
            }
            int[][] r = sortSafe(in);
            // Compare neighbours with long arithmetic so the check itself cannot wrap.
            for (int i = 1; i < n; i++) {
                long d = (long) r[i - 1][0] - r[i][0];
                if (d > 0 || (d == 0 && r[i - 1][1] > r[i][1])) throw new AssertionError("order " + Arrays.deepToString(in));
            }
        }
    }
}
```

#### Solution: [Recognize] Count Groups After Merging (LeetCode 56)
<!-- id: iv-count-merged-groups -->

**Approach.**
The method sorts by start, then scans once while it keeps the largest end of the current group. When the next start is larger than that end, the interval shares no point with the group, because every earlier interval in the group ends at or before the group end, and the method counts a new group. Otherwise the interval joins the group and the group end becomes the larger of the two ends. Sorting by start is what lets one number, the group end, stand for all earlier intervals. The invariant is that `groupEnd` equals the largest end among the intervals of the last group.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the scan adds O(n).
- **Space** is O(n), because the sorted clone holds one reference per interval.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CountGroups {
    /**
     * Returns the number of groups of chained closed intervals.
     * Time: O(n log n), the sort plus one linear scan.
     * Space: O(n), for the cloned array.
     * Invariant: groupEnd is the largest end in the last group.
     */
    static int countGroups(int[][] intervals) {
        // An empty input has no groups.
        if (intervals.length == 0) return 0;
        // Sort by start so the next start can reach only the last group.
        int[][] s = intervals.clone();
        Arrays.sort(s, (a, b) -> Integer.compare(a[0], b[0]));
        // The first interval opens the first group.
        int groups = 1;
        int groupEnd = s[0][1];
        // One pass: the loop runs n - 1 times and does constant work each time.
        for (int i = 1; i < s.length; i++) {
            // A start above the group end shares no point with the group, so a new group begins.
            if (s[i][0] > groupEnd) { groups++; groupEnd = s[i][1]; }
            // Otherwise the interval joins the group and may extend its end.
            else groupEnd = Math.max(groupEnd, s[i][1]);
        }
        return groups;
    }

    /** Reference count: union-find style labelling over all pairs, O(n^3) in the worst case. */
    static int oracle(int[][] in) {
        int n = in.length;
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        // Relabel until no overlapping pair carries different labels.
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (in[i][0] <= in[j][1] && in[j][0] <= in[i][1] && label[i] != label[j]) {
                        int from = Math.max(label[i], label[j]), to = Math.min(label[i], label[j]);
                        for (int k = 0; k < n; k++) if (label[k] == from) label[k] = to;
                        changed = true;
                    }
        }
        // The group count is the number of distinct labels.
        return (int) Arrays.stream(label).distinct().count();
    }

    public static void main(String[] args) {
        // The opening example: arrival order hides the shared hours of [1,4] and [2,5].
        if (countGroups(new int[][] {{1, 4}, {7, 9}, {2, 5}}) != 2) throw new AssertionError("example 1");
        // Touching closed intervals chain: [1,3],[3,5] share the point 3.
        if (countGroups(new int[][] {{1, 3}, {3, 5}, {6, 8}, {10, 12}, {11, 13}}) != 3) throw new AssertionError("example 2");
        // Empty input.
        if (countGroups(new int[0][]) != 0) throw new AssertionError("empty");
        // Sorting by end instead breaks the one-number summary on this input.
        int[][] trap = {{1, 10}, {2, 3}, {4, 5}};
        if (countGroups(trap) != 1) throw new AssertionError("one group");
        // Random inputs agree with the all-pairs reference.
        Random rnd = new Random(4);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(12), e = s + rnd.nextInt(4); in[i] = new int[] {s, e}; }
            if (countGroups(in) != oracle(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```
