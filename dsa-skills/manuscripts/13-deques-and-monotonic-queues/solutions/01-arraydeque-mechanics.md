<!-- solutions-for: 01-arraydeque-mechanics -->
### Solutions For The ArrayDeque Exercises

#### Solution: [Build] Two-Ended Buffer (Author exercise)
<!-- id: dq-two-ended-buffer -->

**Approach.**

The method splits each command into its name and an optional value. It calls the deque method whose name matches the command, so the front calls act on the front and the back calls act on the back. The invariant is that the deque holds exactly the items a plain list would hold after the same commands. The assertions compare the deque with an `ArrayList` model on random command sequences, because the list gives the same answer at a higher cost.

**Complexity.**

- **Time** is O(c) for c commands, because each command is one O(1) deque call.
- **Space** is O(c) in the worst case, because the deque holds every added item.

```java run
import java.util.*;

public final class TwoEndedBuffer {
    /**
     * Applies each command to an empty deque and returns its final contents.
     * Time: O(c) for c commands. Space: O(c) for the stored items.
     * Invariant: the deque equals the sequence the commands describe.
     */
    static int[] apply(String[] commands) {
        Deque<Integer> d = new ArrayDeque<>();
        for (String cmd : commands) {                       // one O(1) call per command
            String[] p = cmd.split(" ");
            switch (p[0]) {
                case "addFirst" -> d.addFirst(Integer.parseInt(p[1]));   // write at the front end
                case "addLast" -> d.addLast(Integer.parseInt(p[1]));     // write at the back end
                case "removeFirst" -> d.removeFirst();                   // valid input, so never empty
                default -> d.removeLast();
            }
        }
        int[] out = new int[d.size()];
        int i = 0;
        for (int x : d) out[i++] = x;                        // iteration runs front to back
        return out;
    }

    /** Model with an ArrayList: same contract, O(n) front operations. */
    static int[] model(String[] commands) {
        List<Integer> l = new ArrayList<>();
        for (String cmd : commands) {
            String[] p = cmd.split(" ");
            switch (p[0]) {
                case "addFirst" -> l.add(0, Integer.parseInt(p[1]));
                case "addLast" -> l.add(Integer.parseInt(p[1]));
                case "removeFirst" -> l.remove(0);
                default -> l.remove(l.size() - 1);
            }
        }
        return l.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // The two worked examples.
        if (!Arrays.equals(apply(new String[]{"addLast 4", "addLast 7", "addFirst 2", "removeLast"}), new int[]{2, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(apply(new String[]{"addFirst 1", "addFirst 2", "addFirst 3", "removeFirst", "addLast 9"}), new int[]{2, 1, 9})) throw new AssertionError("example 2");
        // The empty command list gives an empty result.
        if (apply(new String[0]).length != 0) throw new AssertionError("empty");
        // Random valid command sequences agree with the list model.
        Random rnd = new Random(1);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(30), size = 0;
            String[] cmds = new String[n];
            for (int i = 0; i < n; i++) {
                int k = rnd.nextInt(4);
                if (size == 0 && k >= 2) k = rnd.nextInt(2);   // never remove from an empty deque
                int x = rnd.nextInt(2001) - 1000;
                cmds[i] = switch (k) { case 0 -> "addFirst " + x; case 1 -> "addLast " + x; case 2 -> "removeFirst"; default -> "removeLast"; };
                size += k < 2 ? 1 : -1;
            }
            if (!Arrays.equals(apply(cmds), model(cmds))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Bounded Recent History (Author exercise)
<!-- id: dq-bounded-history -->

**Approach.**

The method appends each item at the back and then checks the size. When the size exceeds the capacity, exactly one item is over, and the oldest item sits at the front, so one `pollFirst` restores the size. The invariant after every step is that the deque holds the most recent `min(c, items so far)` items in arrival order. The assertions compare against a slice of the stream, which states the same contract without a deque.

**Complexity.**

- **Time** is O(n) for a stream of n items, because each item is appended once and removed at most once.
- **Space** is O(c), because the deque holds at most `c + 1` items.

```java run
import java.util.*;

public final class BoundedHistory {
    /**
     * Returns the last c items of the stream from oldest to newest.
     * Time: O(n). Space: O(c). Invariant: the deque holds the newest min(c, seen) items.
     */
    static int[] history(int[] stream, int c) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int x : stream) {                 // each arrival costs O(1)
            d.addLast(x);                      // the newest item enters at the back
            if (d.size() > c) d.pollFirst();   // the oldest item leaves at the front
        }
        int[] out = new int[d.size()];
        int i = 0;
        for (int x : d) out[i++] = x;
        return out;
    }

    public static void main(String[] args) {
        // The two worked examples.
        if (!Arrays.equals(history(new int[]{5, 6, 7, 8}, 3), new int[]{6, 7, 8})) throw new AssertionError("example 1");
        if (!Arrays.equals(history(new int[]{9, 9}, 5), new int[]{9, 9})) throw new AssertionError("example 2");
        // An empty stream and a capacity of one.
        if (history(new int[0], 4).length != 0) throw new AssertionError("empty stream");
        if (!Arrays.equals(history(new int[]{1, 2, 3}, 1), new int[]{3})) throw new AssertionError("capacity one");
        // Random streams agree with a plain slice of the last c items.
        Random rnd = new Random(2);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(40), c = 1 + rnd.nextInt(8);
            int[] s = new int[n];
            for (int i = 0; i < n; i++) s[i] = rnd.nextInt(21) - 10;
            int[] want = Arrays.copyOfRange(s, Math.max(0, n - c), n);
            if (!Arrays.equals(history(s, c), want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty Deque Contract (Author exercise)
<!-- id: dq-empty-contract -->

**Approach.**

The two forms of each call differ only on an empty deque. The returning calls `pollFirst` and `peekLast` give `null` there, and the throwing calls `removeFirst` and `getLast` raise `NoSuchElementException`. The method runs each command, catches that one exception and writes its name. The invariant is that the result text depends only on the command and on whether the deque is empty. The assertions also check the null rejection of `addLast`, which the lesson names as a hazard.

**Complexity.**

- **Time** is O(c) for c commands, because each command is one O(1) call.
- **Space** is O(c), because the output and the deque each hold up to c entries.

```java run
import java.util.*;

public final class EmptyContract {
    /**
     * Runs the commands and returns one result string per command.
     * Time: O(c). Space: O(c). Invariant: the result depends on the call and on emptiness only.
     */
    static String[] run(String[] commands) {
        Deque<Integer> d = new ArrayDeque<>();
        String[] out = new String[commands.length];
        for (int i = 0; i < commands.length; i++) {          // one O(1) call per command
            String[] p = commands[i].split(" ");
            try {
                switch (p[0]) {
                    case "addLast" -> { d.addLast(Integer.parseInt(p[1])); out[i] = "ok"; }
                    case "pollFirst" -> out[i] = String.valueOf(d.pollFirst());   // null text on empty
                    case "peekLast" -> out[i] = String.valueOf(d.peekLast());     // null text on empty
                    case "removeFirst" -> out[i] = String.valueOf(d.removeFirst());
                    default -> out[i] = String.valueOf(d.getLast());
                }
            } catch (NoSuchElementException e) {
                out[i] = "NoSuchElementException";           // only the throwing forms reach here
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The two worked examples.
        if (!Arrays.equals(run(new String[]{"pollFirst", "addLast 3", "peekLast"}), new String[]{"null", "ok", "3"})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new String[]{"removeFirst", "addLast 8", "getLast", "removeFirst", "getLast"}),
                new String[]{"NoSuchElementException", "ok", "8", "8", "NoSuchElementException"})) throw new AssertionError("example 2");
        // The empty command list gives an empty result.
        if (run(new String[0]).length != 0) throw new AssertionError("empty");
        // A peek never removes: two peeks agree.
        if (!Arrays.equals(run(new String[]{"addLast 5", "peekLast", "peekLast"}), new String[]{"ok", "5", "5"})) throw new AssertionError("peek keeps item");
        // The class rejects null, as the lesson states.
        boolean threw = false;
        try { new ArrayDeque<Integer>().addLast(null); } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("null must be rejected");
    }
}
```

#### Solution: [Recognize] Candidate Deque API (Author exercise)
<!-- id: dq-candidate-api -->

**Approach.**

The oldest candidate is the first one added, so it sits at the front. The newest candidate sits at the back. Reading the oldest is `peekFirst`, discarding it is `pollFirst`, reading the newest is `peekLast`, discarding it is `pollLast`, and storing a new item at the newest end is `addLast`. The invariant is that the front is the oldest end and the back is the newest end. The assertions run the five calls on a real deque and confirm that each call touches the end the plan names.

**Complexity.**

- **Time** is O(1), because the plan is a fixed array of five names.
- **Space** is O(1), because the array has a fixed length.

```java run
import java.util.*;

public final class CandidateApi {
    /**
     * Returns the method that performs each of the five steps.
     * Time: O(1). Space: O(1). Invariant: the front holds the oldest candidate, the back the newest.
     */
    static String[] plan() {
        return new String[]{"peekFirst", "pollFirst", "peekLast", "pollLast", "addLast"};
    }

    public static void main(String[] args) {
        // The two worked examples.
        String[] p = plan();
        if (!p[0].equals("peekFirst")) throw new AssertionError("example 1");
        if (!p[4].equals("addLast")) throw new AssertionError("example 2");
        // Run the plan on a real deque holding oldest to newest: 1, 2, 3.
        Deque<Integer> d = new ArrayDeque<>(List.of(1, 2, 3));
        if (d.peekFirst() != 1) throw new AssertionError("peekFirst reads the oldest");
        if (d.pollFirst() != 1) throw new AssertionError("pollFirst discards the oldest");
        if (d.peekLast() != 3) throw new AssertionError("peekLast reads the newest");
        if (d.pollLast() != 3) throw new AssertionError("pollLast discards the newest");
        d.addLast(9);
        if (!d.toString().equals("[2, 9]")) throw new AssertionError("addLast stores at the newest end");
        // Both read calls give null on an empty deque, which the plan relies on.
        Deque<Integer> e = new ArrayDeque<>();
        if (e.peekFirst() != null || e.pollLast() != null) throw new AssertionError("null on empty");
    }
}
```
