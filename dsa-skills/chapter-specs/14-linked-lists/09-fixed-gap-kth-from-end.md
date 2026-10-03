# Lesson spec: Fixed-Gap Kth From End

**Recognition cue.** A node's position is defined relative to the end, but only one traversal is desired. **Invariant.** After advancing `fast` by the prescribed gap, moving both pointers preserves that distance until fast reaches the terminal position. **False friend.** Fast/slow ratio finds a fraction such as the middle; a fixed gap finds an offset from the end.

- **Build - Author exercise: Kth Node From End.** Create a gap of `k` and return the slow node.
- **Vary - Author exercise: Predecessor Of Kth From End.** Start behind a dummy node so slow stops before the target.
- **Boundary - Author exercise: K Equals Length.** Confirm the target is the original head and validate the input contract.
- **Recognize - LC 19 Remove Nth Node From End of List.** Preserve the gap, then bypass the target through its predecessor.
