# Lesson spec: Submask Aggregation

**Recognition cue.** A transition or query ranges over every subset of a mask. **Invariant.** `(sub - 1) & mask` enumerates each nonempty submask exactly once.

- **Build - Author exercise: Enumerate Submasks.** List all nonempty subsets of one mask.
- **Vary - Author exercise: Partition A Mask.** Combine `dp[sub]` with `dp[mask ^ sub]`.
- **Boundary - Author exercise: Include Empty Submask Deliberately.** Prevent an infinite unsigned-style loop.
- **Recognize - Author exercise: SOS Subset Sums.** Aggregate values from every submask using bit dimensions.
