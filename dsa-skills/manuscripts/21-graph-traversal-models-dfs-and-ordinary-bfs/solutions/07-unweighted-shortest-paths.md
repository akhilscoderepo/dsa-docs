<!-- solutions-for: 07-unweighted-shortest-paths -->
### Unweighted Shortest Paths

#### Solution: [Build] Distance From One Source (Author exercise)
<!-- id: gt-distance-from-source -->

**Approach.** Fill a distance table with -1, set the source to 0, and drain a queue. A neighbour that still holds -1 gets `dist[cur] + 1` at that moment and joins the queue, so the table is also the visited check. The oracle is a Bellman-Ford style relaxation with no queue at all: start with the source at 0 and everything else at infinity, then sweep the edge list in both directions over and over until a whole sweep lowers nothing. The checks compare the two on random graphs, confirm that the order in which a recording version dequeues vertices never decreases in distance, show on the lesson's map that the first path a depth-first search finds has four edges where the shortest has two, and confirm that a fresh `int[]` holds zeros, so a table not filled with -1 would take the source for unreached.

**Complexity.** The traversal costs O(V + E) time, since each vertex is queued once and each edge is read from both ends. The table and queue take O(V) memory beyond the adjacency lists.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DistanceSolution {
    static List<List<Integer>> build(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        for (List<Integer> a : adj) java.util.Collections.sort(a);
        return adj;
    }

    static int[] solve(int n, int[][] edges, int source) {
        List<List<Integer>> adj = build(n, edges);
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        dist[source] = 0;
        line.add(source);
        while (!line.isEmpty()) {
            int cur = line.poll();
            for (int next : adj.get(cur)) {
                if (dist[next] != -1) continue;
                dist[next] = dist[cur] + 1;
                line.add(next);
            }
        }
        return dist;
    }

    static int[] oracle(int n, int[][] edges, int source) {
        int inf = Integer.MAX_VALUE / 2;
        int[] d = new int[n];
        Arrays.fill(d, inf);
        d[source] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int[] e : edges) {
                if (d[e[0]] + 1 < d[e[1]]) { d[e[1]] = d[e[0]] + 1; moved = true; }
                if (d[e[1]] + 1 < d[e[0]]) { d[e[0]] = d[e[1]] + 1; moved = true; }
            }
        }
        for (int i = 0; i < n; i++) if (d[i] == inf) d[i] = -1;
        return d;
    }

    static List<Integer> dequeueOrder(int n, int[][] edges, int source, int[] dist) {
        List<List<Integer>> adj = build(n, edges);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        List<Integer> order = new ArrayList<>();
        seen[source] = true;
        line.add(source);
        while (!line.isEmpty()) {
            int cur = line.poll();
            order.add(cur);
            for (int next : adj.get(cur)) {
                if (seen[next]) continue;
                seen[next] = true;
                line.add(next);
            }
        }
        return order;
    }

    static int dfsFirstLength(List<List<Integer>> adj, int at, int goal, boolean[] onRoute) {
        if (at == goal) return 0;
        onRoute[at] = true;
        for (int next : adj.get(at)) {
            if (onRoute[next]) continue;
            int rest = dfsFirstLength(adj, next, goal, onRoute);
            if (rest >= 0) return rest + 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[][] kestrel = {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {0, 5}, {5, 4}, {5, 6}};
        if (!Arrays.equals(solve(7, kestrel, 0), new int[] {0, 1, 2, 3, 2, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(4, new int[][] {{0, 1}, {2, 3}}, 2), new int[] {-1, -1, 0, 1})) throw new AssertionError("example 2");
        int dfs = dfsFirstLength(build(7, kestrel), 0, 4, new boolean[7]);
        int best = solve(7, kestrel, 0)[4];
        if (dfs != 4 || best != 2 || dfs <= best) throw new AssertionError("depth-first first path should be longer: " + dfs + " vs " + best);
        int[] fresh = new int[3];
        if (fresh[0] != 0 || fresh[2] != 0) throw new AssertionError("fresh int array should hold zeros");
        Random rnd = new Random(21701);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9), m = n < 2 ? 0 : rnd.nextInt(2 * n + 1);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n - 1);
                if (v >= u) v++;
                edges[i] = new int[] {u, v};
            }
            int src = rnd.nextInt(n);
            int[] got = solve(n, edges, src), want = oracle(n, edges, src);
            if (!Arrays.equals(got, want)) throw new AssertionError("random " + t);
            List<Integer> order = dequeueOrder(n, edges, src, got);
            for (int i = 0; i + 1 < order.size(); i++)
                if (got[order.get(i)] > got[order.get(i + 1)]) throw new AssertionError("order not non-decreasing " + t);
            for (int v = 0; v < n; v++) if ((got[v] >= 0) != order.contains(v)) throw new AssertionError("reach " + t);
        }
    }
}
```

#### Solution: [Vary] Restore One Shortest Path (Author exercise)
<!-- id: gt-restore-shortest-path -->

**Approach.** Run the same search with sorted adjacency lists and write `parent[next] = cur` at the single moment a vertex is first discovered. For a reached target, walk from the target through the parents to the source, adding each vertex at the front of the list, which yields the path in forward order. An unreached target returns an empty array. The oracle does not use parents. It computes all-pairs distances with Floyd-Warshall on unit weights and then checks that the returned path starts at the source, ends at the target, uses only real edges, and has exactly the Floyd-Warshall distance in edges, or is empty exactly when the distance is infinite. The two examples pin down the tie rule, and an extra assertion checks that the parent of every vertex lies exactly one distance step nearer the source.

**Complexity.** Search and rebuilding together take O(V + E) time. Parents, distances and the queue use O(V) space, and the returned path adds at most V entries.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class RestorePathSolution {
    static int[] solve(int n, int[][] edges, int source, int target) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        for (List<Integer> a : adj) Collections.sort(a);
        int[] parent = new int[n];
        boolean[] seen = new boolean[n];
        Arrays.fill(parent, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        seen[source] = true;
        line.add(source);
        while (!line.isEmpty()) {
            int cur = line.poll();
            for (int next : adj.get(cur)) {
                if (seen[next]) continue;
                seen[next] = true;
                parent[next] = cur;
                line.add(next);
            }
        }
        if (!seen[target]) return new int[0];
        ArrayList<Integer> path = new ArrayList<>();
        for (int v = target; v != -1; v = parent[v]) path.add(v);
        Collections.reverse(path);
        int[] out = new int[path.size()];
        for (int i = 0; i < out.length; i++) out[i] = path.get(i);
        return out;
    }

    static int[][] floyd(int n, int[][] edges) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] e : edges) { d[e[0]][e[1]] = 1; d[e[1]][e[0]] = 1; }
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
        return d;
    }

    public static void main(String[] args) {
        int[][] kestrel = {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {0, 5}, {5, 4}, {5, 6}};
        if (!Arrays.equals(solve(7, kestrel, 0, 3), new int[] {0, 1, 2, 3})) throw new AssertionError("example 1");
        int[][] diamond = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}};
        if (!Arrays.equals(solve(5, diamond, 0, 4), new int[] {0, 1, 3, 4})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(7, kestrel, 0, 4), new int[] {0, 5, 4})) throw new AssertionError("branch beats main line");
        Random rnd = new Random(21702);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9), m = n < 2 ? 0 : rnd.nextInt(2 * n + 1);
            int[][] edges = new int[m][];
            boolean[][] has = new boolean[n][n];
            for (int i = 0; i < m; i++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n - 1);
                if (v >= u) v++;
                edges[i] = new int[] {u, v};
                has[u][v] = true;
                has[v][u] = true;
            }
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            int[] path = solve(n, edges, s, g);
            int[][] d = floyd(n, edges);
            if (d[s][g] >= 1_000_000) {
                if (path.length != 0) throw new AssertionError("should be empty " + t);
                continue;
            }
            if (path.length != d[s][g] + 1) throw new AssertionError("length " + t);
            if (path[0] != s || path[path.length - 1] != g) throw new AssertionError("ends " + t);
            for (int i = 0; i + 1 < path.length; i++)
                if (!has[path[i]][path[i + 1]]) throw new AssertionError("not an edge " + t);
            for (int i = 0; i < path.length; i++)
                if (d[s][path[i]] != i) throw new AssertionError("each vertex one step nearer " + t);
            if (!Arrays.equals(path, solve(n, edges, s, g))) throw new AssertionError("must be deterministic " + t);
        }
    }
}
```

#### Solution: [Boundary] Source Equals Target And Unreachable Target (Author exercise)
<!-- id: gt-source-target-edges -->

**Approach.** Return 0 before building anything when the two vertices coincide. Otherwise run the queue with a distance table filled with -1 and return the distance of the target at the moment it is discovered, which is final because of the ring-by-ring order. If the queue empties first, the target is in another component and the answer is -1. The oracle is Floyd-Warshall on unit weights, mapping infinity to -1, and the random cases deliberately include isolated vertices, repeated edges and equal endpoints, so that the zero case on an edgeless vertex and the -1 case are both exercised many times. Fixed asserts cover both examples and a one-vertex graph with no edges.

**Complexity.** The early stop does not change the worst case of O(V + E) time, and the memory is O(V) for the table and the queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class SourceTargetSolution {
    static int solve(int n, int[][] edges, int source, int target) {
        if (source == target) return 0;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        dist[source] = 0;
        line.add(source);
        while (!line.isEmpty()) {
            int cur = line.poll();
            for (int next : adj.get(cur)) {
                if (dist[next] != -1) continue;
                dist[next] = dist[cur] + 1;
                if (next == target) return dist[next];
                line.add(next);
            }
        }
        return -1;
    }

    static int oracle(int n, int[][] edges, int s, int g) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] e : edges) { d[e[0]][e[1]] = 1; d[e[1]][e[0]] = 1; }
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
        return d[s][g] >= inf ? -1 : d[s][g];
    }

    public static void main(String[] args) {
        int[][] kestrel = {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {0, 5}, {5, 4}, {5, 6}};
        if (solve(7, kestrel, 2, 2) != 0) throw new AssertionError("example 1");
        int[][] split = {{0, 1}, {1, 2}, {0, 3}, {3, 2}, {4, 5}};
        if (solve(6, split, 0, 4) != -1) throw new AssertionError("example 2");
        if (solve(1, new int[0][], 0, 0) != 0) throw new AssertionError("single vertex");
        if (solve(3, new int[][] {{0, 1}}, 2, 2) != 0) throw new AssertionError("edgeless vertex to itself");
        Random rnd = new Random(21703);
        int zeros = 0, fails = 0;
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(8), m = n < 2 ? 0 : rnd.nextInt(n + 1);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n - 1);
                if (v >= u) v++;
                edges[i] = new int[] {u, v};
            }
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            int got = solve(n, edges, s, g), want = oracle(n, edges, s, g);
            if (got != want) throw new AssertionError("random " + t);
            if (got == 0) zeros++;
            if (got == -1) fails++;
        }
        if (zeros == 0 || fails == 0) throw new AssertionError("both boundary cases must occur");
    }
}
```

#### Solution: [Recognize] Shortest Path In Binary Matrix (LeetCode 1091)
<!-- id: gt-binary-matrix-path -->

**Approach.** The cells are the vertices and the eight direction deltas generate the edges on demand. Return -1 at once if the start or end cell is blocked, then run the queue of cell codes with the start at distance 1, because the answer counts cells and not moves. The bounds, openness and seen gates come in that order, and a cell is marked when queued. The oracle relaxes distances directly: it keeps a table of infinity, sets the start to 1, and repeatedly scans every open cell, lowering it to one more than its best open neighbour, until a full scan changes nothing. The comparison runs on random grids of every size up to 7, and the fixed asserts include the examples, a blocked start, a blocked end and the one-cell grid.

**Complexity.** There are n squared cells and each tries eight neighbours, so the time is O(n^2) with a constant of eight. The distance table and queue take O(n^2) memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class BinaryMatrixSolution {
    static int solve(int[][] grid) {
        int n = grid.length;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        int[] dist = new int[n * n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        dist[0] = 1;
        line.add(0);
        while (!line.isEmpty()) {
            int code = line.poll();
            int r = code / n, c = code % n;
            if (r == n - 1 && c == n - 1) return dist[code];
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    if (dr == 0 && dc == 0) continue;
                    int nr = r + dr, nc = c + dc;
                    if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
                    if (grid[nr][nc] == 1) continue;
                    int next = nr * n + nc;
                    if (dist[next] != -1) continue;
                    dist[next] = dist[code] + 1;
                    line.add(next);
                }
            }
        }
        return -1;
    }

    static int oracle(int[][] grid) {
        int n = grid.length, inf = Integer.MAX_VALUE / 2;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        d[0][0] = 1;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = n - 1; r >= 0; r--) {
                for (int c = n - 1; c >= 0; c--) {
                    if (grid[r][c] == 1) continue;
                    for (int dr = -1; dr <= 1; dr++) {
                        for (int dc = -1; dc <= 1; dc++) {
                            int pr = r + dr, pc = c + dc;
                            if ((dr == 0 && dc == 0) || pr < 0 || pr >= n || pc < 0 || pc >= n) continue;
                            if (d[pr][pc] + 1 < d[r][c]) { d[r][c] = d[pr][pc] + 1; moved = true; }
                        }
                    }
                }
            }
        }
        return d[n - 1][n - 1] >= inf ? -1 : d[n - 1][n - 1];
    }

    public static void main(String[] args) {
        if (solve(new int[][] {{0, 0, 1}, {1, 0, 0}, {1, 1, 0}}) != 3) throw new AssertionError("example 1");
        if (solve(new int[][] {{0, 1, 0, 0}, {0, 1, 0, 1}, {0, 0, 1, 0}, {1, 0, 0, 0}}) != 5) throw new AssertionError("example 2");
        if (solve(new int[][] {{1, 0}, {0, 0}}) != -1) throw new AssertionError("blocked start");
        if (solve(new int[][] {{0, 0}, {0, 1}}) != -1) throw new AssertionError("blocked end");
        if (solve(new int[][] {{0}}) != 1) throw new AssertionError("one cell counts as one");
        if (solve(new int[][] {{1}}) != -1) throw new AssertionError("one blocked cell");
        if (solve(new int[][] {{0, 0}, {1, 0}}) != 2) throw new AssertionError("diagonal step");
        if (solve(new int[][] {{0, 1, 1}, {1, 1, 1}, {1, 1, 0}}) != -1) throw new AssertionError("walled in");
        Random rnd = new Random(21704);
        int found = 0, none = 0;
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] g = new int[n][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(10) < 3 ? 1 : 0;
            int got = solve(g), want = oracle(g);
            if (got != want) throw new AssertionError("random " + t);
            if (got > 0) found++; else none++;
        }
        if (found == 0 || none == 0) throw new AssertionError("both outcomes must occur");
    }
}
```
