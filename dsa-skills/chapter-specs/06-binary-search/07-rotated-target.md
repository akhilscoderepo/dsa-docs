# Lesson spec: Rotated Target

**Recognition cue.** A target must be found in a rotated array. **Invariant.** At least one half is normally sorted; determine it before asking whether the target belongs there. **False friend.** Finding the minimum alone does not finish target lookup.

- **Build - LC 33 Search in Rotated Sorted Array.** Identify the sorted half and discard only a half proved unable to contain the target.
- **Vary - Author exercise: Pivot Then Search.** Find the rotation index, then binary-search the appropriate sorted segment.
- **Boundary - LC 81 Search in Rotated Sorted Array II.** When left, mid, and right are equal, sorted-half identity is ambiguous.
- **Recognize - Author exercise: Explain Both Strategies.** Compare one-pass sorted-half search with pivot-plus-search; state complexity and proof obligations.
