# Lesson spec: Unbounded Knapsack

**Recognition cue.** Items have weight and value, capacity is limited, and an item may be reused. **Invariant.** Increasing capacity order allows the current item to contribute again.

- **Build - Author exercise: One Reusable Item.** Fill every feasible capacity multiple.
- **Vary - Author exercise: Maximum Value With Reuse.** Compare skipping with taking from a smaller current-row capacity.
- **Boundary - Author exercise: Zero Capacity.** Prevent zero-weight positive-value items unless the contract excludes them.
- **Recognize - LC 279 Perfect Squares.** Treat square numbers as reusable item weights minimizing count.
