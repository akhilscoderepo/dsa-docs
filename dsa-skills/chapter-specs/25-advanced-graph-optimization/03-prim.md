# Lesson spec: Grow A Spanning Tree With Prim

**Recognition cue.** A weighted undirected graph needs a minimum-cost spanning tree and adjacency expansion is convenient. **Invariant.** The heap contains edges crossing from the built tree to unvisited vertices; the cheapest crossing edge is safe.

- **Build - Author exercise: Grow One Tree Edge.** Accept the cheapest edge reaching an unvisited vertex.
- **Vary - Author exercise: Skip Stale Heap Edges.** Ignore edges whose destination already joined the tree.
- **Boundary - Author exercise: Disconnected Graph.** Detect when the heap empties before all vertices join.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Apply Prim to Manhattan-distance edges.
