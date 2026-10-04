# Lesson spec: Rectangular And Ragged Arrays

**Recognition cue.** Correct traversal depends on whether the matrix is rectangular, square, or ragged. **Invariant.** Every access uses a row and a column legal for that row. **Java hazard.** A ragged `int[][]` requires `grid[r].length`; `grid[0].length` is not a universal column bound.

- **Build - Author exercise: Rectangular Sum.** Sum a guaranteed `rows x cols` matrix. `[[1,2],[3,4]] -> 10`; `[] -> 0` under the stated empty contract.
- **Vary - Author exercise: Ragged Sum.** Sum `[[1,2],[],[3]]` without assuming equal row lengths.
- **Boundary - Author exercise: Empty Rows.** Distinguish `new int[0][]` from `new int[][]{{}}` before reading row zero.
- **Recognize - LC 1572 Matrix Diagonal Sum.** The square-shape guarantee makes both diagonal coordinates legal; subtract the center once when `n` is odd.
