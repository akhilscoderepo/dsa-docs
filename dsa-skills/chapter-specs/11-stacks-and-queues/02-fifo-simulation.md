# Lesson spec: FIFO Simulation

**Recognition cue.** Items must be handled in arrival order while later arrivals wait behind earlier ones. **Invariant.** The front is the next item to process and every enqueued item appears behind all items already present. **False friend.** A stack reverses arrival order.

- **Build - Author exercise: Printer Queue.** Process job IDs in the order received.
- **Vary - Author exercise: Round-Robin One Step.** Remove the front task, decrement its remaining work, and re-enqueue it only when unfinished.
- **Boundary - Author exercise: Queue Becomes Empty.** Guard or prove every removal and handle a task completed on its first turn.
- **Recognize - LC 1700 Number of Students Unable to Eat Lunch.** Simulate only while progress is possible and detect a full unsuccessful rotation.
