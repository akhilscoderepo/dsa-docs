# Lesson spec: Dynamic Rankings

**Recognition cue.** Scores change while queries request the next, top, or lowest ranked entity. **Invariant.** Comparator order is total, tie policy is explicit, and updates remove the exact old key before inserting the new key.

- **Build - LC 1244 Design A Leaderboard.** Maintain scores and top-`k` totals.
- **Vary - LC 2102 Sequentially Ordinal Rank Tracker.** Partition returned and not-yet-returned ranks.
- **Boundary - Author exercise: Equal Scores And Renames.** Use a comparator consistent with identity.
- **Recognize - LC 3408 Design Task Manager.** Update priority and execute the global best task.
