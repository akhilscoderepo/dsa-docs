<!-- lesson-kind: standard -->
<!-- lesson-id: matrix-rotation -->
## Matrix Rotation

<!-- stage: context -->
### Turning A Puzzle Without Spare Table

A square puzzle is made of numbered tiles laid out in rows and columns on a small table, and the puzzle must be turned a quarter turn clockwise so that the tile in the upper-left corner ends up in the upper-right corner. The table is exactly as big as the puzzle, with no room beside it to lay out a second copy. Tiles may be lifted and swapped, but nothing can be set down off the table.

A careful player works out where each tile goes. The top row becomes the right column, the right column becomes the bottom row, and so on around. Moving four tiles at a time in a cycle works, but the bookkeeping is easy to get wrong. A different way of thinking might need only two simple motions, each of which is a sweep of swaps that is hard to confuse with the other.

<!-- stage: naive -->
### Copy Onto A Second Table

If a second table were allowed, the rotation would be a direct copy, with each tile moved to its new position.

```java
static int[][] rotateWithCopy(int[][] matrix) {
    int n = matrix.length;
    int[][] turned = new int[n][n];
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            turned[c][n - 1 - r] = matrix[r][c];
        }
    }
    return turned;
}
```

For `[[1, 2], [3, 4]]` it returns `[[3, 1], [4, 2]]`. The rule that tile `(r, c)` lands at `(c, n - 1 - r)` is simple and easy to check by hand.

<!-- stage: bottleneck -->
### A Full Second Copy Of The Board

The copy method runs in O(n^2) time, and no method can do better, since every tile must move. Its problem is the extra memory, which is another `n * n` cells, so the space is O(n^2). For a 10,000 by 10,000 image of integers that is another four hundred megabytes, and the problem statement for this kind of exercise says the input array itself must be changed.

The rule also hides the difficulty of working in place. Writing a tile to its new position overwrites the tile that was there, which has not moved yet, so a careless in-place loop destroys data. The question is whether the quarter turn can be built from steps that never overwrite an unmoved tile. Swaps never lose data, because a swap writes two cells and both old values are kept in each other's place.

<!-- stage: insight -->
### Rotation Is Transpose Plus Reversal

A quarter turn clockwise can be split into two motions made only of swaps. The first is the **transpose**, which flips the matrix over its main diagonal, so that the cell at row `r` and column `c` trades places with the cell at row `c` and column `r`. The second is **row reversal**, which reverses every row from left to right.

To see why they combine into a rotation, follow one cell. The transpose moves `(r, c)` to `(c, r)`. Reversing the row then moves column `r` to column `n - 1 - r`, so the cell lands at `(c, n - 1 - r)`, which is exactly where the copy method puts it. The two sweeps have the same effect as the quarter turn with no extra memory.

<!-- names: transpose, row reversal, off-diagonal pair -->

The transpose needs one care. Each **off-diagonal pair**, two cells `(r, c)` and `(c, r)` with `r` different from `c`, must be swapped exactly once. If the loop visits every cell and swaps each, then both members of every pair trigger the swap and the matrix returns to where it began. Restricting the inner loop to `c > r` visits each pair once, and the diagonal cells, which are their own mirror images, are never touched.

The invariant is that after the transpose loop has finished a row, the cells on and above the diagonal in that row are correct and each swapped partner has already received its value. For a counterclockwise turn, only the second sweep changes: reverse every column from top to bottom instead of every row. This change turns the same two-step recipe into the opposite rotation, and the exercises name it.

<!-- stage: variables -->
### Two Indices And A Swap

The transpose uses the row `r` and a column `c` that starts at `r + 1`, so every pair is visited once and the diagonal is skipped. A swap needs one temporary variable. The reversal uses the row `r` and two column positions `lo` and `hi`, starting at the ends and moving toward each other until they meet or cross. The size `n` is read once, and the loops use only `n`, since the matrix is square.

<!-- stage: trace -->
### Turning A Three By Three

Take `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]`. The transpose swaps three pairs. Cell `(0, 1)` holding 2 swaps with `(1, 0)` holding 4. Cell `(0, 2)` holding 3 swaps with `(2, 0)` holding 7. Cell `(1, 2)` holding 6 swaps with `(2, 1)` holding 8. The matrix is now `[[1, 4, 7], [2, 5, 8], [3, 6, 9]]`, and the diagonal cells 1, 5 and 9 never moved.

Then each row is reversed. Row 0 swaps its first and last cells, giving `7, 4, 1`. Row 1 swaps 2 and 8 and leaves the middle 5 alone, giving `8, 5, 2`. Row 2 swaps 3 and 9 and leaves 6, giving `9, 6, 3`. The result is `[[7, 4, 1], [8, 5, 2], [9, 6, 3]]`, a clockwise quarter turn. The center cell never moved in either sweep.

A second picture, for a two by two matrix and a counterclockwise turn, shows the changed second step. The transpose swaps the one off-diagonal pair, and then each column is reversed from top to bottom instead.

```trace
{"cells":[1,2,3,4,5,6,7,8,9],"pointers":["first","second"],"steps":[{"at":{"first":1,"second":3},"vars":{"phase":"transpose","matrix":"[[1,4,3],[2,5,6],[7,8,9]]"},"note":"Transpose: swap (0, 1) with (1, 0). Each off-diagonal pair is swapped once."},{"at":{"first":2,"second":6},"vars":{"phase":"transpose","matrix":"[[1,4,7],[2,5,6],[3,8,9]]"},"note":"Transpose: swap (0, 2) with (2, 0). Each off-diagonal pair is swapped once."},{"at":{"first":5,"second":7},"vars":{"phase":"transpose","matrix":"[[1,4,7],[2,5,8],[3,6,9]]"},"note":"Transpose: swap (1, 2) with (2, 1). Each off-diagonal pair is swapped once."},{"at":{"first":0,"second":2},"vars":{"phase":"reverse rows","matrix":"[[7,4,1],[2,5,8],[3,6,9]]"},"note":"Reverse row 0: swap columns 0 and 2."},{"at":{"first":3,"second":5},"vars":{"phase":"reverse rows","matrix":"[[7,4,1],[8,5,2],[3,6,9]]"},"note":"Reverse row 1: swap columns 0 and 2."},{"at":{"first":6,"second":8},"vars":{"phase":"reverse rows","matrix":"[[7,4,1],[8,5,2],[9,6,3]]"},"note":"Reverse row 2: swap columns 0 and 2."}]}
```

```trace
{"cells":[1,2,3,4],"pointers":["first","second"],"steps":[{"at":{"first":1,"second":2},"vars":{"phase":"transpose","matrix":"[[1,3],[2,4]]"},"note":"Transpose: swap (0, 1) with (1, 0). Each off-diagonal pair is swapped once."},{"at":{"first":0,"second":2},"vars":{"phase":"reverse columns","matrix":"[[2,3],[1,4]]"},"note":"Reverse column 0: swap rows 0 and 1."},{"at":{"first":1,"second":3},"vars":{"phase":"reverse columns","matrix":"[[2,4],[1,3]]"},"note":"Reverse column 1: swap rows 0 and 1."}]}
```

<!-- stage: code -->
### Two Sweeps Of Swaps

```java
static void transpose(int[][] m) {
    int n = m.length;
    for (int r = 0; r < n; r++) {
        for (int c = r + 1; c < n; c++) {
            int tmp = m[r][c]; m[r][c] = m[c][r]; m[c][r] = tmp;
        }
    }
}

static void rotateClockwise(int[][] m) {
    transpose(m);
    int n = m.length;
    for (int r = 0; r < n; r++) {
        for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) {
            int tmp = m[r][lo]; m[r][lo] = m[r][hi]; m[r][hi] = tmp;
        }
    }
}

static void rotateCounterclockwise(int[][] m) {
    transpose(m);
    int n = m.length;
    for (int c = 0; c < n; c++) {
        for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) {
            int tmp = m[lo][c]; m[lo][c] = m[hi][c]; m[hi][c] = tmp;
        }
    }
}
```

Each sweep touches every cell a constant number of times, so the time is O(n^2) and the extra space is O(1), with one temporary integer. The transpose starts the inner column at `r + 1`, so each pair is swapped once. The reversal loops stop when `lo` reaches `hi`, which leaves the middle element of an odd-length row untouched. These methods require a square matrix, because the swap targets `m[c][r]` must exist.

<!-- stage: applicability -->
### When A Square Must Turn In Place

Use transpose plus reversal when a square matrix must be rotated by a quarter turn, or flipped over a diagonal, using no second matrix. The invariant is that every off-diagonal pair is swapped exactly once, so the transpose is correct, and every row or column is reversed exactly once. Check the shape first: rows must equal columns.

The false friend is a rectangular matrix. A matrix with two rows and three columns turns into one with three rows and two columns, and the same array cannot change its dimensions, so no in-place rotation exists. A new matrix is needed, and the copy method is the right tool there. Another false friend is the transpose loop that visits every cell, which swaps each pair twice and does nothing. A third is mixing up the direction, so that rotating clockwise is done with column reversal and the result is a counterclockwise turn.

In Java, remember that an `int[][]` is an array of rows, so a row reversal could also be done by swapping whole row references for a vertical flip, but a rotation needs cell-level swaps. Do the swaps with a temporary variable. For other quarter turns, rotating by 180 degrees is two reversals with no transpose, and three quarter turns clockwise equals one counterclockwise.

<!-- stage: exercises -->
### Exercises

#### [Build] Transpose Square (Author exercise)
<!-- id: mx-transpose-square -->

**Prerequisites.** The shape-contract lesson; swapping two array cells.

**Problem.** Transpose a square matrix in place, so that the cell at row `r` and column `c` ends up at row `c` and column `r`. Swap each off-diagonal pair exactly once.

**Constraints.** 1 <= n <= 200, with an `n` by `n` matrix and integer cells. No second matrix is allowed.

**Example 1.** Input `matrix = [[2, 7], [9, 4]]`, output `[[2, 9], [7, 4]]`.

**Example 2.** Input `matrix = [[1, 0, 0], [0, 2, 0], [0, 0, 3]]`, output the same matrix, since it is already symmetric.

**Hint.** Which cells have a mirror image elsewhere? What happens if every cell, and not just half of them, triggers a swap?

**Changed decision.** First rung: the inner loop starts after the diagonal so that each pair is swapped once.

#### [Vary] Rotate Image (LeetCode 48)
<!-- id: mx-rotate-image -->

**Prerequisites.** The transpose-square exercise above.

**Problem.** Rotate an `n` by `n` matrix by ninety degrees clockwise, in place, using no second matrix.

**Constraints.** 1 <= n <= 20 and -1000 <= cell <= 1000. The matrix is square.

**Example 1.** Input `matrix = [[1, 2], [3, 4]]`, output `[[3, 1], [4, 2]]`.

**Example 2.** Input `matrix = [[5, 1, 9], [2, 4, 8], [10, 3, 6]]`, output `[[10, 2, 5], [3, 4, 1], [6, 8, 9]]`.

**Hint.** What does the transpose do to a cell's row and column? What second sweep fixes the column to complete a clockwise turn?

**Changed decision.** A second sweep of reversals is added after the transpose, which turns a diagonal flip into a rotation.

#### [Boundary] Odd Center (Author exercise)
<!-- id: mx-odd-center -->

**Prerequisites.** The two exercises above.

**Problem.** Rotate a `3 x 3` matrix clockwise and show that its center cell stays valid with no special movement. Count the swaps made by the transpose sweep and by the reversal sweep, and explain why neither touches the center.

**Constraints.** The matrix is square. The check also covers `n = 1`, where the only cell is the center.

**Example 1.** Input `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`, output `[[7, 4, 1], [8, 5, 2], [9, 6, 3]]` with 3 swaps in each sweep and the center 5 unchanged.

**Example 2.** Input `matrix = [[7]]`, output `[[7]]` with no swaps.

**Hint.** Which cells does the transpose skip? Which index does a row reversal leave in place when the length is odd?

**Changed decision.** The tests target the one cell that is its own mirror image in both sweeps.

#### [Recognize] Counterclockwise Rotation (Author exercise)
<!-- id: mx-counterclockwise -->

**Prerequisites.** All three exercises above.

**Problem.** Rotate a square matrix ninety degrees counterclockwise, in place. Use the transpose and then change the second sweep, and name the change.

**Constraints.** 1 <= n <= 20 and integer cells. The matrix is square and no second matrix is allowed.

**Example 1.** Input `matrix = [[1, 2], [3, 4]]`, output `[[2, 4], [1, 3]]`.

**Example 2.** Input `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`, output `[[3, 6, 9], [2, 5, 8], [1, 4, 7]]`.

**Hint.** After the transpose, which direction should each line be reversed to put the first row of the input into the first column of the output, read bottom to top?

**Changed decision.** The second sweep reverses columns instead of rows, which changes the quarter turn from clockwise to counterclockwise.
