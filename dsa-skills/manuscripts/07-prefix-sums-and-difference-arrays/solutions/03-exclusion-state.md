<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Totals From Both Sides

#### Solution: [Build] Sum Except Self (Author exercise)
<!-- id: ps-sum-except-self -->

**Approach.**
Addition has an inverse, so the sum of all other values equals the total minus the value at the index. One pass computes the total as a `long`, and a second pass writes `total - nums[i]` for each index. A single value leaves the sum of no values, which is 0. An `int` total would wrap for values near 10^9, so the type of the total is the point of the exercise.

**Complexity.**
- **Time** is O(n), because two passes cost n operations each.
- **Space** is O(n) for the result array, and O(1) beyond it.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SumExceptSelf {
    /**
     * Returns out[i] = sum of all values except nums[i].
     * Time: O(n), two passes.
     * Space: O(n) for the result, O(1) extra.
     * Invariant: after the first pass, total is the sum of all values.
     */
    static long[] sumsExceptSelf(int[] nums) {
        // The total is a long, because the sum can pass the int range.
        long total = 0;
        for (int v : nums) total += v;
        long[] out = new long[nums.length];
        // Subtraction removes the one excluded value from the total.
        for (int i = 0; i < nums.length; i++) out[i] = total - nums[i];
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(sumsExceptSelf(new int[] {1, 2, 3, 4}), new long[] {9, 8, 7, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(sumsExceptSelf(new int[] {5}), new long[] {0})) throw new AssertionError("example 2");
        // Random arrays against a loop over the other values.
        Random rnd = new Random(9);
        for (int t = 0; t < 2000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(8), -1_000_000_000, 1_000_000_000).toArray();
            long[] got = sumsExceptSelf(a);
            for (int i = 0; i < a.length; i++) {
                long s = 0;
                for (int j = 0; j < a.length; j++) if (j != i) s += a[j];
                if (got[i] != s) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Vary] Product Of Array Except Self (LeetCode 238)
<!-- id: ps-product-except-self -->

**Approach.**
The product has no safe inverse, so the method multiplies the two sides separately. A left pass stores in `out[i]` the product of the values before `i`, using a running variable that starts at 1. A right pass then multiplies each `out[i]` by `suffix`, the product of the values after `i`, and updates `suffix` after the use. Each index excludes its own value, because both passes read the running variable before they multiply by `nums[i]`.

**Complexity.**
- **Time** is O(n), because each pass costs n multiplications.
- **Space** is O(1) beyond the output array, because only `running` and `suffix` are stored.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ProductExceptSelf238 {
    /**
     * Returns out[i] = product of all values except nums[i], without division.
     * Time: O(n), two passes.
     * Space: O(1) beyond the output.
     * Invariant: before step i of pass one, running is the product of nums[0..i-1].
     */
    static int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] out = new int[n];
        // The left pass stores each left product before it updates running.
        int running = 1;
        for (int i = 0; i < n; i++) {
            out[i] = running;
            running *= nums[i];
        }
        // The right pass multiplies in the product of the values after i.
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            out[i] *= suffix;
            suffix *= nums[i];
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(productExceptSelf(new int[] {1, 2, 3, 4}), new int[] {24, 12, 8, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(productExceptSelf(new int[] {-1, 1, 0, -3, 3}), new int[] {0, 0, 9, 0, 0})) throw new AssertionError("example 2");
        // Integer division by zero throws, which is why the total shortcut is unsafe.
        try {
            int z = 0;
            int ignored = 6 / z;
            throw new AssertionError("division by zero should throw " + ignored);
        } catch (ArithmeticException expected) {
            // The exception is the behaviour that the lesson claims.
        }
        // Random arrays of small values against a double loop.
        Random rnd = new Random(10);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(2 + rnd.nextInt(6), -4, 5).toArray();
            int[] got = productExceptSelf(a);
            for (int i = 0; i < a.length; i++) {
                int p = 1;
                for (int j = 0; j < a.length; j++) if (j != i) p *= a[j];
                if (got[i] != p) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Boundary] Zeros In The Product (LeetCode 238)
<!-- id: ps-product-zeros -->

**Approach.**
The two passes need no case for zeros. With one zero at index `z`, the left product of every index after `z` and the right product of every index before `z` contain the zero, so those answers are 0. The index `z` multiplies a left part and a right part that both avoid the zero, so it keeps the product of all other values. With two or more zeros, every answer has one of them on a side, so every entry is 0. The result uses `long`, because values up to 100 in magnitude overflow `int` after five factors.

**Complexity.**
- **Time** is O(n), because each pass costs n multiplications.
- **Space** is O(1) beyond the output array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ZerosInProduct {
    /**
     * Returns out[i] = product of all values except nums[i], as longs.
     * Time: O(n), two passes.
     * Space: O(1) beyond the output.
     * Invariant: before step i of pass two, out[i] holds the left product and suffix the right product.
     */
    static long[] productExceptSelf(int[] nums) {
        int n = nums.length;
        long[] out = new long[n];
        long running = 1;
        // The left pass stores the product of the values before each index.
        for (int i = 0; i < n; i++) {
            out[i] = running;
            running *= nums[i];
        }
        long suffix = 1;
        // The right pass completes each entry with the product after it.
        for (int i = n - 1; i >= 0; i--) {
            out[i] *= suffix;
            suffix *= nums[i];
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(productExceptSelf(new int[] {0, 4, 5}), new long[] {20, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(productExceptSelf(new int[] {0, 0, 3}), new long[] {0, 0, 0})) throw new AssertionError("example 2");
        // The smallest length with a zero.
        if (!Arrays.equals(productExceptSelf(new int[] {2, 0}), new long[] {0, 2})) throw new AssertionError("pair");
        // The int range is too small for the largest allowed input.
        int wrapped = 1;
        for (int i = 0; i < 6; i++) wrapped *= 100;
        if (wrapped == 1_000_000_000_000L) throw new AssertionError("int product should wrap");
        // Random arrays with many zeros against a double loop.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int[] a = rnd.ints(2 + rnd.nextInt(8), -3, 4).toArray();
            long[] got = productExceptSelf(a);
            for (int i = 0; i < a.length; i++) {
                long p = 1;
                for (int j = 0; j < a.length; j++) if (j != i) p *= a[j];
                if (got[i] != p) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Recognize] Prefix And Suffix Maximums (Author exercise)
<!-- id: ps-side-maximums -->

**Approach.**
A maximum has no inverse, so the total shortcut is unavailable and each side needs its own pass. The left pass keeps `best`, the maximum of the values before `i`, and writes it before it folds in `nums[i]`. The right pass does the same from the end. Both passes start with `best = -1`. This value is below every allowed number, so it acts as the neutral element of a maximum and also marks an empty side.

**Complexity.**
- **Time** is O(n), because each pass makes n comparisons.
- **Space** is O(n) for the two returned arrays.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SideMaximums {
    /**
     * Returns {left, right} where left[i] is the maximum of nums[0..i-1] and right[i] of nums[i+1..n-1].
     * Time: O(n), two passes.
     * Space: O(n) for the two result arrays.
     * Invariant: before step i of a pass, best is the maximum of the values already passed, or -1.
     */
    static int[][] sideMaximums(int[] nums) {
        int n = nums.length;
        int[] left = new int[n], right = new int[n];
        // The value -1 is below every allowed input and marks an empty side.
        int best = -1;
        for (int i = 0; i < n; i++) {
            // Store the maximum of the values before i, then include nums[i].
            left[i] = best;
            best = Math.max(best, nums[i]);
        }
        best = -1;
        for (int i = n - 1; i >= 0; i--) {
            // Store the maximum of the values after i, then include nums[i].
            right[i] = best;
            best = Math.max(best, nums[i]);
        }
        return new int[][] {left, right};
    }

    public static void main(String[] args) {
        // The statement examples.
        int[][] a = sideMaximums(new int[] {3, 1, 4});
        if (!Arrays.equals(a[0], new int[] {-1, 3, 3}) || !Arrays.equals(a[1], new int[] {4, 4, -1})) throw new AssertionError("example 1");
        int[][] b = sideMaximums(new int[] {7});
        if (!Arrays.equals(b[0], new int[] {-1}) || !Arrays.equals(b[1], new int[] {-1})) throw new AssertionError("example 2");
        // Random arrays against a loop over each side.
        Random rnd = new Random(12);
        for (int t = 0; t < 3000; t++) {
            int[] nums = rnd.ints(1 + rnd.nextInt(9), 0, 20).toArray();
            int[][] got = sideMaximums(nums);
            for (int i = 0; i < nums.length; i++) {
                int l = -1, r = -1;
                for (int j = 0; j < i; j++) l = Math.max(l, nums[j]);
                for (int j = i + 1; j < nums.length; j++) r = Math.max(r, nums[j]);
                if (got[0][i] != l || got[1][i] != r) throw new AssertionError("random");
            }
        }
    }
}
```
