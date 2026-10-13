# Lesson spec: Nested Iteration

**Recognition cue.** Several arrays, iterators, or nested values must appear as one lazy sequence. **Invariant.** The state identifies exactly the next nonempty source and its local cursor.

- **Build - LC 251 Flatten 2D Vector.** Skip empty rows lazily.
- **Vary - LC 281 Zigzag Iterator.** Rotate only among sources that still contain values.
- **Boundary - LC 341 Flatten Nested List Iterator.** Descend through arbitrarily empty nested lists.
- **Recognize - LC 1286 Iterator for Combination.** Generate the next lexicographic combination from index state.
