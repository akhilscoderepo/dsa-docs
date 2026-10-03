<!-- solutions-for: 06-cycle-entry -->
### Cycle Entry

#### Solution: [Build] Linked List Cycle (LeetCode 141)
<!-- id: ll-detect-cycle -->

**Approach.** Start `slow` and `fast` at the head. While `fast` and `fast.next` are both non-null, advance `slow` by one node and `fast` by two, and report a cycle if they become the same node object. If the loop ends because `fast` reached the end, the list is finite. The comparison is on references, so repeated values cannot cause a false report. The assertions build lists from `values` and `pos` and compare with a detector that records visited node objects in an identity set, including lists whose values are all equal.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.IdentityHashMap;
import java.util.Random;

public final class DetectCycle {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values, int pos) {
        if (values.length == 0) return null;
        Node[] nodes = new Node[values.length];
        for (int i = 0; i < nodes.length; i++) nodes[i] = new Node(values[i]);
        for (int i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0) nodes[nodes.length - 1].next = nodes[pos];
        return nodes[0];
    }
    static boolean hasCycle(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
    static boolean notebook(Node head) {
        IdentityHashMap<Node, Boolean> seen = new IdentityHashMap<>();
        for (Node p = head; p != null; p = p.next) {
            if (seen.containsKey(p)) return true;
            seen.put(p, true);
        }
        return false;
    }

    public static void main(String[] args) {
        if (!hasCycle(build(new int[]{8, 1, 6, 4, 9}, 2))) throw new AssertionError("example 1");
        if (hasCycle(build(new int[]{5, 7}, -1))) throw new AssertionError("example 2");
        if (hasCycle(build(new int[]{3, 3, 3, 3}, -1))) throw new AssertionError("equal values do not make a cycle");
        if (hasCycle(null)) throw new AssertionError("empty list");
        Random rnd = new Random(1421);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int pos = n == 0 ? -1 : rnd.nextInt(n + 1) - 1;
            Node head = build(a, pos);
            if (hasCycle(head) != notebook(head)) throw new AssertionError("disagrees with the identity notebook");
            if (hasCycle(head) != (pos >= 0)) throw new AssertionError("disagrees with the encoding");
        }
    }
}
```

#### Solution: [Vary] Measure Cycle Length (Author exercise)
<!-- id: ll-cycle-length -->

**Approach.** Run the two-speed chase to find a collision node inside the loop, and return 0 if the chase ends without one. From the collision node, walk forward counting steps until the walk returns to it. Every node of the loop is visited exactly once on the way round, so the count is the loop length. The assertions compare with the length derived from the encoding, which is `n - pos` when `pos >= 0`, and with a notebook that records the visit index of each node object.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.IdentityHashMap;
import java.util.Random;

public final class CycleLength {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values, int pos) {
        if (values.length == 0) return null;
        Node[] nodes = new Node[values.length];
        for (int i = 0; i < nodes.length; i++) nodes[i] = new Node(values[i]);
        for (int i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0) nodes[nodes.length - 1].next = nodes[pos];
        return nodes[0];
    }
    static Node collision(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return slow;
        }
        return null;
    }
    static int cycleLength(Node head) {
        Node meet = collision(head);
        if (meet == null) return 0;
        int length = 1;
        for (Node cur = meet.next; cur != meet; cur = cur.next) length++;
        return length;
    }
    static int notebookLength(Node head) {
        IdentityHashMap<Node, Integer> seen = new IdentityHashMap<>();
        int i = 0;
        for (Node p = head; p != null; p = p.next) {
            if (seen.containsKey(p)) return i - seen.get(p);
            seen.put(p, i++);
        }
        return 0;
    }

    public static void main(String[] args) {
        if (cycleLength(build(new int[]{8, 1, 6, 4, 9}, 2)) != 3) throw new AssertionError("example 1");
        if (cycleLength(build(new int[]{5, 7}, -1)) != 0) throw new AssertionError("example 2");
        if (cycleLength(build(new int[]{1}, 0)) != 1) throw new AssertionError("a self-loop has length 1");
        Random rnd = new Random(1422);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            int pos = n == 0 ? -1 : rnd.nextInt(n + 1) - 1;
            Node head = build(a, pos);
            int expected = pos >= 0 ? n - pos : 0;
            if (cycleLength(head) != expected) throw new AssertionError("disagrees with the encoding");
            if (cycleLength(head) != notebookLength(head)) throw new AssertionError("disagrees with the notebook");
        }
    }
}
```

#### Solution: [Boundary] Self-Loop And Two-Node Cycle (Author exercise)
<!-- id: ll-cycle-rounds -->

**Approach.** Guard every double step with `fast != null && fast.next != null`, advance `slow` once and `fast` twice, count the round, and stop if the two references are equal. A single node pointing at itself puts both references on that node in round one, and an acyclic pair sends `fast` to null in round one, so `[1, 1]` and `[0, 1]` come out of the same loop with no special case. The assertions compare the rounds with a simulation over integer positions, where the successor of index `i` is `i + 1`, or `pos` for the last index.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class CycleRounds {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values, int pos) {
        Node[] nodes = new Node[values.length];
        for (int i = 0; i < nodes.length; i++) nodes[i] = new Node(values[i]);
        for (int i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0) nodes[nodes.length - 1].next = nodes[pos];
        return nodes[0];
    }
    static int[] chase(Node head) {
        Node slow = head, fast = head;
        int rounds = 0;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            rounds++;
            if (slow == fast) return new int[]{1, rounds};
        }
        return new int[]{0, rounds};
    }
    static int[] byIndices(int n, int pos) {
        int slow = 0, fast = 0, rounds = 0;
        while (true) {
            if (fast == -1 || next(fast, n, pos) == -1) return new int[]{0, rounds};
            slow = next(slow, n, pos);
            fast = next(next(fast, n, pos), n, pos);
            rounds++;
            if (slow == fast) return new int[]{1, rounds};
        }
    }
    static int next(int i, int n, int pos) {
        if (i < n - 1) return i + 1;
        return pos;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(chase(build(new int[]{4}, 0)), new int[]{1, 1})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(chase(build(new int[]{4, 9}, -1)), new int[]{0, 1})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(chase(build(new int[]{4, 9}, 0)), new int[]{1, 2})) throw new AssertionError("two-node cycle");
        Random rnd = new Random(1423);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int pos = rnd.nextInt(n + 1) - 1;
            if (!java.util.Arrays.equals(chase(build(a, pos)), byIndices(n, pos))) throw new AssertionError("disagrees with the index simulation on n=" + n + " pos=" + pos);
        }
    }
}
```

#### Solution: [Recognize] Linked List Cycle II (LeetCode 142)
<!-- id: ll-cycle-entry -->

**Approach.** Find the collision node with the two-speed chase and return -1 if there is none. Then place a probe at the head and advance the probe and the collision reference one node at a time until they are the same node. If the head is `a` nodes before the entry and the loop has `c` nodes, the two references have walked a total of a multiple of `c` plus `a` when `slow` met `fast`, so `a` more steps bring the slow reference to the entry, which is where the probe arrives as well. The returned node is mapped back to its index. The assertions compare with the encoding, which says that the entry is index `pos`, and use lists of equal values, where only identity can decide.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class CycleEntry {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node[] nodesOf(int[] values, int pos) {
        Node[] nodes = new Node[values.length];
        for (int i = 0; i < nodes.length; i++) nodes[i] = new Node(values[i]);
        for (int i = 0; i + 1 < nodes.length; i++) nodes[i].next = nodes[i + 1];
        if (pos >= 0 && nodes.length > 0) nodes[nodes.length - 1].next = nodes[pos];
        return nodes;
    }
    static Node entry(Node head) {
        Node slow = head, fast = head;
        Node meet = null;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) { meet = slow; break; }
        }
        if (meet == null) return null;
        Node probe = head;
        while (probe != meet) {
            probe = probe.next;
            meet = meet.next;
        }
        return probe;
    }
    static int entryIndex(int[] values, int pos) {
        Node[] nodes = nodesOf(values, pos);
        Node found = entry(nodes.length == 0 ? null : nodes[0]);
        if (found == null) return -1;
        for (int i = 0; i < nodes.length; i++) if (nodes[i] == found) return i;
        throw new AssertionError("the entry must be one of the nodes");
    }

    public static void main(String[] args) {
        if (entryIndex(new int[]{7, 3, 5, 2, 6, 8}, 1) != 1) throw new AssertionError("example 1");
        if (entryIndex(new int[]{4, 4, 4}, 2) != 2) throw new AssertionError("example 2");
        if (entryIndex(new int[]{4, 4, 4}, -1) != -1) throw new AssertionError("equal values without a cycle");
        Random rnd = new Random(1424);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            int pos = n == 0 ? -1 : rnd.nextInt(n + 1) - 1;
            if (entryIndex(a, pos) != pos) throw new AssertionError("wrong entry for n=" + n + " pos=" + pos);
        }
    }
}
```
