# Lesson spec: Meet In Middle

**Recognition cue.** Exponential search has roughly 30–44 choices—too many for `2^n`, but two `2^(n/2)` enumerations are practical. **Invariant.** Every full choice splits uniquely into one subset from each half.

- **Build - Author exercise: Half Subset Sums.** Enumerate sums independently.
- **Vary - Author exercise: Closest Pair Of Half Sums.** Sort one side and binary-search complements.
- **Boundary - Author exercise: Duplicates And Long Sums.** Preserve multiplicity when counting and use `long`.
- **Recognize - LC 1755 Closest Subsequence Sum.** Minimize distance to a target with two half-sum sets.
