<!-- solutions-for: 03-strings -->
### Solutions For Compressing Runs

#### Solution: [Build] String Compression (LeetCode 443)
<!-- id: st-string-compression -->

**Approach.**
The method keeps `start`, the first index of the open run, and `write`, the next index to fill. When the index `i` reaches a run boundary or the end of the array, the run `chars[start..i-1]` closes. The method writes the run character at `write`, and for a length of at least 2 it writes the digits of the length after it. A run of length `L` writes at most `L` characters, because `1 + digits(L) <= L` once `L >= 2`. Since `write <= start` before a run closes, the writes never overwrite a character that the loop has yet to read. The invariant is that `chars[0..write-1]` holds the compressed form of all closed runs. The harness also asserts the lesson's claims about the longest run.

**Complexity.**
- **Time** is O(n), because each index is visited once and each run writes at most four digits for a length up to 2000.
- **Space** is O(1), because the method keeps a few integers, and the digit text of one length has at most four characters.

```java run
import java.util.Arrays;

public final class StringCompression {
    /**
     * Compresses chars in place and returns the written length.
     * Time: O(n). Space: O(1), since a length of at most 2000 has four digits.
     * Invariant: chars[0..write-1] holds the compressed form of every closed run.
     */
    static int compress(char[] chars) {
        // write is the next index to fill, and start is the first index of the open run.
        int write = 0, start = 0;
        // The loop treats index chars.length as a boundary so the final run closes too.
        for (int i = 1; i <= chars.length; i++) {
            // A boundary appears at the end of the array or when the character differs from the run.
            if (i == chars.length || chars[i] != chars[start]) {
                // The run character is written once; write never exceeds start at this point.
                chars[write++] = chars[start];
                // A run of one character writes no length.
                int len = i - start;
                if (len >= 2) {
                    // Each digit of the length takes its own slot, so a length of 12 writes '1' then '2'.
                    for (char d : Integer.toString(len).toCharArray()) chars[write++] = d;
                }
                // The next run opens at the boundary index.
                start = i;
            }
        }
        // write is the length of the compressed prefix.
        return write;
    }

    /** Lesson code: the longest stretch by extending from every index, and the one-pass version. */
    static int naiveLongest(String s, long[] comparisons) {
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            int j = i;
            while (j < s.length() && s.charAt(j) == s.charAt(i)) { j++; comparisons[0]++; }
            best = Math.max(best, j - i);
        }
        return best;
    }

    static int longestRun(String s) {
        int best = 0, start = 0;
        for (int i = 1; i <= s.length(); i++) {
            if (i == s.length() || s.charAt(i) != s.charAt(start)) { best = Math.max(best, i - start); start = i; }
        }
        return best;
    }

    /** Oracle: builds the encoding with a builder from explicit runs. */
    static String oracle(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); ) {
            int j = i;
            while (j < s.length() && s.charAt(j) == s.charAt(i)) j++;
            sb.append(s.charAt(i));
            if (j - i >= 2) sb.append(j - i);
            i = j;
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // The statement examples.
        char[] a = "xxxyzz".toCharArray();
        int k = compress(a);
        if (k != 5 || !new String(a, 0, k).equals("x3yz2")) throw new AssertionError("example 1");
        char[] b = "kkkkkkkkkkkk".toCharArray();
        k = compress(b);
        if (k != 3 || !new String(b, 0, k).equals("k12")) throw new AssertionError("example 2");
        // One character, and no repeated neighbors.
        char[] c = {'q'};
        if (compress(c) != 1 || c[0] != 'q') throw new AssertionError("single character");
        char[] d = "abc".toCharArray();
        if (compress(d) != 3 || !new String(d).equals("abc")) throw new AssertionError("no runs");
        // Random arrays are checked against the oracle.
        java.util.Random rnd = new java.util.Random(61);
        for (int t = 0; t < 1000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(30);
            for (int x = 0; x < len; x++) sb.append((char) ('a' + (rnd.nextInt(4) == 0 ? rnd.nextInt(3) : 0)));
            String s = sb.toString();
            char[] arr = s.toCharArray();
            int w = compress(arr);
            if (!new String(arr, 0, w).equals(oracle(s))) throw new AssertionError("random " + s);
        }
        // A long run: 1 + digits(L) never exceeds L for L from 2 to 2000, so the write index stays behind.
        for (int len = 2; len <= 2000; len++) {
            if (1 + Integer.toString(len).length() > len) throw new AssertionError("write overtakes read at " + len);
        }
        // Lesson claim: the digit cast breaks for lengths of 10 or more, and append(int) writes the digits.
        if ((char) ('0' + 12) == '1') throw new AssertionError("cast hazard");
        if (!new StringBuilder().append(12).toString().equals("12")) throw new AssertionError("append int");
        // Lesson claim: the examples of the lesson text for both longest-run methods.
        long[] cmp = new long[1];
        if (naiveLongest("aabbbc", cmp) != 3 || longestRun("aabbbc") != 3) throw new AssertionError("aabbbc");
        if (naiveLongest("", cmp) != 0 || longestRun("") != 0) throw new AssertionError("empty");
        if (naiveLongest("abc", cmp) != 1 || longestRun("abc") != 1) throw new AssertionError("abc");
        if (longestRun("xyyy") != 3) throw new AssertionError("final run wins");
        // Lesson claim: n equal characters cost n(n + 1) / 2 comparisons in the extending method.
        cmp[0] = 0;
        naiveLongest("z".repeat(50), cmp);
        if (cmp[0] != 50L * 51 / 2) throw new AssertionError("comparison count " + cmp[0]);
        for (int t = 0; t < 300; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(12);
            for (int x = 0; x < len; x++) sb.append((char) ('a' + rnd.nextInt(2)));
            if (naiveLongest(sb.toString(), cmp) != longestRun(sb.toString())) throw new AssertionError("one pass against extension");
        }
    }
}
```

#### Solution: [Vary] Count And Say (LeetCode 38)
<!-- id: st-count-and-say -->

**Approach.**
The method starts from term 1 and builds each next term from the current one in a loop of `n - 1` rounds. Each round scans the current term with the run reader of this lesson. At every run boundary, including the end of the term, the round appends the run length and then the run digit to a new builder. The finished builder becomes the current term. The invariant is that before round `r`, `term` holds term `r - 1` of the sequence. The harness asserts a geometric growth bound to support the cost claim.

**Complexity.**
- **Time** is O(L_1 + L_2 + ... + L_n), where L_k is the length of term k, because each round reads one term once. The lengths grow geometrically, so this sum is a constant multiple of L_n.
- **Space** is O(L_n), because the method holds the current term and the next one.

```java run
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class CountAndSay {
    /**
     * Returns term n of the count-and-say sequence.
     * Time: O(L_1 + ... + L_n). Space: O(L_n).
     * Invariant: before round r, term holds term r - 1.
     */
    static String countAndSay(int n) {
        // Term 1 is given by the definition.
        String term = "1";
        // Each round builds the next term, so the loop runs n - 1 times.
        for (int round = 2; round <= n; round++) {
            StringBuilder next = new StringBuilder();
            int start = 0;
            // The index runs through term.length() so the final run closes at the end.
            for (int i = 1; i <= term.length(); i++) {
                // A boundary closes the run [start, i): its length, then its digit.
                if (i == term.length() || term.charAt(i) != term.charAt(start)) {
                    next.append(i - start).append(term.charAt(start));
                    start = i;
                }
            }
            // The new term replaces the old one for the next round.
            term = next.toString();
        }
        return term;
    }

    /** Oracle: a regular expression finds each maximal run of one digit. */
    static String oracle(int n) {
        String term = "1";
        Pattern p = Pattern.compile("(\\d)\\1*");
        for (int round = 2; round <= n; round++) {
            Matcher m = p.matcher(term);
            StringBuilder sb = new StringBuilder();
            while (m.find()) sb.append(m.group().length()).append(m.group(1));
            term = sb.toString();
        }
        return term;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!countAndSay(5).equals("111221")) throw new AssertionError("example 1");
        if (!countAndSay(2).equals("11")) throw new AssertionError("example 2");
        // The first terms of the sequence.
        String[] known = {"1", "11", "21", "1211", "111221", "312211", "13112221"};
        for (int n = 1; n <= known.length; n++) if (!countAndSay(n).equals(known[n - 1])) throw new AssertionError("term " + n);
        // Every n from 1 to 30 agrees with the oracle, and the terms use only digits 1 to 3.
        long total = 0;
        for (int n = 1; n <= 30; n++) {
            String t = countAndSay(n);
            if (!t.equals(oracle(n))) throw new AssertionError("oracle " + n);
            if (!t.matches("[123]+")) throw new AssertionError("digits " + n);
            total += t.length();
        }
        // The summed lengths stay within a small multiple of the last term, so the total cost is O(L_n).
        if (total > 6L * countAndSay(30).length()) throw new AssertionError("growth bound");
    }
}
```

#### Solution: [Boundary] Final Run (Author exercise)
<!-- id: st-final-run -->

**Approach.**
The method allocates an array of length `s.length()`, which is the largest possible number of runs. The loop runs `i` from 1 through `s.length()` and closes the open run at each boundary. A boundary is a different character at `i` or the end of the string, and closing writes the length `i - start` at the next free slot. The end-of-string boundary records the final run, so `"aaab"` produces both 3 and 1. The method copies the used part into an array of the exact size. The invariant is that `lengths[0..count-1]` holds the lengths of all closed runs.

**Complexity.**
- **Time** is O(n), because the loop makes n iterations and the final copy reads at most n entries.
- **Space** is O(n), because the working array has n entries.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FinalRun {
    /**
     * Returns the lengths of the maximal runs of s from left to right.
     * Time: O(n). Space: O(n) for the working array.
     * Invariant: lengths[0..count-1] holds the lengths of all closed runs.
     */
    static int[] runLengths(String s) {
        // The array has room for the most runs possible, which is one per character.
        int[] lengths = new int[s.length()];
        int count = 0, start = 0;
        // The index runs through s.length() so the final run closes at the end.
        for (int i = 1; i <= s.length(); i++) {
            // A boundary closes the open run.
            if (i == s.length() || s.charAt(i) != s.charAt(start)) {
                // The closed run has length i - start, and the next run opens at i.
                lengths[count++] = i - start;
                start = i;
            }
        }
        // Trimming the array gives the exact answer; an empty string gives length 0.
        return Arrays.copyOf(lengths, count);
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(runLengths("aaab"), new int[] {3, 1})) throw new AssertionError("example 1");
        if (runLengths("").length != 0) throw new AssertionError("example 2");
        // Equal letters far apart form separate runs, which the lesson states.
        if (!Arrays.equals(runLengths("aabaa"), new int[] {2, 1, 2})) throw new AssertionError("separate runs");
        if (!Arrays.equals(runLengths("z"), new int[] {1})) throw new AssertionError("one character");
        // Random strings are checked against a regular-expression oracle, and the entries add up to the length.
        Random rnd = new Random(62);
        for (int t = 0; t < 800; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(14);
            for (int x = 0; x < len; x++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            java.util.regex.Matcher m = java.util.regex.Pattern.compile("(.)\\1*").matcher(s);
            java.util.List<Integer> expect = new java.util.ArrayList<>();
            while (m.find()) expect.add(m.group().length());
            int[] got = runLengths(s);
            if (got.length != expect.size()) throw new AssertionError("count " + s);
            int sum = 0;
            for (int x = 0; x < got.length; x++) { if (got[x] != expect.get(x)) throw new AssertionError("entry " + s); sum += got[x]; }
            if (sum != s.length()) throw new AssertionError("sum " + s);
        }
    }
}
```

#### Solution: [Recognize] Run-Length Encoding (Author exercise)
<!-- id: st-run-length-encoding -->

**Approach.**
The method uses the same boundary loop and emits each run as it closes. At a boundary, the builder receives the decimal length `i - start`, then the run character. The call `append(int)` writes all digits of the length, so a run of 12 appears as `12`. The end-of-string boundary emits the final run, and the empty string never enters the loop, so the answer is the empty string. The invariant is that the builder holds the encoding of all closed runs, and each run appears exactly once.

**Complexity.**
- **Time** is O(n), because the loop reads each character once and each run appends a constant number of characters plus its digits.
- **Space** is O(n), because the output has at most 2n characters for a length of one per run, and at most n runs.

```java run
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class RunLengthEncoding {
    /**
     * Encodes s as the length and the character of each maximal run.
     * Time: O(n). Space: O(n) for the builder.
     * Invariant: out holds the encoding of every closed run, and each run was appended once.
     */
    static String encode(String s) {
        StringBuilder out = new StringBuilder();
        int start = 0;
        // The index runs through s.length() so the final run closes at the end.
        for (int i = 1; i <= s.length(); i++) {
            // A boundary closes the open run.
            if (i == s.length() || s.charAt(i) != s.charAt(start)) {
                // The length is appended as an int, so a length of 12 writes both digits.
                out.append(i - start).append(s.charAt(start));
                start = i;
            }
        }
        // An empty input leaves the builder empty.
        return out.toString();
    }

    public static void main(String[] args) {
        // The statement examples; the first has a two-digit length.
        if (!encode("xxxxxxxxxxxxy").equals("12x1y")) throw new AssertionError("example 1");
        if (!encode("").equals("")) throw new AssertionError("example 2");
        // A single character, and a string whose last run has length one.
        if (!encode("a").equals("1a")) throw new AssertionError("single");
        if (!encode("aaabbc").equals("3a2b1c")) throw new AssertionError("mixed");
        // Random strings are checked against a regular-expression oracle.
        Random rnd = new Random(63);
        Pattern p = Pattern.compile("(.)\\1*");
        for (int t = 0; t < 800; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(16);
            for (int x = 0; x < len; x++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            Matcher m = p.matcher(s);
            StringBuilder expect = new StringBuilder();
            while (m.find()) expect.append(m.group().length()).append(m.group(1));
            if (!encode(s).equals(expect.toString())) throw new AssertionError("random " + s);
        }
    }
}
```
