<!-- solutions-for: 06-binary-search -->
### Solutions For Sorted Value Search

#### Solution: [Build] Binary Search (LeetCode 704)
<!-- id: bs-exact-704 -->

**Approach.**
The search interval starts as the whole array. Each step compares `nums[mid]` with the target. A smaller value means the sort order puts every index up to `mid` below the target, so `lo` moves to `mid + 1`. A larger value moves `hi` to `mid - 1`. Equality returns at once. The invariant is that a present target always lies inside `[lo, hi]`, so an empty interval proves absence. An empty array starts with `hi = -1` and returns `-1` without entering the loop.

**Complexity.**
- **Time** is O(log n), because each step removes `mid` and at least half of the remaining indexes.
- **Space** is O(1), because the code stores only `lo`, `hi` and `mid`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ExactSearch704 {
    /**
     * Returns the index of target in the ascending array nums, or -1 when absent.
     * Time: O(log n), because the interval halves each step.
     * Space: O(1), because only three indexes are stored.
     * Invariant: if target occurs in nums, its index lies in [lo, hi].
     */
    static int search(int[] nums, int target) {
        // The closed interval starts as the whole array.
        int lo = 0, hi = nums.length - 1;
        // The loop runs while at least one candidate index remains.
        while (lo <= hi) {
            // The subtraction form cannot overflow for any int indexes.
            int mid = lo + (hi - lo) / 2;
            // Equality ends the search with the answer.
            if (nums[mid] == target) return mid;
            // A smaller middle value discards indexes lo..mid.
            if (nums[mid] < target) lo = mid + 1;
            // A larger middle value discards indexes mid..hi.
            else hi = mid - 1;
        }
        // An empty interval proves that the target is absent.
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (search(new int[] {-1, 0, 3, 5, 9, 12}, 9) != 4) throw new AssertionError("found");
        if (search(new int[] {5}, 2) != -1) throw new AssertionError("absent");
        // The empty array never enters the loop.
        if (search(new int[0], 7) != -1) throw new AssertionError("empty");
        // The overflow claim: (lo + hi) wraps to a negative int, the subtraction form does not.
        int lo = 2_000_000_000, hi = 2_100_000_000;
        if ((lo + hi) / 2 >= 0) throw new AssertionError("sum should wrap");
        if (lo + (hi - lo) / 2 != 2_050_000_000) throw new AssertionError("safe midpoint");
        // The library returns -(insertion point) - 1 for a missing value, not -1.
        if (Arrays.binarySearch(new int[] {1, 3}, 2) != -2) throw new AssertionError("library contract");
        // Random sorted arrays are checked against a linear scan, for present and absent targets.
        Random rnd = new Random(7);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] a = rnd.ints(n, -20, 20).distinct().sorted().toArray();
            int target = rnd.nextInt(50) - 25;
            int expect = -1;
            for (int i = 0; i < a.length; i++) if (a[i] == target) expect = i;
            if (search(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Vary] Descending Search (Author exercise)
<!-- id: bs-descending -->

**Approach.**
The array is descending. A middle value smaller than the target means the target, if present, sits on the left, where the larger values are. The rule mirrors the ascending one. A smaller `nums[mid]` sets `hi = mid - 1`, and a larger `nums[mid]` sets `lo = mid + 1`. The loop shape, the interval and the invariant stay the same.

**Complexity.**
- **Time** is O(log n), because the interval still halves each step.
- **Space** is O(1), because only the bounds and the midpoint are stored.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DescendingSearch {
    /**
     * Returns the index of target in a strictly descending array, or -1.
     * Time: O(log n), because the interval halves each step.
     * Space: O(1), because only three indexes are stored.
     * Invariant: if target occurs in nums, its index lies in [lo, hi].
     */
    static int search(int[] nums, int target) {
        // The closed interval starts as the whole array.
        int lo = 0, hi = nums.length - 1;
        // At least one candidate remains while lo <= hi.
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            // Equality ends the search.
            if (nums[mid] == target) return mid;
            // A smaller middle value means the larger values, and the target, lie on the left.
            if (nums[mid] < target) hi = mid - 1;
            // A larger middle value means the target lies on the right.
            else lo = mid + 1;
        }
        // Empty interval: the target is absent.
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (search(new int[] {12, 9, 5, 3, 0, -1}, 5) != 2) throw new AssertionError("found");
        if (search(new int[] {12, 9, 5}, 6) != -1) throw new AssertionError("absent");
        // Using the ascending rule on a descending array loses the target, which is why the rule flips.
        int[] d = {12, 9, 5, 3, 0, -1};
        if (Arrays.binarySearch(d, 0) >= 0) throw new AssertionError("ascending rule should miss here");
        // Random descending arrays against a linear scan.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(12), -20, 20).distinct().sorted().toArray();
            for (int i = 0, j = a.length - 1; i < j; i++, j--) { int x = a[i]; a[i] = a[j]; a[j] = x; }
            int target = rnd.nextInt(50) - 25;
            int expect = -1;
            for (int i = 0; i < a.length; i++) if (a[i] == target) expect = i;
            if (search(a, target) != expect) throw new AssertionError("random " + Arrays.toString(a) + " " + target);
        }
    }
}
```

#### Solution: [Boundary] Two Elements (Author exercise)
<!-- id: bs-two-elements -->

**Approach.**
The method runs the search loop and appends each `mid` to a list before it compares. With `[1,3]`, the first midpoint is 0 because `0 + (1 - 0) / 2` rounds down. If the target is larger than `nums[0]`, `lo` becomes 1 and the interval holds one index, so the next midpoint is 1. After that comparison the loop either returns or leaves `lo > hi`. The interval shrinks after every comparison because each branch moves a bound past `mid`. That is why the probe count is at most `floor(log2(n)) + 1`.

**Complexity.**
- **Time** is O(log n), because the loop makes at most one probe per halving.
- **Space** is O(log n), because the answer list holds one entry per probe.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class TwoElementProbes {
    /**
     * Returns the midpoint indexes that the search compares, in order.
     * Time: O(log n), because each probe halves the interval.
     * Space: O(log n), because the list holds one entry per probe.
     * Invariant: before each probe, the target lies in [lo, hi] if it is present.
     */
    static List<Integer> probes(int[] nums, int target) {
        // The list is the answer and the only extra memory.
        List<Integer> out = new ArrayList<>();
        int lo = 0, hi = nums.length - 1;
        // Each pass records one probe.
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            // Record the probe before the comparison decides the next interval.
            out.add(mid);
            // Equality stops the search; the other branches move a bound past mid.
            if (nums[mid] == target) break;
            if (nums[mid] < target) lo = mid + 1; else hi = mid - 1;
        }
        return out;
    }

    public static void main(String[] args) {
        int[] two = {1, 3};
        // The three targets from the statement, with the probe sequences from the trace.
        if (!probes(two, 1).equals(List.of(0))) throw new AssertionError("target 1");
        if (!probes(two, 3).equals(List.of(0, 1))) throw new AssertionError("target 3");
        if (!probes(two, 2).equals(List.of(0, 1))) throw new AssertionError("target 2");
        // The probe count never exceeds floor(log2(n)) + 1 on random sorted arrays.
        Random rnd = new Random(5);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(60), -50, 50).distinct().sorted().toArray();
            int bound = 32 - Integer.numberOfLeadingZeros(a.length);
            if (probes(a, rnd.nextInt(120) - 60).size() > bound) throw new AssertionError("too many probes");
        }
    }
}
```

#### Solution: [Recognize] Matrix As One Sorted Array (LeetCode 74)
<!-- id: bs-matrix-probe-budget -->

**Approach.**
Row-major order with each row starting above the last value of the previous row makes the `m * n` values one ascending sequence. Index `k` maps to row `k / n` and column `k % n`, so the search needs no copy. The loop is the search of this lesson on indexes `0` to `m * n - 1`, and a counter records each comparison. The invariant is the same: a present target lies inside `[lo, hi]`. The count stays within `floor(log2(m * n)) + 1`, because the search never depends on the shape.

**Complexity.**
- **Time** is O(log(m * n)), because the virtual array halves each step.
- **Space** is O(1), because the code stores only the bounds and the counter.

```java run
import java.util.Random;

public final class MatrixProbeBudget {
    /**
     * Returns {comparisons, found} for a search over the matrix read in row-major order.
     * Time: O(log(m * n)), because the virtual array halves each step.
     * Space: O(1), because only the bounds and counters are stored.
     * Invariant: a present target lies in virtual indexes [lo, hi].
     */
    static int[] search(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        // The virtual array has m * n entries and needs no copy.
        int lo = 0, hi = m * n - 1, count = 0;
        // The loop runs while a candidate virtual index remains.
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            // Each pass makes exactly one value comparison.
            count++;
            // Division gives the row and remainder gives the column.
            int v = matrix[mid / n][mid % n];
            if (v == target) return new int[] {count, 1};
            if (v < target) lo = mid + 1; else hi = mid - 1;
        }
        // The interval is empty, so the target is absent.
        return new int[] {count, 0};
    }

    public static void main(String[] args) {
        int[][] g = {{1, 3, 5}, {7, 9, 11}};
        // The statement examples.
        int[] a = search(g, 9), b = search(g, 4);
        if (a[0] != 2 || a[1] != 1) throw new AssertionError("example 1");
        if (b[0] != 3 || b[1] != 0) throw new AssertionError("example 2");
        // Random matrices: presence matches a scan and the count stays inside the budget.
        Random rnd = new Random(3);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] mat = new int[m][n];
            int v = rnd.nextInt(5);
            for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) { v += 1 + rnd.nextInt(3); mat[i][j] = v; }
            int target = rnd.nextInt(v + 5) - 2;
            boolean has = false;
            for (int[] row : mat) for (int x : row) if (x == target) has = true;
            int[] r = search(mat, target);
            if ((r[1] == 1) != has) throw new AssertionError("presence");
            if (r[0] > 32 - Integer.numberOfLeadingZeros(m * n)) throw new AssertionError("budget");
        }
    }
}
```
