# Lesson spec: ArrayDeque Contracts

**Recognition cue.** The algorithm needs LIFO or FIFO access with no indexed search. **Invariant.** One chosen end has one meaning throughout the implementation. Use `addLast/removeLast/peekLast` for a stack or `addLast/removeFirst/peekFirst` for a queue. **False friend.** Java's legacy `Stack` works but is not the preferred ordinary stack. **Java hazard.** `ArrayDeque` rejects `null`, so `null` cannot be a level delimiter.

- **Build - Author exercise: Deque As Stack.** Push three integers and return them in reverse insertion order.
- **Vary - Author exercise: Deque As Queue.** Enqueue the same values and return them in insertion order.
- **Boundary - Author exercise: Empty Access Contract.** Compare exception-throwing `remove`/`get` operations with null-returning `poll`/`peek`, without storing null elements.
- **Recognize - Author exercise: Choose The Ends.** Label the exact deque operations for a LIFO undo log and a FIFO request buffer.
