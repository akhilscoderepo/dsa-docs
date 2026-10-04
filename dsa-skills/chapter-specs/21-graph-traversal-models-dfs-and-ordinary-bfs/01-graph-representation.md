# Lesson spec: Graph Representation

**Recognition cue.** Relationships are arbitrary edges rather than one parent or next pointer. **Invariant.** An adjacency list enumerates exactly each vertex's outgoing neighbors; a matrix answers edge existence directly. **False friend.** A matrix costs `O(V^2)` even for sparse graphs.

- **Build - Author exercise: Undirected Adjacency Lists.** Add both directions for every undirected edge.
- **Vary - Author exercise: Directed Adjacency Lists.** Add only the stated direction and preserve isolated vertices.
- **Boundary - Author exercise: Parallel And Self Edges.** State whether the input permits them before deduplicating.
- **Recognize - LC 1791 Find Center of Star Graph.** Use the graph contract to identify the shared endpoint.
