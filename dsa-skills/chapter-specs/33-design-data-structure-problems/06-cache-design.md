# Lesson spec: Cache Design

**Recognition cue.** Direct key lookup and eviction by recency or frequency must both be constant time. **Invariant.** LRU maps keys to nodes in one recency list; LFU additionally owns frequency buckets and a minimum-frequency pointer.

- **Build - Author exercise: Move Node To Front.** Detach and reinsert behind a sentinel.
- **Vary - LC 146 LRU Cache.** Make both `get` and overwrite refresh recency.
- **Boundary - Author exercise: Capacity One And Repeated Get.** Evict the true least-recent node without duplicating links.
- **Recognize - LC 460 LFU Cache.** Add frequency buckets with LRU tie-breaking inside each bucket.
