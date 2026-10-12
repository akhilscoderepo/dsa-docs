# Lesson spec: Grid DP

**Recognition cue.** Movement restrictions make each cell depend on already processed neighbors. **Invariant.** `dp[r][c]` describes paths or cost to exactly that cell.

- **Build - LC 62 Unique Paths.** Count from top and left.
- **Vary - LC 64 Minimum Path Sum.** Minimize accumulated cost.
- **Boundary - Author exercise: First Row And Column.** Initialize their single available predecessor direction.
- **Recognize - LC 63 Unique Paths II.** Make obstacle cells contribute zero ways.
