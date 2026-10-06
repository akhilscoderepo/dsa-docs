# Lesson spec: Cut A String Into Dictionary Words

**Recognition cue.** A string must be segmented into dictionary words, and trie traversal can test every word beginning at a position without constructing substrings. **Invariant.** From a start index, advancing the trie enumerates exactly the dictionary prefixes of the remaining suffix. **False friend.** Plain recursion repeats the same suffix states exponentially; memoization/DP ownership is deferred to Chapter 26.

- **Build - Author exercise: Dictionary Ends From One Index.** Return every end position reachable by a trie word.
- **Vary - Author exercise: One Valid Segmentation On Short Input.** Recurse from terminal trie nodes while keeping the repeated-state risk visible.
- **Boundary - Author exercise: Prefix Exists But Word Does Not.** Branch only at terminal nodes, not every reachable prefix.
- **Recognize - Author exercise: Explain Trie-Based Word Break State.** Define the start-index state and identify why memoization is needed for scale, without introducing DP prematurely.
