# Lesson spec: Grouping Maps

**Recognition cue.** Several inputs belong to the same output bucket under a stated equivalence relation. **State.** `groups.get(key)` owns the full list for one equivalence class. **False friend.** A frequency map tells how many; it does not preserve the members required by grouped output.

- **Build - Author exercise: Group by Remainder.** Given `nums` and `m`, return groups keyed by `Math.floorMod(value, m)`. `[1,4,2,5], 3 -> [[1,4],[2,5]]`.
- **Vary - LC 1282 Group the People Given the Group Size They Belong To.** A key owns an in-progress bucket that is emitted only when full.
- **Boundary - Author exercise: Empty Buckets.** Do not return keys that received no values; map creation must be demand-driven.
- **Recognize - LC 49 Group Anagrams.** Use a fixed-alphabet count signature as the grouping key; the map owns the buckets for equal signatures.
