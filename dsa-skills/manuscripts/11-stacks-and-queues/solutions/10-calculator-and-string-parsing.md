<!-- solutions-for: 10-calculator-and-string-parsing -->
### Calculator And String Parsing

#### Solution: [Build] Signed Sum (Author exercise)
<!-- id: sq-signed-sum -->

**Approach.** Read the characters in order and build each number with `num = num * 10 + digit`. A number is committed when the next operator or the end of the text arrives, using the sign that preceded it. The final number is committed after the loop, which is the step most often forgotten. With only plus and minus there are no terms to revise, so a running total and a sign are the whole state. The assertions compare with a method that splits the text before each sign using a look-ahead pattern and sums the pieces, on random expressions with multi-digit numbers.

**Complexity.** O(n) time and O(1) space.

```java run
import java.util.Random;

public final class SignedSum {
    static long evaluate(String s) {
        long total = 0, num = 0;
        int sign = 1;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') num = num * 10 + (c - '0');
            else { total += sign * num; num = 0; sign = c == '+' ? 1 : -1; }
        }
        return total + sign * num;
    }
    static long viaSplit(String s) {
        long total = 0;
        for (String piece : s.split("(?=[+-])")) total += Long.parseLong(piece.startsWith("+") ? piece.substring(1) : piece);
        return total;
    }

    public static void main(String[] args) {
        if (evaluate("12+30-5") != 37) throw new AssertionError("example 1");
        if (evaluate("100") != 100) throw new AssertionError("example 2");
        if (evaluate("5-10") != -5) throw new AssertionError("a negative total");
        if (evaluate("2000000000+2000000000") != 4000000000L) throw new AssertionError("the total needs a long");
        Random rnd = new Random(12001);
        for (int t = 0; t < 5000; t++) {
            StringBuilder sb = new StringBuilder();
            sb.append(rnd.nextInt(1000));
            for (int k = rnd.nextInt(8); k > 0; k--) sb.append(rnd.nextBoolean() ? '+' : '-').append(rnd.nextInt(100000));
            String s = sb.toString();
            if (evaluate(s) != viaSplit(s)) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Vary] Basic Calculator II (LeetCode 227)
<!-- id: sq-basic-calculator-two -->

**Approach.** Keep a stack of terms and a pending operator that starts as plus. When an operator or the end of the text arrives, commit the number just read: a pending plus pushes it, a pending minus pushes its negation, and a pending times or divide replaces the top term by the product or quotient. The answer is the sum of the stack. Java integer division truncates toward zero, and the assertions state it with `-7 / 2`. The oracle is a separate recursive-descent parser with one function for sums and one for products, run on random expressions with and without spaces.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class BasicCalculatorTwo {
    static long calculate(String s) {
        ArrayDeque<Long> terms = new ArrayDeque<>();
        long num = 0;
        char op = '+';
        for (int i = 0; i <= s.length(); i++) {
            char c = i < s.length() ? s.charAt(i) : '+';
            if (c >= '0' && c <= '9') { num = num * 10 + (c - '0'); continue; }
            if (c == ' ') continue;
            if (op == '+') terms.addLast(num);
            else if (op == '-') terms.addLast(-num);
            else if (op == '*') terms.addLast(terms.removeLast() * num);
            else terms.addLast(terms.removeLast() / num);
            op = c;
            num = 0;
        }
        long total = 0;
        for (long t : terms) total += t;
        return total;
    }
    static int pos;
    static String text;
    static long oracle(String s) {
        text = s.replace(" ", "");
        pos = 0;
        return sum();
    }
    static long sum() {
        long v = product();
        while (pos < text.length() && (text.charAt(pos) == '+' || text.charAt(pos) == '-')) {
            char op = text.charAt(pos++);
            long r = product();
            v = op == '+' ? v + r : v - r;
        }
        return v;
    }
    static long product() {
        long v = number();
        while (pos < text.length() && (text.charAt(pos) == '*' || text.charAt(pos) == '/')) {
            char op = text.charAt(pos++);
            long r = number();
            v = op == '*' ? v * r : v / r;
        }
        return v;
    }
    static long number() {
        long v = 0;
        while (pos < text.length() && Character.isDigit(text.charAt(pos))) v = v * 10 + (text.charAt(pos++) - '0');
        return v;
    }

    public static void main(String[] args) {
        if (calculate("10-8/3*2") != 6) throw new AssertionError("example 1");
        if (calculate(" 7*3/4+1") != 6) throw new AssertionError("example 2");
        if (calculate("3+2*4") != 11) throw new AssertionError("precedence: applying operators as read would give 20");
        if (-7 / 2 != -3) throw new AssertionError("integer division truncates toward zero");
        if (Math.floorDiv(-7, 2) != -4) throw new AssertionError("floorDiv rounds down, which is a different rule");
        if (calculate("0-7/2") != -3) throw new AssertionError("the quotient is taken before the subtraction");
        Random rnd = new Random(12002);
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder();
            sb.append(rnd.nextInt(30));
            for (int k = rnd.nextInt(8); k > 0; k--) {
                char op = "+-*/".charAt(rnd.nextInt(4));
                if (rnd.nextInt(3) == 0) sb.append(' ');
                sb.append(op);
                if (rnd.nextInt(3) == 0) sb.append(' ');
                sb.append(op == '/' ? 1 + rnd.nextInt(9) : rnd.nextInt(30));
            }
            String s = sb.toString();
            if (calculate(s) != oracle(s)) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Boundary] Spaces And Unary Sign (Author exercise)
<!-- id: sq-spaces-unary-sign -->

**Approach.** Walk the characters and remember the last non-space character that is not a digit, or that no operand has been read yet. A sign is unary when it is the first significant character or when the previous significant character is another operator. A unary sign multiplies the sign of the next number, and a binary sign commits the previous number first. Spaces are skipped everywhere. The assertions compare with a rewriting oracle that removes the spaces and repeatedly collapses `--`, `+-`, `-+` and `++` into one sign before evaluating a signed sum.

**Complexity.** O(n) time and O(1) space.

```java run
import java.util.Random;

public final class SpacesAndUnarySign {
    static long evaluate(String s) {
        long total = 0, num = 0;
        int sign = 1;
        boolean expectOperand = true;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == ' ') continue;
            if (c >= '0' && c <= '9') { num = num * 10 + (c - '0'); expectOperand = false; }
            else if (expectOperand) { if (c == '-') sign = -sign; }
            else { total += sign * num; num = 0; sign = c == '+' ? 1 : -1; expectOperand = true; }
        }
        return total + sign * num;
    }
    static long oracle(String s) {
        String t = s.replace(" ", "");
        String prev;
        do {
            prev = t;
            t = t.replace("--", "+").replace("+-", "-").replace("-+", "-").replace("++", "+");
        } while (!t.equals(prev));
        long total = 0;
        for (String piece : t.split("(?=[+-])")) {
            if (piece.isEmpty()) continue;
            total += Long.parseLong(piece.startsWith("+") ? piece.substring(1) : piece);
        }
        return total;
    }

    public static void main(String[] args) {
        if (evaluate(" -12 + 5 - -3 ") != -4) throw new AssertionError("example 1");
        if (evaluate("7- +2") != 5) throw new AssertionError("example 2");
        if (evaluate("-5") != -5) throw new AssertionError("a leading minus");
        if (evaluate("1 - - - 1") != 0) throw new AssertionError("several unary signs after a binary one");
        Random rnd = new Random(12003);
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder();
            if (rnd.nextInt(3) == 0) sb.append(rnd.nextBoolean() ? '+' : '-');
            sb.append(rnd.nextInt(500));
            for (int k = rnd.nextInt(6); k > 0; k--) {
                if (rnd.nextInt(2) == 0) sb.append(' ');
                sb.append(rnd.nextBoolean() ? '+' : '-');
                for (int u = rnd.nextInt(3) == 0 ? 1 : 0; u > 0; u--) { if (rnd.nextInt(2) == 0) sb.append(' '); sb.append(rnd.nextBoolean() ? '+' : '-'); }
                if (rnd.nextInt(2) == 0) sb.append(' ');
                sb.append(rnd.nextInt(500));
            }
            String s = sb.toString();
            if (evaluate(s) != oracle(s)) throw new AssertionError("differs on [" + s + "]: " + evaluate(s) + " vs " + oracle(s));
        }
    }
}
```

#### Solution: [Recognize] Basic Calculator (LeetCode 224)
<!-- id: sq-basic-calculator -->

**Approach.** Keep the total of the current level, the sign for the next number, and a stack that holds the saved total and the saved sign for every open bracket. A digit extends the number, a plus or minus commits the number with its sign and sets the next sign, an opening bracket saves the total and the sign in front of it and restarts the inside at zero, and a closing bracket commits the number and folds the inside into the saved total using the saved sign. A minus at the start of a bracket commits a zero first, which is why a leading unary sign needs no special case. The assertions compare with a recursive-descent parser that reads a signed term, which is a number or a bracketed expression, on random nested expressions with spaces.

**Complexity.** O(n) time and O(depth) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class BasicCalculatorBrackets {
    static long calculate(String s) {
        ArrayDeque<long[]> saved = new ArrayDeque<>();
        long result = 0, num = 0;
        int sign = 1;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') num = num * 10 + (c - '0');
            else if (c == '+' || c == '-') { result += sign * num; num = 0; sign = c == '+' ? 1 : -1; }
            else if (c == '(') { saved.addLast(new long[] {result, sign}); result = 0; sign = 1; }
            else if (c == ')') {
                result += sign * num; num = 0;
                long[] outer = saved.removeLast();
                result = outer[0] + outer[1] * result;
            }
        }
        return result + sign * num;
    }
    static String text;
    static int pos;
    static long oracle(String s) {
        text = s.replace(" ", "");
        pos = 0;
        return expression();
    }
    static long expression() {
        long v = signedTerm();
        while (pos < text.length() && (text.charAt(pos) == '+' || text.charAt(pos) == '-')) {
            char op = text.charAt(pos++);
            long r = signedTerm();
            v = op == '+' ? v + r : v - r;
        }
        return v;
    }
    static long signedTerm() {
        int sign = 1;
        if (pos < text.length() && (text.charAt(pos) == '-' || text.charAt(pos) == '+')) sign = text.charAt(pos++) == '-' ? -1 : 1;
        if (text.charAt(pos) == '(') {
            pos++;
            long v = expression();
            pos++;
            return sign * v;
        }
        long v = 0;
        while (pos < text.length() && Character.isDigit(text.charAt(pos))) v = v * 10 + (text.charAt(pos++) - '0');
        return sign * v;
    }
    static void build(Random rnd, StringBuilder sb, int depth, boolean allowLeadingSign) {
        if (allowLeadingSign && rnd.nextInt(4) == 0) sb.append('-');
        term(rnd, sb, depth);
        for (int k = rnd.nextInt(3); k > 0; k--) {
            if (rnd.nextInt(2) == 0) sb.append(' ');
            sb.append(rnd.nextBoolean() ? '+' : '-');
            if (rnd.nextInt(2) == 0) sb.append(' ');
            term(rnd, sb, depth);
        }
    }
    static void term(Random rnd, StringBuilder sb, int depth) {
        if (depth > 0 && rnd.nextInt(3) == 0) {
            sb.append('(');
            build(rnd, sb, depth - 1, true);
            sb.append(')');
        } else sb.append(rnd.nextInt(100));
    }

    public static void main(String[] args) {
        if (calculate("1 - (4 + (2 - 3))") != -2) throw new AssertionError("example 1");
        if (calculate("-(2 + 3) + 10") != 5) throw new AssertionError("example 2");
        if (calculate("(-3+1)") != -2) throw new AssertionError("a unary minus at the start of a bracket");
        if (calculate("10-(2+3)-(1-(4-9))") != -1) throw new AssertionError("two brackets and a nested one");
        Random rnd = new Random(12004);
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 3, true);
            String s = sb.toString();
            if (calculate(s) != oracle(s)) throw new AssertionError("differs on [" + s + "]");
        }
    }
}
```
