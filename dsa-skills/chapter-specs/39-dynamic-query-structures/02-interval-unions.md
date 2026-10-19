# Lesson spec: Interval Unions

**Recognition cue.** Public methods add, remove, or count covered coordinates over time. **Invariant.** Stored intervals remain disjoint, ordered, and use one explicit endpoint convention.

- **Build - LC 352 Data Stream as Disjoint Intervals.** Insert one point and merge adjacent runs.
- **Vary - LC 715 Range Module.** Add removal and coverage queries over half-open ranges.
- **Boundary - Author exercise: Touching And Empty Ranges.** Apply endpoint semantics consistently.
- **Recognize - LC 2276 Count Integers in Intervals.** Maintain total covered length while merging.
