# Lesson spec: Two-List Intersection

**Recognition cue.** Two lists are individually sorted and disjoint, and the output needs all pairwise overlaps. **Invariant.** The current pair is the only unresolved cross-list pair involving both current intervals; after emitting their intersection, the interval with the smaller end cannot meet a later interval in the other list. **False friend.** Merging the lists computes a union, not intersections.

- **Build - Author exercise: Intersect One Pair.** Return `[max(start), min(end)]` only when it is nonempty under the endpoint contract.
- **Vary - Author exercise: One Interval Against A Sorted List.** Advance past intervals that end before the fixed interval begins.
- **Boundary - Author exercise: Touching Intersections.** Compare the closed and half-open answers at equal endpoints.
- **Recognize - LC 986 Interval List Intersections.** Emit an overlap and advance the interval with the smaller end.
