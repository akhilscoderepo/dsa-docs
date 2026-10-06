<!-- solutions-for: 22-bfs-variations -->
### Solutions For Count By Whole Layers

#### Solution: [Build] Label BFS Layers (Author exercise)
<!-- id: bv2-label-layers -->

**Approach.**
The method builds the adjacency list `adj` with both directions per edge and starts a queue with the source. Each pass copies `queue.size()` into `size`, removes exactly `size` vertices and appends their unvisited neighbors. The removed vertices form one layer, so the method stores them in one list and sorts it. The appended vertices form the next layer.

The invariant is that at the start of every pass the queue holds all vertices of one distance and no other vertex. The first pass satisfies it with the source alone. A vertex enters the queue at its first discovery, which comes from a vertex one layer closer, so the next pass again holds a single distance. The loop ends when the queue is empty, and unreachable vertices never enter a row. The code asserts the Java fact that a copied `size` stays fixed while `queue.size()` grows.

**Complexity.**
- **Time** is O(V + E + V log V), because each adjacency entry is read once and the sorting of rows costs at most V log V in total.
- **Space** is O(V + E) for the adjacency list, and O(V) for the queue, the flags and the rows.

```java run
import java.util.*;

public final class LabelLayers {
    /**
     * Returns the vertices at each distance from source, one ascending row per distance.
     * Time: O(V + E + V log V). Space: O(V + E).
     * Invariant: at the start of a pass the queue holds exactly one layer.
     */
    static int[][] layers(int n, int[][] edges, int source) {
        // Each undirected edge is stored once per direction.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // The source is discovered first; visited prevents a second discovery.
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        visited[source] = true;
        queue.add(source);
        List<int[]> rows = new ArrayList<>();
        // One iteration of the outer loop handles one whole layer.
        while (!queue.isEmpty()) {
            // The snapshot fixes the layer size before any append changes the queue.
            int size = queue.size();
            List<Integer> row = new ArrayList<>();
            // Exactly size removals consume the current layer and nothing of the next.
            for (int i = 0; i < size; i++) {
                int current = queue.poll();
                row.add(current);
                // Each adjacency entry is read once overall, which gives the O(E) term.
                for (int next : adj.get(current)) {
                    // A visited neighbor belongs to this layer or an earlier one.
                    if (visited[next]) continue;
                    // Marking at discovery keeps every vertex in the queue at most once.
                    visited[next] = true;
                    queue.add(next);
                }
            }
            // Sorting makes the row independent of neighbor order.
            Collections.sort(row);
            rows.add(row.stream().mapToInt(Integer::intValue).toArray());
        }
        return rows.toArray(new int[0][]);
    }

    /** Brute force: Floyd-Warshall distances, then group vertices by distance. */
    static int[][] oracle(int n, int[][] edges, int source) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] r : d) Arrays.fill(r, inf);
        for (int v = 0; v < n; v++) d[v][v] = 0;
        for (int[] e : edges) d[e[0]][e[1]] = d[e[1]][e[0]] = 1;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        int maxD = 0;
        for (int v = 0; v < n; v++) if (d[source][v] < inf) maxD = Math.max(maxD, d[source][v]);
        int[][] out = new int[maxD + 1][];
        for (int k = 0; k <= maxD; k++) {
            List<Integer> row = new ArrayList<>();
            for (int v = 0; v < n; v++) if (d[source][v] == k) row.add(v);
            out[k] = row.stream().mapToInt(Integer::intValue).toArray();
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] e1 = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}, {5, 6}};
        if (!Arrays.deepEquals(layers(7, e1, 0), new int[][] {{0}, {1, 2}, {3}, {4}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(layers(4, new int[][] {{1, 2}, {2, 3}}, 0), new int[][] {{0}})) throw new AssertionError("ex2");
        // Java fact: a size copied into a local stays fixed while the queue grows.
        ArrayDeque<Integer> q = new ArrayDeque<>(List.of(1, 2));
        int copied = q.size();
        q.add(3);
        if (copied != 2 || q.size() != 3) throw new AssertionError("snapshot stays fixed");
        // Random graphs must match the Floyd-Warshall grouping from a random source.
        Random rnd = new Random(2202);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(4) == 0) es.add(new int[] {a, b});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            int s = rnd.nextInt(n);
            if (!Arrays.deepEquals(layers(n, arr, s), oracle(n, arr, s))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Stop At First Target Layer (Author exercise)
<!-- id: bv2-first-target-layer -->

**Approach.**
The method runs the pass loop of the first exercise and keeps the pass number `depth`. A pass removes `size` vertices and appends their unvisited neighbors, and it counts how many appended vertices equal the number of vertices in the next layer. The target is first discovered in some pass, and that pass belongs to layer `depth + 1`. The method continues until the pass that discovered the target has appended its whole layer, and then it returns that depth and the number of appended vertices.

The invariant is that all vertices appended by one pass share the same distance, so the count of appended vertices equals the size of one complete layer, and the pass finishes the layer before the method returns. Stopping inside a pass would report a partial count. If the source equals the target, the answer is `[0, 1]`, because layer 0 is the source alone. If the queue empties first, the target is unreachable and the answer is `[-1, 0]`.

**Complexity.**
- **Time** is O(V + E), because the search reads each adjacency entry at most once and stops no later than the full traversal.
- **Space** is O(V + E) for the adjacency list, and O(V) for the queue and the flags.

```java run
import java.util.*;

public final class FirstTargetLayer {
    /**
     * Returns {distance of target, number of vertices at that distance}, or {-1, 0}.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: vertices appended by one pass share one distance.
     */
    static int[] firstTargetLayer(int n, int[][] edges, int source, int target) {
        // The source layer is complete at once, so equal endpoints need no search.
        if (source == target) return new int[] {0, 1};
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        visited[source] = true;
        queue.add(source);
        int depth = 0;
        // Each pass expands layer depth and appends layer depth + 1.
        while (!queue.isEmpty()) {
            int size = queue.size();
            int appended = 0;
            boolean hit = false;
            // The inner loop removes exactly the current layer.
            for (int i = 0; i < size; i++) {
                int current = queue.poll();
                for (int next : adj.get(current)) {
                    // A visited neighbor already has a distance that is at most depth + 1.
                    if (visited[next]) continue;
                    visited[next] = true;
                    queue.add(next);
                    appended++;
                    // The target is noted, but the pass continues so the layer count is complete.
                    if (next == target) hit = true;
                }
            }
            depth++;
            // Returning after the pass, not inside it, gives the whole layer size.
            if (hit) return new int[] {depth, appended};
        }
        // The queue emptied without discovering the target.
        return new int[] {-1, 0};
    }

    /** Brute force: Floyd-Warshall distances and a count of vertices at the target distance. */
    static int[] oracle(int n, int[][] edges, int source, int target) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] r : d) Arrays.fill(r, inf);
        for (int v = 0; v < n; v++) d[v][v] = 0;
        for (int[] e : edges) d[e[0]][e[1]] = d[e[1]][e[0]] = 1;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        if (d[source][target] >= inf) return new int[] {-1, 0};
        int count = 0;
        for (int v = 0; v < n; v++) if (d[source][v] == d[source][target]) count++;
        return new int[] {d[source][target], count};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] e1 = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {2, 4}, {3, 5}, {4, 5}, {5, 6}, {6, 7}};
        if (!Arrays.equals(firstTargetLayer(8, e1, 0, 4), new int[] {2, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(firstTargetLayer(6, new int[][] {{0, 1}, {1, 2}, {3, 4}}, 0, 4), new int[] {-1, 0})) throw new AssertionError("ex2");
        // Equal endpoints form layer 0 alone.
        if (!Arrays.equals(firstTargetLayer(3, new int[][] {{0, 1}}, 2, 2), new int[] {0, 1})) throw new AssertionError("same vertex");
        // Java fact: Arrays.equals compares contents, while == on two arrays compares references.
        int[] a = {1, 2}, b = {1, 2};
        if (a == b || !Arrays.equals(a, b)) throw new AssertionError("array equality");
        // Random graphs must match the Floyd-Warshall answer for random endpoints.
        Random rnd = new Random(2203);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) if (rnd.nextInt(4) == 0) es.add(new int[] {x, y});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            if (!Arrays.equals(firstTargetLayer(n, arr, s, g), oracle(n, arr, s, g))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Initially Complete State (Author exercise)
<!-- id: bv2-initially-complete -->

**Approach.**
The method runs the pass loop and keeps a counter `units`. For each pass it copies the queue size, removes that many vertices and appends their unvisited neighbors. The counter rises by one only when the pass appended at least one vertex. If the source has no neighbor, the first pass appends nothing, so the method returns 0 before any time unit is counted.

The invariant is that `units` equals the number of completed layers after layer 0, and layer 0 costs no time because the source holds the update from the start. The last pass in every run appends nothing, so counting each pass would overcount by one on every input. The vertices outside the component of the source never enter the queue and do not change the result.

**Complexity.**
- **Time** is O(V + E), because each vertex enters the queue once and each adjacency entry is read once.
- **Space** is O(V + E) for the adjacency list, and O(V) for the queue and the flags.

```java run
import java.util.*;

public final class InitiallyComplete {
    /**
     * Returns the number of time units until the whole component of source holds the update.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: units equals the number of completed layers after layer 0.
     */
    static int timeUnits(int n, int[][] edges, int source) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        visited[source] = true;
        queue.add(source);
        int units = 0;
        // The loop ends when a pass leaves the queue empty.
        while (!queue.isEmpty()) {
            // The snapshot separates the current layer from the one being appended.
            int size = queue.size();
            boolean grew = false;
            for (int i = 0; i < size; i++) {
                int current = queue.poll();
                for (int next : adj.get(current)) {
                    // Neighbors in the same or an earlier layer are skipped.
                    if (visited[next]) continue;
                    visited[next] = true;
                    queue.add(next);
                    grew = true;
                }
            }
            // A pass that adds nothing is the last one and costs no time unit.
            if (grew) units++;
        }
        return units;
    }

    /** Brute force: repeat the spread step on a boolean array until no vertex changes. */
    static int oracle(int n, int[][] edges, int source) {
        boolean[] has = new boolean[n];
        has[source] = true;
        int units = 0;
        while (true) {
            boolean[] next = has.clone();
            for (int[] e : edges) {
                if (has[e[0]]) next[e[1]] = true;
                if (has[e[1]]) next[e[0]] = true;
            }
            if (Arrays.equals(next, has)) return units;
            has = next;
            units++;
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (timeUnits(1, new int[0][], 0) != 0) throw new AssertionError("ex1");
        if (timeUnits(3, new int[][] {{0, 1}, {1, 2}, {0, 2}}, 0) != 1) throw new AssertionError("ex2");
        // A source in the middle of a path needs two time units.
        if (timeUnits(4, new int[][] {{0, 1}, {1, 2}, {2, 3}}, 1) != 2) throw new AssertionError("middle source");
        // Java fact: an int[0][] argument is a valid empty edge list and has length 0.
        if (new int[0][].length != 0) throw new AssertionError("empty edge array");
        // Random graphs must match the repeated spread simulation.
        Random rnd = new Random(2204);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) if (rnd.nextInt(4) == 0) es.add(new int[] {x, y});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            int s = rnd.nextInt(n);
            if (timeUnits(n, arr, s) != oracle(n, arr, s)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Rotting Oranges With Minute Counts (LeetCode 994)
<!-- id: bv2-rotting-counts -->

**Approach.**
The method puts every rotten cell into one queue, because all of them spread at the same time. Each pass copies the queue size, removes that many rotten cells and turns every fresh edge neighbor rotten at the moment it is discovered. The number of cells turned in the pass is one minute's count. The method appends this count to the result only when it is positive.

The invariant is that at the start of each pass the queue holds exactly the oranges that became rotten in the previous minute, or the initial rotten oranges in the first pass. Marking a neighbor rotten at discovery stops a second discovery in the same minute. A fresh orange with no path to a rotten orange is never discovered, so it stays fresh and is not counted. A grid with no rotten orange, or with no fresh orange next to one, gives an empty array. The code asserts that an empty `int[]` has length 0.

**Complexity.**
- **Time** is O(m * n), because each cell is queued at most once and has four neighbors.
- **Space** is O(m * n) for the queue in the worst case and the result list. The grid is modified in place, and the input array is copied first so the caller keeps its grid.

```java run
import java.util.*;

public final class RottingCounts {
    /**
     * Returns how many fresh oranges rot in each minute, skipping minutes with none.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: at the start of a pass the queue holds the oranges that rotted in the last minute.
     */
    static int[] minuteCounts(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        // Work on a copy so the caller's grid is unchanged.
        int[][] g = new int[m][];
        for (int i = 0; i < m; i++) g[i] = grid[i].clone();
        // All rotten oranges start in the same queue because they spread together.
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) if (g[i][j] == 2) queue.add(new int[] {i, j});
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        List<Integer> counts = new ArrayList<>();
        // One iteration of the loop is one minute.
        while (!queue.isEmpty()) {
            // The snapshot keeps this minute's oranges apart from the ones that rot now.
            int size = queue.size();
            int rotted = 0;
            for (int k = 0; k < size; k++) {
                int[] cell = queue.poll();
                for (int[] d : dirs) {
                    int x = cell[0] + d[0], y = cell[1] + d[1];
                    // Only a fresh cell inside the grid changes; empty and rotten cells are skipped.
                    if (x < 0 || y < 0 || x >= m || y >= n || g[x][y] != 1) continue;
                    // Marking at discovery prevents a second discovery in this minute.
                    g[x][y] = 2;
                    queue.add(new int[] {x, y});
                    rotted++;
                }
            }
            // A pass with no new rotten orange is not a minute of the answer.
            if (rotted > 0) counts.add(rotted);
        }
        return counts.stream().mapToInt(Integer::intValue).toArray();
    }

    /** Brute force: rescan the whole grid each minute and rot every fresh cell next to a rotten one. */
    static int[] oracle(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] g = new int[m][];
        for (int i = 0; i < m; i++) g[i] = grid[i].clone();
        List<Integer> counts = new ArrayList<>();
        while (true) {
            List<int[]> turn = new ArrayList<>();
            for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
                if (g[i][j] != 1) continue;
                boolean near = (i > 0 && g[i - 1][j] == 2) || (i < m - 1 && g[i + 1][j] == 2)
                    || (j > 0 && g[i][j - 1] == 2) || (j < n - 1 && g[i][j + 1] == 2);
                if (near) turn.add(new int[] {i, j});
            }
            if (turn.isEmpty()) break;
            for (int[] c : turn) g[c[0]][c[1]] = 2;
            counts.add(turn.size());
        }
        return counts.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(minuteCounts(new int[][] {{2, 1, 1, 0}, {1, 1, 0, 1}, {0, 1, 1, 1}}), new int[] {2, 2, 1, 1, 1, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(minuteCounts(new int[][] {{2, 1, 0}, {0, 0, 1}, {1, 0, 2}}), new int[] {2})) throw new AssertionError("ex2");
        // No rotten orange, and no fresh orange, both give an empty array.
        if (minuteCounts(new int[][] {{1, 1}, {1, 1}}).length != 0) throw new AssertionError("no source");
        if (minuteCounts(new int[][] {{0, 2}}).length != 0) throw new AssertionError("no fresh");
        // The input grid is left unchanged.
        int[][] keep = {{2, 1}};
        minuteCounts(keep);
        if (keep[0][1] != 1) throw new AssertionError("input mutated");
        // Java fact: a stream of an empty list converts to an int[] of length 0.
        if (new ArrayList<Integer>().stream().mapToInt(Integer::intValue).toArray().length != 0) throw new AssertionError("empty int array");
        // Random grids must match the full-rescan simulation.
        Random rnd = new Random(2205);
        for (int t = 0; t < 800; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] grid = new int[m][n];
            for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) grid[i][j] = rnd.nextInt(3);
            if (!Arrays.equals(minuteCounts(grid), oracle(grid))) throw new AssertionError("random " + t);
        }
    }
}
```
