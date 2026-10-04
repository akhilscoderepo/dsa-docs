<!-- solutions-for: 03-strings -->
### Solutions For Build Strings With StringBuilder

#### Solution: [Build] Remove Spaces (Author exercise)
<!-- id: st-remove-spaces -->

**Approach.**
The loop reads each character once and appends it to a `StringBuilder` unless it is a space. The builder is sized to the input length, because the output is never longer than the input. The invariant is that after index `i`, the builder holds the non-space characters of the first `i + 1` input characters, in order. A call to `toString()` at the end creates the result with one copy. The harness at the end of the class also checks the Java claims made in the lesson text.

**Complexity.**
- **Time** is O(n), because each character costs one read and at most one append of amortized constant cost.
- **Space** is O(n), because the builder holds up to n characters.

```java run
import java.util.Random;

public final class RemoveSpaces {
    /**
     * Removes every space character from s.
     * Time: O(n), one pass with amortized O(1) appends. Space: O(n) for the builder.
     * Invariant: after index i, out holds the non-space characters of s[0..i] in order.
     */
    static String removeSpaces(String s) {
        // Reserving s.length() characters means the buffer never has to grow.
        StringBuilder out = new StringBuilder(s.length());
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            // A space is skipped, and every other character is kept.
            if (s.charAt(i) != ' ') {
                // The append writes at the end of the buffer, so earlier text is never copied.
                out.append(s.charAt(i));
            }
        }
        // One conversion at the end creates the result string.
        return out.toString();
    }

    /** Lesson code: comma-separated join with the separator owned by every element except the first. */
    static String joinNumbers(int[] a) {
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < a.length; i++) {
            if (i > 0) out.append(',');
            out.append(a[i]);
        }
        return out.toString();
    }

    /** Lesson code: reversal by appending from the last index down to index 0. */
    static String reverseText(String s) {
        StringBuilder out = new StringBuilder(s.length());
        for (int i = s.length() - 1; i >= 0; i--) out.append(s.charAt(i));
        return out.toString();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!removeSpaces("a b  c").equals("abc")) throw new AssertionError("example 1");
        if (!removeSpaces("").equals("")) throw new AssertionError("example 2");
        if (!removeSpaces("   ").equals("")) throw new AssertionError("only spaces");
        // Random strings are checked against replace.
        Random rnd = new Random(21);
        String pool = "ab  c!";
        for (int t = 0; t < 400; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            if (!removeSpaces(s).equals(s.replace(" ", ""))) throw new AssertionError("random " + t);
        }
        // Lesson claim: the join places no comma at either end, and an empty array gives "".
        if (!joinNumbers(new int[] {3, 1, 4}).equals("3,1,4")) throw new AssertionError("join");
        if (!joinNumbers(new int[] {9, 15}).equals("9,15")) throw new AssertionError("join two digits");
        if (!joinNumbers(new int[0]).equals("")) throw new AssertionError("join empty");
        // Lesson claim: the plus loop leaves a trailing comma.
        String plus = "";
        for (int v : new int[] {3, 1, 4}) plus = plus + v + ",";
        if (!plus.equals("3,1,4,")) throw new AssertionError("plus loop trailing comma");
        // Lesson claim: concatenation builds a new string and leaves the old one unchanged.
        String base = "ab";
        String longer = base + "c";
        if (!base.equals("ab") || longer == base) throw new AssertionError("immutability");
        // Lesson claim: copying n one-digit pieces plus commas totals n * (n + 1) characters.
        int n = 50;
        long copied = 0;
        String r = "";
        for (int k = 0; k < n; k++) { r = r + "7" + ","; copied += r.length(); }
        if (copied != (long) n * (n + 1)) throw new AssertionError("copy total model");
        // Lesson claim: the builder grows its array by a factor, so few resizes occur.
        StringBuilder grow = new StringBuilder();
        int resizes = 0, cap = grow.capacity();
        for (int k = 0; k < 10000; k++) {
            grow.append('x');
            if (grow.capacity() != cap) { resizes++; cap = grow.capacity(); }
        }
        if (resizes > 30) throw new AssertionError("too many resizes: " + resizes);
        // Lesson claim: reversal by appends equals reverse(), and insert(0, ...) gives the same text with n(n-1)/2 shifted characters.
        String word = "abcdefgh";
        if (!reverseText(word).equals(new StringBuilder(word).reverse().toString())) throw new AssertionError("reverse");
        StringBuilder ins = new StringBuilder();
        long shifted = 0;
        for (int k = 0; k < word.length(); k++) { shifted += ins.length(); ins.insert(0, word.charAt(k)); }
        if (!ins.toString().equals(reverseText(word))) throw new AssertionError("insert reversal text");
        if (shifted != (long) word.length() * (word.length() - 1) / 2) throw new AssertionError("insert shift model");
        // Lesson claim: append('a' + 1) writes the digits of the int, and the cast writes the letter.
        if (!new StringBuilder().append('a' + 1).toString().equals("98")) throw new AssertionError("int append");
        if (!new StringBuilder().append((char) ('a' + 1)).toString().equals("b")) throw new AssertionError("char append");
        // Lesson claim: the capacity argument sets capacity and leaves the length at 0, and builders compare by identity.
        StringBuilder sized = new StringBuilder(5);
        if (sized.length() != 0 || sized.capacity() != 5) throw new AssertionError("constructor argument");
        if (new StringBuilder("a").equals(new StringBuilder("a"))) throw new AssertionError("builder equals");
    }
}
```

#### Solution: [Vary] Reverse Words In A String (LeetCode 151)
<!-- id: st-reverse-words -->

**Approach.**
A forward scan finds each word by its first and last index and stores the word in an `ArrayList`. A word starts at a non-space character that follows a space or sits at index 0, and it ends before the next space or at the end of the string. After the scan, a builder receives the stored words from the last to the first. Each word except the first one written owns the single space in front of it, so no space appears at either end. The invariant of the scan is that the list holds every word that ends before index `i`, in input order.

**Complexity.**
- **Time** is O(n), because the scan reads each character once and the final loop appends each character once.
- **Space** is O(n), because the list and the builder each hold at most n characters in total.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class ReverseWords {
    /**
     * Returns the words of s in reverse order, joined by single spaces.
     * Time: O(n), one scan and one build. Space: O(n) for the list and the builder.
     * Invariant: words holds every word that ends before index i, in input order.
     */
    static String reverseWords(String s) {
        // The list receives each word as a substring, created once per word.
        List<String> words = new ArrayList<>();
        // start is the first index of the current word, or -1 outside a word.
        int start = -1;
        // The loop runs one step past the end so the last word is closed too.
        for (int i = 0; i <= s.length(); i++) {
            // Index s.length() counts as a space, which closes a word that ends at the end of the string.
            boolean space = i == s.length() || s.charAt(i) == ' ';
            if (!space && start < 0) {
                // A non-space character after a space opens a word.
                start = i;
            } else if (space && start >= 0) {
                // A space after a word closes it, and the substring covers [start, i).
                words.add(s.substring(start, i));
                start = -1;
            }
        }
        // The builder receives the words from the last to the first.
        StringBuilder out = new StringBuilder(s.length());
        for (int k = words.size() - 1; k >= 0; k--) {
            // Every word except the first one written owns one space in front of it.
            if (out.length() > 0) out.append(' ');
            out.append(words.get(k));
        }
        // The builder holds the final text with no space at either end.
        return out.toString();
    }

    /** Oracle: split on runs of spaces, reverse the list and join. */
    static String oracle(String s) {
        List<String> parts = new ArrayList<>(Arrays.asList(s.trim().split(" +")));
        Collections.reverse(parts);
        return String.join(" ", parts);
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!reverseWords("  one  two three ").equals("three two one")) throw new AssertionError("example 1");
        if (!reverseWords("word").equals("word")) throw new AssertionError("example 2");
        // A single word with spaces at both ends.
        if (!reverseWords("   ab   ").equals("ab")) throw new AssertionError("padded word");
        // Random strings with at least one word are checked against the oracle.
        Random rnd = new Random(22);
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(14);
            for (int k = 0; k < len; k++) sb.append(rnd.nextInt(3) == 0 ? ' ' : (char) ('a' + rnd.nextInt(3)));
            if (sb.toString().trim().isEmpty()) sb.append('z');
            String s = sb.toString();
            if (!reverseWords(s).equals(oracle(s))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty Result (Author exercise)
<!-- id: st-empty-result -->

**Approach.**
The loop appends each letter to the builder and decides on a bar only when a letter opens a field. A letter opens a field when it sits at index 0 or follows a comma. At that moment the builder is either empty, so no bar is written, or it holds earlier fields, so one bar is written first. An input with no letter never appends anything, so the empty builder returns the empty string and no bar can appear at the end. The invariant is that the builder holds the fields that started at or before index `i`, joined by single bars.

**Complexity.**
- **Time** is O(n), because each character causes at most two appends of amortized constant cost.
- **Space** is O(n), because the builder holds at most n characters.

```java run
import java.util.Random;

public final class EmptyResult {
    /**
     * Joins the comma-separated letter fields of s with '|'.
     * Time: O(n), one pass. Space: O(n) for the builder.
     * Invariant: out holds the fields that start at or before index i, joined by single bars.
     */
    static String joinFields(String s) {
        // The builder starts empty, which is also the answer when no field exists.
        StringBuilder out = new StringBuilder(s.length());
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            // Commas never reach the output.
            if (s.charAt(i) == ',') continue;
            // A letter opens a field at index 0 or right after a comma.
            boolean opensField = i == 0 || s.charAt(i - 1) == ',';
            // A bar is written only when a field already exists in the output.
            if (opensField && out.length() > 0) out.append('|');
            // The letter itself always joins the output.
            out.append(s.charAt(i));
        }
        // An input without letters leaves the builder empty, so the result is "".
        return out.toString();
    }

    /** Oracle: split on commas, drop empty pieces and join with bars. */
    static String oracle(String s) {
        StringBuilder sb = new StringBuilder();
        for (String part : s.split(",")) {
            if (part.isEmpty()) continue;
            if (sb.length() > 0) sb.append('|');
            sb.append(part);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!joinFields("ab,,c").equals("ab|c")) throw new AssertionError("example 1");
        if (!joinFields(",,,").equals("")) throw new AssertionError("example 2");
        // Empty input and commas at both ends.
        if (!joinFields("").equals("")) throw new AssertionError("empty input");
        if (!joinFields(",a,b,").equals("a|b")) throw new AssertionError("commas at both ends");
        // Random strings are checked against the oracle.
        Random rnd = new Random(23);
        String pool = "abc,,";
        for (int t = 0; t < 500; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(12);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            if (!joinFields(s).equals(oracle(s))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Zigzag Conversion (LeetCode 6)
<!-- id: st-zigzag -->

**Approach.**
The method owns one builder per row and appends each character to the builder of its current row. The row index starts at 0 and moves by `step`, which is `+1` going down and `-1` going up. The step flips when the row reaches 0 or the last row. When `numRows` is 1 or at least the string length, the zigzag has no turn that changes the order, so the method returns `s`. The invariant is that after index `i`, each row builder holds the characters of `s[0..i]` that belong to that row, in input order.

**Complexity.**
- **Time** is O(n), because the loop appends each character once and the final join reads each builder once.
- **Space** is O(n), because the builders hold n characters in total and the array holds at most n builders.

```java run
import java.util.Random;

public final class Zigzag {
    /**
     * Writes s in a zigzag over numRows rows and reads it row by row.
     * Time: O(n). Space: O(n) for the row builders.
     * Invariant: after index i, each row holds its characters of s[0..i] in input order.
     */
    static String convert(String s, int numRows) {
        // With one row, or with at least one row per character, the reading order equals the input order.
        if (numRows == 1 || numRows >= s.length()) return s;
        // One builder per row, created once, owns the independently constructed text of that row.
        StringBuilder[] rows = new StringBuilder[numRows];
        for (int r = 0; r < numRows; r++) rows[r] = new StringBuilder();
        // row is the current row index, and step is +1 when moving down and -1 when moving up.
        int row = 0, step = 1;
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            // The character joins the builder of its row at the end.
            rows[row].append(s.charAt(i));
            // The direction flips at the top row and at the bottom row.
            if (row == 0) step = 1;
            else if (row == numRows - 1) step = -1;
            // The next character goes one row further in the current direction.
            row += step;
        }
        // The final builder holds rows 0 through numRows - 1 in reading order.
        StringBuilder out = new StringBuilder(s.length());
        for (StringBuilder b : rows) out.append(b);
        return out.toString();
    }

    /** Oracle: reads each row directly from the repeating cycle of length 2 * numRows - 2. */
    static String oracle(String s, int numRows) {
        if (numRows == 1) return s;
        int cycle = 2 * numRows - 2;
        StringBuilder sb = new StringBuilder();
        for (int r = 0; r < numRows; r++) {
            for (int j = r; j < s.length(); j += cycle) {
                sb.append(s.charAt(j));
                int back = j + cycle - 2 * r;
                if (r > 0 && r < numRows - 1 && back < s.length()) sb.append(s.charAt(back));
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!convert("ABCDEFGHIJ", 4).equals("AGBFHCEIDJ")) throw new AssertionError("example 1");
        if (!convert("ABC", 5).equals("ABC")) throw new AssertionError("example 2");
        // Two rows alternate, and one row returns the input.
        if (!convert("ABCDE", 2).equals("ACEBD")) throw new AssertionError("two rows");
        if (!convert("ABCDE", 1).equals("ABCDE")) throw new AssertionError("one row");
        // Random strings and row counts are checked against the cycle-based oracle.
        Random rnd = new Random(24);
        for (int t = 0; t < 500; t++) {
            int len = 1 + rnd.nextInt(15);
            StringBuilder sb = new StringBuilder();
            for (int k = 0; k < len; k++) sb.append((char) ('A' + rnd.nextInt(26)));
            String s = sb.toString();
            int rows = 1 + rnd.nextInt(8);
            if (!convert(s, rows).equals(oracle(s, rows))) throw new AssertionError("random " + t);
        }
    }
}
```
