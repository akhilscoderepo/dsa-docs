<!-- section: unlocked-combinations -->
## Unlocked Combinations

One combination is released by this chapter, and a second one is postponed. A third pairing, the use of a table inside a sorted-input method, is reachable from earlier chapters and is only mentioned here.

### Teach Now

Prefix state with a hash map is the eleventh lesson. Chapter 04 supplied maps that record counts and first positions, and this chapter supplied running totals, balances, remainders and parity masks as keys. Together they answer questions about contiguous stretches whose end keys stand in a simple relation: equal to each other, or differing by a target. The ladder moves from a count of stretches with a wide key type, to a stretch reported as a pair of positions, to a modulus too large for an array, to the earliest stretch satisfying a length rule. Its false friend is a map whose keys have no stated meaning, and whose role has been chosen by copying the nearest solution.

### Deferred

Prefix state with a sliding window is deferred to Chapter 09. What is missing here is a rule for moving both ends of a window and a way to compare a moving total with a target when every value is non-negative. Chapter 09 supplies both. This chapter says only that prefix totals and windows can sometimes answer the same question, and it assigns no exercise that depends on a window. Trees that answer range questions while the data changes belong to Chapter 31, and none of their problems are used here.

### Already Covered

Using a sorted order to simplify a question was taught in Chapter 05, and the chapter before this one taught searching over a monotone predicate. Neither is needed to build or read a prefix table, so no lesson here repeats them. Counting how many earlier items satisfy a relation with the current one was introduced with maps in Chapter 04, and the prefix counts lesson of this chapter only changes what the keys mean.
