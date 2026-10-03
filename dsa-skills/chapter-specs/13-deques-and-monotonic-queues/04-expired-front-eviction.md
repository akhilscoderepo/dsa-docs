# Lesson spec: Expired-Front Eviction

**Recognition cue.** Candidate indices may be optimal by value but no longer lie in the active range. **Invariant.** Before reading the answer for a window ending at `right`, every stored index is greater than `right - k`. **False friend.** Value ordering cannot reveal whether a candidate is stale.

- **Build - Author exercise: Expire One Window.** Remove a front index when it falls left of a supplied boundary.
- **Vary - Author exercise: Jumping Boundary.** Use a loop because one boundary change may expire several stored indices.
- **Boundary - Author exercise: Exact Expiry Point.** For length `k`, verify that index `right - k` is outside the new window.
- **Recognize - Author exercise: Chronological Candidate Queue.** Preserve increasing indices while values remain monotonic.
