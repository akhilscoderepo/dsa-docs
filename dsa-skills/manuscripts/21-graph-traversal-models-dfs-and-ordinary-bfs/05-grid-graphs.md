<!-- lesson-kind: standard -->
<!-- lesson-id: grid-graphs -->
## Grid Graphs

<!-- stage: context -->
### Why Recoloring Every Match Fails

A drawing editor has a paint bucket tool. The user clicks one pixel, and the editor recolors that pixel together with every pixel of the same color that touches it through a shared side. A pixel of the same color in a separate patch must keep its color. The first version of the tool recolored every pixel that matched the clicked color. Users reported that patches far from the click changed too.

The editor needs exactly the patch that connects to the clicked pixel. A map editor has the same need when it counts separate patches of land. This lesson asks how a program finds a connected patch of cells in a table, and how it measures or counts such patches.

<!-- stage: naive -->
### Recoloring Every Pixel That Matches

The direct plan reads the color of the clicked pixel and then scans the whole table. Each pixel with that color receives the new color, wherever it sits. The method needs no helper and finishes after one pass over the rows and columns.

```java
static int[][] recolorEveryMatch(int[][] image, int sr, int sc, int color) {
    int old = image[sr][sc];
    for (int r = 0; r < image.length; r++) {
        for (int c = 0; c < image[r].length; c++) {
            if (image[r][c] == old) image[r][c] = color;
        }
    }
    return image;
}
```

```predict
Run the method on `image = {{1, 0}, {0, 1}}` with the click at row 0, column 0 and `color = 3`. What does it return, and is that the patch that connects to the click?

It returns `{{3, 0}, {0, 3}}`. The pixel at row 1, column 1 has the clicked color, but it touches the clicked pixel only at a corner and shares no side with it. The correct result is `{{3, 0}, {0, 1}}`.
```

<!-- stage: bottleneck -->
### Counting The Work Of A Correct Search

The scan costs O(rows * cols), which is cheap, but it answers the wrong question. It tests each pixel alone and never asks whether the pixel connects to the click.

A correct but slow repair keeps the scan and adds a connection test. Each round scans the whole table for one pixel that has the old color and touches an already recolored pixel, then recolors it. A patch of `k` pixels needs `k` rounds, and each round costs O(rows * cols). In the worst case the patch covers the table, and the total is O((rows * cols)^2). A table of 1,000 by 1,000 pixels then needs about 10^12 steps.

A recursive repair that calls itself on the four touching pixels also fails. Pixel A calls pixel B, and pixel B calls pixel A again, so the calls never end. Both repairs share one flaw. They have no record of which pixels the search already reached, so they repeat work on pixels they have seen. The program needs a rule that reaches each pixel once.

<!-- stage: insight -->
### Treating Cells As Vertices

#### Defining The Graph On Cells

A **grid graph** has one vertex for each cell of a two-dimensional array. Two vertices share an edge when their cells touch through a side, in the direction up, down, left or right. Both cells must also satisfy the rule of the problem. For the paint bucket, the rule is that the cell has the clicked color. A patch of connected cells is a component of this graph, and the clicked cell is the source.

<!-- names: grid graph, direction table, bounds check -->

#### Computing Neighbors On Demand

Nobody stores this graph. The program computes the neighbors of a cell when it needs them, so the `adj` list from the Graph Representation lesson never exists. A **direction table** such as `{{1,0},{-1,0},{0,1},{0,-1}}` holds the four row and column steps. Adding each step to the cell `(r, c)` gives the four candidate neighbors.

Each candidate passes a **bounds check** first. The row must lie in `0..rows-1` and the column in `0..cols-1`. A candidate outside the table has no cell to read, and reading it throws `ArrayIndexOutOfBoundsException`. The check on the cell's rule comes only after the bounds check passes.

#### Marking Each Cell Once

The search keeps `visited` as a boolean array with one slot per cell. It marks a cell at the moment the cell enters the frontier, not when the cell leaves. A cell therefore enters the frontier at most once, and the search never finds it again. The invariant is that every cell in the frontier is in bounds, satisfies the rule and is already marked. Each cell expands once, and each expansion tests four candidates. The work therefore grows with the number of cells.

The program encodes a cell `(r, c)` as the single integer `r * cols + c`. The program decodes it with `id / cols` and `id % cols`. A frontier of plain integers avoids one small array per cell.

<!-- stage: variables -->
### What The Search Keeps

The search keeps a few named values, listed here with the roles they play in the trace below.

- **rows** and **cols** are the table dimensions, read once from the array.
- **dirs** is the direction table, one row and column step for each direction.
- **visited** is a boolean array of size `rows * cols`, indexed by the cell id.
- **frontier** is an `ArrayDeque` of cell ids waiting for expansion.
- **cur** is the id of the cell that just left the frontier.

<!-- stage: trace -->
### Filling A Patch Step By Step

#### Filling A Seven Cell Patch

The first trace uses a table with three rows and three columns, flattened row by row into nine cells, so cell 4 is row 1, column 1. The source is cell 0, whose color is 1. The pointer `cur` marks the cell that leaves the frontier. The variable `frontier` shows the cell ids still waiting, and `reached` counts the cells that have joined the patch.

Cells 2 and 4 hold the color 0, so they block the patch. The patch still wraps around cell 4 through cells 3, 6, 7 and 8, and then reaches cell 5. The search stops after seven cells, and the frontier is empty.

```trace
{"cells":[1,1,0,1,0,1,1,1,1],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"reached":1,"frontier":"3,1"},"note":"Cell 0 at row 0, column 0 leaves the frontier and joins the patch, and it adds 2 new neighbors (3,1)."},{"at":{"cur":3},"vars":{"reached":2,"frontier":"1,6"},"note":"Cell 3 at row 1, column 0 leaves the frontier and joins the patch, and it adds 1 new neighbor (6)."},{"at":{"cur":1},"vars":{"reached":3,"frontier":"6"},"note":"Cell 1 at row 0, column 1 leaves the frontier and joins the patch, and it adds nothing, because every neighbor is out of bounds, has another color or is already marked."},{"at":{"cur":6},"vars":{"reached":4,"frontier":"7"},"note":"Cell 6 at row 2, column 0 leaves the frontier and joins the patch, and it adds 1 new neighbor (7)."},{"at":{"cur":7},"vars":{"reached":5,"frontier":"8"},"note":"Cell 7 at row 2, column 1 leaves the frontier and joins the patch, and it adds 1 new neighbor (8)."},{"at":{"cur":8},"vars":{"reached":6,"frontier":"5"},"note":"Cell 8 at row 2, column 2 leaves the frontier and joins the patch, and it adds 1 new neighbor (5)."},{"at":{"cur":5},"vars":{"reached":7,"frontier":"empty"},"note":"Cell 5 at row 1, column 2 leaves the frontier and joins the patch, and it adds nothing, because every neighbor is out of bounds, has another color or is already marked."}]}
```

#### Stopping At A Corner

The second trace uses a table with three rows and three columns whose patch holds only the cells 0, 3 and 4. The source is cell 0. Cell 8 holds the same color but touches cell 4 only at a corner. Cell 2 holds it too and sits behind a different color. The search never tests cell 8 from cell 4, because none of the four directions in the direction table is diagonal.

```trace
{"cells":[1,0,1,1,1,0,0,0,1],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"reached":1,"frontier":"3"},"note":"Cell 0 at row 0, column 0 leaves the frontier and joins the patch, and it adds 1 new neighbor (3)."},{"at":{"cur":3},"vars":{"reached":2,"frontier":"4"},"note":"Cell 3 at row 1, column 0 leaves the frontier and joins the patch, and it adds 1 new neighbor (4)."},{"at":{"cur":4},"vars":{"reached":3,"frontier":"empty"},"note":"Cell 4 at row 1, column 1 leaves the frontier and joins the patch, and it adds nothing, because every neighbor is out of bounds, has another color or is already marked."}]}
```

<!-- stage: code -->
### Breadth-First Search On A Grid

#### Measuring One Patch

The method below measures the patch of cells that connects to `(sr, sc)` and share its value. It reads the table and writes nothing.

```java
static int patchSize(int[][] grid, int sr, int sc) {
    int rows = grid.length, cols = grid[0].length;
    int want = grid[sr][sc];
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    boolean[] visited = new boolean[rows * cols];
    ArrayDeque<Integer> frontier = new ArrayDeque<>();
    visited[sr * cols + sc] = true;               // mark when queued
    frontier.add(sr * cols + sc);
    int size = 0;
    while (!frontier.isEmpty()) {
        int cur = frontier.poll();
        size++;
        int r = cur / cols, c = cur % cols;       // decode the id
        for (int[] d : dirs) {
            int nr = r + d[0], nc = c + d[1];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;   // bounds check first
            int id = nr * cols + nc;
            if (visited[id] || grid[nr][nc] != want) continue;           // then visited and rule
            visited[id] = true;
            frontier.add(id);
        }
    }
    return size;
}
```

#### Cost Of The Search

- **Time** is O(rows * cols), because each cell enters the frontier at most once and each expansion tests four candidates.
- **Space** is O(rows * cols), because `visited` has one slot per cell and the frontier can hold a large part of the table.

Two small changes turn this method into the first two exercises. To recolor, write the new color into `grid[nr][nc]` when a cell is marked, and skip the `visited` array only when the new color differs from `want`. To count patches, run the same search from every unmarked cell that matches, and add one to a counter for each search that starts.

A recursive version has the same time but nests as deep as the patch is long. A patch of one million cells would overflow the Java call stack, so the lesson uses the frontier.

<!-- stage: applicability -->
### Spotting A Grid Graph In A Problem

#### Reading The Statement

Look for words such as adjacent, connected, region, island, neighbor and touching in a statement about a table. They say that cells are vertices and that moves between touching cells are the edges. The statement also supplies the rule that makes a cell eligible, such as a color or a land marker.

#### Holding The Invariant

Every cell in the frontier must be in bounds, eligible and already marked. If the program marks a cell only when it leaves the frontier, the same cell can enter the frontier several times. The answer stays correct on small inputs and the cost grows quickly on large ones. A recolor that writes the new color into the table can replace `visited`. That works only when the new color differs from the old one, and the boundary exercise below tests that case.

#### Avoiding The Diagonal Trap

A two-dimensional array stores cells in rows and columns, and that layout is a false friend. It suggests that a cell has eight neighbors, while the problem usually grants four. Diagonal contact joins cells only when the statement says so, and then the direction table grows to eight steps. Mixing up the row and column of a step, or testing the cell's rule before the bounds check, are the two other common faults.

<!-- stage: exercises -->
### Exercises

#### [Build] Flood Fill (LeetCode 733)
<!-- id: gt-flood-fill -->

**Prerequisites.** The grid graph, the direction table and the visited array from this lesson.

**Problem.** An image is a rectangular array `image` of integer colors. Two pixels are neighbors when they share a side. A connected patch is the set of pixels reachable from the pixel at `(sr, sc)` by moving between neighbors that all have the color `image[sr][sc]`. Recolor every pixel of this patch to `color`. Return the image after recoloring.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 50`, and every row has the same length.
- **Colors** satisfy `0 <= image[r][c], color < 65536` and have type `int`.
- **Source** `(sr, sc)` is a valid cell of the image.
- **Neighbors** use the four side directions only, and diagonal pixels are not neighbors.
- **Mutation** is permitted; the method may change `image` and return it.

**Example 1.** Input `image = [[1,1,1],[1,1,0],[1,0,1]]`, `sr = 1`, `sc = 1`, `color = 2`, output `[[2,2,2],[2,2,0],[2,0,1]]`.

**Example 2.** Input `image = [[1,0],[0,1]]`, `sr = 0`, `sc = 0`, `color = 3`, output `[[3,0],[0,1]]`, because the pixel at row 1, column 1 touches only at a corner.

**Hint.** Mark a pixel when it enters the frontier. Which three tests does a candidate neighbor need, and in which order?

**Changed decision.** A whole-table scan becomes a search from the source, and the search moves only across shared sides.

#### [Vary] Number Of Islands (LeetCode 200)
<!-- id: gt-island-count -->

**Prerequisites.** The Flood Fill exercise above.

**Problem.** A map is a rectangular `char[][]` array `grid` whose cells hold `'1'` for land or `'0'` for water. An island is a maximal set of land cells in which any two cells connect through neighbors that share a side. Return the number of islands in the map.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 300`, and every row has the same length.
- **Cells** are the `char` values `'0'` and `'1'` only.
- **Neighbors** use the four side directions only.
- **Answer** is an `int`, and it is 0 when the map has no land.
- **Mutation** does not occur; the method must leave `grid` unchanged.

**Example 1.** Input `grid = ["11000","11000","00100","00011"]` with each row written as a string of characters, output 3.

**Example 2.** Input `grid = ["101","010","101"]`, output 5, because corner contact does not join land cells.

**Hint.** One search covers one island. What decides whether a cell starts a new search?

**Changed decision.** The program starts one search for each unvisited land cell and counts the searches.

#### [Boundary] Original Color Equals New Color (Author exercise)
<!-- id: gt-same-color -->

**Prerequisites.** The Flood Fill exercise above.

**Problem.** Use the image, the patch and the neighbor rules of the Flood Fill exercise. The new `color` may equal the color of the pixel at `(sr, sc)`. Return the image after recoloring the patch. When the two colors are equal, the image stays unchanged, and the method must still finish. The method must finish on every legal input.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 50`, and every row has the same length.
- **Colors** satisfy `0 <= image[r][c], color < 65536`.
- **Equal case** `color == image[sr][sc]` can occur and must return the image unchanged.
- **Neighbors** use the four side directions only.
- **Mutation** is permitted; the method may change `image` and return it.

**Example 1.** Input `image = [[0,0],[0,0]]`, `sr = 1`, `sc = 1`, `color = 0`, output `[[0,0],[0,0]]`.

**Example 2.** Input `image = [[0,0],[0,0]]`, `sr = 1`, `sc = 1`, `color = 1`, output `[[1,1],[1,1]]`.

**Hint.** If the program recolors a cell and then tests the color of its neighbors, can a recolored cell look eligible again? What record prevents that?

**Changed decision.** The program stops using the table's own colors to tell visited cells from fresh ones.

#### [Recognize] Max Area Of Island (LeetCode 695)
<!-- id: gt-island-area -->

**Prerequisites.** The Number Of Islands exercise above.

**Problem.** A map is a rectangular array `grid` of `0` for water and `1` for land. An island is a maximal set of land cells connected through neighbors that share a side. The area of an island is its number of cells. Return the largest area among all islands, or 0 when the map has no land.

**Constraints.** The limits are:
- **Size** is `1 <= rows, cols <= 50`, and every row has the same length.
- **Cells** are the `int` values 0 and 1 only.
- **Neighbors** use the four side directions only.
- **Answer** is an `int` between 0 and `rows * cols`.
- **Mutation** is permitted; the method may change `grid`.

**Example 1.** Input `grid = [[0,1,1,0],[0,1,0,0],[1,0,0,1],[1,0,1,1]]`, output 3.

**Example 2.** Input `grid = [[0,0],[0,0]]`, output 0.

**Hint.** The island count of the previous exercise already starts one search per island. What does each search return besides the fact that it ran?

**Changed decision.** Each search returns its component size, and the caller keeps the maximum.
