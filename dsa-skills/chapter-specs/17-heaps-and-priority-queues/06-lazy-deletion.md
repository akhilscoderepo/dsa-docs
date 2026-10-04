# Lesson spec: Lazy Deletion

**Recognition cue.** Priorities change or items expire, but arbitrary heap removal would be linear. **Invariant.** Before using the root, discard entries whose stored version, count, or eligibility no longer matches companion state. **False friend.** `PriorityQueue.remove(Object)` and `contains` are linear, not logarithmic.

- **Build - Author exercise: Versioned Priorities.** Insert a new record after an update and ignore old versions when polled.
- **Vary - Author exercise: Delayed Removal Counts.** Record logical deletions in a map and clean matching roots on demand.
- **Boundary - Author exercise: Several Stale Roots.** Clean in a loop and handle equal values with multiple outstanding copies.
- **Recognize - LC 480 Sliding Window Median.** Combine delayed deletion with two balanced heaps.
