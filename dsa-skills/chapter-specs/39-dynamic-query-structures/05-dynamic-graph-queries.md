# Lesson spec: Dynamic Graph Queries

**Recognition cue.** Graph mutations and path queries share one object. **Invariant.** Every returned distance reflects all accepted edges and the chosen recomputation/incremental strategy.

- **Build - Author exercise: Static Shortest-Path Calculator.** Preprocess or run Dijkstra per query.
- **Vary - LC 2642 Design Graph With Shortest Path Calculator.** Add edges between later queries.
- **Boundary - Author exercise: Duplicate And Dominated Edges.** Preserve the minimum useful cost.
- **Recognize - Author exercise: Update-Frequency Tradeoff.** Choose Floyd-Warshall, repeated Dijkstra, or incremental relaxation from constraints.
