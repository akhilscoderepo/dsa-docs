<!-- lesson-kind: standard -->
<!-- lesson-id: marker-state -->
## Marker State

<!-- stage: context -->
### Recall Stickers In A Warehouse

A warehouse stores boxes in a grid of bins, and a few boxes carry a red recall sticker. When a box is recalled, every bin on the same shelf row and in the same aisle column must be emptied, because the products were stocked together. The manager walks the grid with a cart and a clipboard, and the bins she empties become empty, which looks the same as a bin that was empty to begin with.

Her first plan is to empty the shelf row and aisle column as soon as she sees a red sticker. Halfway through the grid she finds that her own work has fooled her. A bin she emptied a minute ago looks empty, and she cannot tell whether it was a recalled bin or one she cleared, so she keeps spreading the emptiness further than the recall requires. Evidence she still needed was erased by her own cleaning.

<!-- stage: naive -->
### Keep A Pristine Copy To Consult

The straightforward repair is to photograph the grid first and consult the photograph while emptying the real one.

```java
static void setZeroesWithCopy(int[][] grid) {
    int rows = grid.length, cols = grid[0].length;
    int[][] original = new int[rows][];
    for (int r = 0; r < rows; r++) original[r] = grid[r].clone();
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (original[r][c] == 0) {
                for (int k = 0; k < cols; k++) grid[r][k] = 0;
                for (int k = 0; k < rows; k++) grid[k][c] = 0;
            }
        }
    }
}
```

It is correct, because the decisions are made from the untouched copy. For `[[1, 0, 3], [4, 5, 6]]` it turns the first row and the second column to zero and leaves `[[0, 0, 0], [4, 0, 6]]`.

<!-- stage: bottleneck -->
### A Whole Copy And Repeated Clearing

The copy costs O(rows * cols) extra space, which for a large grid doubles the memory. The clearing is also wasteful, since a zero in a row that is already cleared triggers the same clearing again. With many zeros each one clears a row and a column, so the time can grow to O(rows * cols * (rows + cols)). A grid with half its cells zero makes the clearing loops run about once per zero cell.

Neither cost is needed. The decision for every cell depends on only two facts: whether its row contains a zero and whether its column contains a zero. That is `rows + cols` facts in total, which is far smaller than a copy of the grid. If those facts are written down before anything is cleared, the grid can be cleared in one pass with no further need for the original values.

<!-- stage: insight -->
### Record First, Then Change

Split the work into two passes. The **observation pass** reads the grid and writes nothing to it. It records, in a **marker array** for rows and one for columns, which rows and which columns contain a zero. The second pass then reads only the markers and writes the grid. Because the observation finishes before any write, no write can disturb what the observation saw.

The markers take O(rows + cols) space. They can be reduced to O(1) extra space by borrowing the first row and first column of the grid as the marker storage. Cell `(r, 0)` then stands for row `r` and cell `(0, c)` for column `c`. This borrowing destroys the original contents of the first row and first column, so two flags are kept, one asking whether the first row originally held a zero and one for the first column, and the first row and column are cleared last.

<!-- names: observation pass, marker array, state encoding -->

The same separation of reading from writing appears when the information needed later is not a yes or no. A cell in a simulation may need both its old value and its new one, because its neighbors still have to read the old one. A **state encoding** packs two values into one number: if the old state is a single bit, store `old + 2 * new`. The old state is the low bit, the new state is the next bit, and a final sweep shifts every cell right by one to keep only the new state.

The invariant is that every read of old information happens either before the first write, or through the part of the cell that writes never change. The marker pass satisfies it by finishing first. The encoding satisfies it by writing only to the second bit while reads use the first.

<!-- stage: variables -->
### Markers, Flags And Two Phases

The row markers `rowHit[r]` and column markers `colHit[c]` are booleans, false at the start. The observation pass sets `rowHit[r]` and `colHit[c]` whenever it sees a zero at `(r, c)`. In the constant-space version the marker cells are `grid[r][0]` and `grid[0][c]`, and the two extra flags `firstRowZero` and `firstColZero` remember what those cells held originally. For the encoding, a cell holds a number from 0 to 3 whose low bit is the old state and whose next bit is the new state. The order of the phases is the invariant: observe, then write.

<!-- stage: trace -->
### Two Passes Over A Small Grid

Take `[[1, 0, 3], [4, 5, 6]]`. The observation pass walks all six cells and writes nothing. Cell `(0, 0)` holds 1 and cell `(0, 1)` holds 0, so row 0 and column 1 are marked. The remaining cells hold no zero. The markers say row 0 and column 1.

The second pass walks the six cells again, and clears every cell whose row or column is marked. Cells `(0, 0)`, `(0, 1)` and `(0, 2)` are in row 0, so they become 0, and cell `(1, 1)` is in column 1, so it becomes 0. Cells `(1, 0)` and `(1, 2)` are untouched. The result is `[[0, 0, 0], [4, 0, 6]]`. The step to study is the second pass at `(0, 0)`, because the grid there was cleared although it never held a zero, and the decision came from the markers alone.

The second picture is the encoding on a two by two board `[[1, 1], [1, 0]]`, where one generation of Game of Life is computed in place. Each cell's neighbors are read through the low bit, and the new state is stored in the next bit.

```trace
{"cells":[1,0,3,4,5,6],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"phase":"observe","rowHit":"[0,0]","colHit":"[0,0,0]"},"note":"Observe (0, 0) = 1. No zero here; nothing is written."},{"at":{"cell":1},"vars":{"phase":"observe","rowHit":"[1,0]","colHit":"[0,1,0]"},"note":"Observe (0, 1) = 0. A zero, so mark row 0 and column 1."},{"at":{"cell":2},"vars":{"phase":"observe","rowHit":"[1,0]","colHit":"[0,1,0]"},"note":"Observe (0, 2) = 3. No zero here; nothing is written."},{"at":{"cell":3},"vars":{"phase":"observe","rowHit":"[1,0]","colHit":"[0,1,0]"},"note":"Observe (1, 0) = 4. No zero here; nothing is written."},{"at":{"cell":4},"vars":{"phase":"observe","rowHit":"[1,0]","colHit":"[0,1,0]"},"note":"Observe (1, 1) = 5. No zero here; nothing is written."},{"at":{"cell":5},"vars":{"phase":"observe","rowHit":"[1,0]","colHit":"[0,1,0]"},"note":"Observe (1, 2) = 6. No zero here; nothing is written."},{"at":{"cell":0},"vars":{"phase":"clear","grid":"[[0,0,3],[4,5,6]]"},"note":"Clear (0, 0), because its row or column is marked."},{"at":{"cell":1},"vars":{"phase":"clear","grid":"[[0,0,3],[4,5,6]]"},"note":"Clear (0, 1), because its row or column is marked."},{"at":{"cell":2},"vars":{"phase":"clear","grid":"[[0,0,0],[4,5,6]]"},"note":"Clear (0, 2), because its row or column is marked."},{"at":{"cell":3},"vars":{"phase":"clear","grid":"[[0,0,0],[4,5,6]]"},"note":"Keep (1, 0); neither its row nor its column is marked."},{"at":{"cell":4},"vars":{"phase":"clear","grid":"[[0,0,0],[4,0,6]]"},"note":"Clear (1, 1), because its row or column is marked."},{"at":{"cell":5},"vars":{"phase":"clear","grid":"[[0,0,0],[4,0,6]]"},"note":"Keep (1, 2); neither its row nor its column is marked."}]}
```

```trace
{"cells":[1,1,1,0],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"phase":"encode","live":2,"grid":"[[3,1],[1,0]]"},"note":"Cell (0, 0) is live with 2 live neighbors read through the low bit. The new state is live, so the cell now holds 3."},{"at":{"cell":1},"vars":{"phase":"encode","live":2,"grid":"[[3,3],[1,0]]"},"note":"Cell (0, 1) is live with 2 live neighbors read through the low bit. The new state is live, so the cell now holds 3."},{"at":{"cell":2},"vars":{"phase":"encode","live":2,"grid":"[[3,3],[3,0]]"},"note":"Cell (1, 0) is live with 2 live neighbors read through the low bit. The new state is live, so the cell now holds 3."},{"at":{"cell":3},"vars":{"phase":"encode","live":3,"grid":"[[3,3],[3,2]]"},"note":"Cell (1, 1) is dead with 3 live neighbors read through the low bit. The new state is live, so the cell now holds 2."},{"at":{"cell":0},"vars":{"phase":"finish","grid":"[[1,3],[3,2]]"},"note":"Shift cell (0, 0) right by one, keeping only the new state 1."},{"at":{"cell":1},"vars":{"phase":"finish","grid":"[[1,1],[3,2]]"},"note":"Shift cell (0, 1) right by one, keeping only the new state 1."},{"at":{"cell":2},"vars":{"phase":"finish","grid":"[[1,1],[1,2]]"},"note":"Shift cell (1, 0) right by one, keeping only the new state 1."},{"at":{"cell":3},"vars":{"phase":"finish","grid":"[[1,1],[1,1]]"},"note":"Shift cell (1, 1) right by one, keeping only the new state 1."}]}
```

<!-- stage: code -->
### Observe, Then Clear, Or Encode

```java
static void clearBadRows(int[][] grid) {                // a row is bad if it contains -1; clearing writes zeros
    boolean[] bad = new boolean[grid.length];
    for (int r = 0; r < grid.length; r++)
        for (int v : grid[r]) if (v == -1) bad[r] = true;
    for (int r = 0; r < grid.length; r++)
        if (bad[r]) java.util.Arrays.fill(grid[r], 0);
}

static void setZeroes(int[][] grid) {
    int rows = grid.length, cols = grid[0].length;
    boolean[] rowHit = new boolean[rows], colHit = new boolean[cols];
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) if (grid[r][c] == 0) { rowHit[r] = true; colHit[c] = true; }
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) if (rowHit[r] || colHit[c]) grid[r][c] = 0;
}

static void gameOfLife(int[][] board) {
    int rows = board.length, cols = board[0].length;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            int live = 0;
            for (int dr = -1; dr <= 1; dr++)
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = r + dr, nc = c + dc;
                    if ((dr != 0 || dc != 0) && nr >= 0 && nr < rows && nc >= 0 && nc < cols) live += board[nr][nc] & 1;
                }
            boolean alive = (board[r][c] & 1) == 1;
            boolean next = alive ? (live == 2 || live == 3) : live == 3;
            if (next) board[r][c] |= 2;
        }
    for (int[] row : board) for (int c = 0; c < cols; c++) row[c] >>= 1;
}
```

Each method makes a constant number of passes over the grid, so the time is O(rows * cols). The marker versions use O(rows + cols) extra space, and the encoded Game of Life uses O(1) extra space, since the new state lives inside the old cells. In the neighbor loop, the read `board[nr][nc] & 1` takes only the old state, so a neighbor that has already received its new bit does not mislead the count. The first method shows the two-pass shape on its simplest case, and the second shows why the pass order matters.

<!-- stage: applicability -->
### When Writes Would Destroy Evidence

Use marker state when a later mutation depends on facts that earlier mutations could erase, and the facts can be summarized compactly: a bit per row and per column, or a second bit in each cell. The invariant is that every decision reads information that no write has yet changed. State that explicitly before choosing the in-place version.

The false friend is a hash set of row and column numbers, which also works and costs the same order of memory, but needs a collection library and general set semantics that a later chapter teaches. The marker array is simply a set with a dense integer domain. Another false friend is immediate clearing: it looks like one tidy pass and gives wrong answers whenever the written value looks like the value being searched for.

In Java, allocate boolean arrays of the right sizes and remember that they start false. In the constant-space version, process the interior first and clear the first row and column last, with their flags, or the markers would be destroyed before use. Bit operations on `int` cells need care with signs: encode only non-negative states, and use `& 1` and `>> 1` to read and finish. If cell values can already be negative or larger than a bit, use a separate array or a wider encoding.

<!-- stage: exercises -->
### Exercises

#### [Build] Mark Bad Rows (Author exercise)
<!-- id: mx-mark-bad-rows -->

**Prerequisites.** The neighbor-enumeration lesson; boolean arrays.

**Problem.** A row is bad if it contains the value -1. First record which rows are bad, then in a second pass overwrite every cell of each bad row with 0. Leave the other rows unchanged.

**Constraints.** 1 <= rows <= 100, 1 <= cols <= 100, and -1 <= cell <= 100. Use a marker array of length `rows`.

**Example 1.** Input `grid = [[4, 5], [-1, 6], [7, 8]]`, output `[[4, 5], [0, 0], [7, 8]]`.

**Example 2.** Input `grid = [[1, -1, 2], [3, 4, -1]]`, output `[[0, 0, 0], [0, 0, 0]]`.

**Hint.** What would happen if you cleared a row during the scan? For rows alone the answer is harmless, but what would it do to a column question later?

**Changed decision.** First rung: observation and writing are separated into two passes joined by a marker array.

#### [Vary] Set Matrix Zeroes (LeetCode 73)
<!-- id: mx-set-matrix-zeroes -->

**Prerequisites.** The mark-bad-rows exercise above.

**Problem.** Given an integer matrix, if a cell is 0, set its entire row and column to 0, in place. All decisions must use the original zeros only.

**Constraints.** 1 <= rows, cols <= 200 and -1000 <= cell <= 1000. Use two boolean marker arrays, one for rows and one for columns.

**Example 1.** Input `matrix = [[3, 4, 5], [6, 0, 7], [8, 9, 0]]`, output `[[3, 0, 0], [0, 0, 0], [0, 0, 0]]`.

**Example 2.** Input `matrix = [[1, 2], [3, 4]]`, output `[[1, 2], [3, 4]]`, since no zero exists.

**Hint.** Which two facts decide whether a cell must be cleared? Why must both be recorded before any cell is changed?

**Changed decision.** The marker array is now needed twice, for rows and for columns, and immediate clearing would be wrong.

#### [Boundary] Set Matrix Zeroes In Constant Space (LeetCode 73)
<!-- id: mx-set-zeroes-constant -->

**Prerequisites.** The two exercises above.

**Problem.** Solve Set Matrix Zeroes again with O(1) extra space by using the first row and first column as the markers. Keep two flags for whether the first row and first column originally held a zero, and clear them last.

**Constraints.** 1 <= rows, cols <= 200 and -1000 <= cell <= 1000. Only a constant number of extra variables is allowed.

**Example 1.** Input `matrix = [[1, 2], [0, 4]]`, output `[[0, 2], [0, 0]]`, where the zero sits in the first column.

**Example 2.** Input `matrix = [[5, 0], [6, 7]]`, output `[[0, 0], [6, 0]]`, where the zero sits in the first row.

**Hint.** What does a zero in the first row mean once that row also stores markers? How do you tell an original zero from a marker you wrote?

**Changed decision.** The marker storage is borrowed from the grid itself, which creates a conflict that the two flags and the clearing order resolve.

#### [Recognize] Game of Life (LeetCode 289)
<!-- id: mx-game-of-life -->

**Prerequisites.** All three exercises above, and the neighbor-counts exercise from the previous lesson.

**Problem.** A board holds 0 for dead and 1 for live cells. In one generation a live cell with fewer than two or more than three live neighbors dies, a live cell with two or three live neighbors lives, and a dead cell with exactly three live neighbors becomes live. Compute the next generation in place, with no second board.

**Constraints.** 1 <= rows, cols <= 25 and each cell is 0 or 1. Neighbors include the eight surrounding cells, and every neighbor read must see the old generation.

**Example 1.** Input `board = [[1, 1], [1, 0]]`, output `[[1, 1], [1, 1]]`.

**Example 2.** Input `board = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]`, output `[[0, 0, 0], [1, 1, 1], [0, 0, 0]]`.

**Hint.** Where can you store a cell's new state so that its neighbors still read the old one? What final pass leaves only the new states?

**Changed decision.** The marker is no longer a row or column flag but a second bit inside each cell, set by writes and ignored by reads.
