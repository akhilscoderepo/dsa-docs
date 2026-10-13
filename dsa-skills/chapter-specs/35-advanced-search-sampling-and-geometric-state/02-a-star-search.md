# Lesson spec: A Star Search

**Recognition cue.** A shortest-path search has a heuristic lower bound toward the goal. **Invariant.** Priority is `g + h`; an admissible heuristic never overestimates remaining cost, and consistency supports safe closed-state handling.

- **Build - Author exercise: Dijkstra With Zero Heuristic.** Show A* reducing to Dijkstra.
- **Vary - Author exercise: Manhattan Grid Heuristic.** Prioritize states by traveled cost plus Manhattan distance.
- **Boundary - Author exercise: Overestimating Heuristic.** Construct a case where optimality fails.
- **Recognize - Author exercise: A-Star Grid Path.** State admissibility and stale-entry handling before implementation.
