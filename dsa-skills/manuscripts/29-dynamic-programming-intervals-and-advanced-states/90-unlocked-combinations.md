<!-- section: unlocked-combinations -->
## Unlocked Combinations

Splitting sixteen numbers into equal-sum groups by trying every order takes 16! steps, which is about 2.1 * 10^13 and never finishes. A table over the 2^16 = 65,536 subsets of used numbers finishes in milliseconds, but only when the set of used numbers is part of the state. This chapter pairs a recurrence with a richer state. One pairing is taught in a lesson here, and one is deferred to a later chapter.

### Pairing Taught In This Chapter

The lesson DP With Advanced State joins the recurrence habit from the earlier dynamic programming chapters with the range, prefix and mask encodings from the first lessons. The recurrence supplies the reuse of earlier answers. The encoding says which subproblem each stored answer belongs to. The lesson adds one idea: choose the index so that everything outside the stored answer is already fixed. Its four exercises find the longest palindromic subsequence in query ranges, cut a string into pieces of a minimum length, burst items with given outer values, and split numbers into groups of equal sum.

### Pairing That Waits For A Later Chapter

Speedups that cut the number of transitions, such as Knuth optimization, divide and conquer optimization and the convex hull trick, hold only for recurrences with a proven structure. Each needs its own proof. A later chapter takes them, and this chapter assigns no problems to them.
