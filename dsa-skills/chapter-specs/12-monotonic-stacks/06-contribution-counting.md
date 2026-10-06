# Lesson spec: Count Subarrays By Their Minimum

**Recognition cue.** The result is a sum over all subarrays, but each element can be counted as the minimum or maximum for a number of boundary choices. **Invariant.** If index `i` owns subarrays between its selected left and right boundaries, its count is `(i - left) * (right - i)`. **False friend.** This multiplication is valid only after duplicate ownership is proved. **Java hazard.** Multiply with `long` before applying the modulus.

- **Build - Author exercise: Count Subarrays Owned By One Index.** Enumerate left-start and right-end choices from supplied boundaries.
- **Vary - Author exercise: Sum Owned Minimum Contributions.** Multiply each value by its number of owned subarrays.
- **Boundary - Author exercise: Negative And Repeated Values.** Separate arithmetic/modulus handling from the equality ownership proof.
- **Recognize - LC 907 Sum of Subarray Minimums.** Discover boundaries with a monotonic stack and accumulate each index's contribution.
