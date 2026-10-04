<!-- lesson-kind: standard -->
<!-- lesson-id: neighbor-enumeration -->
## Checking The Neighbors Of A Cell

<!-- stage: context -->
### A Mine Counter That Miscounts The Corner

A minesweeper clone shows each safe cell with the number of mines in the cells touching it. The first version spells out the eight touching cells as eight separate `if` statements, each with its own range test. It works for months. Then a player reports that the top-right corner shows a count one too low. One of the eight range tests rejected a cell that lies inside the board. Only a corner cell hit that test.

The task is simple, and the code is long because every touching cell is typed by hand. This lesson asks how to describe the cells that touch a given cell once, in data, so that a loop handles all of them and the range test is written in one place.

<!-- stage: naive -->
### Eight Hand-Written Conditions

The method checks each touching cell with its own condition and adds 1 when the cell holds a mine.

```java
static int countMines(boolean[][] mine, int r, int c) {
    int rows = mine.length, cols = mine[0].length, count = 0;
    if (r > 0 && c > 0 && mine[r - 1][c - 1]) count++;
    if (r > 0 && mine[r - 1][c]) count++;
    if (r > 0 && c < cols - 1 && mine[r - 1][c + 1]) count++;
    if (c > 0 && mine[r][c - 1]) count++;
    if (c < cols - 1 && mine[r][c + 1]) count++;
    if (r < rows - 1 && c > 0 && mine[r + 1][c - 1]) count++;
    if (r < rows - 1 && mine[r + 1][c]) count++;
    if (r < rows - 1 && c < cols - 1 && mine[r + 1][c + 1]) count++;
    return count;
}
```

The method is correct as written. It has eight statements and twelve comparisons, and one mistyped comparison corrupts only edge cells.

<!-- stage: bottleneck -->
### What Grows When The Rule Changes

```predict
Each call does a constant amount of work. What grows with the number of touching cells, and what changes when the game also counts only the four cells directly above, below, left and right?

The work per call stays O(1), but the number of hand-written lines and range tests grows with each touching cell. A four-cell rule needs a new method that repeats half of the lines with a different mix of conditions.
```

The cost per call is constant, so the cost for a whole board is O(R * C). The cost that grows is the amount of code, which is proportional to the number of touching cells. Each variant of the rule, such as four cells instead of eight, forces a fresh copy with a fresh chance of a sign error. The eight tests also repeat the same two checks, one for the row and one for the column, in different combinations. The repeated structure is the signal that the cells should come from a list of data and the range test should run once.

<!-- stage: insight -->
### Offsets And One Range Test

Every touching cell differs from the cell `(r, c)` by a fixed pair of changes, one for the row and one for the column. Such a pair is an **offset**. The cell reached by the offset `(dr, dc)` is `(r + dr, c + dc)`.

#### The Table Of Offsets

A **direction table** lists the offsets of a rule. The four-cell rule uses `(-1, 0)`, `(1, 0)`, `(0, -1)` and `(0, 1)`. The eight-cell rule adds the four diagonal offsets `(-1, -1)`, `(-1, 1)`, `(1, -1)` and `(1, 1)`. The offset `(0, 0)` is never in the table, because it names the cell itself.

#### The Single Range Test

A candidate `(nr, nc)` exists when `0 <= nr < grid.length` and `0 <= nc < grid[nr].length`. The loop computes each candidate and applies this test once. A candidate that fails is skipped, and the cell has no such neighbor. A corner of a rectangular grid therefore has 3 neighbors under the eight-cell rule, an edge cell has 5, and an interior cell has 8. The invariant is that every offset in the table is tried exactly once, and only legal cells are read.

#### The Neighborhood As Data

The set of cells touching a given cell under a chosen table is its **neighborhood**. Changing the rule means changing the table and nothing else.

<!-- names: offset, direction table, neighborhood -->

<!-- stage: variables -->
### The Table, The Candidate And The Count

The loop uses four pieces of state.

- **DIRS4 and DIRS8** are the direction tables, with one row of two integers per offset, and neither table changes.
- **nr and nc** hold the candidate cell for the current offset and are recomputed on each iteration.
- **count** holds the number of qualifying neighbors found so far.
- **r and c** hold the center cell and stay fixed during the loop.

<!-- stage: trace -->
### Counting A Corner And An Edge

#### A Corner With Eight Offsets

Take a 3 by 3 board and the corner cell at row 0, column 0. The loop tries the eight offsets in table order. In the trace below, the pointer `center` marks the cell being examined and `cand` marks the candidate cell by its row-major index, with -1 for a candidate outside the board. The offsets that go up or left give a negative row or column, so five candidates fall outside and three are legal: the cells at index 1, 3 and 4.

#### An Edge Cell With Four Offsets

Now take the cell at row 1, column 0 and the four-cell table. The offset up reaches row 0, column 0 and the offset down reaches row 2, column 0. The offset left leaves the board. The offset right reaches row 1, column 1. Three of the four candidates are legal.

#### Stepping Through Both Counts

```trace
{"cells":[0,1,2,3,4,5,6,7,8],"pointers":["center","cand"],"steps":[{"at":{"center":0,"cand":-1},"vars":{"offset":"(-1,-1)","candidate":"(-1,-1)","count":0},"note":"Offset (-1,-1) reaches row -1, column -1. It lies outside the board, so the count stays 0."},{"at":{"center":0,"cand":-1},"vars":{"offset":"(-1,0)","candidate":"(-1,0)","count":0},"note":"Offset (-1,0) reaches row -1, column 0. It lies outside the board, so the count stays 0."},{"at":{"center":0,"cand":-1},"vars":{"offset":"(-1,1)","candidate":"(-1,1)","count":0},"note":"Offset (-1,1) reaches row -1, column 1. It lies outside the board, so the count stays 0."},{"at":{"center":0,"cand":-1},"vars":{"offset":"(0,-1)","candidate":"(0,-1)","count":0},"note":"Offset (0,-1) reaches row 0, column -1. It lies outside the board, so the count stays 0."},{"at":{"center":0,"cand":1},"vars":{"offset":"(0,1)","candidate":"(0,1)","count":1},"note":"Offset (0,1) reaches row 0, column 1. It lies inside the board, so the count becomes 1."},{"at":{"center":0,"cand":-1},"vars":{"offset":"(1,-1)","candidate":"(1,-1)","count":1},"note":"Offset (1,-1) reaches row 1, column -1. It lies outside the board, so the count stays 1."},{"at":{"center":0,"cand":3},"vars":{"offset":"(1,0)","candidate":"(1,0)","count":2},"note":"Offset (1,0) reaches row 1, column 0. It lies inside the board, so the count becomes 2."},{"at":{"center":0,"cand":4},"vars":{"offset":"(1,1)","candidate":"(1,1)","count":3},"note":"Offset (1,1) reaches row 1, column 1. It lies inside the board, so the count becomes 3."}]}
```

```trace
{"cells":[0,1,2,3,4,5,6,7,8],"pointers":["center","cand"],"steps":[{"at":{"center":3,"cand":0},"vars":{"offset":"(-1,0)","candidate":"(0,0)","count":1},"note":"Offset (-1,0) reaches row 0, column 0. It lies inside the board, so the count becomes 1."},{"at":{"center":3,"cand":6},"vars":{"offset":"(1,0)","candidate":"(2,0)","count":2},"note":"Offset (1,0) reaches row 2, column 0. It lies inside the board, so the count becomes 2."},{"at":{"center":3,"cand":-1},"vars":{"offset":"(0,-1)","candidate":"(1,-1)","count":2},"note":"Offset (0,-1) reaches row 1, column -1. It lies outside the board, so the count stays 2."},{"at":{"center":3,"cand":4},"vars":{"offset":"(0,1)","candidate":"(1,1)","count":3},"note":"Offset (0,1) reaches row 1, column 1. It lies inside the board, so the count becomes 3."}]}
```

<!-- stage: code -->
### One Loop For Every Rule

#### The Table Outside The Loop

```java
private static final int[][] DIRS4 = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
private static final int[][] DIRS8 = {
    {-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}};

static int countLegal(int[][] grid, int r, int c, int[][] dirs) {
    int count = 0;
    for (int[] d : dirs) {
        int nr = r + d[0], nc = c + d[1];
        if (nr >= 0 && nr < grid.length && nc >= 0 && nc < grid[nr].length) count++;
    }
    return count;
}
```

#### Why The Table Is A Static Field

Both tables are created once, as `static final` fields. A table written as `new int[][]{...}` inside the loop would allocate nine objects on every cell, which is 9 * R * C extra allocations on a board of R * C cells. The allocations do not change the time bound, but they add garbage collection work to the inner loop of a hot method. Each call costs O(k) for a table of k offsets, which is a constant, so counting every cell of a board costs O(R * C).

<!-- stage: applicability -->
### Where A Fixed Neighborhood Fits

#### When Offsets Fit

The pattern fits when a cell's result depends only on cells at fixed offsets from it. Counting mines and applying a rule to adjacent cells are examples. The invariant is that every offset is tried once, and only cells inside the grid are read. The table is also the place to encode a rule such as "knight moves" or "left and right only".

#### When Flood Fill Replaces The Offsets

A task that asks for a whole connected region, such as all land cells joined to one cell, uses neighbors too. It is a false friend of the offset table, because it follows neighbors repeatedly. The cell reached by one offset becomes the start of the next round of offsets. That repetition needs a record of visited cells and is a graph traversal, which a later chapter teaches. A fixed neighborhood stops after one round of offsets.

#### A Table That Includes The Center

A table with the offset `(0, 0)` makes the cell its own neighbor. Some rules want that, such as a blur that averages a cell with its neighbors. Counting the neighbors of a cell never wants it, so check the table for the zero offset before reusing it for a different rule.

<!-- stage: exercises -->
### Exercises

#### [Build] Orthogonal Count (Author exercise)
<!-- id: mx-orthogonal-count -->

**Prerequisites.** The direction table and the single range test from this lesson.

**Problem.** An `R x C` grid has cells `(r, c)` with `0 <= r < R` and `0 <= c < C`. The orthogonal neighbors of a cell are the cells directly above, below, left and right of it that lie inside the grid. Given `R`, `C`, `r` and `c`, return the number of orthogonal neighbors of `(r, c)`.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= R, C <= 1000`.
- **Cell** satisfies `0 <= r < R` and `0 <= c < C`.
- **Answer** is an `int` from 0 to 4.
- **Mutation** does not occur, and no grid values are involved.

**Example 1.** Input `R = 3, C = 4, r = 1, c = 2`, output 4.

**Example 2.** Input `R = 3, C = 4, r = 0, c = 0`, output 2.

**Hint.** Which four offsets form the table, and which test removes a candidate that falls off the grid?

**Changed decision.** Basic case: the table lists four offsets, and the range test is written once.

#### [Vary] Eight Neighbors (Author exercise)
<!-- id: mx-eight-neighbors -->

**Prerequisites.** The orthogonal count exercise above.

**Problem.** Use the grid and cell conventions of the previous exercise. The eight neighbors of a cell are the orthogonal neighbors together with the four cells diagonally adjacent to it, restricted to the cells inside the grid. Return the number of eight neighbors of `(r, c)`. The cell itself is never one of its own neighbors.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= R, C <= 1000`.
- **Cell** satisfies `0 <= r < R` and `0 <= c < C`.
- **Answer** is an `int` from 0 to 8.
- **Table** must not contain the offset `(0, 0)`.

**Example 1.** Input `R = 3, C = 3, r = 1, c = 1`, output 8.

**Example 2.** Input `R = 3, C = 4, r = 0, c = 3`, output 3.

**Hint.** Which four offsets are added to the orthogonal table, and which offset must stay out?

**Changed decision.** The table grows from four offsets to eight, and the range test stays the same.

#### [Boundary] Corner Cell (Author exercise)
<!-- id: mx-corner-cell -->

**Prerequisites.** The two counting exercises above.

**Problem.** Given `R`, `C`, `r` and `c` as before, return the list of the eight neighbors of `(r, c)` that lie inside the grid. List each neighbor as `[row, col]`, in increasing order of row and then of column. Return an empty list when the grid has no neighbor of the cell.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= R, C <= 1000`.
- **Cell** satisfies `0 <= r < R` and `0 <= c < C`.
- **Answer** is a list of at most 8 pairs, without duplicates.
- **Indexes** read by the method must never be negative or at least the grid size.

**Example 1.** Input `R = 3, C = 3, r = 0, c = 0`, output `[[0,1],[1,0],[1,1]]`.

**Example 2.** Input `R = 1, C = 1, r = 0, c = 0`, output `[]`, because a single cell has no neighbor.

**Hint.** Which of the eight candidates of the top-left corner have a negative row or column, and what is the order of the offsets in the table?

**Changed decision.** The corner removes five of eight candidates, so the table order must also match the required output order.

#### [Recognize] Game Of Life (LeetCode 289)
<!-- id: mx-life-next -->

**Prerequisites.** All three exercises above.

**Problem.** A board is an `m x n` grid of cells, each 1 (live) or 0 (dead). The next generation follows four rules applied to every cell at once, using the eight neighbors of the cell in the current board. A live cell with fewer than 2 live neighbors dies. A live cell with 2 or 3 live neighbors stays live. A live cell with more than 3 live neighbors dies. A dead cell with exactly 3 live neighbors becomes live. Return the next board as a new array and leave the input board unchanged.

**Constraints.** The limits are:
- **Board** satisfies `1 <= m, n <= 25`, and each cell is 0 or 1.
- **Update** is simultaneous, so every count uses the current board.
- **Mutation** does not occur; the method returns a new `int[][]`.
- **Space** may use O(m * n) for the new board.

**Example 1.** Input `board = [[0,1,0],[0,1,0],[0,1,0]]`, output `[[0,0,0],[1,1,1],[0,0,0]]`.

**Example 2.** Input `board = [[1,1],[1,0]]`, output `[[1,1],[1,1]]`.

**Hint.** Where must the new state be written so that a later cell still reads the old state of its neighbors?

**Changed decision.** The neighbor count feeds a rule, and a second board keeps the old generation readable while the new one is built.
