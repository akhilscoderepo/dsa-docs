<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Prim

#### Solution: [Build] Grow One Tree Edge (Author exercise)
<!-- id: ga-prim-one-edge -->

**Approach.**
The method scans the edge list once and keeps the index of the best crossing edge seen so far. For each edge it tests whether exactly one endpoint is in the tree, by comparing the two flags with `!=`. A self loop has equal flags on both ends, so the test rejects it. An edge replaces the current best only when its weight is strictly smaller, so the first edge among equal weights keeps its place and the smaller index wins.

The invariant is that after reading the first `i` edges, `best` holds the crossing edge with the smallest weight among them, with the smallest index among equals. The strict comparison keeps the invariant when a tie appears. The method returns `-1` when `best` never changed, which means that no edge is crossing.

**Complexity.**
- **Time** is O(E), because the method reads each edge once.
- **Space** is O(1), because it keeps one index and no copy of the input.

```java run
import java.util.*;

public final class PrimOneEdge {
    /**
     * Returns the index of the cheapest crossing edge, or -1 when none crosses.
     * Time: O(E). Space: O(1).
     * Invariant: best is the cheapest crossing edge among the edges read so far, smallest index on ties.
     */
    static int cheapestCrossing(boolean[] inTree, int[][] edges) {
        // No crossing edge is known before the first edge is read.
        int best = -1;
        // One pass reads every edge once, which is the whole cost of the method.
        for (int i = 0; i < edges.length; i++) {
            // Exactly one endpoint inside means the two flags differ; a self loop never differs.
            if (inTree[edges[i][0]] == inTree[edges[i][1]]) continue;
            // A strictly smaller weight replaces the best, so an equal weight keeps the earlier index.
            if (best == -1 || edges[i][2] < edges[best][2]) best = i;
        }
        // The value -1 survives only when no edge crossed.
        return best;
    }

    /** Oracle: collect all crossing indices, sort by weight then index, take the first. */
    static int oracle(boolean[] inTree, int[][] edges) {
        List<Integer> cand = new ArrayList<>();
        for (int i = 0; i < edges.length; i++) {
            int a = edges[i][0], b = edges[i][1];
            if ((inTree[a] && !inTree[b]) || (!inTree[a] && inTree[b])) cand.add(i);
        }
        cand.sort((x, y) -> edges[x][2] != edges[y][2] ? Integer.compare(edges[x][2], edges[y][2]) : Integer.compare(x, y));
        return cand.isEmpty() ? -1 : cand.get(0);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (cheapestCrossing(new boolean[] {true, true, false, false}, new int[][] {{0, 1, 1}, {1, 2, 6}, {0, 3, 4}, {2, 3, 4}}) != 2) throw new AssertionError("ex1");
        if (cheapestCrossing(new boolean[] {true, true, true}, new int[][] {{0, 1, 2}, {1, 2, 3}}) != -1) throw new AssertionError("ex2");
        // A tie keeps the smaller index, and a self loop never crosses.
        if (cheapestCrossing(new boolean[] {true, false}, new int[][] {{1, 1, 0}, {0, 1, 5}, {1, 0, 5}}) != 1) throw new AssertionError("tie");
        // The method leaves its input unchanged.
        boolean[] flags = {true, false, false};
        int[][] es = {{0, 1, 3}, {1, 2, 1}};
        cheapestCrossing(flags, es);
        if (!Arrays.equals(flags, new boolean[] {true, false, false}) || es[0][2] != 3 || es[1][2] != 1) throw new AssertionError("mutation");
        // Random graphs with repeats, self loops, equal weights and the largest weight.
        Random rnd = new Random(2531);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(6);
            boolean[] in = new boolean[n];
            for (int i = 0; i < n; i++) in[i] = rnd.nextBoolean();
            int m = rnd.nextInt(10);
            int[][] e = new int[m][];
            for (int i = 0; i < m; i++) e[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(5) == 0 ? 2_000_000_000 : rnd.nextInt(4)};
            if (cheapestCrossing(in, e) != oracle(in, e)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Skip Stale Heap Edges (Author exercise)
<!-- id: ga-prim-stale-edges -->

**Approach.**
The method runs the lazy Prim loop from vertex 0 and counts instead of summing. The heap compares weight first and vertex second, so equal weights still leave in a fixed order. A removed pair whose vertex is already in the tree increments the counter and does nothing else. Any other pair joins its vertex and pushes one pair for each incident edge that leads to a vertex outside the tree.

The invariant is that the heap holds only pairs pushed from tree vertices, and a pair is stale exactly when its vertex joined after the push. A pair becomes stale only when another pair for the same vertex leaving the heap first. The loop runs until the heap is empty, so every pushed pair leaves. The count therefore equals the number of pushes minus the number of joined vertices other than vertex 0.

**Complexity.**
- **Time** is O(E log E), because the heap receives at most 2E pairs and each pair costs O(log E) to insert and to remove.
- **Space** is O(V + E) for the adjacency list, the flags and a heap of at most 2E pairs.

```java run
import java.util.*;

public final class PrimStaleEdges {
    /**
     * Returns how many removed heap pairs are stale in a Prim run from vertex 0.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: a pair is stale exactly when its vertex joined the tree after the pair was pushed.
     */
    static int staleCount(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each undirected edge is stored under both endpoints.
        for (int[] e : edges) {
            adj.get(e[0]).add(new int[] {e[1], e[2]});
            adj.get(e[1]).add(new int[] {e[0], e[2]});
        }
        boolean[] inTree = new boolean[n];
        // Weight decides first, and the vertex index breaks a tie.
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        heap.add(new long[] {0, 0});
        int stale = 0;
        // Each pass removes one pair, and the heap receives at most two pairs per edge.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int v = (int) top[1];
            // A pair whose vertex is inside is stale, so it is counted and skipped.
            if (inTree[v]) {
                stale++;
                continue;
            }
            inTree[v] = true;
            // Only edges that lead outside the tree enter the heap.
            for (int[] r : adj.get(v)) {
                if (!inTree[r[0]]) heap.add(new long[] {r[1], r[0]});
            }
        }
        return stale;
    }

    /** Oracle: the same rules with a linear scan of a list in place of the heap. */
    static int oracle(int n, int[][] edges) {
        boolean[] in = new boolean[n];
        List<long[]> pool = new ArrayList<>();
        pool.add(new long[] {0, 0});
        int stale = 0;
        while (!pool.isEmpty()) {
            int bi = 0;
            for (int i = 1; i < pool.size(); i++) {
                long[] p = pool.get(i), q = pool.get(bi);
                if (p[0] < q[0] || (p[0] == q[0] && p[1] < q[1])) bi = i;
            }
            long[] top = pool.remove(bi);
            int v = (int) top[1];
            if (in[v]) { stale++; continue; }
            in[v] = true;
            for (int[] e : edges) {
                if (e[0] == v && !in[e[1]]) pool.add(new long[] {e[2], e[1]});
                if (e[1] == v && !in[e[0]]) pool.add(new long[] {e[2], e[0]});
            }
        }
        return stale;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (staleCount(3, new int[][] {{0, 1, 1}, {0, 2, 2}, {1, 2, 5}}) != 1) throw new AssertionError("ex1");
        if (staleCount(3, new int[][] {{0, 1, 4}, {1, 2, 2}}) != 0) throw new AssertionError("ex2");
        // A disconnected vertex adds no pairs, and a lone vertex has none either.
        if (staleCount(4, new int[][] {{0, 1, 2}}) != 0 || staleCount(1, new int[0][]) != 0) throw new AssertionError("isolated");
        // Random graphs with repeats, self loops and many equal weights.
        Random rnd = new Random(2532);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(14);
            int[][] e = new int[m][];
            for (int i = 0; i < m; i++) e[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(4)};
            if (staleCount(n, e) != oracle(n, e)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Disconnected Graph (Author exercise)
<!-- id: ga-prim-disconnected -->

**Approach.**
The method runs lazy Prim from vertex 0 and counts the vertices that join. The total is a `long`, because two weights near two billion already exceed the range of `int`. When the heap empties, the method compares `joined` with `n`. A smaller count means that some vertex has no path to vertex 0, so no spanning tree exists and the method returns minus one. A graph with one vertex joins its only vertex at weight 0 and returns 0.

The invariant is that the tree is a minimum spanning tree of the vertices it covers, after each join, and the heap holds the crossing edges of that tree. When the heap is empty, no crossing edge remains, so the tree already spans the whole component. The tree covers the whole graph exactly when `joined == n`.

**Complexity.**
- **Time** is O(E log E), because the method inserts and removes each of at most 2E pairs once.
- **Space** is O(V + E) for the adjacency list, the flags and the heap.

```java run
import java.util.*;

public final class PrimDisconnected {
    /**
     * Returns the minimum spanning tree weight, or -1 when the graph is not connected.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: the tree is a minimum spanning tree of the vertices it covers.
     */
    static long mstWeight(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each undirected edge is stored under both endpoints.
        for (int[] e : edges) {
            adj.get(e[0]).add(new int[] {e[1], e[2]});
            adj.get(e[1]).add(new int[] {e[0], e[2]});
        }
        boolean[] inTree = new boolean[n];
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        // The first pair joins vertex 0 at no cost.
        heap.add(new long[] {0, 0});
        long total = 0;
        int joined = 0;
        // The loop ends when the heap is empty, which is when no crossing edge remains.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int v = (int) top[1];
            // A stale pair adds nothing.
            if (inTree[v]) continue;
            inTree[v] = true;
            // The sum is a long, so large weights cannot wrap.
            total += top[0];
            joined++;
            for (int[] r : adj.get(v)) {
                if (!inTree[r[0]]) heap.add(new long[] {r[1], r[0]});
            }
        }
        // A short count means a vertex is unreachable, so no tree exists.
        return joined == n ? total : -1;
    }

    /** Oracle: Kruskal with a union-find array, then a check that one component remains. */
    static long oracle(int n, int[][] edges) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        long total = 0;
        int used = 0;
        for (int[] e : sorted) {
            int a = find(parent, e[0]), b = find(parent, e[1]);
            if (a != b) {
                parent[a] = b;
                total += e[2];
                used++;
            }
        }
        return used == n - 1 ? total : -1;
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (mstWeight(3, new int[][] {{0, 1, 2_000_000_000}, {1, 2, 2_000_000_000}}) != 4_000_000_000L) throw new AssertionError("ex1");
        if (mstWeight(4, new int[][] {{0, 1, 3}, {2, 3, 1}}) != -1) throw new AssertionError("ex2");
        // Java fact: the same sum in int arithmetic wraps to a negative value.
        int wrapped = 2_000_000_000 + 2_000_000_000;
        if (wrapped >= 0) throw new AssertionError("int overflow");
        // One vertex costs 0, and two vertices without an edge have no tree.
        if (mstWeight(1, new int[0][]) != 0 || mstWeight(2, new int[0][]) != -1) throw new AssertionError("tiny");
        // Random graphs, many of them disconnected, with large and small weights.
        Random rnd = new Random(2533);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(12);
            int[][] e = new int[m][];
            for (int i = 0; i < m; i++) e[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(3) == 0 ? 2_000_000_000 - rnd.nextInt(3) : rnd.nextInt(6)};
            if (mstWeight(n, e) != oracle(n, e)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: ga-prim-connect-points -->

**Approach.**
The graph is complete, so it has about `n * n / 2` edges, and a heap of all of them would hold up to a million pairs. The method uses the array form of Prim instead. The array `key` holds, for each outside point, the weight of the cheapest edge to the tree, and it starts at infinity except for point 0. Each round scans `key` for the smallest outside entry and adds it to the total. It updates the longest edge and then lowers the other outside entries by their Manhattan distance to the new point. The scan replaces the heap. The method computes each distance on demand, so no edge list exists.

The invariant is that `key[v]` is the cheapest edge from the tree to the outside point `v`, which means the array holds the frontier in compact form. The smallest key is therefore the cheapest crossing edge and is safe. The longest edge is the maximum of the accepted keys. The first accepted key is 0 for point 0, so a single point returns `{0, 0}`.

**Complexity.**
- **Time** is O(n^2), because each of `n` rounds scans `n` entries once to pick and once to update.
- **Space** is O(n) for the `key` and flag arrays, since the edges are never stored.

```java run
import java.util.*;

public final class PrimConnectPoints {
    /**
     * Returns {minimum spanning tree weight, heaviest tree edge} under Manhattan distance.
     * Time: O(n^2). Space: O(n).
     * Invariant: key[v] is the cheapest edge from the tree to the outside point v.
     */
    static long[] connect(int[][] points) {
        int n = points.length;
        long[] key = new long[n];
        // Long.MAX_VALUE marks a point with no known edge to the tree.
        Arrays.fill(key, Long.MAX_VALUE);
        key[0] = 0;
        boolean[] inTree = new boolean[n];
        long total = 0;
        long longest = 0;
        // Each round adds exactly one point, so n rounds build the tree.
        for (int round = 0; round < n; round++) {
            int pick = -1;
            // This scan finds the cheapest crossing edge in O(n).
            for (int v = 0; v < n; v++) {
                if (!inTree[v] && (pick == -1 || key[v] < key[pick])) pick = v;
            }
            inTree[pick] = true;
            // The accepted key is the weight of the edge that attaches the point.
            total += key[pick];
            longest = Math.max(longest, key[pick]);
            // This scan lowers each outside key by the distance to the new point.
            for (int v = 0; v < n; v++) {
                if (inTree[v]) continue;
                long d = (long) Math.abs(points[pick][0] - points[v][0]) + Math.abs(points[pick][1] - points[v][1]);
                if (d < key[v]) key[v] = d;
            }
        }
        return new long[] {total, longest};
    }

    /** Oracle: Kruskal over all pairs; the last accepted edge is the heaviest. */
    static long[] oracle(int[][] points) {
        int n = points.length;
        List<long[]> all = new ArrayList<>();
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                all.add(new long[] {(long) Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]), i, j});
        all.sort((a, b) -> Long.compare(a[0], b[0]));
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        long total = 0, longest = 0;
        for (long[] e : all) {
            int a = find(parent, (int) e[1]), b = find(parent, (int) e[2]);
            if (a != b) {
                parent[a] = b;
                total += e[0];
                longest = e[0];
            }
        }
        return new long[] {total, longest};
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(connect(new int[][] {{0, 0}, {1, 1}, {1, 4}, {6, 1}}), new long[] {10, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(connect(new int[][] {{0, 0}, {0, 5}, {0, 6}}), new long[] {6, 5})) throw new AssertionError("ex2");
        // A single point needs no edge.
        if (!Arrays.equals(connect(new int[][] {{3, 3}}), new long[] {0, 0})) throw new AssertionError("single");
        // Java fact: the distance between extreme points exceeds int range once many edges are summed, so long is needed.
        long far = (long) Math.abs(1_000_000 - -1_000_000) * 2;
        if (far * 1000 <= Integer.MAX_VALUE) throw new AssertionError("range");
        // Random point sets, including extreme coordinates and collinear points.
        Random rnd = new Random(2534);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            Set<Long> seen = new HashSet<>();
            List<int[]> pts = new ArrayList<>();
            int span = rnd.nextInt(3) == 0 ? 1_000_000 : 6;
            while (pts.size() < n) {
                int x = rnd.nextInt(2 * span + 1) - span, y = rnd.nextBoolean() ? 0 : rnd.nextInt(2 * span + 1) - span;
                if (seen.add(x * 4_000_000L + y)) pts.add(new int[] {x, y});
            }
            int[][] p = pts.toArray(new int[0][]);
            if (!Arrays.equals(connect(p), oracle(p))) throw new AssertionError("random " + t);
        }
    }
}
```
