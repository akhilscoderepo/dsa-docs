# Lesson spec: Circular Kadane

**Recognition cue.** A contiguous answer may wrap from the final index back to the first. **Invariant.** A wrapping maximum equals `totalSum - minimumOrdinarySubarray`; compare it with ordinary Kadane and forbid the empty remainder. **False friend.** A fixed-length circular window has a different state.

- **Build — LC 918 Maximum Sum Circular Subarray.** `[1,-2,3,-2] → 3`; `[5,-3,5] → 10`.
- **Vary — Author exercise: Circular Minimum.** Compute the smallest non-empty circular subarray using the symmetric maximum-exclusion argument.
- **Boundary — Author exercise: All Negative.** `[-3,-2,-3] → -2`; explain why the wrap candidate is invalid.
- **Recognize — LC 918 with a proof prompt.** State why every wrapping choice excludes exactly one ordinary contiguous middle segment.
