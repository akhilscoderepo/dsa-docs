<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Product State

#### Solution: [Build] Maximum Product Subarray (LeetCode 152)
<!-- id: ar-max-product -->

**Approach.** A product does not keep the order of values when a negative factor arrives, so one ending value loses information. The scan keeps the largest and the smallest product of a subarray that ends at the current index. At each index it forms three candidates: the value alone, the largest product times the value, and the smallest product times the value. The largest candidate becomes the new largest product and the smallest becomes the new smallest. A negative value therefore turns the old smallest product into the new largest, and a zero resets both. The invariant is that the pair brackets every ending product, and the running maximum of the largest products is the answer.

**Complexity.**

- **Time** is O(n), because each index builds three candidates in constant time.
- **Space** is O(1), because the scan stores three integers and two temporaries.

```java run
import java.util.Random;

public final class MaxProduct {
    /**
     * Returns the largest product of a non-empty contiguous subarray.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only three running values are stored.
     * Invariant: maxEndingHere and minEndingHere are the extreme products of subarrays ending at i.
     */
    static int maxProduct(int[] nums) {
        // All three values start at the first element, so the subarray is non-empty.
        int maxEndingHere = nums[0];
        int minEndingHere = nums[0];
        int bestOverall = nums[0];
        // One pass from index 1; every iteration costs O(1).
        for (int i = 1; i < nums.length; i++) {
            // The current value feeds all three candidates.
            int x = nums[i];
            // Copy the old products first, so the update of one value cannot corrupt the other.
            int fromMax = maxEndingHere * x;
            int fromMin = minEndingHere * x;
            // The new largest is the best of restarting and both extensions.
            maxEndingHere = Math.max(x, Math.max(fromMax, fromMin));
            // The new smallest is the worst of restarting and both extensions.
            minEndingHere = Math.min(x, Math.min(fromMax, fromMin));
            // Fold the new largest ending product into the global best.
            bestOverall = Math.max(bestOverall, maxEndingHere);
        }
        // The global best covers every ending index.
        return bestOverall;
    }

    /** Oracle: multiplies every subarray with a running long product, in O(n^2) time. */
    static long brute(int[] nums) {
        // Start below every product so negative arrays work.
        long best = Long.MIN_VALUE;
        // Each start begins a product of 1.
        for (int s = 0; s < nums.length; s++) {
            long p = 1;
            // Each end multiplies one more value in.
            for (int e = s; e < nums.length; e++) {
                p *= nums[e];
                best = Math.max(best, p);
            }
        }
        // The largest product over all pairs.
        return best;
    }

    public static void main(String[] args) {
        // Checks the lesson arrays and both examples.
        if (maxProduct(new int[]{2, 3, -2, 4}) != 6) throw new AssertionError("lesson array 1");
        if (maxProduct(new int[]{-2, 3, -4}) != 24) throw new AssertionError("lesson array 2");
        if (maxProduct(new int[]{3, -1, 4, -2, -5}) != 40) throw new AssertionError("example 1");
        if (maxProduct(new int[]{-4, 0, -1}) != 0) throw new AssertionError("example 2");
        // Checks that the one-value shortcut from the lesson returns 3 on [-2, 3, -4].
        int e = -2, best = -2;
        for (int x : new int[]{3, -4}) { e = Math.max(x, e * x); best = Math.max(best, e); }
        if (best != 3) throw new AssertionError("shortcut gives 3, which is wrong");
        // Checks 8,000 random arrays with zeros and negatives against the oracle.
        Random rnd = new Random(20);
        for (int t = 0; t < 8000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (maxProduct(a) != brute(a)) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Product Ending Here (Author exercise)
<!-- id: ar-product-ending-here -->

**Approach.** The question asks only for subarrays that end at the last index, so the global best is not needed. The pair of ending products is still required, because the last value may be negative and then needs the smallest product before it. The scan updates both values at every index with the same three candidates and returns the largest ending product after the last index. The invariant is the same as in the maximum product problem, so the earlier global maximum plays no role.

**Complexity.**

- **Time** is O(n), because the scan reads each value once.
- **Space** is O(1), because two running products are the only state.

```java run
import java.util.Random;

public final class ProductEndingHere {
    /**
     * Returns the largest product of a non-empty subarray that ends at the last index.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only two ending products are stored.
     * Invariant: maxEnd and minEnd are the extreme products of subarrays ending at i.
     */
    static int productEndingHere(int[] nums) {
        // Both ending products start at the first element.
        int maxEnd = nums[0];
        int minEnd = nums[0];
        // One pass from index 1; every iteration costs O(1).
        for (int i = 1; i < nums.length; i++) {
            // Read the value and keep the old products before either changes.
            int x = nums[i];
            int fromMax = maxEnd * x;
            int fromMin = minEnd * x;
            // Update the largest and the smallest ending products from the same candidates.
            maxEnd = Math.max(x, Math.max(fromMax, fromMin));
            minEnd = Math.min(x, Math.min(fromMax, fromMin));
        }
        // The largest ending product at the last index is the answer.
        return maxEnd;
    }

    /** Oracle: multiplies every suffix with a long product, in O(n) time per array. */
    static long brute(int[] nums) {
        // Start below every product.
        long best = Long.MIN_VALUE;
        // Each start index defines the suffix that ends at the last index.
        for (int s = 0; s < nums.length; s++) {
            long p = 1;
            // Multiply the suffix values together.
            for (int e = s; e < nums.length; e++) p *= nums[e];
            best = Math.max(best, p);
        }
        // The largest suffix product.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (productEndingHere(new int[]{1, -2, -3, 4}) != 24) throw new AssertionError("example 1");
        if (productEndingHere(new int[]{-3, 0, -5}) != 0) throw new AssertionError("example 2");
        // Checks that a single element returns itself.
        if (productEndingHere(new int[]{-6}) != -6) throw new AssertionError("single element");
        // Checks 8,000 random arrays against the suffix oracle.
        Random rnd = new Random(21);
        for (int t = 0; t < 8000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (productEndingHere(a) != brute(a)) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Zero And Negative Trace (Author exercise)
<!-- id: ar-product-zero-negative-trace -->

**Approach.** The method records the pair of ending products after each index. For `[-2, 3, -4]` the first pair is `[-2, -2]`. The value 3 gives candidates 3, -6 and -6, so the pair is `[3, -6]`. The value -4 gives candidates -4, -12 and 24, so the pair is `[24, -12]`, and the smallest ending product -6 became the largest. For `[0, -2]` the first pair is `[0, 0]`. The value -2 gives candidates -2, 0 and 0, so the pair is `[0, -2]`, and the zero kept the best at 0. The largest first entry is the maximum product.

**Complexity.**

- **Time** is O(n), because each row costs a constant number of operations.
- **Space** is O(n), because the table has one row per index.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ZeroNegativeTrace {
    /**
     * Returns the table of {maxEndingHere, minEndingHere} pairs, one row per index.
     * Time: O(n), because each row takes constant work.
     * Space: O(n), because the table stores n rows.
     * Invariant: row i holds the extreme products of subarrays ending at index i.
     */
    static int[][] pairs(int[] nums) {
        // One row per index of the input.
        int[][] table = new int[nums.length][2];
        // The first row has only one subarray, so both entries equal the first value.
        table[0][0] = nums[0];
        table[0][1] = nums[0];
        // Fill later rows from the previous row; each iteration costs O(1).
        for (int i = 1; i < nums.length; i++) {
            // Candidates come from the value alone and from both old extremes.
            int x = nums[i];
            int fromMax = table[i - 1][0] * x;
            int fromMin = table[i - 1][1] * x;
            // The row stores the largest and the smallest candidate.
            table[i][0] = Math.max(x, Math.max(fromMax, fromMin));
            table[i][1] = Math.min(x, Math.min(fromMax, fromMin));
        }
        // The caller reads the maximum product from the first column.
        return table;
    }

    /** Computes the extreme ending products by multiplying every subarray that ends at index i. */
    static int[][] oracle(int[] nums) {
        // One row per index.
        int[][] table = new int[nums.length][2];
        // For each end index, try every start index.
        for (int e = 0; e < nums.length; e++) {
            long hi = Long.MIN_VALUE, lo = Long.MAX_VALUE, p = 1;
            // Walk the start index from e down to 0 and extend the product to the left.
            for (int s = e; s >= 0; s--) {
                p *= nums[s];
                hi = Math.max(hi, p);
                lo = Math.min(lo, p);
            }
            table[e][0] = (int) hi;
            table[e][1] = (int) lo;
        }
        // The brute table for comparison.
        return table;
    }

    public static void main(String[] args) {
        // Checks both examples row by row.
        if (!Arrays.deepEquals(pairs(new int[]{-2, 3, -4}), new int[][]{{-2, -2}, {3, -6}, {24, -12}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(pairs(new int[]{0, -2}), new int[][]{{0, 0}, {0, -2}})) throw new AssertionError("example 2");
        // Checks that the largest first entry matches the stated maximum products.
        int[][] t = pairs(new int[]{-2, 3, -4});
        if (Math.max(Math.max(t[0][0], t[1][0]), t[2][0]) != 24) throw new AssertionError("maximum is 24");
        // Checks 6,000 random arrays against the per-end oracle.
        Random rnd = new Random(22);
        for (int r = 0; r < 6000; r++) {
            int[] a = new int[1 + rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (!Arrays.deepEquals(pairs(a), oracle(a))) throw new AssertionError("random " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Longest Positive Product Run (LeetCode 1567)
<!-- id: ar-positive-product-length -->

**Approach.** The product itself is never needed, only its sign. The scan keeps the length of the longest subarray ending at the current index with a positive product, and the length of the longest one with a negative product. A positive value extends both lengths, and the negative length only exists once it is above zero. A negative value swaps the two histories: the old negative length plus one becomes the new positive length, and the old positive length plus one becomes the new negative length. A zero resets both lengths to 0. The answer is the largest positive length over all indices.

**Complexity.**

- **Time** is O(n), because each index updates two lengths in constant time.
- **Space** is O(1), because two lengths and one answer are the only state.

```java run
import java.util.Random;

public final class PositiveProductLength {
    /**
     * Returns the length of the longest subarray with a positive product, or 0 if none exists.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only three integers are stored.
     * Invariant: pos and neg are the longest lengths of subarrays ending at i with a positive or negative product.
     */
    static int longestPositive(int[] nums) {
        // Lengths of the longest positive-product and negative-product runs ending at the previous index.
        int pos = 0, neg = 0, best = 0;
        // One pass; every iteration costs O(1).
        for (int x : nums) {
            if (x > 0) {
                // A positive value keeps signs: positive extends positive, and negative extends only if it exists.
                pos = pos + 1;
                neg = neg > 0 ? neg + 1 : 0;
            } else if (x < 0) {
                // A negative value swaps the histories; the negative run exists after one more value.
                int newPos = neg > 0 ? neg + 1 : 0;
                int newNeg = pos + 1;
                pos = newPos;
                neg = newNeg;
            } else {
                // A zero makes every product zero, so both runs reset.
                pos = 0;
                neg = 0;
            }
            // Keep the longest positive run seen so far.
            best = Math.max(best, pos);
        }
        // The longest positive-product run over all ending indices.
        return best;
    }

    /** Oracle: tracks the sign of the product of each subarray in O(n^2) time. */
    static int brute(int[] nums) {
        // Longest length found so far.
        int best = 0;
        // Each start begins a run with positive sign.
        for (int s = 0; s < nums.length; s++) {
            int sign = 1;
            // Each end multiplies the sign by the sign of the next value.
            for (int e = s; e < nums.length; e++) {
                // A zero stops the run for this start, because every longer product is zero.
                if (nums[e] == 0) break;
                if (nums[e] < 0) sign = -sign;
                if (sign > 0) best = Math.max(best, e - s + 1);
            }
        }
        // The longest positive run.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (longestPositive(new int[]{-1, -2, -3, 0, 2}) != 2) throw new AssertionError("example 1");
        if (longestPositive(new int[]{2, -2, -3, 0, 5}) != 3) throw new AssertionError("example 2");
        // Checks the case with no positive run.
        if (longestPositive(new int[]{0, -4, 0}) != 0) throw new AssertionError("no positive run");
        // Checks 8,000 random arrays with zeros against the oracle.
        Random rnd = new Random(23);
        for (int t = 0; t < 8000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5) - 2;
            if (longestPositive(a) != brute(a)) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```
