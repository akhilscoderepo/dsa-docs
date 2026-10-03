<!-- solutions-for: 06-exactly-k-by-subtraction -->
### Exactly-K By Subtraction

#### Solution: [Build] Exactly One Odd Number (Author exercise)
<!-- id: sw-exactly-one-odd -->

**Approach.** Count the subarrays with at most one odd number, then subtract those with at most zero odd numbers. Each pass is a monotone window: the number of odd values is the violation counter, and for each right endpoint every start from `left` to `right` is valid.

**Complexity.** O(n) time and O(1) extra space. The count is a `long` since an array of 10^5 entries has about 5 * 10^9 subarrays.

```java run
public final class ExactlyOneOdd {
    static long atMost(int[] nums, int k) {
        if (k < 0) return 0;
        long total = 0;
        int left = 0, odds = 0;
        for (int right = 0; right < nums.length; right++) {
            odds += nums[right] & 1;
            while (odds > k) {
                odds -= nums[left] & 1;
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    static long exactlyOneOdd(int[] nums) {
        return atMost(nums, 1) - atMost(nums, 0);
    }

    public static void main(String[] args) {
        if (exactlyOneOdd(new int[] {1, 2, 2}) != 3) throw new AssertionError("example 1");
        if (exactlyOneOdd(new int[] {2, 4}) != 0) throw new AssertionError("example 2");
        if (exactlyOneOdd(new int[] {-3}) != 1) throw new AssertionError("negative odd");
        if (exactlyOneOdd(new int[] {1, 1}) != 2) throw new AssertionError("two odds");
    }
}
```

#### Solution: [Vary] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: sw-nice-subarrays -->

**Approach.** The identity is `exactly(k) = atMost(k) - atMost(k - 1)`, where the quantity is the number of odd values. With `k >= 1` the second budget is never negative, though the guard is kept for safety.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class NiceSubarrays {
    static long atMost(int[] nums, int k) {
        if (k < 0) return 0;
        long total = 0;
        int left = 0, odds = 0;
        for (int right = 0; right < nums.length; right++) {
            odds += nums[right] & 1;
            while (odds > k) {
                odds -= nums[left] & 1;
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    static int numberOfSubarrays(int[] nums, int k) {
        return (int) (atMost(nums, k) - atMost(nums, k - 1));
    }

    public static void main(String[] args) {
        if (numberOfSubarrays(new int[] {2, 1, 2, 1, 1, 2}, 2) != 6) throw new AssertionError("example 1");
        if (numberOfSubarrays(new int[] {4, 6}, 1) != 0) throw new AssertionError("example 2");
        if (numberOfSubarrays(new int[] {1, 1, 2, 1, 1}, 3) != 2) throw new AssertionError("lesson trace");
        if (numberOfSubarrays(new int[] {2, 2, 2, 1, 2, 2, 1, 2, 2, 2}, 2) != 16) throw new AssertionError("long quiet stretches");
    }
}
```

#### Solution: [Boundary] Empty At-Most Budget (Author exercise)
<!-- id: sw-empty-budget -->

**Approach.** Count ones as the violation quantity. When `k` is zero, the second pass has a budget of minus one, and the at-most count returns zero immediately because no subarray has fewer than zero ones. The first pass then counts every subarray made only of zeros.

**Complexity.** O(n) time and O(1) extra space, with a `long` accumulator.

```java run
public final class EmptyBudget {
    static long atMost(int[] nums, int k) {
        if (k < 0) return 0;
        long total = 0;
        int left = 0, ones = 0;
        for (int right = 0; right < nums.length; right++) {
            ones += nums[right];
            while (ones > k) {
                ones -= nums[left];
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    static long exactlyK(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    public static void main(String[] args) {
        if (exactlyK(new int[] {0, 0, 0}, 0) != 6) throw new AssertionError("example 1");
        if (exactlyK(new int[] {1, 0, 1}, 3) != 0) throw new AssertionError("example 2");
        if (exactlyK(new int[] {1, 0, 1, 0, 1}, 2) != 4) throw new AssertionError("two ones");
        if (exactlyK(new int[] {1}, 0) != 0) throw new AssertionError("no zero-only subarray");
    }
}
```

#### Solution: [Recognize] Subarrays with K Different Integers (LeetCode 992)
<!-- id: sw-k-different-integers -->

**Approach.** The monotone quantity is the number of distinct values in the window, kept with a count table. The at-most count adds `right - left + 1` for every right endpoint after repairing. The answer is `atMost(k) - atMost(k - 1)`.

**Complexity.** O(n) time. The count table has length `n + 1` because values are bounded by the array length, so extra space is O(n).

```java run
public final class KDifferentIntegers {
    static int atMost(int[] nums, int k) {
        if (k < 0) return 0;
        int[] count = new int[nums.length + 2];
        int distinct = 0, left = 0, total = 0;
        for (int right = 0; right < nums.length; right++) {
            if (count[nums[right]]++ == 0) distinct++;
            while (distinct > k) {
                if (--count[nums[left]] == 0) distinct--;
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    static int subarraysWithKDistinct(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    public static void main(String[] args) {
        if (subarraysWithKDistinct(new int[] {3, 1, 3, 1, 2}, 2) != 7) throw new AssertionError("example 1");
        if (subarraysWithKDistinct(new int[] {2, 2, 2}, 2) != 0) throw new AssertionError("example 2");
        if (subarraysWithKDistinct(new int[] {1, 2, 1, 3, 4}, 3) != 3) throw new AssertionError("three distinct");
        if (subarraysWithKDistinct(new int[] {1, 1, 1}, 1) != 6) throw new AssertionError("all equal");
    }
}
```
