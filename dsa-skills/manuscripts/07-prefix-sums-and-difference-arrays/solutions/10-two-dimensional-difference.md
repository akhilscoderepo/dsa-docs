<!-- solutions-for: 07-two-dimensional-difference -->
### Two-Dimensional Difference

#### Solution: [Build] One Rectangle Add (Author exercise)
<!-- id: ps-one-rectangle-add -->

**Approach.** A sheet one row and one column larger than the grid holds four corner notes for the rectangle: plus the amount at its top-left corner, minus the amount just right of its top-right corner, minus the amount just below its bottom-left corner, and plus the amount just beyond its bottom-right corner. The two-dimensional running sum of the sheet, computed in reading order as the delta plus the total above plus the total to the left minus the total diagonally above-left, gives the amount inside the rectangle and zero outside it. The oracle adds the amount to each cell of the rectangle.

**Complexity.** Four writes and one sweep, so O(R C) time and an extra sheet of (R + 1)(C + 1) slots.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OneRectangleAdd {
    static long[][] rectangleAdd(int rows, int cols, int r1, int c1, int r2, int c2, long amount) {
        long[][] diff = new long[rows + 1][cols + 1];
        diff[r1][c1] += amount;
        diff[r1][c2 + 1] -= amount;
        diff[r2 + 1][c1] -= amount;
        diff[r2 + 1][c2 + 1] += amount;
        long[][] out = new long[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                long above = r > 0 ? out[r - 1][c] : 0;
                long left = c > 0 ? out[r][c - 1] : 0;
                long diag = r > 0 && c > 0 ? out[r - 1][c - 1] : 0;
                out[r][c] = diff[r][c] + above + left - diag;
            }
        }
        return out;
    }
    static long[][] oracle(int rows, int cols, int r1, int c1, int r2, int c2, long amount) {
        long[][] out = new long[rows][cols];
        for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) out[r][c] += amount;
        return out;
    }

    public static void main(String[] args) {
        long[][] one = rectangleAdd(3, 4, 1, 1, 2, 2, 5);
        if (!Arrays.deepEquals(one, new long[][] {{0, 0, 0, 0}, {0, 5, 5, 0}, {0, 5, 5, 0}})) throw new AssertionError("example 1");
        long[][] two = rectangleAdd(2, 2, 0, 0, 1, 1, 3);
        if (!Arrays.deepEquals(two, new long[][] {{3, 3}, {3, 3}})) throw new AssertionError("example 2");
        Random rnd = new Random(8001);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int r1 = rnd.nextInt(rows), r2 = r1 + rnd.nextInt(rows - r1);
            int c1 = rnd.nextInt(cols), c2 = c1 + rnd.nextInt(cols - c1);
            long v = rnd.nextInt(2000000001) - 1000000000;
            if (!Arrays.deepEquals(rectangleAdd(rows, cols, r1, c1, r2, c2, v), oracle(rows, cols, r1, c1, r2, c2, v))) throw new AssertionError("differs");
        }
    }
}
```

#### Solution: [Vary] Increment Submatrices by One (LeetCode 2536)
<!-- id: ps-increment-submatrices -->

**Approach.** Every query is a rectangle with amount one, so the four corner notes are plus one, minus one, minus one and plus one, and all queries write into the same sheet of size `(n + 1)` by `(n + 1)`. Nothing is read until every query has been recorded. One sweep in reading order then produces the final matrix, using the delta plus the total above plus the total to the left minus the diagonal total. The oracle applies each query cell by cell.

**Complexity.** O(queries + n squared) time and an extra sheet of (n + 1) squared slots.

```java run
import java.util.Arrays;
import java.util.Random;

public final class IncrementSubmatrices {
    static int[][] rangeAddQueries(int n, int[][] queries) {
        int[][] diff = new int[n + 1][n + 1];
        for (int[] q : queries) {
            diff[q[0]][q[1]]++;
            diff[q[0]][q[3] + 1]--;
            diff[q[2] + 1][q[1]]--;
            diff[q[2] + 1][q[3] + 1]++;
        }
        int[][] out = new int[n][n];
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int above = r > 0 ? out[r - 1][c] : 0;
                int left = c > 0 ? out[r][c - 1] : 0;
                int diag = r > 0 && c > 0 ? out[r - 1][c - 1] : 0;
                out[r][c] = diff[r][c] + above + left - diag;
            }
        }
        return out;
    }
    static int[][] oracle(int n, int[][] queries) {
        int[][] out = new int[n][n];
        for (int[] q : queries)
            for (int r = q[0]; r <= q[2]; r++)
                for (int c = q[1]; c <= q[3]; c++) out[r][c]++;
        return out;
    }

    public static void main(String[] args) {
        int[][] one = rangeAddQueries(3, new int[][] {{1, 1, 2, 2}, {0, 0, 1, 1}});
        if (!Arrays.deepEquals(one, new int[][] {{1, 1, 0}, {1, 2, 1}, {0, 1, 1}})) throw new AssertionError("example 1");
        int[][] two = rangeAddQueries(2, new int[][] {{0, 0, 1, 1}});
        if (!Arrays.deepEquals(two, new int[][] {{1, 1}, {1, 1}})) throw new AssertionError("example 2");
        Random rnd = new Random(8002);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = 1 + rnd.nextInt(6);
            int[][] qs = new int[m][4];
            for (int i = 0; i < m; i++) {
                int r1 = rnd.nextInt(n), r2 = r1 + rnd.nextInt(n - r1);
                int c1 = rnd.nextInt(n), c2 = c1 + rnd.nextInt(n - c1);
                qs[i] = new int[] {r1, c1, r2, c2};
            }
            if (!Arrays.deepEquals(rangeAddQueries(n, qs), oracle(n, qs))) throw new AssertionError("differs for n=" + n);
        }
    }
}
```

#### Solution: [Boundary] Bottom-Right Edge (Author exercise)
<!-- id: ps-bottom-right-edge -->

**Approach.** A rectangle ending in the last row writes a note at row `rows`, and one ending in the last column writes a note at column `cols`, both one past the grid. A sheet of the same size as the grid throws an exception at the first such write. A sheet with a border row and a border column accepts the notes and the sweep never reads the border, and a guard that skips each write falling outside the grid works equally well, because a note beyond the grid affects no tile. The program shows the throwing version, then both fixes, and compares them with an oracle on random rectangles that favor the bottom-right edge, including a one by one grid.

**Complexity.** O(updates + R C) time with either the border or the guards.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BottomRightEdge {
    static long[][] sweep(long[][] diff, int rows, int cols) {
        long[][] out = new long[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                long above = r > 0 ? out[r - 1][c] : 0;
                long left = c > 0 ? out[r][c - 1] : 0;
                long diag = r > 0 && c > 0 ? out[r - 1][c - 1] : 0;
                out[r][c] = diff[r][c] + above + left - diag;
            }
        }
        return out;
    }
    static long[][] withBorder(int rows, int cols, int[][] ups) {
        long[][] diff = new long[rows + 1][cols + 1];
        for (int[] u : ups) {
            diff[u[0]][u[1]] += u[4];
            diff[u[0]][u[3] + 1] -= u[4];
            diff[u[2] + 1][u[1]] -= u[4];
            diff[u[2] + 1][u[3] + 1] += u[4];
        }
        return sweep(diff, rows, cols);
    }
    static long[][] withGuards(int rows, int cols, int[][] ups) {
        long[][] diff = new long[rows][cols];
        for (int[] u : ups) {
            diff[u[0]][u[1]] += u[4];
            if (u[3] + 1 < cols) diff[u[0]][u[3] + 1] -= u[4];
            if (u[2] + 1 < rows) diff[u[2] + 1][u[1]] -= u[4];
            if (u[2] + 1 < rows && u[3] + 1 < cols) diff[u[2] + 1][u[3] + 1] += u[4];
        }
        return sweep(diff, rows, cols);
    }
    static long[][] tooSmall(int rows, int cols, int[][] ups) {
        long[][] diff = new long[rows][cols];
        for (int[] u : ups) {
            diff[u[0]][u[1]] += u[4];
            diff[u[0]][u[3] + 1] -= u[4];
            diff[u[2] + 1][u[1]] -= u[4];
            diff[u[2] + 1][u[3] + 1] += u[4];
        }
        return sweep(diff, rows, cols);
    }
    static long[][] oracle(int rows, int cols, int[][] ups) {
        long[][] out = new long[rows][cols];
        for (int[] u : ups)
            for (int r = u[0]; r <= u[2]; r++) for (int c = u[1]; c <= u[3]; c++) out[r][c] += u[4];
        return out;
    }

    public static void main(String[] args) {
        int[][] one = {{1, 1, 1, 2, 4}};
        long[][] want1 = {{0, 0, 0}, {0, 4, 4}};
        if (!Arrays.deepEquals(withBorder(2, 3, one), want1) || !Arrays.deepEquals(withGuards(2, 3, one), want1)) throw new AssertionError("example 1");
        int[][] two = {{0, 0, 0, 0, 6}};
        if (!Arrays.deepEquals(withBorder(1, 1, two), new long[][] {{6}}) || !Arrays.deepEquals(withGuards(1, 1, two), new long[][] {{6}})) throw new AssertionError("example 2");
        boolean threw = false;
        try { tooSmall(2, 3, one); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("a sheet of the grid's size should throw");
        Random rnd = new Random(8003);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int m = 1 + rnd.nextInt(4);
            int[][] ups = new int[m][5];
            for (int i = 0; i < m; i++) {
                int r1 = rnd.nextInt(rows), c1 = rnd.nextInt(cols);
                int r2 = rnd.nextBoolean() ? rows - 1 : r1 + rnd.nextInt(rows - r1);
                int c2 = rnd.nextBoolean() ? cols - 1 : c1 + rnd.nextInt(cols - c1);
                ups[i] = new int[] {r1, c1, Math.max(r1, r2), Math.max(c1, c2), rnd.nextInt(21) - 10};
            }
            long[][] want = oracle(rows, cols, ups);
            if (!Arrays.deepEquals(withBorder(rows, cols, ups), want)) throw new AssertionError("border differs");
            if (!Arrays.deepEquals(withGuards(rows, cols, ups), want)) throw new AssertionError("guards differ");
        }
    }
}
```

#### Solution: [Recognize] Weighted Rectangle Updates (Author exercise)
<!-- id: ps-weighted-rectangle-updates -->

**Approach.** The four-corner pattern does not depend on the amount, so a signed weight is written as the weight and its negation at the same four corners. What changes is the width of the numbers: a cell can receive up to a hundred thousand weights of a billion, which is far beyond the range of `int`, so the sheet, the sweep and the output are all `long`. The first example, two updates of two billion each, already gives cells of four billion, which an `int` sweep would wrap. The program runs an `int` version on that example to show the wrap, and checks the `long` version against an oracle on random weighted updates.

**Complexity.** O(updates + R C) time and an extra sheet of (R + 1)(C + 1) `long` slots.

```java run
import java.util.Arrays;
import java.util.Random;

public final class WeightedRectangleUpdates {
    static long[][] apply(int rows, int cols, long[][] ups) {
        long[][] diff = new long[rows + 1][cols + 1];
        for (long[] u : ups) {
            int r1 = (int) u[0], c1 = (int) u[1], r2 = (int) u[2], c2 = (int) u[3];
            diff[r1][c1] += u[4];
            diff[r1][c2 + 1] -= u[4];
            diff[r2 + 1][c1] -= u[4];
            diff[r2 + 1][c2 + 1] += u[4];
        }
        long[][] out = new long[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                long above = r > 0 ? out[r - 1][c] : 0;
                long left = c > 0 ? out[r][c - 1] : 0;
                long diag = r > 0 && c > 0 ? out[r - 1][c - 1] : 0;
                out[r][c] = diff[r][c] + above + left - diag;
            }
        }
        return out;
    }
    static int[][] applyInt(int rows, int cols, long[][] ups) {
        int[][] diff = new int[rows + 1][cols + 1];
        for (long[] u : ups) {
            int r1 = (int) u[0], c1 = (int) u[1], r2 = (int) u[2], c2 = (int) u[3];
            diff[r1][c1] += (int) u[4];
            diff[r1][c2 + 1] -= (int) u[4];
            diff[r2 + 1][c1] -= (int) u[4];
            diff[r2 + 1][c2 + 1] += (int) u[4];
        }
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int above = r > 0 ? out[r - 1][c] : 0;
                int left = c > 0 ? out[r][c - 1] : 0;
                int diag = r > 0 && c > 0 ? out[r - 1][c - 1] : 0;
                out[r][c] = diff[r][c] + above + left - diag;
            }
        }
        return out;
    }
    static long[][] oracle(int rows, int cols, long[][] ups) {
        long[][] out = new long[rows][cols];
        for (long[] u : ups)
            for (int r = (int) u[0]; r <= (int) u[2]; r++)
                for (int c = (int) u[1]; c <= (int) u[3]; c++) out[r][c] += u[4];
        return out;
    }

    public static void main(String[] args) {
        long[][] first = {{0, 0, 1, 1, 2000000000L}, {0, 0, 1, 1, 2000000000L}};
        long[][] got = apply(3, 3, first);
        if (got[0][0] != 4000000000L || got[1][1] != 4000000000L || got[2][2] != 0 || got[0][2] != 0) throw new AssertionError("example 1");
        if (applyInt(3, 3, first)[0][0] == 4000000000L) throw new AssertionError("an int sweep should wrap");
        long[][] second = {{0, 0, 2, 2, 5}, {1, 1, 1, 1, -7}};
        long[][] g2 = apply(3, 3, second);
        if (g2[1][1] != -2 || g2[0][0] != 5 || g2[2][2] != 5) throw new AssertionError("example 2");
        Random rnd = new Random(8004);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int m = 1 + rnd.nextInt(6);
            long[][] ups = new long[m][5];
            for (int i = 0; i < m; i++) {
                int r1 = rnd.nextInt(rows), c1 = rnd.nextInt(cols);
                int r2 = r1 + rnd.nextInt(rows - r1), c2 = c1 + rnd.nextInt(cols - c1);
                ups[i] = new long[] {r1, c1, r2, c2, rnd.nextInt(2000000001) - 1000000000L};
            }
            if (!Arrays.deepEquals(apply(rows, cols, ups), oracle(rows, cols, ups))) throw new AssertionError("differs");
        }
    }
}
```
