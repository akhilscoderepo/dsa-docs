# Lesson spec: Walk Every Edge Once With Hierholzer

**Recognition cue.** Every edge must be consumed exactly once in an Eulerian trail. **Invariant.** Remove edges while walking; append a vertex only when it has no unused outgoing edge, producing reverse trail order.

- **Build - Author exercise: Eulerian Cycle.** Consume each directed edge once and reverse the postorder output.
- **Vary - Author exercise: Eulerian Path.** Start at the vertex required by degree imbalance.
- **Boundary - Author exercise: Parallel Edges.** Represent edge multiplicity rather than neighbor membership.
- **Recognize - LC 332 Reconstruct Itinerary.** Combine Hierholzer's algorithm with lexical edge selection.
