# Lesson spec: Combination Counts

**Recognition cue.** Reusable values form a sum and order does not distinguish results. **Invariant.** Iterate candidates outside and amounts inside so each multiset is formed in one canonical candidate order.

- **Build - Author exercise: Count With One Coin.** Initialize `dp[0] = 1`.
- **Vary - LC 518 Coin Change II.** Add ways coin by coin.
- **Boundary - Author exercise: Empty Combination.** Amount zero has one construction even with no selected coins.
- **Recognize - Author exercise: Explain Loop Order.** Show why swapping loops counts sequences instead.
