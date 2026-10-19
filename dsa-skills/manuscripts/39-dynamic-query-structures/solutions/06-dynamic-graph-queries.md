<!-- solutions-for: 06-dynamic-graph-queries -->
### Solutions For Dynamic Graph Queries

#### Solution: [Build] Static Shortest-Path Calculator (Author exercise)
<!-- id: dq39-static-calculator -->

**Approach.** The graph never changes and queries dominate, so the calculator pays once for a table of all pairs. The constructor sets every cell to `INF`, sets the diagonal to 0, keeps the cheapest cost for repeated pairs and runs Floyd-Warshall. After the pass for intermediate node `k`, each cell holds the cheapest path that uses only intermediates from `0` to `k`. This invariant makes the final table exact.

A query reads one cell and maps `INF` to -1. Dijkstra from the source is the alternative and gives the same answers at O((V + E) log V) per query. The harness compares both with a Bellman-Ford oracle on random graphs, and `INF = Long.MAX_VALUE / 4` keeps sums of costs safe from overflow.

**Complexity.**

- **Time** is O(n^3) for construction and O(1) per query, because the triple loop touches n^3 cells and a query reads one.
- **Space** is O(n^2), because the table stores one `long` per ordered pair.

```java run
import java.util.*;

public final class StaticCalculator {
    private static final long INF = Long.MAX_VALUE / 4; // large, yet two INF values plus a cost still fit in a long
    private final long[][] dist;

    /**
     * Builds the all-pairs table once from the edge list.
     * Time: O(n^3), because Floyd-Warshall visits every (k, i, j) triple.
     * Space: O(n^2), because the table holds one long per ordered pair.
     * Invariant: after round k, dist[i][j] is the cheapest cost using intermediates 0..k only.
     */
    StaticCalculator(int n, int[][] edges) {
        // Allocate the table; this is the O(n^2) memory of the design.
        dist = new long[n][n];
        // Mark every pair unreachable first.
        for (long[] row : dist) Arrays.fill(row, INF);
        // A node reaches itself at cost 0.
        for (int i = 0; i < n; i++) dist[i][i] = 0;
        // Keep only the cheapest cost for repeated pairs.
        for (int[] e : edges) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);
        // Round k allows node k as an intermediate stop.
        for (int k = 0; k < n; k++)
            // Source of the candidate route.
            for (int i = 0; i < n; i++)
                // Target of the candidate route; the n^3 total comes from this nesting.
                for (int j = 0; j < n; j++)
                    // Take the cheaper of the old route and the route through k.
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
    }

    /**
     * Reads one table cell.
     * Time: O(1). Space: O(1).
     * Invariant: the table is exact, so the stored value is the answer.
     */
    long distance(int a, int b) {
        // INF means no path, which the contract reports as -1.
        return dist[a][b] >= INF ? -1 : dist[a][b];
    }

    /**
     * Alternative design: one Dijkstra search per query over adjacency lists.
     * Time: O((V + E) log V) per call. Space: O(V + E).
     * Invariant: a node leaves the queue with its final distance because costs are non-negative.
     */
    static long dijkstra(int n, int[][] edges, int from, int to) {
        // Build adjacency lists of {target, cost}.
        List<long[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) adj[e[0]].add(new long[] {e[1], e[2]});
        // Distances start unreached.
        long[] d = new long[n];
        Arrays.fill(d, INF);
        d[from] = 0;
        // Heap ordered with Long.compare, never subtraction, so large values cannot overflow.
        PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
        pq.add(new long[] {0, from});
        // Each pop settles the cheapest unsettled node.
        while (!pq.isEmpty()) {
            long[] top = pq.poll();
            int u = (int) top[1];
            // Skip an entry that a cheaper one already replaced.
            if (top[0] > d[u]) continue;
            // Try to improve each neighbor through u.
            for (long[] e : adj[u]) {
                int v = (int) e[0];
                // A strictly cheaper route updates the neighbor and queues it.
                if (d[u] + e[1] < d[v]) { d[v] = d[u] + e[1]; pq.add(new long[] {d[v], v}); }
            }
        }
        // Report -1 for unreachable targets.
        return d[to] >= INF ? -1 : d[to];
    }

    /** Brute-force oracle: Bellman-Ford with n rounds over the raw edge list. */
    static long oracle(int n, int[][] edges, int from, int to) {
        // Start with only the source known.
        long[] d = new long[n];
        Arrays.fill(d, INF);
        d[from] = 0;
        // A shortest path has at most n - 1 edges, so n rounds suffice.
        for (int round = 0; round < n; round++)
            // Relax every edge once per round.
            for (int[] e : edges) if (d[e[0]] < INF && d[e[0]] + e[2] < d[e[1]]) d[e[1]] = d[e[0]] + e[2];
        // Same -1 convention as the calculator.
        return d[to] >= INF ? -1 : d[to];
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2 from the problem statement.
        int[][] ex = {{0, 1, 5}, {1, 2, 4}, {2, 3, 1}};
        StaticCalculator c = new StaticCalculator(4, ex);
        if (c.distance(0, 3) != 10) throw new AssertionError("example 1");
        if (c.distance(3, 0) != -1) throw new AssertionError("example 2");
        // Checks a == b returns 0 and that sums near the cost limit stay exact in long.
        if (c.distance(2, 2) != 0) throw new AssertionError("self distance");
        int[][] big = {{0, 1, 1_000_000}, {1, 2, 1_000_000}};
        if (new StaticCalculator(3, big).distance(0, 2) != 2_000_000L) throw new AssertionError("long sum");
        // Checks Floyd-Warshall, Dijkstra and the oracle against each other on random graphs with repeated pairs.
        Random rnd = new Random(39);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(2 * n + 3);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(20)};
            StaticCalculator s = new StaticCalculator(n, edges);
            for (int a = 0; a < n; a++)
                for (int b = 0; b < n; b++) {
                    long want = oracle(n, edges, a, b);
                    if (s.distance(a, b) != want) throw new AssertionError("floyd " + a + "->" + b);
                    if (dijkstra(n, edges, a, b) != want) throw new AssertionError("dijkstra " + a + "->" + b);
                }
        }
    }
}
```

#### Solution: [Vary] Graph With Shortest Path Calculator (LeetCode 2642)
<!-- id: dq39-add-edge-calculator -->

**Approach.** Edges arrive between queries, so the table must stay exact after each insert. The design keeps the all-pairs table. A new edge `a -> b` with cost `w` improves a pair `(i, j)` only through the route `i` to `a`, the new edge, then `b` to `j`, because costs are positive and a shortest path never crosses the same edge twice. Taking the minimum of the old cell and that sum, for every pair, restores the invariant that every cell equals the true shortest cost over all accepted edges.

With about as many inserts as queries and at most 100 nodes, an insert at O(n^2) and a query at O(1) beat a search per query. The alternative `DijkstraGraph` appends to adjacency lists and searches on demand. The harness runs random interleaved calls on both and compares each answer with a Bellman-Ford oracle over the accepted edge list.

**Complexity.**

- **Time** is O(n^3) to construct, O(n^2) per `addEdge` and O(1) per `shortestPath`, because an insert scans each pair once and a query reads one cell.
- **Space** is O(n^2), because the table keeps one `long` per ordered pair.

```java run
import java.util.*;

public final class AddEdgeCalculator {
    private static final long INF = Long.MAX_VALUE / 4; // safe against overflow when two INF values are added
    private final int n;
    private final long[][] dist;

    /**
     * Creates the object and fills the table with Floyd-Warshall.
     * Time: O(n^3). Space: O(n^2).
     * Invariant: dist[i][j] is the true shortest cost over the edges accepted so far.
     */
    AddEdgeCalculator(int n, int[][] edges) {
        // Remember the node count for later inserts.
        this.n = n;
        dist = new long[n][n];
        // Start with no known path.
        for (long[] row : dist) Arrays.fill(row, INF);
        // Zero cost from a node to itself.
        for (int i = 0; i < n; i++) dist[i][i] = 0;
        // Load the initial edges.
        for (int[] e : edges) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);
        // Intermediate node k, then source i, then target j: the n^3 cost.
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    // Keep the cheaper of the direct cell and the route through k.
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
    }

    /**
     * Inserts a directed edge and repairs the table.
     * Time: O(n^2), because every pair is examined once. Space: O(1).
     * Invariant: after the call, every cell is exact for the enlarged edge set.
     */
    void addEdge(int a, int b, long w) {
        // Every possible source of an improved route.
        for (int i = 0; i < n; i++)
            // Every possible target; the pair count n^2 is the cost of one insert.
            for (int j = 0; j < n; j++)
                // The new edge appears once in the route: i to a, the edge, b to j.
                dist[i][j] = Math.min(dist[i][j], dist[i][a] + w + dist[b][j]);
    }

    /**
     * Answers one query from the table.
     * Time: O(1). Space: O(1).
     */
    long shortestPath(int from, int to) {
        // INF means unreachable, which maps to -1.
        return dist[from][to] >= INF ? -1 : dist[from][to];
    }

    /** Alternative: adjacency lists with Dijkstra per query; insert is O(1), query is O((V + E) log V). */
    static final class DijkstraGraph {
        private final int n;
        private final List<long[]>[] adj;

        @SuppressWarnings("unchecked")
        DijkstraGraph(int n, int[][] edges) {
            // One list per node.
            this.n = n;
            adj = new List[n];
            for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
            // Load the initial edges.
            for (int[] e : edges) addEdge(e[0], e[1], e[2]);
        }

        void addEdge(int a, int b, long w) {
            // Appending is O(1) and leaves no stale state.
            adj[a].add(new long[] {b, w});
        }

        long shortestPath(int from, int to) {
            // Fresh distances per query: this is the repeated work.
            long[] d = new long[n];
            Arrays.fill(d, INF);
            d[from] = 0;
            // Compare with Long.compare to avoid subtraction overflow.
            PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
            pq.add(new long[] {0, from});
            // Settle nodes in order of cost.
            while (!pq.isEmpty()) {
                long[] top = pq.poll();
                int u = (int) top[1];
                // Skip outdated entries.
                if (top[0] > d[u]) continue;
                // Relax each outgoing edge.
                for (long[] e : adj[u]) {
                    int v = (int) e[0];
                    if (d[u] + e[1] < d[v]) { d[v] = d[u] + e[1]; pq.add(new long[] {d[v], v}); }
                }
            }
            // -1 when the target stays unreached.
            return d[to] >= INF ? -1 : d[to];
        }
    }

    /** Brute-force oracle: Bellman-Ford over the list of accepted edges. */
    static long oracle(int n, List<int[]> edges, int from, int to) {
        long[] d = new long[n];
        Arrays.fill(d, INF);
        d[from] = 0;
        // n rounds are enough for any simple shortest path.
        for (int r = 0; r < n; r++)
            for (int[] e : edges) if (d[e[0]] < INF && d[e[0]] + e[2] < d[e[1]]) d[e[1]] = d[e[0]] + e[2];
        return d[to] >= INF ? -1 : d[to];
    }

    public static void main(String[] args) {
        // Checks the worked example: 10, then 7 after the shortcut, then 7 after a costlier edge.
        int[][] ex = {{0, 1, 5}, {1, 2, 4}, {2, 3, 1}};
        AddEdgeCalculator g = new AddEdgeCalculator(4, ex);
        if (g.shortestPath(0, 3) != 10) throw new AssertionError("before");
        g.addEdge(0, 2, 6);
        if (g.shortestPath(0, 3) != 7) throw new AssertionError("after shortcut");
        g.addEdge(0, 3, 9);
        if (g.shortestPath(0, 3) != 7) throw new AssertionError("costlier edge");
        // Checks the maximum cost chain sums in long: 99 edges of 10^6 sum to 99,000,000 exactly.
        int[][] chain = new int[99][];
        for (int i = 0; i < 99; i++) chain[i] = new int[] {i, i + 1, 1_000_000};
        if (new AddEdgeCalculator(100, chain).shortestPath(0, 99) != 99_000_000L) throw new AssertionError("chain");
        // Checks interleaved random calls on both designs against the oracle (no duplicate pairs, as stated).
        Random rnd = new Random(2642);
        for (int t = 0; t < 300; t++) {
            int n = 2 + rnd.nextInt(6);
            boolean[][] used = new boolean[n][n];
            List<int[]> all = new ArrayList<>();
            for (int i = 0; i < n * 2; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b || used[a][b]) continue;
                used[a][b] = true;
                all.add(new int[] {a, b, 1 + rnd.nextInt(20)});
            }
            AddEdgeCalculator f = new AddEdgeCalculator(n, all.toArray(new int[0][]));
            DijkstraGraph dj = new DijkstraGraph(n, all.toArray(new int[0][]));
            for (int step = 0; step < 25; step++) {
                if (rnd.nextBoolean()) {
                    int a = rnd.nextInt(n), b = rnd.nextInt(n);
                    if (a == b || used[a][b]) continue;
                    used[a][b] = true;
                    int w = 1 + rnd.nextInt(20);
                    all.add(new int[] {a, b, w});
                    f.addEdge(a, b, w);
                    dj.addEdge(a, b, w);
                } else {
                    int a = rnd.nextInt(n), b = rnd.nextInt(n);
                    long want = oracle(n, all, a, b);
                    if (f.shortestPath(a, b) != want) throw new AssertionError("table " + a + "->" + b);
                    if (dj.shortestPath(a, b) != want) throw new AssertionError("dijkstra " + a + "->" + b);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Duplicate And Dominated Edges (Author exercise)
<!-- id: dq39-dominated-edges -->

**Approach.** Repeated pairs, self-loops and unused edges all share one property: they do not beat the stored value. A new edge `a -> b` with cost `w` can improve some cell only if `w < dist[a][b]`. If `w >= dist[a][b]`, every route through the new edge costs at least as much as the same route through the stored shortest path from `a` to `b`, so no cell changes and the method returns `false` without scanning. A self-loop has `dist[a][a] = 0` and a non-negative cost, so it falls into the same case.

Otherwise the repair scans every pair, counts strict decreases and returns whether the count is positive. Strict comparison makes ties report `false`. The harness compares the returned flag with a full Bellman-Ford recomputation before and after each insert, and it compares the whole table.

**Complexity.**

- **Time** is O(1) for a dominated edge and O(n^2) for an improving edge, because the early check skips the scan and the repair visits every pair.
- **Space** is O(n^2), because the table keeps one `long` per ordered pair and the object stores no edge list.

```java run
import java.util.*;

public final class DominatedEdges {
    private static final long INF = Long.MAX_VALUE / 4; // overflow-safe sentinel for unreachable pairs
    private final int n;
    private final long[][] dist;

    /**
     * Creates an empty graph on n nodes.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: dist[i][j] is the cheapest cost over every accepted edge, and dist[i][i] stays 0.
     */
    DominatedEdges(int n) {
        // Allocate the table.
        this.n = n;
        dist = new long[n][n];
        // No edges yet, so every off-diagonal pair is unreachable.
        for (long[] row : dist) Arrays.fill(row, INF);
        // The diagonal is free.
        for (int i = 0; i < n; i++) dist[i][i] = 0;
    }

    /**
     * Inserts an edge and reports whether any pair distance became strictly smaller.
     * Time: O(1) when dominated, O(n^2) when improving. Space: O(1).
     * Invariant: equal or larger costs leave every cell untouched.
     */
    boolean addEdge(int a, int b, long w) {
        // A dominated edge (duplicate, self-loop or costlier) cannot help any route, so skip the scan.
        if (w >= dist[a][b]) return false;
        // Count cells that strictly decrease.
        int changed = 0;
        // Snapshot the two rows used by the formula, because the loop below overwrites cells of row a and column b.
        long[] toA = new long[n];
        long[] fromB = dist[b].clone();
        // Copy dist[i][a] for every source i.
        for (int i = 0; i < n; i++) toA[i] = dist[i][a];
        // Every source of an improved route.
        for (int i = 0; i < n; i++)
            // Every target; this is the O(n^2) cost of an improving insert.
            for (int j = 0; j < n; j++) {
                // Route i to a, the new edge, then b to j.
                long cand = toA[i] + w + fromB[j];
                // Strict comparison keeps ties as unchanged.
                if (cand < dist[i][j]) { dist[i][j] = cand; changed++; }
            }
        // True exactly when at least one cell shrank.
        return changed > 0;
    }

    /**
     * Reads one cell.
     * Time: O(1). Space: O(1).
     */
    long shortestPath(int from, int to) {
        // Unreachable pairs report -1.
        return dist[from][to] >= INF ? -1 : dist[from][to];
    }

    /** Brute-force oracle: Bellman-Ford distances from every source over the raw edge list. */
    static long[][] oracleTable(int n, List<int[]> edges) {
        long[][] t = new long[n][n];
        // One search per source.
        for (int s = 0; s < n; s++) {
            Arrays.fill(t[s], INF);
            t[s][s] = 0;
            for (int r = 0; r < n; r++)
                for (int[] e : edges) if (t[s][e[0]] < INF && t[s][e[0]] + e[2] < t[s][e[1]]) t[s][e[1]] = t[s][e[0]] + e[2];
        }
        return t;
    }

    public static void main(String[] args) {
        // Checks Example 1: improve, worse duplicate, equal duplicate.
        DominatedEdges g = new DominatedEdges(3);
        if (!g.addEdge(0, 1, 3)) throw new AssertionError("first edge");
        if (g.addEdge(0, 1, 7)) throw new AssertionError("worse duplicate");
        if (g.addEdge(0, 1, 3)) throw new AssertionError("equal duplicate");
        // Checks Example 2: path 0 to 2, a zero-cost self-loop, then a strictly better direct edge.
        g.addEdge(1, 2, 2);
        if (g.shortestPath(0, 2) != 5) throw new AssertionError("path");
        if (g.addEdge(1, 1, 0)) throw new AssertionError("self-loop");
        if (!g.addEdge(0, 2, 4)) throw new AssertionError("better direct edge");
        // Checks a zero-cost edge is accepted and shortens distances.
        DominatedEdges z = new DominatedEdges(2);
        if (!z.addEdge(0, 1, 0) || z.shortestPath(0, 1) != 0) throw new AssertionError("zero cost");
        // Checks every insert against full recomputation: flag, and the whole table.
        Random rnd = new Random(77);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(6);
            DominatedEdges d = new DominatedEdges(n);
            List<int[]> all = new ArrayList<>();
            for (int step = 0; step < 20; step++) {
                long[][] before = oracleTable(n, all);
                int a = rnd.nextInt(n), b = rnd.nextInt(n), w = rnd.nextInt(15);
                boolean got = d.addEdge(a, b, w);
                all.add(new int[] {a, b, w});
                long[][] after = oracleTable(n, all);
                // The expected flag is whether any oracle cell strictly decreased.
                boolean want = false;
                for (int i = 0; i < n; i++)
                    for (int j = 0; j < n; j++) {
                        if (after[i][j] < before[i][j]) want = true;
                        long have = d.shortestPath(i, j);
                        if (have != (after[i][j] >= INF ? -1 : after[i][j])) throw new AssertionError("table " + i + "->" + j);
                    }
                if (got != want) throw new AssertionError("flag at step " + step);
            }
        }
    }
}
```

#### Solution: [Recognize] Update-Frequency Tradeoff (Author exercise)
<!-- id: dq39-update-frequency -->

**Approach.** The task is a chain of tests, each tied to a fact from the lesson. The table needs `n * n` cells, so a memory limit below that rules it out. On a dense graph one search costs about `n^2` and the build costs about `n^3`, so fewer than `n` queries never repay the build. When every update precedes the first query, or no update exists, one build serves all queries. Repair handles only edges that get cheaper or appear, so a removal forces a rebuild after each change. Everything else is the insert-only, online case that the incremental repair serves.

The first matching rule wins, so the order of the tests is part of the answer. The harness compares the picker with a second implementation that scores each rule in a table. It then backs the two key claims with real code. A repair after a cost increase gives a wrong distance that a rebuild corrects, and an insert-only stream of repairs matches a full rebuild. Counted relaxations confirm `n^3` for the build and `n^2` for one repair.

**Complexity.**

- **Time** is O(1), because the method evaluates at most five comparisons.
- **Space** is O(1), because it stores no collection.

```java run
import java.util.*;

public final class UpdateFrequency {
    /**
     * Picks a strategy name from the workload facts.
     * Time: O(1). Space: O(1).
     * Invariant: the first rule that matches decides, in the order memory, query count, batching, removals.
     */
    static String choose(int n, int u, int q, boolean removals, boolean batched, long memory) {
        // The table needs n * n cells; computing in long avoids overflow for any n.
        if ((long) n * n > memory) return "REPEATED_SEARCH";
        // Fewer than n queries never repay the n^3 build against n^2 per search.
        if (q < n) return "REPEATED_SEARCH";
        // One build serves all queries when updates come first or never come.
        if (batched || u == 0) return "REBUILD_ONCE";
        // Repair handles only cheaper or new edges, so removals need a rebuild per change.
        if (removals) return "REBUILD_EACH";
        // Insert-only and online: repair each insert in n^2.
        return "REPAIR_TABLE";
    }

    /** Second implementation: lists the rules as data and scans them in order. */
    static String oracle(int n, int u, int q, boolean removals, boolean batched, long memory) {
        String[] name = {"REPEATED_SEARCH", "REPEATED_SEARCH", "REBUILD_ONCE", "REBUILD_EACH", "REPAIR_TABLE"};
        boolean[] fires = {(long) n * n > memory, q < n, batched || u == 0, removals, true};
        for (int i = 0; i < fires.length; i++) if (fires[i]) return name[i];
        throw new AssertionError("unreachable");
    }

    static long relaxations; // counts inner-loop executions of the real code below

    /** Real Floyd-Warshall that counts its inner updates, to back the n^3 claim. */
    static long[][] floyd(int n, long[][] d) {
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
            relaxations++;
            d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        }
        return d;
    }

    /** Real incremental repair that counts its inner updates, to back the n^2 claim. */
    static void repair(int n, long[][] d, int a, int b, long w) {
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
            relaxations++;
            d[i][j] = Math.min(d[i][j], d[i][a] + w + d[b][j]);
        }
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2, including the first example's batched variant and the second example's removals variant.
        if (!choose(100, 10, 5, false, false, 1_000_000).equals("REPEATED_SEARCH")) throw new AssertionError("example 1");
        if (!choose(100, 1000, 100000, false, false, 1_000_000).equals("REPAIR_TABLE")) throw new AssertionError("example 2");
        // Checks each remaining name once.
        if (!choose(100, 1000, 100000, false, true, 1_000_000).equals("REBUILD_ONCE")) throw new AssertionError("batched");
        if (!choose(100, 1000, 100000, true, false, 1_000_000).equals("REBUILD_EACH")) throw new AssertionError("removals");
        if (!choose(300, 1000, 100000, false, false, 89_999).equals("REPEATED_SEARCH")) throw new AssertionError("memory");
        // Checks the boundary: memory exactly n * n allows the table.
        if (!choose(300, 1000, 100000, false, false, 90_000).equals("REPAIR_TABLE")) throw new AssertionError("memory edge");
        // Checks the picker against the rule-table oracle on random workloads.
        Random rnd = new Random(5);
        for (int t = 0; t < 20000; t++) {
            int n = 1 + rnd.nextInt(300), u = rnd.nextInt(3) == 0 ? 0 : rnd.nextInt(100001), q = rnd.nextInt(100001);
            long memory = rnd.nextInt(3) == 0 ? (long) n * n + rnd.nextInt(3) - 1 : rnd.nextInt(1_000_000_001);
            boolean removals = rnd.nextBoolean(), batched = rnd.nextBoolean();
            if (!choose(n, u, q, removals, batched, Math.max(0, memory)).equals(oracle(n, u, q, removals, batched, Math.max(0, memory))))
                throw new AssertionError("rule mismatch");
        }
        // Checks the counted work: n^3 for the build and n^2 per insert.
        int n = 9;
        long[][] d = new long[n][n];
        for (long[] row : d) Arrays.fill(row, Long.MAX_VALUE / 4);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        relaxations = 0;
        floyd(n, d);
        if (relaxations != (long) n * n * n) throw new AssertionError("n^3 build");
        relaxations = 0;
        repair(n, d, 1, 2, 4);
        if (relaxations != (long) n * n) throw new AssertionError("n^2 repair");
        // Checks that repair equals a full rebuild on an insert-only stream.
        for (int t = 0; t < 200; t++) {
            int k = 2 + rnd.nextInt(6);
            long[][] inc = new long[k][k], all = new long[k][k];
            for (int i = 0; i < k; i++) { Arrays.fill(inc[i], Long.MAX_VALUE / 4); Arrays.fill(all[i], Long.MAX_VALUE / 4); inc[i][i] = 0; all[i][i] = 0; }
            for (int s = 0; s < 8; s++) {
                int a = rnd.nextInt(k), b = rnd.nextInt(k), w = rnd.nextInt(10);
                repair(k, inc, a, b, w);
                inc[a][b] = Math.min(inc[a][b], w);
                all[a][b] = Math.min(all[a][b], w);
                long[][] copy = new long[k][];
                for (int i = 0; i < k; i++) copy[i] = all[i].clone();
                floyd(k, copy);
                if (!Arrays.deepEquals(copy, inc)) throw new AssertionError("repair differs from rebuild");
                all = copy;
            }
        }
        // Checks that repair after a cost increase is wrong: edge 0->1 costs 1, then rises to 5.
        long[][] g = new long[2][2];
        for (long[] row : g) Arrays.fill(row, Long.MAX_VALUE / 4);
        g[0][0] = g[1][1] = 0;
        repair(2, g, 0, 1, 1);
        // The repair formula takes a minimum, so a raised cost of 5 cannot raise the stored 1.
        repair(2, g, 0, 1, 5);
        if (g[0][1] != 1) throw new AssertionError("stale value expected");
        long[][] fresh = new long[2][2];
        for (long[] row : fresh) Arrays.fill(row, Long.MAX_VALUE / 4);
        fresh[0][0] = fresh[1][1] = 0;
        fresh[0][1] = 5;
        floyd(2, fresh);
        if (fresh[0][1] != 5 || g[0][1] == fresh[0][1]) throw new AssertionError("rebuild must differ");
    }
}
```
