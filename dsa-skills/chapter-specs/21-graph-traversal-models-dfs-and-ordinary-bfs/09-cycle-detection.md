# Lesson spec: Cycle Detection

**Recognition cue.** The task asks whether edges return to an already active route. **Invariant.** Undirected DFS ignores the edge back to its parent; directed DFS distinguishes visiting from fully processed nodes. **False friend.** Any visited neighbor indicates a directed cycle only when that neighbor is still active.

- **Build - Author exercise: Undirected Parent Check.** Reject a visited neighbor other than the traversal parent.
- **Vary - Author exercise: Directed Three Colors.** Detect an edge to a visiting node.
- **Boundary - Author exercise: Two-Way Undirected Edge.** Do not mistake the parent edge for a cycle.
- **Recognize - LC 207 Course Schedule.** Detect a directed prerequisite cycle with three-color DFS.
