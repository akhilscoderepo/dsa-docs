<!-- section: unlocked-combinations -->
## Unlocked Combinations

Two combinations are released by this chapter, since every ingredient has now been taught, and each one has its own lesson and its own four-step ladder. One more is deferred to a later chapter, along with several advanced problems whose ingredients are still missing.

### Teach Now

The hash map with binary search is the tenth lesson. Chapter 04 supplied maps that hold a list under each key, and this chapter supplied the search for the latest entry not after a given point. Together they answer questions of the form "what was the value of this key at that moment", and the ladder moves from one key to many keys, to the edges of the time range, to a snapshot array and an election. Its false friend is a map that keeps only the latest value of each key, which loses the past.

The matrix with binary search is the eleventh lesson. The shape of the grid supplied the translation between a position in reading order and a row and a column, and the search supplied the halving. The ladder covers a grid read by shelves, a grid read as one line with duplicates, an empty or enormous shape, and a grid sorted in two directions that needs a different tool. Its false friend is applying the one-line reading to a grid that is only sorted along rows and along columns.

### Deferred

Sorting with binary search is not given a lesson of its own, because the two ingredients appear together only inside problems that need a third idea. The problem of the k-th smallest distance between pairs needs a count of pairs below a limit, which is done with two pointers in Chapter 08. Searching a value space with a counting step that uses a heap or a table of states belongs to the chapters on heaps and on dynamic programming. This chapter mentions those problems in passing and assigns none of them.

### Already Covered

Searching a matrix by treating it as one virtual array was met in the first lesson as a short recognition exercise, and it returns in the eleventh lesson with a row-first variant and a shape guard. Searching over answers with a greedy check is covered in the eighth lesson for whole numbers and in the ninth for real numbers, so those lessons are the place to look when a later chapter asks for a minimum feasible value.
