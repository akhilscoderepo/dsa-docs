# Lesson spec: Skip Equal Values At One Level

**Recognition cue.** Equal input values create identical sibling branches. **Invariant.** After sorting, skip `candidates[i] == candidates[i-1]` only when both are choices at the same recursion depth. **False friend.** Skipping every repeated value prevents valid results containing multiple equal occurrences.

- **Build - Author exercise: Equal Sibling Choices.** Show why two identical first choices generate the same subtree.
- **Vary - LC 90 Subsets II.** Skip duplicates within one loop depth.
- **Boundary - Author exercise: Equal Values At Different Depths.** Permit `[2,2]` when two copies exist.
- **Recognize - LC 40 Combination Sum II.** Combine one-use candidates, target pruning, and same-depth skipping.
