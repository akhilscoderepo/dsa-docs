# Lesson spec: Track Depth And Paths Down A Tree

**Recognition cue.** A result depends on distance from the root, height below a node, or the values along the current root-to-node path. **Invariant.** Downward state is extended before a child call and restored afterward; upward state summarizes a completed subtree. **False friend.** A path list shared across recursion requires backtracking, while an integer depth passed by value does not.

- **Build - LC 104 Maximum Depth of Binary Tree.** Return one plus the larger child depth.
- **Vary - LC 112 Path Sum.** Pass the remaining target down one root-to-leaf path.
- **Boundary - Author exercise: Leaf Versus Internal Match.** Accept a target sum only where the problem requires a leaf.
- **Recognize - LC 113 Path Sum II.** Maintain a mutable path and remove the current node after both child calls.
