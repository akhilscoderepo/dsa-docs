<!-- lesson-kind: standard -->
<!-- lesson-id: direction-state -->
## Moving With A Direction

<!-- stage: context -->
### A Fill Routine That Writes Twice

A print tool numbers the cells of a square sheet from 1 up to `n * n`, starting at the top-left cell and winding clockwise toward the center. The routine uses four loops, one for each side of the sheet, and it passes every test on square sheets. A new product ships on a sheet with 3 rows and 4 columns. The same routine writes into some cells twice and leaves the numbering corrupted, with no error message.

The routine was never wrong about squares. It stored the geometry of a square in four separate loops. This lesson asks what small piece of state describes the next step of a winding walk, so that one loop handles any rectangle and any starting corner.

<!-- stage: naive -->
### Four Loops For Four Sides

The routine keeps four bounds for the unfilled part of the sheet. It fills the top row, then the right column, then the bottom row, then the left column, and it moves each bound inward after its side.

```java
static int[][] fillSquare(int n) {
    int[][] g = new int[n][n];
    int top = 0, bottom = n - 1, left = 0, right = n - 1, v = 1;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; c++) g[top][c] = v++;
        top++;
        for (int r = top; r <= bottom; r++) g[r][right] = v++;
        right--;
        for (int c = right; c >= left; c--) g[bottom][c] = v++;
        bottom--;
        for (int r = bottom; r >= top; r--) g[r][left] = v++;
        left++;
    }
    return g;
}
```

For `n = 3` this writes 1 through 9 correctly. The code assumes that the unfilled part is still non-empty after each side, and a square sheet keeps that assumption true.

<!-- stage: bottleneck -->
### Why Each Change Touches Four Loops

```predict
The routine costs O(n^2) on a square sheet. Why does it still break on a 3 by 4 sheet, and what would a counterclockwise version have to change?

On a 3 by 4 sheet, the loops for the bottom row and the left column run after the top and right sides have already consumed the last remaining row or column. They write cells a second time. A counterclockwise version needs all four loops rewritten in a new order with new bounds.
```

The running time is not the problem. Every cell is written once, so the cost is O(R * C) for a sheet with R rows and C columns. The problem is that the movement rule is spread over four loop bodies and four bound updates. Each loop assumes what the earlier loops left behind. A new shape, a new starting corner or a reversed order changes every one of those assumptions. The movement itself follows a simple rule: keep going the same way until the next cell is unusable, then change the way.

<!-- stage: insight -->
### One Cursor And One Direction

The winding walk has a short description. A single **cursor** stands on one cell. It moves one cell at a time in its current **direction**. When the next cell lies outside the sheet or already holds a number, the cursor makes a **turn** to the next direction in clockwise order and then moves.

#### The Direction Table

Clockwise order from the top-left corner is right, down, left, up. A table stores one row change and one column change for each direction. The table `dr = {0, 1, 0, -1}` and `dc = {1, 0, -1, 0}` encodes the four moves. A direction index `d` selects one entry from each. A turn is the update `d = (d + 1) % 4`, so the fourth turn returns to the first direction.

#### The State That Predicts The Next Step

The triple `(row, col, d)` together with the set of filled cells fixes the next step. The loop does not need to know which side of the sheet it is on. For each value from 1 to `R * C`, it writes the value at the cursor. It then computes the next cell. If that cell is outside the sheet or already filled, it turns first. Then it moves.

#### Why One Loop Is Enough

A filled cell and an outside cell are both reasons to turn, and the same test covers both. In a spiral, a cell is blocked only by the sheet edge or by the part already filled. The test therefore replaces the four bound variables. A rectangle, a different corner or a reversed order changes only the table or the starting triple.

<!-- names: cursor, direction, turn -->

<!-- stage: variables -->
### What The Loop Remembers

The loop keeps four pieces of state, and each changes at a known moment.

- **r and c** hold the cursor position and change on every step.
- **d** holds the direction index, from 0 for right to 3 for up, and changes only on a turn.
- **value** holds the next number to write, from 1 up to `R * C`, and grows after each write.
- **grid** holds the numbers already written, and a cell value of 0 means the cell is empty.

<!-- stage: trace -->
### Filling Two Sheets Clockwise

#### A Three By Three Sheet

Fill a 3 by 3 sheet. The cursor starts at row 0, column 0, with direction right. In the trace below, the pointer `cur` marks the cell index in row-major order, so cell 4 is the center. Values 1, 2 and 3 fill the top row. After the value 3, the next cell is outside the sheet, so the cursor turns down. The values 4 and 5 fill the right column. Then it turns left for 6 and 7, turns up for 8 and turns right for 9.

#### A Two By Three Sheet

Now fill a 2 by 3 sheet. The top row takes 1, 2 and 3. The cursor turns down and writes 4 in the last column of row 1. It turns left and writes 5 and 6 along the bottom row. The sheet is full, so the loop stops without any further turn.

#### Stepping Through Both Sheets

```trace
{"cells":[0,1,2,3,4,5,6,7,8],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"direction":"right","value":1,"filled":"[[1,0,0],[0,0,0],[0,0,0]]"},"note":"Write 1 at row 0, column 0. The next cell is free, so the cursor keeps moving right."},{"at":{"cur":1},"vars":{"direction":"right","value":2,"filled":"[[1,2,0],[0,0,0],[0,0,0]]"},"note":"Write 2 at row 0, column 1. The next cell is free, so the cursor keeps moving right."},{"at":{"cur":2},"vars":{"direction":"down","value":3,"filled":"[[1,2,3],[0,0,0],[0,0,0]]"},"note":"Write 3 at row 0, column 2. The next cell is outside the sheet, so the cursor turns to down."},{"at":{"cur":5},"vars":{"direction":"down","value":4,"filled":"[[1,2,3],[0,0,4],[0,0,0]]"},"note":"Write 4 at row 1, column 2. The next cell is free, so the cursor keeps moving down."},{"at":{"cur":8},"vars":{"direction":"left","value":5,"filled":"[[1,2,3],[0,0,4],[0,0,5]]"},"note":"Write 5 at row 2, column 2. The next cell is outside the sheet, so the cursor turns to left."},{"at":{"cur":7},"vars":{"direction":"left","value":6,"filled":"[[1,2,3],[0,0,4],[0,6,5]]"},"note":"Write 6 at row 2, column 1. The next cell is free, so the cursor keeps moving left."},{"at":{"cur":6},"vars":{"direction":"up","value":7,"filled":"[[1,2,3],[0,0,4],[7,6,5]]"},"note":"Write 7 at row 2, column 0. The next cell is outside the sheet, so the cursor turns to up."},{"at":{"cur":3},"vars":{"direction":"right","value":8,"filled":"[[1,2,3],[8,0,4],[7,6,5]]"},"note":"Write 8 at row 1, column 0. The next cell is already filled, so the cursor turns to right."},{"at":{"cur":4},"vars":{"direction":"right","value":9,"filled":"[[1,2,3],[8,9,4],[7,6,5]]"},"note":"Write 9 at row 1, column 1. The sheet is full, so the loop stops."}]}
```

```trace
{"cells":[0,1,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"direction":"right","value":1,"filled":"[[1,0,0],[0,0,0]]"},"note":"Write 1 at row 0, column 0. The next cell is free, so the cursor keeps moving right."},{"at":{"cur":1},"vars":{"direction":"right","value":2,"filled":"[[1,2,0],[0,0,0]]"},"note":"Write 2 at row 0, column 1. The next cell is free, so the cursor keeps moving right."},{"at":{"cur":2},"vars":{"direction":"down","value":3,"filled":"[[1,2,3],[0,0,0]]"},"note":"Write 3 at row 0, column 2. The next cell is outside the sheet, so the cursor turns to down."},{"at":{"cur":5},"vars":{"direction":"left","value":4,"filled":"[[1,2,3],[0,0,4]]"},"note":"Write 4 at row 1, column 2. The next cell is outside the sheet, so the cursor turns to left."},{"at":{"cur":4},"vars":{"direction":"left","value":5,"filled":"[[1,2,3],[0,5,4]]"},"note":"Write 5 at row 1, column 1. The next cell is free, so the cursor keeps moving left."},{"at":{"cur":3},"vars":{"direction":"left","value":6,"filled":"[[1,2,3],[6,5,4]]"},"note":"Write 6 at row 1, column 0. The sheet is full, so the loop stops."}]}
```

<!-- stage: code -->
### A Single Loop For Any Rectangle

#### The Fill Loop

```java
private static final int[] DR = {0, 1, 0, -1};
private static final int[] DC = {1, 0, -1, 0};

static int[][] fillClockwise(int rows, int cols) {
    int[][] g = new int[rows][cols];
    int r = 0, c = 0, d = 0;
    for (int v = 1; v <= rows * cols; v++) {
        g[r][c] = v;
        int nr = r + DR[d], nc = c + DC[d];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || g[nr][nc] != 0) {
            d = (d + 1) % 4;
            nr = r + DR[d];
            nc = c + DC[d];
        }
        r = nr;
        c = nc;
    }
    return g;
}
```

#### Cost And The Last Step

The loop runs `rows * cols` times and does constant work per step, so it costs O(R * C) time and O(1) extra space beyond the output. After the final write, the code still computes a next cell, and that cell may be outside the sheet. The final assignment is harmless here, because the loop ends before it reads `g[r][c]` again. A version that wrote at the new cursor immediately would crash on the last turn.

<!-- stage: applicability -->
### When One Cursor Is The Right Model

#### Recognizing The Pattern

The pattern fits when one cursor moves by a small cyclic rule and changes course only when the next step is illegal. The invariant is that `(r, c, d)` and the filled cells fully determine the next step. A statement that says "wind", "spiral", "snake" or "bounce" often describes this pattern.

#### A False Friend Called Frontier Search

A search over a grid, such as a breadth-first search, also visits cells in some order. It differs in an important way. A search keeps many candidate cells waiting at once and picks among them. The direction model follows exactly one cursor, and the next cell is forced. If a problem lets the walker choose among several moves, a single direction value cannot describe the state, and the problem needs a search.

#### The Case Of A Single Cell

A `1 x 1` sheet writes once, and the first computed next cell is outside the sheet. The code above turns once after the write and then ends the loop, so the cursor index leaves the sheet but is never read. Count the turns in such a boundary case before relying on the final cursor position.

<!-- stage: exercises -->
### Exercises

#### [Build] Clockwise Walker (Author exercise)
<!-- id: mx-clockwise-walker -->

**Prerequisites.** The direction table and the turn rule from this lesson.

**Problem.** A walker stands at cell `(0, 0)` of an `R x C` grid and faces right. A step moves the walker one cell in the facing direction. If that cell is outside the grid, the walker first rotates clockwise by one quarter turn and then moves. Return the final cell `{row, col}` after exactly `steps` steps.

**Constraints.** The limits are:
- **Grid** satisfies `2 <= R, C <= 100`, so a legal move always exists after one rotation.
- **Steps** satisfy `0 <= steps <= 10^6`.
- **Answer** is an `int[]` of length 2.
- **Cells** are never marked, so the walker circles the border forever.

**Example 1.** Input `R = 2, C = 3, steps = 7`, output `[0,1]`.

**Example 2.** Input `R = 2, C = 2, steps = 4`, output `[0,0]`, because the walker returns to its start after four steps.

**Hint.** Which of the three state values changes only when the next cell is outside the grid?

**Changed decision.** Basic case: the walker records no filled cells, so only the grid edge triggers a turn.

#### [Vary] Spiral Matrix II (LeetCode 59)
<!-- id: mx-spiral-fill -->

**Prerequisites.** The clockwise walker exercise above.

**Problem.** Given a positive integer `n`, return an `n x n` matrix that holds the integers 1 through `n * n` in clockwise spiral order, starting at the top-left cell. The walker turns when the next cell is outside the matrix or already holds a number.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 20`.
- **Order** is clockwise from the top-left cell.
- **Answer** is a new `int[][]`, and the value 0 never appears in it.
- **Mutation** is local, because the method builds the matrix itself.

**Example 1.** Input `n = 3`, output `[[1,2,3],[8,9,4],[7,6,5]]`.

**Example 2.** Input `n = 4`, output `[[1,2,3,4],[12,13,14,5],[11,16,15,6],[10,9,8,7]]`.

**Hint.** Which cells make the walker turn after the top row of the matrix is full?

**Changed decision.** Filled cells now trigger turns together with the edge, so the grid doubles as the record of visited cells.

#### [Boundary] Single Cell (Author exercise)
<!-- id: mx-single-cell -->

**Prerequisites.** The spiral fill exercise above.

**Problem.** Fill an `R x C` grid with the integers 1 through `R * C` in clockwise spiral order, as in the previous exercise but for any rectangle. A turn is counted each time the facing direction changes before a write, and the walker stops right after the last write without testing the next cell. Return the number of turns.

**Constraints.** The limits are:
- **Size** satisfies `1 <= R, C <= 100`.
- **Order** is clockwise, starting at the top-left cell facing right.
- **Answer** is a single `int`.
- **Stop rule** means no turn is counted after the last write.

**Example 1.** Input `R = 1, C = 1`, output 0, because the one cell is written and the walker never moves.

**Example 2.** Input `R = 3, C = 3`, output 4.

**Hint.** Does the walker test the next cell after writing the value `R * C`?

**Changed decision.** The stop rule decides whether a final turn is counted, so a boundary case exposes an off-by-one turn.

#### [Recognize] Spiral Matrix III (LeetCode 885)
<!-- id: mx-spiral-outward -->

**Prerequisites.** All three exercises above.

**Problem.** An `R x C` grid has a walker at `(rStart, cStart)` facing right. The walker follows an outward clockwise spiral on the infinite plane: it walks 1 cell right, 1 down, 2 left, 2 up, 3 right, 3 down, and so on, with each length used twice. The walker may leave the grid and return. Return the coordinates of the grid cells in the order the walker first stands on them, until all `R * C` cells are listed.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= R, C <= 20`.
- **Start** satisfies `0 <= rStart < R` and `0 <= cStart < C`.
- **Answer** is a list of `R * C` pairs `[row, col]`.
- **Outside cells** are walked but never recorded.

**Example 1.** Input `R = 1, C = 4, rStart = 0, cStart = 1`, output `[[0,1],[0,2],[0,0],[0,3]]`.

**Example 2.** Input `R = 2, C = 2, rStart = 1, cStart = 0`, output `[[1,0],[1,1],[0,0],[0,1]]`.

**Hint.** The path is fixed in advance by the segment lengths 1, 1, 2, 2, 3, 3. Which values change after every second segment?

**Changed decision.** The cursor is allowed outside the grid, so only legality of the recorded cell, and not legality of the move, is tested.
