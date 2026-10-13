# Lesson spec: Circular Buffers

**Recognition cue.** A fixed-capacity FIFO or deque must reuse array positions. **Invariant.** `head`, `size`, and modular index arithmetic identify every live slot exactly once.

- **Build - Author exercise: Ring Buffer.** Implement enqueue/dequeue with `head` and `size`.
- **Vary - LC 622 Design Circular Queue.** Expose front, rear, full, and empty without ambiguous indices.
- **Boundary - LC 641 Design Circular Deque.** Support mutation at both ends when capacity is one.
- **Recognize - LC 3508 Implement Router.** Combine bounded FIFO expiry with packet identity and destination queries.
