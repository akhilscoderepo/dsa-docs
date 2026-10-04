<!-- lesson-kind: standard -->
<!-- lesson-id: structured-traversal -->
## Walking Rows, Columns And Diagonals

<!-- stage: context -->
### A Check That Takes Seconds

A tool compares a grid of sensor readings against a calibration rule. The rule says that every line of cells running down and to the right must hold one repeated value. The first version of the check starts at each cell and follows its line to the edge of the grid, comparing as it goes. On a 10 by 10 test grid, it finishes at once. On the real 2,000 by 2,000 grid, it takes several seconds, and the team wants it under one.

The slow check is correct. It repeats work, because many cells lie on the same line and each of them walks that line again. This lesson asks how to describe a line, a column or the outer edge of a grid by its coordinates, so that one pass touches each cell once.

<!-- stage: naive -->
### Walking The Whole Line From Every Cell

Start at each cell, step down and to the right until the grid ends, and compare every cell on the way with the starting value. If any comparison fails, the rule is broken.

```java
static boolean repeatsAlongLines(int[][] grid) {
    for (int r = 0; r < grid.length; r++) {
        for (int c = 0; c < grid[r].length; c++) {
            int start = grid[r][c];
            int i = r + 1, j = c + 1;
            while (i < grid.length && j < grid[i].length) {
                if (grid[i][j] != start) return false;
                i++;
                j++;
            }
        }
    }
    return true;
}
```

The method is correct on every rectangular grid. It also rereads cells. A cell near the top-left corner is read once as a start and again as a member of every earlier start on its line.

<!-- stage: bottleneck -->
### Counting The Repeated Reads

```predict
On an R by C grid, how many cell reads does the naive check make in the worst case, and which reads repeat?

A start cell walks up to min(R, C) steps, so the total is at most R * C * min(R, C) reads, which is O(R * C * min(R, C)). A cell that sits k steps from the top or left edge is read once for each of the k earlier cells on its line.
```

On a 2,000 by 2,000 grid, the walk from the top-left cell alone reads 1,999 cells. The total reaches about 2.7 billion reads, because most cells have long lines behind them. The grid holds only 4 million cells. Each cell needs one comparison with one neighbor to settle the rule, so the work should be O(R * C). The gap comes from describing each line as a walk to the edge, when each cell can describe its own line by a coordinate relation.

<!-- stage: insight -->
### Name A Region By A Coordinate Rule

Every region that a matrix problem asks for has a rule on the pair `(r, c)`. Find the rule first, and the loops follow from it.

#### Rows, Columns And Diagonals

Row `r` holds the cells `(r, 0)` through `(r, cols - 1)`. Column `c` holds the cells `(0, c)` through `(rows - 1, c)`. A **diagonal** is the set of cells with the same value of `r - c`, because stepping down one row and right one column keeps the difference fixed. An **anti-diagonal** is the set of cells with the same value of `r + c`, because stepping down one row and left one column keeps the sum fixed.

<!-- names: diagonal, anti-diagonal, border -->

#### The Border And The Predecessor

The **border** is the set of cells with `r == 0`, `r == rows - 1`, `c == 0` or `c == cols - 1`. A cell with two of these properties, such as a corner, is one cell and must be counted once. A diagonal also gives a cheap local test. Every cell not in row 0 or column 0 has a predecessor at `(r - 1, c - 1)` on the same diagonal. If each cell equals its predecessor, every cell on the diagonal equals its first cell, by repeating the check along the diagonal. One comparison per cell replaces the whole walk.

#### What The Loops Keep True

A traversal is correct when its indexes describe exactly the region that is still unvisited. The loop bounds are the rule, written as inequalities.

<!-- stage: variables -->
### The Coordinates And The Counts

The loops use four pieces of state, and each has a fixed meaning.

- **r** is the row index of the current cell, and it ranges over `0 <= r < grid.length`.
- **c** is the column index of the current cell, and it ranges over `0 <= c < grid[r].length`.
- **r - c** is the diagonal number, and cells with equal values lie on one diagonal.
- **predecessor** is the cell `(r - 1, c - 1)`, which exists only when `r > 0` and `c > 0`.

<!-- stage: trace -->
### Comparing Each Cell With Its Predecessor

#### A Grid That Passes

Take the 3 by 3 grid with rows `[3, 5, 1]`, `[2, 3, 5]` and `[9, 2, 3]`. The cells are numbered row by row from left to right, starting at 0, so cell 4 is row 1, column 1. In the trace below, `cell` marks the cell under test and `pred` marks its predecessor. The first row and the first column have no predecessor, so they are skipped. The cell at row 1, column 1 holds 3 and its predecessor holds 3. Every later comparison also matches, so the grid passes.

#### A Grid That Fails

Now take `[1, 2, 4]`, `[5, 1, 2]` and `[9, 5, 7]`. The comparisons at row 1 succeed, because 1 equals 1 and 2 equals 2. At row 2, column 2, the cell holds 7 and its predecessor holds 1. The check stops there, and the rule is broken on the diagonal that holds 1, 1 and 7.

#### Stepping Through Both Grids

```trace
{"cells":[3,5,1,2,3,5,9,2,3],"pointers":["cell","pred"],"steps":[{"at":{"cell":0,"pred":-1},"vars":{"r":0,"c":0,"verdict":"pending"},"note":"Cell 0 is in row 0, so it has no predecessor and is skipped. All of row 0 and column 0 are skipped the same way."},{"at":{"cell":4,"pred":0},"vars":{"r":1,"c":1,"verdict":"pending"},"note":"Row 1, column 1 holds 3. Its predecessor holds 3, so they match."},{"at":{"cell":5,"pred":1},"vars":{"r":1,"c":2,"verdict":"pending"},"note":"Row 1, column 2 holds 5. Its predecessor holds 5, so they match."},{"at":{"cell":7,"pred":3},"vars":{"r":2,"c":1,"verdict":"pending"},"note":"Row 2, column 1 holds 2. Its predecessor holds 2, so they match."},{"at":{"cell":8,"pred":4},"vars":{"r":2,"c":2,"verdict":"pending"},"note":"Row 2, column 2 holds 3. Its predecessor holds 3, so they match."},{"at":{"cell":9,"pred":-1},"vars":{"verdict":"true"},"note":"Every cell with a predecessor matched it, so the result is true."}]}
```

```trace
{"cells":[1,2,4,5,1,2,9,5,7],"pointers":["cell","pred"],"steps":[{"at":{"cell":0,"pred":-1},"vars":{"r":0,"c":0,"verdict":"pending"},"note":"Cell 0 is in row 0, so it has no predecessor and is skipped. All of row 0 and column 0 are skipped the same way."},{"at":{"cell":4,"pred":0},"vars":{"r":1,"c":1,"verdict":"pending"},"note":"Row 1, column 1 holds 1. Its predecessor holds 1, so they match."},{"at":{"cell":5,"pred":1},"vars":{"r":1,"c":2,"verdict":"pending"},"note":"Row 1, column 2 holds 2. Its predecessor holds 2, so they match."},{"at":{"cell":7,"pred":3},"vars":{"r":2,"c":1,"verdict":"pending"},"note":"Row 2, column 1 holds 5. Its predecessor holds 5, so they match."},{"at":{"cell":8,"pred":4},"vars":{"r":2,"c":2,"verdict":"false"},"note":"Row 2, column 2 holds 7. Its predecessor holds 1, so they differ and the check stops with false."}]}
```

<!-- stage: code -->
### Two Traversals Written From Their Rules

#### Column Totals And The Predecessor Test

```java
static long[] columnSums(int[][] grid) {
    if (grid.length == 0) return new long[0];
    long[] sums = new long[grid[0].length];
    for (int[] row : grid) {
        for (int c = 0; c < row.length; c++) sums[c] += row[c];
    }
    return sums;
}

static boolean sameAlongDiagonals(int[][] grid) {
    for (int r = 1; r < grid.length; r++) {
        for (int c = 1; c < grid[r].length; c++) {
            if (grid[r][c] != grid[r - 1][c - 1]) return false;
        }
    }
    return true;
}
```

#### Cost Of The Traversals

Both methods cost O(R * C) time. The first uses O(C) extra space for the result. The second uses O(1) extra space. The predecessor test starts both loops at 1, so it never forms a negative index. It assumes a rectangular grid, because it reads `grid[r - 1][c - 1]` and trusts that row `r - 1` is at least as long as column `c`.

<!-- stage: applicability -->
### Telling A Region From A Search

#### The Test For A Region Problem

A prompt is a coordinate-region problem when the cells it asks about follow a rule on `r` and `c`. A whole row, a column, a diagonal and the border are examples. The invariant is that the indexes describe exactly the unvisited part of that region, so no cell is skipped and none is counted twice. The usual defects come from the border and the corners, where two properties hold for one cell.

#### When A Search Replaces A Region Rule

A problem that says "connected cells" or "reachable cells" is a false friend of the region rule, because it also moves between cells. It is a different pattern. The cells it needs are defined by connections between neighbors and not by a formula on `(r, c)`. That pattern needs a record of visited cells, and a later chapter on graph traversal teaches it. If a formula on `r` and `c` names the whole region, use loops. If the region is found only by following neighbors, use a search.

#### Where The Predecessor Test Stops Working

The predecessor test depends on equality being transitive along a diagonal. It does not extend to rules such as "values on a diagonal increase by at most 1 each step" without a change, because that rule involves the difference between neighbors and not equality. State the relation between neighbors before choosing a one-comparison test.

<!-- stage: exercises -->
### Exercises

#### [Build] Column Sums (Author exercise)
<!-- id: mx-column-sums -->

**Prerequisites.** The coordinate rule for a column from this lesson.

**Problem.** Given a rectangular integer matrix `grid` with `R` rows and `C` columns, return an array of length `C` whose entry `c` equals the sum of the cells `grid[0][c]` through `grid[R - 1][c]`. When `R` is 0, return an array of length 0.

**Constraints.** The limits are:
- **Shape** is rectangular, so every row has `C` cells.
- **Size** satisfies `0 <= R <= 1000` and `1 <= C <= 1000` when `R >= 1`.
- **Values** satisfy `-10^6 <= grid[r][c] <= 10^6`, and sums have type `long`.
- **Mutation** does not occur; `grid` does not change.

**Example 1.** Input `grid = [[1,2,3],[4,5,6]]`, output `[5,7,9]`.

**Example 2.** Input `grid = []`, output `[]`, because no row exists to supply a column count.

**Hint.** Which index selects the answer slot, the row or the column?

**Changed decision.** The answer is indexed by column, so the inner loop writes to a different slot on each step.

#### [Vary] Matrix Diagonal Sum (LeetCode 1572)
<!-- id: mx-rect-diagonals -->

**Prerequisites.** The column sums exercise and the diagonal rules from this lesson.

**Problem.** Given a rectangular integer matrix `grid` with `R` rows and `C` columns, let `k = min(R, C)`. The first line holds the cells `(i, i)` for `0 <= i < k`. The second line holds the cells `(i, C - 1 - i)` for `0 <= i < k`. Return the sum of all cells on either line, and count a cell that lies on both lines once.

**Constraints.** The limits are:
- **Shape** is rectangular, and `R` and `C` need not be equal.
- **Size** satisfies `1 <= R, C <= 100`.
- **Values** satisfy `-1000 <= grid[r][c] <= 1000`.
- **Overlap** can occur at most once, at a cell where `i == C - 1 - i`.

**Example 1.** Input `grid = [[1,2,3,4],[5,6,7,8]]`, output 18, from 1, 6, 4 and 7.

**Example 2.** Input `grid = [[1,2,3],[4,5,6]]`, output 9, from 1, 5 and 3, with the shared cell 5 counted once.

**Hint.** For which `i` do the two column formulas name the same cell, and is that `i` below `k`?

**Changed decision.** The matrix is no longer promised square, which differs from the earlier lesson, so the loop bound becomes `min(R, C)` and the overlap test needs the `i < k` check.

#### [Boundary] Perimeter Sum (Author exercise)
<!-- id: mx-border-sum -->

**Prerequisites.** The border rule from this lesson.

**Problem.** Given a rectangular integer matrix `grid` with `R` rows and `C` columns, return the sum of all cells `(r, c)` for which `r == 0`, `r == R - 1`, `c == 0` or `c == C - 1`. Each cell counts once, even when it satisfies two of these conditions.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= R, C <= 1000`.
- **Values** satisfy `-10^6 <= grid[r][c] <= 10^6`.
- **Answer** has type `long`.
- **Target** is O(R + C) time, so the loops must not visit interior cells.

**Example 1.** Input `grid = [[1,2,3],[4,5,6],[7,8,9]]`, output 40, which is every cell except the center 5.

**Example 2.** Input `grid = [[4,6,1,2]]`, output 13, because a single row is all border and no cell repeats.

**Hint.** What happens to the bottom row and the right column when `R` is 1 or `C` is 1?

**Changed decision.** A one-row or one-column input makes two border conditions name the same cells, so each side needs a guard against a second count.

#### [Recognize] Toeplitz Matrix (LeetCode 766)
<!-- id: mx-toeplitz -->

**Prerequisites.** All three exercises above.

**Problem.** An `R x C` matrix is Toeplitz when every diagonal that runs from the top-left toward the bottom-right holds one repeated value. Return true when the matrix is Toeplitz and false otherwise.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= R, C <= 20`.
- **Values** satisfy `0 <= grid[r][c] <= 99`.
- **Target** is O(R * C) time and O(1) extra space.
- **Mutation** does not occur; `grid` does not change.

**Example 1.** Input `grid = [[3,5,1],[2,3,5],[9,2,3]]`, output true.

**Example 2.** Input `grid = [[1,2,4],[5,1,2],[9,5,7]]`, output false, because 7 differs from 1 on one diagonal.

**Hint.** Which single earlier cell lets you test a cell without walking to the start of its diagonal?

**Changed decision.** One comparison with the up-left predecessor replaces a walk along the whole diagonal.
