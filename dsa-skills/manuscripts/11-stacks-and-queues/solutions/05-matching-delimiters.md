<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Bracket Matching

#### Solution: [Build] One Bracket Type (Author exercise)
<!-- id: sq-one-bracket-type -->

**Approach.**
The method pushes a marker for each `(` and pops one marker for each `)`. A `)` that finds the stack empty has no opening to close, so the method returns false at once. After the last character, any marker left on the stack is an opening without a closing, so the method answers true only when the stack is empty. At every step, the stack size equals the number of openings read and not yet closed. The harness also confirms that `pop()` on an empty `ArrayDeque` throws `NoSuchElementException`, which is why the emptiness test comes first.

**Complexity.**
- **Time** is O(n), because each character causes one push or one pop of constant cost.
- **Space** is O(n), because a text of only openings leaves n markers on the stack.

```java run
import java.util.ArrayDeque;
import java.util.NoSuchElementException;
import java.util.Random;

public final class OneBracketType {
    /**
     * Returns true when the string of parentheses is balanced.
     * Time: O(n), one push or pop per character.
     * Space: O(n), the stack can hold every opening.
     * Invariant: stack size equals the openings read and not yet closed.
     */
    static boolean balanced(String s) {
        ArrayDeque<Character> stack = new ArrayDeque<>();
        // One pass reads each character exactly once.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(') {
                // An opening waits on the stack until a closing reaches it.
                stack.push(c);
            } else {
                // A closing with an empty stack has no opening to match.
                if (stack.isEmpty()) return false;
                // The newest opening is the one this closing finishes.
                stack.pop();
            }
        }
        // Leftover openings mean some opening never closed.
        return stack.isEmpty();
    }

    /** Reference: delete adjacent pairs until the text stops changing. */
    static boolean oracle(String s) {
        // Each round removes every adjacent pair, and an unchanged text ends the loop.
        while (s.contains("()")) s = s.replace("()", "");
        return s.isEmpty();
    }

    public static void main(String[] args) {
        // Examples: a nested balanced text and the equal-count text with the wrong order.
        if (!balanced("(()())")) throw new AssertionError("example 1");
        if (balanced(")(")) throw new AssertionError("example 2");
        // The empty string is balanced.
        if (!balanced("")) throw new AssertionError("empty");
        // Java claim: pop on an empty ArrayDeque throws, and peek returns null.
        boolean threw = false;
        try { new ArrayDeque<Character>().pop(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("pop on empty");
        if (new ArrayDeque<Character>().peek() != null) throw new AssertionError("peek on empty");
        // Random strings agree with the deletion reference, and both outcomes occur.
        Random rnd = new Random(11);
        int yes = 0, no = 0;
        for (int t = 0; t < 6000; t++) {
            StringBuilder sb = new StringBuilder();
            int len = rnd.nextInt(13);
            for (int k = 0; k < len; k++) sb.append(rnd.nextBoolean() ? '(' : ')');
            String s = sb.toString();
            if (balanced(s) != oracle(s)) throw new AssertionError("random " + s);
            if (balanced(s)) yes++; else no++;
        }
        if (yes == 0 || no == 0) throw new AssertionError("coverage");
    }
}
```

#### Solution: [Vary] Three Delimiter Types (LeetCode 20)
<!-- id: sq-three-delimiter-types -->

**Approach.**
The stack now stores the opening characters themselves. Each closing symbol pops the newest opening and the method compares it with the partner of the closing symbol. An empty stack or a different partner makes the text invalid. The invariant is that the stack holds the pending openings in nesting order, newest on top. The harness confirms that two boxed `Character` values from `valueOf` compare equal with `equals` and that the method compares primitive `char` values, which avoids identity comparison of objects.

**Complexity.**
- **Time** is O(n), because each character causes at most one push or pop.
- **Space** is O(n), because the stack can hold all openings of a text such as `((((`.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class ThreeDelimiterTypes {
    /**
     * Returns true when all delimiters pair by type and close in reverse order.
     * Time: O(n), one push or pop per character.
     * Space: O(n), the stack can hold every opening.
     * Invariant: the stack holds the pending openings, newest on top.
     */
    static boolean valid(String s) {
        ArrayDeque<Character> stack = new ArrayDeque<>();
        // Each character is classified once.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(' || c == '[' || c == '{') {
                // Openings become pending.
                stack.push(c);
            } else {
                // A closing needs a pending opening to exist.
                if (stack.isEmpty()) return false;
                // Unboxing to char makes the comparison one of values.
                char open = stack.pop();
                // The popped opening must be the partner of this closing.
                if (open != partner(c)) return false;
            }
        }
        // The text is valid only when no opening stays pending.
        return stack.isEmpty();
    }

    /** Returns the opening symbol for a closing symbol. Time O(1), space O(1). */
    static char partner(char close) {
        // Each closing has exactly one partner.
        if (close == ')') return '(';
        if (close == ']') return '[';
        return '{';
    }

    /** Reference: delete adjacent matched pairs until the text stops changing. */
    static boolean oracle(String s) {
        String t;
        // The loop ends when a full round removes nothing.
        do {
            t = s;
            s = s.replace("()", "").replace("[]", "").replace("{}", "");
        } while (!s.equals(t));
        return s.isEmpty();
    }

    /** Builds a random valid text by wrapping and concatenating. */
    static String randomValid(Random rnd, int depth) {
        String[] o = {"(", "[", "{"}, c = {")", "]", "}"};
        StringBuilder sb = new StringBuilder();
        // Each group wraps a smaller valid text.
        for (int g = rnd.nextInt(3); g > 0; g--) {
            int k = rnd.nextInt(3);
            sb.append(o[k]).append(depth > 0 ? randomValid(rnd, depth - 1) : "").append(c[k]);
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // Examples: nested valid text and the wrong-type text.
        if (!valid("{[()]}[]")) throw new AssertionError("example 1");
        if (valid("{[}]")) throw new AssertionError("example 2");
        // Equal counts with the wrong order are rejected.
        if (valid("([)]")) throw new AssertionError("order");
        // Java claim: two boxed characters from the same char are equals.
        if (!Character.valueOf('(').equals(Character.valueOf('('))) throw new AssertionError("boxing");
        // Random texts agree with the reference, and valid texts are generated on purpose.
        Random rnd = new Random(12);
        String sym = "()[]{}";
        int yes = 0;
        for (int t = 0; t < 6000; t++) {
            String s;
            if (t % 2 == 0) {
                StringBuilder sb = new StringBuilder();
                for (int k = rnd.nextInt(11); k > 0; k--) sb.append(sym.charAt(rnd.nextInt(6)));
                s = sb.toString();
            } else {
                s = randomValid(rnd, 3);
                // Flip one character in half of the valid texts to create near misses.
                if (!s.isEmpty() && rnd.nextBoolean()) {
                    int p = rnd.nextInt(s.length());
                    s = s.substring(0, p) + sym.charAt(rnd.nextInt(6)) + s.substring(p + 1);
                }
            }
            if (valid(s) != oracle(s)) throw new AssertionError("random " + s);
            if (valid(s)) yes++;
        }
        if (yes < 500) throw new AssertionError("coverage");
    }
}
```

#### Solution: [Boundary] Premature Close And Leftover Open (Author exercise)
<!-- id: sq-premature-close-leftover -->

**Approach.**
The stack stores the index of each opening, so a failure can report a position. A closing symbol at index `i` fails when the stack is empty or when the character at the popped index is not its partner, and the method returns `i` at the first such failure. A failure before the end of the text is always the first closing that cannot be matched, because all earlier characters were consistent. When the scan ends without failure, the stack top is the newest pending opening, and the method returns its index. An empty stack means the text is valid, so the method gives -1 as the sentinel. Throughout the scan, the stack holds the indices of the pending openings, increasing from bottom to top.

**Complexity.**
- **Time** is O(n), because each character causes at most one push or pop.
- **Space** is O(n), because the stack can hold an index for every character.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class FirstBracketError {
    /**
     * Returns -1 for a valid text, else the first unmatched closing index,
     * else the index of the newest pending opening.
     * Time: O(n), one push or pop per character.
     * Space: O(n), indices of pending openings.
     * Invariant: the stack holds increasing indices of pending openings.
     */
    static int firstError(String s) {
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        // The scan stops at the first closing that cannot be matched.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(' || c == '[' || c == '{') {
                // Storing the index lets a leftover opening report its position.
                stack.push(i);
            } else {
                // A closing with no pending opening is the premature close.
                if (stack.isEmpty()) return i;
                // The popped index points at the newest pending opening.
                int open = stack.pop();
                // A different partner means this closing cannot be matched.
                if (s.charAt(open) != partner(c)) return i;
            }
        }
        // After the scan, the newest pending opening is the stack top; empty means valid.
        return stack.isEmpty() ? -1 : stack.peek();
    }

    /** Returns the opening symbol for a closing symbol. Time O(1), space O(1). */
    static char partner(char close) {
        // Each closing has exactly one partner.
        return close == ')' ? '(' : close == ']' ? '[' : '{';
    }

    /** Reference: reduce every prefix by deleting adjacent pairs, tracking indices. */
    static int oracle(String s) {
        // Grow the prefix one character at a time.
        for (int p = 1; p <= s.length(); p++) {
            List<Integer> idx = new ArrayList<>();
            for (int k = 0; k < p; k++) idx.add(k);
            boolean changed = true;
            // Delete adjacent matched pairs until none remain.
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
            // A closing symbol left in the reduced prefix is the first failure.
            for (int k : idx) if (")]}".indexOf(s.charAt(k)) >= 0) return k;
        }
        // Only openings can remain; report the newest one, or -1 when nothing remains.
        List<Integer> idx = new ArrayList<>();
        for (int k = 0; k < s.length(); k++) idx.add(k);
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
        return idx.isEmpty() ? -1 : idx.get(idx.size() - 1);
    }

    public static void main(String[] args) {
        // Example 1: the second closing parenthesis finds an empty stack.
        if (firstError("())(") != 2) throw new AssertionError("example 1");
        // Example 2: the opening at index 1 is newest and still pending.
        if (firstError("[(()") != 1) throw new AssertionError("example 2");
        // A wrong-order closing is reported at the closing, and a valid text gives -1.
        if (firstError("([)]") != 2) throw new AssertionError("order");
        if (firstError("") != -1 || firstError("{[]}") != -1) throw new AssertionError("valid");
        // Random texts agree with the prefix-reduction reference.
        Random rnd = new Random(13);
        String sym = "()[]{}";
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int k = rnd.nextInt(10); k > 0; k--) sb.append(sym.charAt(rnd.nextInt(6)));
            String s = sb.toString();
            if (firstError(s) != oracle(s)) throw new AssertionError("random " + s);
        }
    }
}
```

#### Solution: [Recognize] Remove Outermost Parentheses (LeetCode 1021)
<!-- id: sq-remove-outermost -->

**Approach.**
A primitive piece starts at a `(` that has depth 0 before it and ends at the `)` that returns the depth to 0. The method keeps only the depth, which is the stack size of the earlier scan, because the content of the stack is always the same symbol. For a `(`, the method appends it only when the depth is already above 0, and then raises the depth. For a `)`, the method lowers the depth first and appends it only when the depth is still above 0. The invariant is that the depth equals the number of pending openings before the current character.

**Complexity.**
- **Time** is O(n), because the method reads each character once and appends in O(1) amortized time.
- **Space** is O(n), because the result can hold almost every input character.

```java run
import java.util.Random;

public final class RemoveOutermost {
    /**
     * Removes the first opening and last closing of each primitive piece.
     * Time: O(n), one pass with amortized O(1) appends.
     * Space: O(n) for the result.
     * Invariant: depth is the number of pending openings before the character.
     */
    static String strip(String s) {
        StringBuilder out = new StringBuilder();
        int depth = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                // An opening at depth 0 starts a piece and is dropped.
                if (depth > 0) out.append('(');
                depth++;
            } else {
                // Lower the depth first so the piece's last closing sees depth 0.
                depth--;
                // A closing that returns to depth 0 ends a piece and is dropped.
                if (depth > 0) out.append(')');
            }
        }
        return out.toString();
    }

    /** Reference: cut the text at each balance of zero and trim every piece. */
    static String oracle(String s) {
        StringBuilder out = new StringBuilder();
        int balance = 0, start = 0;
        // The balance returns to zero exactly at the end of each primitive piece.
        for (int i = 0; i < s.length(); i++) {
            balance += s.charAt(i) == '(' ? 1 : -1;
            if (balance == 0) {
                out.append(s, start + 1, i);
                start = i + 1;
            }
        }
        return out.toString();
    }

    /** Builds a random balanced text. */
    static String randomBalanced(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        // Each group wraps a smaller balanced text.
        for (int g = rnd.nextInt(4); g > 0; g--) sb.append('(').append(depth > 0 ? randomBalanced(rnd, depth - 1) : "").append(')');
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1: three pieces of different depth.
        if (!strip("((()))()(())").equals("(())()")) throw new AssertionError("example 1");
        // Example 2: pieces of length two vanish completely.
        if (!strip("()()").isEmpty()) throw new AssertionError("example 2");
        // The empty string stays empty.
        if (!strip("").isEmpty()) throw new AssertionError("empty");
        // Random balanced texts agree with the balance-cut reference.
        Random rnd = new Random(14);
        for (int t = 0; t < 5000; t++) {
            String s = randomBalanced(rnd, 4);
            if (!strip(s).equals(oracle(s))) throw new AssertionError("random " + s);
            // The result is itself balanced.
            int b = 0;
            for (char c : strip(s).toCharArray()) { b += c == '(' ? 1 : -1; if (b < 0) throw new AssertionError("prefix"); }
            if (b != 0) throw new AssertionError("balanced");
        }
    }
}
```
