<!-- solutions-for: 06-nested-structure -->
### Nested Structure

#### Solution: [Build] Maximum Parenthesis Depth (Author exercise)
<!-- id: sq-max-parenthesis-depth -->

**Approach.** Keep the number of open groups as a counter, increase it at an opening bracket, decrease it at a closing one, and remember the largest value reached. Only the height of the stack is needed, so the counter replaces the stack itself. The assertions compare with a version that keeps a real stack and reports its maximum size, and with a recursive definition that takes one plus the largest depth among the children, on random balanced strings.

**Complexity.** O(n) time and O(1) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class MaxParenthesisDepth {
    static int depthCounter(String s) {
        int depth = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') { depth++; best = Math.max(best, depth); }
            else depth--;
        }
        return best;
    }
    static int depthStack(String s) {
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') { stack.addLast(i); best = Math.max(best, stack.size()); }
            else stack.removeLast();
        }
        return best;
    }
    static int recursive(String s, int lo, int hi) {
        int best = 0, i = lo;
        while (i < hi) {
            int bal = 0, j = i;
            do { bal += s.charAt(j) == '(' ? 1 : -1; j++; } while (bal > 0);
            best = Math.max(best, 1 + recursive(s, i + 1, j - 1));
            i = j;
        }
        return best;
    }
    static void build(Random rnd, StringBuilder sb, int depth) {
        int parts = rnd.nextInt(3);
        for (int p = 0; p < parts; p++) {
            sb.append('(');
            if (depth > 0) build(rnd, sb, depth - 1);
            sb.append(')');
        }
    }

    public static void main(String[] args) {
        if (depthCounter("(()(()))") != 3) throw new AssertionError("example 1");
        if (depthCounter("()()") != 1) throw new AssertionError("example 2");
        if (depthCounter("") != 0) throw new AssertionError("empty string");
        Random rnd = new Random(11601);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 5);
            String s = sb.toString();
            int a = depthCounter(s);
            if (a != depthStack(s)) throw new AssertionError("stack differs on " + s);
            if (a != recursive(s, 0, s.length())) throw new AssertionError("recursion differs on " + s);
        }
    }
}
```

#### Solution: [Vary] Sum Values By Nested Group (Author exercise)
<!-- id: sq-sum-by-nested-group -->

**Approach.** Keep a running total for the current level. At an opening bracket, push the current total and start the new level at zero. At a closing bracket, the finished level's total is worth double to its parent, so the new current total is the popped value plus twice the finished one. A digit adds to the current total. After the last character the current total is the value of the whole string. The assertions compare with a closed form in which a digit at depth d contributes the digit times 2 to the power d, which follows from the doubling at every enclosing group, and check both examples.

**Complexity.** O(n) time and O(depth) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class SumByNestedGroup {
    static long value(String s) {
        ArrayDeque<Long> saved = new ArrayDeque<>();
        long current = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(') { saved.addLast(current); current = 0; }
            else if (c == ')') current = saved.removeLast() + 2 * current;
            else current += c - '0';
        }
        return current;
    }
    static long closedForm(String s) {
        long total = 0;
        int depth = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(') depth++;
            else if (c == ')') depth--;
            else total += (long) (c - '0') << depth;
        }
        return total;
    }
    static void build(Random rnd, StringBuilder sb, int depth) {
        int parts = rnd.nextInt(5);
        for (int p = 0; p < parts; p++) {
            if (depth > 0 && rnd.nextInt(3) == 0) {
                sb.append('(');
                build(rnd, sb, depth - 1);
                sb.append(')');
            } else sb.append((char) ('0' + rnd.nextInt(10)));
        }
    }

    public static void main(String[] args) {
        if (value("1(2)3") != 8) throw new AssertionError("example 1");
        if (value("(1(2))") != 10) throw new AssertionError("example 2");
        if (value("") != 0) throw new AssertionError("empty string");
        if (value("1(2(3))4") != 21) throw new AssertionError("the trace in the lesson");
        Random rnd = new Random(11602);
        for (int t = 0; t < 5000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 6);
            String s = sb.toString();
            if (value(s) != closedForm(s)) throw new AssertionError("differs on " + s);
        }
    }
}
```

#### Solution: [Boundary] Deep Single Chain (Author exercise)
<!-- id: sq-deep-single-chain -->

**Approach.** Scan once with a counter for open groups. A closing bracket at height zero means a premature close, so return the failure pair at once. Count each opening as a group and track the largest height. After the scan, a nonzero height means an unclosed group, which is the second failure. No recursion follows the nesting, so a chain of a hundred thousand levels costs only a counter. The assertions run a chain of 100000 openings and closings, show that a naive recursive depth function overflows the call stack on a chain of ten million, and compare with an erase-based validity check and a recursive count on random shallow strings.

**Complexity.** O(n) time and O(1) space.

```java run
import java.util.Random;

public final class DeepSingleChain {
    static int[] measure(String s) {
        int height = 0, deepest = 0, groups = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') { height++; groups++; deepest = Math.max(deepest, height); }
            else {
                if (height == 0) return new int[] {-1, -1};
                height--;
            }
        }
        return height == 0 ? new int[] {deepest, groups} : new int[] {-1, -1};
    }
    static int recursiveDepth(int levels) {
        if (levels == 0) return 0;
        return 1 + recursiveDepth(levels - 1);
    }
    static boolean erasing(String s) {
        String cur = s;
        while (cur.contains("()")) cur = cur.replace("()", "");
        return cur.isEmpty();
    }
    static int groupsByPairs(String s) {
        int n = 0;
        for (int i = 0; i < s.length(); i++) if (s.charAt(i) == '(') n++;
        return n;
    }

    public static void main(String[] args) {
        int[] a = measure("((()))");
        if (a[0] != 3 || a[1] != 3) throw new AssertionError("example 1");
        int[] b = measure("(()");
        if (b[0] != -1 || b[1] != -1) throw new AssertionError("example 2");
        int[] c = measure("())");
        if (c[0] != -1) throw new AssertionError("a closing bracket with nothing open");
        int[] empty = measure("");
        if (empty[0] != 0 || empty[1] != 0) throw new AssertionError("empty string");
        String chain = "(".repeat(100000) + ")".repeat(100000);
        int[] big = measure(chain);
        if (big[0] != 100000 || big[1] != 100000) throw new AssertionError("a deep chain is handled without recursion");
        boolean overflowed = false;
        try { recursiveDepth(10_000_000); } catch (StackOverflowError expected) { overflowed = true; }
        if (!overflowed) throw new AssertionError("recursion on the nesting overflows the call stack");
        Random rnd = new Random(11603);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(rnd.nextBoolean() ? '(' : ')');
            String s = sb.toString();
            int[] got = measure(s);
            boolean valid = erasing(s);
            if (valid != (got[0] >= 0)) throw new AssertionError("validity differs on " + s);
            if (valid && got[1] != groupsByPairs(s)) throw new AssertionError("group count differs on " + s);
        }
    }
}
```

#### Solution: [Recognize] Score of Parentheses (LeetCode 856)
<!-- id: sq-score-of-parentheses -->

**Approach.** Keep a stack of saved totals and a current total. An opening bracket saves the current total and starts at zero. A closing bracket finishes a group whose inner total is the current value: an empty group is worth one, and any other is worth twice its inner total, so the group is worth the larger of two times the inner total and one. That value is added to the saved total, which becomes current. The assertions compare with the recursive definition that splits into top-level groups, and with the depth form, in which each empty pair contributes two to the power of its nesting depth.

**Complexity.** O(n) time and O(depth) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class ScoreOfParentheses {
    static long scoreStack(String s) {
        ArrayDeque<Long> saved = new ArrayDeque<>();
        long current = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') { saved.addLast(current); current = 0; }
            else current = saved.removeLast() + Math.max(2 * current, 1);
        }
        return current;
    }
    static long scoreRecursive(String s, int lo, int hi) {
        long total = 0;
        int i = lo;
        while (i < hi) {
            int bal = 0, j = i;
            do { bal += s.charAt(j) == '(' ? 1 : -1; j++; } while (bal > 0);
            long inner = scoreRecursive(s, i + 1, j - 1);
            total += inner == 0 ? 1 : 2 * inner;
            i = j;
        }
        return total;
    }
    static long scoreByDepth(String s) {
        long total = 0;
        int depth = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') depth++;
            else {
                depth--;
                if (s.charAt(i - 1) == '(') total += 1L << depth;
            }
        }
        return total;
    }
    static void build(Random rnd, StringBuilder sb, int depth) {
        int parts = rnd.nextInt(3);
        for (int p = 0; p < parts; p++) {
            sb.append('(');
            if (depth > 0) build(rnd, sb, depth - 1);
            sb.append(')');
        }
    }

    public static void main(String[] args) {
        if (scoreStack("(()(()))") != 6) throw new AssertionError("example 1");
        if (scoreStack("()()") != 2) throw new AssertionError("example 2");
        if (scoreStack("()") != 1) throw new AssertionError("an empty group is one");
        if (scoreStack("(())") != 2) throw new AssertionError("a group around an empty group");
        Random rnd = new Random(11604);
        for (int t = 0; t < 5000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 5);
            String s = sb.toString();
            if (s.isEmpty()) continue;
            long a = scoreStack(s);
            if (a != scoreRecursive(s, 0, s.length())) throw new AssertionError("recursion differs on " + s);
            if (a != scoreByDepth(s)) throw new AssertionError("depth form differs on " + s);
        }
    }
}
```
