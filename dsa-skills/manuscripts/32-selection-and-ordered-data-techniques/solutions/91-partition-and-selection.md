<!-- solutions-for: 32-selection-and-ordered-data-techniques -->
### Solutions For Partition And Selection

#### Solution: [Build] Kth Largest Element In An Array With Position Range (LeetCode 215)
<!-- id: ps-kth-range -->

**Approach.** The search partitions the current range into larger entries, equal entries and smaller entries, in that order, so the sorted-descending index of each block is known from counts alone.

The variable `before` counts the entries already discarded on the larger side. If the target index `k - 1` is below `before + big`, the larger block holds it and the search keeps that block. If it is at or past `before + big + same`, the smaller block holds it, and `before` grows by `big + same`. Otherwise the pivot is the answer, the first index of the range is `before + big`, and the last is that value plus `same - 1`. The invariant is that every discarded entry on the larger side is greater than every entry in the range, so `before` is exactly the number of entries above the range.

**Complexity.**

- **Time** is expected O(n), because a random pivot shrinks the range by a constant factor in expectation and each round scans the range once.
- **Space** is O(n) for the working copy, because the input must stay unchanged.

```java run
import java.util.*;

public final class KthRange {
    /**
     * Returns {value, firstIndex, lastIndex} of the k-th largest entry in non-increasing order.
     * Time: expected O(n). Space: O(n) for the copy.
     * Invariant: before counts the discarded entries that are larger than everything in a[lo..hi].
     */
    static int[] kthRange(int[] nums, int k, Random rnd) {
        // Copy so the caller's array stays unchanged.
        int[] a = nums.clone();
        // The range starts as the whole array and nothing is discarded yet.
        int lo = 0, hi = a.length - 1, before = 0;
        // Each round removes at least the equal block, so the loop ends.
        while (true) {
            // A random pivot index avoids a fixed worst-case input.
            int pivot = a[lo + rnd.nextInt(hi - lo + 1)];
            // gt..: larger entries go to the front of the range, smaller ones to the back.
            int big = lo, i = lo, small = hi;
            // One scan of the range costs O(hi - lo + 1).
            while (i <= small) {
                // A larger entry swaps into the front block.
                if (a[i] > pivot) { int t = a[big]; a[big] = a[i]; a[i] = t; big++; i++; }
                // A smaller entry swaps into the back block, and the swapped-in entry is unread.
                else if (a[i] < pivot) { int t = a[small]; a[small] = a[i]; a[i] = t; small--; }
                // An equal entry stays in the middle.
                else i++;
            }
            // Descending index of the first and last equal entry in the whole array.
            int first = before + (big - lo), last = before + (small - lo);
            // The target lies in the larger block: keep only that block.
            if (k - 1 < first) hi = big - 1;
            // The target lies in the smaller block: discard the larger and equal blocks.
            else if (k - 1 > last) { before = last + 1; lo = small + 1; }
            // The target lies in the equal block: the pivot is the answer.
            else return new int[]{pivot, first, last};
        }
    }

    public static void main(String[] args) {
        // Checks Example 1 with ties in the answer.
        if (!Arrays.equals(kthRange(new int[]{4, 9, 4, 1, 4, 9, 6}, 5, new Random(1)), new int[]{4, 3, 5})) throw new AssertionError("example 1");
        // Checks Example 2 where all entries tie.
        if (!Arrays.equals(kthRange(new int[]{5, 5, 5, 5}, 3, new Random(1)), new int[]{5, 0, 3})) throw new AssertionError("example 2");
        // Checks the extreme value and that the input is not mutated.
        int[] in = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0};
        if (!Arrays.equals(kthRange(in, 3, new Random(1)), new int[]{Integer.MIN_VALUE, 2, 2})) throw new AssertionError("extreme");
        if (!Arrays.equals(in, new int[]{Integer.MIN_VALUE, Integer.MAX_VALUE, 0})) throw new AssertionError("mutated");
        // Compares with a sort-based oracle on random inputs.
        Random rnd = new Random(3201);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(12);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(6) - 3;
            int k = 1 + rnd.nextInt(n);
            Integer[] s = new Integer[n];
            for (int i = 0; i < n; i++) s[i] = v[i];
            Arrays.sort(s, Collections.reverseOrder());
            int val = s[k - 1], f = -1, l = -1;
            for (int i = 0; i < n; i++) if (s[i] == val) { if (f < 0) f = i; l = i; }
            if (!Arrays.equals(kthRange(v, k, rnd), new int[]{val, f, l})) throw new AssertionError("random " + iter);
        }
    }
}
```

#### Solution: [Vary] K Closest Points To Origin With Tie Counts (LeetCode 973)
<!-- id: ps-closest-ties -->

**Approach.** The code builds a `long[]` of squared distances and applies quickselect with a two-way partition to that array. Selecting on the derived array leaves the points unchanged, and one final pass over the distances counts the entries below and equal to the selected value.

The conversion `(long) x * x` widens before multiplying. Without the cast, `x * x` is computed in `int` and wraps for `x` above 46,340. The invariant of the partition is that after each round the pivot index holds the value that belongs there, so the target index lies in exactly one side or equals the pivot index.

**Complexity.**

- **Time** is expected O(n), with one pass to build the distances, expected linear selection and one counting pass.
- **Space** is O(n) for the distance array.

```java run
import java.util.*;

public final class ClosestTies {
    /**
     * Returns {d, countBelow, countEqual} for the k-th smallest squared distance.
     * Time: expected O(n). Space: O(n).
     * Invariant: after each partition the pivot sits at its final index inside lo..hi.
     */
    static long[] boundary(int[][] points, int k, Random rnd) {
        int n = points.length;
        // Widen before multiplying so the product cannot wrap.
        long[] d = new long[n];
        for (int i = 0; i < n; i++) d[i] = (long) points[i][0] * points[i][0] + (long) points[i][1] * points[i][1];
        // Zero-based target rank in increasing order.
        int target = k - 1, lo = 0, hi = n - 1;
        // The loop ends when the pivot index equals the target.
        while (lo < hi) {
            // Move a random pivot to the end of the range for a Lomuto partition.
            int p = lo + rnd.nextInt(hi - lo + 1);
            long pv = d[p]; d[p] = d[hi]; d[hi] = pv;
            // store marks the end of the block of entries smaller than the pivot.
            int store = lo;
            for (int i = lo; i < hi; i++) {
                // A smaller entry joins the front block.
                if (d[i] < pv) { long t = d[store]; d[store] = d[i]; d[i] = t; store++; }
            }
            // Place the pivot at its final index.
            d[hi] = d[store]; d[store] = pv;
            // Keep the side that holds the target, or stop when the pivot index is the target.
            if (target < store) hi = store - 1;
            else if (target > store) lo = store + 1;
            else lo = hi = store;
        }
        long val = d[target];
        // One counting pass reads the tie boundary.
        long below = 0, equal = 0;
        for (long x : d) { if (x < val) below++; else if (x == val) equal++; }
        return new long[]{val, below, equal};
    }

    public static void main(String[] args) {
        // Checks Example 1 with four tied points.
        if (!Arrays.equals(boundary(new int[][]{{3, 4}, {-3, -4}, {0, 5}, {1, 1}, {5, 0}}, 3, new Random(1)), new long[]{25, 1, 4})) throw new AssertionError("example 1");
        // Checks Example 2 where the squared distance exceeds the int range.
        if (!Arrays.equals(boundary(new int[][]{{1000000000, 1000000000}, {0, 0}}, 2, new Random(1)), new long[]{2000000000000000000L, 1, 1})) throw new AssertionError("example 2");
        // Checks the Java behaviour that int multiplication wraps while the widened product does not.
        int x = 100000;
        if (x * x == (long) x * x) throw new AssertionError("int product should wrap");
        // Checks that the input points are unchanged.
        int[][] pts = {{2, 1}, {0, 0}};
        boundary(pts, 1, new Random(1));
        if (pts[0][0] != 2 || pts[1][0] != 0) throw new AssertionError("mutated");
        // Compares with a sort-based oracle on random inputs.
        Random rnd = new Random(3202);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(10);
            int[][] p = new int[n][2];
            long[] s = new long[n];
            for (int i = 0; i < n; i++) {
                p[i][0] = rnd.nextInt(7) - 3; p[i][1] = rnd.nextInt(7) - 3;
                s[i] = (long) p[i][0] * p[i][0] + (long) p[i][1] * p[i][1];
            }
            int k = 1 + rnd.nextInt(n);
            long[] sorted = s.clone();
            Arrays.sort(sorted);
            long v = sorted[k - 1], b = 0, e = 0;
            for (long y : s) { if (y < v) b++; else if (y == v) e++; }
            if (!Arrays.equals(boundary(p, k, rnd), new long[]{v, b, e})) throw new AssertionError("random " + iter);
        }
    }
}
```

#### Solution: [Boundary] Count Of Smaller Numbers After Self Within A Distance (LeetCode 315)
<!-- id: ps-window-smaller-right -->

**Approach.** Selection cannot answer this because the result differs for every index, so the solution sorts an array of indices by value with merge sort and counts during each merge.

When two halves are sorted by value, every index in the left half precedes every index in the right half. For a left entry `x`, the matching right entries are those with value in `[x - d, x)`. Two positions walk the sorted right half: `hiPos` stops at the first right value that is not below `x`, and `loPos` stops at the first right value that is not below `x - d`. The count `hiPos - loPos` is added to the answer of the left entry's original index. Both positions only move forward, because the left values ascend. The bound `x - d` is computed in `long`. The invariant is that, when a merge starts, each half is sorted by value and each half has already counted all pairs inside itself.

**Complexity.**

- **Time** is O(n log n), since the recursion has log n levels and each merge makes linear moves.
- **Space** is O(n) for the index array, the temporary array and the answers.

```java run
import java.util.*;

public final class WindowSmaller {
    /**
     * Counts, for each i, the later entries j with 0 < nums[i] - nums[j] <= d.
     * Time: O(n log n). Space: O(n).
     * Invariant: before a merge, both halves of idx are sorted by value and count their internal pairs.
     */
    static int[] count(int[] nums, long d) {
        int n = nums.length;
        int[] out = new int[n];
        // idx holds original positions and gets sorted by value.
        int[] idx = new int[n];
        for (int i = 0; i < n; i++) idx[i] = i;
        sort(nums, d, idx, new int[n], 0, n, out);
        return out;
    }

    private static void sort(int[] v, long d, int[] idx, int[] tmp, int lo, int hi, int[] out) {
        // A range of one entry has no pair.
        if (hi - lo < 2) return;
        int mid = (lo + hi) >>> 1;
        // Sort and count inside each half first.
        sort(v, d, idx, tmp, lo, mid, out);
        sort(v, d, idx, tmp, mid, hi, out);
        // Positions in the sorted right half; both only move forward.
        int hiPos = mid, loPos = mid;
        for (int a = lo; a < mid; a++) {
            long x = v[idx[a]];
            // Advance to the first right value that is not below x.
            while (hiPos < hi && v[idx[hiPos]] < x) hiPos++;
            // Advance to the first right value that is not below x - d.
            while (loPos < hi && v[idx[loPos]] < x - d) loPos++;
            // Right values in [x - d, x) are the smaller entries within the window.
            out[idx[a]] += hiPos - loPos;
        }
        // Standard merge by value restores the sorted order for the parent call.
        int l = lo, r = mid, t = lo;
        while (l < mid && r < hi) tmp[t++] = v[idx[l]] <= v[idx[r]] ? idx[l++] : idx[r++];
        while (l < mid) tmp[t++] = idx[l++];
        while (r < hi) tmp[t++] = idx[r++];
        System.arraycopy(tmp, lo, idx, lo, hi - lo);
    }

    public static void main(String[] args) {
        // Checks Example 1.
        if (!Arrays.equals(count(new int[]{8, 5, 7, 3, 5, 2}, 3), new int[]{3, 2, 1, 1, 1, 0})) throw new AssertionError("example 1");
        // Checks Example 2 where the difference exceeds the int range.
        if (!Arrays.equals(count(new int[]{Integer.MAX_VALUE, Integer.MIN_VALUE}, 4294967295L), new int[]{1, 0})) throw new AssertionError("example 2");
        // Checks the Java behaviour that the int difference wraps to a negative value.
        if (Integer.MAX_VALUE - Integer.MIN_VALUE >= 0) throw new AssertionError("int difference should wrap");
        // Checks d = 0 and that the input is unchanged.
        int[] in = {4, 1, 4};
        if (!Arrays.equals(count(in, 0), new int[]{0, 0, 0}) || !Arrays.equals(in, new int[]{4, 1, 4})) throw new AssertionError("zero window");
        // Compares with a double loop on random inputs.
        Random rnd = new Random(3203);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(12);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(9) - 4;
            long d = rnd.nextInt(8);
            int[] expect = new int[n];
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++)
                    if ((long) v[i] - v[j] > 0 && (long) v[i] - v[j] <= d) expect[i]++;
            if (!Arrays.equals(count(v, d), expect)) throw new AssertionError("random " + iter);
        }
    }
}
```

#### Solution: [Recognize] Reverse Pairs With A Triple Threshold (LeetCode 493)
<!-- id: ps-triple-pairs -->

**Approach.** A pair condition between two entries is a cross-pair question, so the solution uses merge counting on values and not selection.

After both halves are sorted ascending, each right entry `y` is checked against the left half. The left entries with value at least `3 * y` form a suffix of the sorted left half, and the pointer `p` marks where the suffix starts. As `y` ascends, `3 * y` ascends, so `p` only moves forward. The count added for `y` is `mid - p`. The product uses `3L * y` so it cannot overflow. The count is counted before the halves merge, so only pairs with the left entry earlier in the array are counted. The invariant is that both halves are sorted and have counted their internal pairs.

**Complexity.**

- **Time** is O(n log n), from log n levels of linear merges.
- **Space** is O(n) for the temporary array and the copy.

```java run
import java.util.*;

public final class TriplePairs {
    /**
     * Counts pairs i < j with nums[i] >= 3 * nums[j].
     * Time: O(n log n). Space: O(n).
     * Invariant: before counting a merge, both halves are sorted ascending and count their own pairs.
     */
    static long count(int[] nums) {
        int[] a = nums.clone();
        return sort(a, new int[a.length], 0, a.length);
    }

    private static long sort(int[] a, int[] tmp, int lo, int hi) {
        // A range of one entry has no pair.
        if (hi - lo < 2) return 0;
        int mid = (lo + hi) >>> 1;
        // Pairs inside each half.
        long total = sort(a, tmp, lo, mid) + sort(a, tmp, mid, hi);
        // p is the first left index whose value reaches the threshold.
        int p = lo;
        for (int r = mid; r < hi; r++) {
            // The threshold ascends with r, so p never moves back.
            while (p < mid && a[p] < 3L * a[r]) p++;
            // Every left entry from p to mid - 1 forms a counted pair.
            total += mid - p;
        }
        // Merge by value so the parent call sees sorted halves.
        int l = lo, r = mid, t = lo;
        while (l < mid && r < hi) tmp[t++] = a[l] <= a[r] ? a[l++] : a[r++];
        while (l < mid) tmp[t++] = a[l++];
        while (r < hi) tmp[t++] = a[r++];
        System.arraycopy(tmp, lo, a, lo, hi - lo);
        return total;
    }

    public static void main(String[] args) {
        // Checks Example 1.
        if (count(new int[]{9, 2, 6, -1, 3, -4}) != 10) throw new AssertionError("example 1");
        // Checks Example 2 where the non-strict comparison counts equal values.
        if (count(new int[]{0, 0, 0}) != 3) throw new AssertionError("example 2");
        // Checks the extreme pair, where the int product 3 * MIN_VALUE would wrap.
        if (count(new int[]{Integer.MAX_VALUE, Integer.MIN_VALUE}) != 1) throw new AssertionError("extreme");
        if (3 * Integer.MIN_VALUE == 3L * Integer.MIN_VALUE) throw new AssertionError("int product should wrap");
        // Checks that the input is unchanged.
        int[] in = {5, 1, 0};
        count(in);
        if (!Arrays.equals(in, new int[]{5, 1, 0})) throw new AssertionError("mutated");
        // Compares with a double loop on random inputs.
        Random rnd = new Random(3204);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(12);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(13) - 6;
            long expect = 0;
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++)
                    if (v[i] >= 3L * v[j]) expect++;
            if (count(v) != expect) throw new AssertionError("random " + iter);
        }
    }
}
```
