# Lesson spec: Merge Feeds From Many Sources

**Recognition cue.** A query returns the newest or highest-priority items from several eligible sources. **Invariant.** Visibility filtering and recency/ranking order apply before the output limit.

- **Build - Author exercise: Merge Recent User Streams.** Use one frontier item per source.
- **Vary - LC 355 Design Twitter.** Combine follow state with a bounded k-way merge.
- **Boundary - Author exercise: Follow Self And Deleted Source.** State identity and lifecycle policies.
- **Recognize - LC 2254 Design Video Sharing Platform.** Coordinate reusable IDs, views, likes, and content lifecycle.
