# Lesson spec: Mark Cells On A Grid

**Recognition cue.** Choices occupy board positions and constrain later spatial choices. **Invariant.** Marker state represents exactly the placements on the current path and is restored after exploration. **False friend.** A global visited mark without restoration incorrectly blocks cells for sibling paths.

- **Build - Author exercise: Four-Direction Path.** Mark one cell, explore legal neighbors, then unmark it.
- **Vary - LC 79 Word Search.** Match one character per cell without reusing a cell in the same path.
- **Boundary - Author exercise: Cell Reuse And Early Success.** Restore the board even when using mutation-based marking and short-circuiting.
- **Recognize - LC 51 N-Queens.** Replace spatial adjacency with column and diagonal occupancy constraints.
