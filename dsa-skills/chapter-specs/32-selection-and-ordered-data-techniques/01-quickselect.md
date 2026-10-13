# Lesson spec: Quickselect

**Recognition cue.** Only one rank is needed, not a fully sorted array. **Invariant.** Partition places the pivot at its final rank and proves which side can contain the target.

- **Build - Author exercise: Select Kth Smallest.** Partition and recurse only toward the target rank.
- **Vary - LC 215 Kth Largest Element in an Array.** Convert kth-largest to a zero-based target index.
- **Boundary - Author exercise: Duplicates And Extreme K.** Preserve progress when many values equal the pivot.
- **Recognize - LC 973 K Closest Points to Origin.** Select by squared distance without sorting every point.
