# Lesson spec: K-Way Merge

**Recognition cue.** Several sources are individually sorted and the next global value must be chosen repeatedly. **Invariant.** The heap contains at most one current head from each nonexhausted source. **False friend.** Inserting every value loses the `O(k)` frontier-space advantage.

- **Build - Author exercise: Merge Three Sorted Arrays.** Store value, source index, and position for each current head.
- **Vary - LC 23 Merge k Sorted Lists.** Poll one list node and offer its successor.
- **Boundary - Author exercise: Empty Sources And Equal Heads.** Skip exhausted sources and use a safe tie policy.
- **Recognize - LC 378 Kth Smallest Element in a Sorted Matrix.** Treat each row as a sorted stream and stop after `k` polls.
