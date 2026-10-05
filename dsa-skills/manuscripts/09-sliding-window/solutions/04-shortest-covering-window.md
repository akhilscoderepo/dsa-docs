<!-- solutions-for: 09-sliding-window -->
### Solutions For Shortest Covering Windows

#### Solution: [Build] Shortest Segment Containing A And B (Author exercise)
<!-- id: sw-shortest-ab -->

**Approach.**
The requirement has two symbols with one copy each, so `missing` starts at 2. The method expands `right` and lowers `missing` when an entering `a` or `b` fills a gap. When `missing` reaches 0, a `while` loop records the length of the block and then removes the leftmost character. The removal raises `missing` only when it takes the last copy of `a` or `b`, and then the loop ends. The invariant is that the method records only blocks that contain an `a` and a `b`.

**Complexity.**
- **Time** is O(n), because `right` advances `n` times and `left` advances at most `n` times.
- **Space** is O(1), because the method keeps two counters for the letters and three integers.

```java run
import java.util.Random;

public final class ShortestAB {
    /**
     * Returns the length of the shortest substring with an 'a' and a 'b', or -1.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), a few counters.
     * Invariant: missing is the number of the symbols a and b absent from s[left..right].
     */
    static int shortest(String s) {
        // Copies held in the block for 'a' and for 'b'.
        int a = 0, b = 0;
        // Two symbols are required, one copy each.
        int missing = 2, left = 0, best = Integer.MAX_VALUE;
        // Expand: one character enters per iteration.
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            // An entering 'a' fills a gap only when the block holds no 'a' yet.
            if (c == 'a') { if (a == 0) missing--; a++; }
            // The same rule applies to 'b'.
            if (c == 'b') { if (b == 0) missing--; b++; }
            // Trim: runs while the block covers both symbols, so the block never loses the cover before it is recorded.
            while (missing == 0) {
                // Record before removing, because the removal may break the cover.
                best = Math.min(best, right - left + 1);
                char d = s.charAt(left);
                // A leaving symbol raises missing only when it was the last copy.
                if (d == 'a') { a--; if (a == 0) missing++; }
                if (d == 'b') { b--; if (b == 0) missing++; }
                left++;
            }
        }
        // MAX_VALUE means no cover was ever recorded.
        return best == Integer.MAX_VALUE ? -1 : best;
    }

    /** Oracle: tests every substring. */
    static int oracle(String s) {
        int best = -1;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            String w = s.substring(i, j + 1);
            if (w.indexOf('a') >= 0 && w.indexOf('b') >= 0 && (best < 0 || w.length() < best)) best = w.length();
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2, and the empty string.
        if (shortest("bccbbacc") != 2) throw new AssertionError("example 1");
        if (shortest("cccab") != 2) throw new AssertionError("example 2");
        if (shortest("") != -1) throw new AssertionError("empty");
        // Random strings agree with the oracle.
        Random rnd = new Random(31);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(14); i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            if (shortest(sb.toString()) != oracle(sb.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Required Multiplicities (Author exercise)
<!-- id: sw-required-multiplicities -->

**Approach.**
The requirement asks for two copies of `a` and one copy of `b`, so `missing` starts at 3. An entering `a` lowers `missing` only while the block holds fewer than two `a` characters, and an entering `b` lowers it only while the block holds none. A third `a` is a surplus and changes nothing. A leaving `a` raises `missing` only when the block drops below two. The method records the length at every cover and trims as before. The invariant is that `missing` equals the number of required copies that the block lacks.

**Complexity.**
- **Time** is O(n), because each index enters once and leaves at most once.
- **Space** is O(1), because the method keeps a few counters.

```java run
import java.util.Random;

public final class RequiredMultiplicities {
    /**
     * Returns the length of the shortest substring with at least two 'a' and one 'b', or -1.
     * Time: O(n), both indexes only move forward.
     * Space: O(1), a few counters.
     * Invariant: missing counts the required copies absent from s[left..right].
     */
    static int shortest(String s) {
        int a = 0, b = 0;
        // The requirement has three copies in total: two a and one b.
        int missing = 3, left = 0, best = Integer.MAX_VALUE;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            // The first two a characters fill gaps; later ones are surplus.
            if (c == 'a') { if (a < 2) missing--; a++; }
            // The first b fills the single gap for b.
            if (c == 'b') { if (b < 1) missing--; b++; }
            // Trim while the block still covers the requirement.
            while (missing == 0) {
                // Record before removing.
                best = Math.min(best, right - left + 1);
                char d = s.charAt(left);
                // Removing an a breaks the cover only when it drops the count below two.
                if (d == 'a') { a--; if (a < 2) missing++; }
                // Removing the last b breaks the cover.
                if (d == 'b') { b--; if (b < 1) missing++; }
                left++;
            }
        }
        // Report the shortest length, or -1 when none was recorded.
        return best == Integer.MAX_VALUE ? -1 : best;
    }

    /** Oracle: tests every substring. */
    static int oracle(String s) {
        int best = -1;
        for (int i = 0; i < s.length(); i++) for (int j = i; j < s.length(); j++) {
            String w = s.substring(i, j + 1);
            long ca = w.chars().filter(x -> x == 'a').count();
            if (ca >= 2 && w.indexOf('b') >= 0 && (best < 0 || w.length() < best)) best = w.length();
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples 1 and 2.
        if (shortest("abcabca") != 4) throw new AssertionError("example 1");
        if (shortest("abc") != -1) throw new AssertionError("example 2");
        // Random strings agree with the oracle.
        Random rnd = new Random(32);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(14); i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            if (shortest(sb.toString()) != oracle(sb.toString())) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] No Cover Exists (Author exercise)
<!-- id: sw-no-cover -->

**Approach.**
The method counts the requirement in `need` and sets `missing` to the length of `t`. An empty `t` gives `missing = 0` before any character is read, so the answer is `{0, 0}` and the method returns at once. Otherwise the method expands and trims as before. It records a block only when its length is strictly smaller than the best, so a tie keeps the leftmost start, because starts are visited in increasing order. If the loop ends with no record, the method returns `{-1, 0}`. The method stores two integers and never builds a substring. The invariant is that `bestStart` and `bestLength` describe the leftmost shortest cover found so far.

**Complexity.**
- **Time** is O(n + m), because building `need` costs `m` and the scan costs `n`.
- **Space** is O(1), because the method keeps two arrays of 26 entries and a few integers.

```java run
import java.util.Random;

public final class NoCover {
    /**
     * Returns {start, length} of the leftmost shortest cover of t in s, {0, 0} for empty t, or {-1, 0}.
     * Time: O(n + m), one pass over each string.
     * Space: O(1), two arrays of 26 entries.
     * Invariant: bestStart and bestLength describe the leftmost shortest cover found so far.
     */
    static int[] shortestCover(String s, String t) {
        // An empty requirement is met by the empty block at index 0.
        if (t.isEmpty()) return new int[] {0, 0};
        int[] need = new int[26], have = new int[26];
        // Count the requirement once, m steps.
        for (int i = 0; i < t.length(); i++) need[t.charAt(i) - 'a']++;
        int missing = t.length(), left = 0, bestStart = -1, bestLength = Integer.MAX_VALUE;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            int c = s.charAt(right) - 'a';
            // Compare before incrementing: only a gap-filling copy lowers missing.
            if (have[c] < need[c]) missing--;
            have[c]++;
            // Trim while the block covers the requirement.
            while (missing == 0) {
                // Strict comparison keeps the leftmost start on a tie.
                if (right - left + 1 < bestLength) { bestLength = right - left + 1; bestStart = left; }
                int d = s.charAt(left) - 'a';
                have[d]--;
                // Compare after decrementing: dropping below need breaks the cover.
                if (have[d] < need[d]) missing++;
                left++;
            }
        }
        // No record means no cover exists.
        return bestStart < 0 ? new int[] {-1, 0} : new int[] {bestStart, bestLength};
    }

    /** Oracle: tests every substring by length and start. */
    static int[] oracle(String s, String t) {
        if (t.isEmpty()) return new int[] {0, 0};
        for (int len = 1; len <= s.length(); len++) for (int st = 0; st + len <= s.length(); st++) {
            String w = s.substring(st, st + len);
            boolean ok = true;
            for (char c0 = 'a'; c0 <= 'z'; c0++) { final char c = c0; if (w.chars().filter(x -> x == c).count() < t.chars().filter(x -> x == c).count()) ok = false; }
            if (ok) return new int[] {st, len};
        }
        return new int[] {-1, 0};
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (!java.util.Arrays.equals(shortestCover("xaybz", "ab"), new int[] {1, 3})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(shortestCover("aab", "abc"), new int[] {-1, 0})) throw new AssertionError("example 2");
        // Empty requirement and empty text.
        if (!java.util.Arrays.equals(shortestCover("abc", ""), new int[] {0, 0})) throw new AssertionError("empty t");
        if (!java.util.Arrays.equals(shortestCover("", "a"), new int[] {-1, 0})) throw new AssertionError("empty s");
        // Random strings agree with the oracle, including ties.
        Random rnd = new Random(33);
        for (int t = 0; t < 3000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0, n = rnd.nextInt(13); i < n; i++) a.append((char) ('a' + rnd.nextInt(3)));
            for (int i = 0, m = rnd.nextInt(5); i < m; i++) b.append((char) ('a' + rnd.nextInt(3)));
            if (!java.util.Arrays.equals(shortestCover(a.toString(), b.toString()), oracle(a.toString(), b.toString()))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Window Substring (LeetCode 76)
<!-- id: sw-minimum-window -->

**Approach.**
The alphabet has 52 letters, so the two count arrays have 128 entries and the index of a character is its code. The method uses the trimming scan of the previous exercises. It stores `bestStart` and `bestLength` and builds the answer with one call to `substring` after the loop. The comparison `<` keeps the leftmost block among those of equal length. The invariant is that, whenever the loop records, the block covers every character of `t` with its multiplicity.

**Complexity.**
- **Time** is O(n + m), because each index enters once and leaves at most once, and the final `substring` costs the answer length.
- **Space** is O(1) for the arrays, plus O(answer length) for the returned string.

```java run
import java.util.Random;

public final class MinimumWindow {
    /**
     * Returns the leftmost shortest substring of s that covers t, or "".
     * Time: O(n + m), both indexes only move forward.
     * Space: O(1) for two arrays of 128 entries, plus the returned string.
     * Invariant: when the loop records, s[left..right] covers every character of t with its count.
     */
    static String minWindow(String s, String t) {
        // The arrays cover all ASCII codes, which includes 'A'..'Z' and 'a'..'z'.
        int[] need = new int[128], have = new int[128];
        // Count the requirement once.
        for (int i = 0; i < t.length(); i++) need[t.charAt(i)]++;
        int missing = t.length(), left = 0, bestStart = 0, bestLength = Integer.MAX_VALUE;
        // Expand: the character at right enters.
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            // Only a copy that fills a gap lowers missing.
            if (have[c] < need[c]) missing--;
            have[c]++;
            // Trim while the block still covers the requirement.
            while (missing == 0) {
                // Record the block if it is strictly shorter, which keeps the leftmost on a tie.
                if (right - left + 1 < bestLength) { bestLength = right - left + 1; bestStart = left; }
                char d = s.charAt(left);
                have[d]--;
                // Dropping below the required count breaks the cover.
                if (have[d] < need[d]) missing++;
                left++;
            }
        }
        // Build the answer once, after the loop.
        return bestLength == Integer.MAX_VALUE ? "" : s.substring(bestStart, bestStart + bestLength);
    }

    /** Oracle: tests every substring by length and start. */
    static String oracle(String s, String t) {
        for (int len = 1; len <= s.length(); len++) for (int st = 0; st + len <= s.length(); st++) {
            String w = s.substring(st, st + len);
            boolean ok = true;
            for (char c : t.toCharArray()) if (w.chars().filter(x -> x == c).count() < t.chars().filter(x -> x == c).count()) ok = false;
            if (ok) return w;
        }
        return "";
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the problem statement.
        if (!minWindow("ADOBECODEBANC", "ABC").equals("BANC")) throw new AssertionError("example 1");
        if (!minWindow("aa", "aaa").isEmpty()) throw new AssertionError("example 2");
        // Random mixed-case strings agree with the oracle.
        Random rnd = new Random(34);
        String alpha = "aAbB";
        for (int t = 0; t < 3000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            for (int i = 0, n = 1 + rnd.nextInt(13); i < n; i++) a.append(alpha.charAt(rnd.nextInt(4)));
            for (int i = 0, m = 1 + rnd.nextInt(4); i < m; i++) b.append(alpha.charAt(rnd.nextInt(4)));
            if (!minWindow(a.toString(), b.toString()).equals(oracle(a.toString(), b.toString()))) throw new AssertionError("random " + t);
        }
    }
}
```
