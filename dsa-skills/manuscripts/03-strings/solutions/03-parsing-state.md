<!-- solutions-for: 03-strings -->
### Solutions For Character Parsing

#### Solution: [Build] Parse A Signed Integer Token (Author exercise)
<!-- id: st-signed-token -->

**Approach.**
The parser has three states. `START` means nothing is read, `SIGN` means a sign is read and no digit follows yet, and `DIGITS` means at least one digit is read. In `START`, a sign moves to `SIGN` and a digit moves to `DIGITS`. In `SIGN` and in `DIGITS`, a digit moves to `DIGITS`, and every other pair of state and character returns the rejection value at once. Only `DIGITS` is accepting, so a sign alone and the empty string are rejected. The invariant is that the state and the accumulator describe exactly the accepted prefix. At most 18 digits keep the accumulator inside the range of a `long`. The harness also asserts the Java behaviors that the lesson text states.

**Complexity.**
- **Time** is O(n), because each character causes one comparison chain and no character is read twice.
- **Space** is O(1), because the method keeps a state, a sign flag, an accumulator and an index.

```java run
import java.util.Random;

public final class SignedToken {
    static final int START = 0, SIGN = 1, DIGITS = 2;

    /**
     * Parses a signed integer token or returns Long.MIN_VALUE.
     * Time: O(n), one pass. Space: O(1).
     * Invariant: state and value describe exactly the accepted prefix s[0..i-1].
     */
    static long parseToken(String s) {
        // The parser starts in START, and negative remembers a leading minus sign.
        int state = START;
        boolean negative = false;
        long value = 0;
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            boolean digit = c >= '0' && c <= '9';
            // A sign is legal only in START, and it leads to SIGN, which is not accepting.
            if (state == START && (c == '+' || c == '-')) {
                negative = c == '-';
                state = SIGN;
            // A digit is legal in every state and always leads to DIGITS.
            } else if (digit) {
                // Appending a digit multiplies by 10, which stays within a long for 18 digits.
                value = value * 10 + (c - '0');
                state = DIGITS;
            } else {
                // No transition exists for this pair, so the token is invalid.
                return Long.MIN_VALUE;
            }
        }
        // Only DIGITS is accepting; START and SIGN mean the token has no digit.
        if (state != DIGITS) return Long.MIN_VALUE;
        // The sign applies once, after all digits are read.
        return negative ? -value : value;
    }

    /** Naive identifier test from the lesson, kept to show its two wrong answers. */
    static boolean naiveIdentifier(String s) {
        if (s.isEmpty()) return false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (!(Character.isLetterOrDigit(c) || c == '_')) return false;
        }
        return true;
    }

    /** Lesson code: the identifier parser with START and BODY. */
    static boolean isIdentifier(String s) {
        final int START = 0, BODY = 1;
        int state = START;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            boolean letter = (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
            boolean digit = c >= '0' && c <= '9';
            if (state == START && letter) state = BODY;
            else if (state == BODY && (letter || digit)) state = BODY;
            else return false;
        }
        return state == BODY;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (parseToken("-408") != -408) throw new AssertionError("example 1");
        if (parseToken("+") != Long.MIN_VALUE) throw new AssertionError("example 2");
        // Boundary inputs: empty, two signs, a sign in the middle and trailing text.
        if (parseToken("") != Long.MIN_VALUE) throw new AssertionError("empty");
        if (parseToken("+-5") != Long.MIN_VALUE) throw new AssertionError("two signs");
        if (parseToken("4-2") != Long.MIN_VALUE) throw new AssertionError("inner sign");
        if (parseToken("12a") != Long.MIN_VALUE) throw new AssertionError("trailing text");
        if (parseToken("007") != 7) throw new AssertionError("leading zeros");
        // Random strings are checked against a regular-expression oracle and Long.parseLong.
        Random rnd = new Random(31);
        String pool = "+-0123x ";
        for (int t = 0; t < 600; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(8);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            long expect = s.matches("[+-]?[0-9]+") ? Long.parseLong(s) : Long.MIN_VALUE;
            if (parseToken(s) != expect) throw new AssertionError("random " + t);
        }
        // Lesson claim: the same-test loop accepts "9lives" and an accented letter, and the parser rejects both.
        if (!naiveIdentifier("9lives") || !naiveIdentifier("café")) throw new AssertionError("naive accepts");
        if (isIdentifier("9lives") || isIdentifier("café") || isIdentifier("")) throw new AssertionError("parser rejects");
        if (!isIdentifier("x_1") || isIdentifier("ab-c") || !isIdentifier("_9")) throw new AssertionError("traces");
        // Lesson claim: library calls accept more than ASCII, and parseInt accepts '+' but rejects a leading space.
        if (!Character.isLetterOrDigit('é')) throw new AssertionError("isLetterOrDigit");
        if (Integer.parseInt("+5") != 5) throw new AssertionError("parseInt plus");
        if (Integer.parseInt("٣") != 3) throw new AssertionError("parseInt non-ASCII digit");
        boolean threw = false;
        try { Integer.parseInt(" 5"); } catch (NumberFormatException e) { threw = true; }
        if (!threw) throw new AssertionError("parseInt leading space");
        // Lesson claim: int arithmetic wraps silently.
        if (Integer.MAX_VALUE + 1 != Integer.MIN_VALUE) throw new AssertionError("wraparound");
    }
}
```

#### Solution: [Vary] String To Integer (LeetCode 8)
<!-- id: st-atoi -->

**Approach.**
The method moves an index past the leading spaces, reads an optional sign, and then reads digits until the first non-digit. The accumulator has type `long` and holds the magnitude. After each digit, a check compares the magnitude with `2^31`, which is one more than the largest positive value. When the magnitude exceeds that limit, the loop stops, because the final answer is a bound whatever digits follow. The accumulator never exceeds about `2^31 * 10` before the check runs, so a `long` cannot overflow. The final step applies the sign and clamps to `Integer.MAX_VALUE` or `Integer.MIN_VALUE`. The invariant is that `mag` equals the value of the digits read so far, or exceeds `2^31` and ends the loop.

**Complexity.**
- **Time** is O(n), because each character is read at most once.
- **Space** is O(1), because the method keeps an index, a sign and one accumulator.

```java run
import java.math.BigInteger;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class Atoi {
    /**
     * Converts the leading number of s to a clamped 32-bit integer.
     * Time: O(n). Space: O(1).
     * Invariant: mag holds the value of the digits read so far, or exceeds 2^31 and ends the loop.
     */
    static int myAtoi(String s) {
        // i is the index of the next unexamined character.
        int i = 0, n = s.length();
        // Leading spaces carry no information, so the index skips them.
        while (i < n && s.charAt(i) == ' ') i++;
        // An optional sign sets the direction; the default is positive.
        boolean negative = false;
        if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) {
            negative = s.charAt(i) == '-';
            i++;
        }
        // mag holds the magnitude as a long, which cannot overflow because the loop stops past 2^31.
        long mag = 0;
        // The loop stops at the first non-digit and costs at most one step per character.
        while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
            mag = mag * 10 + (s.charAt(i) - '0');
            // Any magnitude above 2^31 clamps to a bound, so the remaining digits cannot matter.
            if (mag > (1L << 31)) break;
            i++;
        }
        // The sign applies after the digits; magnitudes beyond the range clamp to the nearest bound.
        long signed = negative ? -mag : mag;
        if (signed > Integer.MAX_VALUE) return Integer.MAX_VALUE;
        if (signed < Integer.MIN_VALUE) return Integer.MIN_VALUE;
        return (int) signed;
    }

    /** Oracle: a regular expression for the prefix and BigInteger for the exact value. */
    static int oracle(String s) {
        Matcher m = Pattern.compile("^ *([+-]?[0-9]+)").matcher(s);
        if (!m.find()) return 0;
        BigInteger v = new BigInteger(m.group(1).replace("+", ""));
        if (v.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) return Integer.MAX_VALUE;
        if (v.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) return Integer.MIN_VALUE;
        return v.intValue();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (myAtoi("   +17 apples") != 17) throw new AssertionError("example 1");
        if (myAtoi("-2147483649x") != Integer.MIN_VALUE) throw new AssertionError("example 2");
        // Boundary values around both bounds, no digit, and a sign followed by a space.
        if (myAtoi("2147483647") != Integer.MAX_VALUE) throw new AssertionError("max");
        if (myAtoi("2147483648") != Integer.MAX_VALUE) throw new AssertionError("max plus one");
        if (myAtoi("-2147483648") != Integer.MIN_VALUE) throw new AssertionError("min");
        if (myAtoi("x5") != 0 || myAtoi("") != 0 || myAtoi("- 3") != 0) throw new AssertionError("no digits");
        if (myAtoi("00000000000000000000000012") != 12) throw new AssertionError("long zero prefix");
        // Random strings are checked against the oracle.
        Random rnd = new Random(32);
        String pool = "  +-0123456789ab.";
        for (int t = 0; t < 1500; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(16);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            if (myAtoi(s) != oracle(s)) throw new AssertionError("random " + t + " [" + s + "]");
        }
    }
}
```

#### Solution: [Boundary] Valid Number (LeetCode 65)
<!-- id: st-valid-number -->

**Approach.**
The parser keeps three flags, `seenDigit`, `seenDot` and `seenExp`, plus `expDigit`, which records a digit after the exponent mark. A digit sets `seenDigit`, and it sets `expDigit` when the exponent has begun. A sign is legal only at index 0 or right after `'e'` or `'E'`. A dot is legal when no earlier dot and no exponent exist. An exponent mark is legal when a digit came before it and no exponent exists, and it clears `expDigit`. Any other character rejects the input. At the end the number is valid when a digit exists and, if an exponent exists, a digit followed it. The invariant is that the flags describe the accepted prefix, and no flag ever turns off except `expDigit` at a new exponent mark.

**Complexity.**
- **Time** is O(n), because the loop reads each character once with constant work.
- **Space** is O(1), because the method keeps four booleans and one index.

```java run
import java.util.Random;

public final class ValidNumber {
    /**
     * Decides whether s is a valid decimal number with an optional exponent.
     * Time: O(n). Space: O(1).
     * Invariant: the flags describe the accepted prefix s[0..i-1].
     */
    static boolean isNumber(String s) {
        // The flags record what the parser has already consumed.
        boolean seenDigit = false, seenDot = false, seenExp = false, expDigit = false;
        // The loop runs once per character, which costs n iterations.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                // A digit counts for the mantissa and, after the mark, for the exponent.
                seenDigit = true;
                if (seenExp) expDigit = true;
            } else if (c == '+' || c == '-') {
                // A sign is legal at the start or right after the exponent mark.
                if (i != 0 && s.charAt(i - 1) != 'e' && s.charAt(i - 1) != 'E') return false;
            } else if (c == '.') {
                // One dot is legal, and only before any exponent mark.
                if (seenDot || seenExp) return false;
                seenDot = true;
            } else if (c == 'e' || c == 'E') {
                // An exponent mark needs a mantissa digit before it and appears only once.
                if (!seenDigit || seenExp) return false;
                seenExp = true;
                expDigit = false;
            } else {
                // Letters other than the exponent mark have no transition.
                return false;
            }
        }
        // The text needs a mantissa digit, and an exponent mark needs its own digit.
        return seenDigit && (!seenExp || expDigit);
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!isNumber("-.5e+3")) throw new AssertionError("example 1");
        if (isNumber(".")) throw new AssertionError("example 2");
        // The hostile cases named in the lesson plan and a few more.
        if (!isNumber("2e10") || !isNumber("3.") || !isNumber("3.e-2") || !isNumber("+.8")) throw new AssertionError("valid forms");
        if (isNumber("e9") || isNumber("1e") || isNumber("1e5.5") || isNumber("--1") || isNumber("1-") || isNumber("+.") || isNumber(".e1")) throw new AssertionError("invalid forms");
        // Random strings are checked against a regular-expression oracle.
        Random rnd = new Random(33);
        String pool = "019+-.eEa";
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = 1 + rnd.nextInt(8);
            for (int k = 0; k < len; k++) sb.append(pool.charAt(rnd.nextInt(pool.length())));
            String s = sb.toString();
            boolean expect = s.matches("[+-]?([0-9]+\\.?[0-9]*|\\.[0-9]+)([eE][+-]?[0-9]+)?");
            if (isNumber(s) != expect) throw new AssertionError("random " + t + " [" + s + "]");
        }
    }
}
```

#### Solution: [Recognize] Compare Version Numbers (LeetCode 165)
<!-- id: st-compare-versions -->

**Approach.**
Each version string has its own index. A helper-free loop reads one component from each string per round. Reading a component means accumulating digits into an `int` until the next dot or the end of that string. A string that already ended contributes the component 0. The loop returns at the first round where the two components differ, and it returns 0 when both strings end with every round equal. The invariant is that before each round, all earlier components are equal. The constraint keeps every component inside an `int`, so the accumulator cannot overflow, and no whole version becomes one number.

**Complexity.**
- **Time** is O(a + b), where a and b are the lengths of the two strings, because each character is read once.
- **Space** is O(1), because the method keeps two indexes and two accumulators.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class CompareVersions {
    /**
     * Compares two dot-separated versions component by component.
     * Time: O(a + b). Space: O(1).
     * Invariant: before each round, all earlier components of both versions are equal.
     */
    static int compare(String v1, String v2) {
        // Each string keeps its own index of the next unexamined character.
        int i = 0, j = 0;
        // The loop runs while either string still has characters, so a missing component counts as 0.
        while (i < v1.length() || j < v2.length()) {
            int a = 0, b = 0;
            // The component of v1 is the digits up to the next dot; leading zeros add nothing.
            while (i < v1.length() && v1.charAt(i) != '.') a = a * 10 + (v1.charAt(i++) - '0');
            // The component of v2 follows the same rule on its own index.
            while (j < v2.length() && v2.charAt(j) != '.') b = b * 10 + (v2.charAt(j++) - '0');
            // The first component that differs decides the answer.
            if (a != b) return a < b ? -1 : 1;
            // Both indexes step over their dot, or past the end, before the next round.
            i++;
            j++;
        }
        // Every round matched, so the versions are equal.
        return 0;
    }

    /** Oracle: split on dots and compare with BigInteger, padding the shorter list with zeros. */
    static int oracle(String v1, String v2) {
        String[] x = v1.split("\\."), y = v2.split("\\.");
        for (int k = 0; k < Math.max(x.length, y.length); k++) {
            BigInteger a = k < x.length ? new BigInteger(x[k]) : BigInteger.ZERO;
            BigInteger b = k < y.length ? new BigInteger(y[k]) : BigInteger.ZERO;
            int c = a.compareTo(b);
            if (c != 0) return c;
        }
        return 0;
    }

    static String random(Random rnd) {
        StringBuilder sb = new StringBuilder();
        int parts = 1 + rnd.nextInt(4);
        for (int p = 0; p < parts; p++) {
            if (p > 0) sb.append('.');
            int digits = 1 + rnd.nextInt(3);
            for (int d = 0; d < digits; d++) sb.append((char) ('0' + (rnd.nextInt(3) == 0 ? rnd.nextInt(10) : 0 + rnd.nextInt(2))));
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // The statement examples.
        if (compare("2.04.0", "2.4") != 0) throw new AssertionError("example 1");
        if (compare("1.9", "1.10") != -1) throw new AssertionError("example 2");
        // Missing components count as zero, and a nonzero tail decides.
        if (compare("1", "1.0.0") != 0) throw new AssertionError("trailing zeros");
        if (compare("1.0.1", "1") != 1) throw new AssertionError("nonzero tail");
        // A component at the top of the int range is read without overflow.
        if (compare("2147483647", "2147483646") != 1) throw new AssertionError("int range");
        // Random versions are checked against the oracle.
        Random rnd = new Random(34);
        for (int t = 0; t < 2000; t++) {
            String a = random(rnd), b = random(rnd);
            if (compare(a, b) != oracle(a, b)) throw new AssertionError("random " + t + " " + a + " " + b);
        }
    }
}
```
