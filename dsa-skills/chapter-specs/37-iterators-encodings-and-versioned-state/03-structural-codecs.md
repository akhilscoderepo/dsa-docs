# Lesson spec: Structural Codecs

**Recognition cue.** A structured value must cross a flat string or tree boundary and be reconstructed exactly. **Invariant.** Every encoded unit has an unambiguous boundary and every decoder step consumes one complete unit.

- **Build - LC 271 Encode and Decode Strings.** Use length framing instead of a fragile delimiter.
- **Vary - LC 297 Serialize and Deserialize Binary Tree.** Preserve shape with null markers.
- **Boundary - LC 431 Encode N-ary Tree to Binary Tree.** Preserve child order and empty child lists.
- **Recognize - LC 449 Serialize and Deserialize BST.** Use the BST ordering contract to reduce structural metadata.
