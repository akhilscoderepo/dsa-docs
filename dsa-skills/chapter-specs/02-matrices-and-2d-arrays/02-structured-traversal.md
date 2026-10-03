# Lesson spec: Structured Traversal

**Recognition cue.** The requested cells form rows, columns, diagonals, or the outer boundary. **State.** Indices describe the exact geometric region still unvisited. **False friend.** Connectivity through neighbors is graph traversal and remains deferred.

- **Build - Author exercise: Column Sums.** Return one sum per column for a rectangular matrix.
- **Vary - LC 1572 Matrix Diagonal Sum.** Visit two coordinate formulas per row.
- **Boundary - Author exercise: Perimeter Sum.** Avoid counting corners twice in a one-row or one-column matrix.
- **Recognize - LC 766 Toeplitz Matrix.** Compare each cell with its upper-left predecessor instead of rescanning whole diagonals.
