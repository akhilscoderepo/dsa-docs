<!-- solutions-for: 93-drop-earlier-items-with-a-stack -->
### Solutions For Dropping With A Stack

#### Solution: [Build] Remove K Digits (LeetCode 402)
<!-- id: gr-remove-k-digits -->

**Approach.**
The method reads the digits left to right and keeps the survivors in a stack. Before it pushes a digit, it pops every larger top while deletions remain, and each pop spends one deletion. A larger top is followed by a smaller digit, so deleting it makes the number smaller at the earlier position. After the last digit the stack is non-decreasing, so any leftover deletions remove the tail. The method then strips the leading zeros and returns `"0"` for an empty stack.

After each digit, the stack holds the smallest survivors of the prefix that the used deletions allow.

**Complexity.**
- **Time** is O(n), because each digit is pushed once and popped at most once.
- **Space** is O(n) for the stack.

```java run
import java.util.*;

public final class RemoveKDigits {
    /**
     * Returns the smallest number after deleting min(k, n) digits.
     * Time: O(n). Space: O(n).
     * Invariant: the stack holds the smallest survivors of the prefix under the deletions used.
     */
    static String remove(String num, int k) {
        StringBuilder stack = new StringBuilder();
        for (int i = 0; i < num.length(); i++) {                       // one digit per step
            char d = num.charAt(i);
            while (k > 0 && stack.length() > 0 && stack.charAt(stack.length() - 1) > d) { // safe pop
                stack.setLength(stack.length() - 1);
                k--;
            }
            stack.append(d);
        }
        stack.setLength(stack.length() - Math.min(k, stack.length())); // leftover deletions take the tail
        int start = 0;
        while (start < stack.length() - 1 && stack.charAt(start) == '0') start++; // strip leading zeros
        return stack.length() == 0 ? "0" : stack.substring(start);
    }

    static String brute(String num, int k) {
        int n = num.length(), del = Math.min(k, n);
        String best = null;
        for (int mask = 0; mask < (1 << n); mask++) {                  // every set of exactly del deletions
            if (Integer.bitCount(mask) != del) continue;
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 0) sb.append(num.charAt(i));
            String v = sb.toString().replaceFirst("^0+(?!$)", "");
            if (v.isEmpty()) v = "0";
            if (best == null || v.length() < best.length() || (v.length() == best.length() && v.compareTo(best) < 0)) best = v;
        }
        return best == null ? "0" : best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!remove("1432219", 3).equals("1219")) throw new AssertionError("ex1");
        if (!remove("10200", 1).equals("200")) throw new AssertionError("ex2");
        // A budget above the length, an empty string and an all-zero result.
        if (!remove("9", 5).equals("0") || !remove("", 3).equals("0") || !remove("100", 2).equals("0")) throw new AssertionError("edge");
        // Random digit strings must match exhaustive deletion.
        Random rnd = new Random(2093);
        for (int t = 0; t < 600; t++) {
            StringBuilder sb = new StringBuilder();
            for (int c = rnd.nextInt(8); c > 0; c--) sb.append((char) ('0' + rnd.nextInt(4)));
            String s = sb.toString();
            int k = rnd.nextInt(10);
            if (!remove(s, k).equals(brute(s, k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Remove Duplicate Letters (LeetCode 316)
<!-- id: gr-remove-duplicate-letters -->

**Approach.**
The method records the last position of every letter and keeps a stack and a flag array for the letters on the stack. For a letter already on the stack, it does nothing, because the kept copy is earlier and no worse. For a new letter, it pops every larger top whose last position lies after the current index, because that top appears again and the pop only moves a smaller letter forward. It then pushes the letter. A top that does not appear again stays, because the string would lose it. The stack at the end holds the smallest string with one copy of each letter.

After each letter, the stack holds the smallest string of the distinct letters of the prefix that can still extend to all letters.

**Complexity.**
- **Time** is O(n), because each letter is pushed once and popped at most once.
- **Space** is O(1) for the 26-entry arrays, plus the stack of at most 26 letters.

```java run
import java.util.*;

public final class RemoveDuplicateLetters {
    /**
     * Returns the smallest subsequence with each distinct letter once.
     * Time: O(n). Space: O(1).
     * Invariant: the stack is the smallest string for the prefix that can still extend to every distinct letter.
     */
    static String smallest(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i; // final write wins
        boolean[] on = new boolean[26];
        StringBuilder stack = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {                         // one letter per step
            char c = s.charAt(i);
            if (on[c - 'a']) continue;                                 // the earlier copy is kept
            while (stack.length() > 0 && stack.charAt(stack.length() - 1) > c && last[stack.charAt(stack.length() - 1) - 'a'] > i) {
                on[stack.charAt(stack.length() - 1) - 'a'] = false;    // pop a larger letter that returns later
                stack.setLength(stack.length() - 1);
            }
            stack.append(c);
            on[c - 'a'] = true;
        }
        return stack.toString();
    }

    static String brute(String s) {
        int distinct = (int) s.chars().distinct().count();
        String best = null;
        for (int mask = 0; mask < (1 << s.length()); mask++) {
            if (Integer.bitCount(mask) != distinct) continue;
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < s.length(); i++) if ((mask >> i & 1) != 0) sb.append(s.charAt(i));
            String v = sb.toString();
            if (v.chars().distinct().count() != distinct) continue;
            if (best == null || v.compareTo(best) < 0) best = v;
        }
        return best == null ? "" : best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!smallest("cbacdcbc").equals("acdb")) throw new AssertionError("ex1");
        if (!smallest("bcabc").equals("abc")) throw new AssertionError("ex2");
        if (!smallest("").isEmpty() || !smallest("aaa").equals("a")) throw new AssertionError("edge");
        // Random strings must match exhaustive subsequences.
        Random rnd = new Random(2094);
        for (int t = 0; t < 600; t++) {
            StringBuilder sb = new StringBuilder();
            for (int c = rnd.nextInt(10); c > 0; c--) sb.append((char) ('a' + rnd.nextInt(4)));
            if (!smallest(sb.toString()).equals(brute(sb.toString()))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Smallest Subsequence of Distinct Characters (LeetCode 1081)
<!-- id: gr-distinct-subsequence-positions -->

**Approach.**
The method runs the same loop as the previous exercise and stores positions on the stack instead of letters. A letter already on the stack is skipped, so the earlier copy keeps its place. A new letter pops every larger top that appears again later, and then the method pushes its position. Skipping later copies picks the earliest positions among equal strings, and any position set that gives the same string uses the same letters in the same order, so the earliest choice is smallest in position order. The boundary cases are an empty string, a string with one distinct letter, and a letter whose copy would have been kept at a later position.

After each position, the stack holds the positions of the smallest string of the prefix, using the earliest copy of each letter.

**Complexity.**
- **Time** is O(n), because each position is pushed once and popped at most once.
- **Space** is O(1) for the arrays of 26 entries, plus at most 26 positions on the stack.

```java run
import java.util.*;

public final class DistinctSubsequencePositions {
    /**
     * Returns the positions of the smallest distinct-letter subsequence, earliest copies first.
     * Time: O(n). Space: O(1).
     * Invariant: the stack holds increasing positions of the smallest string for the prefix, using the earliest copies.
     */
    static int[] positions(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;
        boolean[] on = new boolean[26];
        int[] stack = new int[26];
        int size = 0;
        for (int i = 0; i < s.length(); i++) {                         // one position per step
            int c = s.charAt(i) - 'a';
            if (on[c]) continue;                                       // keep the earlier copy
            while (size > 0 && s.charAt(stack[size - 1]) - 'a' > c && last[s.charAt(stack[size - 1]) - 'a'] > i) {
                on[s.charAt(stack[--size]) - 'a'] = false;             // pop a larger letter that returns later
            }
            stack[size++] = i;
            on[c] = true;
        }
        return Arrays.copyOf(stack, size);
    }

    static int[] brute(String s) {
        int distinct = (int) s.chars().distinct().count();
        String bestStr = null;
        int[] bestPos = new int[0];
        for (int mask = 0; mask < (1 << s.length()); mask++) {
            if (Integer.bitCount(mask) != distinct) continue;
            StringBuilder sb = new StringBuilder();
            int[] pos = new int[distinct];
            int n = 0;
            for (int i = 0; i < s.length(); i++) if ((mask >> i & 1) != 0) { sb.append(s.charAt(i)); pos[n++] = i; }
            if (sb.chars().distinct().count() != distinct) continue;
            String v = sb.toString();
            if (bestStr == null || v.compareTo(bestStr) < 0 || (v.equals(bestStr) && Arrays.compare(pos, bestPos) < 0)) { bestStr = v; bestPos = pos; }
        }
        return bestPos;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(positions("baab"), new int[] {1, 3})) throw new AssertionError("ex1");
        if (!Arrays.equals(positions("abab"), new int[] {0, 1})) throw new AssertionError("ex2");
        if (positions("").length != 0 || !Arrays.equals(positions("aaa"), new int[] {0})) throw new AssertionError("edge");
        // Random strings must match exhaustive subsequences with the position tie rule.
        Random rnd = new Random(2095);
        for (int t = 0; t < 600; t++) {
            StringBuilder sb = new StringBuilder();
            for (int c = rnd.nextInt(10); c > 0; c--) sb.append((char) ('a' + rnd.nextInt(4)));
            if (!Arrays.equals(positions(sb.toString()), brute(sb.toString()))) throw new AssertionError("random " + t + " " + sb);
        }
    }
}
```

#### Solution: [Recognize] Find the Most Competitive Subsequence (LeetCode 1673)
<!-- id: gr-most-competitive-subsequence -->

**Approach.**
The method keeps a stack of the chosen elements and pops a larger top when enough elements remain to still fill `k` places. The element at index `i` may replace the top when `stack.size() - 1 + (n - i) >= k`, which says the stack without its top plus every element from `i` onward can still reach length `k`. That inequality is the removal budget, derived from the final length. After the loop the method keeps only the first `k` entries, because the stack can be longer than `k` when no pop was allowed. The pops are safe by the same exchange argument as before: replacing a larger earlier element with a smaller later one improves the first position where the two differ.

After each element, the stack holds the smallest prefix of length at most `k` that can still extend to length `k`.

**Complexity.**
- **Time** is O(n), because each element is pushed once and popped at most once.
- **Space** is O(k) for the stack, since the method trims a push once the stack is full.

```java run
import java.util.*;

public final class MostCompetitiveSubsequence {
    /**
     * Returns the smallest subsequence of length k.
     * Time: O(n). Space: O(k).
     * Invariant: the stack is the smallest prefix of an answer that can still reach length k.
     */
    static int[] compete(int[] nums, int k) {
        int n = nums.length;
        int[] stack = new int[k];                                      // at most k entries
        int size = 0;
        for (int i = 0; i < n; i++) {                                   // one element per step
            while (size > 0 && stack[size - 1] > nums[i] && size - 1 + (n - i) >= k) size--; // pop while k places remain reachable
            if (size < k) stack[size++] = nums[i];                      // never exceed k entries
        }
        return Arrays.copyOf(stack, size);
    }

    static int[] brute(int[] a, int k) {
        int[] best = null;
        for (int mask = 0; mask < (1 << a.length); mask++) {
            if (Integer.bitCount(mask) != k) continue;
            int[] v = new int[k];
            int n = 0;
            for (int i = 0; i < a.length; i++) if ((mask >> i & 1) != 0) v[n++] = a[i];
            if (best == null || Arrays.compare(v, best) < 0) best = v;
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(compete(new int[] {3, 5, 2, 6}, 2), new int[] {2, 6})) throw new AssertionError("ex1");
        if (!Arrays.equals(compete(new int[] {4, 7, 5, 9, 6, 8}, 3), new int[] {4, 5, 6})) throw new AssertionError("ex2");
        // k equals the length keeps everything, and k = 1 picks the minimum.
        if (!Arrays.equals(compete(new int[] {3, 1, 2}, 3), new int[] {3, 1, 2}) || !Arrays.equals(compete(new int[] {3, 1, 2}, 1), new int[] {1})) throw new AssertionError("edge");
        // Random arrays must match exhaustive subsets.
        Random rnd = new Random(2096);
        for (int t = 0; t < 600; t++) {
            int[] a = new int[1 + rnd.nextInt(8)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            int k = 1 + rnd.nextInt(a.length);
            if (!Arrays.equals(compete(a, k), brute(a, k))) throw new AssertionError("random " + t);
        }
    }
}
```
