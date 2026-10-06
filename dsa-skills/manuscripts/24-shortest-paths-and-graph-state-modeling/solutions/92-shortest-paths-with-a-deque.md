<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Shortest Paths With A Deque

#### Solution: [Build] Zero-One Relaxation (Author exercise)
<!-- id: sp-zero-one-relaxation -->

**Approach.**
The method groups the edges by source vertex in an adjacency list, then keeps a distance array filled with a large sentinel. It removes entries from the front of a deque and skips an entry whose stored cost is larger than the current distance. For each outgoing edge it computes the candidate cost and acts only when the candidate is strictly smaller than the stored distance. A weight-0 edge puts the new entry at the front, and a weight-1 edge puts it at the back.

The invariant is that the deque is sorted by cost and holds at most two distinct costs, `d` and `d + 1`. A front insertion of cost `d` and a back insertion of cost `d + 1` both preserve it. Strict improvement gives each vertex at most two entries, which bounds the work, and it ends zero-weight cycles after one lap. Vertices that keep the sentinel become -1.

**Complexity.**
- **Time** is O(V + E), because each vertex owns at most two entries and each entry scans its adjacency list once.
- **Space** is O(V + E) for the adjacency list, the distance array and at most 2V deque entries.

```java run
import java.util.*;

public final class ZeroOneRelaxation {
    static int pushes;

    /**
     * Returns the minimum weight from src to every vertex, or -1 when unreachable.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: the deque is sorted by cost and holds at most two distinct costs.
     */
    static int[] distances(int n, int[][] edges, int src) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each edge is stored once, so building costs O(E).
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;
        ArrayDeque<int[]> deque = new ArrayDeque<>();
        deque.addFirst(new int[] {src, 0});
        pushes = 1;
        // Each pass removes one entry, and at most 2V entries ever exist.
        while (!deque.isEmpty()) {
            int[] head = deque.pollFirst();
            // A cost above the stored distance marks an entry made stale by a later improvement.
            if (head[1] > dist[head[0]]) continue;
            // Every edge of a live entry is read once.
            for (int[] edge : adj.get(head[0])) {
                int cost = head[1] + edge[1];
                // Only a strict improvement changes state, so zero-weight cycles end.
                if (cost >= dist[edge[0]]) continue;
                dist[edge[0]] = cost;
                pushes++;
                // The weight picks the end, which keeps costs in sorted order.
                if (edge[1] == 0) deque.addFirst(new int[] {edge[0], cost});
                else deque.addLast(new int[] {edge[0], cost});
            }
        }
        // The sentinel marks a vertex that no path reaches.
        for (int v = 0; v < n; v++) if (dist[v] == Integer.MAX_VALUE) dist[v] = -1;
        return dist;
    }

    /** Oracle: Bellman-Ford style passes over all edges until nothing improves. */
    static int[] oracle(int n, int[][] edges, int src) {
        int inf = 1_000_000;
        int[] d = new int[n];
        Arrays.fill(d, inf);
        d[src] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                if (d[e[0]] + e[2] < d[e[1]]) { d[e[1]] = d[e[0]] + e[2]; changed = true; }
            }
        }
        for (int v = 0; v < n; v++) if (d[v] == inf) d[v] = -1;
        return d;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(distances(4, new int[][] {{0, 1, 1}, {0, 2, 0}, {2, 1, 0}, {1, 3, 1}}, 0), new int[] {0, 0, 0, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(distances(5, new int[][] {{0, 1, 0}, {1, 2, 0}, {2, 1, 0}, {0, 3, 1}, {3, 2, 1}}, 0), new int[] {0, 0, 0, 1, -1})) throw new AssertionError("ex2");
        // Java fact: pollFirst returns null on an empty deque, and addFirst puts an element before older ones.
        ArrayDeque<Integer> probe = new ArrayDeque<>();
        if (probe.pollFirst() != null) throw new AssertionError("empty poll");
        probe.addLast(1);
        probe.addFirst(0);
        if (probe.pollFirst() != 0 || probe.pollFirst() != 1) throw new AssertionError("ends");
        // Random graphs with zero cycles, self loops and repeats against the oracle, plus the two-entry bound.
        Random rnd = new Random(2492);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(18);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int src = rnd.nextInt(n);
            if (!Arrays.equals(distances(n, edges, src), oracle(n, edges, src))) throw new AssertionError("random " + t);
            if (pushes > 2 * n) throw new AssertionError("push bound " + t);
        }
    }
}
```

#### Solution: [Vary] Minimum Cost To Make At Least One Valid Path In A Grid (LeetCode 1368)
<!-- id: sp-arrow-grid-ties -->

**Approach.**
The method treats each cell as a vertex numbered `row * n + col`, with no explicit edge list. For a cell it tries the four directions, and the weight of a move is 0 when the direction code equals the arrow of the cell and 1 otherwise. The search is the deque search of the previous exercise. The first entry of the result is the final distance of the last cell.

The new requirement is the count of cells that tie with the goal. Stopping when the goal is removed would leave other cells with distances that are not final yet, so the count would be wrong. The method therefore runs until the deque is empty. At that point every distance is final, and one pass over the table counts the cells equal to the goal cost.

**Complexity.**
- **Time** is O(mn), because each cell has at most two entries and each entry tries four moves, and the counting pass costs O(mn).
- **Space** is O(mn) for the distance table and the deque.

```java run
import java.util.*;

public final class ArrowGridTies {
    static final int[] DR = {0, 0, 0, 1, -1};
    static final int[] DC = {0, 1, -1, 0, 0};

    /**
     * Returns {cost of the bottom right cell, number of cells with that cost}.
     * Time: O(mn). Space: O(mn).
     * Invariant: the deque is sorted by cost and holds at most two distinct costs.
     */
    static int[] costAndTies(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[] dist = new int[m * n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<int[]> deque = new ArrayDeque<>();
        deque.add(new int[] {0, 0});
        // The loop runs until the deque is empty, so every distance becomes final.
        while (!deque.isEmpty()) {
            int[] head = deque.pollFirst();
            int cell = head[0];
            // Skip an entry that a cheaper entry for the same cell has replaced.
            if (head[1] > dist[cell]) continue;
            int r = cell / n, c = cell % n;
            // Four moves per live entry give the constant factor.
            for (int dir = 1; dir <= 4; dir++) {
                int nr = r + DR[dir], nc = c + DC[dir];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
                // A move along the arrow is free and any other direction costs one.
                int w = grid[r][c] == dir ? 0 : 1;
                int cost = head[1] + w;
                int next = nr * n + nc;
                if (cost >= dist[next]) continue;
                dist[next] = cost;
                if (w == 0) deque.addFirst(new int[] {next, cost});
                else deque.addLast(new int[] {next, cost});
            }
        }
        // One pass counts the cells that tie with the goal.
        int goal = dist[m * n - 1], ties = 0;
        for (int d : dist) if (d == goal) ties++;
        return new int[] {goal, ties};
    }

    /** Oracle: repeated passes over every cell and direction until no distance changes. */
    static int[] oracle(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] d = new int[m][n];
        for (int[] row : d) Arrays.fill(row, 1_000_000);
        d[0][0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < m; r++) for (int c = 0; c < n; c++) for (int dir = 1; dir <= 4; dir++) {
                int nr = r + DR[dir], nc = c + DC[dir];
                if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
                int w = grid[r][c] == dir ? 0 : 1;
                if (d[r][c] + w < d[nr][nc]) { d[nr][nc] = d[r][c] + w; changed = true; }
            }
        }
        int ties = 0;
        for (int[] row : d) for (int v : row) if (v == d[m - 1][n - 1]) ties++;
        return new int[] {d[m - 1][n - 1], ties};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(costAndTies(new int[][] {{1, 2}, {4, 3}}), new int[] {1, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(costAndTies(new int[][] {{1, 1, 1, 1}, {2, 2, 2, 2}, {1, 1, 1, 1}, {2, 2, 2, 2}}), new int[] {3, 4})) throw new AssertionError("ex2");
        // Single cell grids have cost 0 and one tying cell, the cell itself.
        if (!Arrays.equals(costAndTies(new int[][] {{4}}), new int[] {0, 1})) throw new AssertionError("single");
        // Java fact: integer division and remainder split a flat index into row and column.
        if (7 / 3 != 2 || 7 % 3 != 1) throw new AssertionError("index split");
        // Random grids against the repeated-pass oracle.
        Random rnd = new Random(1368);
        for (int t = 0; t < 1500; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] g = new int[m][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = 1 + rnd.nextInt(4);
            if (!Arrays.equals(costAndTies(g), oracle(g))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Minimum Obstacle Removal To Reach Corner (LeetCode 2290)
<!-- id: sp-obstacle-corner -->

**Approach.**
Each move has the weight of the cell that it enters, so the weight belongs to the destination and not to the source. The start cell is the origin of the path, and no move enters it, so its cost is never charged. The distance of the start is therefore 0 even when the start holds a 1. The goal cell is entered by a move, so its value is charged when it holds a 1.

The search is the deque search on a flat array. A move into an empty cell has weight 0 and goes to the front. A move into an obstacle has weight 1 and goes to the back. A single cell grid has no move, and the answer is the start distance 0. The strict-improvement test also stops the search from looping through empty cells.

**Complexity.**
- **Time** is O(mn), because each cell owns at most two entries and each entry tries four neighbors.
- **Space** is O(mn) for the distance array and the deque.

```java run
import java.util.*;

public final class ObstacleCorner {
    /**
     * Returns the fewest obstacle cells entered on a path from the top left to the bottom right.
     * Time: O(mn). Space: O(mn).
     * Invariant: the deque is sorted by cost and holds at most two distinct costs.
     */
    static int fewestObstacles(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[] best = new int[m * n];
        Arrays.fill(best, Integer.MAX_VALUE);
        // The start is not entered by any move, so it keeps cost 0 even when it holds a 1.
        best[0] = 0;
        ArrayDeque<int[]> deque = new ArrayDeque<>();
        deque.addFirst(new int[] {0, 0});
        int[][] steps = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        // The search ends when no entry remains, and each cell owns at most two entries.
        while (!deque.isEmpty()) {
            int[] head = deque.pollFirst();
            // A larger stored cost means a cheaper entry for this cell exists.
            if (head[1] > best[head[0]]) continue;
            for (int[] s : steps) {
                int r = head[0] / n + s[0], c = head[0] % n + s[1];
                if (r < 0 || r >= m || c < 0 || c >= n) continue;
                // The move is charged the value of the cell that it enters.
                int w = grid[r][c];
                int cost = head[1] + w;
                if (cost >= best[r * n + c]) continue;
                best[r * n + c] = cost;
                if (w == 0) deque.addFirst(new int[] {r * n + c, cost});
                else deque.addLast(new int[] {r * n + c, cost});
            }
        }
        // The goal distance includes the goal cell's own value, since a move enters it.
        return best[m * n - 1];
    }

    /** Oracle: exhaustive passes until stable, with the same entering-cell charge. */
    static int oracle(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] d = new int[m][n];
        for (int[] row : d) Arrays.fill(row, 1_000_000);
        d[0][0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < m; r++) for (int c = 0; c < n; c++) {
                if (r + 1 < m && d[r][c] + grid[r + 1][c] < d[r + 1][c]) { d[r + 1][c] = d[r][c] + grid[r + 1][c]; changed = true; }
                if (r > 0 && d[r][c] + grid[r - 1][c] < d[r - 1][c]) { d[r - 1][c] = d[r][c] + grid[r - 1][c]; changed = true; }
                if (c + 1 < n && d[r][c] + grid[r][c + 1] < d[r][c + 1]) { d[r][c + 1] = d[r][c] + grid[r][c + 1]; changed = true; }
                if (c > 0 && d[r][c] + grid[r][c - 1] < d[r][c - 1]) { d[r][c - 1] = d[r][c] + grid[r][c - 1]; changed = true; }
            }
        }
        return d[m - 1][n - 1];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (fewestObstacles(new int[][] {{0, 1, 1}, {1, 1, 0}, {1, 1, 0}}) != 2) throw new AssertionError("ex1");
        if (fewestObstacles(new int[][] {{1, 1}, {1, 1}}) != 2) throw new AssertionError("ex2");
        // Single cell grids need no move, so even an obstacle start and goal cost 0.
        if (fewestObstacles(new int[][] {{1}}) != 0 || fewestObstacles(new int[][] {{0}}) != 0) throw new AssertionError("single");
        // Java fact: Integer.MAX_VALUE plus one overflows to a negative value, so the sentinel never enters a sum.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("overflow");
        // Random grids, including obstacle starts and goals, against the oracle.
        Random rnd = new Random(2290);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(6), n = 1 + rnd.nextInt(6);
            int[][] g = new int[m][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(3) == 0 ? 0 : rnd.nextInt(2);
            if (fewestObstacles(g) != oracle(g)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Zero-One Toll (Author exercise)
<!-- id: sp-zero-one-toll -->

**Approach.**
Every toll is 0 or 1, so the problem asks for a shortest path with those weights, and the deque search fits. The method stores each road twice, once for each direction, in arrays `head`, `to`, `toll` and `nxt` that chain the roads of each junction. It starts at junction 0 and returns the final distance of junction `n - 1`, or -1 if that distance keeps the sentinel.

The invariant is that the deque is sorted by cost with at most two distinct costs. Parallel roads and self loops need no special case, because the strict improvement test ignores a road that does not lower a distance. A network with one junction returns 0 at once, since junction 0 is also the target.

**Complexity.**
- **Time** is O(V + E), because there are at most two entries per junction and each road is scanned in both directions.
- **Space** is O(V + E) for the road arrays, the distances and the deque.

```java run
import java.util.*;

public final class ZeroOneToll {
    /**
     * Returns the minimum toll from junction 0 to junction n - 1, or -1 when none exists.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: the deque is sorted by cost and holds at most two distinct costs.
     */
    static int minToll(int n, int[][] roads) {
        int[] head = new int[n];
        Arrays.fill(head, -1);
        int[] to = new int[2 * roads.length], toll = new int[2 * roads.length], nxt = new int[2 * roads.length];
        int used = 0;
        // Each road is added in both directions, which gives 2E list cells.
        for (int[] r : roads) {
            to[used] = r[1]; toll[used] = r[2]; nxt[used] = head[r[0]]; head[r[0]] = used++;
            to[used] = r[0]; toll[used] = r[2]; nxt[used] = head[r[1]]; head[r[1]] = used++;
        }
        int[] cost = new int[n];
        Arrays.fill(cost, Integer.MAX_VALUE);
        cost[0] = 0;
        ArrayDeque<int[]> line = new ArrayDeque<>();
        line.addFirst(new int[] {0, 0});
        // Entries leave from the front, so costs are removed in nondecreasing order.
        while (!line.isEmpty()) {
            int[] top = line.pollFirst();
            // A removed cost above the stored one is a stale duplicate.
            if (top[1] > cost[top[0]]) continue;
            // The chain of a junction is walked once per live entry.
            for (int k = head[top[0]]; k != -1; k = nxt[k]) {
                int c = top[1] + toll[k];
                if (c >= cost[to[k]]) continue;
                cost[to[k]] = c;
                if (toll[k] == 0) line.addFirst(new int[] {to[k], c});
                else line.addLast(new int[] {to[k], c});
            }
        }
        // The sentinel at the target means that no trip exists.
        return cost[n - 1] == Integer.MAX_VALUE ? -1 : cost[n - 1];
    }

    /** Oracle: Floyd-Warshall over all junction pairs on a small network. */
    static int oracle(int n, int[][] roads) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] r : roads) { d[r[0]][r[1]] = Math.min(d[r[0]][r[1]], r[2]); d[r[1]][r[0]] = Math.min(d[r[1]][r[0]], r[2]); }
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        return d[0][n - 1] >= inf ? -1 : d[0][n - 1];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minToll(5, new int[][] {{0, 1, 1}, {1, 4, 0}, {0, 2, 0}, {2, 3, 1}, {3, 4, 0}, {2, 2, 1}}) != 1) throw new AssertionError("ex1");
        if (minToll(4, new int[][] {{0, 1, 1}, {2, 3, 0}}) != -1) throw new AssertionError("ex2");
        // A single junction needs no trip.
        if (minToll(1, new int[0][]) != 0) throw new AssertionError("single");
        // Java fact: a ternary expression with an int sentinel returns -1 without unboxing issues.
        int sentinel = Integer.MAX_VALUE;
        if ((sentinel == Integer.MAX_VALUE ? -1 : sentinel) != -1) throw new AssertionError("ternary");
        // Random networks with parallel roads and self loops against Floyd-Warshall.
        Random rnd = new Random(9202);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(16);
            int[][] roads = new int[m][];
            for (int i = 0; i < m; i++) roads[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            if (minToll(n, roads) != oracle(n, roads)) throw new AssertionError("random " + t);
        }
    }
}
```
