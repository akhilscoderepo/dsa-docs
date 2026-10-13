# Lesson spec: Edit Distance

**Recognition cue.** One string becomes another through insert, delete, and replace operations. **Invariant.** `dp[i][j]` is minimum edits between fixed prefixes; each operation moves to its corresponding smaller state.

- **Build - Author exercise: Insert Or Delete Only.** Model two operations first.
- **Vary - LC 72 Edit Distance.** Add replacement and matching-character transitions.
- **Boundary - Author exercise: Empty String.** Distance equals the other prefix length.
- **Recognize - Author exercise: Reconstruct Operations.** Backtrack a valid optimal edit script.
