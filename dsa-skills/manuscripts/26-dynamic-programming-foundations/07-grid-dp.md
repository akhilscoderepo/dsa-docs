<!-- lesson-kind: standard -->
<!-- lesson-id: grid-dp -->
## Grid DP

<!-- stage: context -->
### A Route Counter That Never Finishes

A planning tool for a warehouse robot counts the distinct routes across a rectangular floor. The robot starts in the top-left cell and must stop in the bottom-right cell. Each step moves it one cell right, one cell down, or one cell down and right at once. Some cells hold shelves, and the robot cannot enter them. The tool must report the route count for any floor plan the operators draw.

The first version works on the 4 by 4 test floor and answers instantly. Operators then upload a 12 by 12 plan, and the call runs for minutes. Nothing is wrong with the logic. Something about the way the count is computed makes the work explode as the floor grows.

A **grid** here is a matrix with `R` rows and `C` columns, where `(r, c)` names the cell in row `r` and column `c`, both counted from 0. A **route** is a sequence of allowed steps that avoids blocked cells. The method reads the floor plan and never changes it. This lesson asks how a count over a grid can stay cheap when millions of routes share the same cells.

<!-- stage: naive -->
### Counting Routes By Recursion

The direct idea works backward from the target. A route that ends at `(r, c)` must have come from the cell above, the cell on the left, or the cell on the upper left. So the number of routes into `(r, c)` is the sum of the route counts of those three cells. The recursion stops at the start cell, which has exactly one route, and at any cell that is blocked or outside the grid, which has none.

```java
static long routes(boolean[][] blocked, int r, int c) {
    if (r < 0 || c < 0 || blocked[r][c]) return 0;
    if (r == 0 && c == 0) return 1;
    return routes(blocked, r - 1, c)
         + routes(blocked, r, c - 1)
         + routes(blocked, r - 1, c - 1);
}
```

The call `routes(blocked, R - 1, C - 1)` returns the answer. The method is correct, because every route has a last step, and that step comes from exactly one of the three neighbors. On the 4 by 4 floor the answer arrives at once.

```predict
On a floor with no shelves, how many calls does routes make for a 4 by 4 grid, and how many for a 12 by 12 grid? The grid has 16 cells and 144 cells.

For the 4 by 4 grid it makes 292 calls, which is already more than 18 calls per cell. For the 12 by 12 grid it makes 242,253,796 calls for only 144 cells. The call count multiplies by roughly five or six every time the grid gains one row and one column, so the work grows exponentially while the number of distinct cells grows only quadratically.
```

<!-- stage: bottleneck -->
### The Same Cell Is Solved Again

The recursion treats every call as new work. Yet the call `routes(blocked, 2, 2)` returns the same number each time it appears, because the answer depends only on the arguments `r` and `c` and on the fixed floor plan. The cell `(2, 2)` is reached from the start through many different routes, and each of them re-enters the full recursion below that cell.

Each cell can be requested by three later cells, so the requests multiply as the recursion deepens. The total call count satisfies roughly `T(r, c) = T(r - 1, c) + T(r, c - 1) + T(r - 1, c - 1) + 1`, which grows exponentially in `R + C`, near O(3^(R + C)) for an open grid. A 12 by 12 floor already needs hundreds of millions of calls. In contrast, the grid holds only `R * C` distinct answers, one per cell.

A usable method must compute each cell's answer once and reuse it. That brings the work down to O(R * C) cell visits, with O(1) work per visit, since each cell combines at most three known numbers. The remaining question is how to guarantee that the three numbers are ready before the cell needs them.

<!-- stage: insight -->
### Filling The Table In Reading Order

Give each cell its own stored answer and fill the answers in an order that never asks for a value before it exists.

<!-- names: predecessor, border, fill order -->

#### One Stored Number Per Cell

The 2D array `dp` has the same shape as the grid. The entry `dp[r][c]` holds the number of routes that end exactly at `(r, c)`. The word exactly matters: it excludes routes that pass through `(r, c)` and continue, so each route is counted once, at the cell where it stops. This one sentence defines the state, and every later rule must preserve it.

#### Predecessors Supply The Recurrence

A **predecessor** of `(r, c)` is a cell from which one allowed step reaches `(r, c)`. For the three moves of the warehouse robot, the predecessors are `(r - 1, c)`, `(r, c - 1)` and `(r - 1, c - 1)`. Every route to `(r, c)` has a last step, so `dp[r][c]` is the sum of `dp` over the predecessors. A blocked cell is the exception, because no route may end there, so its entry stays 0 and contributes nothing to cells that follow.

#### Border Cells Have Fewer Predecessors

The **border** cells are the cells in the first row and the first column. A cell in row 0 has no cell above and no cell on the upper left. A cell in column 0 has no cell on the left and no cell on the upper left. So the recurrence must skip a predecessor that lies outside the grid instead of reading an index of -1. The start cell is a special case with no predecessor, and its entry is 1 unless it is blocked.

#### Row By Row Is A Safe Fill Order

The **fill order** is the order in which the loops visit the cells. Row by row, left to right works for these moves, because every predecessor has a smaller row, or the same row and a smaller column. So all predecessors are filled before the cell that needs them. If a move set sent the robot up or to the left, this order would break, and the loops would need another direction. The rule is to read the move set first and choose the loops from it.

<!-- stage: variables -->
### Grid, Table And Loop Indices

The method receives `blocked`, a `boolean[R][C]` where `true` marks a shelf. It never writes to it. The method keeps three working values.

- **dp** is a `long[R][C]`; `dp[r][c]` counts the routes that end exactly at `(r, c)`.
- **r** is the row index of the cell being filled, from 0 to `R - 1`.
- **c** is the column index of the cell being filled, from 0 to `C - 1`.

The type is `long` because the route count on a 30 by 30 open floor already passes the range of `int`. The answer is the entry `dp[R - 1][C - 1]`, and a blocked start or target gives 0.

<!-- stage: trace -->
### Two Runs On Small Grids

#### Counting Routes Around A Shelf

The first floor has 3 rows and 4 columns, with one shelf at row 1, column 1. Each cell of the trace is one grid cell in reading order, so cell 0 is `(0, 0)` and cell 11 is `(2, 3)`. The pointer `cell` selects the cell being filled. The variables `row` and `col` give its coordinates, and `ways` gives its stored count.

The first row fills with ones, since each cell has only the left predecessor. The shelf stores 0 and blocks the center. Cells below and to the right of it still receive routes from their other predecessors. The last cell stores the answer.

```trace
{"cells":["(0,0)","(0,1)","(0,2)","(0,3)","(1,0)","(1,1)","(1,2)","(1,3)","(2,0)","(2,1)","(2,2)","(2,3)"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"row":0,"col":0,"ways":1},"note":"Cell (0, 0) is the start, so it stores 1."},{"at":{"cell":1},"vars":{"row":0,"col":1,"ways":1},"note":"Cell (0, 1) adds 1 predecessor entry 1 and stores 1."},{"at":{"cell":2},"vars":{"row":0,"col":2,"ways":1},"note":"Cell (0, 2) adds 1 predecessor entry 1 and stores 1."},{"at":{"cell":3},"vars":{"row":0,"col":3,"ways":1},"note":"Cell (0, 3) adds 1 predecessor entry 1 and stores 1."},{"at":{"cell":4},"vars":{"row":1,"col":0,"ways":1},"note":"Cell (1, 0) adds 1 predecessor entry 1 and stores 1."},{"at":{"cell":5},"vars":{"row":1,"col":1,"ways":0},"note":"Cell (1, 1) is a shelf, so it stores 0."},{"at":{"cell":6},"vars":{"row":1,"col":2,"ways":2},"note":"Cell (1, 2) adds 3 predecessor entries 1+0+1 and stores 2."},{"at":{"cell":7},"vars":{"row":1,"col":3,"ways":4},"note":"Cell (1, 3) adds 3 predecessor entries 1+2+1 and stores 4."},{"at":{"cell":8},"vars":{"row":2,"col":0,"ways":1},"note":"Cell (2, 0) adds 1 predecessor entry 1 and stores 1."},{"at":{"cell":9},"vars":{"row":2,"col":1,"ways":2},"note":"Cell (2, 1) adds 3 predecessor entries 0+1+1 and stores 2."},{"at":{"cell":10},"vars":{"row":2,"col":2,"ways":4},"note":"Cell (2, 2) adds 3 predecessor entries 2+2+0 and stores 4."},{"at":{"cell":11},"vars":{"row":2,"col":3,"ways":10},"note":"Cell (2, 3) adds 3 predecessor entries 4+4+2 and stores 10. The answer is 10."}]}
```

#### Collecting The Largest Gain

The second floor stores a gain in every cell, and some gains are negative. The robot now moves only right or down, and the table stores the largest total gain of any route that ends exactly at the cell. The recurrence adds the cell's own gain to the larger of its two predecessor entries. The pointer `cell` again moves in reading order, with `gain` holding the stored value.

A negative cell still gets an entry, because a route may have to cross it. The last entry holds the best total.

```trace
{"cells":["(0,0)","(0,1)","(0,2)","(0,3)","(1,0)","(1,1)","(1,2)","(1,3)","(2,0)","(2,1)","(2,2)","(2,3)"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"row":0,"col":0,"gain":2},"note":"Cell (0, 0) is the start, so it stores its own gain 2."},{"at":{"cell":1},"vars":{"row":0,"col":1,"gain":1},"note":"Cell (0, 1) takes the larger predecessor 2 and adds its own gain -1, storing 1."},{"at":{"cell":2},"vars":{"row":0,"col":2,"gain":4},"note":"Cell (0, 2) takes the larger predecessor 1 and adds its own gain 3, storing 4."},{"at":{"cell":3},"vars":{"row":0,"col":3,"gain":4},"note":"Cell (0, 3) takes the larger predecessor 4 and adds its own gain 0, storing 4."},{"at":{"cell":4},"vars":{"row":1,"col":0,"gain":3},"note":"Cell (1, 0) takes the larger predecessor 2 and adds its own gain 1, storing 3."},{"at":{"cell":5},"vars":{"row":1,"col":1,"gain":7},"note":"Cell (1, 1) takes the larger predecessor 3 and adds its own gain 4, storing 7."},{"at":{"cell":6},"vars":{"row":1,"col":2,"gain":5},"note":"Cell (1, 2) takes the larger predecessor 7 and adds its own gain -2, storing 5."},{"at":{"cell":7},"vars":{"row":1,"col":3,"gain":7},"note":"Cell (1, 3) takes the larger predecessor 5 and adds its own gain 2, storing 7."},{"at":{"cell":8},"vars":{"row":2,"col":0,"gain":0},"note":"Cell (2, 0) takes the larger predecessor 3 and adds its own gain -3, storing 0."},{"at":{"cell":9},"vars":{"row":2,"col":1,"gain":9},"note":"Cell (2, 1) takes the larger predecessor 7 and adds its own gain 2, storing 9."},{"at":{"cell":10},"vars":{"row":2,"col":2,"gain":14},"note":"Cell (2, 2) takes the larger predecessor 9 and adds its own gain 5, storing 14."},{"at":{"cell":11},"vars":{"row":2,"col":3,"gain":13},"note":"Cell (2, 3) takes the larger predecessor 14 and adds its own gain -1, storing 13. The best total is 13."}]}
```

<!-- stage: code -->
### Route Count With A Table

The method returns the number of routes as a `long`, and it returns 0 when the start or the target is blocked. The loops follow reading order, so each predecessor is final before it is read.

```java
static long countRoutes(boolean[][] blocked) {
    int rows = blocked.length, cols = blocked[0].length;
    long[][] dp = new long[rows][cols];
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (blocked[r][c]) continue;
            if (r == 0 && c == 0) { dp[r][c] = 1; continue; }
            long ways = 0;
            if (r > 0) ways += dp[r - 1][c];
            if (c > 0) ways += dp[r][c - 1];
            if (r > 0 && c > 0) ways += dp[r - 1][c - 1];
            dp[r][c] = ways;
        }
    }
    return dp[rows - 1][cols - 1];
}
```

The three guards on `r` and `c` implement the border rule, and the `continue` on a blocked cell keeps its entry at 0. The method runs in O(R * C) time, because each cell does at most three additions. It uses O(R * C) memory for `dp`, not counting the input.

<!-- stage: applicability -->
### Recognizing Grid Problems

#### Reading The Cue

Use a grid table when the statement restricts the moves so that no route can return to a cell it left, and the question asks for a count, a best total or a yes-or-no about routes. Typical moves are right and down, with diagonals added in some statements. The same pattern covers a score grid, a floor plan with shelves and a map of terrain costs. Look for words such as paths, ways, minimum cost or maximum gain between two corners.

#### Checking The Invariant

The **invariant** is a statement that stays true throughout the loops. Here, when the loops reach `(r, c)`, every entry for an earlier cell in reading order equals its exact value, and every entry for the current and later cells is still 0. Test a blocked start, which must give 0. Test a grid with one row and a grid with one column, where the border rules are the only rules in play. Test a blocked target, and a shelf that cuts off every route.

#### Avoiding The False Friend

A **false friend** is a technique that looks right but fails on some inputs. Here the first false friend is a greedy walk that always steps to the neighbor with the best value. It ignores that a poor step now can lead to a rich region. The second is the closed formula for open grids, which counts choose-style combinations. It stops working as soon as a shelf or a different move set removes the symmetry. The third is the reading order itself: with moves that go up or left, filling row by row reads cells that are not ready.

<!-- stage: exercises -->
### Exercises

#### [Build] Routes With Three Moves (Author exercise)
<!-- id: dp-grid-three-moves -->

**Prerequisites.** The route table and the border rule of this lesson.

**Problem.** A grid has `rows` rows and `cols` columns, and `open[r][c]` is `true` when the cell can be entered. A route starts at `(0, 0)` and ends at `(rows - 1, cols - 1)`. Each step moves from `(r, c)` to `(r + 1, c)`, `(r, c + 1)` or `(r + 1, c + 1)`, and every cell on the route, including both ends, must be open. Return the number of distinct routes modulo 1000000007 as an `int`. Two routes are distinct when their cell sequences differ.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= rows, cols <= 300`.
- **Cells** are `true` for open and `false` for blocked.
- **Result** is reduced modulo 1000000007 and lies in `0..1000000006`.
- **Mutation** is not allowed, because `open` stays unchanged.

**Example 1.** Input `open = [[true,true,true],[true,true,true]]`, output `5`.

**Example 2.** Input `open = [[true,true,true],[true,false,true],[true,true,true]]`, output `4`.

**Hint.** Which cells can precede cell `(1, 1)` in the first example, and what value does each hold when the loop reaches it?

**Changed decision.** The table adds a third predecessor, and every sum is reduced modulo 1000000007. The reduction keeps each entry below the modulus, so the sum of three entries fits in a `long`.

#### [Vary] Maximum Gain Path (Author exercise)
<!-- id: dp-grid-max-gain -->

**Prerequisites.** The exercise above.

**Problem.** An `int[][]` named `gain` has `rows` rows and `cols` columns. A route starts at `(0, 0)`, ends at `(rows - 1, cols - 1)`, and each step moves one cell right or one cell down. The total of a route is the sum of `gain` over every cell on it, both ends included. Return the largest total over all routes as an `int`.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= rows, cols <= 200`.
- **Gain** satisfies `-1000 <= gain[r][c] <= 1000`, so negative cells are allowed.
- **Result** fits in an `int`.
- **Mutation** is not allowed, because `gain` stays unchanged.

**Example 1.** Input `gain = [[2,-1,3],[1,4,-2],[-3,2,5]]`, output `14`.

**Example 2.** Input `gain = [[-5,-2],[-7,-9]]`, output `-16`.

**Hint.** In the second example every cell is negative. What would go wrong if the table started from 0 for cells that are not yet filled?

**Changed decision.** The state now stores a total, and the combination is the larger predecessor plus the cell's own gain. A missing predecessor must not act as 0, because a total of 0 can beat a real negative total.

#### [Boundary] First Row And Column (Author exercise)
<!-- id: dp-grid-border-counts -->

**Prerequisites.** The two exercises above.

**Problem.** A grid has `rows` rows and `cols` columns, and `blocked[r][c]` is `true` for a shelf. A step moves one cell right or one cell down. Let `ways(r, c)` be the number of routes from `(0, 0)` to `(r, c)` through cells that are not blocked, with 0 when `(r, c)` is blocked. Return a `long[]` that lists `ways(0, 0), ways(0, 1), ..., ways(0, cols - 1)` followed by `ways(1, 0), ways(2, 0), ..., ways(rows - 1, 0)`.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= rows, cols <= 60`.
- **Result** has length `rows + cols - 1`.
- **Start** may be blocked, and then every entry is 0.
- **Mutation** is not allowed, because `blocked` stays unchanged.

**Example 1.** Input `blocked = [[false,false,true,false],[false,false,false,false]]`, output `[1,1,0,0,1]`.

**Example 2.** Input `blocked = [[false],[true],[false]]`, output `[1,0,0]`.

**Hint.** Once a cell in row 0 is blocked, what do the cells to its right see as their only predecessor?

**Changed decision.** The method fills only the first row and the first column, each from its single predecessor direction. A blocked cell breaks the chain, and every later border cell in that line stays at 0.

#### [Recognize] Unique Paths With Obstacles (LeetCode 63)
<!-- id: dp-grid-blocked-cells -->

**Prerequisites.** All three exercises above.

**Problem.** An `m` by `n` integer matrix `obstacleGrid` has 1 in a cell that holds an obstacle and 0 in an empty cell. A robot starts at the top-left cell and moves one cell right or one cell down per step. It may enter only empty cells. Return the number of distinct routes to the bottom-right cell as an `int`. Return 0 when the start or the target holds an obstacle.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= m, n <= 100`.
- **Cell** values are 0 or 1.
- **Result** fits in an `int` for every input.
- **Mutation** is not allowed, because `obstacleGrid` stays unchanged.

**Example 1.** Input `obstacleGrid = [[0,0,0,0],[0,1,0,0],[0,0,0,0]]`, output `4`.

**Example 2.** Input `obstacleGrid = [[0,1],[0,0]]`, output `1`.

**Hint.** The grid has two move types, not three. Which predecessor of the previous exercises disappears, and what does an obstacle store?

**Changed decision.** The state is the same as in the first exercise with the diagonal move removed. An obstacle stores 0 so later cells receive nothing from it. The result fits in an `int` by the guarantee, so a `long` table is optional.
