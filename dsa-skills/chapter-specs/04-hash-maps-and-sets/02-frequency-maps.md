# Lesson spec: Count Values With A Map

**Recognition cue.** The decision depends on multiplicity, not just existence. **State.** `count.get(key)` means the exact processed frequency, including the convention for absent keys. **False friend.** A set silently loses the count needed for an anagram or top-frequency decision.

- **Build - LC 387 First Unique Character in a String.** Return the first index with frequency one. `"leetcode" -> 0`; `"aabb" -> -1`.
- **Vary - LC 242 Valid Anagram.** Compare two frequency ledgers. `"anagram", "nagaram" -> true`; `"rat", "car" -> false`.
- **Boundary - Author exercise: Remove Zero Counts.** Process additions and removals; delete a key precisely when its count returns to zero. This prevents an empty count from being mistaken for membership.
- **Recognize - LC 1207 Unique Number of Occurrences.** Count each value with a map, then use a set to verify that no two values have the same frequency.
