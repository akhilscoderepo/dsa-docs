# Lesson spec: Transaction Variants

**Recognition cue.** Cooldown, fee, or transaction count changes which transitions are legal. **Invariant.** Every state represents both possession and the restriction needed for the next action.

- **Build - LC 309 Best Time to Buy and Sell Stock with Cooldown.** Add a state that prevents immediate rebuy.
- **Vary - LC 714 Best Time to Buy and Sell Stock with Transaction Fee.** Charge the fee on exactly one transition.
- **Boundary - Author exercise: Update Aliasing.** Compute new states from old states, not partially overwritten values.
- **Recognize - LC 123 Best Time to Buy and Sell Stock III.** Add transaction-count state for at most two completed sales.
