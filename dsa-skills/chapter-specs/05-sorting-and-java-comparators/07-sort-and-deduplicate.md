# Lesson spec: Remove Duplicates After Sorting

**Recognition cue.** Equal values become adjacent after sorting, and output needs one representative or a count per run. **State.** The current run is the only unresolved duplicate group. **False friend.** Sorted in-place deduplication from Arrays assumes the input was already sorted.

- **Build - LC 217 Contains Duplicate.** Sort a copy, then compare neighbors.
- **Vary - LC 349 Intersection of Two Arrays.** Emit each common run once.
- **Boundary - Author exercise: All Equal.** Verify one emitted representative from `[4,4,4]`.
- **Recognize - LC 720 Longest Word in Dictionary.** A sorted word order can make deterministic tie choice explicit.
