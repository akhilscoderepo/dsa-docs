# Lesson spec: Two-Stack Queue

**Recognition cue.** Only LIFO containers are available, but the public API must be FIFO. **Invariant.** New values enter `in`; the oldest available values are on top of `out`. Transfer all values only when `out` is empty. **False friend.** Moving everything on every operation is correct but costs linear time per call.

- **Build - Author exercise: Enqueue And One Dequeue.** Transfer `in` to `out` and observe the reversal.
- **Vary - Author exercise: Interleaved Queue Calls.** Enqueue while `out` remains nonempty and preserve older values ahead of new ones.
- **Boundary - Author exercise: Empty Queue API.** Make `peek` and `pop` follow the stated nonempty-call contract or document the chosen failure behavior.
- **Recognize - LC 232 Implement Queue using Stacks.** Implement the full API and explain why each element moves between stacks at most once.
