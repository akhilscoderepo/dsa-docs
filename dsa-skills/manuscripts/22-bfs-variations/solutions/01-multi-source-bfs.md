<!-- solutions-for: 22-bfs-variations -->
### Solutions For Start From Many Sources

#### Solution: [Build] Nearest Source Distances (Author exercise)
<!-- id: bv1-nearest-source-distances -->

**Approach.**
The method builds the adjacency list with both directions for every edge. It fills `distance` with -1 and then walks over `sources`. A source that is not yet visited is marked visited, receives distance 0 and joins the queue. The visited check makes a repeated source harmless.

The main loop is the ordinary breadth-first loop. It takes the front vertex `current` and gives each unvisited neighbor the value `distance[current] + 1`. All sources sit in the queue before the first removal, so the queue always holds one layer followed by the next. The invariant is that vertices leave the queue in nondecreasing distance, so the first discovery of a vertex fixes its distance to the closest source. The tests also assert that `Arrays.fill` on a new array replaces zeros.

**Complexity.**
- **Time** is O(V + E + S), because each vertex is enqueued once, each adjacency entry is read once and each source is read once.
- **Space** is O(V + E) for the adjacency list, and the arrays and the queue add O(V) more.

```java run
import java.util.*;

public final class NearestSourceDistances {
    /**
     * Returns, for every vertex, the edge count to the closest source, or -1 when none is reachable.
     * Time: O(V + E + S). Space: O(V + E).
     * Invariant: vertices leave the queue in nondecreasing distance.
     */
    static int[] nearest(int n, int[][] edges, int[] sources) {
        // Each undirected edge is stored in both directions.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // Distance starts at -1 so unreachable vertices keep the failure value.
        boolean[] visited = new boolean[n];
        int[] distance = new int[n];
        Arrays.fill(distance, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The loop over sources costs O(S) and puts every distinct source in the queue at distance 0.
        for (int s : sources) {
            // A repeated source is skipped so it never enters the queue twice.
            if (visited[s]) continue;
            visited[s] = true;
            distance[s] = 0;
            queue.add(s);
        }
        // Each iteration expands one vertex, so the loop runs at most n times.
        while (!queue.isEmpty()) {
            int current = queue.poll();
            // Every adjacency entry is read once over the whole run, which gives the O(E) term.
            for (int next : adj.get(current)) {
                // A visited neighbor already has an equal or smaller distance.
                if (visited[next]) continue;
                // Marking at discovery keeps each vertex in the queue at most once.
                visited[next] = true;
                distance[next] = distance[current] + 1;
                queue.add(next);
            }
        }
        // Vertices that no source reaches still hold -1.
        return distance;
    }

    /** Brute force: Floyd-Warshall distances, then the minimum over all sources. */
    static int[] brute(int n, int[][] edges, int[] sources) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int v = 0; v < n; v++) d[v][v] = 0;
        for (int[] e : edges) d[e[0]][e[1]] = d[e[1]][e[0]] = 1;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        int[] out = new int[n];
        for (int v = 0; v < n; v++) {
            int best = inf;
            for (int s : sources) best = Math.min(best, d[s][v]);
            out[v] = best >= inf ? -1 : best;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(nearest(7, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 5}}, new int[] {0, 5}), new int[] {0, 1, 2, 2, 1, 0, -1})) throw new AssertionError("ex1");
        if (!Arrays.equals(nearest(6, new int[][] {{0, 1}, {1, 2}, {3, 4}}, new int[] {1, 1}), new int[] {1, 0, 1, -1, -1, -1})) throw new AssertionError("ex2");
        // An empty source list leaves every vertex at -1.
        if (!Arrays.equals(nearest(3, new int[][] {{0, 1}}, new int[0]), new int[] {-1, -1, -1})) throw new AssertionError("no sources");
        // Java fact: a new int[] holds zeros, so the fill with -1 is required.
        int[] fresh = new int[2];
        if (fresh[0] != 0 || fresh[1] != 0) throw new AssertionError("new int[] holds zeros");
        Arrays.fill(fresh, -1);
        if (fresh[0] != -1 || fresh[1] != -1) throw new AssertionError("fill replaces zeros");
        // Random graphs with random, possibly repeated sources must match the brute force.
        Random rnd = new Random(2211);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(4) == 0) es.add(new int[] {a, b});
            Collections.shuffle(es, rnd);
            int[] src = new int[rnd.nextInt(n + 1)];
            for (int i = 0; i < src.length; i++) src[i] = rnd.nextInt(n);
            int[][] arr = es.toArray(new int[0][]);
            if (!Arrays.equals(nearest(n, arr, src), brute(n, arr, src))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] 01 Matrix (LeetCode 542)
<!-- id: bv1-zero-one-matrix -->

**Approach.**
The graph is implicit, so the method needs no adjacency list. A cell is a vertex, and its four side neighbors are the edges. The method scans the matrix once. Each cell that holds 0 gets distance 0 and joins the queue, and each other cell gets -1 as a marker for not yet discovered. That marker also serves as the visited check, so no second array is needed.

The queue then drives the ordinary loop. A cell is stored as the single int `r * n + c`, and the loop decodes it with division and remainder. Because all zeros enter the queue before any removal, the first discovery of a cell comes from its nearest zero. The invariant is that every dequeued cell holds its final distance. The result is a new matrix, and the input stays unchanged.

**Complexity.**
- **Time** is O(m * n), because each cell enters the queue once and reads four neighbors.
- **Space** is O(m * n) for the output matrix and the queue.

```java run
import java.util.*;

public final class ZeroOneMatrix {
    /**
     * Returns for each cell the number of side moves to the nearest 0.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: a dequeued cell holds its final distance.
     */
    static int[][] distances(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        // -1 marks an undiscovered cell; the output is a new matrix.
        int[][] dist = new int[m][n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // One scan over all cells seeds the queue with every zero at distance 0.
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (mat[r][c] == 0) queue.add(r * n + c);
                else dist[r][c] = -1;
            }
        }
        int[] dr = {1, -1, 0, 0};
        int[] dc = {0, 0, 1, -1};
        // Each cell is removed once, so the loop runs at most m * n times.
        while (!queue.isEmpty()) {
            int code = queue.poll();
            int r = code / n, c = code % n;
            // Four neighbors per cell give the constant factor of the O(m * n) bound.
            for (int k = 0; k < 4; k++) {
                int nr = r + dr[k], nc = c + dc[k];
                // Skip cells outside the matrix and cells that already have a distance.
                if (nr < 0 || nr >= m || nc < 0 || nc >= n || dist[nr][nc] != -1) continue;
                // The first discovery is final, so the cell joins the queue exactly once.
                dist[nr][nc] = dist[r][c] + 1;
                queue.add(nr * n + nc);
            }
        }
        return dist;
    }

    /** Brute force: with no obstacles the answer is the smallest Manhattan distance to a zero. */
    static int[][] brute(int[][] mat) {
        int m = mat.length, n = mat[0].length;
        int[][] out = new int[m][n];
        for (int r = 0; r < m; r++) for (int c = 0; c < n; c++) {
            int best = Integer.MAX_VALUE;
            for (int a = 0; a < m; a++) for (int b = 0; b < n; b++) if (mat[a][b] == 0) best = Math.min(best, Math.abs(a - r) + Math.abs(b - c));
            out[r][c] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(distances(new int[][] {{0, 0, 0}, {0, 1, 0}, {1, 1, 1}}), new int[][] {{0, 0, 0}, {0, 1, 0}, {1, 2, 1}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(distances(new int[][] {{1, 1, 1}, {1, 1, 1}, {1, 1, 0}}), new int[][] {{4, 3, 2}, {3, 2, 1}, {2, 1, 0}})) throw new AssertionError("ex2");
        // A single row and a single cell are the smallest shapes.
        if (!Arrays.deepEquals(distances(new int[][] {{1, 1, 0}}), new int[][] {{2, 1, 0}})) throw new AssertionError("row");
        if (!Arrays.deepEquals(distances(new int[][] {{0}}), new int[][] {{0}})) throw new AssertionError("cell");
        // The input stays unchanged.
        int[][] in = {{1, 0}};
        distances(in);
        if (!Arrays.deepEquals(in, new int[][] {{1, 0}})) throw new AssertionError("input mutated");
        // Java fact: a new int[m][n] holds zeros in every row, so source cells need no write.
        int[][] fresh = new int[2][2];
        if (fresh[1][1] != 0) throw new AssertionError("new int[][] holds zeros");
        // Random matrices with at least one zero must match the brute force.
        Random rnd = new Random(2212);
        for (int t = 0; t < 500; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] mat = new int[m][n];
            for (int[] row : mat) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(3) == 0 ? 0 : 1;
            mat[rnd.nextInt(m)][rnd.nextInt(n)] = 0;
            if (!Arrays.deepEquals(distances(mat), brute(mat))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] No Source Or All Sources (Author exercise)
<!-- id: bv1-no-source-all-sources -->

**Approach.**
The method seeds the queue with all sources, exactly as in the first exercise, and then processes the queue one layer at a time. At the start of each round it reads `size = queue.size()`, which is the number of vertices of the current layer. It removes exactly `size` vertices and discovers their neighbors, and it records whether any neighbor was new.

The counter `rounds` grows only after a round that discovered a vertex. The last layer of the search removes its vertices and finds nothing new, so counting every loop pass would report one round too many. An empty source list never enters the loop, and a list that holds every vertex enters the loop once and finds nothing new, so both return 0. The invariant is that `rounds` equals the largest distance assigned so far.

**Complexity.**
- **Time** is O(V + E), because each vertex and each adjacency entry is handled once, and the layer bookkeeping adds O(1) per layer.
- **Space** is O(V + E) for the adjacency list, and the visited array and the queue add O(V) more.

```java run
import java.util.*;

public final class NoSourceAllSources {
    /**
     * Returns the number of rounds in which at least one new vertex becomes reached.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: rounds equals the largest distance assigned so far.
     */
    static int rounds(int n, int[][] edges, int[] sources) {
        // Adjacency lists with both directions for each edge.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // All sources are reached at round 0, so they enter the queue first.
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int s : sources) { visited[s] = true; queue.add(s); }
        int rounds = 0;
        // Each pass of the loop handles one whole layer; an empty queue skips the loop.
        while (!queue.isEmpty()) {
            // The size is read once, so vertices added during this pass wait for the next pass.
            int size = queue.size();
            boolean grew = false;
            for (int i = 0; i < size; i++) {
                int current = queue.poll();
                // Each adjacency entry is read once over the whole run.
                for (int next : adj.get(current)) {
                    if (visited[next]) continue;
                    visited[next] = true;
                    queue.add(next);
                    grew = true;
                }
            }
            // A pass that found nothing new is not a round, which avoids the false increment.
            if (grew) rounds++;
        }
        return rounds;
    }

    /** Brute force: Floyd-Warshall, then the largest finite minimum distance to a source. */
    static int brute(int n, int[][] edges, int[] sources) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int v = 0; v < n; v++) d[v][v] = 0;
        for (int[] e : edges) d[e[0]][e[1]] = d[e[1]][e[0]] = 1;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        int worst = 0;
        for (int v = 0; v < n; v++) {
            int best = inf;
            for (int s : sources) best = Math.min(best, d[s][v]);
            if (best < inf) worst = Math.max(worst, best);
        }
        return worst;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (rounds(4, new int[][] {{0, 1}, {1, 2}, {2, 3}}, new int[0]) != 0) throw new AssertionError("ex1");
        if (rounds(7, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 5}}, new int[] {0, 5}) != 2) throw new AssertionError("ex2");
        // Every vertex is a source, so no round discovers anything.
        if (rounds(3, new int[][] {{0, 1}, {1, 2}}, new int[] {0, 1, 2}) != 0) throw new AssertionError("all sources");
        // One source on a path of four vertices needs three rounds.
        if (rounds(4, new int[][] {{0, 1}, {1, 2}, {2, 3}}, new int[] {0}) != 3) throw new AssertionError("path");
        // Java fact: size() is a snapshot, so adding to the queue does not change a stored size.
        ArrayDeque<Integer> q = new ArrayDeque<>(List.of(1, 2));
        int size = q.size();
        q.add(3);
        if (size != 2 || q.size() != 3) throw new AssertionError("size snapshot");
        // Random graphs with distinct random sources must match the brute force.
        Random rnd = new Random(2213);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(4) == 0) es.add(new int[] {a, b});
            List<Integer> all = new ArrayList<>();
            for (int v = 0; v < n; v++) if (rnd.nextInt(3) == 0) all.add(v);
            int[] src = all.stream().mapToInt(Integer::intValue).toArray();
            int[][] arr = es.toArray(new int[0][]);
            if (rounds(n, arr, src) != brute(n, arr, src)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Rotting Oranges (LeetCode 994)
<!-- id: bv1-rotting-oranges -->

**Approach.**
Every rotten orange is a source, and one minute is one layer of the search. The method scans the grid once. It puts each rotten cell into the queue and counts the fresh oranges in `fresh`. It then runs the loop while the queue is not empty and `fresh` is positive.

Each pass reads `size = queue.size()` and removes that many cells. A fresh neighbor becomes rotten at once, which also serves as its visited mark, and `fresh` drops by one. After the pass, `minutes` grows by one. The loop stops as soon as `fresh` reaches 0, so the method does not count a layer that rots nothing. If `fresh` is still positive when the queue runs empty, some orange has no path to a rotten one, and the method returns -1. The invariant is that `minutes` equals the number of completed layers. The method changes `grid` in place, which the stated contract allows, because the caller passes a grid that it does not reuse.

**Complexity.**
- **Time** is O(m * n), because each cell enters the queue at most once and reads four neighbors.
- **Space** is O(m * n) for the queue in the worst case, and no other structure grows with the grid.

```java run
import java.util.*;

public final class RottingOranges {
    /**
     * Returns the minutes until no fresh orange remains, or -1 when one is unreachable.
     * Time: O(m * n). Space: O(m * n). Mutates the grid it receives.
     * Invariant: minutes equals the number of completed layers.
     */
    static int minutes(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        int fresh = 0;
        // One scan collects the sources and counts the oranges that still need to rot.
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 2) queue.add(r * n + c);
                else if (grid[r][c] == 1) fresh++;
            }
        }
        int[] dr = {1, -1, 0, 0};
        int[] dc = {0, 0, 1, -1};
        int minutes = 0;
        // The loop stops when nothing is left to rot, so an extra empty layer is never counted.
        while (!queue.isEmpty() && fresh > 0) {
            // The size snapshot separates this minute from the next one.
            int size = queue.size();
            for (int i = 0; i < size; i++) {
                int code = queue.poll();
                int r = code / n, c = code % n;
                // Four neighbors per cell, so the total work is O(m * n).
                for (int k = 0; k < 4; k++) {
                    int nr = r + dr[k], nc = c + dc[k];
                    // Only a fresh orange inside the grid can rot.
                    if (nr < 0 || nr >= m || nc < 0 || nc >= n || grid[nr][nc] != 1) continue;
                    // Rotting the cell now doubles as its visited mark.
                    grid[nr][nc] = 2;
                    fresh--;
                    queue.add(nr * n + nc);
                }
            }
            // One whole layer is one minute.
            minutes++;
        }
        // Remaining fresh oranges have no path to any rotten orange.
        return fresh == 0 ? minutes : -1;
    }

    /** Brute force: apply the rule minute by minute on a deep copy until the grid stops changing. */
    static int brute(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] cur = new int[m][];
        for (int r = 0; r < m; r++) cur[r] = grid[r].clone();
        int t = 0;
        while (true) {
            int[][] next = new int[m][];
            for (int r = 0; r < m; r++) next[r] = cur[r].clone();
            boolean changed = false;
            for (int r = 0; r < m; r++) for (int c = 0; c < n; c++) {
                if (cur[r][c] != 1) continue;
                int[][] d = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
                for (int[] x : d) {
                    int a = r + x[0], b = c + x[1];
                    if (a >= 0 && a < m && b >= 0 && b < n && cur[a][b] == 2) { next[r][c] = 2; changed = true; break; }
                }
            }
            if (!changed) break;
            cur = next;
            t++;
        }
        for (int[] row : cur) for (int v : row) if (v == 1) return -1;
        return t;
    }

    static int[][] copy(int[][] g) {
        int[][] out = new int[g.length][];
        for (int i = 0; i < g.length; i++) out[i] = g[i].clone();
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minutes(copy(new int[][] {{2, 1, 1}, {1, 1, 0}, {0, 1, 1}})) != 4) throw new AssertionError("ex1");
        if (minutes(copy(new int[][] {{2, 1, 1}, {0, 1, 1}, {1, 0, 1}})) != -1) throw new AssertionError("ex2");
        // No fresh orange means no minute passes, and a lone empty cell has nothing to do.
        if (minutes(copy(new int[][] {{0, 2}})) != 0) throw new AssertionError("no fresh");
        if (minutes(copy(new int[][] {{0}})) != 0) throw new AssertionError("empty cell");
        // Fresh oranges and no rotten orange give -1 without entering the loop.
        if (minutes(copy(new int[][] {{1}})) != -1) throw new AssertionError("no source");
        // Java fact: clone of an int[][] copies only the outer array, so rows are shared.
        int[][] g = {{1, 2}};
        int[][] shallow = g.clone();
        shallow[0][0] = 9;
        if (g[0][0] != 9) throw new AssertionError("shallow clone shares rows");
        // Random grids must match the minute-by-minute simulation.
        Random rnd = new Random(2214);
        for (int t = 0; t < 600; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] grid = new int[m][n];
            for (int[] row : grid) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(3);
            int expected = brute(grid);
            if (minutes(copy(grid)) != expected) throw new AssertionError("random " + t);
        }
    }
}
```
