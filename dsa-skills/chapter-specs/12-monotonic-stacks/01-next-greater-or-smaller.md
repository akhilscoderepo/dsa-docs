# Lesson spec: Find The Next Greater Value

**Recognition cue.** Each position needs the first later value that crosses a greater/smaller threshold. **Invariant.** The stack stores unresolved indices in monotonic value order; the current value resolves every top it dominates. **False friend.** A globally greater value is not necessarily the next greater value. **Java hazard.** Store indices when the answer is a distance or position.

- **Build - Author exercise: Next Greater Value.** Scan left to right and fill an answer whenever the current value exceeds the unresolved stack top.
- **Vary - LC 739 Daily Temperatures.** Store indices and return the distance to the resolving warmer day.
- **Boundary - Author exercise: Equal Values Stay Unresolved.** Use strict comparison so an equal value is not mistaken for a greater one.
- **Recognize - LC 496 Next Greater Element I.** Precompute next-greater values for the reference array and answer lookups for the subset.
