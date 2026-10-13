# Lesson spec: Bitmask Assignment

**Recognition cue.** A small set of used items must be part of the state. **Invariant.** Bit `i` records whether item `i` is already assigned; popcount often determines the next position. This lesson includes the needed mask primer because Chapter 30 is numbered later.

- **Build - Author exercise: Set Test And Clear Bits.** Represent a small used set in one integer.
- **Vary - Author exercise: Minimum Assignment Cost.** Add one unused item to the mask.
- **Boundary - Author exercise: Full Mask And State Count.** Stop at `(1 << n) - 1` and budget `2^n` memory.
- **Recognize - LC 698 Partition to K Equal Sum Subsets.** Use a mask and current-bucket state for small input.
