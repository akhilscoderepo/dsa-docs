# Lesson spec: Unweighted Shortest Paths

**Recognition cue.** Every transition has equal cost and the task asks for minimum edges or moves. **Invariant.** BFS dequeues vertices in nondecreasing distance, so first discovery is shortest. **False friend.** DFS may find a path first but not the shortest one.

- **Build - Author exercise: Distance From One Source.** Assign `distance[next] = distance[current] + 1` at discovery.
- **Vary - Author exercise: Restore One Shortest Path.** Store a predecessor for each first discovery.
- **Boundary - Author exercise: Source Equals Target And Unreachable Target.** Return zero or the stated failure value.
- **Recognize - LC 1091 Shortest Path in Binary Matrix.** Apply BFS distance to an implicit eight-direction grid graph.
