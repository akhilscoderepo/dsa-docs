<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For Kruskal Foundations

#### Solution: [Build] Cheapest Safe Edge (Author exercise)
<!-- id: dg-cheapest-safe-edge -->

**Approach.**
The method sorts an array of edge indices, not the edges themselves. The weight is the first key and the input index is the second key. The input index makes the tie rule explicit, so the order does not depend on the stability of the sort. A union-find structure with `parent` and `size` arrays then answers one question per edge: do the two endpoints share a representative? A shared representative means the edge lies inside a group, so the method skips it. Different representatives mean the edge joins two groups. The method records the index, attaches the smaller group below the larger one and adds the size to the new representative.

The invariant is that after each examined edge, the accepted edges form a forest whose connected pieces equal the union-find groups. A self-loop has two equal endpoints, so it always fails the test and no special case is needed. The method stops after `V - 1` acceptances, because the graph is connected and a further edge could only close a cycle.

**Complexity.**
- **Time** is O(E log E) for the index sort plus O(E * alpha(V)) for the `find` calls, so the sort dominates.
- **Space** is O(V + E), because the union-find arrays hold `V` entries and the boxed index array holds `E` entries.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class CheapestSafeEdges {
    private static int find(int[] parent, int x) {
        // Path halving: every visited vertex moves up to its grandparent, which shortens later searches.
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    /**
     * Returns the input indices of the accepted edges in acceptance order for a connected graph.
     * Time: O(E log E) for the sort plus near-constant union-find work per edge.
     * Space: O(V + E) for the union-find arrays and the index array.
     * Invariant: the accepted edges form a forest whose pieces equal the union-find groups.
     */
    static int[] pick(int vertexCount, int[][] edges) {
        Integer[] order = new Integer[edges.length];
        // One slot per edge index, so the sort moves indices and leaves the caller's edges alone.
        for (int k = 0; k < order.length; k++) order[k] = k;
        // Weight first, then input index, which states the tie rule without relying on stability.
        Arrays.sort(order, (a, b) -> edges[a][2] != edges[b][2] ? Integer.compare(edges[a][2], edges[b][2]) : Integer.compare(a, b));
        int[] parent = new int[vertexCount], size = new int[vertexCount];
        // Every vertex starts as a group of one.
        for (int v = 0; v < vertexCount; v++) { parent[v] = v; size[v] = 1; }
        int[] taken = new int[Math.max(vertexCount - 1, 0)];
        int accepted = 0;
        // Each edge is examined at most once, which bounds the loop at E iterations.
        for (int k : order) {
            // A complete tree has V - 1 edges, so later edges cannot help.
            if (accepted == vertexCount - 1) break;
            int ru = find(parent, edges[k][0]), rv = find(parent, edges[k][1]);
            // Equal representatives mean the edge would close a cycle, and a self-loop always lands here.
            if (ru == rv) continue;
            // Attach the smaller group below the larger one.
            if (size[ru] < size[rv]) { int t = ru; ru = rv; rv = t; }
            parent[rv] = ru;
            size[ru] += size[rv];
            // Record the input index in acceptance order.
            taken[accepted++] = k;
        }
        return taken;
    }

    /** Oracle one: the same rule, with a graph search over the accepted edges as the connectivity test. */
    static int[] slow(int vertexCount, int[][] edges) {
        List<Integer> order = new ArrayList<>();
        for (int k = 0; k < edges.length; k++) order.add(k);
        order.sort((a, b) -> edges[a][2] != edges[b][2] ? edges[a][2] - edges[b][2] : a - b);
        List<Integer> taken = new ArrayList<>();
        for (int k : order) {
            if (taken.size() == vertexCount - 1) break;
            boolean[] seen = new boolean[vertexCount];
            // Depth-first search from one endpoint over the edges accepted so far.
            reach(edges[k][0], taken, edges, seen);
            if (!seen[edges[k][1]]) taken.add(k);
        }
        int[] out = new int[taken.size()];
        for (int i = 0; i < out.length; i++) out[i] = taken.get(i);
        return out;
    }

    private static void reach(int u, List<Integer> taken, int[][] edges, boolean[] seen) {
        seen[u] = true;
        for (int k : taken) {
            int a = edges[k][0], b = edges[k][1];
            if (a == u && !seen[b]) reach(b, taken, edges, seen);
            if (b == u && !seen[a]) reach(a, taken, edges, seen);
        }
    }

    /** Oracle two: the lowest total over every subset of V - 1 edges that connects all vertices. */
    static int bestTotal(int vertexCount, int[][] edges) {
        int best = Integer.MAX_VALUE;
        for (int mask = 0; mask < (1 << edges.length); mask++) {
            if (Integer.bitCount(mask) != vertexCount - 1) continue;
            int[] parent = new int[vertexCount];
            for (int v = 0; v < vertexCount; v++) parent[v] = v;
            int sum = 0;
            boolean tree = true;
            for (int k = 0; k < edges.length && tree; k++) {
                if ((mask >> k & 1) == 0) continue;
                int a = find(parent, edges[k][0]), b = find(parent, edges[k][1]);
                if (a == b) tree = false; else parent[a] = b;
                sum += edges[k][2];
            }
            if (tree) best = Math.min(best, sum);
        }
        return best;
    }

    static int total(int[] taken, int[][] edges) {
        int s = 0;
        for (int k : taken) s += edges[k][2];
        return s;
    }

    /** Builds a connected random multigraph: a random tree first, then extra edges that may repeat or loop. */
    static int[][] randomConnected(Random rnd, int vertexCount, int extra, int maxWeight) {
        List<int[]> list = new ArrayList<>();
        for (int v = 1; v < vertexCount; v++) list.add(new int[] {rnd.nextInt(v), v, 1 + rnd.nextInt(maxWeight)});
        for (int i = 0; i < extra; i++) list.add(new int[] {rnd.nextInt(vertexCount), rnd.nextInt(vertexCount), 1 + rnd.nextInt(maxWeight)});
        Collections.shuffle(list, rnd);
        return list.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // Example 1: edge 1 and edge 3 are the cheapest, and edge 2 then joins vertex 0.
        int[][] e1 = {{0, 1, 4}, {1, 2, 1}, {0, 2, 3}, {2, 3, 2}, {1, 3, 5}};
        if (!Arrays.equals(pick(4, e1), new int[] {1, 3, 2})) throw new AssertionError("example 1");
        // Example 2: a self-loop and a repeated edge are both skipped.
        int[][] e2 = {{0, 1, 2}, {1, 1, 1}, {0, 1, 2}, {1, 2, 2}};
        if (!Arrays.equals(pick(3, e2), new int[] {0, 3})) throw new AssertionError("example 2");
        // A single vertex needs no edge, even when only self-loops exist.
        if (pick(1, new int[][] {{0, 0, 5}}).length != 0) throw new AssertionError("single vertex");
        // The method leaves the edge array unchanged.
        int[][] keep = {{0, 1, 9}, {1, 2, 1}};
        pick(3, keep);
        if (!Arrays.deepEquals(keep, new int[][] {{0, 1, 9}, {1, 2, 1}})) throw new AssertionError("mutation");
        // Random connected graphs against the search-based rule, and small ones against the subset oracle.
        Random rnd = new Random(2301);
        for (int t = 0; t < 3000; t++) {
            int v = 1 + rnd.nextInt(6), extra = rnd.nextInt(6);
            int[][] g = randomConnected(rnd, v, extra, 1 + rnd.nextInt(4));
            int[] got = pick(v, g);
            if (!Arrays.equals(got, slow(v, g))) throw new AssertionError("indices " + t + " " + Arrays.deepToString(g));
            if (g.length <= 11 && total(got, g) != bestTotal(v, g)) throw new AssertionError("total " + t + " " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Vary] Stop After V Minus One (Author exercise)
<!-- id: dg-stop-after-v-minus-one -->

**Approach.**
The loop is the same as in the previous solution, with a counter `examined` that rises once per edge the loop looks at. The check `accepted == V - 1` sits at the top of the loop body, before the examination. The loop therefore never counts an edge it did not need. Suppose the last accepted edge is also the last edge in the sorted list. The check at the top never triggers, so the count equals the list length. With `V` equal to 1 the check holds before the first iteration, so the method returns 0.

The invariant is that `examined` equals the number of sorted edges processed so far, and `accepted` is at most `V - 1`. The tie rule matters here, because the position of a skipped edge in the sorted order changes the count.

**Complexity.**
- **Time** is O(E log E) for the sort, and the loop itself runs at most E iterations with near-constant union-find work each.
- **Space** is O(V + E), because of the union-find arrays and the sorted index array.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class ExaminedBeforeStop {
    private static int find(int[] parent, int x) {
        // Path halving shortens the route from x to its representative.
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    /**
     * Returns how many sorted edges the loop examines before it holds V - 1 accepted edges.
     * Time: O(E log E) for the sort plus near-constant union-find work per examined edge.
     * Space: O(V + E) for the union-find arrays and the index array.
     * Invariant: examined counts processed edges and accepted never exceeds V - 1.
     */
    static int examined(int vertexCount, int[][] edges) {
        Integer[] order = new Integer[edges.length];
        // Sort indices so that the input array stays untouched and ties can use the index.
        for (int k = 0; k < order.length; k++) order[k] = k;
        Arrays.sort(order, (a, b) -> edges[a][2] != edges[b][2] ? Integer.compare(edges[a][2], edges[b][2]) : Integer.compare(a, b));
        int[] parent = new int[vertexCount];
        // Every vertex starts as its own representative.
        for (int v = 0; v < vertexCount; v++) parent[v] = v;
        int accepted = 0, count = 0;
        // The loop visits each edge at most once.
        for (int k : order) {
            // Check before the examination, so an edge that is not needed is never counted.
            if (accepted == vertexCount - 1) break;
            count++;
            int ru = find(parent, edges[k][0]), rv = find(parent, edges[k][1]);
            // Only an edge that joins two groups raises the accepted count.
            if (ru != rv) { parent[ru] = rv; accepted++; }
        }
        return count;
    }

    /** Oracle: repeated relabeling of component ids replaces union-find. */
    static int oracle(int vertexCount, int[][] edges) {
        List<int[]> sorted = new ArrayList<>();
        for (int k = 0; k < edges.length; k++) sorted.add(new int[] {edges[k][2], k});
        sorted.sort((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
        int[] label = new int[vertexCount];
        for (int v = 0; v < vertexCount; v++) label[v] = v;
        int accepted = 0, count = 0;
        for (int[] s : sorted) {
            if (accepted == vertexCount - 1) break;
            count++;
            int a = label[edges[s[1]][0]], b = label[edges[s[1]][1]];
            if (a == b) continue;
            // Relabel one whole group, which costs O(V) but needs no tree.
            for (int v = 0; v < vertexCount; v++) if (label[v] == b) label[v] = a;
            accepted++;
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1: the third edge in weight order is skipped, so four edges are examined.
        if (examined(4, new int[][] {{0, 1, 1}, {1, 2, 2}, {0, 2, 3}, {2, 3, 4}}) != 4) throw new AssertionError("example 1");
        // Example 2: one vertex needs no edge, so nothing is examined.
        if (examined(1, new int[][] {{0, 0, 7}, {0, 0, 3}}) != 0) throw new AssertionError("example 2");
        // The last accepted edge is the last edge in the list, so every edge is examined.
        if (examined(3, new int[][] {{0, 1, 1}, {1, 1, 2}, {1, 2, 3}}) != 3) throw new AssertionError("last edge");
        // A path graph accepts every edge in turn.
        if (examined(4, new int[][] {{0, 1, 1}, {1, 2, 1}, {2, 3, 1}}) != 3) throw new AssertionError("path");
        // The method leaves the edge array unchanged.
        int[][] keep = {{0, 1, 9}, {1, 2, 1}};
        examined(3, keep);
        if (!Arrays.deepEquals(keep, new int[][] {{0, 1, 9}, {1, 2, 1}})) throw new AssertionError("mutation");
        // Random connected graphs against the relabeling oracle.
        Random rnd = new Random(2302);
        for (int t = 0; t < 4000; t++) {
            int v = 1 + rnd.nextInt(7), extra = rnd.nextInt(8);
            List<int[]> list = new ArrayList<>();
            for (int u = 1; u < v; u++) list.add(new int[] {rnd.nextInt(u), u, 1 + rnd.nextInt(4)});
            for (int i = 0; i < extra; i++) list.add(new int[] {rnd.nextInt(v), rnd.nextInt(v), 1 + rnd.nextInt(4)});
            Collections.shuffle(list, rnd);
            int[][] g = list.toArray(new int[0][]);
            if (examined(v, g) != oracle(v, g)) throw new AssertionError("random " + t + " " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Boundary] Disconnected Weighted Graph (Author exercise)
<!-- id: dg-disconnected-weighted -->

**Approach.**
The method runs the Kruskal loop over the sorted edges and counts acceptances. After the loop, `accepted == V - 1` proves that one group remains, so the method returns the total. A smaller count proves that at least two groups remain, because every acceptance merges exactly two groups and the start has `V` groups. The method then returns -1. An empty edge list with one vertex passes the test with `accepted == 0 == V - 1` and returns 0.

Two Java details protect the result. The sum uses a `long`, because three weights of 10^9 add to more than `Integer.MAX_VALUE`. The comparator uses `Integer.compare`, because a subtraction of two `int` values overflows when the true difference leaves the `int` range. Positive weights up to 10^9 keep the subtraction safe in this contract, but the habit protects a later contract that allows negative weights. The invariant is that the groups of the union-find structure equal the connected pieces of the accepted edges, and their number equals `V - accepted`.

**Complexity.**
- **Time** is O(E log E) for the sort and O(E * alpha(V)) for the union-find work.
- **Space** is O(V + E), because the `parent` and `size` arrays hold `V` entries and the sorted copy holds `E` references.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ConnectOrReport {
    private static int find(int[] parent, int x) {
        // Path halving keeps later searches short.
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    /**
     * Returns the lowest total weight that connects all vertices, or -1 when the graph is disconnected.
     * Time: O(E log E) for the sort plus near-constant union-find work per edge.
     * Space: O(V + E) for the arrays and the sorted copy.
     * Invariant: the number of groups equals vertexCount minus accepted.
     */
    static long minCost(int vertexCount, int[][] edges) {
        int[][] sorted = edges.clone();
        // Integer.compare avoids the overflow that a subtraction can cause.
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        int[] parent = new int[vertexCount], size = new int[vertexCount];
        // Each vertex starts as a group of one.
        for (int v = 0; v < vertexCount; v++) { parent[v] = v; size[v] = 1; }
        long total = 0;
        int accepted = 0;
        // Each edge is examined once.
        for (int[] e : sorted) {
            // A complete tree needs no further edge.
            if (accepted == vertexCount - 1) break;
            int ru = find(parent, e[0]), rv = find(parent, e[1]);
            // Equal representatives mean a cycle or a self-loop.
            if (ru == rv) continue;
            // Merge the smaller group into the larger one and keep size in step with parent.
            if (size[ru] < size[rv]) { int t = ru; ru = rv; rv = t; }
            parent[rv] = ru;
            size[ru] += size[rv];
            // A long accumulator holds sums beyond the int range.
            total += e[2];
            accepted++;
        }
        // Fewer than V - 1 acceptances leave more than one group.
        return accepted == vertexCount - 1 ? total : -1;
    }

    /** Oracle: a search finds the pieces, and Prim's method on a weight matrix prices a connected graph. */
    static long oracle(int vertexCount, int[][] edges) {
        long inf = Long.MAX_VALUE / 4;
        long[][] w = new long[vertexCount][vertexCount];
        for (long[] row : w) Arrays.fill(row, inf);
        // Keep the lightest of any parallel edges and ignore self-loops.
        for (int[] e : edges) {
            if (e[0] == e[1]) continue;
            w[e[0]][e[1]] = Math.min(w[e[0]][e[1]], e[2]);
            w[e[1]][e[0]] = Math.min(w[e[1]][e[0]], e[2]);
        }
        boolean[] in = new boolean[vertexCount];
        long[] best = new long[vertexCount];
        Arrays.fill(best, inf);
        best[0] = 0;
        long total = 0;
        for (int round = 0; round < vertexCount; round++) {
            int pick = -1;
            for (int v = 0; v < vertexCount; v++) if (!in[v] && (pick == -1 || best[v] < best[pick])) pick = v;
            // The cheapest reachable vertex has no finite link, so the graph is disconnected.
            if (best[pick] >= inf) return -1;
            in[pick] = true;
            total += best[pick];
            for (int v = 0; v < vertexCount; v++) if (!in[v] && w[pick][v] < best[v]) best[v] = w[pick][v];
        }
        return total;
    }

    public static void main(String[] args) {
        // Example 1: no edge joins {0,1,2} to {3,4}.
        if (minCost(5, new int[][] {{0, 1, 3}, {1, 2, 4}, {3, 4, 1}}) != -1) throw new AssertionError("example 1");
        // Example 2: three weights of one billion exceed the int range.
        long big = minCost(4, new int[][] {{0, 1, 1000000000}, {1, 2, 1000000000}, {2, 3, 1000000000}, {0, 3, 1000000000}});
        if (big != 3000000000L) throw new AssertionError("example 2");
        // The int maximum is exceeded, which is why the accumulator is a long.
        if (3000000000L <= Integer.MAX_VALUE) throw new AssertionError("range");
        // A subtraction comparator overflows when the true difference leaves the int range.
        if (!(Integer.MAX_VALUE - (-5) < 0)) throw new AssertionError("overflow");
        // One vertex with no edge costs 0, and two vertices with no edge are disconnected.
        if (minCost(1, new int[0][]) != 0) throw new AssertionError("single vertex");
        if (minCost(2, new int[0][]) != -1) throw new AssertionError("two vertices");
        // Self-loops never connect anything.
        if (minCost(2, new int[][] {{0, 0, 1}, {1, 1, 1}}) != -1) throw new AssertionError("loops");
        // Random graphs, many of them disconnected, against the oracle.
        Random rnd = new Random(2303);
        for (int t = 0; t < 5000; t++) {
            int v = 1 + rnd.nextInt(7), m = rnd.nextInt(10);
            List<int[]> list = new ArrayList<>();
            for (int i = 0; i < m; i++) list.add(new int[] {rnd.nextInt(v), rnd.nextInt(v), 1 + rnd.nextInt(rnd.nextBoolean() ? 5 : 1000000000)});
            int[][] g = list.toArray(new int[0][]);
            if (minCost(v, g) != oracle(v, g)) throw new AssertionError("random " + t + " " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Recognize] Connect All Points At Lowest Cost (LeetCode 1584)
<!-- id: dg-min-cost-points -->

**Approach.**
The vertices are the points. Every pair is an edge whose weight is the Manhattan distance, which gives `n * (n - 1) / 2` edges. The method builds that list, sorts it by weight and runs the Kruskal loop with union-find. The loop accepts an edge only when its endpoints have different representatives, and it stops after `n - 1` acceptances. A complete graph is always connected, so the loop always reaches `n - 1` acceptances.

The invariant is that every accepted link is the cheapest link that leaves its group at that moment. The groups equal the connected pieces of the accepted links. The cost is at most 4 * 10^6 per link and 499 links, which is below 2 * 10^9, so an `int` total holds it. The method does not mutate `points`.

**Complexity.**
- **Time** is O(n^2 log n), because the sort handles about n^2 / 2 edges and the union-find work adds O(n^2 * alpha(n)).
- **Space** is O(n^2), because the explicit edge list holds every pair.

```java run
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class ConnectPoints {
    private static int find(int[] parent, int x) {
        // Path halving shortens the route to the representative.
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    /**
     * Returns the lowest total Manhattan cost of links that connect all points.
     * Time: O(n^2 log n) for sorting the n(n-1)/2 generated edges.
     * Space: O(n^2) for the explicit edge list.
     * Invariant: each accepted link is the cheapest link leaving its group at that moment.
     */
    static int minCost(int[][] points) {
        int n = points.length;
        int[][] edges = new int[n * (n - 1) / 2][];
        int count = 0;
        // Generate each unordered pair once, which is where the n^2 term of the cost comes from.
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int d = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);
                edges[count++] = new int[] {i, j, d};
            }
        }
        // Integer.compare keeps the ordering correct for any weights.
        Arrays.sort(edges, (a, b) -> Integer.compare(a[2], b[2]));
        int[] parent = new int[n];
        // Each point starts as its own group.
        for (int v = 0; v < n; v++) parent[v] = v;
        int total = 0, accepted = 0;
        // The loop examines edges from the cheapest to the dearest.
        for (int[] e : edges) {
            // n - 1 accepted links already connect every point.
            if (accepted == n - 1) break;
            int ru = find(parent, e[0]), rv = find(parent, e[1]);
            // Equal representatives mean the link adds cost and no reach.
            if (ru == rv) continue;
            parent[ru] = rv;
            total += e[2];
            accepted++;
        }
        return total;
    }

    /** Oracle: Prim's method with a distance array. */
    static int oracle(int[][] points) {
        int n = points.length;
        int[] best = new int[n];
        boolean[] in = new boolean[n];
        Arrays.fill(best, Integer.MAX_VALUE);
        best[0] = 0;
        int total = 0;
        for (int round = 0; round < n; round++) {
            int pick = -1;
            for (int v = 0; v < n; v++) if (!in[v] && (pick == -1 || best[v] < best[pick])) pick = v;
            in[pick] = true;
            total += best[pick];
            for (int v = 0; v < n; v++) {
                int d = Math.abs(points[pick][0] - points[v][0]) + Math.abs(points[pick][1] - points[v][1]);
                if (!in[v] && d < best[v]) best[v] = d;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        // Example 1: the links cost 5, 6 and 6.
        if (minCost(new int[][] {{1, 1}, {4, 5}, {0, 6}, {7, 1}}) != 17) throw new AssertionError("example 1");
        // Example 2: the two shortest links cost 10 and 11.
        if (minCost(new int[][] {{-3, 2}, {4, -1}, {1, 9}}) != 21) throw new AssertionError("example 2");
        // One point needs no link.
        if (minCost(new int[][] {{5, 5}}) != 0) throw new AssertionError("single point");
        // Two corner points cost the full Manhattan span of 4 * 10^6.
        if (minCost(new int[][] {{-1000000, -1000000}, {1000000, 1000000}}) != 4000000) throw new AssertionError("extremes");
        // The method leaves the points unchanged.
        int[][] keep = {{0, 0}, {3, 4}};
        minCost(keep);
        if (!Arrays.deepEquals(keep, new int[][] {{0, 0}, {3, 4}})) throw new AssertionError("mutation");
        // Random distinct points against the oracle.
        Random rnd = new Random(2304);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9), range = 3 + rnd.nextInt(8);
            Set<Long> used = new HashSet<>();
            int[][] pts = new int[n][];
            int made = 0;
            while (made < n) {
                int x = rnd.nextInt(range) - range / 2, y = rnd.nextInt(range) - range / 2;
                if (used.add(x * 1000L + y)) pts[made++] = new int[] {x, y};
            }
            if (minCost(pts) != oracle(pts)) throw new AssertionError("random " + t + " " + Arrays.deepToString(pts));
        }
    }
}
```
