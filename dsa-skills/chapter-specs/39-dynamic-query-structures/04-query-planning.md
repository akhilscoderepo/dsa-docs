# Lesson spec: Query Planning

**Recognition cue.** A constructor is followed by many queries whose constraints may justify preprocessing or offline ordering. **Invariant.** The chosen summary is sufficient for every query without rebuilding original work.

- **Build - LC 2080 Range Frequency Queries.** Store sorted positions per value.
- **Vary - LC 1157 Online Majority Element In Subarray.** Combine candidate selection with occurrence verification.
- **Boundary - Author exercise: No Majority Exists.** Verification must reject plausible but insufficient candidates.
- **Recognize - LC 1724 Checking Existence of Edge Length Limited Paths II.** Contrast online API requirements with offline sorted-query DSU.
