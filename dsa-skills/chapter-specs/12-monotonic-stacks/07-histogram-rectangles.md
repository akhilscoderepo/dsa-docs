# Lesson spec: Histogram Rectangles

**Recognition cue.** Every bar may be the limiting height of a rectangle extending until the first smaller bar on either side. **Invariant.** Increasing stack indices await a right boundary; when a shorter bar arrives, the popped bar's right boundary is current and its left boundary is the new stack top. **False friend.** Next-smaller distance on only one side cannot determine rectangle width.

- **Build - Author exercise: Rectangle From Supplied Boundaries.** Compute `height * (right - left - 1)`.
- **Vary - Author exercise: Resolve On A Shorter Bar.** Pop bars and calculate widths during one left-to-right scan.
- **Boundary - Author exercise: Flush Increasing Heights.** Append a conceptual zero-height sentinel so every remaining bar is resolved.
- **Recognize - LC 84 Largest Rectangle in Histogram.** Maintain increasing indices and maximize each popped height's full width.
