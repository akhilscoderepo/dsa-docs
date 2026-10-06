# Lesson spec: Count By Whole Layers

**Recognition cue.** Distance, time, or operation count advances once per entire frontier. **Invariant.** All states in the captured queue size share one distance; their unseen neighbors belong to the next layer. **False friend.** Incrementing time per node overcounts simultaneous work.

- **Build - Author exercise: Label BFS Layers.** Capture the queue size and label every state in one batch equally.
- **Vary - Author exercise: Stop At First Target Layer.** Return when the target is first discovered or dequeued under the chosen invariant.
- **Boundary - Author exercise: Initially Complete State.** Return zero before processing any layer.
- **Recognize - LC 994 Rotting Oranges.** Count only transitions between nonempty layers that create new rotten oranges.
