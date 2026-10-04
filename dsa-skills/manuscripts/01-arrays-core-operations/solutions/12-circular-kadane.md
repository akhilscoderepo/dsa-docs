<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Circular Kadane

#### Solution: [Build] Maximum Circular Subarray (LeetCode 918)
<!-- id: ar-circular-max -->

**Approach.** A circular subarray either stays inside the array or wraps past the last index. A wrapping subarray keeps a prefix and a suffix, so it leaves out one ordinary contiguous segment. Its sum equals the total minus the sum of that segment. The largest wrapping sum therefore uses the smallest ordinary segment sum. One loop computes the ordinary maximum with the restart-or-extend recurrence, the ordinary minimum with the mirrored recurrence, and the total. The answer is the larger of the ordinary maximum and the total minus the ordinary minimum. When the ordinary maximum is negative, every value is negative, the minimum segment is the whole array, the remainder is empty, and the wrapping value 0 is invalid, so the method returns the ordinary maximum.

**Complexity.**

- **Time** is O(n), because one loop updates both scans and the total in constant time per index.
- **Space** is O(1), because five integers hold all the state.

```java run
import java.util.Random;

public final class MaxCircular {
    /**
     * Returns the largest sum of a non-empty circular subarray.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only five integers are stored.
     * Invariant: a wrapping subarray has sum total minus the sum of the ordinary segment it leaves out.
     */
    static int maxCircular(int[] nums) {
        // All running values start at the first element, so every candidate is non-empty.
        int maxEnding = nums[0], maxOverall = nums[0];
        int minEnding = nums[0], minOverall = nums[0];
        int total = nums[0];
        // One pass from index 1; every iteration costs O(1).
        for (int i = 1; i < nums.length; i++) {
            // Read the value once and add it to the total.
            int x = nums[i];
            total += x;
            // Ordinary maximum: restart at x or extend the previous ending run.
            maxEnding = Math.max(x, maxEnding + x);
            maxOverall = Math.max(maxOverall, maxEnding);
            // Ordinary minimum: the mirrored recurrence finds the segment a wrapping run leaves out.
            minEnding = Math.min(x, minEnding + x);
            minOverall = Math.min(minOverall, minEnding);
        }
        // A negative ordinary maximum means every value is negative and the remainder would be empty.
        if (maxOverall < 0) return maxOverall;
        // Otherwise compare the ordinary maximum with the wrapping candidate.
        return Math.max(maxOverall, total - minOverall);
    }

    /** Oracle: tries every start and length with modular indices, in O(n^2) time. */
    static int brute(int[] nums) {
        // Length of the circular array.
        int n = nums.length;
        // Start below every sum.
        int best = Integer.MIN_VALUE;
        // Every start index.
        for (int s = 0; s < n; s++) {
            int sum = 0;
            // Every length from 1 to n, reading positions with the modulo operator.
            for (int l = 1; l <= n; l++) {
                sum += nums[(s + l - 1) % n];
                best = Math.max(best, sum);
            }
        }
        // The largest circular sum.
        return best;
    }

    public static void main(String[] args) {
        // Checks the lesson arrays and both examples.
        if (maxCircular(new int[]{4, -5, 2, -1, 6}) != 11) throw new AssertionError("example 1");
        if (maxCircular(new int[]{-2, 6, -3, 4, -5}) != 7) throw new AssertionError("example 2");
        if (maxCircular(new int[]{-6, -1, -4}) != -1) throw new AssertionError("all negative");
        // Checks that an ordinary scan alone misses the wrapping answer 11 and returns 7.
        int[] a = {4, -5, 2, -1, 6};
        int e = a[0], best = a[0];
        for (int i = 1; i < a.length; i++) { e = Math.max(a[i], e + a[i]); best = Math.max(best, e); }
        if (best != 7) throw new AssertionError("ordinary scan returns 7");
        // Checks a single element.
        if (maxCircular(new int[]{9}) != 9) throw new AssertionError("single element");
        // Checks 8,000 random arrays against the oracle.
        Random rnd = new Random(30);
        for (int t = 0; t < 8000; t++) {
            int[] r = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < r.length; i++) r[i] = rnd.nextInt(21) - 10;
            if (maxCircular(r) != brute(r)) throw new AssertionError("random " + java.util.Arrays.toString(r));
        }
    }
}
```

#### Solution: [Vary] Circular Minimum (Author exercise)
<!-- id: ar-circular-min -->

**Approach.** The argument is symmetric. A wrapping subarray has sum equal to the total minus the sum of the ordinary segment it leaves out, so the smallest wrapping sum uses the largest ordinary segment. The scan computes the ordinary minimum, the ordinary maximum and the total. The answer is the smaller of the ordinary minimum and the total minus the ordinary maximum. When every value is positive, the largest ordinary segment is the whole array, the remainder is empty, and the wrapping value 0 is invalid. That case holds exactly when the ordinary minimum is positive, so the method returns the ordinary minimum then.

**Complexity.**

- **Time** is O(n), because one loop updates the scans and the total per index.
- **Space** is O(1), because the method keeps five integers and no array.

```java run
import java.util.Random;

public final class CircularMinimum {
    /**
     * Returns the smallest sum of a non-empty circular subarray.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only five integers are stored.
     * Invariant: a wrapping subarray has sum total minus the sum of the ordinary segment it leaves out.
     */
    static int minCircular(int[] nums) {
        // All running values start at the first element.
        int maxEnding = nums[0], maxOverall = nums[0];
        int minEnding = nums[0], minOverall = nums[0];
        int total = nums[0];
        // One pass from index 1; every iteration costs O(1).
        for (int i = 1; i < nums.length; i++) {
            // Read the value and add it to the total.
            int x = nums[i];
            total += x;
            // The ordinary maximum is the segment that a wrapping minimum leaves out.
            maxEnding = Math.max(x, maxEnding + x);
            maxOverall = Math.max(maxOverall, maxEnding);
            // The ordinary minimum is the non-wrapping candidate.
            minEnding = Math.min(x, minEnding + x);
            minOverall = Math.min(minOverall, minEnding);
        }
        // A positive ordinary minimum means every value is positive and the remainder would be empty.
        if (minOverall > 0) return minOverall;
        // Otherwise compare the ordinary minimum with the wrapping candidate.
        return Math.min(minOverall, total - maxOverall);
    }

    /** Oracle: tries every start and length with modular indices, in O(n^2) time. */
    static int brute(int[] nums) {
        // Length of the circular array.
        int n = nums.length;
        // Start above every sum.
        int best = Integer.MAX_VALUE;
        // Every start index.
        for (int s = 0; s < n; s++) {
            int sum = 0;
            // Every length from 1 to n.
            for (int l = 1; l <= n; l++) {
                sum += nums[(s + l - 1) % n];
                best = Math.min(best, sum);
            }
        }
        // The smallest circular sum.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (minCircular(new int[]{-2, 6, -3, 4, -5}) != -7) throw new AssertionError("example 1");
        if (minCircular(new int[]{2, 5, 3}) != 2) throw new AssertionError("example 2");
        // Checks that every all-positive array returns its smallest element.
        Random rnd = new Random(31);
        for (int t = 0; t < 2000; t++) {
            int[] a = new int[1 + rnd.nextInt(8)];
            int min = Integer.MAX_VALUE;
            for (int i = 0; i < a.length; i++) { a[i] = 1 + rnd.nextInt(15); min = Math.min(min, a[i]); }
            if (minCircular(a) != min) throw new AssertionError("positive " + java.util.Arrays.toString(a));
        }
        // Checks 8,000 mixed arrays against the oracle.
        for (int t = 0; t < 8000; t++) {
            int[] r = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < r.length; i++) r[i] = rnd.nextInt(21) - 10;
            if (minCircular(r) != brute(r)) throw new AssertionError("random " + java.util.Arrays.toString(r));
        }
    }
}
```

#### Solution: [Boundary] All Negative (Author exercise)
<!-- id: ar-circular-all-negative -->

**Approach.** When every value is negative, any longer run has a smaller sum than its largest element, so the ordinary maximum is the single largest value. The smallest ordinary segment is the whole array, because each added negative value lowers the sum. The wrapping value is the total minus that segment, which is 0. That value comes from removing every element, so it describes the empty subarray and no allowed one. The method returns the pair of the ordinary maximum and the wrapping value, and the first entry is the answer.

**Complexity.**

- **Time** is O(n), because the scans read each value once.
- **Space** is O(1), because the method keeps a few integers and builds a two-entry result.

```java run
import java.util.Random;

public final class AllNegativeCircular {
    /**
     * Returns {largest circular sum, total minus smallest ordinary sum} for an all-negative array.
     * Time: O(n), because each index is read once.
     * Space: O(1), because only a few integers and the two-entry result are stored.
     * Invariant: the second entry equals 0 exactly when the smallest ordinary segment is the whole array.
     */
    static int[] answerAndWrap(int[] nums) {
        // Running values for the ordinary maximum and minimum, plus the total.
        int maxEnding = nums[0], maxOverall = nums[0];
        int minEnding = nums[0], minOverall = nums[0];
        int total = nums[0];
        // One pass from index 1.
        for (int i = 1; i < nums.length; i++) {
            // Add the value to the total and update both scans.
            int x = nums[i];
            total += x;
            maxEnding = Math.max(x, maxEnding + x);
            maxOverall = Math.max(maxOverall, maxEnding);
            minEnding = Math.min(x, minEnding + x);
            minOverall = Math.min(minOverall, minEnding);
        }
        // The answer is the ordinary maximum, and the wrapping value shows the empty remainder.
        return new int[]{maxOverall, total - minOverall};
    }

    /** Oracle: the largest circular sum by trying every start and length. */
    static int brute(int[] nums) {
        // Length of the circular array and a start below every sum.
        int n = nums.length, best = Integer.MIN_VALUE;
        // Every start and every length, with modular indices.
        for (int s = 0; s < n; s++) {
            int sum = 0;
            for (int l = 1; l <= n; l++) { sum += nums[(s + l - 1) % n]; best = Math.max(best, sum); }
        }
        // The largest circular sum.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (!java.util.Arrays.equals(answerAndWrap(new int[]{-6, -1, -4}), new int[]{-1, 0})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(answerAndWrap(new int[]{-5}), new int[]{-5, 0})) throw new AssertionError("example 2");
        // Checks on 5,000 random all-negative arrays that the wrapping value is 0 and the answer matches the oracle.
        Random rnd = new Random(32);
        for (int t = 0; t < 5000; t++) {
            int[] a = new int[1 + rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = -1 - rnd.nextInt(20);
            int[] r = answerAndWrap(a);
            if (r[1] != 0) throw new AssertionError("wrapping value is zero " + java.util.Arrays.toString(a));
            if (r[0] != brute(a)) throw new AssertionError("answer " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Wrapping Choice Leaves One Segment (LeetCode 918)
<!-- id: ar-circular-proof -->

**Approach.** A subarray that contains index `n - 1` and index 0 and omits at least one element keeps a prefix that starts at index 0 and a suffix that ends at index `n - 1`. The omitted elements lie between that prefix and that suffix, so they form exactly one contiguous segment. Both the prefix and the suffix are non-empty, so the segment contains neither index 0 nor index `n - 1`. It lies inside indices 1 through `n - 2` and is non-empty. Conversely, every non-empty segment in that range leaves a valid wrapping subarray. The sum of the wrapping subarray equals the total minus the segment sum, so the largest wrapping sum uses the smallest segment sum in that range. A minimum scan over indices 1 through `n - 2` finds it.

**Complexity.**

- **Time** is O(n), because one pass computes the total and one pass scans the interior.
- **Space** is O(1), because the method stores a few integers.

```java run
import java.util.Random;

public final class WrappingSegment {
    /**
     * Returns the largest sum of a subarray that contains indices 0 and n - 1 and omits at least one element.
     * Time: O(n), because the total and the interior scan each read every index at most once.
     * Space: O(1), because only a few integers are stored.
     * Invariant: minEnding is the smallest sum of a segment inside indices 1..n-2 that ends at the current index.
     */
    static int bestWrapping(int[] nums) {
        // Total of the whole array, computed once.
        int total = 0;
        for (int v : nums) total += v;
        // The interior scan starts at index 1, so the omitted segment never touches index 0.
        int minEnding = nums[1], minOverall = nums[1];
        // The loop stops before index n - 1, so the omitted segment never touches the last index.
        for (int i = 2; i < nums.length - 1; i++) {
            // Restart at the value or extend the previous segment, keeping the smaller sum.
            minEnding = Math.min(nums[i], minEnding + nums[i]);
            // Keep the smallest segment sum seen in the interior.
            minOverall = Math.min(minOverall, minEnding);
        }
        // The wrapping sum is the total minus the smallest omitted segment.
        return total - minOverall;
    }

    /** Oracle: tries every non-empty prefix and suffix that leave at least one element out. */
    static int brute(int[] nums) {
        // Length of the array and a start below every sum.
        int n = nums.length, best = Integer.MIN_VALUE;
        // Prefix length p and suffix length q, both at least 1.
        for (int p = 1; p < n; p++) {
            for (int q = 1; p + q < n; q++) {
                int sum = 0;
                // Add the prefix values.
                for (int i = 0; i < p; i++) sum += nums[i];
                // Add the suffix values.
                for (int i = n - q; i < n; i++) sum += nums[i];
                best = Math.max(best, sum);
            }
        }
        // The largest wrapping sum.
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (bestWrapping(new int[]{2, -6, 3, -1, 4}) != 8) throw new AssertionError("example 1");
        if (bestWrapping(new int[]{-2, 6, -3, 4, -5}) != 3) throw new AssertionError("example 2");
        // Checks the smallest allowed size, where the omitted segment is the single middle element.
        if (bestWrapping(new int[]{5, -3, 5}) != 10) throw new AssertionError("length 3");
        // Checks 8,000 random arrays of length 3 to 10 against the oracle.
        Random rnd = new Random(33);
        for (int t = 0; t < 8000; t++) {
            int[] a = new int[3 + rnd.nextInt(8)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(21) - 10;
            if (bestWrapping(a) != brute(a)) throw new AssertionError("random " + java.util.Arrays.toString(a));
        }
    }
}
```
