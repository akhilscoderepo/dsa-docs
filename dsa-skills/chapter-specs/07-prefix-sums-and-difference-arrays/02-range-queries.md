# Lesson spec: Range Queries

**Recognition cue.** The input is unchanged and many contiguous range sums are requested. **Invariant.** `sum(left..right) = prefix[right+1] - prefix[left]` under the sentinel convention. **False friend.** A sliding window answers one moving family of ranges; it does not provide arbitrary query lookup.

- **Build - LC 303 Range Sum Query - Immutable.** Preprocess once and answer each query in `O(1)`.
- **Vary - Author exercise: Half-Open Query.** Accept `[left,right)` and derive the corresponding formula.
- **Boundary - Author exercise: Whole Array.** Query `[0,n-1]` without reading before index zero.
- **Recognize - LC 1310 XOR Queries of a Subarray.** Replace addition/subtraction with XOR cancellation; the dedicated XOR lesson follows.
