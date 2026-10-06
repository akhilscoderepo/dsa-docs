<!-- section: unlocked-combinations -->
## Unlocked Combinations

A grid game asks for the cheapest path where stepping onto a wall costs 1 and an open cell costs 0. A full heap search works but pays a logarithm on every step. A deque removes that cost. This chapter releases two pairings, where a pairing is a lesson that joins two earlier topics into one method, and it leaves one for later.

### Pairings Taught In This Chapter

The lesson Shortest Paths With A Heap joins the graph with the heap. Edge relaxation proposes better costs, the heap exposes the smallest proposal, and a stale entry check replaces a decrease operation. The lesson adds one idea: the stored cost may be a maximum edge or a product, as long as extending a path never improves it.

The lesson Shortest Paths With A Deque joins the graph with the deque. The edge cost chooses which end of the deque receives the improved vertex. The lesson adds one idea: a grid cell can pay for entering it, and the start cell then pays nothing.

### Pairing That Waits For A Later Chapter

Negative edge costs break both searches, because a cheaper path can appear after a vertex is finished. A method that relaxes every edge in repeated rounds handles them, and this chapter assigns no exercises for it. Chapter 25 covers negative edges, and the repeated-round scan in the heap lesson is the idea that it uses.
