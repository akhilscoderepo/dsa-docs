<!-- solutions-for: 02-graph-cloning -->
### Graph Cloning

#### Solution: [Build] Clone One Edge (Author exercise)
<!-- id: gt-clone-one-edge -->

**Approach.** Build real node objects from the edge, then make both copies up front and only afterwards attach each copy to the other, so neither end lacks a target. The answer lists the `val` of each copy's neighbors. The oracle never touches nodes: it reads the answer straight off the edge array. The assertions run every legal input shape, check that no copy appears among the originals by identity, and confirm that the copied neighbors are copies and not the original objects.

**Complexity.** Constant work, since there are at most two nodes and one thread; the input is read in time linear in its length.

```java run
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;

public final class CloneOneEdge {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static Node[] build(int n, int[][] edges) {
        Node[] nodes = new Node[n];
        for (int v = 0; v < n; v++) nodes[v] = new Node(v);
        for (int[] e : edges) {
            nodes[e[0]].neighbors.add(nodes[e[1]]);
            nodes[e[1]].neighbors.add(nodes[e[0]]);
        }
        return nodes;
    }

    static Node copy(Node top) {
        Node a = new Node(top.val);
        if (top.neighbors.isEmpty()) return a;
        Node other = top.neighbors.get(0);
        Node b = new Node(other.val);
        a.neighbors.add(b);
        b.neighbors.add(a);
        return a;
    }

    static List<List<Integer>> solve(int n, int[][] edges) {
        Node top = copy(build(n, edges)[0]);
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        Map<Node, Boolean> seen = new IdentityHashMap<>();
        List<Node> queue = new ArrayList<>();
        queue.add(top);
        seen.put(top, true);
        for (int i = 0; i < queue.size(); i++) {
            Node cur = queue.get(i);
            for (Node nb : cur.neighbors) {
                out.get(cur.val).add(nb.val);
                if (seen.put(nb, true) == null) queue.add(nb);
            }
        }
        return out;
    }

    static List<List<Integer>> oracle(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        for (int[] e : edges) {
            out.get(e[0]).add(e[1]);
            out.get(e[1]).add(e[0]);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(2, new int[][] {{0, 1}}).toString().equals("[[1], [0]]")) throw new AssertionError("example 1");
        if (!solve(1, new int[0][]).toString().equals("[[]]")) throw new AssertionError("example 2");
        int[][][] shapes = {{}, {{0, 1}}, {{1, 0}}};
        for (int[][] edges : shapes) {
            int n = edges.length == 0 ? 1 : 2;
            if (!solve(n, edges).equals(oracle(n, edges))) throw new AssertionError("shape " + edges.length);
            Node[] original = build(n, edges);
            Node top = copy(original[0]);
            Map<Node, Boolean> originals = new IdentityHashMap<>();
            for (Node o : original) originals.put(o, true);
            if (originals.containsKey(top)) throw new AssertionError("copy is an original");
            for (Node nb : top.neighbors) {
                if (originals.containsKey(nb)) throw new AssertionError("copied thread leads to an original");
                if (nb.neighbors.size() != 1 || nb.neighbors.get(0) != top)
                    throw new AssertionError("far copy must point back at the near copy");
            }
            if (top.neighbors.size() != edges.length) throw new AssertionError("thread count");
        }
    }
}
```

#### Solution: [Vary] Clone A Cycle (Author exercise)
<!-- id: gt-clone-a-cycle -->

**Approach.** The recursive step stores a blank copy in the identity map before it follows any pointer, so a pointer that returns to a half finished card receives that card's copy. Pointers are read in input order, and cards that the walk never meets simply keep empty lists in the answer. The oracle finds the reachable set with a plain reachability sweep over the pair list and reads each reachable card's targets off the pairs in order. The assertions compare the two on random directed boards with cycles and self pointers, require that the number of copies equals the number of reachable cards, and verify by identity that the copy shares no node with the original.

**Complexity.** Every reachable card is made once and every pointer is wired once, giving O(n + E) time with O(n) extra space for the map and the recursion; here n is at most 100, so the stack depth is safe.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class CloneACycle {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static Node[] build(int n, int[][] edges) {
        Node[] nodes = new Node[n];
        for (int v = 0; v < n; v++) nodes[v] = new Node(v);
        for (int[] e : edges) nodes[e[0]].neighbors.add(nodes[e[1]]);
        return nodes;
    }

    static Node visit(Node cur, Map<Node, Node> twin) {
        Node found = twin.get(cur);
        if (found != null) return found;
        Node t = new Node(cur.val);
        twin.put(cur, t);
        for (Node nb : cur.neighbors) t.neighbors.add(visit(nb, twin));
        return t;
    }

    static List<List<Integer>> report(Node top, int n) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        Set<Node> done = java.util.Collections.newSetFromMap(new IdentityHashMap<>());
        java.util.ArrayDeque<Node> stack = new java.util.ArrayDeque<>();
        stack.push(top);
        done.add(top);
        while (!stack.isEmpty()) {
            Node cur = stack.pop();
            for (Node nb : cur.neighbors) {
                out.get(cur.val).add(nb.val);
                if (done.add(nb)) stack.push(nb);
            }
        }
        return out;
    }

    static List<List<Integer>> solve(int n, int[][] edges) {
        Node top = visit(build(n, edges)[0], new IdentityHashMap<>());
        return report(top, n);
    }

    static List<List<Integer>> oracle(int n, int[][] edges) {
        boolean[] reach = new boolean[n];
        reach[0] = true;
        boolean grew = true;
        while (grew) {
            grew = false;
            for (int[] e : edges) if (reach[e[0]] && !reach[e[1]]) { reach[e[1]] = true; grew = true; }
        }
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            List<Integer> to = new ArrayList<>();
            if (reach[v]) for (int[] e : edges) if (e[0] == v) to.add(e[1]);
            out.add(to);
        }
        return out;
    }

    static int countDistinct(Node top) {
        Set<Node> all = java.util.Collections.newSetFromMap(new IdentityHashMap<>());
        List<Node> work = new ArrayList<>();
        work.add(top);
        all.add(top);
        for (int i = 0; i < work.size(); i++)
            for (Node nb : work.get(i).neighbors) if (all.add(nb)) work.add(nb);
        return all.size();
    }

    public static void main(String[] args) {
        if (!solve(4, new int[][] {{0, 1}, {1, 2}, {2, 0}, {3, 0}}).toString().equals("[[1], [2], [0], []]"))
            throw new AssertionError("example 1");
        if (!solve(5, new int[][] {{0, 2}, {2, 4}, {4, 2}, {1, 0}}).toString().equals("[[2], [], [4], [], [2]]"))
            throw new AssertionError("example 2");
        Random rnd = new Random(21202);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            Set<Integer> seen = new HashSet<>();
            List<int[]> list = new ArrayList<>();
            for (int k = rnd.nextInt(18); k > 0; k--) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (seen.add(u * 100 + v)) list.add(new int[] {u, v});
            }
            int[][] edges = list.toArray(new int[0][]);
            if (!solve(n, edges).equals(oracle(n, edges))) throw new AssertionError("random " + t);
            Node[] original = build(n, edges);
            Map<Node, Node> twin = new IdentityHashMap<>();
            Node top = visit(original[0], twin);
            int reachable = countDistinct(original[0]);
            if (twin.size() != reachable || countDistinct(top) != reachable)
                throw new AssertionError("copy count " + t);
            for (Map.Entry<Node, Node> en : twin.entrySet()) {
                if (en.getKey() == en.getValue()) throw new AssertionError("shared node " + t);
                if (twin.containsKey(en.getValue())) throw new AssertionError("copy used as original " + t);
                if (en.getKey().neighbors.size() != en.getValue().neighbors.size())
                    throw new AssertionError("thread count " + t);
                for (int i = 0; i < en.getKey().neighbors.size(); i++)
                    if (twin.get(en.getKey().neighbors.get(i)) != en.getValue().neighbors.get(i))
                        throw new AssertionError("wiring " + t);
            }
        }
    }
}
```

#### Solution: [Boundary] Null And Self-Loop (Author exercise)
<!-- id: gt-null-and-self-loop -->

**Approach.** An empty array is answered with `null` before any node is built or touched. Otherwise the cards are built from the adjacency array and copied breadth first, with the copy of a card put into the map when the card is first discovered, so a self pointer finds its own copy and a card without pointers yields an empty, non-null list. The oracle is just the input array, because a faithful copy must report exactly the neighbor lists it was built from. Assertions cover random reachable boards with many self pointers, the identity of every copy against its original, and the lesson's remark that a `HashMap` with a value-based `equals` merges distinct cards, whereas an `IdentityHashMap` keeps them apart.

**Complexity.** Linear in the number of cards plus pointers for time, and linear in the number of cards for the map and the queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Random;

public final class NullAndSelfLoop {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static final class ValueNode {
        final int val;
        ValueNode(int val) { this.val = val; }
        @Override public boolean equals(Object o) { return o instanceof ValueNode && ((ValueNode) o).val == val; }
        @Override public int hashCode() { return Objects.hash(val); }
    }

    static Node[] build(int[][] adj) {
        Node[] nodes = new Node[adj.length];
        for (int v = 0; v < adj.length; v++) nodes[v] = new Node(v);
        for (int v = 0; v < adj.length; v++) for (int w : adj[v]) nodes[v].neighbors.add(nodes[w]);
        return nodes;
    }

    static Node clone(Node start, Map<Node, Node> twin) {
        if (start == null) return null;
        twin.put(start, new Node(start.val));
        ArrayDeque<Node> line = new ArrayDeque<>();
        line.add(start);
        while (!line.isEmpty()) {
            Node cur = line.poll();
            Node mine = twin.get(cur);
            for (Node nb : cur.neighbors) {
                Node theirs = twin.get(nb);
                if (theirs == null) {
                    theirs = new Node(nb.val);
                    twin.put(nb, theirs);
                    line.add(nb);
                }
                mine.neighbors.add(theirs);
            }
        }
        return twin.get(start);
    }

    static List<List<Integer>> solve(int[][] adj) {
        if (adj.length == 0) return null;
        Node top = clone(build(adj)[0], new IdentityHashMap<>());
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < adj.length; v++) out.add(new ArrayList<>());
        Map<Node, Boolean> seen = new IdentityHashMap<>();
        List<Node> work = new ArrayList<>();
        work.add(top);
        seen.put(top, true);
        for (int i = 0; i < work.size(); i++) {
            Node cur = work.get(i);
            for (Node nb : cur.neighbors) {
                out.get(cur.val).add(nb.val);
                if (seen.put(nb, true) == null) work.add(nb);
            }
        }
        return out;
    }

    static List<List<Integer>> oracle(int[][] adj) {
        if (adj.length == 0) return null;
        List<List<Integer>> out = new ArrayList<>();
        for (int[] row : adj) {
            List<Integer> r = new ArrayList<>();
            for (int w : row) r.add(w);
            out.add(r);
        }
        return out;
    }

    public static void main(String[] args) {
        if (solve(new int[0][]) != null) throw new AssertionError("example 1");
        if (!solve(new int[][] {{1, 0}, {1}}).toString().equals("[[1, 0], [1]]")) throw new AssertionError("example 2");
        Random rnd = new Random(21203);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            List<List<Integer>> rows = new ArrayList<>();
            for (int v = 0; v < n; v++) rows.add(new ArrayList<>());
            for (int v = 1; v < n; v++) rows.get(rnd.nextInt(v)).add(v);
            for (int k = rnd.nextInt(10); k > 0; k--) {
                int u = rnd.nextInt(n), w = rnd.nextInt(n);
                if (!rows.get(u).contains(w)) rows.get(u).add(w);
            }
            int[][] adj = new int[n][];
            for (int v = 0; v < n; v++) {
                Collections.shuffle(rows.get(v), rnd);
                adj[v] = rows.get(v).stream().mapToInt(Integer::intValue).toArray();
            }
            if (!solve(adj).equals(oracle(adj))) throw new AssertionError("random " + t);
            Node[] original = build(adj);
            Map<Node, Node> twin = new IdentityHashMap<>();
            Node top = clone(original[0], twin);
            if (twin.size() != n) throw new AssertionError("every card is reachable " + t);
            for (int v = 0; v < n; v++) {
                Node c = twin.get(original[v]);
                if (c == original[v] || c.neighbors == null) throw new AssertionError("identity " + t);
                for (int i = 0; i < adj[v].length; i++) {
                    if (c.neighbors.get(i) != twin.get(original[adj[v][i]])) throw new AssertionError("wiring " + t);
                    if (c.neighbors.get(i) == original[adj[v][i]]) throw new AssertionError("leak " + t);
                }
                for (int w : adj[v]) if (w == v && c.neighbors.get(c.neighbors.indexOf(c)) != c)
                    throw new AssertionError("self loop " + t);
            }
            if (top != twin.get(original[0])) throw new AssertionError("top " + t);
        }
        Map<ValueNode, String> byValue = new HashMap<>();
        Map<ValueNode, String> byIdentity = new IdentityHashMap<>();
        ValueNode first = new ValueNode(7), second = new ValueNode(7);
        byValue.put(first, "x");
        byValue.put(second, "y");
        byIdentity.put(first, "x");
        byIdentity.put(second, "y");
        if (byValue.size() != 1 || byIdentity.size() != 2) throw new AssertionError("equals-based keys merge cards");
    }
}
```

#### Solution: [Recognize] Clone Graph (LeetCode 133)
<!-- id: gt-clone-graph -->

**Approach.** A queue visits each reachable node once, and the first time a node is discovered its copy is created and entered in an identity map. Every neighbor of a copy is then taken from that map, so the copy refers only to copies, in the same order as the original lists. The oracle is a different method: it clones with the lesson's naive parallel lists and linear identity search, and compares the results through the neighbor numbers. Assertions use random connected simple graphs, verify a bijection by identity between originals and copies, and check the false friend and the depth claim: a label-keyed map loses nodes that share a label, and the queue version copies a chain of 200000 nodes that would overflow a recursive version's default stack.

**Complexity.** Time grows as O(n + E), since each node and each edge end is handled once, and the map and the queue need O(n) space; the naive oracle costs O(n * E) and is used only on small graphs.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class CloneGraph {
    static final class Node {
        final int val;
        final List<Node> neighbors = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    static Node[] build(int n, int[][] edges) {
        Node[] nodes = new Node[n];
        for (int v = 0; v < n; v++) nodes[v] = new Node(v);
        for (int[] e : edges) {
            nodes[e[0]].neighbors.add(nodes[e[1]]);
            nodes[e[1]].neighbors.add(nodes[e[0]]);
        }
        return nodes;
    }

    static Node cloneGraph(Node start, Map<Node, Node> twin) {
        if (start == null) return null;
        twin.put(start, new Node(start.val));
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(start);
        while (!queue.isEmpty()) {
            Node cur = queue.remove();
            for (Node nb : cur.neighbors) {
                if (!twin.containsKey(nb)) {
                    twin.put(nb, new Node(nb.val));
                    queue.add(nb);
                }
                twin.get(cur).neighbors.add(twin.get(nb));
            }
        }
        return twin.get(start);
    }

    static Node naive(Node top) {
        List<Node> originals = new ArrayList<>();
        List<Node> copies = new ArrayList<>();
        originals.add(top);
        copies.add(new Node(top.val));
        for (int i = 0; i < originals.size(); i++) {
            for (Node other : originals.get(i).neighbors) {
                int at = -1;
                for (int j = 0; j < originals.size(); j++) if (originals.get(j) == other) { at = j; break; }
                if (at < 0) {
                    originals.add(other);
                    copies.add(new Node(other.val));
                    at = originals.size() - 1;
                }
                copies.get(i).neighbors.add(copies.get(at));
            }
        }
        return copies.get(0);
    }

    static List<List<Integer>> shape(Node top, int n) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        Map<Node, Boolean> seen = new IdentityHashMap<>();
        List<Node> work = new ArrayList<>();
        work.add(top);
        seen.put(top, true);
        for (int i = 0; i < work.size(); i++) {
            Node cur = work.get(i);
            for (Node nb : cur.neighbors) {
                out.get(cur.val).add(nb.val);
                if (seen.put(nb, true) == null) work.add(nb);
            }
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1}, {1, 2}, {2, 3}, {3, 0}};
        if (!shape(cloneGraph(build(4, e1)[0], new IdentityHashMap<>()), 4).toString()
                .equals("[[1, 3], [0, 2], [1, 3], [2, 0]]")) throw new AssertionError("example 1");
        int[][] e2 = {{2, 0}, {0, 1}, {1, 2}};
        if (!shape(cloneGraph(build(3, e2)[0], new IdentityHashMap<>()), 3).toString()
                .equals("[[2, 1], [0, 2], [0, 1]]")) throw new AssertionError("example 2");
        Random rnd = new Random(21204);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            Set<Integer> seen = new HashSet<>();
            List<int[]> list = new ArrayList<>();
            for (int v = 1; v < n; v++) {
                int u = rnd.nextInt(v);
                seen.add(u * 100 + v);
                list.add(rnd.nextBoolean() ? new int[] {u, v} : new int[] {v, u});
            }
            for (int k = rnd.nextInt(8); k > 0; k--) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (u != v && seen.add(Math.min(u, v) * 100 + Math.max(u, v))) list.add(new int[] {u, v});
            }
            java.util.Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            Node[] original = build(n, edges);
            Map<Node, Node> twin = new IdentityHashMap<>();
            Node top = cloneGraph(original[0], twin);
            if (!shape(top, n).equals(shape(naive(build(n, edges)[0]), n))) throw new AssertionError("random " + t);
            if (twin.size() != n) throw new AssertionError("copy count " + t);
            Set<Node> copies = java.util.Collections.newSetFromMap(new IdentityHashMap<>());
            for (int v = 0; v < n; v++) {
                Node o = original[v], c = twin.get(o);
                if (c == o || !copies.add(c)) throw new AssertionError("identity " + t);
                if (c.val != o.val || c.neighbors.size() != o.neighbors.size()) throw new AssertionError("structure " + t);
                for (int i = 0; i < o.neighbors.size(); i++)
                    if (c.neighbors.get(i) != twin.get(o.neighbors.get(i))) throw new AssertionError("wiring " + t);
            }
            for (Node c : copies) for (Node nb : c.neighbors) if (!copies.contains(nb)) throw new AssertionError("leak " + t);
        }
        Map<Integer, Node> byLabel = new HashMap<>();
        Node a = new Node(7), b = new Node(7), c = new Node(5);
        byLabel.put(a.val, a);
        byLabel.put(b.val, b);
        byLabel.put(c.val, c);
        if (byLabel.size() != 2) throw new AssertionError("label keys lose a card");
        int len = 200000;
        Node[] chain = new Node[len];
        for (int v = 0; v < len; v++) chain[v] = new Node(v);
        for (int v = 0; v + 1 < len; v++) {
            chain[v].neighbors.add(chain[v + 1]);
            chain[v + 1].neighbors.add(chain[v]);
        }
        Map<Node, Node> big = new IdentityHashMap<>();
        cloneGraph(chain[0], big);
        if (big.size() != len) throw new AssertionError("long chain");
    }
}
```
