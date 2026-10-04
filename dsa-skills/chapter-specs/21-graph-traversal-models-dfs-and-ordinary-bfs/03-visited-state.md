# Lesson spec: Visited State

**Recognition cue.** Multiple paths may reach the same vertex. **Invariant.** Each vertex is scheduled once; BFS normally marks at enqueue time and DFS at entry. **False friend.** Marking BFS only when dequeued permits duplicate queue entries.

- **Build - Author exercise: Reachable Vertices.** Traverse from one source with a Boolean visited array.
- **Vary - Author exercise: Iterative DFS.** Mark before pushing or otherwise prove duplicates are harmless.
- **Boundary - Author exercise: Cycle And Disconnected Vertex.** Terminate the cycle without claiming unreachable vertices were visited.
- **Recognize - LC 841 Keys and Rooms.** Treat keys as directed edges and test complete reachability.
