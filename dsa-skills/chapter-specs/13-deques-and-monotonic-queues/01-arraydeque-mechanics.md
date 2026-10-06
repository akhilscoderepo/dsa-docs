# Lesson spec: Use ArrayDeque From Both Ends

**Recognition cue.** The algorithm must inspect or remove candidates at both ends in constant time. **Invariant.** The front and back have fixed roles throughout the method. **False friend.** `LinkedList` can implement a deque, but `ArrayDeque` is the ordinary Java choice when null elements and indexed access are unnecessary. **Java hazard.** `ArrayDeque` rejects `null`.

- **Build - Author exercise: Two-Ended Buffer.** Add and remove integers at both ends using explicit `First` and `Last` methods.
- **Vary - Author exercise: Bounded Recent History.** Append at the back and evict the oldest front item once capacity is exceeded.
- **Boundary - Author exercise: Empty Deque Contract.** Choose deliberately between exception-throwing and sentinel-returning access methods.
- **Recognize - Author exercise: Candidate Deque API.** Identify the operations needed for front expiry and back domination without writing the algorithm yet.
