# Lesson spec: Search And Insert With One Path

**Recognition cue.** BST ordering lets one comparison discard an entire subtree. **Invariant.** At each step, if the target exists under the contract, it lies in the one selected child subtree. **False friend.** Validation needs ancestor bounds; a single search path is enough only when locating or inserting one key.

- **Build - LC 700 Search in a Binary Search Tree.** Follow one branch per comparison.
- **Vary - LC 701 Insert into a Binary Search Tree.** Stop at the null child where the key belongs.
- **Boundary - Author exercise: Duplicate-Key Policy.** Reject, count, or consistently place equality according to the stated representation.
- **Recognize - LC 450 Delete Node in a BST.** Handle zero, one, and two children, replacing a two-child node with a successor or predecessor.
