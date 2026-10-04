# Lesson spec: Local Choice

**Recognition cue.** A decision must be committed now, and a proof shows that replacing any optimal solution's first conflicting decision with this choice cannot make the remainder worse. **Invariant.** After each commitment, an optimal completion still exists for the unresolved suffix. **False friend.** Choosing the locally largest reward is not greedy correctness without a dominance or exchange proof.

- **Build - Author exercise: Smallest Sufficient Match.** Assign the smallest resource that satisfies the smallest remaining demand.
- **Vary - LC 455 Assign Cookies.** Sort both sides and commit only useful assignments.
- **Boundary - Author exercise: Unusable Resources.** Advance the resource pointer without consuming a demand it cannot satisfy.
- **Recognize - LC 860 Lemonade Change.** Preserve scarce five-dollar bills by selecting a safe change combination.
