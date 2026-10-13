<!-- section: unlocked-combinations -->
## Unlocked Combinations

A report must show the 100 slowest requests out of a million, and a second report must count how many requests became slower than an earlier request by more than a fixed margin. The first report needs one rank, and the second needs counted pairs. The pairing below handles both with the same partition and merge ideas.

### Pairing Taught In This Chapter

The lesson Partition And Selection joins partition with quickselect and with merge counting. A partition proves the final position of one value, and selection then discards the side that cannot hold the target position. Merge counting appears as the contrast: it answers questions about pairs, which a single selected rank cannot answer. Its four exercises select a rank and report the range of equal positions, select the closest points and count ties at the boundary, count smaller values to the right within a distance, and count pairs under a scaled threshold.

### Pairing That Waits For A Later Chapter

Order statistics over a stream need a structure that accepts updates and still answers rank questions, and each update needs a stated contract for what is kept. A later chapter owns that topic, and this chapter assigns no problems to it.
