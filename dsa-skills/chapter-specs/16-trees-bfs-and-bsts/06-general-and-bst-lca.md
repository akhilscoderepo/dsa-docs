# Lesson spec: Find The Lowest Common Ancestor

**Recognition cue.** The lowest common ancestor is the deepest node whose subtree contains both targets. **Invariant.** In a general tree, child returns report found targets; in a BST, key order proves whether both targets lie on one side or split at the current node. **False friend.** The BST shortcut is invalid for an unordered binary tree.

- **Build - Author exercise: General-Tree Ancestor Return.** Return the current node when targets are found in different child subtrees.
- **Vary - LC 236 Lowest Common Ancestor of a Binary Tree.** Propagate target nodes and combine two non-null child results.
- **Boundary - Author exercise: One Target Is Ancestor.** Return that target when the other appears below it under the existence guarantee.
- **Recognize - LC 235 Lowest Common Ancestor of a Binary Search Tree.** Use ordering to descend until the target values split or equal the current key.
