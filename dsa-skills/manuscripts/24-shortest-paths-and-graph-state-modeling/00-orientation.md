<!-- section: orientation -->
## Orientation

Counting edges stops being enough the moment edges cost different amounts. A road with a toll, a flight with a fee, a turn that drains a battery, a link that fails with some probability: each asks for the cheapest route and not the shortest one. This chapter keeps the picture of spreading outward from a source, but orders the spreading by accumulated cost. It then shows how to widen what counts as a place in the graph, because many cheapest-route questions hide a second fact, such as a coupon left, a number of legs used or the colour of the last edge, that changes what is allowed next.

### What To Bring

You need the unweighted search of Chapters 21 and 22, the heap and its comparator from Chapter 17, and the deque from Chapter 13. The idea that a state may be richer than a position comes from the state-space lesson of Chapter 22. Negative weights are not assumed anywhere, and the chapter says plainly where they would break its arguments.

### The Eight Lessons

The first lesson relaxes edges and always settles the smallest tentative cost. The second explains why the heap will hold outdated entries, and what to do on removing one. The third gives a vertex a second coordinate and shows how a state pair, not a vertex, becomes the unit of search. The fourth limits the number of legs, and the fifth lets edge colours restrict the next edge. The sixth handles the special case where every cost is zero or one and a double-ended queue replaces the heap. The seventh and eighth are the released combinations: a graph with a heap, and a graph with a deque, each with a ladder of its own.

### How To Work Through A Lesson

Read the scene and guess which cost is paid twice by the slow method. Before an insight, say what the algorithm may promise about the smallest value it removes. In traces, watch two things: what the distance table says and what is still waiting in the frontier. For an exercise, decide first what a state contains, what a proposal is, and what tie rule fixes the answer. Each solution file runs against a slow independent method on random graphs, and the failure of each false friend is asserted on a concrete small graph.

### Leaving The Chapter

You should be able to explain why the smallest remaining cost is final when weights are nonnegative, why a heap entry can be skipped without being removed, how to encode a state that includes a resource or a last colour, why a layer limit needs a fresh copy per layer, and why a deque can stand in for a heap for zero and one costs. The review section turns these into short scenarios.
