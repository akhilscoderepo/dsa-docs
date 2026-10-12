<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Bridges And Low Links

#### Solution: [Build] Discovery And Low Values (Author exercise)
<!-- id: ga-low-disc-values -->

**Approach.**
The method builds an adjacency list in which every entry stores the neighbor and the number of the edge. It then runs a recursive search from vertex 0. On entry to a vertex, the method gives it the next discovery time and sets its low link equal to that time. For each edge in order, it skips the edge number used to arrive, so a second edge between the same pair still counts. A neighbor that is undiscovered becomes a child, and after the call returns the method lowers the low link of the parent to the child value. A neighbor that is already discovered lowers the low link to its discovery time.

The invariant is that when a vertex returns, its low link is the smallest discovery time reachable from its subtree through one back edge other than the arrival edge. A discovered neighbor with a larger time is a descendant, so the minimum ignores it automatically. A self loop shows the vertex itself, which equals its own time and changes nothing.

**Complexity.**
- **Time** is O(V + E), because each adjacency entry is scanned once and each vertex is entered once.
- **Space** is O(V + E) for the adjacency list, the two arrays and a call stack as deep as the longest tree path.

```java run
import java.util.*;

public final class LowLinkValues {
    /** Adjacency list: entry {neighbor, edge number}, in edge order. */
    static List<List<int[]>> build(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        // One empty list per vertex.
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each edge is stored at both ends, so a self loop appears twice at its vertex.
        for (int id = 0; id < edges.length; id++) {
            adj.get(edges[id][0]).add(new int[] {edges[id][1], id});
            adj.get(edges[id][1]).add(new int[] {edges[id][0], id});
        }
        return adj;
    }

    /**
     * Returns {disc, low} for a depth-first search from vertex 0.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: on return, low[u] is the least discovery time the subtree of u reaches by one back edge.
     */
    static int[][] discAndLow(int n, int[][] edges) {
        List<List<int[]>> adj = build(n, edges);
        int[] disc = new int[n];
        int[] low = new int[n];
        // The value -1 marks a vertex the search has not reached.
        Arrays.fill(disc, -1);
        int[] timer = {0};
        visit(0, -1, adj, disc, low, timer);
        return new int[][] {disc, low};
    }

    static void visit(int u, int parentId, List<List<int[]>> adj, int[] disc, int[] low, int[] timer) {
        // The vertex receives the next time, and its low link starts at that time.
        disc[u] = low[u] = timer[0]++;
        // Each adjacency entry is scanned once, which gives the linear cost.
        for (int[] step : adj.get(u)) {
            int v = step[0];
            // The arrival edge is skipped by number, so a parallel edge still counts.
            if (step[1] == parentId) continue;
            if (disc[v] == -1) {
                // A new vertex becomes a child, and its low link is final after the call.
                visit(v, step[1], adj, disc, low, timer);
                low[u] = Math.min(low[u], low[v]);
            } else {
                // A discovered vertex is an ancestor or a finished descendant; a larger time changes nothing.
                low[u] = Math.min(low[u], disc[v]);
            }
        }
    }

    /** Oracle: an explicit-stack search builds the tree, then low is computed straight from its definition. */
    static int[][] oracle(int n, int[][] edges) {
        List<List<int[]>> adj = build(n, edges);
        int[] disc = new int[n];
        int[] parent = new int[n];
        int[] parentEdge = new int[n];
        Arrays.fill(disc, -1);
        Arrays.fill(parent, -1);
        Arrays.fill(parentEdge, -1);
        int[] next = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        int t = 0;
        // The root is discovered first.
        disc[0] = t++;
        stack.push(0);
        // Each loop pass either descends to a new vertex or finishes the top vertex.
        while (!stack.isEmpty()) {
            int u = stack.peek();
            if (next[u] == adj.get(u).size()) { stack.pop(); continue; }
            int[] step = adj.get(u).get(next[u]++);
            if (disc[step[0]] == -1) {
                disc[step[0]] = t++;
                parent[step[0]] = u;
                parentEdge[step[0]] = step[1];
                stack.push(step[0]);
            }
        }
        int[] low = new int[n];
        // For each vertex, take the minimum over its whole subtree by definition.
        for (int u = 0; u < n; u++) {
            int best = disc[u];
            for (int x = 0; x < n; x++) {
                // x is in the subtree of u when walking up the parents from x reaches u.
                boolean inside = false;
                for (int y = x; y != -1; y = parent[y]) if (y == u) { inside = true; break; }
                if (!inside) continue;
                best = Math.min(best, disc[x]);
                // Every edge leaving x counts, except the edge that enters u from its parent.
                for (int[] step : adj.get(x)) {
                    if (step[1] == parentEdge[u]) continue;
                    best = Math.min(best, disc[step[0]]);
                }
            }
            low[u] = best;
        }
        return new int[][] {disc, low};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] a = discAndLow(5, new int[][] {{0,1},{0,2},{1,2},{2,3},{3,4}});
        if (!Arrays.equals(a[0], new int[] {0,1,2,3,4}) || !Arrays.equals(a[1], new int[] {0,0,0,3,4})) throw new AssertionError("ex1");
        int[][] b = discAndLow(3, new int[][] {{0,1},{0,1},{1,2}});
        if (!Arrays.equals(b[0], new int[] {0,1,2}) || !Arrays.equals(b[1], new int[] {0,0,2})) throw new AssertionError("ex2");
        // A single vertex with a self loop keeps low equal to disc.
        int[][] c = discAndLow(1, new int[][] {{0,0}});
        if (c[0][0] != 0 || c[1][0] != 0) throw new AssertionError("self loop");
        // Random connected multigraphs against the oracle.
        Random rnd = new Random(2507);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> list = new ArrayList<>();
            // A random tree first guarantees connectivity.
            for (int v = 1; v < n; v++) list.add(new int[] {rnd.nextInt(v), v});
            int extra = rnd.nextInt(6);
            // Extra edges may repeat a pair or loop on a vertex.
            for (int k = 0; k < extra; k++) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n)});
            Collections.shuffle(list, rnd);
            // Vertex 0 may now be a leaf, which is fine because the search still starts there.
            int[][] edges = list.toArray(new int[0][]);
            int[][] got = discAndLow(n, edges);
            int[][] want = oracle(n, edges);
            if (!Arrays.equals(got[0], want[0]) || !Arrays.equals(got[1], want[1])) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Bridge Test (Author exercise)
<!-- id: ga-low-bridge-test -->

**Approach.**
The method walks the vertices in increasing order and skips the root. For each other vertex `v`, it compares `low[v]` with the discovery time of its parent. A strictly larger low link means that the subtree of `v` has no route to the parent or above. The tree edge is then a bridge, and the method adds `v`. Because the loop runs in increasing order, the output is already sorted.

The invariant is that `low[v] > disc[parent[v]]` holds exactly when the subtree of `v` is attached to the rest of the graph only by its tree edge. The comparison must be strict. An equal value means a back edge lands on the parent itself, which gives a second route.

**Complexity.**
- **Time** is O(n), because the method reads each vertex once and compares two numbers.
- **Space** is O(1) beyond the output list, since it keeps no other structure.

```java run
import java.util.*;

public final class BridgeTestOnArrays {
    /** Adjacency list: entry {neighbor, edge number}, in edge order. */
    static List<List<int[]>> build(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        // One empty list per vertex.
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each edge is stored at both ends, so a self loop appears twice at its vertex.
        for (int id = 0; id < edges.length; id++) {
            adj.get(edges[id][0]).add(new int[] {edges[id][1], id});
            adj.get(edges[id][1]).add(new int[] {edges[id][0], id});
        }
        return adj;
    }

    /**
     * Returns the vertices whose tree edge to the parent is a bridge, in increasing order.
     * Time: O(n). Space: O(1) beyond the result.
     * Invariant: low[v] > disc[parent[v]] exactly when no back edge leaves the subtree of v upward.
     */
    static int[] bridgeChildren(int[] parent, int[] disc, int[] low) {
        List<Integer> out = new ArrayList<>();
        // Vertex 0 is the root and has no tree edge, so the loop starts at 1.
        for (int v = 1; v < parent.length; v++) {
            // A strict comparison separates a stranded subtree from one with a second route.
            if (low[v] > disc[parent[v]]) out.add(v);
        }
        int[] res = new int[out.size()];
        // Copy the list into the int array that the contract requires.
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    /** Test helper: arrays from a depth-first search that skips the arrival edge by number. */
    static int[][] arrays(int n, int[][] edges) {
        List<List<int[]>> adj = build(n, edges);
        int[] disc = new int[n];
        int[] low = new int[n];
        int[] parent = new int[n];
        Arrays.fill(disc, -1);
        Arrays.fill(parent, -1);
        go(0, -1, adj, disc, low, parent, new int[] {0});
        return new int[][] {parent, disc, low};
    }

    static void go(int u, int pid, List<List<int[]>> adj, int[] disc, int[] low, int[] parent, int[] timer) {
        disc[u] = low[u] = timer[0]++;
        for (int[] s : adj.get(u)) {
            if (s[1] == pid) continue;
            if (disc[s[0]] == -1) {
                parent[s[0]] = u;
                go(s[0], s[1], adj, disc, low, parent, timer);
                low[u] = Math.min(low[u], low[s[0]]);
            } else low[u] = Math.min(low[u], disc[s[0]]);
        }
    }

    /** Oracle: remove each edge and search again; a bridge maps to its child endpoint. */
    static int[] oracle(int n, int[][] edges, int[] disc) {
        TreeSet<Integer> kids = new TreeSet<>();
        for (int skip = 0; skip < edges.length; skip++) {
            boolean[] seen = new boolean[n];
            Deque<Integer> st = new ArrayDeque<>();
            seen[0] = true;
            st.push(0);
            // Plain reachability from vertex 0 without the skipped edge.
            while (!st.isEmpty()) {
                int x = st.pop();
                for (int i = 0; i < edges.length; i++) {
                    if (i == skip) continue;
                    int y = edges[i][0] == x ? edges[i][1] : edges[i][1] == x ? edges[i][0] : -1;
                    if (y >= 0 && !seen[y]) { seen[y] = true; st.push(y); }
                }
            }
            boolean cut = false;
            for (boolean s : seen) if (!s) cut = true;
            // The child endpoint is the one discovered later.
            if (cut) kids.add(disc[edges[skip][0]] > disc[edges[skip][1]] ? edges[skip][0] : edges[skip][1]);
        }
        int[] res = new int[kids.size()];
        int k = 0;
        for (int v : kids) res[k++] = v;
        return res;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[] r1 = bridgeChildren(new int[] {-1,0,1,2,3,4}, new int[] {0,1,2,3,4,5}, new int[] {0,0,0,3,4,5});
        if (!Arrays.equals(r1, new int[] {3,4,5})) throw new AssertionError("ex1");
        int[] r2 = bridgeChildren(new int[] {-1,0,1}, new int[] {0,1,2}, new int[] {0,0,0});
        if (r2.length != 0) throw new AssertionError("ex2");
        // The equal case is not a bridge, and one more than the parent time is.
        if (bridgeChildren(new int[] {-1,0}, new int[] {0,1}, new int[] {0,0}).length != 0) throw new AssertionError("equal");
        if (bridgeChildren(new int[] {-1,0}, new int[] {0,1}, new int[] {0,1}).length != 1) throw new AssertionError("greater");
        // Random connected multigraphs: arrays from a real search, answers from edge removal.
        Random rnd = new Random(2508);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> list = new ArrayList<>();
            for (int v = 1; v < n; v++) list.add(new int[] {rnd.nextInt(v), v});
            for (int k = rnd.nextInt(5); k > 0; k--) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n)});
            Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            int[][] a = arrays(n, edges);
            int[] got = bridgeChildren(a[0], a[1], a[2]);
            int[] want = oracle(n, edges, a[1]);
            if (!Arrays.equals(got, want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Root Articulation Rule (Author exercise)
<!-- id: ga-low-root-articulation -->

**Approach.**
The method searches from every undiscovered vertex in increasing order, so each component gets its own root. Inside the recursive call, it counts the children of the current vertex. After each child returns, it lowers the low link of the current vertex. For a vertex that is not a root, one child with `low[c] >= disc[u]` marks the vertex. The comparison is nonstrict, because a back edge that lands exactly on `u` still disconnects the child subtree once `u` is gone. For a root, the method ignores the low links and marks the root only when it has two or more children. A marked vertex goes into a sorted set, so repeats collapse.

The invariant has two parts. A nonroot vertex splits the graph exactly when some child subtree cannot reach a proper ancestor. A root splits it exactly when its tree has two or more child subtrees. In a root with one child, every other vertex of the component sits in that child subtree, so removing the root leaves one piece. The nonroot formula would flag every root with a child, because the root has the smallest discovery time and `low[c] >= disc[root]` always holds.

**Complexity.**
- **Time** is O(V + E), because the searches together scan each adjacency entry once.
- **Space** is O(V + E) for the adjacency list, the arrays, the result set and the call stack.

```java run
import java.util.*;

public final class RootArticulationRule {
    /** Adjacency list: entry {neighbor, edge number}, in edge order. */
    static List<List<int[]>> build(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        // One empty list per vertex.
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each edge is stored at both ends, so a self loop appears twice at its vertex.
        for (int id = 0; id < edges.length; id++) {
            adj.get(edges[id][0]).add(new int[] {edges[id][1], id});
            adj.get(edges[id][1]).add(new int[] {edges[id][0], id});
        }
        return adj;
    }

    /**
     * Returns all articulation points in increasing order.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a nonroot u splits the graph when a child c has low[c] >= disc[u]; a root splits it with two or more children.
     */
    static int[] articulation(int n, int[][] edges) {
        List<List<int[]>> adj = build(n, edges);
        int[] disc = new int[n];
        int[] low = new int[n];
        Arrays.fill(disc, -1);
        TreeSet<Integer> found = new TreeSet<>();
        int[] timer = {0};
        // A new search starts at each vertex that earlier searches did not reach.
        for (int s = 0; s < n; s++) {
            if (disc[s] == -1) visit(s, -1, adj, disc, low, timer, found);
        }
        int[] out = new int[found.size()];
        int k = 0;
        // The tree set already iterates in increasing order.
        for (int v : found) out[k++] = v;
        return out;
    }

    static void visit(int u, int parentId, List<List<int[]>> adj, int[] disc, int[] low, int[] timer, TreeSet<Integer> found) {
        disc[u] = low[u] = timer[0]++;
        int children = 0;
        // Each adjacency entry is scanned once.
        for (int[] step : adj.get(u)) {
            int v = step[0];
            // The arrival edge is skipped by number.
            if (step[1] == parentId) continue;
            if (disc[v] == -1) {
                children++;
                visit(v, step[1], adj, disc, low, timer, found);
                low[u] = Math.min(low[u], low[v]);
                // The nonstrict test applies below the root only.
                if (parentId != -1 && low[v] >= disc[u]) found.add(u);
            } else {
                low[u] = Math.min(low[u], disc[v]);
            }
        }
        // A root is decided by its child count and by nothing else.
        if (parentId == -1 && children >= 2) found.add(u);
    }

    /** Counts components among the vertices that are not removed. */
    static int components(int n, int[][] edges, int removed) {
        boolean[] seen = new boolean[n];
        int count = 0;
        for (int s = 0; s < n; s++) {
            if (s == removed || seen[s]) continue;
            count++;
            Deque<Integer> st = new ArrayDeque<>();
            seen[s] = true;
            st.push(s);
            // Plain reachability that never enters the removed vertex.
            while (!st.isEmpty()) {
                int x = st.pop();
                for (int[] e : edges) {
                    int y = e[0] == x ? e[1] : e[1] == x ? e[0] : -1;
                    if (y >= 0 && y != removed && !seen[y]) { seen[y] = true; st.push(y); }
                }
            }
        }
        return count;
    }

    /** Oracle: remove each vertex and compare component counts. */
    static int[] oracle(int n, int[][] edges) {
        int base = components(n, edges, -1);
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            boolean alone = true;
            // A vertex with no edge to another vertex is a component by itself.
            for (int[] e : edges) if ((e[0] == v || e[1] == v) && e[0] != e[1]) alone = false;
            int expected = alone ? base - 1 : base;
            if (components(n, edges, v) > expected) out.add(v);
        }
        int[] res = new int[out.size()];
        for (int i = 0; i < res.length; i++) res[i] = out.get(i);
        return res;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[] a = articulation(6, new int[][] {{0,1},{0,2},{0,3},{3,4},{4,5},{5,3}});
        if (!Arrays.equals(a, new int[] {0,3})) throw new AssertionError("ex1");
        int[] b = articulation(7, new int[][] {{0,1},{1,2},{2,0},{3,4},{4,5},{5,3},{5,6}});
        if (!Arrays.equals(b, new int[] {5})) throw new AssertionError("ex2");
        // A root with one child is not an articulation point, and an isolated vertex never is.
        if (articulation(2, new int[][] {{0,1}}).length != 0) throw new AssertionError("root one child");
        if (articulation(3, new int[][] {{0,0}}).length != 0) throw new AssertionError("isolated");
        // A path of three has a middle articulation point.
        if (!Arrays.equals(articulation(3, new int[][] {{0,1},{1,2}}), new int[] {1})) throw new AssertionError("path");
        // Random graphs, possibly disconnected, with repeats and loops, against the oracle.
        Random rnd = new Random(2509);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(articulation(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Critical Connections in a Network (LeetCode 1192)
<!-- id: ga-low-critical-connections -->

**Approach.**
The method runs one search from server 0 and returns the size of each subtree. When a child `v` of `u` returns with `low[v] > disc[u]`, the tree edge is critical. The subtree of `v` holds `size[v]` servers, so removing the edge leaves sides of `size[v]` and `n - size[v]`. The method counts the edge and keeps the largest value of the smaller side. The standard task lists the edges. This contract needs only a count and a size, so the method stores no edge list.

The invariant is that after a child returns, `low[v]` and the subtree size of `v` are final. The size is the number of servers on the side of `v` when the tree edge is cut. A bridge leaves no other connection between the subtree and the rest. The method skips the arrival edge by number, so a repeated connection is never critical.

**Complexity.**
- **Time** is O(V + E), because the single search scans each adjacency entry once and adds sizes in constant time per vertex.
- **Space** is O(V + E) for the adjacency list, the arrays and the recursion, which reaches depth n on a path.

```java run
import java.util.*;

public final class CriticalSmallSide {
    /** Adjacency list: entry {neighbor, edge number}, in edge order. */
    static List<List<int[]>> build(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        // One empty list per vertex.
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each edge is stored at both ends, so a self loop appears twice at its vertex.
        for (int id = 0; id < edges.length; id++) {
            adj.get(edges[id][0]).add(new int[] {edges[id][1], id});
            adj.get(edges[id][1]).add(new int[] {edges[id][0], id});
        }
        return adj;
    }

    static int count;
    static int bestSmall;

    /**
     * Returns {number of critical connections, largest small side}.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: when a child returns, low[v] and its subtree size are final, so a bridge cuts size[v] from n - size[v].
     */
    static int[] analyze(int n, int[][] connections) {
        List<List<int[]>> adj = build(n, connections);
        int[] disc = new int[n];
        int[] low = new int[n];
        Arrays.fill(disc, -1);
        count = 0;
        bestSmall = 0;
        visit(0, -1, n, adj, disc, low, new int[] {0});
        return new int[] {count, bestSmall};
    }

    static int visit(int u, int parentId, int n, List<List<int[]>> adj, int[] disc, int[] low, int[] timer) {
        disc[u] = low[u] = timer[0]++;
        // The vertex counts itself in its subtree size.
        int size = 1;
        for (int[] step : adj.get(u)) {
            int v = step[0];
            // The arrival edge is skipped by number.
            if (step[1] == parentId) continue;
            if (disc[v] == -1) {
                int below = visit(v, step[1], n, adj, disc, low, timer);
                size += below;
                low[u] = Math.min(low[u], low[v]);
                // A critical connection cuts the child subtree from the rest of the network.
                if (low[v] > disc[u]) {
                    count++;
                    bestSmall = Math.max(bestSmall, Math.min(below, n - below));
                }
            } else {
                low[u] = Math.min(low[u], disc[v]);
            }
        }
        return size;
    }

    /** Oracle: remove each connection, measure the side that contains server 0, and take the smaller side. */
    static int[] oracle(int n, int[][] connections) {
        int cnt = 0;
        int best = 0;
        for (int skip = 0; skip < connections.length; skip++) {
            boolean[] seen = new boolean[n];
            Deque<Integer> st = new ArrayDeque<>();
            seen[0] = true;
            st.push(0);
            int reached = 1;
            // Reachability from server 0 without the skipped connection.
            while (!st.isEmpty()) {
                int x = st.pop();
                for (int i = 0; i < connections.length; i++) {
                    if (i == skip) continue;
                    int y = connections[i][0] == x ? connections[i][1] : connections[i][1] == x ? connections[i][0] : -1;
                    if (y >= 0 && !seen[y]) { seen[y] = true; reached++; st.push(y); }
                }
            }
            // Fewer reached servers than n means this connection is critical.
            if (reached < n) { cnt++; best = Math.max(best, Math.min(reached, n - reached)); }
        }
        return new int[] {cnt, best};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[] a = analyze(7, new int[][] {{0,1},{1,2},{2,0},{2,3},{3,4},{4,5},{5,3},{5,6},{6,5}});
        if (!Arrays.equals(a, new int[] {1,3})) throw new AssertionError("ex1");
        int[] b = analyze(6, new int[][] {{0,1},{1,2},{2,0},{2,3},{3,4},{4,5}});
        if (!Arrays.equals(b, new int[] {3,3})) throw new AssertionError("ex2");
        // A single server and a pure cycle have no critical connection.
        if (!Arrays.equals(analyze(1, new int[0][]), new int[] {0,0})) throw new AssertionError("single");
        if (!Arrays.equals(analyze(4, new int[][] {{0,1},{1,2},{2,3},{3,0}}), new int[] {0,0})) throw new AssertionError("cycle");
        // A path of 1000 servers recurses 1000 deep and still completes with all 999 connections critical.
        int[][] path = new int[999][];
        for (int i = 0; i < 999; i++) path[i] = new int[] {i, i + 1};
        if (!Arrays.equals(analyze(1000, path), new int[] {999,500})) throw new AssertionError("deep path");
        // Random connected multigraphs against the oracle.
        Random rnd = new Random(2510);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            List<int[]> list = new ArrayList<>();
            for (int v = 1; v < n; v++) list.add(new int[] {rnd.nextInt(v), v});
            for (int k = rnd.nextInt(6); k > 0; k--) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n)});
            Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            if (!Arrays.equals(analyze(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```
