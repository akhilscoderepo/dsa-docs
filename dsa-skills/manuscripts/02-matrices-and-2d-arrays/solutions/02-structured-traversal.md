<!-- solutions-for: 02-structured-traversal -->
### Structured Traversal

#### Solution: [Build] Column Sums (Author exercise)
<!-- id: mx-column-sums -->

**Approach.** Allocate one running total per column and read the matrix in row-major order, adding each cell to the slot named by its column index. The result array has length `cols`, and no column is scanned separately. The assertions compare with a column-first double loop on random rectangles and check that the column sums add up to the total of all cells.

**Complexity.** O(rows * cols) time and O(cols) extra space for the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ColumnSums {
    static int[] columnSums(int[][] grid) {
        int[] sums = new int[grid[0].length];
        for (int[] row : grid)
            for (int c = 0; c < row.length; c++) sums[c] += row[c];
        return sums;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(columnSums(new int[][] {{1, 2, 3}, {4, 5, 6}}), new int[] {5, 7, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(columnSums(new int[][] {{8}, {2}, {5}}), new int[] {15})) throw new AssertionError("example 2");
        Random rnd = new Random(111);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] g = new int[rows][cols];
            int all = 0;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) { g[r][c] = rnd.nextInt(2001) - 1000; all += g[r][c]; }
            int[] got = columnSums(g);
            int sumOfSums = 0;
            for (int c = 0; c < cols; c++) {
                int expected = 0;
                for (int r = 0; r < rows; r++) expected += g[r][c];
                if (got[c] != expected) throw new AssertionError("column " + c);
                sumOfSums += got[c];
            }
            if (sumOfSums != all) throw new AssertionError("columns must add up to the total");
        }
    }
}
```

#### Solution: [Vary] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-diagonal-sum-formulas -->

**Approach.** In row `i` the main diagonal is column `i` and the secondary diagonal is column `n - 1 - i`. Add the first, then add the second only when it is a different column, which happens in every row except the middle row of an odd-sized matrix. This removes the separate correction for the center. The assertions compare with a cell-by-cell test on random square matrices of every size from 1 to 8.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MatrixDiagonalSumFormulas {
    static int diagonalSum(int[][] m) {
        int n = m.length, total = 0;
        for (int i = 0; i < n; i++) {
            total += m[i][i];
            int j = n - 1 - i;
            if (j != i) total += m[i][j];
        }
        return total;
    }
    static int oracle(int[][] m) {
        int n = m.length, total = 0;
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (r == c || r + c == n - 1) total += m[r][c];
        return total;
    }

    public static void main(String[] args) {
        if (diagonalSum(new int[][] {{1, 1}, {2, 3}}) != 7) throw new AssertionError("example 1");
        if (diagonalSum(new int[][] {{5, 1, 2, 1}, {1, 1, 1, 1}, {7, 1, 6, 1}, {1, 2, 1, 9}}) != 25) throw new AssertionError("example 2");
        Random rnd = new Random(112);
        for (int n = 1; n <= 8; n++) {
            for (int t = 0; t < 300; t++) {
                int[][] m = new int[n][n];
                for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) m[r][c] = 1 + rnd.nextInt(100);
                if (diagonalSum(m) != oracle(m)) throw new AssertionError("disagrees at n = " + n);
            }
        }
    }
}
```

#### Solution: [Boundary] Perimeter Sum (Author exercise)
<!-- id: mx-perimeter-sum -->

**Approach.** Add the whole top row. Add the bottom row only when there is more than one row, so a single row is not counted twice. For each middle row add the first column, and add the last column only when there is more than one column, so a single column is not counted twice. Only the ring is touched. The assertions compare with a full scan that tests whether a cell lies in the first or last row or column, over random shapes that include single rows, single columns and one cell.

**Complexity.** O(rows + cols) time and O(1) extra space.

```java run
import java.util.Random;

public final class PerimeterSum {
    static long perimeterSum(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        long total = 0;
        for (int c = 0; c < cols; c++) total += grid[0][c];
        if (rows > 1) for (int c = 0; c < cols; c++) total += grid[rows - 1][c];
        for (int r = 1; r < rows - 1; r++) {
            total += grid[r][0];
            if (cols > 1) total += grid[r][cols - 1];
        }
        return total;
    }
    static long oracle(int[][] g) {
        long total = 0;
        for (int r = 0; r < g.length; r++)
            for (int c = 0; c < g[0].length; c++)
                if (r == 0 || c == 0 || r == g.length - 1 || c == g[0].length - 1) total += g[r][c];
        return total;
    }

    public static void main(String[] args) {
        if (perimeterSum(new int[][] {{7, 8, 9}}) != 24) throw new AssertionError("example 1");
        if (perimeterSum(new int[][] {{1, 1, 1}, {1, 9, 1}, {1, 1, 1}}) != 8) throw new AssertionError("example 2");
        if (perimeterSum(new int[][] {{5}}) != 5) throw new AssertionError("one cell");
        if (perimeterSum(new int[][] {{1}, {2}, {3}}) != 6) throw new AssertionError("one column");
        Random rnd = new Random(113);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] g = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) g[r][c] = rnd.nextInt(2001) - 1000;
            if (perimeterSum(g) != oracle(g)) throw new AssertionError("disagrees on " + rows + "x" + cols);
        }
    }
}
```

#### Solution: [Recognize] Toeplitz Matrix (LeetCode 766)
<!-- id: mx-toeplitz -->

**Approach.** Every cell not in the first row or first column has exactly one predecessor on its diagonal, the cell up and to the left. If every cell equals its predecessor, then by chaining equalities every diagonal is constant, and if some cell differs from its predecessor, that diagonal is not constant. So one pass of single comparisons decides the question. The oracle is the walking check from the lesson. Random inputs are built from a vector of diagonal values, then half of them are changed in one cell, so both outcomes occur.

**Complexity.** O(rows * cols) time and O(1) extra space.

```java run
import java.util.Random;

public final class ToeplitzMatrix {
    static boolean isToeplitz(int[][] m) {
        for (int r = 1; r < m.length; r++)
            for (int c = 1; c < m[r].length; c++)
                if (m[r][c] != m[r - 1][c - 1]) return false;
        return true;
    }
    static boolean oracle(int[][] m) {
        int rows = m.length, cols = m[0].length;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                int rr = r + 1, cc = c + 1;
                while (rr < rows && cc < cols) {
                    if (m[rr][cc] != m[r][c]) return false;
                    rr++; cc++;
                }
            }
        return true;
    }

    public static void main(String[] args) {
        if (!isToeplitz(new int[][] {{3, 5, 8}, {9, 3, 5}, {4, 9, 3}})) throw new AssertionError("example 1");
        if (isToeplitz(new int[][] {{1, 2}, {2, 2}})) throw new AssertionError("example 2");
        Random rnd = new Random(114);
        int trues = 0, falses = 0;
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[] diag = new int[rows + cols];
            for (int i = 0; i < diag.length; i++) diag[i] = rnd.nextInt(10);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = diag[r - c + cols];
            if (rnd.nextBoolean()) m[rnd.nextInt(rows)][rnd.nextInt(cols)] = rnd.nextInt(10);
            boolean got = isToeplitz(m);
            if (got != oracle(m)) throw new AssertionError("disagrees with the walking check");
            if (got) trues++; else falses++;
        }
        if (trues == 0 || falses == 0) throw new AssertionError("random inputs must cover both outcomes");
    }
}
```
