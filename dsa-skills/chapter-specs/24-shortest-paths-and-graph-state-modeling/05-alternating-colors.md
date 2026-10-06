# Lesson spec: Alternate Edge Colors

**Recognition cue.** Edge type constrains which edge type may be used next. **Invariant.** Visited is indexed by node and last color; neighbors must use the opposite color. **False friend.** Marking the node once can suppress a necessary arrival with the other last color.

- **Build - Author exercise: Alternate Red And Blue.** Generate only opposite-color transitions.
- **Vary - Author exercise: Two Start Modes.** Seed both possible previous colors at distance zero.
- **Boundary - Author exercise: Self-Loop And Parallel Colors.** Treat color-state pairs independently.
- **Recognize - LC 1129 Shortest Path with Alternating Colors.** BFS over `(node, lastColor)` and take the smaller state distance.
