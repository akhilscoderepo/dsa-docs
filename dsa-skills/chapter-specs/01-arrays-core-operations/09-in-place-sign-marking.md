# Lesson spec: In-Place Sign Marking

**Recognition cue.** Values are in `1..n`, the input may be mutated, and the question asks which values have appeared rather than where every value belongs. **Invariant.** The sign of slot `v-1` records whether value `v` has been observed; use `abs(nums[i])` because a previously visited slot may already be negative. **False friend.** Cyclic placement uses swaps to restore locations; sign marking only records membership.

- **Build — LC 448 Find All Numbers Disappeared in an Array.** Mark `abs(value)-1` negative and collect still-positive slots.
- **Vary — LC 442 Find All Duplicates in an Array.** If the target slot is already negative, the value is a duplicate; otherwise mark it.
- **Boundary — Author exercise: Re-read a Marked Value.** Explain why indexing with a negative value is invalid and why `Math.abs` is required.
- **Recognize — LC 645 Set Mismatch.** Use sign marking to identify the repeated value, then find the position that remains positive to recover the missing value.
