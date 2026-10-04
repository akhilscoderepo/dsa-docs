# Lesson spec: Node-State Search

**Recognition cue.** Future transitions depend on both location and another fact such as stops used, keys held, or last edge color. **Invariant.** Distance and visited state are indexed by the complete pair `(node, state)`; two states at one node are distinct unless dominance is proved. **False friend.** One distance per node discards potentially necessary routes.

- **Build - Author exercise: Node And Coupon Flag.** Track whether a one-use discount has been consumed.
- **Vary - Author exercise: Distance By State.** Store separate distances for every node-mode pair.
- **Boundary - Author exercise: Same Node, Different Future.** Show why a costlier arrival with an unused resource may remain useful.
- **Recognize - LC 1129 Shortest Path with Alternating Colors.** Include the last edge color in BFS state.
