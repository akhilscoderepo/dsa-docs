# Lesson spec: Iterator Foundations

**Recognition cue.** A client needs the next inorder key on demand without materializing the whole traversal. **Invariant.** The stack stores the unvisited left spine; its top is the next smallest node. After popping, push the left spine of its right subtree. **False friend.** Re-running a root traversal for each call makes iteration quadratic.

- **Build - Author exercise: Push Left Spine.** Load exactly the ancestors leading to the smallest key.
- **Vary - Author exercise: Advance One Inorder Step.** Pop one node and load its right subtree's left spine.
- **Boundary - Author exercise: Empty Iterator And Right Chain.** Define `hasNext` from stack emptiness and avoid invalid pops.
- **Recognize - LC 173 Binary Search Tree Iterator.** Provide amortized `O(1)` `next` with `O(h)` space.
