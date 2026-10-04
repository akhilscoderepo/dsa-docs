# Lesson spec: Constrained Flights

**Recognition cue.** A cheapest route is limited by stops or edges, so cost alone does not dominate every arrival. **Invariant.** State includes node and edges used; relaxations never exceed the allowed count. **False friend.** Plain Dijkstra with one `dist[node]` can discard a more expensive arrival that uses fewer stops.

- **Build - Author exercise: At Most Two Edges.** Compute costs layer by layer without reusing same-layer updates.
- **Vary - Author exercise: Cost By Stops Used.** Store one best cost for each node and allowed edge count.
- **Boundary - Author exercise: Direct Flight And K Zero.** Translate `k` intermediate stops into at most `k + 1` edges.
- **Recognize - LC 787 Cheapest Flights Within K Stops.** Use bounded Bellman-Ford layers or an explicit heap state with correct dominance.
