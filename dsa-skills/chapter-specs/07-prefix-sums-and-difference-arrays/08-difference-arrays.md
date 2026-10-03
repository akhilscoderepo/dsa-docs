# Lesson spec: Difference Arrays

**Recognition cue.** Many range additions are applied, and only the final materialized array is needed. **State.** A delta starts at `left` and is canceled immediately after `right`; one prefix reconstruction applies all updates. **False friend.** Prefix sums preprocess queries; difference arrays batch updates.

- **Build - Author exercise: One Range Add.** Add `value` to `[left,right]` using two delta writes.
- **Vary - LC 1109 Corporate Flight Bookings.** Accumulate many inclusive bookings.
- **Boundary - Author exercise: Final Endpoint.** Use a sentinel slot or guard `right + 1` when the update reaches the final index.
- **Recognize - LC 1094 Car Pooling.** Treat passenger changes as ordered coordinate deltas under the bounded-coordinate contract.
