<!-- section: unlocked-combinations -->
## Unlocked Combinations

A window alone is only a pair of indexes. It becomes a method when something inside the window gives a reason for each move. This chapter taught one pairing that its prerequisites already allow, and it names two pairings that need material from later chapters.

### Pairing Taught In This Chapter

A window with counts forms the lesson Track Counts Inside A Window. The boundaries say which positions are active, and the counts say what those positions hold. The lesson names and generalizes one idea, a status counter that summarises a rule over the counts. The missing count of lesson 04 and the distinct count of lesson 05 are already status counters. Each step answers the rule in constant time, except for the replacement budget, which needs the stale peak of lesson 09. Its exercises use four rules: an exact match, a limit on repeats, a replacement budget and a minimum cover.

### Pairings That Wait

A window that must report the largest or smallest value for every position needs a structure that keeps candidates in order and drops expired ones. That structure is a deque, and the chapter on deques owns the rule for ordering candidates and expiring them by index. This chapter names the combination but assigns none of its problems.

A window that needs the sum of a range for many unrelated queries is better served by prefix sums, which the chapter before this one taught. The window method answers one left-to-right pass, and the prefix method answers any range. The choice depends on how many queries follow, and the lessons here point out each place where that choice matters.

A window whose condition involves the largest or smallest value of the window together with a count, such as a spread below a limit, needs a heap or a pair of deques. The chapter on heaps owns that combination, because a heap supports removal of the best value in logarithmic time.

### What Later Chapters Reuse

Three ideas carry forward.

- **The status counter** returns whenever a later method keeps a rule over counts that changes by one letter per step.
- **The valid starts of an end index** return whenever a later method counts all ranges that satisfy a condition that survives removal.
- **The difference of two at-most counts** returns whenever a later method counts ranges with an exact property that has no stable boundary.
