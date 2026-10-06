<!-- solutions-for: 07-unweighted-shortest-paths -->
### Solutions For Unweighted Shortest Paths

#### Solution: [Build] Distance From One Source (Author exercise)
<!-- id: gt-distance-one-source -->

**Approach.**
The method builds the adjacency list `adj` with both directions for every edge. It fills `distance` with -1, sets the source to 0 and puts the source into an `ArrayDeque`. Each loop step takes the front vertex `current` and scans its neighbors. A neighbor that is not visited is marked visited, gets `distance[current] + 1` and goes to the back of the queue.

The queue holds the vertices of one level followed by the vertices of the next level, so vertices leave the queue in nondecreasing distance. The first discovery of a vertex therefore comes from the smallest possible level and fixes its true distance. The invariant is that every vertex in the queue has its final distance, and no unvisited vertex has a smaller distance than a queued one. The code asserts two Java facts, that a new `int[]` holds zeros and that `poll` on an empty `ArrayDeque` returns `null`.

**Complexity.**
- **Time** is O(V + E), because each vertex enters the queue once and each adjacency entry is read once.
- **Space** is O(V + E) for the adjacency list, plus O(V) for the arrays and the queue.

```java run
import java.util.*;

public final class DistanceOneSource {
    /**
     * Returns the minimum edge count from source to every vertex, or -1 when unreachable.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: queued vertices have final distances, in nondecreasing order.
     */
    static int[] distances(int n, int[][] edges, int source) {
        // Undirected edges are stored in both directions.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // Visited marks discovery; distance starts at -1 so unreachable vertices keep the failure value.
        boolean[] visited = new boolean[n];
        int[] distance = new int[n];
        Arrays.fill(distance, -1);
        // The source is discovered first, at distance 0.
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        visited[source] = true;
        distance[source] = 0;
        queue.add(source);
        // Each iteration expands one vertex; the loop runs at most n times.
        while (!queue.isEmpty()) {
            int current = queue.poll();
            // Each adjacency entry is read once over the whole run, which gives the O(E) term.
            for (int next : adj.get(current)) {
                // A visited neighbor was discovered earlier, so its distance is already minimal.
                if (visited[next]) continue;
                // Marking at discovery keeps every vertex in the queue at most once.
                visited[next] = true;
                distance[next] = distance[current] + 1;
                queue.add(next);
            }
        }
        // Vertices in other components still hold -1.
        return distance;
    }

    /** Brute force: Floyd-Warshall on the edge matrix with a large value for "no path". */
    static int[] floyd(int n, int[][] edges, int source) {
        int inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int v = 0; v < n; v++) d[v][v] = 0;
        for (int[] e : edges) d[e[0]][e[1]] = d[e[1]][e[0]] = 1;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        int[] out = new int[n];
        for (int v = 0; v < n; v++) out[v] = d[source][v] >= inf ? -1 : d[source][v];
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(distances(6, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}}, 0), new int[] {0, 1, 1, 2, 3, -1})) throw new AssertionError("ex1");
        if (!Arrays.equals(distances(5, new int[][] {{0, 1}, {1, 2}, {0, 2}, {2, 3}}, 0), new int[] {0, 1, 1, 2, -1})) throw new AssertionError("ex2");
        // A single vertex has only the source at distance 0.
        if (!Arrays.equals(distances(1, new int[0][], 0), new int[] {0})) throw new AssertionError("single vertex");
        // Java fact: a new int[] holds zeros, which is why the fill with -1 is needed.
        int[] fresh = new int[3];
        if (fresh[0] != 0 || fresh[1] != 0 || fresh[2] != 0) throw new AssertionError("new int[] holds zeros");
        // Java fact: poll on an empty ArrayDeque returns null and does not throw.
        if (new ArrayDeque<Integer>().poll() != null) throw new AssertionError("poll on empty returns null");
        // Random graphs must match Floyd-Warshall from every source.
        Random rnd = new Random(2207);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(4) == 0) es.add(new int[] {a, b});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            int s = rnd.nextInt(n);
            if (!Arrays.equals(distances(n, arr, s), floyd(n, arr, s))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Restore One Shortest Path (Author exercise)
<!-- id: gt-restore-shortest-path -->

**Approach.**
The search is the same, but it stores `predecessor[next] = current` at the moment of first discovery. The method does not need a `distance` array, because the predecessor array also marks discovery: the value -1 means not discovered, and the source gets its own index as predecessor so that it counts as discovered. The search stops as soon as the target is discovered, because its predecessor is final at that moment.

To restore the path, the method starts at the target and follows predecessors until it reaches the source. It then reverses the collected list. Each vertex has exactly one predecessor, so the chain has no repeated vertex and its length equals the distance. The invariant is that following predecessors from any discovered vertex leads to the source through vertices of strictly decreasing distance. An unreachable target ends the loop with an empty queue, and the method returns an empty list.

**Complexity.**
- **Time** is O(V + E) for the search, plus O(L) to restore a path of length `L`, and `L < V`.
- **Space** is O(V + E) for the adjacency list, plus O(V) for the predecessor array and the queue.

```java run
import java.util.*;

public final class RestoreShortestPath {
    /**
     * Returns one shortest path from source to target, or an empty list when none exists.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: predecessor links from a discovered vertex lead back to the source.
     */
    static List<Integer> shortestPath(int n, int[][] edges, int source, int target) {
        // Adjacency lists in edge order, so ties resolve by the order of the input.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // -1 marks "not discovered"; the source points to itself so it counts as discovered.
        int[] predecessor = new int[n];
        Arrays.fill(predecessor, -1);
        predecessor[source] = source;
        ArrayDeque<Integer> queue = new ArrayDeque<>(List.of(source));
        // The loop ends when the queue is empty or the target has been discovered.
        while (!queue.isEmpty() && predecessor[target] == -1) {
            int current = queue.poll();
            for (int next : adj.get(current)) {
                // The first vertex that reaches next is the predecessor, and later ones are ignored.
                if (predecessor[next] != -1) continue;
                predecessor[next] = current;
                queue.add(next);
            }
        }
        // An undiscovered target means no path exists.
        List<Integer> path = new ArrayList<>();
        if (predecessor[target] == -1) return path;
        // Walk back from the target; the source is the only vertex that points to itself.
        for (int v = target; ; v = predecessor[v]) {
            path.add(v);
            if (v == source) break;
        }
        // The walk collected the path backwards, so reverse it in O(L).
        Collections.reverse(path);
        return path;
    }

    /** Brute force distance by repeated relaxation until no value changes. */
    static int[] relax(int n, int[][] edges, int source) {
        int inf = 1_000_000;
        int[] d = new int[n];
        Arrays.fill(d, inf);
        d[source] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                if (d[e[0]] + 1 < d[e[1]]) { d[e[1]] = d[e[0]] + 1; changed = true; }
                if (d[e[1]] + 1 < d[e[0]]) { d[e[0]] = d[e[1]] + 1; changed = true; }
            }
        }
        return d;
    }

    public static void main(String[] args) {
        // Example 1: the first discoverer of vertex 3 is vertex 1, so the path avoids vertex 2.
        List<Integer> r1 = shortestPath(6, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}, {4, 5}}, 0, 5);
        if (!r1.equals(List.of(0, 1, 3, 4, 5))) throw new AssertionError("ex1 " + r1);
        // Example 2: the direct edge from 0 to 3 gives a two-edge path.
        List<Integer> r2 = shortestPath(5, new int[][] {{0, 3}, {0, 1}, {1, 2}, {2, 3}, {3, 4}}, 0, 4);
        if (!r2.equals(List.of(0, 3, 4))) throw new AssertionError("ex2 " + r2);
        // The source as target gives the one-vertex path, and an unreachable target gives an empty list.
        if (!shortestPath(3, new int[][] {{0, 1}}, 1, 1).equals(List.of(1))) throw new AssertionError("same vertex");
        if (!shortestPath(3, new int[][] {{0, 1}}, 0, 2).isEmpty()) throw new AssertionError("unreachable");
        // Random graphs: the result must be a real path of the minimum length.
        Random rnd = new Random(2208);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> es = new ArrayList<>();
            boolean[][] has = new boolean[n][n];
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(3) == 0) { es.add(new int[] {a, b}); has[a][b] = has[b][a] = true; }
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            int s = rnd.nextInt(n), tg = rnd.nextInt(n);
            int want = relax(n, arr, s)[tg];
            List<Integer> p = shortestPath(n, arr, s, tg);
            if (want >= 1_000_000) { if (!p.isEmpty()) throw new AssertionError("should be empty " + t); continue; }
            // A shortest path has want + 1 vertices, starts at s, ends at tg and uses existing edges only.
            if (p.size() != want + 1 || p.get(0) != s || p.get(p.size() - 1) != tg) throw new AssertionError("shape " + t);
            for (int i = 0; i + 1 < p.size(); i++) if (!has[p.get(i)][p.get(i + 1)]) throw new AssertionError("edge " + t);
        }
    }
}
```

#### Solution: [Boundary] Source Equals Target And Unreachable Target (Author exercise)
<!-- id: gt-source-target-boundary -->

**Approach.**
The method answers the equal case before it builds any structure, because the minimum edge count from a vertex to itself is 0. For other targets it runs the search level by level. At the start of each round, `queue.size()` is the number of vertices of the current level, and the round expands exactly that many vertices. The counter `steps` increases by one after each round, so it equals the distance of the vertices discovered in the next round.

The method returns `steps` as soon as it discovers the target. When the queue becomes empty without finding the target, the method returns -1, the failure value of the exercise. The invariant is that at the start of a round, the queue holds exactly the vertices at distance `steps` that are not expanded yet. The final value -1 is correct, because an empty queue means the whole component of the source was visited.

**Complexity.**
- **Time** is O(V + E), because each vertex enters the queue once and each adjacency entry is read once.
- **Space** is O(V + E) for the adjacency list, plus O(V) for `visited` and the queue.

```java run
import java.util.*;

public final class SourceTargetBoundary {
    /**
     * Returns the minimum edge count between source and target, 0 if equal, or -1 if unreachable.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: at the start of a round the queue holds the unexpanded vertices at distance steps.
     */
    static int hops(int n, int[][] edges, int source, int target) {
        // Equal endpoints need no search at all.
        if (source == target) return 0;
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        visited[source] = true;
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(source);
        int steps = 0;
        // One round per level; the loop ends when no vertex is left to expand.
        while (!queue.isEmpty()) {
            // The count is fixed before the round, so vertices added during the round wait for the next one.
            int width = queue.size();
            steps++;
            for (int i = 0; i < width; i++) {
                int current = queue.poll();
                for (int next : adj.get(current)) {
                    if (visited[next]) continue;
                    // The first discovery of the target happens at distance steps.
                    if (next == target) return steps;
                    visited[next] = true;
                    queue.add(next);
                }
            }
        }
        // The queue emptied without discovering the target.
        return -1;
    }

    /** Brute force: the minimum length over every simple path found by exhaustive depth-first search. */
    static int shortestByDfs(int n, boolean[][] has, int cur, int target, boolean[] onPath) {
        if (cur == target) return 0;
        onPath[cur] = true;
        int best = -1;
        for (int v = 0; v < n; v++) {
            if (!has[cur][v] || onPath[v]) continue;
            int r = shortestByDfs(n, has, v, target, onPath);
            if (r >= 0 && (best < 0 || r + 1 < best)) best = r + 1;
        }
        onPath[cur] = false;
        return best;
    }

    public static void main(String[] args) {
        // Example 1: equal endpoints on an isolated vertex give 0.
        if (hops(3, new int[][] {{0, 1}}, 2, 2) != 0) throw new AssertionError("ex1");
        // Example 2: the target lives in another component.
        if (hops(5, new int[][] {{0, 1}, {1, 2}, {3, 4}}, 0, 4) != -1) throw new AssertionError("ex2");
        // A direct edge gives 1, and a path of three edges gives 3.
        if (hops(2, new int[][] {{0, 1}}, 0, 1) != 1) throw new AssertionError("direct");
        if (hops(4, new int[][] {{0, 1}, {1, 2}, {2, 3}}, 0, 3) != 3) throw new AssertionError("chain");
        // Random graphs must match the exhaustive minimum over all simple paths.
        Random rnd = new Random(2209);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(7);
            boolean[][] has = new boolean[n][n];
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(3) == 0) { has[a][b] = has[b][a] = true; es.add(new int[] {a, b}); }
            Collections.shuffle(es, rnd);
            int s = rnd.nextInt(n), tg = rnd.nextInt(n);
            if (hops(n, es.toArray(new int[0][]), s, tg) != shortestByDfs(n, has, s, tg, new boolean[n])) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Shortest Path in Binary Matrix (LeetCode 1091)
<!-- id: gt-shortest-path-binary-matrix -->

**Approach.**
The vertices are the free cells, and the neighbors of a cell are the up to eight cells around it that lie inside the grid and are free. No adjacency list is built, because the offsets `dr` and `dc` generate the neighbors on demand. The method returns -1 at once when either endpoint is blocked. It then runs the same queue search as the graph version, with each cell encoded as `row * n + col` in the queue.

The array `length` stores the number of cells on the best path to each cell, so the start cell gets 1, and a neighbor gets `length[current] + 1` at its first discovery. A value of 0 in `length` means that the cell is not visited yet. The invariant is the same as in the lesson: cells leave the queue in nondecreasing length, so the first discovery is shortest. The length counts cells, which is one more than the number of edges.

**Complexity.**
- **Time** is O(n^2), because each of the `n * n` cells enters the queue at most once and checks eight neighbors.
- **Space** is O(n^2) for the `length` array and the queue.

```java run
import java.util.*;

public final class BinaryMatrixPath {
    /**
     * Returns the number of cells on the shortest clear path from the top-left to the bottom-right cell, or -1.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: cells leave the queue in nondecreasing path length.
     */
    static int shortestClearPath(int[][] grid) {
        int n = grid.length;
        // A blocked endpoint makes every path impossible.
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        // Zero means not visited, so a visited cell always stores a length of at least 1.
        int[][] length = new int[n][n];
        length[0][0] = 1;
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(0);
        // Each cell enters the queue once, which bounds the loop by n * n iterations.
        while (!queue.isEmpty()) {
            int code = queue.poll();
            int r = code / n, c = code % n;
            // The bottom-right cell is final when it leaves the queue.
            if (r == n - 1 && c == n - 1) return length[r][c];
            // Eight offsets from (-1,-1) to (1,1); the offset (0,0) is skipped by the visited test.
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr, nc = c + dc;
                    // Reject cells outside the grid, blocked cells and cells already visited.
                    if (nr < 0 || nc < 0 || nr >= n || nc >= n || grid[nr][nc] == 1 || length[nr][nc] != 0) continue;
                    // The first discovery gives the shortest length, and the encoded cell index goes to the queue.
                    length[nr][nc] = length[r][c] + 1;
                    queue.add(nr * n + nc);
                }
            }
        }
        // The queue emptied without reaching the corner.
        return -1;
    }

    /** Brute force: relax every free cell from its eight neighbors until nothing changes. */
    static int relaxAll(int[][] grid) {
        int n = grid.length, inf = 1_000_000;
        if (grid[0][0] == 1 || grid[n - 1][n - 1] == 1) return -1;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        d[0][0] = 1;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) {
                if (grid[r][c] == 1) continue;
                for (int dr = -1; dr <= 1; dr++) for (int dc = -1; dc <= 1; dc++) {
                    int pr = r + dr, pc = c + dc;
                    if (pr < 0 || pc < 0 || pr >= n || pc >= n || grid[pr][pc] == 1) continue;
                    if (d[pr][pc] + 1 < d[r][c]) { d[r][c] = d[pr][pc] + 1; changed = true; }
                }
            }
        }
        return d[n - 1][n - 1] >= inf ? -1 : d[n - 1][n - 1];
    }

    public static void main(String[] args) {
        // Example 1: the diagonal 0,0 then 1,1 then 2,2 has three cells.
        if (shortestClearPath(new int[][] {{0, 1, 0}, {1, 0, 1}, {0, 0, 0}}) != 3) throw new AssertionError("ex1");
        // Example 2: the path must bend, so it needs four cells.
        if (shortestClearPath(new int[][] {{0, 0, 0}, {1, 1, 0}, {1, 1, 0}}) != 4) throw new AssertionError("ex2");
        // A single free cell has length 1, and a blocked endpoint gives -1.
        if (shortestClearPath(new int[][] {{0}}) != 1) throw new AssertionError("single cell");
        if (shortestClearPath(new int[][] {{1}}) != -1) throw new AssertionError("blocked single cell");
        // A wall of blocked cells separates the corners.
        if (shortestClearPath(new int[][] {{0, 0, 0}, {1, 1, 1}, {1, 1, 0}}) != -1) throw new AssertionError("wall");
        // Random grids must match repeated relaxation.
        Random rnd = new Random(2210);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] g = new int[n][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(3) == 0 ? 1 : 0;
            if (shortestClearPath(g) != relaxAll(g)) throw new AssertionError("random " + t);
        }
    }
}
```
