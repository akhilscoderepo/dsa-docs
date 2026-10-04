<!-- section: unlocked-combinations -->
## Unlocked Combinations

This chapter releases no combination lesson. Every pattern here works on one array with one or two indexes, and each needs a technique from a later chapter before it can merge with another structure. Two combinations stay deferred until their prerequisite chapters exist.

### Combinations Deferred To Later Chapters

Arrays with hash maps wait for Chapter 04. That chapter teaches lookup from a key to a stored state, and the missing piece is the hash map itself. Problems such as counting pairs with a target sum need it, so no exercise here assigns them. The count array in this chapter covers only small, bounded values.

Arrays with two pointers wait for Chapter 08. That chapter teaches two boundaries that move toward each other or in the same direction under one rule. The read index and write index in this chapter both move forward over the same positions. They do not form a two-boundary invariant.

Opposite-end and three-way partition pointers, prefix sums, binary search and sorting also have their own chapters. This chapter names them only to mark where a problem leaves its scope.

### Later Chapters That Use This One

Three ideas from this chapter carry forward.

- **Read and write indexes** (lessons 04 and 05) become the base of the in-place partition work in Chapter 08.
- **Running state with an invariant** (lessons 02, 03, 10, 11 and 12) becomes the base of prefix sums and dynamic programming.
- **Count arrays** (lesson 06) become the base of the hash map counting in Chapter 04.
