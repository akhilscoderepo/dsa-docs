# Lesson spec: Interval Scheduling

**Recognition cue.** The objective selects the largest compatible set or uses the fewest points to cover overlapping intervals. **Invariant.** Keeping the earliest possible finishing boundary leaves at least as much room for all future choices. **False friend.** Sorting by start is natural for merging but does not prove maximum compatible selection.

- **Build - Author exercise: Choose Compatible Meetings.** Sort by end and accept the next nonoverlapping interval.
- **Vary - LC 435 Non-overlapping Intervals.** Count rejected intervals while retaining the earlier finishing one.
- **Boundary - Author exercise: Touching Endpoint Contract.** Decide compatibility using the declared closed or half-open model.
- **Recognize - LC 452 Minimum Number of Arrows to Burst Balloons.** Place one arrow at the current overlap group's earliest end.
