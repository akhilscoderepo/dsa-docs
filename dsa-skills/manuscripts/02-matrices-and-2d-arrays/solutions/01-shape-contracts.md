<!-- solutions-for: 01-shape-contracts -->
### Shape Contracts

#### Solution: [Build] Rectangular Sum (Author exercise)
<!-- id: mx-rectangular-sum -->

**Approach.** Return 0 when there are no rows, since then no row zero exists to read a width from. Otherwise read the width once from row zero and run the nested loops with that bound, which is legal because the contract says every row has that width. The assertions compare the result with a per-row loop on random rectangles, including the empty matrix, and confirm that `grid[0]` would have thrown on the empty input.

**Complexity.** O(rows * cols) time and O(1) extra space.

```java run
import java.util.Random;

public final class RectangularSum {
    static int rectangularSum(int[][] grid) {
        if (grid.length == 0) return 0;
        int cols = grid[0].length;
        int total = 0;
        for (int r = 0; r < grid.length; r++)
            for (int c = 0; c < cols; c++) total += grid[r][c];
        return total;
    }

    public static void main(String[] args) {
        if (rectangularSum(new int[][] {{1, 2}, {3, 4}}) != 10) throw new AssertionError("example 1");
        if (rectangularSum(new int[0][]) != 0) throw new AssertionError("example 2");
        boolean threw = false;
        int[][] none = new int[0][];
        try { int w = none[0].length; } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("reading row 0 of a matrix with no rows must throw");
        Random rnd = new Random(101);
        for (int t = 0; t < 2000; t++) {
            int rows = rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] g = new int[rows][cols];
            int expected = 0;
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) { g[r][c] = rnd.nextInt(2001) - 1000; expected += g[r][c]; }
            if (rectangularSum(g) != expected) throw new AssertionError("disagrees with the per-cell total");
        }
    }
}
```

#### Solution: [Vary] Ragged Sum (Author exercise)
<!-- id: mx-ragged-sum -->

**Approach.** Read the bound from the current row, `grid[r].length`, inside the loops. That handles rows of different lengths and empty rows with no special case. The assertions show that the first-row-width version throws on `[[1, 2], [], [3]]` and silently undercounts on `[[5], [1, 1, 1, 1]]`, then compare the safe version with a for-each total on random ragged grids.

**Complexity.** O(cells) time, where cells is the total number of entries, and O(1) extra space.

```java run
import java.util.Random;

public final class RaggedSum {
    static int raggedSum(int[][] grid) {
        int total = 0;
        for (int r = 0; r < grid.length; r++)
            for (int c = 0; c < grid[r].length; c++) total += grid[r][c];
        return total;
    }
    static int firstRowWidth(int[][] grid) {
        int total = 0;
        for (int r = 0; r < grid.length; r++)
            for (int c = 0; c < grid[0].length; c++) total += grid[r][c];
        return total;
    }

    public static void main(String[] args) {
        if (raggedSum(new int[][] {{1, 2}, {}, {3}}) != 6) throw new AssertionError("example 1");
        if (raggedSum(new int[][] {{5}, {1, 1, 1, 1}}) != 9) throw new AssertionError("example 2");
        boolean threw = false;
        try { firstRowWidth(new int[][] {{1, 2}, {}, {3}}); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("the first-row width must fail on an empty row");
        if (firstRowWidth(new int[][] {{5}, {1, 1, 1, 1}}) != 6) throw new AssertionError("the first-row width undercounts a longer row");
        Random rnd = new Random(102);
        for (int t = 0; t < 2000; t++) {
            int[][] g = new int[rnd.nextInt(6)][];
            int expected = 0;
            for (int r = 0; r < g.length; r++) {
                g[r] = new int[rnd.nextInt(5)];
                for (int c = 0; c < g[r].length; c++) { g[r][c] = rnd.nextInt(2001) - 1000; expected += g[r][c]; }
            }
            if (raggedSum(g) != expected) throw new AssertionError("disagrees with the expected total");
        }
    }
}
```

#### Solution: [Boundary] Empty Rows (Author exercise)
<!-- id: mx-empty-rows -->

**Approach.** A matrix has cells exactly when some row has a positive length, so the helper scans the rows and checks each row's own length. `new int[0][]` has length zero, so the loop body never runs and row zero does not exist, and reading it throws. `new int[][] {{}}` has length one with `grid[0].length == 0`, so reading row zero is legal and yields no cells. Both inputs report no cells, but only the second one can be read at row zero. The assertions exercise each claim directly.

**Complexity.** O(rows) time and O(1) extra space.

```java run
public final class EmptyRows {
    static boolean hasCells(int[][] grid) {
        for (int[] row : grid) if (row.length > 0) return true;
        return false;
    }

    public static void main(String[] args) {
        int[][] noRows = new int[0][];
        int[][] oneEmptyRow = new int[][] {{}};
        if (hasCells(noRows)) throw new AssertionError("no rows means no cells");
        if (hasCells(oneEmptyRow)) throw new AssertionError("one empty row means no cells");
        if (noRows.length != 0) throw new AssertionError("no rows has length 0");
        if (oneEmptyRow.length != 1 || oneEmptyRow[0].length != 0) throw new AssertionError("one empty row has length 1 and width 0");
        boolean threw = false;
        try { int w = noRows[0].length; } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("row 0 of a matrix with no rows must not be readable");
        if (!hasCells(new int[][] {{}, {7}})) throw new AssertionError("a later row can hold the only cell");
    }
}
```

#### Solution: [Recognize] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-diagonal-sum-shape -->

**Approach.** The matrix is square, so for every row `i` both `mat[i][i]` and `mat[i][n - 1 - i]` are legal reads and no per-row width is needed. Add both, then subtract the center cell once when `n` is odd, because for the middle row the two columns coincide and the cell was added twice. The assertions compare with a double loop that tests `r == c || r + c == n - 1` for each cell, which counts the center once by construction.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class MatrixDiagonalSumShape {
    static int diagonalSum(int[][] mat) {
        int n = mat.length;
        int total = 0;
        for (int i = 0; i < n; i++) total += mat[i][i] + mat[i][n - 1 - i];
        if (n % 2 == 1) total -= mat[n / 2][n / 2];
        return total;
    }
    static int oracle(int[][] mat) {
        int n = mat.length, total = 0;
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (r == c || r + c == n - 1) total += mat[r][c];
        return total;
    }

    public static void main(String[] args) {
        if (diagonalSum(new int[][] {{2, 0, 1}, {3, 5, 4}, {6, 7, 9}}) != 23) throw new AssertionError("example 1");
        if (diagonalSum(new int[][] {{4}}) != 4) throw new AssertionError("example 2");
        Random rnd = new Random(103);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] m = new int[n][n];
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) m[r][c] = 1 + rnd.nextInt(100);
            if (diagonalSum(m) != oracle(m)) throw new AssertionError("disagrees with the cell test for n = " + n);
        }
    }
}
```
