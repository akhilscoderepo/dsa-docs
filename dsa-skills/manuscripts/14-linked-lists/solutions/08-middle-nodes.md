<!-- solutions-for: 08-middle-nodes -->
### Middle Nodes

#### Solution: [Build] Odd-Length Middle (Author exercise)
<!-- id: ll-odd-middle -->

**Approach.** Start `slow` and `fast` at the head. While `fast` has a successor, advance `slow` by one node and `fast` by two, and count the round. For a list of odd length `2k + 1` the pointer `fast` reaches the last node after exactly `k` rounds, where it has no successor, and `slow` is on the node with index `k`. The answer is the value at `slow` and the number of rounds. The assertions check that the middle value equals the array element at index `n / 2` and that the number of rounds equals `n / 2`, for every odd length tried.

**Complexity.** O(n) time, since the loop makes about n / 2 rounds, and O(1) extra space.

```java run
import java.util.Random;

public final class OddMiddle {
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
    static long[] middle(Node head) {
        Node slow = head, fast = head;
        int rounds = 0;
        while (fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            rounds++;
            if (fast == null) throw new AssertionError("an odd list must end on the last node");
        }
        return new long[]{slow.value, rounds};
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(middle(build(new int[]{4, 8, 6, 3, 2})), new long[]{6, 2})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(middle(build(new int[]{7})), new long[]{7, 0})) throw new AssertionError("example 2");
        Random rnd = new Random(1429);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + 2 * rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            long[] got = middle(build(a));
            if (got[0] != a[n / 2]) throw new AssertionError("the middle value is wrong");
            if (got[1] != n / 2) throw new AssertionError("the number of rounds is wrong");
        }
    }
}
```

#### Solution: [Vary] Middle of the Linked List (LeetCode 876)
<!-- id: ll-middle-second -->

**Approach.** Advance `slow` one node and `fast` two nodes per round while `fast` is non-null and has a successor. For an even length `2k`, `fast` becomes null after `k` rounds and `slow` stands on the node with index `k`, which is the second of the two middles. For an odd length `2k + 1` it stands on the exact middle. The result is reported as the values from `slow` to the end. The assertions compare with the array slice starting at index `n / 2`, which is the second middle for even lengths, and check that the original list is not modified.

**Complexity.** Time linear in the list length, plus constant extra memory.

```java run
import java.util.Random;

public final class MiddleSecond {
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
    static Node middleNode(Node head) {
        Node slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }
    static int[] fromNode(Node start) {
        int c = 0;
        for (Node cur = start; cur != null; cur = cur.next) c++;
        int[] out = new int[c];
        int i = 0;
        for (Node cur = start; cur != null; cur = cur.next) out[i++] = cur.value;
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(fromNode(middleNode(build(new int[]{3, 5, 2, 8, 1, 6}))), new int[]{8, 1, 6})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(fromNode(middleNode(build(new int[]{9, 4, 7}))), new int[]{4, 7})) throw new AssertionError("example 2");
        Random rnd = new Random(1430);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            Node head = build(a);
            int[] got = fromNode(middleNode(head));
            int[] expected = java.util.Arrays.copyOfRange(a, n / 2, n);
            if (!java.util.Arrays.equals(got, expected)) throw new AssertionError("disagrees with the array slice on length " + n);
            if (!java.util.Arrays.equals(fromNode(head), a)) throw new AssertionError("the list must not be modified");
        }
    }
}
```

#### Solution: [Boundary] First Middle Contract (Author exercise)
<!-- id: ll-first-middle -->

**Approach.** Return -1 for an empty list. Otherwise start `slow` and `fast` at the head and advance them while both `fast.next` and `fast.next.next` exist, which stops one round earlier on an even list than the test of the previous exercise. For an even length `2k` the pointer `fast` stops on the node with index `2k - 2` after `k - 1` rounds, and `slow` is on index `k - 1`, the first middle. For an odd length the result is the same exact middle as before. The assertions compare with the array element at index `(n - 1) / 2` and check that a list of one node returns its own value.

**Complexity.** Time linear in the list length, plus constant extra memory.

```java run
import java.util.Random;

public final class FirstMiddle {
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
    static int firstMiddleValue(Node head) {
        if (head == null) return -1;
        Node slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow.value;
    }

    public static void main(String[] args) {
        if (firstMiddleValue(build(new int[]{3, 5, 2, 8, 1, 6})) != 2) throw new AssertionError("example 1");
        if (firstMiddleValue(build(new int[]{1})) != 1) throw new AssertionError("example 2");
        if (firstMiddleValue(null) != -1) throw new AssertionError("empty list");
        if (firstMiddleValue(build(new int[]{5, 6})) != 5) throw new AssertionError("two nodes");
        Random rnd = new Random(1431);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(100);
            if (firstMiddleValue(build(a)) != a[(n - 1) / 2]) throw new AssertionError("wrong first middle for length " + n);
        }
    }
}
```

#### Solution: [Recognize] Palindrome Linked List (LeetCode 234)
<!-- id: ll-palindrome-list -->

**Approach.** Find the end of the first half with the first-middle test, so that for odd lengths the middle node belongs to the first half and is not compared. Reverse the second half in place, starting after that node, and compare it with the first half from the head, node by node, stopping at a mismatch. Then reverse the second half again and attach it back, so the list is exactly as it was given. The comparison runs over the second half, which is never longer than the first. The assertions compare with a check of the array against its reverse, and confirm after every call that the list's values and the identity of every node are unchanged.

**Complexity.** Time linear in the list length, plus constant extra memory.

```java run
import java.util.Random;

public final class PalindromeList {
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
    static boolean isPalindrome(Node head) {
        Node slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        Node secondHalf = reverse(slow.next);
        boolean same = true;
        Node a = head, b = secondHalf;
        while (b != null) {
            if (a.value != b.value) { same = false; break; }
            a = a.next;
            b = b.next;
        }
        slow.next = reverse(secondHalf);
        return same;
    }

    public static void main(String[] args) {
        if (!isPalindrome(build(new int[]{2, 7, 1, 7, 2}, new Node[5]))) throw new AssertionError("example 1");
        if (isPalindrome(build(new int[]{4, 5, 5, 3}, new Node[4]))) throw new AssertionError("example 2");
        Random rnd = new Random(1432);
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            if (rnd.nextBoolean()) for (int i = 0; i < n / 2; i++) a[n - 1 - i] = a[i];
            boolean expected = true;
            for (int i = 0; i < n; i++) if (a[i] != a[n - 1 - i]) expected = false;
            Node[] nodes = new Node[n];
            Node head = build(a, nodes);
            if (isPalindrome(head) != expected) throw new AssertionError("wrong answer on " + java.util.Arrays.toString(a));
            Node cur = head;
            for (int i = 0; i < n; i++) {
                if (cur != nodes[i]) throw new AssertionError("the list was not restored");
                cur = cur.next;
            }
            if (cur != null) throw new AssertionError("the list has extra nodes");
        }
    }
}
```
