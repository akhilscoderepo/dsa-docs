# Lesson spec: Repeated-Shrink Versus Non-Shrinking Policy

**Recognition cue.** A normal window must restore validity before its state is used; a one-removal formulation is safe only when a separate proof shows that retaining a window of the current best length cannot hide a better answer. **Invariant.** State explicitly whether the maintained window is valid or merely represents a candidate length. **False friend.** Replacing every `while` with `if` is not an optimization rule.

- **Build - Author exercise: Restore Before Record.** Implement a duplicate-free window with a `while` loop and assert validity before measuring it.
- **Vary - Author exercise: One-Removal Maximum-Length Trace.** Trace a proved non-shrinking replacement-budget formulation and identify what its window length represents.
- **Boundary - Author exercise: Multiple Left Removals Needed.** Use an input where one removal leaves the ordinary window invalid.
- **Recognize - LC 424 Longest Repeating Character Replacement.** Compare the always-valid and proved non-shrinking forms, including the invariant required by each.
