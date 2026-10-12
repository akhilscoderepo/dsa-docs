# Lesson spec: Zero-One Knapsack

**Recognition cue.** Each item can be used at most once. **Invariant.** Descending one-dimensional capacity order ensures the current item is not read from a state it just created.

- **Build - Author exercise: One-Use Items.** Fill a two-dimensional item/capacity table.
- **Vary - Author exercise: Descending Compression.** Compress capacity without enabling reuse.
- **Boundary - Author exercise: Ascending-Loop Counterexample.** Show one item being counted twice.
- **Recognize - LC 416 Partition Equal Subset Sum.** Use each number once to reach half the total.
