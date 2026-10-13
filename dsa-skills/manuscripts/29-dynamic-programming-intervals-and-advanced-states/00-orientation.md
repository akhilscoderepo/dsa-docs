<!-- section: orientation -->
## Orientation

A build tool joins four chunk files by always merging the two smallest neighbours and copies 70 megabytes, while another plan copies only 64. A batch system gives each worker the cheapest free job and pays 6 minutes more than the best assignment. A registration system counts codes without the digit 0 by testing every integer, and the same loop stalls on limits near 10^18. Each program fails because one position, one set or one bound is not part of the state. This chapter adds that missing piece to a table entry: a range of positions, the children of a tree node, a set of used items, or the digits seen so far.

### Prerequisites

You should know the three previous dynamic programming chapters. They explained how to state in one sentence what a table entry means, how to seed the base entry, and how to read only entries that are already final. The previous chapter ended with a table indexed by the two ends of one string, and the first lessons here reuse it. The code uses arrays of `int`, `long` and `String`, and it assumes `import java.util.*;` in samples.

### The Seven Lessons

Each lesson fixes one question about what an entry remembers.

- **Interval DP** stores the best value for every contiguous range and combines two shorter ranges around one split.
- **Palindrome Partitions** builds a table that says whether each substring reads the same in both directions, then uses it to count the fewest pieces of a prefix.
- **Tree DP** returns several values from each subtree, one for each choice the parent can make, and leaves the second pass that gives an answer for every root to its last exercise.
- **Bitmask Assignment** packs a set of used items into one `int` and explains the bit operations it needs.
- **Submask Aggregation** visits every subset of a mask, and it sums over all subsets with one pass per bit.
- **Digit DP** counts numbers up to a bound by tracking the position and two flags.
- **Optimization Proofs** shows how to shrink a table or a scan without losing any entry the recurrence reads.

### The Closing Lesson

- **DP With Advanced State** compares the three index choices (range, prefix, mask) on one deletion problem, and its four exercises use a range table, a prefix table, a range table and a mask.

### How To Work Through Each Lesson

A lesson opens with a small program that returns a wrong or slow answer on a realistic input. It shows a first version and asks you to predict its output. Later parts name the rule, list the variables, follow two traces, show the code and say when the rule stops fitting. Four exercises close each lesson, and they climb through Build, Vary, Boundary and Recognize. Read a hint only after a real attempt.

### What You Can Do After This Chapter

You can read a problem and name the state that its entries need: a range, a mask, a pair of flags or a subtree summary. You can size the table before allocating it. You can fill the table in an order that finishes every needed entry first, and you can state which entries an optimization may drop.

### What Later Chapters Reuse

The bit operations from the bitmask lessons return in the bits and number theory chapter, which treats them in depth. Chapters on trees and graphs reuse the subtree summary. Specialized speedups for recurrences, such as Knuth, divide and conquer, and convex hull optimizations, need their own proofs and have no lesson here.
