<!-- solutions-for: 08-count-all-valid-subarrays-windows -->
### Count-All-Valid-Subarrays Windows

#### Solution: [Build] Count Subarrays With At Most One Zero (Author exercise)
<!-- id: sw-count-at-most-one-zero -->

**Approach.** Keep a counter of zeros inside the window and repair from the left while it exceeds one. After repairing, every start from `left` to `right` gives a valid subarray ending at `right`, so add `right - left + 1` to a running total.

**Complexity.** O(n) time and O(1) extra space, with a `long` total.

```java run
public final class CountAtMostOneZero {
    static long count(int[] nums) {
        long total = 0;
        int left = 0, zeros = 0;
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) zeros++;
            while (zeros > 1) {
                if (nums[left] == 0) zeros--;
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        if (count(new int[] {1, 0, 0, 1}) != 6) throw new AssertionError("example 1");
        if (count(new int[] {1, 1, 1}) != 6) throw new AssertionError("example 2");
        if (count(new int[] {0, 0, 0}) != 3) throw new AssertionError("all zeros");
        if (count(new int[] {0}) != 1) throw new AssertionError("single zero");
    }
}
```

#### Solution: [Vary] Count Subarrays With Sum Below K For Positive Values (Author exercise)
<!-- id: sw-count-sum-below-k -->

**Approach.** Positive values mean that removing the leftmost element can only lower the sum, so validity is monotone under removing a prefix. Repair while the sum is at least `k`, then add the number of starts, `right - left + 1`.

**Complexity.** O(n) time and O(1) extra space. The sum and the count are `long`.

```java run
public final class CountSumBelowK {
    static long count(int[] nums, long k) {
        long total = 0, sum = 0;
        int left = 0;
        for (int right = 0; right < nums.length; right++) {
            sum += nums[right];
            while (left <= right && sum >= k) {
                sum -= nums[left];
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        if (count(new int[] {1, 2, 3}, 4) != 4) throw new AssertionError("example 1");
        if (count(new int[] {5, 6}, 5) != 0) throw new AssertionError("example 2");
        if (count(new int[] {2, 5, 1, 3, 2, 9, 1}, 7) != 10) throw new AssertionError("lesson trace");
    }
}
```

#### Solution: [Boundary] K At The Minimum (Author exercise)
<!-- id: sw-k-at-minimum -->

**Approach.** The same loop, with the guard `left <= right` that lets the window empty. When `k` is at most the smallest element, every right edge removes everything and adds zero. When `k` is huge, the repair loop never runs and every subarray counts. A non-positive `k` also admits nothing, because all sums are positive.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class KAtMinimum {
    static long count(int[] nums, long k) {
        long total = 0, sum = 0;
        int left = 0;
        for (int right = 0; right < nums.length; right++) {
            sum += nums[right];
            while (left <= right && sum >= k) {
                sum -= nums[left];
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        if (count(new int[] {3, 4, 5}, 3) != 0) throw new AssertionError("example 1");
        if (count(new int[] {1, 1, 1, 1}, 1000) != 10) throw new AssertionError("example 2");
        if (count(new int[] {1, 2}, -5) != 0) throw new AssertionError("negative k");
        int[] big = new int[100_000];
        java.util.Arrays.fill(big, 1);
        if (count(big, 1_000_000_000L) != 5_000_050_000L) throw new AssertionError("long total");
    }
}
```

#### Solution: [Recognize] Subarray Product Less Than K (LeetCode 713)
<!-- id: sw-product-less-than-k -->

**Approach.** The aggregate is the product of the window. Because every element is at least one, removing the leftmost element by integer division never increases the product, so the block of valid starts is unbroken. A `k` of at most one admits no subarray, since every product is at least one, so return zero immediately.

**Complexity.** O(n) time and O(1) extra space. The product stays below `k`, at most 10^6, before the next multiplication by at most 1000, so it fits in an `int`, but a `long` is used for safety.

```java run
public final class ProductLessThanK {
    static int numSubarrayProductLessThanK(int[] nums, int k) {
        if (k <= 1) return 0;
        long product = 1;
        int left = 0, total = 0;
        for (int right = 0; right < nums.length; right++) {
            product *= nums[right];
            while (product >= k) {
                product /= nums[left];
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }

    public static void main(String[] args) {
        if (numSubarrayProductLessThanK(new int[] {4, 2, 5, 3}, 30) != 7) throw new AssertionError("example 1");
        if (numSubarrayProductLessThanK(new int[] {1, 2, 3}, 1) != 0) throw new AssertionError("example 2");
        if (numSubarrayProductLessThanK(new int[] {1, 2, 3}, 0) != 0) throw new AssertionError("k zero");
        if (numSubarrayProductLessThanK(new int[] {1, 1, 1}, 2) != 6) throw new AssertionError("all ones");
    }
}
```

#### Solution: [Extend] Number of Substrings Containing All Three Characters (LeetCode 1358)
<!-- id: sw-three-characters -->

**Approach.** A range that covers all three letters keeps covering when it grows to the right. For each right edge, shrink from the left while the window covers, so that `left` becomes the first start that no longer covers. Every start before `left` then gives a covering substring ending at `right`, so add `left`.

**Complexity.** O(n) time and O(1) extra space. The total can reach about 1.25 * 10^9, which fits in an `int` for the stated limit, though a `long` is safer.

```java run
public final class ThreeCharacters {
    static long numberOfSubstrings(String s) {
        int[] count = new int[3];
        long total = 0;
        int left = 0;
        for (int right = 0; right < s.length(); right++) {
            count[s.charAt(right) - 'a']++;
            while (count[0] > 0 && count[1] > 0 && count[2] > 0) {
                count[s.charAt(left) - 'a']--;
                left++;
            }
            total += left;
        }
        return total;
    }

    public static void main(String[] args) {
        if (numberOfSubstrings("cabbac") != 7) throw new AssertionError("example 1");
        if (numberOfSubstrings("bbbcc") != 0) throw new AssertionError("example 2");
        if (numberOfSubstrings("aaacb") != 3) throw new AssertionError("late cover");
        if (numberOfSubstrings("abc") != 1) throw new AssertionError("minimal");
        if (numberOfSubstrings("aaaa") != 0) throw new AssertionError("missing letters");
    }
}
```
