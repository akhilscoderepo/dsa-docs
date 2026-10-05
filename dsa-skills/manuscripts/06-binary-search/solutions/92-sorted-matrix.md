<!-- solutions-for: 06-binary-search -->
### Solutions For Searching A Sorted Matrix

#### Solution: [Build] Search A 2D Matrix (LeetCode 74)
<!-- id: bs-matrix-contains -->

**Approach.**
Reading the matrix row after row gives one ascending sequence of `m * n` values, because each row starts above the end of the previous row. The virtual index `k` names the cell in row `k / n` and column `k % n`, and no copy is made. The search is the exact search of the first lesson on `[0, m * n - 1]`, with the cell read at `mid` replacing an array read. An equal value returns true, a smaller value moves `lo` past `mid`, and a larger value moves `hi` below `mid`. The invariant keeps the target, if present, inside `[lo, hi]`, so an empty range proves absence.

**Complexity.**
- **Time** is O(log(m * n)), because each comparison halves the range of virtual indexes.
- **Space** is O(1), because the search keeps three integers and never copies the matrix.

```java run
import java.util.Random;

public final class MatrixContains {
    /**
     * Returns true when target occurs in a matrix that is ascending in row-major order.
     * Time: O(log(m * n)). Space: O(1).
     * Invariant: if target occurs, its virtual index lies in [lo, hi].
     */
    static boolean contains(int[][] matrix, int target) {
        int cols = matrix[0].length;
        int lo = 0, hi = matrix.length * cols - 1;
        // The loop runs while at least one virtual index remains.
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            // The division gives the row and the remainder gives the column of the virtual index.
            int value = matrix[mid / cols][mid % cols];
            if (value == target) return true;
            // A smaller value rules out mid and everything before it.
            if (value < target) lo = mid + 1;
            // A larger value rules out mid and everything after it.
            else hi = mid - 1;
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[][] m = {{2, 4, 6, 8}, {11, 13, 15, 17}, {20, 22, 24, 26}};
        if (!contains(m, 22)) throw new AssertionError("example 1");
        if (contains(m, 12)) throw new AssertionError("example 2");
        // Every present value is found, and every gap between values is rejected.
        for (int target = 0; target <= 28; target++) {
            boolean expect = false;
            for (int[] row : m) for (int v : row) if (v == target) expect = true;
            if (contains(m, target) != expect) throw new AssertionError("target " + target);
        }
        // Random row-major ascending matrices against a scan.
        Random rnd = new Random(111);
        for (int t = 0; t < 3000; t++) {
            int r = 1 + rnd.nextInt(5), c = 1 + rnd.nextInt(5), v = 0;
            int[][] a = new int[r][c];
            for (int i = 0; i < r; i++) for (int j = 0; j < c; j++) a[i][j] = v += 1 + rnd.nextInt(3);
            int target = rnd.nextInt(v + 3);
            boolean expect = false;
            for (int[] row : a) for (int x : row) if (x == target) expect = true;
            if (contains(a, target) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] First Matrix Position (Author exercise)
<!-- id: bs-matrix-first-position -->

**Approach.**
The method treats the matrix as a non-decreasing sequence of `m * n` values and searches for the first virtual index whose value is at least `target`. The half-open interval `[lo, hi)` starts at `[0, m * n)`. A value below `target` moves `lo` past `mid`, and any other value moves `hi` to `mid`, so an equal value is kept as a candidate and the search continues to the left. When the loop ends, `lo` is the first index with a value at least `target`. The method returns the coordinates only when that cell exists and equals `target`. The conversion to row `lo / n` and column `lo % n` happens once, at the end.

**Complexity.**
- **Time** is O(log(m * n)), because each comparison halves the interval.
- **Space** is O(1), because the result is one array of two integers and the search keeps two indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MatrixFirstPosition {
    /**
     * Returns [row, col] of the first occurrence of target in row-major order, or [-1, -1].
     * Time: O(log(m * n)). Space: O(1).
     * Invariant: every virtual index below lo holds a value below target.
     */
    static int[] firstPosition(int[][] matrix, int target) {
        int cols = matrix[0].length;
        int lo = 0, hi = matrix.length * cols;
        // The interval [lo, hi) holds the candidates for the first value at least target.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A value below target cannot be the first one at least target.
            if (matrix[mid / cols][mid % cols] < target) lo = mid + 1;
            // Any other value may be the first, so hi keeps it as the end of the interval.
            else hi = mid;
        }
        // lo can equal the number of cells, and then no value is at least target.
        if (lo == matrix.length * cols || matrix[lo / cols][lo % cols] != target) return new int[]{-1, -1};
        return new int[]{lo / cols, lo % cols};
    }

    public static void main(String[] args) {
        // The statement examples.
        int[][] m = {{1, 2, 2}, {2, 2, 3}, {3, 3, 9}};
        if (!Arrays.equals(firstPosition(m, 2), new int[]{0, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(firstPosition(m, 4), new int[]{-1, -1})) throw new AssertionError("example 2");
        // A target above every value reaches the end index without reading past the matrix.
        if (!Arrays.equals(firstPosition(m, 100), new int[]{-1, -1})) throw new AssertionError("large");
        // Random matrices with duplicates against a scan in row-major order.
        Random rnd = new Random(112);
        for (int t = 0; t < 3000; t++) {
            int r = 1 + rnd.nextInt(5), c = 1 + rnd.nextInt(5), v = 0;
            int[][] a = new int[r][c];
            for (int i = 0; i < r; i++) for (int j = 0; j < c; j++) a[i][j] = v += rnd.nextInt(3);
            int target = rnd.nextInt(v + 3);
            int[] expect = {-1, -1};
            for (int i = r - 1; i >= 0; i--) for (int j = c - 1; j >= 0; j--) if (a[i][j] == target) expect = new int[]{i, j};
            if (!Arrays.equals(firstPosition(a, target), expect)) throw new AssertionError("random " + Arrays.deepToString(a) + " " + target);
        }
    }
}
```

#### Solution: [Boundary] Empty Shape (Author exercise)
<!-- id: bs-matrix-empty-shape -->

**Approach.**
A matrix with zero rows has no `matrix[0]`, so the expression that reads `cols` would throw an `ArrayIndexOutOfBoundsException`. A matrix with rows of zero columns has `cols == 0`, and then the last virtual index `rows * cols - 1` is -1, so the search range would read cell `matrix[0][0]` in the first iteration if the guard were missing. The method therefore returns `false` before reading `cols` whenever there are no rows or no columns. Otherwise it runs the virtual index search. The invariant of the search is unchanged, and the guard handles the only cases in which the range `[0, rows * cols - 1]` does not name a real cell.

**Complexity.**
- **Time** is O(1) for an empty shape and O(log(m * n)) otherwise.
- **Space** is O(1), because the method stores no extra structure.

```java run
import java.util.Random;

public final class MatrixEmptyShape {
    /**
     * Returns true when target occurs, and false for every empty shape.
     * Time: O(log(m * n)). Space: O(1).
     * Invariant: if target occurs, its virtual index lies in [lo, hi].
     */
    static boolean contains(int[][] matrix, int target) {
        // The guard runs first, because matrix[0] does not exist when there are no rows.
        if (matrix.length == 0 || matrix[0].length == 0) return false;
        int cols = matrix[0].length;
        int lo = 0, hi = matrix.length * cols - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int value = matrix[mid / cols][mid % cols];
            if (value == target) return true;
            if (value < target) lo = mid + 1; else hi = mid - 1;
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples: no rows, and one row with no columns.
        if (contains(new int[0][], 5)) throw new AssertionError("example 1");
        if (contains(new int[][]{{}}, 5)) throw new AssertionError("example 2");
        // Several rows with no columns, and a one-cell matrix on both sides of the target.
        if (contains(new int[][]{{}, {}}, 0)) throw new AssertionError("empty rows");
        if (!contains(new int[][]{{7}}, 7) || contains(new int[][]{{7}}, 6)) throw new AssertionError("single cell");
        // The unguarded read fails with the exception that the guard prevents.
        boolean threw = false;
        try { int[][] none = new int[0][]; int cols = none[0].length; } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("matrix[0] should not exist");
        // Random shapes including empty ones against a scan.
        Random rnd = new Random(113);
        for (int t = 0; t < 3000; t++) {
            int r = rnd.nextInt(5), c = rnd.nextInt(5), v = 0;
            int[][] a = new int[r][c];
            for (int i = 0; i < r; i++) for (int j = 0; j < c; j++) a[i][j] = v += 1 + rnd.nextInt(3);
            int target = rnd.nextInt(v + 3);
            boolean expect = false;
            for (int[] row : a) for (int x : row) if (x == target) expect = true;
            if (contains(a, target) != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] Search A 2D Matrix II (LeetCode 240)
<!-- id: bs-matrix-staircase -->

**Approach.**
The top-right cell is the largest value of its row and the smallest value of its column. If it is larger than the target, the whole column below it is larger too, so the walk moves one column left. If it is smaller, the whole row to its left is smaller too, so the walk moves one row down. An equal value returns true. Each step removes one row or one column from the region that may hold the target, so the walk ends within `m + n` steps. The invariant is that the target, if present, lies at or below `row` and at or left of `col`. A virtual index search is wrong here, because the row-major sequence is not sorted.

**Complexity.**
- **Time** is O(m + n), because every step removes a row or a column.
- **Space** is O(1), because the walk keeps two coordinates.

```java run
import java.util.Random;

public final class MatrixStaircase {
    /**
     * Returns true when target occurs in a matrix with ascending rows and ascending columns.
     * Time: O(m + n). Space: O(1).
     * Invariant: if target occurs, it lies in rows row.. and columns ..col.
     */
    static boolean contains(int[][] matrix, int target) {
        int row = 0, col = matrix[0].length - 1;
        // The walk stays inside the matrix while a row and a column remain.
        while (row < matrix.length && col >= 0) {
            int value = matrix[row][col];
            if (value == target) return true;
            // A larger value rules out its whole column below it.
            if (value > target) col--;
            // A smaller value rules out the rest of its row to the left.
            else row++;
        }
        return false;
    }

    /** The virtual index search, which is only valid for row-major ascending matrices. */
    static boolean virtual(int[][] matrix, int target) {
        int cols = matrix[0].length, lo = 0, hi = matrix.length * cols - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2, v = matrix[mid / cols][mid % cols];
            if (v == target) return true;
            if (v < target) lo = mid + 1; else hi = mid - 1;
        }
        return false;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[][] m = {{1, 4, 7, 11}, {2, 5, 8, 12}, {3, 6, 9, 16}, {10, 13, 14, 17}};
        if (!contains(m, 13)) throw new AssertionError("example 1");
        if (contains(m, 15)) throw new AssertionError("example 2");
        // The virtual index search misses a present value in this matrix, so it is not a valid substitute.
        boolean missed = false;
        for (int[] row : m) for (int v : row) if (!virtual(m, v)) missed = true;
        if (!missed) throw new AssertionError("the virtual search should miss a value here");
        // Random matrices with sorted rows and columns against a scan.
        Random rnd = new Random(114);
        for (int t = 0; t < 3000; t++) {
            int r = 1 + rnd.nextInt(6), c = 1 + rnd.nextInt(6);
            int[][] a = new int[r][c];
            // Each cell is at least its upper and left neighbors, so rows and columns ascend.
            for (int i = 0; i < r; i++) for (int j = 0; j < c; j++) {
                int up = i > 0 ? a[i - 1][j] : 0, left = j > 0 ? a[i][j - 1] : 0;
                a[i][j] = Math.max(up, left) + rnd.nextInt(3);
            }
            int target = rnd.nextInt(a[r - 1][c - 1] + 3);
            boolean expect = false;
            for (int[] row : a) for (int x : row) if (x == target) expect = true;
            if (contains(a, target) != expect) throw new AssertionError("random");
        }
    }
}
```
