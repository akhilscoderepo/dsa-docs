<!-- solutions-for: 01-graph-representation -->
### Solutions For Graph Representation

#### Solution: [Build] Undirected Adjacency Lists (Author exercise)
<!-- id: gt-undirected-adjacency -->

**Approach.**
The method first creates `n` separate empty lists, so every vertex has an answer even when no edge mentions it. It then reads each edge once and appends each endpoint to the list of the other endpoint. Processing edges in input order fixes the order inside every list.

The invariant is that after `k` edges, `adj[v]` holds exactly the neighbors of `v` that the first `k` edges name. The list creation needs one new `ArrayList` per vertex, because a single shared list would give every vertex the same neighbors.

**Complexity.**
- **Time** is O(n + m), because the method creates `n` lists and then performs two appends for each of the `m` edges.
- **Space** is O(n + m), because the lists hold `n` headers and `2 * m` entries.

```java run
import java.util.*;

public final class UndirectedAdjacency {
    /**
     * Builds the adjacency list of an undirected graph.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: after k edges, adj[v] holds exactly the neighbors of v named by the first k edges.
     */
    static List<List<Integer>> build(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();                 // outer list, one slot per vertex
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());      // n separate lists, O(n) work
        for (int[] e : edges) {                                      // one pass over the m edges
            adj.get(e[0]).add(e[1]);                                 // b becomes a neighbor of a
            adj.get(e[1]).add(e[0]);                                 // a becomes a neighbor of b
        }
        return adj;                                                  // lists hold 2 * m entries in total
    }

    /** Oracle: for each vertex, scan every edge and collect the other endpoint. */
    static List<List<Integer>> brute(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            List<Integer> found = new ArrayList<>();
            for (int[] e : edges) {
                if (e[0] == v) found.add(e[1]);
                else if (e[1] == v) found.add(e[0]);
            }
            out.add(found);
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!build(4, new int[][] {{0, 1}, {0, 2}, {2, 3}}).toString().equals("[[1, 2], [0], [0, 3], [2]]")) throw new AssertionError("ex1");
        if (!build(3, new int[][] {{1, 2}, {0, 1}}).toString().equals("[[1], [2, 0], [1]]")) throw new AssertionError("ex2");
        // An isolated vertex keeps an empty list, and an empty edge array gives n empty lists.
        if (!build(3, new int[0][]).toString().equals("[[], [], []]")) throw new AssertionError("no edges");
        // The prose claim: nCopies repeats one reference, so a new list per vertex is required.
        List<List<Integer>> shared = new ArrayList<>(Collections.nCopies(2, new ArrayList<Integer>()));
        shared.get(0).add(7);
        if (shared.get(0) != shared.get(1) || shared.get(1).size() != 1) throw new AssertionError("nCopies shares one list");
        List<List<Integer>> own = build(2, new int[][] {{0, 1}});
        if (own.get(0) == own.get(1)) throw new AssertionError("build must create separate lists");
        // Random simple graphs must match the scan oracle, and entries must total 2 * m.
        Random rnd = new Random(2101);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(7);
            List<int[]> list = new ArrayList<>();
            Set<Integer> seen = new HashSet<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
                if (rnd.nextInt(3) == 0 && seen.add(a * 10 + b)) list.add(rnd.nextBoolean() ? new int[] {a, b} : new int[] {b, a});
            }
            Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            List<List<Integer>> got = build(n, edges);
            if (!got.equals(brute(n, edges))) throw new AssertionError("random " + t);
            int total = 0;
            for (List<Integer> l : got) total += l.size();
            if (total != 2 * edges.length) throw new AssertionError("entry count " + t);
        }
    }
}
```

#### Solution: [Vary] Directed Adjacency Lists (Author exercise)
<!-- id: gt-directed-adjacency -->

**Approach.**
The method creates all `n` lists first, which preserves isolated vertices. It then reads each edge once and appends the target to the list of the source only. The second append of the undirected build disappears, because a directed edge says nothing about the reverse direction.

The invariant is that after `k` edges, `adj[v]` holds exactly the targets of the edges that start at `v` among the first `k`.

**Complexity.**
- **Time** is O(n + m), because the method makes `n` lists and one append per edge.
- **Space** is O(n + m), because the lists hold `n` headers and `m` entries.

```java run
import java.util.*;

public final class DirectedAdjacency {
    /**
     * Builds the adjacency list of a directed graph.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: after k edges, adj[v] holds the targets of the first k edges that start at v.
     */
    static List<List<Integer>> build(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();                 // outer list, one slot per vertex
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());      // every vertex gets a list, even if isolated
        for (int[] e : edges) adj.get(e[0]).add(e[1]);               // only the source records the target
        return adj;                                                  // lists hold m entries in total
    }

    /** Oracle: for each vertex, scan every edge that starts there. */
    static List<List<Integer>> brute(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            List<Integer> found = new ArrayList<>();
            for (int[] e : edges) if (e[0] == v) found.add(e[1]);
            out.add(found);
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!build(4, new int[][] {{2, 0}, {0, 1}, {2, 1}}).toString().equals("[[1], [], [0, 1], []]")) throw new AssertionError("ex1");
        if (!build(2, new int[][] {{1, 0}}).toString().equals("[[], [0]]")) throw new AssertionError("ex2");
        // The directed build records one direction, so vertex 0 gets no neighbor from the edge [1,0].
        if (!build(2, new int[][] {{1, 0}}).get(0).isEmpty()) throw new AssertionError("no reverse entry");
        // Random edge sets without repeats or self edges must match the oracle and hold m entries.
        Random rnd = new Random(2102);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(7);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) if (a != b && rnd.nextInt(4) == 0) list.add(new int[] {a, b});
            Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            List<List<Integer>> got = build(n, edges);
            if (!got.equals(brute(n, edges))) throw new AssertionError("random " + t);
            int total = 0;
            for (List<Integer> l : got) total += l.size();
            if (total != edges.length) throw new AssertionError("entry count " + t);
        }
    }
}
```

#### Solution: [Boundary] Parallel And Self Edges (Author exercise)
<!-- id: gt-parallel-self-edges -->

**Approach.**
The contract permits repeated and self edges, so the build must remove them before reporting neighbors. The method keeps one `TreeSet` per vertex. A `TreeSet` ignores a value it already holds and iterates in ascending order, so repeats vanish and the output order is fixed without a later sort.

For each edge, the method skips a self edge, which would make a vertex its own neighbor. Otherwise it inserts each endpoint into the set of the other. The invariant is that each set holds the distinct neighbors, other than itself, from the edges read so far.

**Complexity.**
- **Time** is O(n + m log m), because each of the up to `2 * m` insertions costs O(log m) in a balanced tree.
- **Space** is O(n + m), because the sets hold at most `2 * m` entries.

```java run
import java.util.*;

public final class ParallelAndSelfEdges {
    /**
     * Returns sorted distinct neighbor lists, ignoring repeated and self edges.
     * Time: O(n + m log m). Space: O(n + m).
     * Invariant: sets[v] holds the distinct neighbors of v, other than v, from the edges read so far.
     */
    static List<List<Integer>> build(int n, int[][] edges) {
        List<TreeSet<Integer>> sets = new ArrayList<>();             // one ordered set per vertex
        for (int v = 0; v < n; v++) sets.add(new TreeSet<>());       // n separate sets, O(n) work
        for (int[] e : edges) {                                      // one pass over the m edges
            if (e[0] == e[1]) continue;                              // a self edge adds no neighbor
            sets.get(e[0]).add(e[1]);                                // the set drops a value it already holds
            sets.get(e[1]).add(e[0]);                                // the edge works in both directions
        }
        List<List<Integer>> adj = new ArrayList<>();                 // final answer in list form
        for (TreeSet<Integer> s : sets) adj.add(new ArrayList<>(s)); // a TreeSet iterates in ascending order
        return adj;
    }

    /** Oracle: a boolean matrix marks each pair once, then each row is read in order. */
    static List<List<Integer>> brute(int n, int[][] edges) {
        boolean[][] m = new boolean[n][n];
        for (int[] e : edges) if (e[0] != e[1]) { m[e[0]][e[1]] = true; m[e[1]][e[0]] = true; }
        List<List<Integer>> out = new ArrayList<>();
        for (int a = 0; a < n; a++) {
            List<Integer> row = new ArrayList<>();
            for (int b = 0; b < n; b++) if (m[a][b]) row.add(b);
            out.add(row);
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!build(3, new int[][] {{0, 1}, {1, 0}, {1, 1}, {1, 2}}).toString().equals("[[1], [0, 2], [1]]")) throw new AssertionError("ex1");
        if (!build(2, new int[][] {{0, 0}, {1, 1}}).toString().equals("[[], []]")) throw new AssertionError("ex2");
        // The prose claim about TreeSet: repeats are ignored and iteration is ascending.
        TreeSet<Integer> t = new TreeSet<>(List.of(5, 2));
        if (t.add(2) || !t.toString().equals("[2, 5]")) throw new AssertionError("TreeSet ignores repeats and sorts");
        // Random multigraphs with repeats and self edges must match the matrix oracle.
        Random rnd = new Random(2103);
        for (int r = 0; r < 400; r++) {
            int n = 1 + rnd.nextInt(6);
            int[][] edges = new int[rnd.nextInt(12)][];
            for (int k = 0; k < edges.length; k++) edges[k] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!build(n, edges).equals(brute(n, edges))) throw new AssertionError("random " + r);
        }
    }
}
```

#### Solution: [Recognize] Find Center of Star Graph (LeetCode 1791)
<!-- id: gt-star-center -->

**Approach.**
The graph contract makes a build unnecessary. The center shares an edge with every other vertex, so it appears in every edge. Any other vertex appears in exactly one edge. Two different edges therefore share exactly one endpoint, and that endpoint is the center.

The method reads only the first two edges. If the first endpoint of the first edge occurs in the second edge, that endpoint is the center. Otherwise the second endpoint of the first edge is the center. The invariant is that the center is the only vertex common to both rows.

**Complexity.**
- **Time** is O(1), because the method compares at most four numbers from two rows.
- **Space** is O(1), because the method stores no extra structure.

```java run
import java.util.*;

public final class StarCenter {
    /**
     * Returns the center of a valid star graph.
     * Time: O(1). Space: O(1).
     * Invariant: the center is the only vertex that appears in both of the first two edges.
     */
    static int center(int[][] edges) {
        int[] a = edges[0], b = edges[1];                            // two edges are enough, because n >= 3
        if (a[0] == b[0] || a[0] == b[1]) return a[0];               // the first endpoint is shared, so it is the center
        return a[1];                                                 // otherwise the second endpoint is shared
    }

    /** Oracle: count how often each vertex appears and return the vertex that appears n - 1 times. */
    static int brute(int n, int[][] edges) {
        int[] count = new int[n];
        for (int[] e : edges) { count[e[0]]++; count[e[1]]++; }
        for (int v = 0; v < n; v++) if (count[v] == n - 1) return v;
        throw new AssertionError("no center");
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (center(new int[][] {{0, 1}, {2, 0}, {0, 3}}) != 0) throw new AssertionError("ex1");
        if (center(new int[][] {{3, 1}, {3, 0}, {2, 3}, {3, 4}}) != 3) throw new AssertionError("ex2");
        // Random stars with shuffled labels, endpoint order and edge order must match the count oracle.
        Random rnd = new Random(2104);
        for (int t = 0; t < 400; t++) {
            int n = 3 + rnd.nextInt(8);
            int c = rnd.nextInt(n);
            List<int[]> list = new ArrayList<>();
            for (int v = 0; v < n; v++) if (v != c) list.add(rnd.nextBoolean() ? new int[] {c, v} : new int[] {v, c});
            Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            if (center(edges) != c || center(edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```
