# Lesson spec: Validated Priority

**Recognition cue.** Fast updates make direct arbitrary heap removal expensive. **Invariant.** The map/record is authoritative; a heap root is exposed only if it still matches current state.

- **Build - Author exercise: Versioned Heap Entry.** Reject stale roots by version.
- **Vary - LC 1912 Design Movie Rental System.** Maintain ordered availability and rental reports.
- **Boundary - Author exercise: Repeated Corrections.** Prevent stale entries from changing observable results.
- **Recognize - LC 3815 Design Auction System.** Select the current winning bid under updates and withdrawals.
