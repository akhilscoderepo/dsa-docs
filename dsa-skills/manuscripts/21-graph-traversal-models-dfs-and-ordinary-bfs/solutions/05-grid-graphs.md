<!-- solutions-for: 05-grid-graphs -->
### Grid Graphs

#### Solution: [Build] Flood Fill (LeetCode 733)
<!-- id: gt-flood-fill -->

**Approach.** Read the starting colour before anything changes, mark the start seen, and drain a queue of cell codes, recolouring each tile as it leaves the queue. A neighbor is queued only after the bounds, colour and seen gates, in that order, and it is marked at the moment it is queued. The oracle never builds a queue. It repeatedly sweeps a boolean table, wetting any same-coloured tile beside a wet one, until a whole sweep changes nothing, then paints the result on a copy. The assertions compare the two on random grids, require that the very same array object comes back, and confirm four claims from the lesson: a neighbor read outside the array throws, the code `r * cols + c` decodes back to `r` and `c`, marking at removal instead of at insertion would queue some tiles twice, and a diagonal tile is never reached.

**Complexity.** Each tile is queued once and tried from four sides, giving O(R * C) time. The seen table and the queue add O(R * C) memory beyond the image.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class FloodFillSolution {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    static int[][] solve(int[][] image, int sr, int sc, int color) {
        int rows = image.length, cols = image[0].length;
        int tone = image[sr][sc];
        boolean[] seen = new boolean[rows * cols];
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        seen[sr * cols + sc] = true;
        frontier.add(sr * cols + sc);
        while (!frontier.isEmpty()) {
            int code = frontier.poll();
            int r = code / cols, c = code % cols;
            image[r][c] = color;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (image[nr][nc] != tone) continue;
                int next = nr * cols + nc;
                if (seen[next]) continue;
                seen[next] = true;
                frontier.add(next);
            }
        }
        return image;
    }

    static int[][] oracle(int[][] image, int sr, int sc, int color) {
        int rows = image.length, cols = image[0].length, tone = image[sr][sc];
        boolean[][] wet = new boolean[rows][cols];
        wet[sr][sc] = true;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = rows - 1; r >= 0; r--) {
                for (int c = cols - 1; c >= 0; c--) {
                    if (wet[r][c] || image[r][c] != tone) continue;
                    boolean near = false;
                    for (int d = 0; d < 4; d++) {
                        int nr = r + DR[d], nc = c + DC[d];
                        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && wet[nr][nc]) near = true;
                    }
                    if (near) { wet[r][c] = true; moved = true; }
                }
            }
        }
        int[][] out = new int[rows][];
        for (int r = 0; r < rows; r++) {
            out[r] = image[r].clone();
            for (int c = 0; c < cols; c++) if (wet[r][c]) out[r][c] = color;
        }
        return out;
    }

    static int enqueuesWhenMarkedLate(int[][] image, int sr, int sc) {
        int rows = image.length, cols = image[0].length, tone = image[sr][sc];
        boolean[] seen = new boolean[rows * cols];
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        frontier.add(sr * cols + sc);
        int adds = 1;
        while (!frontier.isEmpty()) {
            int code = frontier.poll();
            if (seen[code]) continue;
            seen[code] = true;
            int r = code / cols, c = code % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (image[nr][nc] != tone || seen[nr * cols + nc]) continue;
                frontier.add(nr * cols + nc);
                adds++;
            }
        }
        return adds;
    }

    public static void main(String[] args) {
        int[][] a = {{2, 2, 0}, {2, 0, 2}, {1, 2, 2}};
        if (!java.util.Arrays.deepToString(solve(a, 0, 0, 5)).equals("[[5, 5, 0], [5, 0, 2], [1, 2, 2]]"))
            throw new AssertionError("example 1");
        int[][] b = {{1, 0, 1}, {0, 1, 0}};
        if (!java.util.Arrays.deepToString(solve(b, 1, 1, 4)).equals("[[1, 0, 1], [0, 4, 0]]"))
            throw new AssertionError("example 2");
        int[][] diag = {{1, 0}, {0, 1}};
        solve(diag, 0, 0, 7);
        if (diag[1][1] != 1 || diag[0][0] != 7) throw new AssertionError("diagonal tile must stay");
        try {
            int[] row = new int[3];
            int bad = row[-1];
            throw new AssertionError("negative index should throw " + bad);
        } catch (ArrayIndexOutOfBoundsException expected) {
            // bounds must be tested before any read
        }
        int cols = 7;
        for (int r = 0; r < 6; r++) for (int c = 0; c < cols; c++) {
            int code = r * cols + c;
            if (code / cols != r || code % cols != c) throw new AssertionError("code round trip");
        }
        if (enqueuesWhenMarkedLate(new int[][] {{1, 1}, {1, 1}}, 0, 0) <= 4)
            throw new AssertionError("late marking should queue a tile twice");
        Random rnd = new Random(21501);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(6), w = 1 + rnd.nextInt(6), k = 1 + rnd.nextInt(3);
            int[][] img = new int[rows][w];
            for (int[] row : img) for (int c = 0; c < w; c++) row[c] = rnd.nextInt(k);
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(w), color = rnd.nextInt(k + 1);
            int[][] want = oracle(img, sr, sc, color);
            int[][] copy = new int[rows][];
            for (int r = 0; r < rows; r++) copy[r] = img[r].clone();
            int[][] got = solve(copy, sr, sc, color);
            if (got != copy) throw new AssertionError("must return the same array " + t);
            if (!java.util.Arrays.deepEquals(got, want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Number Of Islands (LeetCode 200)
<!-- id: gt-island-count -->

**Approach.** An outer scan visits every cell in reading order and launches one traversal at each land tile that the private seen table has not yet claimed, so the number of launches is the answer. The traversal uses a queue of cell codes and the same three gates as the lesson, and the input grid is only read. The oracle gives every land tile its own label and then sweeps the grid again and again, lowering a label to match any land neighbor with a smaller one, until nothing moves, and counts the labels that equal their own tile number. The assertions run on random boards, check by a before and after copy that the grid is untouched, and show that `grid[r][c] == 1` is false for `'1'` whose code is 49, that corner-touching land counts as two islands, and that a recursive version on a thousand-by-thousand board of land overflows a small thread stack while the queue version finishes.

**Complexity.** O(R * C) time, because the scan and all traversals together touch each tile a constant number of times. Space is O(R * C) for the seen table plus the queue.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class IslandCountSolution {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    static int solve(char[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        boolean[] seen = new boolean[rows * cols];
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        int islands = 0;
        for (int start = 0; start < rows * cols; start++) {
            if (seen[start] || grid[start / cols][start % cols] != '1') continue;
            islands++;
            seen[start] = true;
            frontier.add(start);
            while (!frontier.isEmpty()) {
                int code = frontier.poll();
                int r = code / cols, c = code % cols;
                for (int d = 0; d < 4; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    if (grid[nr][nc] != '1') continue;
                    int next = nr * cols + nc;
                    if (seen[next]) continue;
                    seen[next] = true;
                    frontier.add(next);
                }
            }
        }
        return islands;
    }

    static int oracle(char[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] label = new int[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) label[r][c] = r * cols + c;
        boolean moved = true;
        while (moved) {
            moved = false;
            for (int r = 0; r < rows; r++) {
                for (int c = 0; c < cols; c++) {
                    if (grid[r][c] != '1') continue;
                    for (int d = 0; d < 4; d++) {
                        int nr = r + DR[d], nc = c + DC[d];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] != '1') continue;
                        if (label[nr][nc] < label[r][c]) { label[r][c] = label[nr][nc]; moved = true; }
                    }
                }
            }
        }
        int roots = 0;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == '1' && label[r][c] == r * cols + c) roots++;
        return roots;
    }

    static void dive(boolean[][] land, int r, int c) {
        if (r < 0 || r >= land.length || c < 0 || c >= land[0].length || !land[r][c]) return;
        land[r][c] = false;
        dive(land, r + 1, c);
        dive(land, r, c + 1);
        dive(land, r - 1, c);
        dive(land, r, c - 1);
    }

    static char[][] make(String... rows) {
        char[][] g = new char[rows.length][];
        for (int i = 0; i < rows.length; i++) g[i] = rows[i].toCharArray();
        return g;
    }

    public static void main(String[] args) throws Exception {
        if (solve(make("11000", "11000", "00100", "00011")) != 3) throw new AssertionError("example 1");
        if (solve(make("101", "010", "101")) != 5) throw new AssertionError("example 2");
        if (solve(make("10", "01")) != 2) throw new AssertionError("corner contact is not a link");
        char[][] one = make("1");
        if (one[0][0] == 1) throw new AssertionError("char '1' must not equal int 1");
        if ((int) one[0][0] != 49) throw new AssertionError("code of '1' is 49");
        Random rnd = new Random(21502);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            char[][] g = new char[rows][cols];
            for (char[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(10) < 5 ? '1' : '0';
            char[][] before = new char[rows][];
            for (int r = 0; r < rows; r++) before[r] = g[r].clone();
            int got = solve(g);
            if (got != oracle(g)) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(g, before)) throw new AssertionError("grid was modified " + t);
        }
        int n = 1000;
        char[][] big = new char[n][n];
        for (char[] row : big) Arrays.fill(row, '1');
        if (solve(big) != 1) throw new AssertionError("queue version on a full board");
        boolean[][] land = new boolean[n][n];
        for (boolean[] row : land) Arrays.fill(row, true);
        Throwable[] caught = new Throwable[1];
        Thread worker = new Thread(null, () -> {
            try {
                dive(land, 0, 0);
            } catch (Throwable e) {
                caught[0] = e;
            }
        }, "dive", 1 << 20);
        worker.start();
        worker.join();
        if (!(caught[0] instanceof StackOverflowError)) throw new AssertionError("recursion should overflow");
    }
}
```

#### Solution: [Boundary] Original Color Equals New Color (Author exercise)
<!-- id: gt-same-color -->

**Approach.** With no seen table, the new colour itself is the only mark, which works only when it differs from the old one. So the method returns the image untouched when the two colours match, and otherwise paints the start and then paints each neighbor at the instant it is queued, so the eligibility gate rejects it from then on. The oracle is a repeated sweep to a fixpoint over a separate boolean table, applied to a copy. The assertions cover random grids with few colours so that equal old and new colours are common, check that the same array comes back, and show that the unguarded variant really would loop without end by counting its queue removals against a cap.

**Complexity.** Linear in the tile count for time, O(R * C), with only the queue as extra storage, which is O(R * C) in the worst case.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class SameColorSolution {
    private static final int[] DR = {0, 1, 0, -1};
    private static final int[] DC = {1, 0, -1, 0};

    static int[][] solve(int[][] image, int sr, int sc, int color) {
        int tone = image[sr][sc];
        if (tone == color) return image;
        int rows = image.length, cols = image[0].length;
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        image[sr][sc] = color;
        frontier.add(sr * cols + sc);
        while (!frontier.isEmpty()) {
            int code = frontier.poll();
            int r = code / cols, c = code % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (image[nr][nc] != tone) continue;
                image[nr][nc] = color;
                frontier.add(nr * cols + nc);
            }
        }
        return image;
    }

    static boolean unguardedLoops(int[][] image, int sr, int sc, int color, int cap) {
        int rows = image.length, cols = image[0].length, tone = image[sr][sc];
        int[][] work = new int[rows][];
        for (int r = 0; r < rows; r++) work[r] = image[r].clone();
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        frontier.add(sr * cols + sc);
        int removals = 0;
        while (!frontier.isEmpty()) {
            if (++removals > cap) return true;
            int code = frontier.poll();
            int r = code / cols, c = code % cols;
            work[r][c] = color;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (work[nr][nc] == tone) frontier.add(nr * cols + nc);
            }
        }
        return false;
    }

    static int[][] oracle(int[][] image, int sr, int sc, int color) {
        int rows = image.length, cols = image[0].length, tone = image[sr][sc];
        boolean[][] hit = new boolean[rows][cols];
        hit[sr][sc] = true;
        boolean again = true;
        while (again) {
            again = false;
            for (int c = 0; c < cols; c++) {
                for (int r = 0; r < rows; r++) {
                    if (hit[r][c] || image[r][c] != tone) continue;
                    boolean next = (r > 0 && hit[r - 1][c]) || (r + 1 < rows && hit[r + 1][c])
                            || (c > 0 && hit[r][c - 1]) || (c + 1 < cols && hit[r][c + 1]);
                    if (next) { hit[r][c] = true; again = true; }
                }
            }
        }
        int[][] out = new int[rows][];
        for (int r = 0; r < rows; r++) {
            out[r] = image[r].clone();
            for (int c = 0; c < cols; c++) if (hit[r][c]) out[r][c] = color;
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{6, 6, 2}, {2, 6, 6}};
        if (!Arrays.deepToString(solve(a, 0, 0, 6)).equals("[[6, 6, 2], [2, 6, 6]]"))
            throw new AssertionError("example 1");
        int[][] b = {{1, 1}, {1, 0}};
        if (!Arrays.deepToString(solve(b, 0, 1, 0)).equals("[[0, 0], [0, 0]]"))
            throw new AssertionError("example 2");
        if (!unguardedLoops(new int[][] {{3, 3}, {3, 3}}, 0, 0, 3, 1000))
            throw new AssertionError("equal colours without a guard never end");
        Random rnd = new Random(21503);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6), k = 2 + rnd.nextInt(2);
            int[][] img = new int[rows][cols];
            for (int[] row : img) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(k);
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(cols), color = rnd.nextInt(k);
            int[][] want = oracle(img, sr, sc, color);
            int[][] mine = new int[rows][];
            for (int r = 0; r < rows; r++) mine[r] = img[r].clone();
            int[][] got = solve(mine, sr, sc, color);
            if (got != mine) throw new AssertionError("same array expected " + t);
            if (!Arrays.deepEquals(got, want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Max Area Of Island (LeetCode 695)
<!-- id: gt-max-island-area -->

**Approach.** The scan is the same as for counting islands, but each launched traversal tallies the tiles it takes off the queue and returns that tally, and the running best keeps the larger of the old best and the new size right after the traversal ends. A grid with no land never launches one, so the best stays 0. The grid is only read, because progress lives in a private seen table. The oracle labels every tile with its own number and lowers labels across land neighbors in repeated sweeps until stable, then tallies each label and takes the biggest tally. The assertions compare the two on random grids, verify the input is unchanged, and check the all-water case.

**Complexity.** O(R * C) time for the scan plus every traversal, and O(R * C) space for the seen table and queue.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class MaxIslandAreaSolution {
    private static final int[] DR = {1, -1, 0, 0};
    private static final int[] DC = {0, 0, 1, -1};

    static int claim(int[][] grid, boolean[] seen, int start) {
        int rows = grid.length, cols = grid[0].length;
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        seen[start] = true;
        frontier.add(start);
        int size = 0;
        while (!frontier.isEmpty()) {
            int code = frontier.poll();
            size++;
            int r = code / cols, c = code % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (grid[nr][nc] != 1) continue;
                int next = nr * cols + nc;
                if (seen[next]) continue;
                seen[next] = true;
                frontier.add(next);
            }
        }
        return size;
    }

    static int solve(int[][] grid) {
        int cols = grid[0].length;
        boolean[] seen = new boolean[grid.length * cols];
        int best = 0;
        for (int start = 0; start < seen.length; start++) {
            if (seen[start] || grid[start / cols][start % cols] != 1) continue;
            best = Math.max(best, claim(grid, seen, start));
        }
        return best;
    }

    static int oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] label = new int[rows * cols];
        for (int i = 0; i < label.length; i++) label[i] = i;
        boolean shifted = true;
        while (shifted) {
            shifted = false;
            for (int r = rows - 1; r >= 0; r--) {
                for (int c = cols - 1; c >= 0; c--) {
                    if (grid[r][c] != 1) continue;
                    for (int d = 0; d < 4; d++) {
                        int nr = r + DR[d], nc = c + DC[d];
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] != 1) continue;
                        int low = Math.min(label[r * cols + c], label[nr * cols + nc]);
                        if (label[r * cols + c] != low) { label[r * cols + c] = low; shifted = true; }
                        if (label[nr * cols + nc] != low) { label[nr * cols + nc] = low; shifted = true; }
                    }
                }
            }
        }
        int[] tally = new int[rows * cols];
        int best = 0;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] != 1) continue;
                best = Math.max(best, ++tally[label[r * cols + c]]);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] one = {{0, 1, 1, 0, 0}, {0, 1, 0, 0, 1}, {1, 0, 0, 1, 1}, {1, 0, 1, 1, 0}};
        if (solve(one) != 5) throw new AssertionError("example 1");
        if (solve(new int[][] {{1, 0, 1}, {0, 1, 0}}) != 1) throw new AssertionError("example 2");
        if (solve(new int[][] {{0, 0}, {0, 0}}) != 0) throw new AssertionError("no land");
        Random rnd = new Random(21504);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            int[][] g = new int[rows][cols];
            int bias = 2 + rnd.nextInt(7);
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(10) < bias ? 1 : 0;
            int[][] before = new int[rows][];
            for (int r = 0; r < rows; r++) before[r] = g[r].clone();
            if (solve(g) != oracle(g)) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(g, before)) throw new AssertionError("grid was modified " + t);
        }
    }
}
```
