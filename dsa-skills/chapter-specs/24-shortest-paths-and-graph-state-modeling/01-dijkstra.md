# Lesson spec: Dijkstra

**Recognition cue.** Edges have nonnegative weights and the task asks for minimum total cost from a source. **Invariant.** When the smallest nonstale tentative distance is removed from the heap, no later path can improve it; relaxing an edge proposes `dist[u] + weight`. **False friend.** Ordinary BFS is correct only when transition costs are equal.

- **Build - Author exercise: Relax One Edge.** Update a neighbor only when the proposed distance is smaller.
- **Vary - Author exercise: Small Weighted Graph.** Repeatedly process the smallest tentative distance.
- **Boundary - Author exercise: Unreachable Vertex And Large Sum.** Preserve infinity and use `long` when path sums may overflow.
- **Recognize - LC 743 Network Delay Time.** Run Dijkstra from the source and return the largest finite finalized distance.
