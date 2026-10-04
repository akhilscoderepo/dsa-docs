<!-- solutions-for: 08-graph-and-deque -->
### Graph And Deque

#### Solution: [Build] Zero-One Relaxation (Author exercise)
<!-- id: sd-zero-one-relaxation -->

**Approach.** Build adjacency lists, set the distance of vertex 0 to zero and put 0 in an `ArrayDeque`. Each pop reads the current distance of the vertex, and every outgoing edge that gives a strictly smaller number for its head updates the distance and puts the head at the front for a zero edge or at the back for a one edge. Entries that were overtaken are simply expanded again without effect. The oracle is a Bellman-Ford loop that sweeps the edge list until a whole sweep changes nothing, and a second oracle is Floyd-Warshall on the matrix of edge weights, so two unrelated methods vouch for 3000 random graphs that include zero cycles and self-loops. The run also asserts that no vertex is ever put in the deque more than twice, which is the reason the loop is linear. The Java claims of the applicability stage are asserted as well: `addFirst(null)` and `addLast(null)` throw `NullPointerException`, `push` places at the front and `offer` at the back, and the false friend (plain breadth-first search that fixes a vertex when first discovered) is shown to be wrong on a concrete graph.

**Complexity.** Linear in the graph, O(V + E) time and O(V + E) memory, because each vertex is inserted at most twice and each insertion expands its out-edges once.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ZeroOneRelaxation {
    static int maxInserts;

    static int[] solve(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        int[] dist = new int[n];
        int[] inserts = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        dq.addFirst(0);
        inserts[0] = 1;
        while (!dq.isEmpty()) {
            int u = dq.pollFirst();
            for (int[] e : adj.get(u)) {
                int cand = dist[u] + e[1];
                if (cand < dist[e[0]]) {
                    dist[e[0]] = cand;
                    inserts[e[0]]++;
                    if (e[1] == 0) dq.addFirst(e[0]); else dq.addLast(e[0]);
                }
            }
        }
        maxInserts = 0;
        for (int c : inserts) maxInserts = Math.max(maxInserts, c);
        for (int i = 0; i < n; i++) if (dist[i] == Integer.MAX_VALUE) dist[i] = -1;
        return dist;
    }

    static int[] bellman(int n, int[][] edges) {
        int inf = 1_000_000;
        int[] d = new int[n];
        Arrays.fill(d, inf);
        d[0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                if (d[e[0]] < inf && d[e[0]] + e[2] < d[e[1]]) { d[e[1]] = d[e[0]] + e[2]; changed = true; }
            }
        }
        for (int i = 0; i < n; i++) if (d[i] == inf) d[i] = -1;
        return d;
    }

    static int[] floyd(int n, int[][] edges) {
        int inf = 1_000_000;
        int[][] m = new int[n][n];
        for (int[] row : m) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) m[i][i] = 0;
        for (int[] e : edges) m[e[0]][e[1]] = Math.min(m[e[0]][e[1]], e[2]);
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (m[i][k] + m[k][j] < m[i][j]) m[i][j] = m[i][k] + m[k][j];
        int[] d = new int[n];
        for (int j = 0; j < n; j++) d[j] = m[0][j] >= inf ? -1 : m[0][j];
        return d;
    }

    // the false friend: breadth-first search that fixes a vertex the first time it is seen
    static int[] firstSeen(int n, int[][] edges) {
        int[] d = new int[n];
        Arrays.fill(d, -1);
        d[0] = 0;
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(0);
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int[] e : edges) {
                if (e[0] == u && d[e[1]] == -1) { d[e[1]] = d[u] + e[2]; q.add(e[1]); }
            }
        }
        return d;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{0, 1, 1}, {0, 2, 0}, {2, 1, 0}, {2, 3, 1}, {3, 2, 0}};
        if (!Arrays.equals(solve(5, ex1), new int[] {0, 0, 0, 1, -1})) throw new AssertionError("example 1");
        int[][] ex2 = {{0, 1, 0}, {1, 0, 0}};
        if (!Arrays.equals(solve(4, ex2), new int[] {0, 0, -1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(1, new int[0][]), new int[] {0})) throw new AssertionError("single vertex");

        int[][] trap = {{0, 1, 1}, {0, 2, 0}, {2, 3, 0}, {3, 1, 0}};
        if (solve(4, trap)[1] != 0) throw new AssertionError("true distance");
        if (firstSeen(4, trap)[1] != 1) throw new AssertionError("false friend should answer 1 here");

        boolean npe = false;
        ArrayDeque<Integer> probe = new ArrayDeque<>();
        try { probe.addFirst(null); } catch (NullPointerException ex) { npe = true; }
        if (!npe) throw new AssertionError("addFirst(null)");
        npe = false;
        try { probe.addLast(null); } catch (NullPointerException ex) { npe = true; }
        if (!npe) throw new AssertionError("addLast(null)");
        probe.offer(5);
        probe.push(7);
        probe.offer(9);
        if (probe.peekFirst() != 7 || probe.peekLast() != 9) throw new AssertionError("push is front, offer is back");
        if (probe.pop() != 7 || probe.poll() != 5) throw new AssertionError("pop and poll take from the front");

        Random rnd = new Random(24081);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int[] got = solve(n, edges);
            if (!Arrays.equals(got, bellman(n, edges))) throw new AssertionError("bellman differs " + Arrays.deepToString(edges));
            if (!Arrays.equals(got, floyd(n, edges))) throw new AssertionError("floyd differs " + Arrays.deepToString(edges));
            if (maxInserts > 2) throw new AssertionError("a vertex was inserted three times");
        }
    }
}
```

#### Solution: [Vary] Minimum Cost to Make at Least One Valid Path in a Grid (LeetCode 1368)
<!-- id: sd-valid-path-zero-cells -->

**Approach.** A cell of the grid is a vertex, and the move to each of the four neighbours costs 0 when the arrow in the current cell points that way and 1 otherwise. The deque holds `long` entries with the cost in the high half and the cell number in the low half, built with `(long) cost << 32 | cell`. A popped entry whose cost is larger than the stored cost of its cell is stale and skipped, which makes the final distance array exact. After the search, the first answer is the distance of the last cell and the second is the number of cells whose stored distance is 0. The oracle sweeps all cell-to-neighbour moves, Bellman-Ford style, until nothing improves, and a second oracle runs Dijkstra with a `PriorityQueue` of `long` keys. The run asserts both examples and 3000 random grids up to 4 by 4, and it asserts the shift claim of the code stage: `1 << 32` on an `int` equals 1, while `1L << 32` is 4294967296.

**Complexity.** Each cell is inserted at most twice, so the search takes O(R * C) time and memory for R rows and C columns.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class ValidPathZeroCells {
    static final int[] DR = {0, 0, 1, -1};
    static final int[] DC = {1, -1, 0, 0};

    static int[] solve(int[][] g) {
        int rows = g.length, cols = g[0].length;
        int[] dist = new int[rows * cols];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<Long> dq = new ArrayDeque<>();
        dq.addFirst(0L);
        while (!dq.isEmpty()) {
            long entry = dq.pollFirst();
            int cost = (int) (entry >>> 32), cell = (int) entry;
            if (cost > dist[cell]) continue;
            int r = cell / cols, c = cell % cols;
            for (int k = 0; k < 4; k++) {
                int nr = r + DR[k], nc = c + DC[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int w = g[r][c] == k + 1 ? 0 : 1;
                int to = nr * cols + nc;
                if (cost + w < dist[to]) {
                    dist[to] = cost + w;
                    long packed = ((long) dist[to] << 32) | to;
                    if (w == 0) dq.addFirst(packed); else dq.addLast(packed);
                }
            }
        }
        int zeros = 0;
        for (int d : dist) if (d == 0) zeros++;
        return new int[] {dist[rows * cols - 1], zeros};
    }

    static int[] sweep(int[][] g) {
        int rows = g.length, cols = g[0].length, inf = 1_000_000;
        int[] d = new int[rows * cols];
        Arrays.fill(d, inf);
        d[0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++)
                    for (int k = 0; k < 4; k++) {
                        int nr = r + DR[k], nc = c + DC[k];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                        int w = g[r][c] == k + 1 ? 0 : 1;
                        if (d[r * cols + c] + w < d[nr * cols + nc]) { d[nr * cols + nc] = d[r * cols + c] + w; changed = true; }
                    }
        }
        int zeros = 0;
        for (int x : d) if (x == 0) zeros++;
        return new int[] {d[rows * cols - 1], zeros};
    }

    static int[] heap(int[][] g) {
        int rows = g.length, cols = g[0].length;
        int[] d = new int[rows * cols];
        Arrays.fill(d, Integer.MAX_VALUE);
        d[0] = 0;
        PriorityQueue<Long> pq = new PriorityQueue<>();
        pq.add(0L);
        while (!pq.isEmpty()) {
            long e = pq.poll();
            int cost = (int) (e >>> 32), cell = (int) e;
            if (cost > d[cell]) continue;
            int r = cell / cols, c = cell % cols;
            for (int k = 0; k < 4; k++) {
                int nr = r + DR[k], nc = c + DC[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int w = g[r][c] == k + 1 ? 0 : 1;
                if (cost + w < d[nr * cols + nc]) { d[nr * cols + nc] = cost + w; pq.add(((long) d[nr * cols + nc] << 32) | (nr * cols + nc)); }
            }
        }
        int zeros = 0;
        for (int x : d) if (x == 0) zeros++;
        return new int[] {d[rows * cols - 1], zeros};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[][] {{1, 1, 3}, {4, 2, 2}, {3, 3, 1}}), new int[] {1, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[][] {{2, 2, 2}, {2, 2, 2}}), new int[] {3, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][] {{4}}), new int[] {0, 1})) throw new AssertionError("single cell");
        if ((1 << 32) != 1 || (1L << 32) != 4294967296L) throw new AssertionError("shift claim");
        Random rnd = new Random(24082);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(4), cols = 1 + rnd.nextInt(4);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = 1 + rnd.nextInt(4);
            int[] got = solve(g);
            if (!Arrays.equals(got, sweep(g))) throw new AssertionError("sweep differs " + Arrays.deepToString(g));
            if (!Arrays.equals(got, heap(g))) throw new AssertionError("heap differs " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Boundary] Minimum Obstacle Removal to Reach Corner (LeetCode 2290)
<!-- id: sd-obstacle-removal -->

**Approach.** The cost of a move is the value of the cell being entered, so an empty cell costs 0 and an obstacle costs 1, and the start cell is never charged because the search begins with distance 0 on it. Moves into empty cells go to the front of the deque and moves into obstacles to the back. Because the start is given as empty, a one-cell grid answers 0 at once, and a corridor of empty cells answers 0 without ever using the back of the deque. The oracle is Floyd-Warshall on the matrix of cells, where the edge from a cell to a neighbour has the weight of the neighbour, and a second oracle is a `PriorityQueue` Dijkstra. The run asserts the examples, the one-cell grid and 3000 random grids up to 5 by 4 with both corners forced empty.

**Complexity.** Linear in the grid, O(R * C) time and memory, since a cell is queued at most twice.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class ObstacleRemoval {
    static final int[] DR = {1, -1, 0, 0};
    static final int[] DC = {0, 0, 1, -1};

    static int solve(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] dist = new int[rows * cols];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        dq.addFirst(0);
        while (!dq.isEmpty()) {
            int cell = dq.pollFirst();
            int r = cell / cols, c = cell % cols;
            for (int k = 0; k < 4; k++) {
                int nr = r + DR[k], nc = c + DC[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int w = grid[nr][nc];
                int to = nr * cols + nc;
                if (dist[cell] + w < dist[to]) {
                    dist[to] = dist[cell] + w;
                    if (w == 0) dq.addFirst(to); else dq.addLast(to);
                }
            }
        }
        return dist[rows * cols - 1];
    }

    static int floyd(int[][] grid) {
        int rows = grid.length, cols = grid[0].length, n = rows * cols, inf = 1_000_000;
        int[][] m = new int[n][n];
        for (int[] row : m) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) m[i][i] = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                for (int k = 0; k < 4; k++) {
                    int nr = r + DR[k], nc = c + DC[k];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    m[r * cols + c][nr * cols + nc] = grid[nr][nc];
                }
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (m[i][k] + m[k][j] < m[i][j]) m[i][j] = m[i][k] + m[k][j];
        return m[0][n - 1];
    }

    static int heap(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] d = new int[rows * cols];
        Arrays.fill(d, Integer.MAX_VALUE);
        d[0] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        pq.add(new int[] {0, 0});
        while (!pq.isEmpty()) {
            int[] e = pq.poll();
            if (e[0] > d[e[1]]) continue;
            int r = e[1] / cols, c = e[1] % cols;
            for (int k = 0; k < 4; k++) {
                int nr = r + DR[k], nc = c + DC[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int to = nr * cols + nc;
                if (e[0] + grid[nr][nc] < d[to]) { d[to] = e[0] + grid[nr][nc]; pq.add(new int[] {d[to], to}); }
            }
        }
        return d[rows * cols - 1];
    }

    public static void main(String[] args) {
        if (solve(new int[][] {{0, 1, 1}, {1, 1, 0}, {1, 1, 0}}) != 2) throw new AssertionError("example 1");
        if (solve(new int[][] {{0, 1, 0, 0, 0}, {0, 1, 0, 1, 0}, {0, 0, 0, 1, 0}}) != 0) throw new AssertionError("example 2");
        if (solve(new int[][] {{0}}) != 0) throw new AssertionError("one cell");
        if (solve(new int[][] {{0, 0, 0}}) != 0) throw new AssertionError("corridor");
        if (solve(new int[][] {{0, 1}, {1, 0}}) != 1) throw new AssertionError("two blocked ways");
        Random rnd = new Random(24083);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(4);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(10) < 4 ? 1 : 0;
            g[0][0] = 0;
            g[rows - 1][cols - 1] = 0;
            int got = solve(g);
            if (got != floyd(g)) throw new AssertionError("floyd differs " + Arrays.deepToString(g));
            if (got != heap(g)) throw new AssertionError("heap differs " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Recognize] Minimum Zero-One Toll (Author exercise)
<!-- id: sd-minimum-toll -->

**Approach.** Every lane is stored in both directions, including parallel lanes and self-loops, which do no harm because a self-loop can never lower a distance. The search starts at `start` with distance 0 and uses the front-or-back rule by weight, so the first time the deque yields `goal` its distance is already final, though the loop here runs to the end for simplicity and reads `dist[goal]`. A goal that was never reached gives -1. The oracle is Floyd-Warshall on the symmetric matrix and a second oracle is a `PriorityQueue` Dijkstra. The run asserts the examples, the case `start == goal`, and the false friend: counting lanes with ordinary breadth-first search gives the fewest lanes, which is 1 on a graph where the cheapest route has three free lanes and the direct lane costs a toll, and the true answer is 0.

**Complexity.** The run takes time proportional to the number of vertices plus lanes, O(V + E), with the adjacency lists as the only large memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class MinimumToll {
    static int solve(int n, int[][] lanes, int start, int goal) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : lanes) {
            adj.get(e[0]).add(new int[] {e[1], e[2]});
            adj.get(e[1]).add(new int[] {e[0], e[2]});
        }
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;
        ArrayDeque<Integer> dq = new ArrayDeque<>();
        dq.addFirst(start);
        while (!dq.isEmpty()) {
            int u = dq.pollFirst();
            for (int[] e : adj.get(u)) {
                if (dist[u] + e[1] < dist[e[0]]) {
                    dist[e[0]] = dist[u] + e[1];
                    if (e[1] == 0) dq.addFirst(e[0]); else dq.addLast(e[0]);
                }
            }
        }
        return dist[goal] == Integer.MAX_VALUE ? -1 : dist[goal];
    }

    static int floyd(int n, int[][] lanes, int start, int goal) {
        int inf = 1_000_000;
        int[][] m = new int[n][n];
        for (int[] row : m) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) m[i][i] = 0;
        for (int[] e : lanes) {
            m[e[0]][e[1]] = Math.min(m[e[0]][e[1]], e[2]);
            m[e[1]][e[0]] = Math.min(m[e[1]][e[0]], e[2]);
        }
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (m[i][k] + m[k][j] < m[i][j]) m[i][j] = m[i][k] + m[k][j];
        return m[start][goal] >= inf ? -1 : m[start][goal];
    }

    static int heap(int n, int[][] lanes, int start, int goal) {
        int[] d = new int[n];
        Arrays.fill(d, Integer.MAX_VALUE);
        d[start] = 0;
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        pq.add(new int[] {0, start});
        while (!pq.isEmpty()) {
            int[] top = pq.poll();
            if (top[0] > d[top[1]]) continue;
            for (int[] e : lanes) {
                for (int side = 0; side < 2; side++) {
                    int a = side == 0 ? e[0] : e[1], b = side == 0 ? e[1] : e[0];
                    if (a == top[1] && top[0] + e[2] < d[b]) { d[b] = top[0] + e[2]; pq.add(new int[] {d[b], b}); }
                }
            }
        }
        return d[goal] == Integer.MAX_VALUE ? -1 : d[goal];
    }

    // the false friend: the fewest lanes, ignoring the tolls
    static int fewestLanes(int n, int[][] lanes, int start, int goal) {
        int[] d = new int[n];
        Arrays.fill(d, -1);
        d[start] = 0;
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(start);
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int[] e : lanes) {
                int v = e[0] == u ? e[1] : e[1] == u ? e[0] : -1;
                if (v >= 0 && d[v] == -1) { d[v] = d[u] + 1; q.add(v); }
            }
        }
        return d[goal];
    }

    public static void main(String[] args) {
        int[][] ex1 = {{0, 1, 1}, {1, 2, 1}, {0, 3, 0}, {3, 4, 0}, {4, 2, 0}, {2, 5, 1}, {5, 5, 0}, {0, 0, 1}};
        if (solve(6, ex1, 0, 5) != 1) throw new AssertionError("example 1");
        int[][] ex2 = {{0, 1, 1}, {1, 1, 0}, {2, 3, 0}};
        if (solve(4, ex2, 0, 3) != -1) throw new AssertionError("example 2");
        if (solve(3, new int[][] {{0, 1, 1}}, 2, 2) != 0) throw new AssertionError("start is goal");

        int[][] trap = {{0, 3, 1}, {0, 1, 0}, {1, 2, 0}, {2, 3, 0}};
        if (solve(4, trap, 0, 3) != 0) throw new AssertionError("free detour");
        if (fewestLanes(4, trap, 0, 3) != 1) throw new AssertionError("lane count says one lane");

        Random rnd = new Random(24084);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(14);
            int[][] lanes = new int[m][];
            for (int i = 0; i < m; i++) lanes[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            int got = solve(n, lanes, s, g);
            if (got != floyd(n, lanes, s, g)) throw new AssertionError("floyd differs " + Arrays.deepToString(lanes));
            if (got != heap(n, lanes, s, g)) throw new AssertionError("heap differs " + Arrays.deepToString(lanes));
        }
    }
}
```
