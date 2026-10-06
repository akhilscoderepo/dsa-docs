<!-- solutions-for: 12-monotonic-stacks -->
### Solutions For Contribution Counting

#### Solution: [Build] Count Subarrays Owned By One Index (Author exercise)
<!-- id: ms-count-owned-by-one-index -->

**Approach.**
A pair `(l, r)` is valid for index `i` when `l` lies in `left[i] + 1` through `i` and `r` lies in `i` through `right[i] - 1`. The first range has `i - left[i]` members and the second has `right[i] - i` members. The two ranges do not depend on each other, so every start combines with every end, and the count is the product of the two sizes. The product is formed in `long`, because two `int` factors near 50000 already overflow `int`.

**Complexity.**
- **Time** is O(n), because each index needs one subtraction pair and one multiplication.
- **Space** is O(n) for the result array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CountOwnedByOneIndex {
    /**
     * Returns (i - left[i]) * (right[i] - i) for every index.
     * Time: O(n). Space: O(n).
     * Invariant: starts and ends are chosen independently.
     */
    static long[] solve(int[] left, int[] right) {
        long[] count = new long[left.length];
        // One product per index replaces a loop over all pairs.
        for (int i = 0; i < left.length; i++) {
            long starts = i - left[i];
            long ends = right[i] - i;
            count[i] = starts * ends;
        }
        return count;
    }

    /** Reference: count valid pairs one by one. */
    static long[] oracle(int[] left, int[] right) {
        long[] count = new long[left.length];
        for (int i = 0; i < left.length; i++) {
            for (int l = left[i] + 1; l <= i; l++) {
                for (int r = i; r < right[i]; r++) count[i]++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {-1, -1, -1}, new int[] {1, 2, 3}), new long[] {1, 2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {-1, 0, 0, 2}, new int[] {1, 4, 3, 4}), new long[] {1, 3, 2, 1})) throw new AssertionError("example 2");
        // The int product of two factors near 50000 wraps, while the long product is exact.
        int wrapped = 50001 * 50000;
        if (wrapped >= 0 || (long) 50001 * 50000 != 2500050000L) throw new AssertionError("overflow claim");
        // Random valid boundaries must match the pair-by-pair count.
        Random rnd = new Random(89);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] left = new int[n];
            int[] right = new int[n];
            for (int i = 0; i < n; i++) {
                left[i] = -1 + rnd.nextInt(i + 1);
                right[i] = i + 1 + rnd.nextInt(n - i);
            }
            if (!Arrays.equals(solve(left, right), oracle(left, right))) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Sum Owned Minimum Contributions (Author exercise)
<!-- id: ms-sum-owned-minimum-contributions -->

**Approach.**
One stack pass finds both boundaries. The stack keeps values that strictly increase from bottom to top. A new value pops every top that is greater than or equal to it, and each popped index receives the new index as its right boundary, the first smaller-or-equal value. The surviving top is the nearest strictly smaller value, so it is the left boundary of the new index. The contribution of index `i` is `nums[i]` times its start choices times its end choices, computed in `long`. The last entry is the sum of the contributions, which equals the sum of all window minimums. The harness also checks the mirror rule for maximums by negating the input.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), for the stack, the boundaries and the result.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class OwnedMinimumContributions {
    /**
     * Returns each index's contribution followed by their sum.
     * Time: O(n). Space: O(n).
     * Invariant: stack values strictly increase from bottom to top.
     */
    static long[] solve(int[] nums) {
        int n = nums.length;
        int[] left = new int[n];
        int[] right = new int[n];
        // Never-popped indices keep the right sentinel n.
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            // Greater or equal tops end at i, the first smaller-or-equal value.
            while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) right[stack.pop()] = i;
            // The surviving top is strictly smaller than nums[i].
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        long[] out = new long[n + 1];
        // The cast widens the first factor, so the whole product is long.
        for (int i = 0; i < n; i++) {
            out[i] = (long) nums[i] * (i - left[i]) * (right[i] - i);
            out[n] += out[i];
        }
        return out;
    }

    /** The maximum version from the lesson, with both comparisons reversed. */
    static long sumOfMaximums(int[] nums) {
        int n = nums.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] <= nums[i]) right[stack.pop()] = i;
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        long total = 0;
        for (int i = 0; i < n; i++) total += (long) nums[i] * (i - left[i]) * (right[i] - i);
        return total;
    }

    /** Reference: extend every window with running extremes. */
    static long[] oracle(int[] nums, boolean max) {
        long total = 0;
        for (int l = 0; l < nums.length; l++) {
            int best = max ? Integer.MIN_VALUE : Integer.MAX_VALUE;
            for (int r = l; r < nums.length; r++) {
                best = max ? Math.max(best, nums[r]) : Math.min(best, nums[r]);
                total += best;
            }
        }
        return new long[] {total};
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {2, 5, 3, 5, 1}), new long[] {8, 5, 12, 5, 5, 35})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {3, 3, 3}), new long[] {3, 6, 9, 18})) throw new AssertionError("example 2");
        // The maximum version matches the lesson trace total.
        if (sumOfMaximums(new int[] {2, 5, 3, 5, 1}) != 66) throw new AssertionError("maximum trace");
        // Random arrays with repeated values must match the oracle for both extremes.
        Random rnd = new Random(97);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(4);
            long[] got = solve(a);
            if (got[a.length] != oracle(a, false)[0]) throw new AssertionError("min " + Arrays.toString(a));
            if (sumOfMaximums(a) != oracle(a, true)[0]) throw new AssertionError("max " + Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Negative And Repeated Values (Author exercise)
<!-- id: ms-negative-and-repeated-values -->

**Approach.**
The ownership argument compares values and never uses their sign, so the same boundaries apply: a strictly smaller left boundary and a smaller-or-equal right boundary. Each window then has one owner, and the owner's value is the window's minimum, negative or not. The counts `(i - left) * (right - i)` stay positive, and only the product with a negative value is negative. The `long` total keeps its sign, so no remainder or absolute value is needed. The harness checks the tie behavior on repeated negative values and the sign of the result.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), for the stack and the two boundary arrays.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class NegativeAndRepeated {
    /**
     * Returns the exact sum of subarray minimums, which can be negative.
     * Time: O(n). Space: O(n).
     * Invariant: boundaries compare values only, so the sign does not matter.
     */
    static long solve(int[] nums) {
        int n = nums.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            // Greater or equal tops pop, regardless of sign.
            while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) right[stack.pop()] = i;
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        long total = 0;
        // A negative value makes its contribution negative, and long keeps the sign.
        for (int i = 0; i < n; i++) total += (long) nums[i] * (i - left[i]) * (right[i] - i);
        return total;
    }

    /** Reference: extend every window with a running minimum. */
    static long oracle(int[] nums) {
        long total = 0;
        for (int l = 0; l < nums.length; l++) {
            int min = Integer.MAX_VALUE;
            for (int r = l; r < nums.length; r++) {
                min = Math.min(min, nums[r]);
                total += min;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (solve(new int[] {-2, 5, -2}) != -5) throw new AssertionError("example 1");
        if (solve(new int[] {4, 1, 4, 1, 4}) != 24) throw new AssertionError("example 2");
        // An all-negative array gives a negative sum.
        if (solve(new int[] {-3, -3, -3}) != -18) throw new AssertionError("all negative");
        // Random arrays with negatives and repeats must match the oracle.
        Random rnd = new Random(101);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7) - 3;
            if (solve(a) != oracle(a)) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-of-subarray-minimums-modulo -->

**Approach.**
The cue is a sum over all subarrays that depends only on each subarray's minimum. Under the rightmost-minimum rule, index `i` owns `(i - left) * (right - i)` subarrays, with a strictly smaller left boundary and a smaller-or-equal right boundary. One stack pass finds both. Each contribution is formed in `long`, and the remainder is applied to the two factors before they multiply, so no product exceeds the `long` limit. The running total stays below the modulus after each addition.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), for the stack and the two boundary arrays.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class SubarrayMinimumsModulo {
    static final long MOD = 1_000_000_007L;

    /**
     * Returns the sum of subarray minimums modulo 10^9 + 7.
     * Time: O(n). Space: O(n).
     * Invariant: stack values strictly increase from bottom to top.
     */
    static int sumSubarrayMins(int[] arr) {
        int n = arr.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            // Equal values pop, so the later index owns windows with ties.
            while (!stack.isEmpty() && arr[stack.peek()] >= arr[i]) right[stack.pop()] = i;
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        long total = 0;
        for (int i = 0; i < n; i++) {
            // The window count is formed in long, then reduced before the value multiplies it.
            long windows = (long) (i - left[i]) * (right[i] - i) % MOD;
            total = (total + arr[i] % MOD * windows) % MOD;
        }
        return (int) total;
    }

    /** Reference: extend every window with a running minimum, then reduce once. */
    static long oracle(int[] arr) {
        long total = 0;
        for (int l = 0; l < arr.length; l++) {
            int min = Integer.MAX_VALUE;
            for (int r = l; r < arr.length; r++) {
                min = Math.min(min, arr[r]);
                total += min;
            }
        }
        return total % MOD;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (sumSubarrayMins(new int[] {7, 2, 9, 2, 5}) != 45) throw new AssertionError("example 1");
        int[] big = new int[30000];
        Arrays.fill(big, 30000);
        if (sumSubarrayMins(big) != 449905500) throw new AssertionError("example 2");
        // Random arrays with repeated values must match the oracle.
        Random rnd = new Random(103);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(30000);
            if (sumSubarrayMins(a) != oracle(a)) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```
