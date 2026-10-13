<!-- solutions-for: 92-a-star-heuristics -->
### Solutions For A-Star Heuristics

#### Solution: [Build] Zero-Heuristic Search (Author exercise)
<!-- id: ah35-zero-heuristic-order -->

**Approach.**
With a zero guess, the priority `f` equals the cost so far `g`, so the search is Dijkstra's algorithm. The queue entry holds the cost and the vertex id, and the comparator orders by cost and then by id. A pop is stale when its cost is larger than the recorded cost, and the method skips it. Every other pop finalizes its vertex, so the method appends the vertex to the result. If the vertex is the goal, the method returns the result. Because weights are non-negative, an entry with the smallest cost cannot be improved later, so a non-stale pop carries the final cost. When the queue empties first, the goal is unreachable and the result lists the reachable vertices. The invariant is that finalized vertices have final costs and appear in non-decreasing cost order.

The program compares the order with an array-based Dijkstra that scans for the unfinalized vertex with the smallest pair (cost, id), a different structure from the queue. It uses random graphs with zero weights and unreachable goals.

**Complexity.**
- **Time** is O((V + E) log V), because each edge can push one entry.
- **Space** is O(V + E) for the adjacency lists and the queue.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class ZeroHeuristicOrderBuild {
    /**
     * Returns the vertices in finalization order, ending with the goal when it is reachable.
     * Time: O((V + E) log V). Space: O(V + E).
     * Invariant: finalized vertices carry final costs and appear in non-decreasing cost order.
     */
    static int[] finalizeOrder(int n, int[][] edges, int start, int goal) {
        List<int[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) adj[e[0]].add(new int[]{e[1], e[2]});
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Long.compare(x[0], y[0]) : Long.compare(x[1], y[1]));
        best[start] = 0;
        pq.add(new long[]{0, start});
        List<Integer> order = new ArrayList<>();
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            int u = (int) cur[1];
            if (cur[0] > best[u]) continue; // stale entry
            order.add(u); // non-stale pop finalizes u
            if (u == goal) break;
            for (int[] nb : adj[u]) {
                long g = cur[0] + nb[1];
                if (g < best[nb[0]]) { best[nb[0]] = g; pq.add(new long[]{g, nb[0]}); }
            }
        }
        return order.stream().mapToInt(Integer::intValue).toArray();
    }

    static int[] oracle(int n, int[][] edges, int start, int goal) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        boolean[] done = new boolean[n];
        dist[start] = 0;
        List<Integer> order = new ArrayList<>();
        while (true) {
            int u = -1;
            for (int v = 0; v < n; v++) if (!done[v] && dist[v] != Long.MAX_VALUE && (u == -1 || dist[v] < dist[u])) u = v; // smallest (cost, id)
            if (u == -1) break;
            done[u] = true;
            order.add(u);
            if (u == goal) break;
            for (int[] e : edges) if (e[0] == u && dist[u] + e[2] < dist[e[1]]) dist[e[1]] = dist[u] + e[2];
        }
        return order.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        int[][] e1 = {{0,1,2},{0,2,1},{1,3,1},{2,3,4},{2,4,1},{4,3,1},{3,5,2}};
        if (!Arrays.equals(finalizeOrder(6, e1, 0, 5), new int[]{0, 2, 1, 4, 3, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(finalizeOrder(3, new int[][]{{0,1,1}}, 0, 2), new int[]{0, 1})) throw new AssertionError("ex2");
        // random graphs with zero weights and unreachable goals
        Random rnd = new Random(91);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[]{rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(5)};
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            if (!Arrays.equals(finalizeOrder(n, edges, s, g), oracle(n, edges, s, g))) throw new AssertionError("random " + Arrays.deepToString(edges));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Manhattan Grid Search (Author exercise)
<!-- id: ah35-manhattan-graph-search -->

**Approach.**
The guess of a vertex is the Manhattan distance from its position to the goal's position. Every edge weight is at least the Manhattan distance between its endpoints, so the guess cannot exceed the true remaining cost: by the triangle inequality for the Manhattan metric, any path from `v` to the goal has length at least the direct distance. The reduced weight `w + h(v) - h(u)` is at least `d(u, v) + h(v) - h(u)`. The triangle inequality `h(u) <= d(u, v) + h(v)` makes that non-negative, so the guess is also consistent. The search orders entries by the pair (`g + h`, vertex id), skips stale entries, counts every other pop and returns at the goal. Consistency means each vertex is finalized at its first pop, so the pop count is the number of finalized vertices. The invariant is that every popped entry has priority at most the cheapest cost until the goal pops.

The program builds random graphs with coordinates and weights above the Manhattan bound. It compares the result with an array-based version of the same rule, with an unguided Dijkstra for the cost. It confirms that the guided search never finalizes more vertices than the unguided search by more than ties allow.

**Complexity.**
- **Time** is O((V + E) log V) in the worst case.
- **Space** is O(V + E).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class ManhattanGraphSearchVary {
    /**
     * Returns {cost, pops} for the guided search, or {-1, pops}.
     * Time: O((V + E) log V). Space: O(V + E).
     * Invariant: every popped entry has priority at most the cheapest cost until the goal pops.
     */
    static int[] manhattanSearch(int n, int[][] pos, int[][] edges, int start, int goal) {
        List<int[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) adj[e[0]].add(new int[]{e[1], e[2]});
        int[] h = new int[n];
        for (int v = 0; v < n; v++) h[v] = Math.abs(pos[v][0] - pos[goal][0]) + Math.abs(pos[v][1] - pos[goal][1]); // Manhattan guess
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Long.compare(x[0], y[0]) : Long.compare(x[1], y[1]));
        best[start] = 0;
        pq.add(new long[]{h[start], start, 0});
        int pops = 0;
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            int u = (int) cur[1];
            if (cur[2] > best[u]) continue; // stale entry
            pops++; // a finalized vertex
            if (u == goal) return new int[]{(int) cur[2], pops};
            for (int[] nb : adj[u]) {
                long g = cur[2] + nb[1];
                if (g < best[nb[0]]) { best[nb[0]] = g; pq.add(new long[]{g + h[nb[0]], nb[0], g}); }
            }
        }
        return new int[]{-1, pops};
    }

    static int[] oracle(int n, int[][] pos, int[][] edges, int start, int goal, boolean guided) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        boolean[] done = new boolean[n];
        dist[start] = 0;
        int pops = 0;
        while (true) {
            int u = -1;
            long bestF = 0;
            for (int v = 0; v < n; v++) {
                if (done[v] || dist[v] == Long.MAX_VALUE) continue;
                long f = dist[v] + (guided ? Math.abs(pos[v][0] - pos[goal][0]) + Math.abs(pos[v][1] - pos[goal][1]) : 0);
                if (u == -1 || f < bestF) { u = v; bestF = f; } // smallest (priority, id)
            }
            if (u == -1) return new int[]{-1, pops};
            done[u] = true;
            pops++;
            if (u == goal) return new int[]{(int) dist[u], pops};
            for (int[] e : edges) if (e[0] == u && dist[u] + e[2] < dist[e[1]]) dist[e[1]] = dist[u] + e[2];
        }
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        int[][] pos1 = {{0,0},{4,1},{3,3},{2,2},{1,3},{0,1},{4,0}};
        int[][] e1 = {{2,4,3},{0,5,2},{0,3,6},{3,5,4},{2,6,5},{5,6,7},{3,4,4},{5,4,3},{4,2,2},{6,1,1},{3,6,4}};
        if (!Arrays.equals(manhattanSearch(7, pos1, e1, 0, 6), new int[]{9, 3})) throw new AssertionError("ex1");
        int[][] pos2 = {{0,0},{1,0},{0,2},{2,1},{1,3},{3,3}};
        int[][] e2 = {{0,1,1},{0,2,2},{1,3,2},{2,4,2},{3,5,3},{4,5,3},{2,3,4},{1,4,5}};
        if (!Arrays.equals(manhattanSearch(6, pos2, e2, 0, 5), new int[]{6, 6})) throw new AssertionError("ex2");
        // random graphs with weights at least the Manhattan distance
        Random rnd = new Random(92);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] pos = new int[n][];
            for (int i = 0; i < n; i++) pos[i] = new int[]{rnd.nextInt(5), rnd.nextInt(5)};
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                int d = Math.abs(pos[u][0] - pos[v][0]) + Math.abs(pos[u][1] - pos[v][1]);
                edges[i] = new int[]{u, v, d + rnd.nextInt(3)}; // weight at least the Manhattan distance
            }
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            int[] got = manhattanSearch(n, pos, edges, s, g);
            if (!Arrays.equals(got, oracle(n, pos, edges, s, g, true))) throw new AssertionError("guided oracle");
            if (got[0] != oracle(n, pos, edges, s, g, false)[0]) throw new AssertionError("cost differs from Dijkstra");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Inadmissible Counterexample (Author exercise)
<!-- id: ah35-check-guess -->

**Approach.**
The method reverses every edge and runs Dijkstra from the goal. The resulting distance of a vertex is the true remaining cost `hstar[v]`, the length of the cheapest path from `v` to the goal in the original graph. Admissibility holds when no guess is above its true remaining cost, so the method scans the vertices and records the largest overshoot `h[v] - hstar[v]`, with 0 as the floor. Consistency holds when every edge has a non-negative reduced weight `w + h[v] - h[u]`, so a second scan over the edges decides it. The two properties are independent. The guess `[0, 0, 4, 0, 0, 0]` is admissible because each value is at most the true remaining cost. It is inconsistent because the edge from vertex 2 to vertex 4 has reduced weight `1 + 0 - 4 = -3`. The guess with 7 at the start overestimates by 2, which breaks admissibility whether or not one particular search happens to return a wrong cost. The invariant is that `hstar` holds exact shortest distances to the goal, so the comparisons are against the truth.

The program checks the three examples, then compares the result with a Floyd-Warshall oracle on random graphs in which every vertex reaches the goal. It also runs the unchecked search from the lesson with the overestimating guess on the lesson's three-vertex graph and confirms it returns 10 where 2 is optimal.

**Complexity.**
- **Time** is O((V + E) log V) for the reverse Dijkstra and O(V + E) for the scans.
- **Space** is O(V + E).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class CheckGuessBoundary {
    /**
     * Returns {admissible, consistent, excess}.
     * Time: O((V + E) log V). Space: O(V + E).
     * Invariant: hstar[v] is the exact cheapest cost from v to the goal.
     */
    static int[] checkGuess(int n, int[][] edges, int goal, int[] h) {
        List<int[]>[] rev = new List[n];
        for (int i = 0; i < n; i++) rev[i] = new ArrayList<>();
        for (int[] e : edges) rev[e[1]].add(new int[]{e[0], e[2]}); // reversed edge
        long[] hs = new long[n];
        Arrays.fill(hs, Long.MAX_VALUE);
        PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
        hs[goal] = 0;
        pq.add(new long[]{0, goal});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            if (cur[0] > hs[(int) cur[1]]) continue; // stale entry
            for (int[] nb : rev[(int) cur[1]])
                if (cur[0] + nb[1] < hs[nb[0]]) { hs[nb[0]] = cur[0] + nb[1]; pq.add(new long[]{hs[nb[0]], nb[0]}); }
        }
        int admissible = 1, consistent = 1;
        long excess = 0;
        for (int v = 0; v < n; v++) {
            excess = Math.max(excess, h[v] - hs[v]); // overshoot against the true remaining cost
            if (h[v] > hs[v]) admissible = 0;
        }
        for (int[] e : edges) if (e[2] + h[e[1]] - h[e[0]] < 0) consistent = 0; // negative reduced weight
        return new int[]{admissible, consistent, (int) excess};
    }

    static int unchecked(int n, int[][] edges, int start, int goal, int[] h) {
        List<int[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) adj[e[0]].add(new int[]{e[1], e[2]});
        int[] best = new int[n];
        Arrays.fill(best, Integer.MAX_VALUE);
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> x[0] - y[0]);
        best[start] = 0;
        pq.add(new int[]{h[start], start, 0});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            if (cur[2] > best[cur[1]]) continue;
            if (cur[1] == goal) return cur[2];
            for (int[] nb : adj[cur[1]]) {
                int g = cur[2] + nb[1];
                if (g < best[nb[0]]) { best[nb[0]] = g; pq.add(new int[]{g + h[nb[0]], nb[0], g}); }
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        // the examples from the problem text
        int[][] e1 = {{0,1,2},{0,2,1},{1,3,1},{2,3,4},{2,4,1},{4,3,1},{3,5,2}};
        if (!Arrays.equals(checkGuess(6, e1, 5, new int[]{5, 3, 4, 2, 3, 0}), new int[]{1, 1, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(checkGuess(6, e1, 5, new int[]{7, 3, 4, 2, 3, 0}), new int[]{0, 0, 2})) throw new AssertionError("ex2a");
        if (!Arrays.equals(checkGuess(6, e1, 5, new int[]{0, 0, 4, 0, 0, 0}), new int[]{1, 0, 0})) throw new AssertionError("ex2b");
        // the lesson's three-vertex graph: the overestimate 20 makes the search return 10 where 2 is optimal
        int[][] tri = {{0, 2, 10}, {0, 1, 1}, {1, 2, 1}};
        if (unchecked(3, tri, 0, 2, new int[]{0, 20, 0}) != 10 || unchecked(3, tri, 0, 2, new int[]{0, 0, 0}) != 2) throw new AssertionError("lesson claim");
        if (checkGuess(3, tri, 2, new int[]{0, 20, 0})[0] != 0) throw new AssertionError("should be inadmissible");
        // random graphs in which every vertex reaches the goal, checked against Floyd-Warshall
        Random rnd = new Random(93);
        for (int t = 0; t < 500; t++) {
            int n = 2 + rnd.nextInt(6), goal = rnd.nextInt(n);
            List<int[]> list = new ArrayList<>();
            for (int v = 0; v < n; v++) if (v != goal) list.add(new int[]{v, goal, 1 + rnd.nextInt(9)}); // guarantees reachability
            for (int i = rnd.nextInt(10); i > 0; i--) list.add(new int[]{rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(6)});
            int[][] edges = list.toArray(new int[0][]);
            int[] h = new int[n];
            for (int v = 0; v < n; v++) h[v] = rnd.nextInt(12);
            long INF = 1_000_000;
            long[][] d = new long[n][n];
            for (long[] row : d) Arrays.fill(row, INF);
            for (int v = 0; v < n; v++) d[v][v] = 0;
            for (int[] e : edges) d[e[0]][e[1]] = Math.min(d[e[0]][e[1]], e[2]);
            for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
            int adm = 1, cons = 1, ex = 0;
            for (int v = 0; v < n; v++) { if (h[v] > d[v][goal]) adm = 0; ex = (int) Math.max(ex, h[v] - d[v][goal]); }
            for (int[] e : edges) if (e[2] + h[e[1]] - h[e[0]] < 0) cons = 0;
            if (!Arrays.equals(checkGuess(n, edges, goal, h), new int[]{adm, cons, ex})) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] A-Star Grid Path (Author exercise)
<!-- id: ah35-reopen-grid -->

**Approach.**
The guess is admissible, so the first goal pop is optimal as long as no cheaper entry is thrown away. The method therefore keeps no closed set. It records the cheapest cost per cell. A pop is stale when its cost is larger than the record, and the method skips it. A non-stale pop of a cell that was expanded before happens when an entry with a smaller cost arrived after the first expansion. The method counts it as a reopening and expands the cell again. Neighbour updates use a strict comparison, so only cheaper costs create entries. The guess in the example is inconsistent, because the cell at row 1, column 0 has guess 3 while its neighbour at row 1, column 1 has guess 0 and the step costs 1, giving the reduced weight `1 + 0 - 3 = -2`. The cell at row 1, column 1 is therefore expanded through the top route first and reached more cheaply through row 1, column 0 later. The invariant is that the recorded cost of a cell never increases and the goal pop carries the cheapest cost.

The program verifies that the example guess is admissible by computing true remaining costs, runs the examples, and compares the cost with a Bellman-Ford relaxation on random grids with random admissible guesses. It also checks that a variant that never reopens returns 6 on the first example, so the reopening is what keeps the answer at 5.

**Complexity.**
- **Time** is O(R * C * log(R * C)) per expansion round, and the number of reopenings can exceed 0 only when the guess is inconsistent.
- **Space** is O(R * C).

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class ReopenGridRecognize {
    /**
     * Returns {cost, reopened} for an admissible guess, with reopening allowed.
     * Time: O(R*C log(R*C)) per round of expansions. Space: O(R*C).
     * Invariant: best never increases, and the first goal pop carries the cheapest cost.
     */
    static int[] searchWithReopen(int[][] cost, int sr, int sc, int gr, int gc, int[][] h, boolean allowReopen) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        boolean[][] expanded = new boolean[R][C];
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0])
                : x[1] != y[1] ? Integer.compare(x[1], y[1]) : Integer.compare(x[2], y[2]));
        best[sr][sc] = 0;
        pq.add(new int[]{h[sr][sc], sr, sc, 0});
        int reopened = 0;
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int r = cur[1], c = cur[2], g = cur[3];
            if (g > best[r][c]) continue; // stale entry
            if (expanded[r][c]) { if (!allowReopen) continue; reopened++; } // a cheaper cost reached an expanded cell
            expanded[r][c] = true;
            if (r == gr && c == gc) return new int[]{g, reopened};
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue;
                int ng = g + cost[nr][nc];
                if (ng < best[nr][nc]) {
                    if (expanded[nr][nc] && !allowReopen) continue; // the closed-set variant ignores the improvement
                    best[nr][nc] = ng;
                    pq.add(new int[]{ng + h[nr][nc], nr, nc, ng});
                }
            }
        }
        return new int[]{-1, reopened};
    }

    static int[][] trueRemaining(int[][] cost, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        int[][] zero = new int[R][C];
        int[][] res = new int[R][C];
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) {
            int d = r == gr && c == gc ? 0 : cost[r][c] == 0 ? -1 : searchWithReopen(cost, r, c, gr, gc, zero, true)[0];
            res[r][c] = d == -1 ? Integer.MAX_VALUE : d; // no route to the goal means no finite remaining cost
        }
        return res;
    }

    public static void main(String[] args) {
        int[][] cost = {{2, 2, 9, 1}, {1, 1, 2, 1}};
        int[][] h = {{0, 1, 2, 0}, {3, 0, 1, 0}};
        // the example guess is admissible
        int[][] hs = trueRemaining(cost, 1, 3);
        for (int r = 0; r < 2; r++) for (int c = 0; c < 4; c++) if (h[r][c] > hs[r][c]) throw new AssertionError("not admissible");
        // the two examples from the problem text
        if (!Arrays.equals(searchWithReopen(cost, 0, 0, 1, 3, h, true), new int[]{5, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(searchWithReopen(cost, 0, 0, 1, 3, new int[2][4], true), new int[]{5, 0})) throw new AssertionError("ex2");
        // without reopening the same guess returns 6
        if (searchWithReopen(cost, 0, 0, 1, 3, h, false)[0] != 6) throw new AssertionError("closed set should be wrong");
        // random grids with random admissible guesses: the cost equals the true shortest cost
        Random rnd = new Random(94);
        int reopenSeen = 0;
        for (int t = 0; t < 600; t++) {
            int R = 1 + rnd.nextInt(4), C = 1 + rnd.nextInt(4);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(5) == 0 ? 0 : 1 + rnd.nextInt(8);
            g[0][0] = 1; g[R - 1][C - 1] = 1;
            int[][] tr = trueRemaining(g, R - 1, C - 1);
            int[][] guess = new int[R][C];
            for (int r = 0; r < R; r++) for (int c = 0; c < C; c++)
                guess[r][c] = tr[r][c] == Integer.MAX_VALUE ? 0 : rnd.nextInt(tr[r][c] + 1); // admissible by construction
            int[] got = searchWithReopen(g, 0, 0, R - 1, C - 1, guess, true);
            if (got[0] != tr[0][0] && !(g[0][0] == 1 && tr[0][0] == Integer.MAX_VALUE && got[0] == -1)) throw new AssertionError("cost " + got[0] + " vs " + tr[0][0]);
            reopenSeen += got[1];
        }
        if (reopenSeen == 0) throw new AssertionError("no reopening exercised");
        System.out.println("ok");
    }
}
```
