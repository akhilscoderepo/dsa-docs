<!-- lesson-kind: standard -->
<!-- lesson-id: two-dimensional-prefix -->
## Two-Dimensional Prefix

<!-- stage: context -->
### A Farmer's Yield Map

A farmer has a satellite map of a field cut into small square cells, and each cell has a number: the harvest from that square in kilograms, which can be negative where a drainage ditch cost her more than it gave. The map has hundreds of rows and columns. A buyer calls with a stream of offers, each naming a rectangular block of the field, from this row and column to that row and column, and the farmer must say how much the block produced.

The map never changes during the day, but the offers keep coming. Adding up a block by hand means visiting each of its cells, and big blocks have tens of thousands of them. The farmer would like to prepare something once, so that each offer can be answered by looking at a handful of numbers.

<!-- stage: naive -->
### Add Up Every Cell Of The Block

The direct approach is to answer each offer by visiting every cell inside the block and adding it up.

```java
static long blockYield(int[][] field, int r1, int c1, int r2, int c2) {
    long total = 0;
    for (int r = r1; r <= r2; r++) {
        for (int c = c1; c <= c2; c++) {
            total += field[r][c];
        }
    }
    return total;
}
```

All four limits are included, and the loop gives the exact total for any block inside the map.

<!-- stage: bottleneck -->
### Large Blocks Are Revisited Cell By Cell

An offer for a block of h rows and w columns costs O(h w), so q offers on a field with R rows and C columns cost O(q R C) at worst. With a thousand rows, a thousand columns and a hundred thousand offers, that is a hundred billion additions. The same cells are summed again and again, because neighboring offers cover almost the same area.

In one dimension, a block is the difference of two stored totals. The same idea applies to a rectangle: the yield of a block is a large rectangle that starts at the top-left corner of the map, with some strips cut away. If the yield of every corner-anchored rectangle is stored once, an offer becomes a few lookups and a few additions and subtractions, with no loop over cells, so O(1) per offer after one O(R C) pass to build the table.

<!-- stage: insight -->
### Cut Two Strips, Restore The Overlap

Store a table where each entry holds the total of the rectangle that starts at the top-left cell of the map and ends at that entry. To avoid special cases at the edges, give the table one extra row and one extra column of zeros at the top and left, the **sentinel border**. With it, entry `[r + 1][c + 1]` is the total of rows `0` to `r` and columns `0` to `c`. Building it needs one rule: the entry equals the cell itself plus the entry above it plus the entry to the left, minus the entry diagonally above-left, which would otherwise be counted twice.

To answer an offer for rows `r1` to `r2` and columns `c1` to `c2`, start with the big rectangle that ends at the bottom-right of the block. Remove the strip above the block, which is the rectangle ending at row `r1 - 1`, and remove the strip to its left, the rectangle ending at column `c1 - 1`. The corner where those two strips meet was removed twice, so it must be added back once. This is **inclusion-exclusion**: subtract two overlapping pieces and restore their common part. In table terms the answer is four **corner lookups**, `P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]`.

<!-- names: sentinel border, inclusion-exclusion, corner lookups -->

The invariant is that every table entry is the exact total of its corner-anchored rectangle, so any block is those four entries combined with signs plus, minus, minus, plus. The sentinel border guarantees that the indices `r1` and `c1` are valid even when the block starts at the first row or column, since entry zero holds zero. This is a different tool from the difference array of the previous lesson: the table here prepares many reads of a fixed grid, and it does not take updates.

<!-- stage: variables -->
### The Padded Table And Four Corners

`P` has `rows + 1` rows and `cols + 1` columns, and its first row and column stay zero. `P[r + 1][c + 1]` is filled in reading order, from the cell and three earlier entries. For a block, `r1`, `c1`, `r2` and `c2` are inclusive limits, and the four corners read are `P[r2+1][c2+1]`, `P[r1][c2+1]`, `P[r2+1][c1]` and `P[r1][c1]`. The entries are `long`, because the sum of a large grid of large numbers can pass the range of `int`.

<!-- stage: trace -->
### Filling The Table, Then Reading Four Corners

The first trace fills the padded table for the small field 1, 2, 3 over 4, 5, 6. The cells are the padded table of three rows and four columns, written row by row, and each step computes one entry. Study the fifth step, which writes the entry for the cell 5: it is 5 plus 3 above, plus 5 to the left, minus 1 on the diagonal, which gives 12, and the minus 1 corrects for the cell 1 being included in both neighbors.

```trace
{"cells":["0","0","0","0","0","1","3","6","0","5","12","21"],"pointers":["w"],"steps":[{"at":{"w":5},"vars":{"cell":1,"above":0,"left":0,"diagonal":0,"entry":1},"note":"The cell is 1. Entry = 1 + 0 above + 0 left - 0 diagonal = 1."},{"at":{"w":6},"vars":{"cell":2,"above":0,"left":1,"diagonal":0,"entry":3},"note":"The cell is 2. Entry = 2 + 0 above + 1 left - 0 diagonal = 3."},{"at":{"w":7},"vars":{"cell":3,"above":0,"left":3,"diagonal":0,"entry":6},"note":"The cell is 3. Entry = 3 + 0 above + 3 left - 0 diagonal = 6."},{"at":{"w":9},"vars":{"cell":4,"above":1,"left":0,"diagonal":0,"entry":5},"note":"The cell is 4. Entry = 4 + 1 above + 0 left - 0 diagonal = 5."},{"at":{"w":10},"vars":{"cell":5,"above":3,"left":5,"diagonal":1,"entry":12},"note":"The cell is 5. Entry = 5 + 3 above + 5 left - 1 diagonal = 12."},{"at":{"w":11},"vars":{"cell":6,"above":6,"left":12,"diagonal":3,"entry":21},"note":"The cell is 6. Entry = 6 + 6 above + 12 left - 3 diagonal = 21."}]}
```

The second trace answers an offer for the single row of the second line, columns 1 and 2, which holds 5 and 6. The four corners are read in turn. Look at the last step: the sum 21 - 6 - 5 + 1 equals 11, where the final plus 1 is the overlap that was subtracted twice.

```trace
{"cells":["0","0","0","0","0","1","3","6","0","5","12","21"],"pointers":["read"],"steps":[{"at":{"read":11},"vars":{"corner":"bottom-right","value":21,"runningTotal":21},"note":"Read the bottom-right entry, which holds 21, and add it. The running total is 21."},{"at":{"read":7},"vars":{"corner":"top","value":6,"runningTotal":15},"note":"Read the top entry, which holds 6, and subtract it. The running total is 15."},{"at":{"read":9},"vars":{"corner":"left","value":5,"runningTotal":10},"note":"Read the left entry, which holds 5, and subtract it. The running total is 10."},{"at":{"read":5},"vars":{"corner":"overlap","value":1,"runningTotal":11},"note":"Read the overlap entry, which holds 1, and add it. The running total is 11."}]}
```

<!-- stage: code -->
### A Padded Table And A Four-Term Formula

```java
static long[][] buildTable(int[][] m) {
    int rows = m.length, cols = m[0].length;
    long[][] p = new long[rows + 1][cols + 1];
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            p[r + 1][c + 1] = m[r][c] + p[r][c + 1] + p[r + 1][c] - p[r][c];
        }
    }
    return p;
}

static long region(long[][] p, int r1, int c1, int r2, int c2) {
    return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1];
}

static int[][] matrixBlockSum(int[][] m, int k) {
    int rows = m.length, cols = m[0].length;
    long[][] p = buildTable(m);
    int[][] out = new int[rows][cols];
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            int r1 = Math.max(0, r - k), c1 = Math.max(0, c - k);
            int r2 = Math.min(rows - 1, r + k), c2 = Math.min(cols - 1, c + k);
            out[r][c] = (int) region(p, r1, c1, r2, c2);
        }
    }
    return out;
}
```

The table is built in O(R C) time and space, and each offer costs four reads. The block-sum function clips the window to the grid before calling the formula, so no index leaves the table.

<!-- stage: applicability -->
### When Grid Blocks Are Asked Repeatedly

Use a two-dimensional prefix table when the grid does not change and many questions ask for the total of a rectangle. The invariant is that each entry equals the sum of its corner-anchored rectangle, and the formula for any block combines four of them with signs plus, minus, minus, plus.

A false friend is the habit of summing each row separately, which turns each offer into a loop over h rows and is still slower than four lookups. Another is the table of row-wise prefix sums only, which handles a block one row at a time. A third is applying the table to a grid that receives updates: after a change the entries below and to the right are stale, and a different structure is needed.

In Java, give the table the extra row and column and index it by `r + 1` and `c + 1`, so the first row and column of the grid never need a branch. Use `long` for the entries, and clip any window to the grid with `Math.max` and `Math.min` before computing the corners. Say in a comment whether limits are inclusive, since mixing inclusive and exclusive limits shifts every corner by one.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Sum Query 2D - Immutable (LeetCode 304)
<!-- id: ps-range-sum-2d -->

**Prerequisites.** The range queries lesson, and nested loops over matrices from Chapter 02.

**Problem.** Design a class that receives a matrix once and then answers many requests for the sum of the cells in the rectangle with top-left corner `(r1, c1)` and bottom-right corner `(r2, c2)`, all four limits included. Each request must take constant time.

**Constraints.** 1 <= rows, cols <= 200, -100000 <= matrix[i][j] <= 100000, and up to 10000 requests with 0 <= r1 <= r2 < rows and 0 <= c1 <= c2 < cols.

**Example 1.** Input `matrix = [[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1]]` and the request `(1, 1, 2, 2)`, output 11.

**Example 2.** Input the same matrix and the request `(0, 0, 2, 3)`, output 28.

**Hint.** What does each table entry store? Which four entries give the rectangle?

**Changed decision.** First rung: the one-dimensional table becomes a table with a padded border, and a request combines four entries.

#### [Vary] Matrix Block Sum (LeetCode 1314)
<!-- id: ps-matrix-block-sum -->

**Prerequisites.** The Range Sum Query 2D exercise above.

**Problem.** Given a matrix and a distance `k`, return a matrix of the same shape in which each cell holds the sum of all the cells within `k` rows and `k` columns of it, including itself, ignoring positions outside the matrix.

**Constraints.** 1 <= rows, cols <= 100, 0 <= k <= 100, and 1 <= matrix[i][j] <= 100.

**Example 1.** Input `mat = [[1, 0, 2], [3, 1, 0], [0, 4, 1]], k = 1`, output `[[5, 7, 3], [9, 12, 8], [8, 9, 6]]`.

**Example 2.** Input `mat = [[1, 2], [3, 4]], k = 5`, output `[[10, 10], [10, 10]]`.

**Hint.** What are the limits of the window around a cell near the border? Can the same table answer every window?

**Changed decision.** A query is made for every cell, and each window must be clipped to the grid before the corners are read.

#### [Boundary] Single Cell Rectangle (Author exercise)
<!-- id: ps-single-cell-rectangle -->

**Prerequisites.** The two exercises above.

**Problem.** Check that a rectangle covering exactly one cell returns that cell, for every cell including the four corners of the matrix and cells that hold negative numbers. Explain which two corner terms cancel to leave the cell.

**Constraints.** 1 <= rows, cols <= 100 and -1000000000 <= matrix[i][j] <= 1000000000, so the table needs `long`.

**Example 1.** Input `matrix = [[5, -2], [3, 4]]` and the request `(0, 1, 0, 1)`, output -2.

**Example 2.** Input the same matrix and the request `(1, 0, 1, 0)`, output 3.

**Hint.** If `r1 == r2` and `c1 == c2`, which entries are read? What is left of the four-term formula?

**Changed decision.** The smallest possible rectangle exercises the four corners at once, and the table's entries must hold exact totals of their rectangles.

#### [Recognize] Whole Matrix Query (Author exercise)
<!-- id: ps-whole-matrix-query -->

**Prerequisites.** All three exercises above.

**Problem.** Answer the request that covers the whole matrix, `(0, 0, rows - 1, cols - 1)`, and also a request covering a whole first row or whole first column. Explain why no index below zero is read, and which sentinel entries are used.

**Constraints.** 1 <= rows, cols <= 100 and -1000000000 <= matrix[i][j] <= 1000000000.

**Example 1.** Input `matrix = [[2, 3], [4, 5]]` and the request `(0, 0, 1, 1)`, output 14.

**Example 2.** Input a matrix with one cell `[[7]]` and the request `(0, 0, 0, 0)`, output 7.

**Hint.** Which entries are read when `r1` and `c1` are zero? What do they contain?

**Changed decision.** The request touches the first row and column of the grid, so the zero border supplies the entries that would otherwise be negative indices.
