<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Limit A Route By Stops

#### Solution: [Build] At Most Two Edges (Author exercise)
<!-- id: sp-at-most-two-edges -->

**Approach.**
The method keeps one array of costs, with infinity for cities that no route reaches yet. Each of the two passes copies the array first. It then reads the flight start only from the old array and writes the improved cost into the copy. The copy replaces the old array when the pass ends. Because no pass reads its own writes, pass `j` adds exactly one flight to the routes of pass `j - 1`.

The invariant is that after pass `j` the array holds the lowest cost over routes with at most `j` flights. Starting the copy from the old values keeps routes that need fewer flights. The final loop turns infinity into the required `-1`.

**Complexity.**
- **Time** is O(E), because two passes each read every flight once and copy an array of length n.
- **Space** is O(V) for the old array and its copy.

```java run
import java.util.*;

public final class AtMostTwoEdges {
    /**
     * Returns the lowest cost from city 0 to each city with at most two flights.
     * Time: O(E). Space: O(V).
     * Invariant: after pass j the array holds the minimum over routes of at most j flights.
     */
    static long[] withinTwo(int n, int[][] flights) {
        // INF marks an unreached city and leaves room for one addition without overflow.
        final long INF = Long.MAX_VALUE / 4;
        long[] best = new long[n];
        // Every city starts unreached except the source.
        Arrays.fill(best, INF);
        best[0] = 0;
        // Exactly two passes run, one for each allowed flight.
        for (int pass = 0; pass < 2; pass++) {
            // The copy is the new row; best stays frozen during the pass.
            long[] next = best.clone();
            // Each flight is read once per pass, which gives the O(E) term.
            for (int[] f : flights) {
                // A flight offers a price only when its start city is reached in the frozen row.
                if (best[f[0]] < INF && best[f[0]] + f[2] < next[f[1]]) {
                    // The lower offer replaces the stored cost of the end city.
                    next[f[1]] = best[f[0]] + f[2];
                }
            }
            // The finished row becomes the frozen row of the next pass.
            best = next;
        }
        // Unreached cities map to the required sentinel.
        for (int v = 0; v < n; v++) if (best[v] >= INF) best[v] = -1;
        return best;
    }

    /** Oracle: tries every walk of at most two flights from city 0. */
    static long[] oracle(int n, int[][] flights) {
        long[] out = new long[n];
        Arrays.fill(out, -1);
        out[0] = 0;
        for (int[] a : flights) {
            if (a[0] == 0) {
                if (out[a[1]] < 0 || a[2] < out[a[1]]) out[a[1]] = a[2];
                for (int[] b : flights) {
                    if (b[0] == a[1] && (out[b[1]] < 0 || a[2] + b[2] < out[b[1]])) out[b[1]] = a[2] + b[2];
                }
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(withinTwo(4, new int[][] {{0, 1, 10}, {1, 2, 10}, {2, 3, 10}, {0, 2, 50}}), new long[] {0, 10, 20, 60})) throw new AssertionError("ex1");
        if (!Arrays.equals(withinTwo(3, new int[][] {{0, 1, 5}, {1, 2, 5}, {2, 0, 5}}), new long[] {0, 5, 10})) throw new AssertionError("ex2");
        // Java facts used in the prose: clone gives an independent array, and int addition wraps.
        long[] a = {1, 2};
        long[] b = a.clone();
        b[0] = 9;
        if (a[0] != 1) throw new AssertionError("clone is independent");
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("int overflow");
        if (Long.MAX_VALUE / 4 + 1000 < 0) throw new AssertionError("INF headroom");
        // Random graphs with repeats and self loops against the walk oracle.
        Random rnd = new Random(2404);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = rnd.nextInt(12);
            int[][] flights = new int[m][];
            for (int i = 0; i < m; i++) flights[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(20)};
            if (!Arrays.equals(withinTwo(n, flights), oracle(n, flights))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Cost By Stops Used (Author exercise)
<!-- id: sp-cost-by-stops-used -->

**Approach.**
The method allocates a table with `limit + 1` rows. Row 0 holds 0 for `src` and infinity elsewhere. Each later row starts as a copy of the row above it, and then every flight offers its price from the row above to its end city. No code changes a row after it is built, so a flight cannot read a value of its own row.

The invariant is that row `j` holds the lowest cost over routes with at most `j` flights. Copying keeps every earlier option, so an entry never rises from one row to the next. A final pass converts infinity to `-1` in every row.

**Complexity.**
- **Time** is O(limit · (V + E)), because each of the `limit` rows copies V entries and reads E flights.
- **Space** is O(limit · V) for the stored table.

```java run
import java.util.*;

public final class CostByStopsUsed {
    /**
     * Returns the table of lowest costs for at most j flights, for j from 0 to limit.
     * Time: O(limit * (V + E)). Space: O(limit * V).
     * Invariant: row j is final and holds the minimum over routes of at most j flights.
     */
    static long[][] table(int n, int[][] flights, int src, int limit) {
        // INF marks an unreached city and survives one addition.
        final long INF = Long.MAX_VALUE / 4;
        long[][] rows = new long[limit + 1][n];
        // Row 0 knows only the source.
        Arrays.fill(rows[0], INF);
        rows[0][src] = 0;
        // One row is built per allowed flight, which gives the limit factor.
        for (int j = 1; j <= limit; j++) {
            // The new row starts from the row above, which keeps shorter routes.
            rows[j] = rows[j - 1].clone();
            // Each flight is read once per row.
            for (int[] f : flights) {
                // The offer reads the finished row above, never the row under construction.
                if (rows[j - 1][f[0]] < INF && rows[j - 1][f[0]] + f[2] < rows[j][f[1]]) {
                    rows[j][f[1]] = rows[j - 1][f[0]] + f[2];
                }
            }
        }
        // Unreached entries map to the required sentinel in every row.
        for (long[] row : rows) for (int v = 0; v < n; v++) if (row[v] >= INF) row[v] = -1;
        return rows;
    }

    /** Oracle: enumerates every walk of at most j flights by recursion for each row. */
    static long[][] oracle(int n, int[][] flights, int src, int limit) {
        long[][] out = new long[limit + 1][n];
        for (int j = 0; j <= limit; j++) {
            Arrays.fill(out[j], -1);
            walk(flights, src, 0, j, out[j]);
        }
        return out;
    }

    private static void walk(int[][] flights, int city, long cost, int left, long[] best) {
        if (best[city] < 0 || cost < best[city]) best[city] = cost;
        if (left == 0) return;
        for (int[] f : flights) if (f[0] == city) walk(flights, f[1], cost + f[2], left - 1, best);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        long[][] e1 = {{0, -1, -1, -1}, {0, 10, 50, -1}, {0, 10, 20, 60}};
        if (!Arrays.deepEquals(table(4, new int[][] {{0, 1, 10}, {1, 2, 10}, {2, 3, 10}, {0, 2, 50}}, 0, 2), e1)) throw new AssertionError("ex1");
        long[][] e2 = {{0, -1, -1}, {0, 7, 9}, {0, 7, 8}, {0, 7, 8}};
        if (!Arrays.deepEquals(table(3, new int[][] {{0, 1, 7}, {1, 2, 1}, {0, 2, 9}}, 0, 3), e2)) throw new AssertionError("ex2");
        // Random graphs against the walk oracle, with entries that never rise between rows.
        Random rnd = new Random(2414);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = rnd.nextInt(11);
            int[][] flights = new int[m][];
            for (int i = 0; i < m; i++) flights[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(20)};
            int src = rnd.nextInt(n);
            int limit = rnd.nextInt(5);
            long[][] got = table(n, flights, src, limit);
            if (!Arrays.deepEquals(got, oracle(n, flights, src, limit))) throw new AssertionError("random " + t);
            for (int j = 1; j <= limit; j++) {
                for (int v = 0; v < n; v++) {
                    if (got[j - 1][v] >= 0 && (got[j][v] < 0 || got[j][v] > got[j - 1][v])) throw new AssertionError("monotone " + t);
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Direct Flight And K Zero (Author exercise)
<!-- id: sp-direct-flight-k-zero -->

**Approach.**
The method converts `k` stops into `limit = k + 1` flights, so `k = 0` allows exactly one pass and therefore a direct flight. It runs the pass loop with a frozen copy and watches the cost of `dst`. Prices are positive, so the cost of `dst` falls only when a pass finds a cheaper route that needs the new flight. The method stores the number of the last pass that lowered the cost, which is the first pass that reaches the final cost.

The invariant is that `firstPass` is the smallest flight count whose layer already holds the cost of `dst` seen so far. The start layer gives `{0, 0}` when `src == dst`, and positive prices keep that answer from improving. A destination that stays at infinity returns `{-1, -1}`.

**Complexity.**
- **Time** is O((k + 1) · (V + E)), because each pass reads E flights and copies V entries.
- **Space** is O(V) for the frozen array and its copy.

```java run
import java.util.*;

public final class DirectFlightKZero {
    /**
     * Returns {lowest cost, fewest flights for that cost} within k stops, or {-1, -1}.
     * Time: O((k + 1) * (V + E)). Space: O(V).
     * Invariant: firstPass is the earliest pass after which dst holds its current cost.
     */
    static int[] cheapest(int n, int[][] flights, int src, int dst, int k) {
        // INF marks an unreached city and survives one addition.
        final long INF = Long.MAX_VALUE / 4;
        // Stops translate to flights by adding one, so k = 0 gives a single pass.
        int limit = k + 1;
        long[] best = new long[n];
        Arrays.fill(best, INF);
        best[src] = 0;
        // The empty route already reaches dst when the ends are equal.
        int firstPass = 0;
        // One pass per allowed flight.
        for (int pass = 1; pass <= limit; pass++) {
            // The frozen row is copied so that the pass adds exactly one flight.
            long[] next = best.clone();
            // Each flight is read once per pass.
            for (int[] f : flights) {
                if (best[f[0]] < INF && best[f[0]] + f[2] < next[f[1]]) next[f[1]] = best[f[0]] + f[2];
            }
            // A strict drop at dst means this pass found a cheaper route with this many flights.
            if (next[dst] < best[dst]) firstPass = pass;
            best = next;
        }
        // An unreached destination returns the sentinel pair.
        if (best[dst] >= INF) return new int[] {-1, -1};
        return new int[] {(int) best[dst], firstPass};
    }

    /** Oracle: enumerates every walk of at most k + 1 flights and keeps the best (cost, flights). */
    static int[] oracle(int n, int[][] flights, int src, int dst, int k) {
        long[] best = {Long.MAX_VALUE, Long.MAX_VALUE};
        walk(flights, src, dst, 0, 0, k + 1, best);
        if (best[0] == Long.MAX_VALUE) return new int[] {-1, -1};
        return new int[] {(int) best[0], (int) best[1]};
    }

    private static void walk(int[][] flights, int city, int dst, long cost, int used, int limit, long[] best) {
        if (city == dst && (cost < best[0] || (cost == best[0] && used < best[1]))) {
            best[0] = cost;
            best[1] = used;
        }
        if (used == limit) return;
        for (int[] f : flights) if (f[0] == city) walk(flights, f[1], dst, cost + f[2], used + 1, limit, best);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] g = {{0, 1, 10}, {1, 2, 10}, {2, 3, 10}, {0, 2, 50}, {0, 3, 70}};
        if (!Arrays.equals(cheapest(4, g, 0, 3, 0), new int[] {70, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(cheapest(3, new int[][] {{0, 1, 4}}, 2, 2, 0), new int[] {0, 0})) throw new AssertionError("ex2");
        // The same graph with more stops shows the translation of k into flights.
        if (!Arrays.equals(cheapest(4, g, 0, 3, 1), new int[] {60, 2})) throw new AssertionError("k1");
        if (!Arrays.equals(cheapest(4, g, 0, 3, 2), new int[] {30, 3})) throw new AssertionError("k2");
        // Random graphs against the walk oracle, including equal ends and unreachable targets.
        Random rnd = new Random(2424);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = rnd.nextInt(11);
            int[][] flights = new int[m][];
            for (int i = 0; i < m; i++) flights[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(20)};
            int src = rnd.nextInt(n);
            int dst = rnd.nextInt(n);
            int k = rnd.nextInt(5);
            if (!Arrays.equals(cheapest(n, flights, src, dst, k), oracle(n, flights, src, dst, k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: sp-cheapest-flights-k-stops -->

**Approach.**
The method runs a heap search over states of city and flights used. The heap orders states by cost, so the first state popped for `dst` is the cheapest legal route. An array `fewest` stores, for each city, the smallest flight count among states already popped there. A state popped later costs at least as much as every earlier pop. If its flight count is not lower than `fewest[city]`, an earlier state dominates it, and the method discards it.

The invariant is that every state expanded so far is either undominated or the first at its city. The method records states with `k + 1` flights but never expands them. Every state in the heap therefore has at most `k + 1` flights. A heap that runs empty means no legal route exists.

**Complexity.**
- **Time** is O(k · E log(k · E)), because each city expands at most `k + 1` times and each expansion pushes at most its out-degree. Each push costs one heap operation.
- **Space** is O(k · E) for the heap entries, plus O(V + E) for the adjacency list.

```java run
import java.util.*;

public final class CheapestFlightsKStops {
    /**
     * Returns the lowest price of a route with at most k stops, or -1.
     * Time: O(k * E log(k * E)). Space: O(k * E).
     * Invariant: a popped state is skipped only when an earlier pop at its city used no more flights.
     */
    static int cheapest(int n, int[][] flights, int src, int dst, int k) {
        // The adjacency list keeps each flight as {to, price}.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] f : flights) adj.get(f[0]).add(new int[] {f[1], f[2]});
        // fewest[c] is the smallest flight count among states popped at city c.
        int[] fewest = new int[n];
        Arrays.fill(fewest, Integer.MAX_VALUE);
        // The heap orders states {cost, city, flights used} by cost alone.
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, src, 0});
        // Each pop either ends the search, is discarded, or expands one state.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int city = (int) top[1];
            int used = (int) top[2];
            // The first pop of dst has the lowest cost among states within the limit.
            if (city == dst) return (int) top[0];
            // An earlier pop cost no more and used no more flights, so this state is dominated.
            if (used >= fewest[city]) continue;
            fewest[city] = used;
            // A state with all flights used cannot continue.
            if (used == k + 1) continue;
            // Each outgoing flight creates one state with one more flight used.
            for (int[] e : adj.get(city)) heap.add(new long[] {top[0] + e[1], e[0], used + 1});
        }
        // An empty heap means no route within the limit reaches dst.
        return -1;
    }

    /** Oracle: enumerates every walk of at most k + 1 flights and keeps the cheapest one at dst. */
    static int oracle(int n, int[][] flights, int src, int dst, int k) {
        long[] best = {Long.MAX_VALUE};
        walk(flights, src, dst, 0, 0, k + 1, best);
        return best[0] == Long.MAX_VALUE ? -1 : (int) best[0];
    }

    private static void walk(int[][] flights, int city, int dst, long cost, int used, int limit, long[] best) {
        if (city == dst && cost < best[0]) best[0] = cost;
        if (used == limit) return;
        for (int[] f : flights) if (f[0] == city) walk(flights, f[1], dst, cost + f[2], used + 1, limit, best);
    }

    /** Helper that keeps one distance per city, to show the false friend of the lesson. */
    static long plain(int n, int[][] flights, int src, int dst) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        for (int round = 0; round < n; round++) {
            for (int[] f : flights) {
                if (dist[f[0]] != Long.MAX_VALUE && dist[f[0]] + f[2] < dist[f[1]]) dist[f[1]] = dist[f[0]] + f[2];
            }
        }
        return dist[dst] == Long.MAX_VALUE ? -1 : dist[dst];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] g1 = {{0, 1, 100}, {1, 2, 100}, {2, 0, 100}, {1, 3, 600}, {2, 3, 200}};
        if (cheapest(4, g1, 0, 3, 1) != 700) throw new AssertionError("ex1");
        int[][] g2 = {{0, 1, 100}, {1, 2, 100}, {0, 2, 500}};
        if (cheapest(3, g2, 0, 2, 0) != 500) throw new AssertionError("ex2");
        // One distance per city gives 200 on the second example, which breaks the limit.
        if (plain(3, g2, 0, 2) != 200) throw new AssertionError("false friend");
        // Random graphs without repeated pairs against the walk oracle.
        Random rnd = new Random(2434);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(5);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++) {
                for (int b = 0; b < n; b++) {
                    if (a != b && rnd.nextInt(3) == 0) list.add(new int[] {a, b, 1 + rnd.nextInt(30)});
                }
            }
            int[][] flights = list.toArray(new int[0][]);
            int src = rnd.nextInt(n);
            int dst = (src + 1 + rnd.nextInt(n - 1)) % n;
            int k = rnd.nextInt(n);
            if (cheapest(n, flights, src, dst, k) != oracle(n, flights, src, dst, k)) throw new AssertionError("random " + t);
        }
    }
}
```
