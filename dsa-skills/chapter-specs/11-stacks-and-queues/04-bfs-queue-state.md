# Lesson spec: BFS Queue State

**Recognition cue.** States are explored in nondecreasing number of transitions from a start. **Invariant.** The queue contains discovered but unprocessed states; each state is marked when enqueued so it is not scheduled twice. **False friend.** A stack explores deeply and does not preserve shortest unweighted transition count. Full graph modeling arrives in Chapter 21.

- **Build - Author exercise: Process A Supplied Frontier.** Remove states from a queue and append their already-supplied unseen successors.
- **Vary - Author exercise: Minimum Add-One Or Double Steps.** Search integer states within a stated bound and return the first distance to a target.
- **Boundary - Author exercise: Start Is Target.** Return distance zero before generating successors and mark states at enqueue time.
- **Recognize - Author exercise: Shortest Word Transform From Supplied Neighbors.** Use the queue invariant without requiring graph construction techniques not yet taught.
