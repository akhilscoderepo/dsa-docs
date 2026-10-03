# Lesson spec: Nested Structure

**Recognition cue.** Inner structures must finish before their enclosing structures can be finalized. **Invariant.** Each stack frame contains the unresolved state of one nesting level. **False friend.** A single global accumulator loses the parent state when nesting begins.

- **Build - Author exercise: Maximum Parenthesis Depth.** Track opened but unresolved levels.
- **Vary - Author exercise: Sum Values By Nested Group.** Save a parent accumulator when entering a group and restore it when leaving.
- **Boundary - Author exercise: Deep Single Chain.** Trace nested empty groups and reject unbalanced input under the stated contract.
- **Recognize - LC 856 Score of Parentheses.** Resolve each completed nested group into the value expected by its parent.
