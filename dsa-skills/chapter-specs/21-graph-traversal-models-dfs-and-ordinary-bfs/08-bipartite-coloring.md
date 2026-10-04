# Lesson spec: Bipartite Coloring

**Recognition cue.** Vertices must split into two groups with every edge crossing groups. **Invariant.** Each colored edge endpoint must receive opposite colors; every component needs its own start. **False friend.** Checking only one connected component is incomplete.

- **Build - Author exercise: Color One Component.** Assign opposite colors during BFS.
- **Vary - Author exercise: Process Disconnected Components.** Start coloring from every uncolored vertex.
- **Boundary - Author exercise: Self-Loop And Odd Cycle.** Reject both because they force a color conflict.
- **Recognize - LC 785 Is Graph Bipartite?.** Validate two-colorability across the entire graph.
