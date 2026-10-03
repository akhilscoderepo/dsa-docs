<!-- solutions-for: 01-arraydeque-mechanics -->
### ArrayDeque Mechanics

#### Solution: [Build] Two-Ended Buffer (Author exercise)
<!-- id: dq-two-ended-buffer -->

**Approach.** Split each command on the space, call the one `ArrayDeque` method that carries the end in its name, and append to the result only for the four removing or peeking commands. The two `add` commands change the order in opposite ways: `addLast` puts the item behind everything and `addFirst` puts it in front. The assertions run both examples, compare with a model built on an `ArrayList` with explicit index work, and check the Java fact that `push` is `addFirst`, which is why a program that mixes the stack names with the queue names confuses the roles of the ends.

**Complexity.** O(1) amortized per command, so O(c) time for `c` commands, and O(c) memory for the deque and the result.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class TwoEndedBuffer {
    static List<Integer> run(String[] commands) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (String c : commands) {
            String[] p = c.split(" ");
            switch (p[0]) {
                case "addFirst": d.addFirst(Integer.parseInt(p[1])); break;
                case "addLast": d.addLast(Integer.parseInt(p[1])); break;
                case "removeFirst": out.add(d.removeFirst()); break;
                case "removeLast": out.add(d.removeLast()); break;
                case "peekFirst": out.add(d.peekFirst()); break;
                case "peekLast": out.add(d.peekLast()); break;
                default: throw new AssertionError("unknown command " + c);
            }
        }
        return out;
    }
    static List<Integer> model(String[] commands) {
        ArrayList<Integer> line = new ArrayList<>();
        List<Integer> out = new ArrayList<>();
        for (String c : commands) {
            String[] p = c.split(" ");
            switch (p[0]) {
                case "addFirst": line.add(0, Integer.parseInt(p[1])); break;
                case "addLast": line.add(Integer.parseInt(p[1])); break;
                case "removeFirst": out.add(line.remove(0)); break;
                case "removeLast": out.add(line.remove(line.size() - 1)); break;
                case "peekFirst": out.add(line.get(0)); break;
                case "peekLast": out.add(line.get(line.size() - 1)); break;
                default: throw new AssertionError("unknown command " + c);
            }
        }
        return out;
    }

    public static void main(String[] args) {
        String[] e1 = {"addLast 4", "addFirst 7", "addLast 9", "removeFirst", "peekLast", "removeLast"};
        if (!run(e1).equals(Arrays.asList(7, 9, 9))) throw new AssertionError("example 1");
        String[] e2 = {"addFirst 1", "addFirst 2", "peekFirst", "peekLast"};
        if (!run(e2).equals(Arrays.asList(2, 1))) throw new AssertionError("example 2");
        ArrayDeque<Integer> s = new ArrayDeque<>();
        s.push(1);
        s.push(2);
        if (s.peekFirst() != 2 || s.peekLast() != 1) throw new AssertionError("push is addFirst");
        Random rnd = new Random(1301);
        for (int t = 0; t < 3000; t++) {
            List<String> cmds = new ArrayList<>();
            int size = 0;
            int n = 1 + rnd.nextInt(20);
            for (int i = 0; i < n; i++) {
                int k = rnd.nextInt(6);
                if (size == 0 || k < 2) { cmds.add((k == 0 ? "addFirst " : "addLast ") + rnd.nextInt(50)); size++; }
                else if (k == 2) { cmds.add("removeFirst"); size--; }
                else if (k == 3) { cmds.add("removeLast"); size--; }
                else cmds.add(k == 4 ? "peekFirst" : "peekLast");
            }
            String[] arr = cmds.toArray(new String[0]);
            if (!run(arr).equals(model(arr))) throw new AssertionError("disagrees with the list model on " + cmds);
        }
    }
}
```

#### Solution: [Vary] Bounded Recent History (Author exercise)
<!-- id: dq-bounded-recent-history -->

**Approach.** Append each value at the back, then check the size. If it exceeds the capacity, remove the front and record it. Checking after the append means the history briefly holds `capacity + 1` items, which is fine, and the evicted item is always the oldest. The assertions check both examples, compare with a simulation on an `ArrayList` that removes index 0, and count the item moves that the list version performs to confirm the cost described in the lesson: every front removal from a list of `capacity + 1` items moves `capacity` items, so `r` evictions cost `r * capacity` moves, which grows with the product of the two sizes.

**Complexity.** O(n) time for `n` values, and O(capacity) extra space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class BoundedRecentHistory {
    static List<Integer> evicted(int[] stream, int capacity) {
        ArrayDeque<Integer> history = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (int x : stream) {
            history.addLast(x);
            if (history.size() > capacity) out.add(history.removeFirst());
        }
        return out;
    }
    static long listMoves;
    static List<Integer> evictedByList(int[] stream, int capacity) {
        ArrayList<Integer> history = new ArrayList<>();
        List<Integer> out = new ArrayList<>();
        for (int x : stream) {
            history.add(x);
            if (history.size() > capacity) { listMoves += history.size() - 1; out.add(history.remove(0)); }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!evicted(new int[]{5, 6, 7, 8, 9}, 3).equals(Arrays.asList(5, 6))) throw new AssertionError("example 1");
        if (!evicted(new int[]{1, 2}, 5).isEmpty()) throw new AssertionError("example 2");
        Random rnd = new Random(1302);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(20);
            int[] s = new int[n];
            for (int i = 0; i < n; i++) s[i] = rnd.nextInt(100);
            int cap = 1 + rnd.nextInt(6);
            if (!evicted(s, cap).equals(evictedByList(s, cap))) throw new AssertionError("disagrees with the list simulation");
        }
        int n = 2000;
        int[] stream = new int[n];
        listMoves = 0;
        evictedByList(stream, n / 2);
        if (listMoves != (long) (n - n / 2) * (n / 2)) throw new AssertionError("each front removal shifts the other items: " + listMoves);
    }
}
```

#### Solution: [Boundary] Empty Deque Contract (Author exercise)
<!-- id: dq-empty-deque-contract -->

**Approach.** Use `pollFirst`, `pollLast`, `peekFirst` and `peekLast`, which return `null` on an empty deque, hold the result in an `Integer`, and convert to the sentinel -1 when it is `null`. The sentinel is safe because items are non-negative. The throwing methods would end the program on the first empty access. The assertions check both examples and every fact about the contract that the lesson states: `removeFirst` throws `NoSuchElementException` on an empty deque, `pollFirst` returns `null`, `ArrayDeque` rejects `null` items with a `NullPointerException`, `LinkedList` accepts them, and unboxing a `null` into an `int` throws.

**Complexity.** O(1) amortized per command and O(c) memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class EmptyDequeContract {
    static List<Integer> run(String[] script) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        for (String c : script) {
            String[] p = c.split(" ");
            Integer got = null;
            boolean produces = true;
            switch (p[0]) {
                case "addLast": d.addLast(Integer.parseInt(p[1])); produces = false; break;
                case "pollFirst": got = d.pollFirst(); break;
                case "pollLast": got = d.pollLast(); break;
                case "peekFirst": got = d.peekFirst(); break;
                case "peekLast": got = d.peekLast(); break;
                default: throw new AssertionError("unknown command " + c);
            }
            if (produces) out.add(got == null ? -1 : got);
        }
        return out;
    }
    static List<Integer> model(String[] script) {
        ArrayList<Integer> line = new ArrayList<>();
        List<Integer> out = new ArrayList<>();
        for (String c : script) {
            String[] p = c.split(" ");
            switch (p[0]) {
                case "addLast": line.add(Integer.parseInt(p[1])); break;
                case "pollFirst": out.add(line.isEmpty() ? -1 : line.remove(0)); break;
                case "pollLast": out.add(line.isEmpty() ? -1 : line.remove(line.size() - 1)); break;
                case "peekFirst": out.add(line.isEmpty() ? -1 : line.get(0)); break;
                case "peekLast": out.add(line.isEmpty() ? -1 : line.get(line.size() - 1)); break;
                default: throw new AssertionError("unknown command " + c);
            }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!run(new String[]{"pollFirst", "addLast 3", "pollFirst", "pollFirst"}).equals(Arrays.asList(-1, 3, -1))) throw new AssertionError("example 1");
        if (!run(new String[]{"peekLast", "peekFirst"}).equals(Arrays.asList(-1, -1))) throw new AssertionError("example 2");
        boolean threw = false;
        try { new ArrayDeque<Integer>().removeFirst(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("removeFirst throws on an empty deque");
        if (new ArrayDeque<Integer>().pollFirst() != null) throw new AssertionError("pollFirst returns null on an empty deque");
        threw = false;
        try { new ArrayDeque<Integer>().addLast(null); } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("ArrayDeque rejects null items");
        LinkedList<Integer> linked = new LinkedList<>();
        linked.addLast(null);
        if (linked.size() != 1) throw new AssertionError("LinkedList accepts null items, so a null result would be ambiguous");
        threw = false;
        try { Integer none = new ArrayDeque<Integer>().pollFirst(); int x = none; } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("unboxing null into int throws");
        Random rnd = new Random(1303);
        String[] kinds = {"pollFirst", "pollLast", "peekFirst", "peekLast"};
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20);
            String[] script = new String[n];
            for (int i = 0; i < n; i++) script[i] = rnd.nextInt(3) == 0 ? "addLast " + rnd.nextInt(30) : kinds[rnd.nextInt(4)];
            if (!run(script).equals(model(script))) throw new AssertionError("disagrees with the list model on " + Arrays.toString(script));
        }
    }
}
```

#### Solution: [Recognize] Candidate Deque API (Author exercise)
<!-- id: dq-candidate-deque-api -->

**Approach.** The oldest candidate is at the front and the newest at the back, so looking at and removing the oldest use `peekFirst` and `removeFirst`, looking at and removing the newest use `peekLast` and `removeLast`, and a new candidate is always added behind everything with `addLast`. The mapping is a table lookup, and the interesting part is why it is right. The assertions replay random step strings against two structures at once: a real `ArrayDeque` driven by the returned method names, and a list model driven by the meaning of each letter, and check that the two always agree on what each look returns and on the final contents.

**Complexity.** O(m) time for a string of `m` steps and O(m) memory for the result.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class CandidateDequeApi {
    static List<String> methods(String steps) {
        List<String> out = new ArrayList<>();
        for (char c : steps.toCharArray()) {
            switch (c) {
                case 'S': out.add("peekFirst"); break;
                case 'E': out.add("removeFirst"); break;
                case 'N': out.add("peekLast"); break;
                case 'D': out.add("removeLast"); break;
                case 'A': out.add("addLast"); break;
                default: throw new AssertionError("unknown step " + c);
            }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!methods("SEA").equals(Arrays.asList("peekFirst", "removeFirst", "addLast"))) throw new AssertionError("example 1");
        if (!methods("NDNA").equals(Arrays.asList("peekLast", "removeLast", "peekLast", "addLast"))) throw new AssertionError("example 2");
        Random rnd = new Random(1304);
        for (int t = 0; t < 3000; t++) {
            StringBuilder sb = new StringBuilder();
            int size = 0;
            int n = 1 + rnd.nextInt(25);
            for (int i = 0; i < n; i++) {
                char c = "SENDA".charAt(rnd.nextInt(5));
                if (size == 0 && c != 'A') c = 'A';
                if (c == 'A') size++;
                if (c == 'E' || c == 'D') size--;
                sb.append(c);
            }
            String steps = sb.toString();
            ArrayDeque<Integer> real = new ArrayDeque<>();
            ArrayList<Integer> model = new ArrayList<>();
            List<String> names = methods(steps);
            int counter = 0;
            for (int i = 0; i < steps.length(); i++) {
                char c = steps.charAt(i);
                String m = names.get(i);
                if (c == 'A') {
                    real.addLast(counter);
                    model.add(counter++);
                } else if (c == 'S') {
                    if (!m.equals("peekFirst") || real.peekFirst().intValue() != model.get(0)) throw new AssertionError("oldest candidate must be at the front");
                } else if (c == 'N') {
                    if (!m.equals("peekLast") || real.peekLast().intValue() != model.get(model.size() - 1)) throw new AssertionError("newest candidate must be at the back");
                } else if (c == 'E') {
                    if (!m.equals("removeFirst") || real.removeFirst().intValue() != model.remove(0)) throw new AssertionError("expiry removes the oldest");
                } else {
                    if (!m.equals("removeLast") || real.removeLast().intValue() != model.remove(model.size() - 1)) throw new AssertionError("domination removes the newest");
                }
            }
            if (!new ArrayList<>(real).equals(model)) throw new AssertionError("final contents differ for " + steps);
        }
    }
}
```
