# Lesson spec: Dummy Heads

**Recognition cue.** The real head may be inserted, removed, or replaced, creating a special first-node case. **Invariant.** `dummy.next` always identifies the current result head while `tail` or `prev` owns the last finalized link. **False friend.** A dummy node is not automatically useful when the head never changes.

- **Build - Author exercise: Prepend Without A Special Case.** Insert through `dummy.next` and return that reference.
- **Vary - LC 21 Merge Two Sorted Lists.** Build the result behind a stable dummy tail.
- **Boundary - LC 203 Remove Linked List Elements.** Remove one or many matching original head nodes uniformly.
- **Recognize - LC 19 Remove Nth Node From End of List.** Let a dummy predecessor make deletion of the original head ordinary.
