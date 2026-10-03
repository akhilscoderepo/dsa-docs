<!-- solutions-for: 01-arraydeque-contracts -->
### ArrayDeque Contracts

#### Solution: [Build] Deque As Stack (Author exercise)
<!-- id: sq-deque-as-stack -->

**Approach.** Add every value with `addLast`, then remove with `removeLast` once per value. Both operations use the same end, which makes the structure last in first out, so the output is the input reversed. The assertions compare with a manual reversal on random arrays, and show that the legacy `push` and `pop` pair on the same deque uses the front instead and still reverses, while mixing `addLast` with `pop` returns the oldest value and so breaks the stack discipline.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class DequeAsStack {
    static int[] reverseWithStack(int[] values) {
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int v : values) stack.addLast(v);
        int[] out = new int[values.length];
        for (int i = 0; i < out.length; i++) out[i] = stack.removeLast();
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(reverseWithStack(new int[] {3, 1, 4}), new int[] {4, 1, 3})) throw new AssertionError("example 1");
        if (reverseWithStack(new int[0]).length != 0) throw new AssertionError("example 2");
        ArrayDeque<Integer> viaPush = new ArrayDeque<>();
        viaPush.push(1); viaPush.push(2);
        if (viaPush.pop() != 2) throw new AssertionError("push and pop share the front, so the newest leaves first");
        ArrayDeque<Integer> mixed = new ArrayDeque<>();
        mixed.addLast(1); mixed.addLast(2);
        if (mixed.pop() != 1) throw new AssertionError("pop takes the front, so addLast with pop breaks the stack rule");
        Random rnd = new Random(11101);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(15);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2001) - 1000;
            int[] want = new int[n];
            for (int i = 0; i < n; i++) want[i] = a[n - 1 - i];
            if (!Arrays.equals(reverseWithStack(a), want)) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Deque As Queue (Author exercise)
<!-- id: sq-deque-as-queue -->

**Approach.** Walk the script once. A nonnegative value goes to the back with `addLast`, and each -1 removes from the front with `removeFirst` and records the value. Arrivals and departures use opposite ends, so the oldest value leaves first. The assertions check the two examples, compare with a plain array-and-head-index simulation on random valid scripts, and confirm that `removeLast` in place of `removeFirst` gives a different order, which proves that the end choice matters.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DequeAsQueue {
    static int[] run(int[] script, boolean fromFront) {
        ArrayDeque<Integer> line = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) line.addLast(s);
            else out.add(fromFront ? line.removeFirst() : line.removeLast());
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] oracle(int[] script) {
        int[] store = new int[script.length];
        int head = 0, tail = 0;
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s >= 0) store[tail++] = s;
            else out.add(store[head++]);
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[] {5, 8, -1, 2, -1, -1}, true), new int[] {5, 8, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[] {7, -1, 9, -1}, true), new int[] {7, 9})) throw new AssertionError("example 2");
        if (Arrays.equals(run(new int[] {1, 2, -1}, false), run(new int[] {1, 2, -1}, true))) throw new AssertionError("the departure end changes the order");
        Random rnd = new Random(11102);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(20);
            int[] script = new int[n];
            int size = 0;
            for (int i = 0; i < n; i++) {
                if (size > 0 && rnd.nextBoolean()) { script[i] = -1; size--; }
                else { script[i] = rnd.nextInt(100); size++; }
            }
            if (!Arrays.equals(run(script, true), oracle(script))) throw new AssertionError("differs on " + Arrays.toString(script));
        }
    }
}
```

#### Solution: [Boundary] Empty Access Contract (Author exercise)
<!-- id: sq-empty-access-contract -->

**Approach.** Execute each command on one real `ArrayDeque<Integer>` and translate the outcome. `add x` returns the dash, `poll` and `peek` return `null` or the value, `remove` and `element` throw `NoSuchElementException` when the deque is empty, and `addnull` throws `NullPointerException` and stores nothing. The solution catches the exceptions and prints their simple class names. The assertions state each Java claim directly: the polling methods return `null` on empty, the throwing methods raise the named exception, and a refused null leaves the size unchanged. The random check compares against a model written with an `ArrayList`.

**Complexity.** O(n) time for n commands and O(n) space for the output.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class EmptyAccessContract {
    static List<String> run(String[] commands) {
        ArrayDeque<Integer> deque = new ArrayDeque<>();
        List<String> out = new ArrayList<>();
        for (String c : commands) {
            try {
                if (c.startsWith("add ")) { deque.addLast(Integer.parseInt(c.substring(4))); out.add("-"); }
                else if (c.equals("addnull")) { deque.addLast(null); out.add("-"); }
                else if (c.equals("poll")) out.add(String.valueOf(deque.pollFirst()));
                else if (c.equals("peek")) out.add(String.valueOf(deque.peekFirst()));
                else if (c.equals("remove")) out.add(String.valueOf(deque.removeFirst()));
                else out.add(String.valueOf(deque.getFirst()));
            } catch (RuntimeException e) {
                out.add(e.getClass().getSimpleName());
            }
        }
        return out;
    }
    static List<String> model(String[] commands) {
        List<Integer> list = new ArrayList<>();
        List<String> out = new ArrayList<>();
        for (String c : commands) {
            if (c.startsWith("add ")) { list.add(Integer.parseInt(c.substring(4))); out.add("-"); }
            else if (c.equals("addnull")) out.add("NullPointerException");
            else if (c.equals("poll")) out.add(list.isEmpty() ? "null" : String.valueOf(list.remove(0)));
            else if (c.equals("peek")) out.add(list.isEmpty() ? "null" : String.valueOf(list.get(0)));
            else if (c.equals("remove")) out.add(list.isEmpty() ? "NoSuchElementException" : String.valueOf(list.remove(0)));
            else out.add(list.isEmpty() ? "NoSuchElementException" : String.valueOf(list.get(0)));
        }
        return out;
    }

    public static void main(String[] args) {
        if (!run(new String[] {"poll", "add 4", "peek", "remove", "remove"}).equals(Arrays.asList("null", "-", "4", "4", "NoSuchElementException"))) throw new AssertionError("example 1");
        if (!run(new String[] {"addnull", "add 1", "element", "poll"}).equals(Arrays.asList("NullPointerException", "-", "1", "1"))) throw new AssertionError("example 2");
        ArrayDeque<Integer> d = new ArrayDeque<>();
        if (d.pollFirst() != null || d.peekFirst() != null || d.pollLast() != null || d.peekLast() != null) throw new AssertionError("polling methods return null on empty");
        try { d.removeLast(); throw new AssertionError("removeLast must throw"); } catch (NoSuchElementException expected) { }
        try { d.getLast(); throw new AssertionError("getLast must throw"); } catch (NoSuchElementException expected) { }
        try { d.addLast(null); throw new AssertionError("null must be refused"); } catch (NullPointerException expected) { }
        if (d.size() != 0) throw new AssertionError("a refused null stores nothing");
        String[] pool = {"poll", "peek", "remove", "element", "addnull", "add 3", "add -2", "add 9"};
        Random rnd = new Random(11103);
        for (int t = 0; t < 3000; t++) {
            String[] cmds = new String[rnd.nextInt(12)];
            for (int i = 0; i < cmds.length; i++) cmds[i] = pool[rnd.nextInt(pool.length)];
            if (!run(cmds).equals(model(cmds))) throw new AssertionError("differs on " + Arrays.toString(cmds));
        }
    }
}
```

#### Solution: [Recognize] Choose The Ends (Author exercise)
<!-- id: sq-choose-the-ends -->

**Approach.** Replay the script twice, once on a stack and once on a queue, both built from an `ArrayDeque` with the ends fixed as in the lesson, and record the values removed by each. Compare each replay with `seen`. A match with both gives `"BOTH"`, a match with one gives that name, and no match gives `"NEITHER"`. The two rules agree whenever the container never holds more than one value at a removal, which the second example uses. The assertions compare with an independent simulation that stores values in plain arrays, and check that the answer is never `"NEITHER"` when `seen` is produced by one of the rules.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ChooseTheEnds {
    static int[] replay(int[] script, boolean lifo) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s > 0) d.addLast(s);
            else out.add(lifo ? d.removeLast() : d.removeFirst());
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static String classify(int[] script, int[] seen) {
        boolean stack = Arrays.equals(replay(script, true), seen);
        boolean queue = Arrays.equals(replay(script, false), seen);
        if (stack && queue) return "BOTH";
        if (stack) return "STACK";
        if (queue) return "QUEUE";
        return "NEITHER";
    }
    static int[] arrays(int[] script, boolean lifo) {
        int[] store = new int[script.length + 1];
        int lo = 0, hi = 0;
        List<Integer> out = new ArrayList<>();
        for (int s : script) {
            if (s > 0) store[hi++] = s;
            else if (lifo) out.add(store[--hi]);
            else out.add(store[lo++]);
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!classify(new int[] {1, 2, 3, 0, 0}, new int[] {3, 2}).equals("STACK")) throw new AssertionError("example 1");
        if (!classify(new int[] {1, 0, 2, 0}, new int[] {1, 2}).equals("BOTH")) throw new AssertionError("example 2");
        if (!classify(new int[] {1, 2, 3, 0, 0}, new int[] {2, 1}).equals("NEITHER")) throw new AssertionError("neither rule gives 2 then 1");
        if (!classify(new int[] {1, 2, 3, 0, 0}, new int[] {1, 2}).equals("QUEUE")) throw new AssertionError("queue answer");
        Random rnd = new Random(11104);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] script = new int[n];
            int size = 0;
            for (int i = 0; i < n; i++) {
                if (size > 0 && rnd.nextInt(3) == 0) { script[i] = 0; size--; }
                else { script[i] = 1 + rnd.nextInt(50); size++; }
            }
            if (!Arrays.equals(replay(script, true), arrays(script, true))) throw new AssertionError("stack replay differs");
            if (!Arrays.equals(replay(script, false), arrays(script, false))) throw new AssertionError("queue replay differs");
            boolean lifo = rnd.nextBoolean();
            String got = classify(script, replay(script, lifo));
            if (got.equals("NEITHER")) throw new AssertionError("a genuine run must be explained by its own rule");
            if (lifo && got.equals("QUEUE")) throw new AssertionError("a stack run cannot be QUEUE only");
            if (!lifo && got.equals("STACK")) throw new AssertionError("a queue run cannot be STACK only");
        }
    }
}
```
