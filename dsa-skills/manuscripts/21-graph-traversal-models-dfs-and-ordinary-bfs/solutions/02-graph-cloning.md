<!-- solutions-for: 02-graph-cloning -->
### Solutions For Graph Cloning

#### Solution: [Build] Clone One Edge (Author exercise)
<!-- id: gt-clone-one-edge -->

**Approach.**
The method creates the clone of `a` and then the clone of `b`, and only afterwards connects them. Both objects exist before either neighbor list is filled, so each list can hold a reference to an object that is already complete. The method adds the clone of `b` to the clone of `a` and the clone of `a` to the clone of `b`.

The invariant is that every wired reference points to a clone and never to an original.

**Complexity.**
- **Time** is O(1), because the method creates two nodes and performs two appends.
- **Space** is O(1), because the result holds two nodes and two references.

```java run
import java.util.*;

public final class CloneOneEdge {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    /**
     * Returns a clone of a, where a and its only neighbor form one undirected edge.
     * Time: O(1). Space: O(1).
     * Invariant: every reference in the result points to a clone, never to an original.
     */
    static Node cloneEdge(Node a) {
        Node b = a.neighbors.get(0);                 // the only other original node
        Node cloneA = new Node(a.val);               // first clone exists before any wiring
        Node cloneB = new Node(b.val);               // second clone exists before any wiring
        cloneA.neighbors.add(cloneB);                // the copied edge in one direction
        cloneB.neighbors.add(cloneA);                // the copied edge in the other direction
        return cloneA;                               // the caller receives the clone of a
    }

    public static void main(String[] args) {
        // Both exercise examples: values 0,1 and values 1,0.
        for (int[] vals : new int[][] {{0, 1}, {1, 0}}) {
            Node a = new Node(vals[0]), b = new Node(vals[1]);
            a.neighbors.add(b);
            b.neighbors.add(a);
            Node c = cloneEdge(a);
            // The clone keeps the values and the shape of the edge.
            if (c.val != vals[0] || c.neighbors.size() != 1 || c.neighbors.get(0).val != vals[1]) throw new AssertionError("shape " + vals[0]);
            // The edge points back to the clone itself, not to the original.
            if (c.neighbors.get(0).neighbors.get(0) != c) throw new AssertionError("back reference " + vals[0]);
            // No result object is an input object.
            if (c == a || c == b || c.neighbors.get(0) == a || c.neighbors.get(0) == b) throw new AssertionError("identity " + vals[0]);
            // The input is unchanged.
            if (a.neighbors.size() != 1 || a.neighbors.get(0) != b || b.neighbors.get(0) != a) throw new AssertionError("mutation " + vals[0]);
        }
    }
}
```

#### Solution: [Vary] Clone A Cycle (Author exercise)
<!-- id: gt-clone-cycle -->

**Approach.**
The method uses a queue of original nodes that still need their neighbors wired. When a node enters the map, its clone is created at the same moment, so the entry exists before the node is processed. The method pops an original, looks at each neighbor and creates a clone only when the neighbor has no entry yet. It then adds the stored clone to the clone of the popped node.

In a cycle, the last node lists the first node. The first node already has an entry, so the method reuses its clone and the loop closes. The invariant is that the map holds exactly one clone for each node that has entered the queue.

**Complexity.**
- **Time** is O(k), because each of the `k` nodes enters the queue once and has one neighbor to read.
- **Space** is O(k), because the map and the queue together hold at most `k` entries each.

```java run
import java.util.*;

public final class CloneCycle {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int v) { val = v; }
    }

    /**
     * Returns the clone of start for a graph reachable from start, using a queue.
     * Time: O(n + m). Space: O(n).
     * Invariant: clones holds exactly one clone for each node that has entered the queue.
     */
    static Node cloneFrom(Node start) {
        Map<Node, Node> clones = new HashMap<>();                    // identity map from original to clone
        Deque<Node> queue = new ArrayDeque<>();                      // originals whose neighbors are not wired yet
        clones.put(start, new Node(start.val));                      // the entry exists before any neighbor is read
        queue.add(start);                                            // start is the first original to process
        while (!queue.isEmpty()) {                                   // each node is polled once
            Node original = queue.poll();                            // next original to wire
            for (Node next : original.neighbors) {                   // one read per reference
                if (!clones.containsKey(next)) {                     // a new node needs its clone and a place in the queue
                    clones.put(next, new Node(next.val));            // entry stored at discovery time
                    queue.add(next);                                 // wired later, when polled
                }
                clones.get(original).neighbors.add(clones.get(next)); // always wire to the stored clone
            }
        }
        return clones.get(start);                                    // clone of the start node
    }

    /** Builds the directed cycle 0 to k-1 and returns its nodes. */
    static Node[] cycle(int k) {
        Node[] nodes = new Node[k];
        for (int i = 0; i < k; i++) nodes[i] = new Node(i);
        for (int i = 0; i < k; i++) nodes[i].neighbors.add(nodes[(i + 1) % k]);
        return nodes;
    }

    /** Oracle: values met when walking neighbors.get(0) for k steps from a node. */
    static List<Integer> walk(Node from, int k) {
        List<Integer> out = new ArrayList<>();
        Node cur = from;
        out.add(cur.val);
        for (int i = 0; i < k; i++) { cur = cur.neighbors.get(0); out.add(cur.val); }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: k = 3, start 0.
        if (!walk(cloneFrom(cycle(3)[0]), 3).equals(List.of(0, 1, 2, 0))) throw new AssertionError("ex1");
        // Example 2: k = 4, start 2.
        if (!walk(cloneFrom(cycle(4)[2]), 4).equals(List.of(2, 3, 0, 1, 2))) throw new AssertionError("ex2");
        // Random cycle sizes and starts: the walk closes after k steps, and the clone never touches the originals.
        Random rnd = new Random(2102);
        for (int t = 0; t < 300; t++) {
            int k = 2 + rnd.nextInt(30), s = rnd.nextInt(k);
            Node[] orig = cycle(k);
            Node c = cloneFrom(orig[s]);
            List<Integer> w = walk(c, k);
            if (w.get(0) != s || !w.get(k).equals(w.get(0))) throw new AssertionError("closed walk " + t);
            Set<Node> originals = Collections.newSetFromMap(new IdentityHashMap<>());
            originals.addAll(Arrays.asList(orig));
            Node cur = c;
            for (int i = 0; i < k; i++) {
                if (originals.contains(cur)) throw new AssertionError("original reached " + t);
                cur = cur.neighbors.get(0);
            }
            if (cur != c) throw new AssertionError("loop returns to the clone " + t);
        }
    }
}
```

#### Solution: [Boundary] Null And Self-Loop (Author exercise)
<!-- id: gt-null-self-loop -->

**Approach.**
The method first returns `null` for a `null` start, because an empty structure has an empty copy. For a real node, a recursive helper stores the new clone in the map and only then reads the neighbor list. A node that lists itself finds its own entry already present, so the helper adds the clone to its own list. Without the early entry, the helper would recurse on the same node forever.

Because the helper processes neighbors in list order and appends one result per neighbor, every clone keeps the neighbor order of its original. The invariant is that the map holds exactly one clone for each node the helper has entered.

**Complexity.**
- **Time** is O(n + m), because each node is entered once and each reference is read once.
- **Space** is O(n), because the map holds one entry per node and the recursion depth is at most `n`.

```java run
import java.util.*;

public final class NullAndSelfLoop {
    static final class Node {
        final int val;
        final List<Node> neighbors;
        Node(int val, List<Node> neighbors) { this.val = val; this.neighbors = neighbors; }
    }

    /**
     * Returns null for a null start, otherwise a clone that keeps self-loops and neighbor order.
     * Time: O(n + m). Space: O(n).
     * Invariant: seen holds exactly one clone for each node that the helper has entered.
     */
    static Node copyOf(Node start) {
        if (start == null) return null;                              // absence stays absence
        return fill(start, new IdentityHashMap<>());                 // identity keys make labels irrelevant
    }

    static Node fill(Node original, Map<Node, Node> seen) {
        Node twin = new Node(original.val, new ArrayList<>());      // new node with an empty list
        seen.put(original, twin);                                    // entry first, so a self-loop finds it
        for (Node next : original.neighbors) {                       // one read per reference, in list order
            if (seen.containsKey(next)) twin.neighbors.add(seen.get(next)); // known node: reuse its clone
            else twin.neighbors.add(fill(next, seen));               // new node: copy it, then wire it
        }
        return twin;                                                 // the clone is complete after the loop
    }

    /** Builds nodes from neighbor lists; node i has value i. */
    static Node[] make(int[][] adj) {
        Node[] nodes = new Node[adj.length];
        for (int i = 0; i < adj.length; i++) nodes[i] = new Node(i, new ArrayList<>());
        for (int i = 0; i < adj.length; i++) for (int j : adj[i]) nodes[i].neighbors.add(nodes[j]);
        return nodes;
    }

    /** Oracle: values of the neighbors of every node reachable from the start, collected by an independent traversal. */
    static Map<Integer, List<Integer>> shape(Node start) {
        Map<Integer, List<Integer>> out = new TreeMap<>();
        Deque<Node> stack = new ArrayDeque<>();
        stack.push(start);
        while (!stack.isEmpty()) {
            Node n = stack.pop();
            if (out.containsKey(n.val)) continue;
            List<Integer> vals = new ArrayList<>();
            for (Node m : n.neighbors) { vals.add(m.val); stack.push(m); }
            out.put(n.val, vals);
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: null stays null.
        if (copyOf(null) != null) throw new AssertionError("null");
        // Example 2: one node with a self-loop gives a clone that lists itself, and is not the original.
        Node one = make(new int[][] {{0}})[0];
        Node c = copyOf(one);
        if (c == one || c.val != 0 || c.neighbors.size() != 1) throw new AssertionError("self-loop shape");
        if (c.neighbors.get(0) != c) throw new AssertionError("clone lists itself");
        if (one.neighbors.get(0) != one) throw new AssertionError("original unchanged");
        // Random graphs with self-loops: shape and neighbor order match, and no original is shared.
        Random rnd = new Random(2103);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] adj = new int[n][];
            for (int i = 0; i < n; i++) {
                List<Integer> l = new ArrayList<>();
                for (int j = 0; j < n; j++) if (rnd.nextInt(3) == 0) l.add(j);
                Collections.shuffle(l, rnd);
                adj[i] = l.stream().mapToInt(Integer::intValue).toArray();
            }
            Node[] orig = make(adj);
            int s = rnd.nextInt(n);
            Node got = copyOf(orig[s]);
            if (!shape(got).equals(shape(orig[s]))) throw new AssertionError("shape " + t);
            Set<Node> originals = Collections.newSetFromMap(new IdentityHashMap<>());
            originals.addAll(Arrays.asList(orig));
            Deque<Node> stack = new ArrayDeque<>();
            Set<Node> seenNodes = Collections.newSetFromMap(new IdentityHashMap<>());
            stack.push(got);
            while (!stack.isEmpty()) {
                Node x = stack.pop();
                if (!seenNodes.add(x)) continue;
                if (originals.contains(x)) throw new AssertionError("shared original " + t);
                for (Node y : x.neighbors) stack.push(y);
            }
            if (seenNodes.size() != shape(orig[s]).size()) throw new AssertionError("one clone per node " + t);
        }
    }
}
```

#### Solution: [Recognize] Clone Graph (LeetCode 133)
<!-- id: gt-clone-graph -->

**Approach.**
The method builds the clones for exactly the nodes that a traversal from the start discovers. It keeps a `HashMap` from each original node to its clone and uses recursion. The helper stores the clone before it reads the neighbors, so a loop or a shared reference finds an existing entry and reuses it. Nodes that the start cannot reach never enter the map, so they never appear in the copy.

The map is keyed by the node object, not by its value. `Node` does not override `equals`, so the map treats two nodes as different keys even when their values match. The invariant is that the map holds exactly one clone for each discovered original node.

**Complexity.**
- **Time** is O(n + m) over the reachable part, because each node is entered once and each reference is read once.
- **Space** is O(n) for the map and the recursion stack, plus O(n + m) for the clones themselves.

```java run
import java.util.*;

public final class CloneGraph {
    static final class Node {
        int val;
        List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    /**
     * Returns a deep copy of the part of the graph reachable from start.
     * Time: O(n + m). Space: O(n).
     * Invariant: clones holds exactly one clone for each discovered original node.
     */
    static Node cloneGraph(Node start, Map<Node, Node> clones) {
        Node clone = new Node(start.val);                            // new node for this original
        clones.put(start, clone);                                    // entry before neighbors: ends loops, shares targets
        for (Node next : start.neighbors) {                          // each reference is read once
            Node known = clones.get(next);                           // O(1) lookup by object identity
            clone.neighbors.add(known != null ? known : cloneGraph(next, clones)); // reuse, or discover and copy
        }
        return clone;                                                // complete clone of this original
    }

    /** Builds the original nodes; node i has value i and neighbors adj[i]. */
    static Node[] make(int[][] adj) {
        Node[] nodes = new Node[adj.length];
        for (int i = 0; i < adj.length; i++) nodes[i] = new Node(i);
        for (int i = 0; i < adj.length; i++) for (int j : adj[i]) nodes[i].neighbors.add(nodes[j]);
        return nodes;
    }

    /** Oracle: reachable set by a plain stack, then neighbor value lists per value. */
    static List<List<Integer>> shape(Node start) {
        TreeMap<Integer, List<Integer>> out = new TreeMap<>();
        Deque<Node> stack = new ArrayDeque<>();
        stack.push(start);
        while (!stack.isEmpty()) {
            Node n = stack.pop();
            if (out.containsKey(n.val)) continue;
            List<Integer> vals = new ArrayList<>();
            for (Node m : n.neighbors) { vals.add(m.val); stack.push(m); }
            out.put(n.val, vals);
        }
        return new ArrayList<>(out.values());
    }

    public static void main(String[] args) {
        // Example 1: all four nodes are reachable from 0.
        int[][] adj1 = {{1, 2}, {0, 2}, {0, 1, 3}, {2}};
        if (!shape(cloneGraph(make(adj1)[0], new HashMap<>())).toString().equals("[[1, 2], [0, 2], [0, 1, 3], [2]]")) throw new AssertionError("ex1");
        // Example 2: only nodes 2 and 3 are reachable from 2, so the copy has two nodes.
        int[][] adj2 = {{1}, {0}, {3}, {2}};
        if (!shape(cloneGraph(make(adj2)[2], new HashMap<>())).toString().equals("[[3], [2]]")) throw new AssertionError("ex2");
        // The prose claim: Node has no equals override, so two nodes with equal values are different keys.
        Map<Node, Node> keys = new HashMap<>();
        keys.put(new Node(5), new Node(1));
        keys.put(new Node(5), new Node(2));
        if (keys.size() != 2) throw new AssertionError("identity keys");
        // Random graphs: the shape matches, the map holds one clone per reachable node, and no original is reused.
        Random rnd = new Random(2104);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] adj = new int[n][];
            for (int i = 0; i < n; i++) {
                List<Integer> l = new ArrayList<>();
                for (int j = 0; j < n; j++) if (j != i && rnd.nextInt(3) == 0) l.add(j);
                adj[i] = l.stream().mapToInt(Integer::intValue).toArray();
            }
            Node[] orig = make(adj);
            int s = rnd.nextInt(n);
            Map<Node, Node> clones = new HashMap<>();
            Node got = cloneGraph(orig[s], clones);
            if (!shape(got).equals(shape(orig[s]))) throw new AssertionError("shape " + t);
            if (clones.size() != shape(orig[s]).size()) throw new AssertionError("one clone per node " + t);
            for (Map.Entry<Node, Node> e : clones.entrySet()) {
                if (e.getKey() == e.getValue()) throw new AssertionError("clone is an original " + t);
            }
        }
    }
}
```
