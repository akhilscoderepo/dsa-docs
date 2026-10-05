# Lesson spec: Split An Array In Three

**Recognition cue.** Values belong to low, middle, or high regions. **Invariant.** `[0,low)` is low, `[low,mid)` is middle, `[mid,high]` unresolved, and `(high,n)` high. This is the Dutch national flag partition.

- **Build - Author exercise: Partition 0,1,2.** Implement the four-region invariant on a short array.
- **Vary - LC 75 Sort Colors.** Apply the same category meanings to the formal problem.
- **Boundary - Author exercise: Reinspect Swapped High.** After swapping with `high`, do not advance `mid`; the incoming value is unresolved.
- **Recognize - Author exercise: Three-Way Pivot Partition.** Replace colors with `< pivot`, `== pivot`, and `> pivot`.
