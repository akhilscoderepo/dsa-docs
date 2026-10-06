<!-- solutions-for: 91-copy-a-list-with-random-links -->
### Solutions For Copying A List

#### Solution: [Build] Original-To-Clone Map (Author exercise)
<!-- id: ll-copy-map -->

**Approach.**
One walk along `next` puts one entry in a hash map for each original node. The key is the original node, and the value is a new node with the same value and `null` links. The map compares keys by identity, because `Node` does not override `equals` or `hashCode`, so two nodes with equal values are two keys. The method returns the map size and the entry of the head, which is `null` for the empty list.

The invariant is that after `i` turns the map holds exactly the first `i` original nodes, each with its own new node.

**Complexity.**
- **Time** is O(n), because the walk makes one hop and one map insertion per node.
- **Space** is O(n), because the map holds one entry and one new node per original node.

```java run
import java.util.*;

public final class CopyMap {
    static final class Node {
        int val;
        Node next, random;
        Node(int val) { this.val = val; }
    }

    /**
     * Builds the identity map from each original node to a fresh node, and reports its size and the head's copy.
     * Time: O(n), because one hop and one insertion run per node.
     * Space: O(n), because the map and the new nodes each hold n entries.
     * Invariant: after i turns the map holds exactly the first i original nodes.
     */
    static Object[] buildMap(Node head) {
        Map<Node, Node> copyOf = new HashMap<>();     // identity keys, because Node keeps the default equals
        // One entry per node; equal values still make different keys.
        for (Node c = head; c != null; c = c.next) copyOf.put(c, new Node(c.val));
        return new Object[] {copyOf.size(), copyOf.get(head)};
    }


    /** Builds n nodes with random next-links in order and random links to any node or null. */
    static Node[] make(int n, Random rnd) {
        Node[] a = new Node[n];
        for (int i = 0; i < n; i++) a[i] = new Node(rnd.nextInt(3));       // few values, so equal values repeat
        for (int i = 0; i + 1 < n; i++) a[i].next = a[i + 1];
        // A random link is null one time in four, and otherwise any node, including its own node.
        for (int i = 0; i < n; i++) a[i].random = rnd.nextInt(4) == 0 ? null : a[rnd.nextInt(n)];
        return a;
    }

    /** Position of each node in an identity map, with null mapped to -1 by the caller. */
    static int pos(Map<Node, Integer> index, Node x) { return x == null ? -1 : index.get(x); }

    /** Checks that copyHead is a deep copy of the n original nodes in orig. */
    static void verifyCopy(Node[] orig, Node copyHead, String tag) {
        int n = orig.length;
        Map<Node, Integer> origIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) origIndex.put(orig[i], i);
        List<Node> cp = new ArrayList<>();
        // Walk the copy by next; a copy that shares a node with the original would be caught below.
        for (Node c = copyHead; c != null && cp.size() <= n; c = c.next) cp.add(c);
        if (cp.size() != n) throw new AssertionError(tag + " length " + cp.size() + " vs " + n);
        Map<Node, Integer> cpIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) cpIndex.put(cp.get(i), i);
        for (int i = 0; i < n; i++) {
            Node k = cp.get(i), o = orig[i];
            if (origIndex.containsKey(k)) throw new AssertionError(tag + " shares node " + i);
            if (k.val != o.val) throw new AssertionError(tag + " value " + i);
            if (k.next != (i + 1 < n ? cp.get(i + 1) : null)) throw new AssertionError(tag + " next " + i);
            if (o.random == null ? k.random != null : (k.random == null || origIndex.containsKey(k.random) || cpIndex.get(k.random) != origIndex.get(o.random)))
                throw new AssertionError(tag + " random " + i);
        }
    }

    /** Records the original random positions so a later check can prove the original is unchanged. */
    static int[] snapshot(Node[] orig) {
        Map<Node, Integer> index = new IdentityHashMap<>();
        for (int i = 0; i < orig.length; i++) index.put(orig[i], i);
        int[] s = new int[orig.length];
        for (int i = 0; i < orig.length; i++) s[i] = pos(index, orig[i].random);
        return s;
    }

    public static void main(String[] args) {
        // Example 1: three nodes give three entries and a new node holding 5.
        Node[] a = make(3, new Random(1));
        a[0].val = 5; a[1].val = 8; a[2].val = 2;
        Object[] r = buildMap(a[0]);
        if ((int) r[0] != 3 || ((Node) r[1]).val != 5 || r[1] == a[0]) throw new AssertionError("ex1");
        // Example 2: equal values stay apart because the keys are identities.
        a = make(2, new Random(2));
        a[0].val = 7; a[1].val = 7;
        r = buildMap(a[0]);
        if ((int) r[0] != 2) throw new AssertionError("ex2 size");
        // The empty list gives size 0 and no head copy.
        r = buildMap(null);
        if ((int) r[0] != 0 || r[1] != null) throw new AssertionError("empty");
        // Random lists: the size is n, the head copy is new, and the original links are unchanged.
        Random rnd = new Random(101);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(10);
            a = make(n, rnd);
            int[] before = snapshot(a);
            r = buildMap(a[0]);
            Node headCopy = (Node) r[1];
            if ((int) r[0] != n || headCopy == a[0] || headCopy.val != a[0].val) throw new AssertionError("random " + t);
            if (!Arrays.equals(before, snapshot(a))) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Vary] Copy List with Random Pointer (LeetCode 138)
<!-- id: ll-copy-random -->

**Approach.**
The first pass creates one new node per original node and stores the pairing in an identity map. The second pass walks the original list again and, for each original node, reads its copy from the map. It assigns the copy's `next` from the map entry of the original `next`, and the copy's `random` from the map entry of the original `random`. A `null` link maps to `null`, so the end of the list and an empty random link need no branch.

The invariant of the second pass is that every lookup finds an entry, because the first pass finished, and no new node is created. The links of the original are only read.

**Complexity.**
- **Time** is O(n), because each pass makes one hop and one map operation per node.
- **Space** is O(n), because the map and the copies hold n entries and n new nodes.

```java run
import java.util.*;

public final class CopyRandom {
    static final class Node {
        int val;
        Node next, random;
        Node(int val) { this.val = val; }
    }

    /**
     * Returns a deep copy of the list.
     * Time: O(n), because two passes each do constant work per node.
     * Space: O(n), because the map and the copy hold n entries and n nodes.
     * Invariant: after pass one every original node has exactly one copy, and pass two only reads the map.
     */
    static Node copyRandomList(Node head) {
        Map<Node, Node> copyOf = new HashMap<>();
        // Pass one: one new node per original node.
        for (Node c = head; c != null; c = c.next) copyOf.put(c, new Node(c.val));
        // Pass two: wire both links by lookup; get(null) returns null.
        for (Node c = head; c != null; c = c.next) {
            Node k = copyOf.get(c);
            k.next = copyOf.get(c.next);
            k.random = copyOf.get(c.random);
        }
        return copyOf.get(head);
    }


    /** Builds n nodes with random next-links in order and random links to any node or null. */
    static Node[] make(int n, Random rnd) {
        Node[] a = new Node[n];
        for (int i = 0; i < n; i++) a[i] = new Node(rnd.nextInt(3));       // few values, so equal values repeat
        for (int i = 0; i + 1 < n; i++) a[i].next = a[i + 1];
        // A random link is null one time in four, and otherwise any node, including its own node.
        for (int i = 0; i < n; i++) a[i].random = rnd.nextInt(4) == 0 ? null : a[rnd.nextInt(n)];
        return a;
    }

    /** Position of each node in an identity map, with null mapped to -1 by the caller. */
    static int pos(Map<Node, Integer> index, Node x) { return x == null ? -1 : index.get(x); }

    /** Checks that copyHead is a deep copy of the n original nodes in orig. */
    static void verifyCopy(Node[] orig, Node copyHead, String tag) {
        int n = orig.length;
        Map<Node, Integer> origIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) origIndex.put(orig[i], i);
        List<Node> cp = new ArrayList<>();
        // Walk the copy by next; a copy that shares a node with the original would be caught below.
        for (Node c = copyHead; c != null && cp.size() <= n; c = c.next) cp.add(c);
        if (cp.size() != n) throw new AssertionError(tag + " length " + cp.size() + " vs " + n);
        Map<Node, Integer> cpIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) cpIndex.put(cp.get(i), i);
        for (int i = 0; i < n; i++) {
            Node k = cp.get(i), o = orig[i];
            if (origIndex.containsKey(k)) throw new AssertionError(tag + " shares node " + i);
            if (k.val != o.val) throw new AssertionError(tag + " value " + i);
            if (k.next != (i + 1 < n ? cp.get(i + 1) : null)) throw new AssertionError(tag + " next " + i);
            if (o.random == null ? k.random != null : (k.random == null || origIndex.containsKey(k.random) || cpIndex.get(k.random) != origIndex.get(o.random)))
                throw new AssertionError(tag + " random " + i);
        }
    }

    /** Records the original random positions so a later check can prove the original is unchanged. */
    static int[] snapshot(Node[] orig) {
        Map<Node, Integer> index = new IdentityHashMap<>();
        for (int i = 0; i < orig.length; i++) index.put(orig[i], i);
        int[] s = new int[orig.length];
        for (int i = 0; i < orig.length; i++) s[i] = pos(index, orig[i].random);
        return s;
    }

    public static void main(String[] args) {
        // Example 1: values 5,8,2 with random positions 2, none and 0.
        Node[] a = make(3, new Random(3));
        a[0].val = 5; a[1].val = 8; a[2].val = 2;
        a[0].random = a[2]; a[1].random = null; a[2].random = a[0];
        verifyCopy(a, copyRandomList(a[0]), "ex1");
        // Example 2: two nodes that point at each other.
        a = make(2, new Random(4));
        a[0].random = a[1]; a[1].random = a[0];
        Node c = copyRandomList(a[0]);
        verifyCopy(a, c, "ex2");
        if (c.random != c.next || c.next.random != c) throw new AssertionError("ex2 links");
        // The empty list copies to null.
        if (copyRandomList(null) != null) throw new AssertionError("empty");
        // Random lists must be deep copies, and the original must keep its links.
        Random rnd = new Random(102);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(10);
            a = make(n, rnd);
            int[] before = snapshot(a);
            verifyCopy(a, copyRandomList(a[0]), "random " + t);
            if (!Arrays.equals(before, snapshot(a))) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Boundary] Null, Self, And Shared Random Targets (Author exercise)
<!-- id: ll-copy-edges -->

**Approach.**
Every allocation happens in the first pass, through one factory method that increments a counter. The second pass only calls `map.get`, which never allocates, so a `random` link that is `null`, points at its own node, or points at a node that other links also target adds no node. The count after the call therefore equals the number of original nodes.

The invariant is that the map has exactly one entry per original node after pass one, so the number of allocations equals `n` and stays `n` through pass two.

**Complexity.**
- **Time** is O(n), because each pass does constant work per node.
- **Space** is O(n), because the map and the copies hold n entries and n nodes.

```java run
import java.util.*;

public final class CopyEdges {
    static final class Node {
        int val;
        Node next, random;
        Node(int val) { this.val = val; }
    }

    static int allocations;                           // counts nodes created by the last call

    static Node fresh(int val) { allocations++; return new Node(val); }

    /**
     * Returns a deep copy and counts the nodes that the call allocates.
     * Time: O(n), because each pass does constant work per node.
     * Space: O(n), because the map and the copy hold n entries and n nodes.
     * Invariant: only pass one allocates, so allocations equals n.
     */
    static Node copy(Node head) {
        allocations = 0;
        Map<Node, Node> copyOf = new HashMap<>();
        // Pass one is the only place that allocates.
        for (Node c = head; c != null; c = c.next) copyOf.put(c, fresh(c.val));
        // Pass two reads the map and never allocates, even for repeated or self targets.
        for (Node c = head; c != null; c = c.next) {
            Node k = copyOf.get(c);
            k.next = copyOf.get(c.next);
            k.random = copyOf.get(c.random);
        }
        return copyOf.get(head);
    }


    /** Builds n nodes with random next-links in order and random links to any node or null. */
    static Node[] make(int n, Random rnd) {
        Node[] a = new Node[n];
        for (int i = 0; i < n; i++) a[i] = new Node(rnd.nextInt(3));       // few values, so equal values repeat
        for (int i = 0; i + 1 < n; i++) a[i].next = a[i + 1];
        // A random link is null one time in four, and otherwise any node, including its own node.
        for (int i = 0; i < n; i++) a[i].random = rnd.nextInt(4) == 0 ? null : a[rnd.nextInt(n)];
        return a;
    }

    /** Position of each node in an identity map, with null mapped to -1 by the caller. */
    static int pos(Map<Node, Integer> index, Node x) { return x == null ? -1 : index.get(x); }

    /** Checks that copyHead is a deep copy of the n original nodes in orig. */
    static void verifyCopy(Node[] orig, Node copyHead, String tag) {
        int n = orig.length;
        Map<Node, Integer> origIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) origIndex.put(orig[i], i);
        List<Node> cp = new ArrayList<>();
        // Walk the copy by next; a copy that shares a node with the original would be caught below.
        for (Node c = copyHead; c != null && cp.size() <= n; c = c.next) cp.add(c);
        if (cp.size() != n) throw new AssertionError(tag + " length " + cp.size() + " vs " + n);
        Map<Node, Integer> cpIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) cpIndex.put(cp.get(i), i);
        for (int i = 0; i < n; i++) {
            Node k = cp.get(i), o = orig[i];
            if (origIndex.containsKey(k)) throw new AssertionError(tag + " shares node " + i);
            if (k.val != o.val) throw new AssertionError(tag + " value " + i);
            if (k.next != (i + 1 < n ? cp.get(i + 1) : null)) throw new AssertionError(tag + " next " + i);
            if (o.random == null ? k.random != null : (k.random == null || origIndex.containsKey(k.random) || cpIndex.get(k.random) != origIndex.get(o.random)))
                throw new AssertionError(tag + " random " + i);
        }
    }

    /** Records the original random positions so a later check can prove the original is unchanged. */
    static int[] snapshot(Node[] orig) {
        Map<Node, Integer> index = new IdentityHashMap<>();
        for (int i = 0; i < orig.length; i++) index.put(orig[i], i);
        int[] s = new int[orig.length];
        for (int i = 0; i < orig.length; i++) s[i] = pos(index, orig[i].random);
        return s;
    }

    public static void main(String[] args) {
        // Example 1: values 4,6,9 with random positions 0, 2 and 2 need 3 allocations.
        Node[] a = make(3, new Random(5));
        a[0].random = a[0]; a[1].random = a[2]; a[2].random = a[2];
        verifyCopy(a, copy(a[0]), "ex1");
        if (allocations != 3) throw new AssertionError("ex1 count " + allocations);
        // Example 2: one node with a null random link needs 1 allocation.
        a = make(1, new Random(6));
        a[0].random = null;
        verifyCopy(a, copy(a[0]), "ex2");
        if (allocations != 1) throw new AssertionError("ex2 count");
        // The empty list allocates nothing.
        if (copy(null) != null || allocations != 0) throw new AssertionError("empty");
        // Random lists: the structure is a deep copy and the count is exactly n.
        Random rnd = new Random(103);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(10);
            a = make(n, rnd);
            verifyCopy(a, copy(a[0]), "random " + t);
            if (allocations != n) throw new AssertionError("count " + t);
        }
    }
}
```

#### Solution: [Recognize] Two Arbitrary References (Author exercise)
<!-- id: ll-copy-two-random -->

**Approach.**
The first pass is unchanged: it creates one new node per original node and fills the identity map. The second pass gains one line. For each original node, it assigns the copy's `next`, `randomA` and `randomB` from three lookups in the same map. Each lookup returns `null` for a `null` link and the unique copy otherwise.

The invariant is that the map pairs each original node with exactly one copy, so any number of extra links needs one more lookup and no change to the first pass.

**Complexity.**
- **Time** is O(n), because each pass does a constant number of map operations per node.
- **Space** is O(n), because the map and the copies hold n entries and n nodes.

```java run
import java.util.*;

public final class CopyTwoRandom {
    static final class Node {
        int val;
        Node next, randomA, randomB;
        Node(int val) { this.val = val; }
    }

    /**
     * Returns a deep copy of a list whose nodes have next, randomA and randomB links.
     * Time: O(n), because each pass does a constant number of map operations per node.
     * Space: O(n), because the map and the copy hold n entries and n nodes.
     * Invariant: each original node has exactly one copy, shared by all three kinds of link.
     */
    static Node copyTwoRandom(Node head) {
        Map<Node, Node> copyOf = new HashMap<>();
        // Pass one is the same for any number of links.
        for (Node c = head; c != null; c = c.next) copyOf.put(c, new Node(c.val));
        // Pass two adds one lookup per extra link.
        for (Node c = head; c != null; c = c.next) {
            Node k = copyOf.get(c);
            k.next = copyOf.get(c.next);
            k.randomA = copyOf.get(c.randomA);
            k.randomB = copyOf.get(c.randomB);
        }
        return copyOf.get(head);
    }


    /** Builds n nodes with next-links in order and two random links to any node or null. */
    static Node[] make(int n, Random rnd) {
        Node[] a = new Node[n];
        for (int i = 0; i < n; i++) a[i] = new Node(rnd.nextInt(3));
        for (int i = 0; i + 1 < n; i++) a[i].next = a[i + 1];
        // Each random link is null one time in four, and otherwise any node.
        for (int i = 0; i < n; i++) {
            a[i].randomA = rnd.nextInt(4) == 0 ? null : a[rnd.nextInt(n)];
            a[i].randomB = rnd.nextInt(4) == 0 ? null : a[rnd.nextInt(n)];
        }
        return a;
    }

    static int pos(Map<Node, Integer> index, Node x) { return x == null ? -1 : index.get(x); }

    /** Checks that copyHead is a deep copy of orig for all three links. */
    static void verifyCopy(Node[] orig, Node copyHead, String tag) {
        int n = orig.length;
        Map<Node, Integer> origIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) origIndex.put(orig[i], i);
        List<Node> cp = new ArrayList<>();
        for (Node c = copyHead; c != null && cp.size() <= n; c = c.next) cp.add(c);
        if (cp.size() != n) throw new AssertionError(tag + " length");
        Map<Node, Integer> cpIndex = new IdentityHashMap<>();
        for (int i = 0; i < n; i++) cpIndex.put(cp.get(i), i);
        for (int i = 0; i < n; i++) {
            Node k = cp.get(i), o = orig[i];
            if (origIndex.containsKey(k) || k.val != o.val) throw new AssertionError(tag + " node " + i);
            if (k.next != (i + 1 < n ? cp.get(i + 1) : null)) throw new AssertionError(tag + " next " + i);
            // Both random links must stay inside the copy and match the original position.
            if (pos(cpIndex, k.randomA) != pos(origIndex, o.randomA) || (k.randomA != null && origIndex.containsKey(k.randomA)))
                throw new AssertionError(tag + " randomA " + i);
            if (pos(cpIndex, k.randomB) != pos(origIndex, o.randomB) || (k.randomB != null && origIndex.containsKey(k.randomB)))
                throw new AssertionError(tag + " randomB " + i);
        }
    }

    public static void main(String[] args) {
        // Example 1: randomA positions 2, 0, none and randomB positions 1, 1, 2.
        Node[] a = make(3, new Random(7));
        a[0].randomA = a[2]; a[1].randomA = a[0]; a[2].randomA = null;
        a[0].randomB = a[1]; a[1].randomB = a[1]; a[2].randomB = a[2];
        verifyCopy(a, copyTwoRandom(a[0]), "ex1");
        // Example 2: every reference points at the second node.
        a = make(2, new Random(8));
        for (Node x : a) { x.randomA = a[1]; x.randomB = a[1]; }
        Node c = copyTwoRandom(a[0]);
        verifyCopy(a, c, "ex2");
        if (c.randomA != c.next || c.next.randomB != c.next) throw new AssertionError("ex2 links");
        // The empty list copies to null.
        if (copyTwoRandom(null) != null) throw new AssertionError("empty");
        // Random lists must be deep copies for all three links.
        Random rnd = new Random(104);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(10);
            a = make(n, rnd);
            verifyCopy(a, copyTwoRandom(a[0]), "random " + t);
        }
    }
}
```
