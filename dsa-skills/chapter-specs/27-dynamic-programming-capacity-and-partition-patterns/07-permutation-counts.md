# Lesson spec: Permutation Counts

**Recognition cue.** Reusable values form a target and different orders count separately. **Invariant.** Iterate totals outside and candidates inside so each final choice extends all smaller ordered sequences.

- **Build - Author exercise: Ordered Sums To Four.** Enumerate sequences from values `1` and `2`.
- **Vary - LC 377 Combination Sum IV.** Count ordered constructions for every total.
- **Boundary - Author exercise: Overflow And Nonpositive Values.** State numeric bounds and exclude transitions that do not shrink the target.
- **Recognize - Author exercise: Compare With Coin Change II.** Same recurrence ingredients, different loop ownership and meaning.
