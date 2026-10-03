<!-- lesson-kind: standard -->
<!-- lesson-id: two-dimensional-difference -->
## Two-Dimensional Difference

<!-- stage: context -->
### A Tiler And Her Glaze Coats

A tiler is finishing a wall made of square tiles in rows and columns, and her work order is a long list of glaze coats. Each coat covers a rectangle of tiles, from one tile to another, and adds one layer of glaze, or in some orders a given thickness, to every tile inside it. Coats overlap freely, and a tile in a busy place may receive dozens of them. The order is complete before she starts, and the only thing she needs at the end is a chart showing how much glaze every tile has received.

Painting each coat tile by tile is slow when the rectangles are big. She wonders whether she could mark only the edges of each coat on a sheet, and do one sweep over the whole wall at the end to turn the marks into amounts.

<!-- stage: naive -->
### Coat Every Tile Of Every Rectangle

The direct approach is to apply each coat by visiting each tile in its rectangle.

```java
static long[][] finalGlaze(int rows, int cols, int[][] coats) {
    long[][] glaze = new long[rows][cols];
    for (int[] coat : coats) {
        for (int r = coat[0]; r <= coat[2]; r++) {
            for (int c = coat[1]; c <= coat[3]; c++) {
                glaze[r][c] += coat[4];
            }
        }
    }
    return glaze;
}
```

All four limits of a coat are included, and the chart is exact for any list of coats inside the wall.

<!-- stage: bottleneck -->
### Large Rectangles Are Painted Again And Again

A coat covering h rows and w columns costs O(h w), so q coats on a wall of R rows and C columns cost O(q R C) at worst. For a thousand by a thousand wall and a hundred thousand coats that is a hundred trillion tile visits, and most of them repeat the same flat change across a big interior where nothing differs between neighboring tiles.

In one dimension, a range update needs two notes, at its start and just after its end. In two dimensions, the edges of a rectangle are lines, but only their corners decide where the amount changes in a sweep that reads left to right and top to bottom. A coat therefore needs four notes, one per corner, and q coats cost O(q) to record. A single sweep over the wall in O(R C) turns all the notes into the final chart, so the whole job costs O(q + R C).

<!-- stage: insight -->
### Four Corner Notes, Then One Sweep

Make a sheet one row and one column larger than the wall, the **border slots**, so that notes just beyond the last row or column have somewhere to go. For a coat with amount `v` over rows `r1` to `r2` and columns `c1` to `c2`, write four **corner deltas**: add `v` at `(r1, c1)`, where the coat starts, subtract `v` at `(r1, c2 + 1)`, where the coat ends along the columns, subtract `v` at `(r2 + 1, c1)`, where it ends along the rows, and add `v` at `(r2 + 1, c2 + 1)`, where the two subtractions overlap and must be repaired.

The sweep is the same two-dimensional prefix as in the last lesson, applied to the sheet of deltas. The **two-dimensional running sum** at a position is the sum of all deltas in the rectangle from the top-left corner to that position. For a tile inside a coat, the start delta is in that rectangle and the three others are not, so the tile gets `v`. For a tile to the right of the coat, the start delta and the column-end delta both lie in its rectangle and cancel to zero. Below the coat, the row-end delta cancels it. Beyond both, all four corners are included and sum to zero, which is why the fourth note exists.

<!-- names: border slots, corner deltas, two-dimensional running sum -->

The invariant is that the sheet always holds only deltas and never totals, and that every coat adds exactly four numbers whose sum is zero. The totals appear only after the sweep. This is the batching counterpart of the previous lesson: that table prepared a fixed grid for many reads, and this sheet collects many writes before a single read of the whole grid.

<!-- stage: variables -->
### The Sheet Of Deltas And The Sweep

`diff` has `rows + 1` rows and `cols + 1` columns, all zero at first, and each coat touches four of its slots. During the sweep, `out[r][c]` is computed in reading order as `diff[r][c]` plus the total above, plus the total to the left, minus the total diagonally above-left, with entries outside the wall treated as zero. The border slots are never copied into the answer. Amounts are `long` when the sum of many large amounts can pass the range of `int`.

<!-- stage: trace -->
### Marking Corners, Then Sweeping

The first trace records one coat of 5 over rows 1 to 2 and columns 1 to 2 on a wall of four rows and four columns. The row of cells is the five by five sheet written row by row, and each step writes one corner. Notice the last step: the corner at row 3 and column 3 is the slot beyond both ends, and it gets plus 5 so that the two minus notes cancel for every tile below and to the right.

```trace
{"cells":["0","0","0","0","0","0","5","0","-5","0","0","0","0","0","0","0","-5","0","5","0","0","0","0","0","0"],"pointers":["w"],"steps":[{"at":{"w":6},"vars":{"row":1,"col":1,"delta":5},"note":"Write +5 at row 1, column 1, the start corner."},{"at":{"w":8},"vars":{"row":1,"col":3,"delta":-5},"note":"Write -5 at row 1, column 3, the end along the columns."},{"at":{"w":16},"vars":{"row":3,"col":1,"delta":-5},"note":"Write -5 at row 3, column 1, the end along the rows."},{"at":{"w":18},"vars":{"row":3,"col":3,"delta":5},"note":"Write +5 at row 3, column 3, the overlap repair."}]}
```

The second trace sweeps the sheet to produce the chart of the four by four wall, one tile per step, in reading order. Take the eighth step: the tile at row 1 and column 3 sits just past the right edge of the coat, its delta is minus 5, and the formula gives 0, which shows the coat ending.

```trace
{"cells":["0","0","0","0","0","0","5","0","-5","0","0","0","0","0","0","0","-5","0","5","0","0","0","0","0","0"],"pointers":["w"],"steps":[{"at":{"w":0},"vars":{"delta":0,"above":0,"left":0,"diagonal":0,"total":0},"note":"Tile (0, 0): 0 + 0 above + 0 left - 0 diagonal = 0."},{"at":{"w":1},"vars":{"delta":0,"above":0,"left":0,"diagonal":0,"total":0},"note":"Tile (0, 1): 0 + 0 above + 0 left - 0 diagonal = 0."},{"at":{"w":2},"vars":{"delta":0,"above":0,"left":0,"diagonal":0,"total":0},"note":"Tile (0, 2): 0 + 0 above + 0 left - 0 diagonal = 0."},{"at":{"w":3},"vars":{"delta":0,"above":0,"left":0,"diagonal":0,"total":0},"note":"Tile (0, 3): 0 + 0 above + 0 left - 0 diagonal = 0."},{"at":{"w":5},"vars":{"delta":0,"above":0,"left":0,"diagonal":0,"total":0},"note":"Tile (1, 0): 0 + 0 above + 0 left - 0 diagonal = 0."},{"at":{"w":6},"vars":{"delta":5,"above":0,"left":0,"diagonal":0,"total":5},"note":"Tile (1, 1): 5 + 0 above + 0 left - 0 diagonal = 5."},{"at":{"w":7},"vars":{"delta":0,"above":0,"left":5,"diagonal":0,"total":5},"note":"Tile (1, 2): 0 + 0 above + 5 left - 0 diagonal = 5."},{"at":{"w":8},"vars":{"delta":-5,"above":0,"left":5,"diagonal":0,"total":0},"note":"Tile (1, 3): -5 + 0 above + 5 left - 0 diagonal = 0."},{"at":{"w":10},"vars":{"delta":0,"above":0,"left":0,"diagonal":0,"total":0},"note":"Tile (2, 0): 0 + 0 above + 0 left - 0 diagonal = 0."},{"at":{"w":11},"vars":{"delta":0,"above":5,"left":0,"diagonal":0,"total":5},"note":"Tile (2, 1): 0 + 5 above + 0 left - 0 diagonal = 5."},{"at":{"w":12},"vars":{"delta":0,"above":5,"left":5,"diagonal":5,"total":5},"note":"Tile (2, 2): 0 + 5 above + 5 left - 5 diagonal = 5."},{"at":{"w":13},"vars":{"delta":0,"above":0,"left":5,"diagonal":5,"total":0},"note":"Tile (2, 3): 0 + 0 above + 5 left - 5 diagonal = 0."},{"at":{"w":15},"vars":{"delta":0,"above":0,"left":0,"diagonal":0,"total":0},"note":"Tile (3, 0): 0 + 0 above + 0 left - 0 diagonal = 0."},{"at":{"w":16},"vars":{"delta":-5,"above":5,"left":0,"diagonal":0,"total":0},"note":"Tile (3, 1): -5 + 5 above + 0 left - 0 diagonal = 0."},{"at":{"w":17},"vars":{"delta":0,"above":5,"left":0,"diagonal":5,"total":0},"note":"Tile (3, 2): 0 + 5 above + 0 left - 5 diagonal = 0."},{"at":{"w":18},"vars":{"delta":5,"above":0,"left":0,"diagonal":5,"total":0},"note":"Tile (3, 3): 5 + 0 above + 0 left - 5 diagonal = 0."}]}
```

<!-- stage: code -->
### Four Writes Per Coat, One Sweep

```java
static long[][] applyRectangles(int rows, int cols, int[][] coats) {
    long[][] diff = new long[rows + 1][cols + 1];
    for (int[] c : coats) {
        long v = c[4];
        diff[c[0]][c[1]] += v;
        diff[c[0]][c[3] + 1] -= v;
        diff[c[2] + 1][c[1]] -= v;
        diff[c[2] + 1][c[3] + 1] += v;
    }
    long[][] out = new long[rows][cols];
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            long above = r > 0 ? out[r - 1][c] : 0;
            long left = c > 0 ? out[r][c - 1] : 0;
            long diag = r > 0 && c > 0 ? out[r - 1][c - 1] : 0;
            out[r][c] = diff[r][c] + above + left - diag;
        }
    }
    return out;
}

static int[][] rangeAddQueries(int n, int[][] queries) {
    long[][] chart = applyRectangles(n, n, withUnitAmount(queries));
    int[][] mat = new int[n][n];
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) mat[r][c] = (int) chart[r][c];
    return mat;
}

static int[][] withUnitAmount(int[][] queries) {
    int[][] coats = new int[queries.length][5];
    for (int i = 0; i < queries.length; i++) {
        System.arraycopy(queries[i], 0, coats[i], 0, 4);
        coats[i][4] = 1;
    }
    return coats;
}
```

Recording a coat is O(1) and the sweep is O(R C), so the total is O(q + R C) time with an extra sheet of (R + 1)(C + 1) slots. The sweep guards the reads above and to the left, so the first row and column need no special sheet.

<!-- stage: applicability -->
### When Rectangles Pile Up Before A Read

Use a two-dimensional difference sheet when many rectangular updates are known before the final grid is needed, and the grid is read once after all of them. The invariant is that each update adds four deltas with sum zero, and the totals are the two-dimensional running sum of the deltas.

A false friend is the prefix table of the previous lesson, which answers rectangle queries over fixed values and cannot take updates. Another false friend is the one-dimensional difference array applied row by row, which costs one pair of notes per row and is slower than four corner notes for tall rectangles. A third is a missing border: the notes at `r2 + 1` and `c2 + 1` fall outside the wall when a rectangle touches the last row or column.

In Java, allocate `rows + 1` by `cols + 1` slots, or guard each write with a bounds test, and say which. Use `long` for the sheet when amounts can be large, and keep the sweep formula with the guarded reads above and left. Check the order of the corner arguments: the four limits are `r1`, `c1`, `r2`, `c2`, and swapping a row limit with a column limit silently puts the notes in the wrong places.

<!-- stage: exercises -->
### Exercises

#### [Build] One Rectangle Add (Author exercise)
<!-- id: ps-one-rectangle-add -->

**Prerequisites.** The difference arrays lesson and the two-dimensional prefix lesson.

**Problem.** Given the size of a grid, one rectangle with both corners included, and an amount, return the grid that starts as zeros and has the amount added to every cell inside the rectangle. Use four corner notes in a sheet and one sweep.

**Constraints.** 1 <= rows, cols <= 500, 0 <= r1 <= r2 < rows, 0 <= c1 <= c2 < cols, and -1000000000 <= amount <= 1000000000.

**Example 1.** Input `rows = 3, cols = 4`, rectangle `(1, 1, 2, 2)` and amount 5, output `[[0, 0, 0, 0], [0, 5, 5, 0], [0, 5, 5, 0]]`.

**Example 2.** Input `rows = 2, cols = 2`, rectangle `(0, 0, 1, 1)` and amount 3, output `[[3, 3], [3, 3]]`.

**Hint.** Which four corners change the sweep's running total? What does each of the four notes cancel?

**Changed decision.** First rung: the two notes of a one-dimensional range become four corner notes, and the sweep becomes a two-dimensional running sum.

#### [Vary] Increment Submatrices by One (LeetCode 2536)
<!-- id: ps-increment-submatrices -->

**Prerequisites.** The One Rectangle Add exercise above.

**Problem.** Start with an `n` by `n` matrix of zeros. Each query `[r1, c1, r2, c2]` adds one to every cell in the rectangle with those corners, all included. Return the matrix after all queries have been applied.

**Constraints.** 1 <= n <= 500, 1 <= queries.length <= 10000, and 0 <= r1 <= r2 < n and 0 <= c1 <= c2 < n.

**Example 1.** Input `n = 3, queries = [[1, 1, 2, 2], [0, 0, 1, 1]]`, output `[[1, 1, 0], [1, 2, 1], [0, 1, 1]]`.

**Example 2.** Input `n = 2, queries = [[0, 0, 1, 1]]`, output `[[1, 1], [1, 1]]`.

**Hint.** What is the amount of each query? Can all the notes be recorded before the single sweep?

**Changed decision.** Many rectangles share one sheet, and all of them are recorded before the grid is read once.

#### [Boundary] Bottom-Right Edge (Author exercise)
<!-- id: ps-bottom-right-edge -->

**Prerequisites.** The two exercises above.

**Problem.** Handle rectangles that touch the last row, the last column, or both. Show that a sheet of the same size as the grid throws when a note is written at `r2 + 1` or `c2 + 1`, and that a sheet with a border row and column, or explicit guards, fixes it.

**Constraints.** 1 <= rows, cols <= 500 and every rectangle satisfies the usual limits, including rectangles that end at `rows - 1` or `cols - 1`.

**Example 1.** Input `rows = 2, cols = 3`, rectangle `(1, 1, 1, 2)` and amount 4, output `[[0, 0, 0], [0, 4, 4]]`.

**Example 2.** Input `rows = 1, cols = 1`, rectangle `(0, 0, 0, 0)` and amount 6, output `[[6]]`.

**Hint.** Which two of the four notes land outside the grid when the rectangle touches the bottom-right corner? Are those slots ever read?

**Changed decision.** Notes may fall one past the last row or column, so the sheet gets a border or each write is guarded.

#### [Recognize] Weighted Rectangle Updates (Author exercise)
<!-- id: ps-weighted-rectangle-updates -->

**Prerequisites.** All three exercises above.

**Problem.** Generalize from increments of one to signed amounts. Each update is a rectangle and a `long` weight that may be negative. Return the final grid, and use `long` throughout so that a cell receiving many large weights does not overflow.

**Constraints.** 1 <= rows, cols <= 300, up to 100000 updates, and -1000000000 <= weight <= 1000000000.

**Example 1.** Input `rows = 3, cols = 3` with two updates of 2000000000 over `(0, 0, 1, 1)`, output a grid whose cells in the top-left two by two block are 4000000000 and all other cells 0.

**Example 2.** Input `rows = 3, cols = 3`, an update of 5 over the whole grid and an update of -7 over `(1, 1, 1, 1)`, output a grid of fives with -2 in the center.

**Hint.** What type do the notes and the sweep need? Does a negative weight change the four-corner pattern?

**Changed decision.** The amount is a signed `long`, so the sheet and the sweep are `long`, and the pattern is unchanged.
