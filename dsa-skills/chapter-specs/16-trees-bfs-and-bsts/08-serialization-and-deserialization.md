# Lesson spec: Serialization And Deserialization

**Recognition cue.** Tree structure must be converted to a reversible sequence, including missing-child positions. **Invariant.** Encoder and decoder follow the same traversal grammar; null markers preserve shape. **False friend.** Recording only values cannot distinguish trees with different missing children. **Java hazard.** Use a moving token index or queue rather than repeatedly removing index zero from an `ArrayList`.

- **Build - Author exercise: Preorder With Null Markers.** Serialize a small tree so its exact shape is recoverable.
- **Vary - Author exercise: Recursive Decoder.** Consume one token per subtree and advance a shared index exactly once.
- **Boundary - Author exercise: Empty, Negative, And Multi-Digit Values.** Choose an unambiguous delimiter and null token.
- **Recognize - LC 297 Serialize and Deserialize Binary Tree.** Implement a matched codec and verify round-trip structure.
