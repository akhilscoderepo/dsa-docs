# Lesson spec: Mutable Range Queries

**Recognition cue.** Queries are no longer separated from updates. **Invariant.** Every tree node or Fenwick entry summarizes exactly its owned range after each mutation.

- **Build - LC 307 Range Sum Query - Mutable.** Upgrade prefix sums to point updates.
- **Vary - LC 308 Range Sum Query 2D - Mutable.** Extend ownership to two dimensions.
- **Boundary - Author exercise: Repeated Assignment.** Apply delta from the old value rather than adding the new value twice.
- **Recognize - Author exercise: Mutable Range Minimum.** Explain when a segment tree replaces a Fenwick tree.
