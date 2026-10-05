# Lesson spec: Merge Intervals And Insert A New One

**Recognition cue.** Overlapping ranges should become their union, or one new range must be added to an already sorted disjoint list. **Invariant.** The output contains finalized disjoint intervals plus at most one active interval that may still grow. **False friend.** Insert does not require re-sorting when the input contract already supplies order and disjointness.

- **Build - LC 56 Merge Intervals.** Sort by start and extend the active end while overlap continues.
- **Vary - Author exercise: Merge Already-Sorted Intervals.** Remove the sorting step under an explicit ordered-input contract.
- **Boundary - Author exercise: One Interval Covers Many.** Let one long range absorb several following ranges and touching endpoints.
- **Recognize - LC 57 Insert Interval.** Emit intervals before the new range, merge its overlap block, then emit intervals after it.
