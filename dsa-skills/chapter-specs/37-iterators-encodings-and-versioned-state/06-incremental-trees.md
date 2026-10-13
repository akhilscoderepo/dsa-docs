# Lesson spec: Incremental Trees

**Recognition cue.** Public methods modify or navigate a tree while retaining auxiliary state. **Invariant.** The stored frontier, parent relation, or traversal history remains consistent with the current tree.

- **Build - LC 919 Complete Binary Tree Inserter.** Keep the queue of nodes missing children.
- **Vary - LC 1586 Binary Search Tree Iterator II.** Add backward navigation without rebuilding traversal state.
- **Boundary - LC 1261 Find Elements in a Contaminated Binary Tree.** Recover membership without relying on corrupted values.
- **Recognize - LC 1993 Operations on Tree.** Maintain lock rules involving ancestors and descendants.
