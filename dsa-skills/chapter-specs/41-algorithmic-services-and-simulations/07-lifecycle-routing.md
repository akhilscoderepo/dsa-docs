# Lesson spec: Track Status And Pick The Next Task

**Recognition cue.** Entities enter, update, complete, cancel, or become eligible while queries select the next one by policy. **Invariant.** Lifecycle state is authoritative and every queue/index exposes only eligible live entities.

- **Build - Author exercise: In-Memory Task Lifecycle.** Add, cancel, and complete by ID.
- **Vary - LC 2590 Design a Todo List.** Filter tasks by user, tag, and completion state.
- **Boundary - Author exercise: Repeated Cancel Or Complete.** Define idempotence and stale index handling.
- **Recognize - LC 3829 Design Ride Sharing System.** Match waiting riders/drivers while preserving request lifecycle state.
