# Lesson spec: Marker State

**Recognition cue.** Rows and columns must be marked for a later mutation, but immediate writes would destroy evidence still needed. **State.** Marker storage records affected rows/columns until the observation pass completes. **False friend.** Hash sets are an allowed auxiliary solution, but Chapter 04 owns general set state.

- **Build - Author exercise: Mark Bad Rows.** First record which rows contain `-1`, then clear them in a second pass.
- **Vary - LC 73 Set Matrix Zeroes.** Record both affected rows and columns before applying zeroes.
- **Boundary - LC 73 Constant-Space Variant.** Reserve the first row/column as markers and keep separate flags for their original state.
- **Recognize - LC 289 Game of Life.** Encode old and new cell state together so neighbor reads still see the original generation.
