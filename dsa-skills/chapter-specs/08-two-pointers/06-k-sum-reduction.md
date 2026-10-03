# Lesson spec: K-Sum Reduction

**Recognition cue.** The array can be sorted, several leading values can be fixed, and the remaining two-value target is monotone. **State.** Each fixed choice reduces both `k` and the remaining target. **Java hazard.** Use `long` for sums when several integers can overflow.

- **Build - LC 15 3Sum.** Fix one value and solve a two-sum target on the suffix.
- **Vary - LC 16 3Sum Closest.** Preserve the closest total instead of collecting exact unique triples.
- **Boundary - Author exercise: Overflowing Sum.** Evaluate extreme integer inputs using `long` arithmetic.
- **Recognize - LC 18 4Sum.** Fix two values, then reuse the pair invariant and duplicate policy.
