<!-- solutions-for: 02-reverse -->
### Solutions For Reversing A List

#### Solution: [Build] Reverse Three Nodes By Hand (Author exercise)
<!-- id: ll-reverse-three -->

**Approach.**
The method performs three rounds of the four-step move without a loop. Each round copies the successor of `curr`, points `curr` at `prev`, and then advances `prev` and `curr`. After the third round, `prev` holds the old last node, so it is the new head.

The invariant is that after round `k`, the first `k` nodes form the reversed prefix and the rest are untouched. The old head ends with `next` equal to `null`, because the first redirect used the initial `null` prefix.

**Complexity.**
- **Time** is O(1), because the code performs three fixed rounds.
- **Space** is O(1), because it stores three references.

```java run
import java.util.*;

public final class ReverseThree {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Reverses a list of exactly three nodes by hand.
     * Time: O(1), because three rounds run.
     * Space: O(1), because three references are stored.
     * Invariant: after round k, k nodes form the reversed prefix.
     */
    static Node reverseThree(Node head) {
        Node prev = null;                             // the reversed prefix is empty
        Node curr = head;                             // the suffix is the whole list
        // Round 1: move the first node across.
        Node saved = curr.next; curr.next = prev; prev = curr; curr = saved;
        // Round 2: move the second node across.
        saved = curr.next; curr.next = prev; prev = curr; curr = saved;
        // Round 3: move the third node across; curr becomes null afterward.
        saved = curr.next; curr.next = prev; prev = curr; curr = saved;
        return prev;                                  // the old last node is the new head
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
        // The first example reverses 1,2,3.
        Node h = build(new int[] {1, 2, 3});
        Node first = h, last = h.next.next;
        Node r = reverseThree(h);
        if (!read(r).equals(List.of(3, 2, 1))) throw new AssertionError("ex1");
        // Nodes keep their identity: the old last node is the new head, the old head is the tail.
        if (r != last || first.next != null) throw new AssertionError("identity");
        // Equal values still reverse by position.
        if (!read(reverseThree(build(new int[] {5, 5, 9}))).equals(List.of(9, 5, 5))) throw new AssertionError("ex2");
        // Random triples must match reversing an ArrayList.
        Random rnd = new Random(11);
        for (int t = 0; t < 300; t++) {
            int[] a = {rnd.nextInt(9), rnd.nextInt(9), rnd.nextInt(9)};
            List<Integer> o = new ArrayList<>(List.of(a[0], a[1], a[2]));
            Collections.reverse(o);
            if (!read(reverseThree(build(a))).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Reverse Linked List (LeetCode 206)
<!-- id: ll-reverse-list -->

**Approach.**
The loop repeats the same four-step move while `curr` is not `null`. The suffix shrinks by one node per turn, so the loop ends after `n` turns, and `prev` holds the new head.

The invariant is that the nodes before `curr` are reversed and the nodes from `curr` are untouched. The statement `saved = curr.next` runs before `curr.next = prev`, so no suffix node is lost.

**Complexity.**
- **Time** is O(n), because each node crosses the boundary once.
- **Space** is O(1), because the loop stores three references.

```java run
import java.util.*;

public final class ReverseList {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Reverses the list and returns the new head.
     * Time: O(n), because each node is moved once.
     * Space: O(1), because three references are stored.
     * Invariant: nodes before curr are reversed, and nodes from curr are untouched.
     */
    static Node reverse(Node head) {
        Node prev = null;                             // start with an empty reversed prefix
        Node curr = head;                             // start with the whole list as the suffix
        // The suffix loses one node per turn, so the loop makes n turns.
        while (curr != null) {
            Node saved = curr.next;                   // keep the suffix reachable
            curr.next = prev;                         // redirect at the reversed prefix
            prev = curr;                              // the prefix grows by this node
            curr = saved;                             // the suffix shrinks by this node
        }
        return prev;                                  // the first node of the reversed list
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
        // Both examples from the statement.
        if (!read(reverse(build(new int[] {1, 2, 3, 4, 5}))).equals(List.of(5, 4, 3, 2, 1))) throw new AssertionError("ex1");
        if (!read(reverse(build(new int[] {1, 2}))).equals(List.of(2, 1))) throw new AssertionError("ex2");
        // The empty list stays empty.
        if (reverse(null) != null) throw new AssertionError("empty");
        // Random lists must match Collections.reverse on an ArrayList.
        Random rnd = new Random(12);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(15);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(50); o.add(a[i]); }
            Collections.reverse(o);
            if (!read(reverse(build(a))).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty And One Node (Author exercise)
<!-- id: ll-reverse-boundary -->

**Approach.**
The same loop handles both boundaries without a length test. For the empty list, `curr` starts as `null`, the body never runs, and the method returns the initial `prev`, which is `null`. For one node, the body runs once, redirects the node at `null`, and returns it. For two or more nodes, the first redirect sets the old head's `next` to `null`, and no later step changes that field.

The invariant is the same as before, and the starting value `prev = null` is what ends the reversed list correctly.

**Complexity.**
- **Time** is O(n), because each node moves once.
- **Space** is O(1), because three references are stored.

```java run
import java.util.*;

public final class ReverseBoundary {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Reverses the list with no length test.
     * Time: O(n), because each node moves once.
     * Space: O(1), because three references are stored.
     * Invariant: the first redirect uses prev == null, so the old head ends the list.
     */
    static Node reverse(Node head) {
        Node prev = null;                             // the null that ends the new list
        Node curr = head;
        // For an empty list the condition is false at once, so the body never runs.
        while (curr != null) {
            Node saved = curr.next;                   // keep the suffix reachable
            curr.next = prev;                         // redirect at the prefix
            prev = curr;                              // extend the prefix
            curr = saved;                             // shrink the suffix
        }
        return prev;                                  // null for the empty list, the same node for one node
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
        // The empty list returns null.
        if (reverse(null) != null) throw new AssertionError("empty");
        // One node returns the same object, with next still null.
        Node one = new Node(7, null);
        if (reverse(one) != one || one.next != null) throw new AssertionError("one");
        // Two nodes: the old head becomes the tail and its next is null.
        Node h = build(new int[] {8, 9});
        Node oldHead = h;
        Node r = reverse(h);
        if (!read(r).equals(List.of(9, 8)) || oldHead.next != null) throw new AssertionError("two");
        // Random lengths from 0 to 8 must match an ArrayList oracle, and the old head must end the list.
        Random rnd = new Random(13);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(9);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(50); o.add(a[i]); }
            Collections.reverse(o);
            Node head = build(a);
            Node old = head;
            if (!read(reverse(head)).equals(o)) throw new AssertionError("random " + t);
            if (old != null && old.next != null) throw new AssertionError("tail " + t);
        }
    }
}
```

#### Solution: [Recognize] Reverse Linked List II (LeetCode 92)
<!-- id: ll-reverse-between -->

**Approach.**
The block from `left` to `right` is a short list that needs the same reversal loop, run for exactly `right - left + 1` nodes. A helper `reverseFirst(start, k)` reverses `k` nodes starting at `start`. When the loop ends, `curr` holds the first node after the block, so the helper sets `start.next` to `curr`. The old block head is now the block tail, and this write reconnects the right boundary.

The caller handles the left boundary. When `left` is 1, the new block head is the new list head. Otherwise the caller walks to the node before the block, assigns its `next` to the helper's result, and returns the original head.

The invariant is that the helper returns the new block head, and the block tail already points at the suffix. Only the node before the block needs one more write.

**Complexity.**
- **Time** is O(n), because one walk reaches the block and the helper moves at most `right - left + 1` nodes.
- **Space** is O(1), because the code stores a few references.

```java run
import java.util.*;

public final class ReverseBetween {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Reverses the k nodes starting at start, reconnects the tail to the suffix, and returns the new block head.
     * Time: O(k), because each node moves once.
     * Space: O(1), because three references are stored.
     * Invariant: the reversed prefix holds the moved nodes, and curr starts the unmoved rest.
     */
    static Node reverseFirst(Node start, int k) {
        Node prev = null;
        Node curr = start;
        // Exactly k nodes cross the boundary, so the loop counts instead of testing null.
        for (int i = 0; i < k; i++) {
            Node saved = curr.next;                   // keep the rest reachable
            curr.next = prev;                         // redirect at the prefix
            prev = curr;                              // extend the prefix
            curr = saved;                             // shrink the rest
        }
        start.next = curr;                            // the old block head is now the tail and links to the suffix
        return prev;                                  // the new block head
    }

    /**
     * Reverses positions left through right, 1-based, and returns the head.
     * Time: O(n), because the walk plus the reversal visit at most n nodes.
     * Space: O(1), because no node is allocated.
     * Invariant: the node before the block links to the new block head.
     */
    static Node reverseBetween(Node head, int left, int right) {
        // With left == 1 there is no node before the block, so the new block head is the list head.
        if (left == 1) return reverseFirst(head, right);
        Node before = head;
        // Walk left - 2 hops so before is the node at position left - 1.
        for (int i = 0; i < left - 2; i++) before = before.next;
        before.next = reverseFirst(before.next, right - left + 1);   // reconnect the left boundary
        return head;                                  // the head is unchanged when left > 1
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
        // The two examples from the statement.
        if (!read(reverseBetween(build(new int[] {1, 2, 3, 4, 5}), 2, 4)).equals(List.of(1, 4, 3, 2, 5))) throw new AssertionError("ex1");
        if (!read(reverseBetween(build(new int[] {3, 5}), 1, 2)).equals(List.of(5, 3))) throw new AssertionError("ex2");
        // A block of one node changes nothing.
        if (!read(reverseBetween(build(new int[] {1, 2, 3}), 2, 2)).equals(List.of(1, 2, 3))) throw new AssertionError("single");
        // Random lists and ranges must match reversing a sublist of an ArrayList.
        Random rnd = new Random(14);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(50); o.add(a[i]); }
            int l = 1 + rnd.nextInt(n);
            int r = l + rnd.nextInt(n - l + 1);
            Collections.reverse(o.subList(l - 1, r));
            if (!read(reverseBetween(build(a), l, r)).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```
