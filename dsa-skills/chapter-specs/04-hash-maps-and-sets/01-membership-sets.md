# Lesson spec: Check Membership With A Set

**Recognition cue.** The question asks whether something has appeared, exists, or is forbidden; its count and order do not matter. **State.** `seen` contains exactly the relevant values processed so far. **False friend.** A map is needless when membership alone answers the question.

- **Build - LC 217 Contains Duplicate.** Given `nums`, return whether any value appears at least twice. `[1,2,3,1] -> true`; `[1,2,3,4] -> false`. Hint: what fact must be remembered after each value?
- **Vary - LC 349 Intersection of Two Arrays.** Return the distinct values present in both arrays. `[1,2,2,1], [2,2] -> [2]`; `[], [1] -> []`.
- **Boundary - LC 202 Happy Number.** Detect the repeated numeric state rather than allowing an infinite loop. `19 -> true`; `2 -> false`.
- **Recognize - LC 128 Longest Consecutive Sequence.** Start only at values whose predecessor is absent; this prevents repeatedly expanding the same run.
