# Lesson spec: Undirected Parent State

**Recognition cue.** An undirected traversal sees every tree edge from both endpoints. **Invariant.** A visited neighbor is a cycle only when it is not the vertex from which the current node was entered. **False friend.** Directed three-color logic is unnecessary for ordinary undirected cycle detection.

- **Build - Author exercise: DFS With Parent.** Pass the previous vertex into each call.
- **Vary - Author exercise: Detect A Triangle.** Find the non-parent visited neighbor.
- **Boundary - Author exercise: Single Edge And Parallel Edges.** State the graph's parallel-edge contract before judging a cycle.
- **Recognize - LC 261 Graph Valid Tree.** Require both no cycle and exactly one connected component.
