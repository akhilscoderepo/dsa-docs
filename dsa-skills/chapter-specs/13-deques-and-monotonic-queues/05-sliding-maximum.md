# Lesson spec: Sliding Maximum

**Recognition cue.** Every fixed-size contiguous window needs its maximum in linear total time. **Invariant.** The deque contains in-window indices in chronological order and decreasing value order; its front is the current maximum. **False friend.** A heap can work but needs lazy stale-entry removal and costs `O(n log k)`.

- **Build - Author exercise: Maximum Of One Moving Window.** Perform expiry, domination, append, then read the front.
- **Vary - Author exercise: Return Maximum Indices.** Expose why the deque stores positions rather than values alone.
- **Boundary - Author exercise: Increasing, Decreasing, And Equal Arrays.** Trace the three shapes that stress opposite ends of the deque.
- **Recognize - LC 239 Sliding Window Maximum.** Produce all maxima in `O(n)` time and `O(k)` space.
