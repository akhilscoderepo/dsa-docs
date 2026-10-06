# Lesson spec: Find The Next And Previous Key

**Recognition cue.** The task asks for the next or previous key in sorted BST order. **Invariant.** When descending, retain the nearest ancestor that could still be the answer; if the node has the relevant subtree, its extreme node decides the result. **False friend.** A parent is not always the successor.

- **Build - Author exercise: Minimum Of Right Subtree.** Follow left links from the right child.
- **Vary - Author exercise: Successor Without Parent Links.** Track the best greater ancestor during root-to-target search.
- **Boundary - Author exercise: Maximum And Minimum Keys.** Return no successor/predecessor when no valid ancestor or subtree exists.
- **Recognize - LC 285 Inorder Successor in BST.** Combine subtree and ancestor cases under the unique-key contract.
