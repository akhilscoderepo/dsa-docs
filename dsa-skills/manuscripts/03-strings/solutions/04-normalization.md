<!-- solutions-for: 03-strings -->
### Solutions For Normalization

#### Solution: [Build] Lowercase Letters Only (Author exercise)
<!-- id: st-letters-only -->

**Approach.**
The loop reads each character and appends it to a `StringBuilder` in one of two ways. An uppercase letter is appended after adding the case distance 32. A lowercase letter is appended unchanged. Every other character is skipped. The invariant is that after index `i`, the builder holds the lowercase letters of `s[0..i]` in order. The harness also asserts the Java behaviors that the lesson text states about product codes.

**Complexity.**
- **Time** is O(n), because each character costs one read and at most one append.
- **Space** is O(n), because the builder holds up to n characters.

```java run
import java.util.Locale;
import java.util.Random;

public final class LettersOnly {
    /**
     * Keeps the ASCII letters of s, lowercased, in order.
     * Time: O(n). Space: O(n) for the builder.
     * Invariant: after index i, out holds the lowercase letters of s[0..i].
     */
    static String lettersOnly(String s) {
        // The builder starts empty, which is also the answer when no letter exists.
        StringBuilder out = new StringBuilder(s.length());
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= 'A' && c <= 'Z') {
                // An uppercase letter moves to its lowercase form by the case distance.
                out.append((char) (c + ('a' - 'A')));
            } else if (c >= 'a' && c <= 'z') {
                // A lowercase letter is already in the canonical form.
                out.append(c);
            }
            // Any other character falls through and is dropped.
        }
        // One conversion creates the result string.
        return out.toString();
    }

    /** Lesson code: letters and digits in lowercase. */
    static String normalize(String s) {
        StringBuilder out = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= 'A' && c <= 'Z') out.append((char) (c + ('a' - 'A')));
            else if ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9')) out.append(c);
        }
        return out.toString();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!lettersOnly("A-b c!").equals("abc")) throw new AssertionError("example 1");
        if (!lettersOnly("2024").equals("")) throw new AssertionError("example 2");
        if (!lettersOnly("").equals("")) throw new AssertionError("empty");
        // Random strings are checked against a regular-expression oracle.
        Random rnd = new Random(41);
        String pool = "aZ-b 3Y?q";
        for (int t = 0; t < 400; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            if (!lettersOnly(s).equals(s.replaceAll("[^A-Za-z]", "").toLowerCase(Locale.ROOT))) throw new AssertionError("random " + t);
        }
        // Lesson claim: lowercasing alone keeps the dash and the space, so it separates the two spellings.
        if ("ab-12".toLowerCase().equals("AB 12".toLowerCase())) throw new AssertionError("naive differs");
        if (!"Ab12".toLowerCase().equals("aB12".toLowerCase())) throw new AssertionError("naive handles case");
        // Lesson claim: normalizing both sides makes the spellings equal, and noise-only input gives "".
        if (!normalize("ab-12").equals(normalize("AB 12"))) throw new AssertionError("same code");
        if (!normalize("?!").equals("")) throw new AssertionError("empty form");
        if (!normalize("A-b 1").equals("ab1")) throw new AssertionError("trace 1");
        // Lesson claim: dropping digits would merge A1 and A2.
        if (!"A1".replaceAll("[0-9]", "").equals("A2".replaceAll("[0-9]", ""))) throw new AssertionError("digit drop merges");
        // Lesson claim: case mapping can change length, and == compares references.
        if ("ß".toUpperCase(Locale.ROOT).length() != 2) throw new AssertionError("sharp s length");
        if (new String("a") == "a") throw new AssertionError("reference comparison");
        // Lesson claim: the default locale changes lowercase, shown with the Turkish locale.
        if ("I".toLowerCase(Locale.forLanguageTag("tr")).equals("i")) throw new AssertionError("locale hazard");
    }
}
```

#### Solution: [Vary] Detect Capital (LeetCode 520)
<!-- id: st-detect-capital -->

**Approach.**
The method builds the three allowed forms of the letters of `word` and checks whether `word` equals one of them. A helper converts each letter to uppercase or lowercase by the case distance, and a flag per form decides the case of the first letter and of the rest. The three forms are all lowercase, all uppercase and an uppercase first letter followed by lowercase letters. The invariant of the helper is that after index `i`, the builder holds the letters of `word[0..i]` in the case that the form demands.

**Complexity.**
- **Time** is O(n), because each of the three builds reads n characters once.
- **Space** is O(n), because each form is a string of n characters.

```java run
import java.util.Random;

public final class DetectCapital {
    /**
     * Rebuilds the letters of word, using one case for the first letter and one for the rest.
     * Time: O(n). Space: O(n). Invariant: after index i, out holds word[0..i] in the requested cases.
     */
    static String form(String word, boolean firstUpper, boolean restUpper) {
        StringBuilder out = new StringBuilder(word.length());
        // The loop runs once per letter, which costs n iterations.
        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);
            // Index 0 follows the first-letter rule, and every later index follows the rest rule.
            boolean upper = i == 0 ? firstUpper : restUpper;
            // The letter is moved to the demanded case by the case distance.
            if (upper && c >= 'a' && c <= 'z') c = (char) (c - ('a' - 'A'));
            else if (!upper && c >= 'A' && c <= 'Z') c = (char) (c + ('a' - 'A'));
            out.append(c);
        }
        return out.toString();
    }

    /**
     * Returns true when word is all lowercase, all uppercase, or capitalized.
     * Time: O(n). Space: O(n). Invariant: each form keeps the letters and only changes their case.
     */
    static boolean detectCapital(String word) {
        // The word is correct when it already equals one of the three allowed forms.
        return word.equals(form(word, false, false))
                || word.equals(form(word, true, true))
                || word.equals(form(word, true, false));
    }

    public static void main(String[] args) {
        // The statement examples.
        if (detectCapital("gRaph")) throw new AssertionError("example 1");
        if (!detectCapital("Graph")) throw new AssertionError("example 2");
        // One letter is correct in either case.
        if (!detectCapital("a") || !detectCapital("A")) throw new AssertionError("single letter");
        // A lone capital in the middle and a lone lowercase at the end are wrong.
        if (detectCapital("GraPh") || detectCapital("GRAPh")) throw new AssertionError("mixed forms");
        // Random words are checked against a regular-expression oracle.
        Random rnd = new Random(42);
        for (int t = 0; t < 1000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(5);
            for (int k = 0; k < len; k++) sb.append(rnd.nextBoolean() ? 'a' : 'B');
            String w = sb.toString();
            boolean expect = w.matches("[a-z]+|[A-Z]+|[A-Z][a-z]*");
            if (detectCapital(w) != expect) throw new AssertionError("random " + w);
        }
    }
}
```

#### Solution: [Boundary] Punctuation Only (Author exercise)
<!-- id: st-punctuation-only -->

**Approach.**
The method normalizes both strings with the same loop, which keeps the lowercase letters, and compares the two results with `equals`. An input with no letters normalizes to the empty string. Two empty results are equal, so the comparison needs no special case for them. The invariant is that each canonical form holds exactly the lowercase letters of its input in order, and two inputs are equivalent exactly when the forms are equal.

**Complexity.**
- **Time** is O(n + m), because each string is read once and the final comparison reads at most min(n, m) characters.
- **Space** is O(n + m), because both canonical forms are stored.

```java run
import java.util.Locale;
import java.util.Random;

public final class PunctuationOnly {
    /**
     * Returns the lowercase letters of s in order.
     * Time: O(n). Space: O(n). Invariant: after index i, out holds the letters of s[0..i] in lowercase.
     */
    static String letters(String s) {
        StringBuilder out = new StringBuilder(s.length());
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            // A letter joins the canonical form in lowercase, and every other character is skipped.
            if (c >= 'A' && c <= 'Z') out.append((char) (c + ('a' - 'A')));
            else if (c >= 'a' && c <= 'z') out.append(c);
        }
        return out.toString();
    }

    /**
     * Returns true when both strings have the same lowercase letters in the same order.
     * Time: O(n + m). Space: O(n + m).
     */
    static boolean sameLetters(String a, String b) {
        // Both sides use the same function, and equals handles two empty forms like any other pair.
        return letters(a).equals(letters(b));
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!sameLetters("Ab,c", "a BC")) throw new AssertionError("example 1");
        if (!sameLetters("?!", "")) throw new AssertionError("example 2");
        // Different letters, different order and one empty side.
        if (sameLetters("ab", "ba")) throw new AssertionError("order matters");
        if (sameLetters("a", "!")) throw new AssertionError("letter against noise");
        // Random pairs are checked against a regular-expression oracle.
        Random rnd = new Random(43);
        String pool = "aAbB-? ";
        for (int t = 0; t < 1000; t++) {
            String a = rnd(rnd, pool), b = rnd(rnd, pool);
            boolean expect = a.replaceAll("[^A-Za-z]", "").toLowerCase(Locale.ROOT)
                    .equals(b.replaceAll("[^A-Za-z]", "").toLowerCase(Locale.ROOT));
            if (sameLetters(a, b) != expect) throw new AssertionError("random " + t);
        }
    }

    static String rnd(Random r, String pool) {
        StringBuilder sb = new StringBuilder();
        int len = r.nextInt(6);
        for (int k = 0; k < len; k++) sb.append(pool.charAt(r.nextInt(pool.length())));
        return sb.toString();
    }
}
```

#### Solution: [Recognize] License Key Formatting (LeetCode 482)
<!-- id: st-license-key -->

**Approach.**
Groups fill from the right end, so the method reads `s` backward. Each non-dash character is uppercased and appended to a builder. A counter records how many characters the current group holds. Before the method appends a character to a full group, it appends one dash and resets the counter. A dash therefore appears only when another character follows, and the key never starts or ends with a dash. The builder holds the key in reverse order, so one call to `reverse()` restores it. The invariant is that after index `i`, the builder holds the reversed formatted key of the non-dash characters of `s[i..n-1]`.

**Complexity.**
- **Time** is O(n), because the loop reads each character once and the reverse reads the output once.
- **Space** is O(n), because the builder holds at most n plus the dashes, which is under 2n characters.

```java run
import java.util.Random;

public final class LicenseKey {
    /**
     * Formats s into groups of k characters, with a shorter first group.
     * Time: O(n). Space: O(n).
     * Invariant: after index i, out holds the reversed key of the non-dash characters of s[i..n-1].
     */
    static String format(String s, int k) {
        // The builder collects the key backward, because the groups fill from the right.
        StringBuilder out = new StringBuilder(s.length() + s.length() / k + 1);
        // size counts the characters in the current group.
        int size = 0;
        // The loop reads from the last index down to 0, which costs n iterations.
        for (int i = s.length() - 1; i >= 0; i--) {
            char c = s.charAt(i);
            // Dashes in the input carry no meaning, so the loop skips them.
            if (c == '-') continue;
            // A full group is closed by one dash, written only when another character follows.
            if (size == k) {
                out.append('-');
                size = 0;
            }
            // A lowercase letter moves to uppercase by the case distance; digits stay unchanged.
            if (c >= 'a' && c <= 'z') c = (char) (c - ('a' - 'A'));
            out.append(c);
            size++;
        }
        // One reversal puts the groups in reading order.
        return out.reverse().toString();
    }

    /** Oracle: clean the string first, then cut it into groups from the left with a computed first length. */
    static String oracle(String s, int k) {
        String clean = s.replace("-", "").toUpperCase();
        if (clean.isEmpty()) return "";
        int first = clean.length() % k == 0 ? k : clean.length() % k;
        StringBuilder sb = new StringBuilder(clean.substring(0, first));
        for (int p = first; p < clean.length(); p += k) sb.append('-').append(clean, p, p + k);
        return sb.toString();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!format("x1-k9", 3).equals("X-1K9")) throw new AssertionError("example 1");
        if (!format("--", 2).equals("")) throw new AssertionError("example 2");
        // A full first group, a group size of one and a single character.
        if (!format("ab-cd", 2).equals("AB-CD")) throw new AssertionError("full first group");
        if (!format("ab-c", 1).equals("A-B-C")) throw new AssertionError("group size one");
        if (!format("z", 5).equals("Z")) throw new AssertionError("single character");
        // Random strings and group sizes are checked against the oracle.
        Random rnd = new Random(44);
        String pool = "aB1-z9--";
        for (int t = 0; t < 1000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            int k = 1 + rnd.nextInt(4);
            if (!format(s, k).equals(oracle(s, k))) throw new AssertionError("random " + t + " " + s + " " + k);
        }
    }
}
```
