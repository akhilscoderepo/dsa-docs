<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Running Totals

#### Solution: [Build] Running Sum Of 1d Array (LeetCode 1480)
<!-- id: ps-running-sum -->

**Approach.**
The output at index `i` equals the output at index `i - 1` plus `nums[i]`, so one pass with a `long` accumulator produces every entry. The accumulator never drops below the sum of the visited values, which is the invariant. The accumulator needs type `long`, because three values of 10^9 already pass the `int` maximum.

**Complexity.**
- **Time** is O(n), because the loop performs one addition per value.
- **Space** is O(n) for the returned array, and O(1) beyond it.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RunningSum1480 {
    /**
     * Returns out[i] = nums[0] + ... + nums[i] as longs.
     * Time: O(n), one addition per value.
     * Space: O(n) for the result, O(1) extra.
     * Invariant: before step i, sum equals nums[0] + ... + nums[i - 1].
     */
    static long[] runningSum(int[] nums) {
        // The result has one slot per input value.
        long[] out = new long[nums.length];
        // The accumulator is a long so that sums above 2^31 - 1 stay exact.
        long sum = 0;
        // One pass, so the cost is n additions.
        for (int i = 0; i < nums.length; i++) {
            // Extend the previous total by one value.
            sum += nums[i];
            // Store the total through index i.
            out[i] = sum;
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(runningSum(new int[] {1, 2, 3, 4}), new long[] {1, 3, 6, 10})) throw new AssertionError("example 1");
        long[] big = runningSum(new int[] {1_000_000_000, 1_000_000_000, 1_000_000_000});
        if (big[2] != 3_000_000_000L) throw new AssertionError("example 2");
        // An int accumulator wraps for the same input, which is why the type is long.
        int wrapped = 0;
        for (int i = 0; i < 3; i++) wrapped += 1_000_000_000;
        if (wrapped >= 0) throw new AssertionError("int sum should wrap");
        // The empty array gives the empty result.
        if (runningSum(new int[0]).length != 0) throw new AssertionError("empty");
        // Random arrays against a recomputation from the first value.
        Random rnd = new Random(1);
        for (int t = 0; t < 2000; t++) {
            int[] a = rnd.ints(rnd.nextInt(10), -1_000_000_000, 1_000_000_000).toArray();
            long[] got = runningSum(a);
            for (int i = 0; i < a.length; i++) {
                long expect = 0;
                for (int j = 0; j <= i; j++) expect += a[j];
                if (got[i] != expect) throw new AssertionError("random " + Arrays.toString(a));
            }
        }
    }
}
```

#### Solution: [Vary] Find Pivot Index (LeetCode 724)
<!-- id: ps-pivot-index -->

**Approach.**
The method builds the prefix array with the sentinel and takes the total from its last entry. For index `p`, the left side is `prefix[p]`, and the right side is `total - prefix[p + 1]`, which removes both the left side and `nums[p]`. The loop returns the first `p` where the two sides match, so ties give the smallest index. The empty array has no index and returns `-1`.

**Complexity.**
- **Time** is O(n), because the loop builds the array in one pass and scans it in another.
- **Space** is O(n) for the prefix array.

```java run
import java.util.Random;

public final class PivotIndex724 {
    /**
     * Returns the smallest p with sum(left of p) == sum(right of p), or -1.
     * Time: O(n), two passes.
     * Space: O(n), the prefix array.
     * Invariant: prefix[i] is the sum of nums[0..i-1].
     */
    static int pivot(int[] nums) {
        int n = nums.length;
        long[] prefix = new long[n + 1];
        // The recurrence fills the array with one addition per value.
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
        long total = prefix[n];
        // The scan tests every candidate in increasing order.
        for (int p = 0; p < n; p++) {
            // The right side removes the left side and nums[p] from the total.
            long right = total - prefix[p + 1];
            // The first equality is the smallest pivot.
            if (prefix[p] == right) return p;
        }
        // No index balanced the two sides.
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (pivot(new int[] {1, 7, 3, 6, 5, 6}) != 3) throw new AssertionError("example 1");
        if (pivot(new int[] {2, 1, -1}) != 0) throw new AssertionError("example 2");
        // The empty array has no pivot, and one value is its own pivot.
        if (pivot(new int[0]) != -1) throw new AssertionError("empty");
        if (pivot(new int[] {5}) != 0) throw new AssertionError("single");
        // Random arrays against a direct sum on each side.
        Random rnd = new Random(2);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(9), -4, 5).toArray();
            int expect = -1;
            for (int p = 0; p < a.length && expect < 0; p++) {
                long l = 0, r = 0;
                for (int j = 0; j < p; j++) l += a[j];
                for (int j = p + 1; j < a.length; j++) r += a[j];
                if (l == r) expect = p;
            }
            if (pivot(a) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Empty Prefix (Author exercise)
<!-- id: ps-empty-prefix -->

**Approach.**
The array has length `n + 1` and its first entry is the sentinel 0. Reading entry `c` then returns the sum of the first `c` values for every `c` from 0 to `n`. The case `c = 0` reads the sentinel and needs no branch. The empty input still allocates one slot, so `nums = []` with `c = 0` returns 0.

**Complexity.**
- **Time** is O(n), because the construction visits each value once and the read is one access.
- **Space** is O(n) for the array of length `n + 1`.

```java run
import java.util.Random;

public final class EmptyPrefix {
    /**
     * Returns the sum of the first c values of nums.
     * Time: O(n), one pass to build, one read.
     * Space: O(n), the prefix array.
     * Invariant: prefix[i] is the sum of the first i values, with prefix[0] = 0.
     */
    static long firstSum(int[] nums, int c) {
        // The extra slot holds the sentinel for zero values.
        long[] prefix = new long[nums.length + 1];
        // Each entry extends the previous one by one value.
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        // The read needs no special case for c = 0.
        return prefix[c];
    }

    public static void main(String[] args) {
        // The statement examples.
        if (firstSum(new int[] {4, -2, 7}, 0) != 0) throw new AssertionError("example 1");
        if (firstSum(new int[0], 0) != 0) throw new AssertionError("example 2");
        // The full count reads the last entry.
        if (firstSum(new int[] {4, -2, 7}, 3) != 9) throw new AssertionError("full");
        // Random arrays and counts against a direct loop.
        Random rnd = new Random(3);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(9), -1_000_000_000, 1_000_000_000).toArray();
            int c = rnd.nextInt(a.length + 1);
            long expect = 0;
            for (int i = 0; i < c; i++) expect += a[i];
            if (firstSum(a, c) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Prefix Averages (Author exercise)
<!-- id: ps-prefix-averages -->

**Approach.**
The average at index `i` divides the sum of `i + 1` values by `i + 1`. The running total supplies the numerator and the loop index supplies the denominator, so the same pass computes both. The division uses `long` operands, and Java truncates the quotient toward zero, which matches the specification for negative totals. A division of `int` values would overflow in the numerator first, so the total stays `long`.

**Complexity.**
- **Time** is O(n), because each position costs one addition and one division.
- **Space** is O(n) for the returned array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PrefixAverages {
    /**
     * Returns avg[i] = (nums[0] + ... + nums[i]) / (i + 1), truncated toward zero.
     * Time: O(n), one addition and one division per position.
     * Space: O(n) for the result.
     * Invariant: before step i, sum equals nums[0] + ... + nums[i - 1].
     */
    static long[] averages(int[] nums) {
        long[] avg = new long[nums.length];
        // The accumulator is a long because the total can pass the int range.
        long sum = 0;
        for (int i = 0; i < nums.length; i++) {
            // Extend the total by one value.
            sum += nums[i];
            // The divisor i + 1 equals the number of values in the total.
            avg[i] = sum / (i + 1);
        }
        return avg;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(averages(new int[] {4, 6, 5}), new long[] {4, 5, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(averages(new int[] {-3, 0, 0}), new long[] {-3, -1, -1})) throw new AssertionError("example 2");
        // Java division truncates toward zero, so -3 / 2 is -1 and not -2.
        if (-3L / 2 != -1) throw new AssertionError("truncation");
        // Random arrays against a recomputation of each total.
        Random rnd = new Random(4);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(rnd.nextInt(10), -1_000_000_000, 1_000_000_000).toArray();
            long[] got = averages(a);
            for (int i = 0; i < a.length; i++) {
                long s = 0;
                for (int j = 0; j <= i; j++) s += a[j];
                if (got[i] != s / (i + 1)) throw new AssertionError("random");
            }
        }
    }
}
```
