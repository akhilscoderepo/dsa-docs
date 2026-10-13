<!-- section: unlocked-combinations -->
## Unlocked Combinations

A route planner must visit every depot at least once, and the set of depots already visited changes at each stop. A table keyed by the current depot alone forgets which depots remain. A table keyed by the current depot and a visited-set stores exactly what the search needs, and one integer can hold that set.

### Pairings Taught In This Chapter

The lesson Bits With Search State joins the mask from lessons 01 and 05 with enumeration and breadth-first search. The mask records which items are chosen or visited, and the search stores one answer for each pair of position and mask. Its four exercises list subsets in a fixed order, hash fixed-width windows of letters, test disjoint word sets and search over a node together with a visited mask.

### Pairings Already Covered

Dynamic programming over assignments and profiles is taught in the chapter on advanced dynamic programming states, which includes its own mask primer. This chapter gives the general bit mechanics that primer uses and assigns no assignment or profile problems.
