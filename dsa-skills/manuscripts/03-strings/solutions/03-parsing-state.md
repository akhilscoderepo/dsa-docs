<!-- solutions-for: 03-parsing-state -->
### Parsing State

#### Solution: [Build] Parse a Signed Integer Token (Author exercise)
<!-- id: st-parse-signed-integer -->

**Approach.** Read an optional sign at index 0, then require at least one digit and nothing but digits until the end. The value accumulates as `value * 10 + digit` in a `long`, which cannot overflow for at most 18 digits. Any other character, or no digit at all, makes the token invalid, and the method returns an empty result. The assertions compare with a regular-expression check and with `Long.parseLong` on every valid token that random generation produces.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.OptionalLong;
import java.util.Random;

public final class ParseSignedInteger {
    static OptionalLong parse(String token) {
        int i = 0, n = token.length();
        boolean negative = false;
        if (i < n && (token.charAt(i) == '+' || token.charAt(i) == '-')) { negative = token.charAt(i) == '-'; i++; }
        if (i == n) return OptionalLong.empty();
        long value = 0;
        for (; i < n; i++) {
            char c = token.charAt(i);
            if (c < '0' || c > '9') return OptionalLong.empty();
            value = value * 10 + (c - '0');
        }
        return OptionalLong.of(negative ? -value : value);
    }

    public static void main(String[] args) {
        if (parse("-205").getAsLong() != -205) throw new AssertionError("example 1");
        if (parse("12a").isPresent()) throw new AssertionError("example 2");
        if (parse("").isPresent() || parse("+").isPresent() || parse("-").isPresent()) throw new AssertionError("no digits");
        if (parse("+7").getAsLong() != 7) throw new AssertionError("plus sign");
        Random rnd = new Random(221);
        String alphabet = "0123456789+-a ";
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(8);
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            boolean valid = s.matches("[+-]?[0-9]+");
            OptionalLong got = parse(s);
            if (got.isPresent() != valid) throw new AssertionError("validity differs on: [" + s + "]");
            if (valid && got.getAsLong() != Long.parseLong(s.startsWith("+") ? s.substring(1) : s)) throw new AssertionError("value differs on: [" + s + "]");
        }
    }
}
```

#### Solution: [Vary] String to Integer (atoi) (LeetCode 8)
<!-- id: st-atoi -->

**Approach.** Skip spaces, read an optional sign, then read digits and stop at the first non-digit. Before each multiplication, test whether `value` already exceeds `(Integer.MAX_VALUE - digit) / 10`. If it does, the next step would overflow, so return the clamp for the sign. At the limit the negative clamp equals the exact value, since -2147483648 is the minimum. If no digit is read, the value stays 0. The oracle extracts the prefix with a regular expression, converts it with `BigInteger` and clamps.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.math.BigInteger;
import java.util.Random;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class Atoi {
    static int atoi(String s) {
        int i = 0, n = s.length(), sign = 1, value = 0;
        while (i < n && s.charAt(i) == ' ') i++;
        if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) { if (s.charAt(i) == '-') sign = -1; i++; }
        while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
            int d = s.charAt(i) - '0';
            if (value > (Integer.MAX_VALUE - d) / 10) return sign == 1 ? Integer.MAX_VALUE : Integer.MIN_VALUE;
            value = value * 10 + d;
            i++;
        }
        return sign * value;
    }
    static final Pattern PREFIX = Pattern.compile("^ *([+-]?[0-9]+)");
    static int oracle(String s) {
        Matcher m = PREFIX.matcher(s);
        if (!m.find()) return 0;
        String t = m.group(1);
        BigInteger v = new BigInteger(t.startsWith("+") ? t.substring(1) : t);
        if (v.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0) return Integer.MAX_VALUE;
        if (v.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) return Integer.MIN_VALUE;
        return v.intValue();
    }

    public static void main(String[] args) {
        if (atoi("   -42abc") != -42) throw new AssertionError("example 1");
        if (atoi("99999999999") != 2147483647) throw new AssertionError("example 2");
        if (atoi("words 5") != 0) throw new AssertionError("no digits");
        if (atoi("+-3") != 0) throw new AssertionError("two signs");
        if (atoi("2147483647") != Integer.MAX_VALUE) throw new AssertionError("exact maximum");
        if (atoi("-2147483648") != Integer.MIN_VALUE) throw new AssertionError("exact minimum");
        if (atoi("-2147483649") != Integer.MIN_VALUE) throw new AssertionError("below the minimum clamps");
        Random rnd = new Random(222);
        String alphabet = "0123456789 +-a";
        for (int t = 0; t < 8000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = rnd.nextInt(14);
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            if (atoi(s) != oracle(s)) throw new AssertionError("disagrees with the BigInteger oracle on: [" + s + "]");
        }
    }
}
```

#### Solution: [Boundary] Valid Number (LeetCode 65)
<!-- id: st-valid-number -->

**Approach.** Keep four flags: a digit has been seen, a dot has been seen, an exponent mark has been seen, and a digit has followed the exponent mark. A sign is legal only at index 0 or directly after an exponent mark. A dot is illegal after another dot or after an exponent. An exponent mark needs a digit before it and may appear once. At the end, the string is valid only when a digit was seen and the exponent, if any, received a digit. The lone dot fails because no digit was seen, and `2e10` passes. The assertions also show that `Double.parseDouble` accepts `NaN`, `Infinity`, `1d` and padded text that the contract rejects, and compare the flags with a regular expression on random strings.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class ValidNumber {
    static boolean isNumber(String s) {
        boolean seenDigit = false, seenDot = false, seenExp = false, digitAfterExp = true;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') { seenDigit = true; digitAfterExp = true; }
            else if (c == '+' || c == '-') { if (i != 0 && s.charAt(i - 1) != 'e' && s.charAt(i - 1) != 'E') return false; }
            else if (c == '.') { if (seenDot || seenExp) return false; seenDot = true; }
            else if (c == 'e' || c == 'E') { if (seenExp || !seenDigit) return false; seenExp = true; digitAfterExp = false; }
            else return false;
        }
        return seenDigit && digitAfterExp;
    }
    static boolean libraryAccepts(String s) {
        try { Double.parseDouble(s); return true; } catch (NumberFormatException e) { return false; }
    }

    public static void main(String[] args) {
        if (isNumber(".")) throw new AssertionError("example 1");
        if (!isNumber("2e10")) throw new AssertionError("example 2");
        String[] yes = {"0", "+5", "-.5", "5.", "1e+5", "3.14E-2", "+.8"};
        String[] no = {"", "e3", "6e", "--1", "+", "1e5.2", "1.2.3", "0e", "1 ", "abc", "1+2"};
        for (String s : yes) if (!isNumber(s)) throw new AssertionError("should be valid: " + s);
        for (String s : no) if (isNumber(s)) throw new AssertionError("should be invalid: " + s);
        for (String s : new String[] {"NaN", "Infinity", "1d", " 5 "}) {
            if (!libraryAccepts(s)) throw new AssertionError("the library should accept " + s);
            if (isNumber(s)) throw new AssertionError("the contract rejects " + s);
        }
        Random rnd = new Random(223);
        String alphabet = "012.eE+-x";
        for (int t = 0; t < 20000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(7);
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String s = sb.toString();
            boolean expected = s.matches("[+-]?([0-9]+\\.?[0-9]*|\\.[0-9]+)([eE][+-]?[0-9]+)?");
            if (isNumber(s) != expected) throw new AssertionError("disagrees with the grammar on: [" + s + "]");
        }
    }
}
```

#### Solution: [Recognize] Compare Version Numbers (LeetCode 165)
<!-- id: st-compare-versions -->

**Approach.** Walk both strings with their own cursors. At each step, find the end of the next component in each, treating a finished string as an empty component. Drop leading zeros in each digit run, then compare the run lengths, since a longer run without leading zeros is the larger number, and then compare digit by digit. If the components are equal, step past the dots and continue. An empty run compares as zero, so `1.0` equals `1.0.0`. No component is converted to an integer, so a component of hundreds of digits is handled. The oracle splits on dots and compares components with `BigInteger`.

**Complexity.** O(n + m) time and O(1) extra space.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class CompareVersions {
    static int compareVersions(String a, String b) {
        int i = 0, j = 0;
        while (i < a.length() || j < b.length()) {
            int si = i, sj = j;
            while (i < a.length() && a.charAt(i) != '.') i++;
            while (j < b.length() && b.charAt(j) != '.') j++;
            while (si < i && a.charAt(si) == '0') si++;
            while (sj < j && b.charAt(sj) == '0') sj++;
            if (i - si != j - sj) return i - si < j - sj ? -1 : 1;
            for (; si < i; si++, sj++) if (a.charAt(si) != b.charAt(sj)) return a.charAt(si) < b.charAt(sj) ? -1 : 1;
            i++; j++;
        }
        return 0;
    }
    static int oracle(String a, String b) {
        String[] x = a.split("\\.", -1), y = b.split("\\.", -1);
        for (int k = 0; k < Math.max(x.length, y.length); k++) {
            BigInteger p = k < x.length ? new BigInteger(x[k]) : BigInteger.ZERO;
            BigInteger q = k < y.length ? new BigInteger(y[k]) : BigInteger.ZERO;
            int c = p.compareTo(q);
            if (c != 0) return c;
        }
        return 0;
    }

    public static void main(String[] args) {
        if (compareVersions("3.07.1", "3.7") != 1) throw new AssertionError("example 1");
        if (compareVersions("0.9.9", "0.10") != -1) throw new AssertionError("example 2");
        if (compareVersions("1.0", "1.0.0.0") != 0) throw new AssertionError("missing components are zero");
        String huge = "9".repeat(60);
        if (compareVersions("1." + huge, "1." + huge + "0") != -1) throw new AssertionError("components longer than any integer type");
        Random rnd = new Random(224);
        for (int t = 0; t < 8000; t++) {
            String a = randomVersion(rnd), b = randomVersion(rnd);
            if (compareVersions(a, b) != oracle(a, b)) throw new AssertionError("disagrees on " + a + " vs " + b);
            if (compareVersions(a, b) != -compareVersions(b, a)) throw new AssertionError("antisymmetry on " + a + " vs " + b);
        }
    }
    static String randomVersion(Random rnd) {
        int parts = 1 + rnd.nextInt(4);
        StringBuilder sb = new StringBuilder();
        for (int p = 0; p < parts; p++) {
            if (p > 0) sb.append('.');
            int digits = 1 + rnd.nextInt(3);
            for (int d = 0; d < digits; d++) sb.append((char) ('0' + (rnd.nextInt(3) == 0 ? 0 : rnd.nextInt(10))));
        }
        return sb.toString();
    }
}
```
