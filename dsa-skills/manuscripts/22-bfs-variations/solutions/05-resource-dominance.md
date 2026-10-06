<!-- solutions-for: 22-bfs-variations -->
### Solutions For Keep The Best Resource Left

#### Solution: [Build] Position And Remaining Breaks (Author exercise)
<!-- id: bv5-position-remaining-breaks -->

**Approach.**
The queue entry is the triple `{node, remaining, dist}`. The method marks the pair of node and remaining budget as visited, because two entries with the same pair have the same future and the same cost to reach it. Each blocked edge subtracts its cost from `remaining`, and an edge is skipped when the result would be negative.

Entries leave the queue in nondecreasing `dist`, so the first dequeue of the target carries the minimum move count. The invariant is that each pair enters the queue at most once and with the smallest move count that reaches it. The first example of the exercise shows a visited array by node alone fails, since room 1 arrives with zero charges first. The harness asserts that case.

**Complexity.**
- **Time** is O((V + E) * k), because each of the V * (k + 1) pairs is dequeued once and scans its outgoing edges.
- **Space** is O(V * k) for the visited pairs and the queue, plus O(E) for the adjacency list.

```java run
import java.util.*;

public final class PositionRemainingBreaks {
    /**
     * Returns the fewest edges on a route from 0 to n-1 whose cost is at most k, or -1.
     * Time: O((V + E) * k). Space: O(V * k + E).
     * Invariant: each pair (node, remaining) is enqueued once, at its smallest move count.
     */
    static int fewestEdges(int n, int[][] edges, int k) {
        // Directed adjacency lists hold {next, cost} pairs.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        // One flag per pair of vertex and remaining budget; this is the n * (k + 1) state space.
        boolean[][] seen = new boolean[n][k + 1];
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        seen[0][k] = true;
        queue.add(new int[] {0, k, 0});
        // Each iteration expands one pair; the loop runs at most n * (k + 1) times.
        while (!queue.isEmpty()) {
            int[] entry = queue.poll();
            // The queue is ordered by dist, so the first target entry is optimal.
            if (entry[0] == n - 1) return entry[2];
            // Every edge of the expanded vertex is read once per remaining value, the O(E * k) term.
            for (int[] edge : adj.get(entry[0])) {
                int left = entry[1] - edge[1];
                // A negative budget means the edge is not affordable.
                if (left < 0 || seen[edge[0]][left]) continue;
                // Marking at enqueue time keeps each pair in the queue at most once.
                seen[edge[0]][left] = true;
                queue.add(new int[] {edge[0], left, entry[2] + 1});
            }
        }
        // The queue emptied without dequeuing the target.
        return -1;
    }

    /** Oracle: repeated relaxation of dist[v][r] until nothing improves. */
    static int oracle(int n, int[][] edges, int k) {
        int inf = 1_000_000;
        int[][] dist = new int[n][k + 1];
        for (int[] row : dist) Arrays.fill(row, inf);
        dist[0][k] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) for (int r = e[2]; r <= k; r++) {
                if (dist[e[0]][r] + 1 < dist[e[1]][r - e[2]]) { dist[e[1]][r - e[2]] = dist[e[0]][r] + 1; changed = true; }
            }
        }
        int best = inf;
        for (int r = 0; r <= k; r++) best = Math.min(best, dist[n - 1][r]);
        return best >= inf ? -1 : best;
    }

    /** Wrong method kept for the assertion: marks vertices visited, not pairs. */
    static int visitedByNode(int n, int[][] edges, int k) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        boolean[] seen = new boolean[n];
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        seen[0] = true;
        queue.add(new int[] {0, k, 0});
        while (!queue.isEmpty()) {
            int[] entry = queue.poll();
            if (entry[0] == n - 1) return entry[2];
            for (int[] edge : adj.get(entry[0])) {
                int left = entry[1] - edge[1];
                if (left < 0 || seen[edge[0]]) continue;
                seen[edge[0]] = true;
                queue.add(new int[] {edge[0], left, entry[2] + 1});
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] a = {{0, 1, 1}, {1, 2, 0}, {2, 4, 1}, {0, 3, 0}, {3, 4, 1}};
        if (fewestEdges(5, a, 1) != 2) throw new AssertionError("ex1");
        int[][] b = {{0, 1, 1}, {0, 2, 0}, {2, 3, 0}, {3, 1, 0}, {1, 4, 1}};
        if (fewestEdges(5, b, 1) != 4) throw new AssertionError("ex2");
        // The vertex-only visited array loses the charge-holding arrival and reports -1 on the hostile example.
        if (visitedByNode(5, b, 1) != -1) throw new AssertionError("naive fails");
        // A single vertex needs no move, and budget 0 forbids every blocked edge.
        if (fewestEdges(1, new int[0][], 0) != 0) throw new AssertionError("single");
        if (fewestEdges(5, b, 0) != -1) throw new AssertionError("budget 0");
        // Random graphs with cycles and costs 0 or 1 must agree with the oracle for every budget.
        Random rnd = new Random(2201);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(7);
            List<int[]> list = new ArrayList<>();
            int m = rnd.nextInt(2 * n + 3);
            for (int i = 0; i < m; i++) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)});
            int[][] edges = list.toArray(new int[0][]);
            int k = rnd.nextInt(4);
            if (fewestEdges(n, edges, k) != oracle(n, edges, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Best Resource Per Cell (Author exercise)
<!-- id: bv5-best-resource-per-cell -->

**Approach.**
The method replaces the n by (k + 1) array with one integer `best[v]`, the largest remaining budget among entries already enqueued at `v`. A new entry with `left` budget is enqueued only when `left > best[next]`. The array starts at -1, so the first arrival always passes.

The filter is valid because breadth-first search enqueues entries in nondecreasing move count. Every entry counted in `best[next]` has at most as many moves as the new one and at least as much budget, so each route continuing from the new entry also continues from the stored one without finishing later. A later entry with strictly more budget passes the test, since the stored one cannot follow every route of the new one. The invariant is that `best[v]` increases strictly over time. It takes at most `k + 1` values, which bounds the entries per vertex.

**Complexity.**
- **Time** is O((V + E) * k), because a vertex enters the queue at most k + 1 times and each entry scans its edges.
- **Space** is O(V * k) in the worst case for the queue and O(V + E) for `best` and the adjacency list.

```java run
import java.util.*;

public final class BestResourcePerCell {
    /**
     * Returns the fewest edges from 0 to n-1 on a route of total cost at most k, or -1.
     * Time: O((V + E) * k). Space: O(V * k + E).
     * Invariant: best[v] is the largest remaining budget enqueued at v, and only a larger one is enqueued again.
     */
    static int fewestEdges(int n, int[][] edges, int k) {
        // Directed adjacency lists of {next, cost}.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        // -1 means "never reached", which is below every legal remaining budget.
        int[] best = new int[n];
        Arrays.fill(best, -1);
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        best[0] = k;
        queue.add(new int[] {0, k, 0});
        // Entries leave the queue in nondecreasing move count.
        while (!queue.isEmpty()) {
            int[] entry = queue.poll();
            // The first dequeued target entry has the minimum move count.
            if (entry[0] == n - 1) return entry[2];
            for (int[] edge : adj.get(entry[0])) {
                int left = entry[1] - edge[1];
                // Skip unaffordable edges and entries that the stored best budget dominates.
                if (left < 0 || left <= best[edge[0]]) continue;
                // A strictly larger budget replaces the stored value, which bounds entries per vertex by k + 1.
                best[edge[0]] = left;
                queue.add(new int[] {edge[0], left, entry[2] + 1});
            }
        }
        // No legal route reached the target.
        return -1;
    }

    /** Oracle: repeated relaxation of dist[v][r] until nothing improves. */
    static int oracle(int n, int[][] edges, int k) {
        int inf = 1_000_000;
        int[][] dist = new int[n][k + 1];
        for (int[] row : dist) Arrays.fill(row, inf);
        dist[0][k] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) for (int r = e[2]; r <= k; r++) {
                if (dist[e[0]][r] + 1 < dist[e[1]][r - e[2]]) { dist[e[1]][r - e[2]] = dist[e[0]][r] + 1; changed = true; }
            }
        }
        int best = inf;
        for (int r = 0; r <= k; r++) best = Math.min(best, dist[n - 1][r]);
        return best >= inf ? -1 : best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise, the second with a back edge that must be discarded.
        int[][] a = {{0, 1, 1}, {0, 2, 0}, {2, 3, 1}, {1, 3, 0}, {3, 4, 0}, {2, 4, 1}, {4, 0, 0}};
        if (fewestEdges(5, a, 1) != 2) throw new AssertionError("ex1");
        int[][] b = {{0, 1, 1}, {0, 2, 0}, {2, 3, 0}, {3, 1, 0}, {1, 4, 0}, {4, 5, 1}, {5, 0, 0}};
        if (fewestEdges(6, b, 1) != 5) throw new AssertionError("ex2");
        // Java fact: a new int[] holds zeros, so the fill with -1 is needed to tell "never reached" from "reached with zero budget".
        int[] zeros = new int[3];
        if (zeros[1] != 0) throw new AssertionError("new int[] holds zeros");
        // A vertex reached with zero budget must still count as reached.
        if (fewestEdges(2, new int[][] {{0, 1, 1}}, 1) != 1) throw new AssertionError("zero budget arrival");
        if (fewestEdges(1, new int[0][], 5) != 0) throw new AssertionError("single");
        // Random graphs with cycles and costs 0 or 1 must agree with the oracle for every budget.
        Random rnd = new Random(2202);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(7);
            List<int[]> list = new ArrayList<>();
            int m = rnd.nextInt(2 * n + 3);
            for (int i = 0; i < m; i++) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)});
            int[][] edges = list.toArray(new int[0][]);
            int k = rnd.nextInt(4);
            if (fewestEdges(n, edges, k) != oracle(n, edges, k)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Fewest Moves And Most Charges Left (Author exercise)
<!-- id: bv5-longer-path-more-resource -->

**Approach.**
The search is the filtered search of the previous exercise with two changes. The method does not stop at the first entry for the target. It records the move count and remaining budget of that entry, and it keeps dequeuing while the move count stays equal, raising the stored budget when an entry offers more. It stops at the first target entry with a larger move count, and an empty queue means no legal route.

The filter compares budgets only. A later entry with more budget at an already visited vertex passes, so a longer route that saves a charge is never cut off, and the answer shows this in the first example, where only the route with 4 edges is legal. Among target entries in one layer, the filter keeps the largest budget, because the entries arrive in increasing order of budget. The invariant is that the dequeue order has nondecreasing move counts, so every target entry of the minimum move count is dequeued before the loop stops.

**Complexity.**
- **Time** is O((V + E) * k), because each vertex enters the queue at most k + 1 times and each entry scans its edges once.
- **Space** is O(V * k) for the queue in the worst case, plus O(V + E) for `best` and the adjacency list.

```java run
import java.util.*;

public final class LongerPathMoreResource {
    /**
     * Returns {fewest edges, largest remaining budget at that edge count}, or {-1, -1}.
     * Time: O((V + E) * k). Space: O(V * k + E).
     * Invariant: entries are dequeued in nondecreasing move count, and best[v] only increases.
     */
    static int[] fewestWithLeftover(int n, int[][] edges, int k) {
        // Directed adjacency lists of {next, cost}.
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        int[] best = new int[n];
        Arrays.fill(best, -1);
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        best[0] = k;
        queue.add(new int[] {0, k, 0});
        int[] answer = {-1, -1};
        // Entries leave the queue in nondecreasing move count.
        while (!queue.isEmpty()) {
            int[] entry = queue.poll();
            if (entry[0] == n - 1) {
                // The first target entry fixes the move count; later ones in the same layer may raise the leftover.
                if (answer[0] == -1) answer = new int[] {entry[2], entry[1]};
                else if (entry[2] == answer[0]) answer[1] = Math.max(answer[1], entry[1]);
                // A target entry with more moves cannot improve either field, so the search ends.
                else break;
                // Expanding the target would only produce entries with more moves.
                continue;
            }
            for (int[] edge : adj.get(entry[0])) {
                int left = entry[1] - edge[1];
                // Unaffordable edges and dominated entries are skipped; a larger budget at a later layer passes.
                if (left < 0 || left <= best[edge[0]]) continue;
                best[edge[0]] = left;
                queue.add(new int[] {edge[0], left, entry[2] + 1});
            }
        }
        // {-1, -1} remains when the target was never dequeued.
        return answer;
    }

    /** Oracle: repeated relaxation of dist[v][r], then the smallest distance and, on ties, the largest r. */
    static int[] oracle(int n, int[][] edges, int k) {
        int inf = 1_000_000;
        int[][] dist = new int[n][k + 1];
        for (int[] row : dist) Arrays.fill(row, inf);
        dist[0][k] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) for (int r = e[2]; r <= k; r++) {
                if (dist[e[0]][r] + 1 < dist[e[1]][r - e[2]]) { dist[e[1]][r - e[2]] = dist[e[0]][r] + 1; changed = true; }
            }
        }
        int[] out = {-1, -1};
        int min = inf;
        for (int r = 0; r <= k; r++) if (dist[n - 1][r] <= min) { min = dist[n - 1][r]; out = new int[] {min, r}; }
        return min >= inf ? new int[] {-1, -1} : out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise: a longer route with more budget, and a tie between two routes.
        int[][] a = {{0, 1, 1}, {0, 2, 0}, {2, 3, 0}, {3, 1, 0}, {1, 4, 1}};
        if (!Arrays.equals(fewestWithLeftover(5, a, 1), new int[] {4, 0})) throw new AssertionError("ex1");
        int[][] b = {{0, 1, 1}, {1, 3, 0}, {0, 2, 0}, {2, 3, 0}};
        if (!Arrays.equals(fewestWithLeftover(4, b, 1), new int[] {2, 1})) throw new AssertionError("ex2");
        // A single vertex returns zero moves and the whole budget; an unreachable target returns {-1, -1}.
        if (!Arrays.equals(fewestWithLeftover(1, new int[0][], 3), new int[] {0, 3})) throw new AssertionError("single");
        if (!Arrays.equals(fewestWithLeftover(3, new int[][] {{0, 1, 0}}, 2), new int[] {-1, -1})) throw new AssertionError("unreachable");
        // Random graphs with cycles must match the oracle for every budget.
        Random rnd = new Random(2203);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(7);
            List<int[]> list = new ArrayList<>();
            int m = rnd.nextInt(2 * n + 3);
            for (int i = 0; i < m; i++) list.add(new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)});
            int[][] edges = list.toArray(new int[0][]);
            int k = rnd.nextInt(4);
            if (!Arrays.equals(fewestWithLeftover(n, edges, k), oracle(n, edges, k))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Shortest Path in a Grid with Obstacles Elimination (LeetCode 1293)
<!-- id: bv5-grid-obstacles-elimination -->

**Approach.**
The graph is implicit. A vertex is a cell, and the search state is the triple of row, column and remaining eliminations. A move onto an obstacle subtracts 1 from the remaining count, and a move onto an empty cell subtracts 0. The method stores `best[r][c]`, the largest remaining count enqueued at each cell, and enqueues a neighbor only when its remaining count is strictly larger.

Discarding is safe because the queue yields entries in nondecreasing move count. An entry at a cell with no more remaining eliminations than an earlier entry at that cell has no route the earlier entry lacks, and it starts no sooner. A Boolean array by cell discards entries with more eliminations left, which is wrong, and the harness shows that it returns -1 on the second example. The invariant is that `best[r][c]` increases strictly, so a cell enters the queue at most `k + 1` times, and fewer in practice.

**Complexity.**
- **Time** is O(m * n * k), because each cell enters the queue at most `k + 1` times and each entry tries four neighbors.
- **Space** is O(m * n * k) in the worst case for the queue, plus O(m * n) for `best`.

```java run
import java.util.*;

public final class GridObstaclesElimination {
    /**
     * Returns the fewest moves from the top-left to the bottom-right cell with at most k eliminations, or -1.
     * Time: O(m * n * k). Space: O(m * n * k).
     * Invariant: best[r][c] is the largest remaining count enqueued at the cell, and only a larger one is enqueued.
     */
    static int shortestPath(int[][] grid, int k) {
        int rows = grid.length, cols = grid[0].length;
        // -1 means "never reached", below every legal remaining count.
        int[][] best = new int[rows][cols];
        for (int[] row : best) Arrays.fill(row, -1);
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        best[0][0] = k;
        queue.add(new int[] {0, 0, k, 0});
        // Entries leave the queue in nondecreasing move count.
        while (!queue.isEmpty()) {
            int[] entry = queue.poll();
            // The first dequeued target entry has the minimum move count.
            if (entry[0] == rows - 1 && entry[1] == cols - 1) return entry[3];
            // Four neighbors per entry give the constant factor of the time bound.
            for (int[] d : dirs) {
                int r = entry[0] + d[0], c = entry[1] + d[1];
                // Cells outside the grid are skipped.
                if (r < 0 || r >= rows || c < 0 || c >= cols) continue;
                int left = entry[2] - grid[r][c];
                // Skip an unaffordable obstacle or an entry no better than the stored remaining count.
                if (left < 0 || left <= best[r][c]) continue;
                best[r][c] = left;
                queue.add(new int[] {r, c, left, entry[3] + 1});
            }
        }
        // The queue emptied without reaching the corner.
        return -1;
    }

    /** Wrong method kept for the assertion: a Boolean visited array by cell. */
    static int visitedByCell(int[][] grid, int k) {
        int rows = grid.length, cols = grid[0].length;
        boolean[][] seen = new boolean[rows][cols];
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        seen[0][0] = true;
        queue.add(new int[] {0, 0, k, 0});
        while (!queue.isEmpty()) {
            int[] entry = queue.poll();
            if (entry[0] == rows - 1 && entry[1] == cols - 1) return entry[3];
            for (int[] d : dirs) {
                int r = entry[0] + d[0], c = entry[1] + d[1];
                if (r < 0 || r >= rows || c < 0 || c >= cols || seen[r][c]) continue;
                int left = entry[2] - grid[r][c];
                if (left < 0) continue;
                seen[r][c] = true;
                queue.add(new int[] {r, c, left, entry[3] + 1});
            }
        }
        return -1;
    }

    /** Oracle: repeated relaxation of dist[r][c][used] until nothing improves. */
    static int oracle(int[][] grid, int k) {
        int rows = grid.length, cols = grid[0].length, inf = 1_000_000;
        int[][][] dist = new int[rows][cols][k + 1];
        for (int[][] a : dist) for (int[] b : a) Arrays.fill(b, inf);
        dist[0][0][0] = 0;
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) for (int u = 0; u <= k; u++) {
                if (dist[r][c][u] >= inf) continue;
                for (int[] d : dirs) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    int nu = u + grid[nr][nc];
                    if (nu <= k && dist[r][c][u] + 1 < dist[nr][nc][nu]) { dist[nr][nc][nu] = dist[r][c][u] + 1; changed = true; }
                }
            }
        }
        int best = inf;
        for (int u = 0; u <= k; u++) best = Math.min(best, dist[rows - 1][cols - 1][u]);
        return best >= inf ? -1 : best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] g1 = {{0, 0, 0}, {1, 1, 0}, {0, 0, 0}, {0, 1, 1}, {0, 0, 0}};
        if (shortestPath(g1, 1) != 6) throw new AssertionError("ex1");
        int[][] g2 = {{0, 0, 1, 0}, {1, 0, 1, 1}, {1, 0, 1, 0}};
        if (shortestPath(g2, 1) != 5) throw new AssertionError("ex2");
        // The cell-only visited array loses the arrival with eliminations left and returns -1 on the second example.
        if (visitedByCell(g2, 1) != -1) throw new AssertionError("naive fails");
        // A one-cell grid needs no move.
        if (shortestPath(new int[][] {{0}}, 1) != 0) throw new AssertionError("single cell");
        // Random grids must match the oracle; the start and end cells are empty as the contract states.
        Random rnd = new Random(2204);
        for (int t = 0; t < 600; t++) {
            int rows = 1 + rnd.nextInt(4), cols = 1 + rnd.nextInt(4);
            int[][] grid = new int[rows][cols];
            for (int[] row : grid) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(3) == 0 ? 1 : 0;
            grid[0][0] = 0;
            grid[rows - 1][cols - 1] = 0;
            int k = 1 + rnd.nextInt(3);
            if (shortestPath(grid, k) != oracle(grid, k)) throw new AssertionError("random " + t);
        }
    }
}
```
