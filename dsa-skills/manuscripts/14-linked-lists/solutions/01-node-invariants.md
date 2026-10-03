<!-- solutions-for: 01-node-invariants -->
### Node Invariants

#### Solution: [Build] Traverse And Count (Author exercise)
<!-- id: ll-traverse-and-count -->

**Approach.** Start a cursor at the head and move it with `cur = cur.next` until it is null, adding one to a counter and the node's value to a `long` sum at each stop. An empty list has a null head, so the loop condition fails at once and the result is `[0, 0]` with no special case. The sum is widened to `long` because a hundred thousand values near a billion exceed `int`. The assertions compare with array-based totals on random lists, and confirm that the walk leaves every `next` field untouched by walking the chain a second time.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class TraverseAndCount {
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
    static long[] countAndSum(Node head) {
        long count = 0, sum = 0;
        for (Node cur = head; cur != null; cur = cur.next) {
            count++;
            sum += cur.value;
        }
        return new long[]{count, sum};
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(countAndSum(build(new int[]{4, 7, 1, 9})), new long[]{4, 21})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(countAndSum(build(new int[]{})), new long[]{0, 0})) throw new AssertionError("example 2");
        long[] big = countAndSum(build(new int[]{1000000000, 1000000000, 1000000000}));
        if (big[1] != 3000000000L) throw new AssertionError("the sum must not wrap");
        Random rnd = new Random(1401);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            long s = 0;
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(41) - 20; s += a[i]; }
            Node head = build(a);
            long[] got = countAndSum(head);
            if (got[0] != n || got[1] != s) throw new AssertionError("disagrees with the array totals");
            long again = countAndSum(head)[0];
            if (again != n) throw new AssertionError("the walk must not change the chain");
        }
    }
}
```

#### Solution: [Vary] Insert After A Node (Author exercise)
<!-- id: ll-insert-after-node -->

**Approach.** Walk to the node at position `p`. Save its successor in a local reference, point the new node at the saved reference, and then point the node at the new node. In that order the old tail is held by a reference at every moment, so nothing becomes unreachable. If `p` names the last node the saved successor is null, and the new node becomes the new tail with no special case. The assertions compare with `ArrayList.add`, and show that writing the two links in the wrong order drops every node after the position.

**Complexity.** O(p) time to reach the node and O(1) extra space for the insertion.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class InsertAfterNode {
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
    static int[] toArray(Node head) {
        int c = 0;
        for (Node n = head; n != null; n = n.next) c++;
        int[] out = new int[c];
        int i = 0;
        for (Node n = head; n != null; n = n.next) out[i++] = n.value;
        return out;
    }
    static int[] insertAfter(int[] values, int p, int x) {
        Node head = build(values);
        Node node = head;
        for (int i = 0; i < p; i++) node = node.next;
        Node fresh = new Node(x);
        Node saved = node.next;
        fresh.next = saved;
        node.next = fresh;
        return toArray(head);
    }
    static int[] wrongOrder(int[] values, int p, int x) {
        Node head = build(values);
        Node node = head;
        for (int i = 0; i < p; i++) node = node.next;
        Node fresh = new Node(x);
        node.next = fresh;
        fresh.next = node.next;
        int[] seen = new int[20];
        int c = 0;
        for (Node n = head; n != null && c < 20; n = n.next) seen[c++] = n.value;
        return java.util.Arrays.copyOf(seen, c);
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(insertAfter(new int[]{4, 7, 1, 9}, 1, 5), new int[]{4, 7, 5, 1, 9})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(insertAfter(new int[]{3}, 0, 8), new int[]{3, 8})) throw new AssertionError("example 2");
        int[] lost = wrongOrder(new int[]{4, 7, 1, 9}, 1, 5);
        for (int v : lost) if (v == 1 || v == 9) throw new AssertionError("the wrong order must lose the old tail, but got " + java.util.Arrays.toString(lost));
        if (lost.length != 20) throw new AssertionError("the wrong order makes the new node point at itself, so the walk never ends");
        Random rnd = new Random(1402);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(20);
            int p = rnd.nextInt(n), x = rnd.nextInt(20);
            List<Integer> expected = new ArrayList<>();
            for (int v : a) expected.add(v);
            expected.add(p + 1, x);
            int[] got = insertAfter(a, p, x);
            for (int i = 0; i < got.length; i++) if (got[i] != expected.get(i)) throw new AssertionError("disagrees with ArrayList.add");
            if (got.length != expected.size()) throw new AssertionError("length mismatch");
        }
    }
}
```

#### Solution: [Boundary] Empty And Singleton Lists (Author exercise)
<!-- id: ll-empty-and-singleton -->

**Approach.** Handle the two small cases first and then walk with a lookahead. An empty list returns null, and a one-node list returns null as well, since its only node is the last. Otherwise move a cursor until `cur.next.next` is null, which means `cur.next` is the last node, and cut it off with `cur.next = null`. The lookahead is safe because the test `cur.next == null` has already excluded the one-node case, so `cur.next.next` is only read when `cur.next` is a real node. The assertions compare with array truncation and walk the chain to confirm that no cycle or leftover node remains.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class EmptyAndSingleton {
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
    static int[] toArray(Node head) {
        int c = 0;
        for (Node n = head; n != null; n = n.next) c++;
        int[] out = new int[c];
        int i = 0;
        for (Node n = head; n != null; n = n.next) out[i++] = n.value;
        return out;
    }
    static Node deleteLast(Node head) {
        if (head == null || head.next == null) return null;
        Node cur = head;
        while (cur.next.next != null) cur = cur.next;
        cur.next = null;
        return head;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(toArray(deleteLast(build(new int[]{6}))), new int[]{})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(deleteLast(build(new int[]{}))), new int[]{})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(toArray(deleteLast(build(new int[]{1, 2}))), new int[]{1})) throw new AssertionError("two nodes");
        boolean threw = false;
        try { Node head = null; int unused = head.next == null ? 0 : 1; }
        catch (NullPointerException expected) { threw = true; }
        if (!threw) throw new AssertionError("dereferencing a null head throws NullPointerException");
        Random rnd = new Random(1403);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(20);
            int[] got = toArray(deleteLast(build(a)));
            int[] expected = n == 0 ? new int[0] : java.util.Arrays.copyOf(a, n - 1);
            if (!java.util.Arrays.equals(got, expected)) throw new AssertionError("disagrees with truncation");
        }
    }
}
```

#### Solution: [Recognize] Remove Linked List Elements (LeetCode 203)
<!-- id: ll-remove-elements -->

**Approach.** Advance the head while it holds the target, so the first node of the result, if any, is a keeper. Then walk with a cursor that is always a kept node and look at its successor. If the successor matches, bypass it with `cur.next = cur.next.next` and stay on the same cursor, since the new successor has not been tested. Otherwise move forward. The assertions compare with a filter on arrays, including inputs made only of the target value and inputs with long runs of it.

**Complexity.** O(n) time, since every node is examined once, and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RemoveElements {
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
    static int[] toArray(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node n = head; n != null; n = n.next) out.add(n.value);
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }
    static Node removeElements(Node head, int val) {
        while (head != null && head.value == val) head = head.next;
        Node cur = head;
        while (cur != null && cur.next != null) {
            if (cur.next.value == val) cur.next = cur.next.next;
            else cur = cur.next;
        }
        return head;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(toArray(removeElements(build(new int[]{4, 4, 1, 4, 2, 4}), 4)), new int[]{1, 2})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(toArray(removeElements(build(new int[]{5, 5}), 5)), new int[]{})) throw new AssertionError("example 2");
        Random rnd = new Random(1404);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int val = rnd.nextInt(3);
            List<Integer> kept = new ArrayList<>();
            for (int v : a) if (v != val) kept.add(v);
            int[] got = toArray(removeElements(build(a), val));
            if (got.length != kept.size()) throw new AssertionError("length differs");
            for (int i = 0; i < got.length; i++) if (got[i] != kept.get(i)) throw new AssertionError("value differs");
        }
    }
}
```
