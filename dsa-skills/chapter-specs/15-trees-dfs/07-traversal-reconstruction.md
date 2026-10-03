# Lesson spec: Traversal Reconstruction

**Recognition cue.** Two traversal orders describe one tree with unique values, and one order identifies the root while the other partitions subtrees. **Invariant.** Each recursive call owns matching traversal ranges for exactly one subtree. **False friend.** Preorder alone does not uniquely determine an arbitrary binary tree. **Java hazard.** Map inorder values to indices to avoid repeated linear searches.

- **Build - Author exercise: Split One Root.** Locate the preorder root in inorder and identify left/right sizes.
- **Vary - Author exercise: Reconstruct By Index Ranges.** Pass boundaries instead of copying slices.
- **Boundary - Author exercise: Empty Range And Skewed Tree.** Stop exactly when the owned range is empty.
- **Recognize - LC 105 Construct Binary Tree from Preorder and Inorder Traversal.** Combine the index map with a moving preorder position.
