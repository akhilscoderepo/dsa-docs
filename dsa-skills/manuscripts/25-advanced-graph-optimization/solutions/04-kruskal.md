<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Kruskal

#### Solution: [Build] Sorted Safe Edges (Author exercise)
<!-- id: ga-kr-sorted-safe-edges -->

**Approach.**
The method creates a `parent` array in which every vertex is its own root. It scans the edges in the given order. For every edge it looks up the roots of both endpoints. Different roots mean the endpoints lie in different groups, so the method records `true` and links one root below the other. Equal roots mean the edge would close a cycle, so the method records `false` and changes nothing. A self-loop has the same vertex on both sides, so its roots are always equal and it is always skipped.

The invariant is that the groups of `parent` equal the connected pieces of the accepted edges, so the accepted edges form a forest. A merge joins exactly two pieces, and a skip leaves the pieces alone. The input is already sorted, so the method does not sort and does not touch the array.

**Complexity.**
- **Time** is O(m * alpha(n)) for `m` edges, because each edge costs two `find` calls and at most one merge. The sorted input needs no sort.
- **Space** is O(n + m), because `parent` holds `n` entries and the result holds `m` flags.

```java run
import java.util.*;

public final class KruskalSortedSafeEdges {
    /**
     * Returns one flag per edge that tells whether the scan accepts that edge.
     * Time: O(m * alpha(n)). Space: O(n + m).
     * Invariant: the groups of parent equal the connected pieces of the accepted edges.
     */
    static boolean[] safeFlags(int n, int[][] edges) {
        // Each vertex starts as the root of its own group.
        int[] parent = new int[n];
        for (int v = 0; v < n; v++) parent[v] = v;
        boolean[] flags = new boolean[edges.length];
        // One pass over the edges, with no early stop, as the problem requires.
        for (int k = 0; k < edges.length; k++) {
            int ru = find(parent, edges[k][0]);
            int rv = find(parent, edges[k][1]);
            // Equal roots mean the edge lies inside a group, so the flag stays false.
            if (ru == rv) continue;
            // Different roots mean the edge joins two groups, so one root moves below the other.
            parent[rv] = ru;
            flags[k] = true;
        }
        return flags;
    }

    /** Follows parent links to the root and halves the path on the way. Time: amortized near O(1). Space: O(1). */
    static int find(int[] parent, int x) {
        // The loop ends at a root, which is the only vertex that points at itself.
        while (parent[x] != x) {
            // Pointing x at its grandparent shortens later searches.
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    /** Oracle: a label per vertex, relabeled in full on every accepted edge. */
    static boolean[] oracle(int n, int[][] edges) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        boolean[] flags = new boolean[edges.length];
        for (int k = 0; k < edges.length; k++) {
            int a = label[edges[k][0]], b = label[edges[k][1]];
            if (a == b) continue;
            // Every vertex of the second group takes the label of the first group.
            for (int v = 0; v < n; v++) if (label[v] == b) label[v] = a;
            flags[k] = true;
        }
        return flags;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(safeFlags(4, new int[][] {{0, 1, 1}, {2, 3, 2}, {1, 2, 3}, {0, 3, 4}, {1, 3, 5}}), new boolean[] {true, true, true, false, false})) throw new AssertionError("ex1");
        if (!Arrays.equals(safeFlags(3, new int[][] {{0, 0, 1}, {0, 1, 1}, {0, 1, 2}, {1, 2, 2}}), new boolean[] {false, true, false, true})) throw new AssertionError("ex2");
        // An empty edge list gives an empty result, and one vertex accepts nothing.
        if (safeFlags(1, new int[0][]).length != 0) throw new AssertionError("empty");
        // The method leaves the input array untouched.
        int[][] keep = {{0, 1, 5}, {1, 2, 6}};
        int[][] snapshot = {{0, 1, 5}, {1, 2, 6}};
        safeFlags(3, keep);
        if (!Arrays.deepEquals(keep, snapshot)) throw new AssertionError("mutated");
        // Random sorted edge lists, including self-loops and repeated edges.
        Random rnd = new Random(2504);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(6)};
            Arrays.sort(edges, (a, b) -> Integer.compare(a[2], b[2]));
            if (!Arrays.equals(safeFlags(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Stop At V Minus One (Author exercise)
<!-- id: ga-kr-stop-count -->

**Approach.**
The method orders a copy of the edges by weight. `Arrays.sort` on an array of objects is stable, so equal weights keep their input order. It then runs the same group rule as before and counts every edge whose roots are equal. After each purchase it tests whether `n - 1` edges are accepted. It leaves the loop at that moment. Edges after the stop are never examined, so they never add to the count.

The invariant has two parts. The count `skipped` equals the number of examined edges that closed a cycle. The groups equal the connected pieces of the accepted edges. The stop is valid because a connected graph with `n - 1` accepted edges has one group, and every later edge would have equal roots. The exercise states that the graph is connected, so the loop always reaches `n - 1` purchases before the edges run out.

**Complexity.**
- **Time** is O(m log m), because the sort dominates and the loop adds O(m * alpha(n)).
- **Space** is O(n + m), because the sorted copy holds `m` references and `parent` holds `n` entries.

```java run
import java.util.*;

public final class KruskalStopCount {
    /**
     * Returns how many edges the scan skips before it accepts n - 1 edges.
     * Time: O(m log m). Space: O(n + m).
     * Invariant: skipped counts examined edges with equal roots, and the groups match the accepted edges.
     */
    static int skippedBeforeStop(int n, int[][] edges) {
        // The copy keeps the caller's order intact, and the stable sort keeps input order among ties.
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        int[] parent = new int[n];
        for (int v = 0; v < n; v++) parent[v] = v;
        int bought = 0, skipped = 0;
        for (int[] e : sorted) {
            // A complete tree ends the scan, so later edges are not examined.
            if (bought == n - 1) break;
            int ru = find(parent, e[0]);
            int rv = find(parent, e[1]);
            // Equal roots mean a cycle, so the edge counts as skipped.
            if (ru == rv) {
                skipped++;
                continue;
            }
            // Different roots mean a purchase and a merge.
            parent[rv] = ru;
            bought++;
        }
        return skipped;
    }

    /** Follows parent links to the root and halves the path. Time: amortized near O(1). Space: O(1). */
    static int find(int[] parent, int x) {
        // Stops at the root, which points at itself.
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    /** Oracle: full relabeling over a manually sorted copy, with an insertion sort that keeps ties stable. */
    static int oracle(int n, int[][] edges) {
        List<int[]> list = new ArrayList<>();
        for (int[] e : edges) {
            int pos = list.size();
            // Insert after the last edge of weight at most e[2], which keeps equal weights in input order.
            while (pos > 0 && list.get(pos - 1)[2] > e[2]) pos--;
            list.add(pos, e);
        }
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        int bought = 0, skipped = 0;
        for (int[] e : list) {
            if (bought == n - 1) break;
            int a = label[e[0]], b = label[e[1]];
            if (a == b) { skipped++; continue; }
            for (int v = 0; v < n; v++) if (label[v] == b) label[v] = a;
            bought++;
        }
        return skipped;
    }

    /** Builds a random connected multigraph by chaining a random order of vertices and adding extra edges. */
    static int[][] randomConnected(Random rnd, int n) {
        List<int[]> list = new ArrayList<>();
        for (int v = 1; v < n; v++) list.add(new int[] {rnd.nextInt(v), v, rnd.nextInt(6)});
        int extra = rnd.nextInt(8);
        for (int i = 0; i < extra; i++) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(6)});
        Collections.shuffle(list, rnd);
        return list.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] a = {{0, 1, 4}, {1, 2, 1}, {0, 2, 3}, {2, 3, 2}, {1, 3, 5}, {3, 4, 6}, {0, 3, 2}, {1, 4, 7}};
        if (skippedBeforeStop(5, a) != 3) throw new AssertionError("ex1");
        int[][] b = {{0, 1, 2}, {1, 2, 2}, {0, 2, 2}, {2, 3, 9}, {0, 3, 9}};
        if (skippedBeforeStop(4, b) != 1) throw new AssertionError("ex2");
        // One vertex needs no edge, and no scan happens.
        if (skippedBeforeStop(1, new int[0][]) != 0) throw new AssertionError("single");
        // Java fact: Arrays.sort on an object array is stable, so a tie keeps input order.
        int[][] ties = {{9, 9, 1}, {8, 8, 1}, {7, 7, 1}};
        int[][] copy = ties.clone();
        Arrays.sort(copy, (x, y) -> Integer.compare(x[2], y[2]));
        if (copy[0][0] != 9 || copy[1][0] != 8 || copy[2][0] != 7) throw new AssertionError("stable");
        // The input array order stays as the caller gave it.
        skippedBeforeStop(4, b);
        if (b[0][2] != 2 || b[3][2] != 9 || b[4][0] != 0) throw new AssertionError("mutated");
        // Random connected graphs with zero weights and repeated edges.
        Random rnd = new Random(2514);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] edges = randomConnected(rnd, n);
            if (skippedBeforeStop(n, edges) != oracle(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Equal Weights And Disconnection (Author exercise)
<!-- id: ga-kr-forest-tally -->

**Approach.**
The method orders a copy of the edges and then scans all of them. It starts with `groups` equal to `n`. Each accepted edge merges two groups, so the method lowers `groups` by one and adds the weight to a `long` total. An edge with equal roots changes nothing. The scan has no early stop based on `n - 1`, because a disconnected graph never reaches that count. The scan ends with the last edge. The result pairs the final `groups` with the total.

The invariant is that `groups` equals the number of connected pieces of the accepted edges, and `total` is the sum of their weights. Equal weights may appear in any order. Two lightest crossing edges of the same weight are both safe, so either choice keeps the total the same. The solution checks this by shuffling ties. The total uses `long` because two weights of 2000000000 already exceed `Integer.MAX_VALUE`, and the solution asserts that fact.

**Complexity.**
- **Time** is O(m log m), because the sort dominates and the loop adds O(m * alpha(n)).
- **Space** is O(n + m), because the sorted copy holds `m` references and `parent` holds `n` entries.

```java run
import java.util.*;

public final class KruskalForestTally {
    /**
     * Returns {groups left, total weight of accepted edges} for a possibly disconnected graph.
     * Time: O(m log m). Space: O(n + m).
     * Invariant: groups counts the connected pieces of the accepted edges, and total sums their weights.
     */
    static long[] forestTally(int n, int[][] edges) {
        // Sorting a copy leaves the caller's array unchanged.
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        int[] parent = new int[n];
        for (int v = 0; v < n; v++) parent[v] = v;
        // Every vertex starts alone, so there are n groups.
        long groups = n;
        // A long accumulator holds sums beyond the int range.
        long total = 0;
        for (int[] e : sorted) {
            int ru = find(parent, e[0]);
            int rv = find(parent, e[1]);
            // Equal roots mean the edge would close a cycle.
            if (ru == rv) continue;
            // A merge joins two groups into one.
            parent[rv] = ru;
            groups--;
            total += e[2];
        }
        return new long[] {groups, total};
    }

    /** Follows parent links to the root and halves the path. Time: amortized near O(1). Space: O(1). */
    static int find(int[] parent, int x) {
        // The loop stops at the root.
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    /** Oracle: counts pieces by repeated search and takes the cheapest crossing edge in each round (Boruvka style, with index ties). */
    static long[] oracle(int n, int[][] edges) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        long total = 0;
        while (true) {
            // Find the lightest edge that joins two different pieces; the lower index wins a tie.
            int best = -1;
            for (int k = 0; k < edges.length; k++) {
                if (label[edges[k][0]] == label[edges[k][1]]) continue;
                if (best == -1 || edges[k][2] < edges[best][2]) best = k;
            }
            if (best == -1) break;
            int a = label[edges[best][0]], b = label[edges[best][1]];
            for (int v = 0; v < n; v++) if (label[v] == b) label[v] = a;
            total += edges[best][2];
        }
        Set<Integer> pieces = new HashSet<>();
        for (int v = 0; v < n; v++) pieces.add(label[v]);
        return new long[] {pieces.size(), total};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        long big = 2_000_000_000L;
        if (!Arrays.equals(forestTally(3, new int[][] {{0, 1, 2_000_000_000}, {1, 2, 2_000_000_000}, {0, 2, 2_000_000_000}}), new long[] {1, 2 * big})) throw new AssertionError("ex1");
        if (!Arrays.equals(forestTally(5, new int[][] {{0, 1, 2}, {1, 0, 2}, {2, 3, 7}}), new long[] {3, 9})) throw new AssertionError("ex2");
        // Java fact: two weights of 2000000000 overflow an int sum but not a long sum.
        if (2_000_000_000 + 2_000_000_000 >= 0) throw new AssertionError("int overflow");
        if (2_000_000_000L + 2_000_000_000 != 4_000_000_000L) throw new AssertionError("long sum");
        // Java fact: subtracting extreme int weights flips the sign, which is why the sort uses Integer.compare.
        if (Integer.MAX_VALUE - (-5) >= 0) throw new AssertionError("subtract overflow");
        // No edges leave every vertex alone with total zero.
        if (!Arrays.equals(forestTally(4, new int[0][]), new long[] {4, 0})) throw new AssertionError("no edges");
        // Random graphs, and the same graph with tied edges shuffled gives the same result.
        Random rnd = new Random(2524);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(12);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(4)};
            long[] got = forestTally(n, edges);
            if (!Arrays.equals(got, oracle(n, edges))) throw new AssertionError("random " + t);
            List<int[]> shuffled = new ArrayList<>(Arrays.asList(edges));
            Collections.shuffle(shuffled, rnd);
            if (!Arrays.equals(got, forestTally(n, shuffled.toArray(new int[0][])))) throw new AssertionError("ties " + t);
        }
    }
}
```

#### Solution: [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: ga-kr-heaviest-link -->

**Approach.**
The method turns the points into edges, one edge for every pair, with the Manhattan distance as the weight. It sorts the edges, then runs the group rule. Every purchase has a weight at least as large as the one before it, so the last purchase is the heaviest accepted edge. The method returns the weight of the last purchase, and it returns 0 for a single point because no purchase happens. The answer does not depend on tie order, because every cheapest spanning tree has the same sorted list of weights.

The invariant has two parts. The accepted edges form a forest whose groups equal the connected pieces. Each accepted edge is a lightest edge that leaves its group. The heaviest accepted edge is also the smallest limit `t` for which the edges of weight at most `t` connect all points. The oracle uses that second description. The method stores all `n * (n - 1) / 2` edges, which is more memory than Prim needs. Prim keeps one best distance per point and stays at O(n) extra memory on top of the points. Kruskal trades that memory for a simpler loop and an early stop.

**Complexity.**
- **Time** is O(n^2 log n), because there are about n^2 / 2 edges. The sort costs O(n^2 log n^2), which equals O(n^2 log n), and the union-find calls add O(n^2 * alpha(n)).
- **Space** is O(n^2), because the method stores every pair as an edge, whereas Prim needs only O(n) beyond the input.

```java run
import java.util.*;

public final class KruskalHeaviestLink {
    /**
     * Returns the largest connection cost among the connections of a cheapest plan that joins all points.
     * Time: O(n^2 log n). Space: O(n^2).
     * Invariant: accepted edges form a forest, and each is a lightest edge leaving its group.
     */
    static int heaviestLink(int[][] points) {
        int n = points.length;
        // A single point needs no connection.
        if (n == 1) return 0;
        // One edge per pair, stored as {i, j, distance}; this is the n * (n - 1) / 2 memory cost.
        int[][] edges = new int[n * (n - 1) / 2][];
        int idx = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int d = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);
                edges[idx++] = new int[] {i, j, d};
            }
        }
        // Integer.compare avoids the overflow that a subtraction of weights could cause.
        Arrays.sort(edges, (a, b) -> Integer.compare(a[2], b[2]));
        int[] parent = new int[n];
        for (int v = 0; v < n; v++) parent[v] = v;
        int bought = 0, last = 0;
        for (int[] e : edges) {
            // The tree is complete after n - 1 purchases, so the scan stops.
            if (bought == n - 1) break;
            int ri = find(parent, e[0]);
            int rj = find(parent, e[1]);
            // Equal roots mean the pair is already connected.
            if (ri == rj) continue;
            parent[rj] = ri;
            // Weights come in nondecreasing order, so the latest purchase is the heaviest so far.
            last = e[2];
            bought++;
        }
        return last;
    }

    /** Follows parent links to the root and halves the path. Time: amortized near O(1). Space: O(1). */
    static int find(int[] parent, int x) {
        // The loop ends at the root.
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    /** Oracle: the smallest limit t such that pairs at distance at most t connect all points, tested by flood fill. */
    static int oracle(int[][] points) {
        int n = points.length;
        for (int t = 0; ; t++) {
            boolean[] seen = new boolean[n];
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(0);
            seen[0] = true;
            int count = 1;
            while (!stack.isEmpty()) {
                int u = stack.pop();
                for (int v = 0; v < n; v++) {
                    int d = Math.abs(points[u][0] - points[v][0]) + Math.abs(points[u][1] - points[v][1]);
                    if (!seen[v] && d <= t) {
                        seen[v] = true;
                        count++;
                        stack.push(v);
                    }
                }
            }
            if (count == n) return t;
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (heaviestLink(new int[][] {{0, 0}, {1, 1}, {1, 0}, {5, 5}}) != 8) throw new AssertionError("ex1");
        if (heaviestLink(new int[][] {{0, 0}, {0, 4}, {9, 0}}) != 9) throw new AssertionError("ex2");
        // One point returns 0, and two points return their distance.
        if (heaviestLink(new int[][] {{7, -3}}) != 0) throw new AssertionError("single");
        if (heaviestLink(new int[][] {{-1000000, -1000000}, {1000000, 1000000}}) != 4_000_000) throw new AssertionError("far");
        // Java fact: the pair count for 500 points is 124750 and fits an int array index.
        if (500 * 499 / 2 != 124_750) throw new AssertionError("pairs");
        // The method leaves the points unchanged.
        int[][] pts = {{3, 3}, {0, 0}};
        heaviestLink(pts);
        if (pts[0][0] != 3 || pts[1][1] != 0) throw new AssertionError("mutated");
        // Random distinct point sets against the flood fill oracle.
        Random rnd = new Random(2534);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7);
            Set<Long> used = new HashSet<>();
            int[][] pts2 = new int[n][];
            for (int i = 0; i < n; i++) {
                int x, y;
                do { x = rnd.nextInt(15) - 7; y = rnd.nextInt(15) - 7; } while (!used.add(x * 100L + y));
                pts2[i] = new int[] {x, y};
            }
            if (heaviestLink(pts2) != oracle(pts2)) throw new AssertionError("random " + t);
        }
    }
}
```
