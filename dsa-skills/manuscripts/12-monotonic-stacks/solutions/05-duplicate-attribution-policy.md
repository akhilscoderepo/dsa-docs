<!-- solutions-for: 12-monotonic-stacks -->
### Solutions For Breaking Ties

#### Solution: [Build] Two Equal Minima Ownership (Author exercise)
<!-- id: ms-two-equal-minima -->

**Approach.**
Fix the first index `l` of a window and extend the last index `r` from `l` to the end. Keep `best`, the index of the rightmost minimum of the window so far. When the new value is less than or equal to the value at `best`, the new index becomes the owner, because an equal value to the right takes the title. Each extension gives one credit to `best`. The invariant is that `best` holds the rightmost minimum of the window from `l` to `r`, so every window gets exactly one credit.

**Complexity.**
- **Time** is O(n^2), because the loops visit every window once.
- **Space** is O(n) for the result array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TwoEqualMinima {
    /**
     * Counts the windows owned by each index under the rightmost-minimum rule.
     * Time: O(n^2). Space: O(n).
     * Invariant: best is the rightmost minimum of the window from l to r.
     */
    static int[] solve(int[] nums) {
        int n = nums.length;
        int[] owned = new int[n];
        // Each start index opens n - l windows.
        for (int l = 0; l < n; l++) {
            int best = l;
            // Extending r adds one window per step.
            for (int r = l; r < n; r++) {
                // A tie moves the title to the later index.
                if (nums[r] <= nums[best]) best = r;
                owned[best]++;
            }
        }
        return owned;
    }

    /** Reference: find the rightmost minimum of every window by a separate scan. */
    static int[] oracle(int[] nums) {
        int n = nums.length;
        int[] owned = new int[n];
        for (int l = 0; l < n; l++) {
            for (int r = l; r < n; r++) {
                int min = Integer.MAX_VALUE;
                for (int k = l; k <= r; k++) min = Math.min(min, nums[k]);
                int owner = r;
                while (nums[owner] != min) owner--;
                owned[owner]++;
            }
        }
        return owned;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {2, 2, 2}), new int[] {1, 2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {2, 7, 2, 7, 2}), new int[] {2, 1, 6, 1, 5})) throw new AssertionError("example 2");
        // Random arrays with repeated values must match the oracle and cover every window.
        Random rnd = new Random(71);
        for (int t = 0; t < 2000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3);
            int[] got = solve(a);
            if (!Arrays.equals(got, oracle(a))) throw new AssertionError(Arrays.toString(a));
            int sum = 0;
            for (int c : got) sum += c;
            if (sum != a.length * (a.length + 1) / 2) throw new AssertionError("partition");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Strict Left, Non-Strict Right (Author exercise)
<!-- id: ms-strict-left-non-strict-right -->

**Approach.**
One stack pass finds both boundaries. The stack keeps indices with strictly increasing values. A new value pops every top that is greater than or equal to it, and each popped index receives the new index as its right boundary, the first value that is smaller or equal. After the pops, the surviving top is the nearest strictly smaller value before the new index, so it becomes the left boundary. Indices that remain at the end receive the right sentinel `n`. The count for index `i` is `(i - left) * (right - i)`, computed in `long` because the product can pass the range of `int`.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), for the stack and the two boundary arrays.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class StrictLeftNonStrictRight {
    /**
     * Returns (i - left) * (right - i) for every index, with a strict left and a non-strict right boundary.
     * Time: O(n). Space: O(n).
     * Invariant: stack values strictly increase from bottom to top.
     */
    static long[] solve(int[] nums) {
        int n = nums.length;
        int[] left = new int[n];
        int[] right = new int[n];
        // Indices that are never popped keep the right sentinel n.
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            // Greater or equal tops end at i, which is smaller or equal for them.
            while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) right[stack.pop()] = i;
            // The surviving top is strictly smaller than nums[i].
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        long[] owned = new long[n];
        // The cast keeps the product in long before it can overflow int.
        for (int i = 0; i < n; i++) owned[i] = (long) (i - left[i]) * (right[i] - i);
        return owned;
    }

    /** Reference: enumerate every window and credit its rightmost minimum. */
    static long[] oracle(int[] nums) {
        int n = nums.length;
        long[] owned = new long[n];
        for (int l = 0; l < n; l++) {
            int best = l;
            for (int r = l; r < n; r++) {
                if (nums[r] <= nums[best]) best = r;
                owned[best]++;
            }
        }
        return owned;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {3, 2, 2, 4, 2, 5}), new long[] {1, 2, 6, 1, 10, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {4, 4, 1, 4, 4}), new long[] {1, 2, 9, 1, 2})) throw new AssertionError("example 2");
        // One minimum in the middle of a long array owns more windows than int can count.
        int[] big = new int[100000];
        java.util.Arrays.fill(big, 1);
        big[50000] = 0;
        if (solve(big)[50000] != 50001L * 50000L || solve(big)[50000] <= Integer.MAX_VALUE) throw new AssertionError("middle");
        // Random arrays with repeated values must match the oracle.
        Random rnd = new Random(73);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] All Equal Array (Author exercise)
<!-- id: ms-all-equal-array -->

**Approach.**
The counts come from the same single pass, and the final entry is their sum. In an all-equal array, each new value pops the previous index, so index `i` has right boundary `i + 1` and left boundary `-1`. Its count is `(i + 1) * 1`, which gives 1, 2 up to `n`, and the sum is `n * (n + 1) / 2`. The solution checks the sum against that formula before it returns, so a wrong tie rule fails loudly. The harness also confirms that the strict-both and non-strict-both variants break the sum, which shows why the two sides must differ.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), for the stack, the boundaries and the result.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class AllEqualCounts {
    /**
     * Returns the owned counts followed by their sum.
     * Time: O(n). Space: O(n).
     * Invariant: the left side is strict and the right side is non-strict, so every window has one owner.
     */
    static long[] solve(int[] nums, boolean strictLeft, boolean strictRight) {
        int n = nums.length;
        long[] out = new long[n + 1];
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        // The left scan stops at a strictly smaller value, or at a smaller-or-equal value.
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && (strictLeft ? nums[stack.peek()] >= nums[i] : nums[stack.peek()] > nums[i])) stack.pop();
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        stack.clear();
        // The right scan resolves at a smaller value, or at a smaller-or-equal value.
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && (strictRight ? nums[stack.peek()] > nums[i] : nums[stack.peek()] >= nums[i])) right[stack.pop()] = i;
            stack.push(i);
        }
        long total = 0;
        for (int i = 0; i < n; i++) {
            out[i] = (long) (i - left[i]) * (right[i] - i);
            total += out[i];
        }
        out[n] = total;
        return out;
    }

    /** The graded convention: strict on the left, non-strict on the right. */
    static long[] solve(int[] nums) {
        return solve(nums, true, false);
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {2, 2, 2}), new long[] {1, 2, 3, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {5, 1, 5, 1, 5}), new long[] {1, 4, 1, 8, 1, 15})) throw new AssertionError("example 2");
        // The graded convention always sums to n(n+1)/2.
        Random rnd = new Random(79);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3);
            long n = a.length;
            if (solve(a)[a.length] != n * (n + 1) / 2) throw new AssertionError("partition " + Arrays.toString(a));
        }
        // Strict on both sides counts the window of two equal values twice.
        if (solve(new int[] {2, 2}, true, true)[2] != 4) throw new AssertionError("strict both");
        // Non-strict on both sides leaves that window without an owner.
        if (solve(new int[] {2, 2}, false, false)[2] != 2) throw new AssertionError("non-strict both");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-of-subarray-minimums-exact -->

**Approach.**
Every window has one minimum value and one owner under the rightmost-minimum rule. The value `arr[i]` therefore contributes `arr[i]` once for each window that index `i` owns. The owned count is `(i - left) * (right - i)`, with a strictly smaller left boundary and a smaller-or-equal right boundary. One stack pass produces both boundaries. The sum of `arr[i] * owned[i]` is the answer. All arithmetic uses `long`, because the products reach about 10^4 times 4.5 x 10^8 and the total passes the range of `int`.

**Complexity.**
- **Time** is O(n), because the loop pushes each index once and pops it at most once.
- **Space** is O(n), for the stack and the boundary arrays.

```java run
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Random;

public final class SubarrayMinimumsExact {
    /**
     * Returns the exact sum of the minimum of every non-empty subarray.
     * Time: O(n). Space: O(n).
     * Invariant: stack values strictly increase from bottom to top.
     */
    static long sumSubarrayMins(int[] arr) {
        int n = arr.length;
        int[] left = new int[n];
        int[] right = new int[n];
        // Never-popped indices keep the sentinel n on the right.
        java.util.Arrays.fill(right, n);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            // Equal values pop, so the later index owns windows with ties.
            while (!stack.isEmpty() && arr[stack.peek()] >= arr[i]) right[stack.pop()] = i;
            left[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(i);
        }
        long sum = 0;
        // Each value counts once for every window its index owns.
        for (int i = 0; i < n; i++) sum += (long) arr[i] * (i - left[i]) * (right[i] - i);
        return sum;
    }

    /** Reference: maintain the running minimum while extending each window. */
    static long oracle(int[] arr) {
        long sum = 0;
        for (int l = 0; l < arr.length; l++) {
            int min = Integer.MAX_VALUE;
            for (int r = l; r < arr.length; r++) {
                min = Math.min(min, arr[r]);
                sum += min;
            }
        }
        return sum;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (sumSubarrayMins(new int[] {2, 7, 2, 7, 2}) != 40) throw new AssertionError("example 1");
        if (sumSubarrayMins(new int[] {6, 3, 6, 3, 6}) != 54) throw new AssertionError("example 2");
        // Random arrays with repeated values must match the oracle.
        Random rnd = new Random(83);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(4);
            if (sumSubarrayMins(a) != oracle(a)) throw new AssertionError(java.util.Arrays.toString(a));
        }
        // A long array of equal values keeps the sum exact.
        int[] big = new int[30000];
        java.util.Arrays.fill(big, 10000);
        if (sumSubarrayMins(big) != 10000L * 30000L * 30001L / 2) throw new AssertionError("big");
        System.out.println("ok");
    }
}
```
