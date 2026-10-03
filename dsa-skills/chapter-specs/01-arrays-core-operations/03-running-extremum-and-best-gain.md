# Lesson spec: Running Extremum And Best Gain

**Recognition cue.** The answer is the best difference between two positions where the earlier one must come first, and the chosen positions need not be adjacent. **State.** `lowestSoFar` is the smallest value among positions already read; `bestGain` is the largest `value - lowestSoFar` seen at any position. **Invariant.** Before reading `nums[i]`, `lowestSoFar` is the minimum of `nums[0..i-1]`. **False friend.** Kadane's algorithm chooses one contiguous block, which this scan does not; the best gain pairs two positions and ignores everything between them. Added by the coverage audit addendum; LC 121 moved here from Aggregation.

- **Build — LC 121 Best Time to Buy and Sell Stock.** `[7,1,5,3,6,4] → 5`; `[7,6,4,3,1] → 0`.
- **Vary — Author exercise: Largest Drop.** Return the largest `earlier - later` over pairs where the earlier value comes first. The changed decision is that the running extremum becomes a maximum.
- **Boundary — Author exercise: No Profitable Pair.** For strictly decreasing prices the contract answer is `0`, not a negative number and not `-1`. State the contract before writing the initial value.
- **Recognize — LC 122 Best Time to Buy and Sell Stock II.** Multiple transactions are now allowed; state the transaction contract first. The state changes from a running minimum to day-to-day differences, so this is a false friend of the lesson's own pattern.
