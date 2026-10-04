<!-- lesson-kind: standard -->
<!-- lesson-id: spiral-boundaries -->
## Walking A Matrix In Spiral Order

<!-- stage: context -->
### A Spiral That Repeats Cells

A test fixture must list the cells of a grid clockwise, starting at the outer cells and moving inward. The first version uses four loops in a row. The loops go along the first row, down the last column, back along the last row, and up the first column. Then the code repeats the four loops on the smaller grid inside. This works on a 4 by 4 grid. On a grid with one row, `{{1, 2, 3}}`, the same code lists `1, 2, 3, 2, 1`, because the loop along the last row walks the same cells again.

The error appears only when the grid becomes one row or one column wide. This lesson asks how a spiral walk knows which cells remain, and how it stops before it repeats one.

<!-- stage: naive -->
### Turning When The Path Is Blocked

The simple method walks one cell at a time. It keeps a direction, and it marks every cell it emits. When the next cell lies outside the matrix or is already marked, it turns clockwise. The matrix has `rows * cols` cells, so the walk stops after that many steps.

```java
static List<Integer> spiralWithMarks(int[][] m) {
    int rows = m.length, cols = m[0].length;
    boolean[][] seen = new boolean[rows][cols];
    int[] dr = {0, 1, 0, -1};
    int[] dc = {1, 0, -1, 0};
    List<Integer> out = new ArrayList<>();
    int r = 0, c = 0, d = 0;
    for (int k = 0; k < rows * cols; k++) {
        out.add(m[r][c]);
        seen[r][c] = true;
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || seen[nr][nc]) {
            d = (d + 1) % 4;
            nr = r + dr[d];
            nc = c + dc[d];
        }
        r = nr;
        c = nc;
    }
    return out;
}
```

The method is correct for every rectangle. On `{{1, 2, 3}, {4, 5, 6}}` it returns `[1, 2, 3, 6, 5, 4]`.

<!-- stage: bottleneck -->
### The Memory For Visited Cells

```predict
The method above stores one boolean per cell. In a spiral, the visited cells always form complete outer rows and columns. How many numbers would describe the cells that remain, and which numbers are they?

Four numbers are enough: the first and last remaining row and the first and last remaining column. The remaining cells always form one rectangle, so these four indexes describe it exactly.
```

The walk takes O(rows * cols) time, and no method can emit every cell faster. The waste is O(rows * cols) extra space for `seen`. The turn test also reads `seen` at every step. The structure of a spiral makes that table unnecessary. The cells already emitted always form whole rows and columns that touch the outside of the matrix, so the cells that remain always form a rectangle. Four integers describe a rectangle. The next section keeps those four integers and drops the table.

<!-- stage: insight -->
### Four Indexes Describe What Remains

The walk keeps the edges of the rectangle that has not been emitted yet and shrinks that rectangle after each pass.

#### The Rectangle That Remains

The **boundary** of the walk is four inclusive indexes: `top`, `bottom`, `left` and `right`. They enclose the **unvisited rectangle**, which is the set of cells with `top <= r <= bottom` and `left <= c <= right`. The invariant is that these four indexes enclose exactly the cells not yet emitted. The rectangle is empty when `top > bottom` or `left > right`, and the walk stops at that point.

#### One Layer Takes Four Passes

A **layer** is the outer ring of the unvisited rectangle. The walk emits a layer in four passes. It emits the cells of row `top` from `left` to `right`, and then increases `top`. It emits the cells of column `right` from `top` to `bottom`, and then decreases `right`. It emits the cells of row `bottom` from `right` to `left`, and then decreases `bottom`. It emits the cells of column `left` from `bottom` to `top`, and then increases `left`. Each pass removes the cells it emitted from the rectangle, so the invariant still holds after the pass.

#### Guards For A Single Line

After the first two passes, the rectangle can become one row or one column wide, or empty. The third pass must run only when `top <= bottom`, because otherwise it emits the row that the first pass already emitted. The fourth pass must run only when `left <= right`, because otherwise it emits the column that the second pass already emitted. These two checks are the whole fix for the repeated cells in the opening example.

<!-- names: boundary, unvisited rectangle, layer -->

<!-- stage: variables -->
### The Four Edges And The Output

The method keeps five pieces of state, and each one changes at a known point.

- **top** holds the first unvisited row, and it increases after the pass along the first row.
- **bottom** holds the last unvisited row, and it decreases after the pass along the last row.
- **left** holds the first unvisited column, and it increases after the pass along the first column.
- **right** holds the last unvisited column, and it decreases after the pass along the last column.
- **out** holds the emitted values in order, and every pass appends to it.

<!-- stage: trace -->
### Walking Two Small Matrices

#### A Three By Four Matrix

The first walk covers the rows `[1, 2, 3, 4]`, `[5, 6, 7, 8]` and `[9, 10, 11, 12]`. The cells are numbered by row-major index, and the pointer `p` marks the cell just emitted. The first layer emits the cells 1 to 4, then 8 and 12, then 11, 10 and 9, and then 5. The unvisited rectangle shrinks to row 1 with columns 1 and 2. The top pass emits 6 and 7. After that pass, `top` exceeds `bottom`, so the guard skips the bottom pass.

#### A Matrix With One Column

The second matrix has three rows and one column, with the values 1, 2 and 3. The top pass emits the value 1, and the right pass emits the values 2 and 3. After that pass, `right` is smaller than `left`. The guard on the fourth pass stops it from emitting the value 2 a second time.

#### Stepping Through Both Walks

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11],"pointers":["p"],"steps":[{"at":{"p":-1},"vars":{"top":0,"bottom":2,"left":0,"right":3,"out":0},"note":"Start of the walk. The four edges enclose the whole matrix and nothing is emitted."},{"at":{"p":0},"vars":{"top":0,"bottom":2,"left":0,"right":3,"out":1},"note":"Top pass emits the value 1 from row 0, column 0."},{"at":{"p":1},"vars":{"top":0,"bottom":2,"left":0,"right":3,"out":2},"note":"Top pass emits the value 2 from row 0, column 1."},{"at":{"p":2},"vars":{"top":0,"bottom":2,"left":0,"right":3,"out":3},"note":"Top pass emits the value 3 from row 0, column 2."},{"at":{"p":3},"vars":{"top":0,"bottom":2,"left":0,"right":3,"out":4},"note":"Top pass emits the value 4 from row 0, column 3."},{"at":{"p":7},"vars":{"top":1,"bottom":2,"left":0,"right":3,"out":5},"note":"Right pass emits the value 8 from row 1, column 3."},{"at":{"p":11},"vars":{"top":1,"bottom":2,"left":0,"right":3,"out":6},"note":"Right pass emits the value 12 from row 2, column 3."},{"at":{"p":10},"vars":{"top":1,"bottom":2,"left":0,"right":2,"out":7},"note":"Bottom pass emits the value 11 from row 2, column 2."},{"at":{"p":9},"vars":{"top":1,"bottom":2,"left":0,"right":2,"out":8},"note":"Bottom pass emits the value 10 from row 2, column 1."},{"at":{"p":8},"vars":{"top":1,"bottom":2,"left":0,"right":2,"out":9},"note":"Bottom pass emits the value 9 from row 2, column 0."},{"at":{"p":4},"vars":{"top":1,"bottom":1,"left":0,"right":2,"out":10},"note":"Left pass emits the value 5 from row 1, column 0."},{"at":{"p":5},"vars":{"top":1,"bottom":1,"left":1,"right":2,"out":11},"note":"Top pass emits the value 6 from row 1, column 1."},{"at":{"p":6},"vars":{"top":1,"bottom":1,"left":1,"right":2,"out":12},"note":"Top pass emits the value 7 from row 1, column 2."},{"at":{"p":6},"vars":{"top":2,"bottom":1,"left":1,"right":1,"out":12},"note":"The bottom edge is now above the top edge, so the guard skips the bottom pass."}]}
```

```trace
{"cells":[0,1,2],"pointers":["p"],"steps":[{"at":{"p":-1},"vars":{"top":0,"bottom":2,"left":0,"right":0,"out":0},"note":"Start of the walk. The four edges enclose the whole matrix and nothing is emitted."},{"at":{"p":0},"vars":{"top":0,"bottom":2,"left":0,"right":0,"out":1},"note":"Top pass emits the value 1 from row 0, column 0."},{"at":{"p":1},"vars":{"top":1,"bottom":2,"left":0,"right":0,"out":2},"note":"Right pass emits the value 2 from row 1, column 0."},{"at":{"p":2},"vars":{"top":1,"bottom":2,"left":0,"right":0,"out":3},"note":"Right pass emits the value 3 from row 2, column 0."},{"at":{"p":2},"vars":{"top":1,"bottom":1,"left":0,"right":-1,"out":3},"note":"The right edge is now before the left edge, so the guard skips the left pass."}]}
```

<!-- stage: code -->
### One Loop That Peels Layers

#### The Spiral Method

```java
static List<Integer> spiralOrder(int[][] m) {
    List<Integer> out = new ArrayList<>();
    int top = 0, bottom = m.length - 1;
    int left = 0, right = m[0].length - 1;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; c++) out.add(m[top][c]);
        top++;
        for (int r = top; r <= bottom; r++) out.add(m[r][right]);
        right--;
        if (top <= bottom) {
            for (int c = right; c >= left; c--) out.add(m[bottom][c]);
            bottom--;
        }
        if (left <= right) {
            for (int r = bottom; r >= top; r--) out.add(m[r][left]);
            left++;
        }
    }
    return out;
}
```

#### Cost Of The Method

Each cell is emitted exactly once, so the time is O(rows * cols). The method stores four integers besides the output list, so the extra space is O(1). The output list holds `rows * cols` values, and the problem requires it.

<!-- stage: applicability -->
### When The Edges Replace The Visited Table

#### Recognizing The Pattern

Use this pattern when the output consumes a whole rectangle from the outside in, or fills one from the outside in. The invariant is that the four indexes always enclose the cells not yet handled. Statements such as "in spiral order" or "layer by layer" match it directly.

#### A False Friend From The Direction Walk

The turn-when-blocked walk from the direction lesson earlier in this chapter produces the same output on a plain rectangle, so the two methods look interchangeable. They differ in their failure modes. The direction walk needs a table of visited cells or a blocking rule, and it fits paths that can bend in any order around obstacles. The four-index method needs no table, but it works only when the emitted cells always form whole outer rows and columns. A path with blocked cells breaks that precondition, and that is a no-go condition for this method.

#### Filling Instead Of Reading

The same four indexes can write a matrix as easily as they can read one. A pass that writes `next++` into each cell produces a spiral-filled matrix with the same guards. Name the order of the passes first, and write the guards from the rectangle that remains.

<!-- stage: exercises -->
### Exercises

#### [Build] One Ring (Author exercise)
<!-- id: mx-one-ring -->

**Prerequisites.** The four passes from this lesson.

**Problem.** Given a rectangular integer matrix `m`, return the values of its outer cells in clockwise order, starting at `m[0][0]`. A cell appears once. A matrix with one row returns that row, and a matrix with one column returns that column from top to bottom.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= rows, cols <= 100`.
- **Values** satisfy `-1000 <= m[r][c] <= 1000`.
- **Mutation** is not allowed; the method reads `m` only.
- **Return** is a `List<Integer>` with `2 * (rows + cols) - 4` entries when both dimensions are at least 2.

**Example 1.** Input `m = [[1,2,3],[4,5,6],[7,8,9]]`, output `[1,2,3,6,9,8,7,4]`.

**Example 2.** Input `m = [[1,2],[3,4],[5,6]]`, output `[1,2,4,6,5,3]`.

**Hint.** Which two of the four passes can emit a cell that an earlier pass already emitted?

**Changed decision.** Basic case: one layer only, so the loop of layers disappears and the guards remain.

#### [Vary] Spiral Matrix (LeetCode 54)
<!-- id: mx-spiral-matrix -->

**Prerequisites.** The first exercise above.

**Problem.** Given an `rows x cols` matrix `m`, return all of its values in spiral order. Spiral order starts at `m[0][0]`, moves right along the first row, then down the last column, then left along the last row, then up the first column, and then repeats on the cells that remain.

**Constraints.** The limits are:
- **Shape** is rectangular with `1 <= rows, cols <= 10`.
- **Values** satisfy `-100 <= m[r][c] <= 100`.
- **Mutation** is not allowed; the method reads `m` only.
- **Return** is a `List<Integer>` with `rows * cols` entries.

**Example 1.** Input `m = [[2,4,6],[8,10,12],[14,16,18]]`, output `[2,4,6,12,18,16,14,8,10]`.

**Example 2.** Input `m = [[1,2],[3,4],[5,6],[7,8]]`, output `[1,2,4,6,8,7,5,3]`.

**Hint.** What do the four indexes enclose after each pass, and when does the rectangle become empty?

**Changed decision.** The loop repeats the four passes on the shrinking rectangle until it is empty.

#### [Boundary] Thin Remainder (LeetCode 54)
<!-- id: mx-thin-remainder -->

**Prerequisites.** The Vary exercise above.

**Problem.** A spiral walk over a matrix with `rows` rows and `cols` columns visits every cell in the order of Spiral Matrix. Return the zero-based position `[row, col]` of the last cell the walk visits. The method receives only the two dimensions and builds no matrix.

**Constraints.** The limits are:
- **rows** satisfies `1 <= rows <= 10^9`.
- **cols** satisfies `1 <= cols <= 10^9`.
- **Return** is an `int[]` of length 2.
- **Time** must not depend on `rows * cols`.

**Example 1.** Input `rows = 3, cols = 4`, output `[1,2]`.

**Example 2.** Input `rows = 4, cols = 1`, output `[3,0]`.

**Hint.** Remove full layers until the remaining rectangle has one row, one column or two rows. Which cell ends the walk in each shape?

**Changed decision.** Only the shape of the last thin remainder matters, so the guards of the third and fourth passes decide the answer and no values are read.

#### [Recognize] Spiral Matrix II (LeetCode 59)
<!-- id: mx-spiral-generate -->

**Prerequisites.** The Vary exercise above.

**Problem.** Given a positive integer `n`, return an `n x n` matrix whose cells hold the integers `1` to `n * n` in the order of a spiral walk that starts at the cell `[0][0]` and moves right first.

**Constraints.** The limits are:
- **n** satisfies `1 <= n <= 20`.
- **Values** are the integers `1` to `n * n`, each used once.
- **Return** is a new `int[n][n]`.
- **Space** is O(1) extra space besides the returned matrix.

**Example 1.** Input `n = 2`, output `[[1,2],[4,3]]`.

**Example 2.** Input `n = 4`, output `[[1,2,3,4],[12,13,14,5],[11,16,15,6],[10,9,8,7]]`.

**Hint.** Which statement in the four passes changes from reading `m[r][c]` to writing a counter?

**Changed decision.** The data flows in the opposite direction, because each pass writes the next counter value into a cell.
