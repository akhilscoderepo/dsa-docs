# Lesson spec: Aggregation

**Recognition cue.** The answer can be summarized by a fixed-size value after each element. **Invariant.** Before processing `nums[i]`, the accumulator describes exactly `nums[0..i-1]`. **False friend.** Pair or subarray relationships need more than one scalar summary.

- **Build — Author exercise: Maximum.** Given a non-empty array, return its largest value. `[-3, 8, 1] → 8`; `[-5] → -5`. Initialize from the input, not zero.
- **Vary — LC 1295 Find Numbers with Even Number of Digits.** The state changes from an extremum to a count; `[12,345,2,6,7896] → 2`; `[] → 0`.
- **Boundary — LC 485 Max Consecutive Ones.** Reset the current run at zero while preserving the best completed run. `[1,1,0,1] → 2`; `[0,0] → 0`.
- **Recognize — LC 1491 Average Salary Excluding the Minimum and Maximum Salary.** One pass keeps the sum, the minimum and the maximum together; three scalars summarize everything the final formula needs.
