# Lesson spec: Multi-Source BFS

**Recognition cue.** Several sources spread simultaneously and the answer is distance to the nearest source or total spread time. **Invariant.** Every source begins at distance zero in the same queue; first discovery gives minimum distance to any source. **False friend.** Running one BFS per source repeats most work.

- **Build - Author exercise: Nearest Source Distances.** Enqueue all marked sources before processing.
- **Vary - LC 542 01 Matrix.** Start from every zero and fill distances outward.
- **Boundary - Author exercise: No Source Or All Sources.** Follow the input contract and avoid a false time increment.
- **Recognize - LC 994 Rotting Oranges.** Interpret one BFS layer as one minute of simultaneous spread.
