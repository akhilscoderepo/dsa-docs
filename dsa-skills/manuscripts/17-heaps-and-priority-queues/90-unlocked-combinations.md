<!-- section: unlocked-combinations -->
## Unlocked Combinations

One combination has every prerequisite in place and is taught in full. A second is recorded as deferred, with the chapters that own what it still lacks, and a third group points back to lessons that already exist.

### Teach Now

The heap with intervals is the eighth lesson. Sorting by start time contributes the order in which intervals are met, and the heap of end times contributes a direct answer to which resource frees first. Together they decide whether a new interval can reuse a resource or must open another one. The lesson works through one loop that answers several questions: whether any two meetings clash, how many rooms are needed, how many groups are needed when touching endpoints count as overlap, and what the smallest interval is that contains each of many query points. The ladder moves from a plain sorted neighbour check, through the end heap and a flipped tie rule, to a heap ordered by size in which entries expire at the root. The false friend is the merging of overlapping intervals, which loses the number of intervals that run at once.

### Deferred

Shortest paths on a graph also take the smallest entry from a heap, but their correctness rests on edge relaxation and on a rule for stale distances that depends on a model of graph state. Graph traversal is introduced in Chapter 21, and Chapter 24 owns shortest paths and their stale-entry reasoning. This chapter assigns no problem of that kind.

### Already Covered

Sorting intervals by start and reasoning about where one interval touches the next were taught in Chapter 10, and the lessons here rely on them without repeating the merge routine. The comparator rules behind a tuple order came from Chapter 05 and are tightened in the second lesson. The counting map used to rank frequencies belongs to Chapter 04, and the habit of discarding what can never answer a query again follows the reasoning of the monotonic chapters. A deque answers a window maximum in linear time, as taught in Chapter 13, and the heap-based window median of this chapter does not replace it.
