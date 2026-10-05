<!-- solutions-for: 09-sliding-window -->
### Solutions For Counts Inside A Window

#### Solution: [Build] Permutation In String (LeetCode 567)
<!-- id: sw-comb-permutation -->

**Approach.**
The array `need` holds the pattern counts, and `cnt` holds the window counts, which start at zero. The counter `bad` starts as the number of distinct letters in `p`, because each of them has window count 0 and a different pattern count. When a letter enters, the method records whether its count matched before, changes the count, and checks again. A change from matching to not matching raises `bad` by one, and the reverse lowers it by one. The leaving letter gets the same treatment once the window is longer than `k`. When `bad` is 0 for a full window, every letter matches, so the window is a permutation. The invariant is that `cnt` describes the window and `bad` equals the number of letters with `cnt[x] != need[x]`.

**Complexity.**
- **Time** is O(n + k), because building `need` costs `k` and each step makes two constant updates.
- **Space** is O(1), because the method keeps two arrays of 26 entries.

```java run
import java.util.Random;

public final class CombPermutation {
    /**
     * Returns the smallest start of a permutation of p inside s, or -1.
     * Time: O(n + k), constant work per step and no comparison of arrays.
     * Space: O(1), two arrays of 26 entries.
     * Invariant: cnt describes s[left..right], and bad is the number of letters x with cnt[x] != need[x].
     */
    static int firstMatchStart(String s, String p) {
        int k = p.length();
        // A pattern longer than the text has no window.
        if (k > s.length()) return -1;
        int[] need = new int[26], cnt = new int[26];
        // Count the pattern once.
        for (int i = 0; i < k; i++) need[p.charAt(i) - 'a']++;
        // Every letter of the pattern starts as a mismatch, because its window count is 0.
        int bad = 0;
        for (int x = 0; x < 26; x++) if (need[x] != 0) bad++;
        // Slide loop: one entering letter per step.
        for (int right = 0; right < s.length(); right++) {
            int in = s.charAt(right) - 'a';
            // Entering update: compare the letter's status before and after the count changes.
            boolean wasOk = cnt[in] == need[in];
            cnt[in]++;
            boolean isOk = cnt[in] == need[in];
            if (wasOk && !isOk) bad++; else if (!wasOk && isOk) bad--;
            // Leaving update: the letter at right - k leaves once the window would exceed k letters.
            if (right >= k) {
                int out = s.charAt(right - k) - 'a';
                wasOk = cnt[out] == need[out];
                cnt[out]--;
                isOk = cnt[out] == need[out];
                if (wasOk && !isOk) bad++; else if (!wasOk && isOk) bad--;
            }
            // A full window with no mismatching letter is a permutation, and the first one found has the smallest start.
            if (right >= k - 1 && bad == 0) return right - k + 1;
        }
        // The loop ended without a match.
        return -1;
    }

    /** Oracle: sorts every substring. */
    static int oracle(String s, String p) {
        char[] want = p.toCharArray();
        java.util.Arrays.sort(want);
        for (int st = 0; st + p.length() <= s.length(); st++) {
            char[] b = s.substring(st, st + p.length()).toCharArray();
            java.util.Arrays.sort(b);
            if (java.util.Arrays.equals(b, want)) return st;
        }
        return -1;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (firstMatchStart("eidbaooo", "ab") != 3) throw new AssertionError("example 1");
        if (firstMatchStart("abbaz", "aab") != -1) throw new AssertionError("example 2");
        // Random strings over a small alphabet agree with the oracle.
        Random rnd = new Random(91);
        for (int t = 0; t < 4000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(14); i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0, m = 1 + rnd.nextInt(5); i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (firstMatchStart(a.toString(), b.toString()) != oracle(a.toString(), b.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Longest Substring Without Repeating Characters (LeetCode 3)
<!-- id: sw-comb-repeat-limit -->

**Approach.**
The rule for a character is that its count is at most `limit`. The counter `over` holds the number of characters whose count exceeds `limit`. When a character enters and its count rises from `limit` to `limit + 1`, `over` rises by one. A shrink loop runs while `over` is above 0. Each leaving character whose count falls from `limit + 1` to `limit` lowers `over` by one. After the loop, the counts describe a valid window, and the method records its length. With `limit = 1`, the problem is the longest substring without repeating characters. The invariant is that `over` equals the number of characters with a count above `limit`.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once, with constant work per update.
- **Space** is O(1), because the count array has 128 entries.

```java run
import java.util.Random;

public final class CombRepeatLimit {
    /**
     * Returns the longest substring in which every character occurs at most limit times.
     * Time: O(n), each index enters once and leaves at most once.
     * Space: O(1), a count array of 128 entries.
     * Invariant: over equals the number of characters whose count in s[left..right] exceeds limit.
     */
    static int longest(String s, int limit) {
        int[] cnt = new int[128];
        int over = 0, left = 0, best = 0;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            // Entering update: a count that rises past the limit becomes a violation.
            if (++cnt[s.charAt(right)] == limit + 1) over++;
            // Shrink: runs while any character is over the limit; each pass removes the value at left.
            while (over > 0) {
                // Leaving update: a count that falls back to the limit clears a violation.
                if (cnt[s.charAt(left)]-- == limit + 1) over--;
                left++;
            }
            // The window is valid, so its length is a candidate.
            best = Math.max(best, right - left + 1);
        }
        // The longest valid length.
        return best;
    }

    /** Oracle: tests every substring. */
    static int oracle(String s, int limit) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            int[] c = new int[128];
            boolean ok = true;
            for (int x = i; x <= j; x++) if (++c[s.charAt(x)] > limit) ok = false;
            if (ok) best = Math.max(best, j - i + 1);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (longest("aaabbcaaa", 2) != 5) throw new AssertionError("example 1");
        if (longest("pwwkew", 1) != 3) throw new AssertionError("example 2");
        // Random strings and limits agree with the oracle.
        Random rnd = new Random(92);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(14); i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            int limit = 1 + rnd.nextInt(4);
            if (longest(sb.toString(), limit) != oracle(sb.toString(), limit)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Longest Repeating Character Replacement (LeetCode 424)
<!-- id: sw-comb-leftmost-replacement -->

**Approach.**
The answer needs a start position, so the window must be a valid substring at the moment of recording. The one removal form keeps an invalid window, and its `left` index does not name a valid substring, so the method uses a full shrink. The counts describe the window, and a scan of the 26 counts gives the exact dominant count for the test `length - dominant > k`. After the shrink loop, the window is valid. The method records `{left, length}` only when the length is strictly larger than the best, so the leftmost start wins ties. The invariant is that every recorded window has replacement cost at most `k`.

**Complexity.**
- **Time** is O(26 * n), because each index enters once and leaves at most once, and each loop test scans 26 counts.
- **Space** is O(1), because the count array has 26 entries.

```java run
import java.util.Random;

public final class CombLeftmostReplacement {
    /**
     * Returns {start, length} of the leftmost longest substring that becomes uniform after at most k replacements.
     * Time: O(26 * n), a scan of 26 counts per loop test.
     * Space: O(1), a count array of 26 entries.
     * Invariant: every recorded window has length minus dominant count at most k.
     */
    static int[] leftmostLongest(String s, int k) {
        int[] cnt = new int[26];
        int left = 0, bestStart = 0, bestLength = 0;
        // Expand: the letter at right enters.
        for (int right = 0; right < s.length(); right++) {
            cnt[s.charAt(right) - 'A']++;
            // Shrink: full shrink so that the window is valid when recorded.
            while (true) {
                int top = 0;
                for (int c : cnt) top = Math.max(top, c);
                if (right - left + 1 - top <= k) break;
                cnt[s.charAt(left) - 'A']--;
                left++;
            }
            // Strictly larger lengths only, so the leftmost start wins ties.
            if (right - left + 1 > bestLength) { bestLength = right - left + 1; bestStart = left; }
        }
        // The recorded window is a valid substring.
        return new int[] {bestStart, bestLength};
    }

    /** One removal form: its final left index is not the start of a valid window in general. */
    static int oneRemovalStart(String s, int k) {
        int[] cnt = new int[26];
        int left = 0, peak = 0;
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'A';
            cnt[c]++;
            peak = Math.max(peak, cnt[c]);
            if (right - left + 1 - peak > k) { cnt[s.charAt(left) - 'A']--; left++; }
        }
        return left;
    }

    /** Oracle: tests every substring in order of start. */
    static int[] oracle(String s, int k) {
        int bs = 0, bl = 0;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            int top = 0;
            for (int x = i; x <= j; x++) {
                int c = 0;
                for (int y = i; y <= j; y++) if (s.charAt(y) == s.charAt(x)) c++;
                top = Math.max(top, c);
            }
            if (j - i + 1 - top <= k && j - i + 1 > bl) { bl = j - i + 1; bs = i; }
        }
        return new int[] {bs, bl};
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (!java.util.Arrays.equals(leftmostLongest("AABABBA", 1), new int[] {0, 4})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(leftmostLongest("ABCDE", 0), new int[] {0, 1})) throw new AssertionError("example 2");
        // On "AAABCD" with k = 1, the one removal start is 2, and the substring there has cost 2, so it is not valid.
        if (oneRemovalStart("AAABCD", 1) != 2) throw new AssertionError("one removal start");
        // Random strings agree with the oracle.
        Random rnd = new Random(93);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(13); i < n; i++) sb.append((char) ('A' + rnd.nextInt(3)));
            int k = rnd.nextInt(sb.length() + 1);
            if (!java.util.Arrays.equals(leftmostLongest(sb.toString(), k), oracle(sb.toString(), k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-comb-count-minimum -->

**Approach.**
The counter `bad` holds the number of required copies still missing, starting at the length of `t`. An entering letter lowers it when the window holds fewer copies than required. The trimming loop runs while `bad` is 0. At each pass, the window covers the requirement, so the method compares its length with the shortest so far. A shorter length resets the count of windows to 1, an equal length adds 1, and a longer length changes nothing. Then the loop removes the leftmost letter, and it raises `bad` when the letter was a required copy. Each window of the form `[left..right]` is recorded at most once, because the pair of indexes changes at every pass. Every shortest cover is recorded when `right` reaches its end, because the loop trims `left` down to its start. The invariant is that the count equals the number of recorded windows of the shortest length.

**Complexity.**
- **Time** is O(n + m), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps two arrays of 26 entries.

```java run
import java.util.Random;

public final class CombCountMinimum {
    /**
     * Returns {shortest cover length, number of covers of that length}, or {-1, 0}.
     * Time: O(n + m), both indexes only move forward.
     * Space: O(1), two arrays of 26 entries.
     * Invariant: ways equals the number of recorded covers whose length equals best.
     */
    static int[] shortestAndCount(String s, String t) {
        int[] need = new int[26], cnt = new int[26];
        // Count the requirement once.
        for (int i = 0; i < t.length(); i++) need[t.charAt(i) - 'a']++;
        int bad = t.length(), left = 0, best = Integer.MAX_VALUE, ways = 0;
        // Expand: the letter at right enters.
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'a';
            // Entering update: only a copy that fills a gap lowers bad.
            if (cnt[c] < need[c]) bad--;
            cnt[c]++;
            // Trim: runs while the window covers the requirement.
            while (bad == 0) {
                int len = right - left + 1;
                // A shorter cover resets the count; an equal one adds to it.
                if (len < best) { best = len; ways = 1; } else if (len == best) ways++;
                int d = s.charAt(left) - 'a';
                // Leaving update: removing a required copy breaks the cover.
                cnt[d]--;
                if (cnt[d] < need[d]) bad++;
                left++;
            }
        }
        // No record means that no cover exists.
        return best == Integer.MAX_VALUE ? new int[] {-1, 0} : new int[] {best, ways};
    }

    /** Oracle: tests every substring. */
    static int[] oracle(String s, String t) {
        int best = Integer.MAX_VALUE, ways = 0;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            boolean ok = true;
            for (char c = 'a'; c <= 'z'; c++) {
                int have = 0, want = 0;
                for (int x = i; x <= j; x++) if (s.charAt(x) == c) have++;
                for (int x = 0; x < t.length(); x++) if (t.charAt(x) == c) want++;
                if (have < want) ok = false;
            }
            if (!ok) continue;
            int len = j - i + 1;
            if (len < best) { best = len; ways = 1; } else if (len == best) ways++;
        }
        return best == Integer.MAX_VALUE ? new int[] {-1, 0} : new int[] {best, ways};
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (!java.util.Arrays.equals(shortestAndCount("abcabc", "abc"), new int[] {3, 4})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(shortestAndCount("aa", "aaa"), new int[] {-1, 0})) throw new AssertionError("example 2");
        // Random strings agree with the oracle, including repeated requirements.
        Random rnd = new Random(94);
        for (int t = 0; t < 3000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(13); i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0, m = 1 + rnd.nextInt(4); i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (!java.util.Arrays.equals(shortestAndCount(a.toString(), b.toString()), oracle(a.toString(), b.toString()))) throw new AssertionError("random " + t);
        }
    }
}
```
