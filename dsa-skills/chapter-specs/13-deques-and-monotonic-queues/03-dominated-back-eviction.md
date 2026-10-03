# Lesson spec: Dominated-Back Eviction

**Recognition cue.** A newly arrived value is at least as good as older candidates and will remain eligible longer. **Invariant.** Every stored index can still become the optimum of a future window; anything popped from the back cannot. **False friend.** Removing a smaller value is unsafe when the query asks for a minimum.

- **Build - Author exercise: Insert Maximum Candidate.** Pop smaller back values before appending a new index.
- **Vary - Author exercise: Insert Minimum Candidate.** Pop larger values for a monotonic increasing deque.
- **Boundary - Author exercise: Repeated Equal Values.** Compare keeping all equals with keeping only the newest and preserve a consistent expiry rule.
- **Recognize - Author exercise: Online Suffix Maximum Candidates.** Return the front after every insertion when no expiry is required.
