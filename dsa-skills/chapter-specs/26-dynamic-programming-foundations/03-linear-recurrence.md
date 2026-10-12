# Lesson spec: Linear Recurrence

**Recognition cue.** Each one-dimensional state depends on a fixed number of earlier states. **Invariant.** Before computing `dp[i]`, all referenced earlier states are final.

- **Build - LC 70 Climbing Stairs.** Sum the two predecessor counts.
- **Vary - LC 746 Min Cost Climbing Stairs.** Minimize cost instead of counting ways.
- **Boundary - Author exercise: Short Arrays.** Derive answers from the problem's legal starting positions.
- **Recognize - LC 1137 N-th Tribonacci Number.** Extend the recurrence window from two states to three.
