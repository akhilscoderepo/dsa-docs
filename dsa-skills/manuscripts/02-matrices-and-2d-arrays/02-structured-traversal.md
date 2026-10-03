<!-- lesson-kind: standard -->
<!-- lesson-id: structured-traversal -->
## Structured Traversal

<!-- stage: context -->
### Stripes On A Woven Blanket

A weaver finishes a blanket made of small square patches laid out in rows and columns, and the pattern is meant to have diagonal stripes. Each stripe runs from the upper left toward the lower right, and every patch on one stripe should have the same colour. She wants to know whether the blanket came out right, and she also wants the total thread used in each column and along the outer edge, where the binding is sewn.

For the column totals she simply runs a finger down each column. For the stripes she is tempted to pick a patch and follow its stripe all the way to the edge, then pick the next patch and do the same. After a few rows she notices that she keeps re-walking stripes she has already followed, and the blanket is not a small one.

<!-- stage: naive -->
### Follow Each Stripe From Every Patch

Translated to code, the direct check starts at every cell and walks the diagonal below it to the edge, comparing each patch with the starting one.

```java
static boolean stripesByWalking(int[][] grid) {
    int rows = grid.length, cols = grid[0].length;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            int rr = r + 1, cc = c + 1;
            while (rr < rows && cc < cols) {
                if (grid[rr][cc] != grid[r][c]) return false;
                rr++; cc++;
            }
        }
    }
    return true;
}
```

It is correct and follows the definition literally. On `[[3, 5, 8], [9, 3, 5], [4, 9, 3]]` it confirms that every stripe is constant and returns true.

<!-- stage: bottleneck -->
### Every Stripe Is Walked Many Times

A stripe of length `k` is walked once from each of its `k` patches, with up to `k - 1` comparisons each, so the work on that stripe is about `k * k / 2`. Summed over the whole blanket, the time is O(rows * cols * min(rows, cols)). For a 1,000 by 1,000 grid that is on the order of five hundred million comparisons, and it grows by a factor of a thousand when the grid grows by a factor of ten in each direction.

The repeated work is plain. If patch A equals the patch below and to its right, and that one equals the next, then A equals the third without checking it directly. The comparison of A with distant patches adds nothing. Only the relation between neighbors along the stripe carries information, and each patch has exactly one such neighbor behind it.

<!-- stage: insight -->
### Describe The Region By Its Indices

Many matrix questions ask about cells that form a simple shape: a row, a column, a diagonal, or the outer edge. For each shape there is a small rule on the indices that picks out exactly those cells, and the traversal is written from the rule, not by testing every cell against it.

A full pass over every cell in the usual nested loops visits cells in **row-major order**: all of row 0, then all of row 1, and so on. A column total swaps the loop nesting, or keeps one running sum per column while moving through row-major order. A diagonal is the set of cells with the same difference `r - c`, so that difference is a **diagonal key**, and two cells share a stripe exactly when their keys match. The boundary is the cells of the first and last rows plus the first and last columns, a **perimeter ring** that can be visited directly in O(rows + cols) time without touching the interior.

<!-- names: row-major order, diagonal key, perimeter ring -->

The invariant is that the indices at any moment describe exactly the region still to be visited, so nothing in it is skipped and nothing outside it is read. For the stripe check, the key insight is that cell `(r, c)` has exactly one predecessor on its diagonal, the cell `(r - 1, c - 1)`, so comparing each cell with that predecessor proves the whole stripe constant, by chaining equalities. Cells in the first row or first column have no predecessor and need no comparison. One pass over the cells is enough.

The same habit protects the edge cases of the perimeter. In a matrix with one row or one column, the top row and bottom row are the same row, and the left and right columns are the same column, so adding all four sides counts cells twice. The traversal must be written so that every cell of the ring is counted once, whatever the shape.

<!-- stage: variables -->
### Row, Column And What They Describe

The row `r` and column `c` locate a cell, and in this lesson they also name a region. For column sums, `c` is the column being accumulated, so one running total per column lives in an array indexed by `c`. For the stripe check, the pair `(r - 1, c - 1)` is the only neighbor that needs reading, and only when both `r` and `c` are positive. For the perimeter, the pair of first and last indices `rows - 1` and `cols - 1` defines the ring, and a one-row or one-column matrix is the case where first equals last.

<!-- stage: trace -->
### Comparing Each Cell With Its Upper Left

Take the grid `[[3, 5, 8], [9, 3, 5], [4, 9, 3]]`. Row 0 and column 0 have no upper-left neighbor, so the check begins at row 1, column 1. That cell holds 3 and its upper left holds 3, so they match. Cell `(1, 2)` holds 5 and its upper left, `(0, 1)`, holds 5, a match. Cell `(2, 1)` holds 9 and its upper left, `(1, 0)`, holds 9, a match. Cell `(2, 2)` holds 3 and its upper left, `(1, 1)`, holds 3, a match.

Every comparison succeeded, so every stripe is constant. Four comparisons covered nine cells. The step that matters is the last one, because the cell `(2, 2)` was compared only with the cell `(1, 1)`, and no comparison with `(0, 0)` was needed, since the earlier match already tied them together.

A second picture helps with column totals. For `[[1, 2, 3], [4, 5, 6]]` a running total per column grows as the cells are read in row-major order. After row 0 the totals are 1, 2 and 3. Reading row 1 adds 4, 5 and 6 to the same three slots, giving 5, 7 and 9. The column index picks the slot, and no column is ever scanned separately.

```trace
{"cells":[3,5,8,9,3,5,4,9,3],"pointers":["cell"],"steps":[{"at":{"cell":4},"vars":{"r":1,"c":1,"value":3,"upperLeft":3},"note":"Cell (1, 1) holds 3. Its upper left, (0, 0), holds 3. They match, so this link of the stripe holds."},{"at":{"cell":5},"vars":{"r":1,"c":2,"value":5,"upperLeft":5},"note":"Cell (1, 2) holds 5. Its upper left, (0, 1), holds 5. They match, so this link of the stripe holds."},{"at":{"cell":7},"vars":{"r":2,"c":1,"value":9,"upperLeft":9},"note":"Cell (2, 1) holds 9. Its upper left, (1, 0), holds 9. They match, so this link of the stripe holds."},{"at":{"cell":8},"vars":{"r":2,"c":2,"value":3,"upperLeft":3},"note":"Cell (2, 2) holds 3. Its upper left, (1, 1), holds 3. They match, so this link of the stripe holds."}]}
```

```trace
{"cells":[1,2,3,4,5,6],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"r":0,"c":0,"sums":"[1,0,0]"},"note":"Read 1 and add it to slot 0. The column totals are now [1, 0, 0]."},{"at":{"cell":1},"vars":{"r":0,"c":1,"sums":"[1,2,0]"},"note":"Read 2 and add it to slot 1. The column totals are now [1, 2, 0]."},{"at":{"cell":2},"vars":{"r":0,"c":2,"sums":"[1,2,3]"},"note":"Read 3 and add it to slot 2. The column totals are now [1, 2, 3]."},{"at":{"cell":3},"vars":{"r":1,"c":0,"sums":"[5,2,3]"},"note":"Read 4 and add it to slot 0. The column totals are now [5, 2, 3]."},{"at":{"cell":4},"vars":{"r":1,"c":1,"sums":"[5,7,3]"},"note":"Read 5 and add it to slot 1. The column totals are now [5, 7, 3]."},{"at":{"cell":5},"vars":{"r":1,"c":2,"sums":"[5,7,9]"},"note":"Read 6 and add it to slot 2. The column totals are now [5, 7, 9]."}]}
```

<!-- stage: code -->
### Region Rules As Loops

```java
static int[] columnSums(int[][] grid) {                // contract: rectangular, at least one row
    int[] sums = new int[grid[0].length];
    for (int[] row : grid)
        for (int c = 0; c < row.length; c++) sums[c] += row[c];
    return sums;
}

static boolean isToeplitz(int[][] grid) {
    for (int r = 1; r < grid.length; r++)
        for (int c = 1; c < grid[r].length; c++)
            if (grid[r][c] != grid[r - 1][c - 1]) return false;
    return true;
}

static long perimeterSum(int[][] grid) {               // contract: rectangular, at least one row and column
    int rows = grid.length, cols = grid[0].length;
    long total = 0;
    for (int c = 0; c < cols; c++) total += grid[0][c];
    if (rows > 1) for (int c = 0; c < cols; c++) total += grid[rows - 1][c];
    for (int r = 1; r < rows - 1; r++) {
        total += grid[r][0];
        if (cols > 1) total += grid[r][cols - 1];
    }
    return total;
}
```

The column sums and the stripe check read every cell once, so their time is O(rows * cols), and the perimeter reads only the ring in O(rows + cols) time. All use constant extra space except the column sums, which allocate one array of length `cols`. The guards `rows > 1` and `cols > 1` keep a single row or a single column from being counted twice.

<!-- stage: applicability -->
### When The Cells Form A Shape

Use region rules when the requested cells are rows, columns, diagonals or the outer ring, and an index formula picks them out exactly. The invariant is that the loop bounds describe exactly the unvisited region, so no cell is skipped or counted twice. Prefer a single pass with a predecessor comparison or a per-column running total over repeated rescans of the same line.

The false friend is neighbor-based exploration. If the question is which cells are connected to this one through touching neighbors, the shape is not a row, column or diagonal, and the answer needs a graph traversal with a visited record, which a later chapter owns. A shape described by indices alone is different from a region discovered cell by cell. Another false friend is the diagonal that goes the other way, where cells share the sum `r + c` and not the difference, so the predecessor is `(r - 1, c + 1)`.

Java's `int[][]` is a row of separate arrays, so going down a column touches a different array at each step. That is correct, and it can be slower than going along a row for large grids, which is a reason to keep the row loop on the outside when the answer allows it. Also keep the guard for a single row or column in any perimeter code, and use a `long` total if the cell values can be large.

<!-- stage: exercises -->
### Exercises

#### [Build] Column Sums (Author exercise)
<!-- id: mx-column-sums -->

**Prerequisites.** The shape contract from the previous lesson; nested loops.

**Problem.** Given a rectangular matrix with at least one row, return an array whose entry `c` is the sum of column `c`.

**Constraints.** 1 <= rows <= 200, 1 <= cols <= 200 and -1000 <= cell <= 1000. The matrix is rectangular by contract.

**Example 1.** Input `grid = [[1, 2, 3], [4, 5, 6]]`, output `[5, 7, 9]`.

**Example 2.** Input `grid = [[8], [2], [5]]`, output `[15]`, since there is one column.

**Hint.** What array holds one running total per column? Which index chooses the slot as you read each cell?

**Changed decision.** First rung: the column index chooses a slot, so no column is scanned separately.

#### [Vary] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-diagonal-sum-formulas -->

**Prerequisites.** The column-sums exercise above; the diagonal exercise from the shape lesson.

**Problem.** Given a square matrix, return the sum of the cells on both diagonals, counting a cell that lies on both only once. This time write the loop as a visit to the two coordinate formulas in each row.

**Constraints.** 1 <= n <= 100 and 1 <= cell <= 100. The matrix is `n` by `n`.

**Example 1.** Input `mat = [[1, 1], [2, 3]]`, output 7.

**Example 2.** Input `mat = [[5, 1, 2, 1], [1, 1, 1, 1], [7, 1, 6, 1], [1, 2, 1, 9]]`, output 25.

**Hint.** In row `i`, which two columns are on a diagonal? When do they name the same cell, and what should the loop do then?

**Changed decision.** The center is handled inside the loop by comparing the two columns, so no separate odd-size correction is needed.

#### [Boundary] Perimeter Sum (Author exercise)
<!-- id: mx-perimeter-sum -->

**Prerequisites.** The two exercises above.

**Problem.** Return the sum of the cells on the outer ring of a rectangular matrix, visiting only the ring. A matrix with a single row or a single column is entirely ring, and no cell may be counted twice.

**Constraints.** 1 <= rows <= 200, 1 <= cols <= 200 and -1000 <= cell <= 1000. The matrix is rectangular by contract.

**Example 1.** Input `grid = [[7, 8, 9]]`, output 24, since the whole single row is the ring.

**Example 2.** Input `grid = [[1, 1, 1], [1, 9, 1], [1, 1, 1]]`, output 8, with the center excluded.

**Hint.** What are the top and bottom rows when there is only one row? What are the left and right columns when there is only one column?

**Changed decision.** The first and last indices can coincide, which is the shape that turns four sides into double counting.

#### [Recognize] Toeplitz Matrix (LeetCode 766)
<!-- id: mx-toeplitz -->

**Prerequisites.** All three exercises above.

**Problem.** A matrix is Toeplitz if every diagonal running from the upper left to the lower right has all its entries equal. Given a matrix, return whether it is Toeplitz.

**Constraints.** 1 <= rows, cols <= 20 and 0 <= cell <= 99. Do not rescan whole diagonals.

**Example 1.** Input `matrix = [[3, 5, 8], [9, 3, 5], [4, 9, 3]]`, output true.

**Example 2.** Input `matrix = [[1, 2], [2, 2]]`, output false, since the main diagonal holds 1 and then 2.

**Hint.** How many neighbors does a cell have on its own diagonal behind it? What does chaining equalities along a stripe tell you?

**Changed decision.** Each cell is compared with its upper-left predecessor only, so each diagonal is checked by its links.
