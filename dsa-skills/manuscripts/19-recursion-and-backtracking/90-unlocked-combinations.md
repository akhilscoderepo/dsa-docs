<!-- section: unlocked-combinations -->
## Unlocked Combinations

A word game that runs one board search for each dictionary word repeats every shared prefix, and a memory trick that is applied before its state is defined returns wrong answers. This chapter releases one pairing that its prerequisites allow, and it names one pairing that waits for a later chapter.

### Pairing Taught In This Chapter

A prefix tree and a path search with marks form the lesson Search A Board With A Prefix Tree. The path marks keep each cell on one path at most once and return to their earlier state when a call exits. The tree node spells the letters of the marked cells and shows at once whether any dictionary word still begins with them. The lesson adds one idea. A missing edge ends a call before it marks anything, and a stored word clears its slot after the first report, so each word appears once. Its exercises cover a one-row search, an any-word test, a first-report order and a full two-dimensional board.

### One Pairing Waits For A Later Chapter

A search can remember the answer of a state that it has seen, so the same state costs one visit and not many. The remembered answer is correct only when two calls with equal arguments always return equal answers. That statement needs a precise definition of the state and of the returned value. Chapter 26 defines both in its dynamic programming contract, and it owns this pairing. This chapter assigns none of its problems.
