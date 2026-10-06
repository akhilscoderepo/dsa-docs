<!-- solutions-for: 09-fixed-gap-kth-from-end -->
### Solutions For A Fixed Gap

#### Solution: [Build] Kth Node From End (Author exercise)
<!-- id: ll-kth-from-end -->

**Approach.**
The leading reference moves `k` nodes from the head while the trailing reference stays on the head. This opens a gap of `k` nodes. Then both references move one node per turn until the leading reference is `null`. The leading reference moves `n - k` times in this phase, so the trailing reference ends at index `n - k`, which is the `k`th node from the end.

The invariant is that the gap between the references stays `k` nodes after every move of the second phase. The method returns the value at the trailing reference.

**Complexity.**
- **Time** is O(n), because the leading reference makes `n` hops in total.
- **Space** is O(1), because the method stores two references.

```java run
import java.util.*;

public final class KthFromEnd {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the value of the k-th node from the end, for 1 <= k <= n.
     * Time: O(n), because the leading reference makes n hops.
     * Space: O(1), because two references are stored.
     * Invariant: lead is k nodes ahead of trail after the first loop.
     */
    static int kthFromEnd(Node head, int k) {
        Node lead = head, trail = head;
        // First phase: open a gap of k nodes.
        for (int i = 0; i < k; i++) lead = lead.next;
        // Second phase: both move one node per turn, so the gap stays k.
        while (lead != null) { lead = lead.next; trail = trail.next; }
        return trail.val;                             // k nodes from trail to the end
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    public static void main(String[] args) {
        // Example 1: the second node from the end of 1..5 is 4.
        if (kthFromEnd(build(new int[] {1, 2, 3, 4, 5}), 2) != 4) throw new AssertionError("ex1");
        // Example 2: the first node from the end is the last node.
        if (kthFromEnd(build(new int[] {1, 2, 3, 4, 5}), 1) != 5) throw new AssertionError("ex2");
        // k equal to the length returns the head.
        if (kthFromEnd(build(new int[] {7, 8, 9}), 3) != 7) throw new AssertionError("head");
        // Random lists and k must match array index n - k.
        Random rnd = new Random(81);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            int k = 1 + rnd.nextInt(n);
            if (kthFromEnd(build(a), k) != a[n - k]) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Predecessor Of Kth From End (Author exercise)
<!-- id: ll-kth-predecessor -->

**Approach.**
The method places a dummy node before the head and starts the trailing reference there. The leading reference starts at the head and moves `k` nodes. Then both move together until the leading reference is `null`. The leading reference makes `n - k` more moves, so the trailing reference ends at position `n - k - 1` counting the head as position 0 and the dummy node as position -1. That node is the predecessor of the target. If it is the dummy node, the target is the head, and the method returns -1.

The invariant is that the trailing reference is always `k + 1` positions behind the leading reference, counting the leading reference's position.

**Complexity.**
- **Time** is O(n), because the leading reference makes `n` hops.
- **Space** is O(1), because the method allocates one dummy node.

```java run
import java.util.*;

public final class KthPredecessor {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the value just before the k-th node from the end, or -1 when that node is the head.
     * Time: O(n), because the leading reference makes n hops.
     * Space: O(1), because one dummy node is allocated.
     * Invariant: trail stays one node behind the k-th node from the end.
     */
    static int predecessorValue(Node head, int k) {
        Node dummy = new Node(-1, head);              // stands in for the node before the head
        Node trail = dummy, lead = head;
        // Open a gap of k nodes between lead and the target.
        for (int i = 0; i < k; i++) lead = lead.next;
        // Move both until lead leaves the list.
        while (lead != null) { lead = lead.next; trail = trail.next; }
        return trail == dummy ? -1 : trail.val;       // the dummy node means the target is the head
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    public static void main(String[] args) {
        // Example 1: before the node 4 stands the node 3.
        if (predecessorValue(build(new int[] {1, 2, 3, 4, 5}), 2) != 3) throw new AssertionError("ex1");
        // Example 2: k = n makes the target the head, so the answer is -1.
        if (predecessorValue(build(new int[] {1, 2, 3, 4, 5}), 5) != -1) throw new AssertionError("ex2");
        // k = 1 returns the second last value.
        if (predecessorValue(build(new int[] {4, 5, 6}), 1) != 5) throw new AssertionError("last");
        // Random lists and k must match array index n - k - 1.
        Random rnd = new Random(82);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            int k = 1 + rnd.nextInt(n);
            int expect = n - k - 1 < 0 ? -1 : a[n - k - 1];
            if (predecessorValue(build(a), k) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] K Equals Length (Author exercise)
<!-- id: ll-kth-boundary -->

**Approach.**
The method opens the gap with a loop that tests the leading reference before each move. If the leading reference is `null` before `k` moves are done, the list has fewer than `k` nodes, and the method returns -1. After a successful advance, it moves both references and counts the trailing reference's hops. When the list has exactly `k` nodes, the leading reference is `null` right after the advance, the second loop makes no move, and the count is 0, the index of the head.

The invariant is that the count equals the index of the trailing reference, and the gap is `k` after every second-phase move.

**Complexity.**
- **Time** is O(n), because the leading reference makes at most `n` hops.
- **Space** is O(1), because the method stores two references and a counter.

```java run
import java.util.*;

public final class KthBoundary {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the 0-based index of the k-th node from the end, or -1 if fewer than k nodes exist.
     * Time: O(n), because the leading reference makes at most n hops.
     * Space: O(1), because two references and a counter are stored.
     * Invariant: index equals the number of hops made by trail.
     */
    static int indexFromEnd(Node head, int k) {
        Node lead = head, trail = head;
        // The test runs before every move, so a short list is caught at once.
        for (int i = 0; i < k; i++) {
            if (lead == null) return -1;
            lead = lead.next;
        }
        int index = 0;
        // With exactly k nodes lead is already null, so the loop runs zero times and index stays 0.
        while (lead != null) { lead = lead.next; trail = trail.next; index++; }
        return index;
    }

    static Node build(int n) {
        Node head = null;
        // Build n nodes; the value is irrelevant to the index.
        for (int i = 0; i < n; i++) head = new Node(i, head);
        return head;
    }

    public static void main(String[] args) {
        // Example 1: k equals the length, so the target is the head at index 0.
        if (indexFromEnd(build(3), 3) != 0) throw new AssertionError("ex1");
        // Example 2: k is larger than the length.
        if (indexFromEnd(build(3), 4) != -1) throw new AssertionError("ex2");
        // The empty list has no k-th node for any k.
        if (indexFromEnd(null, 1) != -1) throw new AssertionError("empty");
        // Every length and k up to 15 must match n - k, or -1 when k > n.
        for (int n = 0; n <= 15; n++)
            for (int k = 1; k <= 16; k++)
                if (indexFromEnd(build(n), k) != (k > n ? -1 : n - k)) throw new AssertionError("n=" + n + " k=" + k);
    }
}
```

#### Solution: [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-gap -->

**Approach.**
The method places a dummy node before the head. The leading reference starts at the head, and the trailing reference starts at the dummy node. The leading reference moves `n` nodes, and if it becomes `null` before that, the list is shorter than `n`, so the method returns the original head. Then both references move until the leading reference is `null`, and the trailing reference stands on the predecessor of the target. One write, `trail.next = trail.next.next`, removes the target. The method returns `dummy.next`, which also covers the case where the target was the head.

The invariant is that the trailing reference is the predecessor of the node that is `n`th from the end whenever the leading reference is `null`. The method makes one pass and never computes the length.

**Complexity.**
- **Time** is O(L), because the leading reference makes at most `L` hops.
- **Space** is O(1), because the method allocates one dummy node.

```java run
import java.util.*;

public final class RemoveNthGap {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Removes the n-th node from the end in one pass, or changes nothing when n exceeds the length.
     * Time: O(L), because the leading reference makes at most L hops.
     * Space: O(1), because one dummy node is allocated.
     * Invariant: trail is the predecessor of the n-th node from the end when lead is null.
     */
    static Node removeNthFromEnd(Node head, int n) {
        Node dummy = new Node(0, head);
        Node lead = head, trail = dummy;
        // Open the gap, and stop if the list is shorter than n.
        for (int i = 0; i < n; i++) {
            if (lead == null) return head;
            lead = lead.next;
        }
        // Move both until lead leaves the list.
        while (lead != null) { lead = lead.next; trail = trail.next; }
        trail.next = trail.next.next;                 // skip the target; this also removes the head
        return dummy.next;
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
        // Example 1: the second node from the end of 1..5 is removed.
        if (!read(removeNthFromEnd(build(new int[] {1, 2, 3, 4, 5}), 2)).equals(List.of(1, 2, 3, 5))) throw new AssertionError("ex1");
        // Example 2: n larger than the length changes nothing.
        if (!read(removeNthFromEnd(build(new int[] {1, 2}), 3)).equals(List.of(1, 2))) throw new AssertionError("long n");
        // Removing the only node gives the empty list.
        if (removeNthFromEnd(build(new int[] {1}), 1) != null) throw new AssertionError("single");
        // The empty list stays empty.
        if (removeNthFromEnd(null, 2) != null) throw new AssertionError("empty");
        // Random lists and n (including n > length) must match ArrayList.remove(size - n).
        Random rnd = new Random(83);
        for (int t = 0; t < 2000; t++) {
            int len = rnd.nextInt(10);
            int[] a = new int[len];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < len; i++) { a[i] = rnd.nextInt(100); o.add(a[i]); }
            int n = 1 + rnd.nextInt(12);
            if (n <= len) o.remove(len - n);
            if (!read(removeNthFromEnd(build(a), n)).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```
