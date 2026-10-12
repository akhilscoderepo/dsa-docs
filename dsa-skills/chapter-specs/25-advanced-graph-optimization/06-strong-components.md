# Lesson spec: Find Strongly Connected Components

**Recognition cue.** Directed vertices must be grouped when each can reach every other. **Invariant.** Kosaraju processes the reversed graph in decreasing original finish order, or Tarjan uses discovery and low-link state.

- **Build - Author exercise: Finish Order.** Record vertices after outgoing DFS completes.
- **Vary - Author exercise: Reverse-Graph Components.** Traverse in reverse finish order.
- **Boundary - Author exercise: Singleton And One-Way Edge.** Keep vertices separate without mutual reachability.
- **Recognize - Author exercise: Condensation DAG.** Collapse SCCs and verify the resulting graph is acyclic.
