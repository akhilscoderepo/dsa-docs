<!-- solutions-for: 05-grid-graphs -->
### Solutions For Grid Graphs

#### Solution: [Build] Flood Fill (LeetCode 733)
<!-- id: gt-flood-fill -->

**Approach.**
The method reads the old color at the source and then runs a breadth-first search over a grid graph whose vertices are the pixels. A pixel qualifies as a neighbor when it lies inside the table, is new to the search and holds the old color. The search marks `visited` for a pixel before it enters the frontier, so each pixel enters at most once, and it recolors a pixel when the pixel leaves the frontier.

The invariant is that every id in the frontier names an in-bounds, visited pixel that holds the old color. Because the old color is read once at the start, the later recoloring does not disturb the test. The pixel id `r * cols + c` decodes back to row `id / cols` and column `id % cols`.

**Complexity.**
- **Time** is O(rows * cols), because each pixel enters the frontier at most once and each expansion tests four candidates.
- **Space** is O(rows * cols), because `visited` holds one flag per pixel and the frontier can hold many ids.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class FloodFillGrid {
    /**
     * Recolors the patch of side-connected pixels that share the color of (sr, sc).
     * Time: O(rows * cols), because each pixel is queued at most once.
     * Space: O(rows * cols), because of the visited array and the frontier.
     * Invariant: every queued id is in bounds, visited and holds the old color.
     */
    static int[][] floodFill(int[][] image, int sr, int sc, int color) {
        // Read the table size once so the loops below never touch image.length again.
        int rows = image.length, cols = image[0].length;
        // Remember the old color before any pixel changes.
        int old = image[sr][sc];
        // Row and column steps for down, up, right and left; no diagonal step is listed.
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        // One flag per pixel, so a pixel can never be queued twice.
        boolean[] visited = new boolean[rows * cols];
        // The frontier holds cell ids and avoids allocating one array per pixel.
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        // Mark the source before queuing it, which keeps the invariant true from the start.
        visited[sr * cols + sc] = true;
        frontier.add(sr * cols + sc);
        // Each loop pass expands one pixel, so the loop runs once per patch pixel.
        while (!frontier.isEmpty()) {
            // Take the oldest queued pixel.
            int cur = frontier.poll();
            // Decode the id into row and column.
            int r = cur / cols, c = cur % cols;
            // Recolor now; the test below compares with old, which is a saved copy.
            image[r][c] = color;
            // Four candidates per pixel give the constant factor in the cost.
            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                // Bounds check first, because reading outside the table throws an exception.
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                // Skip pixels that were queued before; this check bounds the total work.
                if (visited[nr * cols + nc]) continue;
                // Skip pixels of another color, so the patch stays connected through old pixels only.
                if (image[nr][nc] != old) continue;
                // Mark at queuing time so a second neighbor cannot queue the same pixel.
                visited[nr * cols + nc] = true;
                frontier.add(nr * cols + nc);
            }
        }
        // The same array comes back, now recolored.
        return image;
    }

    /** Oracle: grows the patch by repeated sweeps until no pixel joins. Time O((rows*cols)^2). */
    static int[][] oracle(int[][] image, int sr, int sc, int color) {
        int rows = image.length, cols = image[0].length;
        int old = image[sr][sc];
        boolean[][] in = new boolean[rows][cols];
        in[sr][sc] = true;
        boolean changed = true;
        // Sweep the whole table until a full sweep adds nothing.
        while (changed) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (in[r][c] || image[r][c] != old) continue;
                boolean touches = (r > 0 && in[r - 1][c]) || (r + 1 < rows && in[r + 1][c])
                        || (c > 0 && in[r][c - 1]) || (c + 1 < cols && in[r][c + 1]);
                if (touches) { in[r][c] = true; changed = true; }
            }
        }
        int[][] out = new int[rows][];
        for (int r = 0; r < rows; r++) {
            out[r] = image[r].clone();
            for (int c = 0; c < cols; c++) if (in[r][c]) out[r][c] = color;
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1 from the problem text.
        int[][] a = floodFill(new int[][] {{1, 1, 1}, {1, 1, 0}, {1, 0, 1}}, 1, 1, 2);
        if (!Arrays.deepEquals(a, new int[][] {{2, 2, 2}, {2, 2, 0}, {2, 0, 1}})) throw new AssertionError("example 1");
        // Example 2: the corner pixel keeps its color, so diagonal pixels are not neighbors.
        int[][] b = floodFill(new int[][] {{1, 0}, {0, 1}}, 0, 0, 3);
        if (!Arrays.deepEquals(b, new int[][] {{3, 0}, {0, 1}})) throw new AssertionError("example 2");
        // The method returns the same array object that it received, as the prose says.
        int[][] same = {{5}};
        if (floodFill(same, 0, 0, 6) != same) throw new AssertionError("same array returned");
        // The id round trip used in the prose: id = r * cols + c decodes with / and %.
        for (int r = 0; r < 4; r++) for (int c = 0; c < 5; c++) {
            int id = r * 5 + c;
            if (id / 5 != r || id % 5 != c) throw new AssertionError("id decode");
        }
        // Reading outside the table throws, which is why the bounds check comes first.
        boolean threw = false;
        int[][] tiny = new int[2][2];
        try { int x = tiny[2][0]; } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("out of bounds read");
        // Random tests against the sweep oracle, with few colors so patches are large.
        Random rnd = new Random(7);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] img = new int[rows][cols];
            for (int[] row : img) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(3);
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(cols), color = rnd.nextInt(4);
            int[][] expect = oracle(img, sr, sc, color);
            int[][] copy = new int[rows][];
            for (int r = 0; r < rows; r++) copy[r] = img[r].clone();
            if (!Arrays.deepEquals(floodFill(copy, sr, sc, color), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Number Of Islands (LeetCode 200)
<!-- id: gt-island-count -->

**Approach.**
The method scans the cells in row-major order. Every unvisited land cell is the source of a new island. The method then adds 1 to `count` and runs a search that marks every cell of that island. A later land cell of the same island is already visited and starts nothing.

The invariant is that after the scan passes a cell, the cell is either water or visited, and `count` equals the number of islands among the cells scanned so far. The search uses a `visited` array and leaves `grid` unchanged. Cell values are `char` values, so the test compares with `'1'` and never with the number 1.

**Complexity.**
- **Time** is O(rows * cols), because the scan visits each cell once and each cell enters a frontier at most once.
- **Space** is O(rows * cols), because the `visited` array has one flag per cell.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class CountIslands {
    /**
     * Counts the islands of land cells joined through shared sides.
     * Time: O(rows * cols), because each cell is scanned once and queued at most once.
     * Space: O(rows * cols), because of the visited array.
     * Invariant: after the scan passes a cell, that cell is water or visited.
     */
    static int countIslands(char[][] grid) {
        // Table size, read once.
        int rows = grid.length, cols = grid[0].length;
        // One flag per cell; the input array stays unchanged.
        boolean[] visited = new boolean[rows * cols];
        // Number of searches started, which equals the number of islands.
        int count = 0;
        // Scan every cell in row-major order; the two loops cost O(rows * cols).
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                // Water and already visited land start nothing.
                if (grid[r][c] != '1' || visited[r * cols + c]) continue;
                // An unvisited land cell is the source of a new island.
                count++;
                // Search marks the whole island so the scan skips its other cells later.
                ArrayDeque<int[]> frontier = new ArrayDeque<>();
                visited[r * cols + c] = true;
                frontier.add(new int[] {r, c});
                // Each cell of the island leaves the frontier exactly once.
                while (!frontier.isEmpty()) {
                    int[] cell = frontier.poll();
                    // The four side steps are written out as a pair of offsets per direction.
                    int[] dr = {1, -1, 0, 0}, dc = {0, 0, 1, -1};
                    for (int k = 0; k < 4; k++) {
                        int nr = cell[0] + dr[k], nc = cell[1] + dc[k];
                        // Bounds check before any read of grid.
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                        // Only unvisited land continues the island.
                        if (grid[nr][nc] != '1' || visited[nr * cols + nc]) continue;
                        // Mark when queued so the cell is queued once.
                        visited[nr * cols + nc] = true;
                        frontier.add(new int[] {nr, nc});
                    }
                }
            }
        }
        // Every land cell is now in exactly one counted island.
        return count;
    }

    /** Oracle: spreads the smallest cell id as a label until stable, then counts distinct land labels. */
    static int oracle(char[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] label = new int[rows * cols];
        for (int i = 0; i < label.length; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (grid[r][c] != '1') continue;
                int id = r * cols + c;
                if (r + 1 < rows && grid[r + 1][c] == '1') {
                    int m = Math.min(label[id], label[id + cols]);
                    if (label[id] != m || label[id + cols] != m) { label[id] = m; label[id + cols] = m; changed = true; }
                }
                if (c + 1 < cols && grid[r][c + 1] == '1') {
                    int m = Math.min(label[id], label[id + 1]);
                    if (label[id] != m || label[id + 1] != m) { label[id] = m; label[id + 1] = m; changed = true; }
                }
            }
        }
        java.util.HashSet<Integer> roots = new java.util.HashSet<>();
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (grid[r][c] == '1') roots.add(label[r * cols + c]);
        return roots.size();
    }

    static char[][] parse(String... rows) {
        char[][] g = new char[rows.length][];
        for (int i = 0; i < rows.length; i++) g[i] = rows[i].toCharArray();
        return g;
    }

    public static void main(String[] args) {
        // Example 1: three islands.
        if (countIslands(parse("11000", "11000", "00100", "00011")) != 3) throw new AssertionError("example 1");
        // Example 2: five single cells, since corner contact does not join them.
        if (countIslands(parse("101", "010", "101")) != 5) throw new AssertionError("example 2");
        // A map with no land has zero islands.
        if (countIslands(parse("000", "000")) != 0) throw new AssertionError("no land");
        // The char '1' differs from the int 1, so a comparison with the number would never match.
        if ('1' == 1) throw new AssertionError("char versus int");
        // The input stays unchanged after counting, as the constraints promise.
        char[][] g = parse("110", "011");
        char[][] before = {g[0].clone(), g[1].clone()};
        countIslands(g);
        if (!Arrays.deepEquals(g, before)) throw new AssertionError("grid mutated");
        // Random tests against the label oracle.
        Random rnd = new Random(11);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            char[][] m = new char[rows][cols];
            for (char[] row : m) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(100) < 45 ? '1' : '0';
            if (countIslands(m) != oracle(m)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Original Color Equals New Color (Author exercise)
<!-- id: gt-same-color -->

**Approach.**
The risky case is `color == image[sr][sc]`. A search that recolors a pixel and then tests neighbors by color finds every recolored pixel eligible again, so the frontier refills forever. The method avoids this by marking `visited` when a pixel enters the frontier and by testing eligibility against the saved old color. Each pixel enters once and receives the value it already holds. The image stays unchanged.

The invariant is that the set of visited pixels only grows and never exceeds the patch. The method needs no special branch for equal colors. The capped test in `main` shows that the version without `visited` never finishes in that case.

**Complexity.**
- **Time** is O(rows * cols), because each pixel is queued at most once, even when the new color equals the old one.
- **Space** is O(rows * cols), because `visited` and the frontier scale with the table.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class SameColorFill {
    /**
     * Recolors the side-connected patch of (sr, sc); the new color may equal the old one.
     * Time: O(rows * cols), because each pixel is queued once.
     * Space: O(rows * cols), because of the visited array and the frontier.
     * Invariant: the visited set grows by one pixel per queuing and stays inside the patch.
     */
    static int[][] fill(int[][] image, int sr, int sc, int color) {
        int rows = image.length, cols = image[0].length;
        // The saved old color is the eligibility test; the table is not consulted for it again.
        int old = image[sr][sc];
        // Visited flags replace the table colors as the record of what was reached.
        boolean[][] seen = new boolean[rows][cols];
        // The frontier holds row and column pairs for readability.
        ArrayDeque<int[]> frontier = new ArrayDeque<>();
        // Mark the source before queuing it.
        seen[sr][sc] = true;
        frontier.add(new int[] {sr, sc});
        // The loop ends when no new pixel is found, so it runs at most rows * cols times.
        while (!frontier.isEmpty()) {
            int[] p = frontier.poll();
            // Writing the same color again changes nothing, which is why equal colors are safe.
            image[p[0]][p[1]] = color;
            // Visit the four side neighbors in a fixed order.
            int[][] steps = {{p[0] + 1, p[1]}, {p[0] - 1, p[1]}, {p[0], p[1] + 1}, {p[0], p[1] - 1}};
            for (int[] q : steps) {
                // Bounds check first.
                if (q[0] < 0 || q[0] >= rows || q[1] < 0 || q[1] >= cols) continue;
                // Visited pixels are never queued again.
                if (seen[q[0]][q[1]]) continue;
                // Another color ends the patch.
                if (image[q[0]][q[1]] != old) continue;
                // Mark at queuing time.
                seen[q[0]][q[1]] = true;
                frontier.add(q);
            }
        }
        return image;
    }

    /**
     * Counts expansions of a search that tests colors only. Returns the cap when the search does not end.
     * This shows why the unguarded method fails when the colors are equal.
     */
    static int unguardedSteps(int[][] image, int sr, int sc, int color, int cap) {
        int rows = image.length, cols = image[0].length;
        int old = image[sr][sc];
        ArrayDeque<int[]> frontier = new ArrayDeque<>();
        frontier.add(new int[] {sr, sc});
        int steps = 0;
        while (!frontier.isEmpty() && steps < cap) {
            int[] p = frontier.poll();
            steps++;
            image[p[0]][p[1]] = color;
            int[][] st = {{p[0] + 1, p[1]}, {p[0] - 1, p[1]}, {p[0], p[1] + 1}, {p[0], p[1] - 1}};
            for (int[] q : st) {
                if (q[0] < 0 || q[0] >= rows || q[1] < 0 || q[1] >= cols) continue;
                if (image[q[0]][q[1]] == old) frontier.add(q);
            }
        }
        return steps;
    }

    /** Oracle: label every pixel by repeated sweeps and recolor those joined to the source. */
    static int[][] oracle(int[][] image, int sr, int sc, int color) {
        int rows = image.length, cols = image[0].length;
        int old = image[sr][sc];
        boolean[][] in = new boolean[rows][cols];
        in[sr][sc] = true;
        for (boolean changed = true; changed; ) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (in[r][c] || image[r][c] != old) continue;
                if ((r > 0 && in[r - 1][c]) || (r + 1 < rows && in[r + 1][c]) || (c > 0 && in[r][c - 1]) || (c + 1 < cols && in[r][c + 1])) {
                    in[r][c] = true;
                    changed = true;
                }
            }
        }
        int[][] out = new int[rows][];
        for (int r = 0; r < rows; r++) {
            out[r] = image[r].clone();
            for (int c = 0; c < cols; c++) if (in[r][c]) out[r][c] = color;
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: equal colors leave the image unchanged.
        if (!Arrays.deepEquals(fill(new int[][] {{0, 0}, {0, 0}}, 1, 1, 0), new int[][] {{0, 0}, {0, 0}})) throw new AssertionError("example 1");
        // Example 2: a different color recolors the whole patch.
        if (!Arrays.deepEquals(fill(new int[][] {{0, 0}, {0, 0}}, 1, 1, 1), new int[][] {{1, 1}, {1, 1}})) throw new AssertionError("example 2");
        // A search without visited flags never ends on equal colors, so it stops at the cap.
        if (unguardedSteps(new int[][] {{0, 0}, {0, 0}}, 0, 0, 0, 5000) != 5000) throw new AssertionError("unguarded should hit the cap");
        // The same unguarded search ends quickly when the colors differ.
        if (unguardedSteps(new int[][] {{0, 0}, {0, 0}}, 0, 0, 1, 5000) >= 5000) throw new AssertionError("unguarded ends on different colors");
        // Random tests, with the new color often equal to the old one.
        Random rnd = new Random(3);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] img = new int[rows][cols];
            for (int[] row : img) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(3);
            int sr = rnd.nextInt(rows), sc = rnd.nextInt(cols);
            int color = rnd.nextBoolean() ? img[sr][sc] : rnd.nextInt(4);
            int[][] expect = oracle(img, sr, sc, color);
            int[][] copy = new int[rows][];
            for (int r = 0; r < rows; r++) copy[r] = img[r].clone();
            if (!Arrays.deepEquals(fill(copy, sr, sc, color), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Max Area Of Island (LeetCode 695)
<!-- id: gt-island-area -->

**Approach.**
The method scans the cells in row-major order, as the island count does. Each unvisited land cell starts one search, and the search returns the number of cells that it marks. The method keeps the larger of that number and `best`. No island appears twice, because the first search marks every cell of its island.

The invariant is that `best` holds the largest area among the islands whose first cell the scan has already passed. The search marks the cell in `grid` by writing 0, which the constraints allow, so no separate `visited` array exists. The mark happens when a cell enters the frontier, so the area counts each cell once.

**Complexity.**
- **Time** is O(rows * cols), because each cell is scanned once and queued at most once.
- **Space** is O(rows * cols) in the worst case, because the frontier can hold a large share of the cells, while no other array is needed.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class LargestIsland {
    /**
     * Returns the largest island area, or 0 when the map has no land. The method overwrites visited land with 0.
     * Time: O(rows * cols), because each cell is queued at most once.
     * Space: O(rows * cols), because the frontier can hold many cell ids.
     * Invariant: best is the largest area among islands found so far.
     */
    static int maxArea(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int best = 0;
        // Scan all cells; each land cell met here belongs to an island that no earlier search reached.
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 0) continue;
                // Mark the source by turning it into water, then queue its id.
                grid[r][c] = 0;
                ArrayDeque<Integer> frontier = new ArrayDeque<>();
                frontier.add(r * cols + c);
                // The area counts how many ids leave the frontier.
                int area = 0;
                while (!frontier.isEmpty()) {
                    int id = frontier.poll();
                    area++;
                    int cr = id / cols, cc = id % cols;
                    // Compute the four neighbors as one flat loop over row and column deltas.
                    for (int k = 0; k < 4; k++) {
                        int nr = cr + (k == 0 ? 1 : k == 1 ? -1 : 0);
                        int nc = cc + (k == 2 ? 1 : k == 3 ? -1 : 0);
                        // Bounds check first, then the land test, which doubles as the visited test.
                        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] == 0) continue;
                        // Overwrite with 0 at queuing time so the cell is counted once.
                        grid[nr][nc] = 0;
                        frontier.add(nr * cols + nc);
                    }
                }
                // Keep the largest area seen so far.
                best = Math.max(best, area);
            }
        }
        return best;
    }

    /** Oracle: spreads the smallest id as a label until stable, then counts cells per label. */
    static int oracle(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] label = new int[rows * cols];
        for (int i = 0; i < label.length; i++) label[i] = i;
        for (boolean changed = true; changed; ) {
            changed = false;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 0) continue;
                int id = r * cols + c;
                int[] nbs = {r > 0 ? id - cols : -1, r + 1 < rows ? id + cols : -1, c > 0 ? id - 1 : -1, c + 1 < cols ? id + 1 : -1};
                for (int nb : nbs) {
                    if (nb < 0 || grid[nb / cols][nb % cols] == 0) continue;
                    int m = Math.min(label[id], label[nb]);
                    if (label[id] != m) { label[id] = m; changed = true; }
                    if (label[nb] != m) { label[nb] = m; changed = true; }
                }
            }
        }
        int[] size = new int[rows * cols];
        int best = 0;
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (grid[r][c] == 1) best = Math.max(best, ++size[label[r * cols + c]]);
        return best;
    }

    public static void main(String[] args) {
        // Example 1: the largest island has three cells.
        if (maxArea(new int[][] {{0, 1, 1, 0}, {0, 1, 0, 0}, {1, 0, 0, 1}, {1, 0, 1, 1}}) != 3) throw new AssertionError("example 1");
        // Example 2: no land gives 0.
        if (maxArea(new int[][] {{0, 0}, {0, 0}}) != 0) throw new AssertionError("example 2");
        // A full map is one island, so the area equals the number of cells.
        if (maxArea(new int[][] {{1, 1, 1}, {1, 1, 1}}) != 6) throw new AssertionError("full map");
        // The method overwrites visited land, which the prose states; the grid is all water afterwards.
        int[][] g = {{1, 0}, {1, 1}};
        maxArea(g);
        if (!Arrays.deepEquals(g, new int[][] {{0, 0}, {0, 0}})) throw new AssertionError("grid becomes water");
        // Random tests against the label oracle.
        Random rnd = new Random(5);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            int[][] m = new int[rows][cols];
            for (int[] row : m) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(100) < 50 ? 1 : 0;
            int expect = oracle(m);
            if (maxArea(m) != expect) throw new AssertionError("random " + t);
        }
    }
}
```
