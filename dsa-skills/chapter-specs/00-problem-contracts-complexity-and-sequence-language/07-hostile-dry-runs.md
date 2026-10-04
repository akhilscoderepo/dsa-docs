# Lesson spec: Writing Edge-Case Tests

**Recognition cue.** A plausible implementation depends on an unstated happy-path assumption. **State.** Select the smallest input that attacks initialization, equality, boundaries, overflow, or mutation order. **Invariant.** A dry run must track variable meanings after every state change, not merely reproduce the sample output. **False friend.** Large random tests are poor substitutes for a tiny case designed around one failure mode.

- **Build - Author exercise: Singleton.** Dry-run a loop over `[7]`. Verify initialization, the number of iterations, and the returned value.
- **Vary - Author exercise: All Equal.** Use `[4,4,4]` to test strict versus non-strict comparisons and duplicate handling.
- **Boundary - Author exercise: Numeric Extremes.** Use `[Integer.MAX_VALUE, Integer.MAX_VALUE]` against code that accumulates into `int`; predict the overflow before running it.
- **Recognize - Author exercise: Mutation Order.** For right-shifting `[1,2,3]` to insert at index 0, trace a left-to-right copy and show exactly where data is overwritten. Then justify right-to-left copying.
