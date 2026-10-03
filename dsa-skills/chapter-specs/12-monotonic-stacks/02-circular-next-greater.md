# Lesson spec: Circular Next Greater

**Recognition cue.** Successors wrap from the end of the array to the beginning, but each answer still needs the first greater value in circular order. **Invariant.** A virtual scan of at most `2n` positions exposes every possible successor; indices are pushed only during the first pass so each position is represented once. **False friend.** Physically duplicating the array is unnecessary.

- **Build - Author exercise: Circular Successor Indices.** Enumerate `(i + 1) % n` order for one starting position.
- **Vary - Author exercise: Virtual Double Scan.** Read `nums[i % n]` across two passes without allocating a copy.
- **Boundary - Author exercise: All Equal Circular Array.** Leave every answer at `-1` and avoid resolving on equality.
- **Recognize - LC 503 Next Greater Element II.** Combine virtual traversal with the unresolved-index stack.
