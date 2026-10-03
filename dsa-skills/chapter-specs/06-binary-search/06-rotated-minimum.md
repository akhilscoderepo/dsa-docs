# Lesson spec: Rotated Minimum

**Recognition cue.** A strictly increasing array was rotated and only the pivot/minimum is needed. **Invariant.** Comparison with the right endpoint identifies which side contains the discontinuity.

- **Build - LC 153 Find Minimum in Rotated Sorted Array.** `[3,4,5,1,2] -> 1`; `[1,2,3] -> 1`.
- **Vary - Author exercise: Rotation Count.** Return the minimum’s index.
- **Boundary - Author exercise: Two Values.** Trace `[2,1]` and `[1,2]`.
- **Recognize - LC 154 Find Minimum in Rotated Sorted Array II.** Duplicates can destroy the strict comparison; shrinking equality may degrade to linear time.
