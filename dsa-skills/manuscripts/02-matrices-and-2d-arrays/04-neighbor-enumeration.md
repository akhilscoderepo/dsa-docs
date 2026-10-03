<!-- lesson-kind: standard -->
<!-- lesson-id: neighbor-enumeration -->
## Neighbor Enumeration

<!-- stage: context -->
### Which Plots Touch This One

A gardener has a large vegetable patch divided into square plots, and a plant disease has been found in some of them. It spreads to touching plots, so for each plot she wants to know how many of its touching plots are infected. A plot in the middle touches eight others if corners count, and a plot at the edge touches fewer, because the fence cuts off some of its surroundings.

She could answer the question for one plot by looking at the plots around it. For all the plots she needs a routine that works the same way everywhere. The routine must handle the middle, the fence and the corners without a separate set of rules for each, because she has hundreds of plots and she will make a mistake if there are special cases.

<!-- stage: naive -->
### Compare Every Plot With Every Other Plot

The most literal translation asks, for each plot, whether each other plot touches it.

```java
static int[][] countsByScanning(int[][] infected) {
    int rows = infected.length, cols = infected[0].length;
    int[][] counts = new int[rows][cols];
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            for (int r2 = 0; r2 < rows; r2++) {
                for (int c2 = 0; c2 < cols; c2++) {
                    boolean touches = (r2 != r || c2 != c) && Math.abs(r2 - r) <= 1 && Math.abs(c2 - c) <= 1;
                    if (touches) counts[r][c] += infected[r2][c2];
                }
            }
        }
    }
    return counts;
}
```

It is correct for every shape, since it never reads outside the grid. For a three-by-three patch it checks eighty-one pairs and produces the right counts.

<!-- stage: bottleneck -->
### Eighty-One Checks For Nine Plots

For `rows * cols = N` plots the four loops perform `N * N` checks, so the time is O(N^2). A modest 200 by 200 patch has forty thousand plots, and the method makes 1.6 billion adjacency tests. The extra space is the output only. The cost is out of proportion to the question, because every plot has at most eight neighbors and the method looks at all `N` plots to find them.

The waste is that the neighbors are known without searching. A plot at row `r` and column `c` touches exactly the plots at row `r - 1`, `r` and `r + 1` and column `c - 1`, `c` and `c + 1`, except itself. That is eight fixed coordinates. The only real question is which of those eight lie inside the grid.

<!-- stage: insight -->
### Offsets Propose, Bounds Decide

The neighborhood of a cell is the cell plus a fixed list of small changes in row and column. Write the list once as an **offset table**: four pairs for up, down, left and right, or eight pairs if diagonals count. Adding each pair to `(r, c)` gives a candidate. Some candidates may fall outside the grid, so each one must pass a **bounds guard**, a check that the row is in `0..rows - 1` and the column in `0..cols - 1`, before the grid is read.

The set of cells that survive the guard is the **neighborhood** of the cell. A middle cell keeps all of its candidates, an edge cell loses some, and a corner cell loses most. The code does not need three cases for these, because the guard does the sorting. The loop over the table is a constant length, so enumerating the neighborhood costs O(1) per cell, and a whole-grid pass costs O(rows * cols).

<!-- names: offset table, bounds guard, neighborhood -->

The invariant is that every grid read happens only after the guard has accepted the coordinates, so no negative index and no index at or past the length is ever used. The table must not contain the pair `(0, 0)`, since that would count the cell as its own neighbor. For eight neighbors it is easiest to write the table out explicitly, or to loop both offsets over `-1, 0, 1` and skip the pair of zeros.

A last point concerns where the table lives. Allocating a fresh array of pairs inside the inner loop creates garbage for every cell. Declare the offsets as constants outside the loops, once per class, and reuse them. The result is the same, and the program does not spend time creating and discarding tiny arrays.

<!-- stage: variables -->
### The Cell, The Offset And The Candidate

The pair `(r, c)` is the cell whose neighborhood is wanted. Each entry of the offset table is a pair `(dr, dc)`, and the candidate is `(nr, nc) = (r + dr, c + dc)`. The guard compares `nr` with zero and `rows` and `nc` with zero and `cols`, using the bounds of the grid and not of a particular row unless the grid may be ragged. A running count or list collects the neighbors that pass. The table is constant, so nothing about it changes between cells.

<!-- stage: trace -->
### A Corner And A Middle Cell

Take the board `[[1, 0, 1], [0, 1, 0], [1, 1, 0]]` and ask about the corner cell `(0, 0)` with eight offsets. The offsets go up-left, up, up-right, left, right, down-left, down, down-right. Up-left is `(-1, -1)`, up is `(-1, 0)` and up-right is `(-1, 1)`, all outside because the row is negative. Left is `(0, -1)`, outside. Right is `(0, 1)`, legal, holding 0. Down-left is `(1, -1)`, outside. Down is `(1, 0)`, legal, holding 0. Down-right is `(1, 1)`, legal, holding 1.

Three of eight candidates survive, and the count of infected neighbors is 1. The step to study is the first one, where a candidate with a negative row was never read. For the middle cell `(1, 1)` with four orthogonal offsets, all four candidates are legal: up holds 0, down holds 1, left holds 0 and right holds 0, so the count is 1 and the guard rejected nothing.

```trace
{"cells":[1,0,1,0,1,0,1,1,0],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"offset":"(-1,-1)","live":0},"note":"Offset up-left gives (-1, -1), which is off the board, so it is never read. The live count stays 0."},{"at":{"cell":-1},"vars":{"offset":"(-1,0)","live":0},"note":"Offset up gives (-1, 0), which is off the board, so it is never read. The live count stays 0."},{"at":{"cell":-1},"vars":{"offset":"(-1,1)","live":0},"note":"Offset up-right gives (-1, 1), which is off the board, so it is never read. The live count stays 0."},{"at":{"cell":-1},"vars":{"offset":"(0,-1)","live":0},"note":"Offset left gives (0, -1), which is off the board, so it is never read. The live count stays 0."},{"at":{"cell":1},"vars":{"offset":"(0,1)","live":0},"note":"Offset right gives (0, 1), which is on the board and holds 0. The live count is 0."},{"at":{"cell":-1},"vars":{"offset":"(1,-1)","live":0},"note":"Offset down-left gives (1, -1), which is off the board, so it is never read. The live count stays 0."},{"at":{"cell":3},"vars":{"offset":"(1,0)","live":0},"note":"Offset down gives (1, 0), which is on the board and holds 0. The live count is 0."},{"at":{"cell":4},"vars":{"offset":"(1,1)","live":1},"note":"Offset down-right gives (1, 1), which is on the board and holds 1. The live count is 1."}]}
```

```trace
{"cells":[1,0,1,0,1,0,1,1,0],"pointers":["cell"],"steps":[{"at":{"cell":1},"vars":{"offset":"(-1,0)","live":0},"note":"Offset up gives (0, 1), which is on the board and holds 0. The live count is 0."},{"at":{"cell":7},"vars":{"offset":"(1,0)","live":1},"note":"Offset down gives (2, 1), which is on the board and holds 1. The live count is 1."},{"at":{"cell":3},"vars":{"offset":"(0,-1)","live":1},"note":"Offset left gives (1, 0), which is on the board and holds 0. The live count is 1."},{"at":{"cell":5},"vars":{"offset":"(0,1)","live":1},"note":"Offset right gives (1, 2), which is on the board and holds 0. The live count is 1."}]}
```

<!-- stage: code -->
### One Table, One Guard

```java
static final int[] DR8 = {-1, -1, -1, 0, 0, 1, 1, 1};
static final int[] DC8 = {-1, 0, 1, -1, 1, -1, 0, 1};
static final int[] DR4 = {-1, 1, 0, 0};
static final int[] DC4 = {0, 0, -1, 1};

static int orthogonalCount(int rows, int cols, int r, int c) {
    int count = 0;
    for (int k = 0; k < 4; k++) {
        int nr = r + DR4[k], nc = c + DC4[k];
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) count++;
    }
    return count;
}

static int liveNeighbors(int[][] board, int r, int c) {
    int live = 0;
    for (int k = 0; k < 8; k++) {
        int nr = r + DR8[k], nc = c + DC8[k];
        if (nr >= 0 && nr < board.length && nc >= 0 && nc < board[0].length) live += board[nr][nc];
    }
    return live;
}

static int[][] neighborCounts(int[][] board) {
    int[][] counts = new int[board.length][board[0].length];
    for (int r = 0; r < board.length; r++)
        for (int c = 0; c < board[0].length; c++) counts[r][c] = liveNeighbors(board, r, c);
    return counts;
}
```

Each cell costs a fixed eight candidates, so the whole pass is O(rows * cols) time with O(1) extra space apart from the output. The tables are `static final` and allocated once. The counts are written to a separate array, so every read sees the original board and no cell's count is changed by an earlier update, a point the later marker lesson turns into a technique.

<!-- stage: applicability -->
### When A Cell Depends On Its Surroundings

Use neighbor enumeration when the value for a cell depends on a fixed local neighborhood, such as touching cells or cells one step away in the four directions. The invariant is that each candidate coordinate is guarded before it is read, and the table is constant. The same code handles middle, edge and corner cells.

The false friend is a question about reachability. Counting the infected plots that touch a plot is local. Asking whether an infected region connects two distant plots through chains of touching plots is not, since the answer depends on paths of unknown length. That needs a graph traversal with a visited record, which a later chapter owns. A second false friend is the guard written as a pair of special cases for the first and last row, which looks tidy for a middle cell and fails on a corner, or on a grid with one row.

In Java, check both bounds on both indices, and put the checks before the read, joined by short-circuit `&&`. If the grid might be ragged, the column bound is `board[nr].length` for the candidate's row, and the row check must come first. Keep the offset tables out of the loop, and do not include the pair `(0, 0)` in them.

<!-- stage: exercises -->
### Exercises

#### [Build] Orthogonal Count (Author exercise)
<!-- id: mx-orthogonal-count -->

**Prerequisites.** The shape-contract lesson; the direction table from the previous lesson.

**Problem.** For a board with `rows` rows and `cols` columns, return how many of the four orthogonal neighbors of cell `(r, c)`, meaning up, down, left and right, lie inside the board.

**Constraints.** 1 <= rows, cols <= 100 and the cell is inside the board. Allocate the offset table once.

**Example 1.** Input `rows = 3, cols = 4, r = 1, c = 2`, output 4.

**Example 2.** Input `rows = 1, cols = 5, r = 0, c = 2`, output 2, since only left and right exist.

**Hint.** What are the four offsets? Which test decides whether a candidate belongs to the board?

**Changed decision.** First rung: neighbors come from a table of offsets and a guard, not from cases for each position.

#### [Vary] Eight Neighbors (Author exercise)
<!-- id: mx-eight-neighbors -->

**Prerequisites.** The orthogonal-count exercise above.

**Problem.** Do the same for the eight surrounding cells, including diagonals, and never count the cell itself. Return the number of legal neighbors of `(r, c)`.

**Constraints.** 1 <= rows, cols <= 100 and the cell is inside the board. The table must not contain the offset `(0, 0)`.

**Example 1.** Input `rows = 3, cols = 3, r = 1, c = 1`, output 8.

**Example 2.** Input `rows = 3, cols = 4, r = 0, c = 1`, output 5.

**Hint.** Which four offsets must be added to the table? Which pair of offsets would turn the cell into its own neighbor?

**Changed decision.** The table grows from four pairs to eight, and the pair of zeros must stay out.

#### [Boundary] Corner Cell (Author exercise)
<!-- id: mx-corner-cell -->

**Prerequisites.** The two exercises above.

**Problem.** List the legal eight-neighborhood coordinates of the corner cell `(0, 0)`, in the order of the offset table, and show that no negative index is ever used to read the board. State the result for a board with a single cell.

**Constraints.** 1 <= rows, cols <= 100. The offset table order is up-left, up, up-right, left, right, down-left, down, down-right.

**Example 1.** Input `rows = 3, cols = 3`, output `[[0, 1], [1, 0], [1, 1]]`.

**Example 2.** Input `rows = 1, cols = 1`, output `[]`, since the only cell has no neighbors.

**Hint.** Which candidates have a negative row or column? Why must the guard run before any read of the board?

**Changed decision.** The tests target the cell that loses the most candidates, where a missing guard fails fastest.

#### [Recognize] Neighbor Counts For Game Of Life (LeetCode 289)
<!-- id: mx-neighbor-counts -->

**Prerequisites.** All three exercises above.

**Problem.** Given a board of 0 and 1 values, where 1 is a live cell, return a new matrix in which each entry is the number of live cells among the eight neighbors of the corresponding cell. This is the first half of one Game of Life generation, and the board is not changed.

**Constraints.** 1 <= rows, cols <= 25 and each cell is 0 or 1. The result is a separate matrix.

**Example 1.** Input `board = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]`, output `[[1, 3, 1], [4, 4, 3], [2, 2, 2]]`.

**Example 2.** Input `board = [[1]]`, output `[[0]]`, because a lone cell has no neighbors.

**Hint.** How many candidates does every cell have, and how are the ones outside the board skipped? Why must the counts go in a separate matrix?

**Changed decision.** The enumeration runs for every cell, and the counts are kept apart from the board so every read sees the original generation.
