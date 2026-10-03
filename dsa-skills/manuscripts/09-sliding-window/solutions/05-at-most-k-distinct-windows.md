<!-- solutions-for: 09-at-most-k-distinct-windows -->
### At-Most-K Distinct Windows

#### Solution: [Build] Longest Segment With One Distinct Value (Author exercise)
<!-- id: sw-one-kind-run -->

**Approach.** Walk once, holding the current key and the length of the run that ends at the current position. If the value equals the key, the run grows. Otherwise the key becomes the new value and the run restarts at one. The answer is the largest run seen. No map is needed because a budget of one means at most one kind is inside. The check compares with a quadratic scan on random arrays with many repeats, covers the empty array, a single element and an all-equal array, asserts the input is not changed, and counts that the method reads each element exactly once.

**Complexity.** One reading per element, so linear time, with two extra variables.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OneKindRun {
    static int reads;

    static int longestRun(int[] nums) {
        int best = 0, run = 0, key = 0;
        for (int i = 0; i < nums.length; i++) {
            int v = nums[i];
            reads++;
            if (run > 0 && v == key) run++;
            else { key = v; run = 1; }
            best = Math.max(best, run);
        }
        return best;
    }

    static int brute(int[] a) {
        int best = 0;
        for (int s = 0; s < a.length; s++) {
            int e = s;
            while (e < a.length && a[e] == a[s]) e++;
            best = Math.max(best, e - s);
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestRun(new int[] {4, 4, 9, 9, 9, 4}) != 3) throw new AssertionError("example 1");
        if (longestRun(new int[0]) != 0) throw new AssertionError("example 2");
        if (longestRun(new int[] {Integer.MIN_VALUE}) != 1) throw new AssertionError("single");
        int[] same = new int[1000];
        Arrays.fill(same, Integer.MAX_VALUE);
        reads = 0;
        if (longestRun(same) != 1000) throw new AssertionError("all equal");
        if (reads != 1000) throw new AssertionError("reads " + reads);
        Random rnd = new Random(905);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3) - 1;
            int[] copy = a.clone();
            if (longestRun(a) != brute(a)) throw new AssertionError("differs on " + Arrays.toString(a));
            if (!Arrays.equals(a, copy)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Vary] Fruit Into Baskets (LeetCode 904)
<!-- id: sw-fruit-baskets -->

**Approach.** This is the general window with a budget of two. Add the fruit at `right` to the count map. While the map holds three types, remove the fruit at `left`, subtract one from its count, delete the key when the count reaches zero, and advance `left`. After the shrink, the window holds at most two types, so its length is a candidate. The check compares with a cubic brute force that tests every subarray with a set, asserts that the map size equals the number of different values in the window after each step, and that no key ever holds a zero count. It also counts map updates to show that at most two happen per position.

**Complexity.** Each index is added once and removed at most once, so at most 2n map updates, which gives expected O(n) time and O(1) space because the map never exceeds three keys.

```java run
import java.util.*;

public final class FruitBaskets {
    static int updates;

    static int pick(int[] fruits) {
        Map<Integer, Integer> basket = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < fruits.length; right++) {
            basket.merge(fruits[right], 1, Integer::sum);
            updates++;
            while (basket.size() > 2) {
                int drop = fruits[left++];
                updates++;
                if (basket.merge(drop, -1, Integer::sum) == 0) basket.remove(drop);
            }
            Set<Integer> real = new HashSet<>();
            for (int i = left; i <= right; i++) real.add(fruits[i]);
            if (real.size() != basket.size()) throw new AssertionError("map size drifted");
            for (int c : basket.values()) if (c <= 0) throw new AssertionError("non-positive count");
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int brute(int[] a) {
        int best = 0;
        for (int s = 0; s < a.length; s++)
            for (int e = s; e < a.length; e++) {
                Set<Integer> kinds = new HashSet<>();
                for (int i = s; i <= e; i++) kinds.add(a[i]);
                if (kinds.size() <= 2) best = Math.max(best, e - s + 1);
            }
        return best;
    }

    public static void main(String[] args) {
        if (pick(new int[] {5, 8, 5, 8, 3, 3, 8}) != 4) throw new AssertionError("example 1");
        if (pick(new int[] {2, 2, 2}) != 3) throw new AssertionError("example 2");
        if (pick(new int[] {7}) != 1) throw new AssertionError("single");
        if (pick(new int[] {1, 2, 3, 4}) != 2) throw new AssertionError("all different");
        Random rnd = new Random(906);
        for (int t = 0; t < 2500; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            updates = 0;
            int got = pick(a);
            if (got != brute(a)) throw new AssertionError("differs on " + Arrays.toString(a));
            if (updates > 2 * n) throw new AssertionError("too many updates");
        }
    }
}
```

#### Solution: [Boundary] K Is Zero (Author exercise)
<!-- id: sw-k-zero -->

**Approach.** Use the general at-most-k loop without any special case for zero. After the first addition the map holds one key, which is over a budget of zero, so the shrink loop removes from the left until the map is empty, leaving `left` equal to `right + 1` and the length zero. Since each removal is matched by an earlier addition, no count can go negative, and `left` stops at `right + 1` because the map is empty exactly then. The check asserts both facts on every step, including that a large `k` returns the whole array, and compares with a brute force on random arrays for k from zero to five.

**Complexity.** Single pass with at most 2n map updates, expected O(n) time and O(min(n, k)) extra space.

```java run
import java.util.*;

public final class KIsZero {
    static int longest(int[] nums, int k) {
        Map<Integer, Integer> tally = new HashMap<>();
        int left = 0, best = 0;
        for (int right = 0; right < nums.length; right++) {
            tally.merge(nums[right], 1, Integer::sum);
            while (tally.size() > k) {
                int out = nums[left++];
                if (tally.merge(out, -1, Integer::sum) == 0) tally.remove(out);
            }
            if (left > right + 1) throw new AssertionError("left passed right + 1");
            for (int c : tally.values()) if (c <= 0) throw new AssertionError("bad count");
            if (k == 0 && left != right + 1) throw new AssertionError("k = 0 must empty the window");
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int brute(int[] a, int k) {
        int best = 0;
        for (int s = 0; s < a.length; s++)
            for (int e = s; e < a.length; e++) {
                Set<Integer> kinds = new HashSet<>();
                for (int i = s; i <= e; i++) kinds.add(a[i]);
                if (kinds.size() <= k) best = Math.max(best, e - s + 1);
            }
        return best;
    }

    public static void main(String[] args) {
        if (longest(new int[] {3, 1, 3}, 0) != 0) throw new AssertionError("example 1");
        if (longest(new int[] {3, 1, 3}, 5) != 3) throw new AssertionError("example 2");
        if (longest(new int[0], 0) != 0) throw new AssertionError("empty");
        if (longest(new int[] {9}, 1) != 1) throw new AssertionError("one element");
        if (longest(new int[] {6, 6, 6, 6}, 0) != 0) throw new AssertionError("all equal, k = 0");
        if (longest(new int[] {Integer.MAX_VALUE, Integer.MIN_VALUE}, 2) != 2) throw new AssertionError("extremes");
        Random rnd = new Random(907);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) - 2;
            int k = rnd.nextInt(6);
            if (longest(a, k) != brute(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
        }
    }
}
```

#### Solution: [Recognize] Longest Substring With At Most K Distinct Characters (Author exercise)
<!-- id: sw-k-distinct-chars -->

**Approach.** The characters come from a fixed alphabet of 26 letters, so a count array replaces the map, and an integer `kinds` replaces `size()`. The counter goes up when a count rises from zero to one and goes down when it falls from one to zero, and those are the only two moments it changes. Shrinking runs while `kinds` exceeds `k`. The check verifies that `kinds` equals the number of non-zero cells after every step, compares with a brute force over all substrings on random strings over a small alphabet, and covers empty strings, k equal to zero, and k at least the alphabet size.

**Complexity.** Linear time with one array of 26 cells, so constant extra space.

```java run
import java.util.*;

public final class KDistinctChars {
    static int longest(String s, int k) {
        int[] seen = new int[26];
        int kinds = 0, left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            if (seen[s.charAt(right) - 'a']++ == 0) kinds++;
            while (kinds > k) {
                if (--seen[s.charAt(left++) - 'a'] == 0) kinds--;
            }
            int nonZero = 0;
            for (int c : seen) if (c > 0) nonZero++;
            if (nonZero != kinds) throw new AssertionError("kinds drifted");
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int brute(String s, int k) {
        int best = 0;
        for (int a = 0; a < s.length(); a++)
            for (int b = a; b < s.length(); b++) {
                Set<Character> kinds = new HashSet<>();
                for (int i = a; i <= b; i++) kinds.add(s.charAt(i));
                if (kinds.size() <= k) best = Math.max(best, b - a + 1);
            }
        return best;
    }

    public static void main(String[] args) {
        if (longest("aabbcbbd", 2) != 5) throw new AssertionError("example 1");
        if (longest("zzzz", 1) != 4) throw new AssertionError("example 2");
        if (longest("", 3) != 0) throw new AssertionError("empty");
        if (longest("abc", 0) != 0) throw new AssertionError("k = 0");
        if (longest("abcdefghijklmnopqrstuvwxyz", 26) != 26) throw new AssertionError("whole alphabet");
        Random rnd = new Random(908);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(4)));
            String s = sb.toString();
            int k = rnd.nextInt(5);
            if (longest(s, k) != brute(s, k)) throw new AssertionError("differs on " + s + " k " + k);
        }
    }
}
```
