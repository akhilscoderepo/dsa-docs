<!-- solutions-for: 05-dummy-heads -->
### Dummy Heads

#### Solution: [Build] Prepend Without A Special Case (Author exercise)
<!-- id: ll-insert-at-position -->

**Approach.** Create a dummy node whose `next` is the head, and walk an owner reference `p` steps from the dummy, so the owner is the node that will precede the new node. Point the new node at the owner's successor and then point the owner at the new node. Position 0 leaves the owner at the dummy and position `n` leaves it at the last node, and in neither case is there a branch. The answer is `dummy.next`. The assertions compare with `ArrayList.add(p, x)`, including an empty list, front and end insertions.

**Complexity.** O(p) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class InsertAtPosition {
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
    static Node insertAt(Node head, int p, int x) {
        Node dummy = new Node(0);
        dummy.next = head;
        Node owner = dummy;
        for (int i = 0; i < p; i++) owner = owner.next;
        Node fresh = new Node(x);
        fresh.next = owner.next;
        owner.next = fresh;
        return dummy.next;
    }
    static List<Integer> toList(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node cur = head; cur != null; cur = cur.next) out.add(cur.value);
        return out;
    }

    public static void main(String[] args) {
        if (!toList(insertAt(build(new int[]{3, 4}), 0, 9)).equals(List.of(9, 3, 4))) throw new AssertionError("example 1");
        if (!toList(insertAt(build(new int[]{3, 4}), 2, 7)).equals(List.of(3, 4, 7))) throw new AssertionError("example 2");
        if (!toList(insertAt(null, 0, 5)).equals(List.of(5))) throw new AssertionError("empty list");
        Random rnd = new Random(1417);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(20); expected.add(a[i]); }
            int p = rnd.nextInt(n + 1), x = rnd.nextInt(20);
            expected.add(p, x);
            if (!toList(insertAt(build(a), p, x)).equals(expected)) throw new AssertionError("disagrees with ArrayList.add");
        }
    }
}
```

#### Solution: [Vary] Merge Two Sorted Lists, Each Value Once (LeetCode 21)
<!-- id: ll-merge-distinct -->

**Approach.** Build the result behind a dummy tail. Repeatedly take the smaller front of the two lists, with the first list winning ties, and advance that list. Attach the taken node only when the tail is the dummy or the tail's value differs from the node's value, and otherwise skip the node. Because merged order is non-decreasing, equal values are adjacent, so comparing with the tail removes all duplicates. After both lists are used, set the tail's `next` to null, since the last attached node may still point into an original list. The assertions compare with a sorted set of the union, and check that the result contains no cycle and only nodes from the inputs.

**Complexity.** O(n + m) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class MergeDistinct {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static Node build(int[] values, List<Node> all) {
        Node head = null, tail = null;
        for (int v : values) {
            Node n = new Node(v);
            all.add(n);
            if (head == null) head = n; else tail.next = n;
            tail = n;
        }
        return head;
    }
    static Node mergeDistinct(Node a, Node b) {
        Node dummy = new Node(0), tail = dummy;
        while (a != null || b != null) {
            Node take;
            if (b == null || (a != null && a.value <= b.value)) { take = a; a = a.next; }
            else { take = b; b = b.next; }
            if (tail == dummy || tail.value != take.value) { tail.next = take; tail = take; }
        }
        tail.next = null;
        return dummy.next;
    }

    public static void main(String[] args) {
        List<Node> pool = new ArrayList<>();
        Node r = mergeDistinct(build(new int[]{1, 3, 3, 6}, pool), build(new int[]{2, 3, 6, 8}, pool));
        List<Integer> got = new ArrayList<>();
        for (Node c = r; c != null; c = c.next) got.add(c.value);
        if (!got.equals(List.of(1, 2, 3, 6, 8))) throw new AssertionError("example 1");
        got.clear();
        for (Node c = mergeDistinct(build(new int[]{4, 4}, pool), null); c != null; c = c.next) got.add(c.value);
        if (!got.equals(List.of(4))) throw new AssertionError("example 2");
        Random rnd = new Random(1418);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(8), m = rnd.nextInt(8);
            int[] a = new int[n], b = new int[m];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            for (int i = 0; i < m; i++) b[i] = rnd.nextInt(6);
            java.util.Arrays.sort(a);
            java.util.Arrays.sort(b);
            List<Node> nodes = new ArrayList<>();
            Node merged = mergeDistinct(build(a, nodes), build(b, nodes));
            IdentityHashMap<Node, Boolean> known = new IdentityHashMap<>();
            for (Node x : nodes) known.put(x, true);
            TreeSet<Integer> expected = new TreeSet<>();
            for (int v : a) expected.add(v);
            for (int v : b) expected.add(v);
            List<Integer> values = new ArrayList<>();
            int steps = 0;
            for (Node c = merged; c != null; c = c.next) {
                if (++steps > n + m + 1) throw new AssertionError("a cycle or a stale tail");
                if (!known.containsKey(c)) throw new AssertionError("only original nodes may appear");
                values.add(c.value);
            }
            if (!values.equals(new ArrayList<>(expected))) throw new AssertionError("disagrees with the sorted union");
        }
    }
}
```

#### Solution: [Boundary] Remove Blocked Values (LeetCode 203)
<!-- id: ll-remove-blocked -->

**Approach.** Put a dummy in front of the list and let the owner start at the dummy. While the owner has a successor, test the successor's value against a set built from `blocked`. A blocked successor is bypassed with `owner.next = owner.next.next` and the owner stays, because the new successor has not been tested. An allowed successor makes the owner move forward. A run of blocked nodes at the front is handled by the same bypass, since the owner is the dummy. The answer is `dummy.next`. The assertions compare with a filter over arrays, including lists that are entirely blocked and lists with long runs of blocked values at the front.

**Complexity.** O(n + b) time for n nodes and b blocked values, and O(b) space for the set.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class RemoveBlocked {
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
    static Node withdraw(Node head, int[] blockedValues) {
        Set<Integer> blocked = new HashSet<>();
        for (int b : blockedValues) blocked.add(b);
        Node dummy = new Node(0);
        dummy.next = head;
        Node owner = dummy;
        while (owner.next != null) {
            if (blocked.contains(owner.next.value)) owner.next = owner.next.next;
            else owner = owner.next;
        }
        return dummy.next;
    }
    static List<Integer> toList(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node cur = head; cur != null; cur = cur.next) out.add(cur.value);
        return out;
    }

    public static void main(String[] args) {
        if (!toList(withdraw(build(new int[]{5, 2, 5, 7, 2, 9}), new int[]{2, 5})).equals(List.of(7, 9))) throw new AssertionError("example 1");
        if (!toList(withdraw(build(new int[]{1, 1}), new int[]{1})).isEmpty()) throw new AssertionError("example 2");
        Random rnd = new Random(1419);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            int[] blocked = new int[rnd.nextInt(4)];
            for (int i = 0; i < blocked.length; i++) blocked[i] = rnd.nextInt(5);
            Set<Integer> set = new HashSet<>();
            for (int b : blocked) set.add(b);
            List<Integer> expected = new ArrayList<>();
            for (int v : a) if (!set.contains(v)) expected.add(v);
            if (!toList(withdraw(build(a), blocked)).equals(expected)) throw new AssertionError("disagrees with the filter");
        }
    }
}
```

#### Solution: [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-dummy -->

**Approach.** Count the nodes to learn the length `L`. Then place a dummy in front of the list and walk the owner `L - n` steps from the dummy, so that it stops on the node just before the target. Bypass the target with `owner.next = owner.next.next`. When `n` equals `L` the owner never leaves the dummy, and the same bypass removes the original head, so no branch is needed. The answer is `dummy.next`. The assertions compare with removing an index from an array list, including single-node lists and removal of the head and of the tail.

**Complexity.** O(n) time in two passes and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RemoveNthDummy {
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
    static Node removeFromEnd(Node head, int n) {
        int length = 0;
        for (Node cur = head; cur != null; cur = cur.next) length++;
        Node dummy = new Node(0);
        dummy.next = head;
        Node owner = dummy;
        for (int i = 0; i < length - n; i++) owner = owner.next;
        owner.next = owner.next.next;
        return dummy.next;
    }
    static List<Integer> toList(Node head) {
        List<Integer> out = new ArrayList<>();
        for (Node cur = head; cur != null; cur = cur.next) out.add(cur.value);
        return out;
    }

    public static void main(String[] args) {
        if (!toList(removeFromEnd(build(new int[]{4, 8, 6, 3, 2}), 2)).equals(List.of(4, 8, 6, 2))) throw new AssertionError("example 1");
        if (!toList(removeFromEnd(build(new int[]{7}), 1)).isEmpty()) throw new AssertionError("example 2");
        Random rnd = new Random(1420);
        for (int t = 0; t < 5000; t++) {
            int len = 1 + rnd.nextInt(10);
            int[] a = new int[len];
            List<Integer> expected = new ArrayList<>();
            for (int i = 0; i < len; i++) { a[i] = rnd.nextInt(100); expected.add(a[i]); }
            int n = 1 + rnd.nextInt(len);
            expected.remove(len - n);
            if (!toList(removeFromEnd(build(a), n)).equals(expected)) throw new AssertionError("disagrees with index removal on " + java.util.Arrays.toString(a) + " n=" + n);
        }
    }
}
```
