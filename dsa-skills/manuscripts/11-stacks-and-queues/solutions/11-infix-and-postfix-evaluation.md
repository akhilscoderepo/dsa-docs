<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Evaluate Postfix And Convert Infix

#### Solution: [Build] Evaluate One Postfix Operator (Author exercise)
<!-- id: sq-eval-one-operator -->

**Approach.**
The method pushes `a` and `b` on an `ArrayDeque` used as a stack, so `b` is on top. The operator needs the left value first in the formula, but the stack returns the last pushed value first. The first pop therefore gives `right`, the second pop gives `left`, and the result is `left op right`. The stack keeps the operands in written order from bottom to top, and that order is the invariant. The test compares against direct arithmetic and checks that swapped order changes the answer for `-` and `/` but not for `+` and `*`.

**Complexity.**
- **Time** is O(1), because the method pushes two values and pops two values.
- **Space** is O(1), because the stack never holds more than two integers.

```java run
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Random;

public final class OnePostfixOperator {
    /**
     * Evaluates the three tokens a, b and op.
     * Time: O(1), two pushes and two pops.
     * Space: O(1), at most two stored integers.
     * Invariant: the stack holds the operands in written order, so the top is the right operand.
     */
    static int evalOne(String[] tokens) {
        // The stack is the same structure the full evaluator uses.
        Deque<Integer> stack = new ArrayDeque<>();
        // Pushing in written order puts b on top of a.
        stack.addLast(Integer.parseInt(tokens[0]));
        stack.addLast(Integer.parseInt(tokens[1]));
        // The last pushed value is the right operand.
        int right = stack.removeLast();
        // The value under it is the left operand.
        int left = stack.removeLast();
        // The switch applies the operator to left and right in that order.
        switch (tokens[2].charAt(0)) {
            case '+': return left + right;
            case '-': return left - right;
            case '*': return left * right;
            default: return left / right;
        }
    }

    public static void main(String[] args) {
        // Example 1: 8 minus 3 gives 5, and the swapped order would give -5.
        if (evalOne(new String[] {"8", "3", "-"}) != 5) throw new AssertionError("example 1");
        // Example 2: Java division truncates toward zero, so -7 / 2 is -3 and not -4.
        if (evalOne(new String[] {"-7", "2", "/"}) != -3) throw new AssertionError("example 2");
        if (Math.floorDiv(-7, 2) != -4) throw new AssertionError("floorDiv differs");
        // The reversed order of the opening formula 6 2 / gives 0, not 3.
        if (evalOne(new String[] {"6", "2", "/"}) != 3 || 2 / 6 != 0) throw new AssertionError("division order");
        // Random triples agree with direct arithmetic for every operator.
        Random rnd = new Random(11);
        String ops = "+-*/";
        for (int t = 0; t < 5000; t++) {
            int a = rnd.nextInt(2001) - 1000, b = rnd.nextInt(2001) - 1000;
            if (b == 0) b = 1;
            char op = ops.charAt(rnd.nextInt(4));
            int expected = op == '+' ? a + b : op == '-' ? a - b : op == '*' ? a * b : a / b;
            if (evalOne(new String[] {"" + a, "" + b, "" + op}) != expected) throw new AssertionError("random");
            // Swapped operands give the same result only for the commutative operators.
            if (op == '+' && b + a != expected) throw new AssertionError("commutative +");
            if (op == '*' && b * a != expected) throw new AssertionError("commutative *");
            // Subtraction changes sign when the operands swap, unless both are equal.
            if (op == '-' && a != b && b - a == expected) throw new AssertionError("order matters");
        }
    }
}
```

#### Solution: [Vary] Evaluate Reverse Polish Notation (LeetCode 150)
<!-- id: sq-leetcode-rpn -->

**Approach.**
One stack holds the finished values. A token with one character from the four operators pops the right operand, pops the left operand, applies the operator and pushes the result. Every other token is parsed as an integer and pushed. The token `-4` has two characters, so it is a number. After the last token the stack holds one value, which is the answer. The invariant is that after each token the stack holds the values of all completed subexpressions that have not yet been consumed. The test builds random expression trees, writes them in postfix order, and compares the stack result with a recursive evaluation of the tree.

**Complexity.**
- **Time** is O(n), because each token is pushed once and popped at most once.
- **Space** is O(n), because a chain of numbers before any operator fills the stack with about n/2 values.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class ReversePolish {
    /**
     * Evaluates a valid postfix token array.
     * Time: O(n), one push and at most one pop per token.
     * Space: O(n), the stack depth.
     * Invariant: the stack holds finished values in written order.
     */
    static int evalRpn(String[] tokens) {
        // The stack stores finished integers only.
        Deque<Integer> stack = new ArrayDeque<>();
        // One pass visits every token once.
        for (String tok : tokens) {
            // A single operator character means an operator; "-4" has two characters and stays a number.
            if (tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0) {
                // The first pop is the right operand because it was pushed last.
                int right = stack.removeLast();
                // The second pop is the left operand.
                int left = stack.removeLast();
                // The result replaces both operands on the stack.
                stack.addLast(apply(left, right, tok.charAt(0)));
            } else {
                // A number token pushes its value.
                stack.addLast(Integer.parseInt(tok));
            }
        }
        // A valid expression leaves exactly one value.
        return stack.removeLast();
    }

    static int apply(int l, int r, char op) {
        // Java int division truncates toward zero, as the problem requires.
        return op == '+' ? l + r : op == '-' ? l - r : op == '*' ? l * r : l / r;
    }

    /** Tree node used only by the reference. */
    static final class Node {
        char op; int val; Node l, r;
    }

    /** Builds a random tree whose division never has a zero divisor. */
    static Node build(Random rnd, int depth) {
        Node n = new Node();
        // A leaf holds a small signed value.
        if (depth == 0 || rnd.nextInt(4) == 0) { n.val = rnd.nextInt(19) - 9; return n; }
        n.op = "+-*/".charAt(rnd.nextInt(4));
        n.l = build(rnd, depth - 1);
        n.r = build(rnd, depth - 1);
        return n;
    }

    /** Recursive reference value; returns null when a division by zero occurs. */
    static Integer value(Node n) {
        if (n.op == 0) return n.val;
        Integer a = value(n.l), b = value(n.r);
        if (a == null || b == null) return null;
        if (n.op == '/' && b == 0) return null;
        return apply(a, b, n.op);
    }

    /** Writes the tree in postfix order. */
    static void emit(Node n, List<String> out) {
        if (n.op == 0) { out.add(String.valueOf(n.val)); return; }
        emit(n.l, out); emit(n.r, out); out.add(String.valueOf(n.op));
    }

    public static void main(String[] args) {
        // Example 1: 6 / -4 is -1, and -1 + 5 is 4.
        if (evalRpn("6 -4 / 5 +".split(" ")) != 4) throw new AssertionError("example 1");
        // Example 2: 3 - 4 is -1, 9 * -1 is -9, and -9 / 2 truncates to -4.
        if (evalRpn("9 3 4 - * 2 /".split(" ")) != -4) throw new AssertionError("example 2");
        // A single number is a valid expression.
        if (evalRpn(new String[] {"-17"}) != -17) throw new AssertionError("single");
        // Random trees agree with the recursive reference.
        Random rnd = new Random(150);
        int checked = 0;
        for (int t = 0; t < 4000; t++) {
            Node root = build(rnd, 1 + rnd.nextInt(5));
            Integer expected = value(root);
            if (expected == null) continue;
            List<String> toks = new ArrayList<>();
            emit(root, toks);
            if (evalRpn(toks.toArray(new String[0])) != expected) throw new AssertionError("random " + toks);
            checked++;
        }
        // Enough trees were valid to make the comparison meaningful.
        if (checked < 1000) throw new AssertionError("too few valid trees");
    }
}
```

#### Solution: [Boundary] Non-Commutative Trace (Author exercise)
<!-- id: sq-operator-results -->

**Approach.**
The method runs the same value stack as the evaluator and keeps a second list. Each time an operator computes a value, the method appends that value to the list before pushing it. The result list has one entry for each operator, in the order the operators run. The token test uses the token length, so `-7` is a number and `-` is an operator. Division uses Java `/`, which truncates toward zero. `Math.floorDiv` would round -7 / 2 down to -4 and is the false friend here. The invariant is that the list holds exactly the values pushed by operators so far. The test compares with a reference that builds a tree and records values in post-order, which is the same order as postfix evaluation.

**Complexity.**
- **Time** is O(n), because each token causes constant work.
- **Space** is O(n), because the stack and the result list together hold at most n values.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class OperatorResults {
    /**
     * Returns the value produced by each operator, in application order.
     * Time: O(n), constant work per token.
     * Space: O(n), the stack plus the result list.
     * Invariant: results holds every value an operator has pushed so far.
     */
    static int[] operatorResults(String[] tokens) {
        // The stack holds finished values, as in the evaluator.
        Deque<Integer> stack = new ArrayDeque<>();
        // The list records operator results in the order they appear.
        List<Integer> results = new ArrayList<>();
        // One pass over the tokens.
        for (String tok : tokens) {
            // The length test separates "-" from "-7".
            boolean isOp = tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0;
            if (!isOp) { stack.addLast(Integer.parseInt(tok)); continue; }
            // Right operand first, because it was pushed last.
            int right = stack.removeLast();
            int left = stack.removeLast();
            int v;
            switch (tok.charAt(0)) {
                case '+': v = left + right; break;
                case '-': v = left - right; break;
                case '*': v = left * right; break;
                // Java division truncates toward zero.
                default: v = left / right;
            }
            // The value is recorded and also returned to the stack.
            results.add(v);
            stack.addLast(v);
        }
        // Copy the list into the array the contract asks for.
        int[] out = new int[results.size()];
        for (int i = 0; i < out.length; i++) out[i] = results.get(i);
        return out;
    }

    /** Reference node for a random expression tree. */
    static final class Node { char op; int val; Node l, r; }

    static Node build(Random rnd, int depth) {
        Node n = new Node();
        if (depth == 0 || rnd.nextInt(3) == 0) { n.val = rnd.nextInt(21) - 10; return n; }
        n.op = "+-*/".charAt(rnd.nextInt(4));
        n.l = build(rnd, depth - 1); n.r = build(rnd, depth - 1);
        return n;
    }

    /** Post-order walk: evaluates a node and records operator values; returns null on division by zero. */
    static Integer walk(Node n, List<String> toks, List<Integer> rec) {
        if (n.op == 0) { toks.add(String.valueOf(n.val)); return n.val; }
        Integer a = walk(n.l, toks, rec), b = walk(n.r, toks, rec);
        toks.add(String.valueOf(n.op));
        if (a == null || b == null || (n.op == '/' && b == 0)) return null;
        int v = n.op == '+' ? a + b : n.op == '-' ? a - b : n.op == '*' ? a * b : a / b;
        rec.add(v);
        return v;
    }

    public static void main(String[] args) {
        // Example 1: one subtraction gives [5], and a swapped pop would give -5.
        if (!Arrays.equals(operatorResults("8 3 -".split(" ")), new int[] {5})) throw new AssertionError("example 1");
        // Example 2: -7 / 2 truncates to -3, then -3 * -3 is 9.
        if (!Arrays.equals(operatorResults("-7 2 / -3 *".split(" ")), new int[] {-3, 9})) throw new AssertionError("example 2");
        // The false friend rounds toward negative infinity and gives a different value.
        if (Math.floorDiv(-7, 2) == -7 / 2) throw new AssertionError("floorDiv claim");
        // A lone number applies no operator, so the result is empty.
        if (operatorResults(new String[] {"-5"}).length != 0) throw new AssertionError("empty");
        // Random trees agree with the post-order reference.
        Random rnd = new Random(1103);
        int checked = 0;
        for (int t = 0; t < 4000; t++) {
            Node root = build(rnd, 1 + rnd.nextInt(5));
            List<String> toks = new ArrayList<>();
            List<Integer> rec = new ArrayList<>();
            if (walk(root, toks, rec) == null) continue;
            int[] got = operatorResults(toks.toArray(new String[0]));
            if (got.length != rec.size()) throw new AssertionError("length " + toks);
            for (int i = 0; i < got.length; i++) if (got[i] != rec.get(i)) throw new AssertionError("value " + toks);
            checked++;
        }
        // The comparison covered many valid expressions.
        if (checked < 1000) throw new AssertionError("too few valid trees");
    }
}
```

#### Solution: [Recognize] Convert Simple Infix To Postfix (Author exercise)
<!-- id: sq-infix-to-postfix -->

**Approach.**
The method converts the infix tokens to postfix with one operator stack and an output list, and it returns that list. A number goes to the output. An operator first pops every waiting operator whose precedence is at least its own, because those operators must run before it, and then waits on the stack. The test is `>=` and not `>`, which makes equal operators run from left to right. For `6 - 2 - 3` the second minus pops the first minus, so the output is `6 2 - 3 -` and not `6 2 3 - -`. At the end of the tokens the remaining operators leave in stack order. The invariant is that precedence on the operator stack never decreases from bottom to top. The test checks the returned list against two facts. Evaluating it must give the value that a separate evaluator computes with a running term and a running sum, and the numbers must keep their input order.

**Complexity.**
- **Time** is O(n), because each token is pushed once and popped at most once.
- **Space** is O(n), because the output list and the operator stack hold at most n tokens.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class InfixViaPostfix {
    static boolean isOp(String s) { return s.length() == 1 && "+-*/".indexOf(s.charAt(0)) >= 0; }

    static int prec(String op) { return op.equals("+") || op.equals("-") ? 1 : 2; }

    /**
     * Converts infix tokens to postfix tokens.
     * Time: O(n), each token is pushed and popped at most once.
     * Space: O(n), the output list and the operator stack.
     * Invariant: precedence on the operator stack does not decrease from bottom to top.
     */
    static List<String> toPostfix(String[] infix) {
        // The output receives numbers at once and operators when they are ready.
        List<String> output = new ArrayList<>();
        // Operators wait here for their right operand.
        Deque<String> ops = new ArrayDeque<>();
        // One pass over the infix tokens.
        for (String tok : infix) {
            // A number never waits.
            if (!isOp(tok)) { output.add(tok); continue; }
            // Equal precedence pops too, which makes equal operators left to right.
            while (!ops.isEmpty() && prec(ops.peekLast()) >= prec(tok)) output.add(ops.removeLast());
            // The new operator waits until its right operand has been read.
            ops.addLast(tok);
        }
        // Remaining operators leave from the top of the stack.
        while (!ops.isEmpty()) output.add(ops.removeLast());
        return output;
    }

    /** Evaluates postfix tokens with a value stack, popping the right operand first. */
    static int evalPostfix(List<String> post) {
        Deque<Integer> values = new ArrayDeque<>();
        for (String tok : post) {
            if (!isOp(tok)) { values.addLast(Integer.parseInt(tok)); continue; }
            int right = values.removeLast(), left = values.removeLast();
            char c = tok.charAt(0);
            values.addLast(c == '+' ? left + right : c == '-' ? left - right : c == '*' ? left * right : left / right);
        }
        return values.removeLast();
    }

    /** Reference: running sum and running term, no postfix list. */
    static int oracle(String[] t) {
        int sum = 0, term = Integer.parseInt(t[0]), sign = 1;
        for (int i = 1; i < t.length; i += 2) {
            int n = Integer.parseInt(t[i + 1]);
            char c = t[i].charAt(0);
            if (c == '*') term *= n;
            else if (c == '/') term /= n;
            else { sum += sign * term; sign = c == '+' ? 1 : -1; term = n; }
        }
        return sum + sign * term;
    }

    public static void main(String[] args) {
        // Example 1: equal precedence pops, so the postfix form keeps left-to-right order.
        if (!toPostfix("9 / 2 * 4 - 7".split(" ")).equals(List.of("9", "2", "/", "4", "*", "7", "-"))) throw new AssertionError("example 1");
        // Its value is 9: 9 / 2 is 4, 4 * 4 is 16, and 16 - 7 is 9.
        if (evalPostfix(toPostfix("9 / 2 * 4 - 7".split(" "))) != 9) throw new AssertionError("value 1");
        // Example 2: left association gives 6 2 - 3 - with value 1; right association would give 7.
        if (!toPostfix("6 - 2 - 3".split(" ")).equals(List.of("6", "2", "-", "3", "-"))) throw new AssertionError("example 2");
        if (evalPostfix(toPostfix("6 - 2 - 3".split(" "))) != 1) throw new AssertionError("value 2");
        if (6 - (2 - 3) != 7) throw new AssertionError("right association claim");
        // Precedence: 8 - 3 * 2 + 1 becomes 8 3 2 * - 1 + and equals 3.
        if (!toPostfix("8 - 3 * 2 + 1".split(" ")).equals(List.of("8", "3", "2", "*", "-", "1", "+"))) throw new AssertionError("postfix 2");
        // A single number passes through unchanged.
        if (!toPostfix(new String[] {"-12"}).equals(List.of("-12"))) throw new AssertionError("single");
        // Random expressions with non-zero numbers give a list of the same length, the same number order and the reference value.
        Random rnd = new Random(1111);
        for (int t = 0; t < 6000; t++) {
            int terms = 1 + rnd.nextInt(7);
            String[] tok = new String[2 * terms - 1];
            for (int i = 0; i < tok.length; i++) {
                if (i % 2 == 0) { int v = rnd.nextInt(9) + 1; tok[i] = String.valueOf(rnd.nextBoolean() ? v : -v); }
                else tok[i] = String.valueOf("+-*/".charAt(rnd.nextInt(4)));
            }
            List<String> post = toPostfix(tok);
            if (post.size() != tok.length) throw new AssertionError("length " + String.join(" ", tok));
            List<String> numsIn = new ArrayList<>(), numsOut = new ArrayList<>();
            for (int i = 0; i < tok.length; i += 2) numsIn.add(tok[i]);
            for (String s : post) if (!isOp(s)) numsOut.add(s);
            if (!numsIn.equals(numsOut)) throw new AssertionError("number order " + String.join(" ", tok));
            if (evalPostfix(post) != oracle(tok)) throw new AssertionError("random " + String.join(" ", tok));
        }
    }
}
```
