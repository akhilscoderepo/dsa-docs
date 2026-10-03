<!-- section: review -->
## Review

Work through these questions after the last lesson and repeat them after a short gap. Every scenario hides the name of the technique, so settle on an answer first and read the options second. Recognising a shape and predicting an outcome are the skills on test here, since the exercise ladders only practise building.

### Recognition Questions

```quiz
{"id":"mx-rev-shape","q":"A method sums a Java int[][] by looping r over grid.length and c over grid[0].length. For which input does it return a wrong answer without throwing an exception?","options":["A grid with no rows.","A grid whose first row is shorter than a later row.","A grid whose first row is longer than a later row.","A grid whose rows are all the same length."],"answer":1,"explain":"When a later row is longer than row 0, the loop never reads its extra cells and returns too small a total. A longer first row throws on a short later row, and an empty grid throws on grid[0]."}
```

```quiz
{"id":"mx-rev-traversal","q":"To check that every upper-left to lower-right diagonal of a matrix holds one value, which approach does the lesson recommend?","options":["From every cell, walk down its diagonal and compare each entry with the start.","Compare each cell that has an upper-left neighbor with that neighbor, once.","Sort every diagonal and compare the ends.","Transpose the matrix first."],"answer":1,"explain":"Chained equalities along each stripe prove it constant, so one comparison per cell suffices and the repeated diagonal walks are avoided."}
```

```quiz
{"id":"mx-rev-direction","q":"A spiral fill tracks a heading and decides when to turn by looking one step ahead. Which fact lets the output grid replace a separate list of visited cells?","options":["Every cell starts at zero and every written value is at least 1, so a nonzero cell is a visited cell.","Java arrays remember which cells were written.","Turns only happen at the board edge.","The heading already encodes the visited cells."],"answer":0,"explain":"The filled-tile test works only because zero marks unvisited and written values are positive. If zero were a legal output value, a separate record would be needed."}
```

```quiz
{"id":"mx-rev-neighbors","q":"For the cell (0, 0) of a 3 by 3 board, how many of its eight offset candidates are legal neighbors?","options":["8","5","3","2"],"answer":2,"explain":"Only right, down and down-right stay on the board. The other five candidates have a negative row or column, and the guard rejects them before any read."}
```

```quiz
{"id":"mx-rev-rotation","q":"A square matrix is transposed by swapping m[r][c] with m[c][r] for every r and every c from 0 to n - 1. What is the result?","options":["The transpose.","The original matrix, because every pair is swapped twice.","A rotation by ninety degrees.","An exception for the diagonal cells."],"answer":1,"explain":"Each off-diagonal pair is visited from both sides, so it is swapped back. Starting the inner loop after the diagonal swaps each pair once."}
```

```quiz
{"id":"mx-rev-markers","q":"Set Matrix Zeroes is solved by clearing a cell's row and column the moment a zero is seen during the scan. What goes wrong?","options":["Nothing, it is correct but slow.","Cells cleared by the algorithm look like original zeros and trigger more clearing than the input requires.","The scan skips the first row.","It throws for a one-column matrix."],"answer":1,"explain":"The writes erase the difference between an original zero and a cleared cell, so later reads cannot tell them apart. Recording first and writing second avoids it."}
```

```quiz
{"id":"mx-rev-constant-markers","q":"In the constant-space Set Matrix Zeroes, the first row and column store the markers. Why are two extra flags and a particular clearing order needed?","options":["To save memory.","A zero originally in the first row or column cannot be told from a marker, and clearing them early would destroy markers still needed.","To handle negative numbers.","Because the interior must be processed from the bottom."],"answer":1,"explain":"The flags remember what the first row and column held before they were borrowed, and clearing them last keeps the markers intact until the interior has been processed."}
```

```quiz
{"id":"mx-rev-spiral","q":"In the shrinking-boundary spiral on the matrix [[1, 2, 3]], what stops the bottom strip from emitting the row again in reverse?","options":["The loop condition on the whole while statement.","The guard top <= bottom, which fails once top has moved past bottom.","The right boundary being below zero.","Java ignores out-of-range loops."],"answer":1,"explain":"After the top strip, top is 1 and bottom is 0, so the guard fails and the bottom strip is skipped. Without it the bottom strip would run with the same row index and repeat cells."}
```

```quiz
{"id":"mx-rev-false-friend","q":"A question asks which cells of a grid are connected to a given cell through chains of touching infected cells. Which technique from this chapter answers it?","options":["Neighbor enumeration alone, applied once per cell.","Direction-state simulation.","None of them. It needs a graph traversal with a visited record, deferred to a later chapter.","Marker arrays with one flag per row."],"answer":2,"explain":"Neighbor enumeration answers local questions about one step. Connectivity depends on paths of unknown length, which needs a frontier and a visited record."}
```
