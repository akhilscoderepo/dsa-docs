<!-- solutions-for: 07-two-dimensional-prefix -->
### Two-Dimensional Prefix

#### Solution: [Build] Range Sum Query 2D - Immutable (LeetCode 304)
<!-- id: ps-range-sum-2d -->

**Approach.** The constructor builds a table with one extra row and one extra column of zeros, in which entry `[r + 1][c + 1]` is the total of every cell from the top-left corner through `(r, c)`. Each entry is the cell plus the entry above plus the entry to the left, minus the entry diagonally above-left, which both neighbors include. A request for the rectangle from `(r1, c1)` to `(r2, c2)` starts from the entry at the bottom-right of the block, removes the strip above it and the strip to its left, and adds back the corner that was removed twice. The oracle adds the cells of the rectangle one by one.

**Complexity.** Setup is O(R C) time and space, and each request is O(1).

```java run
import java.util.Random;

public final class RangeSum2D {
    static final class NumMatrix {
        private final long[][] p;
        NumMatrix(int[][] m) {
            int rows = m.length, cols = m[0].length;
            p = new long[rows + 1][cols + 1];
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++)
                    p[r + 1][c + 1] = m[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c];
        }
        int sumRegion(int r1, int c1, int r2, int c2) {
            return (int) (p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1]);
        }
    }

    public static void main(String[] args) {
        int[][] ex = {{3, 0, 1, 4}, {5, 6, 3, 2}, {1, 2, 0, 1}};
        NumMatrix nm = new NumMatrix(ex);
        if (nm.sumRegion(1, 1, 2, 2) != 11) throw new AssertionError("example 1");
        if (nm.sumRegion(0, 0, 2, 3) != 28) throw new AssertionError("example 2");
        if (nm.sumRegion(0, 3, 0, 3) != 4) throw new AssertionError("a corner cell");
        Random rnd = new Random(7901);
        for (int t = 0; t < 300; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = rnd.nextInt(2001) - 1000;
            NumMatrix x = new NumMatrix(m);
            for (int r1 = 0; r1 < rows; r1++)
                for (int r2 = r1; r2 < rows; r2++)
                    for (int c1 = 0; c1 < cols; c1++)
                        for (int c2 = c1; c2 < cols; c2++) {
                            int s = 0;
                            for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) s += m[r][c];
                            if (x.sumRegion(r1, c1, r2, c2) != s) throw new AssertionError("differs for " + r1 + "," + c1 + "," + r2 + "," + c2);
                        }
        }
    }
}
```

#### Solution: [Vary] Matrix Block Sum (LeetCode 1314)
<!-- id: ps-matrix-block-sum -->

**Approach.** The window around a cell is a rectangle whose limits are the cell's row and column plus and minus `k`, so one padded table answers every cell. Near the border the window would leave the grid, and it must be clipped with `Math.max` against zero for the top and left limits and `Math.min` against the last row and column for the bottom and right limits, because cells outside the matrix contribute nothing. The clipped limits are inclusive and feed the four-corner formula. The oracle sums the clipped window directly for each cell.

**Complexity.** O(R C) time and space, independent of `k`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MatrixBlockSum {
    static int[][] matrixBlockSum(int[][] m, int k) {
        int rows = m.length, cols = m[0].length;
        long[][] p = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                p[r + 1][c + 1] = m[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c];
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int r1 = Math.max(0, r - k), c1 = Math.max(0, c - k);
                int r2 = Math.min(rows - 1, r + k), c2 = Math.min(cols - 1, c + k);
                out[r][c] = (int) (p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1]);
            }
        }
        return out;
    }
    static int[][] oracle(int[][] m, int k) {
        int rows = m.length, cols = m[0].length;
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                for (int i = Math.max(0, r - k); i <= Math.min(rows - 1, r + k); i++)
                    for (int j = Math.max(0, c - k); j <= Math.min(cols - 1, c + k); j++) out[r][c] += m[i][j];
        return out;
    }

    public static void main(String[] args) {
        int[][] one = matrixBlockSum(new int[][] {{1, 0, 2}, {3, 1, 0}, {0, 4, 1}}, 1);
        if (!Arrays.deepEquals(one, new int[][] {{5, 7, 3}, {9, 12, 8}, {8, 9, 6}})) throw new AssertionError("example 1");
        int[][] two = matrixBlockSum(new int[][] {{1, 2}, {3, 4}}, 5);
        if (!Arrays.deepEquals(two, new int[][] {{10, 10}, {10, 10}})) throw new AssertionError("example 2");
        Random rnd = new Random(7902);
        for (int t = 0; t < 1500; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = 1 + rnd.nextInt(100);
            int k = rnd.nextInt(8);
            if (!Arrays.deepEquals(matrixBlockSum(m, k), oracle(m, k))) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Single Cell Rectangle (Author exercise)
<!-- id: ps-single-cell-rectangle -->

**Approach.** For a rectangle with `r1 == r2` and `c1 == c2`, the four entries read are the corner-anchored totals through the cell, through the cell above it in the same column, through the cell to its left in the same row, and through the diagonal cell. The formula `P[r+1][c+1] - P[r][c+1] - P[r+1][c] + P[r][c]` is the same expression that built the table entry, rearranged, so it returns the cell exactly, whatever its sign and whatever its position. The program checks every cell of random matrices, including all four corners and cells with large negative values, and the table uses `long` so that values near a billion do not wrap.

**Complexity.** O(R C) to build and O(1) per request.

```java run
import java.util.Random;

public final class SingleCellRectangle {
    static long[][] build(int[][] m) {
        int rows = m.length, cols = m[0].length;
        long[][] p = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                p[r + 1][c + 1] = m[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c];
        return p;
    }
    static long region(long[][] p, int r1, int c1, int r2, int c2) {
        return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1];
    }

    public static void main(String[] args) {
        int[][] ex = {{5, -2}, {3, 4}};
        long[][] p = build(ex);
        if (region(p, 0, 1, 0, 1) != -2) throw new AssertionError("example 1");
        if (region(p, 1, 0, 1, 0) != 3) throw new AssertionError("example 2");
        Random rnd = new Random(7903);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = rnd.nextInt(2000000001) - 1000000000;
            long[][] q = build(m);
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++)
                    if (region(q, r, c, r, c) != m[r][c]) throw new AssertionError("cell " + r + "," + c + " differs");
        }
    }
}
```

#### Solution: [Recognize] Whole Matrix Query (Author exercise)
<!-- id: ps-whole-matrix-query -->

**Approach.** For the request `(0, 0, rows - 1, cols - 1)`, the first corner is the last entry of the table, which holds the total of the whole matrix. The other three corners read row zero or column zero of the table, which is the sentinel border and holds zeros, so the answer is the last entry itself, and no index below zero is read. A request covering the whole first row subtracts nothing above it, since the row above is the zero border, and a request covering the whole first column subtracts nothing to its left for the same reason. The program checks these three families against sums computed directly, and checks the single-cell matrix.

**Complexity.** O(R C) to build and O(1) per request.

```java run
import java.util.Random;

public final class WholeMatrixQuery {
    static long[][] build(int[][] m) {
        int rows = m.length, cols = m[0].length;
        long[][] p = new long[rows + 1][cols + 1];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                p[r + 1][c + 1] = m[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c];
        return p;
    }
    static long region(long[][] p, int r1, int c1, int r2, int c2) {
        return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1];
    }

    public static void main(String[] args) {
        if (region(build(new int[][] {{2, 3}, {4, 5}}), 0, 0, 1, 1) != 14) throw new AssertionError("example 1");
        if (region(build(new int[][] {{7}}), 0, 0, 0, 0) != 7) throw new AssertionError("example 2");
        Random rnd = new Random(7904);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] m = new int[rows][cols];
            long total = 0;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) { m[r][c] = rnd.nextInt(2000000001) - 1000000000; total += m[r][c]; }
            long[][] p = build(m);
            if (region(p, 0, 0, rows - 1, cols - 1) != total) throw new AssertionError("whole matrix differs");
            if (p[rows][cols] != total) throw new AssertionError("the last entry is the total");
            long firstRow = 0, firstCol = 0;
            for (int c = 0; c < cols; c++) firstRow += m[0][c];
            for (int r = 0; r < rows; r++) firstCol += m[r][0];
            if (region(p, 0, 0, 0, cols - 1) != firstRow) throw new AssertionError("first row differs");
            if (region(p, 0, 0, rows - 1, 0) != firstCol) throw new AssertionError("first column differs");
        }
    }
}
```
