<!-- solutions-for: 03-strings -->
### Solutions For Palindrome Expansion

#### Solution: [Build] Palindromic Substrings (LeetCode 647)
<!-- id: st-palindromic-substrings -->

**Approach.**
The method visits every middle: an odd center at each index `c` and a gap between `c` and `c + 1`. For one middle, a helper widens the ends while they match and adds 1 for every successful step, because each successful step proves one more palindromic substring around that middle. The loop adds the helper results over all middles. Every palindromic substring has exactly one middle, so no substring is counted twice. The invariant is that the helper's count equals the number of palindromes around the fixed middle that its loop has verified so far. The harness also asserts the cost claims and the examples from the lesson text.

**Complexity.**
- **Time** is O(n^2) in the worst case, because each of the `2n` middles widens at most about `n / 2` times, and a string of equal letters reaches that bound.
- **Space** is O(1), because the helper keeps two indexes and a counter.

```java run
import java.util.Random;

public final class PalindromicSubstrings {
    /**
     * Counts the palindromes around the middle that starts at (left, right).
     * Time: O(n) per call. Space: O(1).
     * Invariant: m equals the number of verified palindromes around the fixed middle.
     */
    static int matches(String s, int left, int right) {
        int m = 0;
        // The bounds are tested before charAt, so no index outside the string is read.
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            // A successful pair proves one more palindrome around the same middle.
            m++;
            // Both ends move outward by one, so the middle stays fixed.
            left--;
            right++;
        }
        return m;
    }

    /**
     * Counts all palindromic substrings of s by position.
     * Time: O(n^2) worst case. Space: O(1).
     * Invariant: count equals the palindromes whose middle is before the current index plus the odd center at c.
     */
    static int countSubstrings(String s) {
        int count = 0;
        // The loop visits n indexes, and each index owns one odd center and one gap.
        for (int c = 0; c < s.length(); c++) {
            // The odd center starts with both ends on the same character.
            count += matches(s, c, c);
            // The gap starts with the two neighbors c and c + 1; the last gap returns 0 at once.
            count += matches(s, c, c + 1);
        }
        return count;
    }

    /** Lesson code: the expansion method that returns a length, and its counter-instrumented twin. */
    static int expand(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) { left--; right++; }
        return right - left - 1;
    }

    static long rounds(String s) {
        long total = 0;
        for (int c = 0; c < s.length(); c++) {
            total += matches(s, c, c) + matches(s, c, c + 1);
        }
        return total;
    }

    static int naiveLongest(String s) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            for (int j = i + 1; j <= s.length(); j++) {
                String part = s.substring(i, j);
                if (part.equals(new StringBuilder(part).reverse().toString())) best = Math.max(best, part.length());
            }
        }
        return best;
    }

    static int longest(String s) {
        int best = 0;
        for (int c = 0; c < s.length(); c++) {
            best = Math.max(best, expand(s, c, c));
            best = Math.max(best, expand(s, c, c + 1));
        }
        return best;
    }

    /** Oracle: tests every substring against its reverse. */
    static int oracle(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 1; j <= s.length(); j++) {
                String p = s.substring(i, j);
                if (p.equals(new StringBuilder(p).reverse().toString())) count++;
            }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (countSubstrings("level") != 7) throw new AssertionError("example 1");
        if (countSubstrings("ab") != 2) throw new AssertionError("example 2");
        if (countSubstrings("aaa") != 6) throw new AssertionError("equal letters");
        // Random strings are checked against the oracle.
        Random rnd = new Random(71);
        for (int t = 0; t < 600; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (countSubstrings(s) != oracle(s)) throw new AssertionError("random " + s);
            if (longest(s) != naiveLongest(s)) throw new AssertionError("longest " + s);
        }
        // Lesson claim: the examples of the lesson text.
        if (longest("abba") != 4 || longest("abc") != 1 || longest("") != 0) throw new AssertionError("lesson examples");
        if (longest("aba") != 3) throw new AssertionError("trace 1");
        // Lesson claim: n(n + 1) / 2 substrings and n(n + 1)(n + 2) / 6 reversal operations for n = 2000.
        long substrings = 0, operations = 0;
        for (int i = 0; i < 2000; i++) for (int j = i + 1; j <= 2000; j++) { substrings++; operations += j - i; }
        if (substrings != 2000L * 2001 / 2 || operations != 2000L * 2001 * 2002 / 6) throw new AssertionError("naive cost model");
        // Lesson claim: a string has n odd centers plus n - 1 gaps, which is 2n - 1 middles.
        int n = 9;
        if (n + (n - 1) != 2 * n - 1) throw new AssertionError("middle count");
        // Lesson claim: equal letters give quadratic growth, so doubling n multiplies the work by about 4.
        long r1 = rounds("a".repeat(200)), r2 = rounds("a".repeat(400));
        double ratio = (double) r2 / r1;
        if (ratio < 3.5 || ratio > 4.5) throw new AssertionError("growth ratio " + ratio);
        // Lesson claim: the last gap returns 0 at once, and an index outside the string is never read.
        if (expand("a", 0, 1) != 0) throw new AssertionError("last gap");
        if (matches("a", 0, 1) != 0 || matches("", 0, 1) != 0) throw new AssertionError("bounds");
        // Lesson claim: substring includes the first index and excludes the second.
        if (!"abcd".substring(1, 3).equals("bc")) throw new AssertionError("substring bounds");
    }
}
```

#### Solution: [Vary] Longest Palindromic Substring (LeetCode 5)
<!-- id: st-longest-palindrome -->

**Approach.**
The method tries every odd center and every gap and keeps the best interval, not only the best length. For a middle that starts at index `c`, the expansion returns the length `len` of the palindrome. The start index is `c - (len - 1) / 2` for both kinds of middle, with integer division. An odd length `2k + 1` starts at `c - k`, and an even length `2k` starts at `c - k + 1`. The method replaces the best interval only when `len` is strictly larger, and it visits middles in increasing position, so the leftmost palindrome wins a tie. The invariant is that `bestStart` and `bestLen` describe the longest palindrome around the middles tried so far.

**Complexity.**
- **Time** is O(n^2) in the worst case, because there are `2n` middles and each expansion runs at most about `n / 2` rounds.
- **Space** is O(1) besides the returned substring, because the method keeps a few integers.

```java run
import java.util.Random;

public final class LongestPalindrome {
    /**
     * Returns the length of the palindrome around the middle that starts at (left, right).
     * Time: O(n). Space: O(1). Invariant: s[left + 1 .. right - 1] is a palindrome at every test.
     */
    static int expand(String s, int left, int right) {
        // The bounds come first, so charAt never reads outside the string.
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            // A matching pair moves both ends outward, and the middle stays fixed.
            left--;
            right++;
        }
        // The ends stopped one step beyond the palindrome, so its length is right - left - 1.
        return right - left - 1;
    }

    /**
     * Returns the leftmost longest palindromic substring of a non-empty string.
     * Time: O(n^2). Space: O(1) besides the result.
     * Invariant: bestStart and bestLen describe the longest palindrome among the middles tried so far.
     */
    static String longestPalindrome(String s) {
        int bestStart = 0, bestLen = 0;
        // The loop visits each index, and each index owns one odd center and one gap.
        for (int c = 0; c < s.length(); c++) {
            for (int kind = 0; kind < 2; kind++) {
                // kind 0 is the odd center at c, and kind 1 is the gap between c and c + 1.
                int len = expand(s, c, c + kind);
                // A strict comparison keeps the earlier palindrome on a tie.
                if (len > bestLen) {
                    bestLen = len;
                    // The same formula gives the start for odd and even lengths with integer division.
                    bestStart = c - (len - 1) / 2;
                }
            }
        }
        // The interval is [bestStart, bestStart + bestLen), which substring reads with an exclusive end.
        return s.substring(bestStart, bestStart + bestLen);
    }

    /** Oracle: tests every substring and keeps the longest, preferring the smaller start. */
    static String oracle(String s) {
        String best = "";
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 1; j <= s.length(); j++) {
                String p = s.substring(i, j);
                if (p.length() > best.length() && p.equals(new StringBuilder(p).reverse().toString())) best = p;
            }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!longestPalindrome("xabacd").equals("aba")) throw new AssertionError("example 1");
        if (!longestPalindrome("ac").equals("a")) throw new AssertionError("example 2");
        // An even answer, a whole-string answer and a single character.
        if (!longestPalindrome("cbbd").equals("bb")) throw new AssertionError("even answer");
        if (!longestPalindrome("racecar").equals("racecar")) throw new AssertionError("whole string");
        if (!longestPalindrome("z").equals("z")) throw new AssertionError("single character");
        // Random strings are checked against the oracle, including the leftmost tie rule.
        Random rnd = new Random(72);
        for (int t = 0; t < 1000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!longestPalindrome(s).equals(oracle(s))) throw new AssertionError("random " + s);
        }
    }
}
```

#### Solution: [Boundary] Even Center (Author exercise)
<!-- id: st-even-center -->

**Approach.**
Only gaps can produce an even-length palindrome, so the method starts every attempt with `left = c` and `right = c + 1`. The first test compares the two neighbors, and a mismatch ends the attempt with no palindrome. Each successful pair adds one even palindrome around that gap, since the pair `(c - k, c + 1 + k)` proves the substring of length `2k + 2`. Odd centers are never tried. The invariant is that after each successful step, the added count equals the even palindromes around the fixed gap that the loop has verified.

**Complexity.**
- **Time** is O(n^2) in the worst case, because there are `n - 1` gaps and each widens at most about `n / 2` times.
- **Space** is O(1), because the method keeps two indexes and a counter.

```java run
import java.util.Random;

public final class EvenCenter {
    /**
     * Counts the even-length palindromic substrings of s.
     * Time: O(n^2) worst case. Space: O(1).
     * Invariant: count equals the even palindromes around the gaps before c plus the verified part of gap c.
     */
    static int countEven(String s) {
        int count = 0;
        // The loop visits each index c, and the gap after c lies between c and c + 1.
        for (int c = 0; c < s.length(); c++) {
            // A gap starts with the two neighbors, so the first test compares s[c] and s[c + 1].
            int left = c, right = c + 1;
            // The bounds are tested first, and a mismatch ends the attempt.
            while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
                // Each matching pair proves one even palindrome of length right - left + 1.
                count++;
                left--;
                right++;
            }
        }
        // The empty string and strings without equal neighbors return 0.
        return count;
    }

    /** Oracle: tests every substring of even length against its reverse. */
    static int oracle(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 2; j <= s.length(); j += 2) {
                String p = s.substring(i, j);
                if (p.equals(new StringBuilder(p).reverse().toString())) count++;
            }
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (countEven("abba") != 2) throw new AssertionError("example 1");
        if (countEven("aaaa") != 4) throw new AssertionError("example 2");
        // No equal neighbors, an empty string and one character.
        if (countEven("abc") != 0 || countEven("") != 0 || countEven("a") != 0) throw new AssertionError("no even palindrome");
        // An odd palindrome has no even one inside it unless neighbors match.
        if (countEven("aba") != 0) throw new AssertionError("odd palindrome only");
        // Random strings are checked against the oracle.
        Random rnd = new Random(73);
        for (int t = 0; t < 1000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(13);
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (countEven(s) != oracle(s)) throw new AssertionError("random " + s);
        }
    }
}
```

#### Solution: [Recognize] Longest Even-Length Palindrome (Author exercise)
<!-- id: st-longest-even-palindrome -->

**Approach.**
The method keeps the expansion invariant of the lesson and changes the starting boundaries. Every attempt starts at the gap `(c, c + 1)`, so every result has even length. The helper returns the length `len`, which equals `2k` for `k` matched pairs. The start index is `c - len / 2 + 1`, because the left end moved down `k - 1` steps from `c` beyond the first pair. The method replaces the best interval only for a strictly larger length, and it visits gaps from left to right, so the leftmost palindrome wins a tie. When no gap matches, the best length stays 0 and the method returns the empty string.

**Complexity.**
- **Time** is O(n^2) in the worst case, because there are `n - 1` gaps and each widens at most about `n / 2` times.
- **Space** is O(1) besides the returned substring.

```java run
import java.util.Random;

public final class LongestEvenPalindrome {
    /**
     * Returns the length of the even palindrome around the gap between c and c + 1.
     * Time: O(n). Space: O(1). Invariant: s[left + 1 .. right - 1] is an even palindrome at every test.
     */
    static int expandGap(String s, int c) {
        // The first pair is the two neighbors around the gap.
        int left = c, right = c + 1;
        // The bounds come first, so charAt never reads outside the string.
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        // The length is the span strictly between the stopped ends.
        return right - left - 1;
    }

    /**
     * Returns the leftmost longest even-length palindromic substring, or "".
     * Time: O(n^2). Space: O(1) besides the result.
     * Invariant: bestStart and bestLen describe the longest even palindrome among the gaps tried so far.
     */
    static String longestEven(String s) {
        int bestStart = 0, bestLen = 0;
        // The loop visits each gap once; the last index has no right neighbor and returns 0.
        for (int c = 0; c < s.length(); c++) {
            int len = expandGap(s, c);
            // A strict comparison keeps the earlier palindrome on a tie.
            if (len > bestLen) {
                bestLen = len;
                // An even length 2k starts k - 1 steps left of c.
                bestStart = c - len / 2 + 1;
            }
        }
        // A best length of 0 gives the empty substring.
        return s.substring(bestStart, bestStart + bestLen);
    }

    /** Oracle: tests every even-length substring and keeps the longest, preferring the smaller start. */
    static String oracle(String s) {
        String best = "";
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 2; j <= s.length(); j += 2) {
                String p = s.substring(i, j);
                if (p.length() > best.length() && p.equals(new StringBuilder(p).reverse().toString())) best = p;
            }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!longestEven("xabbay").equals("abba")) throw new AssertionError("example 1");
        if (!longestEven("abc").equals("")) throw new AssertionError("example 2");
        // Empty input, equal letters and a tie that the leftmost rule decides.
        if (!longestEven("").equals("")) throw new AssertionError("empty");
        if (!longestEven("aaaaa").equals("aaaa")) throw new AssertionError("equal letters");
        if (!longestEven("aabcc").equals("aa")) throw new AssertionError("leftmost tie");
        // Random strings are checked against the oracle.
        Random rnd = new Random(74);
        for (int t = 0; t < 1000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(13);
            for (int k = 0; k < len; k++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!longestEven(s).equals(oracle(s))) throw new AssertionError("random " + s);
        }
    }
}
```
