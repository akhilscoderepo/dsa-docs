# Lesson spec: Visit Nodes In Three Orders

**Recognition cue.** Every node must be processed once, and the relative position of the node action and child calls determines meaning. **Invariant.** Preorder acts before children, inorder between binary children, and postorder after children. **False friend.** These are not interchangeable labels; reconstruction and sorted BST traversal depend on order.

- **Build - LC 144 Binary Tree Preorder Traversal.** Record node, then left and right subtrees.
- **Vary - LC 94 Binary Tree Inorder Traversal.** Move the action between the two child calls.
- **Boundary - Author exercise: Empty And One-Sided Trees.** Preserve order when one child is null.
- **Recognize - LC 145 Binary Tree Postorder Traversal.** Delay the node action until both subtree calls return.
