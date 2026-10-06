# Lesson spec: Pick The Best XOR Partner

**Recognition cue.** The objective is to maximize XOR, so the highest differing bit dominates all lower bits. **Invariant.** At each bit, prefer the opposite branch when present; the chosen path is lexicographically best in XOR-bit order. **False friend.** A character trie and a binary trie share structure but not edge meaning.

- **Build - Author exercise: Insert Fixed-Width Bits.** Store each integer from the highest considered bit to the lowest.
- **Vary - Author exercise: Best XOR Partner.** Prefer the opposite bit and accumulate the resulting XOR value.
- **Boundary - Author exercise: Equal Values And Sign Policy.** State whether inputs are nonnegative and which bit width is traversed.
- **Recognize - LC 421 Maximum XOR of Two Numbers in an Array.** Query each number against previously inserted or fully stored values.
