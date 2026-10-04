# Lesson spec: Grid Graphs

**Recognition cue.** Cells are vertices and legal moves define implicit edges. **Invariant.** Every queued or recursive coordinate is in bounds, eligible, and not previously visited. **False friend.** Diagonal movement is not implied by a two-dimensional array.

- **Build - LC 733 Flood Fill.** Traverse same-color four-direction neighbors.
- **Vary - LC 200 Number of Islands.** Start one traversal per unvisited land component.
- **Boundary - Author exercise: Original Color Equals New Color.** Avoid endlessly rediscovering unchanged cells.
- **Recognize - LC 695 Max Area of Island.** Return a component size from the grid traversal.
