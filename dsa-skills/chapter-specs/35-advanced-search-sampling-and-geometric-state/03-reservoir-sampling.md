# Lesson spec: Reservoir Sampling

**Recognition cue.** A stream length is unknown and items cannot all be stored, but each must have equal inclusion probability. **Invariant.** After seeing `i` items, each has probability `k/i` of residing in a size-`k` reservoir.

- **Build - Author exercise: Sample One Item.** Replace the sample with probability `1/i`.
- **Vary - LC 382 Linked List Random Node.** Traverse once with constant extra space.
- **Boundary - Author exercise: First K Items And Short Stream.** Initialize the reservoir from available elements.
- **Recognize - LC 398 Random Pick Index.** Uniformly select among occurrences without storing their indices.
