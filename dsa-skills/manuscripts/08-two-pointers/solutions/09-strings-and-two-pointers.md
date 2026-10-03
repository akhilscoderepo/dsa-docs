<!-- solutions-for: 08-strings-and-two-pointers -->
### Strings And Two Pointers

#### Solution: [Build] Valid Palindrome (LeetCode 125)
<!-- id: tp-clean-palindrome -->

**Approach.** Put `left` at the first position and `right` at the last. While `left < right`, a pointer standing on noise moves one step inward and the loop starts again, so both pointers are on a letter or digit at the moment of comparison. The two characters are lowercased and compared, a difference returns false, and a match moves both pointers. When the pointers meet or cross, every mirror pair has matched and the answer is true, so a phrase of noise only is true. The check compares with the copy, reverse and compare method on random printable text, counts the characters read to show that no more than two per position are touched, and asserts the Java facts the lesson states about `isLetterOrDigit`.

**Complexity.** O(n) time, since each pointer only moves inward, and O(1) extra space.

```java run
import java.util.Random;

public final class CleanPalindrome {
    static int reads;

    static char at(String s, int k) {
        reads++;
        return s.charAt(k);
    }

    static boolean readsSameIgnoringNoise(String phrase) {
        int left = 0, right = phrase.length() - 1;
        while (left < right) {
            if (!Character.isLetterOrDigit(at(phrase, left))) { left++; continue; }
            if (!Character.isLetterOrDigit(at(phrase, right))) { right--; continue; }
            if (Character.toLowerCase(at(phrase, left)) != Character.toLowerCase(at(phrase, right))) return false;
            left++;
            right--;
        }
        return true;
    }

    static boolean oracle(String phrase) {
        StringBuilder card = new StringBuilder();
        for (char c : phrase.toCharArray()) if (Character.isLetterOrDigit(c)) card.append(Character.toLowerCase(c));
        return card.toString().equals(new StringBuilder(card).reverse().toString());
    }

    public static void main(String[] args) {
        if (!readsSameIgnoringNoise("Step on no pets!")) throw new AssertionError("example 1");
        if (!readsSameIgnoringNoise(" . , ")) throw new AssertionError("example 2");
        if (!readsSameIgnoringNoise("") || !readsSameIgnoringNoise("x")) throw new AssertionError("short");
        if (readsSameIgnoringNoise("0P")) throw new AssertionError("digit against letter");
        if (!readsSameIgnoringNoise("Madam, I'm Adam")) throw new AssertionError("trace phrase");
        if (!Character.isLetterOrDigit('é')) throw new AssertionError("isLetterOrDigit accepts non-ASCII letters");
        if (!Character.isLetterOrDigit('7') || Character.isLetterOrDigit(',')) throw new AssertionError("digit or comma");
        Random rnd = new Random(8201);
        String alphabet = "aAbB01 ,.!";
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            reads = 0;
            boolean got = readsSameIgnoringNoise(s);
            if (got != oracle(s)) throw new AssertionError("differs on '" + s + "'");
            if (reads > 2 * n) throw new AssertionError("more than two reads per position on '" + s + "'");
        }
    }
}
```

#### Solution: [Vary] Reverse String (LeetCode 344)
<!-- id: tp-reverse-chars -->

**Approach.** Walk `left` up from the front and `right` down from the back, swapping their characters through one temporary `char` and stopping when `left < right` fails, which leaves the middle of an odd length untouched. The method returns the number of swaps, which is the length divided by two, rounded down. The check keeps a reference to the array that went in and asserts that the same object holds the reversed content, and compares against a reversed copy built with a second array. It also shows that a `String` is not changed when its character array copy is reversed, which is why the contract speaks of `char[]`.

**Complexity.** O(n) time with exactly n / 2 swaps, and O(1) extra space for the temporary.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ReverseChars {
    static int reverseInPlace(char[] chars) {
        int swaps = 0;
        for (int left = 0, right = chars.length - 1; left < right; left++, right--) {
            char keep = chars[left];
            chars[left] = chars[right];
            chars[right] = keep;
            swaps++;
        }
        return swaps;
    }

    public static void main(String[] args) {
        char[] one = {'p', 'o', 'l', 'e', 's'};
        char[] same = one;
        int swaps = reverseInPlace(one);
        if (swaps != 2 || !Arrays.equals(one, new char[] {'s', 'e', 'l', 'o', 'p'}) || same != one) throw new AssertionError("example 1");
        char[] two = {'x'};
        if (reverseInPlace(two) != 0 || !Arrays.equals(two, new char[] {'x'})) throw new AssertionError("example 2");
        if (reverseInPlace(new char[0]) != 0) throw new AssertionError("empty");
        String text = "stressed";
        char[] copy = text.toCharArray();
        reverseInPlace(copy);
        if (!text.equals("stressed") || !new String(copy).equals("desserts")) throw new AssertionError("String must stay unchanged");
        Random rnd = new Random(8202);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(15);
            char[] a = new char[n];
            for (int i = 0; i < n; i++) a[i] = (char) ('a' + rnd.nextInt(rnd.nextBoolean() ? 1 : 26));
            char[] expected = new char[n];
            for (int i = 0; i < n; i++) expected[i] = a[n - 1 - i];
            char[] ref = a;
            int s = reverseInPlace(a);
            if (a != ref || !Arrays.equals(a, expected)) throw new AssertionError("wrong reversal");
            if (s != n / 2) throw new AssertionError("swap count " + s + " for length " + n);
        }
    }
}
```

#### Solution: [Boundary] Valid Palindrome II (LeetCode 680)
<!-- id: tp-palindrome-one-skip -->

**Approach.** Walk in from both ends comparing characters. At the first mismatch, return whether the window with the left character dropped is a plain palindrome, or the window with the right character dropped is. The helper compares only, and has no repair of its own, so a second disagreement inside a window gives false. Only the two ends can be the removed character, since every pair outside the window already matched and the ends of what remains are still those two differing characters. If the walk meets without a mismatch, the answer is true with no deletion. The check compares with an oracle that tries every single deletion and the unchanged string, and counts character comparisons to show that the total stays within three times the length.

**Complexity.** O(n) time, because the main walk and the two window checks each pass over at most n / 2 pairs, and O(1) extra space.

```java run
import java.util.Random;

public final class PalindromeOneSkip {
    static int compares;

    static boolean plainWindow(String s, int left, int right) {
        while (left < right) {
            compares++;
            if (s.charAt(left++) != s.charAt(right--)) return false;
        }
        return true;
    }

    static boolean almostPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            compares++;
            if (s.charAt(left) != s.charAt(right)) {
                return plainWindow(s, left + 1, right) || plainWindow(s, left, right - 1);
            }
            left++;
            right--;
        }
        return true;
    }

    static boolean isPal(String s) {
        return new StringBuilder(s).reverse().toString().equals(s);
    }

    static boolean oracle(String s) {
        if (isPal(s)) return true;
        for (int k = 0; k < s.length(); k++) {
            if (isPal(s.substring(0, k) + s.substring(k + 1))) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (!almostPalindrome("abcxcbda")) throw new AssertionError("example 1");
        if (almostPalindrome("abcdefa")) throw new AssertionError("example 2");
        if (!almostPalindrome("") || !almostPalindrome("a") || !almostPalindrome("ab")) throw new AssertionError("short strings");
        if (almostPalindrome("abc")) throw new AssertionError("abc needs two removals");
        if (almostPalindrome("abcabc")) throw new AssertionError("second repair must not be allowed");
        Random rnd = new Random(8203);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(11);
            int letters = 1 + rnd.nextInt(3);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(letters)));
            String s = sb.toString();
            compares = 0;
            boolean got = almostPalindrome(s);
            if (got != oracle(s)) throw new AssertionError("differs on " + s);
            if (compares > 3 * n + 3) throw new AssertionError("too many compares on " + s + ": " + compares);
        }
        StringBuilder big = new StringBuilder();
        for (int i = 0; i < 50000; i++) big.append('a');
        big.setCharAt(25000, 'b');
        compares = 0;
        if (!almostPalindrome(big.toString())) throw new AssertionError("long string with one stray letter");
        if (compares > 3 * big.length()) throw new AssertionError("long string compares " + compares);
    }
}
```

#### Solution: [Recognize] Is Subsequence (LeetCode 392)
<!-- id: tp-subsequence-rates -->

**Approach.** Keep `matched` for the short text and let `at` run over the long text with no pause. A position of the long text that equals the short text's next needed character advances `matched`. The loop ends when the long text is spent or when `matched` reaches the short length, and the answer is whether it did. Taking the earliest match each time is safe because any later occurrence leaves fewer characters for the rest, so an exchange argument shows that the earliest choice never loses a match. The oracle fills the standard table of prefixes, and the check also counts reads to show that scanning stops at the moment the short text is complete.

**Complexity.** O(n) time in the length of the long text and O(1) extra space, with the table used only by the oracle.

```java run
import java.util.Random;

public final class SubsequenceRates {
    static int reads;

    static boolean appearsInOrder(String small, String large) {
        int matched = 0;
        for (int at = 0; at < large.length() && matched < small.length(); at++) {
            reads++;
            if (large.charAt(at) == small.charAt(matched)) matched++;
        }
        return matched == small.length();
    }

    static boolean oracle(String small, String large) {
        boolean[][] ok = new boolean[small.length() + 1][large.length() + 1];
        for (int j = 0; j <= large.length(); j++) ok[0][j] = true;
        for (int i = 1; i <= small.length(); i++) {
            for (int j = 1; j <= large.length(); j++) {
                ok[i][j] = ok[i][j - 1] || (small.charAt(i - 1) == large.charAt(j - 1) && ok[i - 1][j - 1]);
            }
        }
        return ok[small.length()][large.length()];
    }

    public static void main(String[] args) {
        if (!appearsInOrder("ace", "abcde")) throw new AssertionError("example 1");
        if (appearsInOrder("aec", "abcde")) throw new AssertionError("example 2");
        if (!appearsInOrder("", "") || !appearsInOrder("", "abc")) throw new AssertionError("empty small text");
        if (appearsInOrder("a", "")) throw new AssertionError("empty large text");
        reads = 0;
        StringBuilder sb = new StringBuilder("a");
        for (int i = 0; i < 100000; i++) sb.append('z');
        if (!appearsInOrder("a", sb.toString()) || reads != 1) throw new AssertionError("must stop once complete, reads " + reads);
        Random rnd = new Random(8204);
        for (int t = 0; t < 6000; t++) {
            StringBuilder a = new StringBuilder(), b = new StringBuilder();
            int letters = 1 + rnd.nextInt(3);
            for (int i = rnd.nextInt(5); i > 0; i--) a.append((char) ('a' + rnd.nextInt(letters)));
            for (int i = rnd.nextInt(10); i > 0; i--) b.append((char) ('a' + rnd.nextInt(letters)));
            reads = 0;
            boolean got = appearsInOrder(a.toString(), b.toString());
            if (got != oracle(a.toString(), b.toString())) throw new AssertionError("differs on " + a + " in " + b);
            if (reads > b.length()) throw new AssertionError("more reads than the long text has");
        }
    }
}
```
