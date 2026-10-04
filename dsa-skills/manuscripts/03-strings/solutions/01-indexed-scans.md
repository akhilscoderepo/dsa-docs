<!-- solutions-for: 03-strings -->
### Solutions For Scan A String By Index

#### Solution: [Build] Count Digits (Author exercise)
<!-- id: st-count-digits -->

**Approach.**
The loop visits each index once and compares the character with the range `'0'` to `'9'`. The library call `Character.isDigit` is a poor fit, because it also accepts digits from other scripts, and the statement counts only the ten ASCII digits. The invariant is that after the iteration for index `i`, `count` equals the number of digits among the first `i + 1` characters. The empty string never enters the loop, so the answer 0 needs no special case.

**Complexity.**
- **Time** is O(n), because the loop reads each of the n characters exactly once.
- **Space** is O(1), because the method keeps one counter and one index.

```java run
import java.util.Random;

public final class CountDigits {
    /**
     * Counts the characters in the range '0' to '9'.
     * Time: O(n), one read per character. Space: O(1), one counter.
     * Invariant: after index i, count equals the digits among s[0..i].
     */
    static int countDigits(String s) {
        // The counter starts at 0, which is also the answer for the empty string.
        int count = 0;
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            // A range comparison on the char value accepts only the ten ASCII digits.
            if (s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                // Each digit adds one, so this line runs at most n times.
                count++;
            }
        }
        // The counter now covers the whole string.
        return count;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (countDigits("r2d2!") != 2) throw new AssertionError("example 1");
        if (countDigits("") != 0) throw new AssertionError("example 2");
        // The library call accepts an Arabic-Indic digit, which the statement does not count.
        if (!Character.isDigit('٣')) throw new AssertionError("isDigit accepts other scripts");
        if (countDigits("٣") != 0) throw new AssertionError("only ASCII digits count");
        // Random strings are checked against a regular-expression oracle.
        Random rnd = new Random(11);
        String pool = "ab 09:Z!x7";
        for (int t = 0; t < 400; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            if (countDigits(s) != s.replaceAll("[^0-9]", "").length()) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Length Of The Last Word (LeetCode 58)
<!-- id: st-last-word -->

**Approach.**
The loop keeps `len`, the length of the most recent word seen so far. A letter that follows a space, or sits at index 0, starts a new word and resets `len` to 1. A letter that follows another letter extends the word, so `len` grows by one. A space changes nothing, which keeps the last word's length intact when trailing spaces follow it. The invariant is that after index `i`, `len` equals the length of the latest word that starts at or before `i`.

**Complexity.**
- **Time** is O(n), because each of the n characters is read once and each read costs constant time.
- **Space** is O(1), because the method keeps the length and the index only.

```java run
import java.util.Random;

public final class LastWord {
    /**
     * Returns the length of the last word of a string of letters and spaces.
     * Time: O(n), one pass. Space: O(1), one length.
     * Invariant: after index i, len is the length of the latest word starting at or before i.
     */
    static int lastWordLength(String s) {
        // len holds the length of the latest word; the statement guarantees one word exists.
        int len = 0;
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            // Only letters change the length; a space leaves the latest word untouched.
            if (s.charAt(i) != ' ') {
                // The index test comes first so charAt(i - 1) never runs at index 0.
                if (i == 0 || s.charAt(i - 1) == ' ') {
                    // A letter after a space starts a new word of length 1.
                    len = 1;
                } else {
                    // A letter after a letter extends the current word by one.
                    len++;
                }
            }
        }
        // After the last index, len is the length of the last word.
        return len;
    }

    public static void main(String[] args) {
        // The statement examples; the first has trailing spaces.
        if (lastWordLength("go home  ") != 4) throw new AssertionError("example 1");
        if (lastWordLength("a") != 1) throw new AssertionError("example 2");
        // Leading spaces and a single word surrounded by spaces.
        if (lastWordLength("   ab ") != 2) throw new AssertionError("spaces on both sides");
        // Random strings with at least one letter are checked against a split-based oracle.
        Random rnd = new Random(12);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append(rnd.nextInt(3) == 0 ? 'x' : (rnd.nextBoolean() ? ' ' : 'y'));
            if (sb.indexOf("x") < 0 && sb.indexOf("y") < 0) sb.append('x');
            String s = sb.toString();
            String[] parts = s.trim().split(" +");
            if (lastWordLength(s) != parts[parts.length - 1].length()) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] First Delimiter (Author exercise)
<!-- id: st-first-delim -->

**Approach.**
The loop reads characters from index 0 and returns the index of the first colon at once. Returning inside the loop is correct, because no smaller index can match after the loop passed it. When the loop ends without a match, the method returns `-1`, the value the statement reserves for no colon. The invariant is that when the loop reaches index `i`, no index below `i` holds a colon.

**Complexity.**
- **Time** is O(n) in the worst case, which happens when no colon exists or the colon is last. A colon at index k stops the loop after k + 1 reads.
- **Space** is O(1), because the method keeps one index.

```java run
import java.util.Random;

public final class FirstDelimiter {
    /**
     * Returns the first index of ':' or -1.
     * Time: O(n) worst case, O(k + 1) when the colon sits at index k. Space: O(1).
     * Invariant: when the loop reaches index i, no index below i holds a colon.
     */
    static int firstColon(String s) {
        // The loop runs at most n times and leaves early on the first match.
        for (int i = 0; i < s.length(); i++) {
            // The first match is the smallest index, so the method returns immediately.
            if (s.charAt(i) == ':') return i;
        }
        // Reaching this line proves that no index holds a colon.
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (firstColon(":x") != 0) throw new AssertionError("example 1");
        if (firstColon("abc") != -1) throw new AssertionError("example 2");
        // The empty string never enters the loop, and a repeated colon returns the first one.
        if (firstColon("") != -1) throw new AssertionError("empty");
        if (firstColon("a::b") != 1) throw new AssertionError("first of two");
        // Reading a position past the end throws, which is why the loop bound is strict.
        boolean threw = false;
        try { "abc".charAt(3); } catch (StringIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("charAt past the end must throw");
        // Random strings are checked against String.indexOf.
        Random rnd = new Random(13);
        String pool = "ab:c";
        for (int t = 0; t < 400; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(8);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            if (firstColon(s) != s.indexOf(':')) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] To Lower Case (LeetCode 709)
<!-- id: st-to-lower -->

**Approach.**
Each output character depends only on the input character at the same index, so one scan decides everything. The method copies the string into a `char[]`, lowers each letter from `'A'` to `'Z'` by adding the distance `'a' - 'A'`, which is 32. It then builds the result string once. The method avoids `toLowerCase()`, because that call depends on the default locale and maps the letter `I` to a dotless letter in Turkish. The invariant is that after index `i`, positions 0 through `i` of the array hold the final output characters.

**Complexity.**
- **Time** is O(n), because the method copies n characters, scans them once and builds the string once.
- **Space** is O(n), because the output needs its own array of n characters.

```java run
import java.util.Locale;
import java.util.Random;

public final class ToLowerCase {
    /**
     * Lowers the letters 'A' to 'Z' and keeps every other character.
     * Time: O(n), one copy, one scan, one build. Space: O(n) for the output array.
     * Invariant: after index i, chars[0..i] hold the final output characters.
     */
    static String lower(String s) {
        // The copy gives the loop a mutable array and leaves s unchanged.
        char[] chars = s.toCharArray();
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < chars.length; i++) {
            // Only the 26 uppercase letters change; the range test keeps digits and symbols.
            if (chars[i] >= 'A' && chars[i] <= 'Z') {
                // The distance between a letter and its lowercase form is 'a' - 'A', which is 32.
                chars[i] = (char) (chars[i] + ('a' - 'A'));
            }
        }
        // One construction at the end creates the result string from the array.
        return new String(chars);
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!lower("Ab-C9").equals("ab-c9")) throw new AssertionError("example 1");
        if (!lower("").equals("")) throw new AssertionError("example 2");
        // The distance between the cases is 32.
        if ('a' - 'A' != 32) throw new AssertionError("case distance");
        // The default-locale call differs under the Turkish locale, so the loop is the safe choice.
        if (!"I".toLowerCase(Locale.forLanguageTag("tr")).equals("ı")) throw new AssertionError("locale hazard");
        // The input string stays unchanged because the method works on a copy.
        String original = "QZ";
        lower(original);
        if (!original.equals("QZ")) throw new AssertionError("input mutated");
        // Random printable ASCII strings are checked against the root-locale library call.
        Random rnd = new Random(14);
        for (int t = 0; t < 400; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append((char) (32 + rnd.nextInt(95)));
            String s = sb.toString();
            if (!lower(s).equals(s.toLowerCase(Locale.ROOT))) throw new AssertionError("random " + t);
        }
    }
}
```
