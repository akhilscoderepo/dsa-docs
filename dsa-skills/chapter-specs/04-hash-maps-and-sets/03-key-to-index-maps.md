# Lesson spec: Remember Where A Value Appeared

**Recognition cue.** A current value needs one earlier location or complement immediately. **State.** The map records the index meaning stated by the contract: usually the earliest usable index, or the most recent one. **False friend.** Sorting changes original-index requirements and is not a substitute for remembered lookup.

- **Build - LC 1 Two Sum.** Given `nums` and `target`, return indices of two values summing to `target`. `[2,7,11,15], 9 -> [0,1]`; `[3,3], 6 -> [0,1]`.
- **Vary - LC 219 Contains Duplicate II.** Store the last seen index and compare the gap to `k`.
- **Boundary - Author exercise: First Index Wins.** Given repeated values, preserve the first index when the output requires the widest valid pair; name why overwriting would change the answer.
- **Recognize - Author exercise: Widest Equal-Value Pair.** Store the first index of each value and return the largest distance between two equal values.
