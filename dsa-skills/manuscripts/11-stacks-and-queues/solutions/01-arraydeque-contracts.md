<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For ArrayDeque Contracts

#### Solution: [Build] Deque As Stack (Author exercise)
<!-- id: sq-deque-as-stack -->

**Approach.**
The method adds each element at the last end and then removes at the last end. Each removal returns the element added most recently and still present, so removals come out in reverse insertion order. The invariant is that the last end alone changes, and the deque holds the unremoved prefix of the input in index order. The harness also confirms the false friend: `java.util.Stack` gives the same answer but allows `get(0)`, which reads the bottom element, and `ArrayDeque` has no such method.

**Complexity.**
- **Time** is O(n), because each of the n elements is added once and removed once at amortized O(1).
- **Space** is O(n), because the deque holds all elements before the first removal.

```java run
import java.util.ArrayDeque;
import java.util.Random;
import java.util.Stack;

public final class DequeAsStack {
    /**
     * Returns the values in reverse order by using only the last end of one deque.
     * Time: O(n), amortized O(1) per end operation.
     * Space: O(n) for the deque and the output.
     * Invariant: the deque holds the unremoved prefix in index order, and only its last end changes.
     */
    static int[] asStack(int[] values) {
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        // Every element enters at the last end, so the last end holds the newest element.
        for (int v : values) dq.addLast(v);
        int[] out = new int[values.length];
        // Each removal takes the newest remaining element, so the output reverses the input.
        for (int i = 0; i < out.length; i++) out[i] = dq.removeLast();
        return out;
    }

    /** Reference: write the input backwards by index. */
    static int[] oracle(int[] v) {
        int[] r = new int[v.length];
        for (int i = 0; i < v.length; i++) r[i] = v[v.length - 1 - i];
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and example 2 from the exercise.
        if (!java.util.Arrays.equals(asStack(new int[] {4, 7, 9}), new int[] {9, 7, 4})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(asStack(new int[] {2, 2, 5, 1}), new int[] {1, 5, 2, 2})) throw new AssertionError("example 2");
        // Random arrays agree with the index-reversal reference.
        Random rnd = new Random(1101);
        for (int t = 0; t < 3000; t++) {
            int[] v = new int[rnd.nextInt(12)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(7) - 3;
            if (!java.util.Arrays.equals(asStack(v), oracle(v))) throw new AssertionError("random");
        }
        // Legacy Stack allows reading the bottom element by index, which breaks the one-end rule.
        Stack<Integer> legacy = new Stack<>();
        legacy.push(1); legacy.push(2);
        if (legacy.get(0) != 1) throw new AssertionError("Stack.get(0) reads the bottom");
        // ArrayDeque offers push, pop and peek on the first end, so peekLast would read a different element.
        ArrayDeque<Integer> mixed = new ArrayDeque<>();
        mixed.push(1); mixed.push(2);
        if (mixed.peek() != 2 || mixed.peekLast() != 1) throw new AssertionError("push works on the first end");
    }
}
```

#### Solution: [Vary] Deque As Queue (Author exercise)
<!-- id: sq-deque-as-queue -->

**Approach.**
The method adds at the last end and removes at the first end. Elements enter in index order and leave from the opposite end, so the earliest added element always leaves first. The only change from the stack version is the removal call. The invariant is that the first end holds the earliest unremoved element and the last end holds the newest.

**Complexity.**
- **Time** is O(n), because each element is added once and removed once at amortized O(1).
- **Space** is O(n), because the deque holds all elements before the first removal.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class DequeAsQueue {
    /**
     * Returns the values in insertion order by adding at the last end and removing at the first end.
     * Time: O(n), amortized O(1) per end operation.
     * Space: O(n) for the deque and the output.
     * Invariant: the first end holds the earliest unremoved element.
     */
    static int[] asQueue(int[] values) {
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        // New elements enter at the last end behind every present element.
        for (int v : values) dq.addLast(v);
        int[] out = new int[values.length];
        // Each removal takes the earliest remaining element, so arrival order is kept.
        for (int i = 0; i < out.length; i++) out[i] = dq.removeFirst();
        return out;
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the exercise.
        if (!Arrays.equals(asQueue(new int[] {4, 7, 9}), new int[] {4, 7, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(asQueue(new int[] {5, 5, 2}), new int[] {5, 5, 2})) throw new AssertionError("example 2");
        // Random arrays come back unchanged, and the result is a new array.
        Random rnd = new Random(1102);
        for (int t = 0; t < 3000; t++) {
            int[] v = new int[rnd.nextInt(12)];
            for (int i = 0; i < v.length; i++) v[i] = rnd.nextInt(5);
            int[] copy = v.clone();
            int[] got = asQueue(v);
            if (!Arrays.equals(got, copy) || got == v) throw new AssertionError("random");
        }
        // The first end and the last end hold different elements after two insertions.
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        dq.addLast(1); dq.addLast(2);
        if (dq.peekFirst() != 1 || dq.peekLast() != 2) throw new AssertionError("ends");
    }
}
```

#### Solution: [Boundary] Empty Access Contract (Author exercise)
<!-- id: sq-empty-access-contract -->

**Approach.**
The method parses each command and calls the matching deque operation. The forms `poll` and `peek` return `null` on an empty deque, so the method turns that result into the text `"null"`. The forms `remove` and `element` throw `NoSuchElementException`, so the method catches that exception and reports its name. Storing `null` is impossible, because `addLast(null)` throws `NullPointerException`, and that fact makes a `null` result mean empty. The invariant is that the deque holds only non-null integers, so each answer has one cause.

**Complexity.**
- **Time** is O(c) for c commands, because each command costs amortized O(1).
- **Space** is O(c), because the deque and the answers hold at most one entry per command.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class EmptyAccess {
    /**
     * Runs the commands against one deque and reports each outcome.
     * Time: O(c), amortized O(1) per command.
     * Space: O(c) for the deque and the answers.
     * Invariant: the deque never holds null, so a null result always means empty.
     */
    static String[] run(String[] commands) {
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        String[] out = new String[commands.length];
        // One answer per command, in input order.
        for (int i = 0; i < commands.length; i++) {
            String c = commands[i];
            if (c.startsWith("add ")) {
                // add inserts at the last end and always succeeds for a non-null value.
                dq.addLast(Integer.parseInt(c.substring(4)));
                out[i] = "ok";
            } else if (c.equals("poll") || c.equals("peek")) {
                // The null-returning forms report empty as null instead of throwing.
                Integer x = c.equals("poll") ? dq.pollFirst() : dq.peekFirst();
                out[i] = x == null ? "null" : String.valueOf(x);
            } else {
                // The throwing forms signal empty with NoSuchElementException.
                try {
                    out[i] = String.valueOf(c.equals("remove") ? dq.removeFirst() : dq.getFirst());
                } catch (NoSuchElementException e) {
                    out[i] = "NoSuchElementException";
                }
            }
        }
        return out;
    }

    /** Reference: the same commands on an ArrayList that checks emptiness by hand. */
    static String[] oracle(String[] commands) {
        List<Integer> list = new ArrayList<>();
        String[] out = new String[commands.length];
        for (int i = 0; i < commands.length; i++) {
            String c = commands[i];
            if (c.startsWith("add ")) { list.add(Integer.parseInt(c.substring(4))); out[i] = "ok"; }
            else if (list.isEmpty()) out[i] = (c.equals("poll") || c.equals("peek")) ? "null" : "NoSuchElementException";
            else out[i] = String.valueOf(c.equals("poll") || c.equals("remove") ? list.remove(0) : list.get(0));
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: removal on an empty deque throws, and poll returns null.
        String[] e1 = run(new String[] {"poll", "add 3", "peek", "remove", "remove"});
        if (!Arrays.equals(e1, new String[] {"null", "ok", "3", "3", "NoSuchElementException"})) throw new AssertionError("example 1");
        // Example 2: element throws on empty, and peek returns null after the only element is polled.
        String[] e2 = run(new String[] {"element", "add 8", "element", "poll", "peek"});
        if (!Arrays.equals(e2, new String[] {"NoSuchElementException", "ok", "8", "8", "null"})) throw new AssertionError("example 2");
        // Random command lists agree with the reference.
        Random rnd = new Random(1103);
        String[] kinds = {"poll", "remove", "peek", "element"};
        for (int t = 0; t < 3000; t++) {
            String[] cmds = new String[rnd.nextInt(12)];
            for (int i = 0; i < cmds.length; i++) cmds[i] = rnd.nextInt(3) == 0 ? "add " + (rnd.nextInt(9) - 4) : kinds[rnd.nextInt(4)];
            if (!Arrays.equals(run(cmds), oracle(cmds))) throw new AssertionError("random " + Arrays.toString(cmds));
        }
        // The Java hazard behind the contract: ArrayDeque rejects null, in both add forms.
        boolean threw = false;
        try { new ArrayDeque<Integer>().addLast(null); } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("addLast(null) must throw");
        threw = false;
        try { new ArrayDeque<Integer>().offer(null); } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("offer(null) must throw");
    }
}
```

#### Solution: [Recognize] Choose The Ends (Author exercise)
<!-- id: sq-choose-the-ends -->

**Approach.**
Both modes record with `addLast`. The mode `"undo"` takes with `pollLast`, which returns the newest recorded event, and the mode `"buffer"` takes with `pollFirst`, which returns the earliest one. The `poll` forms return `null` for an empty deque, and the method turns that into `-1`. The invariant is that each mode uses one end for taking in every call, so the deque order always equals recording order.

**Complexity.**
- **Time** is O(n), because each event costs amortized O(1).
- **Space** is O(n), because the deque can hold every recorded event.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ChooseEnds {
    /**
     * Returns the value of every take event under the given mode.
     * Time: O(n), amortized O(1) per event.
     * Space: O(n) for the deque and the output.
     * Invariant: the deque holds recorded events in recording order, and each mode takes from one fixed end.
     */
    static int[] replay(int[] events, String mode) {
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        boolean undo = mode.equals("undo");
        // One pass over the events in order.
        for (int e : events) {
            if (e > 0) {
                // Recording is the same for both modes.
                dq.addLast(e);
            } else {
                // The null-returning forms handle an empty deque without an exception.
                Integer taken = undo ? dq.pollLast() : dq.pollFirst();
                out.add(taken == null ? -1 : taken);
            }
        }
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    /** Reference: an ArrayList with explicit index choice. */
    static int[] oracle(int[] events, String mode) {
        List<Integer> list = new ArrayList<>();
        List<Integer> out = new ArrayList<>();
        for (int e : events) {
            if (e > 0) list.add(e);
            else if (list.isEmpty()) out.add(-1);
            else out.add(list.remove(mode.equals("undo") ? list.size() - 1 : 0));
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Examples 1 and 2 from the exercise.
        int[] ev = {3, 8, 0, 5, 0, 0, 0};
        if (!Arrays.equals(replay(ev, "undo"), new int[] {8, 5, 3, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(replay(ev, "buffer"), new int[] {3, 8, 5, -1})) throw new AssertionError("example 2");
        // Random event lists agree with the reference in both modes.
        Random rnd = new Random(1104);
        for (int t = 0; t < 3000; t++) {
            int[] in = new int[rnd.nextInt(14)];
            for (int i = 0; i < in.length; i++) in[i] = rnd.nextInt(3) == 0 ? 0 : 1 + rnd.nextInt(9);
            for (String m : new String[] {"undo", "buffer"})
                if (!Arrays.equals(replay(in, m), oracle(in, m))) throw new AssertionError("random " + m + Arrays.toString(in));
        }
        // poll on an empty deque returns null, while removeFirst throws.
        ArrayDeque<Integer> empty = new ArrayDeque<>();
        if (empty.pollFirst() != null || empty.pollLast() != null) throw new AssertionError("poll returns null");
        boolean threw = false;
        try { empty.removeFirst(); } catch (java.util.NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("removeFirst throws");
    }
}
```
