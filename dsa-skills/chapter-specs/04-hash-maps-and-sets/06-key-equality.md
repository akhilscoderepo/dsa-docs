# Lesson spec: Use Records As Keys

**Recognition cue.** The key is a compound value such as a coordinate, pair, or application object. **State.** Equal logical keys must have equal hashes, and their equality fields must not mutate while stored. **Java hazard.** Use an immutable record or a correctly implemented `equals`/`hashCode`; reference equality is not logical equality.

- **Build - Author exercise: Count Coordinates.** Given `Point(row, col)` observations, count logically equal coordinates using `record Point(int row, int col) {}`.
- **Vary - Author exercise: Undirected Edge Key.** Normalize `(a,b)` and `(b,a)` to the same immutable key before insertion.
- **Boundary - Author exercise: Mutable-Key Failure.** Explain why mutating a field that participates in `hashCode` after insertion makes a stored entry effectively unreachable.
- **Recognize - Author exercise: Count Directed Transitions.** Use an immutable `Pair(from, to)` record as a frequency-map key while keeping `(a, b)` distinct from `(b, a)`.
