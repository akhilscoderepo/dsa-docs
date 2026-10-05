<!-- section: unlocked-combinations -->
## Unlocked Combinations

A search needs a range with order, and two earlier structures supply one in new places. This chapter teaches both pairings as lessons with exercises. A third pairing waits for a later chapter and is only named here.

### Pairings Taught In This Chapter

Maps with a search form the lesson Look Up Values By Time. The map selects the list of one key in expected constant time, and the search selects the last entry at or before a query time. The lesson covers a store of timestamped values and an array whose elements keep a history across snapshots.

Matrices with a search form the lesson Search A Sorted Matrix. The shape of the grid turns one number into a row and a column, so a grid that is sorted row after row behaves as one sorted array. The lesson also shows the grid whose rows and columns are sorted separately, where a walk from one corner replaces the half-cut.

### A Pairing That Waits

Sorting with a search is deferred. Sorting arrives from Chapter 05, and searches that depend on a specific sort, such as a search over sorted pairs or sorted events, belong to a later chapter on selection and ordered data. No exercise here assigns those problems.

### What Later Chapters Reuse

Three ideas carry forward.

- **The monotone yes-or-no test** returns in every chapter that asks for the smallest value that works.
- **The half-open interval with the boundary rule** returns when later chapters insert into or split sorted sequences.
- **The floor search on a history list** returns in chapters that keep versions of a structure over time.
