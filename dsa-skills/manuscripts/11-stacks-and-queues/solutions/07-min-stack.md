<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Tracking The Minimum

#### Solution: [Build] Value-Min Pairs (Author exercise)
<!-- id: sq-value-min-pairs -->

**Approach.**
Each stack entry holds a value and the smallest value at or below its position. A push computes that smallest value from the new value and the entry below, so the result is fixed at push time. A pop discards an entry together with its answer, and the entry underneath still holds the correct answer for the values that remain. The invariant is that every entry's second field equals the minimum of the values from the bottom up to that entry. The read operations return one field of the top entry.

**Complexity.**
- **Time** is O(n) for n operations, because each operation touches only the top entry.
- **Space** is O(n), because every pushed value stores two integers.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ValueMinPairs {
    /**
     * Runs the operations and returns the results of the top and minimum reads.
     * Time: O(n), constant work per operation.
     * Space: O(n), one pair per stored value.
     * Invariant: entry[1] is the minimum of all values at or below that entry.
     */
    static int[] run(int[][] ops) {
        // Each entry is {value, minimum at or below this entry}.
        ArrayDeque<int[]> entries = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        // One pass handles every operation in input order.
        for (int[] op : ops) {
            if (op[0] == 0) {
                // The new minimum is the smaller of the value and the entry below.
                int lowest = entries.isEmpty() ? op[1] : Math.min(op[1], entries.peek()[1]);
                entries.push(new int[] {op[1], lowest});
            } else if (op[0] == 1) {
                // Removing an entry also removes its stored answer.
                entries.pop();
            } else if (op[0] == 2) {
                out.add(entries.peek()[0]);
            } else {
                // The minimum is read from the top entry without a scan.
                out.add(entries.peek()[1]);
            }
        }
        int[] res = new int[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    /** Reference: keep a plain list and scan it for every minimum read. */
    static int[] oracle(int[][] ops) {
        List<Integer> list = new ArrayList<>();
        List<Integer> out = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 0) list.add(op[1]);
            else if (op[0] == 1) list.remove(list.size() - 1);
            else if (op[0] == 2) out.add(list.get(list.size() - 1));
            else {
                int best = Integer.MAX_VALUE;
                for (int v : list) best = Math.min(best, v);
                out.add(best);
            }
        }
        int[] res = new int[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        int[][] e1 = {{0, 5}, {0, 3}, {0, 7}, {3}, {1}, {1}, {3}, {2}};
        if (!Arrays.equals(run(e1), new int[] {3, 5, 5})) throw new AssertionError("example 1");
        int[][] e2 = {{0, 4}, {0, 9}, {0, 2}, {3}, {1}, {3}, {2}};
        if (!Arrays.equals(run(e2), new int[] {2, 4, 9})) throw new AssertionError("example 2");
        // Random valid sequences agree with the scanning reference.
        Random rnd = new Random(1107);
        for (int t = 0; t < 3000; t++) {
            List<int[]> ops = new ArrayList<>();
            int size = 0;
            int n = 1 + rnd.nextInt(30);
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(4);
                // Reads and pops are legal only on a non-empty stack, so an empty stack forces a push.
                if (size == 0 || pick == 0) { ops.add(new int[] {0, rnd.nextInt(11) - 5}); size++; }
                else if (pick == 1) { ops.add(new int[] {1}); size--; }
                else ops.add(new int[] {pick});
            }
            int[][] arr = ops.toArray(new int[0][]);
            if (!Arrays.equals(run(arr), oracle(arr))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Two-Stack Minimum (Author exercise)
<!-- id: sq-two-stack-minimum -->

**Approach.**
The method keeps a main stack and a second stack of minimum levels. A push enters the second stack when the stack is empty or the value is at most the second stack's top. A pop leaves the second stack when the popped value equals its top. The invariant is that the second stack's top equals the minimum of the main stack. After the last operation, the method returns the second stack's size. The comparison with equality keeps one entry for each copy of the minimum, so popping one copy never removes the answer for the others.

**Complexity.**
- **Time** is O(n) for n operations, because each operation does one comparison and at most one push or pop on the second stack.
- **Space** is O(n), because the second stack holds at most one entry per pushed value, and it holds fewer entries when values arrive in increasing order.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class TwoStackMinimum {
    /**
     * Returns the final size of the second stack.
     * Time: O(n), constant work per operation.
     * Space: O(n), both stacks hold at most n entries.
     * Invariant: the second stack's top equals the minimum of the main stack.
     */
    static int run(int[][] ops) {
        ArrayDeque<Integer> main = new ArrayDeque<>();
        ArrayDeque<Integer> mins = new ArrayDeque<>();
        for (int[] op : ops) {
            if (op[0] == 0) {
                main.push(op[1]);
                // Less than or equal keeps a separate entry for each copy of the minimum.
                if (mins.isEmpty() || op[1] <= mins.peek()) mins.push(op[1]);
            } else {
                int v = main.pop();
                // The unboxed int on the left makes this a numeric comparison.
                if (v == mins.peek()) mins.pop();
            }
        }
        return mins.size();
    }

    /** Reference: count positions whose value is at most every value below it. */
    static int oracle(int[][] ops) {
        List<Integer> list = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 0) list.add(op[1]);
            else list.remove(list.size() - 1);
        }
        int count = 0;
        int lowest = Integer.MAX_VALUE;
        // A position counts when it ties or beats the running minimum of the positions below it.
        for (int v : list) {
            if (v <= lowest) count++;
            lowest = Math.min(lowest, v);
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1: the stack ends with 5, 3, 7, 3, 8, 1 reduced by three pops, so 5 and 3 remain.
        int[][] e1 = {{0, 5}, {0, 3}, {0, 7}, {0, 3}, {0, 8}, {0, 1}, {1}, {1}, {1}};
        if (run(e1) != 2) throw new AssertionError("example 1");
        // Example 2: values 4, 2 and 1 each set a new minimum, and 6 does not.
        int[][] e2 = {{0, 4}, {0, 2}, {0, 6}, {0, 1}};
        if (run(e2) != 3) throw new AssertionError("example 2");
        // Equal values each keep an entry, so two equal pushes give two entries.
        if (run(new int[][] {{0, 2}, {0, 2}}) != 2) throw new AssertionError("duplicates");
        // Random valid sequences agree with the position-counting reference.
        Random rnd = new Random(1108);
        for (int t = 0; t < 3000; t++) {
            List<int[]> ops = new ArrayList<>();
            int size = 0;
            int n = 1 + rnd.nextInt(30);
            for (int i = 0; i < n; i++) {
                // A pop is legal only when the stack is non-empty.
                if (size > 0 && rnd.nextInt(3) == 0) { ops.add(new int[] {1}); size--; }
                else { ops.add(new int[] {0, rnd.nextInt(7)}); size++; }
            }
            int[][] arr = ops.toArray(new int[0][]);
            if (run(arr) != oracle(arr)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Duplicate Minima (Author exercise)
<!-- id: sq-duplicate-minima -->

**Approach.**
The method keeps a main stack and a stack of minimum levels. A push enters the level stack when the value is at most the current minimum, so each copy of the minimum has its own entry. A pop removes a level entry only when the popped value equals the level stack's top. After each operation, the method reports the level stack's top, or `Integer.MAX_VALUE` when the level stack is empty. The invariant is that the level stack holds every position whose value ties or beats all values below it. A strict comparison on push would break this invariant on the first duplicate.

**Complexity.**
- **Time** is O(n) for n operations, because each operation performs constant work on the two stacks.
- **Space** is O(n), because the output has n entries and the stacks hold at most n values.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DuplicateMinima {
    /**
     * Reports the minimum after every operation.
     * Time: O(n), constant work per operation.
     * Space: O(n), two stacks and the output.
     * Invariant: mins holds each position whose value is at most all values below it.
     */
    static int[] run(int[][] ops) {
        ArrayDeque<Integer> main = new ArrayDeque<>();
        ArrayDeque<Integer> mins = new ArrayDeque<>();
        int[] out = new int[ops.length];
        for (int i = 0; i < ops.length; i++) {
            if (ops[i][0] == 0) {
                main.push(ops[i][1]);
                // Equal values enter too, so each copy of the minimum has its own entry.
                if (mins.isEmpty() || ops[i][1] <= mins.peek()) mins.push(ops[i][1]);
            } else {
                int v = main.pop();
                // Only the copy that equals the level top gives up its entry.
                if (v == mins.peek()) mins.pop();
            }
            // An empty level stack means an empty main stack, so the sentinel is reported.
            out[i] = mins.isEmpty() ? Integer.MAX_VALUE : mins.peek();
        }
        return out;
    }

    /** Reference: scan the whole list after every operation. */
    static int[] oracle(int[][] ops) {
        List<Integer> list = new ArrayList<>();
        int[] out = new int[ops.length];
        for (int i = 0; i < ops.length; i++) {
            if (ops[i][0] == 0) list.add(ops[i][1]);
            else list.remove(list.size() - 1);
            int best = Integer.MAX_VALUE;
            for (int v : list) best = Math.min(best, v);
            out[i] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        int max = Integer.MAX_VALUE;
        // Example 1: two copies of 2 keep the minimum at 2 after one pop.
        int[][] e1 = {{0, 2}, {0, 2}, {0, 5}, {1}, {1}, {1}};
        if (!Arrays.equals(run(e1), new int[] {2, 2, 2, 2, 2, max})) throw new AssertionError("example 1");
        // Example 2: the minimum returns to 7 after 3 is popped, and 7 is still stored twice.
        int[][] e2 = {{0, 7}, {0, 7}, {1}, {0, 3}, {1}, {1}};
        if (!Arrays.equals(run(e2), new int[] {7, 7, 7, 3, 7, max})) throw new AssertionError("example 2");
        // Large magnitudes at the stated limits behave like small ones.
        int[][] e3 = {{0, 1000000000}, {0, -1000000000}, {0, -1000000000}, {1}, {1}, {1}};
        if (!Arrays.equals(run(e3), new int[] {1000000000, -1000000000, -1000000000, -1000000000, 1000000000, max})) throw new AssertionError("limits");
        // Random sequences with many equal values agree with the scanning reference.
        Random rnd = new Random(1109);
        for (int t = 0; t < 3000; t++) {
            List<int[]> ops = new ArrayList<>();
            int size = 0;
            int n = 1 + rnd.nextInt(30);
            for (int i = 0; i < n; i++) {
                // A pop is legal only when the stack is non-empty.
                if (size > 0 && rnd.nextInt(2) == 0) { ops.add(new int[] {1}); size--; }
                else { ops.add(new int[] {0, rnd.nextInt(4)}); size++; }
            }
            int[][] arr = ops.toArray(new int[0][]);
            if (!Arrays.equals(run(arr), oracle(arr))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Min Stack (LeetCode 155)
<!-- id: sq-leetcode-min-stack -->

**Approach.**
The class stores one pair per pushed value, holding the value and the minimum at or below it. `push` computes the new minimum from the entry below, `pop` removes the top pair, and `top` and `getMin` read one field of the top pair. Each call does a fixed number of steps, so the cost is constant in the worst case and not only on average. The invariant is that each pair's minimum equals the smallest value from the bottom up to that pair. The pair design avoids the equality test of the helper design, so duplicates and the extreme `int` values need no special case.

**Complexity.**
- **Time** is O(1) per call in the worst case, because every call touches only the top pair.
- **Space** is O(n) for n stored values, because each value carries one extra integer.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class LeetCodeMinStack {
    /** Stack with constant-time minimum; each entry is {value, minimum at or below it}. */
    static final class MinStack {
        private final ArrayDeque<int[]> entries = new ArrayDeque<>();

        /** Time O(1), Space O(1) per call; the new pair keeps the invariant for its position. */
        void push(int val) {
            // The first value is its own minimum; later values compare against the entry below.
            int lowest = entries.isEmpty() ? val : Math.min(val, entries.peek()[1]);
            entries.push(new int[] {val, lowest});
        }

        /** Removes the newest pair and its stored minimum in O(1). */
        void pop() { entries.pop(); }

        /** Returns the newest value in O(1). */
        int top() { return entries.peek()[0]; }

        /** Returns the stored minimum of the top pair in O(1). */
        int getMin() { return entries.peek()[1]; }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise text.
        MinStack s = new MinStack();
        s.push(-2); s.push(0); s.push(-3);
        if (s.getMin() != -3) throw new AssertionError("example 1 min");
        s.pop();
        if (s.top() != 0 || s.getMin() != -2) throw new AssertionError("example 1 after pop");
        // Example 2: one pop leaves a second copy of 1.
        MinStack d = new MinStack();
        d.push(2); d.push(1); d.push(1); d.pop();
        if (d.getMin() != 1) throw new AssertionError("example 2");
        // The extreme int values are stored and compared without overflow.
        MinStack x = new MinStack();
        x.push(Integer.MAX_VALUE); x.push(Integer.MIN_VALUE); x.push(Integer.MAX_VALUE);
        if (x.getMin() != Integer.MIN_VALUE) throw new AssertionError("extremes");
        x.pop(); x.pop();
        if (x.getMin() != Integer.MAX_VALUE) throw new AssertionError("extremes after pops");
        // Random call sequences agree with a list that scans for the minimum.
        Random rnd = new Random(1155);
        for (int t = 0; t < 3000; t++) {
            MinStack m = new MinStack();
            List<Integer> list = new ArrayList<>();
            for (int i = 0; i < 40; i++) {
                int pick = rnd.nextInt(4);
                // Pop, top and minimum are legal only on a non-empty stack, so an empty stack forces a push.
                if (list.isEmpty() || pick == 0) {
                    int v = rnd.nextInt(9) - 4;
                    m.push(v); list.add(v);
                } else if (pick == 1) {
                    m.pop(); list.remove(list.size() - 1);
                } else if (pick == 2) {
                    if (m.top() != list.get(list.size() - 1)) throw new AssertionError("top " + t);
                } else {
                    int best = Integer.MAX_VALUE;
                    for (int v : list) best = Math.min(best, v);
                    if (m.getMin() != best) throw new AssertionError("min " + t);
                }
            }
        }
        // The lesson text says Integer objects can be equal in value yet differ in identity above 127.
        Integer a = Integer.valueOf(1000), b = Integer.valueOf(1000);
        if (!a.equals(b)) throw new AssertionError("equals");
        if (a == b) throw new AssertionError("identity above the cache");
        // Unboxing one side makes the comparison numeric.
        int c = 1000;
        if (c != b) throw new AssertionError("numeric comparison");
        // Values from -128 to 127 are cached, so identical small values share one object.
        if (Integer.valueOf(127) != Integer.valueOf(127)) throw new AssertionError("cache");
    }
}
```
