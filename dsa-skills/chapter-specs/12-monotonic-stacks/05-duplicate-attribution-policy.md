# Lesson spec: Duplicate-Attribution Policy

**Recognition cue.** Equal values could claim the same subarray when nearest boundaries are used for counting. **Invariant.** Make one side strict and the other non-strict so every subarray with tied minima has exactly one owner. **False friend.** Using strict comparisons on both sides can double-count; non-strict on both can leave gaps. The chosen asymmetric side is a convention, not a universal direction.

- **Build - Author exercise: Two Equal Minima Ownership.** List subarrays of `[2,2]` and assign each to exactly one index.
- **Vary - Author exercise: Strict Left, Non-Strict Right.** Compute boundaries and verify the ownership partition.
- **Boundary - Author exercise: All Equal Array.** Confirm the total number of owned subarrays is `n(n+1)/2`.
- **Recognize - LC 907 Sum of Subarray Minimums.** Explain the tie convention before translating distances into contributions.
