<!-- solutions-for: 20-greedy -->
### Greedy And Monotonic Stack

#### Solution: [Build] Remove K Digits (LeetCode 402)
<!-- id: gc-remove-k-digits -->

**Approach.** Keep a stack of digits. For each new digit, pop the top while the budget `k` is positive and the top is strictly larger than the newcomer, spending one removal per pop, and then push the newcomer. Strict comparison keeps equal digits in place. After the loop, any unspent budget is taken from the tail, because the surviving stack is non-decreasing and its last digits are the largest. Leading zeros are stripped last, and an empty result prints as "0". The assertions check both examples, the extremes of `k`, and random digit strings against the exhaustive trial that builds every outcome and compares them numerically.

**Complexity.** Every digit is pushed once and popped at most once, so the time is O(n) with an O(n) stack.

```java run
import java.util.Random;

public final class RemoveKDigits {
    static String removeKDigits(String num, int k) {
        StringBuilder stack = new StringBuilder();
        for (char c : num.toCharArray()) {
            while (k > 0 && stack.length() > 0 && stack.charAt(stack.length() - 1) > c) {
                stack.setLength(stack.length() - 1);
                k--;
            }
            stack.append(c);
        }
        stack.setLength(stack.length() - k);
        int start = 0;
        while (start < stack.length() - 1 && stack.charAt(start) == '0') start++;
        return stack.length() == 0 ? "0" : stack.substring(start);
    }

    static boolean numericLess(String a, String b) {
        String x = a.replaceFirst("^0+", ""), y = b.replaceFirst("^0+", "");
        return x.length() != y.length() ? x.length() < y.length() : x.compareTo(y) < 0;
    }

    static String trial(String s, int i, int drop, String kept) {
        if (i == s.length()) return drop == 0 ? kept : null;
        String dropped = drop > 0 ? trial(s, i + 1, drop - 1, kept) : null;
        String retained = trial(s, i + 1, drop, kept + s.charAt(i));
        if (dropped == null) return retained;
        if (retained == null) return dropped;
        return numericLess(dropped, retained) ? dropped : retained;
    }

    static String clean(String s) {
        String t = s.replaceFirst("^0+", "");
        return t.isEmpty() ? "0" : t;
    }

    public static void main(String[] args) {
        if (!removeKDigits("52913", 2).equals("213")) throw new AssertionError("example 1");
        if (!removeKDigits("1002003", 2).equals("3")) throw new AssertionError("example 2");
        if (!removeKDigits("9", 1).equals("0")) throw new AssertionError("everything removed");
        if (!removeKDigits("112", 1).equals("11")) throw new AssertionError("leftover budget comes off the tail");
        if (!removeKDigits("10200", 1).equals("200")) throw new AssertionError("a leading zero after the pop");
        if (!removeKDigits("4321", 0).equals("4321")) throw new AssertionError("no removals");
        if (!removeKDigits("000", 1).equals("0")) throw new AssertionError("all zeros");

        Random rnd = new Random(2801);
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(10);
            StringBuilder sb = new StringBuilder();
            int alpha = 2 + rnd.nextInt(8);
            for (int i = 0; i < n; i++) sb.append((char) ('0' + rnd.nextInt(alpha)));
            String s = sb.toString();
            int k = rnd.nextInt(n + 1);
            String expected = clean(trial(s, 0, k, ""));
            if (!removeKDigits(s, k).equals(expected)) throw new AssertionError("disagrees with the trial on " + s + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Remove Duplicate Letters (LeetCode 316)
<!-- id: gc-remove-duplicate-letters -->

**Approach.** Precompute the last position of each letter. Scan the string and skip any letter that is already on the stack, since its earlier copy sits in a better position. Otherwise pop the top while the top is larger than the newcomer and the top letter occurs again later, clearing its flag, and then push the newcomer and set its flag. A letter that does not occur again is never popped, so every letter ends up present exactly once. The oracle enumerates every choice of one position per distinct letter that keeps reading order and takes the smallest string. The assertions check both examples and random strings over small alphabets.

**Complexity.** Each letter is pushed and popped at most once, so the time is O(n) with a 26-entry table and an O(26) stack.

```java run
import java.util.Random;

public final class RemoveDuplicateLetters {
    static String removeDuplicateLetters(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;
        boolean[] inStack = new boolean[26];
        StringBuilder stack = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (inStack[c - 'a']) continue;
            while (stack.length() > 0 && stack.charAt(stack.length() - 1) > c && last[stack.charAt(stack.length() - 1) - 'a'] > i) {
                inStack[stack.charAt(stack.length() - 1) - 'a'] = false;
                stack.setLength(stack.length() - 1);
            }
            stack.append(c);
            inStack[c - 'a'] = true;
        }
        return stack.toString();
    }

    static String oracle(String s) {
        int n = s.length();
        int distinct = (int) s.chars().distinct().count();
        String best = null;
        for (int mask = 0; mask < (1 << n); mask++) {
            if (Integer.bitCount(mask) != distinct) continue;
            StringBuilder sb = new StringBuilder();
            boolean[] seen = new boolean[26];
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                int c = s.charAt(i) - 'a';
                if (seen[c]) ok = false;
                seen[c] = true;
                sb.append(s.charAt(i));
            }
            if (ok && (best == null || sb.toString().compareTo(best) < 0)) best = sb.toString();
        }
        return best == null ? "" : best;
    }

    public static void main(String[] args) {
        if (!removeDuplicateLetters("dcbadbcd").equals("abcd")) throw new AssertionError("example 1");
        if (!removeDuplicateLetters("baab").equals("ab")) throw new AssertionError("example 2");
        if (!removeDuplicateLetters("").equals("")) throw new AssertionError("empty string");
        if (!removeDuplicateLetters("aaaa").equals("a")) throw new AssertionError("one repeated letter");
        if (!removeDuplicateLetters("zyxzyx").equals("xzy")) throw new AssertionError("letters that do not return are never popped");

        Random rnd = new Random(2802);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(13);
            int alpha = 1 + rnd.nextInt(5);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String s = sb.toString();
            if (!removeDuplicateLetters(s).equals(oracle(s))) throw new AssertionError("disagrees with the enumeration on " + s);
        }
    }
}
```

#### Solution: [Boundary] Smallest Subsequence of Distinct Characters (LeetCode 1081)
<!-- id: gc-distinct-by-rank -->

**Approach.** Build a rank table of 128 entries from `order`, a last-position table, and an in-stack flag per character. Scan the string. Skip a character that is already on the stack. Otherwise pop while the top has a larger rank than the newcomer and the top character occurs again later, then push. All three conditions work together: uniqueness decides the skip, future availability decides whether a pop is allowed, and the rank comparison decides whether a pop is wanted. The oracle enumerates every choice of one position per distinct character in reading order and compares candidates by rank. The assertions check both examples, a string that mixes digits, punctuation and letters, and random strings over a printable pool with random orders.

**Complexity.** One pass with constant-size tables gives O(n) time and O(1) extra memory beyond the answer.

```java run
import java.util.Random;

public final class DistinctByRank {
    static String distinct(String s, String order) {
        int[] rank = new int[128];
        for (int i = 0; i < order.length(); i++) rank[order.charAt(i)] = i;
        int[] last = new int[128];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i)] = i;
        boolean[] inStack = new boolean[128];
        StringBuilder stack = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (inStack[c]) continue;
            while (stack.length() > 0) {
                char top = stack.charAt(stack.length() - 1);
                if (rank[top] > rank[c] && last[top] > i) { inStack[top] = false; stack.setLength(stack.length() - 1); }
                else break;
            }
            stack.append(c);
            inStack[c] = true;
        }
        return stack.toString();
    }

    static String oracle(String s, String order) {
        int n = s.length();
        int distinct = (int) s.chars().distinct().count();
        String best = null;
        for (int mask = 0; mask < (1 << n); mask++) {
            if (Integer.bitCount(mask) != distinct) continue;
            StringBuilder sb = new StringBuilder();
            boolean[] seen = new boolean[128];
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) {
                if ((mask >> i & 1) == 0) continue;
                char c = s.charAt(i);
                if (seen[c]) ok = false;
                seen[c] = true;
                sb.append(c);
            }
            if (!ok) continue;
            if (best == null || lessByRank(sb.toString(), best, order)) best = sb.toString();
        }
        return best == null ? "" : best;
    }

    static boolean lessByRank(String a, String b, String order) {
        for (int i = 0; i < Math.min(a.length(), b.length()); i++) {
            int ra = order.indexOf(a.charAt(i)), rb = order.indexOf(b.charAt(i));
            if (ra != rb) return ra < rb;
        }
        return a.length() < b.length();
    }

    public static void main(String[] args) {
        if (!distinct("bacab", "cba").equals("cab")) throw new AssertionError("example 1");
        if (!distinct("bacab", "abc").equals("acb")) throw new AssertionError("example 2");
        if (!distinct("", "xyz").equals("")) throw new AssertionError("empty string");
        if (!distinct("A1!A1!", "!1A").equals("!A1")) throw new AssertionError("mixed printable characters");
        if (!distinct("A1!A1!", "A1!").equals("A1!")) throw new AssertionError("natural order of the same characters");

        String pool = "aB3!z~";
        Random rnd = new Random(2803);
        for (int t = 0; t < 5000; t++) {
            int alpha = 1 + rnd.nextInt(pool.length());
            int n = rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(pool.charAt(rnd.nextInt(alpha)));
            String s = sb.toString();
            java.util.List<Character> chars = new java.util.ArrayList<>();
            for (char c : pool.toCharArray()) chars.add(c);
            java.util.Collections.shuffle(chars, rnd);
            StringBuilder ord = new StringBuilder();
            for (char c : chars) ord.append(c);
            String order = ord.toString();
            if (!distinct(s, order).equals(oracle(s, order))) throw new AssertionError("disagrees with the enumeration on " + s + " under " + order);
        }
    }
}
```

#### Solution: [Recognize] Find the Most Competitive Subsequence (LeetCode 1673)
<!-- id: gc-competitive-subsequence -->

**Approach.** Keep an array stack of capacity `k`. For each element, pop while the top is strictly larger than the element and enough elements remain to refill the stack: after the pop the stack has `top - 1` entries, and the unread elements including this one number `n - i`, so the pop is allowed when `top - 1 + (n - i) >= k`. After popping, push the element if the stack is not yet full. Equal values are not popped. The oracle enumerates every subsequence of length `k` and compares them position by position with `Integer.compare`. The assertions check both examples, a full-length request, and random arrays with repeated values.

**Complexity.** Each element is pushed and popped at most once, so the time is O(n) and the stack uses O(k) memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CompetitiveSubsequence {
    static int[] competitive(int[] nums, int k) {
        int n = nums.length, top = 0;
        int[] stack = new int[k];
        for (int i = 0; i < n; i++) {
            while (top > 0 && stack[top - 1] > nums[i] && top - 1 + (n - i) >= k) top--;
            if (top < k) stack[top++] = nums[i];
        }
        return stack;
    }

    static int[] oracle(int[] a, int k) {
        int n = a.length;
        int[] best = null;
        for (int mask = 0; mask < (1 << n); mask++) {
            if (Integer.bitCount(mask) != k) continue;
            int[] cand = new int[k];
            for (int i = 0, p = 0; i < n; i++) if ((mask >> i & 1) == 1) cand[p++] = a[i];
            if (best == null || Arrays.compare(cand, best) < 0) best = cand;
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(competitive(new int[]{6, 4, 9, 5, 3, 8, 7}, 3), new int[]{3, 8, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(competitive(new int[]{2, 2, 2}, 2), new int[]{2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(competitive(new int[]{3, 9, 2}, 3), new int[]{3, 9, 2})) throw new AssertionError("a full-length request keeps everything");
        if (!Arrays.equals(competitive(new int[]{5}, 1), new int[]{5})) throw new AssertionError("single element");
        if (!Arrays.equals(competitive(new int[]{1000000000, 0}, 1), new int[]{0})) throw new AssertionError("large and zero values");

        Random rnd = new Random(2804);
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            int range = 2 + rnd.nextInt(7);
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(range);
            int k = 1 + rnd.nextInt(n);
            if (!Arrays.equals(competitive(a, k), oracle(a, k))) throw new AssertionError("disagrees with the enumeration on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```
