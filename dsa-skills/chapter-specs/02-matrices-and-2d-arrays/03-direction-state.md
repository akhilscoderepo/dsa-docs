# Lesson spec: Moving With A Direction

**Recognition cue.** Movement follows a small cyclic direction rule and changes when the next step is illegal or already consumed. **State.** `(row, col, direction)` fully describes the next simulation step. **False friend.** A BFS frontier explores many positions; direction-state simulation follows one evolving cursor.

- **Build - Author exercise: Clockwise Walker.** Move a cursor through four directions and rotate on a blocked edge.
- **Vary - LC 59 Spiral Matrix II.** Write increasing values while turning at boundaries or filled cells.
- **Boundary - Author exercise: Single Cell.** A `1 x 1` board writes exactly once and never performs an extra turn.
- **Recognize - LC 885 Spiral Matrix III.** Allow the cursor outside the result rectangle while recording only legal coordinates.
