# Lesson spec: Tree Representation

**Recognition cue.** Data has one root and recursively nested children rather than one linear successor. **Invariant.** Each recursive call owns one node's subtree; `null` represents an empty binary subtree, while an N-ary node owns a child collection. **False friend.** A general graph may contain cycles or multiple parents; a tree traversal does not need visited state under the tree contract.

- **Build - Author exercise: Construct A Three-Node Tree.** Connect one root to left and right children and identify each empty subtree.
- **Vary - Author exercise: Count N-Ary Children.** Traverse a supplied child list without assuming two positions.
- **Boundary - Author exercise: Empty And Single-Node Trees.** Define the result of each operation at `null` before writing recursion.
- **Recognize - LC 559 Maximum Depth of N-ary Tree.** Generalize the child-to-parent depth recurrence.
