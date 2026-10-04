<!-- solutions-for: 04-neighbor-enumeration -->
### Solutions For Neighbor Checks

#### Solution: [Build] Orthogonal Count (Author exercise)
<!-- id: mx-orthogonal-count -->

**Approach.**
The four offsets form a direction table that is allocated once. For each offset the method computes the candidate `(r + dr, c + dc)` and applies the range test `0 <= nr < R` and `0 <= nc < C` once. Each candidate that passes adds 1 to the count. The invariant is that after `k` offsets, the count equals the number of legal candidates among the first `k` offsets of the table.

**Complexity.**
- **Time** is O(1), because the table holds four offsets and each costs constant work.
- **Space** is O(1), because the method stores only the count and the candidate.

```java run
public final class OrthogonalCount {
    // The table is created once, so no call allocates it again.
    private static final int[][] DIRS4 = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

    /**
     * Counts the orthogonal neighbors of (r, c) inside an R by C grid.
     * Time: O(1), four offsets. Space: O(1).
     * Invariant: after k offsets, count equals the legal candidates among those k.
     */
    static int orthogonal(int rows, int cols, int r, int c) {
        int count = 0;
        // The loop runs four times, one for each offset in the table.
        for (int[] d : DIRS4) {
            // Candidate cell reached by this offset.
            int nr = r + d[0], nc = c + d[1];
            // One range test decides whether the candidate lies inside the grid.
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) count++;
        }
        // The count is between 0 and 4.
        return count;
    }

    /** Oracle: tests every grid cell for a Manhattan distance of exactly 1 from (r, c). */
    static int oracle(int rows, int cols, int r, int c) {
        int n = 0;
        for (int i = 0; i < rows; i++) for (int j = 0; j < cols; j++) if (Math.abs(i - r) + Math.abs(j - c) == 1) n++;
        return n;
    }

    public static void main(String[] args) {
        // Statement examples: an interior cell and a corner.
        if (orthogonal(3, 4, 1, 2) != 4) throw new AssertionError("example 1");
        if (orthogonal(3, 4, 0, 0) != 2) throw new AssertionError("example 2");
        // A single cell has no neighbors.
        if (orthogonal(1, 1, 0, 0) != 0) throw new AssertionError("single cell");
        // Every cell of every grid up to 5 by 5 is checked against the oracle.
        for (int R = 1; R <= 5; R++) for (int C = 1; C <= 5; C++) for (int r = 0; r < R; r++) for (int c = 0; c < C; c++)
            if (orthogonal(R, C, r, c) != oracle(R, C, r, c)) throw new AssertionError(R + "x" + C + " " + r + "," + c);
    }
}
```

#### Solution: [Vary] Eight Neighbors (Author exercise)
<!-- id: mx-eight-neighbors -->

**Approach.**
The eight-offset table adds the four diagonal offsets and leaves out `(0, 0)`. The loop and the range test are the same as in the orthogonal count, and only the table differs. Leaving out the zero offset keeps the cell from counting as its own neighbor. The invariant is that each of the eight offsets is tried once.

**Complexity.**
- **Time** is O(1), because the table holds eight offsets.
- **Space** is O(1), because the method stores only the count and the candidate.

```java run
public final class EightNeighbors {
    // Eight offsets, with no (0, 0) entry, allocated once.
    private static final int[][] DIRS8 = {
        {-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

    /**
     * Counts the eight neighbors of (r, c) inside an R by C grid.
     * Time: O(1), eight offsets. Space: O(1).
     * Invariant: each offset of the table is tried exactly once.
     */
    static int eight(int rows, int cols, int r, int c) {
        int count = 0;
        // Eight iterations, one for each offset.
        for (int[] d : DIRS8) {
            // Candidate cell for this offset.
            int nr = r + d[0], nc = c + d[1];
            // The same single range test as in the four-offset case.
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) count++;
        }
        return count;
    }

    /** Oracle: tests every grid cell for Chebyshev distance exactly 1 from (r, c). */
    static int oracle(int rows, int cols, int r, int c) {
        int n = 0;
        for (int i = 0; i < rows; i++) for (int j = 0; j < cols; j++) if (Math.max(Math.abs(i - r), Math.abs(j - c)) == 1) n++;
        return n;
    }

    public static void main(String[] args) {
        // Statement examples: an interior cell and a corner of a 3 by 4 grid.
        if (eight(3, 3, 1, 1) != 8) throw new AssertionError("example 1");
        if (eight(3, 4, 0, 3) != 3) throw new AssertionError("example 2");
        // The table has no zero offset, so a lone cell counts 0 and not 1.
        if (eight(1, 1, 0, 0) != 0) throw new AssertionError("self");
        // A one-row grid has only the left and right neighbors.
        if (eight(1, 5, 0, 2) != 2) throw new AssertionError("one row");
        // Every cell of every grid up to 5 by 5 is checked against the oracle.
        for (int R = 1; R <= 5; R++) for (int C = 1; C <= 5; C++) for (int r = 0; r < R; r++) for (int c = 0; c < C; c++)
            if (eight(R, C, r, c) != oracle(R, C, r, c)) throw new AssertionError(R + "x" + C + " " + r + "," + c);
    }
}
```

#### Solution: [Boundary] Corner Cell (Author exercise)
<!-- id: mx-corner-cell -->

**Approach.**
The method uses the eight-offset table in an order that already sorts the candidates by row and then by column: the offsets are listed from `(-1, -1)` to `(1, 1)` in row-major order, and the center is absent. Appending each legal candidate in table order therefore produces the required order without a sort. The range test removes every candidate with a negative index or an index at the grid size, so no illegal index is ever read. The invariant is that the output holds the legal candidates of the offsets already tried, in the required order.

**Complexity.**
- **Time** is O(1), because the table holds eight offsets.
- **Space** is O(1), because the output holds at most 8 pairs.

```java run
import java.util.ArrayList;
import java.util.List;

public final class CornerCell {
    // Row-major offset order makes the output order automatic.
    private static final int[][] DIRS8 = {
        {-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

    /**
     * Lists the in-grid neighbors of (r, c) in row-major order.
     * Time: O(1), eight offsets. Space: O(1), at most eight pairs.
     * Invariant: the list holds the legal candidates of the offsets tried so far, in sorted order.
     */
    static List<int[]> neighbors(int rows, int cols, int r, int c) {
        List<int[]> out = new ArrayList<>();
        // Eight iterations; the table order is already row-major.
        for (int[] d : DIRS8) {
            int nr = r + d[0], nc = c + d[1];
            // A negative index or an index at the grid size fails this test, so it is never read.
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) out.add(new int[] {nr, nc});
        }
        return out;
    }

    /** Oracle: scans the whole grid in row-major order and keeps cells at Chebyshev distance 1. */
    static List<int[]> oracle(int rows, int cols, int r, int c) {
        List<int[]> out = new ArrayList<>();
        for (int i = 0; i < rows; i++) for (int j = 0; j < cols; j++)
            if (Math.max(Math.abs(i - r), Math.abs(j - c)) == 1) out.add(new int[] {i, j});
        return out;
    }

    public static void main(String[] args) {
        // Statement examples.
        List<int[]> a = neighbors(3, 3, 0, 0);
        if (a.size() != 3 || a.get(0)[0] != 0 || a.get(0)[1] != 1 || a.get(1)[0] != 1 || a.get(1)[1] != 0 || a.get(2)[0] != 1 || a.get(2)[1] != 1)
            throw new AssertionError("example 1");
        if (!neighbors(1, 1, 0, 0).isEmpty()) throw new AssertionError("example 2");
        // A one-row grid, middle cell: left and right only.
        List<int[]> b = neighbors(1, 3, 0, 1);
        if (b.size() != 2 || b.get(0)[1] != 0 || b.get(1)[1] != 2) throw new AssertionError("one row");
        // Every cell of every grid up to 5 by 5 matches the oracle, including order.
        for (int R = 1; R <= 5; R++) for (int C = 1; C <= 5; C++) for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) {
            List<int[]> x = neighbors(R, C, r, c), y = oracle(R, C, r, c);
            if (x.size() != y.size()) throw new AssertionError("size " + R + "x" + C);
            for (int i = 0; i < x.size(); i++) if (x.get(i)[0] != y.get(i)[0] || x.get(i)[1] != y.get(i)[1]) throw new AssertionError("order");
        }
    }
}
```

#### Solution: [Recognize] Game Of Life (LeetCode 289)
<!-- id: mx-life-next -->

**Approach.**
The method allocates a second board for the next generation. For each cell it counts live neighbors by looping over the eight-offset table on the current board and applies the four rules to produce the new value. Writes go only to the new board and reads come only from the old one, so every neighbor read sees the current generation. The invariant is that the old board never changes during the pass, which makes the update simultaneous.

**Complexity.**
- **Time** is O(m * n), because each cell does eight constant-time reads.
- **Space** is O(m * n), because the new board has the same size as the input.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LifeNext {
    private static final int[][] DIRS8 = {
        {-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

    /**
     * Returns the next generation and leaves the input board unchanged.
     * Time: O(m * n), eight reads per cell. Space: O(m * n) for the new board.
     * Invariant: reads use only the old board, writes use only the new one.
     */
    static int[][] next(int[][] board) {
        int m = board.length, n = board[0].length;
        // The second board holds the new generation.
        int[][] out = new int[m][n];
        // Visit every cell once, which costs m * n iterations.
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                // Count live neighbors on the old board with the shared table.
                int live = 0;
                for (int[] d : DIRS8) {
                    int nr = r + d[0], nc = c + d[1];
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n) live += board[nr][nc];
                }
                // A live cell survives with 2 or 3 live neighbors; a dead cell is born with exactly 3.
                out[r][c] = board[r][c] == 1 ? (live == 2 || live == 3 ? 1 : 0) : (live == 3 ? 1 : 0);
            }
        }
        return out;
    }

    /** Oracle: sums the clipped 3 by 3 window and subtracts the center. */
    static int[][] oracle(int[][] b) {
        int m = b.length, n = b[0].length;
        int[][] out = new int[m][n];
        for (int r = 0; r < m; r++) for (int c = 0; c < n; c++) {
            int s = 0;
            for (int i = Math.max(0, r - 1); i <= Math.min(m - 1, r + 1); i++)
                for (int j = Math.max(0, c - 1); j <= Math.min(n - 1, c + 1); j++) s += b[i][j];
            s -= b[r][c];
            out[r][c] = (s == 3 || (s == 2 && b[r][c] == 1)) ? 1 : 0;
        }
        return out;
    }

    public static void main(String[] args) {
        // Statement examples.
        if (!Arrays.deepEquals(next(new int[][] {{0, 1, 0}, {0, 1, 0}, {0, 1, 0}}), new int[][] {{0, 0, 0}, {1, 1, 1}, {0, 0, 0}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(next(new int[][] {{1, 1}, {1, 0}}), new int[][] {{1, 1}, {1, 1}})) throw new AssertionError("example 2");
        // The input board must stay unchanged.
        int[][] in = {{1, 1}, {1, 0}};
        next(in);
        if (!Arrays.deepEquals(in, new int[][] {{1, 1}, {1, 0}})) throw new AssertionError("input changed");
        // Random boards are checked against the window-sum oracle.
        Random rnd = new Random(21);
        for (int t = 0; t < 400; t++) {
            int m = 1 + rnd.nextInt(6), n = 1 + rnd.nextInt(6);
            int[][] b = new int[m][n];
            for (int[] row : b) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(2);
            if (!Arrays.deepEquals(next(b), oracle(b))) throw new AssertionError("random " + t);
        }
    }
}
```
