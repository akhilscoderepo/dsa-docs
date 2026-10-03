# Lesson spec: Cycle Entry

**Recognition cue.** Following `next` may revisit nodes, and the task asks whether a cycle exists or where it begins. **Invariant.** Floyd's slow and fast pointers collide inside a cycle; after resetting one pointer to the head, equal-speed movement meets at the entry. **False friend.** A value duplicate does not imply a node cycle—identity matters.

- **Build - LC 141 Linked List Cycle.** Detect a collision with one-step and two-step movement.
- **Vary - Author exercise: Measure Cycle Length.** Walk once around from the collision point.
- **Boundary - Author exercise: Self-Loop And Two-Node Cycle.** Guard fast-pointer dereferences correctly.
- **Recognize - LC 142 Linked List Cycle II.** Reset one pointer and locate the cycle entry without extra storage.
