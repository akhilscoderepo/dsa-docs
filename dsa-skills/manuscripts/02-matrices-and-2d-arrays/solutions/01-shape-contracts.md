<!-- solutions-for: 01-shape-contracts -->
### Solutions For Rectangular And Ragged Arrays

#### Solution: [Build] Rectangular Sum (Author exercise)
<!-- id: mx-rect-sum -->

**Approach.**
The statement promises that every row has the same length, so the column count is read once from the first row. The method returns 0 first when `grid.length` is 0, because row 0 does not exist then. The outer loop visits each row index below `grid.length`, and the inner loop visits each column index below the shared column count. The accumulator has type `long`, because 10^6 cells of magnitude 10^6 exceed the `int` range. The invariant is that after the row with index `r`, the accumulator equals the sum of rows 0 through `r`.

**Complexity.**
- **Time** is O(R * C), because each of the R rows contributes C cell reads and nothing else costs more.
- **Space** is O(1), because the method keeps one accumulator and two loop indexes.

```java run
import java.util.Random;

public final class RectSum {
    /**
     * Sums a rectangular table whose rows all share one length.
     * Time: O(R * C), one read per cell. Space: O(1), one accumulator.
     * Invariant: after row r, total equals the sum of rows 0 through r.
     */
    static long sumRectangular(int[][] grid) {
        // No rows means no first row to read, so the sum is 0 and the guard avoids grid[0].
        if (grid.length == 0) return 0;
        // The promise of equal rows lets one read of grid[0].length serve every row.
        int cols = grid[0].length;
        // A long accumulator cannot overflow here: at most 10^6 cells of magnitude 10^6.
        long total = 0;
        // The outer loop runs once per row, which costs R iterations.
        for (int r = 0; r < grid.length; r++) {
            // The inner loop runs cols times per row, so the nested cost is R * C.
            for (int c = 0; c < cols; c++) {
                // Each cell is added once; this statement runs R * C times.
                total += grid[r][c];
            }
        }
        // The accumulator now holds the sum of every row.
        return total;
    }

    public static void main(String[] args) {
        // The two examples from the statement.
        if (sumRectangular(new int[][] {{1, 2}, {3, 4}}) != 10) throw new AssertionError("example 1");
        if (sumRectangular(new int[0][]) != 0) throw new AssertionError("no rows");
        // Rows with zero columns are still a rectangle and sum to 0.
        if (sumRectangular(new int[][] {{}, {}}) != 0) throw new AssertionError("zero columns");
        // Random rectangles are checked against a for-each oracle.
        Random rnd = new Random(1);
        for (int t = 0; t < 300; t++) {
            int rows = rnd.nextInt(6), cols = rnd.nextInt(6);
            int[][] g = new int[rows][cols];
            long expect = 0;
            for (int[] row : g) for (int c = 0; c < cols; c++) { row[c] = rnd.nextInt(21) - 10; expect += row[c]; }
            if (sumRectangular(g) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Ragged Sum (Author exercise)
<!-- id: mx-ragged-sum -->

**Approach.**
Rows may differ in length, so no single column count is correct. The inner bound reads `grid[r].length` for each row. A row of length 0 makes the inner loop run zero times, and no special case is needed. The invariant is that every read uses a column below the length of the row being read.

**Complexity.**
- **Time** is O(R + N), because the outer loop runs R times and the inner loops read N cells in total.
- **Space** is O(1), because the method keeps one accumulator.

```java run
import java.util.Random;

public final class RaggedSum {
    /**
     * Sums a table whose rows may have any length, including 0.
     * Time: O(R + N), where R is the row count and N the cell count. Space: O(1).
     * Invariant: every column index is below the length of its own row.
     */
    static long sumRagged(int[][] grid) {
        // The accumulator starts at 0, which is also the answer for no rows.
        long total = 0;
        // The outer loop runs R times; an empty grid skips it.
        for (int r = 0; r < grid.length; r++) {
            // The bound is read from this row, so a short row cannot be over-read.
            for (int c = 0; c < grid[r].length; c++) {
                // Each cell is added once, so this line runs N times in total.
                total += grid[r][c];
            }
        }
        // The accumulator holds the sum of every cell of every row.
        return total;
    }

    /** Oracle: the same sum through for-each loops, which read each row's own length. */
    static long oracle(int[][] grid) {
        long s = 0;
        for (int[] row : grid) for (int v : row) s += v;
        return s;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (sumRagged(new int[][] {{1, 2}, {}, {3}}) != 6) throw new AssertionError("example 1");
        if (sumRagged(new int[][] {{}, {}}) != 0) throw new AssertionError("example 2");
        // The naive bound grid[0].length would read past row 1 here, so this input proves the fix.
        if (sumRagged(new int[][] {{1, 2, 3}, {4}}) != 10) throw new AssertionError("short second row");
        // A longer later row must not be cut off at the first row's length.
        if (sumRagged(new int[][] {{1}, {2, 3, 4}}) != 10) throw new AssertionError("long second row");
        // Random ragged tables are checked against the oracle.
        Random rnd = new Random(2);
        for (int t = 0; t < 300; t++) {
            int[][] g = new int[rnd.nextInt(6)][];
            for (int r = 0; r < g.length; r++) {
                g[r] = new int[rnd.nextInt(5)];
                for (int c = 0; c < g[r].length; c++) g[r][c] = rnd.nextInt(21) - 10;
            }
            if (sumRagged(g) != oracle(g)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty Rows (Author exercise)
<!-- id: mx-empty-rows -->

**Approach.**
The row count comes from `grid.length` alone, and the cell count comes from the lengths of the rows that exist. The method never reads `grid[0]` directly. The loop visits only indexes below `grid.length`, so `new int[0][]` yields `{0, 0}` without touching a row. The input `new int[][]{{}}` enters the loop once and adds a length of 0, so it yields `{1, 0}`. The invariant is that a row is read only after its index is proven below `grid.length`.

**Complexity.**
- **Time** is O(R), because the loop reads one length per row and never visits a cell.
- **Space** is O(1), because the result array has constant size 2.

```java run
import java.util.Random;

public final class EmptyRows {
    /**
     * Returns {number of rows, number of cells} without assuming that any row exists.
     * Time: O(R), one length read per row. Space: O(1), a result array of size 2.
     * Invariant: grid[r] is read only when r < grid.length.
     */
    static int[] shape(int[][] grid) {
        // The row count is known before any row is touched.
        int cells = 0;
        // The loop bound grid.length makes grid[r] legal on every iteration, even when it is 0.
        for (int r = 0; r < grid.length; r++) {
            // Adding the length of a row counts its cells without visiting them: O(1) per row.
            cells += grid[r].length;
        }
        // Row count and cell count are returned together.
        return new int[] {grid.length, cells};
    }

    public static void main(String[] args) {
        // No rows: grid[0] would be illegal, and the method must not read it.
        int[] a = shape(new int[0][]);
        if (a[0] != 0 || a[1] != 0) throw new AssertionError("no rows");
        // One empty row: grid[0] exists and has length 0, so the row count is 1.
        int[] b = shape(new int[][] {{}});
        if (b[0] != 1 || b[1] != 0) throw new AssertionError("one empty row");
        // The two empty forms differ, which is the point of the lesson.
        if (new int[0][].length == new int[][] {{}}.length) throw new AssertionError("forms differ");
        // Random ragged tables are checked against a counting oracle.
        Random rnd = new Random(3);
        for (int t = 0; t < 300; t++) {
            int[][] g = new int[rnd.nextInt(6)][];
            int expect = 0;
            for (int r = 0; r < g.length; r++) { g[r] = new int[rnd.nextInt(4)]; for (int v : g[r]) expect++; }
            int[] s = shape(g);
            if (s[0] != g.length || s[1] != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-diagonal-sum -->

**Approach.**
The matrix is square, so for every row `i` the columns `i` and `n - 1 - i` are both legal, and no length read is needed. The loop adds `mat[i][i]` and `mat[i][n - 1 - i]` for each row. The two coordinates are equal exactly when `i == n - 1 - i`, which happens at the center row when `n` is odd. That cell is counted twice, so the method subtracts it once after the loop. The invariant is that after row `i`, the accumulator holds both diagonal cells of rows 0 through `i`, counting a shared cell twice.

**Complexity.**
- **Time** is O(n), because the loop runs n times and reads two cells per row.
- **Space** is O(1), because the method keeps one accumulator.

```java run
import java.util.Random;

public final class DiagonalSum {
    /**
     * Sums both diagonals of a square matrix, counting the center cell once.
     * Time: O(n), two reads per row. Space: O(1).
     * Invariant: after row i, total holds both diagonal cells of rows 0 through i.
     */
    static int diagonalSum(int[][] mat) {
        // The square promise makes n the legal bound for both coordinates.
        int n = mat.length;
        int total = 0;
        // One pass over the rows costs n iterations.
        for (int i = 0; i < n; i++) {
            // Primary diagonal cell of row i, then secondary diagonal cell of row i.
            total += mat[i][i] + mat[i][n - 1 - i];
        }
        // An odd n has a center cell on both diagonals, so remove its second copy.
        if (n % 2 == 1) total -= mat[n / 2][n / 2];
        // The corrected total counts every diagonal cell once.
        return total;
    }

    /** Oracle: visits every cell and tests the two diagonal conditions. */
    static int oracle(int[][] m) {
        int s = 0, n = m.length;
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (r == c || r + c == n - 1) s += m[r][c];
        return s;
    }

    public static void main(String[] args) {
        // Statement examples: 2+5+4+1+3 and a single cell.
        if (diagonalSum(new int[][] {{2, 0, 1}, {0, 5, 0}, {3, 0, 4}}) != 15) throw new AssertionError("example 1");
        if (diagonalSum(new int[][] {{7}}) != 7) throw new AssertionError("example 2");
        // An even size has no shared cell, so nothing is subtracted.
        if (diagonalSum(new int[][] {{1, 2}, {3, 4}}) != 10) throw new AssertionError("even size");
        // Random squares of every size up to 7 are checked against the oracle.
        Random rnd = new Random(4);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] m = new int[n][n];
            for (int[] row : m) for (int c = 0; c < n; c++) row[c] = 1 + rnd.nextInt(100);
            if (diagonalSum(m) != oracle(m)) throw new AssertionError("random " + t);
        }
    }
}
```
