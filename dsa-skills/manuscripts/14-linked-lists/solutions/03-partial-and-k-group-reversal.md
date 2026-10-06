<!-- solutions-for: 03-partial-and-k-group-reversal -->
### Solutions For Reversing Blocks

#### Solution: [Build] Reverse Exactly Two Nodes (Author exercise)
<!-- id: ll-two-nodes -->

**Approach.**
The method names the three nodes it needs: `a = pred.next`, `b = a.next`, and `after = b.next`. Then it makes three writes. The write `a.next = after` joins the node `a` to the rest of the list. The write `b.next = a` turns the link between the two nodes around. The write `pred.next = b` joins the predecessor to the new first node of the pair. The method reads `after` before any write, so the suffix stays reachable.

The invariant is that every node after `pred` stays reachable from a local variable until its final link is written.

**Complexity.**
- **Time** is O(1), because the method makes three reads and three writes.
- **Space** is O(1), because it stores three references.

```java run
import java.util.*;

public final class TwoNodes {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Swaps the two nodes that follow pred.
     * Time: O(1), because three reads and three writes run.
     * Space: O(1), because three references are stored.
     * Invariant: after is read before any write, so the suffix stays reachable.
     */
    static void swapAfter(Node pred) {
        Node a = pred.next;                           // first node of the pair
        Node b = a.next;                              // second node of the pair
        Node after = b.next;                          // first node after the pair, possibly null
        a.next = after;                               // the old first node now ends the pair
        b.next = a;                                   // turn the link between the pair around
        pred.next = b;                                // the predecessor reaches the new first node
    }

    static Node build(int[] x) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = x.length - 1; i >= 0; i--) head = new Node(x[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read all values in order.
        for (Node c = head; c != null; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: the pair after the node 1 swaps.
        Node h = build(new int[] {1, 2, 3, 4});
        swapAfter(h);
        if (!read(h).equals(List.of(1, 3, 2, 4))) throw new AssertionError("ex1");
        // Example 2: the pair ends the list, so after is null.
        h = build(new int[] {7, 8, 9});
        swapAfter(h);
        if (!read(h).equals(List.of(7, 9, 8))) throw new AssertionError("ex2");
        // Random lists with a random predecessor must match swapping two ArrayList entries.
        Random rnd = new Random(21);
        for (int t = 0; t < 500; t++) {
            int n = 3 + rnd.nextInt(8);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(100); o.add(a[i]); }
            int p = rnd.nextInt(n - 2);
            Node head = build(a);
            Node pred = head;
            for (int i = 0; i < p; i++) pred = pred.next;
            Collections.swap(o, p + 1, p + 2);
            swapAfter(pred);
            if (!read(head).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Reverse Linked List II (LeetCode 92)
<!-- id: ll-reverse-range-clamped -->

**Approach.**
One walk counts the length `n`. The last position of the block is `last = min(to, n - 1)`. If `from > last`, the block is empty and the method returns `head` untouched. Otherwise the block holds `last - from + 1` nodes. The helper `reverseFirst` reverses that many nodes and links the old block head to the node after the block. When `from` is 0, the helper's result is the new head. Otherwise the method walks to the node before the block and writes its `next`.

The invariant is that the helper returns the new block head with the block tail already linked to the suffix, so only the left boundary needs a write.

**Complexity.**
- **Time** is O(n), because the length walk, the walk to the block and the reversal each touch at most `n` nodes.
- **Space** is O(1), because the code stores a few references.

```java run
import java.util.*;

public final class ReverseRangeClamped {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Reverses k nodes from start and links the old first node to the node after them.
     * Time: O(k), because each node moves once.
     * Space: O(1), because three references are stored.
     * Invariant: the moved nodes form the reversed prefix, and curr starts the unmoved rest.
     */
    static Node reverseFirst(Node start, int k) {
        Node prev = null;
        Node curr = start;
        // Exactly k nodes cross the boundary.
        for (int i = 0; i < k; i++) {
            Node saved = curr.next;                   // keep the rest reachable
            curr.next = prev;                         // redirect at the prefix
            prev = curr;                              // extend the prefix
            curr = saved;                             // shrink the rest
        }
        start.next = curr;                            // the old first node ends the block and links to the suffix
        return prev;                                  // the new first node of the block
    }

    /**
     * Reverses 0-based positions from through min(to, n - 1).
     * Time: O(n), because three walks each cover at most n nodes.
     * Space: O(1), because no node is allocated.
     * Invariant: the node before the block links to the new block head.
     */
    static Node reverseRange(Node head, int from, int to) {
        int n = 0;
        // First walk counts the nodes so the end position can be clamped.
        for (Node c = head; c != null; c = c.next) n++;
        int last = Math.min(to, n - 1);               // clamp the end to the final position
        // An empty block after clamping changes nothing.
        if (from > last) return head;
        int size = last - from + 1;                   // number of nodes in the block
        // A block that starts at position 0 has no node before it.
        if (from == 0) return reverseFirst(head, size);
        Node before = head;
        // Walk from - 1 hops so before is the node at position from - 1.
        for (int i = 0; i < from - 1; i++) before = before.next;
        before.next = reverseFirst(before.next, size);   // reconnect the left boundary
        return head;                                  // the head is unchanged when from > 0
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read all values in order.
        for (Node c = head; c != null; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: a range inside the list.
        if (!read(reverseRange(build(new int[] {1, 2, 3, 4, 5}), 1, 3)).equals(List.of(1, 4, 3, 2, 5))) throw new AssertionError("ex1");
        // Example 2: the end position is clamped to the last node.
        if (!read(reverseRange(build(new int[] {1, 2, 3}), 1, 9)).equals(List.of(1, 3, 2))) throw new AssertionError("ex2");
        // The empty list and a start past the end change nothing.
        if (reverseRange(null, 0, 3) != null) throw new AssertionError("empty");
        if (!read(reverseRange(build(new int[] {1, 2}), 5, 7)).equals(List.of(1, 2))) throw new AssertionError("past end");
        // Random lists and ranges must match reversing a clamped sublist of an ArrayList.
        Random rnd = new Random(22);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(9);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(50); o.add(a[i]); }
            int from = rnd.nextInt(12);
            int to = from + rnd.nextInt(12);
            int last = Math.min(to, n - 1);
            if (from <= last) Collections.reverse(o.subList(from, last + 1));
            if (!read(reverseRange(build(a), from, to)).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Incomplete Final Group (Author exercise)
<!-- id: ll-incomplete-group -->

**Approach.**
A read-only walk moves a probe `k` hops from `head`. If the probe reaches `null` before the `k`th hop, fewer than `k` nodes exist, and the method returns `head` with no write. If the probe completes `k` hops, the method reverses the first `k` nodes with the helper and returns the new first node. The helper links the old head to the probe node, which is the node after the group.

The invariant is that no `next` field changes unless the look-ahead has proved that `k` nodes exist.

**Complexity.**
- **Time** is O(k), because the look-ahead reads at most `k` nodes and the reversal moves `k` nodes.
- **Space** is O(1), because the code stores three references.

```java run
import java.util.*;

public final class IncompleteGroup {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Reverses the first k nodes only when k nodes exist.
     * Time: O(k), because the look-ahead and the reversal each cover k nodes.
     * Space: O(1), because three references are stored.
     * Invariant: no write happens before the look-ahead succeeds.
     */
    static Node reverseIfFull(Node head, int k) {
        Node probe = head;
        int seen = 0;
        // Read-only look-ahead: count up to k nodes without writing.
        while (probe != null && seen < k) { probe = probe.next; seen++; }
        // A short list stays exactly as it is.
        if (seen < k) return head;
        Node prev = null;
        Node curr = head;
        // Exactly k nodes move across the boundary.
        for (int i = 0; i < k; i++) {
            Node saved = curr.next;                   // keep the rest reachable
            curr.next = prev;                         // redirect at the prefix
            prev = curr;                              // extend the prefix
            curr = saved;                             // shrink the rest
        }
        head.next = curr;                             // the old head now ends the group and links to the rest
        return prev;                                  // the new first node
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read all values in order.
        for (Node c = head; c != null; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: a complete group reverses.
        if (!read(reverseIfFull(build(new int[] {1, 2, 3}), 3)).equals(List.of(3, 2, 1))) throw new AssertionError("ex1");
        // Example 2: a short list keeps its nodes and its links.
        Node h = build(new int[] {1, 2});
        Node second = h.next;
        Node r = reverseIfFull(h, 3);
        if (r != h || h.next != second || second.next != null) throw new AssertionError("short");
        // The empty list returns null.
        if (reverseIfFull(null, 2) != null) throw new AssertionError("empty");
        // Random lists must match reversing the first k entries only when n >= k.
        Random rnd = new Random(23);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(9);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(50); o.add(a[i]); }
            int k = 1 + rnd.nextInt(10);
            if (n >= k) Collections.reverse(o.subList(0, k));
            if (!read(reverseIfFull(build(a), k)).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Reverse Nodes in k-Group (LeetCode 25)
<!-- id: ll-reverse-k-group -->

**Approach.**
The method repeats the check-then-reverse step. For the current first node, a read-only look-ahead moves a probe `k` hops. If the probe stops early, the group is short and the loop ends. Otherwise `reverseFirst` reverses the group and links its old first node to the probe. The previous group's tail is the predecessor, and the method writes `pred.next` to the new group head. The first group sets the returned head instead.

After each group, the old first node is the new predecessor, and the probe node is the next first node. The invariant is that every group before `first` is final, the previous group's tail points at `first`, and no node is written before its group is known to be complete.

**Complexity.**
- **Time** is O(n), because the look-ahead reads each node once and the reversal moves each node once.
- **Space** is O(1), because the code stores a few references.

```java run
import java.util.*;

public final class ReverseKGroup {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Reverses k nodes from start and links the old first node to the node after them.
     * Time: O(k), because each node moves once.
     * Space: O(1), because three references are stored.
     * Invariant: the moved nodes form the reversed prefix.
     */
    static Node reverseFirst(Node start, int k) {
        Node prev = null;
        Node curr = start;
        // Exactly k nodes cross the boundary.
        for (int i = 0; i < k; i++) {
            Node saved = curr.next;                   // keep the rest reachable
            curr.next = prev;                         // redirect at the prefix
            prev = curr;                              // extend the prefix
            curr = saved;                             // shrink the rest
        }
        start.next = curr;                            // the old first node ends the group
        return prev;                                  // the new first node of the group
    }

    /**
     * Reverses every complete group of k nodes and leaves a short final group alone.
     * Time: O(n), because each node is read once and moved once.
     * Space: O(1), because three references are stored.
     * Invariant: groups before first are final, and the previous tail points at first.
     */
    static Node reverseKGroup(Node head, int k) {
        Node newHead = null;                          // set by the first complete group
        Node pred = null;                             // tail of the previous group
        Node first = head;                            // first node of the current group
        // Each turn handles one group, so the loop makes about n / k turns.
        while (true) {
            Node probe = first;
            int seen = 0;
            // Read-only look-ahead of at most k hops.
            while (probe != null && seen < k) { probe = probe.next; seen++; }
            // A short or empty group ends the loop with no write.
            if (seen < k) break;
            Node groupHead = reverseFirst(first, k);
            // The first group sets the head; later groups join the previous tail.
            if (pred == null) newHead = groupHead; else pred.next = groupHead;
            pred = first;                             // the old first node is the new group tail
            first = probe;                            // the next group starts after this one
        }
        // With no complete group the original head is the answer.
        return newHead == null ? head : newHead;
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read all values in order.
        for (Node c = head; c != null; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: k = 2 leaves the single last node in place.
        if (!read(reverseKGroup(build(new int[] {1, 2, 3, 4, 5}), 2)).equals(List.of(2, 1, 4, 3, 5))) throw new AssertionError("ex1");
        // Example 2: k = 3 reverses one group and leaves two nodes.
        if (!read(reverseKGroup(build(new int[] {1, 2, 3, 4, 5}), 3)).equals(List.of(3, 2, 1, 4, 5))) throw new AssertionError("ex2");
        // k = 1 changes nothing, and k larger than n changes nothing.
        if (!read(reverseKGroup(build(new int[] {1, 2, 3}), 1)).equals(List.of(1, 2, 3))) throw new AssertionError("k1");
        if (!read(reverseKGroup(build(new int[] {1, 2, 3}), 5)).equals(List.of(1, 2, 3))) throw new AssertionError("big k");
        // Random lists must match reversing each complete chunk of an ArrayList.
        Random rnd = new Random(24);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(50); o.add(a[i]); }
            int k = 1 + rnd.nextInt(5);
            for (int s = 0; s + k <= n; s += k) Collections.reverse(o.subList(s, s + k));
            if (!read(reverseKGroup(build(a), k)).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```
