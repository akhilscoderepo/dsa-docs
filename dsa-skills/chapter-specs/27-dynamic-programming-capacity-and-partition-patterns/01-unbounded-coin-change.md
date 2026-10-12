# Lesson spec: Unbounded Coin Change

**Recognition cue.** Each positive denomination may be reused and the objective minimizes item count. **Invariant.** `dp[a]` is the minimum coins for amount `a`; increasing amounts permit reuse of the current coin.

- **Build - Author exercise: One Denomination.** Mark reachable multiples and impossible amounts.
- **Vary - LC 322 Coin Change.** Minimize across all last-coin choices.
- **Boundary - Author exercise: Amount Zero And Impossible Target.** Return zero or the specified failure value.
- **Recognize - Author exercise: Reconstruct One Minimum Set.** Store the chosen final coin with each improvement.
