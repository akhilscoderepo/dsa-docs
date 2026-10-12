# Lesson spec: Find Shortest Paths With Negative Edges

**Recognition cue.** Weighted edges may be negative, or the number of usable edges is bounded. **Invariant.** After pass `i`, distances cover paths using at most `i` edges. **False friend.** Dijkstra is unsafe with negative edges.

- **Build - Author exercise: One Relaxation Pass.** Read previous distances and write improvements without accidental same-pass chaining.
- **Vary - LC 787 Cheapest Flights Within K Stops.** Run exactly the permitted number of edge layers.
- **Boundary - Author exercise: Unreachable And Negative Cycle.** Guard infinity before addition and explain the extra detection pass.
- **Recognize - Author exercise: Negative-Edge Shortest Paths.** Compute distances where no reachable negative cycle exists.
