# Lesson spec: Kahn Topological Order

**Recognition cue.** Directed prerequisites require an order in which every predecessor appears first. **Invariant.** Indegree counts unresolved incoming prerequisites; the queue contains exactly currently available zero-indegree vertices. **False friend.** Sorting labels cannot satisfy arbitrary dependencies.

- **Build - Author exercise: Compute Indegrees.** Count every directed incoming edge.
- **Vary - LC 207 Course Schedule.** Process zero-indegree courses and test whether all vertices are removed.
- **Boundary - Author exercise: Several Initial Sources.** Enqueue every zero-indegree vertex, including isolated ones.
- **Recognize - LC 210 Course Schedule II.** Return the removal order or an empty result when a cycle remains.
