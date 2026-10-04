# Lesson spec: Levels Zigzag And Views

**Recognition cue.** The result groups nodes by depth or selects a position from each depth. **Invariant.** Capture the queue size before a level; exactly that many removals belong to the current depth. **False friend.** Reading the changing queue size inside the loop mixes children into their parents' level. **Java hazard.** `ArrayDeque` rejects null sentinels.

- **Build - LC 102 Binary Tree Level Order Traversal.** Collect one list from each captured queue level.
- **Vary - LC 103 Binary Tree Zigzag Level Order Traversal.** Change output placement without changing discovery order.
- **Boundary - Author exercise: Empty And One-Sided Trees.** Return an empty outer list for a null root and preserve one node per level in a chain.
- **Recognize - LC 199 Binary Tree Right Side View.** Record the last processed node at each level.
