<!-- solutions-for: 10-kadane-state -->
### Kadane State

#### Solution: [Build] Maximum Subarray (LeetCode 53)
<!-- id: ar-maximum-subarray -->

**Approach.** Keep the best sum of a stretch ending at the current element and the best seen anywhere. For each element, the ending state becomes the larger of the element alone and the old ending state plus the element, and then the overall best is raised if needed. Starting both from the first element keeps the answer non-empty. The assertions compare with the quadratic enumeration on random arrays, including all-negative ones.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MaximumSubarray {
    static int maxSubarraySum(int[] nums) {
        int ending = nums[0], best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            ending = Math.max(nums[i], ending + nums[i]);
            best = Math.max(best, ending);
        }
        return best;
    }
    static int oracle(int[] nums) {
        int best = Integer.MIN_VALUE;
        for (int s = 0; s < nums.length; s++) {
            int sum = 0;
            for (int e = s; e < nums.length; e++) { sum += nums[e]; best = Math.max(best, sum); }
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxSubarraySum(new int[] {3, -4, 2, -1, 5, -6}) != 6) throw new AssertionError("example 1");
        if (maxSubarraySum(new int[] {-7}) != -7) throw new AssertionError("example 2");
        Random rnd = new Random(61);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(21) - 10;
            if (maxSubarraySum(a) != oracle(a)) throw new AssertionError("disagrees with enumeration");
        }
    }
}
```

#### Solution: [Vary] Minimum Subarray Sum (Author exercise)
<!-- id: ar-minimum-subarray-sum -->

**Approach.** The same recurrence with both comparisons flipped: the ending state is the smaller of the element alone and the old ending state plus the element, and the overall best is the smallest ending state seen. For all-positive input the old ending state only adds, so every element restarts the stretch and the answer is the smallest element. The assertions check both examples and compare with the quadratic enumeration.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MinimumSubarraySum {
    static int minSubarraySum(int[] nums) {
        int ending = nums[0], best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            ending = Math.min(nums[i], ending + nums[i]);
            best = Math.min(best, ending);
        }
        return best;
    }
    static int oracle(int[] nums) {
        int best = Integer.MAX_VALUE;
        for (int s = 0; s < nums.length; s++) {
            int sum = 0;
            for (int e = s; e < nums.length; e++) { sum += nums[e]; best = Math.min(best, sum); }
        }
        return best;
    }

    public static void main(String[] args) {
        if (minSubarraySum(new int[] {2, -5, 1, -4, 3, -4}) != -9) throw new AssertionError("example 1");
        if (minSubarraySum(new int[] {4, 2, 7}) != 2) throw new AssertionError("example 2");
        Random rnd = new Random(62);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(21) - 10;
            if (minSubarraySum(a) != oracle(a)) throw new AssertionError("disagrees with enumeration");
        }
        int[] pos = new int[8];
        for (int i = 0; i < pos.length; i++) pos[i] = 3 + rnd.nextInt(9);
        int smallest = Integer.MAX_VALUE;
        for (int v : pos) smallest = Math.min(smallest, v);
        if (minSubarraySum(pos) != smallest) throw new AssertionError("all positive must return the smallest element");
    }
}
```

#### Solution: [Boundary] All Negative (Author exercise)
<!-- id: ar-kadane-all-negative -->

**Approach.** With every value negative, carrying any earlier total forward only makes the sum worse, so every element restarts the stretch, and the best is the largest single element. Initializing from the first element makes that happen automatically. A version that starts the overall best at zero would report an empty stretch, which the contract forbids. The assertions show both versions on the examples and compare the correct one with the maximum element on random all-negative arrays.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class KadaneAllNegative {
    static int correct(int[] nums) {
        int ending = nums[0], best = nums[0];
        for (int i = 1; i < nums.length; i++) {
            ending = Math.max(nums[i], ending + nums[i]);
            best = Math.max(best, ending);
        }
        return best;
    }
    static int zeroStart(int[] nums) {
        int ending = 0, best = 0;
        for (int v : nums) {
            ending = Math.max(v, ending + v);
            best = Math.max(best, ending);
        }
        return best;
    }

    public static void main(String[] args) {
        if (correct(new int[] {-8, -3, -6}) != -3) throw new AssertionError("example 1");
        if (correct(new int[] {-5}) != -5) throw new AssertionError("example 2");
        if (zeroStart(new int[] {-8, -3, -6}) != 0) throw new AssertionError("the zero start reports an empty stretch");
        Random rnd = new Random(63);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            int max = Integer.MIN_VALUE;
            for (int i = 0; i < a.length; i++) { a[i] = -1 - rnd.nextInt(50); max = Math.max(max, a[i]); }
            if (correct(a) != max) throw new AssertionError("the answer must be the largest element");
        }
    }
}
```

#### Solution: [Recognize] Maximum Absolute Sum of Any Subarray (LeetCode 1749)
<!-- id: ar-max-absolute-sum -->

**Approach.** The largest magnitude is the larger of the maximum subarray sum and the negation of the minimum subarray sum. Run both ending states in the same pass, one with the maximum recurrence and one with the minimum recurrence, and return the larger of the best maximum and the negated best minimum. Because the array is non-empty, this is never negative, so allowing the empty subarray does not change the result. The oracle enumerates every subarray, including the empty one.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MaxAbsoluteSum {
    static int maxAbsoluteSum(int[] nums) {
        int hi = nums[0], lo = nums[0], bestHi = nums[0], bestLo = nums[0];
        for (int i = 1; i < nums.length; i++) {
            hi = Math.max(nums[i], hi + nums[i]);
            lo = Math.min(nums[i], lo + nums[i]);
            bestHi = Math.max(bestHi, hi);
            bestLo = Math.min(bestLo, lo);
        }
        return Math.max(bestHi, -bestLo);
    }
    static int oracle(int[] nums) {
        int best = 0;
        for (int s = 0; s < nums.length; s++) {
            int sum = 0;
            for (int e = s; e < nums.length; e++) { sum += nums[e]; best = Math.max(best, Math.abs(sum)); }
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxAbsoluteSum(new int[] {1, -3, 2, 3, -4}) != 5) throw new AssertionError("example 1");
        if (maxAbsoluteSum(new int[] {-2, -1, -3}) != 6) throw new AssertionError("example 2");
        if (maxAbsoluteSum(new int[] {0}) != 0) throw new AssertionError("single zero");
        Random rnd = new Random(64);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(21) - 10;
            if (maxAbsoluteSum(a) != oracle(a)) throw new AssertionError("disagrees with enumeration");
        }
    }
}
```
