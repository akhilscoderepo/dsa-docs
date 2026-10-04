# Lesson spec: Bidirectional Frontiers

**Recognition cue.** One unweighted start and target have reversible transitions and the search space branches heavily. **Invariant.** Two visited-distance maps represent shortest discovery from each side; when a generated state exists in the opposite map, the distances combine. **False friend.** Meeting only when queue fronts are equal can miss crossing edges.

- **Build - Author exercise: Two-Ended Integer Search.** Expand one layer from the smaller frontier.
- **Vary - Author exercise: Detect A Crossing Neighbor.** Test intersection while generating next states.
- **Boundary - Author exercise: Start Equals Target.** Return immediately and keep the two visited maps logically distinct.
- **Recognize - LC 127 Word Ladder.** Expand the smaller word frontier until the searches connect.
