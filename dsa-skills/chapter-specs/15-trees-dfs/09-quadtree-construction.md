# Lesson spec: Quadtree Construction

**Recognition cue.** A square grid region becomes one leaf when uniform; otherwise it divides into four equal quadrants. **Invariant.** Each call owns a precise row/column region and returns the node representing exactly that region. **False friend.** Creating four children before testing uniformity produces unnecessary structure.

- **Build - Author exercise: Uniform Region Test.** Decide whether every cell in one supplied square matches its first cell.
- **Vary - Author exercise: Split Four Quadrants.** Calculate non-overlapping child bounds for an even side length.
- **Boundary - Author exercise: One Cell.** Return a leaf without further subdivision.
- **Recognize - LC 427 Construct Quad Tree.** Recursively compress uniform regions and build internal nodes only when needed.
