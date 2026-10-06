# Lesson spec: Stop A Branch You Can Prove Fails

**Recognition cue.** A partial candidate cannot possibly become valid or beat the current best. **Invariant.** Every pruned branch is ruled out by a monotone constraint or proven bound, not by guesswork. **False friend.** Pruning because a branch “looks bad” risks deleting solutions.

- **Build - Author exercise: Positive Remaining Sum.** Stop when a sorted positive candidate exceeds the remaining target.
- **Vary - Author exercise: Remaining-Slots Bound.** Stop when too few elements remain to complete a fixed-size choice.
- **Boundary - Author exercise: Negative Values Break Sum Pruning.** Identify why an over-target sum could later recover.
- **Recognize - LC 51 N-Queens.** Reject a placement immediately when its column or diagonal is already occupied.
