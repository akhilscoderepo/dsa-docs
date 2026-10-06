<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Shortest Paths With A Heap

#### Solution: [Build] Network Delay With Unreached Count (LeetCode 743)
<!-- id: sp-delay-unreached-count -->

**Approach.**
The method builds an adjacency list from `times` and runs the heap loop from node `k`. Distances are `long` and start at `Long.MAX_VALUE`, except for the source at 0. Each heap entry holds a distance and a node. The loop skips a removed entry whose distance exceeds the stored one, because a better entry for that node was pushed later. Otherwise it scans the outgoing links and pushes every improvement.

The invariant is that a removed current entry carries the final distance of its node, because no weight is negative and the heap returns the smallest entry first. After the heap is empty, the method scans `dist` once. Finite entries feed the maximum and infinite entries feed the unreached count. The source is finite with distance 0, so `delay` is 0 when nothing else is reached.

**Complexity.**
- **Time** is O((n + m) log m) for `m` links, because at most `m + 1` entries enter the heap and each costs O(log m).
- **Space** is O(n + m) for the adjacency list, the distance array and the heap.

```java run
import java.util.*;

public final class DelayUnreached {
    /**
     * Returns {largest finite distance, count of unreached nodes} from node k.
     * Time: O((n + m) log m). Space: O(n + m).
     * Invariant: a removed current entry holds the final distance of its node.
     */
    static int[] delayAndUnreached(int n, int[][] times, int k) {
        // Adjacency list indexed by node, with each entry holding {end, weight}.
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
        for (int[] t : times) adj.get(t[0]).add(new int[] {t[1], t[2]});
        long[] dist = new long[n + 1];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[k] = 0;
        // Entries are {distance, node}; Long.compare avoids the overflow of a subtraction comparator.
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, k});
        // Each loop turn removes one entry, so the number of turns is bounded by the pushes.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            // A larger distance than the stored one marks a stale entry, which costs no further work.
            if (top[0] > dist[u]) continue;
            for (int[] e : adj.get(u)) {
                long cand = top[0] + e[1];
                // Push only a strict improvement, which keeps the heap size within m + 1 entries.
                if (cand < dist[e[0]]) {
                    dist[e[0]] = cand;
                    heap.add(new long[] {cand, e[0]});
                }
            }
        }
        long delay = 0;
        int unreached = 0;
        // One scan over the finished distances yields both values of the result.
        for (int v = 1; v <= n; v++) {
            if (dist[v] == Long.MAX_VALUE) unreached++;
            else delay = Math.max(delay, dist[v]);
        }
        return new int[] {(int) delay, unreached};
    }

    /** Oracle: repeated passes over all links until nothing changes. */
    static int[] oracle(int n, int[][] times, int k) {
        long[] d = new long[n + 1];
        Arrays.fill(d, Long.MAX_VALUE);
        d[k] = 0;
        for (int pass = 0; pass <= n; pass++) {
            for (int[] t : times) {
                if (d[t[0]] != Long.MAX_VALUE && d[t[0]] + t[2] < d[t[1]]) d[t[1]] = d[t[0]] + t[2];
            }
        }
        long delay = 0;
        int un = 0;
        for (int v = 1; v <= n; v++) {
            if (d[v] == Long.MAX_VALUE) un++;
            else delay = Math.max(delay, d[v]);
        }
        return new int[] {(int) delay, un};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(delayAndUnreached(5, new int[][] {{1, 2, 2}, {1, 3, 5}, {3, 2, 1}, {2, 4, 3}, {4, 5, 2}}, 1), new int[] {7, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(delayAndUnreached(3, new int[][] {{1, 1, 5}, {1, 2, 0}}, 1), new int[] {0, 1})) throw new AssertionError("ex2");
        // Java facts: a subtraction comparator overflows for distant longs, and Long.compare does not.
        long big = Long.MAX_VALUE, small = -5;
        if (!(big - small < 0) || Long.compare(big, small) <= 0) throw new AssertionError("comparator overflow");
        // PriorityQueue removes the smallest element first under the comparator.
        PriorityQueue<long[]> probe = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        probe.add(new long[] {3, 0});
        probe.add(new long[] {1, 1});
        if (probe.poll()[0] != 1) throw new AssertionError("heap order");
        // Random networks with parallel links, self loops and zero weights against the repeated-pass oracle.
        Random rnd = new Random(2491);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(16);
            int[][] times = new int[m][];
            for (int i = 0; i < m; i++) times[i] = new int[] {1 + rnd.nextInt(n), 1 + rnd.nextInt(n), rnd.nextInt(7)};
            int k = 1 + rnd.nextInt(n);
            if (!Arrays.equals(delayAndUnreached(n, times, k), oracle(n, times, k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Path With Minimum Effort (LeetCode 1631)
<!-- id: sp-min-effort-route -->

**Approach.**
Each cell is a state, and its stored value is the smallest effort of any route that reaches it. The heap holds entries of effort and cell index. Moving from a cell with effort `e` to a neighbor with step difference `s` gives the candidate `max(e, s)`. The method pushes the candidate when it beats the stored effort of the neighbor, and it skips a removed entry whose effort exceeds the stored one.

The invariant is that a removed current entry has the final effort of its cell. The maximum never decreases when a route grows, and the heap returns the smallest effort first, so no unprocessed route reaches the cell with less. The method returns the stored value of the last cell. A grid with one cell returns 0, since the source is the destination and no step is taken.

**Complexity.**
- **Time** is O(R * C * log(R * C)), because the grid has at most 4RC edges and each successful push costs O(log(RC)).
- **Space** is O(R * C) for the effort array and the heap.

```java run
import java.util.*;

public final class MinEffortRoute {
    /**
     * Returns the smallest possible largest height step from the top left to the bottom right cell.
     * Time: O(R C log(R C)). Space: O(R C).
     * Invariant: a removed current entry holds the final effort of its cell.
     */
    static int minimumEffort(int[][] heights) {
        int rows = heights.length, cols = heights[0].length;
        int[][] effort = new int[rows][cols];
        for (int[] row : effort) Arrays.fill(row, Integer.MAX_VALUE);
        effort[0][0] = 0;
        // Entries are {effort, row, col}; efforts are below 10^6 so Integer.compare is exact.
        PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        heap.add(new int[] {0, 0, 0});
        int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
        while (!heap.isEmpty()) {
            int[] top = heap.poll();
            int r = top[1], c = top[2];
            // Stale entries have a larger effort than the stored one and are skipped.
            if (top[0] > effort[r][c]) continue;
            // The first current removal of the target is final, so the search can stop there.
            if (r == rows - 1 && c == cols - 1) return top[0];
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
                // The new route score is the maximum of the old score and this step, not their sum.
                int cand = Math.max(top[0], Math.abs(heights[nr][nc] - heights[r][c]));
                if (cand < effort[nr][nc]) {
                    effort[nr][nc] = cand;
                    heap.add(new int[] {cand, nr, nc});
                }
            }
        }
        return effort[rows - 1][cols - 1];
    }

    /** Oracle: the smallest adjacent difference t for which a flood fill over steps of at most t reaches the corner. */
    static int oracle(int[][] h) {
        int rows = h.length, cols = h[0].length;
        TreeSet<Integer> cands = new TreeSet<>();
        cands.add(0);
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
            if (r + 1 < rows) cands.add(Math.abs(h[r][c] - h[r + 1][c]));
            if (c + 1 < cols) cands.add(Math.abs(h[r][c] - h[r][c + 1]));
        }
        // Only a step difference present in the grid can be the answer, so the thresholds are tried in ascending order.
        for (int t : cands) {
            boolean[][] seen = new boolean[rows][cols];
            Deque<int[]> st = new ArrayDeque<>();
            seen[0][0] = true;
            st.push(new int[] {0, 0});
            int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
            while (!st.isEmpty()) {
                int[] p = st.pop();
                for (int d = 0; d < 4; d++) {
                    int a = p[0] + dr[d], b = p[1] + dc[d];
                    if (a >= 0 && b >= 0 && a < rows && b < cols && !seen[a][b] && Math.abs(h[a][b] - h[p[0]][p[1]]) <= t) {
                        seen[a][b] = true;
                        st.push(new int[] {a, b});
                    }
                }
            }
            if (seen[rows - 1][cols - 1]) return t;
        }
        throw new AssertionError("unreachable");
    }

    public static void main(String[] args) {
        // The two examples of the exercise and the single-cell grid.
        if (minimumEffort(new int[][] {{3, 3, 9}, {8, 2, 4}, {7, 1, 6}}) != 2) throw new AssertionError("ex1");
        if (minimumEffort(new int[][] {{5, 1}, {5, 9}}) != 4) throw new AssertionError("ex2");
        if (minimumEffort(new int[][] {{7}}) != 0) throw new AssertionError("single cell");
        // Java fact: Math.abs of a difference of values below 10^6 stays nonnegative and exact.
        if (Math.abs(1000000 - 0) != 1000000 || Math.abs(0 - 1000000) != 1000000) throw new AssertionError("abs");
        // Random grids with small and large height ranges against the threshold oracle.
        Random rnd = new Random(2492);
        for (int t = 0; t < 1500; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int range = rnd.nextBoolean() ? 4 : 1000000;
            int[][] h = new int[rows][cols];
            for (int[] row : h) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(range + 1);
            if (minimumEffort(h) != oracle(h)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Cheapest Flights With The Stop Count (LeetCode 787)
<!-- id: sp-flights-stop-count -->

**Approach.**
The state is a pair of a city and the number of flights used, from 0 to `k + 1`. The array `best[city][used]` stores the least price for that pair. The heap holds entries of price, flights used and city, ordered by price and then by flights used. A removed entry is skipped when its price exceeds the stored one. An entry for the destination ends the search. An entry with `k + 1` flights used pushes nothing, because no further flight is allowed.

The invariant is that a removed current entry has the final price for its pair of city and flights used. A single distance per city would overwrite a cheap route that has used up its flights and would lose a costlier route that can still continue. The tie order is the reason for the second sort key. Among entries with equal price, the one with fewer flights comes out first, so the first removed destination entry gives the least price and then the fewest flights. The stop count is the flight count minus one. The method returns `{-1, -1}` when the heap empties before the destination is reached.

**Complexity.**
- **Time** is O((n + m) k log(m k)). The search has `n * (k + 2)` states, and each flight is scanned once per layer.
- **Space** is O(n * k + m) for the state array, the adjacency list and the heap.

```java run
import java.util.*;

public final class FlightsStopCount {
    /**
     * Returns {least price, stops} among routes with at most k stops, preferring fewer stops on ties.
     * Time: O((n + m) k log(m k)). Space: O(n k + m).
     * Invariant: a removed current entry has the final price of its pair of city and flights used.
     */
    static int[] cheapest(int n, int[][] flights, int src, int dst, int k) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] f : flights) adj.get(f[0]).add(new int[] {f[1], f[2]});
        // One stored price for every city and every count of flights from 0 to k + 1.
        int[][] best = new int[n][k + 2];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        best[src][0] = 0;
        // Entries are {price, flights used, city}; equal prices order by fewer flights.
        PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        heap.add(new int[] {0, 0, src});
        while (!heap.isEmpty()) {
            int[] top = heap.poll();
            int used = top[1], city = top[2];
            // A price above the stored one for this exact state is stale.
            if (top[0] > best[city][used]) continue;
            // The first current entry of the destination has the least price and then the fewest flights.
            if (city == dst) return new int[] {top[0], used - 1};
            // With every allowed flight spent, the entry cannot extend, which bounds the layers.
            if (used == k + 1) continue;
            for (int[] e : adj.get(city)) {
                int cand = top[0] + e[1];
                // The next layer is its own state, so a cheaper route with more flights never hides this one.
                if (cand < best[e[0]][used + 1]) {
                    best[e[0]][used + 1] = cand;
                    heap.add(new int[] {cand, used + 1, e[0]});
                }
            }
        }
        return new int[] {-1, -1};
    }

    /** Oracle: enumerates every walk of at most k + 1 flights and keeps the least pair of price and stops. */
    static int[] oracle(int n, int[][] flights, int src, int dst, int k) {
        int[] best = {Integer.MAX_VALUE, Integer.MAX_VALUE};
        walk(flights, src, dst, k, 0, 0, best);
        return best[0] == Integer.MAX_VALUE ? new int[] {-1, -1} : best;
    }

    private static void walk(int[][] flights, int at, int dst, int k, int used, int cost, int[] best) {
        if (at == dst && used >= 1 && (cost < best[0] || (cost == best[0] && used - 1 < best[1]))) {
            best[0] = cost;
            best[1] = used - 1;
        }
        if (used == k + 1) return;
        for (int[] f : flights) if (f[0] == at) walk(flights, f[1], dst, k, used + 1, cost + f[2], best);
    }

    public static void main(String[] args) {
        // The two examples of the exercise, then the case with no route inside the limit.
        if (!Arrays.equals(cheapest(5, new int[][] {{0, 1, 20}, {1, 2, 20}, {2, 4, 20}, {0, 3, 30}, {3, 4, 90}}, 0, 4, 1), new int[] {120, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(cheapest(3, new int[][] {{0, 1, 0}, {1, 2, 0}, {0, 2, 0}}, 0, 2, 1), new int[] {0, 0})) throw new AssertionError("ex2");
        if (!Arrays.equals(cheapest(3, new int[][] {{0, 1, 2}, {1, 2, 2}}, 0, 2, 0), new int[] {-1, -1})) throw new AssertionError("limit");
        // The over-pruning case: a plain distance per city would answer -1 here.
        if (!Arrays.equals(cheapest(4, new int[][] {{0, 1, 1}, {1, 2, 1}, {0, 2, 5}, {2, 3, 1}}, 0, 3, 1), new int[] {6, 1})) throw new AssertionError("over-pruning");
        // Java fact: a ternary comparator with Integer.compare orders by price first and flights second.
        PriorityQueue<int[]> probe = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        probe.add(new int[] {4, 3});
        probe.add(new int[] {4, 1});
        if (probe.poll()[1] != 1) throw new AssertionError("tie order");
        // Random flight sets with zero prices, parallel flights and every limit from 0 to 4.
        Random rnd = new Random(2493);
        for (int t = 0; t < 1000; t++) {
            int n = 2 + rnd.nextInt(5);
            int m = rnd.nextInt(9);
            int[][] fl = new int[m][];
            for (int i = 0; i < m; i++) fl[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(6)};
            int src = rnd.nextInt(n);
            int dst = (src + 1 + rnd.nextInt(n - 1)) % n;
            int k = rnd.nextInt(5);
            if (!Arrays.equals(cheapest(n, fl, src, dst, k), oracle(n, fl, src, dst, k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Path With Maximum Probability (LeetCode 1514)
<!-- id: sp-max-probability-path -->

**Approach.**
The score of a path is a product of factors in the range from 0 to 1, so extending a path never raises its score. That is the mirror image of nonnegative sums, and the heap loop applies after one change. The heap returns the largest probability first, which a comparator on `Double.compare(b[0], a[0])` provides. The stored value `best[v]` starts at 0.0 for all nodes and at 1.0 for the start.

A removed entry with a probability below the stored one is stale and is skipped. The invariant is that a removed current entry holds the final best probability of its node. The method returns as soon as the end node is removed, and it returns 0.0 when the heap empties first. Each undirected edge is stored in both directions.

**Complexity.**
- **Time** is O((n + m) log m), because each edge direction can push at most one entry and each push costs O(log m).
- **Space** is O(n + m) for the adjacency list, the stored values and the heap.

```java run
import java.util.*;

public final class MaxProbabilityPath {
    /**
     * Returns the largest product of edge probabilities over paths from start to end, or 0.0.
     * Time: O((n + m) log m). Space: O(n + m).
     * Invariant: a removed current entry holds the final best probability of its node.
     */
    static double maxProbability(int n, int[][] edges, double[] succProb, int start, int end) {
        List<List<double[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        // Both directions are stored because the edges are undirected.
        for (int i = 0; i < edges.length; i++) {
            adj.get(edges[i][0]).add(new double[] {edges[i][1], succProb[i]});
            adj.get(edges[i][1]).add(new double[] {edges[i][0], succProb[i]});
        }
        double[] best = new double[n];
        best[start] = 1.0;
        // The reversed comparison puts the largest probability at the head of the queue.
        PriorityQueue<double[]> heap = new PriorityQueue<>((a, b) -> Double.compare(b[0], a[0]));
        heap.add(new double[] {1.0, start});
        while (!heap.isEmpty()) {
            double[] top = heap.poll();
            int u = (int) top[1];
            // A probability below the stored one marks a stale entry.
            if (top[0] < best[u]) continue;
            // The first current removal of the end node is final because products never grow.
            if (u == end) return top[0];
            for (double[] e : adj.get(u)) {
                double cand = top[0] * e[1];
                int v = (int) e[0];
                // A strictly larger product improves the node and enters the heap.
                if (cand > best[v]) {
                    best[v] = cand;
                    heap.add(new double[] {cand, v});
                }
            }
        }
        return 0.0;
    }

    /** Oracle: repeated passes over all edges in both directions until no value grows. */
    static double oracle(int n, int[][] edges, double[] p, int start, int end) {
        double[] best = new double[n];
        best[start] = 1.0;
        for (int pass = 0; pass <= n; pass++) {
            for (int i = 0; i < edges.length; i++) {
                int a = edges[i][0], b = edges[i][1];
                if (best[a] * p[i] > best[b]) best[b] = best[a] * p[i];
                if (best[b] * p[i] > best[a]) best[a] = best[b] * p[i];
            }
        }
        return best[end];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        double r1 = maxProbability(4, new int[][] {{0, 1}, {1, 3}, {0, 2}, {2, 3}}, new double[] {0.5, 0.5, 0.75, 0.5}, 0, 3);
        if (Math.abs(r1 - 0.375) > 1e-9) throw new AssertionError("ex1");
        if (maxProbability(4, new int[][] {{0, 1}, {2, 3}}, new double[] {0.5, 0.5}, 0, 3) != 0.0) throw new AssertionError("ex2");
        // Java fact: the reversed Double.compare comparator removes the largest value first.
        PriorityQueue<double[]> probe = new PriorityQueue<>((a, b) -> Double.compare(b[0], a[0]));
        probe.add(new double[] {0.25, 0});
        probe.add(new double[] {0.75, 1});
        if (probe.poll()[0] != 0.75) throw new AssertionError("max-first order");
        // Random graphs with exact binary fractions, and then with arbitrary doubles, against the oracle.
        Random rnd = new Random(2494);
        double[] exact = {0.0, 0.25, 0.5, 0.75, 1.0};
        for (int t = 0; t < 1500; t++) {
            int n = 2 + rnd.nextInt(7);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            double[] p = new double[m];
            for (int i = 0; i < m; i++) {
                edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
                p[i] = t % 2 == 0 ? exact[rnd.nextInt(exact.length)] : rnd.nextDouble();
            }
            int start = rnd.nextInt(n);
            int end = (start + 1 + rnd.nextInt(n - 1)) % n;
            if (Math.abs(maxProbability(n, edges, p, start, end) - oracle(n, edges, p, start, end)) > 1e-9) throw new AssertionError("random " + t);
        }
    }
}
```
