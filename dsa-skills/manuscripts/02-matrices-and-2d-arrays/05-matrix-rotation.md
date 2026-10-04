<!-- lesson-kind: standard -->
<!-- lesson-id: matrix-rotation -->
## Rotating A Square In Place

<!-- stage: context -->
### A Photo Turn That Exhausts Memory

A photo app stores a square image as an `int[][]` of pixel values and lets the user turn it a quarter turn clockwise. The first version builds a second array of the same size, copies every pixel to its new position, and copies the result back. On a 4,096 by 4,096 image the array holds 16,777,216 values, about 64 MiB. The copy needs another 64 MiB while the original is still alive. On a phone with a small heap, the app stops with `OutOfMemoryError`.

The turn is a fixed rule for where each pixel goes. This lesson asks whether the pixels can move inside the same array, and what small set of moves produces the quarter turn.

<!-- stage: naive -->
### Copying Into A Second Array

The naive method writes each pixel at its new position in a new array. A pixel at row `r` and column `c` lands at row `c` and column `n - 1 - r`.

```java
static int[][] turnClockwise(int[][] m) {
    int n = m.length;
    int[][] out = new int[n][n];
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            out[c][n - 1 - r] = m[r][c];
        }
    }
    return out;
}
```

The method is correct. On `{{1, 2}, {3, 4}}` it returns `{{3, 1}, {4, 2}}`. It leaves the input untouched, which is fine when the caller wants a new image and wasteful when the caller wants the same array turned.

<!-- stage: bottleneck -->
### The Memory That The Copy Needs

```predict
The copy takes O(n^2) time, and a pass over every pixel cannot be avoided. Which resource does the copy waste, and why can a direct overwrite not simply follow the same formula?

The copy uses O(n^2) extra space, equal to the input. Overwriting in place with the same formula fails because writing to position (c, n - 1 - r) destroys a pixel that has not been moved yet.
```

Time is not the problem here, because every pixel must move, so any method costs at least O(n^2). The waste is memory. A copy doubles the footprint, and a direct overwrite loses data, because each destination cell still holds a pixel that belongs somewhere else. A pixel at `(r, c)` goes to `(c, n - 1 - r)`. That pixel in turn must go to a third cell, and the cycle of four cells closes after four moves: from `(r, c)` to `(c, n - 1 - r)`, then to `(n - 1 - r, n - 1 - c)`, then to `(n - 1 - c, r)`, and back to `(r, c)`. Following such a chain by hand needs a careful order and is easy to get wrong. A shorter route splits the turn into two moves that each swap pairs of cells.

<!-- stage: insight -->
### Two Simple Swaps Make A Quarter Turn

A quarter turn clockwise equals two steps applied in order. Each step moves a cell only to a mirrored cell, so one temporary value per swap is enough.

#### First Mirror Across The Main Diagonal

The **transpose** sends the cell `(r, c)` to `(c, r)`. It mirrors the matrix across the main diagonal, which runs from the top-left to the bottom-right. The cells with `r == c` stay where they are. Every other cell pairs with exactly one partner, and the two swap values. The loop therefore swaps each pair once, by visiting only the cells with `c > r`. Visiting every cell would swap each pair twice and restore the original.

#### Then Flip Each Row

To **reverse** a row means to swap its first cell with its last, its second with its second to last, and so on. This sends `(c, r)` to `(c, n - 1 - r)`. The transpose followed by this reversal sends `(r, c)` to `(c, n - 1 - r)`, which is the clockwise quarter turn.

<!-- names: transpose, reverse, main diagonal -->

#### Why The Center Needs No Special Move

When `n` is odd, the cell `(r, c)` with `r = c = (n - 1) / 2` maps to itself under the quarter turn. The reason is that `n - 1 - r` equals `r`. The transpose leaves it alone, and the reversal loop stops before the middle cell, so it stays in place. The invariant is that the transpose swaps each pair once and the reversal swaps each row pair once. A fixed cell is not swapped by either step, so the final matrix equals the quarter turn.

<!-- stage: variables -->
### The Indexes And The Spare Value

The two loops need only a few pieces of state.

- **n** holds the side length, which is `m.length`, and it never changes.
- **r and c** hold the pair of indexes being swapped, with `c > r` in the transpose.
- **lo and hi** hold the two ends of a row during the reversal, with `lo` rising and `hi` falling.
- **tmp** holds one value for the duration of a single swap.

<!-- stage: trace -->
### Turning A Three By Three Matrix

#### The Transpose Pass

Take the matrix with rows `[1, 2, 3]`, `[4, 5, 6]` and `[7, 8, 9]`. The cells are numbered by their row-major index. The pointers `a` and `b` mark the two cells being swapped. The transpose visits only the cells above the main diagonal. It swaps cell 1 with cell 3, cell 2 with cell 6 and cell 5 with cell 7. The diagonal cells 0, 4 and 8 never move.

#### The Row Reversal Pass

After the transpose, the rows are `[1, 4, 7]`, `[2, 5, 8]` and `[3, 6, 9]`. Each row swaps its first cell with its last. The middle cell of each row stays, because it is its own mirror. The result is `[7, 4, 1]`, `[8, 5, 2]` and `[9, 6, 3]`, which is the input turned a quarter turn clockwise.

#### Stepping Through Both Passes

```trace
{"cells":[0,1,2,3,4,5,6,7,8],"pointers":["a","b"],"steps":[{"at":{"a":-1,"b":-1},"vars":{"matrix":"[[1,2,3],[4,5,6],[7,8,9]]"},"note":"Start of the transpose pass. Only cells above the main diagonal are visited."},{"at":{"a":1,"b":3},"vars":{"matrix":"[[1,4,3],[2,5,6],[7,8,9]]"},"note":"Swap row 0, column 1 with row 1, column 0. The cells that lie on the main diagonal are never touched."},{"at":{"a":2,"b":6},"vars":{"matrix":"[[1,4,7],[2,5,6],[3,8,9]]"},"note":"Swap row 0, column 2 with row 2, column 0. The cells that lie on the main diagonal are never touched."},{"at":{"a":5,"b":7},"vars":{"matrix":"[[1,4,7],[2,5,8],[3,6,9]]"},"note":"Swap row 1, column 2 with row 2, column 1. The cells that lie on the main diagonal are never touched."}]}
```

```trace
{"cells":[0,1,2,3,4,5,6,7,8],"pointers":["a","b"],"steps":[{"at":{"a":-1,"b":-1},"vars":{"matrix":"[[1,4,7],[2,5,8],[3,6,9]]"},"note":"Start of the reversal pass, on the transposed matrix."},{"at":{"a":0,"b":2},"vars":{"matrix":"[[7,4,1],[2,5,8],[3,6,9]]"},"note":"Row 0 swaps its first and last cells. The middle cell of the row is its own mirror and stays."},{"at":{"a":3,"b":5},"vars":{"matrix":"[[7,4,1],[8,5,2],[3,6,9]]"},"note":"Row 1 swaps its first and last cells. The middle cell of the row is its own mirror and stays."},{"at":{"a":6,"b":8},"vars":{"matrix":"[[7,4,1],[8,5,2],[9,6,3]]"},"note":"Row 2 swaps its first and last cells. The middle cell of the row is its own mirror and stays."}]}
```

<!-- stage: code -->
### Two Loops Over The Same Array

#### The Rotation Method

```java
static void rotateClockwise(int[][] m) {
    int n = m.length;
    for (int r = 0; r < n; r++) {
        for (int c = r + 1; c < n; c++) {
            int tmp = m[r][c];
            m[r][c] = m[c][r];
            m[c][r] = tmp;
        }
    }
    for (int[] row : m) {
        for (int lo = 0, hi = n - 1; lo < hi; lo++, hi--) {
            int tmp = row[lo];
            row[lo] = row[hi];
            row[hi] = tmp;
        }
    }
}
```

#### Cost Of The Rotation

The first pass swaps about `n * (n - 1) / 2` pairs, and the second pass swaps about `n / 2` pairs in each of `n` rows. Both passes are O(n^2) time. The method stores only the indexes and one spare value, so it uses O(1) extra space. It reads nothing outside the square, because both indexes stay below `n`.

<!-- stage: applicability -->
### When A Matrix Can Turn In Place

#### Checking The Statement

The method needs a square matrix, and the statement must allow changing the input. The invariant is that every cell is swapped with its mirror partner exactly once or is its own partner. A prompt that says "rotate the image in place" with an `n x n` matrix matches this pattern directly.

#### When A Rectangle Breaks The Swaps

A rectangle is a false friend of the square, because the same swap code looks valid for it. A rectangle with `R` rows and `C` columns turns into a matrix with `C` rows and `R` columns. When `R` differs from `C`, the result does not fit in the same array object. The two-swap method fails for a rectangle. The method that works copies into a new array with `C` rows and `R` columns. It is the naive version with the new sizes. The statement decides which one applies, so read the shape promise first.

#### Other Turns From The Same Two Moves

The counterclockwise turn needs the transpose and then a reversal of each column, which swaps the cell `(r, c)` with `(n - 1 - r, c)`. A half turn needs no transpose, because reversing each row and then reversing the order of the rows sends `(r, c)` to `(n - 1 - r, n - 1 - c)`. Name the mapping first, then pick the swaps that produce it.

<!-- stage: exercises -->
### Exercises

#### [Build] Transpose Square (Author exercise)
<!-- id: mx-transpose-square -->

**Prerequisites.** The transpose step from this lesson.

**Problem.** Given a square integer matrix `m` with `n` rows and `n` columns, transpose it in place. After the call, the cell `m[r][c]` holds the value that `m[c][r]` held before the call, for all `r` and `c`. Swap each pair of mirrored cells once, and do not allocate a second matrix.

**Constraints.** The limits are:
- **Shape** is square with `1 <= n <= 100`.
- **Values** satisfy `-10^6 <= m[r][c] <= 10^6`.
- **Mutation** is required; the method changes `m` and returns nothing.
- **Space** is O(1) extra space.

**Example 1.** Input `m = [[1,2],[3,4]]`, output `[[1,3],[2,4]]` after the call.

**Example 2.** Input `m = [[1,2,3],[4,5,6],[7,8,9]]`, output `[[1,4,7],[2,5,8],[3,6,9]]` after the call.

**Hint.** What happens to the matrix if the loop visits all cells and swaps each one with its mirror cell?

**Changed decision.** Basic case: the inner loop starts at `r + 1`, so each pair is swapped once.

#### [Vary] Rotate Image (LeetCode 48)
<!-- id: mx-rotate-image -->

**Prerequisites.** The transpose exercise above.

**Problem.** Given an `n x n` matrix `m`, rotate it a quarter turn clockwise in place. After the call, the value that was at `m[r][c]` is at `m[c][n - 1 - r]`. Do not allocate another matrix.

**Constraints.** The limits are:
- **Shape** is square with `1 <= n <= 20`.
- **Values** satisfy `-1000 <= m[r][c] <= 1000`.
- **Mutation** is required; the method returns nothing.
- **Space** is O(1) extra space.

**Example 1.** Input `m = [[1,2],[3,4]]`, output `[[3,1],[4,2]]` after the call.

**Example 2.** Input `m = [[2,4,6],[8,1,3],[5,7,9]]`, output `[[5,8,2],[7,1,4],[9,3,6]]` after the call.

**Hint.** Which mirror step comes first, and which cell mapping does a row reversal add?

**Changed decision.** A row reversal follows the transpose, and together they replace the four-cell chain.

#### [Boundary] Odd Center (Author exercise)
<!-- id: mx-odd-center -->

**Prerequisites.** The rotation exercise above.

**Problem.** A clockwise quarter turn of an `n x n` matrix sends the cell `(r, c)` to the cell `(c, n - 1 - r)`. A cell is fixed when it is sent to itself. Given `n`, return the number of cells that are not fixed.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 10^9`.
- **Answer** has type `long`.
- **Matrix** is never built, because `n` can be too large to store.
- **Formula** must use the mapping only, with no loop over cells.

**Example 1.** Input `n = 3`, output 8, because only the center cell is fixed.

**Example 2.** Input `n = 4`, output 16, because no cell is fixed.

**Hint.** Solve `r = c` and `c = n - 1 - r` together. For which `n` does a whole-number solution exist?

**Changed decision.** The parity of `n` decides whether a fixed cell exists, so odd and even sizes give different answers.

#### [Recognize] Counterclockwise Rotation (Author exercise)
<!-- id: mx-rotate-counter -->

**Prerequisites.** All three exercises above.

**Problem.** Given an `n x n` matrix `m`, rotate it a quarter turn counterclockwise in place. After the call, the value that was at `m[r][c]` is at `m[n - 1 - c][r]`. Use the transpose followed by one more in-place step, and name the step that replaces the row reversal.

**Constraints.** The limits are:
- **Shape** is square with `1 <= n <= 20`.
- **Values** satisfy `-1000 <= m[r][c] <= 1000`.
- **Mutation** is required; the method returns nothing.
- **Space** is O(1) extra space.

**Example 1.** Input `m = [[1,2],[3,4]]`, output `[[2,4],[1,3]]` after the call.

**Example 2.** Input `m = [[2,4,6],[8,1,3],[5,7,9]]`, output `[[6,3,9],[4,1,7],[2,8,5]]` after the call.

**Hint.** After the transpose, which pair of cells in each column must swap to send `(c, r)` to `(n - 1 - c, r)`?

**Changed decision.** The second step reverses each column and not each row, so the swapped pair changes from `(r, lo)` and `(r, hi)` to `(lo, c)` and `(hi, c)`.
