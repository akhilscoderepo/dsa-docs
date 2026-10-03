<!-- lesson-kind: standard -->
<!-- lesson-id: spiral-boundaries -->
## Spiral Boundaries

<!-- stage: context -->
### Painting A Wall In Strips

A painter has to coat a rectangular wall, and she does it in strips. She paints the top strip from left to right, then the right strip from top to bottom, then the bottom strip from right to left, then the left strip from bottom to top. Each strip is one tile wide and she never paints anything twice. When the four strips are done, the unpainted part is a smaller rectangle in the middle of the same shape, and she starts the next round on it.

To remember where she is, she needs no tally of painted tiles. She only needs to know the edges of the part still unpainted: where its top is, where its bottom is, and where its left and right are. A paint line moves inward every time she finishes a strip. When the unpainted rectangle is gone, so is the job.

<!-- stage: naive -->
### Mark Visited Tiles In A Grid

A direct translation keeps a boolean grid the same size as the wall, marks each tile as it is visited, and turns whenever the next tile is off the wall or marked.

```java
static List<Integer> spiralByVisitedGrid(int[][] m) {
    int rows = m.length, cols = m[0].length;
    boolean[][] seen = new boolean[rows][cols];
    int[] dr = {0, 1, 0, -1}, dc = {1, 0, -1, 0};
    List<Integer> out = new ArrayList<>();
    int r = 0, c = 0, d = 0;
    for (int k = 0; k < rows * cols; k++) {
        out.add(m[r][c]);
        seen[r][c] = true;
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || seen[nr][nc]) {
            d = (d + 1) % 4;
            nr = r + dr[d]; nc = c + dc[d];
        }
        r = nr; c = nc;
    }
    return out;
}
```

It is correct on every rectangle and it is the heading-and-visited simulation from the earlier lesson. For a three by four wall it lists the cells in the painter's order.

<!-- stage: bottleneck -->
### A Whole Grid For Four Numbers

The simulation visits each tile once, so the time is O(rows * cols), which is the best possible, since every tile must be listed. The extra memory is the problem: the `seen` grid has `rows * cols` cells, so the space is O(rows * cols) on top of the output. For a large matrix that is as much memory again for a fact the painter held in her head with four numbers.

The grid is also checked on every step, and it hides a design question. The unvisited part is always a rectangle, because strips are peeled off the outside. A rectangle is described completely by its top, bottom, left and right edges. Storing a mark per tile records more than is needed, and the extra detail is where bugs hide, since the program must keep the marks and the turns consistent.

<!-- stage: insight -->
### Four Edges Enclose The Unvisited Rectangle

Keep four **boundary variables**: `top`, `bottom`, `left` and `right`. They are the indices of the first and last unvisited row and the first and last unvisited column. The unvisited tiles are exactly those with a row between `top` and `bottom` and a column between `left` and `right`. One round of the spiral peels off a **layer**, the outer ring of that rectangle, in four strips: the top row, the right column, the bottom row and the left column.

After the top row is emitted, `top` moves down by one. After the right column, `right` moves left by one. After the bottom row, `bottom` moves up by one. After the left column, `left` moves right by one. The rectangle shrinks on all four sides, and the loop runs while it is non-empty, meaning `top <= bottom` and `left <= right`.

<!-- names: boundary variables, layer, thin remainder -->

The delicate case is the **thin remainder**, a layer that has only one row or one column left. Take a single row. The top strip emits all of it. After `top` moves down, `top` exceeds `bottom`, so the rectangle is already empty, yet the bottom strip would run if it were not guarded and emit the same row again in reverse. For a single column the right strip emits it and the left strip would emit it again. So the bottom strip needs the guard `top <= bottom`, and the left strip needs `left <= right`.

The invariant is that the four variables enclose exactly the unvisited rectangle, and each strip is guarded by the condition that its row or column still exists. The heading simulation, by comparison, keeps its state in a cursor and a visited record, and its failure modes are different: a wrong turn rather than a repeated strip.

<!-- stage: variables -->
### Top, Bottom, Left, Right

All four start at the edges of the matrix: `top = 0`, `bottom = rows - 1`, `left = 0`, `right = cols - 1`. Each is changed once per layer, after the strip that uses it, and never changes otherwise. The strips read the matrix with a plain `for` loop over the free index, and the fixed index is one of the boundary variables. Before the bottom strip, check that `top <= bottom` still holds, and before the left strip, check that `left <= right` still holds, since the first two strips may already have emptied the rectangle.

<!-- stage: trace -->
### A Wide Wall And A Row

Take `[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]`, which has three rows and four columns. The first layer begins with the top row, so the output starts 1, 2, 3, 4, and `top` becomes 1. The right column runs from row 1 to row 2, adding 8 and 12, and `right` becomes 2. The bottom row, with `top` at 1 and `bottom` at 2, runs from column 2 down to column 0, adding 11, 10 and 9, and `bottom` becomes 1. The left column runs from row 1 up to row 1, adding 5, and `left` becomes 1.

The rectangle is now rows 1 to 1 and columns 1 to 2, a single row of two tiles. The top row emits 6 and 7, and `top` becomes 2, which exceeds `bottom`. The right column loop is empty. The guard before the bottom strip fails, so nothing repeats, and the output is complete at twelve values. The step to study is the failed guard on the last layer.

A second picture is the single row `[[1, 2, 3]]`. The top strip emits 1, 2 and 3, and then the guard `top <= bottom` fails, which prevents the bottom strip from emitting the row again in reverse.

```trace
{"cells":[1,2,3,4,5,6,7,8,9,10,11,12],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"strip":"top","top":0,"bottom":2,"left":0,"right":3},"note":"Emit 1 from the top strip at (0, 0). The boundaries are top 0, bottom 2, left 0, right 3."},{"at":{"cell":1},"vars":{"strip":"top","top":0,"bottom":2,"left":0,"right":3},"note":"Emit 2 from the top strip at (0, 1). The boundaries are top 0, bottom 2, left 0, right 3."},{"at":{"cell":2},"vars":{"strip":"top","top":0,"bottom":2,"left":0,"right":3},"note":"Emit 3 from the top strip at (0, 2). The boundaries are top 0, bottom 2, left 0, right 3."},{"at":{"cell":3},"vars":{"strip":"top","top":0,"bottom":2,"left":0,"right":3},"note":"Emit 4 from the top strip at (0, 3). The boundaries are top 0, bottom 2, left 0, right 3."},{"at":{"cell":7},"vars":{"strip":"right","top":1,"bottom":2,"left":0,"right":3},"note":"Emit 8 from the right strip at (1, 3). The boundaries are top 1, bottom 2, left 0, right 3."},{"at":{"cell":11},"vars":{"strip":"right","top":1,"bottom":2,"left":0,"right":3},"note":"Emit 12 from the right strip at (2, 3). The boundaries are top 1, bottom 2, left 0, right 3."},{"at":{"cell":10},"vars":{"strip":"bottom","top":1,"bottom":2,"left":0,"right":2},"note":"Emit 11 from the bottom strip at (2, 2). The boundaries are top 1, bottom 2, left 0, right 2."},{"at":{"cell":9},"vars":{"strip":"bottom","top":1,"bottom":2,"left":0,"right":2},"note":"Emit 10 from the bottom strip at (2, 1). The boundaries are top 1, bottom 2, left 0, right 2."},{"at":{"cell":8},"vars":{"strip":"bottom","top":1,"bottom":2,"left":0,"right":2},"note":"Emit 9 from the bottom strip at (2, 0). The boundaries are top 1, bottom 2, left 0, right 2."},{"at":{"cell":4},"vars":{"strip":"left","top":1,"bottom":1,"left":0,"right":2},"note":"Emit 5 from the left strip at (1, 0). The boundaries are top 1, bottom 1, left 0, right 2."},{"at":{"cell":5},"vars":{"strip":"top","top":1,"bottom":1,"left":1,"right":2},"note":"Emit 6 from the top strip at (1, 1). The boundaries are top 1, bottom 1, left 1, right 2."},{"at":{"cell":6},"vars":{"strip":"top","top":1,"bottom":1,"left":1,"right":2},"note":"Emit 7 from the top strip at (1, 2). The boundaries are top 1, bottom 1, left 1, right 2."},{"at":{"cell":-1},"vars":{"strip":"bottom skipped","top":2,"bottom":1,"left":1,"right":1},"note":"The guard top <= bottom fails, since top is 2 and bottom is 1, so the bottom strip is skipped and nothing repeats."}]}
```

```trace
{"cells":[1,2,3],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"strip":"top","top":0,"bottom":0,"left":0,"right":2},"note":"Emit 1 from the top strip at (0, 0). The boundaries are top 0, bottom 0, left 0, right 2."},{"at":{"cell":1},"vars":{"strip":"top","top":0,"bottom":0,"left":0,"right":2},"note":"Emit 2 from the top strip at (0, 1). The boundaries are top 0, bottom 0, left 0, right 2."},{"at":{"cell":2},"vars":{"strip":"top","top":0,"bottom":0,"left":0,"right":2},"note":"Emit 3 from the top strip at (0, 2). The boundaries are top 0, bottom 0, left 0, right 2."},{"at":{"cell":-1},"vars":{"strip":"bottom skipped","top":1,"bottom":0,"left":0,"right":1},"note":"The guard top <= bottom fails, since top is 1 and bottom is 0, so the bottom strip is skipped and nothing repeats."}]}
```

<!-- stage: code -->
### Four Strips With Two Guards

```java
static List<Integer> spiralOrder(int[][] m) {
    List<Integer> out = new ArrayList<>();
    int top = 0, bottom = m.length - 1, left = 0, right = m[0].length - 1;
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

static int[][] spiralFillByLayers(int n) {
    int[][] g = new int[n][n];
    int top = 0, bottom = n - 1, left = 0, right = n - 1, v = 1;
    while (top <= bottom && left <= right) {
        for (int c = left; c <= right; c++) g[top][c] = v++;
        top++;
        for (int r = top; r <= bottom; r++) g[r][right] = v++;
        right--;
        if (top <= bottom) { for (int c = right; c >= left; c--) g[bottom][c] = v++; bottom--; }
        if (left <= right) { for (int r = bottom; r >= top; r--) g[r][left] = v++; left++; }
    }
    return g;
}
```

The first method reads each cell once and the second writes each cell once, so both take O(rows * cols) time. They use O(1) extra space apart from the output, since the boundary variables are four integers. The matrix must have at least one row and one column, because `m[0].length` is read once at the start.

<!-- stage: applicability -->
### When The Output Peels Rings

Use shrinking boundaries when a rectangle is consumed from the outside in, strip by strip, so that the unvisited part is always a rectangle. The invariant is that the four boundary variables enclose exactly the unvisited rectangle, and every strip is guarded by the existence of its row or column. The same code reads a matrix in spiral order or writes values into it.

The false friend is the heading simulation, which gives the same order. It carries a cursor, a heading and a visited record, so it handles shapes with holes or obstacles, where the unvisited part is not a rectangle. Shrinking boundaries cannot do that. In return it needs no visited record, and its mistakes are repeated strips on thin remainders and not wrong turns. Another false friend is a spiral that does not peel rings, such as the walker of the previous lesson that wanders outside the grid.

For Java, pick the guards with care: the top-row and right-column strips need no guard, since the loop condition has just ensured the rectangle is non-empty. Use `List<Integer>` for output of unknown order or an `int[]` of size `rows * cols` when the size is known, and avoid reading `m[0].length` on an empty matrix.

<!-- stage: exercises -->
### Exercises

#### [Build] One Ring (Author exercise)
<!-- id: mx-one-ring -->

**Prerequisites.** The structured-traversal lesson; the shape-contract lesson.

**Problem.** List the cells on the outer ring of a rectangular matrix in clockwise order, starting at the top-left cell and going right. Every cell of the ring appears exactly once, including when the matrix has a single row or a single column.

**Constraints.** 1 <= rows, cols <= 100. The matrix is rectangular and has at least one row and one column.

**Example 1.** Input `matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]`, output `[1, 2, 3, 4, 8, 12, 11, 10, 9, 5]`.

**Example 2.** Input `matrix = [[7, 8, 9]]`, output `[7, 8, 9]`, since the single row is the whole ring.

**Hint.** Which strip starts at which corner? Which strips must be skipped when there is only one row or one column?

**Changed decision.** First rung: four strips are emitted without repeating corners, and the thin shapes need guards.

#### [Vary] Spiral Matrix (LeetCode 54)
<!-- id: mx-spiral-matrix -->

**Prerequisites.** The one-ring exercise above.

**Problem.** Given a rectangular matrix, return all of its elements in clockwise spiral order, starting at the top-left cell.

**Constraints.** 1 <= rows, cols <= 10 and -100 <= cell <= 100. Use four boundary variables and no visited record.

**Example 1.** Input `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]`, output `[1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8]`.

**Example 2.** Input `matrix = [[1, 2], [3, 4], [5, 6]]`, output `[1, 2, 4, 6, 5, 3]`.

**Hint.** After one ring is emitted, what rectangle remains, and how do the four variables describe it?

**Changed decision.** The single ring becomes a repeated peeling, with the four edges moving inward after each strip.

#### [Boundary] Thin Remainder (LeetCode 54)
<!-- id: mx-thin-remainder -->

**Prerequisites.** The two exercises above.

**Problem.** Show what the spiral does on a matrix that is a single row and on one that is a single column, and explain which guards stop the bottom and left strips from repeating cells. Return the spiral order for each.

**Constraints.** 1 <= rows, cols <= 10. One of the two dimensions is 1 in the main cases.

**Example 1.** Input `matrix = [[9, 8, 7]]`, output `[9, 8, 7]`, with the bottom strip skipped.

**Example 2.** Input `matrix = [[1], [2], [3], [4]]`, output `[1, 2, 3, 4]`, with the left strip skipped.

**Hint.** After the top strip of a single row, how do `top` and `bottom` compare? After the right strip of a single column, how do `left` and `right` compare?

**Changed decision.** The tests target the layers that shrink to one line, where an unguarded strip emits the line a second time.

#### [Recognize] Spiral Matrix II By Layers (LeetCode 59)
<!-- id: mx-spiral-layers-fill -->

**Prerequisites.** All three exercises above, and the spiral-matrix exercise from the direction-state lesson.

**Problem.** Generate an `n` by `n` matrix containing the numbers 1 to `n * n` in clockwise spiral order, using the same four boundary variables to decide where each number goes. The data flows in the opposite direction from the spiral-order exercise: values are written and not read.

**Constraints.** 1 <= n <= 20. Use no visited record and no heading.

**Example 1.** Input `n = 3`, output `[[1, 2, 3], [8, 9, 4], [7, 6, 5]]`.

**Example 2.** Input `n = 1`, output `[[1]]`.

**Hint.** What does each strip write, and what happens to the counter? Which guards still apply for the center of an odd-sized matrix?

**Changed decision.** The same shrinking layers are used to write a counter into the matrix instead of reading values out of it.
