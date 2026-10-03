<!-- solutions-for: 06-marker-state -->
### Marker State

#### Solution: [Build] Mark Bad Rows (Author exercise)
<!-- id: mx-mark-bad-rows -->

**Approach.** In the observation pass, set a flag for every row that contains -1, writing nothing to the grid. In the second pass, overwrite each flagged row with zeros. For rows alone a one-pass version would also be correct, because the zeros written by clearing do not look like the -1 that is being searched for, which is why the exercise is only the foundation of the two-pass shape and not a case where it is forced. The assertions compare with a per-row check on random grids and confirm that unflagged rows are untouched.

**Complexity.** O(rows * cols) time and O(rows) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MarkBadRows {
    static void clearBadRows(int[][] grid) {
        boolean[] bad = new boolean[grid.length];
        for (int r = 0; r < grid.length; r++)
            for (int v : grid[r]) if (v == -1) bad[r] = true;
        for (int r = 0; r < grid.length; r++)
            if (bad[r]) Arrays.fill(grid[r], 0);
    }

    public static void main(String[] args) {
        int[][] a = {{4, 5}, {-1, 6}, {7, 8}};
        clearBadRows(a);
        if (!Arrays.deepEquals(a, new int[][] {{4, 5}, {0, 0}, {7, 8}})) throw new AssertionError("example 1");
        int[][] b = {{1, -1, 2}, {3, 4, -1}};
        clearBadRows(b);
        if (!Arrays.deepEquals(b, new int[][] {{0, 0, 0}, {0, 0, 0}})) throw new AssertionError("example 2");
        Random rnd = new Random(141);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols], before = new int[rows][];
            for (int r = 0; r < rows; r++) {
                for (int c = 0; c < cols; c++) g[r][c] = rnd.nextInt(8) - 1;
                before[r] = g[r].clone();
            }
            clearBadRows(g);
            for (int r = 0; r < rows; r++) {
                boolean hadMinusOne = false;
                for (int v : before[r]) if (v == -1) hadMinusOne = true;
                int[] expected = hadMinusOne ? new int[cols] : before[r];
                if (!Arrays.equals(g[r], expected)) throw new AssertionError("row " + r);
            }
        }
    }
}
```

#### Solution: [Vary] Set Matrix Zeroes (LeetCode 73)
<!-- id: mx-set-matrix-zeroes -->

**Approach.** The observation pass sets `rowHit[r]` and `colHit[c]` for every original zero and writes nothing. The second pass zeroes every cell whose row or column is marked. Clearing during the scan would turn cells that were never zero into zeros, and those would then look like original zeros and spread the clearing further. The assertions compare with the copy-based method on random matrices and show that the clear-as-you-go version gives a different, wrong answer on the first example.

**Complexity.** O(rows * cols) time and O(rows + cols) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SetMatrixZeroes {
    static void setZeroes(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        boolean[] rowHit = new boolean[rows], colHit = new boolean[cols];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) if (grid[r][c] == 0) { rowHit[r] = true; colHit[c] = true; }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) if (rowHit[r] || colHit[c]) grid[r][c] = 0;
    }
    static void clearAsYouGo(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == 0) {
                    for (int k = 0; k < cols; k++) grid[r][k] = 0;
                    for (int k = 0; k < rows; k++) grid[k][c] = 0;
                }
    }
    static int[][] copyMethod(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] out = new int[rows][];
        for (int r = 0; r < rows; r++) out[r] = grid[r].clone();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == 0) {
                    for (int k = 0; k < cols; k++) out[r][k] = 0;
                    for (int k = 0; k < rows; k++) out[k][c] = 0;
                }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{3, 4, 5}, {6, 0, 7}, {8, 9, 0}};
        setZeroes(a);
        if (!Arrays.deepEquals(a, new int[][] {{3, 0, 0}, {0, 0, 0}, {0, 0, 0}})) throw new AssertionError("example 1");
        int[][] b = {{1, 2}, {3, 4}};
        setZeroes(b);
        if (!Arrays.deepEquals(b, new int[][] {{1, 2}, {3, 4}})) throw new AssertionError("example 2");
        int[][] trapWrong = {{1, 0, 2}, {3, 4, 5}, {0, 6, 7}};
        clearAsYouGo(trapWrong);
        int[][] trapRight = {{1, 0, 2}, {3, 4, 5}, {0, 6, 7}};
        setZeroes(trapRight);
        if (!Arrays.deepEquals(trapRight, new int[][] {{0, 0, 0}, {0, 0, 5}, {0, 0, 0}})) throw new AssertionError("marker answer on the trap grid");
        if (Arrays.deepEquals(trapWrong, trapRight)) throw new AssertionError("clearing as you go must over-clear on the trap grid");
        if (trapWrong[1][2] != 0) throw new AssertionError("the over-clearing zeroes column 2, which held no original zero");
        Random rnd = new Random(142);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) g[r][c] = rnd.nextInt(4);
            int[][] expected = copyMethod(g);
            setZeroes(g);
            if (!Arrays.deepEquals(g, expected)) throw new AssertionError("disagrees with the copy-based method");
        }
    }
}
```

#### Solution: [Boundary] Set Matrix Zeroes In Constant Space (LeetCode 73)
<!-- id: mx-set-zeroes-constant -->

**Approach.** Before borrowing the first row and first column, record in two flags whether each held a zero. For every interior cell with value zero, write a zero into its row marker in column 0 and its column marker in row 0. Then clear every interior cell whose row marker or column marker is zero. Finally clear the first row if its flag is set and the first column if its flag is set. Skipping the flags misses a zero that sat in the first row or column, because it cannot be told apart from a marker, and clearing the first row and column before the interior destroys the markers before they are read. The assertions show both mistakes failing and compare the correct version with the copy-based method on random matrices.

**Complexity.** O(rows * cols) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SetZeroesConstant {
    static void setZeroes(int[][] m) {
        int rows = m.length, cols = m[0].length;
        boolean firstRowZero = false, firstColZero = false;
        for (int c = 0; c < cols; c++) if (m[0][c] == 0) firstRowZero = true;
        for (int r = 0; r < rows; r++) if (m[r][0] == 0) firstColZero = true;
        for (int r = 1; r < rows; r++)
            for (int c = 1; c < cols; c++) if (m[r][c] == 0) { m[r][0] = 0; m[0][c] = 0; }
        for (int r = 1; r < rows; r++)
            for (int c = 1; c < cols; c++) if (m[r][0] == 0 || m[0][c] == 0) m[r][c] = 0;
        if (firstRowZero) for (int c = 0; c < cols; c++) m[0][c] = 0;
        if (firstColZero) for (int r = 0; r < rows; r++) m[r][0] = 0;
    }
    static void withoutFlags(int[][] m) {
        int rows = m.length, cols = m[0].length;
        for (int r = 1; r < rows; r++)
            for (int c = 1; c < cols; c++) if (m[r][c] == 0) { m[r][0] = 0; m[0][c] = 0; }
        for (int r = 1; r < rows; r++)
            for (int c = 1; c < cols; c++) if (m[r][0] == 0 || m[0][c] == 0) m[r][c] = 0;
    }
    static void clearFirstEarly(int[][] m) {
        int rows = m.length, cols = m[0].length;
        boolean firstRowZero = false, firstColZero = false;
        for (int c = 0; c < cols; c++) if (m[0][c] == 0) firstRowZero = true;
        for (int r = 0; r < rows; r++) if (m[r][0] == 0) firstColZero = true;
        for (int r = 1; r < rows; r++)
            for (int c = 1; c < cols; c++) if (m[r][c] == 0) { m[r][0] = 0; m[0][c] = 0; }
        if (firstRowZero) for (int c = 0; c < cols; c++) m[0][c] = 0;
        if (firstColZero) for (int r = 0; r < rows; r++) m[r][0] = 0;
        for (int r = 1; r < rows; r++)
            for (int c = 1; c < cols; c++) if (m[r][0] == 0 || m[0][c] == 0) m[r][c] = 0;
    }
    static int[][] copyMethod(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] out = new int[rows][];
        for (int r = 0; r < rows; r++) out[r] = grid[r].clone();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (grid[r][c] == 0) {
                    for (int k = 0; k < cols; k++) out[r][k] = 0;
                    for (int k = 0; k < rows; k++) out[k][c] = 0;
                }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2}, {0, 4}};
        setZeroes(a);
        if (!Arrays.deepEquals(a, new int[][] {{0, 2}, {0, 0}})) throw new AssertionError("example 1");
        int[][] b = {{5, 0}, {6, 7}};
        setZeroes(b);
        if (!Arrays.deepEquals(b, new int[][] {{0, 0}, {6, 0}})) throw new AssertionError("example 2");
        int[][] noFlags = {{1, 2}, {0, 4}};
        withoutFlags(noFlags);
        if (Arrays.deepEquals(noFlags, new int[][] {{0, 2}, {0, 0}})) throw new AssertionError("without the flags the first column's zero is not spread to row 0");
        int[][] early = {{0, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        clearFirstEarly(early);
        if (Arrays.deepEquals(early, new int[][] {{0, 0, 0}, {0, 5, 6}, {0, 8, 9}})) throw new AssertionError("clearing the first row early must destroy the markers");
        int[][] ok = {{0, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        setZeroes(ok);
        if (!Arrays.deepEquals(ok, new int[][] {{0, 0, 0}, {0, 5, 6}, {0, 8, 9}})) throw new AssertionError("the correct order keeps the markers");
        Random rnd = new Random(143);
        for (int t = 0; t < 5000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] g = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) g[r][c] = rnd.nextInt(4);
            int[][] expected = copyMethod(g);
            setZeroes(g);
            if (!Arrays.deepEquals(g, expected)) throw new AssertionError("disagrees with the copy-based method");
        }
    }
}
```

#### Solution: [Recognize] Game of Life (LeetCode 289)
<!-- id: mx-game-of-life -->

**Approach.** Encode each cell as `old + 2 * new`. The first sweep counts live neighbors using only the low bit of every neighbor, so a neighbor that already carries its new state still reports its old one, and it sets the second bit on cells that will be alive. The second sweep shifts every cell right by one, leaving the new generation. The rules are applied to the old state only. The assertions compare with the two-board method on random boards, check that the encoded values stay in the range 0 to 3 during the first sweep, and verify both examples.

**Complexity.** O(rows * cols) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class GameOfLife {
    static void step(int[][] board) {
        int rows = board.length, cols = board[0].length;
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                int live = 0;
                for (int dr = -1; dr <= 1; dr++)
                    for (int dc = -1; dc <= 1; dc++) {
                        int nr = r + dr, nc = c + dc;
                        if ((dr != 0 || dc != 0) && nr >= 0 && nr < rows && nc >= 0 && nc < cols) live += board[nr][nc] & 1;
                    }
                boolean alive = (board[r][c] & 1) == 1;
                boolean next = alive ? (live == 2 || live == 3) : live == 3;
                if (next) board[r][c] |= 2;
                if (board[r][c] < 0 || board[r][c] > 3) throw new AssertionError("encoded state out of range");
            }
        for (int[] row : board) for (int c = 0; c < cols; c++) row[c] >>= 1;
    }
    static int[][] twoBoards(int[][] b) {
        int rows = b.length, cols = b[0].length;
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                int live = 0;
                for (int dr = -1; dr <= 1; dr++)
                    for (int dc = -1; dc <= 1; dc++) {
                        int nr = r + dr, nc = c + dc;
                        if ((dr != 0 || dc != 0) && nr >= 0 && nr < rows && nc >= 0 && nc < cols) live += b[nr][nc];
                    }
                out[r][c] = b[r][c] == 1 ? ((live == 2 || live == 3) ? 1 : 0) : (live == 3 ? 1 : 0);
            }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 1}, {1, 0}};
        step(a);
        if (!Arrays.deepEquals(a, new int[][] {{1, 1}, {1, 1}})) throw new AssertionError("example 1");
        int[][] b = {{0, 1, 0}, {0, 1, 0}, {0, 1, 0}};
        step(b);
        if (!Arrays.deepEquals(b, new int[][] {{0, 0, 0}, {1, 1, 1}, {0, 0, 0}})) throw new AssertionError("example 2");
        Random rnd = new Random(144);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] g = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) g[r][c] = rnd.nextInt(2);
            int[][] expected = twoBoards(g);
            step(g);
            if (!Arrays.deepEquals(g, expected)) throw new AssertionError("disagrees with the two-board method");
        }
    }
}
```
