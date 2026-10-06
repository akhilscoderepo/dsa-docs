<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For Undirected Parent State

#### Solution: [Build] DFS With Parent (Author exercise)
<!-- id: dg-dfs-with-parent -->

**Approach.**
The method builds an adjacency list with both directions per edge and starts one depth-first search from every unvisited vertex. Each call receives the vertex that entered it. While a call scans its neighbors, it skips the entry vertex, reports a cycle for any other visited neighbor, and recurses into unvisited neighbors.

The invariant is that the only visited neighbor a call may skip is the tree edge that entered it. In a graph without repeated pairs, one vertex id identifies that edge. Every cycle contains an edge that is not a tree edge. The search reads that edge from an endpoint where it is neither the entry edge nor a way to a new vertex. The rule therefore fires on every cyclic graph and on no forest.

**Complexity.**
- **Time** is O(V + E), because each vertex starts one call and each adjacency entry is read once.
- **Space** is O(V + E) for the adjacency list, and the recursion adds up to V frames.

```java run
import java.util.*;

public final class DfsWithParent {
    /**
     * Returns true when the undirected simple graph contains a cycle.
     * Time: O(V + E). Space: O(V + E) with recursion depth up to V.
     * Invariant: the only visited neighbor skipped is the entry vertex.
     */
    static boolean hasCycle(int n, int[][] edges) {
        // Each undirected edge is stored once at each endpoint.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        // One search per unvisited vertex covers every separate piece.
        for (int start = 0; start < n; start++) {
            if (!visited[start] && dfs(adj, visited, start, -1)) return true;
        }
        return false;
    }

    private static boolean dfs(List<List<Integer>> adj, boolean[] visited, int v, int parent) {
        // Marking on entry means a later read of v sees it as visited.
        visited[v] = true;
        // Each adjacency entry is read once over the whole run, which gives the O(E) term.
        for (int next : adj.get(v)) {
            // The entry vertex is the other end of the tree edge, so it proves nothing.
            if (next == parent) continue;
            // Any other visited neighbor closes a cycle through the tree path.
            if (visited[next]) return true;
            // An unvisited neighbor is discovered here, and v becomes its parent.
            if (dfs(adj, visited, next, v)) return true;
        }
        return false;
    }

    /** Brute force: a label array, where an edge inside one label closes a cycle. */
    static boolean oracle(int n, int[][] edges) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        for (int[] e : edges) {
            if (label[e[0]] == label[e[1]]) return true;
            int from = label[e[1]], to = label[e[0]];
            for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!hasCycle(7, new int[][] {{0, 1}, {1, 2}, {3, 4}, {4, 5}, {5, 3}, {2, 6}})) throw new AssertionError("ex1");
        if (hasCycle(5, new int[][] {{0, 1}, {1, 2}, {2, 3}, {1, 4}})) throw new AssertionError("ex2");
        // Java fact: a path of 1000 vertices reaches depth 1000 and still fits the default stack.
        int[][] path = new int[999][];
        for (int i = 0; i < 999; i++) path[i] = new int[] {i, i + 1};
        if (hasCycle(1000, path)) throw new AssertionError("path");
        // Random simple graphs, with random edge order and orientation, must match the oracle.
        Random rnd = new Random(2303);
        int cyclic = 0;
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(5) == 0) es.add(rnd.nextBoolean() ? new int[] {a, b} : new int[] {b, a});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            boolean expected = oracle(n, arr);
            if (expected) cyclic++;
            if (hasCycle(n, arr) != expected) throw new AssertionError("random " + t);
        }
        // Both outcomes must occur, or the random check proves nothing.
        if (cyclic == 0 || cyclic == 1000) throw new AssertionError("coverage");
    }
}
```

#### Solution: [Vary] Detect A Triangle (Author exercise)
<!-- id: dg-detect-triangle -->

**Approach.**
The method runs the depth-first search with a parent argument. Each time a call reads a visited neighbor `w` that is not its parent, the edge between `v` and `w` is a back edge. The method then marks the neighbors of `v` in a boolean array and scans the neighbors of `w`. A marked vertex is adjacent to both endpoints, so it completes a triangle.

The invariant is that every cycle, and therefore every triangle, contains at least one back edge, because tree edges alone form no cycle. The search reads each back edge from at least one endpoint, so it tests the one edge of each triangle that is not a tree edge. The other two edges of that triangle are exactly a common neighbor. A graph without a back edge has no cycle and so no triangle.

**Complexity.**
- **Time** is O(V + E + B * D), where B counts back edges and D is the largest degree. Each back edge costs one marking pass and one scan.
- **Space** is O(V + E) for the adjacency list and the mark array.

```java run
import java.util.*;

public final class DetectTriangle {
    /**
     * Returns true when the simple undirected graph contains a triangle.
     * Time: O(V + E + B * D). Space: O(V + E).
     * Invariant: every triangle contains a back edge whose endpoints share a neighbor.
     */
    static boolean hasTriangle(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        boolean[] mark = new boolean[n];
        // One search per unvisited vertex covers every separate piece.
        for (int start = 0; start < n; start++) {
            if (!visited[start] && dfs(adj, visited, mark, start, -1)) return true;
        }
        return false;
    }

    private static boolean dfs(List<List<Integer>> adj, boolean[] visited, boolean[] mark, int v, int parent) {
        visited[v] = true;
        for (int next : adj.get(v)) {
            // The entry vertex is the tree edge, not a back edge.
            if (next == parent) continue;
            if (visited[next]) {
                // A back edge was found, so the endpoints need a common neighbor.
                if (shareNeighbor(adj, mark, v, next)) return true;
                continue;
            }
            // An unvisited neighbor is discovered through a tree edge.
            if (dfs(adj, visited, mark, next, v)) return true;
        }
        return false;
    }

    private static boolean shareNeighbor(List<List<Integer>> adj, boolean[] mark, int v, int w) {
        // Marking the neighbors of v costs deg(v).
        for (int x : adj.get(v)) mark[x] = true;
        boolean shared = false;
        // Scanning the neighbors of w costs deg(w); a marked one is adjacent to both.
        for (int y : adj.get(w)) if (mark[y]) { shared = true; break; }
        // The marks are cleared so the next back edge starts from an empty array.
        for (int x : adj.get(v)) mark[x] = false;
        return shared;
    }

    /** Brute force: test every vertex triple against an adjacency matrix. */
    static boolean oracle(int n, int[][] edges) {
        boolean[][] m = new boolean[n][n];
        for (int[] e : edges) m[e[0]][e[1]] = m[e[1]][e[0]] = true;
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) if (m[a][b] && m[b][c] && m[a][c]) return true;
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (hasTriangle(6, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 0}})) throw new AssertionError("ex1");
        if (!hasTriangle(5, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0}, {0, 2}})) throw new AssertionError("ex2");
        // A long cycle whose back edge skips many tree vertices still closes a triangle with a second back edge.
        if (!hasTriangle(6, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 0}, {5, 1}})) throw new AssertionError("far back edge");
        // Random simple graphs must match the triple-loop oracle.
        Random rnd = new Random(2313);
        int yes = 0;
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(4) == 0) es.add(rnd.nextBoolean() ? new int[] {a, b} : new int[] {b, a});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            boolean expected = oracle(n, arr);
            if (expected) yes++;
            if (hasTriangle(n, arr) != expected) throw new AssertionError("random " + t);
        }
        // Both outcomes must occur.
        if (yes == 0 || yes == 1500) throw new AssertionError("coverage");
    }
}
```

#### Solution: [Boundary] Single Edge And Parallel Edges (Author exercise)
<!-- id: dg-parallel-edges -->

**Approach.**
The method stores every adjacency entry as a pair of the neighbor and the index of the edge. A call receives the index of the edge that entered it, with -1 for a start vertex. The call skips only that index. Any other visited neighbor, including the parent vertex reached by a second edge, reports a cycle.

The invariant is that the single skipped adjacency entry is the tree edge that entered the call. A comparison by vertex id would skip both parallel edges and miss the cycle with two edges. A single edge has one entry at each end, so the index test skips it and reports nothing, and the answer for one cable stays false.

**Complexity.**
- **Time** is O(V + E), because each vertex starts one call and each adjacency entry is read once.
- **Space** is O(V + E) for the adjacency entries, and the recursion adds up to V frames.

```java run
import java.util.*;

public final class ParallelEdges {
    /**
     * Returns true when the undirected multigraph contains a cycle, including two parallel edges.
     * Time: O(V + E). Space: O(V + E) with recursion depth up to V.
     * Invariant: only the adjacency entry of the entry edge is skipped.
     */
    static boolean hasCycle(int n, int[][] edges) {
        // Each entry holds {neighbor, edge index}.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int i = 0; i < edges.length; i++) {
            adj.get(edges[i][0]).add(new int[] {edges[i][1], i});
            adj.get(edges[i][1]).add(new int[] {edges[i][0], i});
        }
        boolean[] visited = new boolean[n];
        for (int start = 0; start < n; start++) {
            if (!visited[start] && dfs(adj, visited, start, -1)) return true;
        }
        return false;
    }

    private static boolean dfs(List<List<int[]>> adj, boolean[] visited, int v, int parentEdge) {
        visited[v] = true;
        for (int[] entry : adj.get(v)) {
            // Only the entry edge itself is skipped, never a second edge to the same vertex.
            if (entry[1] == parentEdge) continue;
            // Any other visited neighbor closes a cycle, even when it is the parent vertex.
            if (visited[entry[0]]) return true;
            if (dfs(adj, visited, entry[0], entry[1])) return true;
        }
        return false;
    }

    /** Brute force: a multigraph has a cycle exactly when it has more edges than a forest allows. */
    static boolean oracle(int n, int[][] edges) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        // Merging labels edge by edge counts the pieces without any traversal.
        int pieces = n;
        for (int[] e : edges) {
            int a = label[e[0]], b = label[e[1]];
            if (a == b) continue;
            pieces--;
            for (int v = 0; v < n; v++) if (label[v] == b) label[v] = a;
        }
        return edges.length > n - pieces;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (hasCycle(2, new int[][] {{0, 1}})) throw new AssertionError("ex1");
        if (!hasCycle(3, new int[][] {{0, 1}, {1, 2}, {2, 1}})) throw new AssertionError("ex2");
        // Reversed repeats of one pair also form a cycle of two edges.
        if (!hasCycle(2, new int[][] {{0, 1}, {1, 0}})) throw new AssertionError("reversed pair");
        // Random multigraphs must match the edge-count oracle.
        Random rnd = new Random(2323);
        int yes = 0;
        for (int t = 0; t < 1500; t++) {
            int n = 2 + rnd.nextInt(6);
            int m = rnd.nextInt(7);
            int[][] arr = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n - 1);
                if (b >= a) b++;
                arr[i] = new int[] {a, b};
            }
            boolean expected = oracle(n, arr);
            if (expected) yes++;
            if (hasCycle(n, arr) != expected) throw new AssertionError("random " + t);
        }
        // Both outcomes must occur.
        if (yes == 0 || yes == 1500) throw new AssertionError("coverage");
    }
}
```

#### Solution: [Recognize] Graph Valid Tree (LeetCode 261)
<!-- id: dg-valid-tree -->

**Approach.**
The method runs one depth-first search with a parent argument from vertex 0 and counts the vertices it visits. It answers false as soon as a call reads a visited neighbor that is not its parent, because that is a back edge and so a cycle. After the search it answers true only if the count equals `n`.

The invariant is that the visited count equals the size of the piece that contains vertex 0. A graph is a tree exactly when that piece has no back edge and contains every vertex. The two checks are independent. A forest passes the cycle check and fails the count. A connected graph with an extra edge passes the count and fails the cycle check.

**Complexity.**
- **Time** is O(V + E), because the search visits each vertex of the piece once and reads each adjacency entry once.
- **Space** is O(V + E) for the adjacency list, and the recursion adds up to V frames.

```java run
import java.util.*;

public final class ValidTree {
    private static int visitedCount;

    /**
     * Returns true when the graph is connected and has no cycle.
     * Time: O(V + E). Space: O(V + E) with recursion depth up to V.
     * Invariant: visitedCount equals the size of the piece of vertex 0.
     */
    static boolean validTree(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        visitedCount = 0;
        // A back edge anywhere in the piece of vertex 0 rejects the graph.
        if (hasBackEdge(adj, visited, 0, -1)) return false;
        // Connected means the single search reached every vertex.
        return visitedCount == n;
    }

    private static boolean hasBackEdge(List<List<Integer>> adj, boolean[] visited, int v, int parent) {
        visited[v] = true;
        visitedCount++;
        for (int next : adj.get(v)) {
            if (next == parent) continue;
            if (visited[next]) return true;
            if (hasBackEdge(adj, visited, next, v)) return true;
        }
        return false;
    }

    /** Brute force: a tree has exactly n - 1 edges and one connected piece. */
    static boolean oracle(int n, int[][] edges) {
        if (edges.length != n - 1) return false;
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        for (int[] e : edges) {
            int a = label[e[0]], b = label[e[1]];
            for (int v = 0; v < n; v++) if (label[v] == b) label[v] = a;
        }
        for (int v = 0; v < n; v++) if (label[v] != label[0]) return false;
        return true;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!validTree(5, new int[][] {{0, 1}, {0, 2}, {0, 3}, {1, 4}})) throw new AssertionError("ex1");
        if (validTree(4, new int[][] {{0, 1}, {2, 3}})) throw new AssertionError("ex2");
        // A single vertex without edges is a tree.
        if (!validTree(1, new int[0][])) throw new AssertionError("single");
        // Random graphs near the tree boundary must match the edge-count oracle.
        Random rnd = new Random(2333);
        int yes = 0, no = 0;
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(7);
            List<int[]> es = new ArrayList<>();
            // Start from a random tree, then remove one edge, add one pair, or keep it.
            for (int v = 1; v < n; v++) es.add(new int[] {rnd.nextInt(v), v});
            int mode = rnd.nextInt(3);
            if (mode == 0 && !es.isEmpty()) es.remove(rnd.nextInt(es.size()));
            if (mode == 1 && n >= 3) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                boolean present = a == b;
                for (int[] e : es) if ((e[0] == a && e[1] == b) || (e[0] == b && e[1] == a)) present = true;
                if (!present) es.add(new int[] {a, b});
            }
            for (int[] e : es) if (rnd.nextBoolean()) { int x = e[0]; e[0] = e[1]; e[1] = x; }
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            boolean expected = oracle(n, arr);
            if (expected) yes++; else no++;
            if (validTree(n, arr) != expected) throw new AssertionError("random " + t);
        }
        // Both outcomes must occur.
        if (yes == 0 || no == 0) throw new AssertionError("coverage");
    }
}
```
