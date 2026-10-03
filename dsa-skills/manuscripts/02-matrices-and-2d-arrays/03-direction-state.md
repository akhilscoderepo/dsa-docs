<!-- lesson-kind: standard -->
<!-- lesson-id: direction-state -->
## Direction State

<!-- stage: context -->
### A Mower That Turns At Fences

A small robot mower is dropped at the corner of a walled lawn that is divided into square tiles. It starts facing east and it follows one rule. It keeps going straight while the next tile is open grass. When the next tile is a wall or has already been mown, it turns right and carries on. It never needs a map and never plans ahead. It only needs to know where it is, which way it faces, and whether the tile ahead is open.

The owner wants a record of the order in which the tiles are mown, with the tile numbered 1, 2, 3 and so on in the order of visit. Written out, the numbering winds inward in a spiral, and the robot produced it with nothing but a simple habit. The task for the programmer is to reproduce that record without drawing the spiral by hand.

<!-- stage: naive -->
### Remember Every Visited Tile In A List

A direct translation keeps a list of the coordinates the mower has already visited. Before each step it searches that list to decide whether the tile ahead is taken.

```java
static int[][] spiralByVisitedList(int n) {
    int[][] grid = new int[n][n];
    List<int[]> visited = new ArrayList<>();
    int r = 0, c = 0, dr = 0, dc = 1;
    for (int v = 1; v <= n * n; v++) {
        grid[r][c] = v;
        visited.add(new int[] {r, c});
        if (v == n * n) break;
        int nr = r + dr, nc = c + dc;
        boolean blocked = nr < 0 || nr >= n || nc < 0 || nc >= n;
        for (int[] p : visited) if (p[0] == nr && p[1] == nc) blocked = true;
        if (blocked) { int t = dr; dr = dc; dc = -t; nr = r + dr; nc = c + dc; }
        r = nr; c = nc;
    }
    return grid;
}
```

It produces the right spiral. For `n = 3` it writes 1, 2, 3 across the top, turns, and winds inward to end with 9 in the center.

<!-- stage: bottleneck -->
### A Search Before Every Step

The list grows by one entry per step, and every step searches all of it, so step `k` costs about `k` comparisons. There are `n * n` steps, which makes the total about `(n * n)^2 / 2`, or O(n^4) time. For `n = 300` that is roughly four billion comparisons to number ninety thousand tiles. The extra space is O(n^2) for the list, on top of the grid itself.

The search repeats work that the grid already knows. Every visited tile has been given a number, and a tile that has not been visited still holds zero. Asking the grid whether the tile ahead is zero answers the same question in one read. The list is a second copy of information that the output already carries, and the cost comes from searching it.

<!-- stage: insight -->
### Position And Heading Decide The Next Step

The whole simulation is described by three values: the row, the column and the heading. Those three values are the **cursor state**, and together they determine the next step completely. Nothing about earlier steps is needed except what the grid itself records.

Store the four headings in a **direction table**, ordered clockwise: east, south, west, north, as pairs of row and column offsets. The heading is an index into the table, and turning right is adding one to the index and wrapping around after the fourth entry. The **turn rule** is the test that decides when to do it: turn when the tile ahead is outside the board or is already filled. A filled tile is one that holds a nonzero value, so the output grid doubles as the record of visits.

<!-- names: cursor state, direction table, turn rule -->

The invariant is that after writing the value `k`, the cursor sits on the tile holding `k`, every tile with a smaller number is filled, and the next tile in spiral order is either straight ahead or one right turn away. A single turn is enough, because in a spiral the tile to the right of a blocked heading is open as long as any tile remains. The loop therefore stops after the last value is written and never turns again.

The turn rule is a choice. Here it is wall-and-visited, which suits a board that fills up. Another spiral, taken up in the last exercise, uses a turn after a counted number of steps, and it lets the cursor wander outside the board. In that case the number of steps left in the current leg joins the cursor state, and only tiles inside the board are recorded. The principle is the same: write down everything that determines the next step, and nothing else.

<!-- stage: variables -->
### Row, Column, Heading And The Value

The row `r` and column `c` locate the cursor. The heading `d` is an index from 0 to 3 into two small constant arrays of row and column offsets, so the step is `r + DR[d]` and `c + DC[d]`. The counter `v` is the next value to write, and it also tells the loop when to stop. The grid starts with zeros, and any nonzero entry means visited. Allocate the two offset arrays once, as constants outside the loop, and not on every step. The turn changes only `d`, and the step then uses the new heading.

<!-- stage: trace -->
### Winding Three By Three

Start at the top-left tile heading east. The first write puts 1 at `(0, 0)`. The tile ahead is open, so the cursor steps east and writes 2, then steps east again and writes 3 at `(0, 2)`. Now the tile ahead is outside the board, so the heading turns from east to south, and the cursor writes 4 at `(1, 2)` and 5 at `(2, 2)`.

At `(2, 2)` the south tile is outside, so the heading turns west, and 6 and 7 fill the bottom row. At `(2, 0)` the west tile is outside, so the heading turns north and writes 8 at `(1, 0)`. The tile ahead at `(0, 0)` is already filled, so the heading turns east, and the cursor steps to `(1, 1)` and writes 9. After 9 the loop ends, with no extra turn. The step to study is 8 to 9, where a tile that is inside the board forced a turn because it was already full.

A second picture, with no filled-tile rule, is a walker on a two-by-three board that only turns at the edge. It circles the border and returns to the corner, which shows how little the heading needs to know.

```trace
{"cells":[1,2,3,8,9,4,7,6,5],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"value":1,"r":0,"c":0,"heading":"E"},"note":"Write 1 at (0, 0) heading E."},{"at":{"cell":1},"vars":{"value":2,"r":0,"c":1,"heading":"E"},"note":"Write 2 at (0, 1) heading E."},{"at":{"cell":2},"vars":{"value":3,"r":0,"c":2,"heading":"E"},"note":"Write 3 at (0, 2) heading E. The cell ahead is blocked, so turn to S."},{"at":{"cell":5},"vars":{"value":4,"r":1,"c":2,"heading":"S"},"note":"Write 4 at (1, 2) heading S."},{"at":{"cell":8},"vars":{"value":5,"r":2,"c":2,"heading":"S"},"note":"Write 5 at (2, 2) heading S. The cell ahead is blocked, so turn to W."},{"at":{"cell":7},"vars":{"value":6,"r":2,"c":1,"heading":"W"},"note":"Write 6 at (2, 1) heading W."},{"at":{"cell":6},"vars":{"value":7,"r":2,"c":0,"heading":"W"},"note":"Write 7 at (2, 0) heading W. The cell ahead is blocked, so turn to N."},{"at":{"cell":3},"vars":{"value":8,"r":1,"c":0,"heading":"N"},"note":"Write 8 at (1, 0) heading N. The cell ahead is blocked, so turn to E."},{"at":{"cell":4},"vars":{"value":9,"r":1,"c":1,"heading":"E"},"note":"Write 9 at (1, 1) heading E."}]}
```

```trace
{"cells":[0,0,0,0,0,0],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"step":0,"heading":"E"},"note":"Start at the corner facing east."},{"at":{"cell":1},"vars":{"step":1,"heading":"E"},"note":"Step 1 reaches (0, 1) heading E."},{"at":{"cell":2},"vars":{"step":2,"heading":"E"},"note":"Step 2 reaches (0, 2) heading E."},{"at":{"cell":5},"vars":{"step":3,"heading":"S"},"note":"Step 3 reaches (1, 2) heading S. The cell ahead was off the board, so turn to S."},{"at":{"cell":4},"vars":{"step":4,"heading":"W"},"note":"Step 4 reaches (1, 1) heading W. The cell ahead was off the board, so turn to W."},{"at":{"cell":3},"vars":{"step":5,"heading":"W"},"note":"Step 5 reaches (1, 0) heading W."},{"at":{"cell":0},"vars":{"step":6,"heading":"N"},"note":"Step 6 reaches (0, 0) heading N. The cell ahead was off the board, so turn to N."},{"at":{"cell":1},"vars":{"step":7,"heading":"E"},"note":"Step 7 reaches (0, 1) heading E. The cell ahead was off the board, so turn to E."}]}
```

<!-- stage: code -->
### A Table Of Headings And A Turn

```java
static final int[] DR = {0, 1, 0, -1};                 // east, south, west, north
static final int[] DC = {1, 0, -1, 0};

static int[][] spiralFill(int n) {
    int[][] grid = new int[n][n];
    int r = 0, c = 0, d = 0, total = n * n;
    for (int v = 1; v <= total; v++) {
        grid[r][c] = v;
        if (v == total) break;                          // no step and no turn after the last write
        int nr = r + DR[d], nc = c + DC[d];
        if (nr < 0 || nr >= n || nc < 0 || nc >= n || grid[nr][nc] != 0) {
            d = (d + 1) % 4;
            nr = r + DR[d]; nc = c + DC[d];
        }
        r = nr; c = nc;
    }
    return grid;
}

static int[] walkAroundEdge(int rows, int cols, int steps) {   // returns {row, col, heading}
    int r = 0, c = 0, d = 0;
    for (int s = 0; s < steps; s++) {
        int nr = r + DR[d], nc = c + DC[d];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) { d = (d + 1) % 4; nr = r + DR[d]; nc = c + DC[d]; }
        r = nr; c = nc;
    }
    return new int[] {r, c, d};
}
```

Both methods perform a constant amount of work per step, so the spiral costs O(n^2) time and the walker O(steps), with O(1) extra space apart from the output grid. The offset tables are allocated once as constants, and the check for the last value prevents a pointless final turn. The walker needs a board of at least two rows and two columns, since on a single tile or a single strip a turn does not open a tile.

<!-- stage: applicability -->
### When One Cursor Follows A Turn Rule

Use cursor state when a single moving position follows a cyclic rule for headings and the turn depends on what is ahead or on a counted number of steps. The invariant is that the row, column and heading determine the next step, and the grid records what has been visited. Write the headings in a table and let the heading be an index.

The false friend is a frontier of many positions, as in breadth-first search. That explores outward from a source through every open neighbor and needs a queue and a visited set, and the answer is a distance or a region. A spiral follows one cursor, one path, and one tile at a time. Another false friend is the shrinking-boundary spiral, taught in a later lesson of this chapter. It produces the same order from four boundaries and not from a heading, and it fails in different places, mainly when one row or column remains.

For Java, keep the offsets in two arrays or one array of pairs allocated once. Do not use a zero in the grid as an empty marker when zero is a legal value in the output, since the filled-tile test would then misfire. And decide the stopping condition by counting writes, so the last turn is never made.

<!-- stage: exercises -->
### Exercises

#### [Build] Clockwise Walker (Author exercise)
<!-- id: mx-clockwise-walker -->

**Prerequisites.** The shape-contract lesson; the direction table idea in this lesson.

**Problem.** A walker starts at the top-left cell of a board with `rows` rows and `cols` columns, facing east. It takes `steps` single steps. Before each step, if the cell ahead is off the board, it turns clockwise once and then steps. Return its final row, column and heading, with headings numbered 0 for east, 1 for south, 2 for west and 3 for north.

**Constraints.** 2 <= rows, cols <= 50 and 0 <= steps <= 10^4. Only the board edge causes a turn.

**Example 1.** Input `rows = 3, cols = 3, steps = 5`, output row 2, column 1, heading 2.

**Example 2.** Input `rows = 2, cols = 2, steps = 4`, output row 0, column 0, heading 3, back at the corner after one lap.

**Hint.** What are the four offsets in clockwise order? Which single value changes when the walker turns?

**Changed decision.** First rung: the heading becomes an index into a table, and a turn is an increment with wrap-around.

#### [Vary] Spiral Matrix II (LeetCode 59)
<!-- id: mx-spiral-matrix-two -->

**Prerequisites.** The clockwise-walker exercise above.

**Problem.** Given a positive integer `n`, generate an `n` by `n` matrix filled with the numbers 1 to `n * n` in clockwise spiral order, starting at the top-left corner.

**Constraints.** 1 <= n <= 20. Use the matrix itself to know which cells are filled.

**Example 1.** Input `n = 4`, output `[[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]`.

**Example 2.** Input `n = 2`, output `[[1, 2], [4, 3]]`.

**Hint.** What extra condition besides the board edge should trigger a turn? How can the output grid answer it?

**Changed decision.** The turn rule gains a second trigger, a filled cell, and the output grid serves as the visited record.

#### [Boundary] Single Cell (Author exercise)
<!-- id: mx-single-cell -->

**Prerequisites.** The two exercises above.

**Problem.** Run the spiral fill on a one-by-one board and report how many writes happen and how many turns happen. Explain why the loop must stop after the last write instead of preparing the next step.

**Constraints.** n = 1 for the main case, and then check n = 2 and n = 3 for comparison. The stopping test counts writes.

**Example 1.** Input `n = 1`, output one write, zero turns, and the matrix `[[1]]`.

**Example 2.** Input `n = 3`, output nine writes and four turns, with 9 in the center.

**Hint.** What does the loop look at after writing the last value, and does that look serve any purpose? What would a turn there mean on a one-cell board?

**Changed decision.** The tests target the final iteration, where preparing a next step has nothing to prepare.

#### [Recognize] Spiral Matrix III (LeetCode 885)
<!-- id: mx-spiral-matrix-three -->

**Prerequisites.** All three exercises above.

**Problem.** On a grid with `rows` rows and `cols` columns, a walker starts at `(rStart, cStart)` facing east and walks a clockwise spiral that may leave the grid. The spiral walks 1 step east, 1 south, 2 west, 2 north, 3 east, 3 south, and so on. Return the grid coordinates in the order they are first visited, recording only cells inside the grid, until every cell has been recorded.

**Constraints.** 1 <= rows, cols <= 100 and the start is inside the grid. The walker may be outside the grid for long stretches.

**Example 1.** Input `rows = 2, cols = 3, rStart = 1, cStart = 1`, output `[[1, 1], [1, 2], [1, 0], [0, 0], [0, 1], [0, 2]]`.

**Example 2.** Input `rows = 1, cols = 1, rStart = 0, cStart = 0`, output `[[0, 0]]`.

**Hint.** What decides each turn in this spiral, and what must the state remember to know when it comes? Which steps get recorded?

**Changed decision.** The turn rule counts steps in a leg instead of testing walls, so the cursor state gains a leg length and the cursor may roam outside the grid.
