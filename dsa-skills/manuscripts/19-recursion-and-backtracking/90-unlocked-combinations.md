<!-- section: unlocked-combinations -->
## Unlocked Combinations

Only one pairing is ready to teach in this chapter, and it has its own lesson and ladder. A second pairing is recorded as waiting, together with the chapter that must supply what it lacks.

### Teach Now

Searching a board for many words at once joins the path discipline of this chapter with the trie of Chapter 18, and it is the eleventh lesson. The path side supplies the walk, the marker on every tile in use, and the lifting of each marker on the way back. The trie side supplies a cursor that stands for every listed word compatible with the route so far, which turns a missing edge into an instant refusal. The part that needs care is the report, since several routes can spell the same word and each word must be reported once. The ladder starts with a single row of tiles, moves to counting how many tiles are entered, then to repeated words and repeated routes, and ends on a full grid. The false friend is one full search per word, which repeats every shared beginning.

### Deferred

A recursive search that revisits the same situation many times can remember its answers, so that the second visit costs a lookup. That is a different tool from the shared path, because it needs a precise definition of when two calls are the same situation and what a call returns, and the definition is the subject of the dynamic-programming chapters. Chapter 26 owns this combination, including the memoised forms of partitioning and of reusable-item searches, so no problem for it is assigned here. The lessons of this chapter state the repeated work where it occurs and name that chapter.

### Already Covered

The idea of a return value assembled from smaller calls comes from the tree lessons of Chapter 15, which this chapter reuses in a more general form. The trie itself, with its stored words and its missing edges, was built in Chapter 18 and is not re-taught. Sorting a copy before using order-dependent rules was practised in Chapter 05, the choice between lists of boxed integers and arrays of primitives follows Chapter 01, and the conversion between positions and pieces of a string follows Chapter 03.
