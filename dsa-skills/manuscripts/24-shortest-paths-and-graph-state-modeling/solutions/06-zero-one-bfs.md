<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Zero And One Costs

#### Solution: [Build] Choose Deque End By Weight (Author exercise)
<!-- id: sp-zero-one-end -->

**Approach.**
The method builds the adjacency list in the order of `edges`, so the scan order is fixed. It keeps a distance array and a deque of pairs. The loop removes the front pair and skips it when its distance exceeds the stored one. Otherwise it appends the vertex to the result and scans the edges of that vertex. A strictly smaller sum is stored, and the new pair goes to the front for a zero edge and to the back for a one edge.

The invariant is that the distances in the deque never decrease from front to back and differ by at most 1. A zero push at the front stores the value of the removed entry, which is no larger than any remaining entry. A one push at the back stores that value plus 1, which is no smaller than any remaining entry. A vertex that is not skipped therefore carries its final distance, so the result lists each reachable vertex once.

**Complexity.**
- **Time** is O(V + E), because each vertex enters the deque at most twice and each edge is scanned at most twice.
- **Space** is O(V + E) for the adjacency list, the distance array and at most 2V deque entries.

```java run
import java.util.*;

public final class ZeroOneEnd {
    /**
     * Returns the vertices in the order in which the search records them.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: deque distances never decrease from front to back and span at most two values.
     */
    static int[] order(int n, int[][] edges) {
        return run(n, edges, new int[n]);
    }

    private static int[] run(int n, int[][] edges, int[] pushes) {
        // Build the adjacency list in edge order, which costs O(V + E).
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        // Every vertex starts unreached, except the start with distance 0.
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<int[]> deque = new ArrayDeque<>();
        deque.addLast(new int[] {0, 0});
        pushes[0]++;
        int[] out = new int[n];
        int count = 0;
        // Each iteration removes one entry, and at most 2V entries are ever added.
        while (!deque.isEmpty()) {
            int[] top = deque.pollFirst();
            int cur = top[0];
            // An entry with a larger distance than the stored one is superseded.
            if (top[1] > dist[cur]) continue;
            out[count++] = cur;
            // Each adjacency entry is scanned once per recorded vertex.
            for (int[] edge : adj.get(cur)) {
                int next = edge[0];
                int cand = top[1] + edge[1];
                // Only a strict improvement is stored, which also stops zero-cost cycles.
                if (cand < dist[next]) {
                    dist[next] = cand;
                    pushes[next]++;
                    // The cost picks the end: zero goes in front of larger entries, one goes behind them.
                    if (edge[1] == 0) deque.addFirst(new int[] {next, cand});
                    else deque.addLast(new int[] {next, cand});
                }
            }
        }
        return Arrays.copyOf(out, count);
    }

    /** Oracle: Bellman-Ford distances, with -1 for unreachable vertices. */
    static int[] bellman(int n, int[][] edges) {
        int inf = Integer.MAX_VALUE;
        int[] d = new int[n];
        Arrays.fill(d, inf);
        d[0] = 0;
        for (int round = 0; round <= n; round++) {
            for (int[] e : edges) if (d[e[0]] != inf && d[e[0]] + e[2] < d[e[1]]) d[e[1]] = d[e[0]] + e[2];
        }
        for (int v = 0; v < n; v++) if (d[v] == inf) d[v] = -1;
        return d;
    }

    /** Oracle: the same rule on a LinkedList that stores vertex ids only and a done flag. */
    static int[] reference(int n, int[][] edges) {
        int[] best = new int[n];
        Arrays.fill(best, Integer.MAX_VALUE);
        best[0] = 0;
        boolean[] done = new boolean[n];
        LinkedList<Integer> list = new LinkedList<>();
        list.add(0);
        List<Integer> out = new ArrayList<>();
        while (!list.isEmpty()) {
            int u = list.removeFirst();
            if (done[u]) continue;
            done[u] = true;
            out.add(u);
            for (int[] e : edges) {
                if (e[0] != u || best[u] + e[2] >= best[e[1]]) continue;
                best[e[1]] = best[u] + e[2];
                if (e[2] == 0) list.addFirst(e[1]);
                else list.addLast(e[1]);
            }
        }
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(order(5, new int[][] {{0, 1, 1}, {0, 2, 0}, {2, 3, 0}, {3, 1, 0}, {1, 4, 1}}), new int[] {0, 2, 3, 1, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(order(4, new int[][] {{0, 1, 1}, {0, 2, 1}, {1, 3, 1}}), new int[] {0, 1, 2, 3})) throw new AssertionError("ex2");
        // Java facts: push adds at the front and add adds at the back of an ArrayDeque.
        ArrayDeque<Integer> probe = new ArrayDeque<>();
        probe.add(1);
        probe.push(2);
        probe.add(3);
        if (probe.peekFirst() != 2 || probe.peekLast() != 3) throw new AssertionError("push and add ends");
        // Random graphs with repeats, self loops and zero-cost cycles.
        Random rnd = new Random(2406);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(17);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int[] pushes = new int[n];
            int[] got = run(n, edges, pushes);
            // The order matches the vertex-id reference.
            if (!Arrays.equals(got, reference(n, edges))) throw new AssertionError("reference " + t);
            // The recorded vertices are exactly the reachable ones, each once, in nondecreasing true distance.
            int[] truth = bellman(n, edges);
            int reachable = 0;
            for (int v = 0; v < n; v++) if (truth[v] >= 0) reachable++;
            if (got.length != reachable) throw new AssertionError("count " + t);
            boolean[] seen = new boolean[n];
            int prev = 0;
            for (int v : got) {
                if (seen[v] || truth[v] < prev) throw new AssertionError("order " + t);
                seen[v] = true;
                prev = truth[v];
            }
            // Each vertex enters the deque at most twice.
            for (int v = 0; v < n; v++) if (pushes[v] > 2) throw new AssertionError("pushes " + t);
        }
    }
}
```

#### Solution: [Vary] Reject Nonimproving Relaxations (Author exercise)
<!-- id: sp-reject-nonimproving -->

**Approach.**
The method keeps the search of the previous solution and returns the distance array. A sum is stored and pushed only when it is strictly smaller than the stored value, so a visited flag is never needed. A vertex can be pushed at the back with distance `d + 1` and later at the front with `d`. When the old entry is removed, its distance exceeds the stored one and the method skips it.

The invariant is that `dist[v]` equals the cost of some real path to `v` at every moment, and it equals the minimum when the last entry of `v` is removed. Entries leave in nondecreasing order, so no later entry can offer a smaller sum than the one that fixed the value. Unreached entries convert to -1 at the end.

**Complexity.**
- **Time** is O(V + E), because the deque takes at most two entries per vertex and each edge is scanned at most twice.
- **Space** is O(V + E) for the adjacency list, the array and the deque.

```java run
import java.util.*;

public final class RejectNonimproving {
    /**
     * Returns the cheapest cost from vertex 0 to every vertex, with -1 when unreachable.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: dist[v] is the cost of a real path and entries leave the deque in nondecreasing order.
     */
    static int[] dist(int n, int[][] edges) {
        // Adjacency list in edge order.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        // The unreached value is the largest int, and no sum is ever formed from it.
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<int[]> deque = new ArrayDeque<>();
        deque.addLast(new int[] {0, 0});
        // Each removal is one entry, and each vertex has at most two entries.
        while (!deque.isEmpty()) {
            int[] top = deque.pollFirst();
            int cur = top[0];
            // A superseded entry carries a larger distance than the stored one.
            if (top[1] > dist[cur]) continue;
            // Each edge is scanned once per live removal of its start vertex.
            for (int[] edge : adj.get(cur)) {
                int next = edge[0];
                int cand = top[1] + edge[1];
                // A strict comparison rejects equal and larger sums.
                if (cand < dist[next]) {
                    dist[next] = cand;
                    // Zero edges go to the front and one edges go to the back.
                    if (edge[1] == 0) deque.addFirst(new int[] {next, cand});
                    else deque.addLast(new int[] {next, cand});
                }
            }
        }
        // Translate the unreached value into the return convention.
        for (int v = 0; v < n; v++) if (dist[v] == Integer.MAX_VALUE) dist[v] = -1;
        return dist;
    }

    /** Oracle: Bellman-Ford rounds over the edge list. */
    static int[] bellman(int n, int[][] edges) {
        long inf = Long.MAX_VALUE / 4;
        long[] d = new long[n];
        Arrays.fill(d, inf);
        d[0] = 0;
        for (int round = 0; round <= n; round++) {
            for (int[] e : edges) if (d[e[0]] + e[2] < d[e[1]]) d[e[1]] = d[e[0]] + e[2];
        }
        int[] r = new int[n];
        for (int v = 0; v < n; v++) r[v] = d[v] >= inf ? -1 : (int) d[v];
        return r;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(dist(5, new int[][] {{0, 1, 1}, {0, 2, 0}, {2, 3, 0}, {3, 1, 0}, {1, 4, 1}}), new int[] {0, 0, 0, 0, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(dist(4, new int[][] {{0, 1, 1}, {2, 3, 0}}), new int[] {0, 1, -1, -1})) throw new AssertionError("ex2");
        // A visited flag would keep distance 1 for vertex 1; the strict comparison lowers it to 0.
        if (dist(4, new int[][] {{0, 1, 1}, {0, 2, 0}, {2, 3, 0}, {3, 1, 0}})[1] != 0) throw new AssertionError("flag trap");
        // Random graphs against Bellman-Ford.
        Random rnd = new Random(2416);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(9);
            int m = rnd.nextInt(20);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            if (!Arrays.equals(dist(n, edges), bellman(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Zero-Cost Cycle (Author exercise)
<!-- id: sp-zero-cost-cycle -->

**Approach.**
The method runs the deque search and then reads two values from the final array: the number of zero entries and the last entry. A zero-cost cycle would make a search without a strict test push the same vertices forever, because each lap produces a sum equal to the stored value. The strict test `cand < dist[next]` rejects that sum, so every lap beyond the first pushes nothing and the loop ends.

The invariant is that every push lowers one `dist` entry by at least 1, and `dist` starts at the largest int. A vertex receives at most two distinct finite values over the run, so pushes are bounded by 2V and the loop terminates on every input. A self loop of cost 0 gives a sum equal to the stored value and is rejected at once.

**Complexity.**
- **Time** is O(V + E), because the push bound is 2V and each edge is scanned at most twice.
- **Space** is O(V + E) for the adjacency list, the array and the deque.

```java run
import java.util.*;

public final class ZeroCostCycle {
    /**
     * Returns {number of vertices at distance 0, distance of the last vertex or -1}.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: every push lowers one distance strictly, so zero-cost cycles cannot loop.
     */
    static int[] summary(int n, int[][] edges) {
        // Adjacency list in edge order.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<int[]> deque = new ArrayDeque<>();
        deque.addLast(new int[] {0, 0});
        // The loop ends because the number of pushes is bounded by 2V.
        while (!deque.isEmpty()) {
            int[] top = deque.pollFirst();
            int cur = top[0];
            // Skip an entry that a cheaper entry superseded.
            if (top[1] > dist[cur]) continue;
            // One scan of the adjacency entries of this vertex.
            for (int[] edge : adj.get(cur)) {
                int cand = top[1] + edge[1];
                // Equal sums, including those along a zero-cost cycle, are rejected here.
                if (cand < dist[edge[0]]) {
                    dist[edge[0]] = cand;
                    if (edge[1] == 0) deque.addFirst(new int[] {edge[0], cand});
                    else deque.addLast(new int[] {edge[0], cand});
                }
            }
        }
        // Count the zero entries over the final array.
        int zeros = 0;
        for (int v = 0; v < n; v++) if (dist[v] == 0) zeros++;
        // The last vertex is unreachable when it keeps the unreached value.
        return new int[] {zeros, dist[n - 1] == Integer.MAX_VALUE ? -1 : dist[n - 1]};
    }

    /** Oracle: Bellman-Ford rounds, then the same two reads. */
    static int[] oracle(int n, int[][] edges) {
        long inf = Long.MAX_VALUE / 4;
        long[] d = new long[n];
        Arrays.fill(d, inf);
        d[0] = 0;
        for (int round = 0; round <= n; round++) {
            for (int[] e : edges) if (d[e[0]] + e[2] < d[e[1]]) d[e[1]] = d[e[0]] + e[2];
        }
        int zeros = 0;
        for (int v = 0; v < n; v++) if (d[v] == 0) zeros++;
        return new int[] {zeros, d[n - 1] >= inf ? -1 : (int) d[n - 1]};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(summary(4, new int[][] {{0, 1, 0}, {1, 0, 0}, {1, 2, 1}, {2, 3, 0}, {3, 2, 0}}), new int[] {2, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(summary(3, new int[][] {{0, 0, 0}, {0, 1, 1}, {1, 1, 0}}), new int[] {1, -1})) throw new AssertionError("ex2");
        // A single vertex gives zero entries counted once and distance 0.
        if (!Arrays.equals(summary(1, new int[0][]), new int[] {1, 0})) throw new AssertionError("single");
        // Graphs dense with zero-cost edges so that cycles are common.
        Random rnd = new Random(2426);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(18);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(4) == 0 ? 1 : 0};
            if (!Arrays.equals(summary(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Cost To Make A Valid Path In A Grid (LeetCode 1368)
<!-- id: sp-grid-valid-path -->

**Approach.**
Each cell is a vertex with index `r * n + c`, and each of the four moves is an edge. The edge cost is 0 when the move direction equals the code of the start cell minus 1, and 1 otherwise. All costs are 0 or 1, so the deque search applies. The loop removes the front entry, skips it when it is superseded, and pushes each neighbor with a strictly smaller cost at the front for a free move and at the back for a paid move.

The invariant is the same as in the graph version: the deque distances never decrease from front to back and span at most two values. The edge costs are computed on the fly, so no adjacency list is built. The answer is the stored distance of the last cell.

**Complexity.**
- **Time** is O(m n), because each cell enters the deque at most twice and scans four moves each time.
- **Space** is O(m n) for the distance array and the deque.

```java run
import java.util.*;

public final class GridValidPath {
    private static final int[][] MOVES = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    /**
     * Returns the minimum cost of a path from the top-left to the bottom-right cell.
     * Time: O(m n). Space: O(m n).
     * Invariant: deque distances never decrease from front to back and span at most two values.
     */
    static int minCost(int[][] grid) {
        int m = grid.length;
        int n = grid[0].length;
        // One distance per cell, with the largest int as the unreached value.
        int[] dist = new int[m * n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<int[]> deque = new ArrayDeque<>();
        deque.addLast(new int[] {0, 0});
        // Each removal handles one entry, and each cell has at most two entries.
        while (!deque.isEmpty()) {
            int[] top = deque.pollFirst();
            int r = top[0] / n;
            int c = top[0] % n;
            // A superseded entry carries a larger distance than the stored one.
            if (top[1] > dist[top[0]]) continue;
            // Four moves per cell give the constant factor of the O(m n) bound.
            for (int k = 0; k < 4; k++) {
                int nr = r + MOVES[k][0];
                int nc = c + MOVES[k][1];
                // Moves that leave the grid do not exist.
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
                // Following the arrow is free, and any other direction costs one change.
                int w = grid[r][c] == k + 1 ? 0 : 1;
                int cand = top[1] + w;
                int id = nr * n + nc;
                // Store only a strictly smaller cost, then pick the deque end from the weight.
                if (cand < dist[id]) {
                    dist[id] = cand;
                    if (w == 0) deque.addFirst(new int[] {id, cand});
                    else deque.addLast(new int[] {id, cand});
                }
            }
        }
        // The last cell is always reachable because every move direction is allowed.
        return dist[m * n - 1];
    }

    /** Oracle: Dijkstra with a PriorityQueue of {distance, cell}. */
    static int oracle(int[][] grid) {
        int m = grid.length;
        int n = grid[0].length;
        int[] best = new int[m * n];
        Arrays.fill(best, Integer.MAX_VALUE);
        best[0] = 0;
        PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        heap.add(new int[] {0, 0});
        while (!heap.isEmpty()) {
            int[] top = heap.poll();
            if (top[0] > best[top[1]]) continue;
            int r = top[1] / n;
            int c = top[1] % n;
            for (int k = 0; k < 4; k++) {
                int nr = r + MOVES[k][0];
                int nc = c + MOVES[k][1];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
                int cand = top[0] + (grid[r][c] == k + 1 ? 0 : 1);
                if (cand < best[nr * n + nc]) {
                    best[nr * n + nc] = cand;
                    heap.add(new int[] {cand, nr * n + nc});
                }
            }
        }
        return best[m * n - 1];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minCost(new int[][] {{3, 3, 2}, {1, 4, 4}, {2, 1, 1}}) != 1) throw new AssertionError("ex1");
        if (minCost(new int[][] {{4, 4}, {4, 4}}) != 2) throw new AssertionError("ex2");
        // A single cell needs no move.
        if (minCost(new int[][] {{2}}) != 0) throw new AssertionError("single cell");
        // Random grids against Dijkstra.
        Random rnd = new Random(2436);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(5);
            int n = 1 + rnd.nextInt(5);
            int[][] grid = new int[m][n];
            for (int[] row : grid) for (int j = 0; j < n; j++) row[j] = 1 + rnd.nextInt(4);
            if (minCost(grid) != oracle(grid)) throw new AssertionError("random " + t);
        }
    }
}
```
