# Lesson spec: Partition Generation

**Recognition cue.** The output divides an entire sequence into contiguous valid pieces. **Invariant.** `start` is the first unpartitioned position; each choice selects one valid ending and recursion owns the suffix after it. **False friend.** Subset search may skip elements, while a partition must consume every position exactly once.

- **Build - Author exercise: All Splits Of A Short String.** Choose every possible next endpoint.
- **Vary - Author exercise: Valid-Piece Predicate.** Recurse only when the selected segment satisfies a supplied rule.
- **Boundary - Author exercise: Empty Suffix Completion.** Record a result only when `start == length`.
- **Recognize - LC 131 Palindrome Partitioning.** Generate every partition whose pieces are palindromes.
