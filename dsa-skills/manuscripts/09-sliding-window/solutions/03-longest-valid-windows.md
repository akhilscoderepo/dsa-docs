<!-- solutions-for: 09-longest-valid-windows -->
### Longest-Valid Windows

#### Solution: [Build] Longest Binary Run With One Zero (Author exercise)
<!-- id: sw-one-zero-run -->

**Approach.** Walk `right` across the array and count the zeros in the window. When the count reaches two, advance `left` until the zero that is leaving has been passed, then record the length. The check compares with a quadratic scan of every stretch on random binary arrays, confirms that the input is left untouched, and counts how many times `left` moves to show that it never exceeds the array length.

**Complexity.** One pass with at most 2n pointer moves, so linear time, and constant extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OneZeroRun {
    static int leftMoves;

    static int longest(int[] bits) {
        int left = 0, zeros = 0, best = 0;
        for (int right = 0; right < bits.length; right++) {
            if (bits[right] == 0) zeros++;
            while (zeros > 1) {
                if (bits[left] == 0) zeros--;
                left++;
                leftMoves++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
    static int oracle(int[] bits) {
        int best = 0;
        for (int i = 0; i < bits.length; i++) {
            int z = 0;
            for (int j = i; j < bits.length; j++) {
                if (bits[j] == 0) z++;
                if (z <= 1) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longest(new int[] {1, 0, 1, 1, 0, 1, 1, 1}) != 6) throw new AssertionError("example 1");
        if (longest(new int[] {0, 0, 0}) != 1) throw new AssertionError("example 2");
        if (longest(new int[0]) != 0) throw new AssertionError("empty");
        if (longest(new int[] {1}) != 1 || longest(new int[] {0}) != 1) throw new AssertionError("single");
        int[] ones = new int[1000];
        Arrays.fill(ones, 1);
        leftMoves = 0;
        if (longest(ones) != 1000 || leftMoves != 0) throw new AssertionError("all ones");
        Random rnd = new Random(901);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(16);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3) == 0 ? 0 : 1;
            int[] copy = a.clone();
            leftMoves = 0;
            int got = longest(a);
            if (got != oracle(a)) throw new AssertionError("differs on " + Arrays.toString(a));
            if (!Arrays.equals(a, copy)) throw new AssertionError("input was modified");
            if (leftMoves > n) throw new AssertionError("left moved more than n times");
        }
    }
}
```

#### Solution: [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-no-repeat-substring -->

**Approach.** Keep a table of how many times each character occurs in the window. After adding the character at `right`, run a `while` loop that drops characters from the left as long as the new character's count is above one. The check includes a repeat that needs several removals in one round and counts the removals to show they never exceed the length. The oracle tests every substring with a set.

**Complexity.** Each character is added once and removed at most once, giving linear time with one 128-slot table.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class NoRepeatSubstring {
    static int removals;

    static int longest(String s) {
        int[] count = new int[128];
        int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            count[c]++;
            while (count[c] > 1) {
                count[s.charAt(left)]--;
                left++;
                removals++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }
    static int oracle(String s) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            Set<Character> seen = new HashSet<>();
            for (int j = i; j < s.length(); j++) {
                if (!seen.add(s.charAt(j))) break;
                best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longest("qrsqtuvr") != 6) throw new AssertionError("example 1");
        if (longest("zzzz") != 1) throw new AssertionError("example 2");
        if (longest("") != 0) throw new AssertionError("empty");
        if (longest("x") != 1) throw new AssertionError("single");
        if (longest("abcdefa") != 6) throw new AssertionError("late repeat of first letter");
        if (longest("abcdbfg") != 5) throw new AssertionError("repeat needing several removals");
        StringBuilder all = new StringBuilder();
        for (char c = 0; c < 128; c++) all.append(c);
        if (longest(all.toString()) != 128) throw new AssertionError("whole alphabet");
        Random rnd = new Random(902);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            int alpha = 1 + rnd.nextInt(6);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String s = sb.toString();
            removals = 0;
            if (longest(s) != oracle(s)) throw new AssertionError("differs on " + s);
            if (removals > n) throw new AssertionError("more removals than characters");
        }
    }
}
```

#### Solution: [Boundary] Violation At Both Ends (Author exercise)
<!-- id: sw-violation-both-ends -->

**Approach.** Keep a `long` sum of the window. After adding the element at `right`, remove from the left while the sum exceeds the limit and `left <= right`, counting how many removals this one arrival caused. If the arriving element is too heavy by itself, the loop removes the whole window including that element and `left` ends at `right + 1`, so the length recorded is zero. The largest removal count over all arrivals is the second answer. The checks include two elements equal to `Integer.MAX_VALUE`, whose sum would be negative if held in an `int`, and a test that no element is removed twice.

**Complexity.** Linear time, because the total of all removals cannot exceed n, and constant extra space.

```java run
import java.util.Random;

public final class ViolationBothEnds {
    static int totalRemoved;

    static int[] solve(int[] v, long limit) {
        long sum = 0;
        int left = 0, best = 0, worst = 0;
        for (int right = 0; right < v.length; right++) {
            sum += v[right];
            int removed = 0;
            while (left <= right && sum > limit) {
                sum -= v[left++];
                removed++;
            }
            totalRemoved += removed;
            worst = Math.max(worst, removed);
            best = Math.max(best, right - left + 1);
        }
        return new int[] {best, worst};
    }
    static int[] oracle(int[] v, long limit) {
        int best = 0;
        for (int i = 0; i < v.length; i++) {
            long s = 0;
            for (int j = i; j < v.length; j++) {
                s += v[j];
                if (s <= limit) best = Math.max(best, j - i + 1);
            }
        }
        // the removal count is replayed with an independent, simpler simulation
        int worst = 0;
        int start = 0;
        for (int right = 0; right < v.length; right++) {
            int before = start;
            while (start <= right && windowSum(v, start, right) > limit) start++;
            worst = Math.max(worst, start - before);
        }
        return new int[] {best, worst};
    }
    static long windowSum(int[] v, int from, int to) {
        long s = 0;
        for (int i = from; i <= to; i++) s += v[i];
        return s;
    }

    public static void main(String[] args) {
        int[] r1 = solve(new int[] {2, 3, 1, 9, 2, 2}, 6);
        if (r1[0] != 3 || r1[1] != 4) throw new AssertionError("example 1");
        int[] r2 = solve(new int[] {7, 1, 1}, 5);
        if (r2[0] != 2 || r2[1] != 1) throw new AssertionError("example 2");
        int[] e = solve(new int[0], 10);
        if (e[0] != 0 || e[1] != 0) throw new AssertionError("empty");
        int[] big = solve(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, 4000000000000L);
        if (big[0] != 2) throw new AssertionError("long sum should keep both elements");
        int wrapped = Integer.MAX_VALUE + Integer.MAX_VALUE;
        if (wrapped >= 0) throw new AssertionError("an int sum would overflow here");
        int[] zeroLimit = solve(new int[] {1, 1, 1}, 0);
        if (zeroLimit[0] != 0 || zeroLimit[1] != 1) throw new AssertionError("limit zero");
        Random rnd = new Random(903);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(9);
            long limit = rnd.nextInt(25);
            totalRemoved = 0;
            int[] got = solve(a, limit);
            int[] want = oracle(a, limit);
            if (got[0] != want[0] || got[1] != want[1]) throw new AssertionError("differs on limit " + limit);
            if (totalRemoved > n) throw new AssertionError("an element left twice");
        }
    }
}
```

#### Solution: [Recognize] Max Consecutive Ones III (LeetCode 1004)
<!-- id: sw-max-consecutive-ones-iii -->

**Approach.** Treat the budget as a number that falls each time a zero enters the window. When the budget goes below zero, advance `left`, and give one unit back whenever the element leaving is a zero. The window then holds at most `k` zeros and the best length is recorded each round. The array is only read, which the check confirms, and the oracle tries every stretch and counts zeros directly. The cases `k = 0` and `k` equal to the array length are asserted by name.

**Complexity.** One pass in which each index moves each pointer at most once, so O(n) time and O(1) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MaxOnesBudget {
    static int longestOnes(int[] nums, int k) {
        int budget = k, left = 0, best = 0;
        for (int right = 0; right < nums.length; right++) {
            if (nums[right] == 0) budget--;
            while (budget < 0) {
                if (nums[left] == 0) budget++;
                left++;
            }
            if (right - left + 1 > best) best = right - left + 1;
        }
        return best;
    }
    static int oracle(int[] nums, int k) {
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            for (int j = i; j < nums.length; j++) {
                int zeros = 0;
                for (int x = i; x <= j; x++) if (nums[x] == 0) zeros++;
                if (zeros <= k) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestOnes(new int[] {0, 1, 1, 0, 0, 1, 0, 1}, 2) != 5) throw new AssertionError("example 1");
        if (longestOnes(new int[] {1, 1, 1}, 0) != 3) throw new AssertionError("example 2");
        if (longestOnes(new int[] {0, 0, 0, 0}, 0) != 0) throw new AssertionError("k zero, all zeros");
        if (longestOnes(new int[] {0, 0, 0, 0}, 4) != 4) throw new AssertionError("k covers everything");
        if (longestOnes(new int[] {0}, 1) != 1) throw new AssertionError("single zero");
        Random rnd = new Random(904);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            int k = rnd.nextInt(n + 1);
            int[] copy = a.clone();
            if (longestOnes(a, k) != oracle(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
            if (!Arrays.equals(a, copy)) throw new AssertionError("input was modified");
        }
    }
}
```
