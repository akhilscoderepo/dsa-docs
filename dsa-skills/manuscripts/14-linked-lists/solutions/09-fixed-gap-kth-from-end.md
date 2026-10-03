<!-- solutions-for: 09-fixed-gap-kth-from-end -->
### Fixed-Gap Kth From End

#### Solution: [Build] Kth Node From End (Author exercise)
<!-- id: ll-kth-from-end -->

**Approach.** Advance a lead pointer `k` nodes from the head while the trailing pointer waits at the head, which sets a gap of `k`. Then move both together until the lead is null. Because the lead ends one position past the last node, the trailing pointer stands `k` nodes before that position, which is the `k`-th node from the end. The assertions compare with the array element at index `n - k`, and check that a list of one node with `k = 1` returns its only value.

**Complexity.** One traversal, so O(n) time, with two references and nothing else.

```java run
import java.util.Random;

public final class KthFromEnd {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static int kthFromEnd(Node head, int k) {
        Node lead = head, trail = head;
        for (int i = 0; i < k; i++) lead = lead.next;
        while (lead != null) {
            lead = lead.next;
            trail = trail.next;
        }
        return trail.value;
    }

    public static void main(String[] args) {
        if (kthFromEnd(build(new int[]{4, 8, 6, 3, 2}), 2) != 3) throw new AssertionError("example 1");
        if (kthFromEnd(build(new int[]{5}), 1) != 5) throw new AssertionError("example 2");
        Random rnd = new Random(1433);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            int k = 1 + rnd.nextInt(n);
            if (kthFromEnd(build(a), k) != a[n - k]) throw new AssertionError("wrong node for n=" + n + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Predecessor Of Kth From End (Author exercise)
<!-- id: ll-predecessor-kth -->

**Approach.** Put a dummy node before the head and start both pointers on it. Advance the lead `k` steps, so it stands on the node with index `k - 1`, and then move both while the lead has a successor. The lead stops on the last node, so the trailing pointer stops one node earlier than in the plain version, which is the predecessor of the target. If the trailing pointer is still the dummy, the target is the first node and the answer is -1. The assertions compare with the array element at index `n - k - 1`, with -1 when `k` equals `n`.

**Complexity.** Linear time in one pass with constant extra memory.

```java run
import java.util.Random;

public final class PredecessorKth {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static int predecessorValue(Node head, int k) {
        Node dummy = new Node(-1);
        dummy.next = head;
        Node lead = dummy, trail = dummy;
        for (int i = 0; i < k; i++) lead = lead.next;
        while (lead.next != null) {
            lead = lead.next;
            trail = trail.next;
        }
        return trail == dummy ? -1 : trail.value;
    }

    public static void main(String[] args) {
        if (predecessorValue(build(new int[]{4, 8, 6, 3, 2}), 2) != 6) throw new AssertionError("example 1");
        if (predecessorValue(build(new int[]{5, 9}), 2) != -1) throw new AssertionError("example 2");
        Random rnd = new Random(1434);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            int k = 1 + rnd.nextInt(n);
            int expected = k == n ? -1 : a[n - k - 1];
            if (predecessorValue(build(a), k) != expected) throw new AssertionError("wrong predecessor for n=" + n + " k=" + k);
        }
    }
}
```

#### Solution: [Boundary] K Equals Length (Author exercise)
<!-- id: ll-k-too-large -->

**Approach.** Use a dummy before the head and advance the lead `k` times, testing after each step whether the lead became null. A null means `k` is larger than the length, and the list is returned as it is. Otherwise move both pointers while the lead has a successor, and bypass the node after the trailing pointer. If `k` equals the length the lead stops on the last node after exactly `k` steps, the trailing pointer is still on the dummy, and the bypass removes the first node with no branch. An empty list makes the first advance null, so it is returned unchanged. The assertions compare with removing an index from an array list, including every `k` up to the oversized values.

**Complexity.** Linear time, one traversal, and constant extra memory.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class KTooLarge {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static Node removeKthFromEnd(Node head, int k) {
        Node dummy = new Node(0);
        dummy.next = head;
        Node lead = dummy, trail = dummy;
        for (int i = 0; i < k; i++) {
            lead = lead.next;
            if (lead == null) return head;
        }
        while (lead.next != null) {
            lead = lead.next;
            trail = trail.next;
        }
        trail.next = trail.next.next;
        return dummy.next;
    }
    static List<Integer> toList(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node cur = head; cur != null; cur = cur.next) out.add(cur.value);
        return out;
    }

    public static void main(String[] args) {
        if (!toList(removeKthFromEnd(build(new int[]{4, 8, 6}), 3)).equals(List.of(8, 6))) throw new AssertionError("example 1");
        if (!toList(removeKthFromEnd(build(new int[]{4, 8}), 5)).equals(List.of(4, 8))) throw new AssertionError("example 2");
        if (!toList(removeKthFromEnd(null, 1)).isEmpty()) throw new AssertionError("empty list");
        Random rnd = new Random(1435);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(100); expected.add(a[i]); }
            int k = 1 + rnd.nextInt(n + 3);
            if (k <= n) expected.remove(n - k);
            if (!toList(removeKthFromEnd(build(a), k)).equals(expected)) throw new AssertionError("wrong result for n=" + n + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-gap -->

**Approach.** Place a dummy before the head, send the lead ahead by `n` nodes, and treat a null lead as an oversized `n`, which removes nothing and reports -1. Otherwise move both pointers until the lead has no successor, and the trailing pointer is on the predecessor of the target. Read the target's value, bypass the target, and return the value together with the values of the list behind the dummy. This is a single pass, in contrast with the two-pass method that counts the length first. The assertions compare with removing an index from an array list and with the answer of the two-pass method.

**Complexity.** Linear time in a single traversal and constant extra memory.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RemoveNthGap {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static int removedValue;
    static Node removeNth(Node head, int n) {
        Node dummy = new Node(0);
        dummy.next = head;
        Node lead = dummy, trail = dummy;
        removedValue = -1;
        for (int i = 0; i < n; i++) {
            lead = lead.next;
            if (lead == null) return head;
        }
        while (lead.next != null) {
            lead = lead.next;
            trail = trail.next;
        }
        removedValue = trail.next.value;
        trail.next = trail.next.next;
        return dummy.next;
    }
    static List<Integer> toList(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node cur = head; cur != null; cur = cur.next) out.add(cur.value);
        return out;
    }

    public static void main(String[] args) {
        Node r = removeNth(build(new int[]{9, 1, 7, 2}), 3);
        if (removedValue != 1 || !toList(r).equals(List.of(9, 7, 2))) throw new AssertionError("example 1");
        r = removeNth(build(new int[]{5, 6}), 3);
        if (removedValue != -1 || !toList(r).equals(List.of(5, 6))) throw new AssertionError("example 2");
        Random rnd = new Random(1436);
        for (int t = 0; t < 5000; t++) {
            int len = 1 + rnd.nextInt(10);
            int[] a = new int[len];
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < len; i++) { a[i] = rnd.nextInt(100); expected.add(a[i]); }
            int n = 1 + rnd.nextInt(len + 3);
            int expectedRemoved = -1;
            if (n <= len) expectedRemoved = expected.remove(len - n);
            Node result = removeNth(build(a), n);
            if (removedValue != expectedRemoved) throw new AssertionError("wrong removed value for len=" + len + " n=" + n);
            if (!toList(result).equals(expected)) throw new AssertionError("wrong list for len=" + len + " n=" + n);
        }
    }
}
```
