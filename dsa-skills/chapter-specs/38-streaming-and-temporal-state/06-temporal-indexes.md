# Lesson spec: Temporal Indexes

**Recognition cue.** Events are stored once and later queried by time, granularity, or interval. **Invariant.** Timestamp order and bucket semantics agree with inclusive query boundaries.

- **Build - LC 635 Design Log Storage System.** Normalize timestamp prefixes by requested granularity.
- **Vary - LC 1348 Tweet Counts Per Frequency.** Bucket event counts across a requested range.
- **Boundary - Author exercise: Sparse Empty Buckets.** Return zeros without materializing all time.
- **Recognize - LC 3709 Design Exam Scores Tracker.** Maintain cumulative scores for time/sequence queries.
