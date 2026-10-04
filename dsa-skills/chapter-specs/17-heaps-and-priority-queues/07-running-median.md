# Lesson spec: Running Median

**Recognition cue.** Values arrive online and each prefix needs its median. **Invariant.** A max-heap owns the lower half, a min-heap owns the upper half, their sizes differ by at most one, and every lower value is no greater than every upper value. **False friend.** One heap exposes only one extreme, not the center.

- **Build - Author exercise: Rebalance Two Halves.** Insert one value and move roots until the size invariant holds.
- **Vary - LC 295 Find Median from Data Stream.** Return one root for odd size or the average of two roots for even size.
- **Boundary - Author exercise: Overflow-Safe Even Median.** Convert to `long` or `double` before adding extreme integers.
- **Recognize - LC 480 Sliding Window Median.** Add expiry through lazy deletion while preserving logical heap sizes.
