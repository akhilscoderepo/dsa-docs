# Lesson spec: Move Pieces On A Board

**Recognition cue.** Commands mutate position or occupancy and each move has an ordered sequence of legality checks. **Invariant.** The authoritative position and occupancy representation agree after every accepted move.

- **Build - LC 348 Design Tic-Tac-Toe.** Replace repeated board scans with row/column/diagonal counters.
- **Vary - LC 353 Design Snake Game.** Update tail occupancy in the correct order when the snake moves.
- **Boundary - LC 2069 Walking Robot Simulation II.** Normalize full perimeter cycles without losing direction semantics.
- **Recognize - LC 3391 Design a 3D Binary Matrix with Efficient Layer Tracking.** Maintain layered counts under point updates.
