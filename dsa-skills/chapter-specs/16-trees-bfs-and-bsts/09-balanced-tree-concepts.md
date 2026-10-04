# Lesson spec: Balanced-Tree Concepts

**Recognition cue.** Search performance depends on height, and arbitrary insertion order can create a linear chain. **Invariant.** A height-balanced tree keeps left and right subtree heights within the structure's allowed bound; rotations preserve inorder key order while changing shape. **False friend.** A balanced tree is not necessarily complete or perfectly symmetric.

- **Build - Author exercise: Compare Search Heights.** Contrast the same keys in a chain and a balanced shape.
- **Vary - Author exercise: Identify One Rotation.** Recognize left-left and right-right imbalance from three ordered keys.
- **Boundary - Author exercise: Preserve Inorder Through Rotation.** List keys before and after a rotation and verify identical sorted order.
- **Recognize - Author exercise: Explain Library Choice.** Decide when a self-balancing ordered map is needed instead of a hand-built unbalanced BST; implementation of AVL/red-black deletion is outside this LeetCode core.
