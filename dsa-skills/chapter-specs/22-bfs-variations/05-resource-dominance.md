# Lesson spec: Resource Dominance

**Recognition cue.** Search state includes a consumable resource, but multiple states at the same node may dominate one another. **Invariant.** At equal or smaller distance, reaching a node with more remaining resource dominates a state with less; discard only when that relation is proved. **False friend.** A Boolean visited array by node loses useful resource states.

- **Build - Author exercise: Position And Remaining Breaks.** Encode both fields in the queue state.
- **Vary - Author exercise: Best Resource Per Cell.** Keep the greatest remaining budget seen at an equal-or-better layer.
- **Boundary - Author exercise: Longer Path With More Resource.** Do not apply dominance across distances without checking its proof.
- **Recognize - LC 1293 Shortest Path in a Grid with Obstacles Elimination.** BFS over `(row, col, remainingEliminations)` with safe dominance.
