<!-- solutions-for: 02-prefix-matching -->
### Solutions For Prefix Matching

#### Solution: [Build] Prefix Function (Author exercise)
<!-- id: as-prefix-function -->

**Approach.**
The array `pi` is filled left to right. Before position `i` is read, the variable `k` holds `pi[i - 1]`, the length of the longest proper prefix of `p[0..i-1]` that is also a suffix of it. The character `p[i]` extends that border when it equals `p[k]`. When the two characters differ, no border of length `k + 1` exists, so the loop replaces `k` with `pi[k - 1]`, the next shorter border of the same text, and compares again. The loop stops when a character matches or when `k` reaches 0.

The invariant is that `k` is always the length of a border of the text read so far, and the borders are tried from longest to shortest. Every shorter border is reachable through `pi`, so no candidate is skipped. Each iteration of the outer loop raises `k` by at most 1, and each fallback lowers `k` by at least 1, so the total number of fallbacks never exceeds `n - 1`.

**Complexity.**
- **Time** is O(n), because `k` rises at most `n - 1` times in total and every fallback consumes one unit of that rise.
- **Space** is O(n), because the answer array holds one int per position; the working state is the single int `k`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PrefixFunctionBuild {
    // Counts fallback iterations so that main can check the amortized bound.
    static int fallbacks;

    /**
     * Returns pi, where pi[i] is the length of the longest proper prefix of p[0..i] that is also a suffix of it.
     * Time: O(n), because the matched length k rises at most once per position and each fallback lowers it.
     * Space: O(n), because the result array has one entry per character.
     * Invariant: at the top of iteration i, k equals pi[i - 1].
     */
    static int[] prefixFunction(String p) {
        // One entry per character; pi[0] stays 0 because a one-character text has no proper prefix.
        int[] pi = new int[p.length()];
        // k is the current matched length; it is 0 before any character is read.
        int k = 0;
        // Position 0 needs no work, so the scan starts at 1 and costs n - 1 iterations.
        for (int i = 1; i < p.length(); i++) {
            // A mismatch moves k to the next shorter border; each pass lowers k, which pays for itself.
            while (k > 0 && p.charAt(i) != p.charAt(k)) {
                // Fall back to the longest border of the first k characters.
                k = pi[k - 1];
                // Instrumentation only: it counts fallbacks for the bound checked in main.
                fallbacks++;
            }
            // A match extends the border by one character; this is the only place k grows.
            if (p.charAt(i) == p.charAt(k)) k++;
            // Record the border length for position i.
            pi[i] = k;
        }
        // The caller reads fallback lengths from this array.
        return pi;
    }

    /**
     * Brute-force oracle that tests every proper prefix length against the suffix of the same length.
     * Time: O(n^3), because each position tries up to n lengths and each comparison costs up to n.
     * Space: O(n), because only the result array is stored.
     * Invariant: the first length that matches, tried from longest to shortest, is the maximum.
     */
    static int[] oracle(String p) {
        // Result array, one entry per position.
        int[] pi = new int[p.length()];
        // Every end position is handled independently.
        for (int i = 0; i < p.length(); i++) {
            // Lengths run from the longest proper candidate (i) down to 1.
            for (int len = i; len >= 1; len--) {
                // ok stays true while the prefix and the suffix agree character by character.
                boolean ok = true;
                // Compare p[j] with the character at the same offset inside the suffix ending at i.
                for (int j = 0; j < len && ok; j++) ok = p.charAt(j) == p.charAt(i + 1 - len + j);
                // The first agreeing length is the longest, so the search for this position ends.
                if (ok) { pi[i] = len; break; }
            }
        }
        // The oracle answer is compared with the fast answer in main.
        return pi;
    }

    public static void main(String[] args) {
        // Worked examples from the exercise, including the long match that collapses to 0.
        if (!Arrays.equals(prefixFunction("aabaaab"), new int[] {0, 1, 0, 1, 2, 2, 3})) throw new AssertionError("aabaaab");
        if (!Arrays.equals(prefixFunction("abcabcabd"), new int[] {0, 0, 0, 1, 2, 3, 4, 5, 0})) throw new AssertionError("abcabcabd");
        // A repeated letter makes every border as long as possible but never the whole text.
        if (!Arrays.equals(prefixFunction("aaaa"), new int[] {0, 1, 2, 3})) throw new AssertionError("aaaa");
        // The empty text yields an empty array.
        if (prefixFunction("").length != 0) throw new AssertionError("empty");
        // Random comparison with the oracle; the seed makes any failure reproducible.
        Random rnd = new Random(3402L);
        for (int t = 0; t < 3000; t++) {
            // Small alphabets create many borders and many fallbacks.
            int len = rnd.nextInt(14), alpha = 1 + rnd.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String p = sb.toString();
            // The amortized bound: the fallbacks of one call never exceed n - 1 (and are 0 for an empty text).
            fallbacks = 0;
            int[] got = prefixFunction(p);
            if (!Arrays.equals(got, oracle(p))) throw new AssertionError("mismatch on " + p);
            if (fallbacks > Math.max(0, len - 1)) throw new AssertionError("too many fallbacks on " + p);
        }
    }
}
```

#### Solution: [Vary] First Occurrence With KMP (LeetCode 28)
<!-- id: as-first-occurrence-kmp -->

**Approach.**
The pattern's prefix function is computed once. The text is then scanned with a single index `i` that never moves backward, and a state `k` that holds how many pattern characters currently match the text ending at `i - 1`. When `text[i]` differs from `pattern[k]`, the state falls back to `pi[k - 1]`, because the last `pi[k - 1]` matched characters are also the first characters of the pattern. When the characters agree, `k` grows. When `k` equals the pattern length, the match ends at `i`, so the start is `i - m + 1`, and the method returns it at once, which gives the first occurrence.

The empty pattern is handled before the scan, because the contract returns 0 for it and the loop would otherwise read `pattern.charAt(0)`. The invariant is that `k` is the length of the longest pattern prefix that is a suffix of `text[0..i-1]`, so no earlier start can have been missed.

**Complexity.**
- **Time** is O(n + m), because the prefix function costs O(m) and the scan has the same amortized argument, with `k` rising at most `n` times.
- **Space** is O(m), because the prefix function array has one entry per pattern character and the scan adds one int.

```java run
import java.util.Random;

public final class FirstOccurrenceKmp {
    /**
     * Returns the first index where pattern occurs in text, 0 for an empty pattern, or -1.
     * Time: O(n + m), because i only advances and k falls at most as often as it rose.
     * Space: O(m), because the prefix function array has one entry per pattern character.
     * Invariant: after reading text[i], k is the longest pattern prefix that is a suffix of text[0..i].
     */
    static int indexOf(String text, String pattern) {
        // m is the pattern length; reading it once avoids repeated calls.
        int m = pattern.length();
        // The contract returns 0 for an empty pattern, and the guard keeps the loop from reading pattern.charAt(0).
        if (m == 0) return 0;
        // Fallback lengths for the pattern, built once for O(m) time.
        int[] pi = new int[m];
        // k is reused first as the border length while building pi.
        for (int i = 1, k = 0; i < m; i++) {
            // A mismatch falls back to the next shorter border.
            while (k > 0 && pattern.charAt(i) != pattern.charAt(k)) k = pi[k - 1];
            // A match grows the border by one.
            if (pattern.charAt(i) == pattern.charAt(k)) k++;
            // Store the border length for position i.
            pi[i] = k;
        }
        // k now counts pattern characters matched against the text; i never moves backward.
        int k = 0;
        // One pass over the text costs n iterations plus the fallbacks that earlier growth paid for.
        for (int i = 0; i < text.length(); i++) {
            // Fall back while the next pattern character cannot extend the current match.
            while (k > 0 && text.charAt(i) != pattern.charAt(k)) k = pi[k - 1];
            // Extend the match when the characters agree.
            if (text.charAt(i) == pattern.charAt(k)) k++;
            // A full match ends at i, so the first start is i - m + 1; returning here makes it the first occurrence.
            if (k == m) return i - m + 1;
        }
        // No position completed the pattern.
        return -1;
    }

    /**
     * Brute-force oracle that tries every start and compares character by character.
     * Time: O(n * m), because each start compares up to m characters.
     * Space: O(1), because only indexes are stored.
     * Invariant: starts are tried in increasing order, so the first success is the first occurrence.
     */
    static int oracle(String text, String pattern) {
        // Every start that leaves room for the whole pattern.
        for (int s = 0; s + pattern.length() <= text.length(); s++) {
            // j counts agreeing characters from this start.
            int j = 0;
            while (j < pattern.length() && text.charAt(s + j) == pattern.charAt(j)) j++;
            // A full agreement is a match; an empty pattern matches at 0 here too.
            if (j == pattern.length()) return s;
        }
        // No start matched.
        return -1;
    }

    public static void main(String[] args) {
        // Plain match at the start and an absent pattern.
        if (indexOf("sadbutsad", "sad") != 0) throw new AssertionError("sad");
        if (indexOf("leetcode", "leeto") != -1) throw new AssertionError("leeto");
        // The hostile case: the match starts after a long partial match that must fall back.
        if (indexOf("aaaaab", "aab") != 3) throw new AssertionError("aaaaab");
        if (indexOf("abababaca", "ababaca") != 2) throw new AssertionError("ababaca");
        // The empty pattern returns 0, and this agrees with String.indexOf.
        if (indexOf("abc", "") != 0 || "abc".indexOf("") != 0) throw new AssertionError("empty pattern");
        // A pattern longer than the text cannot match.
        if (indexOf("ab", "abc") != -1) throw new AssertionError("long pattern");
        // Random comparison with the oracle and with String.indexOf.
        Random rnd = new Random(3403L);
        for (int t = 0; t < 5000; t++) {
            // Small alphabets force many partial matches.
            int alpha = 1 + rnd.nextInt(3);
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = rnd.nextInt(16); i > 0; i--) a.append((char) ('a' + rnd.nextInt(alpha)));
            for (int i = rnd.nextInt(6); i > 0; i--) b.append((char) ('a' + rnd.nextInt(alpha)));
            String text = a.toString(), pat = b.toString();
            int want = oracle(text, pat);
            if (indexOf(text, pat) != want) throw new AssertionError("mismatch " + text + " / " + pat);
            if (text.indexOf(pat) != want) throw new AssertionError("library disagrees " + text + " / " + pat);
        }
        // A long repetitive input: a restarting scan would do about 10^8 comparisons here, this one does about 4 * 10^5.
        String big = "a".repeat(200_000), pat = "a".repeat(500) + "b";
        if (indexOf(big, pat) != -1) throw new AssertionError("big");
        if (indexOf(big + "b", pat) != 200_000 - 500) throw new AssertionError("big match");
    }
}
```

#### Solution: [Boundary] Repeated Prefixes (Author exercise)
<!-- id: as-repeated-prefixes -->

**Approach.**
The borders of the first `k` characters are exactly the values reached by starting at `pi[k - 1]` and repeatedly replacing a length `L` with `pi[L - 1]`. The longest border is `pi[k - 1]` by definition. Every shorter border of the full text is also a border of that longest border, because it is a prefix of it and a suffix of it, so `pi[L - 1]` names the next one. The walk stops when `L` reaches 0, and it never reports 0 or `k` itself because both are excluded by the word proper and by the requirement `0 < L`.

For `ababaca` and `k = 5`, the text is `ababa`, `pi[4]` is 3, and `pi[2]` is 1, so the answer is 3 then 1. The invariant is that the list always holds the borders found so far in decreasing order, and `L` holds the longest border that is not yet listed.

**Complexity.**
- **Time** is O(n) for the prefix function plus O(k) for the walk, because each step lowers `L` by at least 1.
- **Space** is O(n), because the prefix function array has one entry per character; the answer holds at most `k - 1` lengths.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class RepeatedPrefixChain {
    /**
     * Returns every L with 0 < L < k such that p[0..L) equals p[k-L..k), in decreasing order.
     * Time: O(n + k), because the prefix function costs O(n) and each chain step lowers L.
     * Space: O(n), because the prefix function array has one entry per character.
     * Invariant: L is the longest border of p[0..k) that is shorter than every length already listed.
     */
    static int[] borderLengths(String p, int k) {
        // Standard prefix function; the borders of every prefix come from this one array.
        int[] pi = new int[p.length()];
        // The matched length while building pi.
        int m = 0;
        for (int i = 1; i < p.length(); i++) {
            // Falls back through shorter borders on a mismatch.
            while (m > 0 && p.charAt(i) != p.charAt(m)) m = pi[m - 1];
            // Extends the border on a match.
            if (p.charAt(i) == p.charAt(m)) m++;
            // Records the border length at position i.
            pi[i] = m;
        }
        // The list grows by one entry per chain step.
        List<Integer> out = new ArrayList<>();
        // Start at the longest proper border of the first k characters; the loop ends when L reaches 0.
        for (int len = pi[k - 1]; len > 0; len = pi[len - 1]) {
            // Each value visited is a border and is longer than every value visited later.
            out.add(len);
        }
        // Copy into a primitive array for the caller.
        int[] res = new int[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    /**
     * Brute-force oracle that tests every length directly.
     * Time: O(k^2), because each of up to k lengths costs up to k comparisons.
     * Space: O(k), because the result list is bounded by k.
     * Invariant: lengths are tested from longest to shortest, which gives the decreasing order.
     */
    static int[] oracle(String p, int k) {
        // Result list in decreasing order of length.
        List<Integer> out = new ArrayList<>();
        // Only proper lengths 1..k-1 qualify.
        for (int len = k - 1; len >= 1; len--) {
            // ok stays true while prefix and suffix agree.
            boolean ok = true;
            for (int j = 0; j < len && ok; j++) ok = p.charAt(j) == p.charAt(k - len + j);
            // Keep the length when the whole comparison agreed.
            if (ok) out.add(len);
        }
        int[] res = new int[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    public static void main(String[] args) {
        // The exercise example: two fallbacks from length 3 to 1 to nothing.
        if (!Arrays.equals(borderLengths("ababaca", 5), new int[] {3, 1})) throw new AssertionError("ababa");
        // The whole pattern has the single border "a".
        if (!Arrays.equals(borderLengths("ababaca", 7), new int[] {1})) throw new AssertionError("ababaca");
        // A repeated letter lists every shorter length, and k = 1 lists none because the whole text is excluded.
        if (!Arrays.equals(borderLengths("aaaa", 4), new int[] {3, 2, 1})) throw new AssertionError("aaaa");
        if (borderLengths("aaaa", 1).length != 0) throw new AssertionError("k = 1");
        // Random comparison with the oracle for every legal k.
        Random rnd = new Random(3404L);
        for (int t = 0; t < 3000; t++) {
            int len = 1 + rnd.nextInt(12), alpha = 1 + rnd.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String p = sb.toString();
            for (int k = 1; k <= len; k++) {
                if (!Arrays.equals(borderLengths(p, k), oracle(p, k))) throw new AssertionError("mismatch " + p + " k=" + k);
            }
        }
    }
}
```

#### Solution: [Recognize] Longest Happy Prefix (LeetCode 1392)
<!-- id: as-longest-happy-prefix -->

**Approach.**
A happy prefix is a non-empty proper prefix that is also a suffix, and the longest one is by definition the last value of the prefix function, `pi[n - 1]`. The answer is the first `pi[n - 1]` characters of the string, and the empty string when that value is 0. The prefix function never reports the whole string, so the proper requirement holds without a separate check. Overlap is allowed, so `ababab` returns `abab`.

The invariant is the one from the Build exercise: after the loop, `k` is the longest border of the entire string. Only one substring is created, at the end, because every comparison inside the loop uses indexes.

**Complexity.**
- **Time** is O(n), because the prefix function is linear and the final copy costs at most n characters.
- **Space** is O(n), because the array holds one entry per character and the returned string can be nearly as long.

```java run
import java.util.Random;

public final class HappyPrefixFinal {
    /**
     * Returns the longest proper prefix of s that is also a suffix, or the empty string.
     * Time: O(n), because the border length rises at most n times and falls no more often than it rose.
     * Space: O(n), because the fallback array has one entry per character.
     * Invariant: after reading s[i], k is the longest proper border of s[0..i].
     */
    static String longestHappyPrefix(String s) {
        // Fallback lengths; only the last entry is needed, but the others drive the loop.
        int[] pi = new int[s.length()];
        // k is the length of the current border.
        int k = 0;
        // Scan from position 1; a single character has no proper border.
        for (int i = 1; i < s.length(); i++) {
            // Mismatch: fall back to the next shorter border, using indexes and no substring.
            while (k > 0 && s.charAt(i) != s.charAt(k)) k = pi[k - 1];
            // Match: the border grows by one character.
            if (s.charAt(i) == s.charAt(k)) k++;
            // Record the border at position i.
            pi[i] = k;
        }
        // One substring at the end; k = 0 yields the empty string and k < n keeps the prefix proper.
        return s.substring(0, k);
    }

    /**
     * Brute-force oracle that tries lengths from longest to shortest.
     * Time: O(n^2), because each of up to n lengths costs up to n comparisons.
     * Space: O(n), because the answer is one substring.
     * Invariant: the first length that agrees is the longest.
     */
    static String oracle(String s) {
        // Proper lengths only: n - 1 down to 1.
        for (int len = s.length() - 1; len >= 1; len--) {
            // Compare the first len characters with the last len characters.
            boolean ok = true;
            for (int j = 0; j < len && ok; j++) ok = s.charAt(j) == s.charAt(s.length() - len + j);
            // The first agreeing length is the maximum.
            if (ok) return s.substring(0, len);
        }
        // No proper border.
        return "";
    }

    public static void main(String[] args) {
        // Overlapping border: the prefix and the suffix share characters.
        if (!longestHappyPrefix("ababab").equals("abab")) throw new AssertionError("ababab");
        // A single-letter border.
        if (!longestHappyPrefix("level").equals("l")) throw new AssertionError("level");
        // No border returns the empty string, and substring(0, 0) is empty.
        if (!longestHappyPrefix("abcd").isEmpty() || !"abcd".substring(0, 0).isEmpty()) throw new AssertionError("abcd");
        // The whole string is never returned, even when it is one repeated letter.
        if (!longestHappyPrefix("aaaa").equals("aaa")) throw new AssertionError("aaaa");
        // A one-character string has no proper border.
        if (!longestHappyPrefix("a").isEmpty()) throw new AssertionError("a");
        // Random comparison with the oracle.
        Random rnd = new Random(3405L);
        for (int t = 0; t < 5000; t++) {
            int len = 1 + rnd.nextInt(14), alpha = 1 + rnd.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String s = sb.toString();
            if (!longestHappyPrefix(s).equals(oracle(s))) throw new AssertionError("mismatch " + s);
        }
    }
}
```

#### Solution: [Extend] Z Array (Author exercise)
<!-- id: as-z-array -->

**Approach.**
The array `z` is filled left to right while the algorithm keeps one window `[l, r)`, the segment that starts at `l`, ends before `r`, and equals the prefix `s[0..r-l)`. For a new position `i` inside the window, the characters `s[i..r)` equal `s[i-l..r-l)`, so `z[i]` starts at `min(r - i, z[i - l])` without any comparison. For a position outside the window the start is 0. The loop then extends by direct comparison, and the window moves to `[i, i + z[i])` when that reaches farther right.

The invariant is that every character of `s` before `r` has already been compared against the prefix, and `r` never decreases. The extension loop only runs past `r`, so it advances `r` by one on every successful comparison, and `r` is at most `n`. This gives O(n) in total.

The two methods keep different state. The window state is a segment of the text, and it answers how far each suffix matches the prefix. The fallback state is a single length, and it answers which prefix the text currently ends. The assertions below show they carry the same information, because the prefix function is recovered from `z` alone by a pass that writes each entry once.

**Complexity.**
- **Time** is O(n), because `r` rises with every successful comparison, never falls, and is capped at `n`, while every other step is constant work.
- **Space** is O(n), because the result array has one entry per position; the window needs only two ints.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ZArrayWindow {
    /**
     * Returns z, where z[i] is the length of the longest common prefix of s and s[i..], with z[0] = n.
     * Time: O(n), because the right edge r never moves left and every direct comparison moves it right.
     * Space: O(n), because the result has one entry per position.
     * Invariant: s[l..r) equals s[0..r-l) and r is the farthest right edge found so far.
     */
    static int[] zArray(String s) {
        // One entry per position; z[0] is defined as n by this contract.
        int n = s.length();
        int[] z = new int[n];
        if (n == 0) return z;
        z[0] = n;
        // The window [l, r) starts empty.
        int l = 0, r = 0;
        // Position 0 is fixed, so the scan starts at 1.
        for (int i = 1; i < n; i++) {
            // len starts at the amount already known to match.
            int len = 0;
            // Inside the window the mirrored entry z[i - l] is reused, capped so it never claims text beyond r.
            if (i < r) len = Math.min(r - i, z[i - l]);
            // Direct comparison runs only past what is known; each success advances i + len, which cannot pass n.
            while (i + len < n && s.charAt(len) == s.charAt(i + len)) len++;
            // Record the answer for position i.
            z[i] = len;
            // Move the window when this match reaches farther right than any earlier one.
            if (i + len > r) { l = i; r = i + len; }
        }
        // The caller reads match lengths from this array.
        return z;
    }

    /**
     * Brute-force oracle that compares each suffix with the prefix.
     * Time: O(n^2), because each of n positions compares up to n characters.
     * Space: O(n), because the result has one entry per position.
     * Invariant: the loop stops at the first mismatch, so the count is the longest common prefix.
     */
    static int[] oracle(String s) {
        int[] z = new int[s.length()];
        // Position 0 is the whole string by definition.
        if (s.length() > 0) z[0] = s.length();
        for (int i = 1; i < s.length(); i++) {
            // Count agreeing characters from the start of the prefix and of the suffix.
            int len = 0;
            while (i + len < s.length() && s.charAt(len) == s.charAt(i + len)) len++;
            z[i] = len;
        }
        return z;
    }

    /**
     * Recovers the prefix function from z alone: each border end is written once, by the earliest window covering it.
     * Time: O(n), because every position is written at most once and each scan stops at a written entry.
     * Space: O(n), because the result has one entry per position.
     * Invariant: pi[j] holds the longest border ending at j once some window with start i + length - 1 >= j has been seen.
     */
    static int[] prefixFromZ(int[] z) {
        int[] pi = new int[z.length];
        // Each start i with z[i] > 0 claims the end positions i .. i + z[i] - 1 that are still unclaimed.
        for (int i = 1; i < z.length; i++) {
            // Walk from the farthest end down; a written entry means all nearer ones are already written.
            for (int j = z[i] - 1; j >= 0 && pi[i + j] == 0; j--) pi[i + j] = j + 1;
        }
        return pi;
    }

    /** Prefix function by fallback, used only to compare with prefixFromZ in main. Time: O(n). Space: O(n). */
    static int[] fallbackPrefix(String p) {
        int[] pi = new int[p.length()];
        int k = 0;
        for (int i = 1; i < p.length(); i++) {
            // Fall back on mismatch.
            while (k > 0 && p.charAt(i) != p.charAt(k)) k = pi[k - 1];
            // Extend on match.
            if (p.charAt(i) == p.charAt(k)) k++;
            pi[i] = k;
        }
        return pi;
    }

    public static void main(String[] args) {
        // Worked examples from the exercise.
        if (!Arrays.equals(zArray("aabxaab"), new int[] {7, 1, 0, 0, 3, 1, 0})) throw new AssertionError("aabxaab");
        if (!Arrays.equals(zArray("aaaaa"), new int[] {5, 4, 3, 2, 1})) throw new AssertionError("aaaaa");
        // The empty string gives an empty array.
        if (zArray("").length != 0) throw new AssertionError("empty");
        // Random comparison with the oracle, and a check that z and the fallback state carry the same information.
        Random rnd = new Random(3406L);
        for (int t = 0; t < 5000; t++) {
            int len = rnd.nextInt(16), alpha = 1 + rnd.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < len; i++) sb.append((char) ('a' + rnd.nextInt(alpha)));
            String s = sb.toString();
            int[] z = zArray(s);
            if (!Arrays.equals(z, oracle(s))) throw new AssertionError("z mismatch " + s);
            if (!Arrays.equals(prefixFromZ(z), fallbackPrefix(s))) throw new AssertionError("pi from z mismatch " + s);
        }
    }
}
```
