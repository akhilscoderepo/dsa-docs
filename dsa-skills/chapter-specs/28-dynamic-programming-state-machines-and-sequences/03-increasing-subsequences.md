# Lesson spec: Increasing Subsequences

**Recognition cue.** The answer is a longest strictly increasing subsequence, not necessarily contiguous. **Invariant.** Quadratic DP ends at each index; patience sorting keeps the smallest possible tail for every length.

- **Build - Author exercise: LIS Ending At I.** Extend from earlier smaller values.
- **Vary - LC 300 Longest Increasing Subsequence.** Compute the quadratic recurrence.
- **Boundary - Author exercise: Duplicates.** Use lower bound so equal values do not increase strict length.
- **Recognize - LC 300 O(n log n).** Maintain minimal tails with binary search and explain why tails are not the actual LIS.
