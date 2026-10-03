<!-- section: unlocked-combinations -->
## Unlocked Combinations

Nothing is released as a teach-now combination here. The arrays chapter supplied one-pass state, compaction, counting and in-place marking on a single sequence, and this chapter extends the cell as the unit of work to two indices. Combining a matrix with a set, with a search, or with a graph traversal needs a prerequisite that has not been taught yet.

### Deferred

Matrices with hash sets are deferred to Chapter 04, which supplies scoped row, column and box membership and ends with the validity check of a Sudoku board. The marker lesson here uses boolean arrays on purpose, so Chapter 04 can show what a general set adds. Matrices with binary search are deferred to Chapter 06, where the order of a sorted matrix supplies the search invariant. Matrices with graph traversal are deferred to Chapter 21, when a frontier and visited semantics exist, and Game of Life neighbor counting here is local and does not need that. Matrices with dynamic programming are deferred to Chapter 26, when cell states and transition order are defined. None of the exercises in this chapter relies on those techniques.

### Already Covered

The in-place marking idea from the arrays chapter, sign marking, returns here in a different form as marker arrays and as a second bit in each cell. The spiral appears twice on purpose, once as a heading with a visited record and once as four shrinking edges, and the false friend in each lesson names the other.
