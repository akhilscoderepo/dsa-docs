# Lesson spec: Invariant Ownership

**Recognition cue.** Several fields encode one logical structure and every mutating method must update them together. **Invariant.** Assign one method responsibility for each cross-field repair.

- **Build - Author exercise: Size Ownership.** Update size exactly once per successful mutation.
- **Vary - Author exercise: Sentinel List Links.** Centralize detach and insert operations.
- **Boundary - Author exercise: Failed Mutation.** Leave all fields unchanged when an operation is rejected.
- **Recognize - LC 146 LRU Cache.** Make map/list synchronization explicit.
