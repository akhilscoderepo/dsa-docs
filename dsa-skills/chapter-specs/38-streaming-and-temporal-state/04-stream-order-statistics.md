# Lesson spec: Stream Order Statistics

**Recognition cue.** Inserts, corrections, or removals must preserve a median, rank, or trimmed aggregate. **Invariant.** Ordered partitions cover every active value exactly once and satisfy their size/order relation.

- **Build - LC 295 Find Median from Data Stream.** Balance lower and upper heaps.
- **Vary - LC 2034 Stock Price Fluctuation.** Correct old timestamps while min/max remain queryable.
- **Boundary - Author exercise: Duplicate And Stale Heap Roots.** Validate heap entries before use.
- **Recognize - LC 1825 Finding MK Average.** Maintain low, middle, and high multisets over a sliding window.
