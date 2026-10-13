# Lesson spec: Segment Trees

**Recognition cue.** Associative range queries and point updates need more flexible state than prefix subtraction. **Invariant.** Every node stores the aggregate for one exact interval, combined from its children.

- **Build - Author exercise: Build Range Sums.** Recursively split and combine one array.
- **Vary - Author exercise: Point Assignment.** Update one leaf and recompute ancestors.
- **Boundary - Author exercise: No Overlap And Full Cover.** Return the operator identity or the stored node aggregate.
- **Recognize - LC 307 Range Sum Query - Mutable.** Implement mutable range sum with a segment tree.
