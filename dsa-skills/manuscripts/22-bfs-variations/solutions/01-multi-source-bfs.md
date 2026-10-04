<!-- solutions-for: 22-bfs-variations -->
### Multi-Source BFS

#### Solution: [Build] Nearest Source Distances (Author exercise)
<!-- id: bv-nearest-source-distances -->

**Approach.** Turn the edge list into adjacency rows, fill the distance table with -1, and put every marked vertex into one queue at distance 0 before the first removal. A vertex that is already labelled is never queued again, so repeated entries would also be harmless. Removal order then gives distances in non-decreasing order, and the first label a vertex receives is its smallest. The oracle uses no queue at all: it starts every marked vertex at 0 and every other vertex at infinity, then relaxes every edge in both directions over and over until a full round changes nothing. The assertions compare the two on random graphs and also check four claims from the lesson: a new `int[]` is full of zeros, queue removal order never decreases in distance, skipping the table check at seeding would queue a repeated station twice, and running one search per station gives the same table while doing several times more vertex visits.

**Complexity.** The run reads each vertex once when it leaves the queue and each edge twice, so the time is O(V + E), with the source list adding O(S). Memory is O(V + E) for the adjacency rows plus O(V) for the distances and queue.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class NearestSourceDistancesSolution {
    static int[][] rows(int n, int[][] edges) {
        int[] deg = new int[n];
        for (int[] e : edges) { deg[e[0]]++; deg[e[1]]++; }
        int[][] adj = new int[n][];
        for (int v = 0; v < n; v++) adj[v] = new int[deg[v]];
        int[] fill = new int[n];
        for (int[] e : edges) {
            adj[e[0]][fill[e[0]]++] = e[1];
            adj[e[1]][fill[e[1]]++] = e[0];
        }
        return adj;
    }

    static int lastPolls;
    static boolean orderNeverDecreased;

    static int[] solve(int n, int[][] edges, int[] sources) {
        int[][] adj = rows(n, edges);
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        for (int s : sources) {
            if (dist[s] != -1) continue;
            dist[s] = 0;
            frontier.add(s);
        }
        int previous = 0;
        lastPolls = 0;
        orderNeverDecreased = true;
        while (!frontier.isEmpty()) {
            int v = frontier.poll();
            lastPolls++;
            if (dist[v] < previous) orderNeverDecreased = false;
            previous = dist[v];
            for (int w : adj[v]) {
                if (dist[w] != -1) continue;
                dist[w] = dist[v] + 1;
                frontier.add(w);
            }
        }
        return dist;
    }

    static int[] oracle(int n, int[][] edges, int[] sources) {
        int inf = Integer.MAX_VALUE / 2;
        int[] d = new int[n];
        Arrays.fill(d, inf);
        for (int s : sources) d[s] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int[] e : edges) {
                if (d[e[0]] + 1 < d[e[1]]) { d[e[1]] = d[e[0]] + 1; moved = true; }
                if (d[e[1]] + 1 < d[e[0]]) { d[e[0]] = d[e[1]] + 1; moved = true; }
            }
        }
        for (int v = 0; v < n; v++) if (d[v] >= inf) d[v] = -1;
        return d;
    }

    static int seedingWithoutCheck(int n, int[] sources) {
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> q = new ArrayDeque<>();
        for (int s : sources) { dist[s] = 0; q.add(s); }
        return q.size();
    }

    static int visitsOfSeparateRuns(int n, int[][] edges, int[] sources, int[] bestOut) {
        int[][] adj = rows(n, edges);
        int visits = 0;
        Arrays.fill(bestOut, -1);
        for (int s : sources) {
            int[] dist = new int[n];
            Arrays.fill(dist, -1);
            ArrayDeque<Integer> q = new ArrayDeque<>();
            dist[s] = 0;
            q.add(s);
            while (!q.isEmpty()) {
                int v = q.poll();
                visits++;
                for (int w : adj[v]) if (dist[w] == -1) { dist[w] = dist[v] + 1; q.add(w); }
            }
            for (int v = 0; v < n; v++)
                if (dist[v] != -1 && (bestOut[v] == -1 || dist[v] < bestOut[v])) bestOut[v] = dist[v];
        }
        return visits;
    }

    public static void main(String[] args) {
        int[] fresh = new int[4];
        for (int x : fresh) if (x != 0) throw new AssertionError("new int[] must hold zeros");
        int[][] path = {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 5}, {5, 6}};
        if (!Arrays.toString(solve(7, path, new int[] {0, 6})).equals("[0, 1, 2, 3, 2, 1, 0]"))
            throw new AssertionError("example 1");
        if (!Arrays.toString(solve(6, new int[][] {{0, 1}, {1, 2}, {3, 4}}, new int[] {2}))
                .equals("[2, 1, 0, -1, -1, -1]"))
            throw new AssertionError("example 2");
        if (seedingWithoutCheck(3, new int[] {1, 1, 1}) != 3)
            throw new AssertionError("an unchecked repeated station is queued repeatedly");
        int[] twice = solve(3, new int[][] {{0, 1}, {1, 2}}, new int[] {1, 1, 1});
        if (lastPolls != 3 || !Arrays.toString(twice).equals("[1, 0, 1]"))
            throw new AssertionError("checked seeding must queue the station once");
        int m = 60;
        int[][] longPath = new int[m - 1][];
        int[] every = new int[m / 2];
        for (int i = 0; i < m - 1; i++) longPath[i] = new int[] {i, i + 1};
        for (int i = 0; i < m / 2; i++) every[i] = 2 * i;
        int[] best = new int[m];
        int separate = visitsOfSeparateRuns(m, longPath, every, best);
        int[] together = solve(m, longPath, every);
        if (!Arrays.equals(best, together)) throw new AssertionError("separate runs must agree");
        if (separate < 10 * lastPolls) throw new AssertionError("separate runs should repeat work " + separate + " vs " + lastPolls);
        Random rnd = new Random(22101);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int e = n > 1 ? rnd.nextInt(2 * n) : 0;
            int[][] edges = new int[e][];
            for (int i = 0; i < e; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b) b = (a + 1) % n;
                edges[i] = new int[] {a, b};
            }
            if (n == 1) edges = new int[0][];
            int k = 1 + rnd.nextInt(n);
            int[] pool = new int[n];
            for (int i = 0; i < n; i++) pool[i] = i;
            for (int i = n - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int x = pool[i]; pool[i] = pool[j]; pool[j] = x; }
            int[] src = Arrays.copyOf(pool, k);
            int[] want = oracle(n, edges, src);
            int[] got = solve(n, edges, src);
            if (!Arrays.equals(got, want)) throw new AssertionError("random " + t);
            if (!orderNeverDecreased) throw new AssertionError("queue order " + t);
            int[] b2 = new int[n];
            visitsOfSeparateRuns(n, edges, src, b2);
            if (!Arrays.equals(b2, want)) throw new AssertionError("separate " + t);
        }
    }
}
```

#### Solution: [Vary] 01 Matrix (LeetCode 542)
<!-- id: bv-zero-one-matrix -->

**Approach.** Scan the grid once and queue every cell holding 0 with answer 0, leaving all other answers at -1 in a freshly allocated result. The search then walks outward through up, down, left and right neighbors, giving each unlabelled cell its parent's answer plus one. Cells holding 1 are what the search is for, while the zeros are the queue's starting layer. The oracle keeps an infinity in every 1-cell and lowers any cell to a neighbor plus one, sweeping the grid in alternating directions until nothing changes. The checks cover the random comparison, the claim that the input is left untouched, and a false friend: a search seeded from only the first zero it finds disagrees with the oracle on some grids.

**Complexity.** Every cell is queued once and compares four neighbors, so the work is proportional to the number of cells, O(R * C). The result and the queue each hold at most R * C entries, which is the same bound for memory.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ZeroOneMatrixSolution {
    private static final int[] STEP_R = {1, -1, 0, 0};
    private static final int[] STEP_C = {0, 0, 1, -1};

    static int[][] solve(int[][] mat, boolean allZeros) {
        int rows = mat.length, cols = mat[0].length;
        int[][] out = new int[rows][cols];
        for (int[] line : out) Arrays.fill(line, -1);
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        outer:
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (mat[r][c] != 0) continue;
                out[r][c] = 0;
                queue.add(new int[] {r, c});
                if (!allZeros) break outer;
            }
        }
        while (!queue.isEmpty()) {
            int[] cell = queue.poll();
            for (int k = 0; k < 4; k++) {
                int nr = cell[0] + STEP_R[k], nc = cell[1] + STEP_C[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (out[nr][nc] != -1) continue;
                out[nr][nc] = out[cell[0]][cell[1]] + 1;
                queue.add(new int[] {nr, nc});
            }
        }
        return out;
    }

    static int[][] oracle(int[][] mat) {
        int rows = mat.length, cols = mat[0].length, inf = 1 << 20;
        int[][] d = new int[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) d[r][c] = mat[r][c] == 0 ? 0 : inf;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = rows - 1; r >= 0; r--) {
                for (int c = cols - 1; c >= 0; c--) {
                    for (int k = 0; k < 4; k++) {
                        int nr = r + STEP_R[k], nc = c + STEP_C[k];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                        if (d[nr][nc] + 1 < d[r][c]) { d[r][c] = d[nr][nc] + 1; moved = true; }
                    }
                }
            }
        }
        return d;
    }

    public static void main(String[] args) {
        int[][] one = {{0, 0, 0}, {0, 1, 0}, {1, 1, 1}};
        if (!Arrays.deepToString(solve(one, true)).equals("[[0, 0, 0], [0, 1, 0], [1, 2, 1]]"))
            throw new AssertionError("example 1");
        int[][] two = {{1, 1, 1}, {1, 1, 1}, {1, 1, 0}};
        if (!Arrays.deepToString(solve(two, true)).equals("[[4, 3, 2], [3, 2, 1], [2, 1, 0]]"))
            throw new AssertionError("example 2");
        int[][] keep = {{0, 1}, {1, 1}};
        int[][] result = solve(keep, true);
        if (result == keep || !Arrays.deepToString(keep).equals("[[0, 1], [1, 1]]"))
            throw new AssertionError("input must stay untouched and a new matrix returned");
        int[][] twoZeros = {{0, 1, 1, 1, 0}};
        if (Arrays.deepEquals(solve(twoZeros, false), oracle(twoZeros)))
            throw new AssertionError("seeding from one zero must be wrong here");
        Random rnd = new Random(22102);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] mat = new int[rows][cols];
            for (int[] line : mat) for (int c = 0; c < cols; c++) line[c] = rnd.nextInt(3) == 0 ? 0 : 1;
            mat[rnd.nextInt(rows)][rnd.nextInt(cols)] = 0;
            int[][] before = new int[rows][];
            for (int r = 0; r < rows; r++) before[r] = mat[r].clone();
            if (!Arrays.deepEquals(solve(mat, true), oracle(mat))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(before, mat)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Boundary] No Source Or All Sources (Author exercise)
<!-- id: bv-no-or-all-sources -->

**Approach.** Label vertices exactly as in the Build rung, but keep two extra numbers while draining the queue: how many vertices have been labelled and the largest label handed out. Rounds are never counted. If the labelled count is n, the answer is the largest label, which is 0 when every vertex was a source; otherwise it is -1, and that includes an empty source list because nothing gets labelled at all. A repeated source is skipped by the table check. The oracle runs Floyd-Warshall over all pairs, then takes for each vertex the smallest distance to a source and the largest of those, and it answers -1 if any of them is infinite. The assertions run the random comparison and show that a loop which adds one minute per round, even a round that discovers nothing, is one too large whenever the answer is not -1.

**Complexity.** Labelling costs time linear in vertices plus edges, O(V + E), and walking the source list costs O(S) on top. Only the distance table, the adjacency rows and the queue are stored, so memory is O(V + E).

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class NoSourceOrAllSourcesSolution {
    static int solve(int n, int[][] edges, int[] sources) {
        List<List<Integer>> next = new ArrayList<>();
        for (int v = 0; v < n; v++) next.add(new ArrayList<>());
        for (int[] e : edges) { next.get(e[0]).add(e[1]); next.get(e[1]).add(e[0]); }
        int[] stamp = new int[n];
        java.util.Arrays.fill(stamp, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        int labelled = 0, latest = 0;
        for (int s : sources) {
            if (stamp[s] != -1) continue;
            stamp[s] = 0;
            labelled++;
            line.add(s);
        }
        while (!line.isEmpty()) {
            int v = line.poll();
            latest = Math.max(latest, stamp[v]);
            for (int w : next.get(v)) {
                if (stamp[w] != -1) continue;
                stamp[w] = stamp[v] + 1;
                labelled++;
                line.add(w);
            }
        }
        return labelled == n ? latest : -1;
    }

    static int roundCounter(int n, int[][] edges, int[] sources) {
        boolean[] marked = new boolean[n];
        int count = 0;
        for (int s : sources) if (!marked[s]) { marked[s] = true; count++; }
        int minutes = 0;
        boolean[] current = marked.clone();
        boolean any = count > 0;
        while (any) {
            boolean[] grown = current.clone();
            any = false;
            for (int[] e : edges) {
                if (current[e[0]] && !grown[e[1]]) { grown[e[1]] = true; count++; }
                if (current[e[1]] && !grown[e[0]]) { grown[e[0]] = true; count++; }
            }
            for (int v = 0; v < n; v++) if (grown[v] && !current[v]) any = true;
            // the last pass found nothing new but the counter has not noticed yet
            minutes++;
            current = grown;
        }
        return count == n ? minutes : -1;
    }

    static int oracle(int n, int[][] edges, int[] sources) {
        int inf = 1 << 20;
        int[][] d = new int[n][n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = i == j ? 0 : inf;
        for (int[] e : edges) d[e[0]][e[1]] = d[e[1]][e[0]] = 1;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
        int worst = 0;
        for (int v = 0; v < n; v++) {
            int near = inf;
            for (int s : sources) near = Math.min(near, d[s][v]);
            if (near >= inf) return -1;
            worst = Math.max(worst, near);
        }
        return worst;
    }

    public static void main(String[] args) {
        if (solve(3, new int[][] {{0, 1}, {1, 2}}, new int[] {2, 0, 1, 1}) != 0) throw new AssertionError("example 1");
        if (solve(2, new int[][] {{0, 1}}, new int[0]) != -1) throw new AssertionError("example 2");
        if (solve(3, new int[][] {{0, 1}, {1, 2}}, new int[] {0, 0}) != 2) throw new AssertionError("repeated source");
        if (roundCounter(3, new int[][] {{0, 1}, {1, 2}}, new int[] {0, 1, 2}) != 1)
            throw new AssertionError("a per-round counter wrongly reports 1 when nothing was ever unmarked");
        Random rnd = new Random(22103);
        int seenPositive = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            int e = n > 1 ? rnd.nextInt(2 * n) : 0;
            int[][] edges = new int[e][];
            for (int i = 0; i < e; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a == b) b = (a + 1) % n;
                edges[i] = new int[] {a, b};
            }
            int k = rnd.nextInt(n + 2);
            int[] src = new int[k];
            for (int i = 0; i < k; i++) src[i] = rnd.nextInt(n);
            int want = oracle(n, edges, src);
            if (solve(n, edges, src) != want) throw new AssertionError("random " + t);
            int rounds = roundCounter(n, edges, src);
            if (want != -1 && rounds != want + 1) throw new AssertionError("round counter should be one too large " + t);
            if (want == -1 && rounds != -1) throw new AssertionError("round counter unreachable " + t);
            if (want > 0) seenPositive++;
        }
        if (seenPositive < 100) throw new AssertionError("tests too easy");
    }
}
```

#### Solution: [Recognize] Rotting Oranges (LeetCode 994)
<!-- id: bv-rotting-oranges -->

**Approach.** Every rotten orange is a source, so queue them all and count the fresh ones. Then take the queue one whole batch at a time: record its size first, process exactly that many cells, and turn each fresh neighbor rotten while queuing it. Only a batch that rotted something adds a minute, which is why the loop stops as soon as the fresh count reaches zero instead of running a final empty round. If any fresh orange remains when the queue dries up, the answer is -1. The oracle is a literal simulation: it copies the grid, rots all neighbors of rotten cells at once, repeats until a minute changes nothing, and reports the minutes that did change something. The assertions run random grids, check that the input array is not changed, and show that a variant counting every batch including the final empty one is wrong on a two-cell grid.

**Complexity.** Each cell enters the queue at most once and is looked at from four sides, so the running time is O(R * C). The queue can hold O(R * C) cells in the worst case, and no second grid is stored because a boolean table stands in for the rotting marks.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class RottingOrangesSolution {
    static int solve(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        boolean[] rotten = new boolean[rows * cols];
        ArrayDeque<Integer> batch = new ArrayDeque<>();
        int fresh = 0;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) { rotten[r * cols + c] = true; batch.add(r * cols + c); }
                else if (grid[r][c] == 1) fresh++;
            }
        }
        int minutes = 0;
        int[] dr = {0, 0, 1, -1}, dc = {1, -1, 0, 0};
        while (fresh > 0 && !batch.isEmpty()) {
            for (int left = batch.size(); left > 0; left--) {
                int code = batch.poll();
                for (int k = 0; k < 4; k++) {
                    int nr = code / cols + dr[k], nc = code % cols + dc[k];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    if (grid[nr][nc] != 1 || rotten[nr * cols + nc]) continue;
                    rotten[nr * cols + nc] = true;
                    fresh--;
                    batch.add(nr * cols + nc);
                }
            }
            minutes++;
        }
        return fresh == 0 ? minutes : -1;
    }

    static int everyBatchCounted(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        boolean[] rotten = new boolean[rows * cols];
        ArrayDeque<Integer> batch = new ArrayDeque<>();
        int fresh = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) { rotten[r * cols + c] = true; batch.add(r * cols + c); }
                else if (grid[r][c] == 1) fresh++;
            }
        int minutes = 0;
        int[] dr = {0, 0, 1, -1}, dc = {1, -1, 0, 0};
        while (!batch.isEmpty()) {
            for (int left = batch.size(); left > 0; left--) {
                int code = batch.poll();
                for (int k = 0; k < 4; k++) {
                    int nr = code / cols + dr[k], nc = code % cols + dc[k];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    if (grid[nr][nc] != 1 || rotten[nr * cols + nc]) continue;
                    rotten[nr * cols + nc] = true;
                    fresh--;
                    batch.add(nr * cols + nc);
                }
            }
            minutes++;
        }
        return fresh == 0 ? minutes : -1;
    }

    static int oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] now = new int[rows][];
        for (int r = 0; r < rows; r++) now[r] = grid[r].clone();
        int minutes = 0;
        while (true) {
            int[][] after = new int[rows][];
            for (int r = 0; r < rows; r++) after[r] = now[r].clone();
            boolean changed = false;
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++) {
                    if (now[r][c] != 1) continue;
                    boolean touch = (r > 0 && now[r - 1][c] == 2) || (r + 1 < rows && now[r + 1][c] == 2)
                            || (c > 0 && now[r][c - 1] == 2) || (c + 1 < cols && now[r][c + 1] == 2);
                    if (touch) { after[r][c] = 2; changed = true; }
                }
            if (!changed) break;
            now = after;
            minutes++;
        }
        for (int[] line : now) for (int x : line) if (x == 1) return -1;
        return minutes;
    }

    public static void main(String[] args) {
        if (solve(new int[][] {{2, 1, 1}, {1, 1, 0}, {0, 1, 1}}) != 4) throw new AssertionError("example 1");
        if (solve(new int[][] {{2, 1, 0, 1}, {1, 1, 0, 1}}) != -1) throw new AssertionError("example 2");
        if (solve(new int[][] {{0, 2}}) != 0) throw new AssertionError("nothing fresh");
        if (solve(new int[][] {{0}}) != 0) throw new AssertionError("empty grid");
        if (everyBatchCounted(new int[][] {{2, 1}}) != 2 || solve(new int[][] {{2, 1}}) != 1)
            throw new AssertionError("counting the final empty batch overcounts");
        Random rnd = new Random(22104);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] grid = new int[rows][cols];
            for (int[] line : grid) for (int c = 0; c < cols; c++) {
                int x = rnd.nextInt(10);
                line[c] = x < 2 ? 0 : x < 8 ? 1 : 2;
            }
            int[][] before = new int[rows][];
            for (int r = 0; r < rows; r++) before[r] = grid[r].clone();
            if (solve(grid) != oracle(before)) throw new AssertionError("random " + t);
            if (!java.util.Arrays.deepEquals(grid, before)) throw new AssertionError("mutated " + t);
        }
    }
}
```
