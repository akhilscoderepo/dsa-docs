<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Nested Groups

#### Solution: [Build] Maximum Parenthesis Depth (Author exercise)
<!-- id: sq-max-nesting-depth -->

**Approach.**
The method pushes one marker for each `(` and pops one for each `)`. Right after each push, the stack size equals the depth of that `(`, so the method keeps the largest size it has seen. The invariant is that the stack size equals the number of groups that are open at the current position.

**Complexity.**
- **Time** is O(n), because each character causes one push or one pop.
- **Space** is O(d) for depth d, because the stack never holds more markers than the number of open groups.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class MaxNestingDepth {
    /**
     * Returns the largest number of groups open at one time.
     * Time: O(n), one push or pop per character.
     * Space: O(d) for the deepest nesting d.
     * Invariant: stack size equals the open groups at the current index.
     */
    static int maxDepth(String s) {
        ArrayDeque<Character> open = new ArrayDeque<>();
        int best = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                // A push opens a level, and the new size is the depth of this character.
                open.push('(');
                best = Math.max(best, open.size());
            } else {
                // A pop closes the innermost level.
                open.pop();
            }
        }
        return best;
    }

    /** Reference: the largest prefix balance, computed for every prefix separately. */
    static int oracle(String s) {
        int best = 0;
        // Each prefix is counted from scratch.
        for (int p = 1; p <= s.length(); p++) {
            int bal = 0;
            for (int k = 0; k < p; k++) bal += s.charAt(k) == '(' ? 1 : -1;
            best = Math.max(best, bal);
        }
        return best;
    }

    /** Builds a random balanced text. */
    static String randomBalanced(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        // Each group wraps a smaller balanced text.
        for (int g = rnd.nextInt(4); g > 0; g--) sb.append('(').append(depth > 0 ? randomBalanced(rnd, depth - 1) : "").append(')');
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1 has an inner pair two levels below the outer group.
        if (maxDepth("(()(()))") != 3) throw new AssertionError("example 1");
        // Example 2 has no group inside another.
        if (maxDepth("()()()") != 1) throw new AssertionError("example 2");
        // The empty string has depth 0.
        if (maxDepth("") != 0) throw new AssertionError("empty");
        // Random balanced texts agree with the prefix-balance reference.
        Random rnd = new Random(21);
        for (int t = 0; t < 4000; t++) {
            String s = randomBalanced(rnd, 5);
            if (maxDepth(s) != oracle(s)) throw new AssertionError("random " + s);
        }
    }
}
```

#### Solution: [Vary] Sum Values By Nested Group (Author exercise)
<!-- id: sq-inclusive-group-totals -->

**Approach.**
The method keeps `cur`, the total of the innermost open group, and a stack of the totals of the outer groups. A `(` pushes `cur` and starts a new total at 0. A digit adds to `cur`. A `)` records `cur` as the answer for that group and pops the saved total of the parent. Because the contract counts nested digits, the method adds the closed group's total to the restored value before it continues. The invariant is that `cur` is the total so far of the innermost open group and the stack holds the totals so far of every group around it.

**Complexity.**
- **Time** is O(n), because each character causes a constant amount of work.
- **Space** is O(d + g), because the stack holds one integer per open level and the result holds one integer per group.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class InclusiveGroupTotals {
    /**
     * Returns the digit total of each group, nested digits included, in closing order.
     * Time: O(n), constant work per character.
     * Space: O(d + g) for the stack and the result.
     * Invariant: cur is the total so far of the innermost open group.
     */
    static int[] totals(String s) {
        ArrayDeque<Integer> saved = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        int cur = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(') {
                // Save the total of the level around this group and start at zero.
                saved.push(cur);
                cur = 0;
            } else if (c == ')') {
                // The group is complete, so its total is final.
                out.add(cur);
                // Restore the saved total and add this group's digits to it.
                cur = saved.pop() + cur;
            } else {
                // A digit belongs to the innermost open group.
                cur += c - '0';
            }
        }
        int[] r = new int[out.size()];
        for (int g = 0; g < r.length; g++) r[g] = out.get(g);
        return r;
    }

    /** Reference: find each group's matching close by counting, then add its digits directly. */
    static int[] oracle(String s) {
        List<Integer> out = new ArrayList<>();
        // The closing parentheses appear in this order, so each one defines a group.
        for (int j = 0; j < s.length(); j++) {
            if (s.charAt(j) != ')') continue;
            // Walk left until the balance shows the matching opening.
            int bal = 0, i = j;
            while (true) {
                bal += s.charAt(i) == ')' ? 1 : s.charAt(i) == '(' ? -1 : 0;
                if (bal == 0) break;
                i--;
            }
            int sum = 0;
            for (int k = i + 1; k < j; k++) if (Character.isDigit(s.charAt(k))) sum += s.charAt(k) - '0';
            out.add(sum);
        }
        int[] r = new int[out.size()];
        for (int g = 0; g < r.length; g++) r[g] = out.get(g);
        return r;
    }

    /** Builds a random balanced text with digits. */
    static String randomText(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        // Each round adds a digit or a group.
        for (int g = rnd.nextInt(5); g > 0; g--) {
            if (rnd.nextInt(3) == 0 || depth == 0) sb.append(rnd.nextInt(10));
            else sb.append('(').append(randomText(rnd, depth - 1)).append(')');
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1: the outer total includes the inner 2 and 9.
        if (!java.util.Arrays.equals(totals("(1(29)4)"), new int[] {11, 16})) throw new AssertionError("example 1");
        // Example 2: digits outside every group appear in no total.
        if (!java.util.Arrays.equals(totals("7(3)(48)2"), new int[] {3, 12})) throw new AssertionError("example 2");
        // A text without a group gives an empty result.
        if (totals("123").length != 0) throw new AssertionError("no group");
        // Random texts agree with the reference.
        Random rnd = new Random(22);
        for (int t = 0; t < 4000; t++) {
            String s = randomText(rnd, 4);
            if (!java.util.Arrays.equals(totals(s), oracle(s))) throw new AssertionError("random " + s);
        }
    }
}
```

#### Solution: [Boundary] Deep Single Chain (Author exercise)
<!-- id: sq-deep-single-chain -->

**Approach.**
Each level keeps the greatest height among the groups that closed directly inside it. A `(` pushes that value for the level around it and starts a new level at 0. A `)` on an empty stack means a close without an open, so the method returns -1. Otherwise the closing group has height `cur + 1`, and the method restores the saved value and keeps the larger of the two. A nonempty stack at the end means an unclosed group, so the method returns -1. The invariant is that `cur` is the greatest height among closed groups directly inside the innermost open group. An empty group closes with `cur = 0` and has height 1.

**Complexity.**
- **Time** is O(n), because each character causes at most one push or pop.
- **Space** is O(d), because the stack holds one integer per open group.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class DeepSingleChain {
    /**
     * Returns the height of a balanced string, or -1 when it is not balanced.
     * Time: O(n), one push or pop per character.
     * Space: O(d) for the deepest nesting d.
     * Invariant: cur is the greatest height of groups closed inside the innermost open group.
     */
    static int height(String s) {
        ArrayDeque<Integer> saved = new ArrayDeque<>();
        int cur = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                // Save the level around this group and start a new level.
                saved.push(cur);
                cur = 0;
            } else {
                // A close with no open group makes the text invalid.
                if (saved.isEmpty()) return -1;
                // The closed group is one taller than its tallest inner group.
                cur = Math.max(saved.pop(), cur + 1);
            }
        }
        // Groups still open at the end make the text invalid.
        return saved.isEmpty() ? cur : -1;
    }

    /** Reference: remove all non-overlapping "()" pairs in rounds; the round count is the height. */
    static int oracle(String s) {
        int rounds = 0;
        // Each round peels the innermost groups.
        while (s.contains("()")) {
            s = s.replace("()", "");
            rounds++;
        }
        return s.isEmpty() ? rounds : -1;
    }

    public static void main(String[] args) {
        // Example 1: five nested empty-bodied groups.
        if (height("((((()))))") != 5) throw new AssertionError("example 1");
        // Example 2: a close before any open.
        if (height(")(") != -1) throw new AssertionError("example 2");
        // Empty input has height 0, and unclosed input is rejected.
        if (height("") != 0 || height("(()") != -1) throw new AssertionError("edges");
        // A long chain keeps the explicit stack off the call stack.
        StringBuilder deep = new StringBuilder();
        for (int k = 0; k < 100000 / 2; k++) deep.append('(');
        for (int k = 0; k < 100000 / 2; k++) deep.append(')');
        if (height(deep.toString()) != 50000) throw new AssertionError("deep chain");
        // Random strings agree with the round-count reference, valid or not.
        Random rnd = new Random(23);
        int valid = 0;
        for (int t = 0; t < 8000; t++) {
            StringBuilder sb = new StringBuilder();
            for (int k = rnd.nextInt(13); k > 0; k--) sb.append(rnd.nextBoolean() ? '(' : ')');
            String s = sb.toString();
            if (height(s) != oracle(s)) throw new AssertionError("random " + s);
            if (height(s) >= 0) valid++;
        }
        if (valid < 100) throw new AssertionError("coverage");
    }
}
```

#### Solution: [Recognize] Score Of Parentheses (LeetCode 856)
<!-- id: sq-score-of-parentheses -->

**Approach.**
Each open level holds the score of the groups that already closed directly inside it. A `(` pushes the current score and starts a level at 0. A `)` closes the level. An empty level scores 1, and a level with inner score `v` scores `2 * v`, so the closed level is worth `max(2 * cur, 1)`. The method pops the saved score of the parent and adds the closed level's value to it, which sums the siblings. The invariant is that `cur` is the sum of the scores of the groups closed directly inside the innermost open group.

**Complexity.**
- **Time** is O(n), because each character causes one push or one pop.
- **Space** is O(d), because the stack holds one integer per open group.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class ScoreOfParentheses {
    /**
     * Returns the score of a balanced string under the three scoring rules.
     * Time: O(n), one push or pop per character.
     * Space: O(d) for the deepest nesting d.
     * Invariant: cur is the sum of scores of groups closed directly inside the open group.
     */
    static int score(String s) {
        ArrayDeque<Integer> saved = new ArrayDeque<>();
        int cur = 0;
        // One pass reads each character once.
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                // Save the sibling sum of the level around this group.
                saved.push(cur);
                cur = 0;
            } else {
                // An empty group is worth 1, and a filled group doubles its inner score.
                int value = Math.max(2 * cur, 1);
                // Restore the saved sum and add this group as one more sibling.
                cur = saved.pop() + value;
            }
        }
        return cur;
    }

    /** Reference: apply the three rules by direct recursion on substrings. */
    static int oracle(String s) {
        // The empty string is the neutral element of concatenation.
        if (s.isEmpty()) return 0;
        // Find the end of the first primitive piece by balance.
        int bal = 0, end = 0;
        for (int i = 0; i < s.length(); i++) {
            bal += s.charAt(i) == '(' ? 1 : -1;
            if (bal == 0) { end = i; break; }
        }
        String inner = s.substring(1, end);
        // Rule 1 for "()", rule 3 for a nonempty inner string.
        int first = inner.isEmpty() ? 1 : 2 * oracle(inner);
        // Rule 2 adds the score of the remaining pieces.
        return first + oracle(s.substring(end + 1));
    }

    /** Builds a random balanced text. */
    static String randomBalanced(Random rnd, int depth) {
        StringBuilder sb = new StringBuilder();
        // Each group wraps a smaller balanced text.
        for (int g = rnd.nextInt(4); g > 0; g--) sb.append('(').append(depth > 0 ? randomBalanced(rnd, depth - 1) : "").append(')');
        return sb.toString();
    }

    public static void main(String[] args) {
        // Example 1: 2 * (2 * (1 + 1)).
        if (score("((()()))") != 8) throw new AssertionError("example 1");
        // Example 2: 1 + 2 + 1.
        if (score("()(())()") != 4) throw new AssertionError("example 2");
        // The basic pair scores 1.
        if (score("()") != 1) throw new AssertionError("pair");
        // Random balanced texts agree with the recursive reference.
        Random rnd = new Random(24);
        for (int t = 0; t < 4000; t++) {
            String s = randomBalanced(rnd, 4);
            if (s.isEmpty()) continue;
            if (score(s) != oracle(s)) throw new AssertionError("random " + s);
        }
    }
}
```
