<!-- section: unlocked-combinations -->
## Unlocked Combinations

No combination lesson belongs to this chapter. A matrix problem becomes a combination problem only when it needs a second structure, and every second structure on the list comes from a later chapter. The sections below name the later chapter that owns each pairing, so that no exercise here uses a tool the reader has not learned.

### Pairings That Wait For A Later Chapter

Matrices with hash sets arrive in Chapter 04. A row, a column and a box each need a membership check, and that check is the set. Valid Sudoku is the first problem that uses it. The boolean marker arrays in this chapter cover only small consecutive indexes.

Matrices with binary search arrive in Chapter 06. A matrix whose rows and columns are sorted gives the search an order to exploit. This chapter treats every matrix as unordered.

Matrices with graph traversal arrive in Chapter 21. A walk that follows connected cells needs a frontier and a rule for visited cells. The direction cursor here follows one fixed path and has no frontier.

Matrices with dynamic programming arrive in Chapter 26. A table of answers needs cell states and a fill order. The traversals in this chapter produce no such table.

### What Later Chapters Reuse

Three ideas from this chapter carry forward.

- **Offset tables** (lesson 04) return in every grid search in Chapters 21 and 22.
- **Marking before changing** (lesson 06) returns whenever a pass must read the original state of a structure.
- **Region rules on indexes** (lesson 02) return in the dynamic programming tables of Chapter 26.
