<!-- solutions-for: 22-bfs-variations -->
### Resource Dominance

#### Solution: [Build] Position And Remaining Breaks (Author exercise)
<!-- id: bv-remaining-breaks -->

**Approach.** Find `S` and `T`, then run an ordinary breadth-first search whose vertex is the packed pair `square * (k + 1) + left`. The seen array, the queue and the step counts all live in flat int arrays indexed by that code, and a neighbor is entered only if the break count stays at or above zero and the pair has not been seen. The oracle never queues anything. It keeps a distance for every pair, starts all of them at infinity except the start pair, and relaxes every move over and over until a whole pass changes nothing, then takes the smallest distance among the pairs on `T`. The assertions compare the two on random grids and check the three examples, and they confirm that a flat seen flag per square returns -1 on the lesson's map where the answer is 8, that the input rows are untouched, and that packing with `k` instead of `k + 1` makes two different states share a code.

**Complexity.** Every pair is queued at most once and tried from four sides, so time and memory are O(R * C * k). Breadth-first order is what makes the first arrival at `T` the smallest.

```java run
import java.util.Random;

public final class RemainingBreaksSolution {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};
    private static final int INF = 1_000_000;

    static int solve(String[] grid, int k) {
        int rows = grid.length, cols = grid[0].length(), width = k + 1;
        int from = -1, to = -1;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                char ch = grid[r].charAt(c);
                if (ch == 'S') from = r * cols + c;
                if (ch == 'T') to = r * cols + c;
            }
        int total = rows * cols * width;
        boolean[] seen = new boolean[total];
        int[] queue = new int[total], dist = new int[total];
        int head = 0, tail = 0;
        int start = from * width + k;
        seen[start] = true;
        queue[tail++] = start;
        while (head < tail) {
            int state = queue[head++];
            int cell = state / width, left = state % width;
            if (cell == to) return dist[state];
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = left - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                if (nl < 0) continue;
                int next = (nr * cols + nc) * width + nl;
                if (seen[next]) continue;
                seen[next] = true;
                dist[next] = dist[state] + 1;
                queue[tail++] = next;
            }
        }
        return -1;
    }

    static int oracle(String[] grid, int k) {
        int rows = grid.length, cols = grid[0].length();
        int[][][] dist = new int[rows][cols][k + 1];
        int tr = -1, tc = -1;
        for (int[][] a : dist) for (int[] b : a) java.util.Arrays.fill(b, INF);
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                if (grid[r].charAt(c) == 'S') dist[r][c][k] = 0;
                if (grid[r].charAt(c) == 'T') { tr = r; tc = c; }
            }
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = rows - 1; r >= 0; r--)
                for (int c = cols - 1; c >= 0; c--)
                    for (int l = 0; l <= k; l++) {
                        if (dist[r][c][l] >= INF) continue;
                        for (int d = 0; d < 4; d++) {
                            int nr = r + DR[d], nc = c + DC[d];
                            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                            int nl = l - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                            if (nl >= 0 && dist[r][c][l] + 1 < dist[nr][nc][nl]) {
                                dist[nr][nc][nl] = dist[r][c][l] + 1;
                                moved = true;
                            }
                        }
                    }
        }
        int best = INF;
        for (int l = 0; l <= k; l++) best = Math.min(best, dist[tr][tc][l]);
        return best >= INF ? -1 : best;
    }

    static int flatSeenPerSquare(String[] grid, int k) {
        int rows = grid.length, cols = grid[0].length();
        boolean[] seen = new boolean[rows * cols];
        int[] queue = new int[rows * cols], left = new int[rows * cols], dist = new int[rows * cols];
        int head = 0, tail = 0, to = -1;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                char ch = grid[r].charAt(c);
                if (ch == 'S') { queue[tail] = r * cols + c; left[tail] = k; seen[r * cols + c] = true; tail++; }
                if (ch == 'T') to = r * cols + c;
            }
        while (head < tail) {
            int cell = queue[head], l = left[head], dd = dist[head];
            head++;
            if (cell == to) return dd;
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = l - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                if (nl < 0 || seen[nr * cols + nc]) continue;
                seen[nr * cols + nc] = true;
                queue[tail] = nr * cols + nc; left[tail] = nl; dist[tail] = dd + 1; tail++;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        String[] lesson = {"S#...", "...##", "..##T"};
        String[] before = lesson.clone();
        if (solve(lesson, 1) != 8) throw new AssertionError("example 1");
        if (solve(lesson, 2) != 6) throw new AssertionError("example 2");
        if (solve(lesson, 0) != -1) throw new AssertionError("no breaks");
        if (!java.util.Arrays.equals(before, lesson)) throw new AssertionError("input changed");
        if (flatSeenPerSquare(lesson, 1) != -1) throw new AssertionError("flat flag should lose the route");
        int k = 2;
        int codeA = 0 * k + k, codeB = 1 * k + 0;
        if (codeA != codeB) throw new AssertionError("width k should collide");
        int w = k + 1;
        if (0 * w + k == 1 * w + 0) throw new AssertionError("width k+1 must not collide");
        Random rnd = new Random(22501);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            if (rows * cols < 2) cols = 2;
            char[][] g = new char[rows][cols];
            for (char[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(10) < 4 ? '#' : '.';
            int s = rnd.nextInt(rows * cols), e;
            do { e = rnd.nextInt(rows * cols); } while (e == s);
            g[s / cols][s % cols] = 'S';
            g[e / cols][e % cols] = 'T';
            String[] grid = new String[rows];
            for (int r = 0; r < rows; r++) grid[r] = new String(g[r]);
            int kk = rnd.nextInt(4);
            int got = solve(grid, kk), want = oracle(grid, kk);
            if (got != want) throw new AssertionError("random " + t + " got " + got + " want " + want);
        }
    }
}
```

#### Solution: [Vary] Best Resource Per Cell (Author exercise)
<!-- id: bv-best-per-cell -->

**Approach.** Keep an array `best` with one entry per square, filled with -1, and set the start entry to `k`. Queue packed pairs of square and breaks left. A neighbor is queued only when the move is affordable and leaves strictly more breaks than the entry for that square, and the entry is raised at the moment of queueing. Steps are never recorded, because the question does not ask for them, which is why a richer state may replace a poorer one no matter how many moves it took. When the queue is empty the table is the answer. The oracle ignores the queue and works with walls: it relaxes the fewest walls needed to reach each square until nothing changes, then reports `k` minus that count when it is at most `k` and -1 otherwise. The assertions compare the two on random grids, check both examples, and show that a table left zero-filled instead of filled with -1 gives a wrong answer for a square that is out of reach.

**Complexity.** A square is queued at most `k + 1` times, since every queueing raises its entry, so the search runs in O(R * C * k) time. The table needs only O(R * C) memory next to the queue.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class BestPerCellSolution {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    static int[][] solve(String[] grid, int k) {
        return run(grid, k, true);
    }

    static int[][] run(String[] grid, int k, boolean fillMinusOne) {
        int rows = grid.length, cols = grid[0].length(), width = k + 1;
        int[] best = new int[rows * cols];
        if (fillMinusOne) Arrays.fill(best, -1);
        best[0] = k;
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(k);
        while (!queue.isEmpty()) {
            int state = queue.poll();
            int cell = state / width, left = state % width;
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = left - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                if (nl < 0) continue;
                int next = nr * cols + nc;
                if (nl <= best[next]) continue;
                best[next] = nl;
                queue.add(next * width + nl);
            }
        }
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) out[r][c] = best[r * cols + c];
        return out;
    }

    static int[][] oracle(String[] grid, int k) {
        int rows = grid.length, cols = grid[0].length(), far = 1_000_000;
        int[][] walls = new int[rows][cols];
        for (int[] row : walls) Arrays.fill(row, far);
        walls[0][0] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = rows - 1; r >= 0; r--)
                for (int c = cols - 1; c >= 0; c--) {
                    if (walls[r][c] >= far) continue;
                    for (int d = 0; d < 4; d++) {
                        int nr = r + DR[d], nc = c + DC[d];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                        int w = walls[r][c] + (grid[nr].charAt(nc) == '#' ? 1 : 0);
                        if (w < walls[nr][nc]) { walls[nr][nc] = w; moved = true; }
                    }
                }
        }
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) out[r][c] = walls[r][c] <= k ? k - walls[r][c] : -1;
        return out;
    }

    public static void main(String[] args) {
        String[] a = {".#.", "..."};
        if (!Arrays.deepToString(solve(a, 1)).equals("[[1, 0, 1], [1, 1, 1]]")) throw new AssertionError("example 1");
        String[] b = {".##", ".#."};
        if (!Arrays.deepToString(solve(b, 1)).equals("[[1, 0, -1], [1, 0, 0]]")) throw new AssertionError("example 2");
        String[] trap = {".#.#"};
        int[][] right = solve(trap, 1);
        int[][] zeroFilled = run(trap, 1, false);
        if (!Arrays.deepToString(right).equals("[[1, 0, 0, -1]]")) throw new AssertionError("trap answer");
        if (Arrays.deepEquals(right, zeroFilled)) throw new AssertionError("zero filled table should differ");
        if (zeroFilled[0][3] != 0) throw new AssertionError("zero filled table reports an unreachable square as 0");
        Random rnd = new Random(22502);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(6);
            String[] grid = new String[rows];
            for (int r = 0; r < rows; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < cols; c++) sb.append(rnd.nextInt(10) < 4 && (r + c) > 0 ? '#' : '.');
                grid[r] = sb.toString();
            }
            String[] copy = grid.clone();
            int k = rnd.nextInt(5);
            if (!Arrays.deepEquals(solve(grid, k), oracle(grid, k))) throw new AssertionError("random " + t);
            if (!Arrays.equals(copy, grid)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Boundary] Longer Path With More Resource (Author exercise)
<!-- id: bv-longer-richer -->

**Approach.** Run the layered search for at most `limit` layers and never return early. The table `best` holds the richest break count queued per square, and a neighbor is queued only if it beats the entry, which is sound because every state already in the table has at most as many moves as the newcomer, and a state that is no quicker and no richer cannot do anything the older one cannot. The answer is the table entry for the target when the layers run out. Dominance is proved exactly when two states share a square, the older one has no more moves and no fewer breaks, and more breaks never forbid or reprice a move. The oracle is a layered walk table: for each move count t from 0 to `limit` it stores the most breaks that any walk of exactly t moves can still hold on each square, revisits allowed, and answers with the best value at the target over all t. The assertions compare the two on random grids, check the examples at limits 5, 6, 7 and 8, show that a flat seen flag per square gives 0 where the answer is 1, and show that a search which ignores the move cap and keeps only the richest state reports 1 at limit 6, where the answer is 0.

**Complexity.** Each square is queued at most `k + 1` times and each queueing does constant work, so the search takes O(R * C * k) time regardless of `limit`, which only cuts it short. The table adds O(R * C) memory, and the oracle costs O(limit * R * C) per grid.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class LongerRicherSolution {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    static int solve(String[] grid, int k, int limit) {
        int rows = grid.length, cols = grid[0].length(), width = k + 1;
        int[] best = new int[rows * cols];
        Arrays.fill(best, -1);
        best[0] = k;
        ArrayDeque<Integer> layer = new ArrayDeque<>();
        layer.add(k);
        for (int step = 0; step < limit && !layer.isEmpty(); step++) {
            for (int size = layer.size(); size > 0; size--) {
                int state = layer.poll();
                int cell = state / width, left = state % width;
                int r = cell / cols, c = cell % cols;
                for (int d = 0; d < 4; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    int nl = left - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                    if (nl < 0) continue;
                    int next = nr * cols + nc;
                    if (nl <= best[next]) continue;
                    best[next] = nl;
                    layer.add(next * width + nl);
                }
            }
        }
        return best[rows * cols - 1];
    }

    static int oracle(String[] grid, int k, int limit) {
        int rows = grid.length, cols = grid[0].length();
        int[][] cur = new int[rows][cols];
        for (int[] row : cur) Arrays.fill(row, -1);
        cur[0][0] = k;
        int answer = cur[rows - 1][cols - 1];
        for (int t = 0; t < limit; t++) {
            int[][] next = new int[rows][cols];
            for (int[] row : next) Arrays.fill(row, -1);
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++) {
                    if (cur[r][c] < 0) continue;
                    for (int d = 0; d < 4; d++) {
                        int nr = r + DR[d], nc = c + DC[d];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                        int nl = cur[r][c] - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                        if (nl >= 0) next[nr][nc] = Math.max(next[nr][nc], nl);
                    }
                }
            cur = next;
            answer = Math.max(answer, cur[rows - 1][cols - 1]);
        }
        return answer;
    }

    static int flatSeenPerSquare(String[] grid, int k, int limit) {
        int rows = grid.length, cols = grid[0].length();
        boolean[] seen = new boolean[rows * cols];
        int[] queue = new int[rows * cols], left = new int[rows * cols], dist = new int[rows * cols];
        int head = 0, tail = 1, answer = -1;
        queue[0] = 0; left[0] = k; seen[0] = true;
        while (head < tail) {
            int cell = queue[head], l = left[head], dd = dist[head];
            head++;
            if (cell == rows * cols - 1) answer = Math.max(answer, l);
            if (dd == limit) continue;
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = l - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                if (nl < 0 || seen[nr * cols + nc]) continue;
                seen[nr * cols + nc] = true;
                queue[tail] = nr * cols + nc; left[tail] = nl; dist[tail] = dd + 1; tail++;
            }
        }
        return answer;
    }

    static int richestIgnoringCap(String[] grid, int k) {
        int rows = grid.length, cols = grid[0].length(), width = k + 1;
        int[] best = new int[rows * cols];
        Arrays.fill(best, -1);
        best[0] = k;
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(k);
        while (!queue.isEmpty()) {
            int state = queue.poll();
            int cell = state / width, left = state % width;
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = left - (grid[nr].charAt(nc) == '#' ? 1 : 0);
                if (nl < 0 || nl <= best[nr * cols + nc]) continue;
                best[nr * cols + nc] = nl;
                queue.add((nr * cols + nc) * width + nl);
            }
        }
        return best[rows * cols - 1];
    }

    public static void main(String[] args) {
        String[] g = {".#...", "...#.", "...#."};
        int[] want = {-1, -1, -1, -1, -1, -1, 0, 0, 1, 1};
        for (int limit = 0; limit < want.length; limit++) {
            if (solve(g, 1, limit) != want[limit]) throw new AssertionError("limit " + limit);
            if (oracle(g, 1, limit) != want[limit]) throw new AssertionError("oracle limit " + limit);
        }
        if (solve(g, 1, 6) != 0 || solve(g, 1, 8) != 1) throw new AssertionError("examples");
        if (flatSeenPerSquare(g, 1, 8) != 0) throw new AssertionError("flat flag should report 0 at limit 8");
        if (richestIgnoringCap(g, 1) != 1 || solve(g, 1, 6) == richestIgnoringCap(g, 1))
            throw new AssertionError("ignoring the cap should overstate the answer at limit 6");
        if (solve(new String[] {"."}, 3, 0) != 3) throw new AssertionError("one square");
        Random rnd = new Random(22503);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            String[] grid = new String[rows];
            for (int r = 0; r < rows; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < cols; c++) sb.append(rnd.nextInt(10) < 4 && (r + c) > 0 && (r + 1 < rows || c + 1 < cols) ? '#' : '.');
                grid[r] = sb.toString();
            }
            String[] copy = grid.clone();
            int k = rnd.nextInt(4), limit = rnd.nextInt(13);
            int got = solve(grid, k, limit), exp = oracle(grid, k, limit);
            if (got != exp) throw new AssertionError("random " + t + " got " + got + " want " + exp);
            if (!Arrays.equals(copy, grid)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Recognize] Shortest Path In A Grid With Obstacles Elimination (LeetCode 1293)
<!-- id: bv-obstacle-elimination -->

**Approach.** If `k` is at least `rows + cols - 2`, the plain staircase walk of that length is already allowed, because it passes at most `rows + cols - 3` obstacles, so that length is returned at once and large `k` never costs memory. Otherwise a breadth-first search runs over packed pairs of cell and eliminations left, stored in flat arrays with the step count beside each queued state. A table `best` with one entry per cell starts at -1, and a neighbor is queued only when it holds strictly more eliminations than the entry, which is safe because breadth-first order has already queued every state of equal or smaller distance. The start enters the table directly, so a search with `k = 0` still begins. Three oracles stand against it: a breadth-first search that marks the full triple `(row, col, left)`, and a Bellman-Ford style pass that relaxes a distance for every triple until nothing changes. The assertions compare all three on random grids, require the pruned search never to queue more states than full marking and to queue strictly fewer on at least one grid, and show that a flat seen flag per cell returns -1 on a grid whose answer is 8 and that a zero-filled table breaks a search whose `k` is 0.

**Complexity.** Pruned search queues each cell at most `k + 1` times, with constant work per queueing, so it runs in O(R * C * min(k, R + C)) time. The table is O(R * C), and the queue array holds at most the same number of states.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ObstacleEliminationSolution {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};
    private static final int FAR = 1_000_000;
    static int lastQueued;

    static int solve(int[][] grid, int k) {
        return pruned(grid, k, true);
    }

    static int pruned(int[][] grid, int k, boolean fillMinusOne) {
        int rows = grid.length, cols = grid[0].length;
        if (k >= rows + cols - 2) { lastQueued = 0; return rows + cols - 2; }
        int width = k + 1, cells = rows * cols;
        int[] best = new int[cells];
        if (fillMinusOne) Arrays.fill(best, -1);
        int[] queue = new int[cells * width], dist = new int[cells * width];
        int head = 0, tail = 0;
        best[0] = k;
        queue[tail++] = k;
        while (head < tail) {
            int state = queue[head], steps = dist[head];
            head++;
            int cell = state / width, left = state % width;
            if (cell == cells - 1) { lastQueued = tail; return steps; }
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = left - grid[nr][nc];
                if (nl < 0) continue;
                int next = nr * cols + nc;
                if (nl <= best[next]) continue;
                best[next] = nl;
                queue[tail] = next * width + nl;
                dist[tail] = steps + 1;
                tail++;
            }
        }
        lastQueued = tail;
        return -1;
    }

    static int fullMarking(int[][] grid, int k) {
        int rows = grid.length, cols = grid[0].length, width = k + 1;
        boolean[] seen = new boolean[rows * cols * width];
        int[] queue = new int[rows * cols * width], dist = new int[rows * cols * width];
        int head = 0, tail = 0;
        seen[k] = true;
        queue[tail++] = k;
        while (head < tail) {
            int state = queue[head], steps = dist[head];
            head++;
            int cell = state / width, left = state % width;
            if (cell == rows * cols - 1) { lastQueued = tail; return steps; }
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = left - grid[nr][nc];
                if (nl < 0) continue;
                int next = (nr * cols + nc) * width + nl;
                if (seen[next]) continue;
                seen[next] = true;
                queue[tail] = next;
                dist[tail] = steps + 1;
                tail++;
            }
        }
        lastQueued = tail;
        return -1;
    }

    static int relaxation(int[][] grid, int k) {
        int rows = grid.length, cols = grid[0].length;
        int[][][] dist = new int[rows][cols][k + 1];
        for (int[][] a : dist) for (int[] b : a) Arrays.fill(b, FAR);
        dist[0][0][k] = 0;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = rows - 1; r >= 0; r--)
                for (int c = cols - 1; c >= 0; c--)
                    for (int l = 0; l <= k; l++) {
                        if (dist[r][c][l] >= FAR) continue;
                        for (int d = 0; d < 4; d++) {
                            int nr = r + DR[d], nc = c + DC[d];
                            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                            int nl = l - grid[nr][nc];
                            if (nl >= 0 && dist[r][c][l] + 1 < dist[nr][nc][nl]) {
                                dist[nr][nc][nl] = dist[r][c][l] + 1;
                                moved = true;
                            }
                        }
                    }
        }
        int best = FAR;
        for (int l = 0; l <= k; l++) best = Math.min(best, dist[rows - 1][cols - 1][l]);
        return best >= FAR ? -1 : best;
    }

    static int flatSeenPerCell(int[][] grid, int k) {
        int rows = grid.length, cols = grid[0].length;
        boolean[] seen = new boolean[rows * cols];
        int[] queue = new int[rows * cols], left = new int[rows * cols], dist = new int[rows * cols];
        int head = 0, tail = 1;
        left[0] = k;
        seen[0] = true;
        while (head < tail) {
            int cell = queue[head], l = left[head], steps = dist[head];
            head++;
            if (cell == rows * cols - 1) return steps;
            int r = cell / cols, c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int nl = l - grid[nr][nc];
                if (nl < 0 || seen[nr * cols + nc]) continue;
                seen[nr * cols + nc] = true;
                queue[tail] = nr * cols + nc; left[tail] = nl; dist[tail] = steps + 1; tail++;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 0}, {1, 1, 0}, {0, 0, 0}};
        if (solve(e1, 1) != 4) throw new AssertionError("example 1");
        int[][] e2 = {{0, 1, 1}, {1, 1, 1}, {1, 1, 0}};
        if (solve(e2, 1) != -1) throw new AssertionError("example 2");
        if (solve(new int[][] {{0}}, 0) != 0) throw new AssertionError("single cell");
        int[][] trap = {{0, 1, 0, 0, 0}, {0, 0, 0, 1, 1}, {0, 0, 1, 1, 0}};
        if (solve(trap, 1) != 8 || fullMarking(trap, 1) != 8 || relaxation(trap, 1) != 8)
            throw new AssertionError("trap answer");
        if (flatSeenPerCell(trap, 1) != -1) throw new AssertionError("flat flag should lose the route");
        int[][] zeroCase = {{0, 0}};
        if (solve(zeroCase, 0) != 1) throw new AssertionError("k = 0 baseline");
        int[][] longer = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
        if (pruned(longer, 0, false) != -1) throw new AssertionError("zero filled table should lose the start");
        Random rnd = new Random(22504);
        long prunedTotal = 0, fullTotal = 0;
        boolean strictlyFewer = false;
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] grid = new int[rows][cols];
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++)
                    grid[r][c] = rnd.nextInt(10) < 4 && (r + c) > 0 && (r + 1 < rows || c + 1 < cols) ? 1 : 0;
            int k = rnd.nextInt(9);
            int[][] copy = new int[rows][];
            for (int r = 0; r < rows; r++) copy[r] = grid[r].clone();
            int a = solve(grid, k), pq = lastQueued;
            int b = fullMarking(grid, k), fq = lastQueued;
            int c2 = relaxation(grid, k);
            if (a != b || b != c2) throw new AssertionError("random " + t + ": " + a + " " + b + " " + c2);
            if (!Arrays.deepEquals(copy, grid)) throw new AssertionError("input changed");
            if (k < rows + cols - 2) {
                if (pq > fq) throw new AssertionError("pruning queued more states");
                if (pq < fq) strictlyFewer = true;
            }
        }
        if (!strictlyFewer) throw new AssertionError("pruning never saved a state");
    }
}
```
