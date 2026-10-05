<!-- lesson-kind: standard -->
<!-- lesson-id: two-dimensional-prefix -->
## Sum A Rectangle In Constant Time

<!-- stage: context -->
### Selecting A Region On A Map

A weather application shows a grid of 1,000 by 1,000 map cells, and each cell holds the rainfall measured in that area. The user drags a rectangle over the map, and the application shows the total rainfall inside it. The user keeps dragging, and each new rectangle triggers a new total. A rectangle that covers most of the map adds close to a million numbers, and the display lags behind the mouse.

The readings do not change while the user drags. This lesson extends the idea of the earlier prefix sums from a line to a grid. The question is how a program answers the sum of any rectangle with a fixed number of reads.

<!-- stage: naive -->
### Adding Every Cell Of The Rectangle

The direct method adds the cells of the rectangle row by row. A query is the four numbers `r1`, `c1`, `r2` and `c2`, where the corners `(r1, c1)` and `(r2, c2)` both belong to the rectangle.

```java
static long rectangleSum(int[][] grid, int r1, int c1, int r2, int c2) {
    long sum = 0;
    for (int r = r1; r <= r2; r++) {
        for (int c = c1; c <= c2; c++) sum += grid[r][c];
    }
    return sum;
}
```

For the grid `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]` and the rectangle from `(1, 1)` to `(2, 2)`, the method adds 5, 6, 8 and 9 and returns 28.

```predict
The grid has 1,000 rows and 1,000 columns, and 100,000 queries each cover the whole grid. How many additions does `rectangleSum` perform in total?

It performs 100,000 times 1,000,000 additions, which is 100,000,000,000. A query costs the area of its rectangle, so the cost is O(m * n) per query for an m by n grid.
```

<!-- stage: bottleneck -->
### Every Query Pays For Its Area

A query costs as many additions as its rectangle has cells. In the worst case that is `m * n`, so `q` queries cost O(m * n * q). The grid does not change, and overlapping rectangles repeat the same additions.

The earlier lessons removed this cost for a line, by storing the sum of everything before each position. A grid has two directions, and a rectangle has a corner in each of them. The question is whether stored sums of the rectangles that start at the top-left corner can produce any other rectangle, using the subtraction that worked for lines.

<!-- stage: insight -->
### Store Sums From The Top-Left Corner

A **prefix matrix** `P` has `m + 1` rows and `n + 1` columns. The entry `P[r][c]` is the sum of all grid cells in the rows `0` through `r - 1` and the columns `0` through `c - 1`. It sums the rectangle that starts at the top-left cell and ends just before row `r` and column `c`.

#### The Border Of Zeros

The first row and the first column of `P` are 0, because a rectangle with zero rows or zero columns has no cells. This is a **sentinel border**, which means extra entries that exist so that the formulas need no special case at the edges. The cell `grid[r][c]` is the last cell that `P[r + 1][c + 1]` adds.

#### Building Each Entry From Three Neighbours

The entry `P[r + 1][c + 1]` combines the entry above, the entry to the left and the cell itself. Adding the entry above and the entry to the left counts their shared part twice. The shared part is `P[r][c]`, so it is subtracted once. The formula is `P[r + 1][c + 1] = P[r][c + 1] + P[r + 1][c] - P[r][c] + grid[r][c]`.

#### A Query By Inclusion-Exclusion

**Inclusion-exclusion** counts a union of regions by adding the regions and subtracting their overlaps. The rectangle from `(r1, c1)` to `(r2, c2)` equals the large rectangle `P[r2 + 1][c2 + 1]`, minus the strip above, `P[r1][c2 + 1]`, minus the strip on the left, `P[r2 + 1][c1]`. The two subtractions remove the corner region `P[r1][c1]` twice, so the formula adds it back once. A query reads four entries, so it costs O(1), and the construction of `P` costs O(m * n).

<!-- names: prefix matrix, sentinel border, inclusion-exclusion -->

<!-- stage: variables -->
### Seven Names And Their Roles

The query reads four entries of the matrix. The code writes the matrix as `p`, and this list names the four reads `whole`, `above`, `left` and `corner` for explanation only.

- **P** is the `long` matrix with `m + 1` rows and `n + 1` columns, built once and never changed.
- **r1** and **c1** are the top row and the left column of the rectangle.
- **r2** and **c2** are the bottom row and the right column of the rectangle, both inside it.
- **whole** is `P[r2 + 1][c2 + 1]`, the sum from the top-left cell to the bottom-right corner.
- **above** is `P[r1][c2 + 1]`, the rows that lie over the rectangle.
- **left** is `P[r2 + 1][c1]`, the columns that lie to its left.
- **corner** is `P[r1][c1]`, the region that the two subtractions both remove, so the formula adds it back.

<!-- stage: trace -->
### Two Queries On One Matrix

#### A Rectangle In The Lower Right

The grid is `[[1, 2, 3], [4, 5, 6], [7, 8, 9]]`. Its prefix matrix has four rows and four columns. The sixteen cells below list it row by row, so the entry `P[r][c]` sits at position `4 * r + c`. The query is the rectangle from `(1, 1)` to `(2, 2)`. The four reads are 45, 6, 12 and 1, and the answer is `45 - 6 - 12 + 1 = 28`.

```trace
{"cells":[0,0,0,0,0,1,3,6,0,5,12,21,0,12,27,45],"pointers":["whole","above","left","corner"],"steps":[{"at":{"whole":-1,"above":-1,"left":-1,"corner":-1},"vars":{"query":"(1,1) to (2,2)"},"note":"The prefix matrix is ready. The query reads four entries, and the pointers will mark them in turn."},{"at":{"whole":15,"above":-1,"left":-1,"corner":-1},"vars":{"total":"45"},"note":"Start with whole = P[3][3] = 45, the sum from the top-left cell to the bottom-right corner."},{"at":{"whole":15,"above":7,"left":-1,"corner":-1},"vars":{"total":"45 - 6 = 39"},"note":"Subtract above = P[1][3] = 6, the rows over the rectangle."},{"at":{"whole":15,"above":7,"left":13,"corner":-1},"vars":{"total":"39 - 12 = 27"},"note":"Subtract left = P[3][1] = 12, the columns to its left."},{"at":{"whole":15,"above":7,"left":13,"corner":5},"vars":{"total":"27 + 1 = 28"},"note":"Add back the corner P[1][1] = 1, which both subtractions removed."}]}
```

#### A Rectangle Of One Cell

The query is the rectangle from `(1, 1)` to `(1, 1)`, which holds only the value 5. The four reads are `P[2][2] = 12`, `P[1][2] = 3`, `P[2][1] = 5` and `P[1][1] = 1`. The answer is `12 - 3 - 5 + 1 = 5`, the cell itself.

```trace
{"cells":[0,0,0,0,0,1,3,6,0,5,12,21,0,12,27,45],"pointers":["whole","above","left","corner"],"steps":[{"at":{"whole":-1,"above":-1,"left":-1,"corner":-1},"vars":{"query":"(1,1) to (1,1)"},"note":"The prefix matrix is ready. The query reads four entries, and the pointers will mark them in turn."},{"at":{"whole":10,"above":-1,"left":-1,"corner":-1},"vars":{"total":"12"},"note":"Start with whole = P[2][2] = 12, the sum from the top-left cell to the bottom-right corner."},{"at":{"whole":10,"above":6,"left":-1,"corner":-1},"vars":{"total":"12 - 3 = 9"},"note":"Subtract above = P[1][2] = 3, the rows over the rectangle."},{"at":{"whole":10,"above":6,"left":9,"corner":-1},"vars":{"total":"9 - 5 = 4"},"note":"Subtract left = P[2][1] = 5, the columns to its left."},{"at":{"whole":10,"above":6,"left":9,"corner":5},"vars":{"total":"4 + 1 = 5"},"note":"Add back the corner P[1][1] = 1, which both subtractions removed."}]}
```

<!-- stage: code -->
### Build And Query In Java

```java
static long[][] buildPrefix(int[][] grid) {
    int m = grid.length, n = grid[0].length;
    long[][] p = new long[m + 1][n + 1];
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) {
            p[r + 1][c + 1] = p[r][c + 1] + p[r + 1][c] - p[r][c] + grid[r][c];
        }
    }
    return p;
}

static long rectangleSum(long[][] p, int r1, int c1, int r2, int c2) {
    return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1];
}
```

Java fills a new array with zeros, so the border is already in place. The query never reads a negative index, even when `r1` or `c1` is 0, because it reads row `r1` and column `c1` of `P` and not row `r1 - 1`. The matrix has type `long`, because a million cells of size 10^9 add up past the `int` range.

<!-- stage: applicability -->
### When The Matrix Of Sums Fits

#### The Invariant

The invariant is that `P[r][c]` equals the sum of the cells in the rows `0` through `r - 1` and the columns `0` through `c - 1`, for all `r` and `c` from 0 up to `m` and `n`. The inclusion-exclusion step then removes exactly the rows above and the columns to the left, and it adds back the corner region once.

#### The False Friend

The false friend is a single prefix array over the rows. It looks sufficient, because it also answers range sums in constant time. A rectangle needs a range of columns inside each row, so the sums of whole rows are not enough. One prefix array per row would answer a query in O(rows), which is better than a loop over cells and worse than constant time.

#### Conditions That Break The Fit

The grid must not change between queries, since one change alters every entry to the lower right. The query must ask for a rectangle with sides parallel to the axes, and a diagonal or L-shaped region needs a different method. The operation must have an inverse, so the same formula does not give a maximum over a rectangle.

<!-- stage: exercises -->
### Exercises

#### [Build] Range Sum Query 2D Immutable (LeetCode 304)
<!-- id: ps-matrix-sum-304 -->

**Prerequisites.** The prefix matrix and the four-read formula of this lesson.

**Problem.** Given an integer matrix `matrix` and a list of queries `[r1, c1, r2, c2]`, return for each query the sum of all cells `matrix[r][c]` with `r1 <= r <= r2` and `c1 <= c <= c2`.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 200`.
- **Values** are `int` values with `|matrix[r][c]| <= 10^4`.
- **Queries** number at most `10^4`, with `0 <= r1 <= r2 < m` and `0 <= c1 <= c2 < n`.
- **Mutation** does not occur; `matrix` does not change.

**Example 1.** Input `matrix = [[1,2,3],[4,5,6],[7,8,9]]` and queries `[[1,1,2,2],[0,0,2,2]]`, output `[28,45]`.

**Example 2.** Input `matrix = [[-4]]` and queries `[[0,0,0,0]]`, output `[-4]`.

**Hint.** Build the matrix with one extra row and one extra column of zeros. Which four entries bound the rectangle?

**Changed decision.** Basic case: filling the matrix costs `m * n` once, and each query reads four entries.

#### [Vary] Matrix Block Sum (LeetCode 1314)
<!-- id: ps-block-sum-1314 -->

**Prerequisites.** The first exercise above.

**Problem.** Given an `m` by `n` matrix `mat` and an integer `k`, return the matrix `answer` where `answer[i][j]` is the sum of all cells `mat[r][c]` with `i - k <= r <= i + k` and `j - k <= c <= j + k` that lie inside the matrix. Rows and columns outside the matrix are ignored.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 100`.
- **Values** are `int` values with `1 <= mat[i][j] <= 100`.
- **Radius** satisfies `0 <= k <= 100`.
- **Clipping** is required near the edges.

**Example 1.** Input `mat = [[1,2,3],[4,5,6]]` and `k = 1`, output `[[12,21,16],[12,21,16]]`.

**Example 2.** Input `mat = [[5]]` and `k = 0`, output `[[5]]`.

**Hint.** For each cell, clamp the four corners to the grid with `Math.max` and `Math.min` before the four reads.

**Changed decision.** Every cell issues one query, and clamping the corners keeps the formula valid at the edges.

#### [Boundary] Single Cell Rectangle (Author exercise)
<!-- id: ps-single-cell -->

**Prerequisites.** The first exercise and the second trace of this lesson.

**Problem.** Given a prefix matrix `P` with `m + 1` rows and `n + 1` columns, whose first row and first column are zero, return the original `m` by `n` matrix. Recover each cell as the sum of the rectangle that contains only that cell.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 200`.
- **Input** is a valid prefix matrix of some matrix with `int` values.
- **Values** of the original matrix satisfy `|value| <= 10^4`.
- **Return type** is `int[][]` of shape `m` by `n`.

**Example 1.** Input `P = [[0,0,0],[0,3,5],[0,4,9]]`, output `[[3,2],[1,3]]`.

**Example 2.** Input `P = [[0,0],[0,-6]]`, output `[[-6]]`.

**Hint.** The cell `(r, c)` is the rectangle from `(r, c)` to `(r, c)`. Which four entries of `P` does the formula read?

**Changed decision.** The rectangle shrinks to one cell, so the inclusion-exclusion formula must return exactly that cell.

#### [Recognize] Whole Matrix Query (Author exercise)
<!-- id: ps-origin-rectangle -->

**Prerequisites.** All exercises above.

**Problem.** Given an integer matrix `matrix`, return the largest sum among all rectangles whose top-left cell is `(0, 0)`. Each such rectangle is fixed by its bottom-right cell `(r, c)`, and the whole matrix is one of the candidates.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 200`.
- **Values** are `int` values with `|matrix[r][c]| <= 10^4`.
- **Candidates** are the `m * n` rectangles that start at the origin.
- **Return type** is `long`.

**Example 1.** Input `matrix = [[1,-2],[-3,4]]`, output 1.

**Example 2.** Input `matrix = [[-5]]`, output -5.

**Hint.** Every candidate starts at row 0 and column 0. Which entry of the prefix matrix is already the sum of such a rectangle, and why does the border keep the indexes non-negative?

**Changed decision.** All queries touch the first row and the first column, so the border of zeros decides whether any index is negative.
