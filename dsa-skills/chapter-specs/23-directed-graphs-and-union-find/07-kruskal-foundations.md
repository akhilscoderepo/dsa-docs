# Lesson spec: Kruskal Foundations

**Recognition cue.** The graph must connect all vertices with minimum total edge cost. **Invariant.** Edges are considered by increasing weight; accept an edge only when it joins different components. The cut property makes that edge safe. **False friend.** Choosing the cheapest edges without cycle checks may not form a tree.

- **Build - Author exercise: Cheapest Safe Edge.** Sort edges and skip one whose endpoints already connect.
- **Vary - Author exercise: Stop After V Minus One.** End once the spanning tree has enough edges.
- **Boundary - Author exercise: Disconnected Weighted Graph.** Report that no spanning tree exists.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Generate weighted edges and apply Kruskal with union-find.
