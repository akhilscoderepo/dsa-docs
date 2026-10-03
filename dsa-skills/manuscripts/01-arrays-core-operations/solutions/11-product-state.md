<!-- solutions-for: 11-product-state -->
### Product State

#### Solution: [Build] Maximum Product Subarray (LeetCode 152)
<!-- id: ar-maximum-product-subarray -->

**Approach.** Keep the largest and smallest product of a stretch ending at the current element. When the new element is negative, swap the two before multiplying, so each product uses the extreme the sign needs. Then the new high is the larger of the element alone and the high times the element, and the new low is the smaller of the element alone and the low times the element. A zero collapses both to zero and the next element restarts. The assertions compare with the quadratic enumeration on random arrays with zeros and negatives.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MaximumProductSubarray {
    static int maxProduct(int[] nums) {
        int hi = nums[0], lo = nums[0], best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            if (x < 0) { int t = hi; hi = lo; lo = t; }
            hi = Math.max(x, hi * x);
            lo = Math.min(x, lo * x);
            best = Math.max(best, hi);
        }
        return best;
    }
    static long oracle(int[] nums) {
        long best = Long.MIN_VALUE;
        for (int s = 0; s < nums.length; s++) {
            long p = 1;
            for (int e = s; e < nums.length; e++) { p *= nums[e]; best = Math.max(best, p); }
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxProduct(new int[] {2, -1, 3, -2, 2}) != 24) throw new AssertionError("example 1");
        if (maxProduct(new int[] {-4}) != -4) throw new AssertionError("example 2");
        Random rnd = new Random(71);
        for (int t = 0; t < 6000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (maxProduct(a) != oracle(a)) throw new AssertionError("disagrees with enumeration");
        }
    }
}
```

#### Solution: [Vary] Product Ending Here (Author exercise)
<!-- id: ar-product-ending-here -->

**Approach.** Run the same pair of ending states and return the high at the end, since the high is by definition the largest product of a stretch that ends at, and so includes, the final element. The overall best is not needed. The oracle multiplies every stretch that ends at the last index and takes the maximum.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class ProductEndingHere {
    static int endingHere(int[] nums) {
        int hi = nums[0], lo = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            if (x < 0) { int t = hi; hi = lo; lo = t; }
            hi = Math.max(x, hi * x);
            lo = Math.min(x, lo * x);
        }
        return hi;
    }
    static long oracle(int[] nums) {
        long best = Long.MIN_VALUE;
        long p = 1;
        for (int s = nums.length - 1; s >= 0; s--) { p *= nums[s]; best = Math.max(best, p); }
        return best;
    }

    public static void main(String[] args) {
        if (endingHere(new int[] {2, -3, 4, -1}) != 24) throw new AssertionError("example 1");
        if (endingHere(new int[] {3, 0, -2}) != 0) throw new AssertionError("example 2");
        Random rnd = new Random(72);
        for (int t = 0; t < 6000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (endingHere(a) != oracle(a)) throw new AssertionError("disagrees with the suffix oracle");
        }
    }
}
```

#### Solution: [Boundary] Zeros And Negatives In Maximum Product (LeetCode 152)
<!-- id: ar-product-zeros-negatives -->

**Approach.** On `[-2, 3, -4]` the first element sets high and low to -2. The 3 gives a high of 3 and a low of -6. The -4 swaps them, so the high is -6 times -4, which is 24, and the low is 3 times -4, which is -12, so the best is 24. On `[0, -2]` the first element sets both to 0. The -2 swaps zeros, the high is 0 because 0 beats -2, and the low is -2, so the best stays 0. A zero needs no branch, because after it the "alone" choice wins for any positive follower and the products stay at zero otherwise. The assertions record the state after every element and compare the recorded sequences.

**Complexity.** O(n) time and O(n) space for the recorded states, or O(1) without recording.

```java run
import java.util.Arrays;

public final class ProductZerosNegatives {
    static int[][] states(int[] nums) {                    // rows of {hi, lo, best}
        int[][] out = new int[nums.length][];
        int hi = nums[0], lo = nums[0], best = nums[0];
        out[0] = new int[] {hi, lo, best};
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            if (x < 0) { int t = hi; hi = lo; lo = t; }
            hi = Math.max(x, hi * x);
            lo = Math.min(x, lo * x);
            best = Math.max(best, hi);
            out[i] = new int[] {hi, lo, best};
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = states(new int[] {-2, 3, -4});
        if (!Arrays.deepEquals(a, new int[][] {{-2, -2, -2}, {3, -6, 3}, {24, -12, 24}})) throw new AssertionError("example 1: " + Arrays.deepToString(a));
        int[][] b = states(new int[] {0, -2});
        if (!Arrays.deepEquals(b, new int[][] {{0, 0, 0}, {0, -2, 0}})) throw new AssertionError("example 2: " + Arrays.deepToString(b));
        int[][] c = states(new int[] {3, 0, 5});
        if (c[1][0] != 0 || c[1][1] != 0) throw new AssertionError("a zero collapses both states");
        if (c[2][0] != 5) throw new AssertionError("the element after a zero restarts the stretch");
    }
}
```

#### Solution: [Recognize] Maximum Length of Subarray With Positive Product (LeetCode 1567)
<!-- id: ar-positive-product-length -->

**Approach.** Keep the longest stretch ending at the current element with a positive product and the longest with a negative product, both as lengths. A positive element extends the positive length and extends the negative length only if one exists. A negative element swaps the roles: the new positive length is the old negative length plus one if that exists, and the new negative length is the old positive length plus one. A zero resets both. No product is computed, so nothing can overflow. The oracle checks every stretch by counting negatives and testing for zeros.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class PositiveProductLength {
    static int longestPositiveProduct(int[] nums) {
        int pos = 0, neg = 0, best = 0;
        for (int x : nums) {
            if (x == 0) { pos = 0; neg = 0; }
            else if (x > 0) { pos = pos + 1; neg = neg > 0 ? neg + 1 : 0; }
            else { int newPos = neg > 0 ? neg + 1 : 0; neg = pos + 1; pos = newPos; }
            best = Math.max(best, pos);
        }
        return best;
    }
    static int oracle(int[] nums) {
        int best = 0;
        for (int s = 0; s < nums.length; s++) {
            int negatives = 0;
            for (int e = s; e < nums.length; e++) {
                if (nums[e] == 0) break;
                if (nums[e] < 0) negatives++;
                if (negatives % 2 == 0) best = Math.max(best, e - s + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestPositiveProduct(new int[] {-1, 2, -3, 4, -5}) != 4) throw new AssertionError("example 1");
        if (longestPositiveProduct(new int[] {-2, 0, 3}) != 1) throw new AssertionError("example 2");
        if (longestPositiveProduct(new int[] {0}) != 0) throw new AssertionError("only zero");
        Random rnd = new Random(73);
        for (int t = 0; t < 6000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5) - 2;
            if (longestPositiveProduct(a) != oracle(a)) throw new AssertionError("disagrees with the sign-count oracle");
        }
    }
}
```
