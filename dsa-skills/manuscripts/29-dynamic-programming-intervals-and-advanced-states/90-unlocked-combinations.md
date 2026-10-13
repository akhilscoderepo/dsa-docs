<!-- section: unlocked-combinations -->
## Unlocked Combinations

A scheduler assigns twenty jobs to twenty machines by trying every order, which is about 2.4 * 10^18 orders and never finishes. A table over the set of used machines finishes in milliseconds, but only when the set of used machines is part of the state. This chapter combines a recurrence with a richer state, and each pairing below is a lesson that joins earlier topics.

### Pairing Taught In This Chapter

The lesson DP With Advanced State joins the recurrence habit from the earlier dynamic programming chapters with the range, prefix and mask encodings from the first lessons. The recurrence supplies the reuse of earlier answers. The encoding says which subproblem each stored answer belongs to. The lesson adds one idea: choose the index so that everything outside the stored answer is already fixed. Its four exercises find the longest palindromic subsequence in query ranges, cut a string into pieces of a minimum length, burst items with given outer values, and split numbers into groups of equal sum.

### Pairing That Waits For A Later Chapter

Speedups that cut the number of transitions, such as Knuth optimization, divide and conquer optimization and the convex hull trick, hold only for recurrences with a proven structure. Each needs its own proof. A later chapter takes them, and this chapter assigns no problems to them.
