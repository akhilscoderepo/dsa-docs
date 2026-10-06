<!-- solutions-for: 09-sliding-window -->
### Solutions For Counting Exactly K

#### Solution: [Build] Exactly One Odd Number (Author exercise)
<!-- id: sw-exactly-one-odd -->

**Approach.**
The helper `atMost` runs one shrinking window. For each `right`, it adds the entering value to the odd count, shrinks `left` while the count exceeds the limit, and adds `right - left + 1` to the total. That sum is the number of ranges with at most the limit of odd numbers. The answer is `atMost(1) - atMost(0)`. The ranges with at most 0 odd numbers lie inside the ranges with at most 1, so the difference leaves exactly the ranges with one odd number. The invariant is that after the shrink loop, every start from `left` to `right` gives a range with at most `limit` odd numbers.

**Complexity.**
- **Time** is O(n), because two passes each move `right` `n` times and `left` at most `n` times.
- **Space** is O(1), because each pass keeps three variables.

```java run
import java.util.Random;

public final class ExactlyOneOdd {
    /**
     * Counts ranges with at most limit odd numbers.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), three variables.
     * Invariant: after the shrink loop, every start in left..right gives a valid range ending at right.
     */
    static long atMost(int[] nums, int limit) {
        // A negative budget admits no range, and the loop below would run left past the array, so return early.
        if (limit < 0) return 0;
        int left = 0, odd = 0;
        // total is a long: it can reach n * (n + 1) / 2.
        long total = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            // The test is != 0, so negative odd numbers count; -3 % 2 is -1 in Java.
            if (nums[right] % 2 != 0) odd++;
            // Shrink: runs while the window holds too many odd numbers.
            while (odd > limit) {
                if (nums[left] % 2 != 0) odd--;
                left++;
            }
            // Every start from left to right gives a valid range that ends at right.
            total += right - left + 1;
        }
        // The count of all ranges with at most limit odd numbers.
        return total;
    }

    /** Answer: ranges with exactly one odd number. */
    static long exactlyOne(int[] nums) {
        // The nested sets differ by exactly the ranges with one odd number.
        return atMost(nums, 1) - atMost(nums, 0);
    }

    /** Oracle: tests every range. */
    static long oracle(int[] a, int k) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            int odd = 0;
            for (int j = i; j < a.length; j++) { if (a[j] % 2 != 0) odd++; if (odd == k) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (exactlyOne(new int[] {2, 1, 3, 4, 1}) != 6) throw new AssertionError("example 1");
        if (exactlyOne(new int[] {4, 6}) != 0) throw new AssertionError("example 2");
        // Java hazard: -3 % 2 is -1, so a test against 1 would miss negative odd numbers.
        if (-3 % 2 != -1) throw new AssertionError("remainder sign");
        if (exactlyOne(new int[] {-3}) != 1) throw new AssertionError("negative odd");
        // Random arrays with negative values agree with the oracle.
        Random rnd = new Random(51);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(11) - 5;
            if (exactlyOne(a) != oracle(a, 1)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Count Number Of Nice Subarrays (LeetCode 1248)
<!-- id: sw-nice-subarrays -->

**Approach.**
The target `k` is a parameter, so the method calls the helper twice, with the limits `k` and `k - 1`. Each call counts the ranges with at most its limit of odd numbers, and the second set lies inside the first. The difference is the number of ranges with exactly `k` odd numbers. The helper is the same shrinking window as in the previous exercise, and each call keeps the invariant that every start from `left` to `right` gives a valid range.

**Complexity.**
- **Time** is O(n), because the method makes two linear passes.
- **Space** is O(1), because each pass keeps three variables.

```java run
import java.util.Random;

public final class NiceSubarrays {
    /**
     * Counts ranges with at most limit odd numbers, and 0 for a negative limit.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), three variables.
     * Invariant: after the shrink loop, nums[left..right] holds at most limit odd numbers.
     */
    static long atMost(int[] nums, int limit) {
        if (limit < 0) return 0;
        int left = 0, odd = 0;
        long total = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] % 2 != 0) odd++;
            // Shrink while the odd count exceeds the limit.
            while (odd > limit) { if (nums[left] % 2 != 0) odd--; left++; }
            // The valid starts for this right number right - left + 1.
            total += right - left + 1;
        }
        return total;
    }

    /** Returns the number of ranges with exactly k odd numbers. */
    static long numberOfSubarrays(int[] nums, int k) {
        // exactly(k) = atMost(k) - atMost(k - 1)
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    /** Oracle: tests every range. */
    static long oracle(int[] a, int k) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            int odd = 0;
            for (int j = i; j < a.length; j++) { if (a[j] % 2 != 0) odd++; if (odd == k) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (numberOfSubarrays(new int[] {2, 1, 3, 4, 1}, 2) != 5) throw new AssertionError("example 1");
        if (numberOfSubarrays(new int[] {2, 4, 6}, 1) != 0) throw new AssertionError("example 2");
        // Random arrays and targets agree with the oracle.
        Random rnd = new Random(52);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(11) - 5;
            int k = 1 + rnd.nextInt(a.length);
            if (numberOfSubarrays(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty At-Most Budget (Author exercise)
<!-- id: sw-empty-budget -->

**Approach.**
For `k = 0`, the identity needs `atMost(-1)`. No range has at most -1 odd numbers, so the helper returns 0 for a negative limit before it runs any loop. Without that line, the shrink loop would try to bring the odd count below 0, which it can never do, and `left` would pass the end of the array and cause an `ArrayIndexOutOfBoundsException`. With the guard, the method returns `atMost(0)`, the number of ranges made of even numbers only. The invariant is that every call counts ranges with at most its limit, and a negative limit counts none.

**Complexity.**
- **Time** is O(n), because at most two linear passes run.
- **Space** is O(1), because each pass keeps three variables.

```java run
import java.util.Random;

public final class EmptyBudget {
    /**
     * Counts ranges with at most limit odd numbers, and 0 for a negative limit.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), three variables.
     * Invariant: after the shrink loop, nums[left..right] holds at most limit odd numbers.
     */
    static long atMost(int[] nums, int limit, boolean guard) {
        // The guard is the line under test: it protects the loop from a negative limit.
        if (guard && limit < 0) return 0;
        int left = 0, odd = 0;
        long total = 0;
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] % 2 != 0) odd++;
            // Without the guard and with limit = -1, this loop runs left past the array end.
            while (odd > limit) { if (nums[left] % 2 != 0) odd--; left++; }
            total += right - left + 1;
        }
        return total;
    }

    /** Returns the number of ranges with exactly k odd numbers, for k >= 0. */
    static long exactly(int[] nums, int k) {
        return atMost(nums, k, true) - atMost(nums, k - 1, true);
    }

    /** Oracle: tests every range. */
    static long oracle(int[] a, int k) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            int odd = 0;
            for (int j = i; j < a.length; j++) { if (a[j] % 2 != 0) odd++; if (odd == k) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (exactly(new int[] {2, 1, 3, 4, 1}, 0) != 2) throw new AssertionError("example 1");
        if (exactly(new int[] {4, 6}, 0) != 3) throw new AssertionError("example 2");
        // Without the guard, a negative limit fails: left runs past the array.
        boolean failed = false;
        try { atMost(new int[] {4, 6}, -1, false); } catch (ArrayIndexOutOfBoundsException e) { failed = true; }
        if (!failed) throw new AssertionError("unguarded call should fail");
        // Random arrays and targets, including 0, agree with the oracle.
        Random rnd = new Random(53);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(11) - 5;
            int k = rnd.nextInt(a.length + 1);
            if (exactly(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Subarrays With K Different Integers (LeetCode 992)
<!-- id: sw-k-different -->

**Approach.**
The property is the number of different integers, and the at-most count uses the count map of the at-most-K lesson. For each `right`, the window shrinks while the map holds more than `limit` keys, and the method adds `right - left + 1` to the total. A key is removed when its count reaches 0, so `size()` equals the number of different values. The answer is `atMost(k) - atMost(k - 1)`. The invariant is that, after the shrink loop, every start from `left` to `right` gives a range with at most `limit` different values.

**Complexity.**
- **Time** is O(n) on average, because two passes each move both indexes forward `n` times with O(1) average map work.
- **Space** is O(k), because the map holds at most `limit + 1` keys.

```java run
import java.util.*;

public final class KDifferent {
    /**
     * Counts ranges with at most limit different values, and 0 for a negative limit.
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(limit), the map holds at most limit + 1 keys.
     * Invariant: counts holds exactly the values of nums[left..right] with positive counts.
     */
    static long atMost(int[] nums, int limit) {
        if (limit < 0) return 0;
        Map<Integer, Integer> counts = new HashMap<>();
        int left = 0;
        long total = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            counts.merge(nums[right], 1, Integer::sum);
            // Shrink while more than limit different values are present.
            while (counts.size() > limit) {
                int gone = nums[left];
                int c = counts.get(gone) - 1;
                // Remove the key at zero so size() stays the distinct count.
                if (c == 0) counts.remove(gone); else counts.put(gone, c);
                left++;
            }
            // Every start from left to right gives a valid range ending at right.
            total += right - left + 1;
        }
        return total;
    }

    /** Returns the number of ranges with exactly k different values. */
    static long exactly(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    /** Oracle: tests every range with a set. */
    static long oracle(int[] a, int k) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            Set<Integer> s = new HashSet<>();
            for (int j = i; j < a.length; j++) { s.add(a[j]); if (s.size() == k) c++; }
        }
        return c;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (exactly(new int[] {2, 1, 2, 3, 1}, 2) != 5) throw new AssertionError("example 1");
        if (exactly(new int[] {3, 3, 3}, 2) != 0) throw new AssertionError("example 2");
        // Random arrays and targets agree with the oracle.
        Random rnd = new Random(54);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(4);
            int k = 1 + rnd.nextInt(a.length);
            if (exactly(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```
