# Lesson spec: Coordinate Compression

**Recognition cue.** Values are sparse or huge, but only relative order and equality matter. **Invariant.** Each distinct value maps to a dense rank preserving order.

- **Build - Author exercise: Compress Distinct Values.** Sort, deduplicate, and map ranks.
- **Vary - Author exercise: Preserve Equal Ranks.** Give duplicates the same coordinate.
- **Boundary - Author exercise: Negative And Extreme Values.** Compare safely and do not use values as raw array indices.
- **Recognize - LC 1649 Create Sorted Array through Instructions.** Query counts below and above each compressed rank with a Fenwick tree.
