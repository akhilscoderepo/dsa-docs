# Lesson spec: Find Bridges With Low Links

**Recognition cue.** Removing one undirected edge or vertex may disconnect the graph. **Invariant.** `low[u]` is the earliest discovery time reachable from `u`'s DFS subtree without using its parent edge.

- **Build - Author exercise: Discovery And Low Values.** Update low links from child returns and back edges.
- **Vary - Author exercise: Bridge Test.** Mark `(u,v)` when `low[v] > disc[u]`.
- **Boundary - Author exercise: Root Articulation Rule.** Treat a DFS root by child count rather than the nonroot formula.
- **Recognize - LC 1192 Critical Connections in a Network.** Return all bridges in one DFS.
