<!-- solutions-for: 03-direction-state -->
### Direction State

#### Solution: [Build] Clockwise Walker (Author exercise)
<!-- id: mx-clockwise-walker -->

**Approach.** Keep the row, the column and the heading as an index into two offset tables ordered east, south, west, north. Before each step, if the cell ahead is off the board, increase the heading by one modulo four, and step in the new direction. On a board with at least two rows and two columns, one turn always opens a cell. The assertions check both examples and compare the heading and position with a separately written oracle that unrolls the same walk using the perimeter order of the board.

**Complexity.** O(steps) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public final class ClockwiseWalker {
    static final int[] DR = {0, 1, 0, -1};
    static final int[] DC = {1, 0, -1, 0};

    static int[] walk(int rows, int cols, int steps) {
        int r = 0, c = 0, d = 0;
        for (int s = 0; s < steps; s++) {
            int nr = r + DR[d], nc = c + DC[d];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
                d = (d + 1) % 4;
                nr = r + DR[d]; nc = c + DC[d];
            }
            r = nr; c = nc;
        }
        return new int[] {r, c, d};
    }
    static int[] oracle(int rows, int cols, int steps) {    // the walk is a loop around the border
        List<int[]> ring = new ArrayList<>();
        for (int c = 0; c < cols - 1; c++) ring.add(new int[] {0, c, 0});
        for (int r = 0; r < rows - 1; r++) ring.add(new int[] {r, cols - 1, 1});
        for (int c = cols - 1; c > 0; c--) ring.add(new int[] {rows - 1, c, 2});
        for (int r = rows - 1; r > 0; r--) ring.add(new int[] {r, 0, 3});
        int[] at = ring.get(steps % ring.size());
        return new int[] {at[0], at[1], at[2]};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(walk(3, 3, 5), new int[] {2, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(walk(2, 2, 4), new int[] {0, 0, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(walk(4, 5, 0), new int[] {0, 0, 0})) throw new AssertionError("zero steps");
        for (int rows = 2; rows <= 6; rows++)
            for (int cols = 2; cols <= 6; cols++)
                for (int steps = 0; steps <= 60; steps++) {
                    int[] got = walk(rows, cols, steps), expected = oracle(rows, cols, steps);
                    if (got[0] != expected[0] || got[1] != expected[1]) throw new AssertionError("position " + rows + "x" + cols + " steps " + steps);
                }
    }
}
```

#### Solution: [Vary] Spiral Matrix II (LeetCode 59)
<!-- id: mx-spiral-matrix-two -->

**Approach.** Write the next number at the cursor, then look one step ahead in the current heading. If that cell is off the board or already holds a nonzero number, turn clockwise once, which always opens the next cell while any remain. The output grid doubles as the visited record because every written number is at least 1. The assertions check the examples, that every number from 1 to `n * n` appears exactly once, and that consecutive numbers are in adjacent cells.

**Complexity.** O(n^2) time and O(1) extra space apart from the output.

```java run
import java.util.Arrays;

public final class SpiralMatrixTwo {
    static final int[] DR = {0, 1, 0, -1};
    static final int[] DC = {1, 0, -1, 0};

    static int[][] spiralFill(int n) {
        int[][] grid = new int[n][n];
        int r = 0, c = 0, d = 0, total = n * n;
        for (int v = 1; v <= total; v++) {
            grid[r][c] = v;
            if (v == total) break;
            int nr = r + DR[d], nc = c + DC[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n || grid[nr][nc] != 0) {
                d = (d + 1) % 4;
                nr = r + DR[d]; nc = c + DC[d];
            }
            r = nr; c = nc;
        }
        return grid;
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(spiralFill(4), new int[][] {{1, 2, 3, 4}, {12, 13, 14, 5}, {11, 16, 15, 6}, {10, 9, 8, 7}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(spiralFill(2), new int[][] {{1, 2}, {4, 3}})) throw new AssertionError("example 2");
        for (int n = 1; n <= 12; n++) {
            int[][] g = spiralFill(n);
            int[] where = new int[n * n + 1];
            Arrays.fill(where, -1);
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) {
                int v = g[r][c];
                if (v < 1 || v > n * n || where[v] != -1) throw new AssertionError("value " + v + " misplaced or repeated at n = " + n);
                where[v] = r * n + c;
            }
            for (int v = 1; v < n * n; v++) {
                int r1 = where[v] / n, c1 = where[v] % n, r2 = where[v + 1] / n, c2 = where[v + 1] % n;
                if (Math.abs(r1 - r2) + Math.abs(c1 - c2) != 1) throw new AssertionError("values " + v + " and " + (v + 1) + " are not adjacent");
            }
        }
    }
}
```

#### Solution: [Boundary] Single Cell (Author exercise)
<!-- id: mx-single-cell -->

**Approach.** The loop writes a value and then stops if that value was the last one, before computing any next position. On a one-by-one board the first write is also the last, so there is one write and no turn. Without the early stop, the loop would look one step east, find the board edge, turn, and compute a position that does not exist. The turn is harmless to the output only because that position is never used, but it is a turn that should not happen. The assertions count writes and turns with and without the stop and compare the turn counts for `n = 1`, 2 and 3.

**Complexity.** O(n^2) time and O(1) extra space apart from the output.

```java run
public final class SingleCell {
    static final int[] DR = {0, 1, 0, -1};
    static final int[] DC = {1, 0, -1, 0};

    static int[] counts(int n, boolean stopAtLast) {            // returns {writes, turns}
        int[][] grid = new int[n][n];
        int r = 0, c = 0, d = 0, total = n * n, writes = 0, turns = 0;
        for (int v = 1; v <= total; v++) {
            grid[r][c] = v; writes++;
            if (stopAtLast && v == total) break;
            int nr = r + DR[d], nc = c + DC[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n || grid[nr][nc] != 0) {
                d = (d + 1) % 4; turns++;
                nr = r + DR[d]; nc = c + DC[d];
            }
            if (nr < 0 || nr >= n || nc < 0 || nc >= n) break;      // nothing is left to visit
            r = nr; c = nc;
        }
        return new int[] {writes, turns};
    }

    public static void main(String[] args) {
        int[] one = counts(1, true);
        if (one[0] != 1 || one[1] != 0) throw new AssertionError("n = 1 must write once and never turn");
        int[] oneLoose = counts(1, false);
        if (oneLoose[1] != 1) throw new AssertionError("without the stop the loop turns once for nothing");
        int[] two = counts(2, true);
        if (two[0] != 4 || two[1] != 2) throw new AssertionError("n = 2: " + two[0] + " writes, " + two[1] + " turns");
        int[] three = counts(3, true);
        if (three[0] != 9 || three[1] != 4) throw new AssertionError("n = 3: " + three[0] + " writes, " + three[1] + " turns");
    }
}
```

#### Solution: [Recognize] Spiral Matrix III (LeetCode 885)
<!-- id: mx-spiral-matrix-three -->

**Approach.** The cursor state is the row, the column and the heading, plus the length of the current leg. The legs have lengths 1, 1, 2, 2, 3, 3 and so on, so the leg length grows by one after every second turn. The cursor takes one step at a time, records the cell when it is inside the grid, and turns when the leg is used up. The loop ends when every cell has been recorded. The assertions compare the examples with fixed arrays and check, on every start of random grids, that each cell appears exactly once, that the first cell is the start, and that the maximum of the row and column distances from the start never decreases along the output, as it must for a square spiral.

**Complexity.** O(max(rows, cols)^2) time, since the spiral may have to reach the farthest corner, and O(1) extra space apart from the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class SpiralMatrixThree {
    static final int[] DR = {0, 1, 0, -1};
    static final int[] DC = {1, 0, -1, 0};

    static int[][] spiral(int rows, int cols, int rStart, int cStart) {
        List<int[]> out = new ArrayList<>();
        int r = rStart, c = cStart, d = 0, leg = 1, legsAtLength = 0;
        out.add(new int[] {r, c});
        while (out.size() < rows * cols) {
            for (int s = 0; s < leg; s++) {
                r += DR[d]; c += DC[d];
                if (r >= 0 && r < rows && c >= 0 && c < cols) out.add(new int[] {r, c});
            }
            d = (d + 1) % 4;
            if (++legsAtLength == 2) { legsAtLength = 0; leg++; }
        }
        return out.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        int[][] a = spiral(2, 3, 1, 1);
        if (!Arrays.deepEquals(a, new int[][] {{1, 1}, {1, 2}, {1, 0}, {0, 0}, {0, 1}, {0, 2}})) throw new AssertionError("example 1: " + Arrays.deepToString(a));
        if (!Arrays.deepEquals(spiral(1, 1, 0, 0), new int[][] {{0, 0}})) throw new AssertionError("example 2");
        for (int rows = 1; rows <= 6; rows++)
            for (int cols = 1; cols <= 6; cols++)
                for (int rs = 0; rs < rows; rs++)
                    for (int cs = 0; cs < cols; cs++) {
                        int[][] got = spiral(rows, cols, rs, cs);
                        if (got.length != rows * cols) throw new AssertionError("every cell must be recorded");
                        if (got[0][0] != rs || got[0][1] != cs) throw new AssertionError("the start comes first");
                        boolean[][] seen = new boolean[rows][cols];
                        int ring = 0;
                        for (int[] p : got) {
                            if (seen[p[0]][p[1]]) throw new AssertionError("a cell was recorded twice");
                            seen[p[0]][p[1]] = true;
                            int dist = Math.max(Math.abs(p[0] - rs), Math.abs(p[1] - cs));
                            if (dist < ring) throw new AssertionError("the ring distance must not decrease");
                            ring = dist;
                        }
                    }
    }
}
```
