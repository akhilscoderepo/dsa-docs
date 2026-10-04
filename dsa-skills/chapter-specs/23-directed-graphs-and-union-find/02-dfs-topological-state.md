# Lesson spec: DFS Topological State

**Recognition cue.** Directed cycle detection and topological order can be produced through recursive completion. **Invariant.** White is unvisited, gray is active, and black is complete; only an edge to gray proves a cycle. Postorder reversal yields an order when no cycle exists.

- **Build - Author exercise: Three-Color Trace.** Mark entry gray and exit black.
- **Vary - Author exercise: Postorder Topological List.** Append only after every outgoing neighbor completes.
- **Boundary - Author exercise: Cross Edge To Black.** Accept it because it does not return to an active ancestor.
- **Recognize - LC 210 Course Schedule II.** Produce an order with DFS or reject a gray back edge.
