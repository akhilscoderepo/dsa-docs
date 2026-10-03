<!-- solutions-for: 02-safe-construction -->
### Safe Construction

#### Solution: [Build] Remove Spaces (Author exercise)
<!-- id: st-remove-spaces -->

**Approach.** Append each non-space character to a `StringBuilder` and convert once at the end. The concatenation version copies the whole result at every step, which the assertions model by counting the characters copied: `k` kept characters cost `k * (k + 1) / 2` copies, against `k` appends for the builder. The assertions also show that appending the result of `char` arithmetic without a cast appends digits, and compare the builder with a replace-based answer on random strings.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.Random;

public final class RemoveSpaces {
    static String removeSpaces(String s) {
        StringBuilder out = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c != ' ') out.append(c);
        }
        return out.toString();
    }
    static long copiedByConcatenation(String s) {
        long copied = 0;
        int length = 0;
        for (int i = 0; i < s.length(); i++) if (s.charAt(i) != ' ') { length++; copied += length; }
        return copied;
    }

    public static void main(String[] args) {
        if (!removeSpaces("a b  c ").equals("abc")) throw new AssertionError("example 1");
        if (!removeSpaces("").equals("")) throw new AssertionError("example 2");
        String kept = "x".repeat(1000);
        if (copiedByConcatenation(kept) != 1000L * 1001 / 2) throw new AssertionError("concatenation copies n(n+1)/2 characters");
        StringBuilder sb = new StringBuilder();
        sb.append('a' + 1);
        if (!sb.toString().equals("98")) throw new AssertionError("appending an int appends its digits");
        StringBuilder fixed = new StringBuilder();
        fixed.append((char) ('a' + 1));
        if (!fixed.toString().equals("b")) throw new AssertionError("the cast appends the character");
        Random rnd = new Random(211);
        for (int t = 0; t < 3000; t++) {
            StringBuilder in = new StringBuilder();
            int n = rnd.nextInt(20);
            for (int i = 0; i < n; i++) in.append(rnd.nextBoolean() ? ' ' : (char) ('a' + rnd.nextInt(5)));
            String s = in.toString();
            if (!removeSpaces(s).equals(s.replace(" ", ""))) throw new AssertionError("disagrees with replace on: [" + s + "]");
        }
    }
}
```

#### Solution: [Vary] Reverse Words in a String (LeetCode 151)
<!-- id: st-reverse-words -->

**Approach.** Scan from the end. Skip spaces, then find the word whose last character is at `end` by moving left until a space or the start. Write a single space only if the builder already holds something, then append the word in one call. Reading from the right makes the words arrive in reverse order, so no `insert(0, ...)` is needed. The assertions compare with a split-and-reverse oracle on random strings with repeated, leading and trailing spaces.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class ReverseWords {
    static String reverseWords(String s) {
        StringBuilder out = new StringBuilder();
        int i = s.length() - 1;
        while (i >= 0) {
            while (i >= 0 && s.charAt(i) == ' ') i--;
            if (i < 0) break;
            int end = i;
            while (i >= 0 && s.charAt(i) != ' ') i--;
            if (out.length() > 0) out.append(' ');
            out.append(s, i + 1, end + 1);
        }
        return out.toString();
    }
    static String oracle(String s) {
        String trimmed = s.trim();
        if (trimmed.isEmpty()) return "";
        List<String> words = Arrays.asList(trimmed.split(" +"));
        Collections.reverse(words);
        return String.join(" ", words);
    }

    public static void main(String[] args) {
        if (!reverseWords("  the sky  is blue ").equals("blue is sky the")) throw new AssertionError("example 1");
        if (!reverseWords("solo").equals("solo")) throw new AssertionError("example 2");
        Random rnd = new Random(212);
        for (int t = 0; t < 4000; t++) {
            StringBuilder in = new StringBuilder();
            int n = 1 + rnd.nextInt(16);
            for (int i = 0; i < n; i++) in.append(rnd.nextInt(3) == 0 ? ' ' : (char) ('a' + rnd.nextInt(3)));
            String s = in.toString();
            String got = reverseWords(s);
            if (!got.equals(oracle(s))) throw new AssertionError("disagrees with the oracle on: [" + s + "]");
            if (got.startsWith(" ") || got.endsWith(" ") || got.contains("  ")) throw new AssertionError("separator ownership violated on: [" + s + "]");
        }
    }
}
```

#### Solution: [Boundary] Empty Result (Author exercise)
<!-- id: st-empty-result -->

**Approach.** The separator-first rule writes a space only when the builder is non-empty, so an input with no words never writes anything and the result is the empty string. A version that writes a space after every word and then removes the last character has nothing to remove when no word was written, and the removal fails. The assertions run both versions on `"   "` and `" "`, check that the first returns the empty string, and that the second throws an exception.

**Complexity.** O(n) time and O(n) space for the output.

```java run
public final class EmptyResult {
    static String separatorFirst(String s) {
        StringBuilder out = new StringBuilder();
        int i = s.length() - 1;
        while (i >= 0) {
            while (i >= 0 && s.charAt(i) == ' ') i--;
            if (i < 0) break;
            int end = i;
            while (i >= 0 && s.charAt(i) != ' ') i--;
            if (out.length() > 0) out.append(' ');
            out.append(s, i + 1, end + 1);
        }
        return out.toString();
    }
    static String separatorAfter(String s) {
        StringBuilder out = new StringBuilder();
        int i = s.length() - 1;
        while (i >= 0) {
            while (i >= 0 && s.charAt(i) == ' ') i--;
            if (i < 0) break;
            int end = i;
            while (i >= 0 && s.charAt(i) != ' ') i--;
            out.append(s, i + 1, end + 1).append(' ');
        }
        out.setLength(out.length() - 1);                       // removes the last separator, if there is one
        return out.toString();
    }

    public static void main(String[] args) {
        if (!separatorFirst("   ").equals("")) throw new AssertionError("example 1");
        if (!separatorFirst(" ").equals("")) throw new AssertionError("example 2");
        if (!separatorFirst("").equals("")) throw new AssertionError("empty input");
        if (!separatorAfter("a b").equals("b a")) throw new AssertionError("the after-version works when words exist");
        boolean threw = false;
        try { separatorAfter("   "); } catch (IndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("the after-version must fail when nothing was written");
        threw = false;
        try { separatorAfter(" "); } catch (IndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("the after-version must fail on a single space");
    }
}
```

#### Solution: [Recognize] Zigzag Conversion (LeetCode 6)
<!-- id: st-zigzag -->

**Approach.** Give each row its own builder. Walk the string once, append each character to the current row, and change direction when the cursor reaches the top or bottom row. With one row the direction logic would move out of range, so that case returns the string unchanged, and the same early return covers a row count at least as large as the string, where each character sits in its own row. At the end the rows are appended in order. The oracle uses the cycle formula: with `cycle = 2 * numRows - 2`, row `r` takes the characters at positions `r + k * cycle` and `(k + 1) * cycle - r`.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.Random;

public final class Zigzag {
    static String zigzag(String s, int numRows) {
        if (numRows == 1 || numRows >= s.length()) return s;
        StringBuilder[] rows = new StringBuilder[numRows];
        for (int r = 0; r < numRows; r++) rows[r] = new StringBuilder();
        int row = 0, step = 1;
        for (int i = 0; i < s.length(); i++) {
            rows[row].append(s.charAt(i));
            if (row == 0) step = 1;
            else if (row == numRows - 1) step = -1;
            row += step;
        }
        StringBuilder out = new StringBuilder(s.length());
        for (StringBuilder r : rows) out.append(r);
        return out.toString();
    }
    static String oracle(String s, int numRows) {
        if (numRows == 1) return s;
        int cycle = 2 * numRows - 2;
        StringBuilder out = new StringBuilder();
        for (int r = 0; r < numRows; r++)
            for (int base = 0; base < s.length(); base += cycle) {
                if (base + r < s.length()) out.append(s.charAt(base + r));
                if (r != 0 && r != numRows - 1 && base + cycle - r < s.length()) out.append(s.charAt(base + cycle - r));
            }
        return out.toString();
    }

    public static void main(String[] args) {
        if (!zigzag("ABCDEFGHIJKLM", 3).equals("AEIMBDFHJLCGK")) throw new AssertionError("example 1: " + zigzag("ABCDEFGHIJKLM", 3));
        if (!zigzag("ABC", 1).equals("ABC")) throw new AssertionError("example 2");
        Random rnd = new Random(213);
        for (int t = 0; t < 4000; t++) {
            StringBuilder in = new StringBuilder();
            int n = 1 + rnd.nextInt(25);
            for (int i = 0; i < n; i++) in.append((char) ('a' + rnd.nextInt(26)));
            String s = in.toString();
            int rows = 1 + rnd.nextInt(7);
            if (!zigzag(s, rows).equals(oracle(s, rows))) throw new AssertionError("disagrees with the cycle formula on " + s + " with " + rows + " rows");
        }
    }
}
```
