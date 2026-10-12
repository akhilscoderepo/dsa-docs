# Lesson spec: State Definition

**Recognition cue.** Recursive subproblems repeat and their future answer depends on a small set of arguments. **Invariant.** `dp[state]` has one complete sentence defining exactly what it returns.

- **Build - Author exercise: Name The Subproblem.** Define `dp[i]` before writing a recurrence.
- **Vary - Author exercise: Add One Necessary Dimension.** Show why two calls with different remaining state cannot share a cache entry.
- **Boundary - Author exercise: Base-State Contract.** Make every transition terminate at a defined state.
- **Recognize - LC 70 Climbing Stairs.** Define ways to reach or leave index `i` consistently.
