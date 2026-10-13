# Lesson spec: Common Subsequences

**Recognition cue.** Two sequences may skip characters while preserving relative order. **Invariant.** `dp[i][j]` is the best result for stated prefixes or suffixes; equal characters match, otherwise one side is skipped.

- **Build - Author exercise: LCS Of Short Prefixes.** Fill match and mismatch transitions.
- **Vary - LC 1143 Longest Common Subsequence.** Build the full table.
- **Boundary - Author exercise: Empty Prefix.** Initialize zero row and column.
- **Recognize - LC 583 Delete Operation for Two Strings.** Express deletions through LCS length.
