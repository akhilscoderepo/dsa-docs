# Lesson spec: Stability And Ties

**Recognition cue.** Equal primary keys must retain or explicitly replace original order. **State.** The tie rule is part of correctness, not a cosmetic comparator detail. **Java hazard.** `Arrays.sort(Object[])` is stable; do not rely on primitive-array stability.

- **Build - Author exercise: Stable Score Sort.** Preserve arrival order for equal scores.
- **Vary - Author exercise: Explicit Index Tie.** Attach original index and sort by it when the API cannot promise the required stability.
- **Boundary - Author exercise: Comparator Equality.** Verify comparator returns zero only for interchangeable output positions.
- **Recognize - LC 1356 Sort Integers by The Number of 1 Bits.** The numeric tie rule must be explicit.
