<!-- solutions-for: 07-min-stack -->
### Min Stack

#### Solution: [Build] Value-Min Pairs (Author exercise)
<!-- id: sq-value-min-pairs -->

**Approach.** Each push stores the value together with the smaller of the value and the minimum recorded by the entry below, or the value itself on an empty stack. A pop removes the top pair, and a question reads the second slot of the top pair. The minimum of every prefix is fixed at the moment that prefix is created, so nothing is recomputed. The assertions compare with a scan over a plain stack at every question, on random valid scripts.

**Complexity.** O(1) per operation and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ValueMinPairs {
    static int[] answers(int[] script) {
        ArrayDeque<int[]> pairs = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) {
                int below = pairs.isEmpty() ? s : pairs.peekLast()[1];
                pairs.addLast(new int[] {s, Math.min(s, below)});
            } else if (s == -1) pairs.removeLast();
            else out.add(pairs.peekLast()[1]);
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] oracle(int[] script) {
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) stack.addLast(s);
            else if (s == -1) stack.removeLast();
            else {
                int m = Integer.MAX_VALUE;
                for (int v : stack) m = Math.min(m, v);
                out.add(m);
            }
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(answers(new int[] {5, 3, 7, -2, -1, -2, -1, -2}), new int[] {3, 3, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(answers(new int[] {9, -2}), new int[] {9})) throw new AssertionError("example 2");
        Random rnd = new Random(11701);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(25);
            int[] script = new int[n];
            int size = 0;
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(4);
                if (size > 0 && pick == 0) { script[i] = -1; size--; }
                else if (size > 0 && pick == 1) script[i] = -2;
                else { script[i] = rnd.nextInt(10); size++; }
            }
            if (!Arrays.equals(answers(script), oracle(script))) throw new AssertionError("differs on " + Arrays.toString(script));
        }
    }
}
```

#### Solution: [Vary] Two-Stack Minimum (Author exercise)
<!-- id: sq-two-stack-minimum -->

**Approach.** Keep the readings in one stack and the records in another. A pushed value is recorded when it is smaller than or equal to the top record, or when the record stack is empty. A pop removes the record when the popped value equals the top record. A question reads the top record. The answer list ends with the size of the record stack. The assertions compare the answers with a scan oracle, compare the final size with a direct count of the values that are at most every value below them, and show that a strict comparison gives a smaller record stack and fails on duplicates.

**Complexity.** O(1) per operation and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class TwoStackMinimum {
    static int[] run(int[] script, boolean allowEqual) {
        ArrayDeque<Integer> values = new ArrayDeque<>(), mins = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) {
                values.addLast(s);
                if (mins.isEmpty() || (allowEqual ? s <= mins.peekLast() : s < mins.peekLast())) mins.addLast(s);
            } else if (s == -1) {
                int x = values.removeLast();
                if (!mins.isEmpty() && x == mins.peekLast()) mins.removeLast();
            } else out.add(mins.isEmpty() ? Integer.MIN_VALUE : mins.peekLast());
        }
        out.add(mins.size());
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] oracle(int[] script) {
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) stack.addLast(s);
            else if (s == -1) stack.removeLast();
            else { int m = Integer.MAX_VALUE; for (int v : stack) m = Math.min(m, v); out.add(m); }
        }
        List<Integer> list = new ArrayList<>(stack);
        int records = 0;
        for (int i = 0; i < list.size(); i++) {
            boolean atMost = true;
            for (int j = 0; j < i; j++) if (list.get(j) < list.get(i)) atMost = false;
            if (atMost) records++;
        }
        out.add(records);
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[] {4, 4, 2, -2}, true), new int[] {2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[] {5, 6, 7, -2}, true), new int[] {5, 1})) throw new AssertionError("example 2");
        if (run(new int[] {4, 4}, false)[0] != 1) throw new AssertionError("a strict comparison records only one of two equal minimums");
        Random rnd = new Random(11702);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(25);
            int[] script = new int[n];
            int size = 0;
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(4);
                if (size > 0 && pick == 0) { script[i] = -1; size--; }
                else if (size > 0 && pick == 1) script[i] = -2;
                else { script[i] = rnd.nextInt(5); size++; }
            }
            if (!Arrays.equals(run(script, true), oracle(script))) throw new AssertionError("differs on " + Arrays.toString(script));
        }
    }
}
```

#### Solution: [Boundary] Duplicate Minima (Author exercise)
<!-- id: sq-duplicate-minima -->

**Approach.** Use the two-stack layout with the rule that equal values are recorded. Each pop reports the removed value and removes a record when the value equals the top record, each top command reports the top reading, and each question reports the top record. With equality recorded, two copies of the minimum have two records, so popping one leaves the other. The assertions run the strict version on the second example and show that it loses the minimum and fails with an exception or a wrong value, and compare the equal-recording version with a scan oracle on random scripts with many duplicates.

**Complexity.** O(1) per operation and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DuplicateMinima {
    static int[] run(int[] script, boolean allowEqual) {
        ArrayDeque<Integer> values = new ArrayDeque<>(), mins = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) {
                values.addLast(s);
                if (mins.isEmpty() || (allowEqual ? s <= mins.peekLast() : s < mins.peekLast())) mins.addLast(s);
            } else if (s == -1) {
                int x = values.removeLast();
                if (!mins.isEmpty() && x == mins.peekLast()) mins.removeLast();
                out.add(x);
            } else if (s == -2) out.add(mins.peekLast());
            else out.add(values.peekLast());
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] oracle(int[] script) {
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) stack.addLast(s);
            else if (s == -1) out.add(stack.removeLast());
            else if (s == -2) { int m = Integer.MAX_VALUE; for (int v : stack) m = Math.min(m, v); out.add(m); }
            else out.add(stack.peekLast());
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[] {2, 2, -1, -2}, true), new int[] {2, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[] {3, 1, 1, 4, -1, -1, -2, -3}, true), new int[] {4, 1, 1, 1})) throw new AssertionError("example 2");
        boolean broke = false;
        try {
            int[] bad = run(new int[] {2, 2, -1, -2}, false);
            if (bad[1] != 2) broke = true;
        } catch (RuntimeException e) { broke = true; }
        if (!broke) throw new AssertionError("the strict version should lose the duplicate minimum");
        Random rnd = new Random(11703);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(25);
            int[] script = new int[n];
            int size = 0;
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(5);
                if (size > 0 && pick == 0) { script[i] = -1; size--; }
                else if (size > 0 && pick == 1) script[i] = -2;
                else if (size > 0 && pick == 2) script[i] = -3;
                else { script[i] = rnd.nextInt(3); size++; }
            }
            if (!Arrays.equals(run(script, true), oracle(script))) throw new AssertionError("differs on " + Arrays.toString(script));
        }
    }
}
```

#### Solution: [Recognize] Min Stack (LeetCode 155)
<!-- id: sq-min-stack -->

**Approach.** Store each entry as a pair of the exact value and the exact minimum of the stack up to that entry. No difference between two values is ever stored, since a difference of two `int` values can overflow. Each command is a constant number of deque calls. The assertions show the overflow that rules out the difference encoding, compare a replay of random command lists with a scan oracle that includes extreme values, and count the deque calls per command to confirm that each stays within a fixed bound.

**Complexity.** O(1) worst case per command and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class MinStackDesign {
    static final class MinStack {
        private final ArrayDeque<int[]> pairs = new ArrayDeque<>();
        int calls;
        void push(int x) {
            int below = pairs.isEmpty() ? x : pairs.peekLast()[1];
            calls = 3;
            pairs.addLast(new int[] {x, Math.min(x, below)});
        }
        void pop() { calls = 1; pairs.removeLast(); }
        int top() { calls = 1; return pairs.peekLast()[0]; }
        int getMin() { calls = 1; return pairs.peekLast()[1]; }
    }
    static List<String> run(String[] commands) {
        MinStack s = new MinStack();
        List<String> out = new ArrayList<>();
        for (String c : commands) {
            if (c.startsWith("push ")) { s.push(Integer.parseInt(c.substring(5))); out.add("-"); }
            else if (c.equals("pop")) { s.pop(); out.add("-"); }
            else if (c.equals("top")) out.add(String.valueOf(s.top()));
            else out.add(String.valueOf(s.getMin()));
            if (s.calls > 3) throw new AssertionError("more than a constant number of calls");
        }
        return out;
    }
    static List<String> oracle(String[] commands) {
        ArrayList<Integer> stack = new ArrayList<>();
        List<String> out = new ArrayList<>();
        for (String c : commands) {
            if (c.startsWith("push ")) { stack.add(Integer.parseInt(c.substring(5))); out.add("-"); }
            else if (c.equals("pop")) { stack.remove(stack.size() - 1); out.add("-"); }
            else if (c.equals("top")) out.add(String.valueOf(stack.get(stack.size() - 1)));
            else { int m = Integer.MAX_VALUE; for (int v : stack) m = Math.min(m, v); out.add(String.valueOf(m)); }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!run(new String[] {"push 6", "push 2", "getMin", "pop", "top", "getMin"}).equals(List.of("-", "-", "2", "-", "6", "6"))) throw new AssertionError("example 1");
        if (!run(new String[] {"push -2147483648", "push 5", "getMin", "pop", "getMin"}).equals(List.of("-", "-", "-2147483648", "-", "-2147483648"))) throw new AssertionError("example 2");
        if (Integer.MAX_VALUE - Integer.MIN_VALUE >= 0) throw new AssertionError("the difference of two extreme ints overflows to a negative number");
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, -1, 1, 7};
        Random rnd = new Random(11704);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(20);
            List<String> cmds = new ArrayList<>();
            int size = 0;
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(5);
                if (size > 0 && pick == 0) { cmds.add("pop"); size--; }
                else if (size > 0 && pick == 1) cmds.add("top");
                else if (size > 0 && pick == 2) cmds.add("getMin");
                else { cmds.add("push " + pool[rnd.nextInt(pool.length)]); size++; }
            }
            String[] arr = cmds.toArray(new String[0]);
            if (!run(arr).equals(oracle(arr))) throw new AssertionError("differs on " + cmds);
        }
    }
}
```
