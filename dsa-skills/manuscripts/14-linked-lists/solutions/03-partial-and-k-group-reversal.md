<!-- solutions-for: 03-partial-and-k-group-reversal -->
### Partial And K-Group Reversal

#### Solution: [Build] Reverse Exactly Two Nodes (Author exercise)
<!-- id: ll-swap-pair -->

**Approach.** Walk to the node at position `p`, remembering the node before it. Let `first` be that node and `second` its successor. Point `first` at the node after the pair, then point `second` at `first`, and finally point the node before the pair at `second`, or return `second` as the new head when the pair starts the list. Writing the links in this order means the second node is always reachable until it has been relinked. The assertions compare with swapping two array entries, and confirm that the node objects themselves moved by checking that the object formerly at position `p` is now at position `p + 1`.

**Complexity.** O(p) time to reach the pair and O(1) extra space.

```java run
import java.util.Random;

public final class SwapPair {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values, Node[] store) {
        Node head = null, tail = null;
        for (int i = 0; i < values.length; i++) {
            Node n = new Node(values[i]);
            store[i] = n;
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static Node swapPairAfter(Node head, int p) {
        Node before = null, first = head;
        for (int i = 0; i < p; i++) { before = first; first = first.next; }
        Node second = first.next;
        first.next = second.next;
        second.next = first;
        if (before == null) return second;
        before.next = second;
        return head;
    }
    static int[] toArray(Node head, int n) {
        int[] out = new int[n];
        int i = 0;
        for (Node cur = head; cur != null && i < n; cur = cur.next) out[i++] = cur.value;
        return out;
    }

    public static void main(String[] args) {
        Node[] store = new Node[4];
        if (!java.util.Arrays.equals(toArray(swapPairAfter(build(new int[]{4, 7, 1, 9}, store), 1), 4), new int[]{4, 1, 7, 9})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(swapPairAfter(build(new int[]{2, 3}, new Node[2]), 0), 2), new int[]{3, 2})) throw new AssertionError("example 2");
        Random rnd = new Random(1409);
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            int p = rnd.nextInt(n - 1);
            Node[] nodes = new Node[n];
            Node head = swapPairAfter(build(a, nodes), p);
            int[] expected = a.clone();
            int tmp = expected[p]; expected[p] = expected[p + 1]; expected[p + 1] = tmp;
            if (!java.util.Arrays.equals(toArray(head, n), expected)) throw new AssertionError("disagrees with the array swap");
            Node cur = head;
            for (int i = 0; i < p; i++) cur = cur.next;
            if (cur != nodes[p + 1] || cur.next != nodes[p]) throw new AssertionError("the node objects must have moved, not their values");
        }
    }
}
```

#### Solution: [Vary] Reverse A Half-Open Range (LeetCode 92)
<!-- id: ll-reverse-half-open -->

**Approach.** Count the list length first, then clamp `to` to it. The range holds `to - from` nodes, and if that is less than two the list is returned as it is. Otherwise walk to position `from`, remember the node before it and the first node of the range, and reverse exactly `to - from` nodes with the three moves. The old first node of the range then points at the node that follows the range, which is null when the range ran to the end. The node before the range is pointed at the new front, or the new front becomes the head when `from` is 0. The assertions compare with reversing a clamped slice of an array, including ranges that start at 0, that run past the end, and that are empty.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class ReverseHalfOpen {
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
    static int[] toArray(Node head, int n) {
        int[] out = new int[n];
        int i = 0;
        for (Node cur = head; cur != null && i < n; cur = cur.next) out[i++] = cur.value;
        return out;
    }
    static Node reverseRange(Node head, long from, long to) {
        int n = 0;
        for (Node cur = head; cur != null; cur = cur.next) n++;
        int hi = (int) Math.min(to, n);
        if (from >= hi || hi - from < 2) return head;
        int lo = (int) from;
        Node before = null, start = head;
        for (int i = 0; i < lo; i++) { before = start; start = start.next; }
        Node prev = null, curr = start;
        for (int i = lo; i < hi; i++) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        start.next = curr;
        if (before == null) return prev;
        before.next = prev;
        return head;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(toArray(reverseRange(build(new int[]{5, 1, 7, 3, 8}), 1, 99), 5), new int[]{5, 8, 3, 7, 1})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(reverseRange(build(new int[]{4, 6, 2}), 2, 2), 3), new int[]{4, 6, 2})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(toArray(reverseRange(build(new int[]{}), 0, 5), 0), new int[]{})) throw new AssertionError("empty list");
        Random rnd = new Random(1410);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            int from = rnd.nextInt(n + 2);
            int to = from + rnd.nextInt(n + 3);
            int[] expected = a.clone();
            int hi = Math.min(to, n);
            for (int i = from, j = hi - 1; i < j; i++, j--) { int tmp = expected[i]; expected[i] = expected[j]; expected[j] = tmp; }
            int[] got = toArray(reverseRange(build(a), from, to), n);
            if (!java.util.Arrays.equals(got, expected)) throw new AssertionError("disagrees with slice reversal on " + java.util.Arrays.toString(a) + " " + from + " " + to);
        }
    }
}
```

#### Solution: [Boundary] Incomplete Final Group (Author exercise)
<!-- id: ll-first-full-group -->

**Approach.** Walk a probe forward over up to `k` nodes without changing any link. If the count is below `k`, return the list as it is, since no link has been touched. Otherwise the probe rests on the node after the group. Run the reversal with `prev` seeded as the probe, so the old first node points at the rest of the list, and return the last `prev` as the new head. The assertions compare with array reversal of the first `k` entries when `k <= n`, and with the unchanged array otherwise, and they check that for a short list every `next` reference is the same object as before.

**Complexity.** O(min(n, k)) time and O(1) extra space.

```java run
import java.util.Random;

public final class FirstFullGroup {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values, Node[] store) {
        Node head = null, tail = null;
        for (int i = 0; i < values.length; i++) {
            Node n = new Node(values[i]);
            store[i] = n;
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static int[] toArray(Node head, int n) {
        int[] out = new int[n];
        int i = 0;
        for (Node cur = head; cur != null && i < n; cur = cur.next) out[i++] = cur.value;
        return out;
    }
    static Node reverseFirstGroup(Node head, int k) {
        Node probe = head;
        int c = 0;
        while (probe != null && c < k) { probe = probe.next; c++; }
        if (c < k) return head;
        Node prev = probe, curr = head;
        for (int i = 0; i < k; i++) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        return prev;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(toArray(reverseFirstGroup(build(new int[]{1, 2, 3, 4, 5}, new Node[5]), 3), 5), new int[]{3, 2, 1, 4, 5})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(reverseFirstGroup(build(new int[]{1, 2}, new Node[2]), 3), 2), new int[]{1, 2})) throw new AssertionError("example 2");
        Random rnd = new Random(1411);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(9);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            int k = 1 + rnd.nextInt(10);
            Node[] nodes = new Node[n];
            Node head = build(a, nodes);
            Node[] oldNext = new Node[n];
            for (int i = 0; i < n; i++) oldNext[i] = nodes[i].next;
            Node result = reverseFirstGroup(head, k);
            int[] expected = a.clone();
            if (k <= n) for (int i = 0, j = k - 1; i < j; i++, j--) { int tmp = expected[i]; expected[i] = expected[j]; expected[j] = tmp; }
            if (!java.util.Arrays.equals(toArray(result, n), expected)) throw new AssertionError("disagrees with the array version");
            if (k > n) for (int i = 0; i < n; i++) if (nodes[i].next != oldNext[i]) throw new AssertionError("a short list must be left untouched");
        }
    }
}
```

#### Solution: [Recognize] Reverse Nodes in k-Group (LeetCode 25)
<!-- id: ll-reverse-k-group -->

**Approach.** Repeat the bounded reversal while a full group exists. For each group, a look-ahead probe walks up to `k` nodes from the group start without changing links, and the loop ends when fewer than `k` are found. A full group is reversed with the usual three moves, seeded so that the old first node points at the node after the group. The node before the group, or the head if there is none, is pointed at the new front. The old first node becomes the new group predecessor, and the probe becomes the next start. The assertions compare with block-wise reversal of an array and check that the number of nodes is unchanged and no cycle forms.

**Complexity.** O(n) time, since each node is visited by one look-ahead and one flip, and O(1) extra space.

```java run
import java.util.Random;

public final class ReverseKGroup {
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
    static int[] toArray(Node head, int n) {
        int[] out = new int[n + 1];
        int i = 0;
        for (Node cur = head; cur != null && i <= n; cur = cur.next) out[i++] = cur.value;
        return java.util.Arrays.copyOf(out, i);
    }
    static Node reverseGroups(Node head, int k) {
        Node before = null, start = head;
        while (true) {
            Node probe = start;
            int c = 0;
            while (probe != null && c < k) { probe = probe.next; c++; }
            if (c < k) break;
            Node prev = probe, curr = start;
            for (int i = 0; i < k; i++) {
                Node saved = curr.next;
                curr.next = prev;
                prev = curr;
                curr = saved;
            }
            if (before == null) head = prev; else before.next = prev;
            before = start;
            start = probe;
        }
        return head;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(toArray(reverseGroups(build(new int[]{2, 4, 6, 8, 10, 12}), 4), 6), new int[]{8, 6, 4, 2, 10, 12})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(reverseGroups(build(new int[]{9, 4, 7, 2, 8, 5, 3}), 3), 7), new int[]{7, 4, 9, 5, 8, 2, 3})) throw new AssertionError("example 2");
        Random rnd = new Random(1412);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            int k = 1 + rnd.nextInt(n);
            int[] expected = a.clone();
            for (int s = 0; s + k <= n; s += k)
                for (int i = s, j = s + k - 1; i < j; i++, j--) { int tmp = expected[i]; expected[i] = expected[j]; expected[j] = tmp; }
            int[] got = toArray(reverseGroups(build(a), k), n);
            if (!java.util.Arrays.equals(got, expected)) throw new AssertionError("disagrees with block reversal on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```
