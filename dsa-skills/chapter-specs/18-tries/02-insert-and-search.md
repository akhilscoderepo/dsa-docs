# Lesson spec: Insert And Look Up Words

**Recognition cue.** Operations consume one character at a time and either create a missing edge or fail when an edge is absent. **Invariant.** After processing `i` characters, the current node represents `word[0..i]`. **Java hazard.** A 26-slot array is valid only for a lowercase-English contract; otherwise use a map.

- **Build - Author exercise: Insert Lowercase Words.** Create only missing child nodes.
- **Vary - Author exercise: Search Versus StartsWith.** Require a terminal marker only for exact search.
- **Boundary - Author exercise: Word Is Prefix Of Another.** Store `app` and `apple` without confusing their terminal states.
- **Recognize - LC 208 Implement Trie.** Implement the complete API under an explicit character-domain contract.
