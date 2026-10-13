# Lesson spec: Query Objects

**Recognition cue.** A constructor receives stable data and many queries follow. **Invariant.** Preprocessing preserves exactly the information needed by the query while avoiding repeated full scans.

- **Build - LC 244 Shortest Word Distance II.** Store sorted positions per word.
- **Vary - LC 1570 Dot Product of Two Sparse Vectors.** Iterate only represented nonzero entries.
- **Boundary - LC 288 Unique Word Abbreviation.** Distinguish one owning word from collisions among different words.
- **Recognize - LC 2080 Range Frequency Queries.** Binary-search first and last relevant positions.
