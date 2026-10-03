<!-- section: orientation -->
## Orientation

This chapter teaches twelve small techniques for working directly on arrays: scanning with a clear result contract, aggregating, tracking a running extreme, compacting in place, deduplicating sorted data, counting in a bounded domain, voting for a majority, using the array as its own table, and carrying a small state through contiguous sums and products. Each technique is taught on its own, with its own invariant, its own false friend and its own four-step practice ladder. Later chapters combine them, and they can only be combined by someone who knows each one separately.

### What You Need Before Starting

You should have finished Chapter 00, or be comfortable doing what it teaches. That means reading a problem's constraints to estimate a time budget, asking whether the input may be modified, telling a subarray from a subsequence, and counting the executions of the dominant statement. You should also be able to write a loop over an array in Java and to compile and run a short program. No data structure other than the array appears in this chapter, and the only library classes used are `List` for output and `Random` inside the checking code.

### The Twelve Lessons

The first six lessons build the vocabulary of one pass. Direct scans return early on a match and state what a miss means. Aggregation folds the array into one value and fixes where the fold starts. Running extremum and best gain keep the smallest value seen so far to price a later position. Stable compaction uses a read index and a write index to keep chosen elements in order. Sorted deduplication uses the ordering to turn a membership test into one comparison. Frequency arrays let a value choose its own slot when the range is small and promised.

The last six lessons carry state that is cleverer than a single number. Majority vote cancels distinct pairs and demands a verification pass. Cyclic placement swaps each value into its home slot. Sign marking records a sighting in the sign of a slot. Kadane state keeps the best stretch ending here. Product state keeps both the best and the worst, because a negative reverses the order. Circular Kadane turns a wrapping stretch into a total minus an excluded block.

### How To Work Through A Lesson

Start with the story and the plain first version, and decide for yourself what is wasteful before the bottleneck section tells you. Use the buttons to step through the trace, pausing on the step that the text singles out. Attempt the exercises in order, put your own answer in the notes box before opening the hint, and read the solution last. Each solution carries Java that runs with assertions during the build, and each is checked against a slow but obviously correct oracle on random inputs, so the numbers in the solutions were executed.

### Leaving The Chapter

By the end you should be able to look at an array problem and name the contract, the state you would carry, the invariant that makes the shortcut valid, and the nearest technique that looks similar but is not. The questions in the review section probe exactly that, and you can retake them after a few days.
