<!-- solutions-for: 03-undirected-parent-state -->
### Undirected Parent State

#### Solution: [Build] DFS With Parent (Author exercise)
<!-- id: ug-dfs-parent -->

**Approach.** Build one neighbor list per vertex in a loop, then start a walk from every vertex not yet seen. Each call takes the vertex it was entered from; a neighbor equal to that vertex is passed over, and any other neighbor that is already seen proves a cycle. The oracle never walks: it labels every vertex with the smallest vertex number in its piece by repeated propagation until nothing changes, counts the pieces c, and reports a cycle exactly when the edge count exceeds n - c. The assertions also pin three claims from the lesson: a walk that does not skip the parent reports a cycle on a single edge, `Collections.nCopies` hands out one shared list, and the input array is left unchanged.

**Complexity.** Each vertex is entered once and each edge is inspected from both ends, giving O(n + m) time, and the lists plus the recursion stack take O(n + m) memory.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class DfsWithParentSolution {
    static List<List<Integer>> build(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        return adj;
    }

    static boolean walk(List<List<Integer>> adj, boolean[] seen, int v, int parent) {
        seen[v] = true;
        for (int w : adj.get(v)) {
            if (w == parent) continue;
            if (seen[w] || walk(adj, seen, w, v)) return true;
        }
        return false;
    }

    static boolean solve(int n, int[][] edges) {
        List<List<Integer>> adj = build(n, edges);
        boolean[] seen = new boolean[n];
        for (int s = 0; s < n; s++) {
            if (!seen[s] && walk(adj, seen, s, -1)) return true;
        }
        return false;
    }

    static boolean walkNoParent(List<List<Integer>> adj, boolean[] seen, int v) {
        seen[v] = true;
        for (int w : adj.get(v)) {
            if (seen[w] || walkNoParent(adj, seen, w)) return true;
        }
        return false;
    }

    static boolean oracle(int n, int[][] edges) {
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                int m = Math.min(label[e[0]], label[e[1]]);
                if (label[e[0]] != m) { label[e[0]] = m; changed = true; }
                if (label[e[1]] != m) { label[e[1]] = m; changed = true; }
            }
        }
        int pieces = 0;
        for (int i = 0; i < n; i++) if (label[i] == i) pieces++;
        return edges.length > n - pieces;
    }

    public static void main(String[] args) {
        if (!solve(5, new int[][] {{0, 1}, {1, 2}, {2, 0}, {3, 4}})) throw new AssertionError("example 1");
        if (solve(6, new int[][] {{0, 1}, {1, 2}, {1, 3}, {4, 5}})) throw new AssertionError("example 2");
        if (solve(1, new int[][] {})) throw new AssertionError("single vertex");
        // false friend: without the parent, one lone edge looks like a cycle
        List<List<Integer>> one = build(2, new int[][] {{0, 1}});
        if (!walkNoParent(one, new boolean[2], 0)) throw new AssertionError("no-parent walk must misfire");
        if (solve(2, new int[][] {{0, 1}})) throw new AssertionError("parent walk on one edge");
        // Java hazard: nCopies repeats one list object
        List<List<Integer>> shared = new ArrayList<>(Collections.nCopies(3, new ArrayList<Integer>()));
        shared.get(0).add(7);
        if (shared.get(1).size() != 1 || shared.get(0) != shared.get(2)) throw new AssertionError("nCopies shares");
        Random rnd = new Random(23301);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(9);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++)
                for (int b = a + 1; b < n; b++)
                    if (rnd.nextInt(100) < 18) list.add(rnd.nextBoolean() ? new int[] {a, b} : new int[] {b, a});
            Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            int[][] copy = new int[edges.length][];
            for (int i = 0; i < edges.length; i++) copy[i] = edges[i].clone();
            boolean got = solve(n, edges);
            for (int i = 0; i < edges.length; i++)
                if (edges[i][0] != copy[i][0] || edges[i][1] != copy[i][1]) throw new AssertionError("mutated");
            if (got != oracle(n, edges)) throw new AssertionError("random n=" + n + " t=" + t);
        }
    }
}
```

#### Solution: [Vary] Detect A Triangle (Author exercise)
<!-- id: ug-triangle -->

**Approach.** Store each vertex's neighbors in a sorted set. For every vertex p in increasing order, take each larger neighbor v in increasing order, which is the step from the parent p to v, and look through v's larger neighbors w in increasing order for one that p also touches. The first hit is the smallest triple, because the three loops follow lexicographic order. The oracle tries all triples a < b < c against an adjacency matrix and keeps the first one that is complete. The assertions confirm that an `int[]` is not `equals` to another array with the same contents, so the check uses `Arrays.equals`, and that a four-cycle with no chord yields the empty array.

**Complexity.** For each of the m edges the inner scan covers at most the larger neighbors of one endpoint, so the worst case is O(m * d) for maximum degree d, which is at most 300 * 59 steps here, with O(n + m) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;
import java.util.TreeSet;

public final class DetectTriangleSolution {
    static int[] solve(int n, int[][] edges) {
        List<TreeSet<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new TreeSet<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        for (int p = 0; p < n; p++) {
            for (int v : adj.get(p).tailSet(p, false)) {
                for (int w : adj.get(v).tailSet(v, false)) {
                    if (adj.get(p).contains(w)) return new int[] {p, v, w};
                }
            }
        }
        return new int[0];
    }

    static int[] oracle(int n, int[][] edges) {
        boolean[][] g = new boolean[n][n];
        for (int[] e : edges) g[e[0]][e[1]] = g[e[1]][e[0]] = true;
        for (int a = 0; a < n; a++)
            for (int b = a + 1; b < n; b++)
                for (int c = b + 1; c < n; c++)
                    if (g[a][b] && g[b][c] && g[a][c]) return new int[] {a, b, c};
        return new int[0];
    }

    public static void main(String[] args) {
        int[][] ex1 = {{0, 1}, {1, 2}, {2, 3}, {3, 1}, {3, 4}, {4, 5}};
        if (!Arrays.equals(solve(6, ex1), new int[] {1, 2, 3})) throw new AssertionError("example 1");
        int[][] ex2 = {{0, 1}, {1, 2}, {2, 3}, {3, 0}};
        if (solve(4, ex2).length != 0) throw new AssertionError("example 2");
        if (solve(1, new int[][] {}).length != 0) throw new AssertionError("single vertex");
        int[] a = {1, 2, 3}, b = {1, 2, 3};
        if (a.equals(b) || !Arrays.equals(a, b)) throw new AssertionError("array equality");
        Random rnd = new Random(23302);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(10);
            List<int[]> list = new ArrayList<>();
            for (int x = 0; x < n; x++)
                for (int y = x + 1; y < n; y++)
                    if (rnd.nextInt(100) < 22) list.add(rnd.nextBoolean() ? new int[] {x, y} : new int[] {y, x});
            int[][] edges = list.toArray(new int[0][]);
            int[][] copy = new int[edges.length][];
            for (int i = 0; i < edges.length; i++) copy[i] = edges[i].clone();
            int[] got = solve(n, edges);
            for (int i = 0; i < edges.length; i++)
                if (!Arrays.equals(edges[i], copy[i])) throw new AssertionError("mutated");
            if (!Arrays.equals(got, oracle(n, edges))) throw new AssertionError("random t=" + t);
        }
    }
}
```

#### Solution: [Boundary] Single Edge And Parallel Edges (Author exercise)
<!-- id: ug-parallel-edges -->

**Approach.** Label every vertex with a piece number using a stack walk over the neighbor lists, where a self-loop simply puts the vertex into its own list. Then count the vertices and the edges in each piece. A piece holding k vertices and k - 1 edges is a tree, and anything with k or more edges contains a cycle, so the answer is true as soon as one piece has edges >= vertices. A doubled pair or a self-loop pushes its piece over that line without the code ever asking who the parent was. The oracle is different in kind: for each edge it removes that edge and asks by a fresh search whether its endpoints are still joined, and any edge that is still bridged means a cycle. The assertions include the false friend, a parent-vertex walk over set-based neighbors, which collapses a doubled pair into one entry and so reports no cycle.

**Complexity.** Labelling visits every vertex and every list entry once, and the counting pass touches each edge once, so time is O(n + m) and space is O(n + m).

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ParallelEdgesSolution {
    static boolean solve(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        int[] piece = new int[n];
        java.util.Arrays.fill(piece, -1);
        int pieces = 0;
        for (int s = 0; s < n; s++) {
            if (piece[s] != -1) continue;
            ArrayDeque<Integer> stack = new ArrayDeque<>();
            piece[s] = pieces;
            stack.push(s);
            while (!stack.isEmpty()) {
                int v = stack.pop();
                for (int w : adj.get(v)) {
                    if (piece[w] == -1) {
                        piece[w] = pieces;
                        stack.push(w);
                    }
                }
            }
            pieces++;
        }
        int[] verts = new int[pieces], cables = new int[pieces];
        for (int i = 0; i < n; i++) verts[piece[i]]++;
        for (int[] e : edges) cables[piece[e[0]]]++;
        for (int p = 0; p < pieces; p++) {
            if (cables[p] >= verts[p]) return true;
        }
        return false;
    }

    static boolean parentWithSets(int n, int[][] edges) {
        List<java.util.Set<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new java.util.HashSet<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        boolean[] seen = new boolean[n];
        for (int s = 0; s < n; s++) {
            if (!seen[s] && walkSets(adj, seen, s, -1)) return true;
        }
        return false;
    }

    static boolean walkSets(List<java.util.Set<Integer>> adj, boolean[] seen, int v, int parent) {
        seen[v] = true;
        for (int w : adj.get(v)) {
            if (w == parent) continue;
            if (seen[w] || walkSets(adj, seen, w, v)) return true;
        }
        return false;
    }

    static boolean joinedWithout(int n, int[][] edges, int skip, int from, int to) {
        boolean[] lit = new boolean[n];
        lit[from] = true;
        boolean grew = true;
        while (grew) {
            grew = false;
            for (int i = 0; i < edges.length; i++) {
                if (i == skip) continue;
                int a = edges[i][0], b = edges[i][1];
                if (lit[a] && !lit[b]) { lit[b] = true; grew = true; }
                if (lit[b] && !lit[a]) { lit[a] = true; grew = true; }
            }
        }
        return lit[to];
    }

    static boolean oracle(int n, int[][] edges) {
        for (int i = 0; i < edges.length; i++) {
            if (joinedWithout(n, edges, i, edges[i][0], edges[i][1])) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        if (!solve(4, new int[][] {{0, 1}, {1, 2}, {2, 1}})) throw new AssertionError("example 1");
        if (solve(3, new int[][] {{0, 1}})) throw new AssertionError("example 2");
        if (!solve(2, new int[][] {{1, 1}})) throw new AssertionError("self-loop");
        if (solve(1, new int[][] {})) throw new AssertionError("no edges");
        // false friend: parent rule over set-based neighbors cannot see a doubled string
        if (parentWithSets(2, new int[][] {{0, 1}, {1, 0}})) throw new AssertionError("set adjacency should miss");
        if (!solve(2, new int[][] {{0, 1}, {1, 0}})) throw new AssertionError("doubled pair");
        Random rnd = new Random(23303);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(8);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = edges[i].clone();
            boolean got = solve(n, edges);
            for (int i = 0; i < m; i++)
                if (edges[i][0] != copy[i][0] || edges[i][1] != copy[i][1]) throw new AssertionError("mutated");
            if (got != oracle(n, edges)) throw new AssertionError("random t=" + t);
        }
    }
}
```

#### Solution: [Recognize] Graph Valid Tree (LeetCode 261)
<!-- id: ug-valid-tree -->

**Approach.** Reject at once when the number of edges is not n - 1. Otherwise walk from vertex 0 with an explicit stack, marking each vertex the first time it is met, and answer true exactly when all n vertices were reached. No parent bookkeeping is needed, since n - 1 edges with one piece cannot hold a cycle. The oracle states the definition directly: the graph is a tree when it is connected and every single edge is a bridge, meaning that removing it leaves its endpoints apart, and it runs on random multigraphs as well as simple ones. The assertions cover both examples, the hostile layout with a triangle plus a path that has exactly n - 1 edges, and the false friend, a parent-vertex walk from vertex 0 that reports no cycle on two separate pieces.

**Complexity.** A single pass over the edge count, one list build and one walk give O(n + m) time, and the lists, marks and stack use O(n + m) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ValidTreeSolution {
    static boolean solve(int n, int[][] edges) {
        if (edges.length != n - 1) return false;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        seen[0] = true;
        stack.push(0);
        int reached = 1;
        while (!stack.isEmpty()) {
            int v = stack.pop();
            for (int w : adj.get(v)) {
                if (!seen[w]) {
                    seen[w] = true;
                    reached++;
                    stack.push(w);
                }
            }
        }
        return reached == n;
    }

    static boolean noRingFromZero(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        return !walk(adj, new boolean[n], 0, -1);
    }

    static boolean walk(List<List<Integer>> adj, boolean[] seen, int v, int parent) {
        seen[v] = true;
        for (int w : adj.get(v)) {
            if (w == parent) continue;
            if (seen[w] || walk(adj, seen, w, v)) return true;
        }
        return false;
    }

    static boolean[] litFrom(int n, int[][] edges, int skip, int from) {
        boolean[] lit = new boolean[n];
        lit[from] = true;
        boolean grew = true;
        while (grew) {
            grew = false;
            for (int i = 0; i < edges.length; i++) {
                if (i == skip) continue;
                int a = edges[i][0], b = edges[i][1];
                if (lit[a] && !lit[b]) { lit[b] = true; grew = true; }
                if (lit[b] && !lit[a]) { lit[a] = true; grew = true; }
            }
        }
        return lit;
    }

    static boolean oracle(int n, int[][] edges) {
        for (boolean on : litFrom(n, edges, -1, 0)) if (!on) return false;
        for (int i = 0; i < edges.length; i++) {
            if (litFrom(n, edges, i, edges[i][0])[edges[i][1]]) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        if (!solve(5, new int[][] {{0, 1}, {0, 2}, {0, 3}, {1, 4}})) throw new AssertionError("example 1");
        int[][] hostile = {{0, 1}, {1, 2}, {2, 0}, {3, 4}, {4, 5}};
        if (solve(6, hostile)) throw new AssertionError("example 2");
        if (!solve(1, new int[][] {})) throw new AssertionError("single vertex");
        if (solve(2, new int[][] {})) throw new AssertionError("two lone vertices");
        if (solve(3, new int[][] {{0, 1}, {1, 0}})) throw new AssertionError("doubled pair");
        // false friend: a ring-free report from vertex 0 says nothing about unreached pieces
        if (!noRingFromZero(4, new int[][] {{0, 1}, {2, 3}})) throw new AssertionError("walk reports no ring");
        if (solve(4, new int[][] {{0, 1}, {2, 3}})) throw new AssertionError("two pieces are not a tree");
        Random rnd = new Random(23304);
        int trees = 0;
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(3) == 0 ? n - 1 : rnd.nextInt(8);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = edges[i].clone();
            boolean got = solve(n, edges);
            for (int i = 0; i < m; i++)
                if (edges[i][0] != copy[i][0] || edges[i][1] != copy[i][1]) throw new AssertionError("mutated");
            if (got != oracle(n, edges)) throw new AssertionError("random t=" + t);
            if (got) trees++;
        }
        if (trees == 0) throw new AssertionError("random test never produced a tree");
    }
}
```
