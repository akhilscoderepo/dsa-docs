# Lesson spec: Give Each End One Job

**Recognition cue.** One end answers the current query while the other end admits a new candidate and removes weaker ones. **Invariant.** The front is the best surviving candidate; order toward the back follows the stated monotonic rule. **False friend.** Treating both ends as interchangeable destroys the proof.

- **Build - Author exercise: Decreasing Candidate Values.** Maintain a deque whose values decrease from front to back.
- **Vary - Author exercise: Increasing Candidate Values.** Reverse the comparison to support minima.
- **Boundary - Author exercise: Equal Candidate Policy.** Decide whether the newer equal value replaces the older one and explain how indices affect expiry.
- **Recognize - Author exercise: Name Each End.** Given a moving-range trace, identify whether each removal is expiration or domination.
