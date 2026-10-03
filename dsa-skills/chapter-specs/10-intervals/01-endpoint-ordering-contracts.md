# Lesson spec: Endpoint Ordering Contracts

**Recognition cue.** Each record describes a range and the algorithm needs a reliable order before making local overlap decisions. **Invariant.** Intervals already processed precede every unresolved interval under the stated comparator. **False friend.** Sorting by end supports selection problems, but it does not replace sorting by start for ordinary merging. **Java hazard.** Use `Integer.compare(a[0], b[0])`, not subtraction that can overflow.

- **Build - Author exercise: Order By Start Then End.** Sort intervals lexicographically and explain the tie rule.
- **Vary - Author exercise: Order By End Then Start.** Change the comparator for a scheduling objective and state what decision it enables.
- **Boundary - Author exercise: Equal And Extreme Endpoints.** Test equal starts and integer extremes with safe comparisons.
- **Recognize - LC 56 Merge Intervals.** Choose start order because only the current merged interval can overlap the next one.
