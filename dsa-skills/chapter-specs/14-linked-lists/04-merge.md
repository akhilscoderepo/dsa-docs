# Lesson spec: Merge Two Sorted Lists

**Recognition cue.** Two sorted linked chains must become one sorted chain without allocating replacement nodes. **Invariant.** The result tail ends a sorted finalized prefix; both remaining heads begin sorted suffixes. **False friend.** Copying values into an array avoids the pointer problem but violates the intended space and node-reuse contract.

- **Build - Author exercise: Merge Two One-Node Lists.** Attach the smaller head and then the remainder.
- **Vary - LC 21 Merge Two Sorted Lists.** Repeatedly consume the smaller current node.
- **Boundary - Author exercise: One Empty Or Exhausted List.** Attach the entire remaining suffix in one step.
- **Recognize - LC 148 Sort List.** Split, recursively sort, and reuse the merge invariant in linked-list merge sort.
