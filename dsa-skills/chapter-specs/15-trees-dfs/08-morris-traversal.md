# Lesson spec: Walk A Tree Without A Stack

**Recognition cue.** Inorder or preorder traversal is required with `O(1)` auxiliary space and temporary reversible threading is allowed. **Invariant.** A predecessor's null right link temporarily points back to the current node and is restored on the second encounter. **False friend.** Forgetting restoration corrupts the input tree and can create a cycle.

- **Build - Author exercise: Find Inorder Predecessor.** Walk to the rightmost node of the left subtree.
- **Vary - Author exercise: Create And Remove One Thread.** Distinguish first and second arrival at the same node.
- **Boundary - Author exercise: No Left Child And Existing Thread.** Visit directly in the first case and restore in the second.
- **Recognize - LC 94 Binary Tree Inorder Traversal.** Implement Morris inorder and verify the tree is unchanged afterward.
