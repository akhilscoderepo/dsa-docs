<!-- solutions-for: 04-normalization -->
### Normalization

#### Solution: [Build] Lowercase Letters Only (Author exercise)
<!-- id: st-lowercase-letters -->

**Approach.** Scan once. An ASCII uppercase letter is appended after shifting it to lowercase, an ASCII lowercase letter is appended as it is, and every other character is skipped. The ASCII ranges are used instead of `Character.isLetter`, which accepts letters of all scripts, and instead of the default-locale `toLowerCase`, which can change the result. The assertions show both library behaviors and compare the scan with a locale-independent filter on random printable ASCII.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.Locale;
import java.util.Random;

public final class LowercaseLetters {
    static String lowercaseLetters(String s) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= 'A' && c <= 'Z') out.append((char) (c + ('a' - 'A')));
            else if (c >= 'a' && c <= 'z') out.append(c);
        }
        return out.toString();
    }

    public static void main(String[] args) {
        if (!lowercaseLetters("A-b, C!").equals("abc")) throw new AssertionError("example 1");
        if (!lowercaseLetters("x9 Y").equals("xy")) throw new AssertionError("example 2");
        if (!Character.isLetter('é')) throw new AssertionError("isLetter accepts letters outside ASCII");
        if (!lowercaseLetters("éa").equals("a")) throw new AssertionError("the contract keeps ASCII letters only");
        String turkish = "I".toLowerCase(Locale.forLanguageTag("tr"));
        if (turkish.equals("i")) throw new AssertionError("a Turkish locale changes the lowercase of I");
        if (!"I".toLowerCase(Locale.ROOT).equals("i")) throw new AssertionError("the root locale gives i");
        Random rnd = new Random(231);
        for (int t = 0; t < 4000; t++) {
            StringBuilder in = new StringBuilder();
            int n = rnd.nextInt(25);
            for (int i = 0; i < n; i++) in.append((char) (32 + rnd.nextInt(95)));
            String s = in.toString();
            String expected = s.toLowerCase(Locale.ROOT).replaceAll("[^a-z]", "");
            if (!lowercaseLetters(s).equals(expected)) throw new AssertionError("disagrees on: " + s);
        }
    }
}
```

#### Solution: [Vary] Detect Capital (LeetCode 520)
<!-- id: st-detect-capital -->

**Approach.** The three allowed forms are all lowercase, all capitals, and a single leading capital. Count the capitals and test the first letter. The word is allowed when the count is 0, when it equals the length, or when it is exactly 1 and the first letter is the capital. No second string is built. The oracle compares the word with its upper-case form, its lower-case form, and with its first letter upper-cased followed by a lower-cased remainder.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Locale;
import java.util.Random;

public final class DetectCapital {
    static boolean detectCapital(String word) {
        int upper = 0;
        for (int i = 0; i < word.length(); i++) if (word.charAt(i) >= 'A' && word.charAt(i) <= 'Z') upper++;
        boolean firstUpper = word.length() > 0 && word.charAt(0) >= 'A' && word.charAt(0) <= 'Z';
        return upper == 0 || upper == word.length() || (upper == 1 && firstUpper);
    }
    static boolean oracle(String w) {
        String up = w.toUpperCase(Locale.ROOT), low = w.toLowerCase(Locale.ROOT);
        String title = up.substring(0, 1) + low.substring(1);
        return w.equals(up) || w.equals(low) || w.equals(title);
    }

    public static void main(String[] args) {
        if (!detectCapital("Zebra")) throw new AssertionError("example 1");
        if (detectCapital("zEbra")) throw new AssertionError("example 2");
        if (!detectCapital("Q") || !detectCapital("q")) throw new AssertionError("single letters");
        if (detectCapital("ZEbra") || detectCapital("zebrA")) throw new AssertionError("mixed forms");
        Random rnd = new Random(232);
        for (int t = 0; t < 8000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(6);
            for (int i = 0; i < n; i++) sb.append((char) ((rnd.nextBoolean() ? 'A' : 'a') + rnd.nextInt(3)));
            String w = sb.toString();
            if (detectCapital(w) != oracle(w)) throw new AssertionError("disagrees on: " + w);
        }
    }
}
```

#### Solution: [Boundary] Punctuation Only (Author exercise)
<!-- id: st-punctuation-only -->

**Approach.** A builder that never receives an append is empty, and `toString()` of an empty builder is the empty string, not null, so the method needs no special case. Under the contract that only letters matter, two inputs without letters have the same canonical form, so they are equal. The contract can instead say that a card with no letters is malformed, in which case the method should reject it before comparison. The code states the first contract and the assertions document it. They check the empty results, that the result is not null, and that two punctuation-only cards compare as equal while a card with a letter does not.

**Complexity.** O(n) time and O(n) space for the output.

```java run
public final class PunctuationOnly {
    static String normalize(String s) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= 'A' && c <= 'Z') out.append((char) (c + ('a' - 'A')));
            else if (c >= 'a' && c <= 'z') out.append(c);
        }
        return out.toString();
    }
    static boolean sameCard(String a, String b) { return normalize(a).equals(normalize(b)); }

    public static void main(String[] args) {
        if (!normalize("?!").equals("")) throw new AssertionError("example 1");
        if (!normalize(" ,.- ").equals("")) throw new AssertionError("example 2");
        if (normalize("") == null || !normalize("").isEmpty()) throw new AssertionError("empty input gives the empty string, never null");
        if (!sameCard("?!", " ,.- ")) throw new AssertionError("two cards with nothing relevant have the same canonical form");
        if (sameCard("?!", "?a!")) throw new AssertionError("a card with a letter differs from a card with none");
        if (!sameCard("Smith, J.", "smith j")) throw new AssertionError("decoration does not matter");
    }
}
```

#### Solution: [Recognize] License Key Formatting (LeetCode 482)
<!-- id: st-license-key -->

**Approach.** Scan from the end, skip dashes, and append each remaining character uppercased. Before appending, if the current group already holds `k` characters, append a dash and start a new group. The builder then holds the key reversed, and one `reverse()` at the end puts it in order, leaving the short group at the front. This avoids inserting at the front and needs no knowledge of the total length. The oracle computes the size of the first group from the number of kept characters by remainder and regroups with explicit substrings.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.Locale;
import java.util.Random;

public final class LicenseKey {
    static String licenseKey(String s, int k) {
        StringBuilder out = new StringBuilder();
        int groupLen = 0;
        for (int i = s.length() - 1; i >= 0; i--) {
            char c = s.charAt(i);
            if (c == '-') continue;
            if (groupLen == k) { out.append('-'); groupLen = 0; }
            out.append(Character.toUpperCase(c));
            groupLen++;
        }
        return out.reverse().toString();
    }
    static String oracle(String s, int k) {
        String clean = s.replace("-", "").toUpperCase(Locale.ROOT);
        if (clean.isEmpty()) return "";
        int first = clean.length() % k == 0 ? k : clean.length() % k;
        StringBuilder out = new StringBuilder(clean.substring(0, first));
        for (int i = first; i < clean.length(); i += k) out.append('-').append(clean, i, i + k);
        return out.toString();
    }

    public static void main(String[] args) {
        if (!licenseKey("x7-k-p-02-q9", 3).equals("X7-KP0-2Q9")) throw new AssertionError("example 1: " + licenseKey("x7-k-p-02-q9", 3));
        if (!licenseKey("---", 2).equals("")) throw new AssertionError("example 2");
        if (!licenseKey("abcd", 4).equals("ABCD")) throw new AssertionError("exactly one full group");
        if (!licenseKey("abcde", 2).equals("A-BC-DE")) throw new AssertionError("short first group");
        Random rnd = new Random(233);
        String alphabet = "abcXYZ019-";
        for (int t = 0; t < 8000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(16);
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            int k = 1 + rnd.nextInt(5);
            if (!licenseKey(s, k).equals(oracle(s, k))) throw new AssertionError("disagrees on " + s + " with k = " + k);
        }
    }
}
```
