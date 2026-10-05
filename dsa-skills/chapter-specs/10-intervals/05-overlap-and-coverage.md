# Lesson spec: Keep The Most Intervals Without Overlap

**Recognition cue.** The objective is to keep many compatible intervals, remove overlaps, or detect intervals fully covered by another. **Invariant.** For non-overlap selection, the kept interval has the smallest possible end among processed choices; for coverage, the greatest reachable end summarizes prior containers. **False friend.** Merging changes intervals and loses which original intervals should be removed.

- **Build - Author exercise: Keep Earlier Finishing Interval.** Given two overlapping intervals, identify which one leaves more room for future choices.
- **Vary - LC 435 Non-overlapping Intervals.** Sort by end and count intervals rejected by the greedy compatibility rule.
- **Boundary - LC 1288 Remove Covered Intervals.** Sort equal starts by descending end so a shorter interval cannot hide its container.
- **Recognize - LC 452 Minimum Number of Arrows to Burst Balloons.** Treat each arrow as a point kept inside the current intersection of compatible balloons.
