# Lesson spec: Choose K Values Without Reordering

**Recognition cue.** Select `k` distinct values where order does not matter. **Invariant.** Every recursive choice comes from indices at or after `start`, so each set appears in one increasing order. **False friend.** A global used array allows multiple orders of the same combination.

- **Build - Author exercise: Choose Two From Four.** Advance the next start beyond the chosen index.
- **Vary - LC 77 Combinations.** Stop when the path contains `k` values.
- **Boundary - Author exercise: Insufficient Remaining Values.** End the loop when too few candidates remain to fill the path.
- **Recognize - LC 216 Combination Sum III.** Add a remaining-sum state while preserving increasing choices.
