# Lesson spec: Zero-One BFS

**Recognition cue.** Every edge weight is exactly zero or one. **Invariant.** The deque processes tentative distances in nondecreasing order by pushing zero-cost improvements to the front and one-cost improvements to the back. **False friend.** Ordinary BFS counts edges, while Dijkstra works but pays an unnecessary heap cost.

- **Build - Author exercise: Choose Deque End By Weight.** Push a relaxed zero edge first and a one edge last.
- **Vary - Author exercise: Reject Nonimproving Relaxations.** Maintain a distance array exactly as in weighted search.
- **Boundary - Author exercise: Zero-Cost Cycle.** Terminate through distance improvement checks rather than Boolean discovery alone.
- **Recognize - LC 1368 Minimum Cost to Make at Least One Valid Path in a Grid.** Model following an arrow as zero and changing direction as one.
