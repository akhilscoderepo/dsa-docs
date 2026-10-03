<!-- section: unlocked-combinations -->
## Unlocked Combinations

This chapter releases one combination and defers two. A combination is released only when every technique it needs has already been taught, and each released one gets its own lesson with its own exercise ladder.

### Released Now

Sliding Window With Frequency State is released. It needs moving boundaries, which this chapter taught, and counts, deficits and violations kept in a table, which Chapter 04 and the earlier lessons here taught. The lesson that follows this page, Window Frequency State, pulls the shared skeleton out of four problems and shows that one status counter, updated only at the slot that changed, serves all of them. Its ladder revisits Permutation in String, Longest Substring Without Repeating Characters, Longest Repeating Character Replacement and Minimum Window Substring, and each exercise changes the alphabet or the contract so that it is a new task rather than a repeat.

### Deferred

Sliding Window With A Deque is deferred to Chapter 13. A deque can keep the best candidate for each moving window, but its two invariants, that candidates are kept in dominance order and that expired indices are discarded from the front, have not been taught yet. Sliding Window Maximum and its relatives belong to Chapter 13, and no exercise in this chapter assigns them.

Sliding Window With A Heap is deferred for a similar reason. A heap can supply a window's extreme value with lazy deletion, but heaps are taught in Chapter 17, so the combination waits for that chapter.

### Already Covered

Prefix sums as an alternative to a window were taught in Chapter 07, so this chapter links back to them instead of teaching them again. The counting lesson names the exact situation, a sum condition over values that may be negative, where the window is wrong and prefix sums are the right tool.
