# Lesson spec: Multilevel Flattening

**Recognition cue.** Nodes form a main doubly linked chain plus child chains that must be spliced into depth-first order. **Invariant.** Each splice preserves `prev`/`next` symmetry and retains the old successor so traversal can resume after the child chain. **False friend.** Updating only forward links creates a list that looks correct in one direction but is structurally broken.

- **Build - Author exercise: Splice One Child Chain.** Connect parent, child head, child tail, and saved successor in a safe order.
- **Vary - Author exercise: Stack Of Deferred Successors.** Push the old `next` when descending and restore it after a child chain ends.
- **Boundary - Author exercise: Child At Tail And Nested Child.** Handle a null saved successor and more than one nesting level.
- **Recognize - LC 430 Flatten a Multilevel Doubly Linked List.** Produce preorder flattening while clearing every child pointer.
