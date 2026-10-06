# Lesson spec: Undo Each Choice After Exploring It

**Recognition cue.** The algorithm builds one candidate, explores consequences, then must restore shared mutable state before trying a sibling. **Invariant.** On entry to each call, the working state represents exactly the choices on the current recursion path. **False friend.** Forgetting the unchoose step leaks one branch into another.

- **Build - Author exercise: Binary Choices.** Append one choice, recurse, then remove it before the alternative.
- **Vary - Author exercise: Variable Candidate Loop.** Apply the same mutation discipline to several choices at one depth.
- **Boundary - Author exercise: Store A Completed Path.** Copy the list before adding it to results.
- **Recognize - LC 78 Subsets.** Generate every include/exclude outcome exactly once.
