# Lesson spec: Subarrays, Subsequences And Subsets Compared

**Recognition cue.** The prompt uses terms such as subarray, substring, subsequence, subset, prefix, or suffix. **State.** Write down which index relationships must be preserved. **Invariant.** A subarray/substring occupies consecutive positions; a subsequence preserves relative order but may skip positions; a subset need not preserve either adjacency or order. **False friend.** These words are not interchangeable even when a sample answer happens to satisfy several definitions.

- **Build - Author exercise: Classify `[2,4]`.** For `nums = [1,2,3,4]`, decide whether `[2,4]` is a subarray, subsequence, and subset. Explain each answer from index positions.
- **Vary - Author exercise: Order Matters.** For the same input, classify `[4,2]`. The changed decision is whether original relative order must be preserved.
- **Boundary - Author exercise: Empty Choice.** State whether an empty subarray or subsequence is legal only after reading the problem’s non-empty/empty contract; do not assume one universal convention.
- **Recognize - Author exercise: Contiguous Maximum.** Explain why “maximum sum subarray” cannot freely skip a negative middle value, while a maximum-sum subsequence may. Kadane’s algorithm remains deferred to Chapter 01.
