<!-- solutions-for: 04-neighbor-enumeration -->
### Neighbor Enumeration

#### Solution: [Build] Orthogonal Count (Author exercise)
<!-- id: mx-orthogonal-count -->

**Approach.** Keep the four offsets for up, down, left and right in a constant table. For each offset form the candidate and count it only if its row is in range and its column is in range. The same loop gives 4 for a middle cell, 3 for an edge cell and 2 for a corner, with no case analysis. The assertions compare with a formula that counts the legal sides directly from the position, over every cell of many board shapes.

**Complexity.** O(1) time and O(1) space.

```java run
public final class OrthogonalCount {
    static final int[] DR4 = {-1, 1, 0, 0};
    static final int[] DC4 = {0, 0, -1, 1};

    static int orthogonalCount(int rows, int cols, int r, int c) {
        int count = 0;
        for (int k = 0; k < 4; k++) {
            int nr = r + DR4[k], nc = c + DC4[k];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) count++;
        }
        return count;
    }
    static int oracle(int rows, int cols, int r, int c) {
        return (r > 0 ? 1 : 0) + (r < rows - 1 ? 1 : 0) + (c > 0 ? 1 : 0) + (c < cols - 1 ? 1 : 0);
    }

    public static void main(String[] args) {
        if (orthogonalCount(3, 4, 1, 2) != 4) throw new AssertionError("example 1");
        if (orthogonalCount(1, 5, 0, 2) != 2) throw new AssertionError("example 2");
        for (int rows = 1; rows <= 7; rows++)
            for (int cols = 1; cols <= 7; cols++)
                for (int r = 0; r < rows; r++)
                    for (int c = 0; c < cols; c++)
                        if (orthogonalCount(rows, cols, r, c) != oracle(rows, cols, r, c)) throw new AssertionError("cell " + r + "," + c + " in " + rows + "x" + cols);
    }
}
```

#### Solution: [Vary] Eight Neighbors (Author exercise)
<!-- id: mx-eight-neighbors -->

**Approach.** Extend the table to eight pairs and keep the pair `(0, 0)` out of it, so a cell is never its own neighbor. The guard is unchanged. A middle cell has 8 neighbors, an edge cell 5, and a corner cell 3, except on thin boards where fewer exist. The assertions count the legal cells in the surrounding three-by-three window minus the cell itself, and compare over every cell of many board shapes. A check on the table confirms that it holds eight distinct pairs and no zero pair.

**Complexity.** O(1) time and O(1) space.

```java run
import java.util.HashSet;
import java.util.Set;

public final class EightNeighbors {
    static final int[] DR8 = {-1, -1, -1, 0, 0, 1, 1, 1};
    static final int[] DC8 = {-1, 0, 1, -1, 1, -1, 0, 1};

    static int eightCount(int rows, int cols, int r, int c) {
        int count = 0;
        for (int k = 0; k < 8; k++) {
            int nr = r + DR8[k], nc = c + DC8[k];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) count++;
        }
        return count;
    }
    static int oracle(int rows, int cols, int r, int c) {
        int inside = 0;
        for (int rr = r - 1; rr <= r + 1; rr++)
            for (int cc = c - 1; cc <= c + 1; cc++)
                if (rr >= 0 && rr < rows && cc >= 0 && cc < cols) inside++;
        return inside - 1;
    }

    public static void main(String[] args) {
        if (eightCount(3, 3, 1, 1) != 8) throw new AssertionError("example 1");
        if (eightCount(3, 4, 0, 1) != 5) throw new AssertionError("example 2");
        Set<String> pairs = new HashSet<>();
        for (int k = 0; k < 8; k++) {
            if (DR8[k] == 0 && DC8[k] == 0) throw new AssertionError("the table must not contain the zero pair");
            pairs.add(DR8[k] + "," + DC8[k]);
        }
        if (pairs.size() != 8) throw new AssertionError("the eight offsets must be distinct");
        for (int rows = 1; rows <= 7; rows++)
            for (int cols = 1; cols <= 7; cols++)
                for (int r = 0; r < rows; r++)
                    for (int c = 0; c < cols; c++)
                        if (eightCount(rows, cols, r, c) != oracle(rows, cols, r, c)) throw new AssertionError("cell " + r + "," + c + " in " + rows + "x" + cols);
    }
}
```

#### Solution: [Boundary] Corner Cell (Author exercise)
<!-- id: mx-corner-cell -->

**Approach.** For the corner `(0, 0)`, five of the eight candidates have a negative row or a negative column and are rejected by the guard, leaving right, down and down-right in table order. The guard must run before the read, because the read of a negative index would throw. The assertions record every coordinate that is read from the board, check that none is negative and all are inside the board, and compare the list with the expected arrays for a three-by-three board and a one-by-one board.

**Complexity.** O(1) time and O(1) extra space apart from the output list.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class CornerCell {
    static final int[] DR8 = {-1, -1, -1, 0, 0, 1, 1, 1};
    static final int[] DC8 = {-1, 0, 1, -1, 1, -1, 0, 1};

    static List<int[]> neighbors(int rows, int cols, int r, int c, List<int[]> reads) {
        List<int[]> out = new ArrayList<>();
        for (int k = 0; k < 8; k++) {
            int nr = r + DR8[k], nc = c + DC8[k];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
                reads.add(new int[] {nr, nc});               // the only place the board would be read
                out.add(new int[] {nr, nc});
            }
        }
        return out;
    }

    public static void main(String[] args) {
        List<int[]> reads = new ArrayList<>();
        List<int[]> got = neighbors(3, 3, 0, 0, reads);
        if (!Arrays.deepEquals(got.toArray(new int[0][]), new int[][] {{0, 1}, {1, 0}, {1, 1}})) throw new AssertionError("example 1");
        for (int[] p : reads) if (p[0] < 0 || p[1] < 0 || p[0] >= 3 || p[1] >= 3) throw new AssertionError("a read left the board");
        if (!neighbors(1, 1, 0, 0, new ArrayList<>()).isEmpty()) throw new AssertionError("example 2");
        int rejected = 0;
        for (int k = 0; k < 8; k++) if (DR8[k] < 0 || DC8[k] < 0) rejected++;
        if (rejected != 5) throw new AssertionError("five of the eight candidates of a corner lie off the board");
        boolean threw = false;
        int[][] board = new int[3][3];
        try { int x = board[0 + DR8[0]][0 + DC8[0]]; } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("an unguarded read of the first candidate must fail");
    }
}
```

#### Solution: [Recognize] Neighbor Counts For Game Of Life (LeetCode 289)
<!-- id: mx-neighbor-counts -->

**Approach.** For every cell, run the eight-offset loop with the bounds guard and add the board value of each legal neighbor. The counts go into a new matrix, so every read sees the unchanged board. The cost per cell is a constant eight candidates. The oracle is the quadratic scan from the lesson, which tests adjacency for every pair of cells, and the assertions also check that the input board is not modified.

**Complexity.** O(rows * cols) time and O(rows * cols) extra space for the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NeighborCounts {
    static final int[] DR8 = {-1, -1, -1, 0, 0, 1, 1, 1};
    static final int[] DC8 = {-1, 0, 1, -1, 1, -1, 0, 1};

    static int[][] neighborCounts(int[][] board) {
        int rows = board.length, cols = board[0].length;
        int[][] counts = new int[rows][cols];
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                int live = 0;
                for (int k = 0; k < 8; k++) {
                    int nr = r + DR8[k], nc = c + DC8[k];
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) live += board[nr][nc];
                }
                counts[r][c] = live;
            }
        return counts;
    }
    static int[][] oracle(int[][] b) {
        int rows = b.length, cols = b[0].length;
        int[][] out = new int[rows][cols];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++)
            for (int r2 = 0; r2 < rows; r2++) for (int c2 = 0; c2 < cols; c2++)
                if ((r2 != r || c2 != c) && Math.abs(r2 - r) <= 1 && Math.abs(c2 - c) <= 1) out[r][c] += b[r2][c2];
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 0, 1}, {0, 1, 0}, {1, 1, 0}};
        int[][] snapshot = {{1, 0, 1}, {0, 1, 0}, {1, 1, 0}};
        if (!Arrays.deepEquals(neighborCounts(a), new int[][] {{1, 3, 1}, {4, 4, 3}, {2, 2, 2}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(a, snapshot)) throw new AssertionError("the board must not change");
        if (!Arrays.deepEquals(neighborCounts(new int[][] {{1}}), new int[][] {{0}})) throw new AssertionError("example 2");
        Random rnd = new Random(124);
        for (int t = 0; t < 2000; t++) {
            int rows = 1 + rnd.nextInt(6), cols = 1 + rnd.nextInt(6);
            int[][] b = new int[rows][cols];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) b[r][c] = rnd.nextInt(2);
            if (!Arrays.deepEquals(neighborCounts(b), oracle(b))) throw new AssertionError("disagrees with the pair scan");
        }
    }
}
```
