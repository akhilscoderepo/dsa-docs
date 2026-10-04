# Chapter 02: Matrices and 2D arrays

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| shape contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| row/column/diagonal/boundary traversal | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| direction-state and layer-state simulation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| neighbor enumeration | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| in-place transpose/rotation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| row-column marker state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| spiral traversal | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| Bundle 1-1 | 2D Matrix | Spiral Matrix | Learn | — |
| Bundle 1-2 | 2D Matrix | Spiral Matrix II | Extend | — |
| Bundle 1-3 | 2D Matrix | Rotate Image | Twist | — |
| Bundle 2-12 | Grid | Maximal Square | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Shrink four boundaries | Need visit matrix by layers/boundaries | Each layer is consumed once | https://leetcode.com/problems/spiral-matrix/ | Core |
| Transpose + reverse | Need rotate/transform square matrix in-place | Composition of two reversible transforms equals the desired rotation | https://leetcode.com/problems/rotate-image/ | Core |


### Released Combination Ladders

No combination is released by this chapter's current prerequisite boundary. The visible deferred entries below remain ownership notes, not premature exercises.


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Rectangular And Ragged Arrays

**Recognition cue.** Correct traversal depends on whether the matrix is rectangular, square, or ragged. **Invariant.** Every access uses a row and a column legal for that row. **Java hazard.** A ragged `int[][]` requires `grid[r].length`; `grid[0].length` is not a universal column bound.

- **Build - Author exercise: Rectangular Sum.** Sum a guaranteed `rows x cols` matrix. `[[1,2],[3,4]] -> 10`; `[] -> 0` under the stated empty contract.
- **Vary - Author exercise: Ragged Sum.** Sum `[[1,2],[],[3]]` without assuming equal row lengths.
- **Boundary - Author exercise: Empty Rows.** Distinguish `new int[0][]` from `new int[][]{{}}` before reading row zero.
- **Recognize - LC 1572 Matrix Diagonal Sum.** The square-shape guarantee makes both diagonal coordinates legal; subtract the center once when `n` is odd.

### Walking Rows, Columns And Diagonals

**Recognition cue.** The requested cells form rows, columns, diagonals, or the outer boundary. **State.** Indices describe the exact geometric region still unvisited. **False friend.** Connectivity through neighbors is graph traversal and remains deferred.

- **Build - Author exercise: Column Sums.** Return one sum per column for a rectangular matrix.
- **Vary - LC 1572 Matrix Diagonal Sum.** Visit two coordinate formulas per row.
- **Boundary - Author exercise: Perimeter Sum.** Avoid counting corners twice in a one-row or one-column matrix.
- **Recognize - LC 766 Toeplitz Matrix.** Compare each cell with its upper-left predecessor instead of rescanning whole diagonals.

### Moving With A Direction

**Recognition cue.** Movement follows a small cyclic direction rule and changes when the next step is illegal or already consumed. **State.** `(row, col, direction)` fully describes the next simulation step. **False friend.** A BFS frontier explores many positions; direction-state simulation follows one evolving cursor.

- **Build - Author exercise: Clockwise Walker.** Move a cursor through four directions and rotate on a blocked edge.
- **Vary - LC 59 Spiral Matrix II.** Write increasing values while turning at boundaries or filled cells.
- **Boundary - Author exercise: Single Cell.** A `1 x 1` board writes exactly once and never performs an extra turn.
- **Recognize - LC 885 Spiral Matrix III.** Allow the cursor outside the result rectangle while recording only legal coordinates.

### Checking The Neighbors Of A Cell

**Recognition cue.** A cell operation depends on a fixed local neighborhood. **State.** A direction table enumerates candidate offsets; bounds checks decide which neighbors exist. **Java hazard.** Allocate the direction table once, outside hot loops.

- **Build - Author exercise: Orthogonal Count.** Count legal up/down/left/right neighbors of `(r,c)`.
- **Vary - Author exercise: Eight Neighbors.** Add diagonal offsets without duplicating the center.
- **Boundary - Author exercise: Corner Cell.** Verify `(0,0)` has only its legal neighbors and never uses negative indices.
- **Recognize - LC 289 Game of Life.** Count eight local neighbors; in-place state encoding is taught only after the next marker lesson.

### Rotating A Square In Place

**Recognition cue.** A square matrix must be transformed in place. **Invariant.** Transposition swaps each off-diagonal pair once; reversing each row then completes a clockwise rotation. **False friend.** A rectangular matrix cannot be rotated in place into the same dimensions.

- **Build - Author exercise: Transpose Square.** Swap `matrix[r][c]` with `matrix[c][r]` only for `c > r`.
- **Vary - LC 48 Rotate Image.** Transpose, then reverse each row.
- **Boundary - Author exercise: Odd Center.** Show why the center of a `3 x 3` matrix remains valid without special movement.
- **Recognize - Author exercise: Counterclockwise Rotation.** Transpose, then reverse columns; name the changed transformation.

### Marking Rows Before Clearing Them

**Recognition cue.** Rows and columns must be marked for a later mutation, but immediate writes would destroy evidence still needed. **State.** Marker storage records affected rows/columns until the observation pass completes. **False friend.** Hash sets are an allowed auxiliary solution, but Chapter 04 owns general set state.

- **Build - Author exercise: Mark Bad Rows.** First record which rows contain `-1`, then clear them in a second pass.
- **Vary - LC 73 Set Matrix Zeroes.** Record both affected rows and columns before applying zeroes.
- **Boundary - LC 73 Constant-Space Variant.** Reserve the first row/column as markers and keep separate flags for their original state.
- **Recognize - LC 289 Game of Life.** Encode old and new cell state together so neighbor reads still see the original generation.

### Walking A Matrix In Spiral Order

**Recognition cue.** Output consumes a rectangle layer by layer. **Invariant.** `top`, `bottom`, `left`, and `right` enclose exactly the unvisited rectangle. **False friend.** Direction-state simulation and shrinking-boundary traversal can produce similar output, but their state and failure modes differ.

- **Build - Author exercise: One Ring.** Emit the perimeter of a rectangular matrix without repeating corners.
- **Vary - LC 54 Spiral Matrix.** Repeatedly consume top row, right column, bottom row, and left column.
- **Boundary - LC 54 Thin Remainder.** Guard the bottom and left passes when only one row or one column remains.
- **Recognize - LC 59 Spiral Matrix II.** Reverse the data flow: generate values into the same shrinking layers.

## Deferred Combinations

- **Matrices + Hash Sets:** released in Chapter 04 as scoped row/column/box membership, culminating in LC 36 Valid Sudoku.
- **Matrices + Binary Search:** released in Chapter 06; sorted-matrix order supplies the search invariant.
- **Matrices + Graph Traversal:** released in Chapter 21 when a frontier and visited semantics are available.
- **Matrices + Dynamic Programming:** released in Chapter 26 when cell states and transition order are defined.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Distinguish rectangular inputs from ragged `int[][]`; use `grid[r].length` for ragged traversal.
- Avoid allocating neighbor-direction arrays inside an inner loop.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Deferred | Matrices + Hash Sets | Chapter 04 supplies membership state |
| Deferred | Matrix + BFS/DFS | Chapter 21 supplies graph frontier state |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** graph traversal, dynamic programming, sorted-matrix binary search.

For every released combination, create a dedicated lesson that states each prerequisite's contribution, the combined state/invariant, a false friend, implementation, and its own Build → Vary → Boundary → Recognize staircase. Deferred combinations receive an explanation and a future owner only—never premature exercises.

## Publication Gate

- Crosswalk every required micro-pattern to a named lesson and practice ladder.
- Run the composition audit and record released/deferred outcomes.
- Run the Java integrity focus against every code example.
- Verify exact problem wording, examples, complexity, and prerequisite ownership.
- Render and inspect the PDF; then perform text extraction checks.

## Research Baseline

- [LeetCode Study Plans](https://leetcode.com/studyplan/) for problem discovery and current interview-style prompts.
- [NeetCode Roadmap](https://neetcode.io/roadmap) for a cross-check of prerequisite order and representative pattern families.
- [Tech Interview Handbook study cheatsheets](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) for topic-specific corner cases, complexity review, and interview habits.
- [Oracle Java Collections documentation](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) for Java collection semantics. Prefer the installed JDK documentation for version-specific details when a chapter relies on a newer API.
- Supplied reference books: *Cracking the Coding Interview*, *Grokking Algorithms*, and *Elements of Programming Interviews in Java*. They guide explanation quality and problem selection; they are not copied verbatim.

