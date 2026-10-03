# Lesson spec: Exact Search

**Recognition cue.** The array is sorted and the question asks whether or where one exact target occurs. **Invariant.** If the target exists, it remains inside the current search interval. **False friend.** Unsorted input has no safe half to discard.

- **Build - LC 704 Binary Search.** Return the target index or `-1`. `[-1,0,3,5,9,12], 9 -> 4`; `[5], 2 -> -1`.
- **Vary - Author exercise: Descending Search.** Reverse the comparison-to-movement rule under a descending-order contract.
- **Boundary - Author exercise: Two Elements.** Trace `[1,3]` for targets `1`, `3`, and `2`; prove the interval shrinks after every comparison.
- **Recognize - LC 74 Search a 2D Matrix.** Treat a globally row-major sorted matrix as one virtual sorted array; the full combination lesson appears below.
