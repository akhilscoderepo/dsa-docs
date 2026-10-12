<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Grid DP

#### Solution: [Build] Routes With Three Moves (Author exercise)
<!-- id: dp-grid-three-moves -->

**Approach.**
The method keeps a table `dp` where `dp[r][c]` is the number of routes that end exactly at `(r, c)`, reduced modulo 1000000007. It visits cells in reading order. A closed cell keeps 0. The start cell gets 1 when it is open. Every other open cell adds the entries of the cell above, the cell on the left and the cell on the upper left, and it skips a neighbor that lies outside the grid. Each addition happens in a `long`, and the sum is reduced once per cell.

The invariant is that when the loops reach a cell, all three possible predecessors already hold their final reduced values, since each has a smaller row or the same row with a smaller column. The reduction matters because three entries below the modulus add up to more than `Integer.MAX_VALUE`, so an `int` sum would wrap. The test below asserts that fact.

**Complexity.**
- **Time** is O(rows * cols), because each cell performs at most three additions and one reduction.
- **Space** is O(rows * cols) for the table, and the input stays unchanged.

```java run
import java.util.*;

public final class DpGridThreeMoves {
    static final int MOD = 1_000_000_007;

    /**
     * Counts routes from the top-left to the bottom-right cell using right, down and diagonal steps.
     * Time: O(rows * cols). Space: O(rows * cols).
     * Invariant: dp[r][c] is the number of routes ending exactly at (r, c), modulo MOD.
     */
    static int countRoutes(boolean[][] open) {
        int rows = open.length, cols = open[0].length;
        // The table has one long per cell, which is the O(rows * cols) memory cost.
        long[][] dp = new long[rows][cols];
        // Reading order makes every predecessor final before it is read.
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                // A closed cell cannot end a route, so its entry stays 0.
                if (!open[r][c]) continue;
                // The start has no predecessor and holds the single empty route.
                if (r == 0 && c == 0) { dp[r][c] = 1; continue; }
                long ways = 0;
                // The cell above exists only below row 0.
                if (r > 0) ways += dp[r - 1][c];
                // The cell on the left exists only right of column 0.
                if (c > 0) ways += dp[r][c - 1];
                // The upper-left cell needs both a row above and a column to the left.
                if (r > 0 && c > 0) ways += dp[r - 1][c - 1];
                // One reduction per cell keeps every stored value below MOD.
                dp[r][c] = ways % MOD;
            }
        }
        // The answer is the entry of the target cell.
        return (int) dp[rows - 1][cols - 1];
    }

    /** Oracle: plain recursion over the last step, without any stored answers. */
    static long oracle(boolean[][] open, int r, int c) {
        if (r < 0 || c < 0 || !open[r][c]) return 0;
        if (r == 0 && c == 0) return 1;
        return oracle(open, r - 1, c) + oracle(open, r, c - 1) + oracle(open, r - 1, c - 1);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countRoutes(new boolean[][] {{true, true, true}, {true, true, true}}) != 5) throw new AssertionError("ex1");
        if (countRoutes(new boolean[][] {{true, true, true}, {true, false, true}, {true, true, true}}) != 4) throw new AssertionError("ex2");
        // Java fact: three entries just below the modulus overflow an int sum but fit a long sum.
        int e = MOD - 1;
        if (e + e + e >= 0) throw new AssertionError("int sum should wrap");
        if (3L * e <= Integer.MAX_VALUE) throw new AssertionError("long sum should exceed int range");
        // Blocked start and blocked target both give 0.
        if (countRoutes(new boolean[][] {{false, true}, {true, true}}) != 0) throw new AssertionError("start");
        if (countRoutes(new boolean[][] {{true, true}, {true, false}}) != 0) throw new AssertionError("target");
        // Large open grid: the value must stay inside the modulus range.
        boolean[][] big = new boolean[300][300];
        for (boolean[] row : big) Arrays.fill(row, true);
        int bigAns = countRoutes(big);
        if (bigAns < 0 || bigAns >= MOD) throw new AssertionError("range");
        // Random small grids against the oracle, including single rows and columns.
        Random rnd = new Random(2601);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            boolean[][] g = new boolean[rows][cols];
            for (boolean[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(4) != 0;
            boolean[][] copy = new boolean[rows][];
            for (int i = 0; i < rows; i++) copy[i] = g[i].clone();
            long want = oracle(g, rows - 1, cols - 1) % MOD;
            if (countRoutes(g) != want) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(g, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Vary] Maximum Gain Path (Author exercise)
<!-- id: dp-grid-max-gain -->

**Approach.**
The table entry `best[r][c]` is the largest total over routes that end exactly at `(r, c)`. The start cell holds its own gain. A cell in row 0 can come only from the left, and a cell in column 0 can come only from above, so each takes its single predecessor. Any other cell takes the larger of the two predecessor entries and adds its own gain. The answer is the entry of the bottom-right cell.

The invariant is that every stored entry is the total of a real route, and no entry starts from a made-up zero. That is why the border cells read only the predecessor that exists. If a missing predecessor counted as 0, a cell in the first row would pretend that a route with total 0 reaches it, and the method would return 0 instead of -16 on the second example. The test below asserts this difference.

**Complexity.**
- **Time** is O(rows * cols), because each cell compares at most two entries once.
- **Space** is O(rows * cols) for the table, and the input stays unchanged.

```java run
import java.util.*;

public final class DpGridMaxGain {
    /**
     * Returns the largest total gain over right/down routes from the top-left to the bottom-right cell.
     * Time: O(rows * cols). Space: O(rows * cols).
     * Invariant: best[r][c] is the largest total of a route that ends exactly at (r, c).
     */
    static int maxGain(int[][] gain) {
        int rows = gain.length, cols = gain[0].length;
        // One int per cell stores the best total ending there.
        int[][] best = new int[rows][cols];
        // Reading order guarantees the cell above and the cell on the left are final.
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (r == 0 && c == 0) {
                    // The start route consists of the start cell alone.
                    best[r][c] = gain[r][c];
                } else if (r == 0) {
                    // First row: the only predecessor is on the left.
                    best[r][c] = best[r][c - 1] + gain[r][c];
                } else if (c == 0) {
                    // First column: the only predecessor is above.
                    best[r][c] = best[r - 1][c] + gain[r][c];
                } else {
                    // Interior: extend the better of the two real predecessors.
                    best[r][c] = Math.max(best[r - 1][c], best[r][c - 1]) + gain[r][c];
                }
            }
        }
        // The target cell holds the best total over all complete routes.
        return best[rows - 1][cols - 1];
    }

    /** Wrong variant used only in the test: a missing predecessor counts as 0. */
    static int zeroStart(int[][] gain) {
        int rows = gain.length, cols = gain[0].length;
        int[][] best = new int[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int up = r > 0 ? best[r - 1][c] : 0, left = c > 0 ? best[r][c - 1] : 0;
                best[r][c] = gain[r][c] + Math.max(up, left);
            }
        }
        return best[rows - 1][cols - 1];
    }

    /** Oracle: depth-first search over every route. */
    static int oracle(int[][] g, int r, int c) {
        if (r == g.length - 1 && c == g[0].length - 1) return g[r][c];
        int best = Integer.MIN_VALUE;
        if (r + 1 < g.length) best = Math.max(best, oracle(g, r + 1, c));
        if (c + 1 < g[0].length) best = Math.max(best, oracle(g, r, c + 1));
        return g[r][c] + best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (maxGain(new int[][] {{2, -1, 3}, {1, 4, -2}, {-3, 2, 5}}) != 14) throw new AssertionError("ex1");
        int[][] allNeg = {{-5, -2}, {-7, -9}};
        if (maxGain(allNeg) != -16) throw new AssertionError("ex2");
        // The zero-start variant returns a wrong value on the all-negative grid.
        if (zeroStart(allNeg) == -16) throw new AssertionError("zero start should differ");
        // A single cell and single lines are plain sums.
        if (maxGain(new int[][] {{-3}}) != -3) throw new AssertionError("one cell");
        if (maxGain(new int[][] {{1, -4, 2}}) != -1) throw new AssertionError("one row");
        if (maxGain(new int[][] {{1}, {-4}, {2}}) != -1) throw new AssertionError("one column");
        // Random grids with negative cells against the oracle.
        Random rnd = new Random(2602);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = rnd.nextInt(41) - 25;
            int[][] copy = new int[rows][];
            for (int i = 0; i < rows; i++) copy[i] = g[i].clone();
            if (maxGain(g) != oracle(g, 0, 0)) throw new AssertionError("random " + t);
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
