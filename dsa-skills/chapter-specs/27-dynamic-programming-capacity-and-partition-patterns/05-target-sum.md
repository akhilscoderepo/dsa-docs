# Lesson spec: Target Sum

**Recognition cue.** Each nonnegative value receives `+` or `-`, and assignments must reach a target. **Invariant.** Algebra converts sign assignments to selecting a subset with derived sum `(total + target)/2` when parity and range permit it.

- **Build - Author exercise: Derive The Subset Equation.** Separate positive and negative groups.
- **Vary - Author exercise: Count Derived Subsets.** Count one-use subsets reaching the derived target.
- **Boundary - Author exercise: Zero Values And Parity.** Zero doubles assignment counts; invalid parity returns zero.
- **Recognize - LC 494 Target Sum.** Apply the reduction with counting DP.
