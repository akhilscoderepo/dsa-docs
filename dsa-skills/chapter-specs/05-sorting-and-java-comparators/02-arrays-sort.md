# Lesson spec: Sort A Primitive Array

**Recognition cue.** Primitive values need a complete natural ordering and mutation of the input is permitted. **Invariant.** After `Arrays.sort(nums)`, every adjacent pair is nondecreasing and equal values form contiguous runs. **False friend.** `Arrays.sort(int[])` cannot accept a custom comparator.

- **Build - Author exercise: Sort A Primitive Copy.** Preserve the caller's array by copying before sorting.
- **Vary - Author exercise: Sort A Subrange.** State the inclusive/exclusive bounds used by the Java API.
- **Boundary - Author exercise: Empty, Singleton, And Extreme Values.** Verify natural ordering without comparator subtraction.
- **Recognize - LC 217 Contains Duplicate.** Sort, then detect equal adjacent values.
