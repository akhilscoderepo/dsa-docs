<!-- lesson-kind: standard -->
<!-- lesson-id: grid-graphs -->
## Grid Graphs

<!-- stage: context -->
### The Glaze Spill At Wren Tileworks

The showroom floor at Wren Tileworks is laid in square tiles, each glazed in one of a few colours: cream, slate, rust. Late on a Friday an apprentice tips a bucket of blue glaze onto a single cream tile. Glaze creeps. It slides across the grout into any cream tile that shares an edge with a wet one, and it stops dead at slate and rust. The owner wants to know, before the floor is scrubbed, exactly which tiles end up blue.

The apprentice stands over the spill with a mop, looking at tiles that touch the wet patch only at a corner, and wonders whether a corner counts. It does not, since glaze cannot cross a corner. The owner wants an answer for any floor and any starting tile, written down as a procedure, not worked out by eye.

<!-- stage: naive -->
### Sweep The Floor Until Nothing Changes

The direct method does what the glaze seems to do. Mark the starting tile wet. Then walk the whole floor, row by row, and wet any cream tile that has a wet tile directly above, below, left or right. One walk may wet new tiles that help the next walk, so repeat the walk until a whole pass wets nothing new.

```java
static boolean[][] reachBySweeps(int[][] floor, int sr, int sc) {
    int rows = floor.length, cols = floor[0].length, tone = floor[sr][sc];
    boolean[][] wet = new boolean[rows][cols];
    wet[sr][sc] = true;
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (wet[r][c] || floor[r][c] != tone) continue;
                boolean touches = (r > 0 && wet[r - 1][c]) || (r + 1 < rows && wet[r + 1][c])
                        || (c > 0 && wet[r][c - 1]) || (c + 1 < cols && wet[r][c + 1]);
                if (touches) { wet[r][c] = true; changed = true; }
            }
        }
    }
    return wet;
}
```

The method is correct for any floor, because a pass that changes nothing proves that no dry cream tile touches a wet one. It also leaves the floor itself untouched and reports the wet tiles in a separate table.

<!-- stage: bottleneck -->
### Each Pass Rereads The Entire Floor

A single pass costs O(R * C) for R rows and C columns, however small the spill. The number of passes is the trouble. Passes run in reading order, so glaze that has to travel up or leftward gains only one tile per pass, and a winding corridor of cream tile can need a pass for nearly every tile it contains. That gives O((R * C)^2) in the worst case, which for a floor of a thousand by a thousand tiles is about a trillion tile checks to wet a corridor that holds a million tiles.

Most of that work is wasted looking. When a tile turns wet, only its four neighbours can possibly be affected, yet the sweep rechecks every other tile on the floor anyway. A better method should remember the freshly wet tiles and look only around those, so that each tile is examined a small fixed number of times in total.

<!-- stage: insight -->
### Tiles As Vertices With Computed Neighbors

Treat every tile as a vertex and never store the edges. The neighbors of a tile are produced on demand by the **direction deltas**, two short arrays `DR = {-1, 1, 0, 0}` and `DC = {0, 0, -1, 1}`. Entry d says how far to shift the row and the column for the d-th move, so the four entries mean up, down, left and right. A diagonal move would need four more entries. Nothing in a rectangular array supplies them, and the contract must say so explicitly if they are wanted.

A candidate tile then passes three gates in a fixed order. Bounds come first, because reading `floor[nr][nc]` outside the array throws before anything else can be asked. Eligibility comes second, since it reads the tile and asks whether it has the colour the spill can travel through. Visited comes last, because only a tile that is inside the board and has the right colour ever needs a look in the seen table.

The queue should not hold small objects. Allocating an `int[]{r, c}` for every tile creates garbage for every move, so pack the two numbers into one **cell code**, `r * cols + c`, and recover them with `code / cols` and `code % cols`. The same code indexes a flat `boolean` array of `rows * cols` cells, and one `int` travels through an `ArrayDeque<Integer>`.

That queue is the **frontier**: the tiles that are wet but whose neighbours have not yet been examined. Mark a tile seen at the moment it joins the frontier, not when it leaves, because two wet neighbours can both reach the same tile before either is removed, and a late mark would enqueue it twice.

The invariant is that every code ever placed on the frontier is in bounds, has the spill colour, and was marked seen exactly once.

<!-- names: direction deltas, cell code, frontier -->

<!-- stage: variables -->
### Floor, Codes And The Seen Table

The 2D array `floor` holds a colour number per tile, `rows` and `cols` come from its shape, and `tone` is the colour of the starting tile, read before anything is changed. The array `seen` has `rows * cols` booleans, indexed by code. The integer `code` is the tile just taken from the queue, `r` and `c` are decoded from it, and `nr` and `nc` are the neighbor being tried for move `d`. The color `newColor` is what each reached tile becomes.

<!-- stage: trace -->
### Two Spills On A Small Floor

The first trace uses a floor of three rows and three columns, stored as one flat row-major list of colours, so the pointer `cur` is a flat index and tile (1, 1) is index 4. The cream tiles are colour 1 and the spill starts at index 0. The vars show the queue after the tile is expanded and how many tiles have been recoloured. The corner tile at index 6 is cream as well, but no wet tile ever touches it by an edge, so it is never reached, which is the diagonal rule at work.

```trace
{"cells":[1,1,0,0,1,0,1,0,1],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"recoloured":1,"queue":"1"},"note":"Tile 0 at row 0, column 0 is recoloured, and it queues 1 new neighbor tile (1)."},{"at":{"cur":1},"vars":{"recoloured":2,"queue":"4"},"note":"Tile 1 at row 0, column 1 is recoloured, and it queues 1 new neighbor tile (4)."},{"at":{"cur":4},"vars":{"recoloured":3,"queue":"empty"},"note":"Tile 4 at row 1, column 1 is recoloured, and it queues nothing, since every neighbor is out of bounds, another colour or already seen."}]}
```

The second trace uses a flat grid of three rows and four columns of '1' (land) and '0' (water), and the pointer `scan` is the outer loop walking all twelve cells in reading order. The loop starts a fresh traversal only at land that is not yet seen, and the vars report how many islands have been started and how many tiles the last traversal claimed. Land at index 1 is skipped because the first traversal already claimed it, and land at index 6 is a separate island even though it touches index 1 at a corner.

@@TRACE2@@

<!-- stage: code -->
### Spilling With A Queue

```java
final class Floor {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    static int[][] spill(int[][] floor, int sr, int sc, int newColor) {
        int rows = floor.length, cols = floor[0].length;
        int tone = floor[sr][sc];
        boolean[] seen = new boolean[rows * cols];
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        seen[sr * cols + sc] = true;
        frontier.add(sr * cols + sc);
        while (!frontier.isEmpty()) {
            int code = frontier.poll();
            int r = code / cols, c = code % cols;
            floor[r][c] = newColor;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d], nc = c + DC[d];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                if (floor[nr][nc] != tone) continue;
                int next = nr * cols + nc;
                if (seen[next]) continue;
                seen[next] = true;
                frontier.add(next);
            }
        }
        return floor;
    }
}
```

The three `continue` lines are the three gates in their order. Time is O(R * C), since each tile enters the queue at most once and spends four checks, and space is O(R * C) for the table and the queue. The code recolours at removal, which is safe here because the table, not the colour, guards against repeats.

<!-- stage: applicability -->
### Boards, Mazes And Pixel Regions

Reach for this model whenever the input is a rectangular board and a question asks what is connected to what: paint buckets, islands on a map, rooms in a floor plan, regions of a screenshot, or the squares a robot can reach. The three-gate order is the invariant to defend in every variant, since each tile that reaches the queue must already be inside the board, allowed by the rule, and new. Counting regions, measuring a region and recolouring a region all use the same traversal and differ only in what happens when a tile is claimed.

The nearest false friend is the belief that a two-dimensional array brings diagonal neighbors along with it. It does not, and an island map where two land tiles meet only at a corner has two islands under the standard contract. A second false friend is recursion for the same job: a depth-first version on a thousand-by-thousand board of one colour recurses a million deep and overflows the Java stack, while the queue does not.

There is no use for this model when the moves are not uniform, for example when each step has a different cost or a tile has hidden doors, because a weighted or explicit graph is then needed. In Java, remember that `char` and `int` compare by number: with a `char[][]` grid, `grid[r][c] == 1` compiles and is always false, because the land character is `'1'`, which has code 49.

<!-- stage: exercises -->
### Exercises

#### [Build] Flood Fill (LeetCode 733)
<!-- id: gt-flood-fill -->

**Prerequisites.** The three-gate order and the queue of cell codes from this lesson.

**Problem.** The `image` is a rectangular grid of colour numbers. Starting at tile `(sr, sc)`, recolour that tile and every tile reachable from it through up, down, left and right steps over tiles that have the starting colour, so that all of them become `color`. The contract is that `image` is modified in place and the same array is returned.

**Constraints.** 1 <= rows, cols <= 50, colours are numbers from 0 to 65535, and the start lies inside the grid. The new colour may equal the old one.

**Example 1.** Input `image = [[2,2,0],[2,0,2],[1,2,2]], sr = 0, sc = 0, color = 5`, output `[[5,5,0],[5,0,2],[1,2,2]]`.

**Example 2.** Input `image = [[1,0,1],[0,1,0]], sr = 1, sc = 1, color = 4`, output `[[1,0,1],[0,4,0]]`.

**Hint.** Which colour must be read before the first tile changes, and what stops a reached tile from being queued twice?

**Changed decision.** A separate seen table guards the traversal, so recolouring cannot be confused with the visited check.

#### [Vary] Number Of Islands (LeetCode 200)
<!-- id: gt-island-count -->

**Prerequisites.** The Flood Fill rung.

**Problem.** The `grid` is a rectangular `char[][]` of `'1'` (land) and `'0'` (water). Return the number of islands, where an island is a maximal group of land tiles joined through up, down, left and right steps. The contract is that `grid` is not modified, so the traversal keeps its own seen table.

**Constraints.** 1 <= rows, cols <= 50, and every entry is the character `'1'` or `'0'`.

**Example 1.** Input rows `"11000"`, `"11000"`, `"00100"`, `"00011"`, output `3`.

**Example 2.** Input rows `"101"`, `"010"`, `"101"`, output `5`.

**Hint.** When the scan meets land, how do you know whether it already belongs to an island that was counted?

**Changed decision.** The traversal is started once per unseen land tile, and the answer is the number of starts instead of the set of recoloured tiles.

#### [Boundary] Original Color Equals New Color (Author exercise)
<!-- id: gt-same-color -->

**Prerequisites.** The Number Of Islands rung.

**Problem.** The contract of Flood Fill holds with one change: no seen table or other extra grid is allowed, so the only memory of progress is the colour written into `image` itself. The new colour may equal the colour of the start tile. Recolour in place and return the same array.

**Constraints.** 1 <= rows, cols <= 50, colours are numbers from 0 to 9, and the start lies inside the grid.

**Example 1.** Input `image = [[6,6,2],[2,6,6]], sr = 0, sc = 0, color = 6`, output `[[6,6,2],[2,6,6]]`.

**Example 2.** Input `image = [[1,1],[1,0]], sr = 0, sc = 1, color = 0`, output `[[0,0],[0,0]]`.

**Hint.** After a tile is recoloured, can the eligibility check tell it apart from an unvisited tile when the two colours match?

**Changed decision.** When the two colours match the answer is the input itself, so the method returns before the first tile is queued.

#### [Recognize] Max Area Of Island (LeetCode 695)
<!-- id: gt-max-island-area -->

**Prerequisites.** The Number Of Islands rung.

**Problem.** The `grid` is a rectangular `int[][]` of `1` (land) and `0` (water). Return the size of the largest island, using up, down, left and right connections, or `0` when the grid holds no land. The contract is that `grid` is not modified.

**Constraints.** 1 <= rows, cols <= 50, and every entry is 0 or 1.

**Example 1.** Input `grid = [[0,1,1,0,0],[0,1,0,0,1],[1,0,0,1,1],[1,0,1,1,0]]`, output `5`.

**Example 2.** Input `grid = [[1,0,1],[0,1,0]]`, output `1`.

**Hint.** What can be counted while a traversal claims tiles, and when must the running best be compared?

**Changed decision.** Each traversal returns the number of tiles it claimed, and the answer is the largest of those sizes instead of their count.
