<!-- solutions-for: 01-fixed-size-aggregate-windows -->
### Fixed-Size Aggregate Windows

#### Solution: [Build] Sums of Every K-Block (Author exercise)
<!-- id: sw-block-sums -->

**Approach.** Keep one running total. Add each new value as `right` advances, and once `right` reaches `k` subtract the value that fell out of the window, which sits at `right - k`. Write the total into the answer whenever the window is full, which starts at `right = k - 1`.

**Complexity.** O(n) time, since each value is added once and subtracted at most once, and O(1) extra space beyond the returned array.

```java run
import java.util.Arrays;

public final class BlockSums {
    static int[] blockSums(int[] nums, int k) {
        int[] out = new int[nums.length - k + 1];
        int total = 0;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            if (right >= k) total -= nums[right - k];
            if (right >= k - 1) out[right - k + 1] = total;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(blockSums(new int[] {4, 2, 1, 7, 8}, 3), new int[] {7, 10, 16})) throw new AssertionError("example 1");
        if (!Arrays.equals(blockSums(new int[] {5}, 1), new int[] {5})) throw new AssertionError("example 2");
        int[] trace = blockSums(new int[] {4, 2, 1, 7, 8, 1, 2, 8, 1, 0}, 3);
        if (!Arrays.equals(trace, new int[] {7, 10, 16, 16, 11, 11, 11, 9})) throw new AssertionError("lesson trace");
    }
}
```

#### Solution: [Vary] Maximum Average Subarray I (LeetCode 643)
<!-- id: sw-max-average -->

**Approach.** The average of a block is its sum divided by `k`, and `k` is the same for every block, so the block with the largest sum has the largest average. Track the best sum, starting from the sum of the first block rather than from zero so that all-negative inputs work, and divide once at the end.

**Complexity.** O(n) time and O(1) extra space. The sum fits in an `int` here, because it is at most 10^5 values of size 10^4, which is 10^9.

```java run
public final class MaxAverage {
    static double findMaxAverage(int[] nums, int k) {
        int total = 0;
        for (int i = 0; i < k; i++) total += nums[i];
        int best = total;
        for (int right = k; right < nums.length; right++) {
            total += nums[right] - nums[right - k];
            best = Math.max(best, total);
        }
        return (double) best / k;
    }

    public static void main(String[] args) {
        if (Math.abs(findMaxAverage(new int[] {3, -1, 4, 1, 5}, 2) - 3.0) > 1e-9) throw new AssertionError("example 1");
        if (Math.abs(findMaxAverage(new int[] {-8, -3, -6}, 2) - (-4.5)) > 1e-9) throw new AssertionError("example 2");
        if (Math.abs(findMaxAverage(new int[] {-1}, 1) - (-1.0)) > 1e-9) throw new AssertionError("single negative");
    }
}
```

#### Solution: [Boundary] Whole-Array Window (Author exercise)
<!-- id: sw-whole-array-window -->

**Approach.** Check the contract first and return an empty array for a bad `k` before allocating anything. The accumulator and the output are `long`, because 10^5 values of size 10^9 reach 10^14. The loop is the same as the build exercise, and for `k == nums.length` the window is full only at the last index, so exactly one value is written.

**Complexity.** O(n) time and O(1) extra space beyond the output. An empty input array falls out of the first check, since `k > 0 = nums.length`.

```java run
import java.util.Arrays;

public final class WholeArrayWindow {
    static long[] blockSums(int[] nums, int k) {
        if (k < 1 || k > nums.length) return new long[0];
        long[] out = new long[nums.length - k + 1];
        long total = 0;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            if (right >= k) total -= nums[right - k];
            if (right >= k - 1) out[right - k + 1] = total;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(blockSums(new int[] {3, 1, 4}, 3), new long[] {8})) throw new AssertionError("example 1");
        if (!Arrays.equals(blockSums(new int[] {3, 1, 4}, 4), new long[0])) throw new AssertionError("example 2");
        if (!Arrays.equals(blockSums(new int[0], 1), new long[0])) throw new AssertionError("empty input");
        if (!Arrays.equals(blockSums(new int[] {1, 2}, 0), new long[0])) throw new AssertionError("k zero");
        int big = 1_000_000_000;
        if (!Arrays.equals(blockSums(new int[] {big, big, big}, 3), new long[] {3_000_000_000L})) throw new AssertionError("overflow");
    }
}
```

#### Solution: [Recognize] Maximum Number of Vowels in a Substring of Given Length (LeetCode 1456)
<!-- id: sw-max-vowels -->

**Approach.** Each character contributes 1 to the aggregate when it is a vowel and 0 otherwise, so the aggregate is the vowel count of the current window. A small helper decides the contribution, and the same helper is applied to the entering letter and to the leaving letter. No substring is ever created.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class MaxVowels {
    private static int vowel(char c) {
        return (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') ? 1 : 0;
    }

    static int maxVowels(String s, int k) {
        int count = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            count += vowel(s.charAt(right));
            if (right >= k) count -= vowel(s.charAt(right - k));
            if (right >= k - 1) best = Math.max(best, count);
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxVowels("queueing", 3) != 3) throw new AssertionError("example 1");
        if (maxVowels("rhythms", 4) != 0) throw new AssertionError("example 2");
        if (maxVowels("abciiidef", 3) != 3) throw new AssertionError("run of vowels");
        if (maxVowels("aeiou", 5) != 5) throw new AssertionError("whole string");
    }
}
```

#### Solution: [Extend] Grumpy Bookstore Owner (LeetCode 1052)
<!-- id: sw-grumpy-owner -->

**Approach.** Customers in minutes when the owner is already calm are satisfied regardless, so add them up once as a baseline. The technique can only add customers from grumpy minutes inside its window, so the running aggregate of a fixed window of length `minutes` is the sum of `customers[i]` over grumpy minutes in it. The answer is the baseline plus the largest such gain.

**Complexity.** O(n) time and O(1) extra space. The largest possible total is 2 * 10^4 * 1000 = 2 * 10^7, which fits in an `int`.

```java run
public final class GrumpyOwner {
    static int maxSatisfied(int[] customers, int[] grumpy, int minutes) {
        int baseline = 0, gain = 0, bestGain = 0;
        for (int right = 0; right < customers.length; right++) {
            if (grumpy[right] == 0) baseline += customers[right];
            else gain += customers[right];
            if (right >= minutes && grumpy[right - minutes] == 1) gain -= customers[right - minutes];
            if (right >= minutes - 1) bestGain = Math.max(bestGain, gain);
        }
        return baseline + bestGain;
    }

    public static void main(String[] args) {
        if (maxSatisfied(new int[] {2, 3, 1, 4, 2}, new int[] {1, 0, 1, 1, 0}, 2) != 10) throw new AssertionError("example 1");
        if (maxSatisfied(new int[] {5, 1}, new int[] {1, 1}, 1) != 5) throw new AssertionError("example 2");
        if (maxSatisfied(new int[] {4, 10, 10}, new int[] {1, 1, 0}, 2) != 24) throw new AssertionError("calm at the end");
        if (maxSatisfied(new int[] {5}, new int[] {1}, 1) != 5) throw new AssertionError("single minute");
    }
}
```
