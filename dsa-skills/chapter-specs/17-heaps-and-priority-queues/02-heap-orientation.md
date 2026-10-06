# Lesson spec: Choose The Order With A Comparator

**Recognition cue.** Correctness depends on which candidate must be exposed first and how ties are resolved. **Invariant.** The comparator orders the exact priority tuple used by the algorithm. **False friend.** Negating integers to imitate a max-heap can overflow at `Integer.MIN_VALUE`. **Java hazard.** Use `Integer.compare` or `Comparator.comparingInt` rather than subtraction.

- **Build - Author exercise: Safe Max-Heap.** Create a reverse comparator without numeric negation.
- **Vary - Author exercise: Pair Priority.** Order tasks by duration, then original index.
- **Boundary - Author exercise: Equal Priorities And Extreme Integers.** Verify deterministic ties and overflow-safe comparison.
- **Recognize - LC 1834 Single-Threaded CPU.** Select by processing time and index among currently available tasks.
