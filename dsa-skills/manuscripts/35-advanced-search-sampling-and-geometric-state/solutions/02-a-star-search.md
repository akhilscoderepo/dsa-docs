<!-- solutions-for: 02-a-star-search -->
### Solutions For A Star Search

#### Solution: [Build] Dijkstra With Zero Heuristic (Author exercise)
<!-- id: as35-zero-heuristic -->

**Approach.**
With `h = 0` the priority `f` equals `g`, so the loop is Dijkstra's algorithm. The queue holds entries `(f, row, col, g)` ordered by `f`, then row, then column. Each pop first compares the entry's `g` with `best` for the cell. A larger `g` means a cheaper route was recorded after the entry was pushed, so the entry is stale and the loop skips it without counting. Every other pop counts as one expansion. When the goal pops, its `g` is final, because every entry still in the queue has `f` at least as large and no entering cost is negative. The method then returns the cost and the count. If the queue empties, the goal is unreachable and the method returns -1 with the count so far. The invariant is that a cell pops non-stale at most once, and its `g` equals the cheapest cost from the start.

The program checks the cost against a Bellman-Ford style relaxation oracle. It checks the expansion count against a second implementation that keeps entries in a `TreeSet`, so the order of pops comes from a different structure.

**Complexity.**
- **Time** is O(V log V) for `V` cells, because each cell enters the queue a bounded number of times and every queue operation costs O(log V).
- **Space** is O(V) for `best` and the queue.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.TreeSet;

public final class ZeroHeuristicBuild {
    /**
     * Dijkstra on a cost grid, reported as {cost, nonStalePops}.
     * Time: O(V log V). Space: O(V).
     * Invariant: a non-stale pop carries the final cost of its cell.
     */
    static int[] zeroHeuristic(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE); // no route is known yet
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> {
            if (x[0] != y[0]) return Integer.compare(x[0], y[0]); // smallest f first
            if (x[1] != y[1]) return Integer.compare(x[1], y[1]); // then smallest row
            return Integer.compare(x[2], y[2]);                   // then smallest column
        });
        best[sr][sc] = 0;
        pq.add(new int[]{0, sr, sc, 0});
        int expanded = 0;
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!pq.isEmpty()) { // each pop either skips a stale entry or finalizes one cell
            int[] cur = pq.poll();
            int r = cur[1], c = cur[2], g = cur[3];
            if (g > best[r][c]) continue;          // stale entry: not counted
            expanded++;                            // one finalized cell
            if (r == gr && c == gc) return new int[]{g, expanded}; // first goal pop is optimal
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue; // wall or outside
                int ng = g + cost[nr][nc];         // cost so far of the neighbour
                if (ng < best[nr][nc]) { best[nr][nc] = ng; pq.add(new int[]{ng, nr, nc, ng}); } // h = 0, so f = g
            }
        }
        return new int[]{-1, expanded};
    }

    static int bellman(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        long[][] dist = new long[R][C];
        for (long[] row : dist) Arrays.fill(row, Long.MAX_VALUE / 4);
        dist[sr][sc] = 0;
        boolean changed = true;
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (changed) { // repeated relaxation reaches every shortest distance
            changed = false;
            for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) {
                if (cost[r][c] == 0) continue;
                for (int d = 0; d < 4; d++) {
                    int pr = r + dr[d], pc = c + dc[d];
                    if (pr < 0 || pc < 0 || pr >= R || pc >= C || cost[pr][pc] == 0) continue;
                    if (dist[pr][pc] + cost[r][c] < dist[r][c]) { dist[r][c] = dist[pr][pc] + cost[r][c]; changed = true; }
                }
            }
        }
        return dist[gr][gc] >= Long.MAX_VALUE / 4 ? -1 : (int) dist[gr][gc];
    }

    static int[] treeVersion(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        TreeSet<long[]> set = new TreeSet<>((x, y) -> {
            for (int i = 0; i < 4; i++) if (x[i] != y[i]) return Long.compare(x[i], y[i]);
            return 0;
        });
        best[sr][sc] = 0;
        set.add(new long[]{0, sr, sc, 0});
        int expanded = 0;
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!set.isEmpty()) {
            long[] cur = set.pollFirst();
            int r = (int) cur[1], c = (int) cur[2], g = (int) cur[3];
            if (g > best[r][c]) continue;
            expanded++;
            if (r == gr && c == gc) return new int[]{g, expanded};
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue;
                if (g + cost[nr][nc] < best[nr][nc]) { best[nr][nc] = g + cost[nr][nc]; set.add(new long[]{best[nr][nc], nr, nc, best[nr][nc]}); }
            }
        }
        return new int[]{-1, expanded};
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (!Arrays.equals(zeroHeuristic(new int[][]{{1,1,1},{1,0,1},{1,1,1}}, 0, 0, 2, 2), new int[]{4, 8})) throw new AssertionError("ex1");
        if (!Arrays.equals(zeroHeuristic(new int[][]{{1,0,1}}, 0, 0, 0, 2), new int[]{-1, 1})) throw new AssertionError("ex2");
        // random grids: cost against relaxation, expansions against the TreeSet version
        Random rnd = new Random(41);
        for (int t = 0; t < 400; t++) {
            int R = 1 + rnd.nextInt(5), C = 1 + rnd.nextInt(5);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(4) == 0 ? 0 : 1 + rnd.nextInt(4);
            g[0][0] = 1; g[R - 1][C - 1] = 1;
            int[] got = zeroHeuristic(g, 0, 0, R - 1, C - 1);
            if (got[0] != bellman(g, 0, 0, R - 1, C - 1)) throw new AssertionError("cost");
            if (!Arrays.equals(got, treeVersion(g, 0, 0, R - 1, C - 1))) throw new AssertionError("expansions");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Manhattan Grid Heuristic (Author exercise)
<!-- id: as35-manhattan-grid -->

**Approach.**
The change from the previous exercise is the priority. A pushed entry carries `f = g + h`, where `h` is the row difference plus the column difference to the goal. Every open cell costs at least 1 to enter, so a route to the goal needs at least `h` more cost, and `h` never overestimates. Moving from `u` to `v` changes `h` by at most 1 and costs at least 1, so `h(u) <= w + h(v)` holds, and `h` is consistent. A consistent heuristic makes `f` non-decreasing along pops, so the first pop of a cell carries its final cost and the first goal pop is optimal. The stale-entry skip and the count stay as before. The invariant is that every popped entry has `f` no larger than the optimal cost until the goal pops.

The program checks the cost against Bellman-Ford relaxation on random grids and checks the count against a `TreeSet` implementation. It also confirms the examples show fewer expansions than `h = 0` and that the two heuristics give equal costs.

**Complexity.**
- **Time** is O(V log V) in the worst case, the bound of Dijkstra, and it is smaller in practice because cells with a large `f` stay in the queue.
- **Space** is O(V) for `best` and the queue.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.TreeSet;

public final class ManhattanGridVary {
    /**
     * A star with Manhattan distance, reported as {cost, nonStalePops}; weight 0 turns the guess off.
     * Time: O(V log V). Space: O(V).
     * Invariant: popped entries have f no larger than the optimal cost until the goal pops.
     */
    static int[] search(int[][] cost, int sr, int sc, int gr, int gc, int weight) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0])
                : x[1] != y[1] ? Integer.compare(x[1], y[1]) : Integer.compare(x[2], y[2]));
        best[sr][sc] = 0;
        pq.add(new int[]{weight * (Math.abs(sr - gr) + Math.abs(sc - gc)), sr, sc, 0});
        int expanded = 0;
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int r = cur[1], c = cur[2], g = cur[3];
            if (g > best[r][c]) continue;            // stale entry
            expanded++;                              // finalized cell
            if (r == gr && c == gc) return new int[]{g, expanded}; // goal pop
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue;
                int ng = g + cost[nr][nc];
                if (ng < best[nr][nc]) {
                    best[nr][nc] = ng;
                    int h = Math.abs(nr - gr) + Math.abs(nc - gc); // Manhattan distance to the goal
                    pq.add(new int[]{ng + weight * h, nr, nc, ng}); // f = g + h
                }
            }
        }
        return new int[]{-1, expanded};
    }

    static int[] manhattan(int[][] cost, int sr, int sc, int gr, int gc) { return search(cost, sr, sc, gr, gc, 1); }

    static int[] oracle(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        TreeSet<long[]> set = new TreeSet<>((x, y) -> {
            for (int i = 0; i < 4; i++) if (x[i] != y[i]) return Long.compare(x[i], y[i]);
            return 0;
        });
        best[sr][sc] = 0;
        set.add(new long[]{Math.abs(sr - gr) + Math.abs(sc - gc), sr, sc, 0});
        int expanded = 0;
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!set.isEmpty()) {
            long[] cur = set.pollFirst();
            int r = (int) cur[1], c = (int) cur[2], g = (int) cur[3];
            if (g > best[r][c]) continue;
            expanded++;
            if (r == gr && c == gc) return new int[]{g, expanded};
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue;
                int ng = g + cost[nr][nc];
                if (ng < best[nr][nc]) { best[nr][nc] = ng; set.add(new long[]{ng + Math.abs(nr - gr) + Math.abs(nc - gc), nr, nc, ng}); }
            }
        }
        return new int[]{-1, expanded};
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        int[][] open = new int[3][4];
        for (int[] row : open) Arrays.fill(row, 1);
        if (!Arrays.equals(manhattan(open, 0, 0, 0, 3), new int[]{3, 4})) throw new AssertionError("ex1");
        int[][] mixed = {{1,2,1,1},{1,1,1,3},{2,1,1,1}};
        if (!Arrays.equals(manhattan(mixed, 0, 0, 2, 3), new int[]{5, 7})) throw new AssertionError("ex2");
        if (!Arrays.equals(search(mixed, 0, 0, 2, 3, 0), new int[]{5, 11})) throw new AssertionError("zero heuristic");
        // random grids: same cost as h = 0, same pop count as the TreeSet version
        Random rnd = new Random(42);
        for (int t = 0; t < 400; t++) {
            int R = 1 + rnd.nextInt(6), C = 1 + rnd.nextInt(6);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(4) == 0 ? 0 : 1 + rnd.nextInt(5);
            g[0][0] = 1; g[R - 1][C - 1] = 1;
            int[] a = manhattan(g, 0, 0, R - 1, C - 1), z = search(g, 0, 0, R - 1, C - 1, 0);
            if (a[0] != z[0]) throw new AssertionError("cost differs");
            if (!Arrays.equals(a, oracle(g, 0, 0, R - 1, C - 1))) throw new AssertionError("oracle");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Overestimating Heuristic (Author exercise)
<!-- id: as35-overestimating-heuristic -->

**Approach.**
The method multiplies the Manhattan distance by `w`. For `w = 1` the guess is admissible and consistent, so the first goal pop is optimal. For `w` above 1 the guess can exceed the true remaining cost. In the second example the guess at the top row route is large relative to the cost so far, so the planner follows the cell with the smallest `h` and pops the goal through the route that enters the cost-2 cell. The goal pops with `g = 6` while a route of cost 5 exists through the middle column. The queue never ranks the cheaper route first, because the entry on that route has a larger `f`. Closed cells are never reopened here, which matches the problem text, so a later cheaper route to a closed cell cannot repair the result. The invariant that failed is "every queue entry has `f` at most the optimal cost".

The program runs both examples, compares every weight against a `TreeSet` implementation on random grids, and checks two facts. The result for `w = 1` always equals the true cost, and the result for every `w` is never below the true cost. A search over random grids confirms that inflated weights do overshoot on some inputs.

**Complexity.**
- **Time** is O(V log V), because the loop is the same as before.
- **Space** is O(V).

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.TreeSet;

public final class OverestimatingHeuristicBoundary {
    /**
     * First goal pop of the weighted search, or -1.
     * Time: O(V log V). Space: O(V).
     * Invariant for w = 1 only: every queued entry has f at most the optimal cost.
     */
    static int inflated(int[][] cost, int sr, int sc, int gr, int gc, int w) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        boolean[][] closed = new boolean[R][C];
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0])
                : x[1] != y[1] ? Integer.compare(x[1], y[1]) : Integer.compare(x[2], y[2]));
        best[sr][sc] = 0;
        pq.add(new int[]{w * (Math.abs(sr - gr) + Math.abs(sc - gc)), sr, sc, 0});
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int r = cur[1], c = cur[2], g = cur[3];
            if (g > best[r][c] || closed[r][c]) continue; // stale or already expanded
            closed[r][c] = true;                          // closed cells are never reopened
            if (r == gr && c == gc) return g;             // with w > 1 this g can exceed the optimum
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0 || closed[nr][nc]) continue;
                int ng = g + cost[nr][nc];
                if (ng < best[nr][nc]) {
                    best[nr][nc] = ng;
                    pq.add(new int[]{ng + w * (Math.abs(nr - gr) + Math.abs(nc - gc)), nr, nc, ng});
                }
            }
        }
        return -1;
    }

    static int viaTree(int[][] cost, int sr, int sc, int gr, int gc, int w) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
        boolean[][] closed = new boolean[R][C];
        TreeSet<long[]> set = new TreeSet<>((x, y) -> {
            for (int i = 0; i < 4; i++) if (x[i] != y[i]) return Long.compare(x[i], y[i]);
            return 0;
        });
        best[sr][sc] = 0;
        set.add(new long[]{(long) w * (Math.abs(sr - gr) + Math.abs(sc - gc)), sr, sc, 0});
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!set.isEmpty()) {
            long[] cur = set.pollFirst();
            int r = (int) cur[1], c = (int) cur[2], g = (int) cur[3];
            if (g > best[r][c] || closed[r][c]) continue;
            closed[r][c] = true;
            if (r == gr && c == gc) return g;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0 || closed[nr][nc]) continue;
                if (g + cost[nr][nc] < best[nr][nc]) {
                    best[nr][nc] = g + cost[nr][nc];
                    set.add(new long[]{best[nr][nc] + (long) w * (Math.abs(nr - gr) + Math.abs(nc - gc)), nr, nc, best[nr][nc]});
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[][] ex = {{1,1,1,2},{0,1,0,1},{0,1,1,1}};
        // the two examples from the problem text
        if (inflated(ex, 0, 0, 2, 3, 1) != 5) throw new AssertionError("ex1");
        if (inflated(ex, 0, 0, 2, 3, 4) != 6) throw new AssertionError("ex2");
        // random grids: w = 1 is optimal, every weight is at least the optimum, and the TreeSet version agrees
        Random rnd = new Random(43);
        int overshoots = 0;
        for (int t = 0; t < 600; t++) {
            int R = 1 + rnd.nextInt(5), C = 1 + rnd.nextInt(5);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(4) == 0 ? 0 : 1 + rnd.nextInt(5);
            g[0][0] = 1; g[R - 1][C - 1] = 1;
            int opt = inflated(g, 0, 0, R - 1, C - 1, 1);
            for (int w = 1; w <= 6; w++) {
                int got = inflated(g, 0, 0, R - 1, C - 1, w);
                if (got != viaTree(g, 0, 0, R - 1, C - 1, w)) throw new AssertionError("oracle");
                if ((got == -1) != (opt == -1) || (opt != -1 && got < opt)) throw new AssertionError("below optimum");
                if (got > opt) overshoots++;
            }
        }
        if (overshoots == 0) throw new AssertionError("no overshoot found");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] A-Star Grid Path (Author exercise)
<!-- id: as35-grid-path -->

**Approach.**
The heuristic is the Manhattan distance, which is admissible because every move costs at least 1 and consistent because one move changes the distance by at most 1. The method keeps `best` and a predecessor matrix. When a neighbour gets a strictly cheaper cost, the method stores the current cell as its predecessor and pushes a new entry. The strict comparison fixes the choice among equal routes, since the first cheapest predecessor found stays. A stale entry carries a `g` above `best`, so the method skips it before it touches any neighbour. That skip protects the predecessor matrix, because a stale expansion could push entries based on an outdated cost. When the goal pops, the method follows predecessors back to the start and reverses the list. The invariant is that `prev[v]` is the cell that produced `best[v]`.

The program checks that the returned route starts and ends at the right cells, that consecutive cells are neighbours, that the route cost equals the Bellman-Ford optimum, and that the example route matches. It also checks the single-cell case and unreachable goals.

**Complexity.**
- **Time** is O(V log V) for the search plus O(V) to rebuild the route.
- **Space** is O(V) for `best`, the predecessor matrix and the queue.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class GridPathRecognize {
    /**
     * Cheapest route from start to goal as a list of cells, or an empty list.
     * Time: O(V log V). Space: O(V).
     * Invariant: prev[v] is the cell that produced best[v], and best only decreases.
     */
    static List<int[]> route(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        int[][] prev = new int[R][C];
        for (int i = 0; i < R; i++) { Arrays.fill(best[i], Integer.MAX_VALUE); Arrays.fill(prev[i], -1); }
        PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0])
                : x[1] != y[1] ? Integer.compare(x[1], y[1]) : Integer.compare(x[2], y[2]));
        best[sr][sc] = 0;
        pq.add(new int[]{Math.abs(sr - gr) + Math.abs(sc - gc), sr, sc, 0});
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1}; // up, down, left, right
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int r = cur[1], c = cur[2], g = cur[3];
            if (g > best[r][c]) continue; // stale entry: its predecessor choice is outdated
            if (r == gr && c == gc) {
                List<int[]> path = new ArrayList<>();
                for (int at = r * C + c; at != -1; at = prev[at / C][at % C]) path.add(new int[]{at / C, at % C}); // walk predecessors
                Collections.reverse(path); // start first
                return path;
            }
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue;
                int ng = g + cost[nr][nc];
                if (ng < best[nr][nc]) { // strictly cheaper only, so equal routes keep the first predecessor
                    best[nr][nc] = ng;
                    prev[nr][nc] = r * C + c;
                    pq.add(new int[]{ng + Math.abs(nr - gr) + Math.abs(nc - gc), nr, nc, ng});
                }
            }
        }
        return new ArrayList<>();
    }

    static int optimum(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        long INF = Long.MAX_VALUE / 4;
        long[][] dist = new long[R][C];
        for (long[] row : dist) Arrays.fill(row, INF);
        dist[sr][sc] = 0;
        boolean changed = true;
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (changed) {
            changed = false;
            for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) if (cost[r][c] != 0)
                for (int d = 0; d < 4; d++) {
                    int pr = r + dr[d], pc = c + dc[d];
                    if (pr < 0 || pc < 0 || pr >= R || pc >= C || cost[pr][pc] == 0 || dist[pr][pc] >= INF) continue;
                    if (dist[pr][pc] + cost[r][c] < dist[r][c]) { dist[r][c] = dist[pr][pc] + cost[r][c]; changed = true; }
                }
        }
        return dist[gr][gc] >= INF ? -1 : (int) dist[gr][gc];
    }

    public static void main(String[] args) {
        int[][] ex = {{1,1,1,2},{0,1,0,1},{0,1,1,1}};
        // the two examples from the problem text
        int[][] want = {{0,0},{0,1},{1,1},{2,1},{2,2},{2,3}};
        List<int[]> got = route(ex, 0, 0, 2, 3);
        if (got.size() != want.length) throw new AssertionError("ex1 length");
        for (int i = 0; i < want.length; i++) if (!Arrays.equals(got.get(i), want[i])) throw new AssertionError("ex1 cell " + i);
        List<int[]> single = route(new int[][]{{7}}, 0, 0, 0, 0);
        if (single.size() != 1 || single.get(0)[0] != 0 || single.get(0)[1] != 0) throw new AssertionError("ex2");
        // an unreachable goal gives an empty list
        if (!route(new int[][]{{1,0,1}}, 0, 0, 0, 2).isEmpty()) throw new AssertionError("unreachable");
        // random grids: valid neighbour steps and optimal route cost
        Random rnd = new Random(44);
        for (int t = 0; t < 500; t++) {
            int R = 1 + rnd.nextInt(6), C = 1 + rnd.nextInt(6);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(4) == 0 ? 0 : 1 + rnd.nextInt(6);
            g[0][0] = 1; g[R - 1][C - 1] = 1;
            List<int[]> p = route(g, 0, 0, R - 1, C - 1);
            int opt = optimum(g, 0, 0, R - 1, C - 1);
            if (opt == -1) { if (!p.isEmpty()) throw new AssertionError("should be empty"); continue; }
            if (p.get(0)[0] != 0 || p.get(0)[1] != 0 || p.get(p.size() - 1)[0] != R - 1 || p.get(p.size() - 1)[1] != C - 1) throw new AssertionError("ends");
            int total = 0;
            for (int i = 1; i < p.size(); i++) {
                int[] a = p.get(i - 1), b = p.get(i);
                if (Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]) != 1 || g[b[0]][b[1]] == 0) throw new AssertionError("step");
                total += g[b[0]][b[1]]; // pay the entering cost
            }
            if (total != opt) throw new AssertionError("route cost " + total + " vs " + opt);
        }
        System.out.println("ok");
    }
}
```
