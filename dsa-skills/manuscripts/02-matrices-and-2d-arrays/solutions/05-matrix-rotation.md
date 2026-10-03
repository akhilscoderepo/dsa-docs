<!-- solutions-for: 05-matrix-rotation -->
### Matrix Rotation

#### Solution: [Build] Transpose Square (Author exercise)
<!-- id: mx-transpose-square -->

**Approach.** For each row `r`, swap `m[r][c]` with `m[c][r]` for every column `c` greater than `r`. That visits each pair of mirror cells exactly once and never touches the diagonal. If the inner loop started at zero, every pair would be swapped twice and the matrix would come back unchanged. The assertions compare with a copy-based transpose on random matrices and show that the visit-everything loop returns the original matrix.

**Complexity.** O(n^2) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class TransposeSquare {
    static void transpose(int[][] m) {
        int n = m.length;
        for (int r = 0; r < n; r++)
            for (int c = r + 1; c < n; c++) { int tmp = m[r][c]; m[r][c] = m[c][r]; m[c][r] = tmp; }
    }
    static void transposeAllCells(int[][] m) {
        int n = m.length;
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) { int tmp = m[r][c]; m[r][c] = m[c][r]; m[c][r] = tmp; }
    }

    public static void main(String[] args) {
        int[][] a = {{2, 7}, {9, 4}};
        transpose(a);
        if (!Arrays.deepEquals(a, new int[][] {{2, 9}, {7, 4}})) throw new AssertionError("example 1");
        int[][] b = {{1, 0, 0}, {0, 2, 0}, {0, 0, 3}};
        transpose(b);
        if (!Arrays.deepEquals(b, new int[][] {{1, 0, 0}, {0, 2, 0}, {0, 0, 3}})) throw new AssertionError("example 2");
        Random rnd = new Random(131);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] m = new int[n][n], copy = new int[n][n];
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) m[r][c] = rnd.nextInt(100);
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) copy[c][r] = m[r][c];
            int[][] original = new int[n][];
            for (int r = 0; r < n; r++) original[r] = m[r].clone();
            transpose(m);
            if (!Arrays.deepEquals(m, copy)) throw new AssertionError("disagrees with the copy-based transpose");
            int[][] twice = deepCopy(original);
            transposeAllCells(twice);
            if (!Arrays.deepEquals(twice, original)) throw new AssertionError("visiting every cell must undo itself");
        }
    }
    static int[][] deepCopy(int[][] m) {
        int[][] out = new int[m.length][];
        for (int r = 0; r < m.length; r++) out[r] = m[r].clone();
        return out;
    }
}
```

#### Solution: [Vary] Rotate Image (LeetCode 48)
<!-- id: mx-rotate-image -->

**Approach.** Transpose the matrix, then reverse every row. A cell at `(r, c)` goes to `(c, r)` and then to `(c, n - 1 - r)`, which is the clockwise destination. Only swaps are used, so no value is lost. The assertions compare with the copy-based rotation on random square matrices, and they also show why a rectangular matrix cannot be rotated in place: the rotated copy of a two-row, three-column matrix has three rows and two columns.

**Complexity.** O(n^2) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RotateImage {
    static void rotate(int[][] m) {
        int n = m.length;
        for (int r = 0; r < n; r++)
            for (int c = r + 1; c < n; c++) { int tmp = m[r][c]; m[r][c] = m[c][r]; m[c][r] = tmp; }
        for (int r = 0; r < n; r++)
            for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) { int tmp = m[r][lo]; m[r][lo] = m[r][hi]; m[r][hi] = tmp; }
    }
    static int[][] rotateCopy(int[][] m) {
        int rows = m.length, cols = m[0].length;
        int[][] out = new int[cols][rows];
        for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) out[c][rows - 1 - r] = m[r][c];
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2}, {3, 4}};
        rotate(a);
        if (!Arrays.deepEquals(a, new int[][] {{3, 1}, {4, 2}})) throw new AssertionError("example 1");
        int[][] b = {{5, 1, 9}, {2, 4, 8}, {10, 3, 6}};
        rotate(b);
        if (!Arrays.deepEquals(b, new int[][] {{10, 2, 5}, {3, 4, 1}, {6, 8, 9}})) throw new AssertionError("example 2");
        Random rnd = new Random(132);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] m = new int[n][n];
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) m[r][c] = rnd.nextInt(2001) - 1000;
            int[][] expected = rotateCopy(m);
            rotate(m);
            if (!Arrays.deepEquals(m, expected)) throw new AssertionError("disagrees with the copy-based rotation");
        }
        int[][] wide = {{1, 2, 3}, {4, 5, 6}};
        int[][] turned = rotateCopy(wide);
        if (turned.length != 3 || turned[0].length != 2) throw new AssertionError("a rotated 2x3 matrix has 3 rows and 2 columns, so no in-place rotation exists");
    }
}
```

#### Solution: [Boundary] Odd Center (Author exercise)
<!-- id: mx-odd-center -->

**Approach.** The transpose only swaps pairs with the column greater than the row, so it skips every diagonal cell, and the center of an odd matrix lies on the diagonal. The row reversal swaps positions `lo` and `hi` while `lo < hi`, so for an odd length the middle position is never part of a swap. For `n = 3`, the transpose makes three swaps and the reversal makes one swap in each of three rows, three in total. For `n = 1` there is nothing to swap. The assertions count the swaps in both sweeps and check the center value before and after.

**Complexity.** O(n^2) time and O(1) extra space.

```java run
import java.util.Arrays;

public final class OddCenter {
    static int transposeSwaps, reverseSwaps;

    static void rotate(int[][] m) {
        int n = m.length;
        transposeSwaps = 0; reverseSwaps = 0;
        for (int r = 0; r < n; r++)
            for (int c = r + 1; c < n; c++) { int tmp = m[r][c]; m[r][c] = m[c][r]; m[c][r] = tmp; transposeSwaps++; }
        for (int r = 0; r < n; r++)
            for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) { int tmp = m[r][lo]; m[r][lo] = m[r][hi]; m[r][hi] = tmp; reverseSwaps++; }
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        rotate(a);
        if (!Arrays.deepEquals(a, new int[][] {{7, 4, 1}, {8, 5, 2}, {9, 6, 3}})) throw new AssertionError("example 1");
        if (a[1][1] != 5) throw new AssertionError("the center must stay in place");
        if (transposeSwaps != 3 || reverseSwaps != 3) throw new AssertionError("swap counts " + transposeSwaps + " and " + reverseSwaps);
        int[][] b = {{7}};
        rotate(b);
        if (!Arrays.deepEquals(b, new int[][] {{7}}) || transposeSwaps != 0 || reverseSwaps != 0) throw new AssertionError("example 2");
        for (int n = 1; n <= 9; n += 2) {
            int[][] m = new int[n][n];
            int center = 1000 + n;
            m[n / 2][n / 2] = center;
            rotate(m);
            if (m[n / 2][n / 2] != center) throw new AssertionError("center moved for n = " + n);
            if (transposeSwaps != n * (n - 1) / 2) throw new AssertionError("transpose swap count for n = " + n);
            if (reverseSwaps != n * (n / 2)) throw new AssertionError("reversal swap count for n = " + n);
        }
    }
}
```

#### Solution: [Recognize] Counterclockwise Rotation (Author exercise)
<!-- id: mx-counterclockwise -->

**Approach.** Transpose first, then reverse each column from top to bottom instead of reversing each row. A cell at `(r, c)` goes to `(c, r)` and then, with the row index flipped, to `(n - 1 - c, r)`, which is the counterclockwise destination. The changed step is the second sweep: columns replace rows. The assertions compare with a copy-based counterclockwise rotation and check that a clockwise turn followed by a counterclockwise turn restores the matrix.

**Complexity.** O(n^2) time and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class Counterclockwise {
    static void transpose(int[][] m) {
        int n = m.length;
        for (int r = 0; r < n; r++)
            for (int c = r + 1; c < n; c++) { int tmp = m[r][c]; m[r][c] = m[c][r]; m[c][r] = tmp; }
    }
    static void clockwise(int[][] m) {
        transpose(m);
        int n = m.length;
        for (int r = 0; r < n; r++)
            for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) { int tmp = m[r][lo]; m[r][lo] = m[r][hi]; m[r][hi] = tmp; }
    }
    static void counterclockwise(int[][] m) {
        transpose(m);
        int n = m.length;
        for (int c = 0; c < n; c++)
            for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) { int tmp = m[lo][c]; m[lo][c] = m[hi][c]; m[hi][c] = tmp; }
    }
    static int[][] copyCounterclockwise(int[][] m) {
        int n = m.length;
        int[][] out = new int[n][n];
        for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) out[n - 1 - c][r] = m[r][c];
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2}, {3, 4}};
        counterclockwise(a);
        if (!Arrays.deepEquals(a, new int[][] {{2, 4}, {1, 3}})) throw new AssertionError("example 1");
        int[][] b = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        counterclockwise(b);
        if (!Arrays.deepEquals(b, new int[][] {{3, 6, 9}, {2, 5, 8}, {1, 4, 7}})) throw new AssertionError("example 2");
        Random rnd = new Random(133);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] m = new int[n][n];
            for (int r = 0; r < n; r++) for (int c = 0; c < n; c++) m[r][c] = rnd.nextInt(100);
            int[][] expected = copyCounterclockwise(m);
            int[][] original = new int[n][];
            for (int r = 0; r < n; r++) original[r] = m[r].clone();
            counterclockwise(m);
            if (!Arrays.deepEquals(m, expected)) throw new AssertionError("disagrees with the copy-based rotation");
            clockwise(m);
            if (!Arrays.deepEquals(m, original)) throw new AssertionError("clockwise then counterclockwise must restore the matrix");
        }
    }
}
```
