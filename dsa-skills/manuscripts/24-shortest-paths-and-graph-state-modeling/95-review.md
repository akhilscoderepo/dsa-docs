<!-- section: review -->
## Review

Return here after the lessons and again after a few days. The scenarios do not name the technique, so decide first what a state contains, what a cost is and which order the frontier must follow, then read the options. These questions test prediction and recognition, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "sp-rev-bfs-weights", "q": "Roads have tolls of 1, 5 and 20. A student runs ordinary breadth-first search and reports the fewest roads. What has been answered?", "options": ["The cheapest route.", "The route with the fewest roads, which may cost more than another route.", "The most expensive route.", "Nothing useful, the search never ends."], "answer": 1, "explain": "Breadth-first search treats every road as one step. It is correct for cost only when every step costs the same."}
```

```quiz
{"id": "sp-rev-final-value", "q": "With nonnegative weights, why is the smallest tentative cost taken from the heap already final?", "options": ["Every other cost is larger, and adding a nonnegative weight cannot make a later route cheaper.", "The heap sorts all edges first.", "The graph is a tree.", "Costs never change after the first push."], "answer": 0, "explain": "Any route through an unsettled vertex already costs at least the removed value, and further nonnegative weights only add to it."}
```

```quiz
{"id": "sp-rev-negative-edge", "q": "What breaks when one edge has a negative weight?", "options": ["Nothing, only the code size changes.", "A vertex taken from the heap may later be reached more cheaply through the negative edge, so it was not final.", "The heap refuses negative numbers.", "The graph becomes directed."], "answer": 1, "explain": "The argument that a removed value cannot improve depends on weights never decreasing a route."}
```

```quiz
{"id": "sp-rev-stale", "q": "A heap holds two entries for the same vertex, with costs 9 and 4. The table says the best cost is 4. The entry with 9 is popped later. What should happen?", "options": ["Relax all its edges again.", "Remove the 4 from the table.", "Skip it, because its stored cost differs from the table.", "Stop the whole search."], "answer": 2, "explain": "The entry is stale. Its stored cost is no longer the best known, so expanding it can only repeat work."}
```

```quiz
{"id": "sp-rev-remove-object", "q": "Why is calling remove(Object) on a PriorityQueue to delete an outdated entry a poor plan?", "options": ["It throws an exception.", "It deletes every entry.", "It reorders the table.", "It scans the queue linearly to find the entry."], "answer": 3, "explain": "The queue is not indexed by value, so removal is a linear search. Leaving the entry and skipping it later is cheaper."}
```

```quiz
{"id": "sp-rev-state-pair", "q": "A traveller holds one single-use coupon. The distance table has one cell per stop. What can go wrong?", "options": ["A cheaper arrival that has already spent the coupon may hide a dearer arrival that still holds it.", "The table is too large.", "The coupon makes distances negative.", "Stops cannot be numbered."], "answer": 0, "explain": "The two arrivals have different futures. The table needs a cell for each pair of stop and coupon state."}
```

```quiz
{"id": "sp-rev-leg-limit", "q": "A trip may use at most k flights. Why does plain Dijkstra with one cost per city fail?", "options": ["Because costs are negative.", "Because it cannot read flights.", "Because it needs a stack.", "It may keep the cheapest arrival at a city and discard a dearer one that used fewer flights and could still continue."], "answer": 3, "explain": "Cost alone does not dominate when the number of legs is limited. State must include how many flights were used."}
```

```quiz
{"id": "sp-rev-layer-copy", "q": "In a layered relaxation that allows at most one more flight per round, why read the previous round's table and write a fresh one?", "options": ["Updating in place can chain two flights within one round, breaking the limit.", "It saves memory.", "It makes the answer smaller.", "It is only a style choice."], "answer": 0, "explain": "In-place updates let a cost improved in this round be used again in the same round, which counts as extra flights."}
```

```quiz
{"id": "sp-rev-alt-colour", "q": "Edges are red or blue and must alternate. A vertex is marked visited when first reached. What can be lost?", "options": ["Nothing, the first arrival is the best.", "Arrivals with the other last colour, whose next edges differ.", "The source.", "Self-loops only."], "answer": 1, "explain": "The last colour decides which edges may follow, so the visited mark belongs to the pair of vertex and last colour."}
```

```quiz
{"id": "sp-rev-deque-end", "q": "In a search where every edge costs zero or one, where does a successful zero-cost relaxation put the neighbour?", "options": ["At the back of the deque.", "In a heap.", "Nowhere, zero edges are ignored.", "At the front of the deque, so it is processed at the same cost as its parent."], "answer": 3, "explain": "A free step keeps the cost unchanged, so the neighbour belongs with the current cost band at the front. A paid step goes to the back."}
```
