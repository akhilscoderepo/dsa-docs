<!-- lesson-kind: standard -->
<!-- lesson-id: shape-contracts -->
## Shape Contracts

<!-- stage: context -->
### Counting Seats From A Floor Plan

A theatre manager has a floor plan drawn as a list of rows, and each row lists the seats in it. She wants the total number of seats sold so far, and she asks a new assistant to add them up. The assistant looks at the front row, sees twelve seats, and decides every row must have twelve, so he multiplies by the number of rows.

On the ground floor that works. The balcony does not, because its rows curve around the edge and hold ten, eight and six seats. His total is wrong, and nobody notices, since the number looks plausible. The assistant answered a question about the plan without asking what shape the plan promised to have.

<!-- stage: naive -->
### Use The First Row As The Width

The quick way to walk a grid in Java reads the width once from the first row and then runs a pair of nested loops.

```java
static int sumByFirstRowWidth(int[][] grid) {
    int total = 0;
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < grid[0].length; c++) {
            total += grid[r][c];
        }
    }
    return total;
}
```

On `[[1, 2], [3, 4]]` it returns 10, and on any grid whose rows all have the same length it is correct. It is short, it is what most tutorials show, and it hides an assumption in the expression `grid[0].length`.

<!-- stage: bottleneck -->
### Fine Speed, Wrong Bound

Every cell must be read once, so any correct sum costs O(rows * cols) time and O(1) extra space, and this method matches that. Speed is not the problem. The problem is a hidden promise. `grid[0].length` is the width of one row, and the loop treats it as the width of every row.

When a later row is shorter, the loop reads past its end and throws an `ArrayIndexOutOfBoundsException`. When a later row is longer, the loop silently skips its extra cells and returns too small a total. When the grid has no rows at all, `grid[0]` itself throws before any cell is read. Three different inputs produce three different failures from one expression, and none of them is a performance issue.

<!-- stage: insight -->
### Every Access Needs Legal Indices

Java has no matrix type. An `int[][]` is an array whose elements are themselves arrays, and each inner array has its own length. A **rectangular matrix** is the special case in which every inner array has the same length, so one number describes the width. A **ragged array** is the general case in which rows may differ, and some rows may even be empty.

The safe rule is that an access `grid[r][c]` is legal only when `r` is below `grid.length` and `c` is below the length of that particular row. Use the **row bound** `grid[r].length` in the inner loop and the claim holds for every shape. Using `grid[0].length` is allowed only when the problem promises a rectangular matrix and also promises at least one row.

<!-- names: rectangular matrix, ragged array, row bound -->

The invariant is that every read uses a row index within the outer length and a column index within the length of that row. Three shapes need distinct thought. A matrix with no rows is `new int[0][]`, and reading row zero throws. A matrix with one empty row is `new int[][] {{}}`, which has a row zero of width zero and sums to zero without any error. A ragged array has rows of different widths, so the width must be read per row.

The decision is made once, at the start, from the contract: does the statement promise rectangular shape, a square shape, or nothing? A promise lets the code use a single width and skip a per-row read. Without a promise, per-row reading costs one field access per row and is always safe, so it is the default.

<!-- stage: variables -->
### Row Index, Column Index And The Bound

The outer loop variable `r` runs from zero to `grid.length`. For each row the inner loop variable `c` runs from zero to that row's own length, which is `grid[r].length`. When the shape is promised rectangular, read the width once into a local variable before the loops, after confirming that a row exists. Keep the running total in a variable that is wide enough for the problem. The values never change between rows, but the column bound may, so it belongs inside the outer loop unless a promise says otherwise.

<!-- stage: trace -->
### Two Grids, Two Row Lengths

First grid: `[[1, 2], [], [3]]`, with rows of length 2, 0 and 1. The row-major flattening is `1, 2, 3`. In row 0 the column goes 0 then 1, adding 1 and 2. Row 1 has length zero, so the inner loop reads nothing at all and the cursor does not move. Row 2 has length one, so the column stays at 0 and adds 3. The total is 6. A loop that used the first row's width of 2 would have tried to read `grid[1][0]` and thrown an exception on the empty row.

Second grid: `[[1, 2, 3], [4, 5, 6]]`, a plain rectangle. The column runs 0, 1, 2 in row 0, then resets to 0 at the start of row 1 and runs 0, 1, 2 again. The hardest step is the reset, because the column index is rebuilt for each row, which is exactly why the bound can safely be read from the row that is current.

```trace
{"cells":[1,2,3],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"r":0,"c":0,"rowLength":2,"total":1},"note":"Read grid[0][0] = 1. The column bound is this row's length, 2. The total is 1."},{"at":{"cell":1},"vars":{"r":0,"c":1,"rowLength":2,"total":3},"note":"Read grid[0][1] = 2. The column bound is this row's length, 2. The total is 3."},{"at":{"cell":2},"vars":{"r":1,"rowLength":0,"total":3},"note":"Row 1 has length 0, so the inner loop reads nothing and the cursor stays where it was."},{"at":{"cell":2},"vars":{"r":2,"c":0,"rowLength":1,"total":6},"note":"Read grid[2][0] = 3. The column bound is this row's length, 1. The total is 6."}]}
```

```trace
{"cells":[1,2,3,4,5,6],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"r":0,"c":0,"rowLength":3,"total":1},"note":"Read grid[0][0] = 1. The column bound is this row's length, 3. The total is 1."},{"at":{"cell":1},"vars":{"r":0,"c":1,"rowLength":3,"total":3},"note":"Read grid[0][1] = 2. The column bound is this row's length, 3. The total is 3."},{"at":{"cell":2},"vars":{"r":0,"c":2,"rowLength":3,"total":6},"note":"Read grid[0][2] = 3. The column bound is this row's length, 3. The total is 6."},{"at":{"cell":3},"vars":{"r":1,"c":0,"rowLength":3,"total":10},"note":"Read grid[1][0] = 4. The column bound is this row's length, 3. The total is 10."},{"at":{"cell":4},"vars":{"r":1,"c":1,"rowLength":3,"total":15},"note":"Read grid[1][1] = 5. The column bound is this row's length, 3. The total is 15."},{"at":{"cell":5},"vars":{"r":1,"c":2,"rowLength":3,"total":21},"note":"Read grid[1][2] = 6. The column bound is this row's length, 3. The total is 21."}]}
```

<!-- stage: code -->
### Three Shapes, Three Short Methods

```java
static int rectangularSum(int[][] grid) {              // contract: rows x cols, possibly zero rows
    if (grid.length == 0) return 0;
    int cols = grid[0].length;                         // legal only because a row exists
    int total = 0;
    for (int r = 0; r < grid.length; r++)
        for (int c = 0; c < cols; c++) total += grid[r][c];
    return total;
}

static int raggedSum(int[][] grid) {                   // no shape promise
    int total = 0;
    for (int r = 0; r < grid.length; r++)
        for (int c = 0; c < grid[r].length; c++) total += grid[r][c];
    return total;
}

static boolean hasNoCells(int[][] grid) {
    for (int[] row : grid) if (row.length > 0) return false;
    return true;
}
```

Both sums read every cell once, so the time is O(rows * cols) in the rectangular case and proportional to the number of cells in the ragged case, with O(1) extra space. The first is correct only under its stated contract, and the second is correct for every shape, including zero rows and empty rows. The third helper shows that no rows and only empty rows both mean no cells, which is a different statement from `grid.length == 0`.

<!-- stage: applicability -->
### When The Shape Is A Promise

Use the single-width form only when the statement promises a rectangular matrix and the rows count is positive, or after an explicit emptiness check. Use `grid[r].length` whenever a row may differ, or whenever the contract is silent. The invariant is that every access names a row below the outer length and a column below that row's own length.

The false friend is `grid[0].length` itself, which looks like a safe universal width. It is a statement about row zero and nothing else. A second false friend is the idea that an empty matrix has a single representation. `new int[0][]` has no rows and `new int[][] {{}}` has one row of no cells, and code that treats them alike will either crash or return a wrong answer for one of them.

Java adds a few details to remember. The array of arrays is built row by row, so rows can be separately allocated, shared or null. A null row throws a `NullPointerException` on `.length`, which is why inputs promised to be well formed are worth a sentence in the contract. And a square matrix, where rows equal columns, makes both `grid[i][i]` and `grid[i][n - 1 - i]` legal for every `i`, which is the promise used in the last exercise.

<!-- stage: exercises -->
### Exercises

#### [Build] Rectangular Sum (Author exercise)
<!-- id: mx-rectangular-sum -->

**Prerequisites.** Nested loops over arrays; the contract sheet from Chapter 00.

**Problem.** Given a matrix promised to be rectangular, with `rows` rows of `cols` cells each, return the sum of all cells. If there are no rows, return 0.

**Constraints.** 0 <= rows <= 200 and 1 <= cols <= 200 when rows > 0, with -1000 <= cell <= 1000. The matrix is rectangular by contract.

**Example 1.** Input `grid = [[1, 2], [3, 4]]`, output 10.

**Example 2.** Input `grid = []`, output 0, because the empty contract is stated and no cell exists.

**Hint.** Where does the width come from, and when is it safe to read it? What must be checked before touching row zero?

**Changed decision.** First rung: the shape promise lets the width be read once, after one emptiness check.

#### [Vary] Ragged Sum (Author exercise)
<!-- id: mx-ragged-sum -->

**Prerequisites.** The rectangular-sum exercise above.

**Problem.** Given an array of integer arrays whose rows may have different lengths, including length zero, return the sum of every cell. The rows are not promised to match.

**Constraints.** 0 <= rows <= 200, 0 <= row length <= 200 and -1000 <= cell <= 1000. No row is null.

**Example 1.** Input `grid = [[1, 2], [], [3]]`, output 6.

**Example 2.** Input `grid = [[5], [1, 1, 1, 1]]`, output 9, because the second row is longer than the first.

**Hint.** What would the width of row 0 do on the second example? Which expression gives the length of the row you are on?

**Changed decision.** The width moves inside the outer loop, one read per row, which removes the shape promise.

#### [Boundary] Empty Rows (Author exercise)
<!-- id: mx-empty-rows -->

**Prerequisites.** The two exercises above.

**Problem.** Write a method that tells whether a matrix has any cells. Distinguish `new int[0][]`, which has no rows, from `new int[][] {{}}`, which has one empty row, and show what reading `grid[0]` does in each case.

**Constraints.** The input is never null. Rows are never null, and `grid.length` can be zero.

**Example 1.** Input `grid = new int[0][]`, output false, and reading `grid[0]` throws.

**Example 2.** Input `grid = new int[][] {{}}`, output false, and `grid[0].length` is 0 without any error.

**Hint.** What are `grid.length` and `grid[0].length` for each input? Which one is safe to read first?

**Changed decision.** The tests target the two shapes that share a sum of zero but fail differently on a careless read.

#### [Recognize] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-diagonal-sum-shape -->

**Prerequisites.** All three exercises above.

**Problem.** Given a square matrix, return the sum of the main diagonal plus the secondary diagonal, counting the center cell once when the size is odd.

**Constraints.** 1 <= n <= 100 and 1 <= cell <= 100, with `n` rows and `n` columns. The matrix is square by contract.

**Example 1.** Input `mat = [[2, 0, 1], [3, 5, 4], [6, 7, 9]]`, output 23.

**Example 2.** Input `mat = [[4]]`, output 4, where the single cell is both diagonals and is counted once.

**Hint.** Which two columns do you read in row `i`? When do they coincide, and what should happen then?

**Changed decision.** The square promise makes both diagonal columns legal for every row, so no per-row width is read at all.
