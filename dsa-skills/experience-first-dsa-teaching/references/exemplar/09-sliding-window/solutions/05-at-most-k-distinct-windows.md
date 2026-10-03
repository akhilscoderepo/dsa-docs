<!-- solutions-for: 05-at-most-k-distinct-windows -->
### At-Most-K Distinct Windows

#### Solution: [Build] Longest Segment With One Distinct Value (Author exercise)
<!-- id: sw-one-distinct-value -->

**Approach.** Keep the window as `left..right`, one active value and its count. When a different value arrives the old run ends, so the window restarts at `right` with a count of one. Otherwise the count grows. The best length is the largest count seen.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class OneDistinctValue {
    static int longestRun(int[] nums) {
        int best = 0, count = 0;
        for (int right = 0; right < nums.length; right++) {
            if (right > 0 && nums[right] == nums[right - 1]) count++;
            else count = 1;
            best = Math.max(best, count);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestRun(new int[] {4, 4, 2, 2, 2, 4}) != 3) throw new AssertionError("example 1");
        if (longestRun(new int[0]) != 0) throw new AssertionError("example 2");
        if (longestRun(new int[] {7}) != 1) throw new AssertionError("single");
        if (longestRun(new int[] {1, 2, 3}) != 1) throw new AssertionError("all different");
    }
}
```

#### Solution: [Vary] Fruit Into Baskets (LeetCode 904)
<!-- id: sw-fruit-into-baskets -->

**Approach.** This is the longest window with at most two distinct values. Keep a count per fruit type. When a third type arrives, drop trees from the left, decrementing counts and tracking the number of types still present, until only two remain.

**Complexity.** O(n) time and O(n) extra space for the count table, since the types are bounded by the array length. The table never holds more than three non-zero entries.

```java run
public final class FruitIntoBaskets {
    static int totalFruit(int[] fruits) {
        int[] count = new int[fruits.length + 1];
        int types = 0, left = 0, best = 0;
        for (int right = 0; right < fruits.length; right++) {
            if (count[fruits[right]]++ == 0) types++;
            while (types > 2) {
                if (--count[fruits[left]] == 0) types--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (totalFruit(new int[] {4, 4, 5, 4, 6, 6}) != 4) throw new AssertionError("example 1");
        if (totalFruit(new int[] {0, 3, 2, 3, 3, 2}) != 5) throw new AssertionError("example 2");
        if (totalFruit(new int[] {0, 1, 2, 2}) != 3) throw new AssertionError("third type");
        if (totalFruit(new int[] {0}) != 1) throw new AssertionError("single tree");
    }
}
```

#### Solution: [Boundary] K Is Zero (Author exercise)
<!-- id: sw-k-is-zero -->

**Approach.** Return zero immediately when `k` is zero, since no value is allowed. Otherwise use a count map and repair from the left whenever the number of keys exceeds `k`, removing a key when its count reaches zero. A budget larger than the distinct count never enters the repair loop.

**Complexity.** O(n) time and O(min(n, k)) extra space.

```java run
import java.util.HashMap;
import java.util.Map;

public final class KIsZero {
    static int longestAtMostK(int[] nums, int k) {
        if (k <= 0) return 0;
        Map<Integer, Integer> count = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < nums.length; right++) {
            count.merge(nums[right], 1, Integer::sum);
            while (count.size() > k) {
                int out = nums[left];
                if (count.merge(out, -1, Integer::sum) == 0) count.remove(out);
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestAtMostK(new int[] {1, 2}, 0) != 0) throw new AssertionError("example 1");
        if (longestAtMostK(new int[] {5, 5, 5}, 3) != 3) throw new AssertionError("example 2");
        if (longestAtMostK(new int[0], 2) != 0) throw new AssertionError("empty");
        if (longestAtMostK(new int[] {1, 2, 1, 3, 3, 2, 2, 4}, 2) != 4) throw new AssertionError("lesson trace");
    }
}
```

#### Solution: [Recognize] Longest Substring With At Most K Distinct Characters (Author exercise)
<!-- id: sw-at-most-k-characters -->

**Approach.** The characters are ASCII, so a table of 128 counts replaces the map. A separate integer counts the distinct characters, rising when a count goes from zero to one and falling when it goes from one to zero. Repair from the left while that integer exceeds `k`.

**Complexity.** O(n) time and O(1) extra space for the fixed table.

```java run
public final class AtMostKCharacters {
    static int lengthOfLongestSubstringKDistinct(String s, int k) {
        if (k <= 0) return 0;
        int[] count = new int[128];
        int distinct = 0, left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            if (count[s.charAt(right)]++ == 0) distinct++;
            while (distinct > k) {
                if (--count[s.charAt(left)] == 0) distinct--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        if (lengthOfLongestSubstringKDistinct("eceba", 2) != 3) throw new AssertionError("example 1");
        if (lengthOfLongestSubstringKDistinct("aa", 1) != 2) throw new AssertionError("example 2");
        if (lengthOfLongestSubstringKDistinct("abc", 0) != 0) throw new AssertionError("zero budget");
        if (lengthOfLongestSubstringKDistinct("", 3) != 0) throw new AssertionError("empty");
    }
}
```
