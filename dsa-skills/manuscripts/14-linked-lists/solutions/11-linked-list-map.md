<!-- solutions-for: 11-linked-list-map -->
### Linked List Map

#### Solution: [Build] Original-To-Clone Map (Author exercise)
<!-- id: llm-original-clone-map -->

**Approach.** Walk the list once and create a clone for each node. Put each pair into an `IdentityHashMap` keyed by the original node object, so every node has its own entry, and also put each clone into a `HashMap` keyed by the node's value, so that nodes with equal values overwrite one another. The two sizes are the answer. The assertions show that the identity map always has one entry per node, that the value-keyed map has one entry per distinct value, and that an ordinary `HashMap` keyed by a node class that overrides `equals` and `hashCode` by value also collapses the entries, which is why an `IdentityHashMap` is the safe choice.

**Complexity.** O(n) time and O(n) extra space for the maps.

```java run
import java.util.HashMap;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class OriginalCloneMap {
    static final class Node {
        int value;
        Node next;
        Node(int value) { this.value = value; }
    }
    static final class ValueEqualNode {
        final int value;
        ValueEqualNode(int value) { this.value = value; }
        @Override public boolean equals(Object o) { return o instanceof ValueEqualNode && ((ValueEqualNode) o).value == value; }
        @Override public int hashCode() { return Integer.hashCode(value); }
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
    static int[] sizes(Node head) {
        IdentityHashMap<Node, Node> byIdentity = new IdentityHashMap<>();
        Map<Integer, Node> byValue = new HashMap<>();
        for (Node o = head; o != null; o = o.next) {
            Node clone = new Node(o.value);
            byIdentity.put(o, clone);
            byValue.put(o.value, clone);
        }
        return new int[]{byIdentity.size(), byValue.size()};
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(sizes(build(new int[]{7, 7, 3, 7})), new int[]{4, 2})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(sizes(build(new int[]{})), new int[]{0, 0})) throw new AssertionError("example 2");
        Map<ValueEqualNode, Integer> hashed = new HashMap<>();
        IdentityHashMap<ValueEqualNode, Integer> identity = new IdentityHashMap<>();
        for (int v : new int[]{7, 7, 3, 7}) {
            ValueEqualNode n = new ValueEqualNode(v);
            hashed.put(n, 1);
            identity.put(n, 1);
        }
        if (hashed.size() != 2 || identity.size() != 4) throw new AssertionError("a value-equal key class collapses in HashMap but not in IdentityHashMap");
        Random rnd = new Random(1441);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            Set<Integer> distinct = new HashSet<>();
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(4); distinct.add(a[i]); }
            int[] got = sizes(build(a));
            if (got[0] != n || got[1] != distinct.size()) throw new AssertionError("wrong map sizes");
        }
    }
}
```

#### Solution: [Vary] Copy List with Random Pointer (LeetCode 138)
<!-- id: llm-copy-random-list -->

**Approach.** In the first pass, create a clone holding the same value for every original node and record the pair in an identity map, with no links set. In the second pass, for every original node set its clone's `next` to the clone of the original's `next` and its clone's `random` to the clone of the original's `random`, using one lookup for each and leaving null references null. Because every clone exists before any link is written, a random target that lies later in the list, earlier in the list, or at the node itself is found the same way. The result is read back as pairs of value and index in the copy. The assertions compare with the input encoding, check that no clone reference is an original node, and check that the original structure was not changed.

**Complexity.** O(n) time and O(n) extra space for the map and the clones.

```java run
import java.util.IdentityHashMap;
import java.util.Random;

public final class CopyRandomList {
    static final class Node {
        int value;
        Node next, random;
        Node(int value) { this.value = value; }
    }
    static Node[] build(int[] values, int[] random) {
        Node[] nodes = new Node[values.length];
        for (int i = 0; i < nodes.length; i++) nodes[i] = new Node(values[i]);
        for (int i = 0; i < nodes.length; i++) {
            if (i + 1 < nodes.length) nodes[i].next = nodes[i + 1];
            if (random[i] >= 0) nodes[i].random = nodes[random[i]];
        }
        return nodes;
    }
    static Node copyList(Node head) {
        if (head == null) return null;
        IdentityHashMap<Node, Node> clone = new IdentityHashMap<>();
        for (Node o = head; o != null; o = o.next) clone.put(o, new Node(o.value));
        for (Node o = head; o != null; o = o.next) {
            Node c = clone.get(o);
            c.next = o.next == null ? null : clone.get(o.next);
            c.random = o.random == null ? null : clone.get(o.random);
        }
        return clone.get(head);
    }
    static int[][] readBack(Node head) {
        IdentityHashMap<Node, Integer> index = new IdentityHashMap<>();
        int n = 0;
        for (Node c = head; c != null; c = c.next) index.put(c, n++);
        int[][] out = new int[n][2];
        int i = 0;
        for (Node c = head; c != null; c = c.next) {
            out[i][0] = c.value;
            out[i][1] = c.random == null ? -1 : index.get(c.random);
            i++;
        }
        return out;
    }

    public static void main(String[] args) {
        Node[] a = build(new int[]{5, 9, 2, 6}, new int[]{2, 0, -1, 3});
        if (!java.util.Arrays.deepEquals(readBack(copyList(a[0])), new int[][]{{5, 2}, {9, 0}, {2, -1}, {6, 3}})) throw new AssertionError("example 1");
        Node[] b = build(new int[]{4}, new int[]{-1});
        if (!java.util.Arrays.deepEquals(readBack(copyList(b[0])), new int[][]{{4, -1}})) throw new AssertionError("example 2");
        if (copyList(null) != null) throw new AssertionError("empty list");
        Random rnd = new Random(1442);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] values = new int[n], random = new int[n];
            for (int i = 0; i < n; i++) { values[i] = rnd.nextInt(3); random[i] = rnd.nextInt(n + 1) - 1; }
            Node[] originals = build(values, random);
            Node copy = copyList(originals[0]);
            int[][] got = readBack(copy);
            if (got.length != n) throw new AssertionError("wrong number of nodes");
            for (int i = 0; i < n; i++) if (got[i][0] != values[i] || got[i][1] != random[i]) throw new AssertionError("copy differs at " + i);
            IdentityHashMap<Node, Boolean> origSet = new IdentityHashMap<>();
            for (Node o : originals) origSet.put(o, true);
            for (Node c = copy; c != null; c = c.next) {
                if (origSet.containsKey(c) || (c.next != null && origSet.containsKey(c.next)) || (c.random != null && origSet.containsKey(c.random)))
                    throw new AssertionError("a clone refers to an original node");
            }
            for (int i = 0; i < n; i++) {
                if (i + 1 < n && originals[i].next != originals[i + 1]) throw new AssertionError("the original next changed");
                if (random[i] >= 0 && originals[i].random != originals[random[i]]) throw new AssertionError("the original random changed");
            }
        }
    }
}
```

#### Solution: [Boundary] Null, Self, And Shared Random Targets (Author exercise)
<!-- id: llm-null-self-shared -->

**Approach.** Clone with the identity map in two passes, creating all clones first and wiring afterwards. Then read the clone: count the clone nodes whose random reference is null, those whose random reference is the clone node itself, and, with a second identity map counting how many clone nodes point at each target, the targets pointed at by two or more. A lookup for a self reference returns the node's own clone, and a lookup for a shared target returns the same clone object each time, since each original has exactly one clone. The assertions compare the three counts with counts computed from the encoding alone, and check that the number of distinct clone objects is exactly n.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.IdentityHashMap;
import java.util.Random;

public final class NullSelfShared {
    static final class Node {
        int value;
        Node next, random;
        Node(int value) { this.value = value; }
    }
    static Node[] build(int[] values, int[] random) {
        Node[] nodes = new Node[values.length];
        for (int i = 0; i < nodes.length; i++) nodes[i] = new Node(values[i]);
        for (int i = 0; i < nodes.length; i++) {
            if (i + 1 < nodes.length) nodes[i].next = nodes[i + 1];
            if (random[i] >= 0) nodes[i].random = nodes[random[i]];
        }
        return nodes;
    }
    static Node copyList(Node head) {
        if (head == null) return null;
        IdentityHashMap<Node, Node> clone = new IdentityHashMap<>();
        for (Node o = head; o != null; o = o.next) clone.put(o, new Node(o.value));
        for (Node o = head; o != null; o = o.next) {
            Node c = clone.get(o);
            c.next = o.next == null ? null : clone.get(o.next);
            c.random = o.random == null ? null : clone.get(o.random);
        }
        return clone.get(head);
    }
    static int[] report(Node copy, int expectedNodes) {
        IdentityHashMap<Node, Integer> pointedAt = new IdentityHashMap<>();
        IdentityHashMap<Node, Boolean> distinct = new IdentityHashMap<>();
        int nulls = 0, selves = 0;
        for (Node c = copy; c != null; c = c.next) {
            distinct.put(c, true);
            if (c.random == null) nulls++;
            else {
                if (c.random == c) selves++;
                pointedAt.merge(c.random, 1, Integer::sum);
            }
        }
        if (distinct.size() != expectedNodes) throw new AssertionError("wrong number of distinct clones");
        int shared = 0;
        for (int count : pointedAt.values()) if (count >= 2) shared++;
        return new int[]{nulls, selves, shared};
    }
    static int[] fromEncoding(int[] random) {
        int nulls = 0, selves = 0, shared = 0;
        int[] counts = new int[random.length];
        for (int i = 0; i < random.length; i++) {
            if (random[i] < 0) nulls++;
            else { counts[random[i]]++; if (random[i] == i) selves++; }
        }
        for (int c : counts) if (c >= 2) shared++;
        return new int[]{nulls, selves, shared};
    }

    public static void main(String[] args) {
        int[] r1 = {-1, 1, 2, 2};
        Node[] a = build(new int[]{1, 2, 3, 4}, r1);
        if (!java.util.Arrays.equals(report(copyList(a[0]), 4), new int[]{1, 2, 1})) throw new AssertionError("example 1");
        Node[] b = build(new int[]{8}, new int[]{0});
        if (!java.util.Arrays.equals(report(copyList(b[0]), 1), new int[]{0, 1, 0})) throw new AssertionError("example 2");
        Random rnd = new Random(1443);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] values = new int[n], random = new int[n];
            for (int i = 0; i < n; i++) { values[i] = rnd.nextInt(2); random[i] = rnd.nextInt(n + 1) - 1; }
            Node[] originals = build(values, random);
            if (!java.util.Arrays.equals(report(copyList(originals[0]), n), fromEncoding(random))) throw new AssertionError("counts differ from the encoding");
        }
    }
}
```

#### Solution: [Recognize] Two Arbitrary References (Author exercise)
<!-- id: llm-two-references -->

**Approach.** The identity-map invariant does not depend on the number of references a node has. In the first pass create a clone for every original node and record the pair. In the second pass, for each original, set its clone's `next`, `a` and `b` to the lookups of the original's references, leaving null references null. Every clone exists before any link is written, so each lookup succeeds. The result is read back as triples of value and the two target positions in the clone. The assertions compare with the input encoding, include lists where all values are equal, and check that no clone reference points to an original.

**Complexity.** O(n) time and O(n) extra space for the map and the clones.

```java run
import java.util.IdentityHashMap;
import java.util.Random;

public final class TwoReferences {
    static final class Wide {
        int value;
        Wide next, a, b;
        Wide(int value) { this.value = value; }
    }
    static Wide[] build(int[] values, int[] a, int[] b) {
        Wide[] nodes = new Wide[values.length];
        for (int i = 0; i < nodes.length; i++) nodes[i] = new Wide(values[i]);
        for (int i = 0; i < nodes.length; i++) {
            if (i + 1 < nodes.length) nodes[i].next = nodes[i + 1];
            if (a[i] >= 0) nodes[i].a = nodes[a[i]];
            if (b[i] >= 0) nodes[i].b = nodes[b[i]];
        }
        return nodes;
    }
    static Wide copyWide(Wide head) {
        if (head == null) return null;
        IdentityHashMap<Wide, Wide> clone = new IdentityHashMap<>();
        for (Wide o = head; o != null; o = o.next) clone.put(o, new Wide(o.value));
        for (Wide o = head; o != null; o = o.next) {
            Wide c = clone.get(o);
            c.next = o.next == null ? null : clone.get(o.next);
            c.a = o.a == null ? null : clone.get(o.a);
            c.b = o.b == null ? null : clone.get(o.b);
        }
        return clone.get(head);
    }
    static int[][] readBack(Wide head) {
        IdentityHashMap<Wide, Integer> index = new IdentityHashMap<>();
        int n = 0;
        for (Wide c = head; c != null; c = c.next) index.put(c, n++);
        int[][] out = new int[n][3];
        int i = 0;
        for (Wide c = head; c != null; c = c.next) {
            out[i][0] = c.value;
            out[i][1] = c.a == null ? -1 : index.get(c.a);
            out[i][2] = c.b == null ? -1 : index.get(c.b);
            i++;
        }
        return out;
    }

    public static void main(String[] args) {
        Wide[] x = build(new int[]{3, 5, 8}, new int[]{2, -1, 0}, new int[]{1, 1, -1});
        if (!java.util.Arrays.deepEquals(readBack(copyWide(x[0])), new int[][]{{3, 2, 1}, {5, -1, 1}, {8, 0, -1}})) throw new AssertionError("example 1");
        Wide[] y = build(new int[]{6, 6}, new int[]{1, 0}, new int[]{0, 1});
        if (!java.util.Arrays.deepEquals(readBack(copyWide(y[0])), new int[][]{{6, 1, 0}, {6, 0, 1}})) throw new AssertionError("example 2");
        Random rnd = new Random(1444);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] values = new int[n], a = new int[n], b = new int[n];
            for (int i = 0; i < n; i++) { values[i] = rnd.nextInt(2); a[i] = rnd.nextInt(n + 1) - 1; b[i] = rnd.nextInt(n + 1) - 1; }
            Wide[] originals = build(values, a, b);
            Wide copy = copyWide(originals[0]);
            int[][] got = readBack(copy);
            if (got.length != n) throw new AssertionError("wrong number of nodes");
            for (int i = 0; i < n; i++)
                if (got[i][0] != values[i] || got[i][1] != a[i] || got[i][2] != b[i]) throw new AssertionError("copy differs at " + i);
            IdentityHashMap<Wide, Boolean> origSet = new IdentityHashMap<>();
            for (Wide o : originals) origSet.put(o, true);
            for (Wide c = copy; c != null; c = c.next)
                if (origSet.containsKey(c) || (c.a != null && origSet.containsKey(c.a)) || (c.b != null && origSet.containsKey(c.b)))
                    throw new AssertionError("a clone refers to an original node");
        }
    }
}
```
