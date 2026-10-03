# Lesson spec: Iterative DFS

**Recognition cue.** Depth-first order is required without relying on the language call stack. **Invariant.** The explicit stack contains subtrees or frames still to be processed. **False friend.** Pushing left before right produces right-first preorder because the stack is LIFO.

- **Build - Author exercise: Iterative Preorder.** Push right before left so the left child is processed next.
- **Vary - Author exercise: Iterative Inorder.** Push the entire left spine, then visit and move right.
- **Boundary - Author exercise: Deep Skewed Tree.** Avoid recursive stack overflow and handle an initially null root.
- **Recognize - LC 145 Binary Tree Postorder Traversal.** Use explicit visit state or a controlled reverse-preorder construction.
