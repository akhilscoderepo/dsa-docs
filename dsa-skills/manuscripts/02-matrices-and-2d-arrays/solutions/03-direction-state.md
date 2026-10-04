<!-- solutions-for: 03-direction-state -->
### Solutions For Moving With A Direction

#### Solution: [Build] Clockwise Walker (Author exercise)
<!-- id: mx-clockwise-walker -->

**Approach.**
The state is the position `(r, c)` and the direction index `d`. Each step computes the next cell from the direction table. If that cell is outside the grid, the walker rotates with `d = (d + 1) % 4` and recomputes the next cell. The grid has at least two rows and two columns, so one rotation always leaves a legal move. The invariant is that after `s` steps the pair `(r, c)` is where a walker that obeyed the rule would stand after `s` steps. The loop runs `steps` times, and no cell is ever marked.

**Complexity.**
- **Time** is O(steps), because each step does a constant amount of work.
- **Space** is O(1), because the state is two positions and one direction index.

```java run
public final class ClockwiseWalker {
    // The direction table is allocated once, outside the loop that reads it.
    private static final int[] DR = {0, 1, 0, -1};
    private static final int[] DC = {1, 0, -1, 0};

    /**
     * Returns the cell after the given number of steps along the border.
     * Time: O(steps). Space: O(1).
     * Invariant: (r, c) is the walker's cell after the steps taken so far, and d faces its next move.
     */
    static int[] walk(int rows, int cols, int steps) {
        // The walker starts at the top-left cell facing right, which is direction index 0.
        int r = 0, c = 0, d = 0;
        // Each iteration is one step, so the loop costs steps iterations.
        for (int s = 0; s < steps; s++) {
            // Candidate next cell in the current direction.
            int nr = r + DR[d], nc = c + DC[d];
            // Only the grid edge blocks the walker here, because no cell is marked.
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
                // A quarter turn clockwise; the fourth turn returns to direction 0.
                d = (d + 1) % 4;
                // At least two rows and columns exist, so the rotated move is legal.
                nr = r + DR[d];
                nc = c + DC[d];
            }
            // Commit the move.
            r = nr;
            c = nc;
        }
        // The final cell is returned as row and column.
        return new int[] {r, c};
    }

    /** Oracle: lists the border cells clockwise and indexes into that cycle. */
    static int[] oracle(int rows, int cols, int steps) {
        java.util.List<int[]> ring = new java.util.ArrayList<>();
        for (int c = 0; c < cols - 1; c++) ring.add(new int[] {0, c});
        for (int r = 0; r < rows - 1; r++) ring.add(new int[] {r, cols - 1});
        for (int c = cols - 1; c > 0; c--) ring.add(new int[] {rows - 1, c});
        for (int r = rows - 1; r > 0; r--) ring.add(new int[] {r, 0});
        return ring.get(steps % ring.size());
    }

    public static void main(String[] args) {
        // Statement examples.
        int[] a = walk(2, 3, 7);
        if (a[0] != 0 || a[1] != 1) throw new AssertionError("example 1");
        int[] b = walk(2, 2, 4);
        if (b[0] != 0 || b[1] != 0) throw new AssertionError("example 2");
        // Zero steps leaves the walker at its start.
        int[] z = walk(5, 5, 0);
        if (z[0] != 0 || z[1] != 0) throw new AssertionError("zero steps");
        // Every grid size from 2 by 2 to 6 by 6 and many step counts are checked against the ring oracle.
        for (int R = 2; R <= 6; R++) for (int C = 2; C <= 6; C++) for (int s = 0; s <= 40; s++) {
            int[] x = walk(R, C, s), y = oracle(R, C, s);
            if (x[0] != y[0] || x[1] != y[1]) throw new AssertionError(R + "x" + C + " steps " + s);
        }
    }
}
```

#### Solution: [Vary] Spiral Matrix II (LeetCode 59)
<!-- id: mx-spiral-fill -->

**Approach.**
The matrix starts with zeros, and the value 0 means that a cell is empty. The loop writes each value from 1 to `n * n` at the cursor. It then computes the next cell and checks two conditions: the cell is outside the matrix, or it already holds a nonzero value. If either holds, the direction index advances by one, and the next cell is recomputed. The invariant is that the cursor always stands on an empty cell when a value is written. This holds because a turn happens exactly when the straight move is blocked, and a spiral always has an empty cell in the turned direction until the last value.

**Complexity.**
- **Time** is O(n^2), because each of the `n * n` values costs constant work.
- **Space** is O(1) beyond the returned matrix, because the matrix itself records which cells are filled.

```java run
public final class SpiralFill {
    private static final int[] DR = {0, 1, 0, -1};
    private static final int[] DC = {1, 0, -1, 0};

    /**
     * Builds an n by n matrix holding 1..n*n in clockwise spiral order.
     * Time: O(n^2). Space: O(1) beyond the output.
     * Invariant: the cursor stands on an empty cell whenever a value is written.
     */
    static int[][] generate(int n) {
        // A new matrix is the output, and its zeros mark empty cells.
        int[][] g = new int[n][n];
        int r = 0, c = 0, d = 0;
        // One iteration per value, n * n in total.
        for (int v = 1; v <= n * n; v++) {
            // Write the value at the cursor.
            g[r][c] = v;
            // Candidate next cell in the current direction.
            int nr = r + DR[d], nc = c + DC[d];
            // A cell outside the matrix or already filled blocks the straight move.
            if (nr < 0 || nr >= n || nc < 0 || nc >= n || g[nr][nc] != 0) {
                // Turn clockwise and recompute; the turned cell is empty except after the last write.
                d = (d + 1) % 4;
                nr = r + DR[d];
                nc = c + DC[d];
            }
            // Commit the move; after the last write this cell is never read.
            r = nr;
            c = nc;
        }
        return g;
    }

    /** Oracle: shrinking bounds, a different algorithm that gives the same matrix. */
    static int[][] oracle(int n) {
        int[][] g = new int[n][n];
        int top = 0, bottom = n - 1, left = 0, right = n - 1, v = 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) g[top][c] = v++;
            top++;
            for (int r = top; r <= bottom; r++) g[r][right] = v++;
            right--;
            for (int c = right; c >= left; c--) g[bottom][c] = v++;
            bottom--;
            for (int r = bottom; r >= top; r--) g[r][left] = v++;
            left++;
        }
        return g;
    }

    public static void main(String[] args) {
        // Statement examples, written out in full.
        if (!java.util.Arrays.deepEquals(generate(3), new int[][] {{1, 2, 3}, {8, 9, 4}, {7, 6, 5}})) throw new AssertionError("n=3");
        if (!java.util.Arrays.deepEquals(generate(4), new int[][] {{1, 2, 3, 4}, {12, 13, 14, 5}, {11, 16, 15, 6}, {10, 9, 8, 7}})) throw new AssertionError("n=4");
        // The smallest size writes a single 1.
        if (generate(1)[0][0] != 1) throw new AssertionError("n=1");
        // Every size up to 20 is checked against the oracle, and no zero may remain.
        for (int n = 1; n <= 20; n++) {
            int[][] g = generate(n);
            if (!java.util.Arrays.deepEquals(g, oracle(n))) throw new AssertionError("oracle n=" + n);
            for (int[] row : g) for (int x : row) if (x == 0) throw new AssertionError("zero left n=" + n);
        }
    }
}
```

#### Solution: [Boundary] Single Cell (Author exercise)
<!-- id: mx-single-cell -->

**Approach.**
The simulation is the same as in the spiral fill, extended to an `R x C` grid. After writing each value except the last, the code tests the next cell and counts one turn when the straight move is blocked. The loop stops right after the last write without testing the next cell. This stop rule gives 0 turns for a `1 x 1` grid. The invariant is that the turn counter equals the number of direction changes between the first and the current write.

**Complexity.**
- **Time** is O(R * C), because each cell is written once and tested once.
- **Space** is O(R * C), because the grid records which cells are filled.

```java run
public final class SingleCell {
    private static final int[] DR = {0, 1, 0, -1};
    private static final int[] DC = {1, 0, -1, 0};

    /**
     * Counts the turns made while filling an R by C grid clockwise.
     * Time: O(R * C). Space: O(R * C) for the filled marks.
     * Invariant: turns equals the direction changes made before the current write.
     */
    static int countTurns(int rows, int cols) {
        boolean[][] filled = new boolean[rows][cols];
        int r = 0, c = 0, d = 0, turns = 0;
        // One iteration per cell, rows * cols in total.
        for (int v = 1; v <= rows * cols; v++) {
            // Mark the cursor cell as written.
            filled[r][c] = true;
            // After the last write the walker stops, so no turn is counted for it.
            if (v == rows * cols) break;
            int nr = r + DR[d], nc = c + DC[d];
            // A blocked straight move forces exactly one counted turn.
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || filled[nr][nc]) {
                d = (d + 1) % 4;
                turns++;
                nr = r + DR[d];
                nc = c + DC[d];
            }
            r = nr;
            c = nc;
        }
        return turns;
    }

    /** Oracle: builds the spiral order with shrinking bounds and counts changes of step direction. */
    static int oracle(int rows, int cols) {
        java.util.List<int[]> path = new java.util.ArrayList<>();
        int top = 0, bottom = rows - 1, left = 0, right = cols - 1;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) path.add(new int[] {top, c});
            for (int r = top + 1; r <= bottom; r++) path.add(new int[] {r, right});
            if (top < bottom) for (int c = right - 1; c >= left; c--) path.add(new int[] {bottom, c});
            if (left < right) for (int r = bottom - 1; r > top; r--) path.add(new int[] {r, left});
            top++; bottom--; left++; right--;
        }
        int turns = 0, pdr = 0, pdc = 1; // the walker starts facing right
        for (int i = 1; i < path.size(); i++) {
            int dr = path.get(i)[0] - path.get(i - 1)[0], dc = path.get(i)[1] - path.get(i - 1)[1];
            if (dr != pdr || dc != pdc) turns++;
            pdr = dr; pdc = dc;
        }
        return turns;
    }

    public static void main(String[] args) {
        // The single cell never moves and never turns.
        if (countTurns(1, 1) != 0) throw new AssertionError("1x1");
        // The 3 by 3 spiral turns four times, as in the statement.
        if (countTurns(3, 3) != 4) throw new AssertionError("3x3");
        // A single row never turns, but a single column turns once because the walker starts facing right.
        if (countTurns(1, 5) != 0 || countTurns(5, 1) != 1) throw new AssertionError("line");
        // Every rectangle up to 8 by 8 is checked against the oracle.
        for (int R = 1; R <= 8; R++) for (int C = 1; C <= 8; C++)
            if (countTurns(R, C) != oracle(R, C)) throw new AssertionError(R + "x" + C);
    }
}
```

#### Solution: [Recognize] Spiral Matrix III (LeetCode 885)
<!-- id: mx-spiral-outward -->

**Approach.**
The path on the plane is fixed. It uses segment lengths 1, 1, 2, 2, 3, 3 and so on, with the directions right, down, left and up in order. The loop keeps the cursor, the direction index and the current segment length. For each segment it moves one cell at a time and records the cell only when it lies inside the grid. After every two segments the length grows by 1. The loop ends when `R * C` cells are recorded. The invariant is that the cursor visits plane cells in spiral order, so the recorded cells appear in the order the walker first stands on them. A cell is never visited twice, because the spiral never revisits a cell.

**Complexity.**
- **Time** is O(max(R, C)^2), because the walker must cover a square of side about `2 * max(R, C)` around the start before it has seen every grid cell.
- **Space** is O(R * C), because the result lists every cell.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class SpiralOutward {
    private static final int[] DR = {0, 1, 0, -1};
    private static final int[] DC = {1, 0, -1, 0};

    /**
     * Lists grid cells in the order an outward clockwise spiral first stands on them.
     * Time: O(max(R, C)^2). Space: O(R * C) for the result.
     * Invariant: the cursor follows the infinite spiral; only in-grid cells are recorded.
     */
    static int[][] spiral(int rows, int cols, int rStart, int cStart) {
        int[][] out = new int[rows * cols][];
        int count = 0, r = rStart, c = cStart, d = 0, len = 1;
        // The start cell is inside the grid by the constraints, so it is recorded first.
        out[count++] = new int[] {r, c};
        // Keep walking until every grid cell has been recorded.
        while (count < rows * cols) {
            // Two segments share each length, so this loop runs twice per length.
            for (int rep = 0; rep < 2; rep++) {
                // Walk len cells in the current direction.
                for (int s = 0; s < len; s++) {
                    r += DR[d];
                    c += DC[d];
                    // Cells outside the grid are walked but never recorded.
                    if (r >= 0 && r < rows && c >= 0 && c < cols) out[count++] = new int[] {r, c};
                }
                // Rotate clockwise for the next segment.
                d = (d + 1) % 4;
            }
            // The length grows after both segments of one length are done.
            len++;
        }
        return out;
    }

    /** Oracle: turns right whenever the cell on the right is unvisited, which is the spiral property. */
    static int[][] oracle(int rows, int cols, int rStart, int cStart) {
        Set<Long> seen = new HashSet<>();
        List<int[]> out = new ArrayList<>();
        // Facing up at the start makes the right-hand rule choose east first.
        int r = rStart, c = cStart, d = 3;
        seen.add(key(r, c));
        out.add(new int[] {r, c});
        while (out.size() < rows * cols) {
            int rd = (d + 1) % 4;
            if (!seen.contains(key(r + DR[rd], c + DC[rd]))) d = rd;
            r += DR[d];
            c += DC[d];
            if (seen.add(key(r, c)) && r >= 0 && r < rows && c >= 0 && c < cols) out.add(new int[] {r, c});
        }
        return out.toArray(new int[0][]);
    }
    private static long key(int r, int c) { return (long) (r + 100) * 1000 + (c + 100); }

    public static void main(String[] args) {
        // Statement examples, recomputed by the method itself.
        if (!java.util.Arrays.deepEquals(spiral(1, 4, 0, 1), new int[][] {{0, 1}, {0, 2}, {0, 0}, {0, 3}})) throw new AssertionError("example 1");
        if (!java.util.Arrays.deepEquals(spiral(2, 2, 1, 0), new int[][] {{1, 0}, {1, 1}, {0, 0}, {0, 1}})) throw new AssertionError("example 2");
        // A single cell is listed once with no walking.
        if (spiral(1, 1, 0, 0).length != 1) throw new AssertionError("single cell");
        // Random grids and starts are checked against the oracle.
        Random rnd = new Random(15);
        for (int t = 0; t < 300; t++) {
            int R = 1 + rnd.nextInt(7), C = 1 + rnd.nextInt(7), rs = rnd.nextInt(R), cs = rnd.nextInt(C);
            if (!java.util.Arrays.deepEquals(spiral(R, C, rs, cs), oracle(R, C, rs, cs))) throw new AssertionError("random " + t);
        }
    }
}
```
