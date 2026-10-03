<!-- solutions-for: 07-center-expansion -->
### Center Expansion

#### Solution: [Build] Palindromic Substrings (LeetCode 647)
<!-- id: st-palindromic-substrings -->

**Approach.** Try all `n` odd centers and all `n - 1` even centers. For each, move the boundaries outward while they stay inside the string and the characters match, adding one for every successful step, since each step is a distinct symmetric substring. The brute force reverses every substring and compares it, and it serves as the oracle on random strings over a small alphabet, where long palindromes are common.

**Complexity.** O(n * n) time and O(1) extra space.

```java run
import java.util.Random;

public final class PalindromicSubstrings {
    static int expandCount(String s, int left, int right) {
        int found = 0;
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) { found++; left--; right++; }
        return found;
    }
    static int countPalindromes(String s) {
        int total = 0;
        for (int c = 0; c < s.length(); c++) {
            total += expandCount(s, c, c);
            total += expandCount(s, c, c + 1);
        }
        return total;
    }
    static int oracle(String s) {
        int total = 0;
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 1; j <= s.length(); j++) {
                String p = s.substring(i, j);
                if (p.equals(new StringBuilder(p).reverse().toString())) total++;
            }
        return total;
    }

    public static void main(String[] args) {
        if (countPalindromes("abc") != 3) throw new AssertionError("example 1");
        if (countPalindromes("aaa") != 6) throw new AssertionError("example 2");
        if (countPalindromes("abba") != 6) throw new AssertionError("abba has six");
        Random rnd = new Random(71);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(14);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (countPalindromes(s) != oracle(s)) throw new AssertionError("disagrees with the oracle on " + s);
        }
    }
}
```

#### Solution: [Vary] Longest Palindromic Substring (LeetCode 5)
<!-- id: st-longest-palindromic -->

**Approach.** Run the same walks but measure each finished expansion as `right - left - 1`, the width of the last symmetric stretch. Compare the better of the odd and even lengths against the best so far, with a strict comparison so that earlier starts win ties, and compute the start as `c - (len - 1) / 2`. The answer is cut out once at the end. The oracle checks every substring from the longest length downward and from the earliest start, and the assertions require the same string, which also confirms the tie rule.

**Complexity.** O(n * n) time and O(1) extra space apart from the returned substring.

```java run
import java.util.Random;

public final class LongestPalindromic {
    static int expandLength(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) { left--; right++; }
        return right - left - 1;
    }
    static String longestPalindrome(String s) {
        int bestStart = 0, bestLen = 0;
        for (int c = 0; c < s.length(); c++) {
            int len = Math.max(expandLength(s, c, c), expandLength(s, c, c + 1));
            if (len > bestLen) { bestLen = len; bestStart = c - (len - 1) / 2; }
        }
        return s.substring(bestStart, bestStart + bestLen);
    }
    static boolean isPal(String p) { return p.equals(new StringBuilder(p).reverse().toString()); }
    static String oracle(String s) {
        for (int len = s.length(); len >= 1; len--)
            for (int i = 0; i + len <= s.length(); i++)
                if (isPal(s.substring(i, i + len))) return s.substring(i, i + len);
        return "";
    }

    public static void main(String[] args) {
        if (!longestPalindrome("dcbabcx").equals("cbabc")) throw new AssertionError("example 1");
        if (!longestPalindrome("ac").equals("a")) throw new AssertionError("example 2");
        if (!longestPalindrome("abba").equals("abba")) throw new AssertionError("even whole string");
        if (!longestPalindrome("").isEmpty()) throw new AssertionError("empty string");
        Random rnd = new Random(72);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(16);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!longestPalindrome(s).equals(oracle(s))) throw new AssertionError("disagrees with the oracle on " + s);
        }
    }
}
```

#### Solution: [Boundary] Even Center (Author exercise)
<!-- id: st-even-center -->

**Approach.** For each gap between index `c` and `c + 1`, start `left = c` and `right = c + 1` and expand while the characters match, counting each step. A walk that starts with both boundaries on one character always has odd width, so it can never reach the width-2 stretch `bb` or the width-4 stretch `abba`. At the last index the right boundary is outside the string, so the walk stops at once with a count of zero, and the loop may simply stop one index earlier. The assertions compare the count with a brute force over even-length substrings, and show that an odd-only counter finds none in `abba`.

**Complexity.** O(n * n) time and O(1) extra space.

```java run
import java.util.Random;

public final class EvenCenter {
    static int expandCount(String s, int left, int right) {
        int found = 0;
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) { found++; left--; right++; }
        return found;
    }
    static int evenPalindromes(String s) {
        int total = 0;
        for (int c = 0; c + 1 < s.length(); c++) total += expandCount(s, c, c + 1);
        return total;
    }
    static int oddOnlyWronglyEven(String s) {              // counts walks from one character, keeping only even widths
        int total = 0;
        for (int c = 0; c < s.length(); c++) {
            int steps = expandCount(s, c, c);
            for (int k = 1; k <= steps; k++) if ((2 * k - 1) % 2 == 0) total++;
        }
        return total;
    }
    static int oracle(String s) {
        int total = 0;
        for (int i = 0; i < s.length(); i++)
            for (int j = i + 2; j <= s.length(); j += 2) {
                String p = s.substring(i, j);
                if (p.equals(new StringBuilder(p).reverse().toString())) total++;
            }
        return total;
    }

    public static void main(String[] args) {
        if (evenPalindromes("abba") != 2) throw new AssertionError("example 1");
        if (evenPalindromes("abc") != 0) throw new AssertionError("example 2");
        if (evenPalindromes("") != 0 || evenPalindromes("z") != 0) throw new AssertionError("no gap centers");
        if (oddOnlyWronglyEven("abba") != 0) throw new AssertionError("odd centers cannot find even palindromes");
        Random rnd = new Random(73);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(16);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (evenPalindromes(s) != oracle(s)) throw new AssertionError("disagrees with the oracle on " + s);
        }
    }
}
```

#### Solution: [Recognize] Longest Even-Length Palindrome (Author exercise)
<!-- id: st-longest-even-palindrome -->

**Approach.** Try only the gap centers. For each, expand and measure the width as `right - left - 1`, which is even, and keep the longest with a strict comparison so the earliest wins ties. The start is `c - len / 2 + 1`, since a gap center at `c` with width `len` covers `len / 2` characters to its left, including `c`. A best width of zero means no two neighbours match, and the answer is the empty string. The oracle checks even lengths from the longest down, earliest start first, and the assertions require identical strings.

**Complexity.** O(n * n) time and O(1) extra space apart from the returned substring.

```java run
import java.util.Random;

public final class LongestEvenPalindrome {
    static int expandLength(String s, int left, int right) {
        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) { left--; right++; }
        return right - left - 1;
    }
    static String longestEven(String s) {
        int bestStart = 0, bestLen = 0;
        for (int c = 0; c + 1 < s.length(); c++) {
            int len = expandLength(s, c, c + 1);
            if (len > bestLen) { bestLen = len; bestStart = c - len / 2 + 1; }
        }
        return s.substring(bestStart, bestStart + bestLen);
    }
    static String oracle(String s) {
        for (int len = s.length() - s.length() % 2; len >= 2; len -= 2)
            for (int i = 0; i + len <= s.length(); i++) {
                String p = s.substring(i, i + len);
                if (p.equals(new StringBuilder(p).reverse().toString())) return p;
            }
        return "";
    }

    public static void main(String[] args) {
        if (!longestEven("xabbay").equals("abba")) throw new AssertionError("example 1");
        if (!longestEven("abcd").isEmpty()) throw new AssertionError("example 2");
        if (!longestEven("").isEmpty() || !longestEven("q").isEmpty()) throw new AssertionError("too short for a gap center");
        if (!longestEven("aabbaa").equals("aabbaa")) throw new AssertionError("whole string");
        Random rnd = new Random(74);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(18);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!longestEven(s).equals(oracle(s))) throw new AssertionError("disagrees with the oracle on " + s);
        }
    }
}
```
