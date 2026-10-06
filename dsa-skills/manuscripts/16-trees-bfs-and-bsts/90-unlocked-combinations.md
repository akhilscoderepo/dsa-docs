<!-- section: unlocked-combinations -->
## Unlocked Combinations

A row-by-row printout of a tree crashes on a long chain, and a validity check that repeats a lookup for every node never finishes at scale. This chapter releases two pairings that its prerequisites allow, and it names one pairing that waits for the heap chapter.

### Pairings Taught In This Chapter

A tree and a queue form the lesson Group Nodes By Depth With A Queue. The tree supplies the children of each node, and the queue supplies the order that keeps one depth together. The lesson adds one idea: the loop that reads rows works unchanged for any number of children, for any aggregate of a row, and for a limit on the number of rows. Its exercises cover row sums, a bottom-up zigzag, a right-side view of the first rows and the N-ary tree.

A search tree and value limits form the lesson Search And Validate A Search Tree. The comparisons of a one-path lookup define an interval of keys for every position, and the limits carried down the recursion are exactly that interval. The lesson adds one idea: a single pass that checks each node against its interval replaces a separate lookup for every node. Its exercises cover the depth of a key, a check against outer limits, the kth largest key and a delete that uses the predecessor.

### One Pairing Waits For The Heap Chapter

Traversing a tree in the order of a priority queue joins the tree walks of this chapter with a heap. That pairing needs the heap operations and the rule for ordering ties, which Chapter 17 teaches. Chapter 17 owns the problems of that pairing, and this chapter assigns none of them.
