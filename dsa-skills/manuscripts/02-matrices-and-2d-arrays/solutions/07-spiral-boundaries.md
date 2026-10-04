<!-- solutions-for: 07-spiral-boundaries -->
### Solutions For Walking In A Spiral

#### Solution: [Build] One Ring (Author exercise)
<!-- id: mx-one-ring -->

**Approach.**
The method runs one layer of the walk. When the matrix has one row, the first pass already emits every cell, and the method returns. When it has one column, the first pass emits the top cell and the second pass emits the rest, so the method returns after those two. Otherwise the method emits the first row from left to right, the last column below it, the last row from right to left, and the first column between the two corner rows. The invariant is that no cell appears twice, because each pass skips the corner that the previous pass emitted.

**Complexity.**
- **Time** is O(rows + cols), because the method touches only the outer cells.
- **Space** is O(1) besides the output list.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class OneRing {
    /**
     * Returns the outer cells of a matrix in clockwise order, each cell once.
     * Time: O(rows + cols). Space: O(1) besides the output.
     * Invariant: each pass starts after the corner that the previous pass emitted.
     */
    static List<Integer> ring(int[][] m) {
        int rows = m.length, cols = m[0].length;
        List<Integer> out = new ArrayList<>();
        // The first row is always emitted in full, which costs cols steps.
        for (int c = 0; c < cols; c++) out.add(m[0][c]);
        // A single row has no cells below it.
        if (rows == 1) return out;
        // The last column starts below the first row, so the top-right corner is not repeated.
        for (int r = 1; r < rows; r++) out.add(m[r][cols - 1]);
        // A single column has no cells to the left of the last column.
        if (cols == 1) return out;
        // The last row runs right to left and starts before the bottom-right corner.
        for (int c = cols - 2; c >= 0; c--) out.add(m[rows - 1][c]);
        // The first column runs upward and stops below the first row.
        for (int r = rows - 2; r >= 1; r--) out.add(m[r][0]);
        return out;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (!ring(new int[][] {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}).equals(Arrays.asList(1, 2, 3, 6, 9, 8, 7, 4))) throw new AssertionError("example 1");
        if (!ring(new int[][] {{1, 2}, {3, 4}, {5, 6}}).equals(Arrays.asList(1, 2, 4, 6, 5, 3))) throw new AssertionError("example 2");
        // One row, one column and one cell are the thin shapes.
        if (!ring(new int[][] {{7, 8, 9}}).equals(Arrays.asList(7, 8, 9))) throw new AssertionError("one row");
        if (!ring(new int[][] {{7}, {8}, {9}}).equals(Arrays.asList(7, 8, 9))) throw new AssertionError("one column");
        if (!ring(new int[][] {{5}}).equals(Arrays.asList(5))) throw new AssertionError("one cell");
        // Random rectangles are compared with an oracle that scans every cell and keeps the outer ones in clockwise order.
        Random rnd = new Random(71);
        for (int t = 0; t < 300; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = rnd.nextInt(100);
            List<Integer> expect = new ArrayList<>();
            int cells = rows == 1 || cols == 1 ? rows * cols : 2 * (rows + cols) - 4;
            int r = 0, c = 0, d = 0;
            int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
            // The oracle turns at the matrix edge, and a one-line matrix is its own ring.
            if (rows == 1 || cols == 1) { for (int[] row : m) for (int v : row) expect.add(v); }
            else {
                for (int k = 0; k < cells; k++) {
                    expect.add(m[r][c]);
                    int nr = r + dr[d], nc = c + dc[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) { d++; nr = r + dr[d]; nc = c + dc[d]; }
                    r = nr; c = nc;
                }
            }
            if (!ring(m).equals(expect)) throw new AssertionError("random " + t);
            if (ring(m).size() != cells) throw new AssertionError("count " + t);
        }
    }
}
```

#### Solution: [Vary] Spiral Matrix (LeetCode 54)
<!-- id: mx-spiral-matrix -->

**Approach.**
The method keeps `top`, `bottom`, `left` and `right`, which enclose the cells not yet emitted. Each loop iteration emits one layer in four passes and moves the matching edge inward after each pass. The third pass runs only when `top <= bottom`, and the fourth runs only when `left <= right`, because the first two passes can leave a single row or column that they already emitted. The loop ends when the rectangle is empty. The invariant is that the four indexes enclose exactly the cells not yet emitted.

**Complexity.**
- **Time** is O(rows * cols), because each cell is emitted once.
- **Space** is O(1) besides the output list, because the method keeps four integers.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SpiralMatrix {
    /**
     * Returns all values of a matrix in spiral order.
     * Time: O(rows * cols). Space: O(1) besides the output.
     * Invariant: top, bottom, left and right enclose exactly the cells not yet emitted.
     */
    static List<Integer> spiralOrder(int[][] m) {
        List<Integer> out = new ArrayList<>();
        int top = 0, bottom = m.length - 1;
        int left = 0, right = m[0].length - 1;
        // The loop runs while the unvisited rectangle is not empty.
        while (top <= bottom && left <= right) {
            // Top pass: emits row top, and the edge moves down because that row is consumed.
            for (int c = left; c <= right; c++) out.add(m[top][c]);
            top++;
            // Right pass: emits column right below the corner, and the edge moves left.
            for (int r = top; r <= bottom; r++) out.add(m[r][right]);
            right--;
            // The guard skips the bottom pass when the top pass already consumed the last row.
            if (top <= bottom) {
                for (int c = right; c >= left; c--) out.add(m[bottom][c]);
                bottom--;
            }
            // The guard skips the left pass when the right pass already consumed the last column.
            if (left <= right) {
                for (int r = bottom; r >= top; r--) out.add(m[r][left]);
                left++;
            }
        }
        return out;
    }

    static List<Integer> oracle(int[][] m) {
        int rows = m.length, cols = m[0].length;
        boolean[][] seen = new boolean[rows][cols];
        int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
        List<Integer> out = new ArrayList<>();
        int r = 0, c = 0, d = 0;
        for (int k = 0; k < rows * cols; k++) {
            // The oracle marks each cell and turns when the next cell is outside or marked.
            out.add(m[r][c]);
            seen[r][c] = true;
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || seen[nr][nc]) {
                d = (d + 1) % 4;
                nr = r + dr[d];
                nc = c + dc[d];
            }
            r = nr;
            c = nc;
        }
        return out;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (!spiralOrder(new int[][] {{2, 4, 6}, {8, 10, 12}, {14, 16, 18}}).equals(List.of(2, 4, 6, 12, 18, 16, 14, 8, 10))) throw new AssertionError("example 1");
        if (!spiralOrder(new int[][] {{1, 2}, {3, 4}, {5, 6}, {7, 8}}).equals(List.of(1, 2, 4, 6, 8, 7, 5, 3))) throw new AssertionError("example 2");
        // The opening failure: a one-row matrix must not repeat cells.
        if (!spiralOrder(new int[][] {{1, 2, 3}}).equals(List.of(1, 2, 3))) throw new AssertionError("one row");
        if (!spiralOrder(new int[][] {{1}, {2}, {3}}).equals(List.of(1, 2, 3))) throw new AssertionError("one column");
        // Random rectangles are compared with the oracle, and the output size equals rows * cols.
        Random rnd = new Random(72);
        for (int t = 0; t < 500; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            int[][] m = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = r * cols + c;
            List<Integer> got = spiralOrder(m);
            if (!got.equals(oracle(m))) throw new AssertionError("random " + t);
            if (got.size() != rows * cols) throw new AssertionError("size " + t);
        }
    }
}
```

#### Solution: [Boundary] Thin Remainder (Author exercise)
<!-- id: mx-thin-remainder -->

**Approach.**
Each full layer removes one row from the top, one row from the bottom, one column from the left and one column from the right. After `k = (min(rows, cols) - 1) / 2` layers, the remaining rectangle has `rows - 2k` rows and `cols - 2k` columns, and its smaller side is 1 or 2. When the remainder has one row, the first pass ends the walk at the last cell of that row. When it has one column, the second pass ends the walk at the bottom cell of that column. Otherwise the remainder has two rows or two columns and at least two of each, and the left pass ends the walk at the cell just below the top-left corner of the remainder. The invariant is that the walk after the removed layers behaves like a walk over the remainder alone.

**Complexity.**
- **Time** is O(1), because the method uses arithmetic on the two dimensions.
- **Space** is O(1), because no matrix is built.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ThinRemainder {
    /**
     * Returns the last cell visited by a spiral walk over rows x cols cells.
     * Time: O(1). Space: O(1).
     * Invariant: after k full layers, the walk continues on the remaining rectangle only.
     */
    static int[] lastCell(int rows, int cols) {
        // k full layers fit, and the remainder has a smaller side of 1 or 2.
        int k = (Math.min(rows, cols) - 1) / 2;
        int rr = rows - 2 * k, cc = cols - 2 * k;
        // One remaining row: the top pass ends at its last column.
        if (rr == 1) return new int[] {k, k + cc - 1};
        // One remaining column: the right pass ends at its last row.
        if (cc == 1) return new int[] {k + rr - 1, k};
        // Two rows or two columns with the other side at least two: the left pass ends below the corner.
        return new int[] {k + 1, k};
    }

    static int[] oracle(int rows, int cols) {
        int top = 0, bottom = rows - 1, left = 0, right = cols - 1;
        int[] last = {0, 0};
        // The oracle runs the four-pass walk and records every visited cell.
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) last = new int[] {top, c};
            top++;
            for (int r = top; r <= bottom; r++) last = new int[] {r, right};
            right--;
            if (top <= bottom) { for (int c = right; c >= left; c--) last = new int[] {bottom, c}; bottom--; }
            if (left <= right) { for (int r = bottom; r >= top; r--) last = new int[] {r, left}; left++; }
        }
        return last;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (!Arrays.equals(lastCell(3, 4), new int[] {1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(lastCell(4, 1), new int[] {3, 0})) throw new AssertionError("example 2");
        // A single cell and the largest dimensions finish with constant work.
        if (!Arrays.equals(lastCell(1, 1), new int[] {0, 0})) throw new AssertionError("single cell");
        if (!Arrays.equals(lastCell(1_000_000_000, 1), new int[] {999_999_999, 0})) throw new AssertionError("tall column");
        // Every small shape is compared with the oracle.
        for (int rows = 1; rows <= 12; rows++) {
            for (int cols = 1; cols <= 12; cols++) {
                if (!Arrays.equals(lastCell(rows, cols), oracle(rows, cols))) throw new AssertionError(rows + "x" + cols);
            }
        }
        // Random larger shapes add coverage of the remainder cases.
        Random rnd = new Random(73);
        for (int t = 0; t < 200; t++) {
            int rows = 1 + rnd.nextInt(60), cols = 1 + rnd.nextInt(60);
            if (!Arrays.equals(lastCell(rows, cols), oracle(rows, cols))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Spiral Matrix II (LeetCode 59)
<!-- id: mx-spiral-generate -->

**Approach.**
The method uses the same four edges and the same guards as the reading walk. Each statement that read `m[r][c]` now writes `m[r][c] = next++`, so the counter hands out `1` to `n * n` in the order the walk visits cells. The loop ends when the rectangle is empty, and a matrix with an odd `n` ends with the center cell filled by the last pass. The invariant is that the cells outside the four edges hold the smallest values and the counter equals one more than the number of filled cells.

**Complexity.**
- **Time** is O(n^2), because each cell receives exactly one value.
- **Space** is O(1) besides the returned matrix, because the method keeps the four edges and a counter.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SpiralFill {
    /**
     * Returns an n x n matrix filled with 1 to n*n in spiral order.
     * Time: O(n^2). Space: O(1) besides the returned matrix.
     * Invariant: the counter equals one more than the number of cells outside the unvisited rectangle.
     */
    static int[][] generate(int n) {
        int[][] m = new int[n][n];
        int top = 0, bottom = n - 1, left = 0, right = n - 1;
        int next = 1;
        // Each iteration fills one layer, and the loop stops when the rectangle is empty.
        while (top <= bottom && left <= right) {
            // Top pass writes the counter into row top, then the edge moves down.
            for (int c = left; c <= right; c++) m[top][c] = next++;
            top++;
            // Right pass writes below the corner, then the edge moves left.
            for (int r = top; r <= bottom; r++) m[r][right] = next++;
            right--;
            // Guard: the bottom pass needs a row that the top pass did not consume.
            if (top <= bottom) {
                for (int c = right; c >= left; c--) m[bottom][c] = next++;
                bottom--;
            }
            // Guard: the left pass needs a column that the right pass did not consume.
            if (left <= right) {
                for (int r = bottom; r >= top; r--) m[r][left] = next++;
                left++;
            }
        }
        return m;
    }

    static int[][] oracle(int n) {
        int[][] m = new int[n][n];
        int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
        int r = 0, c = 0, d = 0;
        // The oracle turns whenever the next cell is outside the matrix or already filled.
        for (int v = 1; v <= n * n; v++) {
            m[r][c] = v;
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n || m[nr][nc] != 0) {
                d = (d + 1) % 4;
                nr = r + dr[d];
                nc = c + dc[d];
            }
            r = nr;
            c = nc;
        }
        return m;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (!Arrays.deepEquals(generate(2), new int[][] {{1, 2}, {4, 3}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(generate(5), new int[][] {{1, 2, 3, 4, 5}, {16, 17, 18, 19, 6}, {15, 24, 25, 20, 7}, {14, 23, 22, 21, 8}, {13, 12, 11, 10, 9}})) throw new AssertionError("example 2");
        // The smallest size and an odd size with a center cell.
        if (!Arrays.deepEquals(generate(1), new int[][] {{1}})) throw new AssertionError("n = 1");
        if (generate(5)[2][2] != 25) throw new AssertionError("center of n = 5 holds the last value");
        // Every size in range is compared with the oracle, and each value appears once.
        for (int n = 1; n <= 20; n++) {
            int[][] got = generate(n);
            if (!Arrays.deepEquals(got, oracle(n))) throw new AssertionError("n = " + n);
            boolean[] used = new boolean[n * n + 1];
            for (int[] row : got) for (int v : row) used[v] = true;
            for (int v = 1; v <= n * n; v++) if (!used[v]) throw new AssertionError("missing " + v + " for n = " + n);
        }
    }
}
```
