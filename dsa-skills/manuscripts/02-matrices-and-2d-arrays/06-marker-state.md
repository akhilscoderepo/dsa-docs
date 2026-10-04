<!-- lesson-kind: standard -->
<!-- lesson-id: marker-state -->
## Marking Rows Before Clearing Them

<!-- stage: context -->
### A Cleanup Job That Wipes Too Much

A data table is stored as an `int[][]`, and a cleanup job must set a whole row and a whole column to `0` whenever one cell holds `0`. A developer writes the obvious loop. The loop scans the cells, and when it finds a `0` at `(r, c)`, it writes zeros across row `r` and column `c` at once. On `{{0, 2, 3}, {4, 5, 6}, {7, 8, 9}}` the scan reaches column 1 of row 0, finds a zero that the job itself just wrote, and clears column 1 as well. The result loses the values 5 and 8, although the input had a single zero.

The bug comes from reading cells that the loop already changed. This lesson asks how a loop can remember what it must clear without destroying the evidence it still needs.

<!-- stage: naive -->
### Reading From A Copy

The safe method scans a copy of the matrix, and writes zeros only into the original. The copy never changes, so every read sees the input as it was given.

```java
static void setZeroesWithCopy(int[][] m) {
    int rows = m.length, cols = m[0].length;
    int[][] copy = new int[rows][];
    for (int r = 0; r < rows; r++) {
        copy[r] = m[r].clone();
    }
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (copy[r][c] == 0) {
                for (int k = 0; k < cols; k++) m[r][k] = 0;
                for (int k = 0; k < rows; k++) m[k][c] = 0;
            }
        }
    }
}
```

The method is correct on every rectangular matrix. On `{{0, 2, 3}, {4, 5, 6}, {7, 8, 9}}` it returns `{{0, 0, 0}, {0, 5, 6}, {0, 8, 9}}`.

<!-- stage: bottleneck -->
### The Copy And The Repeated Clearing

```predict
The copy method stores a full second matrix. A matrix has `rows` rows and `cols` columns. How many bits of information does the job really need to remember, and why is that far less than the whole matrix?

Each row needs one yes-or-no fact, and so does each column. The job has to remember `rows + cols` facts, which is far less than `rows * cols` values, because only the question "is this row or column cleared" matters later.
```

The copy costs O(rows * cols) extra space, which equals the input. The clearing loops add a second cost. Every zero triggers a pass over its whole row and its whole column, so a matrix full of zeros does O(rows * cols * (rows + cols)) writes. The job needs far less. Each row has one fact to remember, and each column has one fact to remember. A fact is either "this line holds a zero" or "it does not". The next section stores exactly those facts and clears each line once.

<!-- stage: insight -->
### Record First, Then Change

The fix separates reading from writing. The loop first records which lines to clear, and only afterwards changes any cell.

#### Two Passes With Separate Jobs

A **marker** is one stored fact about a row or a column, here "this line must be cleared". The **observation pass** reads every cell and sets markers. It writes nothing into the matrix. The **update pass** reads the markers and writes zeros. It never looks for zeros in the matrix, so zeros written by the update pass cannot start a second round of clearing. The invariant is that the observation pass sees the input exactly as given, because no write happens before it finishes.

#### Markers Kept In The Matrix Itself

Two arrays, `boolean[rows]` and `boolean[cols]`, hold the markers in O(rows + cols) space. The matrix can also carry them. The cell `(0, c)` can mark column `c`, and the cell `(r, 0)` can mark row `r`. A marker written into a cell of the **first row** or the first column overwrites a value the matrix may need. Two extra booleans solve this, because they record whether the first row and the first column held a zero in the input. The update pass handles those two lines last, so their markers stay readable until every other cell is done. This brings the extra space to O(1).

<!-- names: marker, observation pass, update pass, first row -->

<!-- stage: variables -->
### The Marker Arrays And Their Writers

The method keeps a small amount of state, and each piece changes at one point.

- **rows and cols** hold the two matrix dimensions, and they never change.
- **rowMark[r]** holds `true` when row `r` contains a zero in the input, and only the observation pass sets it.
- **colMark[c]** holds `true` when column `c` contains a zero in the input, and only the observation pass sets it.
- **r and c** hold the row and column indexes of the cell being read or written.

<!-- stage: trace -->
### Clearing A Three By Four Matrix

#### The Observation Pass

The first example has the rows `[1, 2, 3, 4]`, `[5, 0, 7, 8]` and `[9, 10, 0, 12]`. The cells are numbered by row-major index, so the cell `(1, 1)` is cell 5 and the cell `(2, 2)` is cell 10. The pointer `p` marks the cell being read. The scan changes no value. It finds zeros at cell 5 and cell 10. Those two finds mark rows 1 and 2 and columns 1 and 2.

#### The Update Pass

The update pass then clears each marked row and each marked column. The pointers `a` and `b` mark the first and last cell of the line being cleared. A cell that lies in a marked row and a marked column is cleared twice, which is harmless because a second write of zero changes nothing. The final matrix is `[1, 0, 0, 4]`, `[0, 0, 0, 0]`, `[0, 0, 0, 0]`.

#### Stepping Through Both Passes

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11],"pointers":["p"],"steps":[{"at":{"p":-1},"vars":{"marks":"rows 000 cols 0000"},"note":"Start of the observation pass. No marker is set and no cell has been read."},{"at":{"p":5},"vars":{"marks":"rows 010 cols 0100"},"note":"The cell in row 1, column 1 holds zero. The pass sets the marker of row 1 and the marker of column 1 and changes no cell."},{"at":{"p":10},"vars":{"marks":"rows 011 cols 0110"},"note":"The cell in row 2, column 2 holds zero. The pass sets the marker of row 2 and the marker of column 2 and changes no cell."}]}
```

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11],"pointers":["a","b"],"steps":[{"at":{"a":-1,"b":-1},"vars":{"matrix":"[[1,2,3,4],[5,0,7,8],[9,10,0,12]]"},"note":"Start of the update pass. The markers name rows 1 and 2 and columns 1 and 2."},{"at":{"a":4,"b":7},"vars":{"matrix":"[[1,2,3,4],[0,0,0,0],[9,10,0,12]]"},"note":"Row 1 is marked, so the pass writes zero into its first and last cell and every cell between them."},{"at":{"a":8,"b":11},"vars":{"matrix":"[[1,2,3,4],[0,0,0,0],[0,0,0,0]]"},"note":"Row 2 is marked, so the pass writes zero into its first and last cell and every cell between them."},{"at":{"a":1,"b":9},"vars":{"matrix":"[[1,0,3,4],[0,0,0,0],[0,0,0,0]]"},"note":"Column 1 is marked, so the pass writes zero from its top cell to its bottom cell. Cells already cleared by a row stay zero."},{"at":{"a":2,"b":10},"vars":{"matrix":"[[1,0,0,4],[0,0,0,0],[0,0,0,0]]"},"note":"Column 2 is marked, so the pass writes zero from its top cell to its bottom cell. Cells already cleared by a row stay zero."}]}
```

<!-- stage: code -->
### Two Passes Over The Matrix

#### The Method With Two Marker Arrays

```java
static void setZeroes(int[][] m) {
    int rows = m.length, cols = m[0].length;
    boolean[] rowMark = new boolean[rows];
    boolean[] colMark = new boolean[cols];
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (m[r][c] == 0) {
                rowMark[r] = true;
                colMark[c] = true;
            }
        }
    }
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            if (rowMark[r] || colMark[c]) m[r][c] = 0;
        }
    }
}
```

#### Cost Of The Method

Each pass visits every cell once, so the time is O(rows * cols). The two marker arrays hold `rows + cols` booleans, so the extra space is O(rows + cols). Storing the markers in the first row and first column lowers the extra space to O(1) and keeps the time.

<!-- stage: applicability -->
### When To Record Before Writing

#### Recognizing The Pattern

Use the pattern when a write to one cell changes what a later read of another cell would see, and the later read must see the input. The invariant is that every read in the observation pass sees the original value. Statements such as "set the row and column to zero" or "update all cells at the same time" signal it.

#### A False Friend From Clearing While Scanning

Clearing a line as soon as the scan finds a zero looks like the same job with fewer passes. It breaks the invariant, because the loop then reads zeros that it wrote itself. A hash set of row indexes and column indexes also solves the problem, and Chapter 04 teaches sets. Boolean arrays are enough here because the indexes are small consecutive integers.

#### The Same Idea With Two Bits Per Cell

Conway's Game of Life updates every cell from the old values of its eight neighbors. A second matrix would work, but the same job fits in one matrix. Bit 0 of each cell holds the old state, and bit 1 holds the new state. Neighbor reads use only bit 0, so they still see the old generation. A final shift moves bit 1 into place. The exercise below uses this idea.

<!-- stage: exercises -->
### Exercises

#### [Build] Mark Bad Rows (Author exercise)
<!-- id: mx-mark-bad-rows -->

**Prerequisites.** The two passes from this lesson.

**Problem.** Given an integer matrix `m`, a row is bad when it contains the value `-1`. In a first pass, record which rows are bad without changing `m`. In a second pass, set every cell of each bad row to `0`. Return the number of bad rows.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= rows, cols <= 100`.
- **Values** satisfy `-10^6 <= m[r][c] <= 10^6`.
- **Mutation** is required; the method changes `m` in place.
- **Return** is an `int` that counts bad rows.

**Example 1.** Input `m = [[1,2],[3,-1],[5,6]]`, output 1, and `m` becomes `[[1,2],[0,0],[5,6]]`.

**Example 2.** Input `m = [[-1,-1],[2,-1]]`, output 2, and `m` becomes `[[0,0],[0,0]]`.

**Hint.** Which array has one entry per row, and which pass is allowed to write into it?

**Changed decision.** Basic case: the pass that records rows never writes into `m`.

#### [Vary] Set Matrix Zeroes (LeetCode 73)
<!-- id: mx-set-zeroes -->

**Prerequisites.** The first exercise above.

**Problem.** Given an `rows x cols` integer matrix `m`, set every cell of row `r` and every cell of column `c` to `0` for each cell `m[r][c] == 0` in the input. A zero written by the method must not cause any further clearing. Change `m` in place.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= rows, cols <= 200`.
- **Values** are `int`, and any value including `Integer.MIN_VALUE` can appear.
- **Mutation** is required; the method returns nothing.
- **Space** may be O(rows + cols).

**Example 1.** Input `m = [[5,0,6],[7,8,9],[1,2,3]]`, output `[[0,0,0],[7,0,9],[1,0,3]]` after the call.

**Example 2.** Input `m = [[1,2,3,4],[5,0,7,8],[9,10,0,12]]`, output `[[1,0,0,4],[0,0,0,0],[0,0,0,0]]` after the call.

**Hint.** Which two arrays hold the facts, and why must every zero be recorded before the first write?

**Changed decision.** Rows and columns both need markers, so one boolean array is not enough.

#### [Boundary] Constant-Space Variant (LeetCode 73)
<!-- id: mx-set-zeroes-constant -->

**Prerequisites.** The Vary exercise above.

**Problem.** Solve the same task as Set Matrix Zeroes, but use no array whose length depends on `rows` or `cols`. Store the markers inside the matrix, and keep two booleans for the original content of the first row and the first column.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= rows, cols <= 200`.
- **Values** are `int`, and any value can appear.
- **Mutation** is required; the method returns nothing.
- **Space** is O(1) extra space.

**Example 1.** Input `m = [[8,0,1],[2,3,4]]`, output `[[0,0,0],[2,0,4]]` after the call.

**Example 2.** Input `m = [[3,4],[0,5],[6,7]]`, output `[[0,4],[0,0],[0,7]]` after the call.

**Hint.** The cell `(0, 0)` is a marker for two lines. Which lines can the booleans keep apart?

**Changed decision.** The markers overwrite real data, so the first row and the first column are cleared last, using the saved booleans.

#### [Recognize] Game Of Life (LeetCode 289)
<!-- id: mx-game-of-life -->

**Prerequisites.** The Boundary exercise above.

**Problem.** A cell is live (`1`) or dead (`0`). A live cell stays live when exactly 2 or 3 of its 8 neighbors are live, and it dies otherwise. A dead cell becomes live when exactly 3 neighbors are live. Neighbors outside the matrix count as dead. Compute the next generation in place, where every cell is updated from the old values of the whole generation.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= rows, cols <= 25`.
- **Values** are `0` or `1`.
- **Mutation** is required; the method returns nothing.
- **Space** is O(1) extra space.

**Example 1.** Input `m = [[0,0,0,0],[0,1,1,1],[1,1,1,0],[0,0,0,0]]`, output `[[0,0,1,0],[1,0,0,1],[1,0,0,1],[0,1,0,0]]` after the call.

**Example 2.** Input `m = [[0,1,1],[1,0,0],[0,0,0]]`, output `[[0,1,0],[0,1,0],[0,0,0]]` after the call.

**Hint.** If a cell stores the old state in bit 0, which bit can hold the new state without disturbing neighbor reads?

**Changed decision.** The marker is now a bit of the cell itself, so a neighbor read must mask the old state with `& 1`.
