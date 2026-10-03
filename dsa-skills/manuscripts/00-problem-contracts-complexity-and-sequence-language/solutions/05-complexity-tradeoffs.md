<!-- solutions-for: 05-complexity-tradeoffs -->
### Complexity Tradeoffs

#### Solution: [Build] Consecutive Loops (Author exercise)
<!-- id: pc-consecutive-loops -->

**Approach.** The second scan runs `n` times no matter how many times the first one ran, so the two counts are added, giving `n + n = 2n`. Dropping the constant factor of two leaves O(n). The factor still exists, since doubling the work means doubling the time, but it does not change how the cost scales when `n` grows. The counter below runs the two loops and asserts the count.

**Complexity.** O(n) time, O(1) extra space.

```java run
public final class ConsecutiveLoops {
    static long countTwoScans(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++) steps++;
        for (int i = 0; i < n; i++) steps++;
        return steps;
    }

    public static void main(String[] args) {
        if (countTwoScans(10) != 20) throw new AssertionError("n = 10");
        if (countTwoScans(1) != 2) throw new AssertionError("n = 1");
        if (countTwoScans(2000) != 2 * countTwoScans(1000)) throw new AssertionError("doubling n doubles the count");
    }
}
```

#### Solution: [Vary] Triangular Work (Author exercise)
<!-- id: pc-triangular-work -->

**Approach.** For `i = 0` the inner loop runs `n - 1` times, for `i = 1` it runs `n - 2` times, and so on down to 0. The total is `(n - 1) + (n - 2) + ... + 1`, which equals `n(n - 1) / 2`. That expression is about half of `n^2`, so the class is O(n^2). The half is a constant factor and is dropped from the bound while remaining visible in the count. The assertions check the formula over many sizes instead of two.

**Complexity.** O(n^2) time, O(1) extra space.

```java run
public final class TriangularWork {
    static long countTriangular(int n) {
        long steps = 0;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) steps++;
        return steps;
    }

    public static void main(String[] args) {
        if (countTriangular(5) != 10) throw new AssertionError("n = 5");
        if (countTriangular(1) != 0) throw new AssertionError("n = 1");
        for (int n = 0; n <= 60; n++) {
            if (countTriangular(n) != (long) n * (n - 1) / 2) throw new AssertionError("formula at n = " + n);
        }
        if (countTriangular(8) != 28) throw new AssertionError("doubling 4 to 8 is nearly four times the work");
    }
}
```

#### Solution: [Boundary] Two Dimensions (Author exercise)
<!-- id: pc-two-dimensions -->

**Approach.** A grid traversal visits every cell once, so the cost is `rows * cols`, with both variables kept in the bound. If both are called `n`, the bound reads O(n^2), which is right for a square grid and badly pessimistic for a long thin one. With `rows = 1000` and `cols = 2` the real count is 2,000, while the merged claim would suggest a million. Keeping two letters also lets you say how the cost responds to each dimension separately.

**Complexity.** O(rows * cols) time, O(1) extra space.

```java run
public final class TwoDimensions {
    static long countGrid(int rows, int cols) {
        long steps = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) steps++;
        return steps;
    }

    public static void main(String[] args) {
        if (countGrid(3, 4) != 12) throw new AssertionError("3 x 4");
        if (countGrid(1000, 2) != 2000) throw new AssertionError("1000 x 2");
        long merged = 1000L * 1000L;
        if (!(merged > 400 * countGrid(1000, 2))) throw new AssertionError("calling both dimensions n overstates the cost");
        if (countGrid(1, 500) != 500) throw new AssertionError("a single row is linear");
    }
}
```

#### Solution: [Recognize] Sort Then Scan (Author exercise)
<!-- id: pc-sort-then-scan -->

**Approach.** Sort a copy of the array, then scan once comparing each element with the previous one. Equal values must be adjacent after sorting, so any duplicate shows up as equal neighbors. The cost is O(n log n) for the sort plus O(n) for the scan, which is dominated by the sort. The tradeoffs are that the sorted copy needs O(n) extra space, or sorting in place would destroy the original order and any index information. All-pairs comparison needs O(1) extra space and O(n^2) time, so the choice buys speed with memory. The randomized check compares both methods on many small arrays.

**Complexity.** O(n log n) time and O(n) extra space for the sorted copy, versus O(n^2) time and O(1) space for all pairs.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortThenScan {
    static boolean hasDuplicateSorted(int[] nums) {
        int[] copy = nums.clone();
        Arrays.sort(copy);
        for (int i = 1; i < copy.length; i++) if (copy[i] == copy[i - 1]) return true;
        return false;
    }
    static boolean hasDuplicateAllPairs(int[] nums) {
        for (int i = 0; i < nums.length; i++)
            for (int j = i + 1; j < nums.length; j++) if (nums[i] == nums[j]) return true;
        return false;
    }

    public static void main(String[] args) {
        int[] a = {4, 1, 3, 1};
        int[] snapshot = a.clone();
        if (!hasDuplicateSorted(a)) throw new AssertionError("duplicate present");
        if (!Arrays.equals(a, snapshot)) throw new AssertionError("the copy keeps the original order intact");
        if (hasDuplicateSorted(new int[] {4, 1, 3, 2})) throw new AssertionError("all distinct");
        Random rnd = new Random(7);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(8)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(10);
            if (hasDuplicateSorted(x) != hasDuplicateAllPairs(x)) throw new AssertionError("methods disagree on " + Arrays.toString(x));
        }
    }
}
```
