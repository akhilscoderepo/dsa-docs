# Lesson spec: Store Keys In Direct Slots

**Recognition cue.** The prompt forbids a library map/set or provides a bounded key domain. **Invariant.** Each key has one deterministic bucket or direct slot, and update/remove preserve bucket ownership.

- **Build - Author exercise: Boolean Direct Set.** Use a bounded key domain.
- **Vary - LC 705 Design HashSet.** Replace direct addressing with bucketed collision handling.
- **Boundary - LC 706 Design HashMap.** Distinguish absent keys from stored values and update in place.
- **Recognize - LC 707 Design Linked List.** Preserve head/tail/size ownership across indexed mutation.
