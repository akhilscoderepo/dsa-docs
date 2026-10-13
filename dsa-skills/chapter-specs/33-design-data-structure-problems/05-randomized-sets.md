# Lesson spec: Pick A Random Value In Constant Time

**Recognition cue.** Insert, remove, membership, and uniform random selection must all be expected constant time. **Invariant.** The array contains exactly current values; the map stores each value's exact array index.

- **Build - Author exercise: Swap-With-Last Removal.** Move the last value into the deleted slot.
- **Vary - LC 380 Insert Delete GetRandom O(1).** Sample a uniform array index.
- **Boundary - Author exercise: Removing The Last Value.** Update in an order that does not resurrect the deleted map entry.
- **Recognize - LC 381 Insert Delete GetRandom O(1) - Duplicates Allowed.** Replace one index with a set of indices per value.
