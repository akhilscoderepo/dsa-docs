# Lesson spec: Farthest Frontier

**Recognition cue.** Many paths reach positions in a linear sequence, but only the farthest reachable boundary matters. **Invariant.** Every index up to `farthest` is reachable; encountering an index beyond it proves failure. **False friend.** Backtracking explores exponentially many jump sequences that the frontier already dominates.

- **Build - Author exercise: Update Reachable Prefix.** Scan only indices already inside the frontier.
- **Vary - LC 55 Jump Game.** Return whether the frontier reaches the last index.
- **Boundary - Author exercise: Zero Before The Frontier.** A zero is harmless when an earlier jump already crosses it.
- **Recognize - LC 45 Jump Game II.** Treat the current reachable boundary as one BFS-like jump layer and track the next frontier.
