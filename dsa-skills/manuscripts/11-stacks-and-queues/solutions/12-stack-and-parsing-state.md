<!-- solutions-for: 12-stack-and-parsing-state -->
### Stack And Parsing State

#### Solution: [Build] Evaluate Reverse Polish With Peak (LeetCode 150)
<!-- id: sq-sp-rpn-with-peak -->

**Approach.** Run the value-stack evaluator and record the stack size after every token. A number grows the stack by one, and an operator pops two values and pushes one, so the size drops by one. The operand popped first is the right operand, which matters for minus and divide. The answer is the final value and the largest recorded size. The assertions compare with a recursive evaluation of a random expression tree whose peak is computed from the tree shape, using the rule that evaluating the left subtree and then the right subtree needs the maximum of the left peak and one more than the right peak.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class RpnWithPeak {
    static long[] run(String[] tokens) {
        ArrayDeque<Long> values = new ArrayDeque<>();
        int peak = 0;
        for (String tok : tokens) {
            if (tok.length() == 1 && "+-*/".indexOf(tok.charAt(0)) >= 0) {
                long right = values.removeLast(), left = values.removeLast();
                values.addLast(tok.equals("+") ? left + right : tok.equals("-") ? left - right
                        : tok.equals("*") ? left * right : left / right);
            } else values.addLast(Long.parseLong(tok));
            peak = Math.max(peak, values.size());
        }
        return new long[] {values.removeLast(), peak};
    }
    static long[] build(Random rnd, List<String> out, int depth) {
        if (depth == 0 || rnd.nextInt(4) == 0) {
            int v = rnd.nextInt(41) - 20;
            out.add(String.valueOf(v));
            return new long[] {v, 1};
        }
        long[] l = build(rnd, out, depth - 1);
        long[] r = build(rnd, out, depth - 1);
        char op = "+-*/".charAt(rnd.nextInt(4));
        if (op == '/' && r[0] == 0) op = '-';
        out.add(String.valueOf(op));
        long v = op == '+' ? l[0] + r[0] : op == '-' ? l[0] - r[0] : op == '*' ? l[0] * r[0] : l[0] / r[0];
        return new long[] {v, Math.max(l[1], 1 + r[1])};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new String[] {"6", "2", "/", "4", "3", "-", "*"}), new long[] {3, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new String[] {"5"}), new long[] {5, 1})) throw new AssertionError("example 2");
        if (run(new String[] {"8", "3", "-"})[0] != 5) throw new AssertionError("the right operand is popped first");
        Random rnd = new Random(12201);
        for (int t = 0; t < 5000; t++) {
            List<String> tokens = new ArrayList<>();
            long[] want = build(rnd, tokens, 5);
            if (!Arrays.equals(run(tokens.toArray(new String[0])), want)) throw new AssertionError("differs on " + tokens);
        }
    }
}
```

#### Solution: [Vary] Decoded Length Without Building (LeetCode 394)
<!-- id: sq-sp-decoded-length -->

**Approach.** Keep a current length and a count being read. An opening bracket parks the parent length and the count and starts the inner level at zero. A closing bracket multiplies the inner length by the parked count, saturating at the cap plus one, and adds the parent length, again saturating. A letter adds one. A count of zero gives zero even for a saturated inner length, because the product is taken as zero when either factor is zero. At the end a value above the cap gives -1. The assertions compare with exact `BigInteger` arithmetic that follows the same structure but never saturates, then apply the cap at the end.

**Complexity.** O(n) time and O(depth) space.

```java run
import java.math.BigInteger;
import java.util.ArrayDeque;
import java.util.Random;

public final class DecodedLength {
    static final long CAP = 1_000_000_000_000_000_000L;
    static long length(String s) {
        ArrayDeque<long[]> frames = new ArrayDeque<>();
        long cur = 0, count = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') count = count * 10 + (c - '0');
            else if (c == '[') { frames.addLast(new long[] {cur, count}); cur = 0; count = 0; }
            else if (c == ']') {
                long[] f = frames.removeLast();
                long repeated = (f[1] == 0 || cur == 0) ? 0 : (cur > (CAP + 1) / f[1] ? CAP + 1 : f[1] * cur);
                cur = Math.min(f[0] + repeated, CAP + 1);
            } else cur = Math.min(cur + 1, CAP + 1);
        }
        return cur > CAP ? -1 : cur;
    }
    static long exact(String s) {
        ArrayDeque<BigInteger[]> frames = new ArrayDeque<>();
        BigInteger cur = BigInteger.ZERO, count = BigInteger.ZERO;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') count = count.multiply(BigInteger.TEN).add(BigInteger.valueOf(c - '0'));
            else if (c == '[') { frames.addLast(new BigInteger[] {cur, count}); cur = BigInteger.ZERO; count = BigInteger.ZERO; }
            else if (c == ']') { BigInteger[] f = frames.removeLast(); cur = f[0].add(f[1].multiply(cur)); }
            else cur = cur.add(BigInteger.ONE);
        }
        return cur.compareTo(BigInteger.valueOf(CAP)) > 0 ? -1 : cur.longValueExact();
    }
    static void build(Random rnd, StringBuilder sb, int depth, boolean big) {
        for (int parts = 1 + rnd.nextInt(3); parts > 0; parts--) {
            if (depth > 0 && rnd.nextInt(2) == 0) {
                int count = big ? (rnd.nextInt(3) == 0 ? 0 : 1 + rnd.nextInt(1000000000)) : rnd.nextInt(5);
                sb.append(count).append('[');
                build(rnd, sb, depth - 1, big);
                sb.append(']');
            } else sb.append((char) ('a' + rnd.nextInt(3)));
        }
    }

    public static void main(String[] args) {
        if (length("3[ab2[c]]d") != 13) throw new AssertionError("example 1");
        if (length("1000000000[1000000000[1000000000[a]]]") != -1) throw new AssertionError("example 2");
        if (length("0[1000000000[1000000000[1000000000[a]]]]x") != 1) throw new AssertionError("a zero count hides a huge group");
        if (length("12[a]") != 12) throw new AssertionError("a multi-digit count");
        Random rnd = new Random(12202);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 4, t % 2 == 1);
            String s = sb.toString();
            if (length(s) != exact(s)) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Boundary] Simplify Path (LeetCode 71)
<!-- id: sq-sp-simplify-path -->

**Approach.** Split the path at slashes and give each part a stack action. An empty part or a single dot does nothing, a double dot removes the newest open directory if there is one, and any other part is added. A double dot on an empty stack is ignored, so the result cannot climb above the root. Parts are compared by exact text, so `...` is an ordinary name. The canonical path is the slash-joined names, or a single slash when no names remain. The assertions compare with the backward-scanning method of the lesson and check the examples and the three-dot name.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class SimplifyPathSolution {
    static String simplify(String path) {
        ArrayDeque<String> names = new ArrayDeque<>();
        for (String part : path.split("/")) {
            if (part.isEmpty() || part.equals(".")) continue;
            if (part.equals("..")) { if (!names.isEmpty()) names.removeLast(); }
            else names.addLast(part);
        }
        StringBuilder sb = new StringBuilder();
        for (String n : names) sb.append('/').append(n);
        return sb.length() == 0 ? "/" : sb.toString();
    }
    static String scanning(String path) {
        String[] parts = path.split("/");
        boolean[] gone = new boolean[parts.length];
        for (int i = 0; i < parts.length; i++) {
            if (parts[i].isEmpty() || parts[i].equals(".")) gone[i] = true;
            else if (parts[i].equals("..")) {
                gone[i] = true;
                for (int j = i - 1; j >= 0; j--) if (!gone[j]) { gone[j] = true; break; }
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < parts.length; i++) if (!gone[i]) sb.append('/').append(parts[i]);
        return sb.length() == 0 ? "/" : sb.toString();
    }

    public static void main(String[] args) {
        if (!simplify("/a/./b/../../c/").equals("/c")) throw new AssertionError("example 1");
        if (!simplify("/../").equals("/")) throw new AssertionError("example 2");
        if (!simplify("/home//foo/").equals("/home/foo")) throw new AssertionError("doubled slashes");
        if (!simplify("/.../a/..").equals("/...")) throw new AssertionError("three dots is a name");
        if (!simplify("/a/b/../../..").equals("/")) throw new AssertionError("climbing above the root");
        String[] pool = {"a", "b", "c", ".", "..", "...", "", "x_1"};
        Random rnd = new Random(12203);
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder("/");
            for (int k = rnd.nextInt(10); k > 0; k--) sb.append(pool[rnd.nextInt(pool.length)]).append('/');
            if (rnd.nextBoolean() && sb.length() > 1) sb.setLength(sb.length() - 1);
            String p = sb.toString();
            if (!simplify(p).equals(scanning(p))) throw new AssertionError("differs on " + p);
        }
    }
}
```

#### Solution: [Recognize] Basic Calculator With Depth (LeetCode 224)
<!-- id: sq-sp-calculator-depth -->

**Approach.** Keep the level total, the sign for the next number, and a stack with the saved total and sign for each open bracket. A plus or minus commits the number read so far, an opening bracket saves the total and the sign and restarts the inside, and a closing bracket commits the number and folds the inside into the saved total with the saved sign. The depth is the largest size that the stack reaches. A minus at the start of a bracket commits a zero, so it needs no special case. All arithmetic is in `long`. The assertions compare with a recursive-descent parser that also reports the deepest bracket nesting it enters, on random nested expressions with large numbers.

**Complexity.** O(n) time and O(depth) space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class CalculatorWithDepth {
    static long[] calculate(String s) {
        ArrayDeque<long[]> saved = new ArrayDeque<>();
        long result = 0, num = 0;
        int sign = 1, deepest = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') num = num * 10 + (c - '0');
            else if (c == '+' || c == '-') { result += sign * num; num = 0; sign = c == '+' ? 1 : -1; }
            else if (c == '(') { saved.addLast(new long[] {result, sign}); deepest = Math.max(deepest, saved.size()); result = 0; sign = 1; }
            else if (c == ')') {
                result += sign * num; num = 0;
                long[] outer = saved.removeLast();
                result = outer[0] + outer[1] * result;
            }
        }
        return new long[] {result + sign * num, deepest};
    }
    static String text;
    static int pos, level, maxLevel;
    static long[] oracle(String s) {
        text = s.replace(" ", "");
        pos = 0; level = 0; maxLevel = 0;
        long v = expression();
        return new long[] {v, maxLevel};
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
            level++;
            maxLevel = Math.max(maxLevel, level);
            long v = expression();
            pos++;
            level--;
            return sign * v;
        }
        long v = 0;
        while (pos < text.length() && Character.isDigit(text.charAt(pos))) v = v * 10 + (text.charAt(pos++) - '0');
        return sign * v;
    }
    static void build(Random rnd, StringBuilder sb, int depth, boolean lead) {
        if (lead && rnd.nextInt(4) == 0) sb.append('-');
        term(rnd, sb, depth);
        for (int k = rnd.nextInt(3); k > 0; k--) {
            if (rnd.nextInt(2) == 0) sb.append(' ');
            sb.append(rnd.nextBoolean() ? '+' : '-');
            if (rnd.nextInt(2) == 0) sb.append(' ');
            term(rnd, sb, depth);
        }
    }
    static void term(Random rnd, StringBuilder sb, int depth) {
        if (depth > 0 && rnd.nextInt(3) == 0) { sb.append('('); build(rnd, sb, depth - 1, true); sb.append(')'); }
        else sb.append(rnd.nextInt(2) == 0 ? rnd.nextInt(100) : 1_000_000_000_000L - rnd.nextInt(1000));
    }

    public static void main(String[] args) {
        if (!Arrays.equals(calculate("2-(5-(6+1))+(10-3)"), new long[] {11, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(calculate("-(-3+10)"), new long[] {-7, 1})) throw new AssertionError("example 2");
        if (calculate("1000000000000+1000000000000")[0] != 2_000_000_000_000L) throw new AssertionError("values beyond int need a long");
        if (calculate("5")[1] != 0) throw new AssertionError("no brackets means depth zero");
        Random rnd = new Random(12204);
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 4, true);
            String s = sb.toString();
            if (!Arrays.equals(calculate(s), oracle(s))) throw new AssertionError("differs on [" + s + "]");
        }
    }
}
```
