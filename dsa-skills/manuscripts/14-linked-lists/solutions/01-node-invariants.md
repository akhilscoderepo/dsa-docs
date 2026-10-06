<!-- solutions-for: 01-node-invariants -->
### Solutions For Following References

#### Solution: [Build] Traverse And Count (Author exercise)
<!-- id: ll-traverse-count -->

**Approach.**
The method keeps one reference `curr` that starts at `head`. Each loop turn adds one to the count and the node's value to the sum, then moves `curr` to `curr.next`. The loop ends when `curr` is `null`, which also covers the empty list, because `head` is already `null` and the body never runs.

The invariant is that before each turn the count and sum cover exactly the nodes strictly before `curr`. No field is written, so the list is unchanged.

**Complexity.**
- **Time** is O(n), because the loop makes one hop per node and does constant work at each node.
- **Space** is O(1), because the method stores two integers and one reference.

```java run
import java.util.*;

public final class TraverseCount {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns {count, sum} of the list starting at head.
     * Time: O(n), because each node is visited once.
     * Space: O(1), because only counters and one reference are stored.
     * Invariant: count and sum cover the nodes before curr.
     */
    static long[] countAndSum(Node head) {
        long count = 0;                               // nodes visited so far
        long sum = 0;                                 // values added so far
        // One hop per node; the loop ends at null, so n nodes cost n turns.
        for (Node curr = head; curr != null; curr = curr.next) {
            count++;                                  // curr is one more node
            sum += curr.val;                          // add its value to the sum
        }
        // The pair is the whole answer; nothing was written to any node.
        return new long[] {count, sum};
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each new node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    public static void main(String[] args) {
        // The example list gives count 3 and sum 20.
        long[] r = countAndSum(build(new int[] {4, 7, 9}));
        if (r[0] != 3 || r[1] != 20) throw new AssertionError("example");
        // The empty list gives count 0 and sum 0, with no null dereference.
        r = countAndSum(null);
        if (r[0] != 0 || r[1] != 0) throw new AssertionError("empty");
        // Random lists must agree with an array oracle, and the walk must not change the values.
        Random rnd = new Random(1);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            long s = 0;
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(21) - 10; s += a[i]; }
            Node h = build(a);
            r = countAndSum(h);
            if (r[0] != n || r[1] != s) throw new AssertionError("random " + t);
            int i = 0;
            for (Node c = h; c != null; c = c.next) if (c.val != a[i++]) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Vary] Insert After A Node (Author exercise)
<!-- id: ll-insert-after -->

**Approach.**
Before any write, the method copies `node.next` into `saved`. Then it sets `node.next` to a new node whose own `next` is `saved`. At the instant between the two writes, the old successor has two references, so it never becomes unreachable.

The invariant is that every node that followed `node` before the call stays reachable after each statement. Writing `node.next` first and reading it second would make the new node point to itself and lose the old suffix.

**Complexity.**
- **Time** is O(1), because the method follows no reference beyond `node.next`.
- **Space** is O(1), because it allocates one node.

```java run
import java.util.*;

public final class InsertAfter {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Inserts a node holding x right after node.
     * Time: O(1), because only node.next is read and written.
     * Space: O(1), because one node is allocated.
     * Invariant: the old successor stays reachable after every statement.
     */
    static void insertAfter(Node node, int x) {
        Node saved = node.next;                       // second reference to the old successor
        node.next = new Node(x, saved);               // the new node takes over the old chain
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read every value from the head; a cycle would never end, so the oracle limit guards it.
        for (Node c = head; c != null && out.size() < 1000; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // Inserting after the middle node keeps the suffix: 4,7,9 becomes 4,7,5,9.
        Node h = build(new int[] {4, 7, 9});
        insertAfter(h.next, 5);
        if (!read(h).equals(List.of(4, 7, 5, 9))) throw new AssertionError("middle");
        // Inserting after the last node appends, because the saved successor is null.
        h = build(new int[] {4, 7, 9});
        insertAfter(h.next.next, 1);
        if (!read(h).equals(List.of(4, 7, 9, 1))) throw new AssertionError("tail");
        // Random positions must match list.add(index + 1, x) on an ArrayList oracle.
        Random rnd = new Random(2);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            List<Integer> oracle = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(100); oracle.add(a[i]); }
            Node head = build(a);
            int pos = rnd.nextInt(n);
            Node at = head;
            for (int i = 0; i < pos; i++) at = at.next;
            int x = rnd.nextInt(100);
            insertAfter(at, x);
            oracle.add(pos + 1, x);
            if (!read(head).equals(oracle)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty And Singleton Lists (Author exercise)
<!-- id: ll-empty-singleton -->

**Approach.**
The method `secondValue` tests `head` first, then `head.next`, because each read is legal only when the reference before it is not `null`. It returns -1 when either test fails. The method `appendValue` returns a one-node list when `head` is `null`, because the empty list has no last node to change. Otherwise it walks until `curr.next` is `null`, which stops on the last node, and links the new node there.

The invariant is that every dereference follows a test that the reference is not `null`. The returned head is the old head unless the list was empty.

**Complexity.**
- **Time** is O(1) for `secondValue` and O(n) for `appendValue`, because only the append walks to the last node.
- **Space** is O(1), because both methods store one reference and at most one new node.

```java run
import java.util.*;

public final class EmptySingleton {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the second value, or -1 when fewer than two nodes exist.
     * Time: O(1), because two reads are made.
     * Space: O(1), because nothing is stored.
     * Invariant: head.next is read only after head is known to be non-null.
     */
    static int secondValue(Node head) {
        // Either test failing means there is no second node.
        if (head == null || head.next == null) return -1;
        return head.next.val;                         // both references are non-null here
    }

    /**
     * Appends x after the last node and returns the head.
     * Time: O(n), because the walk visits every node once.
     * Space: O(1), because one node is allocated.
     * Invariant: curr is never null inside the loop.
     */
    static Node appendValue(Node head, int x) {
        // The empty list has no last node, so the new node becomes the head.
        if (head == null) return new Node(x, null);
        Node curr = head;
        // Stop on the last node, whose next is null, so the write below has a target.
        while (curr.next != null) curr = curr.next;
        curr.next = new Node(x, null);                // link the new node after the last node
        return head;                                  // the head is unchanged for a non-empty list
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read all values in order from the head.
        for (Node c = head; c != null; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // The empty list has no second value, and appending creates the head.
        if (secondValue(null) != -1) throw new AssertionError("empty second");
        if (!read(appendValue(null, 6)).equals(List.of(6))) throw new AssertionError("empty append");
        // A one-node list has no second value, and appending adds a second node.
        if (secondValue(build(new int[] {3})) != -1) throw new AssertionError("single second");
        if (!read(appendValue(build(new int[] {3}), 6)).equals(List.of(3, 6))) throw new AssertionError("single append");
        // Random lists must agree with an ArrayList oracle.
        Random rnd = new Random(3);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(6);
            int[] a = new int[n];
            List<Integer> oracle = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(100); oracle.add(a[i]); }
            int expectSecond = n >= 2 ? a[1] : -1;
            if (secondValue(build(a)) != expectSecond) throw new AssertionError("second " + t);
            int x = rnd.nextInt(100);
            oracle.add(x);
            if (!read(appendValue(build(a), x)).equals(oracle)) throw new AssertionError("append " + t);
        }
    }
}
```

#### Solution: [Recognize] Remove Linked List Elements (LeetCode 203)
<!-- id: ll-remove-elements -->

**Approach.**
First the method drops every leading node whose value equals `target`, by moving `head` forward, because no earlier node exists to rewrite. After that the head holds a kept value or is `null`. Then a reference `prev` holds the last kept node, and a walk reads `prev.next`. If that node matches, `prev.next` skips it by taking its successor. If it does not match, `prev` advances.

The invariant is that the chain from `head` to `prev` holds only kept values, and `prev.next` starts the unchecked suffix. A deleted node is unlinked and its successor is read from the field before the skip, so the suffix stays reachable.

**Complexity.**
- **Time** is O(n), because each node is read once and each skip is a single write.
- **Space** is O(1), because the method stores two references and allocates nothing.

```java run
import java.util.*;

public final class RemoveElements {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Removes every node with value target and returns the new head.
     * Time: O(n), because each node is examined once.
     * Space: O(1), because no node is allocated.
     * Invariant: head to prev holds kept values, and prev.next starts the unchecked suffix.
     */
    static Node removeElements(Node head, int target) {
        // Leading matches have no earlier node to rewrite, so the head itself moves forward.
        while (head != null && head.val == target) head = head.next;
        Node prev = head;                             // last node known to be kept
        // Each turn either skips prev.next or advances prev, so the loop makes at most n turns.
        while (prev != null && prev.next != null) {
            if (prev.next.val == target) prev.next = prev.next.next;   // skip the match, reading its successor first
            else prev = prev.next;                    // keep the node and advance
        }
        return head;                                  // the head is the first kept node, or null
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read all values in order from the head.
        for (Node c = head; c != null; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // The first example removes the 6 nodes in the middle and at the end.
        if (!read(removeElements(build(new int[] {1, 2, 6, 3, 4, 5, 6}), 6)).equals(List.of(1, 2, 3, 4, 5))) throw new AssertionError("ex1");
        // A list of only matches becomes empty.
        if (removeElements(build(new int[] {7, 7, 7, 7}), 7) != null) throw new AssertionError("all");
        // The empty list stays empty.
        if (removeElements(null, 1) != null) throw new AssertionError("empty");
        // Random lists with few distinct values must agree with removeIf on an ArrayList.
        Random rnd = new Random(4);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            List<Integer> oracle = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = 1 + rnd.nextInt(3); oracle.add(a[i]); }
            int target = 1 + rnd.nextInt(3);
            oracle.removeIf(v -> v == target);
            if (!read(removeElements(build(a), target)).equals(oracle)) throw new AssertionError("random " + t);
        }
    }
}
```
