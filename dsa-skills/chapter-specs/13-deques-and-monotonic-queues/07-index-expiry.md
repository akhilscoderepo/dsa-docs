# Lesson spec: Index Expiry

**Recognition cue.** Eligibility depends on age, distance, or an index interval as well as candidate quality. **Invariant.** Indices are appended in increasing order and the front is removed as soon as it crosses the legal left boundary. **False friend.** Storing only values loses identity when duplicates expire at different times.

- **Build - Author exercise: Best Of Last K Scores.** Maintain the maximum score among indices `[i-k, i-1]`.
- **Vary - Author exercise: Variable Legal Left Bound.** Expire against a supplied boundary array rather than constant `k`.
- **Boundary - Author exercise: Duplicate Values, Different Ages.** Prove expiry removes the correct occurrence.
- **Recognize - LC 1696 Jump Game VI.** Combine recent-index eligibility with the best previous dynamic-programming score.
