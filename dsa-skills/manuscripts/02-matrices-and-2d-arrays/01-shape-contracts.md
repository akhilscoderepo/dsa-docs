<!-- lesson-kind: standard -->
<!-- lesson-id: shape-contracts -->
## Rectangular And Ragged Arrays

<!-- stage: context -->
### A Sum That Crashes On One Row

A reporting job reads a table of daily counts from a file and sums every cell. The table has three rows. The second row lost its last value during export, so the rows hold 3, 2 and 3 values. The job runs for months on complete files. On the damaged file, it stops with `ArrayIndexOutOfBoundsException` after reading only five cells.

The code did not contain an arithmetic mistake. It contained a belief about the table: every row has the same number of values. Nothing in Java enforces that belief. This lesson asks one question. What does the type `int[][]` actually promise about row lengths, and how does a loop stay legal when the promise is weaker than the loop assumes?

<!-- stage: naive -->
### Using The First Row As The Width

The usual loop over a table reads the row count from `grid.length` and the column count from the first row, `grid[0].length`. Both bounds look natural, and they work on every table written by hand in a textbook.

```java
static int sumAll(int[][] grid) {
    int total = 0;
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < grid[0].length; c++) {
            total += grid[r][c];
        }
    }
    return total;
}
```

On `{{1, 2, 3}, {4, 5, 6}}` this returns 21. On `{{1, 2, 3}, {4, 5}}` it reads `grid[1][2]` and throws. On `{{}, {1, 2}}` it returns 0 and silently ignores the second row.

<!-- stage: bottleneck -->
### Two Failures From One Assumption

```predict
The naive loop uses grid[0].length for every row. Name the two different ways it goes wrong when row lengths differ, and say whether the cost of a correct loop changes.

When a later row is shorter than the first row, the loop reads past the end of that row and throws. When a later row is longer, the loop stops early and skips cells without any error. A correct loop reads the true length of each row and costs O(R + N), where R is the row count and N is the total number of cells.
```

The first failure is loud and the second one is silent. The silent failure is worse, because the program returns a plausible wrong number. Both come from the same assumption, so one fix covers both. The fix does not make the loop slower. Reading `grid[r].length` once per row adds R extra reads, and the cell visits still total N, so the whole loop runs in O(R + N) time. The remaining question is which guarantees the statement gives, so that you know when the cheaper `grid[0].length` is safe.

<!-- stage: insight -->
### Each Row Is Its Own Array

A two-dimensional array in Java is an array whose elements are arrays. Each row is a separate object with its own length. The row count comes from `grid.length`, and the length of row `r` comes from `grid[r].length`. No object stores a single column count for the whole table.

#### Three Shapes A Table Can Have

A **rectangular** table has the same length in every row, so one column count describes all rows. A **square** table is rectangular with as many rows as columns. A **ragged** table has at least two rows of different lengths. The type `int[][]` allows all three. Only the problem statement says which one a method receives.

<!-- names: rectangular, square, ragged -->

#### The Rule For Every Access

A cell `(r, c)` is legal when `0 <= r < grid.length` and `0 <= c < grid[r].length`. The column bound depends on the row. Reading the bound from `grid[r]` is correct for all three shapes. Reading it from `grid[0]` is correct only when the statement promises a rectangular table. When the promise exists, the cheaper form is safe, because every row length equals the first one.

#### Two Empty Cases That Differ

`new int[0][]` has no rows, so `grid[0]` itself does not exist. `new int[][]{{}}` has one row with no cells, so `grid[0]` exists and its length is 0. A method that reads `grid[0].length` before checking `grid.length` throws on the first form and survives the second.

<!-- stage: variables -->
### Row Count, Row Length And Cell Total

The loop needs three pieces of state, and each one changes at a known moment.

- **grid.length** holds the row count and never changes during the loop.
- **grid[r].length** holds the number of cells in row `r` and is read once when the loop enters that row.
- **total** holds the sum of all cells visited so far and grows by one cell value per inner step.

<!-- stage: trace -->
### Summing Two Tables With Different Rows

#### A Rectangular Table

Take `grid = {{1, 2}, {3, 4}}`. The pointer `r` marks the current row. Each step of the trace below finishes one whole row. Row 0 holds two cells and adds 3. Row 1 also holds two cells and adds 7, so the total becomes 10. For this table, the bound `grid[0].length` gives the same answer as `grid[r].length`.

#### A Ragged Table

Now take `grid = {{1, 2}, {}, {3}}`. Row 1 holds no cells, so the inner loop runs zero times and the total stays 3. Row 2 holds one cell and adds 3. The final total is 6. The bound `grid[0].length` equals 2 for every row on this table, so it would try to read two cells from the empty row 1 and throw.

#### Stepping Through Both Tables

```trace
{"cells":["[1,2]","[3,4]"],"pointers":["r"],"steps":[{"at":{"r":-1},"vars":{"total":0},"note":"Start: no row has been read, so total is 0."},{"at":{"r":0},"vars":{"rowLength":2,"total":3},"note":"Row 0 holds 2 cell(s) and adds 3. The total is 3."},{"at":{"r":1},"vars":{"rowLength":2,"total":10},"note":"Row 1 holds 2 cell(s) and adds 7. The total is 10."}]}
```

```trace
{"cells":["[1,2]","[]","[3]"],"pointers":["r"],"steps":[{"at":{"r":-1},"vars":{"total":0},"note":"Start: no row has been read, so total is 0."},{"at":{"r":0},"vars":{"rowLength":2,"total":3},"note":"Row 0 holds 2 cell(s) and adds 3. The total is 3."},{"at":{"r":1},"vars":{"rowLength":0,"total":3},"note":"Row 1 holds 0 cell(s), so the inner loop runs zero times. The total is 3."},{"at":{"r":2},"vars":{"rowLength":1,"total":6},"note":"Row 2 holds 1 cell(s) and adds 3. The total is 6."},{"at":{"r":3},"vars":{"total":6},"note":"The row index equals grid.length, so the loop ends with total 6."}]}
```

<!-- stage: code -->
### Summing With The Row's Own Length

#### A Loop That Reads Each Row's Length

```java
static long sumRagged(int[][] grid) {
    long total = 0;
    for (int[] row : grid) {
        for (int value : row) {
            total += value;
        }
    }
    return total;
}

static long sumRectangular(int[][] grid, int cols) {
    long total = 0;
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < cols; c++) {
            total += grid[r][c];
        }
    }
    return total;
}
```

#### When Each Form Applies

The first method needs no promise about row lengths, because the for-each loop reads each row's own length. The second method takes the column count `cols` as a parameter, which is correct only when the statement promises a rectangular table. Both methods cost O(R + N) time and O(1) extra space. The accumulator has type `long`, because a table of 10^5 cells with values near 2^31 overflows an `int`.

<!-- stage: applicability -->
### Reading The Shape From The Statement

#### Looking For The Promise

Before writing any loop, find the sentence that fixes the shape. Phrases such as "an `m x n` matrix" or "an `n x n` matrix" promise a rectangular or square table. A phrase such as "a list of rows" or "rows may differ in length" promises nothing. When the statement is silent, treat the table as ragged. The invariant of the lesson is that every access uses a row index below `grid.length` and a column index below the length of that same row.

#### A False Friend From Other Languages

Many readers carry over a rule from languages with true two-dimensional arrays, where one declaration fixes both sizes. In Java the declaration `new int[3][4]` happens to build a rectangular table, but the type does not remember it. A later assignment such as `grid[1] = new int[2]` makes the table ragged without any error. Code that receives the table cannot tell the two apart without reading the row lengths.

#### When A Row Can Be Null

A table declared as `new int[3][]` has three rows that are all `null` until assigned. Reading `grid[0].length` on it throws `NullPointerException`. Statements that give an `int[][]` almost never contain null rows, so check the contract before adding a guard that the contract makes unnecessary.

<!-- stage: exercises -->
### Exercises

#### [Build] Rectangular Sum (Author exercise)
<!-- id: mx-rect-sum -->

**Prerequisites.** The rule for a legal cell and the rectangular shape from this lesson.

**Problem.** Let `grid` be an `int[][]` that holds `rows` rows with exactly `cols` cells each. Return the sum of every cell, as a `long`. A table with no rows has sum 0.

**Constraints.** The limits are:
- **Shape** is rectangular, so every row has the same length.
- **Size** satisfies `0 <= rows <= 1000` and `0 <= cols <= 1000`.
- **Values** satisfy `-10^6 <= grid[r][c] <= 10^6`.
- **Mutation** does not occur; `grid` does not change.

**Example 1.** Input `grid = [[1,2],[3,4]]`, output 10.

**Example 2.** Input `grid = []`, output 0, because no cell exists.

**Hint.** Where does the column count come from when the statement promises equal rows, and what happens when `grid` has no rows at all?

**Changed decision.** Basic case: one promised column count replaces a per-row read.

#### [Vary] Ragged Sum (Author exercise)
<!-- id: mx-ragged-sum -->

**Prerequisites.** The rectangular sum exercise above.

**Problem.** Let `grid` be an `int[][]` whose rows may have different lengths, including length 0. Return the sum of all cells as a `long`.

**Constraints.** The limits are:
- **Shape** is ragged; rows may have different lengths.
- **Rows** satisfy `0 <= grid.length <= 1000`, and each row length satisfies `0 <= grid[r].length <= 1000`.
- **Values** satisfy `-10^6 <= grid[r][c] <= 10^6`.
- **Rows** are never `null`.
- **Mutation** does not occur; `grid` does not change.

**Example 1.** Input `grid = [[1,2],[],[3]]`, output 6.

**Example 2.** Input `grid = [[],[]]`, output 0, because both rows are empty.

**Hint.** Which expression gives the number of cells in row `r`?

**Changed decision.** The column bound moves from one shared value to a value read for each row.

#### [Boundary] Empty Rows (Author exercise)
<!-- id: mx-empty-rows -->

**Prerequisites.** The two sums above and the two empty forms from this lesson.

**Problem.** Let `grid` be an `int[][]`. Return an `int[]` of length 2 that holds the number of rows and the number of cells. A row with no cells counts as a row and adds 0 cells. Do not read any row before checking that the row exists.

**Constraints.** The limits are:
- **Shape** may be ragged, and `grid` itself is never `null`.
- **Rows** satisfy `0 <= grid.length <= 1000`; a row may have length 0.
- **Answer** is `{rows, cells}`, both of type `int`.
- **Mutation** does not occur; `grid` does not change.

**Example 1.** Input `grid = new int[0][]`, output `[0, 0]`.

**Example 2.** Input `grid = new int[][]{{}}`, output `[1, 0]`.

**Hint.** Which of the two inputs makes `grid[0]` itself illegal?

**Changed decision.** The empty input splits into two cases, and the loop bound alone handles both.

#### [Recognize] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-diagonal-sum -->

**Prerequisites.** All three exercises above.

**Problem.** Let `mat` be a square `n x n` integer matrix. The primary diagonal holds the cells `mat[i][i]`. The secondary diagonal holds the cells `mat[i][n - 1 - i]`. Return the sum of all cells on either diagonal, and count a cell that lies on both diagonals once.

**Constraints.** The limits are:
- **Shape** is square, so both coordinates stay legal for every `i`.
- **Size** satisfies `1 <= n <= 100`.
- **Values** satisfy `1 <= mat[i][j] <= 100`.
- **Overlap** happens exactly at the center cell when `n` is odd.

**Example 1.** Input `mat = [[2,0,1],[0,5,0],[3,0,4]]`, output 15, from 2, 5, 4, 1 and 3.

**Example 2.** Input `mat = [[7]]`, output 7, because the one cell lies on both diagonals.

**Hint.** The square promise makes both formulas legal. When do the two formulas name the same cell?

**Changed decision.** The promise of a square shape replaces every per-row length check.
