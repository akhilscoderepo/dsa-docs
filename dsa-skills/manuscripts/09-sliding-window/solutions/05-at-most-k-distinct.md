<!-- solutions-for: 09-sliding-window -->
### Solutions For At-Most-K Windows

#### Solution: [Build] Longest Segment With One Distinct Value (Author exercise)
<!-- id: sw-one-distinct -->

**Approach.**
The window holds one active value, `key`, and its count `count`. When a value equal to `key` enters, the count rises by one. When a different value enters, the window holds two distinct values, so a `while` loop removes values from the left until the count of the old key reaches 0. The loop runs `count` times, and `left` then equals `right`. The entering value becomes the new key with count 1. The invariant is that the window `nums[left..right]` holds only `key`, `count` times.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps a key, a count and two indexes.

```java run
import java.util.Random;

public final class OneDistinct {
    /**
     * Returns the longest block of equal values.
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(1), one key and one count.
     * Invariant: nums[left..right] holds only key, and count equals right - left + 1.
     */
    static int longest(int[] nums) {
        // Empty input has no block.
        if (nums.length == 0) return 0;
        int left = 0, best = 0, key = nums[0], count = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            // A different value breaks validity, so the old block must leave first.
            if (nums[right] != key) {
                // Shrink: removes the old key's copies one by one; the total over the call is at most n steps.
                while (count > 0) { count--; left++; }
                // The entering value starts a new block.
                key = nums[right];
            }
            // The entering value joins the window.
            count++;
            // The window is valid here, so its length is a candidate.
            best = Math.max(best, right - left + 1);
        }
        // The longest block recorded.
        return best;
    }

    /** Oracle: tests every block. */
    static int oracle(int[] a) {
        int best = 0;
        for (int i = 0; i < a.length; i++) for (int j = i; j < a.length; j++) {
            boolean same = true;
            for (int x = i; x <= j; x++) if (a[x] != a[i]) same = false;
            if (same) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2, and the empty array.
        if (longest(new int[] {5, 5, 2, 2, 2, 7}) != 3) throw new AssertionError("example 1");
        if (longest(new int[] {9}) != 1) throw new AssertionError("example 2");
        if (longest(new int[0]) != 0) throw new AssertionError("empty");
        // Random arrays agree with the oracle.
        Random rnd = new Random(41);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3);
            if (longest(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Fruit Into Baskets (LeetCode 904)
<!-- id: sw-fruit-baskets -->

**Approach.**
The method keeps a map from fruit type to its count in the window. An entering type raises its count. While the map holds three keys, the loop removes the type at `left`, lowers its count, and deletes the key when the count reaches 0. The deletion matters, because `size()` must equal the number of types in the window. After the loop at most two types remain, so the method records the length. The invariant is that every key of the map has a positive count and the keys are exactly the types in the window.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once, with O(1) average cost per map operation.
- **Space** is O(1), because the map holds at most three keys.

```java run
import java.util.*;

public final class FruitBaskets {
    /**
     * Returns the longest block with at most two different values.
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(1), the map holds at most three keys.
     * Invariant: counts has exactly the values of fruits[left..right], each with a positive count.
     */
    static int totalFruit(int[] fruits) {
        Map<Integer, Integer> counts = new HashMap<>();
        int left = 0, best = 0;
        // Expand: the type at right enters.
        for (int right = 0; right < fruits.length; right++) {
            // merge adds 1 to an existing count or creates the key with count 1.
            counts.merge(fruits[right], 1, Integer::sum);
            // Shrink: runs while three types are present; each pass removes one index.
            while (counts.size() > 2) {
                int gone = fruits[left];
                int c = counts.get(gone) - 1;
                // Remove the key at zero, or size() would overstate the distinct count.
                if (c == 0) counts.remove(gone); else counts.put(gone, c);
                left++;
            }
            // The window is valid, so its length is a candidate.
            best = Math.max(best, right - left + 1);
        }
        // The longest valid length.
        return best;
    }

    /** Oracle: tests every block with a set. */
    static int oracle(int[] a) {
        int best = 0;
        for (int i = 0; i < a.length; i++) for (int j = i; j < a.length; j++) {
            Set<Integer> s = new HashSet<>();
            for (int x = i; x <= j; x++) s.add(a[x]);
            if (s.size() <= 2) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (totalFruit(new int[] {1, 2, 1, 3, 3, 2, 2}) != 4) throw new AssertionError("example 1");
        if (totalFruit(new int[] {4, 4, 4}) != 3) throw new AssertionError("example 2");
        // Random arrays agree with the oracle.
        Random rnd = new Random(42);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            if (totalFruit(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] K Is Zero (Author exercise)
<!-- id: sw-k-zero -->

**Approach.**
With `k = 0`, any entering value raises the distinct count to 1, which exceeds the limit. The shrink loop then removes values from the left. It removes the entering value itself, because the window holds nothing else after the loop begins to empty it. The loop ends when the map is empty, and `left` equals `right + 1`. The length `right - left + 1` is 0. Counts never drop below 0, because the method decrements a count only for an index that is inside the window. The invariant is that `left <= right + 1` after every loop.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(min(n, k)), because the map holds at most `k + 1` keys.

```java run
import java.util.*;

public final class KIsZero {
    /**
     * Returns the longest block with at most k different values, where k may be 0.
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(min(n, k)), the map holds at most k + 1 keys.
     * Invariant: left <= right + 1, and counts holds exactly the values of nums[left..right].
     */
    static int longest(int[] nums, int k) {
        Map<Integer, Integer> counts = new HashMap<>();
        int left = 0, best = 0;
        // Expand: one value enters per iteration.
        for (int right = 0; right < nums.length; right++) {
            counts.merge(nums[right], 1, Integer::sum);
            // Shrink: with k = 0 this loop empties the window, and left ends at right + 1.
            while (counts.size() > k) {
                int gone = nums[left];
                int c = counts.get(gone) - 1;
                // The count is read from an index inside the window, so c is never negative.
                if (c == 0) counts.remove(gone); else counts.put(gone, c);
                left++;
            }
            // An empty window has length right - (right + 1) + 1 = 0.
            best = Math.max(best, right - left + 1);
        }
        // Return the best length, which is 0 when k = 0.
        return best;
    }

    /** Oracle: tests every block with a set. */
    static int oracle(int[] a, int k) {
        int best = 0;
        for (int i = 0; i < a.length; i++) for (int j = i; j < a.length; j++) {
            Set<Integer> s = new HashSet<>();
            for (int x = i; x <= j; x++) s.add(a[x]);
            if (s.size() <= k) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement, plus an empty array.
        if (longest(new int[] {4, 4}, 0) != 0) throw new AssertionError("example 1");
        if (longest(new int[] {1, 2, 2}, 1) != 2) throw new AssertionError("example 2");
        if (longest(new int[0], 0) != 0) throw new AssertionError("empty");
        // Random arrays and limits, including 0, agree with the oracle.
        Random rnd = new Random(43);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            int k = rnd.nextInt(5);
            if (longest(a, k) != oracle(a, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Longest Substring With At Most K Distinct Characters (Author exercise)
<!-- id: sw-at-most-k-chars -->

**Approach.**
The values are ASCII characters, so a count array of 128 entries replaces the map, and a separate integer `distinct` replaces `size()`. An entering character raises `distinct` when its count was 0. A leaving character lowers `distinct` when its count becomes 0. The shrink loop runs while `distinct > k`, and the method records the length after it. The invariant is that `distinct` equals the number of array entries with a positive count.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the count array has 128 entries.

```java run
import java.util.*;

public final class AtMostKChars {
    /**
     * Returns the length of the longest substring with at most k different characters (ASCII).
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(1), a table of 128 counters.
     * Invariant: distinct equals the number of positive entries of cnt.
     */
    static int longest(String s, int k) {
        int[] cnt = new int[128];
        int distinct = 0, left = 0, best = 0;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            // A character whose count was 0 is new to the window.
            if (cnt[s.charAt(right)]++ == 0) distinct++;
            // Shrink: runs while the window holds more than k kinds of characters.
            while (distinct > k) {
                // A character whose count falls to 0 leaves the window completely.
                if (--cnt[s.charAt(left)] == 0) distinct--;
                left++;
            }
            // The window is valid, so its length is a candidate.
            best = Math.max(best, right - left + 1);
        }
        // The longest valid length.
        return best;
    }

    /** Oracle: tests every substring with a set. */
    static int oracle(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            Set<Character> set = new HashSet<>();
            for (int x = i; x <= j; x++) set.add(s.charAt(x));
            if (set.size() <= k) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (longest("eceba", 2) != 3) throw new AssertionError("example 1");
        if (longest("aaabbb", 1) != 3) throw new AssertionError("example 2");
        // Random strings and limits agree with the oracle.
        Random rnd = new Random(44);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(14); i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            int k = rnd.nextInt(5);
            if (longest(sb.toString(), k) != oracle(sb.toString(), k)) throw new AssertionError("random " + t);
        }
    }
}
```
