# Lesson spec: Count Subarrays With A Target Sum

**Recognition cue.** Count subarrays whose additive relation can be written as `currentPrefix - earlierPrefix = target`. **State.** A frequency map records how many earlier prefixes have each value. **Invariant.** Seed prefix zero once so subarrays beginning at index zero are counted.

- **Build - LC 560 Subarray Sum Equals K.** Look up `prefix - k` before recording the current prefix.
- **Vary - LC 930 Binary Subarrays With Sum.** Apply the same count state to a binary domain.
- **Boundary - Author exercise: Zero Target.** Repeated equal prefixes create multiple zero-sum subarrays; a set would undercount them.
- **Recognize - LC 1248 Count Number of Nice Subarrays.** Convert odd values to one and count target-sum subarrays.
