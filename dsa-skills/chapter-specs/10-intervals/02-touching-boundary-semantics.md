# Lesson spec: Decide When Touching Intervals Overlap

**Recognition cue.** Correctness changes when one interval ends exactly where another begins. **Invariant.** The overlap predicate follows the declared model: closed `[a,b]`, open, or half-open `[a,b)`. **False friend.** Memorizing `<=` or `<` without the contract produces plausible but inconsistent answers.

- **Build - Author exercise: Closed Interval Overlap.** Decide whether `[1,3]` and `[3,5]` overlap when both endpoints are included.
- **Vary - Author exercise: Half-Open Reservations.** Decide whether `[1,3)` and `[3,5)` require the same resource.
- **Boundary - Author exercise: Zero-Length Range.** State whether `[x,x]` is one point and whether `[x,x)` is empty.
- **Recognize - Author exercise: Merge Under A Supplied Contract.** Implement the same scan twice with only the overlap predicate changed.
