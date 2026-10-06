<!-- solutions-for: 04-merge -->
### Solutions For Merging Sorted Lists

#### Solution: [Build] Merge Two One-Node Lists (Author exercise)
<!-- id: ll-merge-one-node -->

**Approach.**
The method compares the two values. The smaller node becomes the head, and a tie keeps the node of `a` first. The head's `next` is set to the other node with one write. The other node's `next` is already `null`, so the list ends correctly.

The invariant is that the head is no larger than the node attached after it. Only one `next` field changes, because the other node already ends the list.

**Complexity.**
- **Time** is O(1), because the method makes one comparison and one write.
- **Space** is O(1), because it allocates nothing.

```java run
import java.util.*;

public final class MergeOneNode {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Merges two one-node lists.
     * Time: O(1), because one comparison and one write run.
     * Space: O(1), because no node is allocated.
     * Invariant: the head is no larger than the node attached after it.
     */
    static Node mergeOne(Node a, Node b) {
        // A strict comparison sends ties to a, so equal values keep the input order.
        if (b.val < a.val) { b.next = a; return b; }
        a.next = b;                                   // attach the other node with one write
        return a;
    }

    public static void main(String[] args) {
        // Example 1: 5 and 3 merge to 3,5.
        Node a = new Node(5, null), b = new Node(3, null);
        Node h = mergeOne(a, b);
        if (h != b || h.next != a || a.next != null) throw new AssertionError("ex1");
        // Example 2: equal values keep a first.
        a = new Node(4, null); b = new Node(4, null);
        h = mergeOne(a, b);
        if (h != a || h.next != b || b.next != null) throw new AssertionError("ex2");
        // Random pairs must come out sorted with a before b on ties.
        Random rnd = new Random(31);
        for (int t = 0; t < 500; t++) {
            a = new Node(rnd.nextInt(5), null); b = new Node(rnd.nextInt(5), null);
            Node expectFirst = b.val < a.val ? b : a;
            h = mergeOne(a, b);
            if (h != expectFirst || h.val > h.next.val || h.next.next != null) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Merge Two Sorted Lists (LeetCode 21)
<!-- id: ll-merge-two-sorted -->

**Approach.**
The method returns the other list when one list is empty. Otherwise it chooses the smaller head as the answer head and keeps a result tail. While both lists have unplaced nodes, it attaches the smaller head to the result tail and advances that list. When the loop ends, one list is empty, and the method attaches the other list with one write.

The invariant is that the chain from `head` to `tail` is sorted and no node in it is larger than any unplaced node. A strict comparison sends ties to the first list, which keeps the merge stable.

**Complexity.**
- **Time** is O(m + n), because each turn places one node and the remainder costs one write.
- **Space** is O(1), because the method stores four references.

```java run
import java.util.*;

public final class MergeTwoSorted {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Merges two sorted lists by reusing their nodes.
     * Time: O(m + n), because each node is placed once.
     * Space: O(1), because four references are stored.
     * Invariant: head to tail is sorted and no larger than any unplaced node.
     */
    static Node merge(Node a, Node b) {
        // An empty list leaves the other list as the answer.
        if (a == null) return b;
        if (b == null) return a;
        Node head;
        // The smaller head starts the answer; a tie keeps a first.
        if (b.val < a.val) { head = b; b = b.next; } else { head = a; a = a.next; }
        Node tail = head;                             // the finalized prefix is the node head
        // Each turn places one node, so the loop makes at most m + n - 1 turns.
        while (a != null && b != null) {
            if (b.val < a.val) { tail.next = b; b = b.next; }
            else { tail.next = a; a = a.next; }       // attach the smaller head, then advance its list
            tail = tail.next;                         // the finalized prefix grows by one node
        }
        tail.next = (a != null) ? a : b;              // one write attaches the remainder
        return head;
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
        // Example 1: duplicates across the lists.
        if (!read(merge(build(new int[] {1, 2, 4}), build(new int[] {1, 3, 4}))).equals(List.of(1, 1, 2, 3, 4, 4))) throw new AssertionError("ex1");
        // Example 2: an empty first list returns the second list.
        if (!read(merge(null, build(new int[] {0}))).equals(List.of(0))) throw new AssertionError("ex2");
        // Both empty returns null.
        if (merge(null, null) != null) throw new AssertionError("both empty");
        // Random sorted lists must match sorting the combined values.
        Random rnd = new Random(32);
        for (int t = 0; t < 1000; t++) {
            int[] x = sortedRandom(rnd), y = sortedRandom(rnd);
            List<Integer> o = new ArrayList<>();
            for (int v : x) o.add(v);
            for (int v : y) o.add(v);
            Collections.sort(o);
            if (!read(merge(build(x), build(y))).equals(o)) throw new AssertionError("random " + t);
        }
    }

    static int[] sortedRandom(Random rnd) {
        int[] r = new int[rnd.nextInt(8)];
        // Small value range forces many ties between the two lists.
        for (int i = 0; i < r.length; i++) r[i] = rnd.nextInt(10);
        Arrays.sort(r);
        return r;
    }
}
```

#### Solution: [Boundary] One Empty Or Exhausted List (Author exercise)
<!-- id: ll-merge-exhausted -->

**Approach.**
The method is the merge from the previous exercise with a counter. The counter increases once per loop turn, because each turn evaluates one comparison of two node values. The initial head choice also compares once when both lists are non-empty. When either list is empty at the start, no comparison happens. When the loop ends, one write attaches the remainder, and the counter does not change.

The invariant is that the counter equals the number of nodes placed by comparison. Because the remainder is attached without a test, the count is at most `m + n - 1` and is smaller whenever one list is much shorter or entirely smaller.

**Complexity.**
- **Time** is O(m + n), because each comparison places one node.
- **Space** is O(1), because the code stores four references and one counter.

```java run
import java.util.*;

public final class MergeExhausted {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static int comparisons;                           // counts value comparisons of the last call

    /**
     * Merges two sorted lists and counts value comparisons.
     * Time: O(m + n), because each comparison places one node.
     * Space: O(1), because four references and a counter are stored.
     * Invariant: comparisons equals the number of nodes placed by comparison.
     */
    static Node merge(Node a, Node b) {
        comparisons = 0;
        // An empty list needs no comparison at all.
        if (a == null) return b;
        if (b == null) return a;
        Node head;
        comparisons++;                                // the head choice compares the two first nodes
        if (b.val < a.val) { head = b; b = b.next; } else { head = a; a = a.next; }
        Node tail = head;
        // Each turn compares two values, then places one node.
        while (a != null && b != null) {
            comparisons++;
            if (b.val < a.val) { tail.next = b; b = b.next; }
            else { tail.next = a; a = a.next; }
            tail = tail.next;
        }
        tail.next = (a != null) ? a : b;              // the remainder needs no comparison
        return head;
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
        // Example 1: the first list is entirely smaller, so 3 comparisons place its 3 nodes.
        List<Integer> r = read(merge(build(new int[] {1, 2, 3}), build(new int[] {7, 8})));
        if (!r.equals(List.of(1, 2, 3, 7, 8)) || comparisons != 3) throw new AssertionError("ex1");
        // Example 2: an empty list means 0 comparisons.
        r = read(merge(null, build(new int[] {4})));
        if (!r.equals(List.of(4)) || comparisons != 0) throw new AssertionError("ex2");
        // Random lists: compare with an oracle that simulates the same two-pointer walk on arrays.
        Random rnd = new Random(33);
        for (int t = 0; t < 1000; t++) {
            int[] x = sortedRandom(rnd), y = sortedRandom(rnd);
            int i = 0, j = 0, c = 0;
            List<Integer> o = new ArrayList<>();
            // The oracle counts one comparison per placed node while both arrays have nodes left.
            while (i < x.length && j < y.length) { c++; if (y[j] < x[i]) o.add(y[j++]); else o.add(x[i++]); }
            while (i < x.length) o.add(x[i++]);
            while (j < y.length) o.add(y[j++]);
            if (!read(merge(build(x), build(y))).equals(o) || comparisons != c) throw new AssertionError("random " + t);
        }
    }

    static int[] sortedRandom(Random rnd) {
        int[] r = new int[rnd.nextInt(8)];
        // Small value range forces many ties between the two lists.
        for (int i = 0; i < r.length; i++) r[i] = rnd.nextInt(10);
        Arrays.sort(r);
        return r;
    }
}
```

#### Solution: [Recognize] Sort List (LeetCode 148)
<!-- id: ll-sort-list -->

**Approach.**
The method counts the nodes, and a list of 0 or 1 node is already sorted. Otherwise it walks `n / 2 - 1` hops to the last node of the first half and cuts the link after it, so the two halves share no node. It sorts each half recursively and merges the sorted halves with the merge from this lesson.

The invariant is that every call returns a sorted list built from exactly the nodes it received. The cut before the recursive calls keeps the two halves disjoint. The recursion is `log n` levels deep, and each level touches every node once for the split walk and once for the merge.

**Complexity.**
- **Time** is O(n log n), because there are about `log n` levels and each level costs O(n) for the walks and merges.
- **Space** is O(log n), because the recursion holds one frame per level and the merge allocates nothing.

```java run
import java.util.*;

public final class SortList {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Sorts the list by merge sort and reuses its nodes.
     * Time: O(n log n), because each of about log n levels costs O(n).
     * Space: O(log n), because recursion depth is log n.
     * Invariant: each call returns a sorted list of exactly the nodes it received.
     */
    static Node sortList(Node head) {
        int n = 0;
        // One walk counts the nodes so the split point is known.
        for (Node c = head; c != null; c = c.next) n++;
        // Zero or one node is already sorted.
        if (n <= 1) return head;
        Node mid = head;
        // Walk n / 2 - 1 hops to the last node of the first half.
        for (int i = 0; i < n / 2 - 1; i++) mid = mid.next;
        Node second = mid.next;                       // first node of the second half
        mid.next = null;                              // cut so the halves share no node
        return merge(sortList(head), sortList(second));
    }

    /**
     * Merges two sorted lists.
     * Time: O(m + n), because each node is placed once.
     * Space: O(1), because four references are stored.
     * Invariant: head to tail is sorted and no larger than any unplaced node.
     */
    static Node merge(Node a, Node b) {
        // An empty list leaves the other list as the answer.
        if (a == null) return b;
        if (b == null) return a;
        Node head;
        // The smaller head starts the answer; a tie keeps a first.
        if (b.val < a.val) { head = b; b = b.next; } else { head = a; a = a.next; }
        Node tail = head;
        // Each turn places one node.
        while (a != null && b != null) {
            if (b.val < a.val) { tail.next = b; b = b.next; }
            else { tail.next = a; a = a.next; }
            tail = tail.next;
        }
        tail.next = (a != null) ? a : b;              // one write attaches the remainder
        return head;
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
        // Both examples from the statement.
        if (!read(sortList(build(new int[] {4, 2, 1, 3}))).equals(List.of(1, 2, 3, 4))) throw new AssertionError("ex1");
        if (!read(sortList(build(new int[] {-1, 5, 3, 4, 0}))).equals(List.of(-1, 0, 3, 4, 5))) throw new AssertionError("ex2");
        // Empty and one-node lists return unchanged.
        if (sortList(null) != null) throw new AssertionError("empty");
        // Random lists with many duplicates must match Collections.sort, and every node must be reused.
        Random rnd = new Random(34);
        for (int t = 0; t < 1000; t++) {
            int n = rnd.nextInt(20);
            int[] x = new int[n];
            List<Integer> o = new ArrayList<>();
            for (int i = 0; i < n; i++) { x[i] = rnd.nextInt(6) - 3; o.add(x[i]); }
            Collections.sort(o);
            Node h = build(x);
            Set<Node> before = Collections.newSetFromMap(new IdentityHashMap<>());
            for (Node c = h; c != null; c = c.next) before.add(c);
            Node s = sortList(h);
            Set<Node> after = Collections.newSetFromMap(new IdentityHashMap<>());
            for (Node c = s; c != null; c = c.next) after.add(c);
            if (!read(s).equals(o) || !before.equals(after)) throw new AssertionError("random " + t);
        }
    }
}
```
