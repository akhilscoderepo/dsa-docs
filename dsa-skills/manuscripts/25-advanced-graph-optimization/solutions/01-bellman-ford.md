<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Negative Edges

#### Solution: [Build] One Relaxation Pass (Author exercise)
<!-- id: ga-bf-one-pass -->

**Approach.**
The method copies `dist` into a new array `next` and treats the original array as the snapshot of the previous pass. For each transfer, it skips the transfer when the source fee in the snapshot is the unknown marker. Otherwise it computes the proposal as a `long` sum of the snapshot fee and the weight. It writes the proposal into `next` only when the proposal is strictly smaller than the stored value. The method never reads from `next` and never writes into `dist`.

The invariant is that `next[v]` equals the smaller of the old fee of `v` and every proposal read from the old array. So no chain of updates uses more than one new transfer. The guard for the unknown marker matters in both directions. A positive weight added to `Long.MAX_VALUE` wraps to a negative number, and a negative weight gives a value just below the marker that looks like a real fee. The tests below assert both facts.

**Complexity.**
- **Time** is O(V + E), because the copy touches each account once and the loop touches each transfer once.
- **Space** is O(V) for the returned array, and the input array stays unchanged.

```java run
import java.util.*;

public final class BfOnePass {
    /**
     * Returns the fees after one pass in which every proposal reads the old array.
     * Time: O(V + E). Space: O(V).
     * Invariant: next[v] is the minimum of dist[v] and all proposals computed from dist.
     */
    static long[] onePass(long[] dist, int[][] edges) {
        // The copy is the only array that receives writes, so dist acts as the snapshot.
        long[] next = dist.clone();
        // Each transfer is visited once, so the loop costs O(E).
        for (int[] e : edges) {
            // An unknown source offers no route, and adding to the marker would corrupt the fee.
            if (dist[e[0]] == Long.MAX_VALUE) continue;
            // The proposal is a long sum of the old fee and the weight, so it cannot wrap here.
            long proposal = dist[e[0]] + e[2];
            // Only a strictly smaller proposal replaces the stored value.
            if (proposal < next[e[1]]) next[e[1]] = proposal;
        }
        // The caller receives the new array, and the input was never written.
        return next;
    }

    /** Oracle: for every account, scan all transfers and take the minimum directly. */
    static long[] oracle(long[] dist, int[][] edges) {
        long[] out = new long[dist.length];
        for (int v = 0; v < dist.length; v++) {
            long best = dist[v];
            for (int[] e : edges) {
                if (e[1] == v && dist[e[0]] != Long.MAX_VALUE && dist[e[0]] + e[2] < best) best = dist[e[0]] + e[2];
            }
            out[v] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        final long INF = Long.MAX_VALUE;
        // The two examples of the exercise.
        long[] a = {0, INF, INF, INF};
        long[] aCopy = a.clone();
        if (!Arrays.equals(onePass(a, new int[][] {{0, 1, 4}, {1, 2, -2}, {2, 3, 1}}), new long[] {0, 4, INF, INF})) throw new AssertionError("ex1");
        if (!Arrays.equals(a, aCopy)) throw new AssertionError("input changed");
        if (!Arrays.equals(onePass(new long[] {0, 5, INF}, new int[][] {{0, 1, 7}, {1, 2, -3}, {0, 2, 9}}), new long[] {0, 5, 2})) throw new AssertionError("ex2");
        // Java facts: a positive weight wraps the marker to a negative number, a negative weight stays near the marker.
        if (Long.MAX_VALUE + 5 >= 0) throw new AssertionError("wraparound");
        if (!(Long.MAX_VALUE + (-5) < Long.MAX_VALUE) || Long.MAX_VALUE + (-5) == Long.MAX_VALUE) throw new AssertionError("near marker");
        // Random arrays and transfers against the oracle, including unknown entries and loops.
        Random rnd = new Random(2501);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(6);
            long[] d = new long[n];
            for (int i = 0; i < n; i++) d[i] = rnd.nextInt(3) == 0 ? INF : rnd.nextInt(41) - 20;
            int m = rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(21) - 10};
            long[] copy = d.clone();
            if (!Arrays.equals(onePass(d, edges), oracle(d, edges))) throw new AssertionError("random " + t);
            if (!Arrays.equals(d, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Vary] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: ga-bf-flights-by-limit -->

**Approach.**
A route with at most `j` stops uses at most `j + 1` flights, so the method runs `k + 1` passes of the snapshot relaxation from `src`. After pass `p`, the array `dist` holds the lowest price over routes with at most `p` flights. The method reads `dist[dst]` right after each pass and stores it in slot `p - 1` of the answer, after converting the unknown marker to `Integer.MAX_VALUE`. The method does not stop early, because a later pass can still lower the price of the destination even when an earlier pass changed little.

The invariant is that after pass `p` each finite `dist[v]` is the lowest price using at most `p` flights, which needs the snapshot. Without the snapshot, a pass could chain several flights and report a price for a limit that is too small. A loop with a negative total causes no trouble, because the method always runs exactly `k + 1` passes and never waits for the fees to settle. The answer is non-increasing along its length, since a larger limit allows every route of a smaller limit.

**Complexity.**
- **Time** is O(k * (V + E)), because each of `k + 1` passes copies the array and scans every flight.
- **Space** is O(V) for `dist` and the snapshot, plus O(k) for the answer.

```java run
import java.util.*;

public final class BfFlightsByLimit {
    /**
     * Returns the lowest price from src to dst for each stop limit 0..k.
     * Time: O(k * (V + E)). Space: O(V + k).
     * Invariant: after pass p, dist[v] is the lowest price using at most p flights.
     */
    static int[] byLimit(int n, int[][] flights, int src, int dst, int k) {
        // Unknown prices use the largest long value, and the source costs nothing.
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        int[] answer = new int[k + 1];
        // One pass per allowed flight, which is k + 1 passes in total.
        for (int pass = 1; pass <= k + 1; pass++) {
            // The snapshot keeps this pass from chaining two flights.
            long[] prev = dist.clone();
            // Each flight is relaxed once per pass, which costs O(E).
            for (int[] f : flights) {
                // Skip flights that start at a city with no known price.
                if (prev[f[0]] == Long.MAX_VALUE) continue;
                long next = prev[f[0]] + f[2];
                // Keep the strictly cheaper price.
                if (next < dist[f[1]]) dist[f[1]] = next;
            }
            // The destination price after pass p belongs to the limit with p - 1 stops.
            answer[pass - 1] = dist[dst] == Long.MAX_VALUE ? Integer.MAX_VALUE : (int) dist[dst];
        }
        return answer;
    }

    /** Oracle: exhaustive search of every flight sequence with at most limit + 1 flights. */
    static int[] oracle(int n, int[][] flights, int src, int dst, int k) {
        int[] out = new int[k + 1];
        for (int j = 0; j <= k; j++) {
            out[j] = (int) Math.min(Integer.MAX_VALUE, search(flights, src, dst, j + 1));
        }
        return out;
    }

    /** Returns the lowest price from city to dst using at most left flights, or the long marker. */
    static long search(int[][] flights, int city, int dst, int left) {
        long best = city == dst ? 0 : Long.MAX_VALUE;
        if (left == 0) return best;
        for (int[] f : flights) {
            if (f[0] != city) continue;
            long rest = search(flights, f[1], dst, left - 1);
            if (rest != Long.MAX_VALUE) best = Math.min(best, rest + f[2]);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] f1 = {{0, 1, 100}, {1, 2, 100}, {2, 3, 100}, {0, 3, 500}};
        if (!Arrays.equals(byLimit(4, f1, 0, 3, 2), new int[] {500, 500, 300})) throw new AssertionError("ex1");
        int[][] f2 = {{0, 1, 50}, {1, 2, -20}, {0, 2, 40}};
        if (!Arrays.equals(byLimit(3, f2, 0, 2, 1), new int[] {40, 30})) throw new AssertionError("ex2");
        // A negative loop with a fixed pass count still terminates and matches the oracle.
        int[][] loop = {{0, 1, 1}, {1, 2, -5}, {2, 1, 1}, {2, 3, 1}};
        if (!Arrays.equals(byLimit(4, loop, 0, 3, 4), oracle(4, loop, 0, 3, 4))) throw new AssertionError("loop");
        // The answer never increases when the limit grows.
        int[] chain = byLimit(4, loop, 0, 3, 4);
        for (int i = 1; i < chain.length; i++) if (chain[i] > chain[i - 1]) throw new AssertionError("monotone");
        // Random small graphs with credits, loops and parallel flights.
        Random rnd = new Random(2502);
        for (int t = 0; t < 2000; t++) {
            int n = 2 + rnd.nextInt(5);
            int m = rnd.nextInt(11);
            int[][] fl = new int[m][];
            for (int i = 0; i < m; i++) fl[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(14) - 4};
            int src = rnd.nextInt(n);
            int dst = (src + 1 + rnd.nextInt(n - 1)) % n;
            int k = rnd.nextInt(n + 1);
            if (!Arrays.equals(byLimit(n, fl, src, dst, k), oracle(n, fl, src, dst, k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Unreachable And Negative Cycle (Author exercise)
<!-- id: ga-bf-unreachable-cycle -->

**Approach.**
The method runs up to n - 1 snapshot passes from account 0 and stops early when a pass changes nothing. Every transfer whose source fee is the unknown marker is skipped before any sum, so a negative weight never turns the marker into a fake fee. After the passes, one more loop looks at every transfer once. If some transfer can still lower a fee, the method returns an empty array. Otherwise it returns the fees with the marker left in place for unreachable accounts.

The invariant is that after pass `i`, each finite fee is the lowest fee over routes with at most `i` transfers. Suppose no negative cycle is reachable from account 0. Then some cheapest route to each reachable account repeats no account, so n - 1 passes make every fee exact and the extra loop finds nothing. With such a cycle, going around it lowers the fee of every account on it, so the fees never become stable and the extra loop finds an improvement. A negative cycle that account 0 cannot reach never produces a finite source fee, so the guard keeps it out of the computation and the answer stays valid.

**Complexity.**
- **Time** is O(V * (V + E)), because each of at most n - 1 passes copies the array and scans every transfer.
- **Space** is O(V) for `dist` and the snapshot.

```java run
import java.util.*;

public final class BfUnreachableCycle {
    /**
     * Returns the lowest fees from account 0, or an empty array when a negative cycle is reachable.
     * Time: O(V * (V + E)). Space: O(V).
     * Invariant: after pass i, each finite dist[v] is the lowest fee over routes with at most i transfers.
     */
    static long[] fees(int n, int[][] edges) {
        // The marker means no known route, and only account 0 starts with a fee.
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        // A cheapest route without a repeated account has at most n - 1 transfers.
        for (int pass = 1; pass <= n - 1; pass++) {
            // The snapshot keeps the pass from using more than one new transfer.
            long[] prev = dist.clone();
            boolean changed = false;
            // Each transfer is checked once per pass, which costs O(E).
            for (int[] e : edges) {
                // The guard keeps the marker out of every sum.
                if (prev[e[0]] == Long.MAX_VALUE) continue;
                long next = prev[e[0]] + e[2];
                if (next < dist[e[1]]) {
                    dist[e[1]] = next;
                    changed = true;
                }
            }
            // A pass without change repeats forever, so the fees are final.
            if (!changed) return dist;
        }
        // The extra pass only reads, because one improvement already proves a reachable negative cycle.
        for (int[] e : edges) {
            if (dist[e[0]] != Long.MAX_VALUE && dist[e[0]] + e[2] < dist[e[1]]) return new long[0];
        }
        return dist;
    }

    /** Oracle: lowest cost of walks with exactly L transfers for every L, compared at limits n - 1 and 2n. */
    static long[] oracle(int n, int[][] edges) {
        long inf = Long.MAX_VALUE;
        long[] cur = new long[n];
        Arrays.fill(cur, inf);
        cur[0] = 0;
        long[] best = cur.clone();
        long[] bestShort = null;
        // Walks of every length up to 2n are enumerated by dynamic programming over the length.
        for (int len = 1; len <= 2 * n; len++) {
            long[] nxt = new long[n];
            Arrays.fill(nxt, inf);
            for (int[] e : edges) {
                if (cur[e[0]] != inf && cur[e[0]] + e[2] < nxt[e[1]]) nxt[e[1]] = cur[e[0]] + e[2];
            }
            cur = nxt;
            for (int v = 0; v < n; v++) best[v] = Math.min(best[v], cur[v]);
            if (len == n - 1) bestShort = best.clone();
        }
        if (bestShort == null) bestShort = new long[] {0};
        // A difference between the two limits proves that a longer walk is cheaper.
        return Arrays.equals(bestShort, best) ? bestShort : new long[0];
    }

    public static void main(String[] args) {
        final long INF = Long.MAX_VALUE;
        // The two examples of the exercise.
        if (fees(3, new int[][] {{0, 1, 5}, {1, 2, -3}, {2, 1, 1}}).length != 0) throw new AssertionError("ex1");
        long[] ex2 = fees(5, new int[][] {{0, 1, 3}, {1, 2, -2}, {3, 4, -5}, {4, 3, 1}});
        if (!Arrays.equals(ex2, new long[] {0, 3, 1, INF, INF})) throw new AssertionError("ex2");
        // Java fact: with a negative weight the marker plus the weight is below the marker and looks like a fee.
        if (!(INF + (-5) < INF)) throw new AssertionError("fake fee");
        // One account with a negative self loop is a reachable negative cycle.
        if (fees(1, new int[][] {{0, 0, -1}}).length != 0) throw new AssertionError("self loop");
        // One account with a nonnegative self loop keeps fee 0.
        if (!Arrays.equals(fees(1, new int[][] {{0, 0, 2}}), new long[] {0})) throw new AssertionError("plain loop");
        // Large weights stay exact in long arithmetic.
        if (!Arrays.equals(fees(3, new int[][] {{0, 1, 1_000_000_000}, {1, 2, 1_000_000_000}}), new long[] {0, 1_000_000_000L, 2_000_000_000L})) throw new AssertionError("large");
        // Random graphs with negative weights and unreachable regions against the oracle.
        Random rnd = new Random(2503);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(13) - 4};
            if (!Arrays.equals(fees(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Negative-Edge Shortest Paths (Author exercise)
<!-- id: ga-bf-negative-edge-paths -->

**Approach.**
The statement guarantees that no negative cycle is reachable, so the extra detection pass is not needed. The method runs snapshot passes from account 0 and stops as soon as a pass changes nothing, with at most n - 1 passes. It then scans the accounts from 1 upward and keeps the account with the strictly lowest known fee. The strict comparison on an increasing index gives the smallest index on a tie. When no account other than 0 has a known fee, the method returns the pair of minus one and zero.

The invariant here says that each finite fee after pass `i` is minimal among routes of at most `i` transfers. The early stop is valid because an unchanged pass repeats forever. Negative fees do not break the scan, because the minimum is taken over final fees, not over a growing frontier. A negative loop among accounts that account 0 cannot reach is harmless, since the guard never lets a sum start from the unknown marker.

**Complexity.**
- **Time** is O(V * (V + E)) in the worst case, because each of up to n - 1 passes copies the array and scans every transfer.
- **Space** is O(V) for the fee array and the snapshot.

```java run
import java.util.*;

public final class BfNegativeEdgePaths {
    /** Number of passes that the last call used, which the tests read to check the early stop. */
    static int lastPasses;

    /**
     * Returns {account, fee} for the reachable account other than 0 with the lowest fee, or {-1, 0}.
     * Time: O(V * (V + E)). Space: O(V).
     * Invariant: after pass i, each finite fee is the lowest fee over routes with at most i transfers.
     */
    static long[] cheapestOther(int n, int[][] transfers) {
        // The marker means unreachable, and account 0 starts at fee 0.
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        lastPasses = 0;
        // At most n - 1 passes are needed, since no negative cycle is reachable.
        for (int pass = 1; pass <= n - 1; pass++) {
            lastPasses = pass;
            // The snapshot keeps every pass limited to one new transfer.
            long[] prev = dist.clone();
            boolean changed = false;
            // One scan of all transfers per pass costs O(E).
            for (int[] t : transfers) {
                // The guard keeps the marker out of every sum.
                if (prev[t[0]] == Long.MAX_VALUE) continue;
                long next = prev[t[0]] + t[2];
                if (next < dist[t[1]]) {
                    dist[t[1]] = next;
                    changed = true;
                }
            }
            // An unchanged pass means all fees are final.
            if (!changed) break;
        }
        int bestAccount = -1;
        // The scan from index 1 upward with a strict test keeps the smallest index on a tie.
        for (int v = 1; v < n; v++) {
            if (dist[v] != Long.MAX_VALUE && (bestAccount == -1 || dist[v] < dist[bestAccount])) bestAccount = v;
        }
        return bestAccount == -1 ? new long[] {-1, 0} : new long[] {bestAccount, dist[bestAccount]};
    }

    /** Oracle: depth-first search over routes that repeat no account, which suffices without negative cycles. */
    static long[] oracle(int n, int[][] transfers) {
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[0] = 0;
        boolean[] on = new boolean[n];
        on[0] = true;
        walk(transfers, 0, 0, on, best);
        int bestAccount = -1;
        for (int v = 1; v < n; v++) {
            if (best[v] != Long.MAX_VALUE && (bestAccount == -1 || best[v] < best[bestAccount])) bestAccount = v;
        }
        return bestAccount == -1 ? new long[] {-1, 0} : new long[] {bestAccount, best[bestAccount]};
    }

    /** Extends the route that ends at city with the given cost and records the cost of each account. */
    static void walk(int[][] transfers, int city, long cost, boolean[] on, long[] best) {
        for (int[] t : transfers) {
            if (t[0] != city || on[t[1]]) continue;
            long c = cost + t[2];
            if (c < best[t[1]]) best[t[1]] = c;
            on[t[1]] = true;
            walk(transfers, t[1], c, on, best);
            on[t[1]] = false;
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(cheapestOther(4, new int[][] {{0, 1, 4}, {0, 2, 6}, {2, 1, -5}, {1, 3, 3}}), new long[] {1, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(cheapestOther(4, new int[][] {{0, 1, 2}, {2, 3, -4}, {3, 2, 1}}), new long[] {1, 2})) throw new AssertionError("ex2");
        // No other account is reachable.
        if (!Arrays.equals(cheapestOther(3, new int[][] {{1, 2, -1}}), new long[] {-1, 0})) throw new AssertionError("none");
        if (!Arrays.equals(cheapestOther(1, new int[0][]), new long[] {-1, 0})) throw new AssertionError("single");
        // A tie goes to the smaller index.
        if (!Arrays.equals(cheapestOther(3, new int[][] {{0, 2, -3}, {0, 1, -3}}), new long[] {1, -3})) throw new AssertionError("tie");
        // The early stop: a forward chain of three transfers needs three changing passes, and the fourth is never started.
        cheapestOther(5, new int[][] {{0, 1, 1}, {1, 2, 1}, {2, 3, 1}});
        if (lastPasses != 4) throw new AssertionError("passes " + lastPasses);
        // Random graphs without negative cycles: weights come from node potentials plus a nonnegative extra.
        Random rnd = new Random(2504);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[] pot = new int[n];
            for (int i = 0; i < n; i++) pot[i] = rnd.nextInt(8);
            boolean hidden = n >= 4 && rnd.nextBoolean();
            int core = hidden ? n - 2 : n;
            int m = rnd.nextInt(12);
            List<int[]> list = new ArrayList<>();
            for (int i = 0; i < m; i++) {
                int u = rnd.nextInt(core), v = rnd.nextInt(core);
                list.add(new int[] {u, v, pot[u] - pot[v] + rnd.nextInt(3)});
            }
            // An unreachable negative cycle sits on the last two accounts.
            if (hidden) {
                list.add(new int[] {n - 2, n - 1, -3});
                list.add(new int[] {n - 1, n - 2, 1});
            }
            int[][] transfers = list.toArray(new int[0][]);
            if (!Arrays.equals(cheapestOther(n, transfers), oracle(n, transfers))) throw new AssertionError("random " + t);
        }
    }
}
```
