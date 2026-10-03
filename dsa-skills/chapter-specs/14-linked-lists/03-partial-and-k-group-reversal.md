# Lesson spec: Partial And K-Group Reversal

**Recognition cue.** Only complete blocks or a bounded sublist should have their edges reversed. **Invariant.** Before reversing, identify the block predecessor, first node, successor after the block, and whether a full block exists. **False friend.** Reversing first and discovering a short final group later makes restoration unnecessarily difficult.

- **Build - Author exercise: Reverse Exactly Two Nodes.** Reconnect a supplied predecessor and successor.
- **Vary - LC 92 Reverse Linked List II.** Locate one range, reverse it, and preserve the surrounding chain.
- **Boundary - Author exercise: Incomplete Final Group.** Look ahead `k` nodes and leave a short suffix unchanged.
- **Recognize - LC 25 Reverse Nodes in k-Group.** Repeat the bounded reversal while full groups remain.
