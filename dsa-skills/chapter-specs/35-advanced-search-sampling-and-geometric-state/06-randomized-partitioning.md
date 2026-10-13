# Lesson spec: Randomized Partitioning

**Recognition cue.** Partition-based selection risks adversarial pivots. **Invariant.** A uniformly random pivot makes expected partition balance independent of input order while correctness remains deterministic after pivot choice.

- **Build - Author exercise: Uniform Pivot Index.** Sample within the active inclusive range.
- **Vary - Author exercise: Randomized Quickselect.** Partition and retain only the target side.
- **Boundary - Author exercise: Equal Values.** Use three-way partitioning to avoid repeated near-identical work.
- **Recognize - LC 215 Kth Largest Element in an Array.** Explain expected linear time and worst-case quadratic time.
