# Lesson spec: Graph Cloning

**Recognition cue.** A reachable object graph must be copied while preserving identity and cycles. **Invariant.** The map holds exactly one clone for each discovered original node. **False friend.** Cloning by value merges distinct nodes with equal labels.

- **Build - Author exercise: Clone One Edge.** Create both clones before wiring the copied edge.
- **Vary - Author exercise: Clone A Cycle.** Insert the mapping before traversing neighbors.
- **Boundary - Author exercise: Null And Self-Loop.** Preserve both absence and an edge back to the same identity.
- **Recognize - LC 133 Clone Graph.** Traverse every reachable node and wire clone neighbors through the identity map.
