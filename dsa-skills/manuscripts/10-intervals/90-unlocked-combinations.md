<!-- section: unlocked-combinations -->
## Unlocked Combinations

An interval is only a pair of numbers until a rule says how two pairs relate and an order says which pair to look at next. This chapter used one pairing that its prerequisites already allow, and it names two pairings that need later chapters.

### Pairing Taught In This Chapter

Sorting with intervals forms the lesson Sort Intervals Then Scan Once. Sorting puts processed ranges before unresolved ones, and the interval rule supplies the overlap test. The lesson adds one idea: each question about a list needs a sort key and one carried value, so a decision about the next range takes constant time. Its exercises cover a union length, an insert under a half-open rule, a selection under a closed rule and the positions of arrows.

### Pairings That Wait

A problem that asks how many rooms or machines run at once for assigned work needs the identity of the range that ends next. That structure is a heap ordered by end time, and Chapter 17 owns the rule for keeping and releasing its entries. This chapter names the pairing and assigns none of its problems.

Greedy scheduling with weights also waits. The end-order choice in this chapter maximizes a count, and a weighted version needs a method that compares choices, which a later chapter on dynamic programming supplies.

### What Later Chapters Reuse

Three ideas carry forward.

- **The carried end** returns whenever a later scan keeps the largest or smallest end of what it has processed.
- **The tie policy** returns whenever a later method orders events that share a coordinate, such as in a sweep over a plane.
- **The closed or half-open test** returns whenever a later problem names a range and a boundary that may or may not belong to it.
