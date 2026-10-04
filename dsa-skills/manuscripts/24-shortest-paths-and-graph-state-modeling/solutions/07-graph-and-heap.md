<!-- solutions-for: 07-graph-and-heap -->
### Graph And Heap

#### Solution: [Build] Network Delay Time (LeetCode 743)
<!-- id: sh-last-to-light -->

**Approach.** Keep `best[pad]` as a `long`, push the offer `{time, pad}` whenever a proposal beats the table, and drop any entry whose time exceeds the table value of its pad. After the heap is empty, scan the pads in increasing label order and keep a pad only when its time is strictly larger than the current worst, so the smallest label wins every tie. A pad still at `Long.MAX_VALUE` makes the answer `{-1, -1}`. The asserts replay both examples, the unreachable case, a single node, and a chain of three edges of two billion that only a `long` holds. They also show why the unreached marker is never added to, why the comparator uses `Long.compare` and not an `int` cast of a difference, and the no-go case: a copy of the loop with a settled mark keeps `1` for node 2 on a graph with a negative edge where Bellman-Ford to a fixpoint finds `-2`. The oracle is Floyd-Warshall on random maps with zero and parallel edges, and the input rows are compared before and after.

**Complexity.** About O((V + E) log E) time, since each improvement adds one heap entry, and O(V + E) memory for the adjacency lists, table and heap.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class LastToLight {
    static long[] solve(int n, int[][] times, int k) {
        List<int[]>[] out = new List[n + 1];
        for (int i = 1; i <= n; i++) out[i] = new ArrayList<>();
        for (int[] t : times) out[t[0]].add(new int[] {t[1], t[2]});
        long[] dist = new long[n + 1];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[k] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, k});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] > dist[u]) continue;
            for (int[] e : out[u]) {
                long cand = top[0] + e[1];
                if (cand < dist[e[0]]) {
                    dist[e[0]] = cand;
                    heap.add(new long[] {cand, e[0]});
                }
            }
        }
        long worst = -1;
        int who = -1;
        for (int v = 1; v <= n; v++) {
            if (dist[v] == Long.MAX_VALUE) return new long[] {-1, -1};
            if (dist[v] > worst) { worst = dist[v]; who = v; }
        }
        return new long[] {worst, who};
    }

    static long[] oracle(int n, int[][] times, int k) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n + 1][n + 1];
        for (long[] row : d) Arrays.fill(row, inf);
        for (int i = 1; i <= n; i++) d[i][i] = 0;
        for (int[] t : times) d[t[0]][t[1]] = Math.min(d[t[0]][t[1]], t[2]);
        for (int m = 1; m <= n; m++)
            for (int i = 1; i <= n; i++)
                for (int j = 1; j <= n; j++) d[i][j] = Math.min(d[i][j], d[i][m] + d[m][j]);
        long worst = -1;
        int who = -1;
        for (int v = 1; v <= n; v++) {
            if (d[k][v] >= inf) return new long[] {-1, -1};
            if (d[k][v] > worst) { worst = d[k][v]; who = v; }
        }
        return new long[] {worst, who};
    }

    /** Same loop with a settled mark and one negative edge: the mark freezes a node too early. */
    static long[] withSettledMark(int n, int[][] times, int k) {
        long[] dist = new long[n + 1];
        Arrays.fill(dist, Long.MAX_VALUE);
        boolean[] done = new boolean[n + 1];
        dist[k] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, k});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (done[u]) continue;
            done[u] = true;
            for (int[] t : times) {
                if (t[0] != u || done[t[1]]) continue;
                long cand = top[0] + t[2];
                if (cand < dist[t[1]]) { dist[t[1]] = cand; heap.add(new long[] {cand, t[1]}); }
            }
        }
        return dist;
    }

    static String show(long[] a) { return Arrays.toString(a); }

    public static void main(String[] args) {
        int[][] one = {{2, 1, 2}, {2, 3, 1}, {3, 4, 3}, {1, 4, 1}, {4, 5, 2}};
        if (!show(solve(5, one, 2)).equals("[5, 5]")) throw new AssertionError("example 1");
        int[][] two = {{3, 1, 0}, {3, 2, 4}, {1, 4, 4}, {3, 4, 5}};
        if (!show(solve(4, two, 3)).equals("[4, 2]")) throw new AssertionError("example 2: tie goes to the smaller label");
        if (!show(solve(3, new int[][] {{1, 2, 1}}, 1)).equals("[-1, -1]")) throw new AssertionError("unreachable");
        if (!show(solve(1, new int[][] {}, 1)).equals("[0, 1]")) throw new AssertionError("single node");
        int[][] chain = {{1, 2, 2_000_000_000}, {2, 3, 2_000_000_000}, {3, 4, 2_000_000_000}};
        if (!show(solve(4, chain, 1)).equals("[6000000000, 4]")) throw new AssertionError("long sums");
        if (Long.MAX_VALUE + 1 >= 0) throw new AssertionError("adding to the unreached marker would wrap negative");
        if ((int) (3_000_000_000L - 1L) >= 0) throw new AssertionError("an int cast of a long difference flips the sign");
        int[][] neg = {{1, 2, 1}, {1, 3, 3}, {3, 2, -5}};
        long[] marked = withSettledMark(3, neg, 1);
        if (marked[2] != 1) throw new AssertionError("the settled mark keeps the early value");
        // Bellman-Ford to a fixpoint as the independent oracle for the negative edge
        long[] bf = new long[4];
        Arrays.fill(bf, Long.MAX_VALUE / 4);
        bf[1] = 0;
        for (int pass = 0; pass < 4; pass++)
            for (int[] t : neg) bf[t[1]] = Math.min(bf[t[1]], bf[t[0]] + t[2]);
        if (bf[2] != -2 || marked[2] == bf[2]) throw new AssertionError("negative edge breaks the early freeze");
        Random rnd = new Random(24701);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7), k = 1 + rnd.nextInt(n), m = rnd.nextInt(16);
            int[][] times = new int[m][];
            for (int i = 0; i < m; i++) times[i] = new int[] {1 + rnd.nextInt(n), 1 + rnd.nextInt(n), rnd.nextInt(4) == 0 ? 0 : rnd.nextInt(9)};
            int[][] copy = Arrays.stream(times).map(int[]::clone).toArray(int[][]::new);
            if (!show(solve(n, times, k)).equals(show(oracle(n, times, k)))) throw new AssertionError("differs on " + Arrays.deepToString(times) + " n=" + n + " k=" + k);
            if (!Arrays.deepEquals(copy, times)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Vary] Path With Minimum Effort (LeetCode 1631)
<!-- id: sh-min-effort -->

**Approach.** The loop of the Build rung is reused with one line changed: the offer for a neighbouring square is `Math.max(effort so far, step)`. Extending a ride never lowers its effort, so the smallest entry in the heap is final and the stale test still applies. The search stops as soon as the bottom-right square leaves the heap. The false friend is the same loop with a sum, and the asserts show it returns 7 on the second example where the answer is 3, and that it disagrees with the answer on some random grid. Two independent oracles are used: a Floyd-style closure that replaces plus by maximum over all pairs of squares, and an exhaustive search over simple paths on grids of at most nine squares. The input grid is compared with a copy.

**Complexity.** The heap holds at most one entry per improvement, giving O(RC log(RC)) time for an R by C grid and O(RC) extra space.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class MinEffortRide {
    static final int[][] STEPS = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    static int solve(int[][] h) {
        int rows = h.length, cols = h[0].length;
        int[] best = new int[rows * cols];
        Arrays.fill(best, Integer.MAX_VALUE);
        best[0] = 0;
        PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        heap.add(new int[] {0, 0});
        while (!heap.isEmpty()) {
            int[] top = heap.poll();
            int cell = top[1];
            if (top[0] > best[cell]) continue;
            if (cell == rows * cols - 1) return top[0];
            int r = cell / cols, c = cell % cols;
            for (int[] s : STEPS) {
                int nr = r + s[0], nc = c + s[1];
                if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
                int cand = Math.max(top[0], Math.abs(h[r][c] - h[nr][nc]));
                if (cand < best[nr * cols + nc]) {
                    best[nr * cols + nc] = cand;
                    heap.add(new int[] {cand, nr * cols + nc});
                }
            }
        }
        return best[rows * cols - 1];
    }

    /** Floyd-style minimax closure over all cells. */
    static int closure(int[][] h) {
        int rows = h.length, cols = h[0].length, n = rows * cols;
        int inf = Integer.MAX_VALUE;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                for (int[] s : STEPS) {
                    int nr = r + s[0], nc = c + s[1];
                    if (nr >= 0 && nc >= 0 && nr < rows && nc < cols) d[r * cols + c][nr * cols + nc] = Math.abs(h[r][c] - h[nr][nc]);
                }
        for (int m = 0; m < n; m++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (d[i][m] != inf && d[m][j] != inf) d[i][j] = Math.min(d[i][j], Math.max(d[i][m], d[m][j]));
        return d[0][n - 1];
    }

    static int bestSimple;

    static void walk(int[][] h, int r, int c, boolean[][] seen, int worst) {
        if (worst >= bestSimple) return;
        if (r == h.length - 1 && c == h[0].length - 1) { bestSimple = worst; return; }
        seen[r][c] = true;
        for (int[] s : STEPS) {
            int nr = r + s[0], nc = c + s[1];
            if (nr < 0 || nc < 0 || nr >= h.length || nc >= h[0].length || seen[nr][nc]) continue;
            walk(h, nr, nc, seen, Math.max(worst, Math.abs(h[r][c] - h[nr][nc])));
        }
        seen[r][c] = false;
    }

    static int simplePaths(int[][] h) {
        bestSimple = Integer.MAX_VALUE;
        walk(h, 0, 0, new boolean[h.length][h[0].length], 0);
        return bestSimple;
    }

    /** The false friend: the same heap loop, but a path is priced by the sum of its steps. */
    static int sumOfSteps(int[][] h) {
        int rows = h.length, cols = h[0].length;
        long[] best = new long[rows * cols];
        Arrays.fill(best, Long.MAX_VALUE);
        best[0] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, 0});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int cell = (int) top[1];
            if (top[0] > best[cell]) continue;
            int r = cell / cols, c = cell % cols;
            for (int[] s : STEPS) {
                int nr = r + s[0], nc = c + s[1];
                if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
                long cand = top[0] + Math.abs(h[r][c] - h[nr][nc]);
                if (cand < best[nr * cols + nc]) { best[nr * cols + nc] = cand; heap.add(new long[] {cand, nr * cols + nc}); }
            }
        }
        return (int) best[rows * cols - 1];
    }

    public static void main(String[] args) {
        int[][] one = {{3, 3, 3}, {3, 9, 3}, {3, 3, 3}};
        if (solve(one) != 0) throw new AssertionError("example 1");
        int[][] two = {{4, 9, 3}, {6, 8, 2}, {1, 8, 5}};
        if (solve(two) != 3) throw new AssertionError("example 2");
        if (sumOfSteps(two) != 7) throw new AssertionError("summing prices the best route at 7, not 3");
        if (solve(new int[][] {{7}}) != 0) throw new AssertionError("single cell");
        if (solve(new int[][] {{1, 1_000_000}}) != 999_999) throw new AssertionError("one step");
        Random rnd = new Random(24702);
        int mismatchSeen = 0;
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(4), cols = 1 + rnd.nextInt(4);
            int[][] h = new int[rows][cols];
            int top = 1 + rnd.nextInt(12);
            for (int[] row : h) for (int j = 0; j < cols; j++) row[j] = 1 + rnd.nextInt(top);
            int[][] copy = Arrays.stream(h).map(int[]::clone).toArray(int[][]::new);
            int got = solve(h);
            if (got != closure(h)) throw new AssertionError("closure differs on " + Arrays.deepToString(h));
            if (rows * cols <= 9 && got != simplePaths(h)) throw new AssertionError("simple paths differ on " + Arrays.deepToString(h));
            if (!Arrays.deepEquals(copy, h)) throw new AssertionError("input changed");
            if (sumOfSteps(h) != got) mismatchSeen++;
        }
        if (mismatchSeen == 0) throw new AssertionError("the false friend should fail on some grid");
    }
}
```

#### Solution: [Boundary] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: sh-fewest-cheapest -->

**Approach.** A state is the pair of an airstrip and the number of flights used, so `best[strip][used]` has k + 2 columns and a dearer arrival with fewer flights is never compared with a cheaper one that has used more. The heap orders by cost, then flights used, then strip, so the first entry for `dst` has the least cost and, among equal costs, the fewest flights. A state with all k + 1 flights used is not expanded. The prices are summed in `long`. The asserts replay the examples, the case with no direct flight, a graph where the dearer route with fewer flights is the only legal one, a three-flight route costing six billion, and the comparator hazard. The false friend keeps one distance per airstrip, and the assert shows it answers `{-1, -1}` where the answer is `{6, 2}`, and that it fails on some random graph. The oracle is a layered table of the cheapest cost with exactly e flights for each e up to k + 1.

**Complexity.** There are at most V(k + 2) states and each is expanded once, so the running time is O((k + 2) E log E) with O(V(k + 2) + E) space.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class FewestCheapest {
    static long[] solve(int n, int[][] flights, int src, int dst, int k) {
        int cap = k + 1;
        long[][] best = new long[n][cap + 1];
        for (long[] row : best) Arrays.fill(row, Long.MAX_VALUE);
        best[src][0] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> {
            int byCost = Long.compare(a[0], b[0]);
            if (byCost != 0) return byCost;
            int byEdges = Long.compare(a[1], b[1]);
            return byEdges != 0 ? byEdges : Long.compare(a[2], b[2]);
        });
        heap.add(new long[] {0, 0, src});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            long cost = top[0];
            int used = (int) top[1], u = (int) top[2];
            if (cost > best[u][used]) continue;
            if (u == dst) return new long[] {cost, used};
            if (used == cap) continue;
            for (int[] f : flights) {
                if (f[0] != u) continue;
                long cand = cost + f[2];
                if (cand < best[f[1]][used + 1]) {
                    best[f[1]][used + 1] = cand;
                    heap.add(new long[] {cand, used + 1, f[1]});
                }
            }
        }
        return new long[] {-1, -1};
    }

    /** Layered table: cheapest cost of a walk with exactly e flights. */
    static long[] oracle(int n, int[][] flights, int src, int dst, int k) {
        long inf = Long.MAX_VALUE / 4;
        long[][] f = new long[k + 2][n];
        for (long[] row : f) Arrays.fill(row, inf);
        f[0][src] = 0;
        for (int e = 0; e <= k; e++)
            for (int[] fl : flights)
                if (f[e][fl[0]] < inf) f[e + 1][fl[1]] = Math.min(f[e + 1][fl[1]], f[e][fl[0]] + fl[2]);
        long cost = inf;
        int fewest = -1;
        for (int e = 0; e <= k + 1; e++)
            if (f[e][dst] < cost) { cost = f[e][dst]; fewest = e; }
        return cost >= inf ? new long[] {-1, -1} : new long[] {cost, fewest};
    }

    /** The false friend: one distance per airport prunes a dearer route that uses fewer flights. */
    static long[] oneDistancePerNode(int n, int[][] flights, int src, int dst, int k) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, 0, src});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[2];
            if (top[0] > dist[u]) continue;
            if (u == dst) return new long[] {top[0], top[1]};
            if (top[1] == k + 1) continue;
            for (int[] f : flights) {
                if (f[0] != u || top[0] + f[2] >= dist[f[1]]) continue;
                dist[f[1]] = top[0] + f[2];
                heap.add(new long[] {dist[f[1]], top[1] + 1, f[1]});
            }
        }
        return new long[] {-1, -1};
    }

    static String show(long[] a) { return Arrays.toString(a); }

    public static void main(String[] args) {
        int[][] one = {{0, 1, 2}, {1, 2, 2}, {2, 4, 2}, {0, 3, 3}, {3, 4, 9}, {0, 2, 7}};
        if (!show(solve(5, one, 0, 4, 2)).equals("[6, 3]")) throw new AssertionError("example 1");
        if (!show(solve(5, one, 0, 4, 1)).equals("[9, 2]")) throw new AssertionError("fewer stops, dearer");
        if (!show(solve(5, one, 0, 4, 0)).equals("[-1, -1]")) throw new AssertionError("no direct flight");
        int[][] two = {{0, 1, 4}, {1, 3, 4}, {0, 2, 2}, {2, 3, 6}, {0, 3, 8}};
        if (!show(solve(4, two, 0, 3, 1)).equals("[8, 1]")) throw new AssertionError("example 2: equal cost, fewest flights");
        int[][] trap = {{0, 1, 1}, {1, 2, 1}, {2, 3, 1}, {0, 2, 5}};
        if (!show(solve(4, trap, 0, 3, 1)).equals("[6, 2]")) throw new AssertionError("state key keeps the dearer short route");
        if (!show(oneDistancePerNode(4, trap, 0, 3, 1)).equals("[-1, -1]")) throw new AssertionError("one distance per airport over-prunes");
        int[][] big = {{0, 1, 2_000_000_000}, {1, 2, 2_000_000_000}, {2, 3, 2_000_000_000}};
        if (!show(solve(4, big, 0, 3, 2)).equals("[6000000000, 3]")) throw new AssertionError("long cost");
        if ((int) (3_000_000_000L - 1L) >= 0) throw new AssertionError("a subtraction comparator cast to int misorders big costs");
        Random rnd = new Random(24703);
        int fooled = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(5), m = rnd.nextInt(14), k = rnd.nextInt(4);
            int[][] fl = new int[m][];
            for (int i = 0; i < m; i++) fl[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(6)};
            int src = rnd.nextInt(n), dst = (src + 1 + rnd.nextInt(n - 1)) % n;
            int[][] copy = Arrays.stream(fl).map(int[]::clone).toArray(int[][]::new);
            long[] got = solve(n, fl, src, dst, k);
            if (!show(got).equals(show(oracle(n, fl, src, dst, k)))) throw new AssertionError("differs on " + Arrays.deepToString(fl) + " " + src + "->" + dst + " k=" + k);
            if (!Arrays.deepEquals(copy, fl)) throw new AssertionError("input changed");
            if (!show(oneDistancePerNode(n, fl, src, dst, k)).equals(show(got))) fooled++;
        }
        if (fooled == 0) throw new AssertionError("the false friend should fail somewhere");
    }
}
```

#### Solution: [Recognize] Path with Maximum Probability (LeetCode 1514)
<!-- id: sh-max-probability -->

**Approach.** The heap releases the largest probability first, with `Double.compare(b[0], a[0])`, the offer is the product of the entry and the link, and an entry is stale when its value is below the table value of its beacon. Products of numbers in the range 0 to 1 never exceed their first factor, so the first release of a beacon is final. The search uses exact `double` comparison and no epsilon: two products that differ only by rounding give nearly the same answer whichever one is kept, and a link of probability zero never beats the initial 0.0. The test oracle works with whole percents, enumerates every simple path, and keeps the numerator of the product over `100^length` as a `BigInteger`, comparing paths by cross-multiplication, so no floating point is used to decide the best path. The result is converted to a double, and only the final check allows a tolerance of 1e-12. The asserts also show that `(int) (0.9 - 0.5)` is 0, which would make a casted difference useless as a comparator, and that the fewest-links route of the second example is worth only 0.7.

**Complexity.** Each improvement pushes one entry, so the time is O((V + E) log E) and the memory O(V + E).

```java run
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class SureBetRoute {
    static double solve(int n, int[][] edges, double[] prob, int start, int end) {
        List<double[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int i = 0; i < edges.length; i++) {
            adj[edges[i][0]].add(new double[] {edges[i][1], prob[i]});
            adj[edges[i][1]].add(new double[] {edges[i][0], prob[i]});
        }
        double[] best = new double[n];
        best[start] = 1.0;
        PriorityQueue<double[]> heap = new PriorityQueue<>((a, b) -> Double.compare(b[0], a[0]));
        heap.add(new double[] {1.0, start});
        while (!heap.isEmpty()) {
            double[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] < best[u]) continue;
            if (u == end) return top[0];
            for (double[] e : adj[u]) {
                double cand = top[0] * e[1];
                if (cand > best[(int) e[0]]) {
                    best[(int) e[0]] = cand;
                    heap.add(new double[] {cand, e[0]});
                }
            }
        }
        return 0.0;
    }

    static BigInteger bestNum;
    static int bestLen;

    /** Exact rational brute force: probabilities are whole percents, a path of L edges is num / 100^L. */
    static void walk(List<int[]>[] adj, int u, int end, boolean[] seen, BigInteger num, int len) {
        if (u == end) {
            BigInteger left = num.multiply(BigInteger.valueOf(100).pow(bestLen));
            BigInteger right = bestNum.multiply(BigInteger.valueOf(100).pow(len));
            if (left.compareTo(right) > 0) { bestNum = num; bestLen = len; }
            return;
        }
        seen[u] = true;
        for (int[] e : adj[u])
            if (!seen[e[0]]) walk(adj, e[0], end, seen, num.multiply(BigInteger.valueOf(e[1])), len + 1);
        seen[u] = false;
    }

    static double exact(int n, int[][] edges, int[] pct, int start, int end) {
        List<int[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int i = 0; i < edges.length; i++) {
            adj[edges[i][0]].add(new int[] {edges[i][1], pct[i]});
            adj[edges[i][1]].add(new int[] {edges[i][0], pct[i]});
        }
        bestNum = BigInteger.ZERO;
        bestLen = 0;
        walk(adj, start, end, new boolean[n], BigInteger.ONE, 0);
        return new java.math.BigDecimal(bestNum).divide(new java.math.BigDecimal(BigInteger.valueOf(100).pow(bestLen)), 40, java.math.RoundingMode.HALF_EVEN).doubleValue();
    }

    static double[] asDoubles(int[] pct) {
        double[] p = new double[pct.length];
        for (int i = 0; i < p.length; i++) p[i] = pct[i] / 100.0;
        return p;
    }

    public static void main(String[] args) {
        int[][] one = {{0, 1}, {1, 2}, {0, 2}, {2, 3}};
        if (Math.abs(solve(4, one, asDoubles(new int[] {50, 50, 20, 90}), 0, 3) - 0.225) > 1e-12) throw new AssertionError("example 1");
        int[][] two = {{0, 1}, {1, 2}, {2, 4}, {0, 3}, {3, 4}};
        int[] pct2 = {90, 90, 90, 70, 100};
        if (Math.abs(solve(5, two, asDoubles(pct2), 0, 4) - 0.729) > 1e-12) throw new AssertionError("example 2: three good legs beat two middling ones");
        if (solve(5, two, asDoubles(pct2), 0, 4) <= 0.7 * 1.0) throw new AssertionError("the two-link route is worth 0.7, below the answer");
        if (solve(3, new int[][] {{0, 1}}, new double[] {0.4}, 0, 2) != 0.0) throw new AssertionError("unreachable gives exactly 0");
        if (solve(3, new int[][] {{0, 1}, {1, 2}}, new double[] {0.0, 1.0}, 0, 2) != 0.0) throw new AssertionError("a zero edge never improves");
        if ((int) (0.9 - 0.5) != 0) throw new AssertionError("casting a double difference to int collapses to 0, so it cannot be a comparator");
        if (0.1 + 0.2 == 0.3) throw new AssertionError("doubles are inexact");
        Random rnd = new Random(24704);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(6), m = rnd.nextInt(10);
            int[][] edges = new int[m][];
            int[] pct = new int[m];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                edges[i] = new int[] {a, b == a ? (a + 1) % n : b};
                pct[i] = rnd.nextInt(4) == 0 ? 100 : rnd.nextInt(101);
            }
            int start = rnd.nextInt(n), end = (start + 1 + rnd.nextInt(n - 1)) % n;
            double got = solve(n, edges, asDoubles(pct), start, end);
            double want = exact(n, edges, pct, start, end);
            if (Math.abs(got - want) > 1e-12 * Math.max(1.0, want)) throw new AssertionError("differs " + got + " vs " + want + " on " + Arrays.deepToString(edges) + Arrays.toString(pct));
        }
    }
}
```
