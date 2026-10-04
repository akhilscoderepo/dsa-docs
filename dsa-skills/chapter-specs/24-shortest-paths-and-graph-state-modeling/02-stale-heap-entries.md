# Lesson spec: Stale Heap Entries

**Recognition cue.** Java's heap has no decrease-key operation, so a vertex may have several queued distances. **Invariant.** `dist[node]` is the best known value; discard a popped entry when its stored distance differs from that value. **False friend.** Removing the old heap object with `remove(Object)` is linear.

- **Build - Author exercise: Two Entries For One Node.** Insert an improved distance and identify the old entry as stale.
- **Vary - Author exercise: Skip Before Expansion.** Reject stale entries before relaxing outgoing edges.
- **Boundary - Author exercise: Equal-Cost Alternatives.** Keep the distance contract consistent when a proposal ties the current best.
- **Recognize - LC 743 Network Delay Time.** Use duplicate insertion plus stale rejection instead of decrease-key.
