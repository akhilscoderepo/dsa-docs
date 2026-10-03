<!-- solutions-for: 06-run-construction -->
### Run Construction

#### Solution: [Build] String Compression (LeetCode 443)
<!-- id: st-string-compression -->

**Approach.** Hold the pending run as a character and a length. Whenever the next character differs, or the end of the array is reached, flush by writing the character and then the digits of the length if it exceeds 1. The write position never passes the read position, because a run of length 1 writes one character, a run of length 2 writes two and every longer run writes fewer characters than it consumes. The assertions rebuild the expected compressed form with a different method, which scans forward from each run start, and compare it with the in-place result on random arrays, including runs of length 10 or more.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class StringCompression {
    static int compress(char[] chars) {
        if (chars.length == 0) return 0;
        int write = 0;
        char cur = chars[0];
        int len = 1;
        for (int i = 1; i <= chars.length; i++) {
            if (i < chars.length && chars[i] == cur) { len++; continue; }
            chars[write++] = cur;
            if (len > 1) for (char d : Integer.toString(len).toCharArray()) chars[write++] = d;
            if (i < chars.length) { cur = chars[i]; len = 1; }
        }
        return write;
    }
    static String oracle(char[] chars) {
        StringBuilder sb = new StringBuilder();
        int start = 0;
        while (start < chars.length) {
            int end = start;
            while (end < chars.length && chars[end] == chars[start]) end++;
            sb.append(chars[start]);
            if (end - start > 1) sb.append(end - start);
            start = end;
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        char[] a = "zzzzyyx".toCharArray();
        int n = compress(a);
        if (n != 5 || !new String(a, 0, n).equals("z4y2x")) throw new AssertionError("example 1");
        char[] b = {'q'};
        if (compress(b) != 1 || b[0] != 'q') throw new AssertionError("example 2");
        char[] c = new char[12];
        Arrays.fill(c, 'k');
        int m = compress(c);
        if (m != 3 || !new String(c, 0, m).equals("k12")) throw new AssertionError("two digit count");
        Random rnd = new Random(61);
        for (int t = 0; t < 4000; t++) {
            char[] x = new char[1 + rnd.nextInt(30)];
            for (int i = 0; i < x.length; i++) x[i] = (char) ('a' + (rnd.nextInt(5) == 0 ? rnd.nextInt(3) : 0) + (i / 7 % 2));
            String expected = oracle(x);
            int len = compress(x);
            if (len != expected.length() || !new String(x, 0, len).equals(expected)) throw new AssertionError("disagrees with the oracle: " + expected);
        }
    }
}
```

#### Solution: [Vary] Count and Say (LeetCode 38)
<!-- id: st-count-and-say -->

**Approach.** Start from `"1"` and apply the run encoder `n - 1` times, since each term reads the previous one as runs of equal digits and writes count then digit. The buffer-based encoder keeps each step linear in the length of its input. The first six terms are `1`, `11`, `21`, `1211`, `111221` and `312211`, and the assertions check them, then compare the encoder against a second implementation that scans forward from each run start, and confirm that only the digits 1, 2 and 3 appear.

**Complexity.** O(L) time for the final term of length L, plus the lengths of the earlier terms, and O(L) space.

```java run
public final class CountAndSay {
    static String encode(String s) {
        StringBuilder out = new StringBuilder();
        char cur = s.charAt(0);
        int len = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == cur) len++;
            else { out.append(len).append(cur); cur = s.charAt(i); len = 1; }
        }
        out.append(len).append(cur);
        return out.toString();
    }
    static String countAndSay(int n) {
        String term = "1";
        for (int step = 1; step < n; step++) term = encode(term);
        return term;
    }
    static String viaForwardScan(String s) {
        StringBuilder sb = new StringBuilder();
        int start = 0;
        while (start < s.length()) {
            int end = start;
            while (end < s.length() && s.charAt(end) == s.charAt(start)) end++;
            sb.append(end - start).append(s.charAt(start));
            start = end;
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        String[] known = {"1", "11", "21", "1211", "111221", "312211"};
        for (int i = 0; i < known.length; i++)
            if (!countAndSay(i + 1).equals(known[i])) throw new AssertionError("term " + (i + 1));
        String term = "1";
        for (int n = 1; n <= 20; n++) {
            if (!countAndSay(n).equals(term)) throw new AssertionError("term " + n + " differs from the chain");
            for (char ch : term.toCharArray()) if (ch < '1' || ch > '3') throw new AssertionError("unexpected digit in term " + n);
            term = viaForwardScan(term);
        }
    }
}
```

#### Solution: [Boundary] Final Run (Author exercise)
<!-- id: st-final-run -->

**Approach.** The pending run ends when the character changes or when the input ends. A loop that only writes on a change never fires for the last run, so `aaab` loses its `1b` and `zz` produces the empty string. The correct version performs one more flush after the loop, and it returns the empty string for an empty input before reading a first character. The assertions compare the faulty loop and the correct one on the examples, and then check that decoding the correct output returns the original string on random inputs.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.Random;

public final class FinalRun {
    static String encode(String s) {
        if (s.isEmpty()) return "";
        StringBuilder out = new StringBuilder();
        char cur = s.charAt(0);
        int len = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == cur) len++;
            else { out.append(len).append(cur); cur = s.charAt(i); len = 1; }
        }
        out.append(len).append(cur);
        return out.toString();
    }
    static String forgetsTheLast(String s) {
        if (s.isEmpty()) return "";
        StringBuilder out = new StringBuilder();
        char cur = s.charAt(0);
        int len = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == cur) len++;
            else { out.append(len).append(cur); cur = s.charAt(i); len = 1; }
        }
        return out.toString();
    }
    static String decode(String enc) {
        StringBuilder sb = new StringBuilder();
        int i = 0;
        while (i < enc.length()) {
            int count = 0;
            while (Character.isDigit(enc.charAt(i))) count = count * 10 + (enc.charAt(i++) - '0');
            char c = enc.charAt(i++);
            for (int k = 0; k < count; k++) sb.append(c);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        if (!encode("aaab").equals("3a1b")) throw new AssertionError("example 1");
        if (!encode("zz").equals("2z")) throw new AssertionError("example 2");
        if (!encode("").isEmpty()) throw new AssertionError("empty string");
        if (!forgetsTheLast("aaab").equals("3a")) throw new AssertionError("the faulty loop must drop 1b");
        if (!forgetsTheLast("zz").isEmpty()) throw new AssertionError("the faulty loop must drop the only run");
        Random rnd = new Random(62);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(25);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!decode(encode(s)).equals(s)) throw new AssertionError("round trip failed for " + s);
        }
    }
}
```

#### Solution: [Recognize] Run-Length Encoding (Author exercise)
<!-- id: st-run-length-encoding -->

**Approach.** Keep the pending run, write count then character on each change, and flush once more after the loop. Equal characters that are not neighbours stay in separate runs, so `abab` encodes to `1a1b1a1b`. A table of totals cannot reproduce that, since it keeps no positions. The assertions check that the output decodes back to the input, that no two consecutive runs in the output share a character, which is what makes every run maximal, and that the number of runs equals one plus the number of positions where neighbours differ.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RunLengthEncoding {
    static String encode(String s) {
        if (s.isEmpty()) return "";
        StringBuilder out = new StringBuilder();
        char cur = s.charAt(0);
        int len = 1;
        for (int i = 1; i < s.length(); i++) {
            if (s.charAt(i) == cur) len++;
            else { out.append(len).append(cur); cur = s.charAt(i); len = 1; }
        }
        out.append(len).append(cur);
        return out.toString();
    }
    static List<int[]> parse(String enc) {                  // each entry is {count, character}
        List<int[]> runs = new ArrayList<>();
        int i = 0;
        while (i < enc.length()) {
            int count = 0;
            while (Character.isDigit(enc.charAt(i))) count = count * 10 + (enc.charAt(i++) - '0');
            runs.add(new int[] {count, enc.charAt(i++)});
        }
        return runs;
    }

    public static void main(String[] args) {
        if (!encode("aaabbc").equals("3a2b1c")) throw new AssertionError("example 1");
        if (!encode("abab").equals("1a1b1a1b")) throw new AssertionError("example 2");
        if (!encode("").isEmpty()) throw new AssertionError("empty string");
        Random rnd = new Random(63);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(30);
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            List<int[]> runs = parse(encode(s));
            StringBuilder back = new StringBuilder();
            for (int[] r : runs) for (int k = 0; k < r[0]; k++) back.append((char) r[1]);
            if (!back.toString().equals(s)) throw new AssertionError("round trip failed for " + s);
            for (int k = 1; k < runs.size(); k++)
                if (runs.get(k)[1] == runs.get(k - 1)[1]) throw new AssertionError("adjacent runs share a character in " + s);
            int changes = 0;
            for (int i = 1; i < s.length(); i++) if (s.charAt(i) != s.charAt(i - 1)) changes++;
            if (runs.size() != (s.isEmpty() ? 0 : changes + 1)) throw new AssertionError("run count for " + s);
        }
    }
}
```
