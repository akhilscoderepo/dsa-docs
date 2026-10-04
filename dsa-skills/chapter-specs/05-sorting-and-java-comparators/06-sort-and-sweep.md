# Lesson spec: Sweep A Sorted Array

**Recognition cue.** After sorting, only neighboring or frontier items can affect the next decision. **State.** A sweep summary owns everything still relevant from earlier items. **False friend.** Intervals add endpoint semantics and receive their full chapter later.

- **Build - LC 977 Squares of a Sorted Array.** Sorting supplies order, though Chapter 08 later gives the optimal two-pointer version.
- **Vary - LC 406 Queue Reconstruction by Height.** Process a sorted order and preserve the partial output invariant.
- **Boundary - Author exercise: A Long Run of Equal Values.** After sorting, compute the increments needed to make every value unique; use `long` for the accumulated cost and test a large duplicate run.
- **Recognize - LC 945 Minimum Increment to Make Array Unique.** After sorting, raise each value to at least one more than the previous finalized value.
