# Lesson spec: Split An Array In Two

**Recognition cue.** Output needs two regions and relative order is not required. **Invariant.** Values before the boundary satisfy one category; unresolved values remain outside final regions. **False friend.** Stable compaction preserves order and may perform more writes.

- **Build - LC 905 Sort Array By Parity.** Swap misplaced values from opposite regions.
- **Vary - Author exercise: Partition Around Pivot.** Place values `< pivot` before values `>= pivot` without promising internal order.
- **Boundary - Author exercise: One Empty Region.** Test all-even and all-odd arrays.
- **Recognize - LC 922 Sort Array By Parity II.** Pointer positions encode even and odd destination classes.
