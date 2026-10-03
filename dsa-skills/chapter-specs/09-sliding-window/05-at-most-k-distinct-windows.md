# Lesson spec: At-Most-K Distinct Windows

**Recognition cue.** Validity is monotone under removing elements and is expressed as no more than `k` distinct values. **Invariant.** The map contains positive counts for exactly the values in the current window. **Java hazard.** Remove a key when its count reaches zero or `map.size()` stops representing distinct values.

- **Build - Author exercise: Longest Segment With One Distinct Value.** Maintain one active key and its count.
- **Vary - LC 904 Fruit Into Baskets.** Find the longest subarray containing at most two distinct values.
- **Boundary - Author exercise: K Is Zero.** Return zero without allowing a negative count or an invalid left boundary.
- **Recognize - Author exercise: Longest Substring With At Most K Distinct Characters.** Transfer the same invariant from integers to characters.
