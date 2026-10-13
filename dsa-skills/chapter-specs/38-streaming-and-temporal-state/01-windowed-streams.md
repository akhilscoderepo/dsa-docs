# Lesson spec: Windowed Streams

**Recognition cue.** Values arrive one at a time and only the last `k` items or recent duration matters. **Invariant.** Stored state contains exactly the active window and its aggregate.

- **Build - LC 346 Moving Average from Data Stream.** Maintain a bounded queue and running sum.
- **Vary - LC 933 Number of Recent Calls.** Expire timestamps outside the time window.
- **Boundary - Author exercise: Large Sum Window.** Use `long` and define inclusive time boundaries.
- **Recognize - LC 362 Design Hit Counter.** Compare event queue and fixed-bucket implementations.
