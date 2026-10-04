# Lesson spec: PriorityQueue Mechanics

**Recognition cue.** The algorithm repeatedly needs the smallest or largest currently eligible item while the candidate set changes. **Invariant.** `peek()` is the extreme under the queue's comparator; the rest of the heap is only partially ordered. **False friend.** Iterating a `PriorityQueue` does not produce sorted order.

- **Build - Author exercise: Repeated Minimum.** Insert values, then poll them in nondecreasing order.
- **Vary - LC 1046 Last Stone Weight.** Repeatedly remove the two largest values and reinsert a remainder.
- **Boundary - Author exercise: Empty And Singleton Heap.** State when `peek` or `poll` is legal and what one remaining item means.
- **Recognize - LC 703 Kth Largest Element in a Stream.** Maintain a heap whose root is the kth-largest boundary.
