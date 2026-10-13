# Lesson spec: Interval DP

**Recognition cue.** The answer for a contiguous interval depends on choosing a split or final operation inside it. **Invariant.** `dp[left][right]` owns exactly that interval and reads only shorter completed intervals.

- **Build - Author exercise: Best Split Of A Short Interval.** Combine left and right subinterval values around each split.
- **Vary - Author exercise: Matrix Chain Cost.** Minimize multiplication cost across split positions.
- **Boundary - Author exercise: Empty And Singleton Intervals.** Define neutral base values explicitly.
- **Recognize - LC 312 Burst Balloons.** Choose the last balloon removed inside each interval.
