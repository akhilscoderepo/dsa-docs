<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Two Stack Queues

#### Solution: [Build] Enqueue And One Dequeue (Author exercise)
<!-- id: sq-enqueue-one-dequeue -->

**Approach.**
The method pushes each value of `values` onto `in`, so the last value ends on top. It then pops `in` until empty and pushes each popped value onto `out`. Each pop from `in` yields the newest remaining value, and each push places it under the next one, so the first value finishes on top of `out`. The method pops that value and reads the rest of `out` from bottom to top. The invariant during the move is that `out` holds the already moved values in arrival order from the bottom up when read in reverse, and the oldest unmoved value is the top of `in` after the newer ones are gone.

**Complexity.**
- **Time** is O(n), because each value is pushed and popped a constant number of times on each stack.
- **Space** is O(n), because the two stacks together hold all n values.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class OneDequeue {
    /**
     * Moves values from in to out, pops one value, and lists the rest of out.
     * Time: O(n), every value is pushed and popped a fixed number of times.
     * Space: O(n), two stacks hold the values.
     * Invariant: after the move, the top of out is the first value of the input.
     */
    static int[] firstThenRest(int[] values) {
        ArrayDeque<Integer> in = new ArrayDeque<>();
        ArrayDeque<Integer> out = new ArrayDeque<>();
        // Each push places the next value above the earlier ones in `in`.
        for (int v : values) in.push(v);
        // Popping in and pushing out reverses the stack order once.
        while (!in.isEmpty()) out.push(in.pop());
        int[] res = new int[values.length];
        // The first slot receives the popped top of out, the oldest value.
        int k = 0;
        res[k++] = out.pop();
        // The descending iterator of the deque visits the stack from bottom to top.
        java.util.Iterator<Integer> it = out.descendingIterator();
        while (it.hasNext()) res[k++] = it.next();
        return res;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(firstThenRest(new int[] {5, 8, 2}), new int[] {5, 2, 8})) throw new AssertionError("example 1");
        if (!Arrays.equals(firstThenRest(new int[] {3, 3, 9, 1}), new int[] {3, 1, 9, 3})) throw new AssertionError("example 2");
        // Reversal fact: a stack read from top to bottom lists values newest first.
        ArrayDeque<Integer> probe = new ArrayDeque<>();
        probe.push(1); probe.push(2); probe.push(3);
        if (!probe.toString().equals("[3, 2, 1]")) throw new AssertionError("stack order");
        // Random inputs give the first value, then the other values in reverse arrival order.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            int[] want = new int[a.length];
            want[0] = a[0];
            for (int i = 1; i < a.length; i++) want[i] = a[a.length - i];
            if (!Arrays.equals(firstThenRest(a), want)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Interleaved Queue Calls (Author exercise)
<!-- id: sq-interleaved-queue-calls -->

**Approach.**
The method keeps `in` for arrivals and `out` for departures. A row `{1, v}` pushes onto `in` and never touches `out`, so values already in `out` stay ahead of the new one. A dequeue row first checks whether `out` is empty and moves all of `in` across only in that case. It then pops `out`. The invariant is that every value in `in` arrived after every value in `out`, so the top of `out` is the oldest value in the queue.

**Complexity.**
- **Time** is O(m) for m rows, because each value moves between the stacks at most once and each row does constant other work.
- **Space** is O(m), because the stacks hold at most the enqueued values and the result holds one entry per dequeue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class InterleavedCalls {
    /**
     * Replays enqueue and dequeue rows on two stacks.
     * Time: O(m) for m rows, each value moves between stacks once.
     * Space: O(m) for the stacks and the result.
     * Invariant: every value in `in` arrived after every value in `out`.
     */
    static int[] replay(int[][] ops) {
        ArrayDeque<Integer> in = new ArrayDeque<>();
        ArrayDeque<Integer> out = new ArrayDeque<>();
        List<Integer> got = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 1) {
                // An arrival goes on top of in and leaves out untouched.
                in.push(op[1]);
            } else {
                // Transfer out only when it is empty, otherwise older values would sit under newer ones.
                if (out.isEmpty()) while (!in.isEmpty()) out.push(in.pop());
                got.add(out.pop());
            }
        }
        int[] res = new int[got.size()];
        for (int i = 0; i < res.length; i++) res[i] = got.get(i);
        return res;
    }

    /** Reference: a real FIFO queue. */
    static int[] oracle(int[][] ops) {
        ArrayDeque<Integer> q = new ArrayDeque<>();
        List<Integer> got = new ArrayList<>();
        for (int[] op : ops) if (op[0] == 1) q.addLast(op[1]); else got.add(q.removeFirst());
        return got.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Both examples from the exercise text.
        if (!Arrays.equals(replay(new int[][] {{1, 4}, {1, 7}, {2}, {1, 2}, {2}, {2}}), new int[] {4, 7, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(replay(new int[][] {{1, 6}, {2}, {1, 1}, {1, 5}, {2}, {2}}), new int[] {6, 1, 5})) throw new AssertionError("example 2");
        // Random valid call sequences match the reference queue.
        Random rnd = new Random(12);
        for (int t = 0; t < 4000; t++) {
            List<int[]> ops = new ArrayList<>();
            int size = 0;
            for (int i = 0, n = rnd.nextInt(30); i < n; i++) {
                if (size > 0 && rnd.nextBoolean()) { ops.add(new int[] {2}); size--; }
                else { ops.add(new int[] {1, rnd.nextInt(1000)}); size++; }
            }
            int[][] a = ops.toArray(new int[0][]);
            if (!Arrays.equals(replay(a), oracle(a))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Empty Queue API (Author exercise)
<!-- id: sq-empty-queue-api -->

**Approach.**
Every row that reads a value first moves `in` onto `out` when `out` is empty. After that step, an empty `out` means the whole queue is empty, so the method appends `-1` and changes nothing. Otherwise a dequeue pops `out` and a peek reads `out` without removing. The check happens after the transfer, because testing `out` alone would report an empty queue while `in` still holds values. The invariant is that the queue is empty exactly when both stacks are empty, and after a transfer that means `out` is empty. The harness also confirms that `ArrayDeque.peek` returns `null` on an empty stack and `pop` throws, which is why the method tests emptiness explicitly.

**Complexity.**
- **Time** is O(m) for m rows, because each value moves between the stacks at most once.
- **Space** is O(m), because the stacks and the result hold at most one entry per row.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class EmptyCalls {
    /**
     * Serves dequeue and peek rows and answers -1 on an empty queue.
     * Time: O(m) for m rows, each value moves between stacks once.
     * Space: O(m) for the stacks and the result.
     * Invariant: after a transfer, out is empty only if the whole queue is empty.
     */
    static int[] serve(int[][] ops) {
        ArrayDeque<Integer> in = new ArrayDeque<>();
        ArrayDeque<Integer> out = new ArrayDeque<>();
        List<Integer> res = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 1) { in.push(op[1]); continue; }
            // Transfer first, so an empty out proves the whole queue is empty.
            if (out.isEmpty()) while (!in.isEmpty()) out.push(in.pop());
            if (out.isEmpty()) res.add(-1);
            else if (op[0] == 2) res.add(out.pop());
            else res.add(out.peek());
        }
        return res.stream().mapToInt(Integer::intValue).toArray();
    }

    /** Reference: a list used as a queue. */
    static int[] oracle(int[][] ops) {
        List<Integer> q = new ArrayList<>();
        List<Integer> res = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 1) q.add(op[1]);
            else if (q.isEmpty()) res.add(-1);
            else res.add(op[0] == 2 ? q.remove(0) : q.get(0));
        }
        return res.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Both examples from the exercise text.
        if (!Arrays.equals(serve(new int[][] {{2}, {1, 8}, {3}, {2}, {3}}), new int[] {-1, 8, 8, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(serve(new int[][] {{1, 5}, {1, 6}, {3}, {3}, {2}, {2}, {2}}), new int[] {5, 5, 5, 6, -1})) throw new AssertionError("example 2");
        // Library contract: peek on an empty deque gives null and pop throws.
        ArrayDeque<Integer> empty = new ArrayDeque<>();
        if (empty.peek() != null) throw new AssertionError("peek null");
        boolean threw = false;
        try { empty.pop(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("pop throws");
        // Random rows, including calls on an empty queue, match the reference.
        Random rnd = new Random(13);
        for (int t = 0; t < 4000; t++) {
            int[][] a = new int[rnd.nextInt(30)][];
            for (int i = 0; i < a.length; i++) {
                int k = 1 + rnd.nextInt(3);
                a[i] = k == 1 ? new int[] {1, rnd.nextInt(100)} : new int[] {k};
            }
            if (!Arrays.equals(serve(a), oracle(a))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Implement Queue Using Stacks (LeetCode 232)
<!-- id: sq-implement-queue-stacks -->

**Approach.**
The class `MyQueue` keeps `in` and `out` and a counter of moves. The call `push` goes onto `in`. The calls `pop` and `peek` call a private transfer that moves `in` onto `out` only when `out` is empty. The call `empty` is true when both stacks are empty. A value enters `in` once, leaves `in` once during a transfer, and leaves `out` once, because a transfer empties `in` completely and values on `out` never return. So the moves counter never exceeds the number of pushes. The invariant is that `out` holds the oldest values in arrival order, with the oldest on top.

**Complexity.**
- **Time** is amortized O(1) per call and O(m) for m calls, because the moves counter is at most the number of pushes.
- **Space** is O(n) for n stored values, because each value sits on exactly one stack.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MyQueueRun {
    static final class MyQueue {
        private final ArrayDeque<Integer> in = new ArrayDeque<>();
        private final ArrayDeque<Integer> out = new ArrayDeque<>();
        int moves = 0;

        /** Adds x behind every stored value. Time: O(1). Space: O(1). */
        void push(int x) { in.push(x); }

        // Transfers out only when it is empty, which keeps the oldest value on top.
        private void transfer() {
            if (!out.isEmpty()) return;
            while (!in.isEmpty()) { out.push(in.pop()); moves++; }
        }

        /** Removes the oldest value. Time: amortized O(1). Space: O(1). */
        int pop() { transfer(); return out.pop(); }

        /** Reads the oldest value. Time: amortized O(1). Space: O(1). */
        int peek() { transfer(); return out.peek(); }

        /** True when no value is stored. Time: O(1). Space: O(1). */
        boolean empty() { return in.isEmpty() && out.isEmpty(); }
    }

    static int[] run(int[][] ops, int[] movesOut) {
        MyQueue q = new MyQueue();
        List<Integer> res = new ArrayList<>();
        int pushes = 0;
        for (int[] op : ops) {
            switch (op[0]) {
                case 1 -> { q.push(op[1]); pushes++; }
                case 2 -> res.add(q.pop());
                case 3 -> res.add(q.peek());
                default -> res.add(q.empty() ? 1 : 0);
            }
            // Each value moves at most once, so the count never passes the pushes so far.
            if (q.moves > pushes) throw new AssertionError("moves exceed pushes");
        }
        movesOut[0] = q.moves;
        return res.stream().mapToInt(Integer::intValue).toArray();
    }

    /** Reference: a real FIFO queue. */
    static int[] oracle(int[][] ops) {
        ArrayDeque<Integer> q = new ArrayDeque<>();
        List<Integer> res = new ArrayList<>();
        for (int[] op : ops) {
            switch (op[0]) {
                case 1 -> q.addLast(op[1]);
                case 2 -> res.add(q.pollFirst());
                case 3 -> res.add(q.peekFirst());
                default -> res.add(q.isEmpty() ? 1 : 0);
            }
        }
        return res.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        int[] mv = new int[1];
        // Both examples from the exercise text.
        if (!Arrays.equals(run(new int[][] {{1, 3}, {1, 8}, {3}, {2}, {4}, {2}, {4}}, mv), new int[] {3, 3, 0, 8, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[][] {{4}, {1, 6}, {1, 2}, {2}, {1, 9}, {2}, {2}, {4}}, mv), new int[] {1, 6, 2, 9, 1})) throw new AssertionError("example 2");
        // Random valid sequences match the reference and respect the move bound.
        Random rnd = new Random(14);
        for (int t = 0; t < 4000; t++) {
            List<int[]> ops = new ArrayList<>();
            int size = 0;
            for (int i = 0, n = rnd.nextInt(40); i < n; i++) {
                int k = 1 + rnd.nextInt(4);
                if ((k == 2 || k == 3) && size == 0) k = 1;
                if (k == 1) { ops.add(new int[] {1, 1 + rnd.nextInt(100)}); size++; }
                else { ops.add(new int[] {k}); if (k == 2) size--; }
            }
            int[][] a = ops.toArray(new int[0][]);
            if (!Arrays.equals(run(a, mv), oracle(a))) throw new AssertionError("random");
        }
    }
}
```
