# Lesson spec: Neighbor Enumeration

**Recognition cue.** A cell operation depends on a fixed local neighborhood. **State.** A direction table enumerates candidate offsets; bounds checks decide which neighbors exist. **Java hazard.** Allocate the direction table once, outside hot loops.

- **Build - Author exercise: Orthogonal Count.** Count legal up/down/left/right neighbors of `(r,c)`.
- **Vary - Author exercise: Eight Neighbors.** Add diagonal offsets without duplicating the center.
- **Boundary - Author exercise: Corner Cell.** Verify `(0,0)` has only its legal neighbors and never uses negative indices.
- **Recognize - LC 289 Game of Life.** Count eight local neighbors; in-place state encoding is taught only after the next marker lesson.
