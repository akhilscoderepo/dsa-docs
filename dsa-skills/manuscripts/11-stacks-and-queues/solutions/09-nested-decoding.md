<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Nested Decoding

#### Solution: [Build] Decode One Flat Group (Author exercise)
<!-- id: sq-decode-flat-group -->

**Approach.**
The method reads the text once from left to right. The first character is a digit, so it goes into `count`. The `[` needs no frame for a flat group, because no text exists outside the group. Each letter after it goes into `cur`. At the `]` the method appends the finished body `count` times to a result. The invariant is that `cur` holds the letters of the body read so far, and `count` still holds the repeat number until the group closes.

**Complexity.**
- **Time** is O(n + L), because each input character is read once and each output character is written once.
- **Space** is O(L) for the result, plus O(b) for the body of length `b`.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class DecodeFlatGroup {
    /**
     * Decodes one text of the form d[body].
     * Time: O(n + L) for input length n and output length L.
     * Space: O(L), the body and the result.
     * Invariant: cur holds the body letters read so far; count holds the digit.
     */
    static String decodeFlat(String s) {
        StringBuilder cur = new StringBuilder();
        StringBuilder result = new StringBuilder();
        int count = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            // A digit builds the repeat number.
            if (c >= '0' && c <= '9') count = count * 10 + (c - '0');
            // The bracket opens the body; no text exists outside it, so nothing is saved.
            else if (c == '[') cur.setLength(0);
            // The closing bracket writes the finished body count times.
            else if (c == ']') for (int t = 0; t < count; t++) result.append(cur);
            // Any other character belongs to the body.
            else cur.append(c);
        }
        return result.toString();
    }

    public static void main(String[] args) {
        // Example 1 and Example 2.
        if (!decodeFlat("4[xy]").equals("xyxyxyxy")) throw new AssertionError("example 1");
        if (!decodeFlat("5[]").isEmpty()) throw new AssertionError("example 2");
        // ArrayDeque push and pop use the first position, so the last pushed value pops first.
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        dq.push(1);
        dq.push(2);
        if (dq.peekFirst() != 2 || dq.pop() != 2 || dq.pop() != 1) throw new AssertionError("push and pop order");
        // Random groups agree with String.repeat.
        Random rnd = new Random(1101);
        for (int t = 0; t < 3000; t++) {
            int d = 1 + rnd.nextInt(9);
            StringBuilder body = new StringBuilder();
            for (int k = rnd.nextInt(8); k > 0; k--) body.append((char) ('a' + rnd.nextInt(26)));
            String in = d + "[" + body + "]";
            if (!decodeFlat(in).equals(body.toString().repeat(d))) throw new AssertionError("random " + in);
        }
    }
}
```

#### Solution: [Vary] Multi-Digit Repeat Count (Author exercise)
<!-- id: sq-multi-digit-repeat -->

**Approach.**
A digit extends the number, so each digit changes `count` to `count * 10 + digit`. After `1` the number is 1, and after the next digit `0` it is 10. The method must not use the number before the `[`, because the next character could be another digit. The rest is the same as the flat case. The invariant is that `count` equals the decimal number formed by the digits read since the last non-digit.

**Complexity.**
- **Time** is O(n + L), because each input character is read once and each output character is written once.
- **Space** is O(L) for the result and the body.

```java run
import java.util.Random;

public final class MultiDigitRepeat {
    /**
     * Decodes n[body] where n has one or more digits.
     * Time: O(n + L) for input length n and output length L.
     * Space: O(L).
     * Invariant: count is the number formed by the digits read since the last non-digit.
     */
    static String decodeNumber(String s) {
        StringBuilder body = new StringBuilder();
        int count = 0;
        int i = 0;
        // The digits come first, and each one extends the number by one decimal place.
        while (s.charAt(i) != '[') {
            count = count * 10 + (s.charAt(i) - '0');
            i++;
        }
        // The body runs from after the bracket to just before the closing bracket.
        for (i = i + 1; s.charAt(i) != ']'; i++) body.append(s.charAt(i));
        // The finished body is written count times.
        StringBuilder result = new StringBuilder();
        for (int t = 0; t < count; t++) result.append(body);
        return result.toString();
    }

    public static void main(String[] args) {
        // Example 1 and Example 2.
        if (!decodeNumber("10[z]").equals("zzzzzzzzzz")) throw new AssertionError("example 1");
        if (!decodeNumber("11[mn]").equals("mnmnmnmnmnmnmnmnmnmnmn")) throw new AssertionError("example 2");
        // The digit-by-digit update gives the same number as parsing the digits at once.
        if (decodeNumber("999[]").length() != 0 || decodeNumber("100[a]").length() != 100) throw new AssertionError("hundreds");
        // Character.isDigit accepts digits from other scripts, so the range test is the safer check.
        if (!Character.isDigit('٣') || ('٣' >= '0' && '٣' <= '9')) throw new AssertionError("isDigit");
        // Random numbers agree with Integer.parseInt and String.repeat.
        Random rnd = new Random(1102);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(999);
            StringBuilder body = new StringBuilder();
            for (int k = rnd.nextInt(6); k > 0; k--) body.append((char) ('a' + rnd.nextInt(26)));
            String in = n + "[" + body + "]";
            int parsed = Integer.parseInt(in.substring(0, in.indexOf('[')));
            if (!decodeNumber(in).equals(body.toString().repeat(parsed))) throw new AssertionError("random " + in);
        }
    }
}
```

#### Solution: [Boundary] Adjacent And Nested Groups (Author exercise)
<!-- id: sq-adjacent-nested-groups -->

**Approach.**
The method keeps `cur` and `count` and one stack of frames. At `[` it saves the parent text and the number, then gives `cur` a fresh empty builder and sets `count` to 0. At `]` it pops the frame, appends the body to the parent text as many times as the frame says, and returns to the parent. Two adjacent groups never share state, because the first `]` has already popped the frame before the next `[` pushes a new one. An empty body appends nothing, so the group disappears. The invariant is that the stack has one frame for each open group.

**Complexity.**
- **Time** is O(n + L * d), because each `]` copies its body once per repetition and a character is copied once for each enclosing group.
- **Space** is O(d) frames plus the text those frames hold.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class AdjacentNestedGroups {
    /**
     * Decodes letters and groups d[body] with one-digit numbers.
     * Time: O(n + L * d) for output length L and depth d.
     * Space: O(d) frames plus saved text.
     * Invariant: stack size equals the number of open groups.
     */
    static String decode(String s) {
        ArrayDeque<StringBuilder> parents = new ArrayDeque<>();
        ArrayDeque<Integer> repeats = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int count = 0;
        // One pass handles each character once.
        for (char c : s.toCharArray()) {
            if (c >= '0' && c <= '9') {
                // The digit is the number for the next group.
                count = c - '0';
            } else if (c == '[') {
                // Save the parent text and the number, then start an empty group.
                parents.push(cur);
                repeats.push(count);
                cur = new StringBuilder();
                count = 0;
            } else if (c == ']') {
                // Close the group by appending its body to the parent text.
                StringBuilder parent = parents.pop();
                int times = repeats.pop();
                for (int t = 0; t < times; t++) parent.append(cur);
                cur = parent;
            } else {
                // A letter extends the text of the innermost open group.
                cur.append(c);
            }
        }
        return cur.toString();
    }

    /** Reference: rewrite the first innermost group until none is left. */
    static String oracle(String s) {
        // The first ] always closes a group that has no group inside.
        while (s.indexOf(']') >= 0) {
            int close = s.indexOf(']');
            int open = s.lastIndexOf('[', close);
            int times = s.charAt(open - 1) - '0';
            s = s.substring(0, open - 1) + s.substring(open + 1, close).repeat(times) + s.substring(close + 1);
        }
        return s;
    }

    static String gen(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        // A random mix of letters and groups, deeper groups becoming less likely.
        for (int k = rnd.nextInt(4); k > 0; k--) {
            if (depth < 3 && rnd.nextInt(3) == 0) sb.append(1 + rnd.nextInt(3)).append('[').append(gen(rnd, depth + 1)).append(']');
            else sb.append((char) ('a' + rnd.nextInt(3)));
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1: adjacent groups with a nested group in the second.
        if (!decode("2[a]3[b2[c]]").equals("aabccbccbcc")) throw new AssertionError("example 1");
        // Example 2: an empty inner body vanishes and the outer group repeats the rest.
        if (!decode("2[2[]a]").equals("aa")) throw new AssertionError("example 2");
        // The empty text decodes to the empty text.
        if (!decode("").isEmpty()) throw new AssertionError("empty");
        // Random well-formed texts agree with the rewriting reference.
        Random rnd = new Random(1103);
        for (int t = 0; t < 4000; t++) {
            String in = gen(rnd, 0);
            if (!decode(in).equals(oracle(in))) throw new AssertionError("random " + in);
        }
    }
}
```

#### Solution: [Recognize] Decode String (LeetCode 394)
<!-- id: sq-leetcode-decode-string -->

**Approach.**
The cue is a number that applies to a bracketed text that can contain further groups. The method combines the pieces of the earlier exercises. Digits build `count` by `count * 10 + digit`. A `[` pushes one frame that holds the parent text and the number, and starts an empty current text. A `]` pops the frame and appends the body to the parent text that many times. The invariant is that the current text belongs to the innermost open group and the stack has one frame for each group around it. This version stores each frame in a small record and uses one stack.

**Complexity.**
- **Time** is O(n + L * d), because a character is copied once for each group that encloses it.
- **Space** is O(d) frames plus the text those frames hold.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class DecodeString {
    /** One saved level: the text before the group and the number the group repeats. */
    record Frame(StringBuilder parent, int times) {}

    /**
     * Decodes a well-formed encoded string.
     * Time: O(n + L * d) for output length L and depth d.
     * Space: O(d) frames plus saved text.
     * Invariant: cur is the innermost open group so far; the stack has one frame per open group.
     */
    static String decodeString(String s) {
        ArrayDeque<Frame> stack = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int count = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                // Each digit extends the number by one decimal place.
                count = count * 10 + (c - '0');
            } else if (c == '[') {
                // Save the parent text with the number, then start a new empty group.
                stack.push(new Frame(cur, count));
                cur = new StringBuilder();
                count = 0;
            } else if (c == ']') {
                // The group is complete, so it joins its parent as many times as the frame says.
                Frame f = stack.pop();
                for (int t = 0; t < f.times(); t++) f.parent().append(cur);
                cur = f.parent();
            } else {
                // A letter extends the innermost open group.
                cur.append(c);
            }
        }
        return cur.toString();
    }

    // Recursive-descent reference with a shared read position.
    static int pos;

    static String oracle(String s) {
        pos = 0;
        return parseSeq(s);
    }

    static String parseSeq(String s) {
        StringBuilder out = new StringBuilder();
        // A sequence ends at the end of the text or at the bracket that closes the caller's group.
        while (pos < s.length() && s.charAt(pos) != ']') {
            if (Character.isLetter(s.charAt(pos))) {
                out.append(s.charAt(pos++));
            } else {
                int n = 0;
                while (Character.isDigit(s.charAt(pos))) n = n * 10 + (s.charAt(pos++) - '0');
                pos++;
                String inner = parseSeq(s);
                pos++;
                out.append(inner.repeat(n));
            }
        }
        return out.toString();
    }

    static String gen(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        // Numbers have one to three digits, so the multi-digit path runs often.
        for (int k = rnd.nextInt(4); k > 0; k--) {
            if (depth < 3 && rnd.nextInt(3) == 0) {
                int n = rnd.nextInt(4) == 0 ? 10 + rnd.nextInt(30) : 1 + rnd.nextInt(4);
                sb.append(n).append('[').append(gen(rnd, depth + 1)).append(']');
            } else {
                sb.append((char) ('a' + rnd.nextInt(4)));
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1: a nested group followed by a letter outside every group.
        if (!decodeString("3[a2[b]]c").equals("abbabbabbc")) throw new AssertionError("example 1");
        // Example 2: letters on both sides of a nested group.
        if (!decodeString("a2[b3[c]]d").equals("abcccbcccd")) throw new AssertionError("example 2");
        // A two-digit number and the empty input.
        if (!decodeString("12[a2[b]]").equals("abb".repeat(12))) throw new AssertionError("two digits");
        if (!decodeString("").isEmpty()) throw new AssertionError("empty");
        // Random well-formed texts agree with the recursive-descent reference.
        Random rnd = new Random(1104);
        for (int t = 0; t < 4000; t++) {
            String in = gen(rnd, 0);
            if (!decodeString(in).equals(oracle(in))) throw new AssertionError("random " + in);
        }
    }
}
```
