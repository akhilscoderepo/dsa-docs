<!-- solutions-for: 05-matching-delimiters -->
### Matching Delimiters

#### Solution: [Build] One Bracket Type (Author exercise)
<!-- id: sq-one-bracket-type -->

**Approach.** Push a marker for each opening bracket and, for each closing bracket, remove one marker, rejecting the text when the stack is empty. The text is accepted if the stack is empty at the end. With one kind of bracket the stack content carries no information beyond its size, so a counter would give the same answer, and the assertions confirm that the stack version agrees with a counter that is never allowed to go negative. They also compare with the erase-and-repeat method on random strings and show that `)(` has equal counts but is rejected.

**Complexity.** O(n) time and O(n) space for the stack.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class OneBracketType {
    static boolean valid(String s) {
        ArrayDeque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') stack.addLast('(');
            else {
                if (stack.isEmpty()) return false;
                stack.removeLast();
            }
        }
        return stack.isEmpty();
    }
    static boolean counter(String s) {
        int depth = 0;
        for (int i = 0; i < s.length(); i++) {
            depth += s.charAt(i) == '(' ? 1 : -1;
            if (depth < 0) return false;
        }
        return depth == 0;
    }
    static boolean erasing(String s) {
        String cur = s;
        while (cur.contains("()")) cur = cur.replace("()", "");
        return cur.isEmpty();
    }

    public static void main(String[] args) {
        if (!valid("(()())")) throw new AssertionError("example 1");
        if (valid("())(")) throw new AssertionError("example 2");
        if (valid(")(")) throw new AssertionError("equal counts do not prove a valid order");
        if (!valid("")) throw new AssertionError("the empty string is valid");
        ArrayDeque<Character> empty = new ArrayDeque<>();
        try { empty.removeLast(); throw new AssertionError("removeLast on empty must throw"); } catch (java.util.NoSuchElementException expected) { }
        Random rnd = new Random(11501);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(14);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(rnd.nextBoolean() ? '(' : ')');
            String s = sb.toString();
            if (valid(s) != erasing(s)) throw new AssertionError("differs from erasing on " + s);
            if (valid(s) != counter(s)) throw new AssertionError("differs from the counter on " + s);
        }
    }
}
```

#### Solution: [Vary] Valid Parentheses (LeetCode 20)
<!-- id: sq-valid-parentheses -->

**Approach.** Push each opening character. For a closing character, require a nonempty stack and require the removed top to equal the partner of the closing character; otherwise return false. Accept only if the stack is empty at the end. The partner lookup is the one new piece compared with a single bracket kind. The assertions compare with the erase-and-repeat method on random strings over all six characters, and check the crossed case `([)]`, which has a matching count of each kind and is invalid.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class ValidParentheses {
    static char partner(char closing) { return closing == ')' ? '(' : closing == ']' ? '[' : '{'; }
    static boolean valid(String s) {
        ArrayDeque<Character> open = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(' || c == '[' || c == '{') open.addLast(c);
            else if (open.isEmpty() || open.removeLast() != partner(c)) return false;
        }
        return open.isEmpty();
    }
    static boolean erasing(String s) {
        String cur = s;
        while (true) {
            String next = cur.replace("()", "").replace("[]", "").replace("{}", "");
            if (next.length() == cur.length()) break;
            cur = next;
        }
        return cur.isEmpty();
    }

    public static void main(String[] args) {
        if (!valid("{[()]}")) throw new AssertionError("example 1");
        if (valid("([)]")) throw new AssertionError("example 2");
        if (valid("(]")) throw new AssertionError("one pair of the wrong kind");
        if (valid("]")) throw new AssertionError("a closing with nothing open");
        if (!valid("()[]{}")) throw new AssertionError("side by side pairs");
        String chars = "()[]{}";
        Random rnd = new Random(11502);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(chars.charAt(rnd.nextInt(6)));
            String s = sb.toString();
            if (valid(s) != erasing(s)) throw new AssertionError("differs on " + s);
        }
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            buildBalanced(rnd, sb, 3);
            if (!valid(sb.toString())) throw new AssertionError("a built balanced string must pass: " + sb);
        }
    }
    static void buildBalanced(Random rnd, StringBuilder sb, int depth) {
        int parts = rnd.nextInt(3);
        for (int p = 0; p < parts; p++) {
            int k = rnd.nextInt(3);
            sb.append("([{".charAt(k));
            if (depth > 0) buildBalanced(rnd, sb, depth - 1);
            sb.append(")]}".charAt(k));
        }
    }
}
```

#### Solution: [Boundary] Premature Close And Leftover Open (Author exercise)
<!-- id: sq-premature-close-leftover -->

**Approach.** Store the positions of openings on the stack. When a closing finds the stack empty or its top has the wrong kind, return that closing's index. After the scan, if the stack is nonempty, the earliest leftover opening is the bottom of the stack, which is its first element, and its index is the answer. Otherwise return -1. The assertions compare with an index-tracking erase method: repeatedly delete adjacent matched pairs from a list of positions, then read the first remaining closer, or else the first remaining opener, and the first example `())` shows a failure during the scan while the second shows a leftover.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class PrematureCloseLeftover {
    static char partner(char closing) { return closing == ')' ? '(' : closing == ']' ? '[' : '{'; }
    static int firstProblem(String s) {
        ArrayDeque<Integer> open = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(' || c == '[' || c == '{') open.addLast(i);
            else if (open.isEmpty() || s.charAt(open.removeLast()) != partner(c)) return i;
        }
        return open.isEmpty() ? -1 : open.peekFirst();
    }
    static int viaErasing(String s) {
        int n = s.length();
        for (int end = 1; end <= n; end++) {
            List<Integer> idx = reduce(s, end);
            for (int k : idx) {
                char c = s.charAt(k);
                if (c == ')' || c == ']' || c == '}') return firstCloserIn(s, end);
            }
        }
        List<Integer> all = reduce(s, n);
        return all.isEmpty() ? -1 : all.get(0);
    }
    static int firstCloserIn(String s, int end) {
        for (int e = 1; e <= end; e++) {
            for (int k : reduce(s, e)) if (")]}".indexOf(s.charAt(k)) >= 0) return k;
        }
        return -2;
    }
    static List<Integer> reduce(String s, int end) {
        List<Integer> idx = new ArrayList<>();
        for (int i = 0; i < end; i++) idx.add(i);
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int k = 0; k + 1 < idx.size(); k++) {
                char a = s.charAt(idx.get(k)), b = s.charAt(idx.get(k + 1));
                if ((a == '(' && b == ')') || (a == '[' && b == ']') || (a == '{' && b == '}')) {
                    idx.remove(k + 1);
                    idx.remove(k);
                    changed = true;
                    break;
                }
            }
        }
        return idx;
    }

    public static void main(String[] args) {
        if (firstProblem("())") != 2) throw new AssertionError("example 1");
        if (firstProblem("(([]") != 0) throw new AssertionError("example 2");
        if (firstProblem("") != -1) throw new AssertionError("empty is balanced");
        if (firstProblem("([)]") != 2) throw new AssertionError("the crossed closing");
        if (firstProblem("{}[") != 2) throw new AssertionError("a leftover opening at the end");
        String chars = "()[]{}";
        Random rnd = new Random(11503);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(10);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append(chars.charAt(rnd.nextInt(6)));
            String s = sb.toString();
            if (firstProblem(s) != viaErasing(s)) throw new AssertionError("differs on " + s + ": " + firstProblem(s) + " vs " + viaErasing(s));
        }
    }
}
```

#### Solution: [Recognize] Remove Outermost Parentheses (LeetCode 1021)
<!-- id: sq-remove-outermost -->

**Approach.** Only the nesting depth matters. Decrease the depth before testing a closing parenthesis and increase it after testing an opening one, and keep a character exactly when the depth at that moment is positive. A group's first opening is seen at depth zero and its last closing leaves depth zero, so both are dropped. This replaces the stack by a counter, since nothing but its height is read. The assertions compare with a stack of indices that records matched pairs and drops the pairs whose opening was pushed on an empty stack, and with a split into primitives by a running balance.

**Complexity.** O(n) time and O(n) space for the output.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class RemoveOutermost {
    static String removeOutermost(String s) {
        StringBuilder out = new StringBuilder();
        int depth = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == ')') depth--;
            if (depth > 0) out.append(c);
            if (c == '(') depth++;
        }
        return out.toString();
    }
    static String viaStack(String s) {
        boolean[] drop = new boolean[s.length()];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                if (stack.isEmpty()) drop[i] = true;
                stack.addLast(i);
            } else {
                int open = stack.removeLast();
                if (stack.isEmpty()) { drop[open] = true; drop[i] = true; }
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) if (!drop[i]) sb.append(s.charAt(i));
        return sb.toString();
    }
    static String viaPrimitives(String s) {
        StringBuilder sb = new StringBuilder();
        int balance = 0, start = 0;
        for (int i = 0; i < s.length(); i++) {
            balance += s.charAt(i) == '(' ? 1 : -1;
            if (balance == 0) { sb.append(s, start + 1, i); start = i + 1; }
        }
        return sb.toString();
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
        if (!removeOutermost("(()())(())").equals("()()()")) throw new AssertionError("example 1");
        if (!removeOutermost("()()").equals("")) throw new AssertionError("example 2");
        if (!removeOutermost("((()))").equals("(())")) throw new AssertionError("one deep group");
        Random rnd = new Random(11504);
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            build(rnd, sb, 4);
            if (sb.length() == 0) continue;
            String s = sb.toString();
            String got = removeOutermost(s);
            if (!got.equals(viaStack(s))) throw new AssertionError("differs from the stack on " + s);
            if (!got.equals(viaPrimitives(s))) throw new AssertionError("differs from the primitives on " + s);
        }
    }
}
```
