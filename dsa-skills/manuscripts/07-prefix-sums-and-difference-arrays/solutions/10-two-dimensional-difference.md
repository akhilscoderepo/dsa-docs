<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Rectangle Updates

#### Solution: [Build] One Rectangle Add (Author exercise)
<!-- id: ps-one-rectangle -->

**Approach.**
The difference matrix has one extra row and one extra column. The update writes `+value` at the top-left corner. It writes `-value` in the column just right of the rectangle and in the row just below it. It writes `+value` at the corner past both. The final pass adds the upper and left neighbours to each entry and subtracts the upper-left neighbour. Each cell then equals the sum of all entries above it and to its left. Only the cells inside the rectangle keep the net `+value`. The invariant is that a cell's value equals the sum of `D[i][j]` over `i <= r` and `j <= c`.

**Complexity.**
- **Time** is O(m * n), because the update costs four writes and the pass visits each cell once.
- **Space** is O(m * n) for the difference matrix and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class OneRectangle {
    /**
     * Returns the matrix with value inside the rectangle and 0 elsewhere.
     * Time: O(m * n), four writes and one pass.
     * Space: O(m * n) for the difference matrix and the result.
     * Invariant: grid[r][c] is the sum of d[i][j] over i <= r and j <= c.
     */
    static long[][] rectangleAdd(int m, int n, int r1, int c1, int r2, int c2, int value) {
        // One extra row and column hold the cancelling writes of the rectangle.
        long[][] d = new long[m + 1][n + 1];
        d[r1][c1] += value;
        d[r1][c2 + 1] -= value;
        d[r2 + 1][c1] -= value;
        d[r2 + 1][c2 + 1] += value;
        long[][] grid = new long[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                // Each neighbour is read only when it exists, because grid has no extra row.
                long up = r > 0 ? grid[r - 1][c] : 0;
                long left = c > 0 ? grid[r][c - 1] : 0;
                long diag = r > 0 && c > 0 ? grid[r - 1][c - 1] : 0;
                // Up plus left counts the diagonal twice, so one copy is subtracted.
                grid[r][c] = d[r][c] + up + left - diag;
            }
        }
        return grid;
    }

    public static void main(String[] args) {
        // The statement examples.
        long[][] a = rectangleAdd(3, 4, 1, 1, 1, 2, 5);
        if (!Arrays.deepEquals(a, new long[][] {{0, 0, 0, 0}, {0, 5, 5, 0}, {0, 0, 0, 0}})) throw new AssertionError("example 1");
        long[][] b = rectangleAdd(4, 4, 1, 1, 2, 2, -1);
        if (!Arrays.deepEquals(b, new long[][] {{0, 0, 0, 0}, {0, -1, -1, 0}, {0, -1, -1, 0}, {0, 0, 0, 0}})) throw new AssertionError("example 2");
        // Random interior rectangles against a direct fill.
        Random rnd = new Random(37);
        for (int t = 0; t < 2000; t++) {
            int m = 3 + rnd.nextInt(5), n = 3 + rnd.nextInt(5);
            int r1 = 1 + rnd.nextInt(m - 2), r2 = r1 + rnd.nextInt(m - 1 - r1);
            int c1 = 1 + rnd.nextInt(n - 2), c2 = c1 + rnd.nextInt(n - 1 - c1);
            int v = rnd.nextInt(2_000_000_001) - 1_000_000_000;
            long[][] expect = new long[m][n];
            for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) expect[r][c] = v;
            if (!Arrays.deepEquals(rectangleAdd(m, n, r1, c1, r2, c2, v), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Increment Submatrices By One (LeetCode 2536)
<!-- id: ps-increment-2536 -->

**Approach.**
All queries share one difference matrix of size `(n + 1)` by `(n + 1)`. Each query adds four corner writes. The value `+1` goes to the top-left corner and `+1` to the corner past both sides. The value `-1` goes to the column right of the rectangle and to the row below it. Writes from different queries add up in the same entries. A single pass of the two-dimensional running sum then gives every cell the number of rectangles that contain it. The batching is the point, because the work per query stays constant.

**Complexity.**
- **Time** is O(n^2 + q), because each query costs four writes and the pass visits n^2 cells.
- **Space** is O(n^2) for the difference matrix and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class Increment2536 {
    /**
     * Returns the matrix after adding 1 to every query rectangle.
     * Time: O(n^2 + q), four writes per query and one pass.
     * Space: O(n^2) for the difference matrix and the result.
     * Invariant: result[r][c] is the sum of d[i][j] over i <= r and j <= c.
     */
    static int[][] rangeAddQueries(int n, int[][] queries) {
        // The extra row and column take the cancelling writes of rectangles that reach the edge.
        int[][] d = new int[n + 1][n + 1];
        for (int[] q : queries) {
            d[q[0]][q[1]]++;
            d[q[0]][q[3] + 1]--;
            d[q[2] + 1][q[1]]--;
            d[q[2] + 1][q[3] + 1]++;
        }
        int[][] result = new int[n][n];
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int up = r > 0 ? result[r - 1][c] : 0;
                int left = c > 0 ? result[r][c - 1] : 0;
                int diag = r > 0 && c > 0 ? result[r - 1][c - 1] : 0;
                // The same recurrence as the prefix matrix, applied to the deltas.
                result[r][c] = d[r][c] + up + left - diag;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.deepEquals(rangeAddQueries(3, new int[][] {{0, 1, 1, 2}, {1, 0, 2, 1}}), new int[][] {{0, 1, 1}, {1, 2, 1}, {1, 1, 0}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(rangeAddQueries(1, new int[][] {{0, 0, 0, 0}}), new int[][] {{1}})) throw new AssertionError("example 2");
        // Random queries against a direct fill.
        Random rnd = new Random(38);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] qs = new int[rnd.nextInt(6)][];
            int[][] expect = new int[n][n];
            for (int k = 0; k < qs.length; k++) {
                int r1 = rnd.nextInt(n), r2 = r1 + rnd.nextInt(n - r1), c1 = rnd.nextInt(n), c2 = c1 + rnd.nextInt(n - c1);
                qs[k] = new int[] {r1, c1, r2, c2};
                for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) expect[r][c]++;
            }
            if (!Arrays.deepEquals(rangeAddQueries(n, qs), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Bottom-Right Edge (Author exercise)
<!-- id: ps-bottom-right-edge -->

**Approach.**
A rectangle that ends at row `m - 1` writes its cancelling delta in row `m`, and a rectangle that ends at column `n - 1` writes in column `n`. The difference matrix has `m + 1` rows and `n + 1` columns, so these indexes exist and no guard is needed. The final pass reads only the first `m` rows and `n` columns, so the extra entries never become cell values. A matrix of exactly `m` by `n` would throw an `ArrayIndexOutOfBoundsException` on the first edge update.

**Complexity.**
- **Time** is O(m * n + u), because each update costs four writes and the pass visits each cell once.
- **Space** is O(m * n) for the difference matrix and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BottomRightEdge {
    /**
     * Returns the matrix after adding 1 to every update rectangle.
     * Time: O(m * n + u), four writes per update and one pass.
     * Space: O(m * n) for the difference matrix and the result.
     * Invariant: result[r][c] is the sum of d[i][j] over i <= r and j <= c.
     */
    static int[][] apply(int m, int n, int[][] updates) {
        // The extra row and the extra column hold the cancelling writes at the edge.
        int[][] d = new int[m + 1][n + 1];
        for (int[] u : updates) {
            d[u[0]][u[1]]++;
            d[u[0]][u[3] + 1]--;
            d[u[2] + 1][u[1]]--;
            d[u[2] + 1][u[3] + 1]++;
        }
        int[][] result = new int[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                int up = r > 0 ? result[r - 1][c] : 0;
                int left = c > 0 ? result[r][c - 1] : 0;
                int diag = r > 0 && c > 0 ? result[r - 1][c - 1] : 0;
                result[r][c] = d[r][c] + up + left - diag;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.deepEquals(apply(2, 3, new int[][] {{0, 1, 1, 2}}), new int[][] {{0, 1, 1}, {0, 1, 1}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(apply(1, 1, new int[][] {{0, 0, 0, 0}, {0, 0, 0, 0}}), new int[][] {{2}})) throw new AssertionError("example 2");
        // A matrix without the extra row and column fails on an edge update.
        try {
            int[][] tight = new int[2][3];
            tight[1 + 1][1]--;
            throw new AssertionError("expected an out of range write");
        } catch (ArrayIndexOutOfBoundsException expected) {
            // This is the failure that the extra row prevents.
        }
        // Random non-square grids, with many updates at the edges, against a direct fill.
        Random rnd = new Random(39);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(6), n = 1 + rnd.nextInt(6);
            int[][] ups = new int[rnd.nextInt(6)][];
            int[][] expect = new int[m][n];
            for (int k = 0; k < ups.length; k++) {
                int r1 = rnd.nextInt(m), r2 = rnd.nextBoolean() ? m - 1 : r1 + rnd.nextInt(m - r1);
                int c1 = rnd.nextInt(n), c2 = rnd.nextBoolean() ? n - 1 : c1 + rnd.nextInt(n - c1);
                ups[k] = new int[] {r1, c1, r2, c2};
                for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) expect[r][c]++;
            }
            if (!Arrays.deepEquals(apply(m, n, ups), expect)) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Weighted Rectangle Updates (Author exercise)
<!-- id: ps-weighted-rectangles -->

**Approach.**
The pattern of four writes is unchanged. The top-left corner and the corner past both sides receive `+weight`, and the two cancelling entries receive `-weight`. The weight is a signed `long`, and the matrix of deltas and the result use `long`, because 10^4 weights of 10^12 add up to 10^16. The two-dimensional running sum of the deltas gives each cell the sum of the weights of all rectangles that contain it. A negative weight needs no special case, because every step is an addition or a subtraction.

**Complexity.**
- **Time** is O(m * n + u), because each update costs four writes and the pass visits each cell once.
- **Space** is O(m * n) for the delta matrix and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class WeightedRectangles {
    /**
     * Returns the matrix after adding each weight to its rectangle.
     * Time: O(m * n + u), four writes per update and one pass.
     * Space: O(m * n) for the delta matrix and the result.
     * Invariant: result[r][c] is the sum of d[i][j] over i <= r and j <= c.
     */
    static long[][] apply(int m, int n, long[][] updates) {
        // The extra row and column hold the cancelling writes at the edge.
        long[][] d = new long[m + 1][n + 1];
        for (long[] u : updates) {
            int r1 = (int) u[0], c1 = (int) u[1], r2 = (int) u[2], c2 = (int) u[3];
            long w = u[4];
            d[r1][c1] += w;
            d[r1][c2 + 1] -= w;
            d[r2 + 1][c1] -= w;
            d[r2 + 1][c2 + 1] += w;
        }
        long[][] result = new long[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                long up = r > 0 ? result[r - 1][c] : 0;
                long left = c > 0 ? result[r][c - 1] : 0;
                long diag = r > 0 && c > 0 ? result[r - 1][c - 1] : 0;
                result[r][c] = d[r][c] + up + left - diag;
            }
        }
        return result;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.deepEquals(apply(2, 2, new long[][] {{0, 0, 1, 1, 5}, {1, 1, 1, 1, -7}}), new long[][] {{5, 5}, {5, -2}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(apply(1, 1, new long[][] {{0, 0, 0, 0, 3_000_000_000_000L}}), new long[][] {{3_000_000_000_000L}})) throw new AssertionError("example 2");
        // Random signed weights against a direct fill.
        Random rnd = new Random(40);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(6), n = 1 + rnd.nextInt(6);
            long[][] ups = new long[rnd.nextInt(6)][];
            long[][] expect = new long[m][n];
            for (int k = 0; k < ups.length; k++) {
                int r1 = rnd.nextInt(m), r2 = r1 + rnd.nextInt(m - r1), c1 = rnd.nextInt(n), c2 = c1 + rnd.nextInt(n - c1);
                long w = (long) (rnd.nextDouble() * 2e12) - 1_000_000_000_000L;
                ups[k] = new long[] {r1, c1, r2, c2, w};
                for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) expect[r][c] += w;
            }
            if (!Arrays.deepEquals(apply(m, n, ups), expect)) throw new AssertionError("random");
        }
    }
}
```
