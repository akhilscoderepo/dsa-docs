<!-- lesson-kind: standard -->
<!-- lesson-id: dynamic-graph-queries -->
## Dynamic Graph Queries

<!-- stage: context -->
### Why Quoted Delivery Costs Go Stale

A logistics service quotes the cheapest delivery cost between two depots. Dispatchers also add new routes during the day, and a route can open a shortcut that makes an earlier quote too high. If the service caches quotes, a customer sees a price that no longer matches the network. If the service recomputes every quote from nothing, a busy morning of lookups slows the whole system.

Both problems come from one object that owns two jobs. It accepts new edges, and it answers shortest-path questions about the edges accepted so far. This lesson asks how such an object keeps every answer correct after each new edge without paying the full price on every call. The answer depends on how many edges arrive compared with how many questions arrive.

<!-- stage: naive -->
### Running Dijkstra On Every Query

The direct design stores the edges in adjacency lists and runs Dijkstra from the source on every question. An added edge only appends to a list, so it costs O(1) and leaves no stale state. A query always sees every accepted edge, because it reads the lists at that moment.

```java
static long shortestPath(java.util.List<long[]>[] adj, int from, int to) {
    long[] dist = new long[adj.length];
    java.util.Arrays.fill(dist, Long.MAX_VALUE);          // Long.MAX_VALUE marks unreached nodes
    dist[from] = 0;
    java.util.PriorityQueue<long[]> pq =
        new java.util.PriorityQueue<>((x, y) -> Long.compare(x[0], y[0])); // compare, never subtract
    pq.add(new long[] {0, from});
    while (!pq.isEmpty()) {
        long[] top = pq.poll();
        int u = (int) top[1];
        if (top[0] > dist[u]) continue;                   // skip an outdated queue entry
        for (long[] e : adj[u]) {                         // e = {neighbor, cost}
            int v = (int) e[0];
            if (dist[u] + e[1] < dist[v]) {
                dist[v] = dist[u] + e[1];
                pq.add(new long[] {dist[v], v});
            }
        }
    }
    return dist[to] == Long.MAX_VALUE ? -1 : dist[to];
}
```

This is correct for any mix of calls. Each query pays for one full search.

<!-- stage: bottleneck -->
### Paying A Full Search Per Question

```predict
A network has 100 nodes and about 9,900 edges, and the service answers 100,000 queries. How many edge examinations does the repeated search perform, roughly?

About one billion. Each query examines every edge reachable from the source, so 100,000 queries times about 10,000 edges gives 10^9 examinations, and the heap adds a logarithmic factor on top.
```

One search costs O((V + E) log V) for V nodes and E edges. A workload with Q queries therefore costs O(Q * (V + E) log V). On a dense graph, E is close to V squared, so each query costs about V squared times a logarithm, even when the query repeats a pair that the service already answered a moment ago.

The repeated work is the bottleneck. Between two queries only a few edges change, yet the search forgets everything it learned. Rebuilding a table of all pairs from scratch after every edge is no better. Floyd-Warshall costs O(V^3), so one rebuild per added edge costs O(V^3) per edge and wastes the old table.

<!-- stage: insight -->
### Keep All Pairs And Repair On Insert

#### Store Every Pair Once

Keep one **distance matrix** `dist` where `dist[i][j]` holds the cheapest known cost from `i` to `j`. Fill it once with Floyd-Warshall in O(V^3). A query then reads one cell in O(1). The matrix holds the invariant that each cell equals the true shortest cost over all edges accepted so far.

#### Repair With One Edge

A new edge `a -> b` with cost `w` can improve a pair `(i, j)` only by using that edge exactly once. The cheapest such route is `dist[i][a] + w + dist[b][j]`. This update is **incremental relaxation**: replace `dist[i][j]` by the smaller of its old value and that sum, for every pair. The loop touches V squared cells, so an insertion costs O(V^2) and the invariant holds again. One pass suffices because a shortest path never needs to cross the same new edge twice when costs are not negative.

#### Compare By The Update-To-Query Ratio

The **update-to-query ratio** decides which design wins. Dijkstra per query costs nothing on insert and a full search per question. The matrix costs O(V^3) once, O(V^2) per insert and O(1) per query. With few queries, the search wins because it never builds the table. With many queries, the matrix wins. Whether the calls are known in advance also matters: when all inserts precede all queries, one Floyd-Warshall rebuild replaces every repair.

<!-- names: distance matrix, incremental relaxation, update-to-query ratio -->

<!-- stage: variables -->
### Name The State And The Workload

Four quantities control the design, and each needs a fixed meaning before any comparison.

- **`dist[i][j]`** is a `long` holding the cheapest known cost from `i` to `j`, or `INF` when no path exists.
- **`INF`** is `Long.MAX_VALUE / 4`, so the sum of two `INF` values and one cost never overflows.
- **`a`, `b`, `w`** are the source, target and non-negative cost of the inserted edge.
- **`U` and `Q`** are the numbers of inserts and queries, and they fix the update-to-query ratio.

A query returns -1 when `dist[from][to]` is still `INF`. The diagonal `dist[i][i]` starts at 0.

<!-- stage: trace -->
### Follow Edge Insertions Through Queries

The first trace uses four nodes with edges 0 to 1 at cost 5, 1 to 2 at cost 4 and 2 to 3 at cost 1. The cells are the nodes, and each step shows the distances from node 0 to every node, with `INF` for unreachable nodes. The first query from 0 to 3 reads the table and returns 10. Inserting edge 0 to 2 at cost 6 gives route 0, 2, 3 with cost 6 + 1 = 7, so the repair lowers `dist[0][2]` from 9 to 6 and `dist[0][3]` from 10 to 7. The next query returns 7. Inserting edge 0 to 3 at cost 9 offers a route costlier than 7, so the repair changes no cell.

```trace
{"cells":["0","1","2","3"],"pointers":["a","b"],"steps":[{"at":{"a":0,"b":3},"vars":{"row0":"0,5,9,10","result":"10"},"note":"query(0, 3) reads dist[0][3] and returns 10."},{"at":{"a":0,"b":2},"vars":{"row0":"0,5,6,7","changed":"2"},"note":"addEdge(0, 2, 6) repairs every pair and lowers 2 cells."},{"at":{"a":0,"b":3},"vars":{"row0":"0,5,6,7","result":"7"},"note":"query(0, 3) reads dist[0][3] and returns 7."},{"at":{"a":0,"b":3},"vars":{"row0":"0,5,6,7","changed":"0"},"note":"addEdge(0, 3, 9) offers no cheaper route, so the repair changes no cell."},{"at":{"a":0,"b":3},"vars":{"row0":"0,5,6,7","result":"7"},"note":"query(0, 3) reads dist[0][3] and returns 7."}]}
```

The second trace uses three nodes with a single edge 0 to 1 at cost 3. A query from 0 to 2 returns -1 because no path exists. Inserting edge 1 to 2 at cost 2 creates the path with cost 5. A second edge between the same pair at cost 7 is a duplicate that costs more, so nothing changes. An edge 0 to 2 at cost 5 ties the stored value, and the strict comparison leaves it alone. A final edge 0 to 2 at cost 4 improves the pair.

```trace
{"cells":["0","1","2"],"pointers":["a","b"],"steps":[{"at":{"a":0,"b":2},"vars":{"row0":"0,3,INF","result":"-1"},"note":"query(0, 2) reads dist[0][2] and returns -1."},{"at":{"a":1,"b":2},"vars":{"row0":"0,3,5","changed":"2"},"note":"addEdge(1, 2, 2) repairs every pair and lowers 2 cells."},{"at":{"a":0,"b":2},"vars":{"row0":"0,3,5","result":"5"},"note":"query(0, 2) reads dist[0][2] and returns 5."},{"at":{"a":1,"b":2},"vars":{"row0":"0,3,5","changed":"0"},"note":"addEdge(1, 2, 7) offers no cheaper route, so the repair changes no cell."},{"at":{"a":0,"b":2},"vars":{"row0":"0,3,5","changed":"0"},"note":"addEdge(0, 2, 5) offers no cheaper route, so the repair changes no cell."},{"at":{"a":0,"b":2},"vars":{"row0":"0,3,4","changed":"1"},"note":"addEdge(0, 2, 4) repairs every pair and lowers 1 cells."},{"at":{"a":0,"b":2},"vars":{"row0":"0,3,4","result":"4"},"note":"query(0, 2) reads dist[0][2] and returns 4."}]}
```

<!-- stage: code -->
### Build The Table And Repair It

```java
final class GraphIndex {
    private static final long INF = Long.MAX_VALUE / 4;
    private final int n;
    private final long[][] dist;

    GraphIndex(int n, int[][] edges) {
        this.n = n;
        dist = new long[n][n];
        for (long[] row : dist) java.util.Arrays.fill(row, INF);   // no path known yet
        for (int i = 0; i < n; i++) dist[i][i] = 0;                // a node reaches itself for free
        for (int[] e : edges) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);
        for (int k = 0; k < n; k++)                                // allow k as an intermediate node
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
    }

    void addEdge(int a, int b, long w) {
        for (int i = 0; i < n; i++)                                // every source that reaches a
            for (int j = 0; j < n; j++)                            // every target reachable from b
                dist[i][j] = Math.min(dist[i][j], dist[i][a] + w + dist[b][j]);
    }

    long query(int from, int to) {
        return dist[from][to] >= INF ? -1 : dist[from][to];
    }
}
```

The constructor costs O(n^3) and each `addEdge` costs O(n^2). The array uses `long`, and `INF` leaves room for two additions without overflow. The result of an unreachable query is -1 and the stored `INF` never leaves the class.

<!-- stage: applicability -->
### Choose A Design From The Workload

#### State The Invariant First

Every returned distance must reflect all accepted edges, so the invariant belongs to the object and not to one method. The constructor, the insert and the query all preserve it. A design is acceptable only if each public call leaves the stored table consistent with the accepted edges.

#### Pick By Counting Calls

Use repeated search when queries are rare, when the graph is sparse or when the node count is large. The table needs V squared longs, which is too much memory for a large graph. Use the table with incremental repair when both inserts and queries are frequent and V is small, as in a limit of a few hundred nodes. Use one rebuild when every insert is known before the first query.

#### Watch The False Friend

Re-running Floyd-Warshall after each insert looks safe and is a false friend, because it recomputes what the old table already knows and costs O(V^3) per insert. A second false friend is repair with removals. The repair formula handles only edges that get cheaper or appear, so deleting an edge or raising a cost forces a rebuild. Negative costs also break the single-crossing argument.

<!-- stage: exercises -->
### Exercises

#### [Build] Static Shortest-Path Calculator (Author exercise)
<!-- id: dq39-static-calculator -->

**Prerequisites.** Dijkstra and Floyd-Warshall from the shortest-path chapter.

**Problem.** A directed graph has `n` nodes numbered `0` to `n - 1` and a list of weighted edges. Each edge is a triple `{from, to, cost}`. Build a calculator once from the edge list. Then answer queries `distance(a, b)`, which returns the minimum total cost of a directed path from `a` to `b`, or `-1` when no path exists. The graph never changes after construction. The workload has zero updates and many queries, and all edges are known in advance.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 100`.
- **Edges** number at most `n * (n - 1)`, with `0 <= cost <= 10^6`, and repeated pairs are allowed.
- **Queries** number at most `10^5`, and `a` may equal `b`, which returns `0`.
- **Return value** is a `long`.

**Example 1.** Input `n = 4`, edges `{0,1,5}, {1,2,4}, {2,3,1}` and query `distance(0, 3)`, output 10.

**Example 2.** Input the same graph and query `distance(3, 0)`, output -1.

**Hint.** With many queries and no updates, which one-time table makes each query O(1)?

**Changed decision.** Nothing mutates, so the calculator may spend O(n^3) once and answer from a table.

#### [Vary] Graph With Shortest Path Calculator (LeetCode 2642)
<!-- id: dq39-add-edge-calculator -->

**Prerequisites.** The static calculator exercise above.

**Problem.** Design a graph object that is built from `n` and an initial edge list. It supports `addEdge(a, b, w)`, which inserts a directed edge, and `shortestPath(a, b)`, which returns the minimum path cost over all edges inserted so far, or `-1` when none exists. Calls arrive one at a time, in unknown order, so the object cannot see the future. The update-to-query ratio is about one to one.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 100`, and every edge cost is an `int` with `1 <= w <= 10^6`.
- **`addEdge`** is never called for a pair that already has an edge.
- **Calls** number at most `100` of each kind.
- **Return value** is a `long`.

**Example 1.** Input `n = 4`, edges `{0,1,5}, {1,2,4}, {2,3,1}`, then `shortestPath(0, 3)`, `addEdge(0, 2, 6)`, `shortestPath(0, 3)`, output 10 and then 7.

**Example 2.** Input the same graph after `addEdge(0, 2, 6)`, then `addEdge(0, 3, 9)` and `shortestPath(0, 3)`, output 7.

**Hint.** Which cells can an edge `a -> b` improve, and by what sum?

**Changed decision.** Edges now arrive between queries, so the table must be repaired on insert and not only built once.

#### [Boundary] Duplicate And Dominated Edges (Author exercise)
<!-- id: dq39-dominated-edges -->

**Prerequisites.** The add-edge calculator exercise above.

**Problem.** Extend the graph object so that `addEdge(a, b, w)` may repeat an existing pair, add a self-loop `a == b` or add an edge that no shortest path uses. The method returns `true` exactly when at least one pair distance becomes strictly smaller, and `false` otherwise. Queries return the minimum path cost as before, or `-1`. The object must keep only the minimum useful cost, so a dominated edge never raises any distance. Calls arrive online, and the update-to-query ratio is about two to one.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 60`, and every cost `w` is an `int` with `0 <= w <= 10^6`.
- **Pairs** may repeat, and zero-cost edges are allowed.
- **Calls** number at most `200` of each kind.
- **Return value** is `boolean` for `addEdge` and `long` for queries.

**Example 1.** Input `n = 3`, no edges, then `addEdge(0, 1, 3)`, `addEdge(0, 1, 7)`, `addEdge(0, 1, 3)`, output true, false, false.

**Example 2.** Input the same graph, then `addEdge(1, 2, 2)`, `shortestPath(0, 2)`, `addEdge(1, 1, 0)`, `addEdge(0, 2, 4)`, output true, 5, false, true.

**Hint.** If the new edge does not beat the current `dist[a][b]`, can any other pair improve through it?

**Changed decision.** The insert must detect that it changes nothing, and equal or larger costs must leave every cell untouched.

#### [Recognize] Update-Frequency Tradeoff (Author exercise)
<!-- id: dq39-update-frequency -->

**Prerequisites.** The three exercises above.

**Problem.** A workload has `n` nodes, `m` initial edges, `U` edge insertions, `Q` queries, and a flag `batched` that is true when every insertion is known before the first query. Compare three strategies by operation count. `DIJKSTRA` costs `Q * (m + U + n) * L`, where `L` is the number of bits in `n`. `FLOYD_REBUILD` costs `n^3 * (batched ? 1 : 1 + U) + Q`. `FLOYD_INCREMENTAL` costs `n^3 + U * n^2 + Q`. Return the name of the cheapest strategy. On a tie, prefer the earlier name in the order listed.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 300`, and `0 <= m <= n * (n - 1)`.
- **`U` and `Q`** are `int` values with `0 <= U, Q <= 10^5`.
- **Costs** need `long` arithmetic.
- **Return value** is one of the three names.

**Example 1.** Input `n = 100, m = 300, U = 10, Q = 5, batched = false`, output `DIJKSTRA`.

**Example 2.** Input `n = 100, m = 300, U = 1000, Q = 100000, batched = false`, output `FLOYD_INCREMENTAL`.

**Hint.** Which strategy has the cheapest insert, and which has the cheapest query?

**Changed decision.** The choice is now driven by the counts of calls, so the update-to-query ratio and the batching flag select the strategy.
