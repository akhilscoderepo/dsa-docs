# Lesson spec: Subset Masks

**Recognition cue.** A universe is small enough to enumerate all selected/unselected combinations. **Invariant.** Mask bit `i` states whether item `i` belongs to the subset.

- **Build - Author exercise: Enumerate All Masks.** Produce subsets for `0..(1<<n)-1`.
- **Vary - LC 78 Subsets.** Translate each mask into one result list.
- **Boundary - Author exercise: Exponential Budget.** State why enumeration is practical only for small `n`.
- **Recognize - LC 847 Shortest Path Visiting All Nodes.** Combine graph node and visited-set mask.
