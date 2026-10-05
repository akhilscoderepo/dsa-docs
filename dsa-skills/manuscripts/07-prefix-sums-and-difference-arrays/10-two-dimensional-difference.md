<!-- lesson-kind: standard -->
<!-- lesson-id: two-dimensional-difference -->
## Add To Rectangles In Constant Time

<!-- stage: context -->
### Counting How Many Zones Cover Each Cell

A delivery company divides a city into a grid of 500 by 500 cells. Each delivery zone is a rectangle of cells, and the company has 10,000 zones that overlap in many places. The planners need to know, for every cell, how many zones cover it. A zone that spans the whole city touches 250,000 cells, and 10,000 such zones take billions of steps.

Nobody reads the counts until all zones are entered. The program writes a rectangle for each zone and reads every cell once. The lesson on range updates solved the same task on a line. This lesson asks how a rectangle update can cost a fixed number of writes.

<!-- stage: naive -->
### Looping Over Every Cell Of Each Rectangle

The direct method loops over the rows and columns of each rectangle and adds the value to every cell. An update is `{r1, c1, r2, c2, value}`, and the corners `(r1, c1)` and `(r2, c2)` both belong to the rectangle.

```java
static long[][] applyAll(int m, int n, int[][] updates) {
    long[][] grid = new long[m][n];
    for (int[] u : updates) {
        for (int r = u[0]; r <= u[2]; r++) {
            for (int c = u[1]; c <= u[3]; c++) grid[r][c] += u[4];
        }
    }
    return grid;
}
```

For a 3 by 4 grid and the update `{1, 1, 1, 2, 5}`, the method sets the two cells of row 1 in columns 1 and 2 to 5 and leaves the rest at 0.

```predict
The grid has 500 rows and 500 columns, and 10,000 updates each cover the whole grid. How many additions does `applyAll` perform?

It performs 10,000 times 250,000 additions, which is 2,500,000,000. An update costs the area of its rectangle, so the cost is O(m * n) per update and O(m * n * u) for u updates.
```

<!-- stage: bottleneck -->
### Each Update Pays For Its Area

An update costs as many additions as its rectangle has cells, and `u` updates cost O(m * n * u) in the worst case. The program writes the same value into every cell of a rectangle, and the program reads the grid only once at the end.

On a line, the earlier lesson recorded the start and the stop of a range and spread the value in one pass. A rectangle has a start in two directions, and it also has a stop in two directions. The question is which few writes record a rectangle, so that one pass over the grid can spread them into the right cells.

<!-- stage: insight -->
### Write Four Signed Values At The Corners

A **difference matrix** `D` has `m + 1` rows and `n + 1` columns. The value of a cell is the sum of every entry of `D` that lies above it and to its left, including the entry at the cell itself. This is the two-dimensional version of the running sum from the lesson on ranges.

#### Four Corner Deltas For One Rectangle

A **corner delta** is a signed value written at one corner position of the rectangle. To add `v` to the rectangle from `(r1, c1)` to `(r2, c2)`, the program writes four entries. The write `D[r1][c1] += v` starts the value for every cell at the lower right of the top-left corner. The write `D[r1][c2 + 1] -= v` cancels that value in the columns right of the rectangle, in every row from `r1` downward. The write `D[r2 + 1][c1] -= v` cancels it in the rows below the rectangle, in every column from `c1` rightward. The cells below and right of the rectangle lost the value twice, so the write `D[r2 + 1][c2 + 1] += v` restores it once.

Only the cells inside the rectangle keep the net `+v`. An update costs four writes, which is O(1).

#### One Pass For All Cells

The final pass computes a **two-dimensional running sum** of `D`. Each cell equals the entry above it, plus the entry to its left, minus the entry above and to the left, plus the cell's own entry of `D`. This is the formula of the prefix matrix, applied to `D`. The pass costs O(m * n), so `u` updates and one read cost O(m * n + u).

<!-- names: difference matrix, corner delta, two-dimensional running sum -->

#### The Extra Row And Column

The updates write to the row `r2 + 1` and the column `c2 + 1`. For a rectangle that reaches the last row or the last column, these indexes equal `m` or `n`. The matrix has one extra row and one extra column, so those writes land inside the array. The extra entries are never read as cells.

<!-- stage: variables -->
### Five Names And Their Roles

The method keeps five names.

- **D** is the `long` matrix with `m + 1` rows and `n + 1` columns that holds the corner deltas.
- **r1**, **c1**, **r2** and **c2** are the corners of an update, and both corners belong to the rectangle.
- **value** is the amount that the update adds to each cell of the rectangle.
- **grid** is the final matrix with `m` rows and `n` columns.
- **cur** is the running sum at the current cell during the final pass.

The updates change only `D`. The final pass reads `D` and writes `grid`, and it never reads the extra row or the extra column.

<!-- stage: trace -->
### From Corner Deltas To Cell Values

#### Two Overlapping Rectangles

The grid has 3 rows and 3 columns, and the updates are `{0, 0, 1, 1, +1}` and `{1, 1, 2, 2, +1}`. The matrix `D` has 4 rows and 4 columns, and the sixteen cells below list it row by row, so the entry `D[r][c]` sits at position `4 * r + c`. The pass visits the nine grid cells in order. The cell `(1, 1)` is covered twice and gets 2.

```trace
{"cells":[1,0,-1,0,0,1,0,-1,-1,0,1,0,0,-1,0,1],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{},"note":"The corner deltas are written. The pass visits the cells of the grid in row order."},{"at":{"i":0},"vars":{"cell":"(0,0)","D":"1","up":"0","left":"0","diag":"0","value":"1"},"note":"Value = 1 + 0 + 0 - 0 = 1 for the cell (0,0)."},{"at":{"i":1},"vars":{"cell":"(0,1)","D":"0","up":"0","left":"1","diag":"0","value":"1"},"note":"Value = 0 + 0 + 1 - 0 = 1 for the cell (0,1)."},{"at":{"i":2},"vars":{"cell":"(0,2)","D":"-1","up":"0","left":"1","diag":"0","value":"0"},"note":"Value = -1 + 0 + 1 - 0 = 0 for the cell (0,2)."},{"at":{"i":4},"vars":{"cell":"(1,0)","D":"0","up":"1","left":"0","diag":"0","value":"1"},"note":"Value = 0 + 1 + 0 - 0 = 1 for the cell (1,0)."},{"at":{"i":5},"vars":{"cell":"(1,1)","D":"1","up":"1","left":"1","diag":"1","value":"2"},"note":"Value = 1 + 1 + 1 - 1 = 2 for the cell (1,1)."},{"at":{"i":6},"vars":{"cell":"(1,2)","D":"0","up":"0","left":"2","diag":"1","value":"1"},"note":"Value = 0 + 0 + 2 - 1 = 1 for the cell (1,2)."},{"at":{"i":8},"vars":{"cell":"(2,0)","D":"-1","up":"1","left":"0","diag":"0","value":"0"},"note":"Value = -1 + 1 + 0 - 0 = 0 for the cell (2,0)."},{"at":{"i":9},"vars":{"cell":"(2,1)","D":"0","up":"2","left":"0","diag":"1","value":"1"},"note":"Value = 0 + 2 + 0 - 1 = 1 for the cell (2,1)."},{"at":{"i":10},"vars":{"cell":"(2,2)","D":"1","up":"1","left":"1","diag":"2","value":"1"},"note":"Value = 1 + 1 + 1 - 2 = 1 for the cell (2,2)."}]}
```

#### A Rectangle That Reaches The Edge

The grid has 2 rows and 2 columns, and the update is `{0, 0, 1, 1, +3}`. The rectangle covers the whole grid, so its cancelling writes land in row 2 and column 2, the extra row and column. The nine cells below list `D` row by row with three entries per row. The pass visits the four grid cells and each gets 3.

```trace
{"cells":[3,0,-3,0,0,0,-3,0,3],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{},"note":"The corner deltas are written. The pass visits the cells of the grid in row order."},{"at":{"i":0},"vars":{"cell":"(0,0)","D":"3","up":"0","left":"0","diag":"0","value":"3"},"note":"Value = 3 + 0 + 0 - 0 = 3 for the cell (0,0)."},{"at":{"i":1},"vars":{"cell":"(0,1)","D":"0","up":"0","left":"3","diag":"0","value":"3"},"note":"Value = 0 + 0 + 3 - 0 = 3 for the cell (0,1)."},{"at":{"i":3},"vars":{"cell":"(1,0)","D":"0","up":"3","left":"0","diag":"0","value":"3"},"note":"Value = 0 + 3 + 0 - 0 = 3 for the cell (1,0)."},{"at":{"i":4},"vars":{"cell":"(1,1)","D":"0","up":"3","left":"3","diag":"3","value":"3"},"note":"Value = 0 + 3 + 3 - 3 = 3 for the cell (1,1)."}]}
```

<!-- stage: code -->
### Updates And Final Pass In Java

```java
static long[][] applyAll(int m, int n, int[][] updates) {
    long[][] d = new long[m + 1][n + 1];
    for (int[] u : updates) {
        d[u[0]][u[1]] += u[4];
        d[u[0]][u[3] + 1] -= u[4];
        d[u[2] + 1][u[1]] -= u[4];
        d[u[2] + 1][u[3] + 1] += u[4];
    }
    long[][] grid = new long[m][n];
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) {
            long up = r > 0 ? grid[r - 1][c] : 0;
            long left = c > 0 ? grid[r][c - 1] : 0;
            long diag = r > 0 && c > 0 ? grid[r - 1][c - 1] : 0;
            grid[r][c] = d[r][c] + up + left - diag;
        }
    }
    return grid;
}
```

The final pass guards the three neighbours at the top and left borders, because `grid` has no extra row. The matrix `d` has the extra row and column, so the four writes need no guard. All writes use `+=` and `-=`, since different updates can write to one entry.

<!-- stage: applicability -->
### When Corner Deltas Replace Loops

#### The Invariant

The invariant is that the value of cell `(r, c)` equals the sum of all entries `D[i][j]` with `i <= r` and `j <= c`. A rectangle that contains `(r, c)` contributes `+v` from its top-left corner, and its three other corners lie outside the sum. A rectangle that does not contain the cell contributes `+v - v - v + v`, which is 0, or only part of that pattern that also sums to 0.

#### The False Friend

The two-dimensional prefix table of the previous lesson is the false friend. It reads fixed values and answers rectangle sums. It cannot absorb a write, because one changed cell alters every entry to its lower right. The difference matrix is the reverse. It absorbs many rectangle writes in constant time each, and it gives the cell values only after the final pass.

#### Conditions That Break The Fit

All updates must arrive before the first read. Reading the grid between two updates costs a full pass. The updates must add the same value to every cell of an axis-parallel rectangle. A change that depends on the cell, such as a gradient, does not fit. The method also fails on a range assignment, because assignments do not combine by addition.

<!-- stage: exercises -->
### Exercises

#### [Build] One Rectangle Add (Author exercise)
<!-- id: ps-one-rectangle -->

**Prerequisites.** The four corner deltas and the final pass of this lesson.

**Problem.** Given the grid shape `m` by `n`, the corners `(r1, c1)` and `(r2, c2)` of an interior rectangle, and an integer `value`, return the matrix that holds `value` inside the rectangle and 0 elsewhere. Use four writes to a difference matrix.

**Constraints.** The limits are:
- **Shape** is `3 <= m, n <= 200`.
- **Interior** rectangle satisfies `1 <= r1 <= r2 <= m - 2` and `1 <= c1 <= c2 <= n - 2`.
- **Value** is an `int` with `|value| <= 10^9`.
- **Return type** is `long[][]` of shape `m` by `n`.

**Example 1.** Input `m = 3`, `n = 4`, corners `(1,1)` and `(1,2)`, and `value = 5`, output `[[0,0,0,0],[0,5,5,0],[0,0,0,0]]`.

**Example 2.** Input `m = 4`, `n = 4`, corners `(1,1)` and `(2,2)`, and `value = -1`, output `[[0,0,0,0],[0,-1,-1,0],[0,-1,-1,0],[0,0,0,0]]`.

**Hint.** Which of the four entries start a value and which cancel it? Check that all four lie inside a matrix with one extra row and column.

**Changed decision.** Basic case: one rectangle costs four writes, and one pass turns them into cell values.

#### [Vary] Increment Submatrices By One (LeetCode 2536)
<!-- id: ps-increment-2536 -->

**Prerequisites.** The first exercise above.

**Problem.** Given an integer `n` and a list of queries `[r1, c1, r2, c2]`, start with an `n` by `n` matrix of zeros. For each query, add 1 to every cell `(r, c)` with `r1 <= r <= r2` and `c1 <= c <= c2`. Return the matrix after all queries.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 500`.
- **Queries** number at most `10^4`, with `0 <= r1 <= r2 < n` and `0 <= c1 <= c2 < n`.
- **Overlap** between queries is allowed.
- **Return type** is `int[][]`, because every cell is at most 10^4.

**Example 1.** Input `n = 3` and `queries = [[0,1,1,2],[1,0,2,1]]`, output `[[0,1,1],[1,2,1],[1,1,0]]`.

**Example 2.** Input `n = 1` and `queries = [[0,0,0,0]]`, output `[[1]]`.

**Hint.** Collect all queries in one difference matrix before the pass. Which two entries of the matrix cancel the effect to the right and below?

**Changed decision.** Many rectangles overlap, so all updates are batched and a single pass resolves them together.

#### [Boundary] Bottom-Right Edge (Author exercise)
<!-- id: ps-bottom-right-edge -->

**Prerequisites.** The first exercise above and the second trace of this lesson.

**Problem.** Given the grid shape `m` by `n` and a list of updates `[r1, c1, r2, c2]` that each add 1, return the matrix after all updates. Some updates end at row `m - 1`, at column `n - 1`, or at both. The difference matrix must reserve space for their cancelling writes, and the code may not skip them with a guard.

**Constraints.** The limits are:
- **Shape** satisfies `1 <= m, n <= 500`, and `m` need not equal `n`.
- **Updates** number at most `10^4`, with `0 <= r1 <= r2 <= m - 1` and `0 <= c1 <= c2 <= n - 1`.
- **Edge** updates with `r2 = m - 1` or `c2 = n - 1` are valid.
- **Return type** is `int[][]`.

**Example 1.** Input `m = 2`, `n = 3` and updates `[[0,1,1,2]]`, output `[[0,1,1],[0,1,1]]`.

**Example 2.** Input `m = 1`, `n = 1` and updates `[[0,0,0,0],[0,0,0,0]]`, output `[[2]]`.

**Hint.** For `r2 = m - 1`, the cancelling row is `m`. How many rows and columns must the difference matrix have for all four writes to exist?

**Changed decision.** The rectangle can touch the last row and the last column, so the difference matrix needs the extra row and column that the cells never use.

#### [Recognize] Weighted Rectangle Updates (Author exercise)
<!-- id: ps-weighted-rectangles -->

**Prerequisites.** All exercises above.

**Problem.** Given the grid shape `m` by `n` and a list of updates `[r1, c1, r2, c2, weight]`, start with a matrix of zeros and add `weight` to every cell of each rectangle. Weights may be negative. Return the matrix after all updates.

**Constraints.** The limits are:
- **Shape** satisfies `1 <= m, n <= 500`.
- **Updates** number at most `10^4`, with `0 <= r1 <= r2 <= m - 1` and `0 <= c1 <= c2 <= n - 1`.
- **Weight** is a `long` with `|weight| <= 10^12`.
- **Return type** is `long[][]`, because the sum of 10^4 weights exceeds the `int` range.

**Example 1.** Input `m = 2`, `n = 2` and updates `[[0,0,1,1,5],[1,1,1,1,-7]]`, output `[[5,5],[5,-2]]`.

**Example 2.** Input `m = 1`, `n = 1` and updates `[[0,0,0,0,3000000000000]]`, output `[[3000000000000]]`.

**Hint.** The four corner writes use `+weight` and `-weight` in the same pattern as before. Which Java type must the matrix and the weights have?

**Changed decision.** The increment becomes a signed `long`, so the pattern of four writes stays and the number type must widen.
