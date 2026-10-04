<!-- solutions-for: 02-structured-traversal -->
### Solutions For Walking Rows, Columns And Diagonals

#### Solution: [Build] Column Sums (Author exercise)
<!-- id: mx-column-sums -->

**Approach.**
The answer array has one slot per column, so its length comes from the first row, and an input with no rows returns an empty array before that read. The outer loop visits each row, and the inner loop adds each cell to the slot that has the same column index. The invariant is that after row `r`, slot `c` holds the sum of the cells in column `c` of rows 0 through `r`.

**Complexity.**
- **Time** is O(R * C), because each cell is added to one slot exactly once.
- **Space** is O(C), because the result array holds one `long` per column.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ColumnSums {
    /**
     * Returns one sum per column of a rectangular matrix.
     * Time: O(R * C), one addition per cell. Space: O(C), the result array.
     * Invariant: after row r, sums[c] equals the column-c total of rows 0 through r.
     */
    static long[] columnSums(int[][] grid) {
        // With no rows, the column count is unknown and the contract asks for an empty array.
        if (grid.length == 0) return new long[0];
        // One slot per column is the only allocation.
        long[] sums = new long[grid[0].length];
        // The outer loop runs once per row.
        for (int r = 0; r < grid.length; r++) {
            // The inner loop writes slot c, so the column index selects the answer slot.
            for (int c = 0; c < sums.length; c++) sums[c] += grid[r][c];
        }
        // Each slot now holds a complete column total.
        return sums;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (!Arrays.equals(columnSums(new int[][] {{1, 2, 3}, {4, 5, 6}}), new long[] {5, 7, 9})) throw new AssertionError("example 1");
        if (columnSums(new int[0][]).length != 0) throw new AssertionError("no rows");
        // Random rectangles are checked against a column-first oracle.
        Random rnd = new Random(11);
        for (int t = 0; t < 300; t++) {
            int R = 1 + rnd.nextInt(5), C = 1 + rnd.nextInt(5);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(21) - 10;
            long[] expect = new long[C];
            for (int c = 0; c < C; c++) for (int r = 0; r < R; r++) expect[c] += g[r][c];
            if (!Arrays.equals(columnSums(g), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-rect-diagonals -->

**Approach.**
Both lines have `k = min(R, C)` cells, because the first line runs out of rows or columns after `k` steps and the second one does as well. The loop runs `i` from 0 to `k - 1` and adds `grid[i][i]` and `grid[i][C - 1 - i]`. The two cells are the same cell exactly when `i == C - 1 - i`. That equation has a solution only when `C` is odd, and the solution counts only when it is below `k`. The method subtracts the shared cell once in that case. The invariant is that after step `i`, the total holds both cells of steps 0 through `i`, with a shared cell counted twice.

**Complexity.**
- **Time** is O(min(R, C)), because the loop runs `k` times and reads two cells per step.
- **Space** is O(1), because the method keeps one accumulator.

```java run
import java.util.Random;

public final class RectDiagonals {
    /**
     * Sums the two lines of length min(R, C) that start at the top corners.
     * Time: O(min(R, C)). Space: O(1).
     * Invariant: after step i, total holds both cells of steps 0 through i.
     */
    static int sumLines(int[][] grid) {
        // The shorter side limits both lines.
        int k = Math.min(grid.length, grid[0].length);
        int cols = grid[0].length;
        int total = 0;
        // The loop runs k times, so cost does not depend on the longer side.
        for (int i = 0; i < k; i++) {
            // The first term walks down and right, and the second walks down and left.
            total += grid[i][i] + grid[i][cols - 1 - i];
            // At a shared cell both terms named the same cell, so remove the second copy.
            if (i == cols - 1 - i) total -= grid[i][i];
        }
        // Every cell on either line is counted once.
        return total;
    }

    /** Oracle: visits every cell and tests the two line conditions with the same k. */
    static int oracle(int[][] g) {
        int R = g.length, C = g[0].length, k = Math.min(R, C), s = 0;
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) {
            boolean first = r == c && r < k;
            boolean second = c == C - 1 - r && r < k;
            if (first || second) s += g[r][c];
        }
        return s;
    }

    public static void main(String[] args) {
        // The statement examples; the second has a shared cell.
        if (sumLines(new int[][] {{1, 2, 3, 4}, {5, 6, 7, 8}}) != 18) throw new AssertionError("example 1");
        if (sumLines(new int[][] {{1, 2, 3}, {4, 5, 6}}) != 9) throw new AssertionError("example 2");
        // A tall matrix has k equal to the column count.
        if (sumLines(new int[][] {{1, 2}, {3, 4}, {5, 6}}) != 10) throw new AssertionError("tall");
        // Random rectangles of both orientations are checked against the oracle.
        Random rnd = new Random(12);
        for (int t = 0; t < 400; t++) {
            int R = 1 + rnd.nextInt(6), C = 1 + rnd.nextInt(6);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(41) - 20;
            if (sumLines(g) != oracle(g)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Perimeter Sum (Author exercise)
<!-- id: mx-border-sum -->

**Approach.**
The method adds the top row first. When `R > 1`, it adds the bottom row as well, so a one-row matrix does not count its row twice. Then it adds the left column and, when `C > 1`, the right column, but only for the rows strictly between the top and the bottom, because the corners are already counted. The loop for the side columns runs from row 1 to row `R - 2`, so it is empty when `R <= 2`. The invariant is that each border cell is added by exactly one of the four passes.

**Complexity.**
- **Time** is O(R + C), because two passes cover `C` cells each and two cover at most `R - 2` cells each.
- **Space** is O(1), because the method keeps one accumulator.

```java run
import java.util.Random;

public final class BorderSum {
    /**
     * Sums every cell with r == 0, r == R-1, c == 0 or c == C-1, each cell once.
     * Time: O(R + C). Space: O(1).
     * Invariant: each border cell is added by exactly one of the four passes.
     */
    static long borderSum(int[][] grid) {
        int R = grid.length, C = grid[0].length;
        long total = 0;
        // The top row is always part of the border.
        for (int c = 0; c < C; c++) total += grid[0][c];
        // The bottom row is a separate row only when R > 1; otherwise it is the top row again.
        if (R > 1) for (int c = 0; c < C; c++) total += grid[R - 1][c];
        // Middle rows contribute their first cell; corners are already counted, so r skips 0 and R-1.
        for (int r = 1; r < R - 1; r++) total += grid[r][0];
        // The last column is separate only when C > 1; otherwise it is the first column again.
        if (C > 1) for (int r = 1; r < R - 1; r++) total += grid[r][C - 1];
        // Four passes cover the border once each, so the cost is about 2C + 2R.
        return total;
    }

    /** Oracle: scans every cell and tests the border condition once per cell. */
    static long oracle(int[][] g) {
        long s = 0;
        int R = g.length, C = g[0].length;
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) if (r == 0 || r == R - 1 || c == 0 || c == C - 1) s += g[r][c];
        return s;
    }

    public static void main(String[] args) {
        // Statement examples: a 3 by 3 and a single row.
        if (borderSum(new int[][] {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}) != 40) throw new AssertionError("example 1");
        if (borderSum(new int[][] {{4, 6, 1, 2}}) != 13) throw new AssertionError("example 2");
        // A single column and a single cell must not double count.
        if (borderSum(new int[][] {{1}, {2}, {3}}) != 6) throw new AssertionError("single column");
        if (borderSum(new int[][] {{9}}) != 9) throw new AssertionError("single cell");
        // Random shapes from 1 by 1 to 6 by 6 are checked against the oracle.
        Random rnd = new Random(13);
        for (int t = 0; t < 400; t++) {
            int R = 1 + rnd.nextInt(6), C = 1 + rnd.nextInt(6);
            int[][] g = new int[R][C];
            for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(41) - 20;
            if (borderSum(g) != oracle(g)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Toeplitz Matrix (LeetCode 766)
<!-- id: mx-toeplitz -->

**Approach.**
Every cell not in row 0 or column 0 has a predecessor at `(r - 1, c - 1)` on the same diagonal. The loops start at row 1 and column 1, so the predecessor index is never negative. If every such cell equals its predecessor, then every cell on a diagonal equals the first cell of that diagonal, by induction along the diagonal. The method returns false at the first mismatch. The invariant is that when the loop reaches `(r, c)`, all cells above and left of it already match their predecessors.

**Complexity.**
- **Time** is O(R * C), because each cell is compared once with one neighbor.
- **Space** is O(1), because the method stores only the loop indexes.

```java run
import java.util.Random;

public final class Toeplitz {
    /**
     * Tests whether every top-left to bottom-right diagonal holds one value.
     * Time: O(R * C), one comparison per cell. Space: O(1).
     * Invariant: at (r, c), every earlier cell already equals its up-left predecessor.
     */
    static boolean isToeplitz(int[][] g) {
        // Row 0 has no predecessor row, so the scan starts at row 1.
        for (int r = 1; r < g.length; r++) {
            // Column 0 has no predecessor column, so the scan starts at column 1.
            for (int c = 1; c < g[r].length; c++) {
                // One mismatch with the predecessor breaks the diagonal, so the answer is final.
                if (g[r][c] != g[r - 1][c - 1]) return false;
            }
        }
        // No mismatch means every diagonal is constant.
        return true;
    }

    /** Oracle: walks the full diagonal from every cell, as the naive method does. */
    static boolean oracle(int[][] g) {
        for (int r = 0; r < g.length; r++) for (int c = 0; c < g[0].length; c++)
            for (int i = r + 1, j = c + 1; i < g.length && j < g[0].length; i++, j++) if (g[i][j] != g[r][c]) return false;
        return true;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (!isToeplitz(new int[][] {{3, 5, 1}, {2, 3, 5}, {9, 2, 3}})) throw new AssertionError("example 1");
        if (isToeplitz(new int[][] {{1, 2, 4}, {5, 1, 2}, {9, 5, 7}})) throw new AssertionError("example 2");
        // A single row or a single column has no predecessor pair, so it passes.
        if (!isToeplitz(new int[][] {{1, 2, 3}})) throw new AssertionError("single row");
        if (!isToeplitz(new int[][] {{1}, {2}})) throw new AssertionError("single column");
        // Random small matrices over two values hit both outcomes often.
        Random rnd = new Random(14);
        for (int t = 0; t < 600; t++) {
            int R = 1 + rnd.nextInt(4), C = 1 + rnd.nextInt(4);
            int[][] g = new int[R][C];
            if (rnd.nextBoolean()) { // build a Toeplitz matrix from first row and column values
                int[] seed = new int[R + C - 1];
                for (int i = 0; i < seed.length; i++) seed[i] = rnd.nextInt(3);
                for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) g[r][c] = seed[c - r + R - 1];
            } else for (int[] row : g) for (int c = 0; c < C; c++) row[c] = rnd.nextInt(2);
            if (isToeplitz(g) != oracle(g)) throw new AssertionError("random " + t);
        }
    }
}
```
