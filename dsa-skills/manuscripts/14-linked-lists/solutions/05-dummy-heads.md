<!-- solutions-for: 05-dummy-heads -->
### Solutions For The Dummy Node

#### Solution: [Build] Prepend Without A Special Case (Author exercise)
<!-- id: ll-insert-at -->

**Approach.**
The method places a dummy node before the head and walks `p` hops from the dummy node. After `p` hops, `prev` holds the predecessor of position `p`, which is the dummy node when `p` is 0. One write inserts the new node after `prev`, and the new node takes over the old `prev.next`. The method returns `dummy.next`.

The invariant is that `prev` is the node at position `i - 1` after `i` hops, with the dummy node standing for position -1. Position 0 therefore follows the same write as every other position.

**Complexity.**
- **Time** is O(p), because the walk takes `p` hops and the insertion is one write.
- **Space** is O(1), because the method allocates one dummy node and one new node.

```java run
import java.util.*;

public final class InsertAt {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Inserts x so that it becomes the node at 0-based position p.
     * Time: O(p), because the walk takes p hops.
     * Space: O(1), because one dummy node and one new node are allocated.
     * Invariant: after i hops, prev is the node at position i - 1, and the dummy node is position -1.
     */
    static Node insertAt(Node head, int p, int x) {
        Node dummy = new Node(0, head);               // position -1; its value is never read
        Node prev = dummy;
        // p hops land on the predecessor of position p, even when p is 0.
        for (int i = 0; i < p; i++) prev = prev.next;
        prev.next = new Node(x, prev.next);           // the new node keeps the old successor
        return dummy.next;                            // correct even when the new node is the head
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
        // Example 1: position 0 makes the new node the head.
        if (!read(insertAt(build(new int[] {1, 2}), 0, 9)).equals(List.of(9, 1, 2))) throw new AssertionError("ex1");
        // Example 2: position n appends.
        if (!read(insertAt(build(new int[] {1, 2}), 2, 5)).equals(List.of(1, 2, 5))) throw new AssertionError("ex2");
        // The empty list accepts position 0.
        if (!read(insertAt(null, 0, 3)).equals(List.of(3))) throw new AssertionError("empty");
        // Random lists and positions must match ArrayList.add(p, x).
        Random rnd = new Random(41);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(50); o.add(a[i]); }
            int p = rnd.nextInt(n + 1);
            int x = rnd.nextInt(50);
            o.add(p, x);
            if (!read(insertAt(build(a), p, x)).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Merge Two Sorted Lists (LeetCode 21)
<!-- id: ll-merge-unique -->

**Approach.**
The method builds the result behind a dummy tail. At each turn it picks the smaller head, with ties going to the first list, and advances that list. The picked node attaches only if the tail is the dummy node or the picked value differs from `tail.val`. Otherwise the node is dropped and the tail stays. After the loop, the leftover list is not attached in one write, because its nodes may repeat the last kept value, so the method feeds each leftover node through the same attach rule.

The invariant is that the chain from the dummy node to `tail` is strictly increasing and no node is larger than any unplaced node. A dropped node is never reachable from the result, and the last written `next` field ends with `null`.

**Complexity.**
- **Time** is O(m + n), because every node is examined once.
- **Space** is O(1), because the method allocates one dummy node.

```java run
import java.util.*;

public final class MergeUnique {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Merges two sorted lists and keeps one node per value.
     * Time: O(m + n), because every node is examined once.
     * Space: O(1), because one dummy node is allocated.
     * Invariant: dummy to tail is strictly increasing and no node exceeds an unplaced node.
     */
    static Node mergeUnique(Node a, Node b) {
        Node dummy = new Node(0, null);               // the first tail; its value is never read
        Node tail = dummy;
        // Each turn consumes one node, so the loop ends after m + n turns.
        while (a != null || b != null) {
            Node pick;
            // Choose the smaller head; a missing list loses the comparison.
            if (b == null || (a != null && a.val <= b.val)) { pick = a; a = a.next; }
            else { pick = b; b = b.next; }
            // Attach only if the value is new; the dummy node counts as "no value yet".
            if (tail == dummy || tail.val != pick.val) {
                tail.next = pick;
                tail = pick;
            }
        }
        tail.next = null;                             // the last kept node must end the list
        return dummy.next;
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
        // Example 1: duplicates across the lists collapse.
        if (!read(mergeUnique(build(new int[] {1, 2, 4}), build(new int[] {1, 3, 4}))).equals(List.of(1, 2, 3, 4))) throw new AssertionError("ex1");
        // Example 2: a run of equal values keeps one node.
        if (!read(mergeUnique(build(new int[] {2, 2, 2}), null)).equals(List.of(2))) throw new AssertionError("ex2");
        // Both empty returns null.
        if (mergeUnique(null, null) != null) throw new AssertionError("empty");
        // Random sorted lists must match a TreeSet of the combined values.
        Random rnd = new Random(42);
        for (int t = 0; t < 1000; t++) {
            int[] x = sortedRandom(rnd), y = sortedRandom(rnd);
            TreeSet<Integer> set = new TreeSet<>();
            for (int v : x) set.add(v);
            for (int v : y) set.add(v);
            if (!read(mergeUnique(build(x), build(y))).equals(new ArrayList<>(set))) throw new AssertionError("random " + t);
        }
    }

    static int[] sortedRandom(Random rnd) {
        int[] r = new int[rnd.nextInt(8)];
        // A small value range forces many equal values.
        for (int i = 0; i < r.length; i++) r[i] = rnd.nextInt(6);
        Arrays.sort(r);
        return r;
    }
}
```

#### Solution: [Boundary] Remove Linked List Elements (LeetCode 203)
<!-- id: ll-remove-up-to -->

**Approach.**
The method uses a dummy node and one rule. While `prev.next` exists, it checks whether that node matches `target` and the removal budget is not spent. If both hold, it unlinks the node with `prev.next = prev.next.next` and decrements the budget. Otherwise it advances `prev`. The original head follows the same rule as every other node.

The invariant is that every node from the dummy node to `prev` is kept, and at most `limit` matches have been removed so far. When the budget reaches 0, matches are kept like any other node.

**Complexity.**
- **Time** is O(n), because each loop turn removes or passes one node.
- **Space** is O(1), because the method allocates one dummy node.

```java run
import java.util.*;

public final class RemoveUpTo {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Removes the first limit nodes whose value equals target.
     * Time: O(n), because each turn handles one node.
     * Space: O(1), because one dummy node is allocated.
     * Invariant: dummy to prev is kept, and at most limit matches were removed.
     */
    static Node removeUpTo(Node head, int target, int limit) {
        Node dummy = new Node(0, head);               // stands in for the node before the head
        Node prev = dummy;
        int budget = limit;                           // removals still allowed
        // Each turn either unlinks prev.next or advances prev.
        while (prev.next != null) {
            if (budget > 0 && prev.next.val == target) {
                prev.next = prev.next.next;           // unlink the match
                budget--;                             // one removal is spent
            } else {
                prev = prev.next;                     // keep this node
            }
        }
        return dummy.next;                            // correct when the original head was removed
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
        // Example 1: two removals at the front, then a kept match.
        if (!read(removeUpTo(build(new int[] {7, 7, 3, 7}), 7, 2)).equals(List.of(3, 7))) throw new AssertionError("ex1");
        // Example 2: a zero limit changes nothing.
        if (!read(removeUpTo(build(new int[] {5, 5}), 5, 0)).equals(List.of(5, 5))) throw new AssertionError("ex2");
        // The empty list stays empty.
        if (removeUpTo(null, 1, 3) != null) throw new AssertionError("empty");
        // Random lists must match an ArrayList oracle that removes the first limit matches.
        Random rnd = new Random(43);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(3); o.add(a[i]); }
            int target = rnd.nextInt(3), limit = rnd.nextInt(5);
            // Oracle: scan left to right and drop matches while the budget lasts.
            List<Integer> expect = new ArrayList<>();
            int budget = limit;
            for (int v : o) { if (budget > 0 && v == target) budget--; else expect.add(v); }
            if (!read(removeUpTo(build(a), target, limit)).equals(expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Remove Nth Node From End of List (LeetCode 19)
<!-- id: ll-remove-nth-count -->

**Approach.**
The first walk counts the length `L`. The target node sits at position `L - n` from the start, counting from 0, so its predecessor is reached after `L - n` hops from the dummy node. One write, `prev.next = prev.next.next`, removes the target. When the target is the original head, `prev` is the dummy node and the same write removes it. The method returns `dummy.next`.

The invariant is that after `i` hops, `prev` is the node at position `i - 1`, with the dummy node standing for position -1. The walk therefore ends one node before the target.

**Complexity.**
- **Time** is O(L), because one walk counts and a second walk takes at most `L` hops.
- **Space** is O(1), because the method allocates one dummy node.

```java run
import java.util.*;

public final class RemoveNthCount {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Removes the n-th node from the end, where 1 <= n <= length.
     * Time: O(L), because two walks each cover at most L nodes.
     * Space: O(1), because one dummy node is allocated.
     * Invariant: after i hops, prev is the node at position i - 1.
     */
    static Node removeNth(Node head, int n) {
        int len = 0;
        // The first walk counts the nodes.
        for (Node c = head; c != null; c = c.next) len++;
        Node dummy = new Node(0, head);               // position -1
        Node prev = dummy;
        // len - n hops reach the predecessor of the target.
        for (int i = 0; i < len - n; i++) prev = prev.next;
        prev.next = prev.next.next;                   // skip the target; this also removes the head when len == n
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
        // Example 1: the second node from the end of 1..5 is 4.
        if (!read(removeNth(build(new int[] {1, 2, 3, 4, 5}), 2)).equals(List.of(1, 2, 3, 5))) throw new AssertionError("ex1");
        // Example 2: removing the only node leaves the empty list.
        if (removeNth(build(new int[] {1}), 1) != null) throw new AssertionError("ex2");
        // Removing the original head by n = length.
        if (!read(removeNth(build(new int[] {1, 2, 3}), 3)).equals(List.of(2, 3))) throw new AssertionError("head");
        // Random lists and positions must match ArrayList.remove(size - n).
        Random rnd = new Random(44);
        for (int t = 0; t < 1000; t++) {
            int len = 1 + rnd.nextInt(10);
            int[] a = new int[len];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < len; i++) { a[i] = rnd.nextInt(100); o.add(a[i]); }
            int n = 1 + rnd.nextInt(len);
            o.remove(len - n);
            if (!read(removeNth(build(a), n)).equals(o)) throw new AssertionError("random " + t);
        }
    }
}
```
