<!-- solutions-for: 03-palindrome-radii -->
### Solutions For Palindrome Radii

#### Solution: [Build] Expand Odd Centers (Author exercise)
<!-- id: as-expand-odd-centers -->

**Approach.**
For each index `c`, the code keeps a counter `k` that starts at 0 and grows while the characters at `c - k - 1` and `c + k + 1` are both inside the string and equal. The invariant is that the characters from `c - k` through `c + k` already form a palindrome before each comparison, so a successful comparison extends the palindrome by one character on each side. The loop ends at a mismatch or at an end of the string, and the final `k` is the odd radius of `c`. A brute-force oracle checks every `k` independently with an index-range palindrome test.

**Complexity.**
- **Time** is O(n^2) in the worst case, because a string of identical letters lets each of the `n` centers expand about `n / 4` times on average.
- **Space** is O(1) beyond the result array, because the loop keeps only the counters `c` and `k`.

```java run
import java.util.Random;

public final class OddCenterRadii {
    /**
     * Returns the odd radius of every index of s by direct expansion.
     * Time: O(n^2) worst case, because each center may expand across the string.
     * Space: O(n) for the result array and O(1) extra.
     * Invariant: s[c - k .. c + k] is a palindrome before each comparison.
     */
    static int[] oddRadii(String s) {
        // One result slot per index of s.
        int n = s.length();
        int[] out = new int[n];
        // Each index is a center; this loop runs n times.
        for (int c = 0; c < n; c++) {
            int k = 0; // current radius, the palindrome s[c..c] has radius 0
            // Stay inside the string and extend only while the next outer pair is equal.
            while (c - k - 1 >= 0 && c + k + 1 < n && s.charAt(c - k - 1) == s.charAt(c + k + 1)) {
                k++; // one more matching pair, so the palindrome grows by two characters
            }
            out[c] = k; // the first mismatch or boundary ends the expansion
        }
        // The caller reads one radius per index.
        return out;
    }

    /**
     * Tests whether s[lo..hi] reads the same in both directions without allocating a substring.
     * Time: O(hi - lo), because one pass compares symmetric pairs.
     * Space: O(1), because only two indexes are kept.
     * Invariant: every pair outside the moving indexes has matched.
     */
    static boolean isPalindrome(String s, int lo, int hi) {
        // Move the two ends toward each other until they cross.
        while (lo < hi) {
            // A mismatch means the block is not a palindrome.
            if (s.charAt(lo++) != s.charAt(hi--)) return false;
        }
        // Every pair matched, or the block had at most one character.
        return true;
    }

    /**
     * Oracle: tries every k and keeps the largest one whose block is a palindrome.
     * Time: O(n^2) per center in the worst case, because each test is linear.
     * Space: O(1) beyond the result array.
     * Invariant: best holds the largest verified k so far.
     */
    static int[] oracle(String s) {
        // Result array, one entry per index.
        int[] out = new int[s.length()];
        // Check every center.
        for (int c = 0; c < s.length(); c++) {
            // Check every candidate k that fits inside the string.
            for (int k = 0; c - k >= 0 && c + k < s.length(); k++) {
                // Keep the largest k whose whole block is a palindrome.
                if (isPalindrome(s, c - k, c + k)) out[c] = k;
            }
        }
        // The caller compares this array with the fast result.
        return out;
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        if (!java.util.Arrays.equals(oddRadii("abaab"), new int[] {0, 1, 0, 0, 0})) throw new AssertionError("abaab");
        // Example 2: radius at each index is limited by the nearer end.
        if (!java.util.Arrays.equals(oddRadii("aaaaa"), new int[] {0, 1, 2, 1, 0})) throw new AssertionError("aaaaa");
        // A one-character string has radius 0.
        if (!java.util.Arrays.equals(oddRadii("z"), new int[] {0})) throw new AssertionError("single");
        // Random strings over a small alphabet produce many palindromes.
        Random rnd = new Random(34031);
        for (int iter = 0; iter < 2000; iter++) {
            // Length 1..14 over the letters a and b.
            int n = 1 + rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            String s = sb.toString();
            // The fast result must equal the oracle on every index.
            if (!java.util.Arrays.equals(oddRadii(s), oracle(s))) throw new AssertionError("mismatch on " + s);
        }
    }
}
```

#### Solution: [Vary] Unified Separators (Author exercise)
<!-- id: as-unified-separators -->

**Approach.**
The code builds `t` with a `#` before, between and after the letters, so the length is `2n + 1` and letter `k` of `s` sits at index `2k + 1`. Every palindrome of `t` has odd length, and the gap between two letters is a separator index, so one expansion loop covers both parities. This invariant matches the previous exercise, applied to `t`: before each comparison, `t[i - k .. i + k]` is a palindrome. The oracle ignores `t` entirely and computes, for every center of `s` (a letter or a gap), the longest palindrome directly in `s`, and the two results must agree at index `i` of `t`.

**Complexity.**
- **Time** is O(n^2) in the worst case, because each of the `2n + 1` centers can expand across the whole string.
- **Space** is O(n), because `t` and `rad` each hold `2n + 1` values.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SeparatorRadii {
    /**
     * Builds the separator string as a char array.
     * Time: O(n), because each letter is written once.
     * Space: O(n), because the array has 2n + 1 slots.
     * Invariant: letter k of s sits at index 2k + 1 and every other index is a separator.
     */
    static char[] withSeparators(String s) {
        // 2n + 1 slots: a separator before, between and after the letters.
        char[] t = new char[2 * s.length() + 1];
        // Fill every slot with a separator first.
        Arrays.fill(t, '#');
        // Then place each letter at its odd index.
        for (int k = 0; k < s.length(); k++) t[2 * k + 1] = s.charAt(k);
        // The caller expands around each index of t.
        return t;
    }

    /**
     * Returns the radius of every index of t by direct expansion.
     * Time: O(n^2) worst case.
     * Space: O(n) for the result.
     * Invariant: t[i - k .. i + k] is a palindrome before each comparison.
     */
    static int[] radii(String s) {
        char[] t = withSeparators(s);
        // One radius per index of t.
        int[] rad = new int[t.length];
        // Every index of t is a center, odd or even in the original string.
        for (int i = 0; i < t.length; i++) {
            int k = 0; // radius found so far
            // Extend while the next outer pair exists and is equal.
            while (i - k - 1 >= 0 && i + k + 1 < t.length && t[i - k - 1] == t[i + k + 1]) k++;
            rad[i] = k; // store the final radius
        }
        // The caller reads the array by index.
        return rad;
    }

    /**
     * Oracle: longest palindrome of s centered at t-index i, computed on s itself.
     * Time: O(n) per call, because one expansion crosses the string at most once.
     * Space: O(1).
     * Invariant: lo..hi is a palindrome whenever the loop test runs.
     */
    static int centeredLength(String s, int i) {
        // Odd i is a letter index 2k + 1, even i is the gap before letter i / 2.
        int lo, hi;
        if (i % 2 == 1) { lo = i / 2; hi = i / 2; } // start from the letter itself
        else { lo = i / 2 - 1; hi = i / 2; } // start from the empty gap between two letters
        // Grow the block while both ends exist and match.
        while (lo >= 0 && hi < s.length() && s.charAt(lo) == s.charAt(hi)) { lo--; hi++; }
        // Characters strictly between the failed ends.
        return hi - lo - 1;
    }

    public static void main(String[] args) {
        // Example 1: the even palindrome abba appears as radius 4 at index 4.
        if (!Arrays.equals(radii("abba"), new int[] {0, 1, 0, 1, 4, 1, 0, 1, 0})) throw new AssertionError("abba");
        // Example 2: the gap between two equal letters has radius 2.
        if (!Arrays.equals(radii("aa"), new int[] {0, 1, 2, 1, 0})) throw new AssertionError("aa");
        // The padded array has length 2n + 1 and starts and ends with separators.
        char[] t = withSeparators("abc");
        if (t.length != 7 || t[0] != '#' || t[6] != '#' || t[3] != 'b') throw new AssertionError("layout");
        // Random strings: the radius at i must equal the longest palindrome of s centered there.
        Random rnd = new Random(34032);
        for (int iter = 0; iter < 2000; iter++) {
            int n = 1 + rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            String s = sb.toString();
            int[] rad = radii(s);
            // Length check first, then each index against the oracle.
            if (rad.length != 2 * n + 1) throw new AssertionError("length " + s);
            for (int i = 0; i < rad.length; i++) {
                if (rad[i] != centeredLength(s, i)) throw new AssertionError("index " + i + " of " + s);
            }
        }
    }
}
```

#### Solution: [Boundary] Mirror Beyond Boundary (Author exercise)
<!-- id: as-mirror-beyond-boundary -->

**Approach.**
The scan keeps `center` and `right`, where `right = center + rad[center]` is the farthest right edge of any finished palindrome. For an index `i < right`, the mirror `2 * center - i` has a finished radius, but that palindrome may extend left of the big palindrome, where the reflection argument gives no guarantee. The code therefore starts `rad[i]` at `min(right - i, rad[mirror])` and expands from there. The invariant is that all characters within `rad[i]` of `i` match before the first comparison. The solution also contains an unbounded variant that skips the `min`. The assertions show that this variant returns a wrong radius on `abab` and on `aaabaa`, which is the reason for the clamp.

**Complexity.**
- **Time** is O(n), because `right` never decreases and every successful comparison advances it, which allows at most `2n + 1` successful comparisons plus one failed comparison per index.
- **Space** is O(n), because `t` and `rad` hold `2n + 1` values each.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MirrorClamp {
    /**
     * Builds t with a separator before, between and after the letters.
     * Time: O(n). Space: O(n).
     * Invariant: letter k of s sits at index 2k + 1.
     */
    static char[] withSeparators(String s) {
        // 2n + 1 slots, all separators first.
        char[] t = new char[2 * s.length() + 1];
        Arrays.fill(t, '#');
        // Letters go to the odd indexes.
        for (int k = 0; k < s.length(); k++) t[2 * k + 1] = s.charAt(k);
        return t;
    }

    /**
     * Computes every radius of t with the copy limited by the right edge.
     * Time: O(n), because right only moves forward.
     * Space: O(n) for rad.
     * Invariant: all characters within rad[i] of i match before the first comparison at i.
     */
    static int[] radii(String s, boolean clamp) {
        char[] t = withSeparators(s);
        int m = t.length;
        // rad[i] is final once the scan leaves i.
        int[] rad = new int[m];
        // center is the finished palindrome with the farthest right edge.
        int center = 0, right = 0;
        // One pass over all indexes of t.
        for (int i = 0; i < m; i++) {
            // Only indexes strictly left of the right edge have a usable mirror.
            if (i < right) {
                int mirror = 2 * center - i; // same distance from center on the other side
                // The bounded copy stays inside the known palindrome; the unbounded copy does not.
                rad[i] = clamp ? Math.min(right - i, rad[mirror]) : rad[mirror];
            }
            // Expand while the next outer pair exists and matches.
            while (i - rad[i] - 1 >= 0 && i + rad[i] + 1 < m && t[i - rad[i] - 1] == t[i + rad[i] + 1]) {
                rad[i]++; // each success moves i + rad[i] one step right
            }
            // A palindrome reaching farther right becomes the new reference.
            if (i + rad[i] > right) { center = i; right = i + rad[i]; }
        }
        // The caller reads rad by index.
        return rad;
    }

    /**
     * Oracle: expands every index of t independently.
     * Time: O(n^2) worst case. Space: O(n).
     * Invariant: t[i - k .. i + k] is a palindrome before each comparison.
     */
    static int[] oracle(String s) {
        char[] t = withSeparators(s);
        int[] rad = new int[t.length];
        // Independent expansion at each index, with no reuse.
        for (int i = 0; i < t.length; i++) {
            int k = 0;
            while (i - k - 1 >= 0 && i + k + 1 < t.length && t[i - k - 1] == t[i + k + 1]) k++;
            rad[i] = k;
        }
        return rad;
    }

    public static void main(String[] args) {
        // Example 1: the bounded copy gives 1 at index 7.
        if (!Arrays.equals(radii("abab", true), new int[] {0, 1, 0, 3, 0, 3, 0, 1, 0})) throw new AssertionError("abab");
        // Example 2: the bounded copy gives 1 and 0 at the last two indexes.
        if (!Arrays.equals(radii("aaabaa", true), new int[] {0, 1, 2, 3, 2, 1, 0, 5, 0, 1, 2, 1, 0})) throw new AssertionError("aaabaa");
        // The unbounded copy is wrong on both inputs, so the bound is necessary.
        if (Arrays.equals(radii("abab", false), oracle("abab"))) throw new AssertionError("abab unbounded should differ");
        if (radii("abab", false)[7] != 3) throw new AssertionError("unbounded value at index 7");
        if (radii("aaabaa", false)[11] != 3) throw new AssertionError("unbounded value at index 11");
        // Random strings: the bounded scan must equal the independent expansion.
        Random rnd = new Random(34033);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(16);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!Arrays.equals(radii(s, true), oracle(s))) throw new AssertionError("mismatch on " + s);
        }
        // A long repetitive string finishes and gives the expected maximum radius.
        char[] big = new char[100000];
        Arrays.fill(big, 'a');
        int[] r = radii(new String(big), true);
        if (r[100000] != 100000) throw new AssertionError("center of the long string");
    }
}
```

#### Solution: [Recognize] Longest Palindromic Substring (LeetCode 5)
<!-- id: as-longest-palindrome-radii -->

**Approach.**
The code computes all radii of the separator string with the bounded copy, then scans them once and keeps the first index with the maximum radius. A strict comparison keeps the leftmost center on a tie, and among equal radii a smaller center index gives a smaller start in `s`, so the tie rule holds. The radius at center `i` equals the palindrome length in `s`, and the start is `(i - radius) / 2`. The invariant of the scan is that all characters within `rad[i]` of `i` match before the first comparison, and the invariant of the final pass is that `bestCenter` holds the leftmost index of the largest radius seen so far. The oracle tries every substring start and length with an index-based palindrome test, and no substring is allocated. A last assertion records that a character outside the Basic Multilingual Plane is two Java `char` values, which is why the code treats text as UTF-16 code units.

**Complexity.**
- **Time** is O(n), because the radius scan advances `right` at most `2n + 1` times and the final pass visits each index once.
- **Space** is O(n), because the separator array and the radius array each hold `2n + 1` values.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LongestPalindromeRadii {
    /**
     * Returns {start, length} of the leftmost longest palindromic substring.
     * Time: O(n), because right only moves forward.
     * Space: O(n) for the padded array and the radii.
     * Invariant: bestCenter is the leftmost index holding the largest radius so far.
     */
    static int[] longest(String s) {
        int n = s.length();
        // Padded array: separators before, between and after the letters.
        char[] t = new char[2 * n + 1];
        Arrays.fill(t, '#');
        for (int k = 0; k < n; k++) t[2 * k + 1] = s.charAt(k);
        int m = t.length;
        int[] rad = new int[m];
        int center = 0, right = 0;
        // Scan every index once, left to right.
        for (int i = 0; i < m; i++) {
            // Copy from the mirror, limited to the known right edge.
            if (i < right) rad[i] = Math.min(right - i, rad[2 * center - i]);
            // Expand beyond the known coverage only.
            while (i - rad[i] - 1 >= 0 && i + rad[i] + 1 < m && t[i - rad[i] - 1] == t[i + rad[i] + 1]) rad[i]++;
            // Update the reference palindrome when this one reaches farther right.
            if (i + rad[i] > right) { center = i; right = i + rad[i]; }
        }
        // Pick the first maximum so the leftmost palindrome wins ties.
        int bestCenter = 0;
        for (int i = 1; i < m; i++) if (rad[i] > rad[bestCenter]) bestCenter = i;
        // The radius is the palindrome length in s, and the start follows from the center.
        return new int[] {(bestCenter - rad[bestCenter]) / 2, rad[bestCenter]};
    }

    /**
     * Oracle: tries every start and length, keeping the longest and then leftmost.
     * Time: O(n^3) worst case. Space: O(1).
     * Invariant: bestLen is the longest palindrome length verified so far.
     */
    static int[] oracle(String s) {
        int bestStart = 0, bestLen = 0;
        // Every start index in order, so an earlier start wins on equal length.
        for (int start = 0; start < s.length(); start++) {
            // Every end index from the start.
            for (int end = start; end < s.length(); end++) {
                int len = end - start + 1;
                // Replace only when strictly longer, which keeps the leftmost on ties.
                if (len > bestLen && isPalindrome(s, start, end)) { bestLen = len; bestStart = start; }
            }
        }
        return new int[] {bestStart, bestLen};
    }

    /**
     * Index-based palindrome test with no substring allocation.
     * Time: O(hi - lo). Space: O(1).
     * Invariant: all pairs outside lo..hi have matched.
     */
    static boolean isPalindrome(String s, int lo, int hi) {
        while (lo < hi) if (s.charAt(lo++) != s.charAt(hi--)) return false;
        return true;
    }

    public static void main(String[] args) {
        // Example 1: bab and aba tie at length 3, and bab starts first.
        if (!Arrays.equals(longest("babad"), new int[] {0, 3})) throw new AssertionError("babad");
        // Example 2: abcba and defed tie at length 5, and abcba starts first.
        if (!Arrays.equals(longest("abcbaxdefed"), new int[] {0, 5})) throw new AssertionError("abcbaxdefed");
        // A single character is its own palindrome.
        if (!Arrays.equals(longest("q"), new int[] {0, 1})) throw new AssertionError("single");
        // An even palindrome is found through the gap center.
        if (!Arrays.equals(longest("cbbd"), new int[] {1, 2})) throw new AssertionError("cbbd");
        // Random strings over a small alphabet, compared with the brute-force oracle.
        Random rnd = new Random(34034);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(20);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!Arrays.equals(longest(s), oracle(s))) throw new AssertionError("mismatch on " + s);
        }
        // The long repetitive line from the lesson finishes and returns the whole string.
        char[] big = new char[100000];
        Arrays.fill(big, 'a');
        if (!Arrays.equals(longest(new String(big)), new int[] {0, 100000})) throw new AssertionError("long line");
        // A character outside the Basic Multilingual Plane is two UTF-16 units in a Java String.
        if ("\uD83D\uDE00".length() != 2) throw new AssertionError("surrogate pair length");
    }
}
```
