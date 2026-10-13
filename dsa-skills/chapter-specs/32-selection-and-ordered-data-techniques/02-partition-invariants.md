# Lesson spec: Partition Invariants

**Recognition cue.** Values must be divided around a pivot in-place. **Invariant.** Each pointer delimits finalized less/equal/greater and unresolved regions.

- **Build - Author exercise: Lomuto Partition.** Maintain a prefix strictly below the pivot.
- **Vary - Author exercise: Three-Way Partition.** Group values below, equal, and above the pivot.
- **Boundary - Author exercise: All Equal Values.** Guarantee pointer progress and correct equal region.
- **Recognize - LC 215 Kth Largest Element in an Array.** Use pivot rank to discard one partition.
