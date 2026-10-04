# Lesson spec: Extend Runs With A Set

**Recognition cue.** A numeric sequence can be extended by local predecessor/successor membership tests. **State.** The set describes the complete input; iteration begins only from a sequence start. **False friend.** Sorting can also expose runs, but it mutates or costs `O(n log n)` when a set gives expected `O(n)` time.

- **Build - LC 128 Longest Consecutive Sequence.** Begin at `x` only when `x - 1` is absent.
- **Vary - LC 349 Intersection of Two Arrays.** Use membership across two collections while emitting each shared value once.
- **Boundary - Author exercise: Duplicate Starts.** Insert duplicates into the set first, then prove they cannot create duplicate runs.
- **Recognize - LC 202 Happy Number.** Store previously seen states in a set and stop when the numeric sequence reaches `1` or repeats.
