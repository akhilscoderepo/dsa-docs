<!-- solutions-for: 06-matrix-search -->
### Matrix Search

#### Solution: [Build] Search a 2D Matrix (LeetCode 74)
<!-- id: bs-search-matrix-rows -->

**Approach.** The first values of the rows are increasing, so the target can be only in the last row whose first value is at most the target. A search over the rows finds the first row whose first value is greater than the target, which is the upper bound over the first column, and the candidate row is the one before it. If that position is before the first row, the target is smaller than everything and the answer is false. A second exact search then runs inside the row. The program also runs the virtual-index version and checks that the two agree with a scan on random matrices that satisfy the promise.

**Complexity.** O(log R + log C) time and O(1) extra space.

```java run
import java.util.Random;

public final class SearchMatrixRows {
    static boolean byRows(int[][] a, int target) {
        if (a.length == 0 || a[0].length == 0) return false;
        int lo = 0, hi = a.length;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid][0] <= target) lo = mid + 1;
            else hi = mid;
        }
        if (lo == 0) return false;
        int[] row = a[lo - 1];
        int left = 0, right = row.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (row[mid] == target) return true;
            if (row[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return false;
    }
    static boolean byIndex(int[][] a, int target) {
        if (a.length == 0 || a[0].length == 0) return false;
        int cols = a[0].length;
        int lo = 0, hi = a.length * cols - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int v = a[mid / cols][mid % cols];
            if (v == target) return true;
            if (v < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
    static boolean scan(int[][] a, int target) {
        for (int[] r : a) for (int v : r) if (v == target) return true;
        return false;
    }

    public static void main(String[] args) {
        int[][] ex = {{1, 3, 5, 7}, {10, 11, 16, 20}, {23, 30, 34, 60}};
        if (!byRows(ex, 3)) throw new AssertionError("example 1");
        if (byRows(ex, 13)) throw new AssertionError("example 2");
        if (byRows(ex, 0)) throw new AssertionError("smaller than everything");
        if (!byRows(ex, 60)) throw new AssertionError("last cell");
        Random rnd = new Random(711);
        for (int t = 0; t < 3000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] a = new int[rows][cols];
            int cur = rnd.nextInt(3);
            for (int i = 0; i < rows; i++)
                for (int j = 0; j < cols; j++) { a[i][j] = cur; cur += 1 + rnd.nextInt(3); }
            int q = rnd.nextInt(cur + 3) - 1;
            boolean want = scan(a, q);
            if (byRows(a, q) != want) throw new AssertionError("rows differ for q=" + q);
            if (byIndex(a, q) != want) throw new AssertionError("index differs for q=" + q);
        }
    }
}
```

#### Solution: [Vary] First Matrix Position (Author exercise)
<!-- id: bs-first-matrix-position -->

**Approach.** With cells non-decreasing in reading order, the cells that are at least the target form a suffix of the virtual line. The first-true pattern finds its start: `hi` begins at the number of cells, a cell that is at least the target sends `hi` to `mid`, and anything smaller sends `lo` to `mid + 1`. The start is the first candidate for the target, so the position must be checked: it must lie inside the line and hold exactly the target. Only then is it converted with `lo / cols` and `lo % cols`. The oracle scans the cells in reading order and returns the first match.

**Complexity.** O(log (R C)) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FirstMatrixPosition {
    static int[] firstPosition(int[][] a, int target) {
        if (a.length == 0 || a[0].length == 0) return new int[] {-1, -1};
        int cols = a[0].length;
        int lo = 0, hi = a.length * cols;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (a[mid / cols][mid % cols] >= target) hi = mid;
            else lo = mid + 1;
        }
        if (lo == a.length * cols || a[lo / cols][lo % cols] != target) return new int[] {-1, -1};
        return new int[] {lo / cols, lo % cols};
    }
    static int[] oracle(int[][] a, int target) {
        for (int i = 0; i < a.length; i++)
            for (int j = 0; j < a[i].length; j++) if (a[i][j] == target) return new int[] {i, j};
        return new int[] {-1, -1};
    }

    public static void main(String[] args) {
        int[][] ex = {{1, 2, 2}, {2, 3, 5}};
        if (!Arrays.equals(firstPosition(ex, 2), new int[] {0, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(firstPosition(ex, 4), new int[] {-1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(firstPosition(ex, 9), new int[] {-1, -1})) throw new AssertionError("larger than everything");
        Random rnd = new Random(712);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] a = new int[rows][cols];
            int cur = rnd.nextInt(3);
            for (int i = 0; i < rows; i++)
                for (int j = 0; j < cols; j++) { a[i][j] = cur; cur += rnd.nextInt(3); }
            int q = rnd.nextInt(cur + 3) - 1;
            if (!Arrays.equals(firstPosition(a, q), oracle(a, q))) throw new AssertionError("differs for q=" + q);
        }
    }
}
```

#### Solution: [Boundary] Empty Shape (Author exercise)
<!-- id: bs-empty-shape -->

**Approach.** Reading `a[0].length` fails when there are no rows, and dividing by `cols` fails when there are rows with no columns, so the guard checks `a.length == 0` first and then `a[0].length == 0`, and returns false before computing anything. For shapes that can reach ten billion cells, the count of cells is `(long) rows * cols`, the positions are `long`, and the row and column come from `position / cols` and `position % cols` converted back to `int` only after the division, when both fit. The program shows that an unguarded search throws on an empty matrix, checks all the guarded shapes, and checks the arithmetic of a large shape against exact values and against the wrapped `int` product.

**Complexity.** O(log (R C)) time and O(1) extra space.

```java run
public final class EmptyShape {
    static boolean search(int[][] a, int target) {
        if (a.length == 0 || a[0].length == 0) return false;
        long cols = a[0].length;
        long lo = 0, hi = a.length * cols - 1;
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            int v = a[(int) (mid / cols)][(int) (mid % cols)];
            if (v == target) return true;
            if (v < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
    static boolean unguarded(int[][] a, int target) {
        int cols = a[0].length;
        int lo = 0, hi = a.length * cols - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int v = a[mid / cols][mid % cols];
            if (v == target) return true;
            if (v < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }

    public static void main(String[] args) {
        if (search(new int[0][], 5)) throw new AssertionError("example 1");
        if (search(new int[3][0], 5)) throw new AssertionError("example 2");
        boolean threw = false;
        try { unguarded(new int[0][], 5); } catch (ArrayIndexOutOfBoundsException e) { threw = true; }
        if (!threw) throw new AssertionError("the unguarded search should fail on no rows");
        int[][] one = {{4}};
        if (!search(one, 4) || search(one, 3) || search(one, 5)) throw new AssertionError("single cell");
        int[][] flat = {{1, 2, 3, 4, 5}};
        if (!search(flat, 5) || search(flat, 6)) throw new AssertionError("single row");
        int[][] column = {{1}, {3}, {5}};
        if (!search(column, 3) || search(column, 4)) throw new AssertionError("single column");

        long cols = 100000, rows = 100000;
        long last = rows * cols - 1;
        if (last / cols != 99999 || last % cols != 99999) throw new AssertionError("last cell of a large shape");
        long position = 99999L * cols + 5;
        if (position / cols != 99999 || position % cols != 5) throw new AssertionError("mapping with long");
        int wrapped = 100000 * 100000;
        if (wrapped == rows * cols) throw new AssertionError("the int product should have wrapped");
    }
}
```

#### Solution: [Recognize] Search a 2D Matrix II (LeetCode 240)
<!-- id: bs-search-matrix-two -->

**Approach.** Start at the top right corner. If the cell is larger than the target, every cell below it in the column is larger as well, so the column is discarded and the walk moves left. If the cell is smaller, every cell to its left in the row is smaller as well, so the row is discarded and the walk moves down. Each step discards a whole row or column, so at most R plus C steps are taken. The virtual index does not work here, because reading order is not increasing: the program shows a matrix and a target for which a binary search over the virtual line misses a value that the walk finds. It then checks the walk against a scan on random matrices with sorted rows and columns.

**Complexity.** O(R + C) time and O(1) extra space.

```java run
import java.util.Random;

public final class SearchMatrixTwo {
    static boolean staircase(int[][] a, int target) {
        if (a.length == 0 || a[0].length == 0) return false;
        int r = 0, c = a[0].length - 1;
        while (r < a.length && c >= 0) {
            int v = a[r][c];
            if (v == target) return true;
            if (v > target) c--;
            else r++;
        }
        return false;
    }
    static boolean virtualLine(int[][] a, int target) {
        int cols = a[0].length;
        int lo = 0, hi = a.length * cols - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            int v = a[mid / cols][mid % cols];
            if (v == target) return true;
            if (v < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return false;
    }
    static boolean scan(int[][] a, int target) {
        for (int[] r : a) for (int v : r) if (v == target) return true;
        return false;
    }

    public static void main(String[] args) {
        int[][] ex = {{1, 4, 7}, {2, 5, 8}, {3, 6, 9}};
        if (!staircase(ex, 6)) throw new AssertionError("example 1");
        if (staircase(ex, 10)) throw new AssertionError("example 2");
        if (virtualLine(ex, 2)) throw new AssertionError("the virtual line should miss 2 in this matrix");
        if (!staircase(ex, 2)) throw new AssertionError("the walk should find 2");
        Random rnd = new Random(713);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(5), cols = 1 + rnd.nextInt(5);
            int[][] a = new int[rows][cols];
            for (int i = 0; i < rows; i++)
                for (int j = 0; j < cols; j++) {
                    int up = i > 0 ? a[i - 1][j] : 0;
                    int left = j > 0 ? a[i][j - 1] : 0;
                    a[i][j] = Math.max(up, left) + rnd.nextInt(3);
                }
            int q = rnd.nextInt(a[rows - 1][cols - 1] + 3);
            if (staircase(a, q) != scan(a, q)) throw new AssertionError("differs for q=" + q);
        }
    }
}
```
