# Lesson spec: BST Invariant And Bounds

**Recognition cue.** Every node separates all values in its left and right subtrees according to a declared duplicate policy. **Invariant.** A node must lie inside bounds inherited from every ancestor, not merely compare correctly with its parent. **False friend.** Checking only immediate children misses deep violations. **Java hazard.** Use `long` bounds or nullable bounds when node values span all `int` values.

- **Build - Author exercise: Validate One Root And Children.** State the allowed interval for each child.
- **Vary - Author exercise: Propagate Ancestor Bounds.** Narrow the upper bound on left descent and lower bound on right descent.
- **Boundary - Author exercise: Integer Extremes And Duplicates.** Avoid overflowing sentinels and state whether equality is legal.
- **Recognize - LC 98 Validate Binary Search Tree.** Validate every node against its complete ancestor-derived range.
