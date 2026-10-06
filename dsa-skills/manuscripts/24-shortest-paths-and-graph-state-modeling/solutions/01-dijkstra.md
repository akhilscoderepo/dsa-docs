<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Cheapest Routes

#### Solution: [Build] Relax One Edge (Author exercise)
<!-- id: sp-dijkstra-relax-edge -->

**Approach.**
The method first tests whether the source distance is the unknown marker. An unknown source cannot offer a route, and adding a weight to `Long.MAX_VALUE` would wrap around to a negative number that looks like a great bargain. When the source is finite, the method computes the proposal as a `long` sum and compares it with the current value of the target. It writes the proposal only when it is strictly smaller and reports that a change happened.

The invariant is that every finite entry of `dist` is the cost of a real route. A relaxation stores `dist[u] + w`, which is the cost of the known route to `u` extended by one road, so the invariant survives. A strict comparison also keeps equal proposals from reporting a change, which a caller needs in order to know when a heap entry is worth adding.

**Complexity.**
- **Time** is O(1), because the method reads two entries and writes at most one.
- **Space** is O(1), because it allocates nothing beyond one local `long`.

```java run
import java.util.*;

public final class RelaxOneEdge {
    /**
     * Relaxes the road u to v and reports whether dist[v] changed.
     * Time: O(1). Space: O(1).
     * Invariant: every finite entry of dist is the cost of an actual route.
     */
    static boolean relax(long[] dist, int u, int v, int w) {
        // An unknown source distance offers no route, and adding to it would overflow.
        if (dist[u] == Long.MAX_VALUE) return false;
        // The sum is a long, so two int-sized values cannot wrap.
        long proposal = dist[u] + w;
        // Only a strictly cheaper route replaces the stored value.
        if (proposal < dist[v]) {
            dist[v] = proposal;
            return true;
        }
        return false;
    }

    /** Oracle: the same decision on a copy of the array. */
    static boolean oracle(long[] copy, int u, int v, int w) {
        boolean known = copy[u] != Long.MAX_VALUE;
        long best = copy[v];
        if (known && copy[u] + (long) w < best) {
            copy[v] = copy[u] + (long) w;
            return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        long[] a = {0, 9, 2};
        if (!relax(a, 2, 1, 3) || !Arrays.equals(a, new long[] {0, 5, 2})) throw new AssertionError("ex1");
        long[] b = {Long.MAX_VALUE, 4, Long.MAX_VALUE};
        if (relax(b, 0, 2, 5) || !Arrays.equals(b, new long[] {Long.MAX_VALUE, 4, Long.MAX_VALUE})) throw new AssertionError("ex2");
        // Java fact: adding a positive int to Long.MAX_VALUE wraps to a negative value.
        if (Long.MAX_VALUE + 5 >= 0) throw new AssertionError("wraparound");
        // An equal proposal is not an improvement.
        long[] c = {0, 5};
        if (relax(c, 0, 1, 5)) throw new AssertionError("equal");
        // Random arrays against the oracle, including unknown entries and the largest weight.
        Random rnd = new Random(2401);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(5);
            long[] d = new long[n];
            for (int i = 0; i < n; i++) d[i] = rnd.nextInt(4) == 0 ? Long.MAX_VALUE : (long) rnd.nextInt(1_000_000) * 1000;
            long[] copy = d.clone();
            int u = rnd.nextInt(n), v = rnd.nextInt(n);
            int w = rnd.nextInt(3) == 0 ? 2_000_000_000 : rnd.nextInt(50);
            boolean r1 = relax(d, u, v, w);
            boolean r2 = oracle(copy, u, v, w);
            if (r1 != r2 || !Arrays.equals(d, copy)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Small Weighted Graph (Author exercise)
<!-- id: sp-dijkstra-small-graph -->

**Approach.**
The method builds an adjacency list and a `dist` array, and pushes the pair of cost 0 and town 0. It then removes the smallest entry repeatedly. The heap compares cost first and town index second, which makes the order of equal costs fixed. An entry whose cost exceeds `dist` of its town is stale, so the method skips it. Every other removal appends the town to the answer and relaxes the roads of that town.

The invariant is that the first nonstale removal of a town carries its final distance, and removals come in nondecreasing cost. Zero weights keep the argument valid, because a relaxed entry can equal the current cost but never fall below it. An equal-cost entry pushed later still sorts by town index, so the tie rule applies to it as well. A duplicate nonstale entry for an already listed town cannot occur, since a second entry needs a strictly smaller cost than the first.

**Complexity.**
- **Time** is O(E log E), because each road adds at most one heap entry and each entry costs O(log E) to insert and remove.
- **Space** is O(V + E) for the adjacency list, the distance array and a heap of at most E entries.

```java run
import java.util.*;

public final class SmallWeightedGraph {
    /**
     * Returns the towns in the order of their final removal from the heap.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: a nonstale removal holds the final distance of its town.
     */
    static int[] removalOrder(int n, int[][] roads) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] r : roads) adj.get(r[0]).add(new int[] {r[1], r[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        // Cost decides first, and the town index breaks a tie.
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        heap.add(new long[] {0, 0});
        List<Integer> order = new ArrayList<>();
        // Each pass removes one entry, and the heap receives at most one entry per road.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            // A stale entry has a cost above the current distance and is skipped.
            if (top[0] > dist[u]) continue;
            order.add(u);
            for (int[] r : adj.get(u)) {
                long next = top[0] + r[1];
                // Only a strictly cheaper route creates a new entry.
                if (next < dist[r[0]]) {
                    dist[r[0]] = next;
                    heap.add(new long[] {next, r[0]});
                }
            }
        }
        int[] out = new int[order.size()];
        for (int i = 0; i < out.length; i++) out[i] = order.get(i);
        return out;
    }

    /** Oracle: repeated linear scan for the smallest unfinished town, with the lower index winning ties. */
    static int[] oracle(int n, int[][] roads) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        boolean[] done = new boolean[n];
        List<Integer> order = new ArrayList<>();
        while (true) {
            int best = -1;
            for (int v = 0; v < n; v++) {
                if (!done[v] && dist[v] != Long.MAX_VALUE && (best == -1 || dist[v] < dist[best])) best = v;
            }
            if (best == -1) break;
            done[best] = true;
            order.add(best);
            for (int[] r : roads) {
                if (r[0] == best && dist[best] + r[2] < dist[r[1]]) dist[r[1]] = dist[best] + r[2];
            }
        }
        int[] out = new int[order.size()];
        for (int i = 0; i < out.length; i++) out[i] = order.get(i);
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] g1 = {{0, 1, 7}, {0, 2, 2}, {2, 1, 3}, {2, 3, 8}, {1, 4, 1}, {3, 4, 2}, {4, 5, 4}, {3, 5, 1}};
        if (!Arrays.equals(removalOrder(6, g1), new int[] {0, 2, 1, 4, 3, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(removalOrder(4, new int[][] {{0, 1, 0}, {0, 2, 0}, {2, 3, 1}, {1, 3, 1}}), new int[] {0, 1, 2, 3})) throw new AssertionError("ex2");
        // Random graphs with small weights, so ties and zero weights occur often.
        Random rnd = new Random(2402);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(16);
            int[][] roads = new int[m][];
            for (int i = 0; i < m; i++) roads[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(4)};
            if (!Arrays.equals(removalOrder(n, roads), oracle(n, roads))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Unreachable Vertex And Large Sum (Author exercise)
<!-- id: sp-dijkstra-unreachable-large -->

**Approach.**
The method runs the heap search of this lesson with `Long.MAX_VALUE` as the marker of an unknown distance. Only a finite cost leaves the heap, so the sum of cost and weight never starts from the marker. The sum is computed in `long`, which holds any path, since the largest total is below 2000 times 2000000000, about 4 times 10 to the 12. After the search ends, a final loop replaces every remaining marker with minus one.

The invariant is that every finite entry of `dist` is the cost of a real route, and every stale entry is skipped before relaxation. A town that no route reaches never enters the heap, so it keeps the marker until the final conversion. Converting at the end, and not during the search, keeps the comparison `next < dist[v]` valid for towns that are still unknown.

**Complexity.**
- **Time** is O(E log E), because each successful relaxation adds one heap entry that costs O(log E).
- **Space** is O(V + E) for the adjacency list, the `long` array and the heap.

```java run
import java.util.*;

public final class UnreachableLargeSum {
    /**
     * Returns the minimum route cost from town 0 to every town, or -1 when unreachable.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: finite entries of dist are real route costs.
     */
    static long[] distances(int n, int[][] roads) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] r : roads) adj.get(r[0]).add(new int[] {r[1], r[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, 0});
        // Each removal either skips a stale entry or relaxes the roads of one town.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] > dist[u]) continue;
            for (int[] r : adj.get(u)) {
                // The sum uses long arithmetic, and top[0] is always finite here.
                long next = top[0] + r[1];
                if (next < dist[r[0]]) {
                    dist[r[0]] = next;
                    heap.add(new long[] {next, r[0]});
                }
            }
        }
        // The marker becomes -1 only after the search, so comparisons stay valid during it.
        for (int v = 0; v < n; v++) if (dist[v] == Long.MAX_VALUE) dist[v] = -1;
        return dist;
    }

    /** Oracle: repeated passes over all roads until nothing improves, using long arithmetic. */
    static long[] oracle(int n, int[][] roads) {
        long[] d = new long[n];
        Arrays.fill(d, -1);
        d[0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] r : roads) {
                if (d[r[0]] >= 0 && (d[r[1]] == -1 || d[r[0]] + r[2] < d[r[1]])) {
                    d[r[1]] = d[r[0]] + r[2];
                    changed = true;
                }
            }
        }
        return d;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(distances(3, new int[][] {{0, 1, 2_000_000_000}, {1, 2, 2_000_000_000}}), new long[] {0, 2_000_000_000L, 4_000_000_000L})) throw new AssertionError("ex1");
        if (!Arrays.equals(distances(4, new int[][] {{0, 1, 5}, {2, 3, 1}}), new long[] {0, 5, -1, -1})) throw new AssertionError("ex2");
        // Java fact: the same sum in int arithmetic wraps to a negative value.
        int wrapped = 2_000_000_000 + 2_000_000_000;
        if (wrapped >= 0) throw new AssertionError("int overflow");
        // Random graphs with large and small weights, many of them disconnected.
        Random rnd = new Random(2403);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(12);
            int[][] roads = new int[m][];
            for (int i = 0; i < m; i++) roads[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(3) == 0 ? 2_000_000_000 - rnd.nextInt(3) : rnd.nextInt(6)};
            if (!Arrays.equals(distances(n, roads), oracle(n, roads))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-dijkstra-network-delay -->

**Approach.**
The nodes are labeled from 1, so the method shifts every label down by one and runs the heap search from `k - 1`. Distances fit in `int` here, but the method keeps `long` for the habit of the lesson. After the search, one pass over `dist` keeps the largest finite value and counts the entries that still hold the unknown marker. The source has distance 0, so a network of one node returns a maximum of 0.

The invariant is that every nonstale removal holds a final distance, so the maximum over finite distances is the time at which the last reachable node hears the signal. Zero weights are allowed and keep the invariant, because a relaxation never lowers a cost below the cost of the entry that produced it. Unreached nodes never enter the heap, so they stay unknown and are counted, not compared.

**Complexity.**
- **Time** is O(E log E) for the search plus O(V) for the final pass.
- **Space** is O(V + E) for the adjacency list, the distance array and the heap.

```java run
import java.util.*;

public final class NetworkDelay {
    /**
     * Returns {largest finite arrival time, number of unreached nodes} for a signal from node k.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: a nonstale removal holds the final distance of its node.
     */
    static int[] delay(int n, int[][] times, int k) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Labels shift from 1..n to 0..n-1 so that they index the arrays.
        for (int[] t : times) adj.get(t[0] - 1).add(new int[] {t[1] - 1, t[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[k - 1] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, k - 1});
        // Each removal skips a stale entry or relaxes the links of one node.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] > dist[u]) continue;
            for (int[] r : adj.get(u)) {
                long next = top[0] + r[1];
                if (next < dist[r[0]]) {
                    dist[r[0]] = next;
                    heap.add(new long[] {next, r[0]});
                }
            }
        }
        // One pass separates finite arrival times from unreached nodes.
        long max = 0;
        int missed = 0;
        for (long d : dist) {
            if (d == Long.MAX_VALUE) missed++;
            else max = Math.max(max, d);
        }
        return new int[] {(int) max, missed};
    }

    /** Oracle: Floyd-Warshall on the full distance matrix, then the same summary. */
    static int[] oracle(int n, int[][] times, int k) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][n];
        for (long[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] t : times) d[t[0] - 1][t[1] - 1] = Math.min(d[t[0] - 1][t[1] - 1], t[2]);
        for (int m = 0; m < n; m++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][m] + d[m][j]);
        long max = 0;
        int missed = 0;
        for (int v = 0; v < n; v++) {
            if (d[k - 1][v] >= inf) missed++;
            else max = Math.max(max, d[k - 1][v]);
        }
        return new int[] {(int) max, missed};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(delay(4, new int[][] {{2, 1, 1}, {2, 3, 1}, {3, 4, 1}}, 2), new int[] {2, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(delay(3, new int[][] {{1, 2, 4}}, 1), new int[] {4, 1})) throw new AssertionError("ex2");
        // A single node needs no time and misses nobody.
        if (!Arrays.equals(delay(1, new int[0][], 1), new int[] {0, 0})) throw new AssertionError("single");
        // Random networks with zero weights, repeats and self loops.
        Random rnd = new Random(2404);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(14);
            int[][] times = new int[m][];
            for (int i = 0; i < m; i++) times[i] = new int[] {1 + rnd.nextInt(n), 1 + rnd.nextInt(n), rnd.nextInt(6)};
            int k = 1 + rnd.nextInt(n);
            if (!Arrays.equals(delay(n, times, k), oracle(n, times, k))) throw new AssertionError("random " + t);
        }
    }
}
```
