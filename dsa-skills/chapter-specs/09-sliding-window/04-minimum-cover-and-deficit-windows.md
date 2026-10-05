# Lesson spec: Find The Shortest Covering Window

**Recognition cue.** The range must cover required values or counts, and the objective is the shortest valid range. **Invariant.** A deficit ledger says whether every requirement is met; while valid, removing the leftmost item tests whether the range can be improved. **False friend.** Equality with a fixed signature is not coverage: a cover may contain surplus characters.

- **Build - Author exercise: Shortest Segment Containing A And B.** Expand until both required symbols appear, then shrink surplus symbols.
- **Vary - Author exercise: Required Multiplicities.** Require two copies of one symbol and track fulfilled counts rather than distinct membership.
- **Boundary - Author exercise: No Cover Exists.** Return the specified empty result without constructing invalid substrings.
- **Recognize - LC 76 Minimum Window Substring.** Maintain deficits, remember the best boundaries, and create the substring once.
