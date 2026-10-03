<!-- solutions-for: 11-infix-and-postfix-evaluation -->
### Infix And Postfix Evaluation

#### Solution: [Build] Evaluate One Postfix Operator (Author exercise)
<!-- id: sq-one-postfix-operator -->

**Approach.** Push the two numbers, then for the operator pop the right operand first and the left operand second, and compute `left op right`. The first pop returns the number pushed last, which is why it is the right operand. The assertions state the order directly with `8 3 -`, show that a swapped order gives the wrong sign, and compare with a direct computation on random numbers and all four operators.

**Complexity.** O(1) time and O(1) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class OnePostfixOperator {
    static long run(String a, String b, String op, boolean swapped) {
        ArrayDeque<Long> values = new ArrayDeque<>();
        values.addLast(Long.parseLong(a));
        values.addLast(Long.parseLong(b));
        long first = values.removeLast();
        long second = values.removeLast();
        long left = swapped ? first : second, right = swapped ? second : first;
        switch (op) {
            case "+": return left + right;
            case "-": return left - right;
            case "*": return left * right;
            default: return left / right;
        }
    }

    public static void main(String[] args) {
        if (run("8", "3", "-", false) != 5) throw new AssertionError("example 1");
        if (run("7", "2", "/", false) != 3) throw new AssertionError("example 2");
        if (run("8", "3", "-", true) != -5) throw new AssertionError("a swapped order gives minus five");
        if (run("2", "5", "+", true) != run("2", "5", "+", false)) throw new AssertionError("plus cannot reveal a swap");
        Random rnd = new Random(12101);
        String ops = "+-*/";
        for (int t = 0; t < 5000; t++) {
            long a = rnd.nextInt(2001) - 1000, b = rnd.nextInt(2001) - 1000;
            String op = String.valueOf(ops.charAt(rnd.nextInt(4)));
            if (op.equals("/") && b == 0) continue;
            long want = op.equals("+") ? a + b : op.equals("-") ? a - b : op.equals("*") ? a * b : a / b;
            if (run(String.valueOf(a), String.valueOf(b), op, false) != want) throw new AssertionError("differs on " + a + " " + op + " " + b);
        }
    }
}
```

#### Solution: [Vary] Evaluate Reverse Polish Notation (LeetCode 150)
<!-- id: sq-evaluate-rpn -->

**Approach.** Walk the tokens once. A token that is exactly one of the four symbols is an operator and pops the right operand and then the left operand, and anything else is parsed as a number and pushed. The token `-11` has length three, so it is not mistaken for the minus key. The single value left at the end is the answer. The oracle builds a random expression tree, prints it as a postfix token array and as a value computed by recursion, and compares the stack machine with that value.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class EvaluateRpn {
    static long evaluate(String[] tokens) {
        ArrayDeque<Long> values = new ArrayDeque<>();
        for (String tok : tokens) {
            if (tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0) {
                long right = values.removeLast(), left = values.removeLast();
                switch (tok.charAt(0)) {
                    case '+': values.addLast(left + right); break;
                    case '-': values.addLast(left - right); break;
                    case '*': values.addLast(left * right); break;
                    default: values.addLast(left / right);
                }
            } else values.addLast(Long.parseLong(tok));
        }
        return values.removeLast();
    }
    static long build(Random rnd, List<String> out, int depth) {
        if (depth == 0 || rnd.nextInt(4) == 0) {
            int v = rnd.nextInt(41) - 20;
            out.add(String.valueOf(v));
            return v;
        }
        List<String> leftTokens = new ArrayList<>(), rightTokens = new ArrayList<>();
        long l = build(rnd, leftTokens, depth - 1);
        long r = build(rnd, rightTokens, depth - 1);
        char op = "+-*/".charAt(rnd.nextInt(4));
        if (op == '/' && r == 0) op = '-';
        out.addAll(leftTokens);
        out.addAll(rightTokens);
        out.add(String.valueOf(op));
        return op == '+' ? l + r : op == '-' ? l - r : op == '*' ? l * r : l / r;
    }

    public static void main(String[] args) {
        if (evaluate(new String[] {"9", "3", "/", "2", "*"}) != 6) throw new AssertionError("example 1");
        if (evaluate(new String[] {"2", "3", "4", "*", "-", "5", "+"}) != -5) throw new AssertionError("example 2");
        if (evaluate(new String[] {"-11", "2", "*"}) != -22) throw new AssertionError("a negative number is not an operator");
        if (evaluate(new String[] {"7"}) != 7) throw new AssertionError("a single number");
        Random rnd = new Random(12102);
        for (int t = 0; t < 5000; t++) {
            List<String> tokens = new ArrayList<>();
            long want = build(rnd, tokens, 4);
            if (evaluate(tokens.toArray(new String[0])) != want) throw new AssertionError("differs on " + tokens);
        }
    }
}
```

#### Solution: [Boundary] Non-Commutative Trace (Author exercise)
<!-- id: sq-non-commutative-trace -->

**Approach.** Run the stack machine as before and append the result of each operator to a list as it is pushed. Java's integer division truncates toward zero, so `-7 / 2` is `-3` and `7 / -2` is also `-3`, and the assertions state both and contrast them with `Math.floorDiv`. The operand order is exposed by the intermediate results, since a swap changes every minus and divide. The assertions compare the list with a recursive evaluation of a random expression tree that records results in post-order.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class NonCommutativeTrace {
    static long[] trace(String[] tokens) {
        ArrayDeque<Long> values = new ArrayDeque<>();
        List<Long> results = new ArrayList<>();
        for (String tok : tokens) {
            if (tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0) {
                long right = values.removeLast(), left = values.removeLast();
                long v = tok.equals("+") ? left + right : tok.equals("-") ? left - right : tok.equals("*") ? left * right : left / right;
                values.addLast(v);
                results.add(v);
            } else values.addLast(Long.parseLong(tok));
        }
        return results.stream().mapToLong(Long::longValue).toArray();
    }
    static long build(Random rnd, List<String> tokens, List<Long> results, int depth) {
        if (depth == 0 || rnd.nextInt(4) == 0) {
            int v = rnd.nextInt(41) - 20;
            tokens.add(String.valueOf(v));
            return v;
        }
        long l = build(rnd, tokens, results, depth - 1);
        long r = build(rnd, tokens, results, depth - 1);
        char op = "+-*/".charAt(rnd.nextInt(4));
        if (op == '/' && r == 0) op = '+';
        tokens.add(String.valueOf(op));
        long v = op == '+' ? l + r : op == '-' ? l - r : op == '*' ? l * r : l / r;
        results.add(v);
        return v;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(trace(new String[] {"8", "3", "-", "2", "/"}), new long[] {5, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(trace(new String[] {"-7", "2", "/", "7", "-2", "/", "-"}), new long[] {-3, -3, 0})) throw new AssertionError("example 2");
        if (-7 / 2 != -3 || 7 / -2 != -3) throw new AssertionError("integer division truncates toward zero");
        if (Math.floorDiv(-7, 2) != -4) throw new AssertionError("floorDiv rounds toward negative infinity");
        Random rnd = new Random(12103);
        for (int t = 0; t < 5000; t++) {
            List<String> tokens = new ArrayList<>();
            List<Long> results = new ArrayList<>();
            build(rnd, tokens, results, 4);
            if (results.isEmpty()) continue;
            long[] want = results.stream().mapToLong(Long::longValue).toArray();
            if (!Arrays.equals(trace(tokens.toArray(new String[0])), want)) throw new AssertionError("differs on " + tokens);
        }
    }
}
```

#### Solution: [Recognize] Convert Simple Infix To Postfix (Author exercise)
<!-- id: sq-infix-to-postfix -->

**Approach.** Read numbers whole and send them straight to the output. For an operator, first move to the output every waiting operator whose precedence is at least as high, then push the new operator. At the end, move the waiting operators to the output from the top down. Releasing on equal precedence makes operators left associative. The assertions evaluate the converted tokens with the postfix engine from the previous exercise and compare with a direct infix evaluator that uses its own precedence-climbing recursion. They also show that releasing only on strictly higher precedence gives the wrong grouping on `8-3-2`.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class InfixToPostfix {
    static int prec(char op) { return op == '*' || op == '/' ? 2 : 1; }
    static List<String> toPostfix(String expr, boolean releaseOnEqual) {
        List<String> out = new ArrayList<>();
        ArrayDeque<Character> ops = new ArrayDeque<>();
        int i = 0;
        while (i < expr.length()) {
            char c = expr.charAt(i);
            if (Character.isDigit(c)) {
                int j = i;
                while (j < expr.length() && Character.isDigit(expr.charAt(j))) j++;
                out.add(expr.substring(i, j));
                i = j;
                continue;
            }
            while (!ops.isEmpty() && (releaseOnEqual ? prec(ops.peekLast()) >= prec(c) : prec(ops.peekLast()) > prec(c))) out.add(String.valueOf(ops.removeLast()));
            ops.addLast(c);
            i++;
        }
        while (!ops.isEmpty()) out.add(String.valueOf(ops.removeLast()));
        return out;
    }
    static long evaluatePostfix(List<String> tokens) {
        ArrayDeque<Long> values = new ArrayDeque<>();
        for (String tok : tokens) {
            if (tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0) {
                long right = values.removeLast(), left = values.removeLast();
                values.addLast(tok.equals("+") ? left + right : tok.equals("-") ? left - right : tok.equals("*") ? left * right : left / right);
            } else values.addLast(Long.parseLong(tok));
        }
        return values.removeLast();
    }
    static String text;
    static int pos;
    static long climb(int minPrec) {
        long left = number();
        while (pos < text.length() && prec(text.charAt(pos)) >= minPrec) {
            char op = text.charAt(pos++);
            long right = climb(prec(op) + 1);
            left = op == '+' ? left + right : op == '-' ? left - right : op == '*' ? left * right : left / right;
        }
        return left;
    }
    static long number() {
        long v = 0;
        while (pos < text.length() && Character.isDigit(text.charAt(pos))) v = v * 10 + (text.charAt(pos++) - '0');
        return v;
    }

    public static void main(String[] args) {
        if (!toPostfix("3+2*4-6/2", true).equals(List.of("3", "2", "4", "*", "+", "6", "2", "/", "-"))) throw new AssertionError("example 1");
        if (!toPostfix("8-3-2", true).equals(List.of("8", "3", "-", "2", "-"))) throw new AssertionError("example 2");
        if (evaluatePostfix(toPostfix("8-3-2", false)) != 7) throw new AssertionError("strict release groups 8-3-2 as 8-(3-2)");
        if (!toPostfix("120+35", true).equals(List.of("120", "35", "+"))) throw new AssertionError("multi-digit numbers stay whole");
        Random rnd = new Random(12104);
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder();
            sb.append(rnd.nextInt(40));
            for (int k = rnd.nextInt(8); k > 0; k--) {
                char op = "+-*/".charAt(rnd.nextInt(4));
                sb.append(op).append(op == '/' ? 1 + rnd.nextInt(9) : rnd.nextInt(40));
            }
            String s = sb.toString();
            text = s;
            pos = 0;
            long want = climb(1);
            if (evaluatePostfix(toPostfix(s, true)) != want) throw new AssertionError("differs on " + s);
        }
    }
}
```
