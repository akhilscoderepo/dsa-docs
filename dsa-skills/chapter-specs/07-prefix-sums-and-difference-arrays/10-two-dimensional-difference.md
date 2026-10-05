# Lesson spec: Add To Rectangles In Constant Time

**Recognition cue.** Many rectangle additions precede one final matrix materialization. **State.** Four signed corner updates encode each rectangle; two-dimensional prefix reconstruction spreads their effects. **False friend.** A 2D prefix-query table reads fixed values; it does not batch writes.

- **Build - Author exercise: One Rectangle Add.** Apply four corner deltas to an interior rectangle.
- **Vary - LC 2536 Increment Submatrices by One.** Batch all rectangle increments before reconstruction.
- **Boundary - Author exercise: Bottom-Right Edge.** Allocate a sentinel border or explicitly guard `r2+1` and `c2+1`.
- **Recognize - Author exercise: Weighted Rectangle Updates.** Generalize increment-by-one to signed `long` weights.
