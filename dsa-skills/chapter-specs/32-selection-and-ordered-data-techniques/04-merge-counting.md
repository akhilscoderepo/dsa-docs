# Lesson spec: Merge Counting

**Recognition cue.** Count cross-pairs satisfying an order relation faster than all-pairs comparison. **Invariant.** Recursive halves are sorted; a monotone pointer counts an entire valid suffix or prefix at once before merge.

- **Build - Author exercise: Count Inversions.** Count left values greater than right values during merge.
- **Vary - LC 315 Count of Smaller Numbers After Self.** Preserve original indices while merging.
- **Boundary - Author exercise: Equal Values.** Match strict versus non-strict comparison to the contract.
- **Recognize - LC 493 Reverse Pairs.** Count `nums[i] > 2 * nums[j]` with `long` arithmetic before merging.
