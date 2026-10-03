# Lesson spec: Prefix Construction

**Recognition cue.** Later work repeatedly needs the aggregate of everything before a position. **State.** With a sentinel convention, `prefix[i]` is the sum of the first `i` values. **Java hazard.** Use `long` when the maximum possible total exceeds `int`.

- **Build - LC 1480 Running Sum of 1d Array.** Construct cumulative sums from left to right.
- **Vary - LC 724 Find Pivot Index.** Compare `prefix before i` with `total - prefix through i`.
- **Boundary - Author exercise: Empty Prefix.** Define `prefix[0] = 0`; verify an empty range contributes zero.
- **Recognize - Author exercise: Prefix Averages.** Reuse cumulative totals while dividing by the correct number of values.
