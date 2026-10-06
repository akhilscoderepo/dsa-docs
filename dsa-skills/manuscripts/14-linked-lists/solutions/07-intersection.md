<!-- solutions-for: 07-intersection -->
### Solutions For Meeting Points

#### Solution: [Build] Compare Node Identity (Author exercise)
<!-- id: ll-node-identity -->

**Approach.**
The method walks both lists with one reference each. At every position it compares `x.val == y.val` for the equal-value count and `x == y` for the same-node count. The two tests are independent, because equal values do not imply the same object, and the same object always implies equal values.

The invariant is that after `i` turns, both counts cover exactly the first `i` positions. The same-node count is never larger than the equal-value count.

**Complexity.**
- **Time** is O(n), because the loop makes one turn per position.
- **Space** is O(1), because the method stores two references and two counters.

```java run
import java.util.*;

public final class NodeIdentity {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns {equal values, same nodes} over matching positions.
     * Time: O(n), because one turn runs per position.
     * Space: O(1), because two references and two counters are stored.
     * Invariant: both counts cover the first i positions after i turns.
     */
    static int[] compare(Node a, Node b) {
        int equalValues = 0, sameNodes = 0;
        // Both lists have the same length, so one null test is enough in a correct input.
        for (Node x = a, y = b; x != null && y != null; x = x.next, y = y.next) {
            if (x.val == y.val) equalValues++;        // value test
            if (x == y) sameNodes++;                  // identity test
        }
        return new int[] {equalValues, sameNodes};
    }

    static Node build(int[] vals, Node tail) {
        Node head = tail;
        // Build from the back so the last built node links to the given tail.
        for (int i = vals.length - 1; i >= 0; i--) head = new Node(vals[i], head);
        return head;
    }

    public static void main(String[] args) {
        // Example 1: separate lists with equal values share no node.
        int[] r = compare(build(new int[] {1, 2, 3}, null), build(new int[] {1, 2, 3}, null));
        if (r[0] != 3 || r[1] != 0) throw new AssertionError("ex1");
        // Example 2: the last two nodes are shared objects.
        Node shared = build(new int[] {2, 3}, null);
        r = compare(new Node(1, shared), new Node(9, shared));
        if (r[0] != 2 || r[1] != 2) throw new AssertionError("ex2");
        // The empty lists give 0 and 0.
        r = compare(null, null);
        if (r[0] != 0 || r[1] != 0) throw new AssertionError("empty");
        // Random pairs with a random shared tail must match array bookkeeping.
        Random rnd = new Random(61);
        for (int t = 0; t < 1000; t++) {
            int p = rnd.nextInt(4), s = rnd.nextInt(4);
            int[] av = new int[p], bv = new int[p], sv = new int[s];
            for (int i = 0; i < p; i++) { av[i] = rnd.nextInt(3); bv[i] = rnd.nextInt(3); }
            for (int i = 0; i < s; i++) sv[i] = rnd.nextInt(3);
            Node tail = build(sv, null);
            int eq = s, same = s;                     // shared nodes are equal in value and identity
            for (int i = 0; i < p; i++) if (av[i] == bv[i]) eq++;
            r = compare(build(av, tail), build(bv, tail));
            if (r[0] != eq || r[1] != same) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Align By Length (Author exercise)
<!-- id: ll-align-by-length -->

**Approach.**
One walk per list gives the lengths `la` and `lb`. The reference of the longer list moves ahead by the difference, so both references stand at the same distance from the end. Then both move one node per turn, and the loop stops at the first equal pair of references. If the lists share no node, the pair first becomes equal at `null`, and the method returns `null`.

The invariant is that at each comparison the two references are the same distance from the end of their lists, so a shared node is found at the first equal pair. Nodes before the shared tail can never be equal at equal distance from the end.

**Complexity.**
- **Time** is O(m + n), because two length walks and one joint walk each take at most `max(m, n)` steps.
- **Space** is O(1), because the method stores two references and two lengths.

```java run
import java.util.*;

public final class AlignByLength {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    static int length(Node head) {
        int n = 0;
        // One walk counts the nodes of a list.
        for (Node c = head; c != null; c = c.next) n++;
        return n;
    }

    /**
     * Returns the first node both lists contain, or null.
     * Time: O(m + n), because three walks each take at most max(m, n) steps.
     * Space: O(1), because two references and two lengths are stored.
     * Invariant: the references are compared at equal distance from the end.
     */
    static Node firstShared(Node a, Node b) {
        int la = length(a), lb = length(b);
        Node pa = a, pb = b;
        // Only one of these loops runs, because one difference is not positive.
        for (int i = 0; i < la - lb; i++) pa = pa.next;
        for (int i = 0; i < lb - la; i++) pb = pb.next;
        // Equal distance from the end: the first equal pair is the first shared node.
        while (pa != pb) { pa = pa.next; pb = pb.next; }
        return pa;                                    // null when both reached the end together
    }

    static Node build(int[] vals, Node tail) {
        Node head = tail;
        // Build from the back so the last built node links to the given tail.
        for (int i = vals.length - 1; i >= 0; i--) head = new Node(vals[i], head);
        return head;
    }

    /** Oracle: the first node of a that appears in b, found with an identity set. */
    static Node oracle(Node a, Node b) {
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node c = b; c != null; c = c.next) seen.add(c);
        for (Node c = a; c != null; c = c.next) if (seen.contains(c)) return c;
        return null;
    }

    public static void main(String[] args) {
        // Example 1: the shared tail starts at the node 8.
        Node tail = build(new int[] {8, 4, 5}, null);
        Node a = build(new int[] {4, 1}, tail), b = build(new int[] {5, 6, 1}, tail);
        if (firstShared(a, b) != tail) throw new AssertionError("ex1");
        // Example 2: no shared node returns null.
        if (firstShared(build(new int[] {1, 9}, null), build(new int[] {2, 3}, null)) != null) throw new AssertionError("ex2");
        // Empty lists return null.
        if (firstShared(null, a) != null || firstShared(null, null) != null) throw new AssertionError("empty");
        // Random pairs with random prefixes and tails must match the identity-set oracle.
        Random rnd = new Random(62);
        for (int t = 0; t < 2000; t++) {
            int s = rnd.nextInt(4);
            int[] sv = new int[s];
            for (int i = 0; i < s; i++) sv[i] = rnd.nextInt(3);
            Node sh = build(sv, null);
            Node x = build(new int[rnd.nextInt(5)], sh), y = build(new int[rnd.nextInt(5)], sh);
            if (firstShared(x, y) != oracle(x, y)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] No Intersection And Shared Head (Author exercise)
<!-- id: ll-meet-boundary -->

**Approach.**
The method runs head switching and counts the turns. Each turn moves both references once. A reference that holds `null` moves to the head of the other list, and any other reference moves to its `next`. The loop condition `pa != pb` is tested before the first turn, so lists that start at the same node, and two empty lists, return 0 without a turn. If no node is shared, both references fall off the end of the second list after `m + n` steps and are `null` together, so the count is `m + n + 1`, and the count is `m` when both lists have the same length, because both references reach `null` together.

The invariant is that after `i` turns, both references have walked the same number of nodes, so they can be equal only at a shared node or at `null`.

**Complexity.**
- **Time** is O(m + n), because the loop makes at most `m + n + 1` turns.
- **Space** is O(1), because the method stores two references and one counter.

```java run
import java.util.*;

public final class MeetBoundary {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the number of head-switching turns before the references are equal.
     * Time: O(m + n), because at most m + n + 1 turns run.
     * Space: O(1), because two references and a counter are stored.
     * Invariant: after i turns, both references have walked i nodes of the combined walk.
     */
    static int turns(Node a, Node b) {
        Node pa = a, pb = b;
        int count = 0;
        // The test runs before each turn, so equal starting references need no turn.
        while (pa != pb) {
            pa = (pa == null) ? b : pa.next;          // continue on the other list after the end
            pb = (pb == null) ? a : pb.next;
            count++;
        }
        return count;
    }

    static int length(Node h) {
        int n = 0;
        for (Node c = h; c != null; c = c.next) n++;
        return n;
    }

    static Node build(int n, Node tail) {
        Node head = tail;
        // Build n nodes in front of the given tail.
        for (int i = 0; i < n; i++) head = new Node(i, head);
        return head;
    }

    public static void main(String[] args) {
        // Example 1: lists of 2 and 1 nodes with no shared node take 4 turns.
        if (turns(build(2, null), build(1, null)) != 4) throw new AssertionError("ex1");
        // Example 2: the same head for both lists takes 0 turns.
        Node h = build(3, null);
        if (turns(h, h) != 0) throw new AssertionError("ex2");
        // Empty lists: both empty takes 0 turns, and one empty takes the length of the other plus 1.
        if (turns(null, null) != 0) throw new AssertionError("both empty");
        if (turns(null, build(4, null)) != 5) throw new AssertionError("one empty");
        // Random pairs: x and y are the unshared prefix lengths and s is the shared tail length.
        Random rnd = new Random(63);
        for (int t = 0; t < 2000; t++) {
            int x = rnd.nextInt(5), y = rnd.nextInt(5), s = rnd.nextInt(4);
            Node sh = build(s, null);
            Node a = build(x, sh), b = build(y, sh);
            // Equal lengths align the references, so they meet after x turns; otherwise each passes null once.
            int expect = (x == y) ? x : x + y + s + 1;
            if (turns(a, b) != expect) throw new AssertionError("random " + t + " x=" + x + " y=" + y + " s=" + s);
        }
    }
}
```

#### Solution: [Recognize] Intersection of Two Linked Lists (LeetCode 160)
<!-- id: ll-intersection-switch -->

**Approach.**
Two references start at the two heads. Each turn moves a reference to its `next`, and a reference that holds `null` moves to the head of the other list. The first reference covers `x + s` nodes of its own list and then `y` nodes of the other list before the shared tail, and the second covers `y + s` and `x`. Both have walked `x + y` nodes, so they stand on the first shared node together. With no shared node, both are `null` after the same number of steps, and the loop ends with `null`.

The invariant is that at every turn both references have walked the same number of nodes, so equal references are either the first shared node or `null` together.

**Complexity.**
- **Time** is O(m + n), because each reference walks each list at most once.
- **Space** is O(1), because the method stores two references.

```java run
import java.util.*;

public final class IntersectionSwitch {
    static final class Node {
        int val;
        Node next;
        Node(int val, Node next) { this.val = val; this.next = next; }
    }

    /**
     * Returns the first shared node, or null.
     * Time: O(m + n), because each reference walks both lists at most once.
     * Space: O(1), because two references are stored.
     * Invariant: both references have walked the same number of nodes at each test.
     */
    static Node getIntersectionNode(Node headA, Node headB) {
        Node pa = headA, pb = headB;
        // Equal references are the shared node, or null together when nothing is shared.
        while (pa != pb) {
            pa = (pa == null) ? headB : pa.next;      // switch lists after the end
            pb = (pb == null) ? headA : pb.next;
        }
        return pa;
    }

    static Node build(int[] vals, Node tail) {
        Node head = tail;
        // Build from the back so the last built node links to the given tail.
        for (int i = vals.length - 1; i >= 0; i--) head = new Node(vals[i], head);
        return head;
    }

    /** Oracle: the first node of a that appears in b, found with an identity set. */
    static Node oracle(Node a, Node b) {
        Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node c = b; c != null; c = c.next) seen.add(c);
        for (Node c = a; c != null; c = c.next) if (seen.contains(c)) return c;
        return null;
    }

    public static void main(String[] args) {
        // Example 1: the shared tail starts at the node 8, and the equal values 1 and 5 are different nodes.
        Node tail = build(new int[] {8, 4, 5}, null);
        Node a = build(new int[] {4, 1}, tail), b = build(new int[] {5, 6, 1}, tail);
        if (getIntersectionNode(a, b) != tail) throw new AssertionError("ex1");
        // Example 2: no shared node returns null.
        if (getIntersectionNode(build(new int[] {2, 6, 4}, null), build(new int[] {1, 5}, null)) != null) throw new AssertionError("ex2");
        // Lists that are the same list return their head.
        if (getIntersectionNode(a, a) != a) throw new AssertionError("same");
        // Random pairs with random prefixes (1 to 5 nodes) and tails must match the oracle.
        Random rnd = new Random(64);
        for (int t = 0; t < 2000; t++) {
            int s = rnd.nextInt(4);
            int[] sv = new int[s];
            for (int i = 0; i < s; i++) sv[i] = rnd.nextInt(3);
            Node sh = build(sv, null);
            Node x = build(new int[1 + rnd.nextInt(5)], sh), y = build(new int[1 + rnd.nextInt(5)], sh);
            if (getIntersectionNode(x, y) != oracle(x, y)) throw new AssertionError("random " + t);
        }
    }
}
```
