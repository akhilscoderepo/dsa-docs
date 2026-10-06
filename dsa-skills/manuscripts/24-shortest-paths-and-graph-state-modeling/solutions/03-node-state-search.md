<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Search Over Place And State

#### Solution: [Build] Node And Coupon Flag (Author exercise)
<!-- id: sp-coupon-flag -->

**Approach.**
The method treats the pair `(node, used)` as one search position and stores its cost in `dist[2 * node + used]`. A heap releases positions in ascending cost. From a position with `used == 0` the method relaxes each edge twice. One relaxation pays the full weight into `used == 0`, and the other pays `w / 2` into `used == 1`. From a position with `used == 1` only the full-weight relaxation exists. A popped entry whose cost exceeds the stored distance is stale and is skipped.

The invariant is that `dist[p]` is the cost of the cheapest route found so far that ends in position `p`. The first non-stale pop of `p` carries its final cost. Weights are nonnegative and the halved weight is not larger than the full weight, so no relaxation lowers a cost below the cost of the entry that made it. The answer is the smaller of the two positions of `dst`, because the flag at arrival does not matter.

**Complexity.**
- **Time** is O((V + E) log(V + E)), because the search holds 2V positions and 2E relaxations, and every successful relaxation pushes one heap entry.
- **Space** is O(V + E) for the adjacency list, the 2V distances and at most 2E heap entries.

```java run
import java.util.*;

public final class CouponFlag {
    /**
     * Returns the cheapest cost from src to dst when at most one edge costs floor(w / 2), or -1.
     * Time: O((V + E) log(V + E)). Space: O(V + E).
     * Invariant: dist[2 * v + used] is the cheapest known cost of arriving at v with that flag.
     */
    static long cheapest(int n, int[][] edges, int src, int dst) {
        // One list of outgoing edges per node, built once in O(V + E).
        List<List<int[]>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        for (int[] e : edges) out.get(e[0]).add(new int[] {e[1], e[2]});
        // Two distance slots per node; Long.MAX_VALUE marks a position nobody has reached.
        long[] dist = new long[2 * n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[2 * src] = 0;
        // Each heap entry holds {cost, node, used}, ordered by cost.
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, src, 0});
        // Each pop removes one entry, and the entry count is bounded by the successful relaxations.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            int used = (int) top[2];
            // A cost above the stored distance means a cheaper entry for this position already ran.
            if (top[0] > dist[2 * u + used]) continue;
            // Each outgoing edge is read once per position of u, so at most twice.
            for (int[] e : out.get(u)) {
                int v = e[0];
                // Full price keeps the flag unchanged; long arithmetic avoids int overflow.
                long full = top[0] + e[1];
                if (full < dist[2 * v + used]) {
                    dist[2 * v + used] = full;
                    heap.add(new long[] {full, v, used});
                }
                // The coupon may be spent only while the flag is still 0.
                if (used == 0) {
                    long half = top[0] + e[1] / 2;
                    if (half < dist[2 * v + 1]) {
                        dist[2 * v + 1] = half;
                        heap.add(new long[] {half, v, 1});
                    }
                }
            }
        }
        // Either flag value is acceptable at the destination.
        long best = Math.min(dist[2 * dst], dist[2 * dst + 1]);
        // The sentinel survives only when neither position was reached.
        return best == Long.MAX_VALUE ? -1 : best;
    }

    /** Oracle: Bellman-Ford style rounds over the positions until no distance changes. */
    static long oracle(int n, int[][] edges, int src, int dst) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][2];
        for (long[] r : d) Arrays.fill(r, inf);
        d[src][0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                for (int s = 0; s < 2; s++) {
                    if (d[e[0]][s] >= inf) continue;
                    if (d[e[0]][s] + e[2] < d[e[1]][s]) { d[e[1]][s] = d[e[0]][s] + e[2]; changed = true; }
                }
                if (d[e[0]][0] < inf && d[e[0]][0] + e[2] / 2 < d[e[1]][1]) { d[e[1]][1] = d[e[0]][0] + e[2] / 2; changed = true; }
            }
        }
        long b = Math.min(d[dst][0], d[dst][1]);
        return b >= inf ? -1 : b;
    }

    /** Summary of a distance array: count of finite entries and the largest one. */
    static int[] summary(int[] d) {
        int count = 0;
        int max = 0;
        // Each node with a nonnegative distance is reached.
        for (int x : d) {
            if (x >= 0) { count++; max = Math.max(max, x); }
        }
        return new int[] {count, max};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (cheapest(4, new int[][] {{0, 1, 8}, {1, 2, 2}, {2, 3, 100}, {0, 2, 30}}, 0, 3) != 60) throw new AssertionError("ex1");
        if (cheapest(3, new int[][] {{0, 1, 7}, {1, 2, 9}, {0, 2, 20}}, 0, 2) != 10) throw new AssertionError("ex2");
        // Unreachable target and source equal to target.
        if (cheapest(3, new int[][] {{0, 1, 5}}, 0, 2) != -1) throw new AssertionError("unreachable");
        if (cheapest(2, new int[][] {{0, 0, 4}}, 0, 0) != 0) throw new AssertionError("same node");
        // Java fact: integer division of a nonnegative int floors, and an int sum can overflow while a long sum does not.
        if (7 / 2 != 3 || 1 / 2 != 0) throw new AssertionError("floor division");
        if (Integer.MAX_VALUE + 1 >= 0 || (long) Integer.MAX_VALUE + 1 != 2147483648L) throw new AssertionError("overflow fact");
        // A chain whose total exceeds the int range still returns the exact long total minus the best halving.
        int[][] chain = new int[5][];
        for (int i = 0; i < 5; i++) chain[i] = new int[] {i, i + 1, 1_000_000_000};
        if (cheapest(6, chain, 0, 5) != 4_500_000_000L) throw new AssertionError("long chain");
        // Random graphs with cycles, repeats and zero weights against the round-based oracle.
        Random rnd = new Random(2403);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(12)};
            int s = rnd.nextInt(n);
            int d = rnd.nextInt(n);
            if (cheapest(n, edges, s, d) != oracle(n, edges, s, d)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Distance By State (Author exercise)
<!-- id: sp-distance-by-state -->

**Approach.**
The method keeps a table with `k + 1` columns for every node, so column `j` counts the coupons spent on the route. A position is the pair `(node, j)`. Relaxing an edge from `(u, j)` produces `(v, j)` at the full weight and, when `j < k`, `(v, j + 1)` at the halved weight. The same heap search as in the previous exercise fills the table, and the method copies unreached cells as `-1`.

The invariant is that the column index never decreases along a route, so a position with a higher count never feeds a lower count. Each cell therefore receives its final value when its first non-stale entry leaves the heap. A column is not merged with another column, because the exercise asks for exactly `j` coupons and a route with fewer coupons answers a different cell.

**Complexity.**
- **Time** is O(k (V + E) log(k (V + E))), because the search holds `(k + 1) V` positions and at most `(k + 1) * 2E` relaxations.
- **Space** is O(k (V + E)) for the table and the heap entries.

```java run
import java.util.*;

public final class DistanceByState {
    /**
     * Returns table[v][j], the cheapest cost to reach v using exactly j coupons, or -1.
     * Time: O(k (V + E) log(k (V + E))). Space: O(k (V + E)).
     * Invariant: a route never moves from a higher coupon count to a lower one.
     */
    static long[][] table(int n, int k, int[][] edges, int src) {
        // Outgoing edges per node as {target, weight}.
        List<List<int[]>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        for (int[] e : edges) out.get(e[0]).add(new int[] {e[1], e[2]});
        // The width is k + 1 because the counts 0..k are all valid columns.
        int w = k + 1;
        long[] dist = new long[n * w];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src * w] = 0;
        // Entries are {cost, position}, where position = node * w + count.
        PriorityQueue<long[]> heap = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
        heap.add(new long[] {0, src * w});
        // The loop ends when every improvement has been consumed.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int pos = (int) top[1];
            // Skip an entry that a cheaper entry for the same position has already replaced.
            if (top[0] > dist[pos]) continue;
            int u = pos / w;
            int j = pos % w;
            // Each edge is read once for each of the k + 1 columns of u.
            for (int[] e : out.get(u)) {
                // Paying the full weight keeps the coupon count.
                long full = top[0] + e[1];
                int same = e[0] * w + j;
                if (full < dist[same]) { dist[same] = full; heap.add(new long[] {full, same}); }
                // Spending a coupon is possible only below the limit.
                if (j < k) {
                    long half = top[0] + e[1] / 2;
                    int next = e[0] * w + j + 1;
                    if (half < dist[next]) { dist[next] = half; heap.add(new long[] {half, next}); }
                }
            }
        }
        // Copy into a node-by-count table and replace the sentinel by -1.
        long[][] res = new long[n][w];
        for (int v = 0; v < n; v++) {
            for (int j = 0; j < w; j++) res[v][j] = dist[v * w + j] == Long.MAX_VALUE ? -1 : dist[v * w + j];
        }
        return res;
    }

    /** Oracle: repeated passes over the edge list on a plain two-dimensional array. */
    static long[][] oracle(int n, int k, int[][] edges, int src) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][k + 1];
        for (long[] r : d) Arrays.fill(r, inf);
        d[src][0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                for (int j = 0; j <= k; j++) {
                    if (d[e[0]][j] >= inf) continue;
                    if (d[e[0]][j] + e[2] < d[e[1]][j]) { d[e[1]][j] = d[e[0]][j] + e[2]; changed = true; }
                    if (j < k && d[e[0]][j] + e[2] / 2 < d[e[1]][j + 1]) { d[e[1]][j + 1] = d[e[0]][j] + e[2] / 2; changed = true; }
                }
            }
        }
        for (long[] r : d) for (int j = 0; j <= k; j++) if (r[j] >= inf) r[j] = -1;
        return d;
    }

    /** Summary of a distance array: count of finite entries and the largest one. */
    static int[] summary(int[] d) {
        int count = 0;
        int max = 0;
        // Each node with a nonnegative distance is reached.
        for (int x : d) {
            if (x >= 0) { count++; max = Math.max(max, x); }
        }
        return new int[] {count, max};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(table(3, 1, new int[][] {{0, 1, 6}, {1, 2, 4}}, 0), new long[][] {{0, -1}, {6, 3}, {10, 7}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(table(4, 2, new int[][] {{0, 1, 5}, {1, 0, 3}, {1, 2, 9}}, 0), new long[][] {{0, 5, 3}, {5, 2, 7}, {14, 9, 6}, {-1, -1, -1}})) throw new AssertionError("ex2");
        // With k = 0 the table is a plain single-source distance column.
        if (!Arrays.deepEquals(table(3, 0, new int[][] {{0, 1, 4}, {0, 2, 9}, {1, 2, 2}}, 0), new long[][] {{0}, {4}, {6}})) throw new AssertionError("k zero");
        // Large weights stay exact in long cells.
        if (table(3, 1, new int[][] {{0, 1, 2_000_000_000}, {1, 2, 2_000_000_000}}, 0)[2][0] != 4_000_000_000L) throw new AssertionError("long cell");
        // Random graphs with cycles and k from 0 to 3 against the pass-based oracle.
        Random rnd = new Random(2413);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(6);
            int k = rnd.nextInt(4);
            int m = rnd.nextInt(12);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(15)};
            int s = rnd.nextInt(n);
            if (!Arrays.deepEquals(table(n, k, edges, s), oracle(n, k, edges, s))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Same Node, Different Future (Author exercise)
<!-- id: sp-same-node-future -->

**Approach.**
The method runs two searches on the same graph and returns both answers. The first search is the position search of the first exercise, which keeps the flag in the position and returns the true minimum. The second search follows the pruned definition of the problem. It pops `(cost, node, used)` triples in ascending order of cost, then node, then flag. It marks a node closed at its first pop and ignores every later triple of that node. It returns the cost at which `dst` is first popped.

The pruned search violates the invariant of the first search, because a closed node keeps one flag and one cost. A triple that arrives later with a higher cost and an unused coupon is dropped, although its future may be cheaper. The returned pair therefore differs exactly when the cheapest arrival at some node on the true best route spends the coupon too early.

**Complexity.**
- **Time** is O((V + E) log(V + E)) for each of the two searches.
- **Space** is O(V + E) for the lists, the distance array and the heaps.

```java run
import java.util.*;

public final class SameNodeFuture {
    /**
     * Returns {exact, pruned}: the true minimum with position state, and the first-pop answer with one state per node.
     * Time: O((V + E) log(V + E)). Space: O(V + E).
     * Invariant of the exact search: the flag is part of the position. The pruned search drops it on purpose.
     */
    static long[] both(int n, int[][] edges, int src, int dst) {
        // Shared adjacency lists of {target, weight}.
        List<List<int[]>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        for (int[] e : edges) out.get(e[0]).add(new int[] {e[1], e[2]});
        // Exact search: two distance slots per node.
        long[] dist = new long[2 * n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[2 * src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, src, 0});
        // The loop pops entries until no improvement remains.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            int used = (int) top[2];
            // Stale entries carry a cost above the stored distance.
            if (top[0] > dist[2 * u + used]) continue;
            // Relax each outgoing edge at full price and, while unused, at half price.
            for (int[] e : out.get(u)) {
                long full = top[0] + e[1];
                if (full < dist[2 * e[0] + used]) { dist[2 * e[0] + used] = full; heap.add(new long[] {full, e[0], used}); }
                if (used == 0 && top[0] + e[1] / 2 < dist[2 * e[0] + 1]) {
                    dist[2 * e[0] + 1] = top[0] + e[1] / 2;
                    heap.add(new long[] {dist[2 * e[0] + 1], e[0], 1});
                }
            }
        }
        long exact = Math.min(dist[2 * dst], dist[2 * dst + 1]);
        if (exact == Long.MAX_VALUE) exact = -1;
        // Pruned search: the heap orders triples by cost, then node, then flag.
        PriorityQueue<long[]> ph = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : a[1] != b[1] ? Long.compare(a[1], b[1]) : Long.compare(a[2], b[2]));
        boolean[] closed = new boolean[n];
        ph.add(new long[] {0, src, 0});
        long pruned = -1;
        // Each pop either closes a node or is discarded.
        while (!ph.isEmpty()) {
            long[] top = ph.poll();
            int u = (int) top[1];
            // A closed node keeps its first cost and first flag, which is the false friend.
            if (closed[u]) continue;
            closed[u] = true;
            // The first pop of dst fixes the pruned answer.
            if (u == dst) { pruned = top[0]; break; }
            // Push both choices from a triple that still has its coupon.
            for (int[] e : out.get(u)) {
                ph.add(new long[] {top[0] + e[1], e[0], top[2]});
                if (top[2] == 0) ph.add(new long[] {top[0] + e[1] / 2, e[0], 1});
            }
        }
        return new long[] {exact, pruned};
    }

    /** Oracle: exact answer by Bellman-Ford rounds; pruned answer by a linear scan over a candidate list. */
    static long[] oracle(int n, int[][] edges, int src, int dst) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][2];
        for (long[] r : d) Arrays.fill(r, inf);
        d[src][0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                for (int s = 0; s < 2; s++) {
                    if (d[e[0]][s] < inf && d[e[0]][s] + e[2] < d[e[1]][s]) { d[e[1]][s] = d[e[0]][s] + e[2]; changed = true; }
                }
                if (d[e[0]][0] < inf && d[e[0]][0] + e[2] / 2 < d[e[1]][1]) { d[e[1]][1] = d[e[0]][0] + e[2] / 2; changed = true; }
            }
        }
        long ex = Math.min(d[dst][0], d[dst][1]);
        List<long[]> cand = new ArrayList<>();
        cand.add(new long[] {0, src, 0});
        boolean[] closed = new boolean[n];
        long pr = -1;
        while (!cand.isEmpty()) {
            int bi = 0;
            for (int i = 1; i < cand.size(); i++) {
                long[] a = cand.get(i), b = cand.get(bi);
                if (a[0] < b[0] || (a[0] == b[0] && (a[1] < b[1] || (a[1] == b[1] && a[2] < b[2])))) bi = i;
            }
            long[] t = cand.remove(bi);
            int u = (int) t[1];
            if (closed[u]) continue;
            closed[u] = true;
            if (u == dst) { pr = t[0]; break; }
            for (int[] e : edges) {
                if (e[0] != u) continue;
                cand.add(new long[] {t[0] + e[2], e[1], t[2]});
                if (t[2] == 0) cand.add(new long[] {t[0] + e[2] / 2, e[1], 1});
            }
        }
        return new long[] {ex >= inf ? -1 : ex, pr};
    }

    public static void main(String[] args) {
        // Example 1: the cheapest arrival at node 1 spends the coupon, but the best route keeps it.
        if (!Arrays.equals(both(4, new int[][] {{0, 1, 8}, {1, 2, 2}, {2, 3, 100}, {0, 2, 30}}, 0, 3), new long[] {60, 106})) throw new AssertionError("ex1");
        // Example 2: both searches agree when no early coupon is wasted.
        if (!Arrays.equals(both(3, new int[][] {{0, 1, 7}, {1, 2, 9}, {0, 2, 20}}, 0, 2), new long[] {10, 10})) throw new AssertionError("ex2");
        // Unreachable target gives -1 for both entries.
        if (!Arrays.equals(both(3, new int[][] {{0, 1, 5}}, 0, 2), new long[] {-1, -1})) throw new AssertionError("unreachable");
        // The pruned answer is never below the exact one, on random graphs, and both match the oracle.
        Random rnd = new Random(2423);
        int differ = 0;
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(30)};
            int s = rnd.nextInt(n);
            int d = rnd.nextInt(n);
            long[] got = both(n, edges, s, d);
            if (!Arrays.equals(got, oracle(n, edges, s, d))) throw new AssertionError("random " + t);
            if (got[0] >= 0 && got[1] < got[0]) throw new AssertionError("pruned below exact " + t);
            if (got[0] != got[1]) differ++;
        }
        // The two answers differ on some inputs, so the boundary case is real and not a rare accident.
        if (differ == 0) throw new AssertionError("no difference found");
    }
}
```

#### Solution: [Recognize] Shortest Path With Alternating Colors (LeetCode 1129)
<!-- id: sp-alternating-colors -->

**Approach.**
The method runs a breadth-first search over positions `(node, last)`, where `last` is 0 for a red arrival, 1 for a blue arrival and 2 for the start. A position with `last == 0` may take only blue edges, a position with `last == 1` only red edges, and the start position takes both. Each position is visited once, and the first visit gives its distance because every edge has length one. The distance of a node is the smaller distance of its red and blue positions, and `0` for node 0. A final pass counts the finite distances and takes their maximum.

The invariant is that the queue holds positions in nondecreasing distance, so a position marked visited already has its shortest alternating distance. One visited flag per node would discard a red arrival when a blue arrival came first, and then the red-only continuation could never run.

**Complexity.**
- **Time** is O(V + E), because the search has 3V positions and each edge is read from at most two positions.
- **Space** is O(V + E) for the two adjacency lists, the distance table and the queue.

```java run
import java.util.*;

public final class AlternatingColors {
    /**
     * Returns the shortest alternating-color walk length from node 0 to every node, or -1.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: queue distances never decrease, so the first visit of a position is its shortest.
     */
    static int[] shortest(int n, int[][] red, int[][] blue) {
        // adj.get(c) holds the outgoing lists of color c, where 0 is red and 1 is blue.
        List<List<List<Integer>>> adj = new ArrayList<>();
        for (int c = 0; c < 2; c++) {
            adj.add(new ArrayList<>());
            for (int v = 0; v < n; v++) adj.get(c).add(new ArrayList<>());
        }
        // Parallel edges and self loops are kept as given.
        for (int[] e : red) adj.get(0).get(e[0]).add(e[1]);
        for (int[] e : blue) adj.get(1).get(e[0]).add(e[1]);
        // dist[v][last] is -1 until the position (v, last) is first reached.
        int[][] dist = new int[n][3];
        for (int[] r : dist) Arrays.fill(r, -1);
        dist[0][2] = 0;
        // A plain array queue works because each of the 3n positions enters at most once.
        int[] queue = new int[3 * n];
        int head = 0;
        int tail = 0;
        queue[tail++] = 0 * 3 + 2;
        // The loop ends after every reachable position has been expanded.
        while (head < tail) {
            int cur = queue[head++];
            int u = cur / 3;
            int last = cur % 3;
            // Try both colors; the color equal to the last arrival is forbidden.
            for (int c = 0; c < 2; c++) {
                if (last == c) continue;
                // Each outgoing edge of this color is read once per allowed position.
                for (int v : adj.get(c).get(u)) {
                    // The first arrival at (v, c) is the shortest, so later arrivals are ignored.
                    if (dist[v][c] == -1) {
                        dist[v][c] = dist[u][last] + 1;
                        queue[tail++] = v * 3 + c;
                    }
                }
            }
        }
        // Combine the positions of each node into one answer.
        int[] ans = new int[n];
        for (int v = 0; v < n; v++) {
            int best = -1;
            for (int last = 0; last < 3; last++) {
                if (dist[v][last] != -1 && (best == -1 || dist[v][last] < best)) best = dist[v][last];
            }
            ans[v] = best;
        }
        return ans;
    }

    /** Oracle: repeated relaxation of (node, last) distances until nothing changes. */
    static int[] oracle(int n, int[][] red, int[][] blue) {
        int inf = 1 << 28;
        int[][] d = new int[n][3];
        for (int[] r : d) Arrays.fill(r, inf);
        d[0][2] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int c = 0; c < 2; c++) {
                int[][] es = c == 0 ? red : blue;
                for (int[] e : es) {
                    for (int last = 0; last < 3; last++) {
                        if (last == c || d[e[0]][last] >= inf) continue;
                        if (d[e[0]][last] + 1 < d[e[1]][c]) { d[e[1]][c] = d[e[0]][last] + 1; changed = true; }
                    }
                }
            }
        }
        int[] ans = new int[n];
        for (int v = 0; v < n; v++) {
            int b = Math.min(d[v][0], Math.min(d[v][1], d[v][2]));
            ans[v] = b >= inf ? -1 : b;
        }
        return ans;
    }

    /** Summary of a distance array: count of finite entries and the largest one. */
    static int[] summary(int[] d) {
        int count = 0;
        int max = 0;
        // Each node with a nonnegative distance is reached.
        for (int x : d) {
            if (x >= 0) { count++; max = Math.max(max, x); }
        }
        return new int[] {count, max};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(summary(shortest(3, new int[][] {{0, 1}, {1, 2}}, new int[][] {})), new int[] {2, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(summary(shortest(5, new int[][] {{0, 1}, {2, 3}, {3, 4}}, new int[][] {{1, 2}, {1, 3}, {0, 0}, {4, 4}})), new int[] {5, 3})) throw new AssertionError("ex2");
        // The trace graph: node 2 is reached at distance 1 by red, but node 3 needs the blue arrival at distance 2.
        if (!Arrays.equals(shortest(4, new int[][] {{0, 1}, {0, 2}, {2, 3}}, new int[][] {{1, 2}, {1, 0}}), new int[] {0, 1, 1, 3})) throw new AssertionError("trace graph");
        // Random multigraphs with self loops against the relaxation oracle.
        Random rnd = new Random(2433);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] red = new int[rnd.nextInt(10)][];
            int[][] blue = new int[rnd.nextInt(10)][];
            for (int i = 0; i < red.length; i++) red[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            for (int i = 0; i < blue.length; i++) blue[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(shortest(n, red, blue), oracle(n, red, blue))) throw new AssertionError("random " + t);
        }
    }
}
```
