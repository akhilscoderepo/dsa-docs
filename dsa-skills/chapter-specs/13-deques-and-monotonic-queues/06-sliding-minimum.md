# Lesson spec: Find The Minimum Of Every Window

**Recognition cue.** Every fixed-size range needs its minimum and the same chronological expiry rule applies. **Invariant.** Values increase from front to back, so the front is the minimum among surviving indices. **False friend.** Copying maximum-window code without reversing every domination comparison silently returns maxima.

- **Build - Author exercise: Minimum Of Every K-Window.** Reverse the value comparison used by the maximum deque.
- **Vary - Author exercise: Window Range.** Maintain a maximum deque and minimum deque, then return `max - min` for each fixed window.
- **Boundary - Author exercise: Duplicate Minima Expire.** Ensure a later equal minimum survives after the earlier index leaves.
- **Recognize - LC 1438 Longest Continuous Subarray With Absolute Difference Less Than or Equal to Limit.** Use both deques while a variable window restores its range constraint.
