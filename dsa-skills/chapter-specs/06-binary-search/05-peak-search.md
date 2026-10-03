# Lesson spec: Peak Search

**Recognition cue.** Local slope determines which side must contain a peak. **Invariant.** Comparing `nums[mid]` with `nums[mid+1]` preserves at least one peak in the remaining interval. **False friend.** This is not target search; equality and direction mean something different.

- **Build - LC 852 Peak Index in a Mountain Array.** Use the guaranteed rise-then-fall shape.
- **Vary - LC 162 Find Peak Element.** Preserve any peak without a unique mountain guarantee.
- **Boundary - Author exercise: Endpoint Peak.** Trace strictly increasing and strictly decreasing arrays.
- **Recognize - LC 1095 Find in Mountain Array.** Peak discovery precedes two ordered searches; API-call cost becomes part of the contract.
