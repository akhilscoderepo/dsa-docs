<!-- solutions-for: 05-matrix-rotation -->
### Solutions For Rotating A Square

#### Solution: [Build] Transpose Square (Author exercise)
<!-- id: mx-transpose-square -->

**Approach.**
The cell `(r, c)` and the cell `(c, r)` exchange values, and the cells with `r == c` stay. The outer loop picks a row `r`. The inner loop starts at `c = r + 1`, so it visits only cells above the main diagonal and each mirrored pair exactly once. Visiting every cell would swap each pair twice and restore the input. The invariant is that after row `r`, every pair whose smaller index is at most `r` has been swapped once.

**Complexity.**
- **Time** is O(n^2), because the loops perform about `n * (n - 1) / 2` swaps.
- **Space** is O(1), because each swap uses one temporary value.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TransposeSquare {
    /**
     * Transposes a square matrix in place.
     * Time: O(n^2), about n(n-1)/2 swaps. Space: O(1), one temporary value.
     * Invariant: after row r, each pair with smaller index at most r is swapped once.
     */
    static void transpose(int[][] m) {
        int n = m.length;
        // The outer loop picks the row of the upper cell in each pair.
        for (int r = 0; r < n; r++) {
            // Starting at r + 1 skips the main diagonal and visits each pair once.
            for (int c = r + 1; c < n; c++) {
                // Swap the mirrored cells through one temporary value.
                int tmp = m[r][c];
                m[r][c] = m[c][r];
                m[c][r] = tmp;
            }
        }
    }

    public static void main(String[] args) {
        // Statement examples.
        int[][] a = {{1, 2}, {3, 4}};
        transpose(a);
        if (!Arrays.deepEquals(a, new int[][] {{1, 3}, {2, 4}})) throw new AssertionError("example 1");
        int[][] b = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        transpose(b);
        if (!Arrays.deepEquals(b, new int[][] {{1, 4, 7}, {2, 5, 8}, {3, 6, 9}})) throw new AssertionError("example 2");
        // A single cell is its own mirror.
        int[][] one = {{5}};
        transpose(one);
        if (one[0][0] != 5) throw new AssertionError("single cell");
        // Random squares are compared with a copy-based oracle, and a second transpose restores the input.
        Random rnd = new Random(31);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] m = new int[n][n], orig = new int[n][n], expect = new int[n][n];
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) { m[r][c] = rnd.nextInt(100); orig[r][c] = m[r][c]; }
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) expect[c][r] = orig[r][c];
            transpose(m);
            if (!Arrays.deepEquals(m, expect)) throw new AssertionError("random " + t);
            transpose(m);
            if (!Arrays.deepEquals(m, orig)) throw new AssertionError("double transpose " + t);
        }
    }
}
```

#### Solution: [Vary] Rotate Image (LeetCode 48)
<!-- id: mx-rotate-image -->

**Approach.**
The method transposes the matrix, which sends `(r, c)` to `(c, r)`, and then reverses each row, which sends `(c, r)` to `(c, n - 1 - r)`. The composition sends the original cell `(r, c)` to `(c, n - 1 - r)`, which is the clockwise quarter turn. Both steps swap mirrored pairs, so the method needs one temporary value. The invariant after the first pass is that the matrix equals the transpose of the input, and after the second pass it equals the quarter turn.

**Complexity.**
- **Time** is O(n^2), because the first pass swaps about `n^2 / 2` pairs and the second pass swaps about `n^2 / 2` pairs.
- **Space** is O(1), because each swap uses one temporary value.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotateImage {
    /**
     * Rotates a square matrix a quarter turn clockwise in place.
     * Time: O(n^2). Space: O(1).
     * Invariant: after pass one the matrix is the transpose, after pass two it is the rotation.
     */
    static void rotate(int[][] m) {
        int n = m.length;
        // Pass one: swap each mirrored pair across the main diagonal once.
        for (int r = 0; r < n; r++) {
            for (int c = r + 1; c < n; c++) {
                int tmp = m[r][c];
                m[r][c] = m[c][r];
                m[c][r] = tmp;
            }
        }
        // Pass two: reverse each row by swapping its two ends and moving inward.
        for (int[] row : m) {
            // lo rises and hi falls, so the loop stops at the middle and costs n / 2 swaps per row.
            for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) {
                int tmp = row[lo];
                row[lo] = row[hi];
                row[hi] = tmp;
            }
        }
    }

    public static void main(String[] args) {
        // Statement examples.
        int[][] a = {{1, 2}, {3, 4}};
        rotate(a);
        if (!Arrays.deepEquals(a, new int[][] {{3, 1}, {4, 2}})) throw new AssertionError("example 1");
        int[][] b = {{2, 4, 6}, {8, 1, 3}, {5, 7, 9}};
        rotate(b);
        if (!Arrays.deepEquals(b, new int[][] {{5, 8, 2}, {7, 1, 4}, {9, 3, 6}})) throw new AssertionError("example 2");
        // Four rotations restore the matrix, and the odd center never moves.
        int[][] c = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        for (int i = 0; i < 4; i++) { rotate(c); if (c[1][1] != 5) throw new AssertionError("center moved"); }
        if (!Arrays.deepEquals(c, new int[][] {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}})) throw new AssertionError("four turns");
        // Random squares are compared with the copy-based formula from the lesson.
        Random rnd = new Random(32);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] m = new int[n][n], expect = new int[n][n];
            for (int r = 0; r < n; r++) for (int col = 0; col < n; col++) m[r][col] = rnd.nextInt(100);
            for (int r = 0; r < n; r++) for (int col = 0; col < n; col++) expect[col][n - 1 - r] = m[r][col];
            rotate(m);
            if (!Arrays.deepEquals(m, expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Odd Center (Author exercise)
<!-- id: mx-odd-center -->

**Approach.**
A cell `(r, c)` is fixed when `(c, n - 1 - r)` equals `(r, c)`. That requires `r == c` and `c == n - 1 - r`, so `2r = n - 1`. A whole-number solution exists only when `n` is odd, and then it is the single center cell `r = (n - 1) / 2`. The answer is `n * n - 1` for odd `n` and `n * n` for even `n`. The method uses `long` arithmetic, because `n * n` reaches 10^18, which fits in a `long` but not in an `int`. The invariant is that the count of fixed cells is the number of solutions of `2r = n - 1` with `0 <= r < n`.

**Complexity.**
- **Time** is O(1), because the formula uses one comparison and one multiplication.
- **Space** is O(1), because the method stores no matrix.

```java run
public final class OddCenter {
    /**
     * Counts the cells that move under a clockwise quarter turn of an n by n matrix.
     * Time: O(1). Space: O(1).
     * Invariant: a cell is fixed exactly when 2r = n - 1, so at most one cell is fixed.
     */
    static long movedCells(long n) {
        // The product needs a long: n * n reaches 10^18 when n is 10^9.
        long all = n * n;
        // An odd n has exactly one fixed cell, the center, and an even n has none.
        return n % 2 == 1 ? all - 1 : all;
    }

    /** Oracle: rotates a matrix of distinct values by the mapping and counts positions whose value changed. */
    static int oracle(int n) {
        int[][] m = new int[n][n], rot = new int[n][n];
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) m[r][c] = r * n + c;
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) rot[c][n - 1 - r] = m[r][c];
        int moved = 0;
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) if (rot[r][c] != m[r][c]) moved++;
        return moved;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (movedCells(3) != 8) throw new AssertionError("example 1");
        if (movedCells(4) != 16) throw new AssertionError("example 2");
        // A single cell is fixed, so no cell moves.
        if (movedCells(1) != 0) throw new AssertionError("n=1");
        // The largest size must not overflow.
        if (movedCells(1_000_000_000L) != 1_000_000_000_000_000_000L) throw new AssertionError("overflow");
        // Every size up to 30 is checked against the oracle.
        for (int n = 1; n <= 30; n++) if (movedCells(n) != oracle(n)) throw new AssertionError("n=" + n);
    }
}
```

#### Solution: [Recognize] Counterclockwise Rotation (Author exercise)
<!-- id: mx-rotate-counter -->

**Approach.**
The mapping is `(r, c)` to `(n - 1 - c, r)`. The transpose sends `(r, c)` to `(c, r)`. The second step must send `(c, r)` to `(n - 1 - c, r)`, which keeps the column and mirrors the row. That step reverses each column, so it swaps the cell `(lo, c)` with the cell `(hi, c)` for each column `c`, with `lo` rising and `hi` falling. The changed transformation is therefore a column reversal and not a row reversal. The invariant after the first pass is the transpose, and after the second pass it is the counterclockwise turn.

**Complexity.**
- **Time** is O(n^2), because each pass swaps about `n^2 / 2` pairs.
- **Space** is O(1), because each swap uses one temporary value.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotateCounter {
    /**
     * Rotates a square matrix a quarter turn counterclockwise in place.
     * Time: O(n^2). Space: O(1).
     * Invariant: after pass one the matrix is the transpose, after pass two it is the rotation.
     */
    static void rotateCounter(int[][] m) {
        int n = m.length;
        // Pass one: the same transpose as the clockwise rotation.
        for (int r = 0; r < n; r++) {
            for (int c = r + 1; c < n; c++) {
                int tmp = m[r][c];
                m[r][c] = m[c][r];
                m[c][r] = tmp;
            }
        }
        // Pass two: reverse each column, so the top and bottom cells of a column swap.
        for (int c = 0; c < n; c++) {
            // lo and hi walk toward the middle of column c, giving n / 2 swaps per column.
            for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) {
                int tmp = m[lo][c];
                m[lo][c] = m[hi][c];
                m[hi][c] = tmp;
            }
        }
    }

    public static void main(String[] args) {
        // Statement examples.
        int[][] a = {{1, 2}, {3, 4}};
        rotateCounter(a);
        if (!Arrays.deepEquals(a, new int[][] {{2, 4}, {1, 3}})) throw new AssertionError("example 1");
        int[][] b = {{2, 4, 6}, {8, 1, 3}, {5, 7, 9}};
        rotateCounter(b);
        if (!Arrays.deepEquals(b, new int[][] {{6, 3, 9}, {4, 1, 7}, {2, 8, 5}})) throw new AssertionError("example 2");
        // Random squares are compared with the copy-based formula (r, c) to (n-1-c, r).
        Random rnd = new Random(33);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] m = new int[n][n], expect = new int[n][n];
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) m[r][c] = rnd.nextInt(100);
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) expect[n - 1 - c][r] = m[r][c];
            rotateCounter(m);
            if (!Arrays.deepEquals(m, expect)) throw new AssertionError("random " + t);
        }
    }
}
```
