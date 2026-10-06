<!-- solutions-for: 08-middle-nodes -->
### Solutions For Middle Nodes

#### Solution: [Build] Odd-Length Middle (Author exercise)
<!-- id: ll-odd-middle -->

**Approach.**
The slow reference moves one node per turn, and the fast reference moves two. For an odd length `n`, the fast reference reaches index `n - 1`, the last node, after `(n - 1) / 2` turns. At that point `fast.next` is `null`, so the loop stops. The slow reference is at index `(n - 1) / 2`, which is the middle node, and the turn count equals that index.

The invariant is that after `k` turns, slow is at index `k` and fast is at index `2k`.

**Complexity.**
- **Time** is O(n), because the fast reference makes about `n` hops.
- **Space** is O(1), because the method stores two references and a counter.

```java run
import java.util.*;

public final class OddMiddle {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns {value of the middle node, number of loop turns} for an odd-length list.
     * Time: O(n), because the fast reference makes about n hops.
     * Space: O(1), because two references and a counter are stored.
     * Invariant: after k turns, slow is at index k and fast is at index 2k.
     */
    static int[] middle(Node head) {
        Node slow = head, fast = head;
        int turns = 0;
        // A double step needs fast and fast.next, in that order.
        while (fast != null && fast.next != null) {
            slow = slow.next;                         // one step
            fast = fast.next.next;                    // two steps
            turns++;
        }
        return new int[] {slow.val, turns};
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    public static void main(String[] args) {
        // Example 1: five nodes give the value 3 after 2 turns.
        int[] r = middle(build(new int[] {1, 2, 3, 4, 5}));
        if (r[0] != 3 || r[1] != 2) throw new AssertionError("ex1");
        // Example 2: one node gives its own value after 0 turns.
        r = middle(build(new int[] {7}));
        if (r[0] != 7 || r[1] != 0) throw new AssertionError("ex2");
        // Random odd lengths must match array indexing at n / 2 with (n - 1) / 2 turns.
        Random rnd = new Random(71);
        for (int t = 0; t < 1000; t++) {
            int n = 2 * rnd.nextInt(8) + 1;
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            r = middle(build(a));
            if (r[0] != a[n / 2] || r[1] != (n - 1) / 2) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Middle of the Linked List (LeetCode 876)
<!-- id: ll-second-middle -->

**Approach.**
The method uses the loop test `fast != null && fast.next != null`. For an even length `n`, the fast reference lands on `null` after `n / 2` turns, so the loop stops with the slow reference at index `n / 2`, the second middle. For an odd length, the fast reference stops on the last node, and the slow reference is on the single middle node. The method returns the slow reference, so the caller reads the list from the middle onward.

The invariant is that after `k` turns, slow is at index `k` and fast is at index `2k`, so at the end slow is at index `n / 2` using integer division.

**Complexity.**
- **Time** is O(n), because the fast reference makes about `n` hops.
- **Space** is O(1), because the method stores two references.

```java run
import java.util.*;

public final class SecondMiddle {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the middle node, or the second of two middle nodes.
     * Time: O(n), because the fast reference makes about n hops.
     * Space: O(1), because two references are stored.
     * Invariant: after k turns, slow is at index k and fast is at index 2k.
     */
    static Node middleNode(Node head) {
        Node slow = head, fast = head;
        // Stopping with fast on null puts slow on the second middle for even n.
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    static List<Integer> read(Node head) {
        List<Integer> out = new ArrayList<>();
        // Read all values from the given node on.
        for (Node c = head; c != null; c = c.next) out.add(c.val);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: five nodes return the node 3.
        if (!read(middleNode(build(new int[] {1, 2, 3, 4, 5}))).equals(List.of(3, 4, 5))) throw new AssertionError("ex1");
        // Example 2: six nodes return the second middle, the node 4.
        if (!read(middleNode(build(new int[] {1, 2, 3, 4, 5, 6}))).equals(List.of(4, 5, 6))) throw new AssertionError("ex2");
        // A single node returns itself.
        if (!read(middleNode(build(new int[] {9}))).equals(List.of(9))) throw new AssertionError("one");
        // Random lengths from 1 to 12 must match array index n / 2.
        Random rnd = new Random(72);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            List<Integer> expect = new ArrayList<>();
            for (int i = n / 2; i < n; i++) expect.add(a[i]);
            if (!read(middleNode(build(a))).equals(expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] First Middle Contract (Author exercise)
<!-- id: ll-first-middle -->

**Approach.**
The method changes only the loop test, to `fast.next != null && fast.next.next != null`. A double step is allowed only when two more nodes exist after `fast`. For an even length `n`, the fast reference stops at index `n - 2`, one double step earlier than before, so the slow reference stops at index `n / 2 - 1`, the first middle. For an odd length, the fast reference stops at index `n - 1`, and the slow reference is on the single middle. The method reads `fast.next` before any test, so it needs a non-empty list.

The invariant is the same as before: after `k` turns, slow is at index `k` and fast is at index `2k`.

**Complexity.**
- **Time** is O(n), because the fast reference makes about `n` hops.
- **Space** is O(1), because the method stores two references.

```java run
import java.util.*;

public final class FirstMiddle {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the middle node, or the first of two middle nodes. The list must be non-empty.
     * Time: O(n), because the fast reference makes about n hops.
     * Space: O(1), because two references are stored.
     * Invariant: after k turns, slow is at index k and fast is at index 2k.
     */
    static Node firstMiddle(Node head) {
        Node slow = head, fast = head;
        // A double step needs two nodes after fast, so even lengths stop one turn earlier.
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    static Node build(int[] a) {
        Node head = null;
        // Build from the back so each node links to the chain already built.
        for (int i = a.length - 1; i >= 0; i--) head = new Node(a[i], head);
        return head;
    }

    public static void main(String[] args) {
        // Example 1: four nodes return the node 2.
        if (firstMiddle(build(new int[] {1, 2, 3, 4})).val != 2) throw new AssertionError("ex1");
        // Example 2: one node returns itself.
        if (firstMiddle(build(new int[] {9})).val != 9) throw new AssertionError("ex2");
        // Random lengths from 1 to 13 must match array index (n - 1) / 2.
        Random rnd = new Random(73);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(13);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = i;      // distinct values identify the index
            if (firstMiddle(build(a)).val != (n - 1) / 2) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Palindrome Linked List (LeetCode 234)
<!-- id: ll-palindrome -->

**Approach.**
The method finds the first middle with the loop test that stops early for even lengths, so the first half ends at that node. It reverses the nodes after the first middle in place, with the reversal loop from the earlier lesson, and keeps the head of the reversed half. Then it compares the first half and the reversed half one node at a time, stopping at the end of the reversed half. An odd-length list leaves the middle node unmatched, which is correct, because the middle node is its own mirror. After the comparison, the method reverses the second half again and links it back, so the list has its original order. The method returns the result of the comparison.

The invariant is that the reversed half holds exactly the nodes after the first middle, and the comparison only reads values. The second reversal restores the links in the same way, because reversing twice returns the original order.

**Complexity.**
- **Time** is O(n), because the search, two reversals and the comparison each take at most `n` steps.
- **Space** is O(1), because the method stores a few references.

```java run
import java.util.*;

public final class Palindrome {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static Node reverse(Node head) {
        Node prev = null, curr = head;
        // The standard reversal: save the successor, redirect, advance.
        while (curr != null) { Node saved = curr.next; curr.next = prev; prev = curr; curr = saved; }
        return prev;
    }

    /**
     * Returns true when the values read the same in both directions, and restores the list.
     * Time: O(n), because each of four passes takes at most n steps.
     * Space: O(1), because a few references are stored.
     * Invariant: the reversed half is exactly the nodes after the first middle.
     */
    static boolean isPalindrome(Node head) {
        Node slow = head, fast = head;
        // Stop early for even lengths, so slow is the last node of the first half.
        while (fast.next != null && fast.next.next != null) { slow = slow.next; fast = fast.next.next; }
        Node secondHalf = reverse(slow.next);         // reverse the nodes after the first middle
        boolean ok = true;
        Node p = head, q = secondHalf;
        // The reversed half is never longer than the first half, so q decides when to stop.
        while (q != null) {
            if (p.val != q.val) { ok = false; break; }
            p = p.next; q = q.next;
        }
        slow.next = reverse(secondHalf);              // restore the original order
        return ok;
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
        // Example 1: an even palindrome.
        if (!isPalindrome(build(new int[] {1, 2, 2, 1}))) throw new AssertionError("ex1");
        // Example 2: not a palindrome, and the list still reads 1,2,3,2.
        Node h = build(new int[] {1, 2, 3, 2});
        if (isPalindrome(h) || !read(h).equals(List.of(1, 2, 3, 2))) throw new AssertionError("ex2");
        // One node is a palindrome.
        if (!isPalindrome(build(new int[] {5}))) throw new AssertionError("one");
        // Random lists over a small alphabet must match an array check, and the list must be restored.
        Random rnd = new Random(74);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2);
            if (rnd.nextBoolean()) for (int i = 0; i < n / 2; i++) a[n - 1 - i] = a[i];   // force many palindromes
            boolean expect = true;
            for (int i = 0; i < n / 2; i++) if (a[i] != a[n - 1 - i]) expect = false;
            Node head = build(a);
            if (isPalindrome(head) != expect) throw new AssertionError("answer " + t);
            List<Integer> orig = new ArrayList<>();
            for (int v : a) orig.add(v);
            if (!read(head).equals(orig)) throw new AssertionError("restore " + t);
        }
    }
}
```
