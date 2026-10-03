# Lesson spec: Balance Sentinels

**Recognition cue.** Every subtree needs a normal summary unless a failure below should terminate or propagate immediately. **Invariant.** The helper returns height for a balanced subtree and a distinguished sentinel for an unbalanced one. **False friend.** Recomputing height separately at every node turns a linear solution into quadratic time on a skewed tree.

- **Build - Author exercise: Height Or Failure.** Return `-1` immediately when a child already failed.
- **Vary - Author exercise: Detect Local Imbalance.** Compare child heights only after both are valid.
- **Boundary - Author exercise: Empty Tree Height.** Choose a base height consistent with the balance difference formula.
- **Recognize - LC 110 Balanced Binary Tree.** Combine detection and height calculation in one postorder pass.
