# Lesson spec: Skip Repeated Values

**Recognition cue.** Sorted candidates can produce the same value combination repeatedly. **Invariant.** Skip equal choices only after one representative branch or pair has been fully processed. **False friend.** Skipping before evaluating the first representative can discard a valid answer.

- **Build - Author exercise: Unique Pairs.** Return distinct sorted pairs summing to a target.
- **Vary - LC 15 3Sum.** Skip repeated fixed values and repeated left/right values after recording a triplet.
- **Boundary - Author exercise: All Equal.** `[0,0,0,0]` produces exactly one triplet.
- **Recognize - LC 18 4Sum.** Duplicate policy applies at every fixed recursion/loop depth and at the final pair scan.
