# Lesson spec: Follow References Through A List

**Recognition cue.** The structure is defined by references rather than contiguous indices, so mutation changes reachability. **Invariant.** Every unreached node remains reachable from a saved reference, and the returned head owns the intended chain. **False friend.** Array-style random access does not exist; reaching position `i` costs a traversal.

- **Build - Author exercise: Traverse And Count.** Follow `next` references without modifying the list.
- **Vary - Author exercise: Insert After A Node.** Save the old successor before linking the new node.
- **Boundary - Author exercise: Empty And Singleton Lists.** State which references may be null under each operation.
- **Recognize - LC 203 Remove Linked List Elements.** Maintain a valid retained chain while removing matching nodes.
