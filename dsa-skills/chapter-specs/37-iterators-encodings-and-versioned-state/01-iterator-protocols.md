# Lesson spec: Iterator Protocols

**Recognition cue.** A class reveals one logical sequence over multiple calls. **Invariant.** Observation does not consume, consumption advances once, and exhaustion behavior is explicit.

- **Build - Author exercise: Array Iterator.** Define `hasNext` and `next` around one cursor.
- **Vary - LC 284 Peeking Iterator.** Cache one element for nonconsuming observation.
- **Boundary - LC 604 Design Compressed String Iterator.** Skip exhausted runs and handle multi-digit counts.
- **Recognize - LC 900 RLE Iterator.** Consume a requested number of logical elements without expanding runs.
