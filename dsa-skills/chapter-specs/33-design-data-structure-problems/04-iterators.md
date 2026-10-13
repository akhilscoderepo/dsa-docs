# Lesson spec: Iterators

**Recognition cue.** A class must expose one logical sequence incrementally while preserving traversal state between calls. **Invariant.** `hasNext()` reports availability without consuming; `next()` advances exactly once.

- **Build - Author exercise: Array Peeking Iterator.** Cache one next element without double advancement.
- **Vary - LC 284 Peeking Iterator.** Separate observation from consumption.
- **Boundary - Author exercise: Repeated hasNext And Peek.** Make both idempotent.
- **Recognize - LC 341 Flatten Nested List Iterator.** Maintain a stack of unfinished nested iterators.
