<!-- solutions-for: 06-marker-state -->
### Solutions For Marking Before Clearing

#### Solution: [Build] Mark Bad Rows (Author exercise)
<!-- id: mx-mark-bad-rows -->

**Approach.**
The first pass reads every cell and sets `bad[r]` when row `r` holds `-1`. It writes nothing into the matrix. The second pass walks the rows, and for each row with `bad[r]` set, it writes zero into every cell and adds one to the count. The invariant after the first pass is that `bad[r]` is true exactly when row `r` of the input held `-1`. Keeping the passes apart means the second pass cannot change what the first pass reads.

**Complexity.**
- **Time** is O(rows * cols), because each pass visits each cell at most once.
- **Space** is O(rows), because `bad` holds one boolean per row.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MarkBadRows {
    /**
     * Clears every row that contains -1 and returns how many rows were cleared.
     * Time: O(rows * cols). Space: O(rows) for the boolean array.
     * Invariant: after pass one, bad[r] is true exactly when input row r held -1.
     */
    static int clearBadRows(int[][] m) {
        boolean[] bad = new boolean[m.length];
        // Pass one reads only: each cell is visited once, which costs rows * cols.
        for (int r = 0; r < m.length; r++) {
            for (int c = 0; c < m[r].length; c++) {
                // A single -1 is enough to mark the row.
                if (m[r][c] == -1) bad[r] = true;
            }
        }
        int count = 0;
        // Pass two writes only: it never looks for -1 again.
        for (int r = 0; r < m.length; r++) {
            if (bad[r]) {
                // Each bad row is cleared once, and the count equals the number of true entries.
                Arrays.fill(m[r], 0);
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // Statement examples.
        int[][] a = {{1, 2}, {3, -1}, {5, 6}};
        if (clearBadRows(a) != 1 || !Arrays.deepEquals(a, new int[][] {{1, 2}, {0, 0}, {5, 6}})) throw new AssertionError("example 1");
        int[][] b = {{-1, -1}, {2, -1}};
        if (clearBadRows(b) != 2 || !Arrays.deepEquals(b, new int[][] {{0, 0}, {0, 0}})) throw new AssertionError("example 2");
        // A matrix without -1 stays unchanged and returns zero.
        int[][] none = {{1, 2}, {3, 4}};
        if (clearBadRows(none) != 0 || !Arrays.deepEquals(none, new int[][] {{1, 2}, {3, 4}})) throw new AssertionError("no bad rows");
        // Random matrices are compared with a row-by-row oracle.
        Random rnd = new Random(61);
        for (int t = 0; t < 300; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] m = new int[rows][cols], expect = new int[rows][cols];
            int bad = 0;
            for (int r = 0; r < rows; r++) {
                boolean has = false;
                for (int c = 0; c < cols; c++) {
                    m[r][c] = rnd.nextInt(6) - 1;
                    expect[r][c] = m[r][c];
                    if (m[r][c] == -1) has = true;
                }
                if (has) { Arrays.fill(expect[r], 0); bad++; }
            }
            if (clearBadRows(m) != bad || !Arrays.deepEquals(m, expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Set Matrix Zeroes (LeetCode 73)
<!-- id: mx-set-zeroes -->

**Approach.**
The observation pass reads each cell of the unchanged input and sets `rowMark[r]` and `colMark[c]` when it finds a zero at `(r, c)`. The update pass then writes zero into every cell whose row mark or column mark is set. Zeros written by the update pass never trigger more clearing, because the update pass does not test cell values. The invariant after the observation pass is that each mark is true exactly when its line held a zero in the input.

**Complexity.**
- **Time** is O(rows * cols), because both passes visit every cell once.
- **Space** is O(rows + cols), because the two arrays hold one boolean per row and per column.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SetZeroes {
    /**
     * Sets the row and column of every input zero to zero, in place.
     * Time: O(rows * cols). Space: O(rows + cols).
     * Invariant: after pass one, each mark is true exactly when its line held a zero in the input.
     */
    static void setZeroes(int[][] m) {
        int rows = m.length, cols = m[0].length;
        boolean[] rowMark = new boolean[rows];
        boolean[] colMark = new boolean[cols];
        // Observation pass: reads every cell once and writes only to the marks.
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (m[r][c] == 0) {
                    // A zero marks its row and its column, and the matrix stays unchanged.
                    rowMark[r] = true;
                    colMark[c] = true;
                }
            }
        }
        // Update pass: writes zero wherever a mark applies and never tests a cell value.
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (rowMark[r] || colMark[c]) m[r][c] = 0;
            }
        }
    }

    static int[][] oracle(int[][] m) {
        int rows = m.length, cols = m[0].length;
        int[][] out = new int[rows][];
        for (int r = 0; r < rows; r++) out[r] = m[r].clone();
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                // The oracle clears from the untouched input for each zero, which costs more time.
                if (m[r][c] == 0) {
                    for (int k = 0; k < cols; k++) out[r][k] = 0;
                    for (int k = 0; k < rows; k++) out[k][c] = 0;
                }
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // Statement examples.
        int[][] a = {{5, 0, 6}, {7, 8, 9}, {1, 2, 3}};
        setZeroes(a);
        if (!Arrays.deepEquals(a, new int[][] {{0, 0, 0}, {7, 0, 9}, {1, 0, 3}})) throw new AssertionError("example 1");
        int[][] b = {{1, 2, 3, 4}, {5, 0, 7, 8}, {9, 10, 0, 12}};
        setZeroes(b);
        if (!Arrays.deepEquals(b, new int[][] {{1, 0, 0, 4}, {0, 0, 0, 0}, {0, 0, 0, 0}})) throw new AssertionError("example 2");
        // The failure case from the lesson: one zero must not spread to column 1.
        int[][] c1 = {{0, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        setZeroes(c1);
        if (!Arrays.deepEquals(c1, new int[][] {{0, 0, 0}, {0, 5, 6}, {0, 8, 9}})) throw new AssertionError("no spread");
        // Integer.MIN_VALUE is an ordinary non-zero value.
        int[][] mn = {{Integer.MIN_VALUE, 1}, {2, 0}};
        setZeroes(mn);
        if (!Arrays.deepEquals(mn, new int[][] {{Integer.MIN_VALUE, 0}, {0, 0}})) throw new AssertionError("min value");
        // Random rectangles are compared with the oracle.
        Random rnd = new Random(62);
        for (int t = 0; t < 400; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = rnd.nextInt(4);
            int[][] expect = oracle(m);
            setZeroes(m);
            if (!Arrays.deepEquals(m, expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Constant-Space Variant (LeetCode 73)
<!-- id: mx-set-zeroes-constant -->

**Approach.**
The method saves two booleans first. `firstRow` records whether row 0 held a zero in the input, and `firstCol` records the same for column 0. The observation pass then covers the cells with `r >= 1` and `c >= 1`. A zero there writes zero into `m[r][0]` and `m[0][c]`, which turns the first column and the first row into the markers. The update pass again covers only the cells with `r >= 1` and `c >= 1`, and clears a cell when its first-column cell or its first-row cell is zero. The first row and the first column are cleared last, based on the two saved booleans, because their cells held the markers until then. The invariant before the last step is that every cell outside the first row and column has its final value.

**Complexity.**
- **Time** is O(rows * cols), because each loop visits each cell at most a constant number of times.
- **Space** is O(1), because the method keeps two booleans and loop indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SetZeroesConstant {
    /**
     * Sets the row and column of every input zero to zero, using the first row and column as markers.
     * Time: O(rows * cols). Space: O(1).
     * Invariant: before the final two loops, every cell with r >= 1 and c >= 1 holds its final value.
     */
    static void setZeroes(int[][] m) {
        int rows = m.length, cols = m[0].length;
        boolean firstRow = false, firstCol = false;
        // Save whether row 0 held a zero, because its cells are about to become markers.
        for (int c = 0; c < cols; c++) if (m[0][c] == 0) firstRow = true;
        // Save whether column 0 held a zero, for the same reason.
        for (int r = 0; r < rows; r++) if (m[r][0] == 0) firstCol = true;
        // Observation pass over the inner cells: a zero marks its line in the first row and first column.
        for (int r = 1; r < rows; r++) {
            for (int c = 1; c < cols; c++) {
                if (m[r][c] == 0) {
                    m[r][0] = 0;
                    m[0][c] = 0;
                }
            }
        }
        // Update pass over the inner cells: a marker in the first column or first row clears the cell.
        for (int r = 1; r < rows; r++) {
            for (int c = 1; c < cols; c++) {
                if (m[r][0] == 0 || m[0][c] == 0) m[r][c] = 0;
            }
        }
        // The first row is cleared only now, because earlier loops still read its markers.
        if (firstRow) for (int c = 0; c < cols; c++) m[0][c] = 0;
        // The first column is cleared last for the same reason.
        if (firstCol) for (int r = 0; r < rows; r++) m[r][0] = 0;
    }

    static int[][] oracle(int[][] m) {
        int rows = m.length, cols = m[0].length;
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                boolean clear = false;
                // A cell clears when its row or its column holds an input zero.
                for (int k = 0; k < cols; k++) if (m[r][k] == 0) clear = true;
                for (int k = 0; k < rows; k++) if (m[k][c] == 0) clear = true;
                out[r][c] = clear ? 0 : m[r][c];
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // Statement examples, one with a zero in the first row and one with a zero in the first column.
        int[][] a = {{8, 0, 1}, {2, 3, 4}};
        setZeroes(a);
        if (!Arrays.deepEquals(a, new int[][] {{0, 0, 0}, {2, 0, 4}})) throw new AssertionError("example 1");
        int[][] b = {{3, 4}, {0, 5}, {6, 7}};
        setZeroes(b);
        if (!Arrays.deepEquals(b, new int[][] {{0, 4}, {0, 0}, {0, 7}})) throw new AssertionError("example 2");
        // A single cell and a single row or column are boundary shapes.
        int[][] one = {{0}};
        setZeroes(one);
        if (one[0][0] != 0) throw new AssertionError("single zero");
        int[][] row = {{1, 0, 2}};
        setZeroes(row);
        if (!Arrays.deepEquals(row, new int[][] {{0, 0, 0}})) throw new AssertionError("single row");
        int[][] col = {{1}, {0}, {2}};
        setZeroes(col);
        if (!Arrays.deepEquals(col, new int[][] {{0}, {0}, {0}})) throw new AssertionError("single column");
        // Random rectangles are compared with the oracle.
        Random rnd = new Random(63);
        for (int t = 0; t < 600; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = rnd.nextInt(4);
            int[][] expect = oracle(m);
            setZeroes(m);
            if (!Arrays.deepEquals(m, expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Game Of Life (LeetCode 289)
<!-- id: mx-game-of-life -->

**Approach.**
Each cell stores its old state in bit 0. The first pass counts the live neighbors of each cell by reading `m[nr][nc] & 1`, which ignores any bit 1 that earlier steps already wrote. When the rule makes the cell live in the next generation, the pass sets bit 1 with `m[r][c] |= 2`. The second pass shifts every cell right by one bit, which discards the old state and keeps the new state. The invariant during the first pass is that bit 0 of every cell still holds the old generation.

**Complexity.**
- **Time** is O(rows * cols), because each cell inspects at most 8 neighbors and the shift pass visits each cell once.
- **Space** is O(1), because the two states share one `int` per cell.

```java run
import java.util.Arrays;
import java.util.Random;

public final class GameOfLife {
    /**
     * Advances a Game of Life board one generation in place.
     * Time: O(rows * cols), at most 8 reads per cell. Space: O(1), two bits per cell.
     * Invariant: while the first pass runs, bit 0 of every cell holds the old state.
     */
    static void step(int[][] m) {
        int rows = m.length, cols = m[0].length;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int live = 0;
                // Visit the up to eight neighbors, which costs a constant number of reads per cell.
                for (int dr = -1; dr <= 1; dr++) {
                    for (int dc = -1; dc <= 1; dc++) {
                        if (dr == 0 && dc == 0) continue;
                        int nr = r + dr, nc = c + dc;
                        // Bounds come first so that an edge cell never reads outside the matrix.
                        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) live += m[nr][nc] & 1;
                    }
                }
                // Masking with & 1 keeps the read on the old generation even after bit 1 is set.
                boolean old = (m[r][c] & 1) == 1;
                if (old ? (live == 2 || live == 3) : live == 3) m[r][c] |= 2;
            }
        }
        // The shift moves the new state into bit 0 and drops the old state.
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) m[r][c] >>= 1;
        }
    }

    static int[][] oracle(int[][] m) {
        int rows = m.length, cols = m[0].length;
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int live = 0;
                for (int dr = -1; dr <= 1; dr++) {
                    for (int dc = -1; dc <= 1; dc++) {
                        int nr = r + dr, nc = c + dc;
                        // The oracle reads the untouched input and writes a separate matrix.
                        if ((dr != 0 || dc != 0) && nr >= 0 && nr < rows && nc >= 0 && nc < cols) live += m[nr][nc];
                    }
                }
                out[r][c] = (live == 3 || (m[r][c] == 1 && live == 2)) ? 1 : 0;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // Statement examples.
        int[][] a = {{0, 0, 0, 0}, {0, 1, 1, 1}, {1, 1, 1, 0}, {0, 0, 0, 0}};
        step(a);
        if (!Arrays.deepEquals(a, new int[][] {{0, 0, 1, 0}, {1, 0, 0, 1}, {1, 0, 0, 1}, {0, 1, 0, 0}})) throw new AssertionError("example 1");
        int[][] b = {{0, 1, 1}, {1, 0, 0}, {0, 0, 0}};
        step(b);
        if (!Arrays.deepEquals(b, new int[][] {{0, 1, 0}, {0, 1, 0}, {0, 0, 0}})) throw new AssertionError("example 2");
        // A 1 x 1 board has no neighbors, so a live cell dies.
        int[][] one = {{1}};
        step(one);
        if (one[0][0] != 0) throw new AssertionError("single cell");
        // A 2 x 2 block of live cells is stable.
        int[][] block = {{1, 1}, {1, 1}};
        step(block);
        if (!Arrays.deepEquals(block, new int[][] {{1, 1}, {1, 1}})) throw new AssertionError("block");
        // Random boards are compared with the copy-based oracle.
        Random rnd = new Random(64);
        for (int t = 0; t < 500; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = rnd.nextInt(2);
            int[][] expect = oracle(m);
            step(m);
            if (!Arrays.deepEquals(m, expect)) throw new AssertionError("random " + t);
        }
    }
}
```
