<!-- solutions-for: 09-nested-decoding -->
### Nested Decoding

#### Solution: [Build] Decode One Flat Group (Author exercise)
<!-- id: sq-decode-flat-group -->

**Approach.** With one level there is nothing to park. Copy letters to the output until the digit, remember the digit as the count, collect the letters up to the closing bracket into a buffer, append the buffer `count` times, and copy the letters after the bracket. The count is a single digit here, read as `c - '0'`. The assertions compare with the rewriting method of the lesson on random inputs of this shape, and check `String.repeat` with a zero count and with a negative count, since the behaviour for those values is part of the contract.

**Complexity.** O(n + L) time for output length L, and O(L) space.

```java run
import java.util.Random;

public final class DecodeFlatGroup {
    static String decode(String s) {
        StringBuilder out = new StringBuilder();
        int i = 0;
        while (i < s.length() && !Character.isDigit(s.charAt(i))) out.append(s.charAt(i++));
        if (i < s.length()) {
            int count = s.charAt(i) - '0';
            i += 2;
            StringBuilder body = new StringBuilder();
            while (s.charAt(i) != ']') body.append(s.charAt(i++));
            i++;
            out.append(body.toString().repeat(count));
            while (i < s.length()) out.append(s.charAt(i++));
        }
        return out.toString();
    }
    static String rewriting(String s) {
        String cur = s;
        while (cur.indexOf(']') >= 0) {
            int close = cur.indexOf(']');
            int open = cur.lastIndexOf('[', close);
            int ds = open;
            while (ds > 0 && Character.isDigit(cur.charAt(ds - 1))) ds--;
            int count = Integer.parseInt(cur.substring(ds, open));
            cur = cur.substring(0, ds) + cur.substring(open + 1, close).repeat(count) + cur.substring(close + 1);
        }
        return cur;
    }

    public static void main(String[] args) {
        if (!decode("3[ab]").equals("ababab")) throw new AssertionError("example 1");
        if (!decode("x2[yz]w").equals("xyzyzw")) throw new AssertionError("example 2");
        if (!"ab".repeat(0).isEmpty()) throw new AssertionError("a zero count gives the empty string");
        try { "ab".repeat(-1); throw new AssertionError("a negative count must throw"); } catch (IllegalArgumentException expected) { }
        if ('7' - '0' != 7) throw new AssertionError("digit arithmetic");
        Random rnd = new Random(11901);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = rnd.nextInt(3); i > 0; i--) sb.append((char) ('a' + rnd.nextInt(3)));
            sb.append(1 + rnd.nextInt(9)).append('[');
            for (int i = 1 + rnd.nextInt(3); i > 0; i--) sb.append((char) ('a' + rnd.nextInt(3)));
            sb.append(']');
            for (int i = rnd.nextInt(3); i > 0; i--) sb.append((char) ('a' + rnd.nextInt(3)));
            String s = sb.toString();
            if (!decode(s).equals(rewriting(s))) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Vary] Multi-Digit Repeat Count (Author exercise)
<!-- id: sq-multi-digit-count -->

**Approach.** Accumulate the count with `count = count * 10 + digit` while digits are being read, and reset it to zero at the opening bracket after using it. Letters and group bodies are collected as before, and several groups may follow each other, since the count restarts for each. A decoder that used only the last digit would read 12 as 2, and the assertions show that on the first example. They compare with the rewriting method on random inputs with counts up to 300.

**Complexity.** O(n + L) time and O(L) space.

```java run
import java.util.Random;

public final class MultiDigitCount {
    static String decode(String s, boolean accumulate) {
        StringBuilder out = new StringBuilder();
        int count = 0, i = 0;
        while (i < s.length()) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                count = accumulate ? count * 10 + (c - '0') : c - '0';
                i++;
            } else if (c == '[') {
                int close = s.indexOf(']', i);
                out.append(s.substring(i + 1, close).repeat(count));
                count = 0;
                i = close + 1;
            } else { out.append(c); i++; }
        }
        return out.toString();
    }
    static String rewriting(String s) {
        String cur = s;
        while (cur.indexOf(']') >= 0) {
            int close = cur.indexOf(']');
            int open = cur.lastIndexOf('[', close);
            int ds = open;
            while (ds > 0 && Character.isDigit(cur.charAt(ds - 1))) ds--;
            int count = Integer.parseInt(cur.substring(ds, open));
            cur = cur.substring(0, ds) + cur.substring(open + 1, close).repeat(count) + cur.substring(close + 1);
        }
        return cur;
    }

    public static void main(String[] args) {
        if (!decode("12[a]", true).equals("a".repeat(12))) throw new AssertionError("example 1");
        if (!decode("10[ab]c", true).equals("ab".repeat(10) + "c")) throw new AssertionError("example 2");
        if (decode("12[a]", false).equals("a".repeat(12))) throw new AssertionError("using the last digit only reads 12 as 2");
        Random rnd = new Random(11902);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int g = rnd.nextInt(4); g >= 0; g--) {
                for (int i = rnd.nextInt(3); i > 0; i--) sb.append((char) ('a' + rnd.nextInt(3)));
                sb.append(1 + rnd.nextInt(300)).append('[');
                for (int i = 1 + rnd.nextInt(3); i > 0; i--) sb.append((char) ('a' + rnd.nextInt(3)));
                sb.append(']');
            }
            String s = sb.toString();
            if (!decode(s, true).equals(rewriting(s))) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Boundary] Adjacent And Nested Groups (Author exercise)
<!-- id: sq-adjacent-nested-groups -->

**Approach.** Park the current row and the count at each opening bracket, start a fresh row, and at each closing bracket repeat the finished row, pop the parked row, and append the repeated text to it. After a group closes the parked row is current again, so the next group starts from it with a fresh count. The assertions compare with a recursive-descent decoder that finds each group by counting brackets, and they check the first example and a triple-nested example, as well as a stack-free version that uses one global builder and so mixes inner and outer rows.

**Complexity.** O(n + L * d) time for output length L and depth d, and O(n + L) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class AdjacentNestedGroups {
    static String decode(String s) {
        ArrayDeque<Integer> counts = new ArrayDeque<>();
        ArrayDeque<StringBuilder> rows = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') count = count * 10 + (c - '0');
            else if (c == '[') { counts.addLast(count); rows.addLast(cur); cur = new StringBuilder(); count = 0; }
            else if (c == ']') { String body = cur.toString(); cur = rows.removeLast(); cur.append(body.repeat(counts.removeLast())); }
            else cur.append(c);
        }
        return cur.toString();
    }
    static String recursive(String s, int lo, int hi) {
        StringBuilder out = new StringBuilder();
        int i = lo;
        while (i < hi) {
            char c = s.charAt(i);
            if (Character.isDigit(c)) {
                int count = 0;
                while (Character.isDigit(s.charAt(i))) count = count * 10 + (s.charAt(i++) - '0');
                int depth = 0, j = i;
                do { depth += s.charAt(j) == '[' ? 1 : s.charAt(j) == ']' ? -1 : 0; j++; } while (depth > 0);
                out.append(recursive(s, i + 1, j - 1).repeat(count));
                i = j;
            } else { out.append(c); i++; }
        }
        return out.toString();
    }
    static String singleBuilder(String s) {
        StringBuilder all = new StringBuilder();
        int count = 0;
        ArrayDeque<Integer> starts = new ArrayDeque<>(), counts = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isDigit(c)) count = count * 10 + (c - '0');
            else if (c == '[') { counts.addLast(count); starts.addLast(0); count = 0; }
            else if (c == ']') { String body = all.toString(); all = new StringBuilder(body.repeat(counts.removeLast())); starts.removeLast(); }
            else all.append(c);
        }
        return all.toString();
    }
    static void build(Random rnd, StringBuilder sb, int depth) {
        for (int parts = 1 + rnd.nextInt(3); parts > 0; parts--) {
            if (depth > 0 && rnd.nextInt(3) == 0) {
                sb.append(1 + rnd.nextInt(3)).append('[');
                build(rnd, sb, depth - 1);
                sb.append(']');
            } else sb.append((char) ('a' + rnd.nextInt(3)));
        }
    }

    public static void main(String[] args) {
        if (!decode("2[a]3[b2[c]]").equals("aabccbccbcc")) throw new AssertionError("example 1");
        if (!decode("2[2[2[a]]]").equals("aaaaaaaa")) throw new AssertionError("example 2");
        if (singleBuilder("a2[b]c").equals(decode("a2[b]c"))) throw new AssertionError("one global builder repeats text outside the group");
        Random rnd = new Random(11903);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 4);
            String s = sb.toString();
            if (!decode(s).equals(recursive(s, 0, s.length()))) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Recognize] Decode String (LeetCode 394)
<!-- id: sq-decode-string -->

**Approach.** Read the string once with a digit accumulator, a current builder and two parallel stacks for parked counts and parked builders. Letters go to the current builder, an opening bracket parks the count and the builder, and a closing bracket repeats the finished body, restores the parent builder and appends. After the last character, the current builder holds the whole answer. The assertions compare with a rewriting method that expands the first innermost group in place and repeats, and with a recursive decoder, on random well-formed inputs including multi-digit counts and several groups in one row.

**Complexity.** O(n + L * d) time for output length L and nesting depth d, and O(n + L) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class DecodeStringSolution {
    static String decode(String s) {
        ArrayDeque<Integer> counts = new ArrayDeque<>();
        ArrayDeque<StringBuilder> rows = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') count = count * 10 + (c - '0');
            else if (c == '[') { counts.addLast(count); rows.addLast(cur); cur = new StringBuilder(); count = 0; }
            else if (c == ']') { String body = cur.toString(); cur = rows.removeLast(); cur.append(body.repeat(counts.removeLast())); }
            else cur.append(c);
        }
        return cur.toString();
    }
    static String rewriting(String s) {
        String cur = s;
        while (cur.indexOf(']') >= 0) {
            int close = cur.indexOf(']');
            int open = cur.lastIndexOf('[', close);
            int ds = open;
            while (ds > 0 && Character.isDigit(cur.charAt(ds - 1))) ds--;
            int count = Integer.parseInt(cur.substring(ds, open));
            cur = cur.substring(0, ds) + cur.substring(open + 1, close).repeat(count) + cur.substring(close + 1);
        }
        return cur;
    }
    static void build(Random rnd, StringBuilder sb, int depth) {
        for (int parts = 1 + rnd.nextInt(3); parts > 0; parts--) {
            if (depth > 0 && rnd.nextInt(3) == 0) {
                sb.append(rnd.nextInt(2) == 0 ? 2 + rnd.nextInt(3) : 10 + rnd.nextInt(3)).append('[');
                build(rnd, sb, depth - 1);
                sb.append(']');
            } else sb.append((char) ('a' + rnd.nextInt(4)));
        }
    }

    public static void main(String[] args) {
        if (!decode("2[x3[y]z]").equals("xyyyzxyyyz")) throw new AssertionError("example 1");
        if (!decode("ab2[c]").equals("abcc")) throw new AssertionError("example 2");
        if (!decode("abc").equals("abc")) throw new AssertionError("no group at all");
        Random rnd = new Random(11904);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 3);
            String s = sb.toString();
            if (!decode(s).equals(rewriting(s))) throw new AssertionError("differs on " + s);
        }
    }
}
```
