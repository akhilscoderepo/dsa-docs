<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Kadane State

#### Solution: [Build] Maximum Subarray (LeetCode 53)
<!-- id: ar-max-subarray -->

**Approach.** The scan keeps the best sum of a subarray that ends at the current index and the best sum seen anywhere. At each index the subarray either restarts at that value or extends the previous ending subarray. The extension wins exactly when the previous ending sum is positive. The invariant is that after index `i`, the ending sum equals the true best sum of a subarray ending at `i`. Every optimal subarray ends at some index, so the running maximum of the ending sums is the answer. Both variables start from `nums[0]`, because zero would stand for an empty subarray.

**Complexity.**

- **Time** is O(n), because one pass makes one constant-time decision per index.
- **Space** is O(1), because the scan stores two integers and one loop index.

```java run
import java.util.Random;

public final class MaxSubarray {
    /**
     * Returns the largest sum of a non-empty contiguous subarray.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only two sums are stored.
     * Invariant: bestEndingHere is the best sum of a subarray that ends at index i.
     */
    static int maxSubarray(int[] nums) {
        // Both sums start at the first value, so the subarray is never empty.
        int bestEndingHere = nums[0];
        int bestOverall = nums[0];
        // Loop from index 1: index 0 is already covered by the initial values; cost is n - 1 iterations.
        for (int i = 1; i < nums.length; i++) {
            // Restart at nums[i] or extend the previous ending subarray, whichever sum is larger.
            bestEndingHere = Math.max(nums[i], bestEndingHere + nums[i]);
            // Fold the new ending sum into the global best.
            bestOverall = Math.max(bestOverall, bestEndingHere);
        }
        // The global best covers every possible ending index.
        return bestOverall;
    }

    /** Oracle: tries every start and end with a running sum, in O(n^2) time. */
    static int brute(int[] nums) {
        // Start below any possible sum so negative arrays work.
        int best = Integer.MIN_VALUE;
        // Each start index begins a fresh running sum.
        for (int s = 0; s < nums.length; s++) {
            int sum = 0;
            // Each end index extends the running sum by one value.
            for (int e = s; e < nums.length; e++) {
                sum += nums[e];
                best = Math.max(best, sum);
            }
        }
        // The largest sum over all pairs.
        return best;
    }

    public static void main(String[] args) {
        // Checks the lesson trace array and the single-element example.
        if (maxSubarray(new int[]{-2, 1, -3, 4, -1, 2, 1, -5, 4}) != 6) throw new AssertionError("lesson array");
        if (maxSubarray(new int[]{5, -9, 6, 2, -1, 3, -8}) != 10) throw new AssertionError("example 1");
        if (maxSubarray(new int[]{-7}) != -7) throw new AssertionError("example 2");
        // Checks that the largest allowed total, 10^4 times 10^5, fits in int.
        int[] big = new int[100000];
        java.util.Arrays.fill(big, 10000);
        if (maxSubarray(big) != 1_000_000_000) throw new AssertionError("large positive sum fits in int");
        // Checks 5,000 random arrays against the oracle, with empty input excluded by contract.
        Random rnd = new Random(10);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(41) - 20;
            if (maxSubarray(a) != brute(a)) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Minimum Subarray Sum (Author exercise)
<!-- id: ar-min-subarray-sum -->

**Approach.** The recurrence mirrors the maximum case with the comparison reversed. The ending sum restarts at `nums[i]` when the previous ending sum is positive, because a positive prefix only raises the total. It extends when the previous ending sum is negative. The invariant is that the ending sum equals the smallest sum of a subarray ending at the current index. For an all-positive array no extension ever helps, so the answer is the smallest element.

**Complexity.**

- **Time** is O(n), because the scan makes one constant-time decision per index.
- **Space** is O(1), because two running minimums are the only state.

```java run
import java.util.Random;

public final class MinSubarraySum {
    /**
     * Returns the smallest sum of a non-empty contiguous subarray.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only two sums are stored.
     * Invariant: minEndingHere is the smallest sum of a subarray that ends at index i.
     */
    static int minSubarray(int[] nums) {
        // Both sums start at the first value, so the subarray is never empty.
        int minEndingHere = nums[0];
        int minOverall = nums[0];
        // One pass from index 1; each iteration costs O(1).
        for (int i = 1; i < nums.length; i++) {
            // Restart or extend, choosing the smaller sum.
            minEndingHere = Math.min(nums[i], minEndingHere + nums[i]);
            // Keep the smallest ending sum seen so far.
            minOverall = Math.min(minOverall, minEndingHere);
        }
        // The smallest ending sum over all indices is the answer.
        return minOverall;
    }

    /** Oracle: tries every start and end with a running sum, in O(n^2) time. */
    static int brute(int[] nums) {
        // Start above any possible sum.
        int best = Integer.MAX_VALUE;
        // Every start index begins a fresh sum.
        for (int s = 0; s < nums.length; s++) {
            int sum = 0;
            // Every end index extends the sum by one value.
            for (int e = s; e < nums.length; e++) {
                sum += nums[e];
                best = Math.min(best, sum);
            }
        }
        // The smallest sum over all pairs.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (minSubarray(new int[]{3, -4, 2, -3, 5}) != -5) throw new AssertionError("example 1");
        if (minSubarray(new int[]{4, 9, 2}) != 2) throw new AssertionError("example 2");
        // Checks that every all-positive array returns its smallest element.
        Random rnd = new Random(11);
        for (int t = 0; t < 2000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            int min = Integer.MAX_VALUE;
            for (int i = 0; i < a.length; i++) { a[i] = 1 + rnd.nextInt(20); min = Math.min(min, a[i]); }
            if (minSubarray(a) != min) throw new AssertionError("positive " + java.util.Arrays.toString(a));
        }
        // Checks 5,000 mixed arrays against the oracle.
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(41) - 20;
            if (minSubarray(a) != brute(a)) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] All Negative (Author exercise)
<!-- id: ar-all-negative-max -->

**Approach.** Extending a negative ending sum with another negative value always gives a smaller number than the value alone. Therefore the ending sum restarts at every index, and the answer is the largest single element. A start value of zero fails because zero is the sum of the empty subarray, which the contract forbids. The scan then returns 0 for every all-negative array, although no non-empty subarray reaches 0. Starting from `nums[0]` keeps every candidate a real non-empty subarray.

**Complexity.**

- **Time** is O(n), because the loop visits every index a single time.
- **Space** is O(1), because the code keeps two sums and no array.

```java run
import java.util.Random;

public final class AllNegative {
    /**
     * Returns the largest non-empty subarray sum, starting from the first element.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only two sums are stored.
     * Invariant: bestEndingHere is the best sum of a non-empty subarray that ends at index i.
     */
    static int correct(int[] nums) {
        // Start from the first element so the subarray is non-empty.
        int bestEndingHere = nums[0];
        int bestOverall = nums[0];
        // One pass; each step restarts or extends.
        for (int i = 1; i < nums.length; i++) {
            bestEndingHere = Math.max(nums[i], bestEndingHere + nums[i]);
            bestOverall = Math.max(bestOverall, bestEndingHere);
        }
        // The result is a real subarray sum.
        return bestOverall;
    }

    /** The faulty variant: it starts both sums at zero, which stands for the empty subarray. */
    static int zeroStart(int[] nums) {
        // Zero start admits the empty subarray, which the contract forbids.
        int bestEndingHere = 0;
        int bestOverall = 0;
        // The same recurrence runs from index 0.
        for (int i = 0; i < nums.length; i++) {
            bestEndingHere = Math.max(nums[i], bestEndingHere + nums[i]);
            bestOverall = Math.max(bestOverall, bestEndingHere);
        }
        // For all-negative input this returns 0, which is wrong.
        return bestOverall;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (correct(new int[]{-8, -3, -6}) != -3) throw new AssertionError("example 1");
        if (correct(new int[]{-1}) != -1) throw new AssertionError("example 2");
        // Checks that the zero start returns 0, which no non-empty subarray of negatives can reach.
        if (zeroStart(new int[]{-8, -3, -6}) != 0) throw new AssertionError("zero start returns zero");
        // Checks that for 3,000 random all-negative arrays the answer is the largest element.
        Random rnd = new Random(12);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            int max = Integer.MIN_VALUE;
            for (int i = 0; i < a.length; i++) { a[i] = -1 - rnd.nextInt(30); max = Math.max(max, a[i]); }
            if (correct(a) != max) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Maximum Absolute Sum (LeetCode 1749)
<!-- id: ar-max-abs-sum -->

**Approach.** The largest absolute sum equals the larger of the largest subarray sum and the negation of the smallest subarray sum. One scan keeps a maximum ending state and a minimum ending state side by side. Both states may restart at zero, because the contract allows the empty subarray with sum 0. The invariant is that after each index the two ending sums are the largest and smallest sums of subarrays ending there, including the empty one. The answer is the largest absolute value either state reaches.

**Complexity.**

- **Time** is O(n), because each index updates two states in constant time.
- **Space** is O(1), because the scan stores two ending sums and one answer.

```java run
import java.util.Random;

public final class MaxAbsSum {
    /**
     * Returns the largest absolute value of any contiguous subarray sum, with the empty subarray allowed.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only three integers are stored.
     * Invariant: maxEnd and minEnd are the largest and smallest sums of subarrays ending at i, or 0 for empty.
     */
    static int maxAbsoluteSum(int[] nums) {
        // Both ending sums start at zero, which is the empty subarray.
        int maxEnd = 0, minEnd = 0, answer = 0;
        // One pass; each index updates both states.
        for (int v : nums) {
            // The largest ending sum restarts at zero when the previous sum is negative.
            maxEnd = Math.max(0, maxEnd + v);
            // The smallest ending sum restarts at zero when the previous sum is positive.
            minEnd = Math.min(0, minEnd + v);
            // Either state can give the largest magnitude.
            answer = Math.max(answer, Math.max(maxEnd, -minEnd));
        }
        // The best magnitude over all ending positions.
        return answer;
    }

    /** Oracle: checks every subarray sum with a running sum. */
    static int brute(int[] nums) {
        // The empty subarray gives 0.
        int best = 0;
        // Every start begins a new sum.
        for (int s = 0; s < nums.length; s++) {
            int sum = 0;
            // Every end extends the sum and updates the best magnitude.
            for (int e = s; e < nums.length; e++) {
                sum += nums[e];
                best = Math.max(best, Math.abs(sum));
            }
        }
        // The largest magnitude.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (maxAbsoluteSum(new int[]{2, -5, 1, -4, 3, -2}) != 8) throw new AssertionError("example 1");
        if (maxAbsoluteSum(new int[]{4, -1, 3}) != 6) throw new AssertionError("example 2");
        // Checks 5,000 random arrays against the oracle.
        Random rnd = new Random(13);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(41) - 20;
            if (maxAbsoluteSum(a) != brute(a)) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```
