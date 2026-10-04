# Lesson spec: Task Selection

**Recognition cue.** Tasks have capacities, deadlines, rewards, or costs, and the algorithm must decide which subset or order to keep. **Invariant.** The retained tasks are feasible under the processed constraint and are best according to the proven replacement rule. **False friend.** Sorting once is insufficient when feasibility can require ejecting an earlier choice.

- **Build - LC 1710 Maximum Units on a Truck.** Take available box types in descending unit value until capacity is filled.
- **Vary - Author exercise: Deadline-Compatible Unit Tasks.** Sort deadlines and take a task whenever one slot remains feasible.
- **Boundary - Author exercise: Equal Reward And Capacity Limit.** State a deterministic tie rule and use `long` for accumulated reward when required.
- **Recognize - LC 630 Course Schedule III.** Sort by deadline, retain durations, and eject the longest task when total time becomes infeasible.
