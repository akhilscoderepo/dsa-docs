# Lesson spec: Find All Distances With Floyd Warshall

**Recognition cue.** A small dense graph needs distances between every pair. **Invariant.** After intermediate `k`, `dist[i][j]` is best using only intermediates `0..k`. **False friend.** Reordering the `k` loop breaks the recurrence.

- **Build - Author exercise: Allow One Intermediate.** Compare the direct route with `i -> k -> j`.
- **Vary - Author exercise: All-Pairs Table.** Add intermediates one by one.
- **Boundary - Author exercise: Infinity Arithmetic.** Never add an unreachable sentinel and use safe numeric width.
- **Recognize - LC 1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance.** Compute all-pairs distances and apply the tie rule.
