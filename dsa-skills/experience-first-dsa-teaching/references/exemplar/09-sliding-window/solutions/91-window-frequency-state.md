<!-- solutions-for: 91-window-frequency-state -->
### Window Frequency State

#### Solution: [Build] Permutation in String With A Matched Counter (LeetCode 567)
<!-- id: sw-permutation-matched -->

**Approach.** Keep `need` and `have` tables over 65,536 slots and a counter `status` of required characters whose window count equals the need. On every arrival and departure of a required character, subtract the slot's old contribution, change the count, and add the new contribution. The window passes when `status` equals the number of distinct required characters. Characters the probe does not contain are skipped, which is safe because the window length equals the probe length.

**Complexity.** O(n + m) time in the loop, plus O(65,536) to allocate the tables once, and O(65,536) extra space.

```java run
import java.util.Arrays;

public final class PermutationMatched {
    static boolean checkInclusion(String s1, String s2) {
        int k = s1.length();
        if (k > s2.length()) return false;
        int[] need = new int[65536], have = new int[65536];
        int distinct = 0;
        for (int i = 0; i < k; i++) if (need[s1.charAt(i)]++ == 0) distinct++;
        int status = 0;
        for (int right = 0; right < s2.length(); right++) {
            char in = s2.charAt(right);
            if (need[in] > 0) {
                if (have[in] == need[in]) status--;
                have[in]++;
                if (have[in] == need[in]) status++;
            }
            if (right >= k) {
                char out = s2.charAt(right - k);
                if (need[out] > 0) {
                    if (have[out] == need[out]) status--;
                    have[out]--;
                    if (have[out] == need[out]) status++;
                }
            }
            if (right >= k - 1 && status == distinct) return true;
        }
        return false;
    }

    static boolean brute(String s1, String s2) {
        int k = s1.length();
        char[] want = s1.toCharArray();
        Arrays.sort(want);
        for (int i = 0; i + k <= s2.length(); i++) {
            char[] block = s2.substring(i, i + k).toCharArray();
            Arrays.sort(block);
            if (Arrays.equals(block, want)) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (!checkInclusion("aab", "zbaaz")) throw new AssertionError("example 1");
        if (checkInclusion("aab", "abbab")) throw new AssertionError("example 2");
        java.util.Random rnd = new java.util.Random(3);
        for (int trial = 0; trial < 4000; trial++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            int n = 1 + rnd.nextInt(4), m = rnd.nextInt(10);
            for (int i = 0; i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (checkInclusion(a.toString(), b.toString()) != brute(a.toString(), b.toString()))
                throw new AssertionError("mismatch " + a + " " + b);
        }
    }
}
```

#### Solution: [Vary] Longest Unique Substring With A Status Counter (LeetCode 3)
<!-- id: sw-unique-status-counter -->

**Approach.** The status counter holds the number of characters that currently occur more than once. An arrival that lifts a count to two raises it, and a departure that drops a count to one lowers it. A `while` loop moves `left` until the counter is zero, so the window is valid when measured. Update the best only when the new length is strictly larger, so the leftmost longest substring wins.

**Complexity.** O(n) time and O(65,536) extra space for the count table.

```java run
import java.util.Arrays;

public final class UniqueStatusCounter {
    static int[] leftmostLongest(String s) {
        int[] count = new int[65536];
        int repeats = 0, left = 0, bestStart = 0, bestLen = 0;
        for (int right = 0; right < s.length(); right++) {
            if (++count[s.charAt(right)] == 2) repeats++;
            while (repeats > 0) {
                if (--count[s.charAt(left)] == 1) repeats--;
                left++;
            }
            if (right - left + 1 > bestLen) {
                bestLen = right - left + 1;
                bestStart = left;
            }
        }
        return new int[] {bestStart, bestLen};
    }

    static int[] brute(String s) {
        int bestStart = 0, bestLen = 0;
        for (int i = 0; i < s.length(); i++) {
            java.util.HashSet<Character> seen = new java.util.HashSet<>();
            for (int j = i; j < s.length(); j++) {
                if (!seen.add(s.charAt(j))) break;
                if (j - i + 1 > bestLen) { bestLen = j - i + 1; bestStart = i; }
            }
        }
        return new int[] {bestStart, bestLen};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(leftmostLongest("dvdfkd"), new int[] {1, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(leftmostLongest("abccdefgcd"), new int[] {3, 5})) throw new AssertionError("example 2");
        if (!Arrays.equals(leftmostLongest(""), new int[] {0, 0})) throw new AssertionError("empty");
        java.util.Random rnd = new java.util.Random(5);
        for (int trial = 0; trial < 4000; trial++) {
            StringBuilder b = new StringBuilder();
            int n = rnd.nextInt(12);
            for (int i = 0; i < n; i++) b.append((char) ('a' + rnd.nextInt(4)));
            if (!Arrays.equals(leftmostLongest(b.toString()), brute(b.toString()))) throw new AssertionError("mismatch " + b);
        }
    }
}
```

#### Solution: [Boundary] Longest Repeating Character Replacement, Mixed Case (LeetCode 424)
<!-- id: sw-replacement-mixed-case -->

**Approach.** Map a letter to a slot in a 52-slot table, with lowercase letters after uppercase ones. Keep a stored dominant count that is raised on arrival and never lowered. It may overstate the dominant count of the current window, but the window length is held at most `maxFreq + k`, and a length of exactly that is reached only after a real window had that dominant count, so the reported length is always achievable. The argument does not depend on the alphabet size.

**Complexity.** O(n) time and O(52) extra space.

```java run
public final class ReplacementMixedCase {
    private static int slot(char c) {
        return c >= 'a' ? 26 + (c - 'a') : c - 'A';
    }

    static int characterReplacement(String s, int k) {
        int[] tally = new int[52];
        int left = 0, maxFreq = 0, best = 0;
        for (int right = 0; right < s.length(); right++) {
            maxFreq = Math.max(maxFreq, ++tally[slot(s.charAt(right))]);
            while (right - left + 1 - maxFreq > k) {
                tally[slot(s.charAt(left))]--;
                left++;
            }
            best = Math.max(best, right - left + 1);
        }
        return best;
    }

    static int brute(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            int[] t = new int[52];
            int most = 0;
            for (int j = i; j < s.length(); j++) {
                most = Math.max(most, ++t[slot(s.charAt(j))]);
                if (j - i + 1 - most <= k) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (characterReplacement("aAaA", 1) != 3) throw new AssertionError("example 1");
        if (characterReplacement("AAaa", 0) != 2) throw new AssertionError("example 2");
        java.util.Random rnd = new java.util.Random(9);
        for (int trial = 0; trial < 4000; trial++) {
            StringBuilder b = new StringBuilder();
            int n = 1 + rnd.nextInt(12);
            for (int i = 0; i < n; i++) b.append(rnd.nextBoolean() ? (char) ('A' + rnd.nextInt(2)) : (char) ('a' + rnd.nextInt(2)));
            int k = rnd.nextInt(n + 1);
            if (characterReplacement(b.toString(), k) != brute(b.toString(), k)) throw new AssertionError("mismatch " + b + " " + k);
        }
    }
}
```

#### Solution: [Recognize] Minimum Window Substring Over Any Characters (LeetCode 76)
<!-- id: sw-minimum-window-any-chars -->

**Approach.** The counter `owed` holds the number of required copies still missing. An arriving character that was still owed reduces it. While it is zero, record the window if it is strictly shorter than the best, so the leftmost shortest wins, then remove the leftmost character with the local update in order: change the count, then check whether the departing character is owed again. A cover requires at-least, so surplus copies, stored as negative table entries, never raise the counter.

**Complexity.** O(n + m) time and O(65,536) extra space, with one call to `substring`.

```java run
public final class MinimumWindowAnyChars {
    static String minWindow(String s, String t) {
        int[] table = new int[65536];
        for (int i = 0; i < t.length(); i++) table[t.charAt(i)]++;
        int owed = t.length();
        int left = 0, bestStart = 0, bestLen = Integer.MAX_VALUE;
        for (int right = 0; right < s.length(); right++) {
            char in = s.charAt(right);
            if (table[in] > 0) owed--;
            table[in]--;
            while (owed == 0) {
                if (right - left + 1 < bestLen) {
                    bestLen = right - left + 1;
                    bestStart = left;
                }
                char out = s.charAt(left);
                table[out]++;
                if (table[out] > 0) owed++;
                left++;
            }
        }
        return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLen);
    }

    static String brute(String s, String t) {
        String best = "";
        for (int i = 0; i < s.length(); i++) {
            for (int j = i + 1; j <= s.length(); j++) {
                String w = s.substring(i, j);
                int[] c = new int[128];
                for (char ch : w.toCharArray()) c[ch]++;
                boolean ok = true;
                for (char ch : t.toCharArray()) if (--c[ch] < 0) ok = false;
                if (ok && (best.isEmpty() || w.length() < best.length())) best = w;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!minWindow("zzxyzxyyz", "xyz").equals("zxy")) throw new AssertionError("example 1");
        if (!minWindow("aa", "aaa").equals("")) throw new AssertionError("example 2");
        java.util.Random rnd = new java.util.Random(13);
        for (int trial = 0; trial < 3000; trial++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            int n = 1 + rnd.nextInt(10), m = 1 + rnd.nextInt(3);
            for (int i = 0; i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0; i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (!minWindow(a.toString(), b.toString()).equals(brute(a.toString(), b.toString())))
                throw new AssertionError("mismatch " + a + " " + b);
        }
    }
}
```

#### Solution: [Extend] Longest Substring with At Least K Repeating Characters (LeetCode 395)
<!-- id: sw-at-least-k-repeating -->

**Approach.** Fix the number of distinct letters allowed, `target`, from 1 to 26. For each target run a window that never holds more than `target` distinct letters, keeping two counters: `unique`, the distinct letters inside, and `enough`, how many of them already occur at least `k` times. Shrink from the left while `unique` exceeds `target`. When `unique` equals `enough`, every letter in the window is frequent enough, so the window is valid and its length is a candidate.

**Complexity.** O(26 * n) time and O(26) extra space.

```java run
public final class AtLeastKRepeating {
    static int longestSubstring(String s, int k) {
        int best = 0;
        for (int target = 1; target <= 26; target++) {
            int[] count = new int[26];
            int unique = 0, enough = 0, left = 0;
            for (int right = 0; right < s.length(); right++) {
                int in = s.charAt(right) - 'a';
                if (count[in]++ == 0) unique++;
                if (count[in] == k) enough++;
                while (unique > target) {
                    int out = s.charAt(left) - 'a';
                    if (count[out] == k) enough--;
                    if (--count[out] == 0) unique--;
                    left++;
                }
                if (unique == enough) best = Math.max(best, right - left + 1);
            }
        }
        return best;
    }

    static int brute(String s, int k) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            for (int j = i + 1; j <= s.length(); j++) {
                int[] c = new int[26];
                for (int p = i; p < j; p++) c[s.charAt(p) - 'a']++;
                boolean ok = true;
                for (int x : c) if (x > 0 && x < k) ok = false;
                if (ok) best = Math.max(best, j - i);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestSubstring("xxyyyzzzzw", 3) != 7) throw new AssertionError("example 1");
        if (longestSubstring("aabbbcccd", 3) != 6) throw new AssertionError("example 2");
        java.util.Random rnd = new java.util.Random(17);
        for (int trial = 0; trial < 3000; trial++) {
            StringBuilder b = new StringBuilder();
            int n = 1 + rnd.nextInt(12);
            for (int i = 0; i < n; i++) b.append((char) ('a' + rnd.nextInt(3)));
            int k = 1 + rnd.nextInt(4);
            if (longestSubstring(b.toString(), k) != brute(b.toString(), k)) throw new AssertionError("mismatch " + b + " " + k);
        }
    }
}
```
