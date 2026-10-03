<!-- solutions-for: 01-indexed-scans -->
### Indexed Scans

#### Solution: [Build] Count Digits (Author exercise)
<!-- id: st-count-digits -->

**Approach.** Move an index over the string once, read each character with `charAt`, and increment a counter when the character lies between `'0'` and `'9'`. The range test is used instead of `Character.isDigit` because `isDigit` also accepts digits of other scripts, which the contract does not call decimal digits. The assertions show that difference with an Arabic-Indic digit, and compare the scan with a stream-based count on random ASCII strings.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class CountDigits {
    static int countDigits(String s) {
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') count++;
        }
        return count;
    }

    public static void main(String[] args) {
        if (countDigits("a1b2") != 2) throw new AssertionError("example 1");
        if (countDigits("") != 0) throw new AssertionError("example 2");
        char arabicThree = '٣';
        if (!Character.isDigit(arabicThree)) throw new AssertionError("Character.isDigit accepts non-ASCII digits");
        if (countDigits("" + arabicThree) != 0) throw new AssertionError("the range test counts ASCII digits only");
        Random rnd = new Random(201);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(20);
            for (int i = 0; i < n; i++) sb.append((char) (32 + rnd.nextInt(95)));
            String s = sb.toString();
            long expected = s.chars().filter(ch -> ch >= '0' && ch <= '9').count();
            if (countDigits(s) != expected) throw new AssertionError("disagrees with the stream count on: " + s);
        }
    }
}
```

#### Solution: [Vary] Length of Last Word (LeetCode 58)
<!-- id: st-length-last-word -->

**Approach.** Scan from the end. First skip spaces, because trailing spaces belong to no word. Then count characters until a space or the start of the string, which ends the word. The count is the length of the last word. Scanning from the front would need to remember the length of the most recent word and reset it at each space, and would still have to ignore trailing spaces. The assertions compare with the split-based method on random strings of letters and spaces.

**Complexity.** O(n) time in the worst case and O(1) extra space.

```java run
import java.util.Random;

public final class LengthOfLastWord {
    static int lengthOfLastWord(String s) {
        int i = s.length() - 1;
        while (i >= 0 && s.charAt(i) == ' ') i--;
        int length = 0;
        while (i >= 0 && s.charAt(i) != ' ') { length++; i--; }
        return length;
    }
    static int oracle(String s) {
        String[] words = s.trim().split(" +");
        return words[words.length - 1].length();
    }

    public static void main(String[] args) {
        if (lengthOfLastWord("  moon rise  ") != 4) throw new AssertionError("example 1");
        if (lengthOfLastWord("a") != 1) throw new AssertionError("example 2");
        Random rnd = new Random(202);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(14);
            boolean letter = false;
            for (int i = 0; i < n; i++) {
                char c = rnd.nextInt(3) == 0 ? ' ' : (char) ('a' + rnd.nextInt(3));
                if (c != ' ') letter = true;
                sb.append(c);
            }
            if (!letter) sb.append('z');
            String s = sb.toString();
            if (lengthOfLastWord(s) != oracle(s)) throw new AssertionError("disagrees with the split method on: [" + s + "]");
        }
    }
}
```

#### Solution: [Boundary] First Delimiter (Author exercise)
<!-- id: st-first-delimiter -->

**Approach.** Read each character by index and return the index of the first colon. If the loop finishes, every position has been examined and none matched, so the answer is -1. A colon at index 0 needs no special case, because the first iteration tests it. The suffix-based version from the lesson returns the same answers, but its cost grows quadratically, since each `substring` copies the rest of the string. The assertions compare the scan with `String.indexOf` and with the suffix version on random strings, and count the characters that the suffix version copies to confirm the quadratic total.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class FirstDelimiter {
    static int firstDelimiter(String s) {
        for (int i = 0; i < s.length(); i++) if (s.charAt(i) == ':') return i;
        return -1;
    }
    static long copiedBySuffix;
    static int bySuffix(String s) {
        for (int i = 0; i < s.length(); i++) {
            copiedBySuffix += s.length() - i;
            if (s.substring(i).startsWith(":")) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (firstDelimiter(":x") != 0) throw new AssertionError("example 1");
        if (firstDelimiter("abc") != -1) throw new AssertionError("example 2");
        if (firstDelimiter("a:b:c") != 1) throw new AssertionError("the first of several colons");
        if (firstDelimiter("") != -1) throw new AssertionError("empty string");
        copiedBySuffix = 0;
        String noColon = "x".repeat(1000);
        if (bySuffix(noColon) != -1) throw new AssertionError("suffix version on no colon");
        if (copiedBySuffix != 1000L * 1001 / 2) throw new AssertionError("suffix version copies n(n+1)/2 characters: " + copiedBySuffix);
        Random rnd = new Random(203);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(12);
            for (int i = 0; i < n; i++) sb.append(rnd.nextInt(4) == 0 ? ':' : (char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (firstDelimiter(s) != s.indexOf(':')) throw new AssertionError("disagrees with indexOf");
            if (bySuffix(s) != s.indexOf(':')) throw new AssertionError("suffix version disagrees");
        }
    }
}
```

#### Solution: [Recognize] To Lower Case (LeetCode 709)
<!-- id: st-to-lower-case -->

**Approach.** Each output character depends only on the input character at the same index, so one pass over a character array is enough. An uppercase ASCII letter is shifted by the distance between `'a'` and `'A'`, which is 32, and every other character is copied as it is. The arithmetic produces an `int`, so the result is cast back to `char`. The assertions compare with `String.toLowerCase` on printable ASCII, where the two agree, and check that the length never changes.

**Complexity.** O(n) time and O(n) space for the output array.

```java run
import java.util.Locale;
import java.util.Random;

public final class ToLowerCase {
    static String toLowerAscii(String s) {
        char[] out = new char[s.length()];
        for (int i = 0; i < out.length; i++) {
            char c = s.charAt(i);
            out[i] = (c >= 'A' && c <= 'Z') ? (char) (c + ('a' - 'A')) : c;
        }
        return new String(out);
    }

    public static void main(String[] args) {
        if (!toLowerAscii("JavaOne 21!").equals("javaone 21!")) throw new AssertionError("example 1");
        if (!toLowerAscii("already lower").equals("already lower")) throw new AssertionError("example 2");
        if ('a' - 'A' != 32) throw new AssertionError("the case distance is 32");
        Random rnd = new Random(204);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(30);
            for (int i = 0; i < n; i++) sb.append((char) (32 + rnd.nextInt(95)));
            String s = sb.toString();
            String got = toLowerAscii(s);
            if (!got.equals(s.toLowerCase(Locale.ROOT))) throw new AssertionError("disagrees with toLowerCase on: " + s);
            if (got.length() != s.length()) throw new AssertionError("length must not change");
        }
    }
}
```
