<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Expression Parsing

#### Solution: [Build] Signed Sum (Author exercise)
<!-- id: sq-signed-sum -->

**Approach.**
The method reads the characters once and keeps `num` for the digits of the current number and `sign` for the operator that stands before it. Each digit changes `num` to `num * 10 + digit`. At a `+` or `-`, and once more at the end of the text, the number is complete, so the method adds `sign * num` to the total and stores the sign of the new operator. The first number gets the sign 1, because no operator stands before it. The invariant is that the total holds the value of every number that is complete, and `num` holds the digits of the one that is not.

**Complexity.**
- **Time** is O(n), because each character causes one digit update or one addition.
- **Space** is O(1), because the method stores three scalars.

```java run
import java.util.Random;

public final class SignedSum {
    /**
     * Evaluates digits joined by + and -.
     * Time: O(n), one step per character.
     * Space: O(1), three scalars.
     * Invariant: total covers all complete numbers; num holds the digits of the current one.
     */
    static long signedSum(String s) {
        long total = 0;
        long num = 0;
        int sign = 1;
        // The index n acts as a final boundary, so the last number gets added too.
        for (int i = 0; i <= s.length(); i++) {
            char c = i < s.length() ? s.charAt(i) : '+';
            if (c >= '0' && c <= '9') {
                // A digit extends the number by one decimal place.
                num = num * 10 + (c - '0');
            } else {
                // An operator or the end completes the number, which takes the sign stored before it.
                total += sign * num;
                num = 0;
                // The new operator decides the sign of the next number.
                sign = c == '+' ? 1 : -1;
            }
        }
        return total;
    }

    /** Reference: cut before each sign and parse each piece with its own sign. */
    static long oracle(String s) {
        long sum = 0;
        // Each piece is a number with an optional leading sign, such as +35 or -8.
        for (String piece : s.split("(?=[+-])")) sum += Long.parseLong(piece);
        return sum;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2.
        if (signedSum("120+35-8") != 147) throw new AssertionError("example 1");
        if (signedSum("10-4-3-2") != 1) throw new AssertionError("example 2");
        // A single number has no operator and gives its own value.
        if (signedSum("7") != 7 || signedSum("0") != 0) throw new AssertionError("single");
        // Random expressions agree with the split-and-parse reference.
        Random rnd = new Random(1110);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder().append(rnd.nextInt(1000001));
            for (int k = rnd.nextInt(6); k > 0; k--) sb.append(rnd.nextBoolean() ? '+' : '-').append(rnd.nextInt(1000001));
            String in = sb.toString();
            if (signedSum(in) != oracle(in)) throw new AssertionError("random " + in);
        }
    }
}
```

#### Solution: [Vary] Basic Calculator II (LeetCode 227)
<!-- id: sq-leetcode-calculator-two -->

**Approach.**
A `+` or `-` starts a new term, and `*` or `/` changes the term that is already open. The method keeps `sum` for the finished terms and `last` for the open term, so the stack of terms shrinks to one value. At each boundary the pending operator `op` is applied to `num`. A `+` adds `last` to `sum` and opens a new term with `num`. A `-` does the same with `-num`. A `*` or `/` changes `last` in place. Division uses Java `/`, which truncates toward zero. That matches the rule even when `last` is negative, because `-7 / 2` is -3. The `Math.floorDiv` method would give -4 and is wrong here. The invariant is that `sum + last` equals the value of the text read before the current number.

**Complexity.**
- **Time** is O(n), because each character causes one digit update or one operator step.
- **Space** is O(1), because `sum`, `last` and `num` replace the stack of terms.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class CalculatorTwo {
    /**
     * Evaluates + - * / with optional spaces and truncating division.
     * Time: O(n), one step per character.
     * Space: O(1), three integers and the pending operator.
     * Invariant: sum + last is the value of everything before the current number.
     */
    static int calculate(String s) {
        int sum = 0;
        int last = 0;
        int num = 0;
        char op = '+';
        // The index n acts as a final boundary with a plus sign.
        for (int i = 0; i <= s.length(); i++) {
            char c = i < s.length() ? s.charAt(i) : '+';
            if (c >= '0' && c <= '9') {
                // A digit extends the number.
                num = num * 10 + (c - '0');
            } else if (c != ' ') {
                // The number is complete, so the pending operator applies to it.
                if (op == '+') { sum += last; last = num; }
                else if (op == '-') { sum += last; last = -num; }
                else if (op == '*') last = last * num;
                else last = last / num;
                // The new operator waits for the next number.
                op = c;
                num = 0;
            }
        }
        return sum + last;
    }

    // Recursive-descent reference over the text without spaces.
    static String src;
    static int pos;

    static int oracle(String s) {
        src = s.replace(" ", "");
        pos = 0;
        return expr();
    }

    static int expr() {
        int v = term();
        // An expression is terms joined by + and -.
        while (pos < src.length() && (src.charAt(pos) == '+' || src.charAt(pos) == '-')) {
            char o = src.charAt(pos++);
            int r = term();
            v = o == '+' ? v + r : v - r;
        }
        return v;
    }

    static int term() {
        int v = number();
        // A term is numbers joined by * and /, applied left to right.
        while (pos < src.length() && (src.charAt(pos) == '*' || src.charAt(pos) == '/')) {
            char o = src.charAt(pos++);
            int r = number();
            v = o == '*' ? v * r : v / r;
        }
        return v;
    }

    static int number() {
        int v = 0;
        while (pos < src.length() && Character.isDigit(src.charAt(pos))) v = v * 10 + (src.charAt(pos++) - '0');
        return v;
    }

    static String sp(Random rnd) {
        // Zero to two spaces between tokens.
        return " ".repeat(rnd.nextInt(3));
    }

    public static void main(String[] args) {
        // Example 1: a negative term is divided by the Java operator without flooring.
        if (calculate("8 - 3*4 + 10/3") != -1) throw new AssertionError("example 1");
        // Example 2: equal-rank division applies left to right.
        if (calculate(" 100/7/2") != 7) throw new AssertionError("example 2");
        // Integer division truncates toward zero, and floorDiv rounds down instead.
        if (-7 / 2 != -3 || Math.floorDiv(-7, 2) != -4) throw new AssertionError("division");
        if (calculate("3 - 7/2") != 0) throw new AssertionError("negative top term");
        // ArrayList.remove shifts later elements one place left.
        List<String> list = new ArrayList<>(List.of("a", "b", "c", "d"));
        list.remove(1);
        if (!list.equals(List.of("a", "c", "d"))) throw new AssertionError("remove shifts");
        // Random expressions agree with the recursive-descent reference.
        Random rnd = new Random(1111);
        for (int t = 0; t < 5000; t++) {
            StringBuilder sb = new StringBuilder(sp(rnd)).append(rnd.nextInt(60));
            for (int k = rnd.nextInt(7); k > 0; k--) {
                char o = "+-*/".charAt(rnd.nextInt(4));
                int n = o == '/' ? 1 + rnd.nextInt(30) : rnd.nextInt(60);
                sb.append(sp(rnd)).append(o).append(sp(rnd)).append(n);
            }
            sb.append(sp(rnd));
            String in = sb.toString();
            if (calculate(in) != oracle(in)) throw new AssertionError("random " + in);
        }
    }
}
```

#### Solution: [Boundary] Spaces And Unary Sign (Author exercise)
<!-- id: sq-spaces-and-unary-sign -->

**Approach.**
The method ignores spaces and keeps a flag `seen` that records whether a digit was read since the last sign. A sign that arrives while `seen` is true is binary. The method adds `sign * num` to the total, clears the flag and stores the new sign. A sign that arrives while `seen` is false is unary. It multiplies the stored sign by 1 or -1 and adds nothing. The first character needs no special case, because the flag starts false and the stored sign starts at 1. The invariant is that the stored sign equals the product of every unary sign since the last number.

**Complexity.**
- **Time** is O(n), because each character causes one constant-time step.
- **Space** is O(1), because the method stores a few scalars.

```java run
import java.util.Random;

public final class SpacesAndUnarySign {
    /**
     * Evaluates digits, + and - with optional spaces and repeated signs.
     * Time: O(n), one step per character.
     * Space: O(1).
     * Invariant: sign is the product of the unary signs since the last number.
     */
    static long evaluate(String s) {
        long total = 0;
        long num = 0;
        int sign = 1;
        boolean seen = false;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                // A digit builds the number and records that a number is open.
                num = num * 10 + (c - '0');
                seen = true;
            } else if (c == '+' || c == '-') {
                int flip = c == '+' ? 1 : -1;
                if (seen) {
                    // A sign after a number is binary, so the number joins the total first.
                    total += sign * num;
                    num = 0;
                    seen = false;
                    sign = flip;
                } else {
                    // A sign with no number since the last sign is unary and changes the pending sign.
                    sign *= flip;
                }
            }
            // A space changes nothing.
        }
        // The text ends with a number, so it still has to join the total.
        return total + sign * num;
    }

    // Recursive-descent reference over the text without spaces.
    static String src;
    static int pos;

    static long oracle(String s) {
        src = s.replace(" ", "");
        pos = 0;
        long v = unary();
        // A binary sign joins the next unary value to the left result.
        while (pos < src.length()) {
            char o = src.charAt(pos++);
            long r = unary();
            v = o == '+' ? v + r : v - r;
        }
        return v;
    }

    static long unary() {
        // A leading sign applies to everything that the rest of this call reads.
        if (src.charAt(pos) == '+') { pos++; return unary(); }
        if (src.charAt(pos) == '-') { pos++; return -unary(); }
        long v = 0;
        while (pos < src.length() && Character.isDigit(src.charAt(pos))) v = v * 10 + (src.charAt(pos++) - '0');
        return v;
    }

    static String sp(Random rnd) {
        // Zero to two spaces between tokens.
        return " ".repeat(rnd.nextInt(3));
    }

    public static void main(String[] args) {
        // Example 1: a leading unary sign and a unary sign after a binary one.
        if (evaluate(" - 4 +10 - -3") != 9) throw new AssertionError("example 1");
        // Example 2: one binary sign followed by two unary signs.
        if (evaluate("5 - - - 2") != 3) throw new AssertionError("example 2");
        // A lone number, a signed number and a double negative.
        if (evaluate("7") != 7 || evaluate("+ 7") != 7 || evaluate("- -3") != 3) throw new AssertionError("small");
        // Random expressions with repeated signs and spaces agree with the reference.
        Random rnd = new Random(1112);
        for (int t = 0; t < 5000; t++) {
            StringBuilder sb = new StringBuilder(sp(rnd));
            for (int k = rnd.nextInt(3); k > 0; k--) sb.append(rnd.nextBoolean() ? '+' : '-').append(sp(rnd));
            sb.append(rnd.nextInt(1001)).append(sp(rnd));
            for (int m = rnd.nextInt(5); m > 0; m--) {
                sb.append(rnd.nextBoolean() ? '+' : '-').append(sp(rnd));
                for (int k = rnd.nextInt(3); k > 0; k--) sb.append(rnd.nextBoolean() ? '+' : '-').append(sp(rnd));
                sb.append(rnd.nextInt(1001)).append(sp(rnd));
            }
            String in = sb.toString();
            if (evaluate(in) != oracle(in)) throw new AssertionError("random " + in);
        }
    }
}
```

#### Solution: [Recognize] Basic Calculator (LeetCode 224)
<!-- id: sq-leetcode-basic-calculator -->

**Approach.**
The cue is a delayed meaning that parentheses can nest. The method keeps `result` for the innermost open group, `sign` for the operator before the next number and `num` for the digits being read. A `+` or `-` adds `sign * num` to `result` and stores the next sign. A `(` pushes a frame with the current `result` and `sign`, then starts the inside with result 0 and sign 1. A `)` finishes the inner number and combines the inner result with its parent as `saved.sign * inner + saved.result`. A unary minus at the start or after `(` needs no special case, because `result` is 0 there and the stored sign carries the negation. The invariant is that `result` belongs to the innermost open group and the stack has one frame for each group around it. The stack lives on the heap, so a depth of 20000 causes no stack overflow.

**Complexity.**
- **Time** is O(n), because each character causes one constant-time step.
- **Space** is O(d) frames for nesting depth `d`.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class BasicCalculator {
    /** One saved parent: its running result and the sign that stands in front of the group. */
    record Frame(int result, int sign) {}

    /**
     * Evaluates + - and parentheses with optional spaces.
     * Time: O(n), one step per character.
     * Space: O(d) frames for nesting depth d.
     * Invariant: result belongs to the innermost open group; the stack has one frame per parent.
     */
    static int calculate(String s) {
        ArrayDeque<Frame> saved = new ArrayDeque<>();
        int result = 0;
        int sign = 1;
        int num = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                // A digit extends the current number.
                num = num * 10 + (c - '0');
            } else if (c == '+' || c == '-') {
                // The number is complete, so it joins the result with the stored sign.
                result += sign * num;
                num = 0;
                sign = c == '+' ? 1 : -1;
            } else if (c == '(') {
                // Save the parent state, then start the inside from zero.
                saved.push(new Frame(result, sign));
                result = 0;
                sign = 1;
            } else if (c == ')') {
                // Finish the inner number, then fold the inner result into its parent.
                result += sign * num;
                num = 0;
                Frame f = saved.pop();
                result = f.sign() * result + f.result();
            }
            // A space changes nothing.
        }
        // The last number still has to join the result.
        return result + sign * num;
    }

    // Recursive-descent reference over the text without spaces.
    static String src;
    static int pos;

    static int oracle(String s) {
        src = s.replace(" ", "");
        pos = 0;
        return expr();
    }

    static int expr() {
        // The first primary may carry a unary minus, and later ones are joined by binary signs.
        int v = 1;
        if (pos < src.length() && src.charAt(pos) == '-') { pos++; v = -1; }
        v *= primary();
        while (pos < src.length() && (src.charAt(pos) == '+' || src.charAt(pos) == '-')) {
            char o = src.charAt(pos++);
            int r = primary();
            v = o == '+' ? v + r : v - r;
        }
        return v;
    }

    static int primary() {
        if (src.charAt(pos) == '(') {
            pos++;
            int v = expr();
            pos++;
            return v;
        }
        int v = 0;
        while (pos < src.length() && Character.isDigit(src.charAt(pos))) v = v * 10 + (src.charAt(pos++) - '0');
        return v;
    }

    static String sp(Random rnd) {
        // Zero to two spaces between tokens.
        return " ".repeat(rnd.nextInt(3));
    }

    static String gen(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        // A unary minus may open any expression.
        if (rnd.nextInt(4) == 0) sb.append('-').append(sp(rnd));
        sb.append(prim(rnd, depth));
        for (int k = rnd.nextInt(4); k > 0; k--) sb.append(rnd.nextBoolean() ? '+' : '-').append(sp(rnd)).append(prim(rnd, depth));
        return sb.toString();
    }

    static String prim(Random rnd, int depth) {
        // Either a group around a smaller expression, or a number with one to two digits.
        if (depth < 4 && rnd.nextInt(3) == 0) return "(" + sp(rnd) + gen(rnd, depth + 1) + ")" + sp(rnd);
        return rnd.nextInt(40) + sp(rnd);
    }

    public static void main(String[] args) {
        // Example 1: nested groups with a negative inner result.
        if (calculate("(1+(4-12))-(3-5)") != -5) throw new AssertionError("example 1");
        // Example 2: unary minus at the start and after an open parenthesis.
        if (calculate("-(2+3)-(-4)") != -1) throw new AssertionError("example 2");
        // Spaces and a single number.
        if (calculate(" 12 ") != 12 || calculate("( 7 )") != 7) throw new AssertionError("small");
        // A depth of 20000 uses the heap stack and gives the inner value.
        String deep = "(".repeat(20000) + "5" + ")".repeat(20000);
        if (calculate(deep) != 5) throw new AssertionError("deep");
        // Random expressions with groups, unary minus and spaces agree with the reference.
        Random rnd = new Random(1113);
        for (int t = 0; t < 5000; t++) {
            String in = sp(rnd) + gen(rnd, 0);
            if (calculate(in) != oracle(in)) throw new AssertionError("random " + in);
        }
    }
}
```
