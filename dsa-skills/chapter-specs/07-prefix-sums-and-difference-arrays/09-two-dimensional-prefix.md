# Lesson spec: Sum A Rectangle In Constant Time

**Recognition cue.** Many immutable rectangle-sum queries target a matrix. **State.** `prefix[r+1][c+1]` stores the rectangle from the origin through `(r,c)`; inclusion-exclusion removes two outside strips and restores their overlap.

- **Build - LC 304 Range Sum Query 2D - Immutable.** Precompute a sentinel-bordered prefix matrix.
- **Vary - LC 1314 Matrix Block Sum.** Query a clipped rectangle around every cell.
- **Boundary - Author exercise: Single Cell Rectangle.** Verify inclusion-exclusion returns exactly one cell.
- **Recognize - Author exercise: Whole Matrix Query.** Confirm sentinel coordinates avoid negative indices.
