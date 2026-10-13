# Lesson spec: Split Containers

**Recognition cue.** Operations target several logical positions that one ordinary deque cannot expose cheaply. **Invariant.** Two containers differ in size by at most one and their boundary defines the logical middle.

- **Build - Author exercise: Balanced Two-Deque Sequence.** Rebalance after end insertion.
- **Vary - LC 1670 Design Front Middle Back Queue.** Define which middle is removed when size is even.
- **Boundary - Author exercise: Oscillating Empty Halves.** Preserve balance through repeated middle removal.
- **Recognize - LC 1172 Dinner Plate Stacks.** Maintain multiple bounded stacks plus the next writable location.
