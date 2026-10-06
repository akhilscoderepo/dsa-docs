<!-- solutions-for: 06-cycle-entry -->
### Solutions For Cycles

#### Solution: [Build] Linked List Cycle (LeetCode 141)
<!-- id: ll-cycle-detect -->

**Approach.**
Two references start at the head. The slow reference moves one node per turn, and the fast reference moves two. The loop runs while the fast reference and its successor are non-null, so the double step never reads `null.next`. If the references become equal, they are on the same node inside a cycle, and the method returns `true`. If the loop ends, the fast reference reached the end of the chain, and the method returns `false`.

The invariant is that both references are on the chain, and the distance from slow to fast along the chain only grows until they enter a cycle. In a cycle the fast reference gains one node per turn, so the gap reaches 0.

**Complexity.**
- **Time** is O(n), because the slow reference makes at most `n` steps before the references meet or the chain ends.
- **Space** is O(1), because the method stores two references.

```java run
import java.util.*;

public final class CycleDetect {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns true when the list has a cycle.
     * Time: O(n), because the references meet or the chain ends within O(n) turns.
     * Space: O(1), because two references are stored.
     * Invariant: both references are on the chain, and equal references mean a cycle.
     */
    static boolean hasCycle(Node head) {
        Node slow = head, fast = head;
        // Both tests run before fast.next.next is read.
        while (fast != null && fast.next != null) {
            slow = slow.next;                         // one step
            fast = fast.next.next;                    // two steps
            if (slow == fast) return true;            // identity, not value
        }
        return false;                                 // the fast reference reached the end
    }

    /** Builds a list from vals; pos is the index the last node points at, or -1 for no cycle. */
    static Node build(int[] vals, int pos) {
        if (vals.length == 0) return null;
        Node[] nodes = new Node[vals.length];
        // Create the nodes first so the cycle link can point back at any of them.
        for (int i = 0; i < vals.length; i++) nodes[i] = new Node(vals[i], null);
        for (int i = 0; i + 1 < vals.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0) nodes[vals.length - 1].next = nodes[pos];
        return nodes[0];
    }

    /** Oracle: walks with an identity set and reports the first repeated node. */
    static boolean oracle(Node head) {
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node c = head; c != null; c = c.next) if (!seen.add(c)) return true;
        return false;
    }

    public static void main(String[] args) {
        // Example 1: a cycle back to the node 2.
        if (!hasCycle(build(new int[] {3, 2, 0, -4}, 1))) throw new AssertionError("ex1");
        // Example 2: repeated values without a repeated node.
        if (hasCycle(build(new int[] {1, 2, 1, 2}, -1))) throw new AssertionError("ex2");
        // The empty list has no cycle.
        if (hasCycle(null)) throw new AssertionError("empty");
        // Random lists with and without cycles must match the identity-set oracle.
        Random rnd = new Random(51);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(10);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(3);
            int pos = n == 0 || rnd.nextBoolean() ? -1 : rnd.nextInt(n);
            Node h = build(v, pos);
            if (hasCycle(h) != oracle(h)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Measure Cycle Length (Author exercise)
<!-- id: ll-cycle-length -->

**Approach.**
The two-speed walk first finds a node inside the cycle. If the walk ends at the end of the chain, the method returns 0. Otherwise it starts a counter at 1, moves a reference one node past the meeting node, and counts nodes until the reference returns to the meeting node. The cycle has no branch, so one full turn visits each cycle node exactly once.

The invariant is that the reference stays on the cycle, so the counting loop ends after exactly `L` nodes.

**Complexity.**
- **Time** is O(n), because the first phase takes at most `a + L` steps and the count takes `L` steps.
- **Space** is O(1), because the method stores a few references and a counter.

```java run
import java.util.*;

public final class CycleLength {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the node count of the cycle, or 0 when no cycle exists.
     * Time: O(n), because the walk plus one turn cover O(n) nodes.
     * Space: O(1), because a few references are stored.
     * Invariant: the counting reference stays on the cycle.
     */
    static int cycleLength(Node head) {
        Node slow = head, fast = head, meet = null;
        // Phase one: find a node inside the cycle, if any.
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) { meet = slow; break; }
        }
        if (meet == null) return 0;                   // the chain ends, so no cycle exists
        int length = 1;                               // the meeting node counts once
        // One full turn returns to the meeting node, counting each cycle node once.
        for (Node c = meet.next; c != meet; c = c.next) length++;
        return length;
    }

    /** Builds a list from vals; pos is the index the last node points at, or -1 for no cycle. */
    static Node build(int[] vals, int pos) {
        if (vals.length == 0) return null;
        Node[] nodes = new Node[vals.length];
        for (int i = 0; i < vals.length; i++) nodes[i] = new Node(vals[i], null);
        for (int i = 0; i + 1 < vals.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0) nodes[vals.length - 1].next = nodes[pos];
        return nodes[0];
    }

    public static void main(String[] args) {
        // Example 1: nodes 3 to 6 form a cycle of 4.
        if (cycleLength(build(new int[] {1, 2, 3, 4, 5, 6}, 2)) != 4) throw new AssertionError("ex1");
        // Example 2: no cycle gives 0.
        if (cycleLength(build(new int[] {7, 8, 9}, -1)) != 0) throw new AssertionError("ex2");
        // A self-loop has length 1, and the empty list has length 0.
        if (cycleLength(build(new int[] {5}, 0)) != 1) throw new AssertionError("self");
        if (cycleLength(null) != 0) throw new AssertionError("empty");
        // Random lists: the cycle length is n - pos, or 0 without a cycle.
        Random rnd = new Random(52);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(12);
            int[] v = new int[n];
            int pos = n == 0 || rnd.nextBoolean() ? -1 : rnd.nextInt(n);
            int expect = pos < 0 ? 0 : n - pos;
            if (cycleLength(build(v, pos)) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Self-Loop And Two-Node Cycle (Author exercise)
<!-- id: ll-cycle-small -->

**Approach.**
The method runs the two-speed loop and counts slow steps. The loop condition tests `fast != null` and then `fast.next != null`, so the empty list and every list that ends in `null` leave the loop without a dereference of `null`. A self-loop makes both references equal after one step, because `slow` and `fast` both move to the same node. A two-node cycle makes them equal after two steps. The method returns the slow-step count when the references meet and -1 when the loop ends.

The invariant is that the two reads of `next` in each turn only happen after both tests pass.

**Complexity.**
- **Time** is O(n), because the references meet or the chain ends within O(n) steps.
- **Space** is O(1), because the method stores two references and a counter.

```java run
import java.util.*;

public final class CycleSmall {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the slow steps taken until slow == fast, or -1 if they never meet.
     * Time: O(n), because the references meet or the chain ends within O(n) steps.
     * Space: O(1), because two references and a counter are stored.
     * Invariant: fast.next.next is read only after fast and fast.next are non-null.
     */
    static int stepsToMeet(Node head) {
        Node slow = head, fast = head;
        int steps = 0;
        // The first test guards fast.next, and the second guards fast.next.next.
        while (fast != null && fast.next != null) {
            slow = slow.next;                         // one step
            fast = fast.next.next;                    // two steps
            steps++;                                  // count the slow step
            if (slow == fast) return steps;           // the first equal pair
        }
        return -1;                                    // the chain ended
    }

    /** Oracle: simulates the same pointers with explicit null checks. */
    static int oracle(Node head, int limit) {
        Node s = head, f = head;
        for (int step = 1; step <= limit; step++) {
            if (f == null || f.next == null) return -1;
            s = s.next; f = f.next.next;
            if (s == f) return step;
        }
        return -1;
    }

    /** Builds a list from n nodes; pos is the index the last node points at, or -1 for no cycle. */
    static Node build(int n, int pos) {
        if (n == 0) return null;
        Node[] nodes = new Node[n];
        for (int i = 0; i < n; i++) nodes[i] = new Node(i, null);
        for (int i = 0; i + 1 < n; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0) nodes[n - 1].next = nodes[pos];
        return nodes[0];
    }

    public static void main(String[] args) {
        // Example 1: a self-loop meets after one step.
        if (stepsToMeet(build(1, 0)) != 1) throw new AssertionError("self");
        // Example 2: a two-node cycle meets after two steps.
        if (stepsToMeet(build(2, 0)) != 2) throw new AssertionError("two");
        // A single node with next null, and the empty list, never meet.
        if (stepsToMeet(build(1, -1)) != -1 || stepsToMeet(null) != -1) throw new AssertionError("no cycle");
        // Every size and cycle position up to 12 must match the oracle.
        for (int n = 0; n <= 12; n++)
            for (int pos = -1; pos < n; pos++)
                if (stepsToMeet(build(n, pos)) != oracle(build(n, pos), 1000)) throw new AssertionError("n=" + n + " pos=" + pos);
    }
}
```

#### Solution: [Recognize] Linked List Cycle II (LeetCode 142)
<!-- id: ll-cycle-entry -->

**Approach.**
The first phase finds a meeting node inside the cycle with the two-speed walk. If the walk ends, the method returns `null`. In the second phase, a reference `walker` starts at the head and a reference `meet` stays at the meeting node. Both move one node per step until they are equal. With `a` nodes before the cycle entry and `t` slow steps at the meeting, the value `t` is a multiple of the cycle length. The meeting node is `t - a` steps past the entry, so `a` more steps put it exactly on the entry, and `walker` also needs `a` steps to reach the entry.

The invariant of the second phase is that the distance from `walker` to the entry equals the distance from `meet` to the entry, measured along the chain and the cycle, so equal steps keep them equal until both stand on the entry.

**Complexity.**
- **Time** is O(n), because the first phase takes at most `a + L` steps and the second phase takes `a` steps.
- **Space** is O(1), because the method stores three references.

```java run
import java.util.*;

public final class CycleEntryNode {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the first node of the cycle, or null when no cycle exists.
     * Time: O(n), because the two phases take at most a + L and a steps.
     * Space: O(1), because three references are stored.
     * Invariant: walker and meet are equally far from the cycle entry.
     */
    static Node detectCycle(Node head) {
        Node slow = head, fast = head, meet = null;
        // Phase one: find a node inside the cycle, if any.
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) { meet = slow; break; }
        }
        if (meet == null) return null;                // the chain ends, so no cycle exists
        Node walker = head;
        // Phase two: both references move one step until they meet at the entry.
        while (walker != meet) { walker = walker.next; meet = meet.next; }
        return walker;
    }

    /** Builds a list from n nodes; pos is the index the last node points at, or -1 for no cycle. */
    static Node[] build(int n, int pos) {
        Node[] nodes = new Node[n];
        for (int i = 0; i < n; i++) nodes[i] = new Node(i % 3, null);   // repeated values test identity
        for (int i = 0; i + 1 < n; i++) nodes[i].next = nodes[i + 1];
        if (n > 0 && pos >= 0) nodes[n - 1].next = nodes[pos];
        return nodes;
    }

    /** Oracle: the first node seen twice by an identity-set walk. */
    static Node oracle(Node head) {
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node c = head; c != null; c = c.next) if (!seen.add(c)) return c;
        return null;
    }

    public static void main(String[] args) {
        // Example 1: the entry is the node at index 1.
        Node[] a = build(4, 1);
        if (detectCycle(a[0]) != a[1]) throw new AssertionError("ex1");
        // Example 2: the entry is the head node.
        a = build(2, 0);
        if (detectCycle(a[0]) != a[0]) throw new AssertionError("ex2");
        // No cycle returns null.
        if (detectCycle(build(3, -1)[0]) != null || detectCycle(null) != null) throw new AssertionError("none");
        // Every size and position up to 15 must match the identity-set oracle.
        for (int n = 1; n <= 15; n++)
            for (int pos = -1; pos < n; pos++) {
                Node[] x = build(n, pos);
                if (detectCycle(x[0]) != oracle(x[0])) throw new AssertionError("n=" + n + " pos=" + pos);
            }
    }
}
```
