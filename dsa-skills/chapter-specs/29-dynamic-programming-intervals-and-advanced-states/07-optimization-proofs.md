# Lesson spec: Optimization Proofs

**Recognition cue.** A correct DP is too slow or large, and structure may reduce transitions or memory. **Invariant.** The optimization must preserve every dependency and candidate needed by the original recurrence.

- **Build - Author exercise: Roll One Dimension.** Prove only the previous layer is read.
- **Vary - Author exercise: Prefix-Minimum Transition.** Replace a repeated range scan with a maintained aggregate.
- **Boundary - Author exercise: In-Place Direction Counterexample.** Show how wrong order changes reuse semantics.
- **Recognize - Author exercise: Optimization Audit.** State original recurrence, dependency set, replacement structure, and resulting complexity.
