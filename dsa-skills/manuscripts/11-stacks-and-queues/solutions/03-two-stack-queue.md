<!-- solutions-for: 03-two-stack-queue -->
### Two-Stack Queue

#### Solution: [Build] Enqueue And One Dequeue (Author exercise)
<!-- id: sq-enqueue-one-dequeue -->

**Approach.** Push every value onto the input stack, which makes the first value the bottom. The single dequeue finds the output stack empty, so it moves all values across with a pop and a push each. The move reverses the order, so the oldest value ends on top of the output stack and is popped. The answer is that value followed by the output stack from bottom to top, which lists the remaining values in reverse arrival order. The assertions compare with a plain list model: the dequeued value is the first value, and the reported output equals the remaining values reversed.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class EnqueueOneDequeue {
    static int[] run(int[] values) {
        ArrayDeque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();
        for (int v : values) in.addLast(v);
        while (!in.isEmpty()) out.addLast(in.removeLast());
        int oldest = out.removeLast();
        int[] result = new int[1 + out.size()];
        result[0] = oldest;
        int i = 1;
        for (int v : out) result[i++] = v;
        return result;
    }
    static int[] oracle(int[] values) {
        List<Integer> rest = new ArrayList<>();
        for (int i = values.length - 1; i >= 1; i--) rest.add(values[i]);
        int[] r = new int[1 + rest.size()];
        r[0] = values[0];
        for (int i = 0; i < rest.size(); i++) r[i + 1] = rest.get(i);
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[] {4, 5, 6}), new int[] {4, 6, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[] {9}), new int[] {9})) throw new AssertionError("example 2");
        ArrayDeque<Integer> check = new ArrayDeque<>();
        check.addLast(1); check.addLast(2);
        int count = 0;
        for (int v : check) { if (count == 0 && v != 1) throw new AssertionError("ArrayDeque iterates from first to last"); count++; }
        Random rnd = new Random(11301);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2001) - 1000;
            if (!Arrays.equals(run(a), oracle(a))) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Interleaved Queue Calls (Author exercise)
<!-- id: sq-interleaved-queue-calls -->

**Approach.** Use the two-stack queue with a shift that moves values only when the output stack is empty, and let both removal and peek call it first. Arrivals always go to the input stack, so a value that arrives while the output stack still holds older ones waits behind them. The assertions compare with a queue built on `ArrayDeque` with `addLast` and `removeFirst`, on random valid scripts, and show that a version that transfers on every removal regardless of the output stack returns a wrong order on the first example.

**Complexity.** O(n) time overall, since each value is moved at most once, and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class InterleavedQueueCalls {
    static int[] run(int[] script, boolean transferAlways) {
        ArrayDeque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();
        List<Integer> results = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) { in.addLast(s); continue; }
            if (transferAlways || out.isEmpty()) while (!in.isEmpty()) out.addLast(in.removeLast());
            results.add(s == -1 ? out.removeLast() : out.peekLast());
        }
        return results.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] oracle(int[] script) {
        ArrayDeque<Integer> q = new ArrayDeque<>();
        List<Integer> results = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) q.addLast(s);
            else results.add(s == -1 ? q.removeFirst() : q.peekFirst());
        }
        return results.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[] {5, 6, -1, 7, 8, -2, -1, -1}, false), new int[] {5, 6, 6, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[] {3, -2, -2, -1}, false), new int[] {3, 3, 3})) throw new AssertionError("example 2");
        int[] strand = {5, 6, -1, 7, 8, -1};
        if (Arrays.equals(run(strand, true), oracle(strand))) throw new AssertionError("transferring while the output holds older values breaks the order");
        Random rnd = new Random(11302);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(20);
            int[] script = new int[n];
            int size = 0;
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(4);
                if (size > 0 && pick == 0) { script[i] = -1; size--; }
                else if (size > 0 && pick == 1) script[i] = -2;
                else { script[i] = rnd.nextInt(100); size++; }
            }
            if (!Arrays.equals(run(script, false), oracle(script))) throw new AssertionError("differs on " + Arrays.toString(script));
        }
    }
}
```

#### Solution: [Boundary] Empty Queue API (Author exercise)
<!-- id: sq-empty-queue-api -->

**Approach.** The queue is empty only when both stacks are empty, so a command first shifts if the output stack is empty, and then looks at the output stack: if it is still empty the command returns -1 and changes nothing. Testing only the output stack before shifting would report empty while the input stack still holds values. The assertions compare with an `ArrayDeque` queue that uses `pollFirst` and `peekFirst`, which return `null` on empty, and show that the faulty version, which checks the output stack before shifting, differs on the first example.

**Complexity.** O(n) time overall and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class EmptyQueueApi {
    static int[] run(int[] script, boolean checkBeforeShift) {
        ArrayDeque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();
        List<Integer> results = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) { in.addLast(s); continue; }
            if (checkBeforeShift && out.isEmpty()) { results.add(-1); continue; }
            if (out.isEmpty()) while (!in.isEmpty()) out.addLast(in.removeLast());
            if (out.isEmpty()) { results.add(-1); continue; }
            results.add(s == -1 ? out.removeLast() : out.peekLast());
        }
        return results.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] oracle(int[] script) {
        ArrayDeque<Integer> q = new ArrayDeque<>();
        List<Integer> results = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) q.addLast(s);
            else {
                Integer v = s == -1 ? q.pollFirst() : q.peekFirst();
                results.add(v == null ? -1 : v);
            }
        }
        return results.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[] {-2, 4, -2, -1, -1}, false), new int[] {-1, 4, 4, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[] {1, 2, -1, 3, -1, -1, -1}, false), new int[] {1, 2, 3, -1})) throw new AssertionError("example 2");
        if (Arrays.equals(run(new int[] {4, -2}, true), oracle(new int[] {4, -2}))) throw new AssertionError("checking the output stack alone reports empty too early");
        Random rnd = new Random(11303);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(18);
            int[] script = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(5);
                script[i] = pick == 0 ? -1 : pick == 1 ? -2 : rnd.nextInt(50);
            }
            if (!Arrays.equals(run(script, false), oracle(script))) throw new AssertionError("differs on " + Arrays.toString(script));
        }
    }
}
```

#### Solution: [Recognize] Implement Queue using Stacks (LeetCode 232)
<!-- id: sq-implement-queue-stacks -->

**Approach.** Build the queue as a small class with an input stack, an output stack and a shift that runs only when the output stack is empty. `push` adds to the input stack, `pop` and `peek` shift and then use the output stack, and `empty` checks both stacks. A counter of moves lets the assertions confirm that no value ever moves more than once, so the total number of moves never exceeds the number of pushes. The assertions replay random command lists against an `ArrayDeque` queue and compare every printed result.

**Complexity.** O(1) amortized per operation, O(n) worst case for one call, and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class QueueUsingStacks {
    static final class TwoStackQueue {
        private final ArrayDeque<Integer> in = new ArrayDeque<>();
        private final ArrayDeque<Integer> out = new ArrayDeque<>();
        int moves;
        void push(int x) { in.addLast(x); }
        private void shift() {
            if (!out.isEmpty()) return;
            while (!in.isEmpty()) { out.addLast(in.removeLast()); moves++; }
        }
        int peek() { shift(); return out.peekLast(); }
        int pop() { shift(); return out.removeLast(); }
        boolean empty() { return in.isEmpty() && out.isEmpty(); }
    }
    static List<String> run(String[] commands, int[] movesOut) {
        TwoStackQueue q = new TwoStackQueue();
        List<String> out = new ArrayList<>();
        int pushes = 0;
        for (String c : commands) {
            if (c.startsWith("push ")) { q.push(Integer.parseInt(c.substring(5))); pushes++; out.add("-"); }
            else if (c.equals("pop")) out.add(String.valueOf(q.pop()));
            else if (c.equals("peek")) out.add(String.valueOf(q.peek()));
            else out.add(String.valueOf(q.empty()));
            if (q.moves > pushes) throw new AssertionError("a value moved more than once");
        }
        movesOut[0] = q.moves;
        return out;
    }
    static List<String> oracle(String[] commands) {
        ArrayDeque<Integer> q = new ArrayDeque<>();
        List<String> out = new ArrayList<>();
        for (String c : commands) {
            if (c.startsWith("push ")) { q.addLast(Integer.parseInt(c.substring(5))); out.add("-"); }
            else if (c.equals("pop")) out.add(String.valueOf(q.removeFirst()));
            else if (c.equals("peek")) out.add(String.valueOf(q.peekFirst()));
            else out.add(String.valueOf(q.isEmpty()));
        }
        return out;
    }

    public static void main(String[] args) {
        int[] m = new int[1];
        if (!run(new String[] {"push 1", "push 2", "peek", "pop", "empty"}, m).equals(List.of("-", "-", "1", "1", "false"))) throw new AssertionError("example 1");
        if (!run(new String[] {"push 7", "pop", "empty"}, m).equals(List.of("-", "7", "true"))) throw new AssertionError("example 2");
        Random rnd = new Random(11304);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(25);
            List<String> cmds = new ArrayList<>();
            int size = 0;
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(5);
                if (size > 0 && pick == 0) { cmds.add("pop"); size--; }
                else if (size > 0 && pick == 1) cmds.add("peek");
                else if (pick == 2) cmds.add("empty");
                else { cmds.add("push " + rnd.nextInt(1000)); size++; }
            }
            String[] arr = cmds.toArray(new String[0]);
            if (!run(arr, m).equals(oracle(arr))) throw new AssertionError("differs on " + cmds);
        }
    }
}
```
