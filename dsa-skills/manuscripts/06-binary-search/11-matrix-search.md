<!-- lesson-kind: combination -->
<!-- lesson-id: matrix-search -->
## Matrix Search

<!-- stage: context -->
### A Warehouse Of Numbered Bins

A warehouse stores small parts in a wall of bins, arranged in shelves with the same number of bins on every shelf. Each bin holds one part and is labeled with the part's number. The stock clerk filled the wall in a strict way: the labels grow from left to right along every shelf, and the first label on each shelf is larger than the last label on the shelf above it. Nothing else is promised.

A picker walks up with a part number and asks whether the warehouse has it, and if so, which shelf and which bin. The wall has thousands of bins, and pickers come all day. The clerk wants a way to answer that does not involve walking along the whole wall for every question.

<!-- stage: contributions -->
### What Each Part Brings

The matrix brings its shape. Because every row has the same number of columns, any cell can be named by a single number that counts the cells in reading order, from the first cell of the first row, along that row, then the next row and so on. A number `p` names the cell in row `p / cols` and column `p % cols`, and the other way round, row `r` and column `c` is number `r * cols + c`. The shape alone says nothing about where a target is, since it is only a way to address cells.

Binary search brings the discarding of half. It needs a sorted line of items, the ability to read the middle one, and a rule that tells which half cannot contain the answer. The matrix is not a line, so the search alone has nothing to run on. The two parts meet in the address translation: the search treats the cells as a line of `rows * cols` items, and the shape converts the number of the middle item into the row and column that must be read.

The recognition cue is a grid whose cells, read in reading order, are in increasing order, so that the whole grid is a sorted sequence folded into rows.

<!-- stage: naive -->
### Walk Past Every Bin

The direct approach is to visit the bins one by one, shelf after shelf, and stop when the label matches.

```java
static boolean containsByWalking(int[][] wall, int part) {
    for (int[] shelf : wall) {
        for (int label : shelf) {
            if (label == part) return true;
        }
    }
    return false;
}
```

It answers correctly for every wall, sorted or not, because it looks at every bin before it gives up.

<!-- stage: bottleneck -->
### Looking At Bins That Cannot Match

With R shelves of C bins the walk reads up to R times C labels per question, so it is O(R C), and thousands of questions over a wall of a million bins read billions of labels. The walk also ignores everything the clerk promised. When a label is smaller than the part, so is every label before it in reading order, and when it is larger, so is every label after it.

Read in order, the labels form one long increasing line that has been cut into shelves. A question about an increasing line of N items takes O(log N) probes with binary search, and here N is R times C, so O(log (R C)), which is the same as O(log R + log C). The only thing missing is a way to read the middle item of a line that exists only as a grid, which is a matter of arithmetic on the shelf width.

<!-- stage: insight -->
### A Grid Read As One Line

Number the cells from zero in **row-major order**, along the first row, then the second, and so on, and call each number a **virtual index**. The grid is never copied into a real line: the virtual index is only a name, and when the search needs the label at `mid`, it computes the row as `mid / cols` and the column as `mid % cols` and reads the grid there. The search itself is the exact search of the first lesson over positions `0` to `rows * cols - 1`, and the invariant is the same: if the part is in the wall, its virtual index lies in `[lo, hi]`.

A second way to use the same promise is to search by rows first. The first label of each shelf is also increasing, so a search over shelves finds the last shelf whose first label is at most the part, and the part can only be on that shelf. A second search along that shelf settles the question. Both ways cost O(log R + log C), and they agree on every wall. Neither route needs extra memory, copies or sorting beyond what the clerk already did. Think of a printed dictionary: a reader opens near the middle, checks the headword at the top of the page, and turns toward the right half, never reading the pages she skips. The virtual index is the page number, and the shelf width is what turns a page number into a spot on the shelf.

Before touching `cols` or computing the number of cells, the code needs a **shape guard**: a wall with no shelves has no first shelf whose width could be read, and a wall whose shelves are empty has zero cells, so the search must not start. The guard is a condition on the rows and columns, checked first, which returns the empty answer.

<!-- names: row-major order, virtual index, shape guard -->

All of this depends on the clerk's promise that the first label of a shelf exceeds the last label of the previous shelf. If only the rows and the columns are sorted separately, each shelf increasing and each column increasing from top to bottom, then a cell can be larger than a cell that comes later in reading order, so the grid is not a sorted line, and the virtual index is not a valid space to search. Such a grid has its own rule: start at the top right corner. If the label there is larger than the part, the whole column below it is larger too, so the column is discarded and the walk moves left. If it is smaller, the whole shelf to its left is smaller, so the shelf is discarded and the walk moves down. Each step discards a row or a column, so the walk takes at most R plus C steps. The corner is special because it is the only place where one comparison can eliminate a whole line in either direction: the opposite corners offer a single direction only, since a top left value is below everything near it and a bottom right value is above everything near it. Choosing the corner is therefore part of the proof, not a stylistic habit. A skeptic might ask whether swapping two shelves could matter; it would, because every elimination rests on knowing what lies beyond the probed cell.

<!-- stage: variables -->
### Positions, Rows And Columns

`rows` and `cols` are the dimensions of the grid, read once after the shape guard. `lo` and `hi` are virtual indices, with `lo` the first possible position and `hi` the last one. `mid` is a virtual index, and `mid / cols` and `mid % cols` give its row and column, which are computed only when a label must be read. For the corner walk, `r` and `c` are a row and a column that always name a cell inside the grid, and the invariant is that the part, if present, is inside the rows `r` and below and the columns `c` and to its left.

<!-- stage: trace -->
### Probing Positions In One Line

The first trace searches the wall of three shelves and four bins, with labels 1, 3, 5, 7, then 10, 11, 16, 20, then 23, 30, 34, 60, for the part 16. The cells are shown in reading order and the pointers are virtual indices. The step to study is the second: the middle position 8 is the first bin of the third shelf, and its label 23 is larger than 16, so everything from there on is discarded.

```trace
{"cells":["1","3","5","7","10","11","16","20","23","30","34","60"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":11,"mid":5},"vars":{"row":1,"col":1,"value":11},"note":"Position 5 is row 1, column 1, and its label is 11, smaller than 16, so lo moves to 6."},{"at":{"lo":6,"hi":11,"mid":8},"vars":{"row":2,"col":0,"value":23},"note":"Position 8 is row 2, column 0, and its label is 23, larger than 16, so hi moves to 7."},{"at":{"lo":6,"hi":7,"mid":6},"vars":{"row":1,"col":2,"value":16},"note":"Position 6 is row 1, column 2, and its label is 16, which is the part, so the answer is yes."}]}
```

The second trace uses the corner walk on a grid whose shelves and columns are each increasing, 1, 4, 7 then 2, 5, 8 then 3, 6, 9, looking for 6. The cells are listed in reading order, and the pointer marks the cell being read. Reading order is not increasing here, since 7 comes before 2, which is why the virtual index would fail. The step to study is the second: 4 is smaller than 6, so the rest of that shelf to its left is discarded and the walk moves down.

```trace
{"cells":["1","4","7","2","5","8","3","6","9"],"pointers":["read"],"steps":[{"at":{"read":2},"vars":{"row":0,"col":2,"value":7},"note":"The cell at row 0, column 2 holds 7, larger than 6, so its column below is discarded and the walk moves left."},{"at":{"read":1},"vars":{"row":0,"col":1,"value":4},"note":"The cell at row 0, column 1 holds 4, smaller than 6, so the rest of its shelf to the left is discarded and the walk moves down."},{"at":{"read":4},"vars":{"row":1,"col":1,"value":5},"note":"The cell at row 1, column 1 holds 5, smaller than 6, so the rest of its shelf to the left is discarded and the walk moves down."},{"at":{"read":7},"vars":{"row":2,"col":1,"value":6},"note":"The cell at row 2, column 1 holds 6, which is the part, so the answer is yes."}]}
```

<!-- stage: code -->
### Index Mapping, First Position And Corner Walk

```java
static boolean searchMatrix(int[][] a, int target) {
    if (a.length == 0 || a[0].length == 0) return false;
    int cols = a[0].length;
    int lo = 0, hi = a.length * cols - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int v = a[mid / cols][mid % cols];
        if (v == target) return true;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}

static int[] firstPosition(int[][] a, int target) {
    if (a.length == 0 || a[0].length == 0) return new int[] {-1, -1};
    int cols = a[0].length;
    int lo = 0, hi = a.length * cols;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid / cols][mid % cols] >= target) hi = mid;
        else lo = mid + 1;
    }
    if (lo == a.length * cols || a[lo / cols][lo % cols] != target) return new int[] {-1, -1};
    return new int[] {lo / cols, lo % cols};
}

static boolean searchSortedRowsAndColumns(int[][] a, int target) {
    if (a.length == 0 || a[0].length == 0) return false;
    int r = 0, c = a[0].length - 1;
    while (r < a.length && c >= 0) {
        int v = a[r][c];
        if (v == target) return true;
        if (v > target) c--;
        else r++;
    }
    return false;
}
```

The two mapped searches take O(log (R C)) time and the corner walk takes O(R + C) time, all with O(1) extra space. Each begins with the shape guard, so an empty grid returns before any index is read.

<!-- stage: applicability -->
### When A Grid Is One Sorted Line

Use the virtual index when the cells in reading order are increasing, that is, each row is sorted and each row starts above where the previous one ended, and every row has the same width. State the ordering promise before coding, since the whole search rests on it. The invariant is the exact-search one over virtual positions. For the first position of a value, use the first-true pattern over the same positions, and convert the final position back to a row and a column only after checking that it holds the target.

False friends come from the promise. A grid with sorted rows and sorted columns but no relation between a row's end and the next row's start is not a sorted line, so the virtual index gives wrong answers and the corner walk is the tool. A grid with rows of different lengths has no single `cols` to divide by. A third false friend is a search that computes `cols` before checking that there is a row.

In Java, check `a.length == 0` before reading `a[0]`, then check `a[0].length == 0` before the search, and compute `a.length * cols` as a `long` when the shape can be large, since the product can pass the range of `int`. Use `mid / cols` for the row and `mid % cols` for the column, never the other way round.

<!-- stage: exercises -->
### Exercises

#### [Build] Search a 2D Matrix (LeetCode 74)
<!-- id: bs-search-matrix-rows -->

**Prerequisites.** The exact search and bounds lessons, and arrays of arrays from Chapter 01.

**Problem.** Each row of an integer matrix is sorted in increasing order, and the first value of each row is greater than the last value of the previous row. Return whether the target is in the matrix. This time search by rows first: find the last row whose first value is at most the target, then search inside that row.

**Constraints.** 1 <= rows, cols <= 100 and values between -10000 and 10000.

**Example 1.** Input `matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 3`, output true.

**Example 2.** Input the same matrix and `target = 13`, output false.

**Hint.** Which row can hold the target if it is present? What does a search over the first column return when the target is smaller than every first value?

**Changed decision.** First rung: two searches in turn, over rows and then inside one row, replace one search over a virtual index.

#### [Vary] First Matrix Position (Author exercise)
<!-- id: bs-first-matrix-position -->

**Prerequisites.** The Search a 2D Matrix exercise above, and the first-true lesson.

**Problem.** The cells of the matrix in reading order are non-decreasing, so equal values may repeat. Return the row and column of the first cell in reading order that holds the target, or minus one and minus one if there is none. Use the first-true pattern over virtual indices and convert only the final position.

**Constraints.** 1 <= rows, cols <= 100, non-decreasing in reading order, and values between -10000 and 10000.

**Example 1.** Input `matrix = [[1, 2, 2], [2, 3, 5]], target = 2`, output `[0, 1]`.

**Example 2.** Input the same matrix and `target = 4`, output `[-1, -1]`.

**Hint.** What is the first virtual index whose value is at least the target? What must hold at that index for the target to be present?

**Changed decision.** The output changes from a boolean to coordinates, and a hit no longer ends the search, since an earlier equal cell may exist.

#### [Boundary] Empty Shape (Author exercise)
<!-- id: bs-empty-shape -->

**Prerequisites.** The two exercises above.

**Problem.** Make the search safe for every shape: a matrix with no rows, a matrix whose rows have no columns, and a matrix so large that rows times columns does not fit in an `int`. Compute the row and column from a position held in a `long`, and show where an unguarded version fails.

**Constraints.** 0 <= rows <= 100000 and 0 <= cols <= 100000, so the number of cells can reach ten billion. Values are `int`.

**Example 1.** Input `matrix = []` and any target, output false.

**Example 2.** Input a matrix with three rows of zero columns, and any target, output false.

**Hint.** Which of `a.length` and `a[0].length` must be read first? What happens to `rows * cols` in `int` arithmetic for 100000 by 100000?

**Changed decision.** The shape may have no cells, so a guard comes before any division, and the position type is widened to `long`.

#### [Recognize] Search a 2D Matrix II (LeetCode 240)
<!-- id: bs-search-matrix-two -->

**Prerequisites.** All three exercises above.

**Problem.** Each row is sorted in increasing order from left to right, and each column is sorted in increasing order from top to bottom, with no other promise. Return whether the target is in the matrix. A virtual index does not apply, since reading order is not increasing, so walk from the top right corner and discard a row or a column at each step.

**Constraints.** 1 <= rows, cols <= 300 and values between -1000000000 and 1000000000.

**Example 1.** Input `matrix = [[1, 4, 7], [2, 5, 8], [3, 6, 9]], target = 6`, output true.

**Example 2.** Input the same matrix and `target = 10`, output false.

**Hint.** What can you say about the rest of a column when its top cell is larger than the target? What can you say about the rest of a row to the left of a cell smaller than the target?

**Changed decision.** The data is ordered in two directions at once, so the tool changes from halving a virtual line to eliminating one row or column per step.
