# Lesson spec: Kth And Range Queries

**Recognition cue.** The answer depends on sorted key order or pruning by a numeric interval. **Invariant.** Inorder traversal visits keys in sorted order; range traversal skips any subtree that cannot contain an allowed value. **False friend.** BFS level order has no relationship to key rank.

- **Build - Author exercise: First K Inorder Values.** Stop after the required number of sorted visits.
- **Vary - LC 230 Kth Smallest Element in a BST.** Use iterative inorder and return on the kth pop.
- **Boundary - Author exercise: K At Either End.** Test the smallest and largest valid rank under the stated nonempty contract.
- **Recognize - LC 938 Range Sum of BST.** Prune left when the key is too small and right when it is too large.
