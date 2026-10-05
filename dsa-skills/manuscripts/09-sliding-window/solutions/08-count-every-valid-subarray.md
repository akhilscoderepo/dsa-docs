<!-- solutions-for: 09-sliding-window -->
### Solutions For Counting Valid Subarrays

#### Solution: [Build] Count Subarrays With At Most One Zero (Author exercise)
<!-- id: sw-count-one-zero -->

**Approach.**
The method expands `right` and counts the zeros in the window. While two zeros are present, it moves `left` forward and subtracts one when `left` passes a zero. After that loop, every start from `left` to `right` gives a subarray with at most one zero, because removing values from the front cannot add a zero. The method adds `right - left + 1` for this end index. Each subarray has one end index, so no subarray is counted twice. The invariant is that, after the loop, the starts `left..right` are exactly the valid starts for `right`.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps a few integers and one `long`.

```java run
import java.util.Random;

public final class CountOneZero {
    /**
     * Counts subarrays with at most one zero.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), a few integers and one long.
     * Invariant: after the shrink loop, the valid starts for right are exactly left..right.
     */
    static long count(int[] bits) {
        int left = 0, zeros = 0;
        // long: the answer can reach n * (n + 1) / 2.
        long total = 0;
        // Expand: one value enters per iteration, so the loop runs n times.
        for (int right = 0; right < bits.length; right++) {
            // A zero entering raises the violation count.
            if (bits[right] == 0) zeros++;
            // Shrink: runs while two zeros are present; each pass removes the value at left.
            while (zeros > 1) {
                if (bits[left] == 0) zeros--;
                left++;
            }
            // Starts left..right are valid for this end index, and there are right - left + 1 of them.
            total += right - left + 1;
        }
        // Each subarray has exactly one end index, so the sum counts it once.
        return total;
    }

    /** Oracle: tests every pair of indexes. */
    static long oracle(int[] a) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            int z = 0;
            for (int j = i; j < a.length; j++) { if (a[j] == 0) z++; if (z <= 1) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (count(new int[] {1, 0, 1, 0, 1}) != 11) throw new AssertionError("example 1");
        if (count(new int[] {0, 0, 0}) != 3) throw new AssertionError("example 2");
        // Random binary arrays agree with the oracle.
        Random rnd = new Random(71);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(2);
            if (count(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Count Subarrays With Sum Below K For Positive Values (Author exercise)
<!-- id: sw-count-sum-below -->

**Approach.**
All values are positive, so removing a value from the front strictly lowers the sum. Therefore a span inside a valid span is valid, and the window method applies. The method adds each entering value to `sum`. While `sum >= k`, it subtracts `nums[left]` and moves `left` forward. Then every start from `left` to `right` gives a sum below `k`, and the method adds `right - left + 1`. The invariant is that `sum` equals the sum of `nums[left..right]`, and it is below `k` after the loop.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps a few variables.

```java run
import java.util.Random;

public final class CountSumBelow {
    /**
     * Counts subarrays of positive integers with sum below k.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), a few variables.
     * Invariant: sum equals nums[left..right] and is below k after the shrink loop.
     */
    static long count(int[] nums, int k) {
        long sum = 0, total = 0;
        int left = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            sum += nums[right];
            // Shrink: runs while the sum reaches k; positivity makes each removal lower the sum.
            while (left <= right && sum >= k) {
                sum -= nums[left];
                left++;
            }
            // All starts left..right give sums below k.
            total += right - left + 1;
        }
        // The total number of valid subarrays.
        return total;
    }

    /** Oracle: tests every pair of indexes. */
    static long oracle(int[] a, int k) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            long s = 0;
            for (int j = i; j < a.length; j++) { s += a[j]; if (s < k) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (count(new int[] {2, 1, 3, 1, 2}, 5) != 9) throw new AssertionError("example 1");
        if (count(new int[] {1, 1, 1}, 3) != 5) throw new AssertionError("example 2");
        // The false friend: with a negative value, the same code undercounts.
        if (count(new int[] {4, -3, 2}, 3) != 3 || oracle(new int[] {4, -3, 2}, 3) != 4) throw new AssertionError("negative values break the rule");
        // Random positive arrays agree with the oracle.
        Random rnd = new Random(72);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(6);
            int k = 1 + rnd.nextInt(20);
            if (count(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] K At The Minimum (Author exercise)
<!-- id: sw-count-k-minimum -->

**Approach.**
For `k = 1`, every value is at least 1, so every single-value span already has a sum of at least `k`. When a value enters, the shrink loop removes values until the window is empty, and the empty window has sum 0, which is below `k`. At that point `left = right + 1`, and the method adds `right - left + 1 = 0`. The loop always ends, because the empty window passes the check, so `left` never exceeds `right + 1`. The invariant is that `left <= right + 1` after every loop and that the contribution of an empty window is 0.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps a few variables.

```java run
import java.util.Random;

public final class KAtMinimum {
    /**
     * Counts subarrays of positive integers with sum below k, for k >= 1.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), a few variables.
     * Invariant: left <= right + 1 after every shrink loop, and sum equals nums[left..right].
     */
    static long count(int[] nums, int k) {
        long sum = 0, total = 0;
        int left = 0;
        for (int right = 0; right < nums.length; right++) {
            sum += nums[right];
            // Shrink: with k = 1 this removes everything, and the empty sum 0 < k ends the loop.
            while (sum >= k) {
                sum -= nums[left];
                left++;
            }
            // An empty window has left = right + 1, so it adds 0.
            total += right - left + 1;
        }
        // For k = 1 the total is 0.
        return total;
    }

    /** Oracle: tests every pair of indexes. */
    static long oracle(int[] a, int k) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            long s = 0;
            for (int j = i; j < a.length; j++) { s += a[j]; if (s < k) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (count(new int[] {2, 3, 1}, 1) != 0) throw new AssertionError("example 1");
        if (count(new int[] {1, 1}, 2) != 2) throw new AssertionError("example 2");
        // Random positive arrays with k near its minimum agree with the oracle.
        Random rnd = new Random(73);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(4);
            int k = 1 + rnd.nextInt(4);
            if (count(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Subarray Product Less Than K (LeetCode 713)
<!-- id: sw-product-less-than-k -->

**Approach.**
All values are at least 1, so removing a value from the front never raises the product. The method keeps the product of the window in a `long`, starting at 1, which is the product of an empty window. While the product reaches `k` and the window is not empty, it divides by `nums[left]` and moves `left` forward. A bound of 0 or 1 empties the window at every end index, and the guard `left <= right` stops the loop. The method adds `right - left + 1` after the loop. The invariant is that `prod` equals the product of `nums[left..right]`, and it is below `k` unless the window is empty.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps a few variables.

```java run
import java.util.Random;

public final class ProductLessThanK {
    /**
     * Counts subarrays with product below k, for positive integers.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), a few variables.
     * Invariant: prod equals the product of nums[left..right], and 1 for an empty window.
     */
    static long numSubarrayProductLessThanK(int[] nums, int k) {
        // The product of an empty window is 1.
        long prod = 1, total = 0;
        int left = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            prod *= nums[right];
            // Shrink: the left <= right guard keeps the loop finite when k is 0 or 1, where even an empty window has prod >= k.
            while (left <= right && prod >= k) {
                // Exact division: nums[left] is a factor of prod.
                prod /= nums[left];
                left++;
            }
            // Starts left..right are valid for this end index.
            total += right - left + 1;
        }
        // The total number of valid subarrays.
        return total;
    }

    /** Oracle: tests every pair of indexes. */
    static long oracle(int[] a, int k) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            long p = 1;
            for (int j = i; j < a.length; j++) { p *= a[j]; if (p < k) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (numSubarrayProductLessThanK(new int[] {3, 2, 4, 1}, 10) != 8) throw new AssertionError("example 1");
        if (numSubarrayProductLessThanK(new int[] {5, 6}, 5) != 0) throw new AssertionError("example 2");
        // Bounds 0 and 1 give no subarray.
        if (numSubarrayProductLessThanK(new int[] {1, 1, 1}, 1) != 0 || numSubarrayProductLessThanK(new int[] {1, 1, 1}, 0) != 0) throw new AssertionError("k <= 1");
        // Random positive arrays agree with the oracle.
        Random rnd = new Random(74);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(5);
            int k = rnd.nextInt(60);
            if (numSubarrayProductLessThanK(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```
