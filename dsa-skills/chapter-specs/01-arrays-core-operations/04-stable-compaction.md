# Lesson spec: Stable Compaction

**Recognition cue.** Keep selected values in original order while reusing the input array. **Invariant.** `nums[0..write-1]` contains exactly the accepted values already read, in order. **Java contract.** Return `write`; never claim the suffix was removed.

- **Build — LC 27 Remove Element.** Filter a value with one read index and one write index.
- **Vary — LC 283 Move Zeroes.** Keep non-zero values stable, then fill the remaining suffix with zeroes. `[0,1,0,3,12] → [1,3,12,0,0]`; `[0] → [0]`.
- **Boundary — Author exercise: Keep Evens.** Given `nums`, overwrite its prefix with its even values and return `k`. `[-2,3,4] → [-2,4], k=2`; `[1,3] → k=0`.
- **Recognize — Author exercise: Filter Positives.** Given `nums`, overwrite its prefix with positive values in their original order and return `k`. The test changes, but the read/write invariant does not.
