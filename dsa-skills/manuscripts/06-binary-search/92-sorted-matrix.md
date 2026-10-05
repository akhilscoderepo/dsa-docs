<!-- lesson-kind: combination -->
<!-- lesson-id: sorted-matrix -->
## Search A Sorted Matrix

<!-- stage: context -->
### A Calibration Table With Millions Of Cells

A sensor calibration table is stored as a grid of readings, one row per device and one column per temperature step. Each row lists readings in ascending order. A technician asks whether the reading 22 appears anywhere in the table, for a grid of 2000 rows and 2000 columns. The program that checks every cell reads four million values for one question.

Some grids hold more order than each row alone. In one case, the whole grid is sorted when it is read row after row. In another case, the rows and the columns are sorted but the rows do not continue each other. The question is which kind of order a grid has, and how much of the grid a search can skip for each kind.

<!-- stage: contributions -->
### What The Shape And The Search Add

A matrix has a fixed shape of `rows` and `cols`. The shape converts a single number into a cell: the number `k` names the cell in row `k / cols` and column `k % cols`. With this conversion, the grid can be addressed as if it were one long array, without copying a value.

Binary search adds the ability to discard half of a sorted range with one comparison. It needs a range with a first and a last position, and the shape supplies that range as the numbers `0` to `rows * cols - 1`. The two parts need each other. The shape gives the search a range to cut, and the search gives the shape a reason to exist. The conversion holds only when the grid is sorted across rows, and a second kind of order needs a different move.

<!-- stage: naive -->
### Reading Every Cell

The direct method reads every cell, row by row, and returns true at the first cell that equals the target.

```java
static boolean containsByScan(int[][] matrix, int target) {
    for (int r = 0; r < matrix.length; r++) {
        for (int c = 0; c < matrix[r].length; c++) {
            if (matrix[r][c] == target) return true;
        }
    }
    return false;
}
```

For the grid `[[2,4,6,8],[11,13,15,17],[20,22,24,26]]` and the target 22, the method reads eight cells and returns true. For the target 12, it reads all twelve cells and returns false.

```predict
The same grid is read row after row as 2, 4, 6, 8, 11, 13, and so on. Is this long sequence ascending, and how many comparisons could a method use to find a value in a sequence of 4 million ascending numbers?

The sequence is ascending, because the last value of each row is smaller than the first value of the next row. A method can find a value in 4 million ascending numbers with about 22 comparisons, because 2^22 is about 4.2 million.
```

<!-- stage: bottleneck -->
### The Scan Ignores Row Order

The scan reads up to `rows * cols` cells, which is O(rows * cols), and it ignores the order inside each row. A missing target costs the full count, and the worst case is exactly the case in which the technician looks for a value that is not there.

The prediction shows the lost information. When the last value of each row is smaller than the first value of the next, reading the grid row after row produces one ascending sequence. One comparison with the middle cell then rules out half of all cells. The scan compares each cell with the target and learns nothing about its neighbors. The other kind of order, with sorted rows and columns that do not continue each other, needs a different argument, which this lesson gives after the first.

<!-- stage: insight -->
### Two Ways To Skip Cells

#### The Grid As One Sorted Sequence

Reading the cells row after row is called **row-major order**. When the grid is sorted in row-major order, the number `k` from 0 to `rows * cols - 1` is a **virtual index**, a position in the sequence that is computed from the shape and never stored. The cell is `matrix[k / cols][k % cols]`. A binary search over `[0, rows * cols - 1]` is then the exact search from the first lesson, with the cell read replacing the array read. It makes O(log(rows * cols)) comparisons.

<!-- names: virtual index, row-major order, staircase walk -->

#### Why Independent Order Needs Another Move

If every row and every column is sorted but a row does not continue the previous one, the row-major sequence is not sorted, and a virtual index would discard cells that hold the target. The matrix `[[1,4],[2,5]]` reads as 1, 4, 2, 5, and the middle comparison would mislead. One cell still has a useful property. The top-right cell is the largest value of its row and the smallest value of its column.

#### The Staircase Walk

The **staircase walk** starts at the top-right cell. If that value equals the target, the walk stops. If the value is larger than the target, the whole column below it holds larger values, so the walk moves one column left. If the value is smaller, the rest of the row to its left holds smaller values, so the walk moves one row down. Each step removes a row or a column, so the walk makes at most `rows + cols` steps. The cost is O(rows + cols), which is larger than the logarithmic cost of the virtual index, and it is the best this order allows with a single walk.

<!-- stage: variables -->
### The Shape And The Pointers

Both methods share the shape of the grid and differ in the state they keep.

- **rows** and **cols** are `matrix.length` and `matrix[0].length`, read once before any search.
- **lo** and **hi** are virtual indexes that bound the cells that may hold the target.
- **mid** is `lo + (hi - lo) / 2`, and its cell is `matrix[mid / cols][mid % cols]`.
- **row** and **col** are the coordinates of the staircase walk, starting at `(0, cols - 1)`.

A matrix with no rows has no `matrix[0]`, so `cols` cannot be read. A guard for an empty shape comes before every other line.

<!-- stage: trace -->
### One Index Search And One Staircase Walk

#### A Search With The Virtual Index

The grid is `[[2,4,6,8],[11,13,15,17],[20,22,24,26]]`, and the target is 15. The cells below are the twelve values in row-major order. The search starts with `lo = 0` and `hi = 11`. The first midpoint is index 5, the cell in row 1 and column 1 with value 13, which is below 15, so `lo` becomes 6. The next midpoint is index 8, the cell in row 2 and column 0 with value 20, which is above 15, so `hi` becomes 7. The midpoint at index 6 holds 15 in row 1 and column 2, and the search returns true.

```trace
{"cells":[2,4,6,8,11,13,15,17,20,22,24,26],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":11,"mid":-1},"vars":{"target":"15"},"note":"Start with the virtual indexes 0 to 11."},{"at":{"lo":6,"hi":11,"mid":5},"vars":{"row":"1","col":"1","value":"13"},"note":"Index 5 is row 1, column 1, and holds 13, which is below 15, so lo becomes 6."},{"at":{"lo":6,"hi":7,"mid":8},"vars":{"row":"2","col":"0","value":"20"},"note":"Index 8 is row 2, column 0, and holds 20, which is above 15, so hi becomes 7."},{"at":{"lo":6,"hi":7,"mid":6},"vars":{"row":"1","col":"2","value":"15"},"note":"Index 6 is row 1, column 2, and holds 15, which equals the target, so the search returns true."}]}
```

#### A Walk Along The Staircase

The grid is `[[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]]`, which is sorted by rows and by columns but not as one sequence. The target is 13. The pointer `cell` below holds `row * 4 + col`. The walk starts at the top-right value 11, which is below 13, and moves down. The value 12 is below 13, so it moves down again. The value 16 is above 13, so the walk moves left to 9, then down to 14, then left to 13, and stops.

```trace
{"cells":[1,4,7,11,2,5,8,12,3,6,9,16,10,13,14,17],"pointers":["cell"],"steps":[{"at":{"cell":3},"vars":{"target":"13","value":"11"},"note":"The value 11 is below 13, so the rest of its row to the left is too small and the walk moves down."},{"at":{"cell":7},"vars":{"target":"13","value":"12"},"note":"The value 12 is below 13, so the rest of its row to the left is too small and the walk moves down."},{"at":{"cell":11},"vars":{"target":"13","value":"16"},"note":"The value 16 is above 13, so the column below it is too large and the walk moves left."},{"at":{"cell":10},"vars":{"target":"13","value":"9"},"note":"The value 9 is below 13, so the rest of its row to the left is too small and the walk moves down."},{"at":{"cell":14},"vars":{"target":"13","value":"14"},"note":"The value 14 is above 13, so the column below it is too large and the walk moves left."},{"at":{"cell":13},"vars":{"target":"13","value":"13"},"note":"The value 13 equals the target, so the walk returns true."}]}
```

<!-- stage: code -->
### Both Methods In Java

```java
static boolean containsVirtual(int[][] matrix, int target) {
    if (matrix.length == 0 || matrix[0].length == 0) return false;
    int cols = matrix[0].length;
    int lo = 0, hi = matrix.length * cols - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int value = matrix[mid / cols][mid % cols];
        if (value == target) return true;
        if (value < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}

static boolean containsStaircase(int[][] matrix, int target) {
    if (matrix.length == 0 || matrix[0].length == 0) return false;
    int row = 0, col = matrix[0].length - 1;
    while (row < matrix.length && col >= 0) {
        int value = matrix[row][col];
        if (value == target) return true;
        if (value > target) col--;
        else row++;
    }
    return false;
}
```

The product `matrix.length * cols` fits an `int` for grids up to about 46000 by 46000, and the exercises stay far below that. The first method requires a rectangular grid, and it reads `cols` once from the first row.

<!-- stage: applicability -->
### Which Order Does The Grid Have

#### The Invariant

The invariant of the virtual search is that the target, if present, has a virtual index in `[lo, hi]`. The invariant of the walk is that the target, if present, lies in the rows from `row` down and the columns from `col` leftward. Each comparison keeps the invariant and shrinks the region, so an empty region proves that the target is absent.

#### The False Friend

A matrix with sorted rows and sorted columns looks like the sorted sequence of the first case. It is the false friend of the virtual index. The conversion `k / cols` and `k % cols` works for every grid, but the discarded half is only safe when the sequence is ascending. In the grid `[[1,4],[2,5]]`, a search for the value 2 compares it with 4 first, moves left, and misses the value.

#### Reading The Contract

Look for the sentence that states how the first value of a row relates to the last value of the previous row. If it says "greater than", the virtual index applies, and the cost is logarithmic in the number of cells. If the contract says only that rows and columns are sorted, use the staircase walk. An unclear contract is a reason to ask, because the wrong choice returns wrong answers without any error.

<!-- stage: exercises -->
### Exercises

#### [Build] Search A 2D Matrix (LeetCode 74)
<!-- id: bs-matrix-contains -->

**Prerequisites.** The exact search of the first lesson and the virtual index of this lesson.

**Problem.** An `m` by `n` matrix of integers has ascending rows, and the first value of each row is larger than the last value of the previous row. Given the matrix and an integer `target`, return `true` when `target` occurs in the matrix and `false` otherwise.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 100`.
- **Values** are distinct `int` values in row-major ascending order.
- **Target** is any `int`.
- **Mutation** does not occur; the matrix does not change.

**Example 1.** Input `matrix = [[2,4,6,8],[11,13,15,17],[20,22,24,26]]` and `target = 22`, output `true`.

**Example 2.** Input `matrix = [[2,4,6,8],[11,13,15,17],[20,22,24,26]]` and `target = 12`, output `false`.

**Hint.** Search the numbers from 0 to `m * n - 1`. Which formulas turn a number into a row and a column?

**Changed decision.** Basic case: the search returns a boolean and reads cells through the virtual index.

#### [Vary] First Matrix Position (Author exercise)
<!-- id: bs-matrix-first-position -->

**Prerequisites.** The previous exercise and the first-and-last lesson.

**Problem.** An `m` by `n` matrix of integers is sorted in non-decreasing order when read row after row, and values may repeat. Given the matrix and an integer `target`, return `[row, col]` of the first occurrence of `target` in row-major order, or `[-1, -1]` when it does not occur.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 100`.
- **Values** are `int` values, non-decreasing in row-major order.
- **Answer** is a coordinate pair or `[-1, -1]`.
- **Mutation** does not occur; the matrix does not change.

**Example 1.** Input `matrix = [[1,2,2],[2,2,3],[3,3,9]]` and `target = 2`, output `[0,1]`.

**Example 2.** Input `matrix = [[1,2,2],[2,2,3],[3,3,9]]` and `target = 4`, output `[-1,-1]`.

**Hint.** Search for the first virtual index with a value at least `target`. Convert it to coordinates only at the end.

**Changed decision.** The answer is a coordinate pair, so the search finds the first matching virtual index and converts it once.

#### [Boundary] Empty Shape (Author exercise)
<!-- id: bs-matrix-empty-shape -->

**Prerequisites.** Both exercises above.

**Problem.** A matrix of integers may have zero rows, or rows with zero columns. When it has cells, it is sorted in strictly ascending order when read row after row. Given the matrix and an integer `target`, return `true` when `target` occurs and `false` otherwise, without throwing an exception.

**Constraints.** The limits are:
- **Rows** satisfy `0 <= m <= 100`.
- **Columns** satisfy `0 <= n <= 100`, equal in all rows.
- **Values** are distinct `int` values in row-major ascending order.
- **Answer** is a boolean for every shape.

**Example 1.** Input `matrix = []` and `target = 5`, output `false`.

**Example 2.** Input `matrix = [[]]` and `target = 5`, output `false`.

**Hint.** Which expression fails first on a matrix with zero rows? Place the guard before it.

**Changed decision.** The shape itself can be empty, so `cols` and the last virtual index are read only after a guard.

#### [Recognize] Search A 2D Matrix II (LeetCode 240)
<!-- id: bs-matrix-staircase -->

**Prerequisites.** All exercises above.

**Problem.** An `m` by `n` matrix of integers has every row sorted in ascending order and every column sorted in ascending order, and a row does not have to continue the previous row. Given the matrix and an integer `target`, return `true` when `target` occurs and `false` otherwise.

**Constraints.** The limits are:
- **Shape** is `1 <= m, n <= 300`.
- **Values** are `int` values, ascending along every row and every column.
- **Order** across rows is not guaranteed.
- **Cost** should be O(m + n).

**Example 1.** Input `matrix = [[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]]` and `target = 13`, output `true`.

**Example 2.** Input the same matrix and `target = 15`, output `false`.

**Hint.** Start at the top-right cell. What does a value larger than the target tell you about its column?

**Changed decision.** The row-major sequence is not sorted, so each comparison removes a whole row or column in place of half of the cells.
