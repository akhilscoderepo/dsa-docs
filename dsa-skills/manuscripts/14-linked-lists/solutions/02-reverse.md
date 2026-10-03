<!-- solutions-for: 02-reverse -->
### Reverse

#### Solution: [Build] Reverse Three Nodes By Hand (Author exercise)
<!-- id: ll-reverse-three-by-hand -->

**Approach.** Set `prev` to null and `curr` to the head. In each of three rounds, save `curr.next`, point `curr.next` at `prev`, then move `prev` to `curr` and `curr` to the saved node. After the third round `curr` is null and `prev` names the old last node, which is the new head. The assertions compare with the reversed array, and confirm that the nodes themselves are reused by checking that the new head is the object that was last in the original chain.

**Complexity.** Three rounds of constant work, so O(1) time and O(1) extra space for a list of exactly three nodes.

```java run
import java.util.Random;

public final class ReverseThreeByHand {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(reverseThree(new int[]{1, 2, 3}), new int[]{3, 2, 1})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(reverseThree(new int[]{5, 5, 9}), new int[]{9, 5, 5})) throw new AssertionError("example 2");
        Node a = new Node(1), b = new Node(2), c = new Node(3);
        a.next = b;
        b.next = c;
        Node prev = null, curr = a;
        for (int round = 0; round < 3; round++) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        if (prev != c || curr != null) throw new AssertionError("the old last node is the new head and curr is null");
        if (c.next != b || b.next != a || a.next != null) throw new AssertionError("every link points the other way");
        Random rnd = new Random(1405);
        for (int t = 0; t < 2000; t++) {
            int[] v = {rnd.nextInt(10), rnd.nextInt(10), rnd.nextInt(10)};
            int[] got = reverseThree(v);
            if (got[0] != v[2] || got[1] != v[1] || got[2] != v[0]) throw new AssertionError("disagrees with the reversed array");
        }
    }

    static int[] reverseThree(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        Node prev = null, curr = head;
        for (int round = 0; round < 3; round++) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        int[] out = new int[3];
        int i = 0;
        for (Node n = prev; n != null; n = n.next) out[i++] = n.value;
        return out;
    }
}
```

#### Solution: [Vary] Reverse Linked List (LeetCode 206)
<!-- id: ll-reverse-list -->

**Approach.** Keep `prev` as the head of the reversed prefix and `curr` as the head of the untouched suffix. While `curr` is not null, save its successor, point it at `prev`, and advance both references. The loop ends when the suffix is empty, and `prev` is returned. The assertions compare with reversing the values of a copy, check that the total number of nodes is unchanged, and check a second reversal restores the original order.

**Complexity.** Linear time with a constant number of extra references.

```java run
import java.util.Random;

public final class ReverseList {
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
    static Node reverse(Node head) {
        Node prev = null, curr = head;
        while (curr != null) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        return prev;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(toArray(reverse(build(new int[]{7, 1, 4, 9, 2})), 5), new int[]{2, 9, 4, 1, 7})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(reverse(build(new int[]{6, 6})), 2), new int[]{6, 6})) throw new AssertionError("example 2");
        Random rnd = new Random(1406);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            Node head = build(a);
            Node rev = reverse(head);
            int[] got = toArray(rev, n);
            for (int i = 0; i < n; i++) if (got[i] != a[n - 1 - i]) throw new AssertionError("not reversed");
            int count = 0;
            for (Node cur = rev; cur != null && count <= n; cur = cur.next) count++;
            if (count != n) throw new AssertionError("a node was lost or a cycle was formed");
            int[] back = toArray(reverse(rev), n);
            if (!java.util.Arrays.equals(back, a)) throw new AssertionError("a second reversal must restore the order");
        }
    }
}
```

#### Solution: [Boundary] Empty And One Node (Author exercise)
<!-- id: ll-reverse-empty-one -->

**Approach.** The same loop handles every size. For a null head the loop condition fails immediately and `prev` is still null, which is also the head of the empty result. For one node the loop runs once: the node's `next` is set to null, `prev` becomes the node, and `curr` becomes null. The returned head is therefore the original node object. The flag compares the references with `==`. The assertions compare with reversed arrays on random lengths, and check that the flag is `1` exactly when the list has zero or one node, since for longer lists the old last node becomes the head.

**Complexity.** Linear time with a constant number of extra references.

```java run
import java.util.Random;

public final class ReverseEmptyOne {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static int[] run(int[] values) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        Node original = head;
        Node prev = null, curr = head;
        while (curr != null) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        int[] out = new int[values.length + 1];
        int i = 0;
        for (Node n = prev; n != null; n = n.next) out[i++] = n.value;
        out[values.length] = prev == original ? 1 : 0;
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(run(new int[]{}), new int[]{1})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(run(new int[]{8}), new int[]{8, 1})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(run(new int[]{1, 2}), new int[]{2, 1, 0})) throw new AssertionError("two nodes change the head");
        Random rnd = new Random(1407);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            int[] got = run(a);
            for (int i = 0; i < n; i++) if (got[i] != a[n - 1 - i]) throw new AssertionError("not reversed");
            int expectedFlag = n <= 1 ? 1 : 0;
            if (got[n] != expectedFlag) throw new AssertionError("head identity flag is wrong for n=" + n);
        }
    }
}
```

#### Solution: [Recognize] Reverse Linked List II (LeetCode 92)
<!-- id: ll-reverse-between -->

**Approach.** Walk to position `left`, remembering the node before it, which is null when `left` is 1, and remember the first segment node, because it becomes the segment tail. Reverse exactly `right - left + 1` nodes with the usual three moves, so that `prev` heads the reversed segment and `curr` is the first node after it. Then point the segment tail at `curr`, and point the node before the segment at `prev`. If there was no node before the segment, `prev` is the new head. The assertions compare with reversing a slice of an array, including segments of length one and segments that touch either end.

**Complexity.** O(n) time in one pass and O(1) extra space.

```java run
import java.util.Random;

public final class ReverseBetween {
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
    static Node reverseBetween(Node head, int left, int right) {
        Node before = null, cursor = head;
        for (int i = 1; i < left; i++) { before = cursor; cursor = cursor.next; }
        Node segmentTail = cursor;
        Node prev = null, curr = cursor;
        for (int i = left; i <= right; i++) {
            Node saved = curr.next;
            curr.next = prev;
            prev = curr;
            curr = saved;
        }
        segmentTail.next = curr;
        if (before == null) return prev;
        before.next = prev;
        return head;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(toArray(reverseBetween(build(new int[]{3, 8, 2, 6, 9, 1}), 2, 4), 6), new int[]{3, 6, 2, 8, 9, 1})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(reverseBetween(build(new int[]{5, 6}), 1, 2), 2), new int[]{6, 5})) throw new AssertionError("example 2");
        Random rnd = new Random(1408);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            int left = 1 + rnd.nextInt(n);
            int right = left + rnd.nextInt(n - left + 1);
            int[] expected = a.clone();
            for (int i = left - 1, j = right - 1; i < j; i++, j--) { int tmp = expected[i]; expected[i] = expected[j]; expected[j] = tmp; }
            int[] got = toArray(reverseBetween(build(a), left, right), n);
            if (!java.util.Arrays.equals(got, expected)) throw new AssertionError("disagrees with slice reversal on " + java.util.Arrays.toString(a) + " " + left + " " + right);
        }
    }
}
```
