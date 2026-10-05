<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Rectangle Sums

#### Solution: [Build] Range Sum Query 2D Immutable (LeetCode 304)
<!-- id: ps-matrix-sum-304 -->

**Approach.**
The prefix matrix has one extra row and one extra column of zeros. Each entry `P[r + 1][c + 1]` adds the entry above and the entry to the left, subtracts their shared part `P[r][c]` once and adds the cell. A query reads the large rectangle `P[r2 + 1][c2 + 1]`. It removes the rows above with `P[r1][c2 + 1]` and the columns on the left with `P[r2 + 1][c1]`. It then adds back the corner `P[r1][c1]`, which both removals subtracted. The invariant is that `P[r][c]` is the sum of the rows `0..r-1` and the columns `0..c-1`.

**Complexity.**
- **Time** is O(m * n + q), because the build visits each cell once and each query reads four entries.
- **Space** is O(m * n) for the prefix matrix.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MatrixSum304 {
    /**
     * Answers rectangle sum queries with a prefix matrix.
     * Time: O(m * n + q), one build and four reads per query.
     * Space: O(m * n) for the prefix matrix.
     * Invariant: p[r][c] is the sum of rows 0..r-1 and columns 0..c-1.
     */
    static long[] answer(int[][] matrix, int[][] queries) {
        int m = matrix.length, n = matrix[0].length;
        // The extra row and column of zeros form the border.
        long[][] p = new long[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                // Above plus left counts the shared part twice, so one copy is subtracted.
                p[r + 1][c + 1] = p[r][c + 1] + p[r + 1][c] - p[r][c] + matrix[r][c];
            }
        }
        long[] out = new long[queries.length];
        for (int k = 0; k < queries.length; k++) {
            int r1 = queries[k][0], c1 = queries[k][1], r2 = queries[k][2], c2 = queries[k][3];
            // Whole rectangle, minus the rows above, minus the columns to the left, plus the corner.
            out[k] = p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1];
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[][] g = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        if (!Arrays.equals(answer(g, new int[][] {{1, 1, 2, 2}, {0, 0, 2, 2}}), new long[] {28, 45})) throw new AssertionError("example 1");
        if (!Arrays.equals(answer(new int[][] {{-4}}, new int[][] {{0, 0, 0, 0}}), new long[] {-4})) throw new AssertionError("example 2");
        // Random matrices and rectangles against a loop over the cells.
        Random rnd = new Random(33);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] mat = new int[m][n];
            for (int[] row : mat) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(20001) - 10000;
            int r1 = rnd.nextInt(m), r2 = r1 + rnd.nextInt(m - r1), c1 = rnd.nextInt(n), c2 = c1 + rnd.nextInt(n - c1);
            long expect = 0;
            for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) expect += mat[r][c];
            if (answer(mat, new int[][] {{r1, c1, r2, c2}})[0] != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Matrix Block Sum (LeetCode 1314)
<!-- id: ps-block-sum-1314 -->

**Approach.**
Each output cell is one rectangle query, with the rows `i - k` through `i + k` and the columns `j - k` through `j + k`. The method clamps the corners to the matrix. The top row becomes `max(0, i - k)`, and the bottom row becomes `min(m - 1, i + k)`. The columns follow the same rule. After clamping, the rectangle lies inside the matrix and the four-read formula applies without any case for the edges. The build runs once, and every cell then costs four reads.

**Complexity.**
- **Time** is O(m * n), because the build and the answer loop each visit every cell a constant number of times.
- **Space** is O(m * n) for the prefix matrix and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BlockSum1314 {
    /**
     * Returns the sum of the clipped (2k+1) by (2k+1) block around every cell.
     * Time: O(m * n), one build and four reads per cell.
     * Space: O(m * n) for the prefix matrix and the result.
     * Invariant: p[r][c] is the sum of rows 0..r-1 and columns 0..c-1.
     */
    static int[][] blockSum(int[][] mat, int k) {
        int m = mat.length, n = mat[0].length;
        int[][] p = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                p[r + 1][c + 1] = p[r][c + 1] + p[r + 1][c] - p[r][c] + mat[r][c];
        int[][] answer = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                // Clamping keeps the rectangle inside the matrix near the edges.
                int r1 = Math.max(0, i - k), r2 = Math.min(m - 1, i + k);
                int c1 = Math.max(0, j - k), c2 = Math.min(n - 1, j + k);
                // The four reads of the rectangle formula.
                answer[i][j] = p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1];
            }
        }
        return answer;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.deepEquals(blockSum(new int[][] {{1, 2, 3}, {4, 5, 6}}, 1), new int[][] {{12, 21, 16}, {12, 21, 16}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(blockSum(new int[][] {{5}}, 0), new int[][] {{5}})) throw new AssertionError("example 2");
        // Random matrices and radii against a loop over each block.
        Random rnd = new Random(34);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5), k = rnd.nextInt(4);
            int[][] mat = new int[m][n];
            for (int[] row : mat) for (int c = 0; c < n; c++) row[c] = 1 + rnd.nextInt(100);
            int[][] got = blockSum(mat, k);
            for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) {
                int s = 0;
                for (int r = Math.max(0, i - k); r <= Math.min(m - 1, i + k); r++)
                    for (int c = Math.max(0, j - k); c <= Math.min(n - 1, j + k); c++) s += mat[r][c];
                if (got[i][j] != s) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Boundary] Single Cell Rectangle (Author exercise)
<!-- id: ps-single-cell -->

**Approach.**
The cell `(r, c)` is the rectangle from `(r, c)` to `(r, c)`. The inclusion-exclusion formula gives `P[r + 1][c + 1] - P[r][c + 1] - P[r + 1][c] + P[r][c]`. The first entry holds the rectangle down to the cell. The second removes the rows above, and the third removes the columns to the left. The last restores the corner that both removals took away. What remains is exactly the one cell. The border of zeros keeps every index non-negative, including for the cells in the first row and the first column.

**Complexity.**
- **Time** is O(m * n), because each cell costs four reads.
- **Space** is O(m * n) for the returned matrix.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SingleCell {
    /**
     * Recovers the original matrix from its prefix matrix.
     * Time: O(m * n), four reads per cell.
     * Space: O(m * n) for the result.
     * Invariant: p[r][c] is the sum of rows 0..r-1 and columns 0..c-1.
     */
    static int[][] recover(int[][] p) {
        int m = p.length - 1, n = p[0].length - 1;
        int[][] cells = new int[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                // The rectangle (r, c) to (r, c) holds exactly one cell.
                cells[r][c] = p[r + 1][c + 1] - p[r][c + 1] - p[r + 1][c] + p[r][c];
            }
        }
        return cells;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.deepEquals(recover(new int[][] {{0, 0, 0}, {0, 3, 5}, {0, 4, 9}}), new int[][] {{3, 2}, {1, 3}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(recover(new int[][] {{0, 0}, {0, -6}}), new int[][] {{-6}})) throw new AssertionError("example 2");
        // Random matrices: build the prefix matrix, then recover the original.
        Random rnd = new Random(35);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] mat = new int[m][n];
            int[][] p = new int[m + 1][n + 1];
            for (int r = 0; r < m; r++) for (int c = 0; c < n; c++) {
                mat[r][c] = rnd.nextInt(20001) - 10000;
                p[r + 1][c + 1] = p[r][c + 1] + p[r + 1][c] - p[r][c] + mat[r][c];
            }
            if (!Arrays.deepEquals(recover(p), mat)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Whole Matrix Query (Author exercise)
<!-- id: ps-origin-rectangle -->

**Approach.**
A rectangle with its top-left cell at `(0, 0)` and its bottom-right cell at `(r, c)` is the query with `r1 = 0` and `c1 = 0`. The formula reads `P[r + 1][c + 1] - P[0][c + 1] - P[r + 1][0] + P[0][0]`. The last three entries lie in the border of zeros, so the sum equals `P[r + 1][c + 1]`. The border row is index 0, so the code reads no negative index for these queries. The method builds the matrix and keeps the maximum of the entries from `P[1][1]` to `P[m][n]`. The whole matrix is the entry `P[m][n]`.

**Complexity.**
- **Time** is O(m * n), because the build and the scan each visit every cell once.
- **Space** is O(m * n) for the prefix matrix.

```java run
import java.util.Random;

public final class OriginRectangle {
    /**
     * Returns the largest sum among rectangles whose top-left cell is (0, 0).
     * Time: O(m * n), one build and one scan.
     * Space: O(m * n) for the prefix matrix.
     * Invariant: p[r][c] is the sum of rows 0..r-1 and columns 0..c-1.
     */
    static long best(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        long[][] p = new long[m + 1][n + 1];
        long best = Long.MIN_VALUE;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                p[r + 1][c + 1] = p[r][c + 1] + p[r + 1][c] - p[r][c] + matrix[r][c];
                // The rectangle from the origin to (r, c) equals p[r + 1][c + 1] because the border is zero.
                best = Math.max(best, p[r + 1][c + 1]);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (best(new int[][] {{1, -2}, {-3, 4}}) != 1) throw new AssertionError("example 1");
        if (best(new int[][] {{-5}}) != -5) throw new AssertionError("example 2");
        // Random matrices against a loop over every origin rectangle.
        Random rnd = new Random(36);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] mat = new int[m][n];
            for (int[] row : mat) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(21) - 10;
            long expect = Long.MIN_VALUE;
            for (int r = 0; r < m; r++) for (int c = 0; c < n; c++) {
                long s = 0;
                for (int i = 0; i <= r; i++) for (int j = 0; j <= c; j++) s += mat[i][j];
                expect = Math.max(expect, s);
            }
            if (best(mat) != expect) throw new AssertionError("random");
        }
    }
}
```
