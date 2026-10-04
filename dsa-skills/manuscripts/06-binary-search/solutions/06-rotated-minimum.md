<!-- solutions-for: 06-binary-search -->
### Solutions For The Minimum After Rotation

#### Solution: [Build] Find Minimum In Rotated Sorted Array (LeetCode 153)
<!-- id: bs-rotated-min-153 -->

**Approach.**
The array is a high ascending run followed by a low ascending run, or one run when the rotation is 0. The search compares `nums[mid]` with the right endpoint `nums[hi]`. A larger middle value lies in the high run, so the pivot is strictly right of `mid` and `lo` becomes `mid + 1`. Otherwise the part from `mid` to `hi` is ascending, so the minimum of that part is at `mid`, and `hi` becomes `mid`. The invariant is that the pivot lies inside `[lo, hi]`. The loop ends with the pivot, and the minimum is the value there.

**Complexity.**
- **Time** is O(log n), because each step halves the interval.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Random;

public final class RotatedMin153 {
    /**
     * Returns the minimum of a rotated ascending array of distinct values.
     * Time: O(log n). Space: O(1).
     * Invariant: the index of the minimum lies inside [lo, hi].
     */
    static int findMin(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        // The loop stops when one candidate index remains.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A middle value above the right endpoint sits in the high run; the pivot is right of it.
            if (nums[mid] > nums[hi]) lo = mid + 1;
            // Otherwise mid..hi is ascending, so the minimum is at mid or to its left.
            else hi = mid;
        }
        return nums[lo];
    }

    /** Builds a sorted array of distinct values rotated by k. */
    static int[] rotated(int n, int k, Random rnd) {
        int[] s = new int[n];
        int v = rnd.nextInt(5);
        for (int i = 0; i < n; i++) s[i] = v += 1 + rnd.nextInt(3);
        int[] r = new int[n];
        for (int i = 0; i < n; i++) r[i] = s[(i - k + n) % n];
        return r;
    }

    public static void main(String[] args) {
        // The statement examples and a single value.
        if (findMin(new int[] {6, 8, 9, 2, 4, 5}) != 2) throw new AssertionError("example 1");
        if (findMin(new int[] {4, 7, 9}) != 4) throw new AssertionError("example 2");
        if (findMin(new int[] {9}) != 9) throw new AssertionError("single");
        // Random rotations, including rotation 0, against a scan.
        Random rnd = new Random(61);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(15), k = rnd.nextInt(n);
            int[] a = rotated(n, k, rnd);
            int expect = a[0];
            for (int x : a) expect = Math.min(expect, x);
            if (findMin(a) != expect) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Rotation Count (Author exercise)
<!-- id: bs-rotation-count -->

**Approach.**
The rotation count equals the pivot index, because the smallest value of the sorted array starts at index 0 and moves right by `k` positions. The search is the one of the previous exercise, and it returns `lo` and not `nums[lo]`. An unrotated array keeps every middle value below the right endpoint, so `hi` moves to 0 and the answer is 0. The invariant keeps the pivot index inside `[lo, hi]`.

**Complexity.**
- **Time** is O(log n), because each step halves the interval.
- **Space** is O(1), because only three indexes are stored.

```java run
import java.util.Random;

public final class RotationCount {
    /**
     * Returns k for an ascending array of distinct values rotated by k.
     * Time: O(log n). Space: O(1).
     * Invariant: the pivot index lies inside [lo, hi].
     */
    static int rotationCount(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // High run: the pivot is to the right of mid.
            if (nums[mid] > nums[hi]) lo = mid + 1;
            // Otherwise the pivot is at mid or to its left.
            else hi = mid;
        }
        // The pivot index is the rotation count.
        return lo;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (rotationCount(new int[] {6, 8, 9, 2, 4, 5}) != 3) throw new AssertionError("example 1");
        if (rotationCount(new int[] {1, 5, 8}) != 0) throw new AssertionError("example 2");
        // Random rotations: rebuild the rotation and compare the count.
        Random rnd = new Random(62);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(15), k = rnd.nextInt(n);
            int[] s = new int[n];
            int v = 0;
            for (int i = 0; i < n; i++) s[i] = v += 1 + rnd.nextInt(3);
            int[] r = new int[n];
            for (int i = 0; i < n; i++) r[i] = s[(i - k + n) % n];
            if (rotationCount(r) != k) throw new AssertionError("random k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Two Values (Author exercise)
<!-- id: bs-two-values -->

**Approach.**
With two values, `lo = 0`, `hi = 1` and `mid = 0`, so `mid` equals `lo`. For `[2,1]`, the test `nums[0] > nums[1]` holds, so `lo` becomes `mid + 1 = 1`. The update drops index 0 and the interval shrinks to one index. For `[1,2]`, the test fails, so `hi` becomes `mid = 0`. The update drops index 1, and the interval shrinks again. A single value never enters the loop, so its step count is 0. In both two-value cases, one step ends the loop, and the pivot stays inside `[lo, hi]` throughout.

**Complexity.**
- **Time** is O(1), because the loop body runs at most once for these lengths.
- **Space** is O(1), because the result pair has fixed size.

```java run
import java.util.Arrays;

public final class TwoValues {
    /**
     * Returns {index of the minimum, loop steps} for a rotated array of distinct values.
     * Time: O(log n), which is O(1) for lengths 1 and 2. Space: O(1).
     * Invariant: the pivot lies inside [lo, hi].
     */
    static int[] pivotAndSteps(int[] nums) {
        int lo = 0, hi = nums.length - 1, steps = 0;
        while (lo < hi) {
            steps++;
            // For two values mid == lo, so both updates drop one index.
            int mid = lo + (hi - lo) / 2;
            if (nums[mid] > nums[hi]) lo = mid + 1; else hi = mid;
        }
        return new int[] {lo, steps};
    }

    public static void main(String[] args) {
        // The statement examples and the single value.
        if (!Arrays.equals(pivotAndSteps(new int[] {2, 1}), new int[] {1, 1})) throw new AssertionError("descending pair");
        if (!Arrays.equals(pivotAndSteps(new int[] {1, 2}), new int[] {0, 1})) throw new AssertionError("ascending pair");
        if (!Arrays.equals(pivotAndSteps(new int[] {5}), new int[] {0, 0})) throw new AssertionError("single");
        // The midpoint of an interval with two indexes equals lo.
        if (0 + (1 - 0) / 2 != 0) throw new AssertionError("midpoint of two");
    }
}
```

#### Solution: [Recognize] Find Minimum With Duplicates (LeetCode 154)
<!-- id: bs-rotated-min-154 -->

**Approach.**
Equal values break the decision. When `nums[mid] == nums[hi]`, the pivot may lie on either side, as in `[2,2,2,0,2]` and `[2,0,2,2,2]`. The move `hi--` is safe, because a copy of the same value remains at `mid`, so the minimum value stays inside the interval. The two strict cases keep the rule from the distinct-value exercise. The invariant is that the minimum value occurs inside `[lo, hi]`. An array of equal values takes `n - 1` steps, so the worst case is O(n), which the test measures.

**Complexity.**
- **Time** is O(log n) when few values repeat and O(n) in the worst case, because the equal case removes one index.
- **Space** is O(1), because the code stores only three indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotatedMin154 {
    static int steps;

    /**
     * Returns the minimum of a rotated non-decreasing array.
     * Time: O(log n) typical, O(n) worst case. Space: O(1).
     * Invariant: the minimum value occurs inside [lo, hi].
     */
    static int findMin(int[] nums) {
        int lo = 0, hi = nums.length - 1;
        steps = 0;
        while (lo < hi) {
            steps++;
            int mid = lo + (hi - lo) / 2;
            // Strictly larger: mid is in the high run, so the minimum is to its right.
            if (nums[mid] > nums[hi]) lo = mid + 1;
            // Strictly smaller: mid..hi is ascending, so the minimum is at mid or to its left.
            else if (nums[mid] < nums[hi]) hi = mid;
            // Equal: nothing is proved, so drop the right end; a copy remains at mid.
            else hi--;
        }
        return nums[lo];
    }

    public static void main(String[] args) {
        // The statement examples.
        if (findMin(new int[] {2, 2, 2, 0, 1}) != 0) throw new AssertionError("example 1");
        if (findMin(new int[] {3, 3, 1, 3}) != 1) throw new AssertionError("example 2");
        // Both ambiguous placements of the 0 still give 0.
        if (findMin(new int[] {2, 2, 2, 0, 2}) != 0 || findMin(new int[] {2, 0, 2, 2, 2}) != 0) throw new AssertionError("ambiguous");
        // The worst case is linear: an array of equal values takes n - 1 steps.
        int[] same = new int[1000];
        Arrays.fill(same, 4);
        findMin(same);
        if (steps != 999) throw new AssertionError("steps " + steps);
        // Random rotations with many duplicates against a scan.
        Random rnd = new Random(63);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14), k = rnd.nextInt(n);
            int[] s = rnd.ints(n, 0, 5).sorted().toArray();
            int[] r = new int[n];
            for (int i = 0; i < n; i++) r[i] = s[(i - k + n) % n];
            if (findMin(r) != s[0]) throw new AssertionError("random " + Arrays.toString(r));
        }
    }
}
```
