<!-- solutions-for: 92-preprocessed-query-apis -->
### Solutions For Preprocessed Query APIs

#### Solution: [Build] Kth Ancestor Of A Tree Node (LeetCode 1483)
<!-- id: dq39-kth-ancestor -->

**Approach.**
The constructor spends O(n log n) time once, because the workload has no updates and many online queries. Row 0 of the table holds the parent of each node, and row `j` holds the ancestor `2^j` steps up. Each row comes from the row below it, because `2^j` steps are two blocks of `2^(j-1)` steps. A missing ancestor stays `-1` all the way up, so a jump from `-1` is never attempted.

A query reads the bits of `k` from the lowest bit to the highest. For each set bit `j`, the current node moves to `up[j][node]`. The loop stops early when the node becomes `-1`. If `k` has a bit above the last row, or if `k` is at least `n`, no node has an ancestor that far away, so the method returns `-1` before the loop.

The invariant is that after the bits below `j` are processed, `node` is the ancestor of the start at distance equal to the low `j` bits of `k`, or `-1` when it does not exist. The oracle walks the parent array one step at a time on random trees whose parent labels are not ordered, and it compares every answer.

**Complexity.**
- **Time** is O(n log n) for the constructor and O(log k) per query, because each query inspects at most `bits(n)` table entries.
- **Space** is O(n log n) for the table of `n` entries in each of about `log n` rows.

```java run
import java.util.Random;

public final class KthAncestorSolution {
    static final class TreeLifting {
        private final int[][] up; // up[j][v] is the ancestor of v that is 2^j steps up, or -1
        private final int n;

        /**
         * Builds the jump table from the parent array.
         * Time: O(n log n). Space: O(n log n).
         * Invariant: row j equals row j-1 applied twice, so it holds the 2^j-th ancestor.
         */
        TreeLifting(int n, int[] parent) {
            this.n = n;
            // Enough rows to cover every distance from 1 to n - 1.
            int rows = 1;
            while ((1 << rows) < n) rows++;
            up = new int[rows][];
            // Row 0 is a copy of the parent array.
            up[0] = parent.clone();
            for (int j = 1; j < rows; j++) {
                up[j] = new int[n];
                for (int v = 0; v < n; v++) {
                    int mid = up[j - 1][v]; // the node 2^(j-1) steps up
                    // A missing midpoint means the whole jump leaves the tree.
                    up[j][v] = mid == -1 ? -1 : up[j - 1][mid];
                }
            }
        }

        /**
         * Returns the k-th ancestor of node, or -1 when the root is closer than k steps.
         * Time: O(log k). Space: O(1).
         * Invariant: after bit j, cur is the ancestor at the distance given by the low j+1 bits of k.
         */
        int kth(int node, int k) {
            // No node has an ancestor n or more steps away.
            if (k >= n) return -1;
            int cur = node;
            // Visit the set bits of k from low to high; stop once the node leaves the tree.
            for (int j = 0; k >> j != 0 && cur != -1; j++) {
                // A set bit means a jump of 2^j steps through one table read.
                if ((k >> j & 1) == 1) cur = up[j][cur];
            }
            return cur;
        }
    }

    /** Brute force: follows the parent pointer k times. */
    static int oracle(int[] parent, int node, int k) {
        int cur = node;
        // Each step moves one level up; -1 absorbs further steps.
        for (int i = 0; i < k && cur != -1; i++) cur = parent[cur];
        return cur;
    }

    public static void main(String[] args) {
        // Example 1: a tree with a branch at nodes 3 and 6, including k = 0 and a miss.
        int[] p1 = {-1, 0, 0, 1, 1, 2, 3, 6, 6};
        TreeLifting t1 = new TreeLifting(9, p1);
        int[][] q1 = {{8, 2}, {8, 3}, {8, 4}, {4, 1}, {4, 2}, {5, 0}};
        int[] e1 = {3, 1, 0, 1, 0, 5};
        for (int i = 0; i < q1.length; i++) {
            if (t1.kth(q1[i][0], q1[i][1]) != e1[i]) throw new AssertionError("example 1 query " + i);
        }
        // Example 2: a path where k equals the depth and then exceeds it by one.
        TreeLifting t2 = new TreeLifting(5, new int[] {-1, 0, 1, 2, 3});
        if (t2.kth(4, 4) != 0 || t2.kth(4, 5) != -1 || t2.kth(2, 1) != 1 || t2.kth(0, 1) != -1) {
            throw new AssertionError("example 2");
        }
        // A single node has no table rows beyond row 0 and still answers.
        TreeLifting one = new TreeLifting(1, new int[] {-1});
        if (one.kth(0, 0) != 0 || one.kth(0, 1) != -1) throw new AssertionError("single node");
        // Random trees with unordered labels against the oracle for every node and every k.
        Random rnd = new Random(39);
        for (int trial = 0; trial < 400; trial++) {
            int n = 1 + rnd.nextInt(40);
            int[] order = new int[n];
            for (int i = 0; i < n; i++) order[i] = i;
            // Shuffle every label except the root 0, which stays first.
            for (int i = n - 1; i > 1; i--) {
                int j = 1 + rnd.nextInt(i);
                int tmp = order[i]; order[i] = order[j]; order[j] = tmp;
            }
            int[] parent = new int[n];
            parent[0] = -1;
            // Each later label attaches to an earlier label, so there is no cycle.
            for (int i = 1; i < n; i++) parent[order[i]] = order[rnd.nextInt(i)];
            TreeLifting t = new TreeLifting(n, parent);
            for (int v = 0; v < n; v++) {
                for (int k = 0; k <= n + 2; k++) {
                    if (t.kth(v, k) != oracle(parent, v, k)) throw new AssertionError("trial " + trial);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Counting Values In A Range (LeetCode 2080)
<!-- id: dq39-value-range-count -->

**Approach.**
A position list per value answers a single value, but a value range would need one binary search per distinct value inside the range. The structure here keeps the positions together instead. The constructor builds a tree over the index range, and each node stores the values of its index segment in sorted order. A query splits `[left, right]` into O(log n) nodes whose segments lie fully inside the range, and each such node counts values in `[lo, hi]` with two binary searches.

The invariant is that every node holds exactly the values of its segment, sorted, so the count inside a node is the difference of an upper bound and a lower bound. A merge of the two children builds the node in linear time, so each level of the tree costs O(n). The oracle scans the range for each query on random arrays with duplicates and negative values.

**Complexity.**
- **Time** is O(n log n) for the constructor and O(log^2 n) per query, because a query visits O(log n) nodes and each node costs one binary search.
- **Space** is O(n log n), because each of the log n levels stores all n values once.

```java run
import java.util.Random;

public final class ValueRangeSolution {
    static final class RangeValueCount {
        private final int[][] tree; // tree[node] holds the sorted values of the node's index segment
        private final int n;

        RangeValueCount(int[] arr) {
            n = arr.length;
            // A recursive layout of 4n nodes is enough for any length.
            tree = new int[4 * n][];
            build(1, 0, n - 1, arr);
        }

        /**
         * Builds the sorted list of one segment from its two children.
         * Time: O(n log n) over the whole tree. Space: O(n log n).
         * Invariant: tree[node] is the sorted multiset of arr[lo..hi].
         */
        private void build(int node, int lo, int hi, int[] arr) {
            // A leaf stores its single value.
            if (lo == hi) { tree[node] = new int[] {arr[lo]}; return; }
            int mid = (lo + hi) >>> 1;
            build(2 * node, lo, mid, arr);
            build(2 * node + 1, mid + 1, hi, arr);
            int[] a = tree[2 * node], b = tree[2 * node + 1], m = new int[a.length + b.length];
            int i = 0, j = 0, k = 0;
            // Standard merge of two sorted lists in linear time.
            while (i < a.length || j < b.length) {
                // Take from a when b is exhausted or a's head is not larger.
                m[k++] = (j == b.length || (i < a.length && a[i] <= b[j])) ? a[i++] : b[j++];
            }
            tree[node] = m;
        }

        /** Returns the count of indices in [left, right] with lo <= value <= hi. Time O(log^2 n). */
        int count(int left, int right, int lo, int hi) {
            // An empty value range matches nothing.
            if (lo > hi) return 0;
            return query(1, 0, n - 1, left, right, lo, hi);
        }

        /**
         * Sums the counts of the nodes that lie fully inside [left, right].
         * Time: O(log^2 n). Space: O(log n) recursion.
         * Invariant: each returned count covers exactly the part of the node segment inside the range.
         */
        private int query(int node, int s, int e, int left, int right, int lo, int hi) {
            // A segment outside the index range contributes nothing.
            if (right < s || e < left) return 0;
            // A segment fully inside is answered by two binary searches on its sorted list.
            if (left <= s && e <= right) return upper(tree[node], hi) - lower(tree[node], lo);
            int mid = (s + e) >>> 1;
            return query(2 * node, s, mid, left, right, lo, hi) + query(2 * node + 1, mid + 1, e, left, right, lo, hi);
        }

        /** First position whose value is at least x. */
        private static int lower(int[] a, int x) {
            int l = 0, r = a.length;
            // The invariant keeps every value before l below x.
            while (l < r) { int m = (l + r) >>> 1; if (a[m] < x) l = m + 1; else r = m; }
            return l;
        }

        /** First position whose value is greater than x. */
        private static int upper(int[] a, int x) {
            int l = 0, r = a.length;
            // The invariant keeps every value before l at most x.
            while (l < r) { int m = (l + r) >>> 1; if (a[m] <= x) l = m + 1; else r = m; }
            return l;
        }
    }

    /** Brute force: scans the index range and tests each value. */
    static int oracle(int[] arr, int left, int right, int lo, int hi) {
        int c = 0;
        // Each entry in the range is tested against both value bounds.
        for (int i = left; i <= right; i++) if (arr[i] >= lo && arr[i] <= hi) c++;
        return c;
    }

    public static void main(String[] args) {
        // Example 1: duplicates, a value range spanning several values, and a miss.
        RangeValueCount r1 = new RangeValueCount(new int[] {5, 1, 5, 9, 2, 5, 9, 1});
        int[][] q1 = {{0, 7, 1, 5}, {2, 5, 5, 9}, {3, 3, 10, 20}, {0, 4, 6, 8}, {1, 6, 2, 2}};
        int[] e1 = {6, 3, 0, 0, 1};
        for (int i = 0; i < q1.length; i++) {
            if (r1.count(q1[i][0], q1[i][1], q1[i][2], q1[i][3]) != e1[i]) throw new AssertionError("example 1 query " + i);
        }
        // Example 2: negative values, repeated values and the full int range.
        RangeValueCount r2 = new RangeValueCount(new int[] {-3, -3, 0, 7, -3});
        if (r2.count(0, 4, -3, -3) != 3 || r2.count(1, 3, -5, 0) != 2 || r2.count(0, 4, 1, 6) != 0
                || r2.count(2, 4, -10, 10) != 3) throw new AssertionError("example 2");
        // Extreme bounds and a reversed value range.
        if (r2.count(0, 4, Integer.MIN_VALUE, Integer.MAX_VALUE) != 5 || r2.count(0, 4, 5, 1) != 0) {
            throw new AssertionError("bounds");
        }
        // Random arrays against the oracle on random index and value ranges.
        Random rnd = new Random(392);
        for (int trial = 0; trial < 500; trial++) {
            int n = 1 + rnd.nextInt(30);
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) arr[i] = rnd.nextInt(15) - 7;
            RangeValueCount t = new RangeValueCount(arr);
            for (int q = 0; q < 40; q++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n), l = Math.min(a, b), r = Math.max(a, b);
                int lo = rnd.nextInt(17) - 8, hi = lo + rnd.nextInt(9) - 1;
                if (t.count(l, r, lo, hi) != oracle(arr, l, r, lo, hi)) throw new AssertionError("trial " + trial);
            }
        }
    }
}
```

#### Solution: [Boundary] Limit Queries On A Growing Graph (LeetCode 1724)
<!-- id: dq39-growing-limited-paths -->

**Approach.**
The index is the minimum spanning forest of the edges seen so far, rooted per tree, with a jump table that stores for each node the ancestor and the maximum edge weight along the jump. A query asks whether the maximum weight on the tree route between two nodes is below the limit, which equals the existence of a path with all edges below the limit. The forest is a minimum bottleneck structure, so the forest path minimizes its heaviest edge over all graph paths.

An inserted edge changes that index only in two cases. The endpoints are in different trees, or the heaviest edge on their current tree path is strictly heavier than the new edge. In every other case the forest stays valid, so the insertion costs one path query and no rebuild. When the edge does change the forest, the index is marked stale. Later insertions then append to the edge list without any check, because one rebuild covers all of them. The rebuild runs inside the next query, at most once per query, and it clears the stale mark.

The invariant is that when the stale mark is clear, the stored forest is a minimum spanning forest of all edges, and when it is set, the edge list still holds every edge so a rebuild restores the first case. The oracle answers each query with a union-find over all edges below the limit. A second oracle model decides staleness by recomputing the total forest weight and the component count with Kruskal, which does not use the jump table.

**Complexity.**
- **Time** is O(E log E) per rebuild, O(log n) per query without a rebuild and O(log n) per insertion that checks the index.
- **Space** is O(E + n log n) for the edge list and the jump tables.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class GrowingLimitedPathsSolution {
    static final class GrowingPaths {
        private final int n;
        private final List<int[]> edges = new ArrayList<>(); // {u, v, w}, every edge ever inserted
        private final int rows;
        private int[][] up, heavy; // up[j][v]: 2^j-th ancestor in the forest; heavy[j][v]: heaviest edge on that jump
        private int[] depth, comp;
        private boolean stale;
        private int rebuilds;

        GrowingPaths(int n, int[][] initial) {
            this.n = n;
            int r = 1;
            // Enough rows for the longest possible tree path.
            while ((1 << r) < Math.max(2, n)) r++;
            rows = r;
            for (int[] e : initial) edges.add(e.clone());
            build(); // the constructor build is not counted in rebuilds
        }

        /**
         * Rebuilds the forest and the jump tables from the full edge list.
         * Time: O(E log E + n log n). Space: O(E + n log n).
         * Invariant: afterwards the tables describe a minimum spanning forest of every stored edge.
         */
        private void build() {
            int[][] sorted = edges.toArray(new int[0][]);
            // Kruskal needs the edges by weight.
            Arrays.sort(sorted, (x, y) -> Integer.compare(x[2], y[2]));
            int[] dsu = new int[n];
            for (int i = 0; i < n; i++) dsu[i] = i;
            List<List<int[]>> adj = new ArrayList<>();
            for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
            for (int[] e : sorted) {
                int a = find(dsu, e[0]), b = find(dsu, e[1]);
                // Keep an edge only when it joins two different trees.
                if (a != b) {
                    dsu[a] = b;
                    adj.get(e[0]).add(new int[] {e[1], e[2]});
                    adj.get(e[1]).add(new int[] {e[0], e[2]});
                }
            }
            up = new int[rows][n];
            heavy = new int[rows][n];
            depth = new int[n];
            comp = new int[n];
            Arrays.fill(comp, -1);
            // Root every tree at its smallest unvisited node with an iterative walk.
            for (int root = 0; root < n; root++) {
                if (comp[root] != -1) continue;
                comp[root] = root;
                up[0][root] = root;
                heavy[0][root] = 0;
                List<Integer> stack = new ArrayList<>();
                stack.add(root);
                while (!stack.isEmpty()) {
                    int u = stack.remove(stack.size() - 1);
                    for (int[] nb : adj.get(u)) {
                        if (comp[nb[0]] != -1) continue; // already placed, so this is the parent side
                        comp[nb[0]] = root;
                        depth[nb[0]] = depth[u] + 1;
                        up[0][nb[0]] = u;
                        heavy[0][nb[0]] = nb[1];
                        stack.add(nb[0]);
                    }
                }
            }
            // Each row doubles the jump and keeps the heavier of the two halves.
            for (int j = 1; j < rows; j++) {
                for (int v = 0; v < n; v++) {
                    int mid = up[j - 1][v];
                    up[j][v] = up[j - 1][mid];
                    heavy[j][v] = Math.max(heavy[j - 1][v], heavy[j - 1][mid]);
                }
            }
        }

        private static int find(int[] d, int x) {
            // Path halving keeps the finds short.
            while (d[x] != x) { d[x] = d[d[x]]; x = d[x]; }
            return x;
        }

        /** Heaviest edge on the forest path between two nodes of one tree; 0 when they are equal. */
        private int pathMax(int a, int b) {
            if (depth[a] < depth[b]) { int t = a; a = b; b = t; }
            int best = 0, diff = depth[a] - depth[b];
            // Lift the deeper node by the depth difference, one set bit at a time.
            for (int j = 0; diff >> j != 0; j++) {
                if ((diff >> j & 1) == 1) { best = Math.max(best, heavy[j][a]); a = up[j][a]; }
            }
            if (a == b) return best;
            // Lift both nodes together while their ancestors differ.
            for (int j = rows - 1; j >= 0; j--) {
                if (up[j][a] != up[j][b]) {
                    best = Math.max(best, Math.max(heavy[j][a], heavy[j][b]));
                    a = up[j][a];
                    b = up[j][b];
                }
            }
            // One last step on each side reaches the common parent.
            return Math.max(best, Math.max(heavy[0][a], heavy[0][b]));
        }

        /**
         * Stores an edge and marks the index stale only when the edge changes the forest.
         * Time: O(log n) when the index is fresh, O(1) when it is already stale.
         * Invariant: a clear stale mark means the tables match all stored edges.
         */
        void addEdge(int u, int v, int w) {
            edges.add(new int[] {u, v, w});
            // A stale index is rebuilt anyway, so no check is needed.
            if (stale) return;
            // Different trees, or a heavier path, means the forest must change.
            if (comp[u] != comp[v] || pathMax(u, v) > w) stale = true;
        }

        /** Returns whether a path from p to q uses only edges with weight below limit. */
        boolean query(int p, int q, int limit) {
            // The first query after a forest change pays for one rebuild.
            if (stale) { build(); stale = false; rebuilds++; }
            // Nodes in different trees have no path at all.
            if (comp[p] != comp[q]) return false;
            return pathMax(p, q) < limit;
        }

        int rebuildCount() { return rebuilds; }
    }

    /** Oracle: union-find over all edges below the limit. */
    static boolean oracle(int n, List<int[]> edges, int p, int q, int limit) {
        int[] d = new int[n];
        for (int i = 0; i < n; i++) d[i] = i;
        // Every light edge joins two sets.
        for (int[] e : edges) if (e[2] < limit) d[find(d, e[0])] = find(d, e[1]);
        return find(d, p) == find(d, q);
    }

    private static int find(int[] d, int x) {
        while (d[x] != x) { d[x] = d[d[x]]; x = d[x]; }
        return x;
    }

    /** Kruskal summary {components, total weight}; it equals the summary before an insertion exactly when the forest stays valid. */
    static long[] summary(int n, List<int[]> edges) {
        int[][] s = edges.toArray(new int[0][]);
        Arrays.sort(s, (x, y) -> Integer.compare(x[2], y[2]));
        int[] d = new int[n];
        for (int i = 0; i < n; i++) d[i] = i;
        long comps = n, total = 0;
        // Count joins and their weights.
        for (int[] e : s) {
            int a = find(d, e[0]), b = find(d, e[1]);
            if (a != b) { d[a] = b; comps--; total += e[2]; }
        }
        return new long[] {comps, total};
    }

    public static void main(String[] args) {
        // Example 1: a rebuild after a useful edge, and no rebuild for useless edges.
        GrowingPaths g = new GrowingPaths(5, new int[][] {{0, 1, 3}, {1, 2, 6}});
        boolean[] got = new boolean[10];
        got[0] = g.query(0, 2, 7);
        g.addEdge(0, 2, 9);
        got[2] = g.query(0, 2, 6);
        g.addEdge(0, 2, 4);
        g.addEdge(3, 4, 2);
        got[5] = g.query(0, 2, 5);
        got[6] = g.query(3, 4, 3);
        g.addEdge(0, 1, 3);
        got[8] = g.query(0, 2, 5);
        got[9] = g.query(2, 3, 100);
        boolean[] exp = {true, false, false, false, false, true, true, false, true, false};
        for (int i : new int[] {0, 2, 5, 6, 8, 9}) if (got[i] != exp[i]) throw new AssertionError("example 1 call " + i);
        if (g.rebuildCount() != 1) throw new AssertionError("example 1 rebuilds " + g.rebuildCount());
        // Example 2: an empty start, stale insertions that skip the check, and two rebuilds.
        GrowingPaths h = new GrowingPaths(4, new int[0][]);
        if (h.query(0, 1, 5)) throw new AssertionError("example 2 first");
        h.addEdge(0, 1, 4);
        h.addEdge(0, 1, 4);
        h.addEdge(0, 1, 2);
        h.addEdge(1, 1, 1);
        if (!h.query(0, 1, 3) || h.query(0, 1, 2)) throw new AssertionError("example 2 limits");
        h.addEdge(2, 3, 8);
        h.addEdge(1, 2, 1);
        if (!h.query(0, 3, 9) || h.query(0, 3, 8)) throw new AssertionError("example 2 chain");
        if (h.rebuildCount() != 2) throw new AssertionError("example 2 rebuilds " + h.rebuildCount());
        // Random workloads: answers against union-find, rebuilds against the Kruskal summary model.
        Random rnd = new Random(1724);
        for (int trial = 0; trial < 600; trial++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> all = new ArrayList<>();
            int init = rnd.nextInt(5);
            int[][] first = new int[init][];
            for (int i = 0; i < init; i++) {
                first[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(9)};
                all.add(first[i]);
            }
            GrowingPaths t = new GrowingPaths(n, first);
            boolean modelStale = false;
            int modelRebuilds = 0;
            long[] sum = summary(n, all);
            for (int step = 0; step < 30; step++) {
                if (rnd.nextInt(2) == 0) {
                    int[] e = {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(9)};
                    all.add(e);
                    t.addEdge(e[0], e[1], e[2]);
                    long[] now = summary(n, all);
                    // The model marks stale only from a fresh state, exactly as the contract says.
                    if (!modelStale && (now[0] != sum[0] || now[1] != sum[1])) modelStale = true;
                    sum = now;
                } else {
                    int p = rnd.nextInt(n), q = rnd.nextInt(n), limit = 1 + rnd.nextInt(11);
                    // The model rebuilds once per stale query.
                    if (modelStale) { modelStale = false; modelRebuilds++; }
                    if (t.query(p, q, limit) != oracle(n, all, p, q, limit)) throw new AssertionError("trial " + trial);
                    if (t.rebuildCount() != modelRebuilds) throw new AssertionError("rebuild count in trial " + trial);
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Edge Cost Decreases With A Fixed Source (LeetCode 2642)
<!-- id: dq39-source-decrease -->

**Approach.**
The workload has one fixed source, many cost decreases and queries that ask for one distance, with no future knowledge. An all-pairs table would cost n^2 memory and repair work that no query needs. A fresh search per query would cost O(m log n) for each of the many queries. The cheaper plan keeps one distance array from the source and makes the query a plain array read.

A decrease of edge `(a, b)` can only help paths that use that edge. If `dist[a] + newCost` is not below `dist[b]`, no distance changes and the method returns after one comparison. Otherwise `dist[b]` drops, and the node `b` starts a Dijkstra-style relaxation that touches only nodes whose distance improves. Costs never rise, so a distance that has dropped never needs to rise again, and each improved node settles through the usual priority-queue rule.

The invariant is that after every call `dist[v]` is the true shortest cost from the source to `v`, or infinity. The relaxation works because all improvements stem from `b`, and every node whose shortest path changes lies behind `b` on its new path. The oracle runs Bellman-Ford from the source on the current edge costs after each update.

**Complexity.**
- **Time** is O(m log n) in the worst case per decrease, O(1) when no distance changes, O(1) per query and O((n + m) log n) for the constructor.
- **Space** is O(n + m) for the adjacency lists and the distance array.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class SourceDecreaseSolution {
    static final class SourceCosts {
        private static final long INF = Long.MAX_VALUE / 4;
        private final int n;
        private final List<int[]>[] out; // out[a] holds {b, edgeId}
        private final long[] cost;       // cost[edgeId] is the current cost
        private final int[] from, to;
        private final long[] dist;

        @SuppressWarnings("unchecked")
        SourceCosts(int n, int source, int[][] edges) {
            this.n = n;
            out = new List[n];
            for (int i = 0; i < n; i++) out[i] = new ArrayList<>();
            cost = new long[edges.length];
            from = new int[edges.length];
            to = new int[edges.length];
            // Each edge keeps a stable id so a later decrease finds it by pair.
            for (int i = 0; i < edges.length; i++) {
                from[i] = edges[i][0]; to[i] = edges[i][1]; cost[i] = edges[i][2];
                out[from[i]].add(new int[] {to[i], i});
            }
            dist = new long[n];
            Arrays.fill(dist, INF);
            dist[source] = 0;
            PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
            pq.add(new long[] {0, source});
            relax(pq); // the full search runs once
        }

        /**
         * Runs the queue until no stored distance can improve.
         * Time: O(k log n) for the k edges scanned. Space: O(n) queue entries.
         * Invariant: a popped entry equal to dist[u] has final edges relaxed from it.
         */
        private void relax(PriorityQueue<long[]> pq) {
            // Each pop either is current and relaxes its edges or is stale and is skipped.
            while (!pq.isEmpty()) {
                long[] top = pq.poll();
                int u = (int) top[1];
                if (top[0] > dist[u]) continue; // stale entry of a node that improved again
                for (int[] e : out[u]) {
                    long cand = dist[u] + cost[e[1]];
                    // A shorter route replaces the stored distance and re-enters the queue.
                    if (cand < dist[e[0]]) { dist[e[0]] = cand; pq.add(new long[] {cand, e[0]}); }
                }
            }
        }

        /**
         * Lowers the cost of the existing edge (a, b); returns true when a distance changes.
         * Time: O(1) without change, O(m log n) worst case. Space: O(n).
         * Invariant: dist equals the shortest costs for the current edge costs.
         */
        boolean lower(int a, int b, long newCost) {
            int id = -1;
            // Find the edge by its endpoints in the list of a.
            for (int[] e : out[a]) if (e[0] == b) id = e[1];
            if (id < 0) throw new IllegalArgumentException("no such edge");
            // A cost that is not smaller changes nothing.
            if (newCost >= cost[id]) return false;
            cost[id] = newCost;
            // An unreachable tail or a tail that gives no better route leaves all distances alone.
            if (dist[a] >= INF || dist[a] + newCost >= dist[b]) return false;
            dist[b] = dist[a] + newCost;
            PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
            pq.add(new long[] {dist[b], b});
            relax(pq); // only nodes behind b can improve
            return true;
        }

        /** Returns the shortest cost from the source, or -1 when unreachable. */
        long cost(int target) {
            return dist[target] >= INF ? -1 : dist[target];
        }
    }

    /** Oracle: Bellman-Ford from the source on the current costs. */
    static long[] oracle(int n, int source, int[][] edges, long[] cur) {
        long inf = Long.MAX_VALUE / 4;
        long[] d = new long[n];
        Arrays.fill(d, inf);
        d[source] = 0;
        // n - 1 passes settle every shortest path with non-negative costs.
        for (int pass = 0; pass < n; pass++) {
            for (int i = 0; i < edges.length; i++) {
                if (d[edges[i][0]] < inf && d[edges[i][0]] + cur[i] < d[edges[i][1]]) d[edges[i][1]] = d[edges[i][0]] + cur[i];
            }
        }
        for (int i = 0; i < n; i++) if (d[i] >= inf) d[i] = -1;
        return d;
    }

    public static void main(String[] args) {
        // Example 1: a decrease that reroutes node 3, a no-gain decrease and a zero cost.
        SourceCosts s = new SourceCosts(4, 0, new int[][] {{0, 1, 6}, {1, 2, 5}, {2, 3, 2}, {0, 2, 20}});
        if (s.cost(3) != 13 || s.cost(2) != 11) throw new AssertionError("example 1 start");
        if (!s.lower(0, 2, 9) || s.cost(2) != 9 || s.cost(3) != 11) throw new AssertionError("example 1 step 1");
        if (s.lower(1, 2, 5)) throw new AssertionError("example 1 equal cost");
        if (s.lower(0, 2, 30)) throw new AssertionError("example 1 raise");
        if (!s.lower(0, 1, 1) || s.cost(2) != 6 || s.cost(3) != 8) throw new AssertionError("example 1 step 4");
        if (!s.lower(2, 3, 0) || s.cost(3) != 6) throw new AssertionError("example 1 zero");
        // Example 2: edges behind an unreachable node never change a distance.
        SourceCosts u = new SourceCosts(4, 0, new int[][] {{1, 2, 5}, {2, 3, 2}});
        if (u.cost(1) != -1 || u.lower(1, 2, 1) || u.cost(3) != -1 || u.cost(0) != 0) throw new AssertionError("example 2");
        // Random graphs without parallel edges against Bellman-Ford after every decrease.
        Random rnd = new Random(2642);
        for (int trial = 0; trial < 600; trial++) {
            int n = 2 + rnd.nextInt(7);
            List<int[]> list = new ArrayList<>();
            boolean[][] used = new boolean[n][n];
            for (int i = 0; i < n * 2; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b || used[a][b]) continue;
                used[a][b] = true;
                list.add(new int[] {a, b, rnd.nextInt(30)});
            }
            if (list.isEmpty()) continue;
            int[][] edges = list.toArray(new int[0][]);
            long[] cur = new long[edges.length];
            for (int i = 0; i < edges.length; i++) cur[i] = edges[i][2];
            int src = rnd.nextInt(n);
            SourceCosts t = new SourceCosts(n, src, edges);
            for (int step = 0; step < 15; step++) {
                int id = rnd.nextInt(edges.length);
                long nc = rnd.nextInt(30);
                long[] before = oracle(n, src, edges, cur);
                if (nc < cur[id]) cur[id] = nc;
                long[] after = oracle(n, src, edges, cur);
                boolean changed = !Arrays.equals(before, after);
                // The returned flag must equal whether any distance changed.
                if (t.lower(edges[id][0], edges[id][1], nc) != changed) throw new AssertionError("flag in trial " + trial);
                for (int v = 0; v < n; v++) if (t.cost(v) != after[v]) throw new AssertionError("distance in trial " + trial);
            }
        }
    }
}
```
