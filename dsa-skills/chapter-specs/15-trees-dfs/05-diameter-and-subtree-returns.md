# Lesson spec: Find The Longest Path In A Tree

**Recognition cue.** The best answer may pass through a node using both children, but the parent can continue through only one child. **Invariant.** Each call returns the best single branch usable by its parent and separately updates the best complete path seen. **False friend.** Returning the full two-branch path upward would fork and cease to be a path.

- **Build - Author exercise: Return Subtree Height.** Compute left and right heights before the parent result.
- **Vary - LC 543 Diameter of Binary Tree.** Update the global or wrapper answer with `leftHeight + rightHeight`.
- **Boundary - Author exercise: Nodes Versus Edges.** State which unit the return value and final diameter use.
- **Recognize - LC 124 Binary Tree Maximum Path Sum.** Return one nonnegative downward gain while allowing the complete answer to use both sides.
