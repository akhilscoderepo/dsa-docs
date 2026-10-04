# Lesson spec: Comparing Time And Space Complexity Trade-Offs

**Recognition cue.** Two correct solutions consume different combinations of time, memory, preprocessing, or mutation. **State.** Name `n`, any secondary dimension, and the exact operation being counted. **Invariant.** The stated bound must describe the dominant work on the worst legal input. **False friend.** Two loops written next to each other are additive; two loops nested over the same growing input are usually multiplicative.

- **Build - Author exercise: Consecutive Loops.** Determine the time cost of scanning an `n`-element array twice. Explain why `O(n) + O(n)` simplifies to `O(n)`.
- **Vary - Author exercise: Triangular Work.** Count iterations of `for (i = 0; i < n; i++) for (j = i + 1; j < n; j++)`. Derive `n(n-1)/2` and classify it as `O(n^2)`.
- **Boundary - Author exercise: Two Dimensions.** A grid has `rows` and `cols`. State traversal time as `O(rows * cols)` rather than silently calling both dimensions `n`.
- **Recognize - Author exercise: Sort Then Scan.** Compare `O(n^2)` all-pairs work with `O(n log n)` sorting followed by `O(n)` scanning. State the tradeoff: changed order, possible mutation/copying, and lower asymptotic time.
