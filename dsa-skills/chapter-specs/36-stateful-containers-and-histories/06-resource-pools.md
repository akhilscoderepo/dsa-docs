# Lesson spec: Reuse Freed Identifiers From A Pool

**Recognition cue.** Identifiers or memory segments move between free and allocated states. **Invariant.** No resource is simultaneously free and allocated, and reuse follows the promised ordering rule.

- **Build - Author exercise: Reusable ID Pool.** Allocate and return identifiers exactly once.
- **Vary - LC 2336 Smallest Number in Infinite Set.** Combine an increasing frontier with returned smaller values.
- **Boundary - LC 379 Design Phone Directory.** Reject duplicate release and exhausted allocation.
- **Recognize - LC 2502 Design Memory Allocator.** Track contiguous free runs and release all blocks owned by one ID.
