# Lesson spec: Reusable Candidates

**Recognition cue.** A candidate may be chosen more than once, but result order still should not create duplicates. **Invariant.** Recurse with the same index after choosing a reusable candidate and a later index when skipping to the next candidate. **False friend.** Restarting at zero after every choice generates reordered duplicates.

- **Build - Author exercise: Sum With Repeated Coins.** Reuse the current candidate while the remaining target permits it.
- **Vary - LC 39 Combination Sum.** Generate nondecreasing combinations that reach the target.
- **Boundary - Author exercise: Candidate Larger Than Remainder.** Under positive sorted inputs, stop later candidates safely.
- **Recognize - Author exercise: Fixed-Length Reusable Sum.** Add a remaining-choice count without changing candidate reuse.
