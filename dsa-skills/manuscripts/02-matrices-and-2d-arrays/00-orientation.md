<!-- section: orientation -->
## Orientation

This chapter teaches seven techniques for matrices, which in Java are arrays of arrays. You will learn to read the shape of a matrix before touching it, to visit rows, columns, diagonals and the outer ring from index rules, to follow a cursor with a heading, to enumerate neighbors with a table of offsets, to rotate a square in place, to record facts before a write destroys them, and to peel a rectangle layer by layer. Each technique has its own invariant and its own false friend, and each has a four-step practice ladder.

### What You Need Before Starting

You should have finished Chapters 00 and 01 or be comfortable with their contents. That means reading a contract, counting the work of a loop, and writing one-pass array code with a clear invariant. You should be able to write nested loops in Java and know that `int[][]` is an array of row arrays. Nothing beyond arrays and `List` appears in this chapter, and graph traversal, dynamic programming and binary search on matrices are deferred to later chapters on purpose.

### The Seven Lessons

Shape contracts come first because every later lesson reads cells, and a wrong bound turns into a crash or a silent wrong answer. Structured traversal covers the cells that form a simple shape and replaces rescans with index rules. Direction state follows one cursor with a heading. Neighbor enumeration turns a local neighborhood into a table of offsets and a guard. Matrix rotation shows that a quarter turn is two sweeps of swaps. Marker state separates observation from mutation so that writes cannot erase the evidence. Spiral boundaries peel a rectangle with four edge variables and two guards.

### How To Work Through A Lesson

Open each lesson with its story and the plain first version, and judge what is wasteful before reading about the bottleneck. Matrix traces list the cells in row-major order, so the step counter together with the row and column variables tells you where you are. Pause the stepper at the step the text calls out. Work the four exercises in sequence, write your attempt in the notes box before looking at the hint, and compare with the solution afterwards. The Java in each solution runs during the build against a slow but obviously correct oracle.

### Leaving The Chapter

Finishing the chapter means you can read a matrix problem and state the promised shape, the region of cells in play, the state that describes the next step, and the neighbor, boundary or marker idea that applies, along with the lookalike that does not. The review questions test this recognition, and they are designed to be retaken after a gap.
