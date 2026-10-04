<!-- solutions-for: 05-complexity-tradeoffs -->
### Solutions For Complexity Trade-Offs

#### Solution: [Build] Consecutive Loops (Author exercise)
<!-- id: pc-consecutive-loops -->

**Approach.** The method adds two sequential loops.

The first loop executes its body `n` times. The second loop also executes its body `n` times, because its bound is `n` and not a value from the first loop. The total is `n + n = 2n`, because sequential loops add.

The constant factor of two drops from the bound, so the bound is O(n). Doubling `n` still doubles the running time, because the factor exists but does not change how cost grows. Multiplication applies only when one loop sits inside the other. The harness asserts the counts for `n = 10`, `n = 1` and a doubled `n`.

**Complexity.**

- **Time** is O(n), because the two loops execute `2n` bodies in total and the constant 2 drops.
- **Space** is O(1), because the code keeps one counter and one index and allocates nothing else.

```java run
public final class ConsecutiveLoops {
    /**
     * Counts loop-body executions of two sequential scans over n positions.
     * Time: O(n), because each loop runs n times and the two counts add.
     * Space: O(1), because only the counter and the loop index are stored.
     */
    static long countTwoScans(int n) {
        // The counter is a long so that large n cannot overflow it.
        long steps = 0;
        // First scan: runs n times, so it contributes n to the total (this is the O(n) cost).
        for (int i = 0; i < n; i++) steps++;
        // Second scan: starts after the first ends, so its n executions add instead of multiply.
        for (int i = 0; i < n; i++) steps++;
        // Return 2n; the caller drops the constant factor to classify the cost as O(n).
        return steps;
    }

    public static void main(String[] args) {
        // Checks the counts from Example 1 and Example 2.
        if (countTwoScans(10) != 20) throw new AssertionError("n = 10");
        if (countTwoScans(1) != 2) throw new AssertionError("n = 1");
        // Checks linear growth: doubling n doubles the count.
        if (countTwoScans(2000) != 2 * countTwoScans(1000)) throw new AssertionError("doubling n doubles the count");
    }
}
```

#### Solution: [Vary] Triangular Work (Author exercise)
<!-- id: pc-triangular-work -->

**Approach.** The method counts a loop whose inner bound depends on `i`.

The inner count is `n - 1` for `i = 0`, `n - 2` for `i = 1`, and 0 for `i = n - 1`. Therefore the sum `(n - 1) + (n - 2) + ... + 1` equals `n(n - 1) / 2`. The bound is O(n^2), because the formula is about half of `n^2` and the bound drops the constant factor. The exact count keeps the factor one half.

The inner bound depends on `i`, so the total is a sum and not the product `n * n`. The harness checks the formula for every `n` from 0 to 60 and not only for two sizes.

**Complexity.**

- **Time** is O(n^2), because the inner body executes `n(n - 1) / 2` times.
- **Space** is O(1), because the code keeps one counter and two indices.

```java run
public final class TriangularWork {
    /**
     * Counts executions of the inner body of a shrinking nested loop.
     * Time: O(n^2), because the inner body runs n(n-1)/2 times in total.
     * Space: O(1), because only the counter and two indices are stored.
     */
    static long countTriangular(int n) {
        // The counter is a long because the count reaches about 5 * 10^9 for n = 10^5.
        long steps = 0;
        // Outer loop: n iterations; each one starts an inner loop whose length depends on i.
        for (int i = 0; i < n; i++)
            // Inner loop starts at i + 1, so it runs n - 1 - i times and shrinks as i grows.
            for (int j = i + 1; j < n; j++) steps++;
        // Return the total, which the caller compares with n(n-1)/2.
        return steps;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2 (the inner loop never runs for n = 1).
        if (countTriangular(5) != 10) throw new AssertionError("n = 5");
        if (countTriangular(1) != 0) throw new AssertionError("n = 1");
        // Checks the closed formula for every size from 0 to 60, including the empty case.
        for (int n = 0; n <= 60; n++) {
            if (countTriangular(n) != (long) n * (n - 1) / 2) throw new AssertionError("formula at n = " + n);
        }
        // Checks quadratic growth: doubling n from 4 to 8 gives 28, nearly four times 6.
        if (countTriangular(8) != 28) throw new AssertionError("doubling 4 to 8 is nearly four times the work");
    }
}
```

#### Solution: [Boundary] Two Dimensions (Author exercise)
<!-- id: pc-two-dimensions -->

**Approach.** The traversal nests a column loop inside a row loop.

The row loop runs `rows` times, and each run starts a column loop of `cols` visits. Therefore the cost is `rows * cols`, because nested loops multiply, and the bound keeps both variables.

The merged claim O(n^2) calls both dimensions `n`. It is correct for a square grid and far too pessimistic for a long thin grid. For example, a thin grid with `rows = 1000` and `cols = 2` has 2,000 visits, while the merged claim suggests 1,000,000. Two letters show how the cost responds to each dimension separately.

**Complexity.**

- **Time** is O(rows * cols), because each of the `rows` outer passes runs `cols` visits.
- **Space** is O(1), because the code keeps one counter and two indices and does not store the grid.

```java run
public final class TwoDimensions {
    /**
     * Counts cell visits of a full row-by-column traversal.
     * Time: O(rows * cols), because each of the rows passes runs cols visits.
     * Space: O(1), because only the counter and two indices are stored.
     */
    static long countGrid(int rows, int cols) {
        // The counter is a long so that large grids cannot overflow it.
        long steps = 0;
        // Outer loop: one pass per row, so it runs rows times.
        for (int r = 0; r < rows; r++)
            // Inner loop: one visit per column in this row; nesting multiplies the cost to rows * cols.
            for (int c = 0; c < cols; c++) steps++;
        // Return the visit count, which equals rows * cols.
        return steps;
    }

    public static void main(String[] args) {
        // Checks Example 1 and the thin grid from Example 2.
        if (countGrid(3, 4) != 12) throw new AssertionError("3 x 4");
        if (countGrid(1000, 2) != 2000) throw new AssertionError("1000 x 2");
        // Checks that the merged n^2 claim (1,000,000) overstates the true count of 2,000 by over 400 times.
        long merged = 1000L * 1000L;
        if (!(merged > 400 * countGrid(1000, 2))) throw new AssertionError("calling both dimensions n overstates the cost");
        // Checks that a single-row grid is linear in cols.
        if (countGrid(1, 500) != 500) throw new AssertionError("a single row is linear");
    }
}
```

#### Solution: [Recognize] Sort Then Scan (Author exercise)
<!-- id: pc-sort-then-scan -->

**Approach.** The method sorts a copy and scans it once.

The method sorts a copy of the array, so `nums` stays unchanged. Then a scan of the copy compares each element with its predecessor. Sorted order places equal values next to each other, so a duplicate exists exactly when some pair of neighbors is equal. The return value is `true` at the first equal pair and `false` when the scan ends without one.

The sort costs O(n log n) and the scan costs O(n), so the sort dominates. The copy needs O(n) extra space, whereas sorting in place would destroy the original order and every index. The all-pairs method needs O(1) extra space but O(n^2) time, so the sorted approach buys speed with memory. The harness compares both methods on 2,000 random small arrays.

**Complexity.**

- **Time** is O(n log n), because sorting the copy costs O(n log n) and the scan adds O(n). The all-pairs method takes O(n^2).
- **Space** is O(n), because the copy holds `n` values. The all-pairs method takes O(1).

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortThenScan {
    /**
     * Detects a duplicate by sorting a copy and comparing neighbors.
     * Time: O(n log n), because the sort dominates the O(n) scan.
     * Space: O(n), because the copy holds every value.
     * Invariant: after sorting, equal values are adjacent.
     */
    static boolean hasDuplicateSorted(int[] nums) {
        // Clone first so the caller's array keeps its order; this is the O(n) extra space.
        int[] copy = nums.clone();
        // Sort the copy; this O(n log n) step brings equal values next to each other.
        Arrays.sort(copy);
        // Scan once from index 1; each step compares a value with its predecessor, so the scan is O(n).
        for (int i = 1; i < copy.length; i++) if (copy[i] == copy[i - 1]) return true;
        // No equal neighbors means no equal values anywhere, so all values are distinct.
        return false;
    }
    /**
     * Detects a duplicate by comparing every pair of positions.
     * Time: O(n^2), because there are n(n-1)/2 pairs in the worst case.
     * Space: O(1), because nothing is copied.
     */
    static boolean hasDuplicateAllPairs(int[] nums) {
        // Outer loop: picks the first position of each pair.
        for (int i = 0; i < nums.length; i++)
            // Inner loop: pairs i with each later position, which gives the quadratic cost.
            for (int j = i + 1; j < nums.length; j++) if (nums[i] == nums[j]) return true;
        // Every pair differs, so there is no duplicate.
        return false;
    }

    public static void main(String[] args) {
        // Checks Example 1: a duplicate is found and the original order stays intact.
        int[] a = {4, 1, 3, 1};
        int[] snapshot = a.clone();
        if (!hasDuplicateSorted(a)) throw new AssertionError("duplicate present");
        if (!Arrays.equals(a, snapshot)) throw new AssertionError("the copy keeps the original order intact");
        // Checks Example 2: all values are distinct.
        if (hasDuplicateSorted(new int[] {4, 1, 3, 2})) throw new AssertionError("all distinct");
        // Checks both methods against each other on 2,000 random arrays with values in 0..9.
        Random rnd = new Random(7);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(8)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(10);
            if (hasDuplicateSorted(x) != hasDuplicateAllPairs(x)) throw new AssertionError("methods disagree on " + Arrays.toString(x));
        }
    }
}
```
