# Lesson spec: Group Queue Items By Level

**Recognition cue.** Work must be grouped by its distance or batch level, and all items currently in the queue belong to the present level. **Invariant.** Capture `levelSize = queue.size()` before the inner loop; exactly those items form the current level. **Java hazard.** Do not use a null sentinel with `ArrayDeque`. Tree level order is applied in Chapter 16.

- **Build - Author exercise: Process Queue In Batches.** Given items that append next-batch items, return the IDs processed at each level.
- **Vary - Author exercise: Count Levels To First Target.** Increment distance after processing one captured batch.
- **Boundary - Author exercise: Expanding Queue.** Prove newly enqueued items are excluded from the current batch despite increasing `queue.size()`.
- **Recognize - Author exercise: Alternate Level Output.** Reverse only the reported order for every other level while preserving FIFO discovery.
