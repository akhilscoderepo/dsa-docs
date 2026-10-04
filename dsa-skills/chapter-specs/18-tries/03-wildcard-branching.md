# Lesson spec: Wildcard Branching

**Recognition cue.** Most query characters select one trie edge, but a wildcard may match any child. **Invariant.** A recursive call represents all dictionary words consistent with the query prefix consumed so far. **False friend.** Branching at ordinary characters turns a narrow search into unnecessary exhaustive traversal.

- **Build - Author exercise: One Final Wildcard.** Check every child only at the wildcard position.
- **Vary - Author exercise: Multiple Wildcards.** Recurse independently through each viable child and short-circuit on success.
- **Boundary - Author exercise: Wildcard At Root And Missing Length.** Match exactly the query length and require terminal state at the end.
- **Recognize - LC 211 Design Add and Search Words Data Structure.** Combine trie insertion with selective wildcard DFS.
