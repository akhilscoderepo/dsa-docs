<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Minimum Spanning Tree Choices

#### Solution: [Build] Distinguish MST From Shortest Paths (Author exercise)
<!-- id: ga-mst-spt-vs-mst -->

**Approach.**
The method computes two totals on the same graph. For the first total it runs Dijkstra's method from vertex 0 with `long` distances. It then scans the edges once more. For each vertex other than 0 it keeps the lightest edge that satisfies `dist[u] + w == dist[v]`, in either direction, and it sums those weights. For the second total it sorts a copy of the edges and runs Kruskal's method with a union-find array, adding an edge when its endpoints have different roots.

The invariant of the second total is that the chosen edges always lie inside some minimum spanning tree, because each added edge is the lightest one that leaves a component. The first total follows a different rule, which buys edges by distance from vertex 0. The two totals agree when the graph has a single spanning tree and differ when a cheap edge lies off every shortest route. The exercise relies on a connected graph, so the distances are all finite.

**Complexity.**
- **Time** is O(E log E), because Dijkstra's heap, the sort for Kruskal and the single scan of the edges each cost at most that much.
- **Space** is O(V + E) for the adjacency list, the heap, the distance array and the copied edge list.

```java run
import java.util.*;

public final class MstSptVsMst {
    /**
     * Returns the shortest-path tree weight and the minimum spanning tree weight.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: Kruskal's chosen edges always lie inside some minimum spanning tree.
     */
    static long[] compare(int n, int[][] edges) {
        // Build an undirected adjacency list; each edge appears twice.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(new int[] {e[1], e[2]});
            adj.get(e[1]).add(new int[] {e[0], e[2]});
        }
        // Distances are long, because a path of many heavy edges exceeds int.
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, 0});
        // Each pass removes one entry; each successful relaxation adds one.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            // A stale entry has a cost above the current distance and is skipped.
            if (top[0] > dist[u]) continue;
            for (int[] e : adj.get(u)) {
                // Only a strictly cheaper route creates a new entry.
                if (top[0] + e[1] < dist[e[0]]) {
                    dist[e[0]] = top[0] + e[1];
                    heap.add(new long[] {dist[e[0]], e[0]});
                }
            }
        }
        // For each vertex keep the lightest edge that lies on some shortest route into it.
        long[] tight = new long[n];
        Arrays.fill(tight, Long.MAX_VALUE);
        for (int[] e : edges) {
            // Test both directions of the undirected edge.
            if (dist[e[0]] + e[2] == dist[e[1]]) tight[e[1]] = Math.min(tight[e[1]], e[2]);
            if (dist[e[1]] + e[2] == dist[e[0]]) tight[e[0]] = Math.min(tight[e[0]], e[2]);
        }
        long sptTotal = 0;
        // Vertex 0 buys nothing, so the sum starts at vertex 1.
        for (int v = 1; v < n; v++) sptTotal += tight[v];
        // Kruskal on a sorted copy keeps the input order unchanged.
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        int[] root = new int[n];
        for (int v = 0; v < n; v++) root[v] = v;
        long mstTotal = 0;
        for (int[] e : sorted) {
            int ra = find(root, e[0]);
            int rb = find(root, e[1]);
            // An edge between two different components is the lightest across that cut.
            if (ra != rb) {
                root[ra] = rb;
                mstTotal += e[2];
            }
        }
        return new long[] {sptTotal, mstTotal};
    }

    /** Finds the root of x with path halving. */
    static int find(int[] root, int x) {
        // Each step halves the path, so repeated calls stay close to constant.
        while (root[x] != x) {
            root[x] = root[root[x]];
            x = root[x];
        }
        return x;
    }

    /** Oracle: Floyd-Warshall distances and a search over every subset of n - 1 edges. */
    static long[] oracle(int n, int[][] edges) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][n];
        for (long[] row : d) Arrays.fill(row, inf);
        for (int v = 0; v < n; v++) d[v][v] = 0;
        for (int[] e : edges) {
            d[e[0]][e[1]] = Math.min(d[e[0]][e[1]], e[2]);
            d[e[1]][e[0]] = Math.min(d[e[1]][e[0]], e[2]);
        }
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        long spt = 0;
        for (int v = 1; v < n; v++) {
            long best = inf;
            for (int[] e : edges) {
                if (e[1] == v && d[0][e[0]] + e[2] == d[0][v]) best = Math.min(best, e[2]);
                if (e[0] == v && d[0][e[1]] + e[2] == d[0][v]) best = Math.min(best, e[2]);
            }
            spt += best;
        }
        long mst = inf;
        int m = edges.length;
        // Try every subset of edges with exactly n - 1 members.
        for (int mask = 0; mask < (1 << m); mask++) {
            if (Integer.bitCount(mask) != n - 1) continue;
            int[] p = new int[n];
            for (int v = 0; v < n; v++) p[v] = v;
            long sum = 0;
            boolean tree = true;
            for (int i = 0; i < m && tree; i++) {
                if ((mask >> i & 1) == 0) continue;
                int ra = find(p, edges[i][0]);
                int rb = find(p, edges[i][1]);
                if (ra == rb) tree = false;
                else { p[ra] = rb; sum += edges[i][2]; }
            }
            if (tree) mst = Math.min(mst, sum);
        }
        return new long[] {spt, mst};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(compare(4, new int[][] {{0, 1, 3}, {1, 2, 1}, {0, 2, 3}, {2, 3, 2}}), new long[] {8, 6})) throw new AssertionError("ex1");
        if (!Arrays.equals(compare(4, new int[][] {{0, 1, 2}, {1, 2, 3}, {2, 3, 4}}), new long[] {9, 9})) throw new AssertionError("ex2");
        // A single vertex buys nothing.
        if (!Arrays.equals(compare(1, new int[][] {}), new long[] {0, 0})) throw new AssertionError("single");
        // Java fact: the difference of two int weights can overflow, so the sort uses Integer.compare.
        if (Integer.MIN_VALUE - 1 <= 0) throw new AssertionError("subtraction overflow");
        if (Integer.compare(Integer.MIN_VALUE, 1) >= 0) throw new AssertionError("compare");
        // Java fact: heavy edges exceed int range, so the totals are long.
        long[] big = compare(3, new int[][] {{0, 1, 1_000_000_000}, {1, 2, 1_000_000_000}, {0, 2, 1_000_000_000}});
        if (big[0] != 2_000_000_000L || big[1] != 2_000_000_000L) throw new AssertionError("big");
        if ((int) (big[0] + big[1]) == big[0] + big[1]) throw new AssertionError("int would overflow");
        // The input array order is unchanged by the call.
        int[][] keep = {{0, 1, 9}, {1, 2, 1}, {0, 2, 5}};
        compare(3, keep);
        if (keep[0][2] != 9 || keep[1][2] != 1 || keep[2][2] != 5) throw new AssertionError("mutated");
        // Random connected graphs of at most six vertices and nine edges, with ties and parallel edges.
        Random rnd = new Random(2581);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = Math.max(n - 1, 0) + rnd.nextInt(10 - Math.max(n - 1, 0));
            m = Math.min(m, 9);
            int[][] edges = new int[m][];
            // The first n - 1 edges link vertex i to an earlier vertex, which keeps the graph connected.
            for (int i = 0; i < m; i++) {
                int a = i < n - 1 ? i + 1 : rnd.nextInt(n);
                int b = i < n - 1 ? rnd.nextInt(i + 1) : rnd.nextInt(n);
                edges[i] = new int[] {a, b, rnd.nextInt(4)};
            }
            if (!Arrays.equals(compare(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Cut-Safe Choice (Author exercise)
<!-- id: ga-mst-cut-safe-choice -->

**Approach.**
The method scans the edges in index order and keeps the index of the lightest crossing edge seen so far. An edge crosses when `side[a] != side[b]`, so self loops never qualify. The scan replaces the stored index only when the new weight is strictly smaller. That strict comparison keeps the lowest index among equal weights, because the scan visits indices in increasing order.

The invariant is that after each edge the stored index points to the lightest crossing edge among the edges seen so far. The empty set of chosen edges respects every cut. So the cut property of the lesson places the returned edge inside some minimum spanning tree when the graph is connected. The oracle checks that claim on connected random graphs by searching all spanning trees that contain the returned edge.

**Complexity.**
- **Time** is O(E), because the scan reads each edge once.
- **Space** is O(1), because it keeps one index and allocates nothing else.

```java run
import java.util.*;

public final class MstCutSafeChoice {
    /**
     * Returns the index of the lightest crossing edge, or -1 when none crosses.
     * Time: O(E). Space: O(1).
     * Invariant: best holds the lightest crossing edge among the edges scanned so far.
     */
    static int lightestCrossing(int n, int[][] edges, boolean[] side) {
        int best = -1;
        // One pass over the edges; each edge costs a constant number of reads.
        for (int i = 0; i < edges.length; i++) {
            // Skip edges whose endpoints lie in the same group, including self loops.
            if (side[edges[i][0]] == side[edges[i][1]]) continue;
            // Strictly smaller weight only, so the lowest index wins a tie.
            if (best == -1 || edges[i][2] < edges[best][2]) best = i;
        }
        return best;
    }

    /** Smallest total weight of a spanning tree that contains edge pick, or -1 when none exists. */
    static long cheapestTreeWith(int n, int[][] edges, int pick) {
        long best = Long.MAX_VALUE;
        int m = edges.length;
        // Try every subset of edges with exactly n - 1 members that contains the pick.
        for (int mask = 0; mask < (1 << m); mask++) {
            if (Integer.bitCount(mask) != n - 1 || (mask >> pick & 1) == 0) continue;
            int[] p = new int[n];
            for (int v = 0; v < n; v++) p[v] = v;
            long sum = 0;
            boolean tree = true;
            for (int i = 0; i < m && tree; i++) {
                if ((mask >> i & 1) == 0) continue;
                int ra = find(p, edges[i][0]);
                int rb = find(p, edges[i][1]);
                if (ra == rb) tree = false;
                else { p[ra] = rb; sum += edges[i][2]; }
            }
            if (tree) best = Math.min(best, sum);
        }
        return best == Long.MAX_VALUE ? -1 : best;
    }

    static int find(int[] p, int x) {
        while (p[x] != x) x = p[x];
        return x;
    }

    /** Oracle for the index: sort the crossing indices by weight and then by index. */
    static int oracleIndex(int n, int[][] edges, boolean[] side) {
        List<Integer> cross = new ArrayList<>();
        for (int i = 0; i < edges.length; i++) if (side[edges[i][0]] != side[edges[i][1]]) cross.add(i);
        if (cross.isEmpty()) return -1;
        cross.sort((x, y) -> edges[x][2] != edges[y][2] ? Integer.compare(edges[x][2], edges[y][2]) : Integer.compare(x, y));
        return cross.get(0);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] e1 = {{0, 1, 4}, {1, 2, 2}, {2, 3, 7}, {0, 3, 2}};
        if (lightestCrossing(4, e1, new boolean[] {true, true, false, false}) != 1) throw new AssertionError("ex1");
        if (lightestCrossing(3, new int[][] {{0, 1, 1}}, new boolean[] {true, true, false}) != -1) throw new AssertionError("ex2");
        // A self loop never crosses, even when it is the lightest edge.
        if (lightestCrossing(2, new int[][] {{0, 0, 0}, {0, 1, 5}}, new boolean[] {true, false}) != 1) throw new AssertionError("loop");
        // Java fact: a boolean array defaults to false, so a fresh array puts every vertex in one group.
        if (lightestCrossing(2, new int[][] {{0, 1, 5}}, new boolean[2]) != -1) throw new AssertionError("default");
        // Random graphs compared with the sorted oracle, and the cut property on connected graphs.
        Random rnd = new Random(2582);
        for (int t = 0; t < 2000; t++) {
            int n = 2 + rnd.nextInt(5);
            int m = n - 1 + rnd.nextInt(5);
            int[][] edges = new int[m][];
            // The first n - 1 edges link vertex i + 1 to an earlier vertex, so the graph is connected.
            for (int i = 0; i < m; i++) {
                int a = i < n - 1 ? i + 1 : rnd.nextInt(n);
                int b = i < n - 1 ? rnd.nextInt(i + 1) : rnd.nextInt(n);
                edges[i] = new int[] {a, b, rnd.nextInt(4)};
            }
            boolean[] side = new boolean[n];
            for (int v = 0; v < n; v++) side[v] = rnd.nextBoolean();
            side[0] = true;
            side[n - 1] = false;
            int got = lightestCrossing(n, edges, side);
            if (got != oracleIndex(n, edges, side)) throw new AssertionError("index " + t);
            // A connected graph has a crossing edge, and the picked edge fits in some cheapest tree.
            if (got == -1) throw new AssertionError("connected graph must cross " + t);
            long overall = Long.MAX_VALUE;
            for (int i = 0; i < m; i++) {
                long w = cheapestTreeWith(n, edges, i);
                if (w != -1) overall = Math.min(overall, w);
            }
            if (cheapestTreeWith(n, edges, got) != overall) throw new AssertionError("cut property " + t);
        }
    }
}
```

#### Solution: [Boundary] Multiple Valid MSTs (Author exercise)
<!-- id: ga-mst-multiple-trees -->

**Approach.**
The method sorts a copy of the edges by weight and walks through each group of equal weight. At the start of a group it finds every edge whose endpoints have different roots, and it counts them as candidates. It then adds the candidates to the union-find structure one by one, and it counts how many actually join two components. After the group it compares the two counts. When some candidate was rejected, that candidate closes a cycle with other edges of the same weight, so swapping them gives a second tree of equal total weight.

The invariant is that before each group the structure holds exactly the components of all lighter edges, and every minimum spanning tree contains a spanning forest of those components. Within a group the number of edges added is fixed, but the choice among candidates is free exactly when some candidate is rejected. Equal weights alone do not create a tie, because a group whose candidates all join separate components has only one choice. Self loops never become candidates, and parallel equal edges do.

**Complexity.**
- **Time** is O(E log E), because the sort dominates and the two passes over each group make E calls to `find` in total.
- **Space** is O(V + E) for the roots and the copied edge list.

```java run
import java.util.*;

public final class MstMultipleTrees {
    /**
     * Returns the minimum spanning tree weight and 1 when that tree is unique, else 0.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: before each weight group the roots describe the components of all lighter edges.
     */
    static long[] weightAndUniqueness(int n, int[][] edges) {
        // Sort a copy so the caller's array keeps its order.
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        int[] root = new int[n];
        for (int v = 0; v < n; v++) root[v] = v;
        long total = 0;
        boolean unique = true;
        int i = 0;
        // Each pass handles one group of edges that share a weight.
        while (i < sorted.length) {
            int j = i;
            while (j < sorted.length && sorted[j][2] == sorted[i][2]) j++;
            // Count candidates before any union of this group changes the roots.
            int candidates = 0;
            for (int k = i; k < j; k++) {
                if (find(root, sorted[k][0]) != find(root, sorted[k][1])) candidates++;
            }
            // Add edges and count the ones that really join two components.
            int added = 0;
            for (int k = i; k < j; k++) {
                int ra = find(root, sorted[k][0]);
                int rb = find(root, sorted[k][1]);
                if (ra != rb) {
                    root[ra] = rb;
                    total += sorted[k][2];
                    added++;
                }
            }
            // A rejected candidate means two equal edges compete for the same connection.
            if (added != candidates) unique = false;
            i = j;
        }
        return new long[] {total, unique ? 1 : 0};
    }

    static int find(int[] root, int x) {
        // Path halving keeps later calls close to constant.
        while (root[x] != x) {
            root[x] = root[root[x]];
            x = root[x];
        }
        return x;
    }

    /** Oracle: enumerate every subset of n - 1 edges and count the trees of least weight. */
    static long[] oracle(int n, int[][] edges) {
        long best = Long.MAX_VALUE;
        int count = 0;
        int m = edges.length;
        for (int mask = 0; mask < (1 << m); mask++) {
            if (Integer.bitCount(mask) != n - 1) continue;
            int[] p = new int[n];
            for (int v = 0; v < n; v++) p[v] = v;
            long sum = 0;
            boolean tree = true;
            for (int i = 0; i < m && tree; i++) {
                if ((mask >> i & 1) == 0) continue;
                int ra = find(p, edges[i][0]);
                int rb = find(p, edges[i][1]);
                if (ra == rb) tree = false;
                else { p[ra] = rb; sum += edges[i][2]; }
            }
            if (!tree) continue;
            if (sum < best) { best = sum; count = 1; }
            else if (sum == best) count++;
        }
        return new long[] {best, count == 1 ? 1 : 0};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(weightAndUniqueness(3, new int[][] {{0, 1, 1}, {1, 2, 1}, {0, 2, 1}}), new long[] {2, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(weightAndUniqueness(4, new int[][] {{0, 1, 2}, {1, 2, 2}, {2, 3, 1}}), new long[] {5, 1})) throw new AssertionError("ex2");
        // A single vertex has exactly one empty tree.
        if (!Arrays.equals(weightAndUniqueness(1, new int[][] {{0, 0, 7}}), new long[] {0, 1})) throw new AssertionError("single");
        // Two parallel equal edges are two different trees.
        if (!Arrays.equals(weightAndUniqueness(2, new int[][] {{0, 1, 3}, {1, 0, 3}}), new long[] {3, 0})) throw new AssertionError("parallel");
        // Java fact: the total of many heavy edges exceeds int range, so the result is long.
        int[][] heavy = new int[3][];
        for (int i = 0; i < 3; i++) heavy[i] = new int[] {i, i + 1, 1_000_000_000};
        long[] big = weightAndUniqueness(4, heavy);
        if (big[0] != 3_000_000_000L || (int) big[0] == big[0]) throw new AssertionError("big");
        // Random connected graphs with many ties, compared with the exhaustive count.
        Random rnd = new Random(2583);
        for (int t = 0; t < 2500; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = (n - 1) + rnd.nextInt(Math.min(4, 10 - n));
            int[][] edges = new int[m][];
            // The first n - 1 edges link vertex i + 1 to an earlier vertex, which keeps the graph connected.
            for (int i = 0; i < m; i++) {
                int a = i < n - 1 ? i + 1 : rnd.nextInt(n);
                int b = i < n - 1 ? rnd.nextInt(i + 1) : rnd.nextInt(n);
                edges[i] = new int[] {a, b, rnd.nextInt(3)};
            }
            if (!Arrays.equals(weightAndUniqueness(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: ga-mst-connect-points -->

**Approach.**
Every pair of points is a possible cable, so the graph is complete and has about n squared over two edges. The method therefore uses dense Prim and never builds an edge list. It first marks the built pairs in a boolean matrix. The price of a pair is zero when the matrix marks it, and the Manhattan distance otherwise. The method grows a tree from point 0. In each round it picks the outside point with the smallest `best` value, adds that value to the total, and counts a new cable when the value is positive. Then it updates `best` for the remaining points from the price to the new tree point.

The invariant is that `best[v]` is the lightest price from `v` to any point in the tree. The picked point therefore has the lightest edge across the cut between the tree and the rest. Points are distinct, so every unbuilt pair costs at least 1, and a positive pick is exactly a new cable. A zero pick follows a built cable. Because the picks reach every point, the number of new cables equals the number of components of the built cables minus one. The total uses `long`, because a single cable between far corners costs more than the range of `int`.

**Complexity.**
- **Time** is O(n^2 + B), because each of n rounds scans n points twice and the built list is read once.
- **Space** is O(n^2) for the boolean matrix of built pairs, which is the only quadratic structure.

```java run
import java.util.*;

public final class MstConnectPoints {
    /**
     * Returns the least cost of new cables and the number of new cables.
     * Time: O(n^2 + B). Space: O(n^2).
     * Invariant: best[v] is the lightest price from v to any point already in the tree.
     */
    static long[] connect(int[][] points, int[][] built) {
        int n = points.length;
        // Mark each built pair in both directions; repeats just set the same cell again.
        boolean[][] free = new boolean[n][n];
        for (int[] b : built) {
            free[b[0]][b[1]] = true;
            free[b[1]][b[0]] = true;
        }
        boolean[] inTree = new boolean[n];
        long[] best = new long[n];
        // Long.MAX_VALUE marks a point whose price is not yet known; it is only compared.
        Arrays.fill(best, Long.MAX_VALUE);
        best[0] = 0;
        long total = 0;
        long cables = 0;
        // Each round adds one point, so there are n rounds.
        for (int round = 0; round < n; round++) {
            int u = -1;
            // Scan for the outside point with the smallest known price.
            for (int v = 0; v < n; v++) {
                if (!inTree[v] && (u == -1 || best[v] < best[u])) u = v;
            }
            inTree[u] = true;
            total += best[u];
            // A positive price is a new cable; a zero price follows a built cable.
            if (best[u] > 0) cables++;
            // Lower the price of every outside point using the new tree point.
            for (int v = 0; v < n; v++) {
                if (inTree[v]) continue;
                long price = free[u][v] ? 0 : Math.abs((long) points[u][0] - points[v][0]) + Math.abs((long) points[u][1] - points[v][1]);
                if (price < best[v]) best[v] = price;
            }
        }
        return new long[] {total, cables};
    }

    /** Oracle: Kruskal on the explicit list of all pairs, with built pairs at price 0. */
    static long[] oracle(int[][] points, int[][] built) {
        int n = points.length;
        Set<Long> free = new HashSet<>();
        for (int[] b : built) {
            free.add((long) Math.min(b[0], b[1]) * 10_000 + Math.max(b[0], b[1]));
        }
        List<long[]> all = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                long price = free.contains((long) i * 10_000 + j) ? 0 : Math.abs((long) points[i][0] - points[j][0]) + Math.abs((long) points[i][1] - points[j][1]);
                all.add(new long[] {price, i, j});
            }
        }
        all.sort((a, b) -> Long.compare(a[0], b[0]));
        int[] p = new int[n];
        for (int v = 0; v < n; v++) p[v] = v;
        long total = 0, cables = 0;
        for (long[] e : all) {
            int ra = find(p, (int) e[1]);
            int rb = find(p, (int) e[2]);
            if (ra != rb) {
                p[ra] = rb;
                total += e[0];
                if (e[0] > 0) cables++;
            }
        }
        return new long[] {total, cables};
    }

    static int find(int[] p, int x) {
        while (p[x] != x) x = p[x];
        return x;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(connect(new int[][] {{0, 0}, {1, 3}, {4, 0}, {4, 4}}, new int[][] {{0, 3}}), new long[] {8, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(connect(new int[][] {{0, 0}, {0, 1}, {0, 2}}, new int[][] {{0, 1}, {1, 2}}), new long[] {0, 0})) throw new AssertionError("ex2");
        // One point needs no cable.
        if (!Arrays.equals(connect(new int[][] {{5, 5}}, new int[][] {}), new long[] {0, 0})) throw new AssertionError("single");
        // Java fact: two coordinate differences of 2 billion sum to a negative int, so the code widens to long first.
        int far = 1_000_000_000;
        int diff = far - (-far);
        if (diff + diff >= 0) throw new AssertionError("int sum should wrap");
        // Extreme corners: one cable costs 4 billion, which is above the int range.
        int[][] corners = {{-far, -far}, {far, far}, {far, -far}};
        long[] big = connect(corners, new int[][] {});
        if (!Arrays.equals(big, new long[] {4_000_000_000L, 2}) || !Arrays.equals(big, oracle(corners, new int[][] {}))) throw new AssertionError("corners");
        if (big[0] <= Integer.MAX_VALUE) throw new AssertionError("sum should exceed int");
        // Random small point sets with random built pairs, including repeats and cycles.
        Random rnd = new Random(2584);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            Set<String> seen = new HashSet<>();
            List<int[]> pts = new ArrayList<>();
            while (pts.size() < n) {
                int x = rnd.nextInt(7) - 3, y = rnd.nextInt(7) - 3;
                if (seen.add(x + "," + y)) pts.add(new int[] {x, y});
            }
            int[][] points = pts.toArray(new int[0][]);
            int bcount = n < 2 ? 0 : rnd.nextInt(6);
            int[][] built = new int[bcount][];
            for (int i = 0; i < bcount; i++) {
                int a = rnd.nextInt(n);
                int b = (a + 1 + rnd.nextInt(n - 1)) % n;
                built[i] = new int[] {a, b};
            }
            if (!Arrays.equals(connect(points, built), oracle(points, built))) throw new AssertionError("random " + t);
        }
    }
}
```
