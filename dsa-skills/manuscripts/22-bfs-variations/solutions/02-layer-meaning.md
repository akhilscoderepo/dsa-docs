<!-- solutions-for: 02-layer-meaning -->
### Layer Meaning

#### Solution: [Build] Label BFS Layers (Author exercise)
<!-- id: bv-layer-lists -->

**Approach.** Build adjacency lists once, mark the source seen, and run the outer loop while the queue is non-empty. Each pass copies `queue.size()` into a local variable, removes that many vertices into one list, sorts it, and appends it as the next row, while newly found neighbors are marked at the moment they are queued. The oracle shares no code with this: it starts every distance at infinity, relaxes every edge in both directions until a full sweep changes nothing, and then groups vertices by distance. The test compares both on random graphs with repeated edges and isolated vertices, checks that the edge array is untouched, and demonstrates the two Java claims from the lesson: a loop bounded by the live `size()` ends in the wrong place and mixes layers, and two `Integer` objects holding 1000 are not `==`.

**Complexity.** Every vertex leaves the queue once and every edge is read from both endpoints, so the running time is O(V + E). Storage beyond the input is O(V + E) for the adjacency lists, the seen flags, the queue and the output rows.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class LayerListsSolution {
    static List<List<Integer>> adjacency(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        return adj;
    }

    static int[][] solve(int n, int[][] edges, int source) {
        List<List<Integer>> adj = adjacency(n, edges);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        seen[source] = true;
        line.add(source);
        List<int[]> rows = new ArrayList<>();
        while (!line.isEmpty()) {
            int size = line.size();
            int[] row = new int[size];
            for (int i = 0; i < size; i++) {
                int v = line.poll();
                row[i] = v;
                for (int next : adj.get(v)) {
                    if (seen[next]) continue;
                    seen[next] = true;
                    line.add(next);
                }
            }
            Arrays.sort(row);
            rows.add(row);
        }
        return rows.toArray(new int[0][]);
    }

    static int[][] buggy(int n, int[][] edges, int source) {
        List<List<Integer>> adj = adjacency(n, edges);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        seen[source] = true;
        line.add(source);
        List<int[]> rows = new ArrayList<>();
        while (!line.isEmpty()) {
            List<Integer> row = new ArrayList<>();
            for (int i = 0; i < line.size(); i++) {
                int v = line.poll();
                row.add(v);
                for (int next : adj.get(v)) {
                    if (seen[next]) continue;
                    seen[next] = true;
                    line.add(next);
                }
            }
            int[] r = row.stream().mapToInt(Integer::intValue).sorted().toArray();
            rows.add(r);
        }
        return rows.toArray(new int[0][]);
    }

    static int[][] oracle(int n, int[][] edges, int source) {
        int inf = Integer.MAX_VALUE / 2;
        int[] dist = new int[n];
        Arrays.fill(dist, inf);
        dist[source] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int[] e : edges) {
                if (dist[e[0]] + 1 < dist[e[1]]) { dist[e[1]] = dist[e[0]] + 1; moved = true; }
                if (dist[e[1]] + 1 < dist[e[0]]) { dist[e[0]] = dist[e[1]] + 1; moved = true; }
            }
        }
        int top = -1;
        for (int d : dist) if (d < inf) top = Math.max(top, d);
        int[][] rows = new int[top + 1][];
        for (int k = 0; k <= top; k++) {
            final int kk = k;
            rows[k] = java.util.stream.IntStream.range(0, n).filter(v -> dist[v] == kk).toArray();
        }
        return rows;
    }

    public static void main(String[] args) throws Exception {
        int[][] e1 = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}, {5, 6}};
        if (!Arrays.deepEquals(solve(7, e1, 0), new int[][]{{0}, {1, 2}, {3}, {4}})) throw new AssertionError("example 1");
        int[][] e2 = {{0, 1}, {1, 2}, {2, 0}, {2, 3}, {3, 4}};
        if (!Arrays.deepEquals(solve(6, e2, 3), new int[][]{{3}, {2, 4}, {0, 1}})) throw new AssertionError("example 2");
        if (!Arrays.deepEquals(solve(1, new int[0][], 0), new int[][]{{0}})) throw new AssertionError("single vertex");

        int[][] path = {{0, 1}, {1, 2}, {2, 3}, {3, 4}};
        if (!Arrays.deepEquals(solve(5, path, 0), new int[][]{{0}, {1}, {2}, {3}, {4}})) throw new AssertionError("path");
        int[][] star = {{0, 1}, {0, 2}, {0, 3}, {0, 4}};
        if (!Arrays.deepEquals(solve(5, star, 0), new int[][]{{0}, {1, 2, 3, 4}})) throw new AssertionError("star");
        if (Arrays.deepEquals(buggy(5, star, 0), solve(5, star, 0))) throw new AssertionError("live size should mix layers");

        ArrayDeque<Integer> probe = new ArrayDeque<>();
        probe.add(1);
        int captured = probe.size();
        probe.add(2);
        if (captured != 1 || probe.size() != 2) throw new AssertionError("size is a live count");
        Integer big1 = 1000, big2 = 1000;
        if (big1 == big2) throw new AssertionError("boxed 1000 should not be identical");
        if (!big1.equals(big2)) throw new AssertionError("equals compares values");

        Random rnd = new Random(22201);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            int m = n == 1 ? 0 : rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b) b = (a + 1) % n;
                edges[i] = new int[]{a, b};
            }
            int[][] copy = Arrays.stream(edges).map(int[]::clone).toArray(int[][]::new);
            int source = rnd.nextInt(n);
            if (!Arrays.deepEquals(solve(n, edges, source), oracle(n, edges, source))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(copy, edges)) throw new AssertionError("edges modified " + t);
        }
    }
}
```

#### Solution: [Vary] Stop At First Target Layer (Author exercise)
<!-- id: bv-first-target-layer -->

**Approach.** Mark targets in a boolean table, run the layered traversal, and count targets while draining each layer. When a pass finishes with a positive count, return the pass number and that count, so no later layer is ever read. Returning on the first target met would give a wrong count whenever two targets share a distance, and the test builds that variant and shows it failing on example 1. The oracle computes all distances by repeated edge relaxation, takes the smallest target distance, and counts the targets at it. A counter of removed vertices confirms that the early exit never removes anything beyond the first productive layer.

**Complexity.** Worst-case time is O(V + E), reached when the target layer is the last one or does not exist, and it can stop earlier. Memory is O(V + E) for adjacency, flags and queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FirstTargetLayerSolution {
    static int removed;

    static List<List<Integer>> adjacency(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        return adj;
    }

    static int[] solve(int n, int[][] edges, int source, int[] targets) {
        boolean[] goal = new boolean[n];
        for (int t : targets) goal[t] = true;
        List<List<Integer>> adj = adjacency(n, edges);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        seen[source] = true;
        line.add(source);
        int layer = 0;
        removed = 0;
        while (!line.isEmpty()) {
            int size = line.size();
            int hits = 0;
            for (int i = 0; i < size; i++) {
                int v = line.poll();
                removed++;
                if (goal[v]) hits++;
                for (int next : adj.get(v)) {
                    if (seen[next]) continue;
                    seen[next] = true;
                    line.add(next);
                }
            }
            if (hits > 0) return new int[]{layer, hits};
            layer++;
        }
        return new int[]{-1, 0};
    }

    static int[] firstHitOnly(int n, int[][] edges, int source, int[] targets) {
        boolean[] goal = new boolean[n];
        for (int t : targets) goal[t] = true;
        List<List<Integer>> adj = adjacency(n, edges);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        seen[source] = true;
        line.add(source);
        int layer = 0;
        while (!line.isEmpty()) {
            int size = line.size();
            for (int i = 0; i < size; i++) {
                int v = line.poll();
                if (goal[v]) return new int[]{layer, 1};
                for (int next : adj.get(v)) {
                    if (seen[next]) continue;
                    seen[next] = true;
                    line.add(next);
                }
            }
            layer++;
        }
        return new int[]{-1, 0};
    }

    static int[] distances(int n, int[][] edges, int source) {
        int inf = Integer.MAX_VALUE / 2;
        int[] dist = new int[n];
        Arrays.fill(dist, inf);
        dist[source] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int[] e : edges) {
                if (dist[e[0]] + 1 < dist[e[1]]) { dist[e[1]] = dist[e[0]] + 1; moved = true; }
                if (dist[e[1]] + 1 < dist[e[0]]) { dist[e[0]] = dist[e[1]] + 1; moved = true; }
            }
        }
        return dist;
    }

    static int[] oracle(int n, int[][] edges, int source, int[] targets) {
        int[] dist = distances(n, edges, source);
        int best = Integer.MAX_VALUE / 2;
        for (int t : targets) best = Math.min(best, dist[t]);
        if (best >= Integer.MAX_VALUE / 2) return new int[]{-1, 0};
        int count = 0;
        for (int t : targets) if (dist[t] == best) count++;
        return new int[]{best, count};
    }

    public static void main(String[] args) throws Exception {
        int[][] e = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}, {4, 5}, {2, 6}};
        if (!Arrays.equals(solve(7, e, 0, new int[]{3, 6, 5}), new int[]{2, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(7, e, 0, new int[]{0, 4}), new int[]{0, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(7, new int[][]{{0, 1}}, 0, new int[]{5}), new int[]{-1, 0})) throw new AssertionError("unreachable");
        if (Arrays.equals(firstHitOnly(7, e, 0, new int[]{3, 6, 5}), new int[]{2, 2})) throw new AssertionError("first-hit variant should miscount");
        solve(7, e, 0, new int[]{3, 6, 5});
        if (removed != 5) throw new AssertionError("only layers 0 to 2 may be read, removed " + removed);

        Random rnd = new Random(22202);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            int m = n == 1 ? 0 : rnd.nextInt(13);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b) b = (a + 1) % n;
                edges[i] = new int[]{a, b};
            }
            List<Integer> pool = new ArrayList<>();
            for (int v = 0; v < n; v++) pool.add(v);
            java.util.Collections.shuffle(pool, rnd);
            int k = 1 + rnd.nextInt(n);
            int[] targets = new int[k];
            for (int i = 0; i < k; i++) targets[i] = pool.get(i);
            int source = rnd.nextInt(n);
            if (!Arrays.equals(solve(n, edges, source, targets), oracle(n, edges, source, targets))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Initially Complete State (Author exercise)
<!-- id: bv-already-complete -->

**Approach.** Mark every entry of `lit` in a boolean table and queue each vertex only the first time it appears, which also yields the number of distinct lit vertices. If that number equals n, return 0 before any pass runs. Otherwise run layered passes and advance the clock only when a pass queued at least one new vertex, so the unproductive last pass is not counted. At the end, return the clock if every vertex was lit and -1 if not. The oracle gives each lit vertex time 0, relaxes both ends of every edge to a fixpoint, and returns the largest finite time, or -1 for any infinite one. Tests show that comparing `lit.length` with n is wrong on repeated entries and that a clock advanced after the empty final pass is one too large.

**Complexity.** Linear in the size of the input, O(V + E + L) where L is the length of `lit`, because each vertex is queued once and each edge is read twice. The table, adjacency and queue use O(V + E) memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class AlreadyCompleteSolution {
    static List<List<Integer>> adjacency(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        return adj;
    }

    static int solve(int n, int[][] edges, int[] lit) {
        List<List<Integer>> adj = adjacency(n, edges);
        boolean[] on = new boolean[n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        int count = 0;
        for (int v : lit) {
            if (on[v]) continue;
            on[v] = true;
            count++;
            line.add(v);
        }
        if (count == n) return 0;
        int minutes = 0;
        while (!line.isEmpty()) {
            int size = line.size();
            boolean grew = false;
            for (int i = 0; i < size; i++) {
                int v = line.poll();
                for (int next : adj.get(v)) {
                    if (on[next]) continue;
                    on[next] = true;
                    count++;
                    grew = true;
                    line.add(next);
                }
            }
            if (grew) minutes++;
        }
        return count == n ? minutes : -1;
    }

    static int naiveLengthCheck(int n, int[][] edges, int[] lit) {
        if (lit.length == n) return 0;
        return solve(n, edges, lit);
    }

    static int overcounting(int n, int[][] edges, int[] lit) {
        List<List<Integer>> adj = adjacency(n, edges);
        boolean[] on = new boolean[n];
        ArrayDeque<Integer> line = new ArrayDeque<>();
        int count = 0;
        for (int v : lit) {
            if (on[v]) continue;
            on[v] = true;
            count++;
            line.add(v);
        }
        int minutes = 0;
        while (!line.isEmpty()) {
            int size = line.size();
            for (int i = 0; i < size; i++) {
                int v = line.poll();
                for (int next : adj.get(v)) {
                    if (on[next]) continue;
                    on[next] = true;
                    count++;
                    line.add(next);
                }
            }
            minutes++;
        }
        return count == n ? minutes : -1;
    }

    static int oracle(int n, int[][] edges, int[] lit) {
        int inf = Integer.MAX_VALUE / 2;
        int[] t = new int[n];
        Arrays.fill(t, inf);
        for (int v : lit) t[v] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int[] e : edges) {
                if (t[e[0]] + 1 < t[e[1]]) { t[e[1]] = t[e[0]] + 1; moved = true; }
                if (t[e[1]] + 1 < t[e[0]]) { t[e[0]] = t[e[1]] + 1; moved = true; }
            }
        }
        int worst = 0;
        for (int x : t) {
            if (x >= inf) return -1;
            worst = Math.max(worst, x);
        }
        return worst;
    }

    public static void main(String[] args) throws Exception {
        int[][] path = {{0, 1}, {1, 2}, {2, 3}};
        if (solve(4, path, new int[]{3, 2, 1, 0}) != 0) throw new AssertionError("example 1");
        if (solve(4, path, new int[]{0, 3, 0, 3}) != 1) throw new AssertionError("example 2");
        if (solve(4, path, new int[]{0}) != 3) throw new AssertionError("single lit end");
        if (solve(3, new int[0][], new int[0]) != -1) throw new AssertionError("nothing lit");
        if (solve(1, new int[0][], new int[]{0}) != 0) throw new AssertionError("one lit vertex");
        if (naiveLengthCheck(4, path, new int[]{0, 3, 0, 3}) != 0) throw new AssertionError("length check should be fooled");
        if (overcounting(4, path, new int[]{3, 2, 1, 0}) != 1) throw new AssertionError("empty pass is counted");
        if (overcounting(4, path, new int[]{0, 3, 0, 3}) != 2) throw new AssertionError("overcount by one");

        Random rnd = new Random(22203);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = n == 1 ? 0 : rnd.nextInt(12);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b) b = (a + 1) % n;
                edges[i] = new int[]{a, b};
            }
            int len = rnd.nextInt(2 * n + 1);
            int[] lit = new int[len];
            for (int i = 0; i < len; i++) lit[i] = rnd.nextInt(n);
            int[] copy = lit.clone();
            if (solve(n, edges, lit) != oracle(n, edges, lit)) throw new AssertionError("random " + t);
            if (!Arrays.equals(copy, lit)) throw new AssertionError("lit modified " + t);
        }
    }
}
```

#### Solution: [Recognize] Rotting Oranges (LeetCode 994)
<!-- id: bv-rotting-final-minute -->

**Approach.** Queue every initially rotten cell and run layered passes over a private copy of the grid, spoiling fresh neighbors at the moment they are queued. Each pass counts how many oranges it spoiled. Only when that count is positive does the pass advance the minutes and record the count as the latest productive layer, so the answer pair is the minutes and the size of the last such layer, and `[0, 0]` falls out when nothing ever rots. The oracle gives rotten cells time 0 and fresh cells infinity, lowers each cell to one more than its best neighbor until nothing changes, and reads the pair off the largest finite time. The test also confirms the input grid is untouched and that a clock per removed orange would report a larger number on example 1.

**Complexity.** The scan is O(R * C), since every cell enters the queue at most once and looks at four neighbors. The queue and grid copy need O(R * C) space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class RottingFinalMinuteSolution {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    static int[] solve(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] state = new int[rows][];
        for (int r = 0; r < rows; r++) state[r] = grid[r].clone();
        ArrayDeque<Integer> line = new ArrayDeque<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (state[r][c] == 2) line.add(r * cols + c);
        int minutes = 0, lastBatch = 0;
        while (!line.isEmpty()) {
            int size = line.size();
            int spoiled = 0;
            for (int i = 0; i < size; i++) {
                int code = line.poll();
                int r = code / cols, c = code % cols;
                for (int d = 0; d < 4; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    if (state[nr][nc] != 1) continue;
                    state[nr][nc] = 2;
                    spoiled++;
                    line.add(nr * cols + nc);
                }
            }
            if (spoiled > 0) { minutes++; lastBatch = spoiled; }
        }
        return new int[]{minutes, lastBatch};
    }

    static int perOrangeClock(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] state = new int[rows][];
        for (int r = 0; r < rows; r++) state[r] = grid[r].clone();
        ArrayDeque<Integer> line = new ArrayDeque<>();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (state[r][c] == 2) line.add(r * cols + c);
        int clock = 0;
        while (!line.isEmpty()) {
            int code = line.poll();
            clock++;
            int r = code / cols, c = code % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || state[nr][nc] != 1) continue;
                state[nr][nc] = 2;
                line.add(nr * cols + nc);
            }
        }
        return clock;
    }

    static int[] oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length, inf = Integer.MAX_VALUE / 2;
        int[][] t = new int[rows][cols];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                t[r][c] = grid[r][c] == 2 ? 0 : inf;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = rows - 1; r >= 0; r--) {
                for (int c = cols - 1; c >= 0; c--) {
                    if (grid[r][c] != 1) continue;
                    for (int d = 0; d < 4; d++) {
                        int nr = r + DR[d], nc = c + DC[d];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == 0) continue;
                        if (t[nr][nc] + 1 < t[r][c]) { t[r][c] = t[nr][nc] + 1; moved = true; }
                    }
                }
            }
        }
        int worst = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] != 0 && t[r][c] < inf) worst = Math.max(worst, t[r][c]);
        int count = 0;
        if (worst > 0)
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++)
                    if (grid[r][c] == 1 && t[r][c] == worst) count++;
        return new int[]{worst, count};
    }

    public static void main(String[] args) throws Exception {
        int[][] a = {{1, 1, 0, 1}, {1, 2, 1, 1}, {0, 1, 0, 2}};
        if (!Arrays.equals(solve(a), new int[]{2, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[][]{{2, 0, 1}}), new int[]{0, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][]{{0}}), new int[]{0, 0})) throw new AssertionError("empty crate");
        if (!Arrays.equals(solve(new int[][]{{2, 2}}), new int[]{0, 0})) throw new AssertionError("all rotten");
        if (!Arrays.equals(solve(new int[][]{{2, 1, 1}}), new int[]{2, 1})) throw new AssertionError("row");
        if (perOrangeClock(a) <= 2) throw new AssertionError("per-orange clock overcounts");

        Random rnd = new Random(22204);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(10) < 2 ? 0 : (rnd.nextInt(10) < 2 ? 2 : 1);
            int[][] copy = new int[rows][];
            for (int r = 0; r < rows; r++) copy[r] = g[r].clone();
            if (!Arrays.equals(solve(g), oracle(g))) throw new AssertionError("random " + t + " " + Arrays.deepToString(g));
            if (!Arrays.deepEquals(copy, g)) throw new AssertionError("grid modified " + t);
        }
    }
}
```
