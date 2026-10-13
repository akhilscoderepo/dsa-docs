# Lesson spec: Frequency Streams

**Recognition cue.** Each update changes multiplicity, uniqueness, or whether a run condition has been met. **Invariant.** Candidate containers may contain stale values only when a count check filters them before exposure.

- **Build - LC 170 Two Sum III - Data structure design.** Store frequencies and answer complement queries.
- **Vary - LC 1429 First Unique Number.** Couple counts with a queue of possible unique values.
- **Boundary - LC 2671 Frequency Tracker.** Keep value counts and count-of-counts synchronized at zero.
- **Recognize - LC 2526 Find Consecutive Integers from a Data Stream.** Track the current suffix run instead of retaining the stream.
