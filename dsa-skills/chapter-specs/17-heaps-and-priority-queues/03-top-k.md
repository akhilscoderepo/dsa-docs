# Lesson spec: Top K

**Recognition cue.** Only the best `k` elements matter, so the weakest retained candidate should be cheap to replace. **Invariant.** A size-`k` heap contains the best `k` items seen; its root is the retention boundary. **False friend.** A max-heap holding every item works for extraction but wastes space when `k` is small.

- **Build - Author exercise: K Largest Values.** Keep a size-`k` min-heap and replace its root when a larger value arrives.
- **Vary - LC 215 Kth Largest Element in an Array.** Return the root after scanning all values.
- **Boundary - Author exercise: K Equals One Or N.** Preserve the same invariant at both extremes.
- **Recognize - LC 347 Top K Frequent Elements.** Count with a map, then heap-select by frequency.
