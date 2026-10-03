<!-- solutions-for: 04-minimum-cover-and-deficit-windows -->
### Minimum-Cover And Deficit Windows

#### Solution: [Build] Shortest Segment Containing A And B (Author exercise)
<!-- id: sw-shortest-a-and-b -->

**Approach.** Keep the count of `a` and of `b` inside the window. Once both are positive the window covers, so record its length and then remove the leftmost letter, repeating while the window still covers. Moving `right` forward restores the cover when removal breaks it.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class ShortestAAndB {
    static int shortest(String s) {
        int a = 0, b = 0, left = 0, best = Integer.MAX_VALUE;
        for (int right = 0; right < s.length(); right++) {
            char in = s.charAt(right);
            if (in == 'a') a++;
            else if (in == 'b') b++;
            while (a > 0 && b > 0) {
                best = Math.min(best, right - left + 1);
                char out = s.charAt(left);
                if (out == 'a') a--;
                else if (out == 'b') b--;
                left++;
            }
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }

    public static void main(String[] args) {
        if (shortest("ccabcb") != 2) throw new AssertionError("example 1");
        if (shortest("aaaa") != -1) throw new AssertionError("example 2");
        if (shortest("") != -1) throw new AssertionError("empty");
        if (shortest("ba") != 2) throw new AssertionError("minimal");
    }
}
```

#### Solution: [Vary] Required Multiplicities (Author exercise)
<!-- id: sw-required-multiplicities -->

**Approach.** The window covers when it holds at least two `a` and at least one `b`. Keeping raw counts and testing `a >= 2 && b >= 1` is enough, because extra copies are allowed. The loop records, then removes, while the condition still holds.

**Complexity.** O(n) time and O(1) extra space.

```java run
public final class RequiredMultiplicities {
    static int shortest(String s) {
        int a = 0, b = 0, left = 0, best = Integer.MAX_VALUE;
        for (int right = 0; right < s.length(); right++) {
            char in = s.charAt(right);
            if (in == 'a') a++;
            else if (in == 'b') b++;
            while (a >= 2 && b >= 1) {
                best = Math.min(best, right - left + 1);
                char out = s.charAt(left);
                if (out == 'a') a--;
                else if (out == 'b') b--;
                left++;
            }
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }

    public static void main(String[] args) {
        if (shortest("abcaab") != 3) throw new AssertionError("example 1");
        if (shortest("bcc") != -1) throw new AssertionError("example 2");
        if (shortest("aab") != 3) throw new AssertionError("exact");
        if (shortest("abab") != 3) throw new AssertionError("interleaved");
    }
}
```

#### Solution: [Boundary] No Cover Exists (Author exercise)
<!-- id: sw-no-cover-exists -->

**Approach.** Use the deficit ledger from the lesson, but remember the start and length of the best cover as integers. If the outstanding count never reaches zero during the scan, the best length stays unset and the method returns `[-1, 0]`. An empty requirement is covered by the empty window, so it is answered before the scan.

**Complexity.** O(n + m) time and O(1) extra space for the 128-slot table. No substring is created.

```java run
import java.util.Arrays;

public final class NoCoverExists {
    static int[] shortestCover(String s, String t) {
        if (t.isEmpty()) return new int[] {0, 0};
        int[] owed = new int[128];
        for (int i = 0; i < t.length(); i++) owed[t.charAt(i)]++;
        int outstanding = t.length();
        int left = 0, bestStart = -1, bestLen = Integer.MAX_VALUE;
        for (int right = 0; right < s.length(); right++) {
            char in = s.charAt(right);
            if (owed[in] > 0) outstanding--;
            owed[in]--;
            while (outstanding == 0) {
                if (right - left + 1 < bestLen) {
                    bestLen = right - left + 1;
                    bestStart = left;
                }
                char out = s.charAt(left);
                owed[out]++;
                if (owed[out] > 0) outstanding++;
                left++;
            }
        }
        return bestStart < 0 ? new int[] {-1, 0} : new int[] {bestStart, bestLen};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(shortestCover("xyz", "xz"), new int[] {0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(shortestCover("a", "aa"), new int[] {-1, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(shortestCover("abc", ""), new int[] {0, 0})) throw new AssertionError("empty requirement");
        if (!Arrays.equals(shortestCover("", "a"), new int[] {-1, 0})) throw new AssertionError("empty text");
    }
}
```

#### Solution: [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-minimum-window-substring -->

**Approach.** The deficit ledger counts how many copies of each required character are still owed, and the outstanding count says whether the window covers. While it covers, record the boundaries if they are the shortest so far, then drop the leftmost character. Build the answer once after the scan.

**Complexity.** O(m + n) time, since each index enters and leaves once, and O(1) extra space for the table.

```java run
public final class MinimumWindowSubstring {
    static String minWindow(String s, String t) {
        int[] owed = new int[128];
        for (int i = 0; i < t.length(); i++) owed[t.charAt(i)]++;
        int outstanding = t.length();
        int left = 0, bestStart = 0, bestLen = Integer.MAX_VALUE;
        for (int right = 0; right < s.length(); right++) {
            char in = s.charAt(right);
            if (owed[in] > 0) outstanding--;
            owed[in]--;
            while (outstanding == 0) {
                if (right - left + 1 < bestLen) {
                    bestLen = right - left + 1;
                    bestStart = left;
                }
                char out = s.charAt(left);
                owed[out]++;
                if (owed[out] > 0) outstanding++;
                left++;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLen);
    }

    public static void main(String[] args) {
        if (!minWindow("bbaacb", "abc").equals("acb")) throw new AssertionError("example 1");
        if (!minWindow("bba", "baa").equals("")) throw new AssertionError("example 2");
        if (!minWindow("ADOBECODEBANC", "ABC").equals("BANC")) throw new AssertionError("lesson trace");
        if (!minWindow("a", "a").equals("a")) throw new AssertionError("single");
        if (!minWindow("aab", "aab").equals("aab")) throw new AssertionError("whole string");
        if (!minWindow("bba", "ab").equals("ba")) throw new AssertionError("tight");
    }
}
```

#### Solution: [Extend] Minimum Size Subarray Sum (LeetCode 209)
<!-- id: sw-minimum-size-subarray-sum -->

**Approach.** The window total plays the part of the outstanding count: the window covers when its total is at least `target`. While it covers, record its length and remove the leftmost value. Because every value is positive, removing a value can only lower the total, which makes the shrink safe and the cover monotone.

**Complexity.** O(n) time and O(1) extra space. The total is at most 10^9 plus one value, which fits in an `int`, but a `long` is a safe habit.

```java run
public final class MinimumSizeSubarraySum {
    static int minSubArrayLen(int target, int[] nums) {
        long total = 0;
        int left = 0, best = Integer.MAX_VALUE;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            while (total >= target) {
                best = Math.min(best, right - left + 1);
                total -= nums[left];
                left++;
            }
        }
        return best == Integer.MAX_VALUE ? 0 : best;
    }

    public static void main(String[] args) {
        if (minSubArrayLen(9, new int[] {3, 1, 4, 1, 5, 2}) != 3) throw new AssertionError("example 1");
        if (minSubArrayLen(20, new int[] {3, 1, 4}) != 0) throw new AssertionError("example 2");
        if (minSubArrayLen(4, new int[] {1, 4, 4}) != 1) throw new AssertionError("single element");
        if (minSubArrayLen(15, new int[] {1, 2, 3, 4, 5}) != 5) throw new AssertionError("whole array");
    }
}
```
