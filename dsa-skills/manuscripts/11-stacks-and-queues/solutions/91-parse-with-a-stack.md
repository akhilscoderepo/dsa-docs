<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Stack And Parsing State

#### Solution: [Build] Postfix With Error Codes (LeetCode 150)
<!-- id: sq-rpn-checked -->

**Approach.**
The reader classifies each token before it touches the stack. An operator token pops the right operand and then the left operand. A token that matches an optional minus sign and digits is a number, and it must fit in an `int`. Every other token is unknown and ends the run with the error text. The values are stored as `long`, so the product of two `int` values fits before the range test runs. After each operator the result must lie in the `int` range, or the run ends with the error text. A zero divisor and an operator with fewer than two values also end the run. At the end the stack must hold exactly one value. The invariant is that the stack holds only finished values that lie in the `int` range. The test generates valid and damaged token arrays and compares with a second evaluator that reads the tokens from the end and builds the operands by recursion.

**Complexity.**
- **Time** is O(n), because each token is classified once and each value is pushed and popped at most once.
- **Space** is O(n), because a run of numbers before the first operator fills the stack.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class CheckedPostfix {
    /**
     * Evaluates a postfix token array and returns ERR for any contract violation.
     * Time: O(n), constant work per token.
     * Space: O(n), the stack depth.
     * Invariant: every value on the stack is a finished result inside the int range.
     */
    static String evalChecked(String[] tokens) {
        // The stack holds long values so that a product of two ints cannot overflow.
        Deque<Long> stack = new ArrayDeque<>();
        // One pass classifies every token exactly once.
        for (String tok : tokens) {
            // Exactly one of the four signs makes the token an operator.
            if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/")) {
                // An operator needs two finished values.
                if (stack.size() < 2) return "ERR";
                // The first pop is the right operand, because it was pushed last.
                long right = stack.removeLast();
                // The second pop is the left operand.
                long left = stack.removeLast();
                long v;
                switch (tok.charAt(0)) {
                    case '+': v = left + right; break;
                    case '-': v = left - right; break;
                    case '*': v = left * right; break;
                    default:
                        // A zero divisor is a contract violation.
                        if (right == 0) return "ERR";
                        // Java division on long truncates toward zero.
                        v = left / right;
                }
                // Any result outside the int range is a contract violation.
                if (v < Integer.MIN_VALUE || v > Integer.MAX_VALUE) return "ERR";
                stack.addLast(v);
            } else if (tok.matches("-?[0-9]+")) {
                // At most 12 characters, so the parse into long cannot overflow.
                long v = Long.parseLong(tok);
                // A literal outside the int range is rejected.
                if (v < Integer.MIN_VALUE || v > Integer.MAX_VALUE) return "ERR";
                stack.addLast(v);
            } else {
                // Any other token is unknown.
                return "ERR";
            }
        }
        // A complete expression leaves exactly one value.
        return stack.size() == 1 ? String.valueOf(stack.removeLast()) : "ERR";
    }

    // Position for the reference reader, which consumes tokens from the end.
    static int pos;

    /** Reference: reads from the end; an operator reads its right and left operands recursively. */
    static Long ref(String[] t) {
        if (pos < 0) return null;
        String tok = t[pos--];
        if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/")) {
            Long r = ref(t);
            if (r == null) return null;
            Long l = ref(t);
            if (l == null) return null;
            long v = tok.equals("+") ? l + r : tok.equals("-") ? l - r : tok.equals("*") ? l * r : 0;
            if (tok.equals("/")) { if (r == 0) return null; v = l / r; }
            return v < Integer.MIN_VALUE || v > Integer.MAX_VALUE ? null : v;
        }
        if (!tok.matches("-?[0-9]+")) return null;
        long v = Long.parseLong(tok);
        return v < Integer.MIN_VALUE || v > Integer.MAX_VALUE ? null : v;
    }

    static String oracle(String[] t) {
        pos = t.length - 1;
        Long v = ref(t);
        return v == null || pos != -1 ? "ERR" : String.valueOf(v);
    }

    static void gen(Random rnd, int depth, List<String> out) {
        if (depth == 0 || rnd.nextInt(3) == 0) {
            int pick = rnd.nextInt(12);
            out.add(pick == 0 ? "46341" : pick == 1 ? "2147483647" : String.valueOf(rnd.nextInt(41) - 20));
            return;
        }
        gen(rnd, depth - 1, out);
        gen(rnd, depth - 1, out);
        out.add(String.valueOf("+-*/".charAt(rnd.nextInt(4))));
    }

    public static void main(String[] args) {
        // Example 1: 7 - 2 is 5, and 5 * 3 is 15.
        if (!evalChecked("7 2 - 3 *".split(" ")).equals("15")) throw new AssertionError("example 1");
        // Example 2: % is not one of the four operators.
        if (!evalChecked("6 3 %".split(" ")).equals("ERR")) throw new AssertionError("example 2");
        // Each rejection rule in turn: empty input, too few operands, leftovers, zero divisor, overflow.
        if (!evalChecked(new String[0]).equals("ERR")) throw new AssertionError("empty");
        if (!evalChecked("4 +".split(" ")).equals("ERR")) throw new AssertionError("underflow");
        if (!evalChecked("1 2".split(" ")).equals("ERR")) throw new AssertionError("leftover");
        if (!evalChecked("5 0 /".split(" ")).equals("ERR")) throw new AssertionError("zero divisor");
        if (!evalChecked("65536 65536 *".split(" ")).equals("ERR")) throw new AssertionError("overflow");
        if (!evalChecked("2147483648".split(" ")).equals("ERR")) throw new AssertionError("literal range");
        if (!evalChecked("+5".split(" ")).equals("ERR")) throw new AssertionError("plus sign");
        // A negative literal is a number, and the lone minus sign is an operator.
        if (!evalChecked("-3 -4 -".split(" ")).equals("1")) throw new AssertionError("negative literal");
        // Random valid and damaged arrays agree with the reference reader.
        Random rnd = new Random(9101);
        String[] junk = {"%", "x", "+5", "99999999999", "0", "-", "1.5"};
        int ok = 0, err = 0;
        for (int t = 0; t < 8000; t++) {
            List<String> toks = new ArrayList<>();
            gen(rnd, 1 + rnd.nextInt(4), toks);
            // Half of the arrays are damaged by one random edit.
            if (rnd.nextBoolean()) {
                int at = rnd.nextInt(toks.size());
                int kind = rnd.nextInt(3);
                if (kind == 0) toks.set(at, junk[rnd.nextInt(junk.length)]);
                else if (kind == 1) toks.remove(at);
                else toks.add(at, junk[rnd.nextInt(junk.length)]);
            }
            String[] arr = toks.toArray(new String[0]);
            String got = evalChecked(arr), want = oracle(arr);
            if (!got.equals(want)) throw new AssertionError(String.join(" ", arr) + " got " + got + " want " + want);
            if (got.equals("ERR")) err++; else ok++;
        }
        // Both outcomes occurred often enough to test each branch.
        if (ok < 500 || err < 500) throw new AssertionError("outcome mix " + ok + " " + err);
    }
}
```

#### Solution: [Vary] Decode With A Length Limit (LeetCode 394)
<!-- id: sq-decode-bounded -->

**Approach.**
The reader keeps the text of the current level, the repeat count being read, and a stack of saved frames. Each frame holds the parent text and a count. An opening bracket saves the frame and starts an empty level. A closing bracket pops the frame and computes the new length as the parent length plus the count times the current length, in `long`. When that length exceeds the limit, the method returns `null` before it appends anything. Otherwise the method appends the current text `count` times to the parent text. A letter also checks the current length, because the final length is never smaller than the current level. The invariant is that no text held in the method is longer than the limit. A hostile input with five nested counts of 300 therefore returns `null` at the first closing bracket whose product exceeds the limit. The test compares with a full expansion of small random encodings.

**Complexity.**
- **Time** is O(n + limit), because the reader visits each character once and every append is within the limit.
- **Space** is O(n + limit), because the frames hold at most the digits and brackets of the input and every stored text is within the limit.

```java run
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Random;

public final class BoundedDecode {
    /**
     * Decodes nested repeat groups, or returns null when the result is longer than limit.
     * Time: O(n + limit), each append stays within the limit.
     * Space: O(n + limit), saved parents never exceed the limit.
     * Invariant: every StringBuilder in the method has length at most limit.
     */
    static String decodeBounded(String s, int limit) {
        // Saved counts and parent texts form the stack of frames.
        Deque<Integer> counts = new ArrayDeque<>();
        Deque<StringBuilder> parents = new ArrayDeque<>();
        // cur is the text of the level being read.
        StringBuilder cur = new StringBuilder();
        // num is the repeat count being read.
        int num = 0;
        // One pass over the characters.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                // A digit extends the count; counts have several digits.
                num = num * 10 + (c - '0');
            } else if (c == '[') {
                // Save the parent text and the count, then start a new level.
                counts.addLast(num);
                parents.addLast(cur);
                cur = new StringBuilder();
                num = 0;
            } else if (c == ']') {
                // Restore the parent frame.
                int k = counts.removeLast();
                StringBuilder parent = parents.removeLast();
                // The new length is computed in long before any text is built.
                long newLen = parent.length() + (long) k * cur.length();
                // Early rejection happens here, before the repeated append.
                if (newLen > limit) return null;
                // The append count is safe because newLen is within the limit.
                for (int r = 0; r < k; r++) parent.append(cur);
                cur = parent;
            } else {
                // A letter extends the current level.
                cur.append(c);
                // The final text is never shorter than the current level, so this check is safe.
                if (cur.length() > limit) return null;
            }
        }
        return cur.toString();
    }

    /** Reference: expands recursively with no limit, then compares lengths. */
    static int at;
    static String expand(String s) {
        StringBuilder sb = new StringBuilder();
        while (at < s.length() && s.charAt(at) != ']') {
            char c = s.charAt(at);
            if (Character.isDigit(c)) {
                int k = 0;
                while (Character.isDigit(s.charAt(at))) k = k * 10 + (s.charAt(at++) - '0');
                at++; // skip [
                String inner = expand(s);
                at++; // skip ]
                sb.append(inner.repeat(k));
            } else { sb.append(c); at++; }
        }
        return sb.toString();
    }

    static String gen(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        int parts = 1 + rnd.nextInt(3);
        for (int i = 0; i < parts; i++) {
            if (depth > 0 && rnd.nextInt(3) == 0) sb.append(1 + rnd.nextInt(12)).append('[').append(gen(rnd, depth - 1)).append(']');
            else sb.append((char) ('a' + rnd.nextInt(3)));
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1: the decoded text has 9 characters, within the limit 20.
        if (!"abbbabbbc".equals(decodeBounded("2[a3[b]]c", 20))) throw new AssertionError("example 1");
        // Example 2: the decoded length is 18, above the limit 10.
        if (decodeBounded("2[3[abc]]", 10) != null) throw new AssertionError("example 2");
        // The limit itself is allowed: 18 characters pass at limit 18 and fail at 17.
        if (decodeBounded("2[3[abc]]", 18) == null || decodeBounded("2[3[abc]]", 17) != null) throw new AssertionError("exact limit");
        // A hostile input has 300^5 decoded characters and returns null at once.
        if (decodeBounded("300[300[300[300[300[a]]]]]", 1_000_000) != null) throw new AssertionError("hostile");
        // A flat letter string longer than the limit is rejected as well.
        if (decodeBounded("abcdef", 5) != null) throw new AssertionError("flat");
        // Random encodings agree with a full expansion and a length comparison.
        Random rnd = new Random(9102);
        int nulls = 0, texts = 0;
        for (int t = 0; t < 5000; t++) {
            String enc = gen(rnd, 3);
            at = 0;
            String full = expand(enc);
            int limit = 1 + rnd.nextInt(60);
            String want = full.length() > limit ? null : full;
            String got = decodeBounded(enc, limit);
            if (want == null ? got != null : !want.equals(got)) throw new AssertionError(enc + " limit " + limit);
            if (want == null) nulls++; else texts++;
        }
        // Both outcomes occurred often.
        if (nulls < 300 || texts < 300) throw new AssertionError("outcome mix " + nulls + " " + texts);
    }
}
```

#### Solution: [Boundary] Simplify A Unix Path (LeetCode 71)
<!-- id: sq-simplify-path -->

**Approach.**
The method keeps the open names in a `String` array and an `int` named `top` that counts them, and it scans the path with `indexOf` to cut one component at a time. Empty components come from repeated or trailing slashes, and the component `.` names the current directory, so both change nothing. The component `..` lowers `top` only when `top` is above 0, because the root has no parent. Any other component, including `...`, is a name and is stored at index `top`. After the last component the entries below `top` hold the names from the root outward. The answer is a slash before each name, or a single slash when `top` is 0. The invariant says that the entries below `top` are the canonical names of the path read so far. The test compares with the rewriting method from the lesson's opening, which deletes a name together with the next `..` until none are left.

**Complexity.**
- **Time** is O(n), because each piece is pushed at most once and popped at most once, and the final join visits each kept character once.
- **Space** is O(n), because the pieces and the stack together hold at most the characters of the path.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class SimplifyUnixPath {
    /**
     * Returns the canonical form of an absolute path.
     * Time: O(n), each component is stored at most once and removed at most once.
     * Space: O(n), the name array and the output.
     * Invariant: names[0..top) are the canonical names of the components read so far.
     */
    static String simplify(String path) {
        // The array is the stack, and top counts the open names.
        String[] names = new String[path.length() / 2 + 1];
        int top = 0;
        // Each pass cuts the component that starts at index from.
        for (int from = 0; from < path.length(); ) {
            int slash = path.indexOf('/', from);
            if (slash < 0) slash = path.length();
            String piece = path.substring(from, slash);
            from = slash + 1;
            // Empty components and the current-directory component change nothing.
            if (piece.isEmpty() || piece.equals(".")) continue;
            if (piece.equals("..")) {
                // The parent move lowers top only above the root; at the root it is a no-op.
                if (top > 0) top--;
            } else {
                // Everything else, including "...", is a name stored at index top.
                names[top++] = piece;
            }
        }
        // A count of 0 is the root alone.
        if (top == 0) return "/";
        // One slash precedes each name, so no trailing slash appears.
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < top; i++) sb.append('/').append(names[i]);
        return sb.toString();
    }

    /** Reference: rewrite until no parent move is left. */
    static String oracle(String path) {
        List<String> parts = new ArrayList<>();
        for (String p : path.split("/")) if (!p.isEmpty() && !p.equals(".")) parts.add(p);
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < parts.size(); i++) {
                if (!parts.get(i).equals("..")) continue;
                parts.remove(i);
                if (i > 0) parts.remove(i - 1);
                changed = true;
                break;
            }
        }
        return "/" + String.join("/", parts);
    }

    public static void main(String[] args) {
        // Example 1: b and a are removed, and c remains.
        if (!simplify("/a/./b/../../c/").equals("/c")) throw new AssertionError("example 1");
        // Example 2: the parent move at the root does nothing, and three periods are a name.
        if (!simplify("/../...//x/").equals("/.../x")) throw new AssertionError("example 2");
        // The root alone and a path that returns to the root.
        if (!simplify("/").equals("/") || !simplify("/a/..").equals("/")) throw new AssertionError("root");
        // A name that starts with periods is still a name.
        if (!simplify("/.hidden/../..a").equals("/..a")) throw new AssertionError("dot names");
        // Random paths agree with the rewriting reference.
        Random rnd = new Random(9103);
        String[] comps = {"a", "b", "c", ".", "..", "...", "", ".x", "a_b"};
        for (int t = 0; t < 8000; t++) {
            StringBuilder sb = new StringBuilder("/");
            int n = rnd.nextInt(12);
            for (int i = 0; i < n; i++) sb.append(comps[rnd.nextInt(comps.length)]).append('/');
            String p = sb.toString();
            // Half of the paths lose their trailing slash.
            if (rnd.nextBoolean() && p.length() > 1) p = p.substring(0, p.length() - 1);
            if (!simplify(p).equals(oracle(p))) throw new AssertionError(p);
        }
    }
}
```

#### Solution: [Recognize] Calculator With Named Variables (LeetCode 224)
<!-- id: sq-calc-variables -->

**Approach.**
The method keeps `result` for the current level and `sign` for the next operand. A number or a name adds `sign` times its value to `result` at once, so no pending number exists between tokens. A plus or minus sets `sign` for the next operand. Because `result` is zero at the start and after an opening parenthesis, a unary minus there sets `sign` to minus one and works like a binary one. An opening parenthesis pushes the pair of `result` and `sign` and starts a level with `result` zero and `sign` one. A closing parenthesis pops the pair and sets `result` to the saved result plus the saved sign times the finished level. A name is read as a run of lowercase letters and looked up in a map built from the arrays. A missing name returns `null`. The invariant is that the stack holds one pair for each open parenthesis, and `result` is the value of the innermost open level so far. The test compares with a recursive descent evaluator on random expressions with spaces, unary minus and undefined names.

**Complexity.**
- **Time** is O(n + m), because the reader visits each character once and the map takes m entries to build.
- **Space** is O(n + m), because the stack holds one pair per open parenthesis and the map holds m names.

```java run
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

public final class NamedCalculator {
    /**
     * Evaluates an expression with names, signs and parentheses, or returns null for an unknown name.
     * Time: O(n + m), one pass plus the map build.
     * Space: O(n + m), the stack and the map.
     * Invariant: the stack has one saved pair per open parenthesis.
     */
    static Integer evaluate(String s, String[] names, int[] values) {
        // The map answers every name lookup in O(1) expected time.
        Map<String, Integer> env = new HashMap<>();
        for (int i = 0; i < names.length; i++) env.put(names[i], values[i]);
        // Each frame is {saved result, saved sign}.
        Deque<int[]> frames = new ArrayDeque<>();
        // result is the value of the innermost open level so far.
        int result = 0;
        // sign multiplies the next operand.
        int sign = 1;
        // The index moves forward because numbers and names span several characters.
        int i = 0;
        while (i < s.length()) {
            char c = s.charAt(i);
            if (c == ' ') {
                // A space carries no meaning.
                i++;
            } else if (Character.isDigit(c)) {
                // Read the whole number, then add it with the pending sign.
                int v = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i))) v = v * 10 + (s.charAt(i++) - '0');
                result += sign * v;
            } else if (Character.isLetter(c)) {
                // Read the whole name, then look it up.
                int start = i;
                while (i < s.length() && Character.isLetter(s.charAt(i))) i++;
                Integer v = env.get(s.substring(start, i));
                // An unknown name rejects the expression.
                if (v == null) return null;
                result += sign * v;
            } else if (c == '+' || c == '-') {
                // The sign applies to the next operand, whether the sign is binary or unary.
                sign = c == '+' ? 1 : -1;
                i++;
            } else if (c == '(') {
                // Save the outer result and the sign in front of the group.
                frames.addLast(new int[] {result, sign});
                result = 0;
                sign = 1;
                i++;
            } else {
                // The closing parenthesis combines the finished group with the saved pair.
                int[] saved = frames.removeLast();
                result = saved[0] + saved[1] * result;
                i++;
            }
        }
        return result;
    }

    // Reference parser state.
    static String src;
    static int p;
    static Map<String, Integer> ref;
    static boolean undefined;

    /** Reference: expr = ['-'] term {('+'|'-') term}. */
    static int expr() {
        skip();
        boolean neg = false;
        if (p < src.length() && src.charAt(p) == '-') { neg = true; p++; }
        int v = term();
        if (neg) v = -v;
        skip();
        while (p < src.length() && (src.charAt(p) == '+' || src.charAt(p) == '-')) {
            char op = src.charAt(p++);
            int r = term();
            v = op == '+' ? v + r : v - r;
            skip();
        }
        return v;
    }

    static int term() {
        skip();
        char c = src.charAt(p);
        if (c == '(') { p++; int v = expr(); skip(); p++; return v; }
        if (Character.isDigit(c)) { int v = 0; while (p < src.length() && Character.isDigit(src.charAt(p))) v = v * 10 + (src.charAt(p++) - '0'); return v; }
        int st = p;
        while (p < src.length() && Character.isLetter(src.charAt(p))) p++;
        Integer v = ref.get(src.substring(st, p));
        if (v == null) { undefined = true; return 0; }
        return v;
    }

    static void skip() { while (p < src.length() && src.charAt(p) == ' ') p++; }

    static String gen(Random rnd, int depth, String[] pool) {
        StringBuilder sb = new StringBuilder();
        if (rnd.nextInt(4) == 0) sb.append('-');
        sb.append(termText(rnd, depth, pool));
        int more = rnd.nextInt(4);
        for (int i = 0; i < more; i++) sb.append(rnd.nextBoolean() ? " + " : "-").append(termText(rnd, depth, pool));
        return sb.toString();
    }

    static String termText(Random rnd, int depth, String[] pool) {
        int k = rnd.nextInt(depth > 0 ? 3 : 2);
        if (k == 0) return String.valueOf(rnd.nextInt(30));
        if (k == 1) return pool[rnd.nextInt(pool.length)];
        return "(" + gen(rnd, depth - 1, pool) + ")";
    }

    public static void main(String[] args) {
        // Example 1: the group is 7, and the whole expression is -7 - 5 = -12.
        if (evaluate("-(x+4)-y", new String[] {"x", "y"}, new int[] {3, 5}) != -12) throw new AssertionError("example 1");
        // Example 2: 7 - (10 - 3) is 0, and an empty map rejects the expression.
        if (evaluate("7-(k-(2+1))", new String[] {"k"}, new int[] {10}) != 0) throw new AssertionError("example 2a");
        if (evaluate("7-(k-(2+1))", new String[0], new int[0]) != null) throw new AssertionError("example 2b");
        // A unary minus before a nested group and a multi-letter name.
        if (evaluate("-(-(ab))", new String[] {"ab"}, new int[] {6}) != 6) throw new AssertionError("double unary");
        // Random expressions agree with the recursive descent reference.
        Random rnd = new Random(9104);
        String[] pool = {"x", "y", "ab", "k", "zz"};
        int nulls = 0, nums = 0;
        for (int t = 0; t < 8000; t++) {
            String expr = gen(rnd, 3, pool);
            // Each name is defined with probability one half.
            java.util.List<String> nm = new java.util.ArrayList<>();
            for (String q : pool) if (rnd.nextBoolean()) nm.add(q);
            String[] names = nm.toArray(new String[0]);
            int[] vals = new int[names.length];
            ref = new HashMap<>();
            for (int i = 0; i < names.length; i++) { vals[i] = rnd.nextInt(41) - 20; ref.put(names[i], vals[i]); }
            src = expr; p = 0; undefined = false;
            int want = expr();
            Integer got = evaluate(expr, names, vals);
            if (undefined ? got != null : (got == null || got != want)) throw new AssertionError(expr);
            if (got == null) nulls++; else nums++;
        }
        // Both outcomes occurred often.
        if (nulls < 500 || nums < 500) throw new AssertionError("outcome mix " + nulls + " " + nums);
    }
}
```
