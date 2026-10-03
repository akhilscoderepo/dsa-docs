# Lesson spec: Cyclic Placement

**Recognition cue.** Each positive value has one intended slot, and mutation is allowed. **Invariant.** A value `v` belonging to `1..n` is either already at `v-1` or is swapped toward that slot. **False friend.** Sign marking records visits but does not put values into their final locations.

- **Build — Author exercise: Place 1..n.** Reorder a permutation of `1..n` so that `v` occupies index `v-1`.
- **Vary — LC 268 Missing Number.** Use the `0..n` placement/range contract and identify the unmatched index.
- **Boundary — Author exercise: Duplicate Slot.** Stop swapping when `nums[i] == nums[nums[i] - 1]`; this avoids an infinite duplicate cycle.
- **Recognize — LC 41 First Missing Positive.** Ignore values outside `1..n`; cyclic placement makes the first misplaced positive identify the answer.
