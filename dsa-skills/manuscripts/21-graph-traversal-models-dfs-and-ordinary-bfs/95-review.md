<!-- section: review -->
## Review

Come back to this section after the lessons and again after a few days. The scenarios avoid naming the technique, so decide first what the vertices are, what an edge means and what the mark records, then read the options. These questions test prediction and recognition, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "gt-rev-matrix-cost", "q": "A road map has 100000 junctions and 150000 roads. Which storage fits in memory, and why?", "options": ["A matrix, since each probe is constant time.", "Lists of neighbours, since the entries number about the roads and not the square of the junctions.", "Either one, since both hold the same cells.", "Neither, since the roads are undirected."], "answer": 1, "explain": "A matrix needs ten billion cells here. Lists hold one entry per edge end, which is a few hundred thousand."}
```

```quiz
{"id": "gt-rev-clone-by-value", "q": "Two different nodes of a graph carry the same label. A copy routine keys its table by the label. What goes wrong?", "options": ["Nothing, the labels are unique anyway.", "The copy visits nodes in a different order.", "Both originals share one copy and the shape of the graph changes.", "The copy loses all labels."], "answer": 2, "explain": "A table keyed by value merges nodes that are distinct objects. The key must be the identity of the original node."}
```

```quiz
{"id": "gt-rev-mark-timing", "q": "A breadth-first walk marks a vertex only when it is taken off the queue. A diamond graph has two routes into its last vertex. What can happen?", "options": ["The last vertex is queued twice.", "The walk never ends.", "The first vertex is skipped.", "Nothing, the answer is the same and so is the cost."], "answer": 0, "explain": "Both middle vertices see the last one as unmarked and queue it. Marking when the vertex enters the queue lets exactly one of them do so."}
```

```quiz
{"id": "gt-rev-scattered-graph", "q": "A walk from vertex 0 marks 6 of 10 vertices. Which statement is safe?", "options": ["The graph has exactly two groups.", "The remaining four are unreachable from vertex 0, and nothing more is known about them.", "The walk has a bug.", "The graph contains a loop."], "answer": 1, "explain": "Unmarked vertices are simply not reachable from the start. They may form one group or several, so counting groups needs a fresh start from each unmarked vertex."}
```

```quiz
{"id": "gt-rev-grid-neighbors", "q": "Four-direction flood fill is run on a board. Two cells of the same colour touch only at a corner. Are they filled together by one walk from one of them?", "options": ["Yes, a board always implies eight neighbours.", "Only if both are on the border.", "Not unless another same-coloured chain joins them through side steps, because the step table lists four directions.", "Only when the colour is dark."], "answer": 2, "explain": "A board does not imply diagonal moves. The step table is the definition of the graph."}
```

```quiz
{"id": "gt-rev-shared-mark-paths", "q": "A route listing keeps one shared set of used vertices that is never cleared. On a diamond graph from top to bottom, how many routes does it find?", "options": ["Two, the correct count.", "One, since the second route meets used vertices.", "None.", "Four."], "answer": 1, "explain": "The first route marks the bottom vertex and the second is then blocked. Route listing needs a path-local mark that is removed on the way back."}
```

```quiz
{"id": "gt-rev-bfs-distance", "q": "Why is the first time a breadth-first walk reaches a vertex a shortest route in an unweighted graph?", "options": ["The queue hands out vertices in nondecreasing distance, so no later route can be shorter.", "The walk tries every route and keeps the least.", "The stack remembers the best route.", "Marking prevents long routes from being written down."], "answer": 0, "explain": "All vertices at distance d leave the queue before any at d + 1, so a vertex first met from distance d gets distance d + 1 and no shorter chance exists."}
```

```quiz
{"id": "gt-rev-two-sides", "q": "A graph has two separate groups. The first is two-colourable and the second contains a triangle. Which method gives the right answer?", "options": ["Colour from vertex 0 only.", "Count the edges.", "Colour every group, starting afresh at each uncoloured vertex.", "Check only the largest group."], "answer": 2, "explain": "A triangle forces a conflict, but only a walk that enters that group can see it."}
```

```quiz
{"id": "gt-rev-directed-cycle", "q": "In a directed depth-first walk, the walk meets a neighbour that is already finished. Is that a cycle?", "options": ["Yes, any marked neighbour is a cycle.", "Yes, if the graph is large.", "Only if the neighbour is the parent.", "No, a finished vertex cannot lead back to the vertices still open."], "answer": 3, "explain": "A cycle needs an edge back to a vertex that is still on the current route. A finished vertex is on no open route, as in a diamond with no loop."}
```

```quiz
{"id": "gt-rev-grid-wrap", "q": "In the terrace combination, a board has columns that wrap around but rows that do not. What changes in the traversal?", "options": ["The visited array becomes a map.", "Only the step table and the column bound change; the outer scan and the mark stay as they were.", "The walk must be recursive.", "Each row needs its own walk."], "answer": 1, "explain": "The graph changes through its neighbour rule, and the traversal that consumes it does not."}
```
