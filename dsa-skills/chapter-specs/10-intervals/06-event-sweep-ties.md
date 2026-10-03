# Lesson spec: Event Sweep Ties

**Recognition cue.** The answer depends on how many intervals are active at each coordinate rather than on their merged geometry. **Invariant.** The running count equals the number of active intervals after all events at the current coordinate have been processed in contract-defined order. **False friend.** Sorting starts and ends independently can find a maximum count, but an explicit event stream is clearer when ties or multiple event types matter.

- **Build - Author exercise: Maximum Concurrent Half-Open Intervals.** Emit `+1` at starts and `-1` at ends, processing an end before a same-time start.
- **Vary - Author exercise: Maximum Concurrent Closed Intervals.** Reverse the equal-coordinate priority because touching closed intervals overlap.
- **Boundary - Author exercise: Many Events At One Coordinate.** Group or order ties so the running count cannot depend on input order.
- **Recognize - Author exercise: First Coordinate Reaching Capacity.** Sweep events and return the earliest point where active count reaches a supplied limit.
