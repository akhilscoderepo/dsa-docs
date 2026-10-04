<!-- solutions-for: 01-dijkstra -->
### Dijkstra

#### Solution: [Build] Relax One Edge (Author exercise)
<!-- id: sp-relax-edge -->

**Approach.** Return `false` at once when `dist[u]` is `Long.MAX_VALUE`, because an unreached town proposes nothing. Otherwise compute `dist[u] + w`, which cannot overflow under the stated limits, and write it into `dist[v]` only when it is strictly smaller. The oracle redoes the comparison in `BigInteger` arithmetic with the maximum value standing for infinity, and checks both the returned flag and the untouched cells on random arrays. The assertions also confirm the Java claims from the lesson: adding a toll to `Long.MAX_VALUE` wraps to a negative number, so an unguarded version would wrongly accept it, and an equal proposal does not count as an improvement.

**Complexity.** One comparison and at most one write, so it runs in constant time and constant extra space.

```java run
import java.math.BigInteger;
import java.util.Arrays;
import java.util.Random;

public final class RelaxEdgeSolution {
    static boolean relax(long[] dist, int u, int v, int w) {
        if (dist[u] == Long.MAX_VALUE) return false;
        long proposal = dist[u] + w;
        if (proposal < dist[v]) {
            dist[v] = proposal;
            return true;
        }
        return false;
    }

    static boolean unguarded(long[] dist, int u, int v, int w) {
        long proposal = dist[u] + w;
        if (proposal < dist[v]) {
            dist[v] = proposal;
            return true;
        }
        return false;
    }

    static boolean oracleWins(long[] dist, int u, int v, int w) {
        if (dist[u] == Long.MAX_VALUE) return false;
        BigInteger p = BigInteger.valueOf(dist[u]).add(BigInteger.valueOf(w));
        BigInteger cur = dist[v] == Long.MAX_VALUE
                ? BigInteger.TEN.pow(40) : BigInteger.valueOf(dist[v]);
        return p.compareTo(cur) < 0;
    }

    public static void main(String[] args) {
        long[] a = {0, 7, Long.MAX_VALUE};
        if (!relax(a, 1, 2, 4) || !Arrays.equals(a, new long[] {0, 7, 11})) throw new AssertionError("example 1");
        long[] b = {0, 3, 6};
        if (relax(b, 1, 2, 3) || !Arrays.equals(b, new long[] {0, 3, 6})) throw new AssertionError("example 2");

        if (Long.MAX_VALUE + 4 >= 0) throw new AssertionError("max plus toll should wrap negative");
        long[] trap = {Long.MAX_VALUE, 5};
        if (!unguarded(trap, 0, 1, 4) || trap[1] >= 0) throw new AssertionError("unguarded accepts the wrapped sum");
        long[] safe = {Long.MAX_VALUE, 5};
        if (relax(safe, 0, 1, 4) || safe[1] != 5) throw new AssertionError("guard failed");

        Random rnd = new Random(24_01_1);
        for (int t = 0; t < 4000; t++) {
            int len = 2 + rnd.nextInt(7);
            long[] d = new long[len];
            for (int i = 0; i < len; i++) {
                d[i] = rnd.nextInt(4) == 0 ? Long.MAX_VALUE : (long) rnd.nextInt(30) * (rnd.nextBoolean() ? 1 : 1_000_000_000L);
            }
            int u = rnd.nextInt(len), v = rnd.nextInt(len), w = rnd.nextInt(3) == 0 ? 1_000_000_000 : rnd.nextInt(30);
            long[] before = d.clone();
            boolean expect = oracleWins(before, u, v, w);
            boolean got = relax(d, u, v, w);
            if (got != expect) throw new AssertionError("flag " + Arrays.toString(before));
            for (int i = 0; i < len; i++) {
                long want = (i == v && expect) ? before[u] + w : before[i];
                if (d[i] != want) throw new AssertionError("cell " + i);
            }
        }
        long[] tie = {0, 3, 8};
        if (relax(tie, 1, 2, 5)) throw new AssertionError("equal proposal is not better");
    }
}
```

#### Solution: [Vary] Small Weighted Graph (Author exercise)
<!-- id: sp-settle-order -->

**Approach.** Run the heap version with pairs ordered by price and then by town number, skip stale pairs, and append each town to the answer the moment its live pair is removed. Because every toll is at least 1, a town whose true cost is d can only become available after a town of smaller cost has been taken, so the removal order is exactly the order of increasing true cost with ties by town number. The oracle uses that fact the other way round: it computes all costs with Floyd-Warshall, keeps the reachable towns and sorts them by cost and then number, which shares no code with the heap. The run also asserts that the heap really holds more than one pair for a town on the first example, matching the lesson's description of leftovers.

**Complexity.** Each road causes at most one push, so the work is O((V + E) log E) time with O(V + E) memory, while the oracle spends O(V^3).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class SettleOrderSolution {
    static int pushes;

    static int[] settleOrder(int n, int[][] roads, int depot) {
        List<int[]>[] out = new List[n];
        for (int i = 0; i < n; i++) out[i] = new ArrayList<>();
        for (int[] r : roads) out[r[0]].add(new int[] {r[1], r[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[depot] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) ->
                a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        heap.add(new long[] {0, depot});
        pushes = 1;
        int[] order = new int[n];
        int count = 0;
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] > dist[u]) continue;
            order[count++] = u;
            for (int[] road : out[u]) {
                long p = top[0] + road[1];
                if (p < dist[road[0]]) {
                    dist[road[0]] = p;
                    heap.add(new long[] {p, road[0]});
                    pushes++;
                }
            }
        }
        return Arrays.copyOf(order, count);
    }

    static int[] oracle(int n, int[][] roads, int depot) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][n];
        for (long[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] r : roads) d[r[0]][r[1]] = Math.min(d[r[0]][r[1]], r[2]);
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
        List<Integer> reach = new ArrayList<>();
        for (int v = 0; v < n; v++) if (d[depot][v] < inf) reach.add(v);
        final long[] row = d[depot];
        reach.sort((x, y) -> row[x] != row[y] ? Long.compare(row[x], row[y]) : Integer.compare(x, y));
        int[] out = new int[reach.size()];
        for (int i = 0; i < out.length; i++) out[i] = reach.get(i);
        return out;
    }

    public static void main(String[] args) {
        int[][] r1 = {{0, 1, 4}, {0, 2, 1}, {2, 1, 2}, {1, 3, 1}, {2, 3, 5}};
        if (!Arrays.equals(settleOrder(5, r1, 0), new int[] {0, 2, 1, 3})) throw new AssertionError("example 1");
        if (pushes <= 4) throw new AssertionError("expected a leftover pair for town 1");
        int[][] r2 = {{0, 1, 3}, {0, 2, 3}, {3, 0, 1}};
        if (!Arrays.equals(settleOrder(4, r2, 0), new int[] {0, 1, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(settleOrder(1, new int[0][], 0), new int[] {0})) throw new AssertionError("single town");

        Random rnd = new Random(24_01_2);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(21);
            int[][] roads = new int[m][];
            for (int i = 0; i < m; i++) roads[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(20)};
            int depot = rnd.nextInt(n);
            int[][] copy = Arrays.stream(roads).map(int[]::clone).toArray(int[][]::new);
            int[] got = settleOrder(n, roads, depot);
            if (!Arrays.equals(got, oracle(n, roads, depot)))
                throw new AssertionError("mismatch " + Arrays.deepToString(roads) + " depot " + depot);
            if (!Arrays.deepEquals(copy, roads)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Boundary] Unreachable Vertex And Large Sum (Author exercise)
<!-- id: sp-large-sum -->

**Approach.** The tags and the heap prices are `long`, the sentinel is `Long.MAX_VALUE`, and the heap comparator uses `Long.compare`. A pair is only expanded when its price is not larger than the tag, and since the only pair ever pushed starts from the depot, no unreached town is ever expanded, so the sentinel is never added to. The oracle is Bellman-Ford run to a fixpoint in `BigInteger`, which cannot overflow at all, with unreachable towns mapped back to the sentinel. Assertions confirm the Java claims: the sum 2,000,000,000 + 2,000,000,000 is negative in `int`, a subtraction comparator gives the wrong sign for two large `long` prices once cast to `int`, and the exact examples from the problem.

**Complexity.** The heap holds at most E + 1 pairs, so the running time is O((V + E) log E) and the extra memory is O(V + E), with no dependence on the size of the tolls.

```java run
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class LargeSumSolution {
    static long[] solve(int n, int[][] roads, int depot) {
        List<int[]>[] out = new List[n];
        for (int i = 0; i < n; i++) out[i] = new ArrayList<>();
        for (int[] r : roads) out[r[0]].add(new int[] {r[1], r[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[depot] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, depot});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] > dist[u]) continue;
            for (int[] road : out[u]) {
                long p = top[0] + road[1];
                if (p < dist[road[0]]) {
                    dist[road[0]] = p;
                    heap.add(new long[] {p, road[0]});
                }
            }
        }
        return dist;
    }

    static long[] oracle(int n, int[][] roads, int depot) {
        BigInteger[] d = new BigInteger[n];
        for (int i = 0; i < n; i++) d[i] = null;
        d[depot] = BigInteger.ZERO;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int[] r : roads) {
                if (d[r[0]] == null) continue;
                BigInteger p = d[r[0]].add(BigInteger.valueOf(r[2]));
                if (d[r[1]] == null || p.compareTo(d[r[1]]) < 0) { d[r[1]] = p; moved = true; }
            }
        }
        long[] out = new long[n];
        for (int i = 0; i < n; i++) out[i] = d[i] == null ? Long.MAX_VALUE : d[i].longValueExact();
        return out;
    }

    public static void main(String[] args) {
        int[][] r1 = {{0, 1, 2_000_000_000}, {1, 2, 2_000_000_000}, {2, 3, 2_000_000_000}};
        if (!Arrays.equals(solve(4, r1, 0), new long[] {0, 2_000_000_000L, 4_000_000_000L, 6_000_000_000L}))
            throw new AssertionError("example 1");
        int[][] r2 = {{0, 1, 5}, {2, 1, 3}};
        if (!Arrays.equals(solve(4, r2, 0), new long[] {0, 5, Long.MAX_VALUE, Long.MAX_VALUE}))
            throw new AssertionError("example 2");

        int intSum = 2_000_000_000 + 2_000_000_000;
        if (intSum >= 0) throw new AssertionError("int sum should wrap negative");
        long big = 5_000_000_000L, small = 1_000_000_000L;
        int badSign = (int) (big - small);
        if (badSign != 4_000_000_000L - (1L << 32) || badSign >= 0) throw new AssertionError("narrowed difference");
        if (Long.compare(big, small) <= 0) throw new AssertionError("Long.compare sign");

        Random rnd = new Random(24_01_3);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10), m = rnd.nextInt(26);
            int[][] roads = new int[m][];
            for (int i = 0; i < m; i++) {
                int toll = rnd.nextInt(3) == 0 ? Integer.MAX_VALUE - rnd.nextInt(5) : rnd.nextInt(40);
                roads[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), toll};
            }
            int depot = rnd.nextInt(n);
            int[][] copy = Arrays.stream(roads).map(int[]::clone).toArray(int[][]::new);
            if (!Arrays.equals(solve(n, roads, depot), oracle(n, roads, depot)))
                throw new AssertionError("mismatch " + Arrays.deepToString(roads));
            if (!Arrays.deepEquals(copy, roads)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-network-delay -->

**Approach.** Convert the labels 1 to n to 0 to n - 1 by subtracting one, run the heap routine from `k - 1`, and take the largest tag. If any tag still holds the sentinel, return -1. The oracle is Floyd-Warshall over all pairs, which shares no structure with the heap. Beyond the random comparison, the file asserts the lesson's two failure claims on concrete graphs: a breadth-first search that counts roads reports the wrong delay on a graph where the direct edge costs 9 and a two-edge detour costs 5, and a version that never reopens a taken node gives 4 instead of 0 for one node once an edge has a negative weight. It also asserts that a stale pair really is left in the heap on the lesson's first trace graph, and that `PriorityQueue` has no public method with a decrease-key name.

**Complexity.** With V nodes and E edges it takes O((V + E) log E) time and O(V + E) space; the oracle is O(V^3) and only used on at most seven nodes.

```java run
import java.lang.reflect.Method;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class NetworkDelaySolution {
    static int staleSeen;

    static long[] tags(int n, int[][] edges, int src) {
        List<int[]>[] out = new List[n];
        for (int i = 0; i < n; i++) out[i] = new ArrayList<>();
        for (int[] e : edges) out[e[0]].add(new int[] {e[1], e[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, src});
        staleSeen = 0;
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] > dist[u]) { staleSeen++; continue; }
            for (int[] e : out[u]) {
                long p = top[0] + e[1];
                if (p < dist[e[0]]) { dist[e[0]] = p; heap.add(new long[] {p, e[0]}); }
            }
        }
        return dist;
    }

    static int delay(int[][] times, int n, int k) {
        int[][] zero = new int[times.length][];
        for (int i = 0; i < times.length; i++) zero[i] = new int[] {times[i][0] - 1, times[i][1] - 1, times[i][2]};
        long worst = 0;
        for (long d : tags(n, zero, k - 1)) {
            if (d == Long.MAX_VALUE) return -1;
            worst = Math.max(worst, d);
        }
        return (int) worst;
    }

    static int oracle(int[][] times, int n, int k) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][n];
        for (long[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] e : times) d[e[0] - 1][e[1] - 1] = Math.min(d[e[0] - 1][e[1] - 1], e[2]);
        for (int m = 0; m < n; m++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (d[i][m] + d[m][j] < d[i][j]) d[i][j] = d[i][m] + d[m][j];
        long worst = 0;
        for (int j = 0; j < n; j++) {
            if (d[k - 1][j] >= inf) return -1;
            worst = Math.max(worst, d[k - 1][j]);
        }
        return (int) worst;
    }

    static long bfsByRoads(int n, int[][] edges, int src, int goal) {
        long[] cost = new long[n];
        int[] hops = new int[n];
        Arrays.fill(hops, -1);
        hops[src] = 0;
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(src);
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int[] e : edges) {
                if (e[0] == u && hops[e[1]] < 0) {
                    hops[e[1]] = hops[u] + 1;
                    cost[e[1]] = cost[u] + e[2];
                    q.add(e[1]);
                }
            }
        }
        return cost[goal];
    }

    static long[] takenOnce(int n, int[][] edges, int src) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        boolean[] done = new boolean[n];
        for (int round = 0; round < n; round++) {
            int u = -1;
            for (int v = 0; v < n; v++)
                if (!done[v] && dist[v] != Long.MAX_VALUE && (u < 0 || dist[v] < dist[u])) u = v;
            if (u < 0) break;
            done[u] = true;
            for (int[] e : edges)
                if (e[0] == u && !done[e[1]] && dist[u] + e[2] < dist[e[1]]) dist[e[1]] = dist[u] + e[2];
        }
        return dist;
    }

    static long[] bellman(int n, int[][] edges, int src) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        for (int pass = 0; pass < n; pass++)
            for (int[] e : edges)
                if (dist[e[0]] != Long.MAX_VALUE && dist[e[0]] + e[2] < dist[e[1]]) dist[e[1]] = dist[e[0]] + e[2];
        return dist;
    }

    public static void main(String[] args) {
        if (delay(new int[][] {{1, 2, 3}, {1, 3, 1}, {3, 2, 1}, {2, 4, 2}}, 4, 1) != 4) throw new AssertionError("example 1");
        if (delay(new int[][] {{1, 2, 3}, {3, 1, 2}}, 3, 1) != -1) throw new AssertionError("example 2");
        if (delay(new int[0][], 1, 1) != 0) throw new AssertionError("lone node");

        int[][] lesson = {{0, 1, 7}, {0, 2, 2}, {2, 1, 3}, {2, 3, 8}, {1, 4, 1}, {3, 4, 2}, {4, 5, 4}, {3, 5, 1}};
        long[] t = tags(6, lesson, 0);
        if (!Arrays.equals(t, new long[] {0, 5, 2, 10, 6, 10}) || staleSeen != 1) throw new AssertionError("lesson trace");

        int[][] trap = {{0, 1, 9}, {0, 2, 2}, {2, 1, 3}};
        if (bfsByRoads(3, trap, 0, 1) != 9 || tags(3, trap, 0)[1] != 5) throw new AssertionError("false friend");

        int[][] neg = {{0, 1, 4}, {0, 2, 5}, {2, 1, -5}, {1, 3, 2}, {3, 4, 1}};
        long[] wrong = takenOnce(5, neg, 0), right = bellman(5, neg, 0);
        if (wrong[1] != 4 || right[1] != 0 || wrong[4] != 7 || right[4] != 3) throw new AssertionError("negative edge");

        for (Method m : PriorityQueue.class.getMethods())
            if (m.getName().toLowerCase().contains("decrease")) throw new AssertionError("unexpected decrease-key");

        Random rnd = new Random(24_01_4);
        for (int tcase = 0; tcase < 4000; tcase++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(16);
            int[][] times = new int[m][];
            for (int i = 0; i < m; i++) times[i] = new int[] {1 + rnd.nextInt(n), 1 + rnd.nextInt(n), rnd.nextInt(21)};
            int k = 1 + rnd.nextInt(n);
            int[][] copy = Arrays.stream(times).map(int[]::clone).toArray(int[][]::new);
            if (delay(times, n, k) != oracle(times, n, k))
                throw new AssertionError("mismatch " + Arrays.deepToString(times) + " n=" + n + " k=" + k);
            if (!Arrays.deepEquals(copy, times)) throw new AssertionError("input changed");
        }
    }
}
```
