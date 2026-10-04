# Lesson spec: Union By Size

**Recognition cue.** Two representatives must merge while keeping parent trees shallow. **Invariant.** Attach the smaller root under the larger root and update size only at the surviving root. **False friend.** Comparing original elements rather than roots corrupts size accounting.

- **Build - Author exercise: Merge Two Roots.** Find both representatives before writing parent links.
- **Vary - Author exercise: Repeated Unequal Merges.** Update the receiving root's size.
- **Boundary - Author exercise: Already Connected.** Return without double-counting size or reducing component count.
- **Recognize - LC 684 Redundant Connection.** The first edge whose endpoints already share a root closes a cycle.
