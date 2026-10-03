<!-- solutions-for: 07-spiral-boundaries -->
### Spiral Boundaries

#### Solution: [Build] One Ring (Author exercise)
<!-- id: mx-one-ring -->

**Approach.** Emit the top row from left to right, then the right column from the second row down, then the bottom row from the second-to-last column leftward only when there is more than one row, then the left column from the second-to-last row upward to the second row only when there is more than one column. Starting each strip one cell past the corner avoids repeating corners. The assertions compare with a full scan that selects cells on the first or last row or column in clockwise order of the angle around the border, for every shape up to six by six.

**Complexity.** O(rows + cols) time and O(1) extra space apart from the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class OneRing {
    static List<Integer> ring(int[][] m) {
        int rows = m.length, cols = m[0].length;
        List<Integer> out = new ArrayList<>();
        for (int c = 0; c < cols; c++) out.add(m[0][c]);
        for (int r = 1; r < rows; r++) out.add(m[r][cols - 1]);
        if (rows > 1) for (int c = cols - 2; c >= 0; c--) out.add(m[rows - 1][c]);
        if (cols > 1) for (int r = rows - 2; r >= 1; r--) out.add(m[r][0]);
        return out;
    }
    static List<Integer> oracle(int[][] m) {
        int rows = m.length, cols = m[0].length;
        List<int[]> cells = new ArrayList<>();
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) if (r == 0 || c == 0 || r == rows - 1 || c == cols - 1) cells.add(new int[] {r, c});
        List<Integer> out = new ArrayList<>();
        int r = 0, c = 0;
        for (int k = 0; k < cells.size(); k++) {
            out.add(m[r][c]);
            if (r == 0 && c < cols - 1) c++;
            else if (c == cols - 1 && r < rows - 1) r++;
            else if (r == rows - 1 && c > 0) c--;
            else r--;
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2, 3, 4}, {5, 6, 7, 8}, {9, 10, 11, 12}};
        if (!ring(a).equals(Arrays.asList(1, 2, 3, 4, 8, 12, 11, 10, 9, 5))) throw new AssertionError("example 1: " + ring(a));
        if (!ring(new int[][] {{7, 8, 9}}).equals(Arrays.asList(7, 8, 9))) throw new AssertionError("example 2");
        if (!ring(new int[][] {{1}, {2}, {3}}).equals(Arrays.asList(1, 2, 3))) throw new AssertionError("single column");
        for (int rows = 1; rows <= 6; rows++)
            for (int cols = 1; cols <= 6; cols++) {
                int[][] m = new int[rows][cols];
                for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = r * 10 + c;
                List<Integer> got = ring(m);
                int expectedCount = rows == 1 ? cols : cols == 1 ? rows : 2 * (rows + cols) - 4;
                if (got.size() != expectedCount) throw new AssertionError("ring size for " + rows + "x" + cols);
                if (new java.util.HashSet<>(got).size() != got.size()) throw new AssertionError("a cell was repeated for " + rows + "x" + cols);
                if (rows > 1 && cols > 1 && !got.equals(oracle(m))) throw new AssertionError("order for " + rows + "x" + cols);
            }
    }
}
```

#### Solution: [Vary] Spiral Matrix (LeetCode 54)
<!-- id: mx-spiral-matrix -->

**Approach.** Keep `top`, `bottom`, `left` and `right`. While the rectangle is non-empty, emit the top row and move `top` down, emit the right column and move `right` left, then, if rows remain, emit the bottom row leftward and move `bottom` up, and if columns remain, emit the left column upward and move `left` right. The oracle is the heading simulation with a visited grid from the lesson, and the assertions compare the two on every rectangle up to seven by seven.

**Complexity.** O(rows * cols) time and O(1) extra space apart from the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class SpiralMatrix {
    static List<Integer> spiralOrder(int[][] m) {
        List<Integer> out = new ArrayList<>();
        int top = 0, bottom = m.length - 1, left = 0, right = m[0].length - 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) out.add(m[top][c]);
            top++;
            for (int r = top; r <= bottom; r++) out.add(m[r][right]);
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) out.add(m[bottom][c]);
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) out.add(m[r][left]);
                left++;
            }
        }
        return out;
    }
    static List<Integer> byVisitedGrid(int[][] m) {
        int rows = m.length, cols = m[0].length;
        boolean[][] seen = new boolean[rows][cols];
        int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
        List<Integer> out = new ArrayList<>();
        int r = 0, c = 0, d = 0;
        for (int k = 0; k < rows * cols; k++) {
            out.add(m[r][c]);
            seen[r][c] = true;
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || seen[nr][nc]) {
                d = (d + 1) % 4;
                nr = r + dr[d]; nc = c + dc[d];
            }
            r = nr; c = nc;
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}, {10, 11, 12}};
        if (!spiralOrder(a).equals(Arrays.asList(1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8))) throw new AssertionError("example 1: " + spiralOrder(a));
        if (!spiralOrder(new int[][] {{1, 2}, {3, 4}, {5, 6}}).equals(Arrays.asList(1, 2, 4, 6, 5, 3))) throw new AssertionError("example 2");
        for (int rows = 1; rows <= 7; rows++)
            for (int cols = 1; cols <= 7; cols++) {
                int[][] m = new int[rows][cols];
                for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) m[r][c] = r * 10 + c;
                if (!spiralOrder(m).equals(byVisitedGrid(m))) throw new AssertionError("disagrees with the visited-grid simulation on " + rows + "x" + cols);
            }
    }
}
```

#### Solution: [Boundary] Thin Remainder (LeetCode 54)
<!-- id: mx-thin-remainder -->

**Approach.** For a single row, the top strip emits the whole row and `top` then exceeds `bottom`. Without the guard `top <= bottom`, the bottom strip would run and emit the row again in reverse. For a single column, the right strip emits everything after the first cell and `right` drops below `left`, and without the guard `left <= right` the left strip would emit part of the column a second time. The assertions run a guarded and an unguarded version, show the repeats of the unguarded one on both shapes, and confirm that the guarded one returns each cell once.

**Complexity.** O(rows * cols) time and O(1) extra space apart from the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class ThinRemainder {
    static List<Integer> spiral(int[][] m, boolean guarded) {
        List<Integer> out = new ArrayList<>();
        int top = 0, bottom = m.length - 1, left = 0, right = m[0].length - 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) out.add(m[top][c]);
            top++;
            for (int r = top; r <= bottom; r++) out.add(m[r][right]);
            right--;
            if (!guarded || top <= bottom) {
                for (int c = right; c >= left; c--) out.add(m[bottom][c]);
                bottom--;
            }
            if (!guarded || left <= right) {
                for (int r = bottom; r >= top; r--) out.add(m[r][left]);
                left++;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] row = {{9, 8, 7}};
        int[][] col = {{1}, {2}, {3}, {4}};
        if (!spiral(row, true).equals(Arrays.asList(9, 8, 7))) throw new AssertionError("example 1");
        if (!spiral(col, true).equals(Arrays.asList(1, 2, 3, 4))) throw new AssertionError("example 2");
        if (spiral(row, false).size() <= 3) throw new AssertionError("without the bottom guard a single row repeats cells");
        if (spiral(col, false).size() <= 4) throw new AssertionError("without the left guard a single column repeats cells");
        for (int n = 1; n <= 8; n++) {
            int[][] r1 = new int[1][n], c1 = new int[n][1];
            for (int i = 0; i < n; i++) { r1[0][i] = i; c1[i][0] = i; }
            if (spiral(r1, true).size() != n || spiral(c1, true).size() != n) throw new AssertionError("each cell once for n = " + n);
        }
    }
}
```

#### Solution: [Recognize] Spiral Matrix II By Layers (LeetCode 59)
<!-- id: mx-spiral-layers-fill -->

**Approach.** Run the same four strips, but write an increasing counter into each visited cell instead of reading from it. The guards before the bottom and left strips are still needed so that a single remaining row or column, the center cell of an odd matrix, is written once. The oracle is the heading simulation from the direction-state lesson, and the assertions also check that every number from 1 to `n * n` appears exactly once.

**Complexity.** O(n^2) time and O(1) extra space apart from the output.

```java run
import java.util.Arrays;

public final class SpiralLayersFill {
    static int[][] fillByLayers(int n) {
        int[][] g = new int[n][n];
        int top = 0, bottom = n - 1, left = 0, right = n - 1, v = 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) g[top][c] = v++;
            top++;
            for (int r = top; r <= bottom; r++) g[r][right] = v++;
            right--;
            if (top <= bottom) { for (int c = right; c >= left; c--) g[bottom][c] = v++; bottom--; }
            if (left <= right) { for (int r = bottom; r >= top; r--) g[r][left] = v++; left++; }
        }
        return g;
    }
    static int[][] byHeading(int n) {
        int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
        int[][] grid = new int[n][n];
        int r = 0, c = 0, d = 0, total = n * n;
        for (int v = 1; v <= total; v++) {
            grid[r][c] = v;
            if (v == total) break;
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n || grid[nr][nc] != 0) { d = (d + 1) % 4; nr = r + dr[d]; nc = c + dc[d]; }
            r = nr; c = nc;
        }
        return grid;
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(fillByLayers(3), new int[][] {{1, 2, 3}, {8, 9, 4}, {7, 6, 5}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(fillByLayers(1), new int[][] {{1}})) throw new AssertionError("example 2");
        for (int n = 1; n <= 15; n++) {
            int[][] g = fillByLayers(n);
            if (!Arrays.deepEquals(g, byHeading(n))) throw new AssertionError("disagrees with the heading simulation at n = " + n);
            boolean[] seen = new boolean[n * n + 1];
            for (int[] row : g) for (int v : row) {
                if (v < 1 || v > n * n || seen[v]) throw new AssertionError("value " + v + " repeated or out of range");
                seen[v] = true;
            }
        }
    }
}
```
