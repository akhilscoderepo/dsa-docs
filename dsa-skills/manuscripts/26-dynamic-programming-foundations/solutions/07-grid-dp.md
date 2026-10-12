<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Grid DP

#### Solution: [Build] Unique Paths (LeetCode 62)
<!-- id: dp-grid-unique-paths -->

**Approach.**
The table entry `ways[r][c]` is the number of routes that end exactly at `(r, c)`. Every cell in row 0 and column 0 has a single predecessor direction and no shelf, so the method sets those entries to 1 before the main loops. Each interior cell then adds the entry above it and the entry on its left. The answer is the entry of the bottom-right cell.

The invariant is that the loops read only entries with a smaller row, or the same row and a smaller column, so every read value is final. The two sets of routes entering a cell from above and from the left are disjoint, so the sum counts each route once. The result fits in an `int` by the stated guarantee, and the test cross-checks the table against the binomial coefficient computed in a `long`.

**Complexity.**
- **Time** is O(m * n), because each interior cell does one addition.
- **Space** is O(m * n) for the table.

```java run
import java.util.*;

public final class DpGridUniquePaths {
    /**
     * Counts right/down routes across an open m by n grid.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: ways[r][c] is the number of routes ending exactly at (r, c).
     */
    static int uniquePaths(int m, int n) {
        // One int per cell.
        int[][] ways = new int[m][n];
        // Border cells have a single predecessor direction, so each holds exactly one route.
        for (int r = 0; r < m; r++) ways[r][0] = 1;
        for (int c = 0; c < n; c++) ways[0][c] = 1;
        // Interior cells combine the two earlier neighbors.
        for (int r = 1; r < m; r++) {
            for (int c = 1; c < n; c++) {
                // Routes from above and routes from the left never overlap.
                ways[r][c] = ways[r - 1][c] + ways[r][c - 1];
            }
        }
        // The target holds the answer.
        return ways[m - 1][n - 1];
    }

    /** Oracle: choose which of the m + n - 2 steps go down, using an exact binomial coefficient. */
    static long oracle(int m, int n) {
        long result = 1;
        int k = Math.min(m - 1, n - 1), total = m + n - 2;
        for (int i = 1; i <= k; i++) result = result * (total - k + i) / i;
        return result;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (uniquePaths(3, 4) != 10) throw new AssertionError("ex1");
        if (uniquePaths(1, 6) != 1) throw new AssertionError("ex2");
        // One cell and one column.
        if (uniquePaths(1, 1) != 1) throw new AssertionError("one cell");
        if (uniquePaths(7, 1) != 1) throw new AssertionError("column");
        // Every size up to 12 by 12 against the binomial oracle; larger sizes stay within long.
        for (int m = 1; m <= 12; m++) for (int n = 1; n <= 12; n++) {
            if (uniquePaths(m, n) != oracle(m, n)) throw new AssertionError(m + "x" + n);
        }
        // Random sizes against a plain recursion on the last step.
        Random rnd = new Random(2601);
        for (int t = 0; t < 300; t++) {
            int m = 1 + rnd.nextInt(8), n = 1 + rnd.nextInt(8);
            if (uniquePaths(m, n) != rec(m - 1, n - 1)) throw new AssertionError("random " + t);
        }
    }

    static long rec(int r, int c) {
        if (r == 0 || c == 0) return 1;
        return rec(r - 1, c) + rec(r, c - 1);
    }
}
```

#### Solution: [Vary] Minimum Path Sum (LeetCode 64)
<!-- id: dp-grid-min-path-sum -->

**Approach.**
The entry `cost[r][c]` is the smallest sum over routes that end exactly at `(r, c)`. The start holds its own value. A cell in row 0 can come only from the left, and a cell in column 0 only from above, so each adds its value to that single predecessor. An interior cell adds its value to the smaller of the two predecessor entries. The answer is the bottom-right entry.

The invariant is that every entry is the sum of a real route. A border cell must not take a minimum against a missing neighbor, because a stand-in of 0 would look cheaper than every real route and produce a wrong sum. The test builds that wrong variant and asserts that it differs on a positive grid.

**Complexity.**
- **Time** is O(m * n), because each cell compares at most two entries.
- **Space** is O(m * n) for the table, and the input stays unchanged.

```java run
import java.util.*;

public final class DpGridMinPathSum {
    /**
     * Returns the smallest sum over right/down routes from the top-left to the bottom-right cell.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: cost[r][c] is the smallest sum of a route ending exactly at (r, c).
     */
    static int minPathSum(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        // One int per cell.
        int[][] cost = new int[m][n];
        cost[0][0] = grid[0][0];
        // First row: the only predecessor is on the left.
        for (int c = 1; c < n; c++) cost[0][c] = cost[0][c - 1] + grid[0][c];
        // First column: the only predecessor is above.
        for (int r = 1; r < m; r++) cost[r][0] = cost[r - 1][0] + grid[r][0];
        // Interior cells extend the cheaper of two real predecessors.
        for (int r = 1; r < m; r++) {
            for (int c = 1; c < n; c++) {
                cost[r][c] = grid[r][c] + Math.min(cost[r - 1][c], cost[r][c - 1]);
            }
        }
        // The target holds the cheapest total.
        return cost[m - 1][n - 1];
    }

    /** Wrong variant used only in the test: a missing predecessor counts as 0. */
    static int zeroPad(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] cost = new int[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                int up = r > 0 ? cost[r - 1][c] : 0, left = c > 0 ? cost[r][c - 1] : 0;
                cost[r][c] = grid[r][c] + Math.min(up, left);
            }
        }
        return cost[m - 1][n - 1];
    }

    /** Oracle: depth-first search over every route. */
    static int oracle(int[][] g, int r, int c) {
        if (r == g.length - 1 && c == g[0].length - 1) return g[r][c];
        int best = Integer.MAX_VALUE;
        if (r + 1 < g.length) best = Math.min(best, oracle(g, r + 1, c));
        if (c + 1 < g[0].length) best = Math.min(best, oracle(g, r, c + 1));
        return g[r][c] + best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minPathSum(new int[][] {{4, 1, 6}, {2, 7, 3}, {5, 2, 1}}) != 14) throw new AssertionError("ex1");
        if (minPathSum(new int[][] {{3, 9, 1, 2}}) != 15) throw new AssertionError("ex2");
        // The zero-padded variant is wrong on a positive grid.
        if (zeroPad(new int[][] {{3, 9, 1, 2}}) == 15) throw new AssertionError("zero pad should differ");
        // One cell and one column.
        if (minPathSum(new int[][] {{7}}) != 7) throw new AssertionError("one cell");
        if (minPathSum(new int[][] {{1}, {4}, {2}}) != 7) throw new AssertionError("column");
        // Random grids against the oracle; the input must stay unchanged.
        Random rnd = new Random(2602);
        for (int t = 0; t < 3000; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] g = new int[m][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(30);
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = g[i].clone();
            if (minPathSum(g) != oracle(g, 0, 0)) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(g, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Boundary] First Row And Column (Author exercise)
<!-- id: dp-grid-border-counts -->

**Approach.**
Only the first row and the first column are needed, and each border cell has a single predecessor direction. The method fills an array `row` for row 0 and an array `col` for column 0. If the start is blocked, both lines stay all zero. Otherwise the start holds 1. Each next cell in row 0 copies the count of its left neighbor when it is open, and stores 0 when it is blocked. Column 0 does the same with the cell above.

The invariant is that `row[j]` equals the number of routes to `(0, j)`, which is 1 until the first shelf and 0 from the shelf onward. A shelf cuts the line because no other predecessor exists on the border. The result lists `row` completely and then `col` from index 1, so the corner appears once, and the length is `rows + cols - 1`.

**Complexity.**
- **Time** is O(rows + cols), because each border cell is read once.
- **Space** is O(rows + cols) for the returned array, and the input stays unchanged.

```java run
import java.util.*;

public final class DpGridBorderCounts {
    /**
     * Returns route counts for the first row, then for the first column below the corner.
     * Time: O(rows + cols). Space: O(rows + cols).
     * Invariant: out[k] is the number of right/down routes to the k-th border cell in the listed order.
     */
    static long[] borderCounts(boolean[][] blocked) {
        int rows = blocked.length, cols = blocked[0].length;
        // The result holds one slot per listed border cell.
        long[] out = new long[rows + cols - 1];
        // A blocked start leaves every count at 0.
        if (blocked[0][0]) return out;
        // The start cell has exactly one route.
        out[0] = 1;
        // Row 0: each cell depends only on its left neighbor.
        for (int c = 1; c < cols; c++) {
            // A shelf stores 0, and an open cell inherits the count to its left.
            out[c] = blocked[0][c] ? 0 : out[c - 1];
        }
        // Column 0: each cell depends only on the cell above, which is the previous listed entry.
        long above = 1;
        for (int r = 1; r < rows; r++) {
            // A shelf stores 0, and later cells in the column then see 0 above them.
            above = blocked[r][0] ? 0 : above;
            out[cols - 1 + r] = above;
        }
        // The array is built from the border alone, so the interior was never read.
        return out;
    }

    /** Oracle: recursion over the last step for each border cell. */
    static long ways(boolean[][] b, int r, int c) {
        if (r < 0 || c < 0 || b[r][c]) return 0;
        if (r == 0 && c == 0) return 1;
        return ways(b, r - 1, c) + ways(b, r, c - 1);
    }

    static long[] oracle(boolean[][] b) {
        int rows = b.length, cols = b[0].length;
        long[] out = new long[rows + cols - 1];
        for (int c = 0; c < cols; c++) out[c] = ways(b, 0, c);
        for (int r = 1; r < rows; r++) out[cols - 1 + r] = ways(b, r, 0);
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(borderCounts(new boolean[][] {{false, false, true, false}, {false, false, false, false}}), new long[] {1, 1, 0, 0, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(borderCounts(new boolean[][] {{false}, {true}, {false}}), new long[] {1, 0, 0})) throw new AssertionError("ex2");
        // A blocked start gives all zeros, and a one-cell grid gives a single 1.
        if (!Arrays.equals(borderCounts(new boolean[][] {{true, false}, {false, false}}), new long[] {0, 0, 0})) throw new AssertionError("blocked start");
        if (!Arrays.equals(borderCounts(new boolean[][] {{false}}), new long[] {1})) throw new AssertionError("one cell");
        // Random grids against the oracle, including inputs that stay unchanged.
        Random rnd = new Random(2603);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            boolean[][] g = new boolean[rows][cols];
            for (boolean[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(5) == 0;
            boolean[][] copy = new boolean[rows][];
            for (int i = 0; i < rows; i++) copy[i] = g[i].clone();
            if (!Arrays.equals(borderCounts(g), oracle(g))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(g, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Recognize] Unique Paths With Obstacles (LeetCode 63)
<!-- id: dp-grid-blocked-cells -->

**Approach.**
The state is the same as before: `ways[r][c]` counts routes that end exactly at `(r, c)`. With only right and down moves, a cell has at most two predecessors, the cell above and the cell on the left. An obstacle cell stores 0, so nothing flows through it. The start stores 1 when it is empty, and the answer is the entry of the bottom-right cell. A grid that has an obstacle on the start or the target yields 0 without any special case, because the start stores 0 and the target stores 0.

The invariant is that every entry is final when the loops reach the cells that read it. A route to a cell enters from above or from the left, and these two sets of routes are disjoint, so their counts add without double counting. The guarantee that the answer fits in an `int` also bounds every intermediate entry, because each entry is at most the answer of a larger cell only when that cell is reachable. The test keeps grids small and checks the table against direct recursion.

**Complexity.**
- **Time** is O(m * n), because each cell adds at most two entries.
- **Space** is O(m * n) for the table, and the input stays unchanged.

```java run
import java.util.*;

public final class DpGridBlockedCells {
    /**
     * Counts right/down routes that avoid obstacle cells.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: ways[r][c] is the number of routes ending exactly at (r, c), and obstacles store 0.
     */
    static int uniquePathsWithObstacles(int[][] obstacleGrid) {
        int m = obstacleGrid.length, n = obstacleGrid[0].length;
        // One int per cell, filled in reading order.
        int[][] ways = new int[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                // An obstacle keeps 0, which blocks every route through the cell.
                if (obstacleGrid[r][c] == 1) continue;
                // An empty start holds the single empty route.
                if (r == 0 && c == 0) { ways[r][c] = 1; continue; }
                int total = 0;
                // Routes entering from above exist only below row 0.
                if (r > 0) total += ways[r - 1][c];
                // Routes entering from the left exist only right of column 0.
                if (c > 0) total += ways[r][c - 1];
                ways[r][c] = total;
            }
        }
        // The target entry is the answer, and it is 0 when the start or target holds an obstacle.
        return ways[m - 1][n - 1];
    }

    /** Oracle: enumerate every route with recursion on the last step. */
    static int oracle(int[][] g, int r, int c) {
        if (r < 0 || c < 0 || g[r][c] == 1) return 0;
        if (r == 0 && c == 0) return 1;
        return oracle(g, r - 1, c) + oracle(g, r, c - 1);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (uniquePathsWithObstacles(new int[][] {{0, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 0, 0}}) != 4) throw new AssertionError("ex1");
        if (uniquePathsWithObstacles(new int[][] {{0, 1}, {0, 0}}) != 1) throw new AssertionError("ex2");
        // Obstacle on the start, obstacle on the target, and a wall that cuts every route.
        if (uniquePathsWithObstacles(new int[][] {{1, 0}, {0, 0}}) != 0) throw new AssertionError("start");
        if (uniquePathsWithObstacles(new int[][] {{0, 0}, {0, 1}}) != 0) throw new AssertionError("target");
        if (uniquePathsWithObstacles(new int[][] {{0, 0, 0}, {1, 1, 1}, {0, 0, 0}}) != 0) throw new AssertionError("wall");
        // One-row and one-column grids.
        if (uniquePathsWithObstacles(new int[][] {{0, 0, 0}}) != 1) throw new AssertionError("row");
        if (uniquePathsWithObstacles(new int[][] {{0}, {1}, {0}}) != 0) throw new AssertionError("column");
        // Random grids against the oracle.
        Random rnd = new Random(2604);
        for (int t = 0; t < 3000; t++) {
            int m = 1 + rnd.nextInt(7), n = 1 + rnd.nextInt(7);
            int[][] g = new int[m][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(4) == 0 ? 1 : 0;
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = g[i].clone();
            if (uniquePathsWithObstacles(g) != oracle(g, m - 1, n - 1)) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(g, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```
