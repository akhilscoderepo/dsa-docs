<!-- section: review -->
## Review

A route finder reports a cost that a cheaper road beats, and a flight search ignores its stop limit. Each failure matches a question below. Return to this page after the lessons and again after a few days. Each question describes a situation and hides the lesson name.

### Recognition Questions

```quiz
{"id": "sp-rev-dijkstra", "q": "A graph has an edge of weight -2. Why can the heap method return a wrong cost?", "options": ["The heap rejects negative keys", "A finished vertex may still be improved through the negative edge later", "The adjacency list loses the edge", "The method overflows an int"], "answer": 1, "explain": "The method assumes that no later path can beat the cheapest unfinished vertex. A negative edge breaks that assumption, so a finished cost can drop."}
```

```quiz
{"id": "sp-rev-stale", "q": "A vertex has the queued entries (9, v) and (4, v), and dist[v] is 4. What does the method do when it removes (9, v)?", "options": ["Expands v with cost 9", "Skips it, because 9 differs from dist[v]", "Replaces dist[v] with 9", "Removes (4, v) from the heap"], "answer": 1, "explain": "The entry carries an outdated cost. Comparing it with the stored best cost identifies it, and the method drops it without relaxing any edge."}
```

```quiz
{"id": "sp-rev-state", "q": "A traveler holds one discount coupon. Why does one cost per city fail?", "options": ["Cities have equal costs", "Arriving with the coupon unused can lead to a cheaper finish than a cheaper arrival without it", "The coupon changes the city name", "The graph becomes undirected"], "answer": 1, "explain": "Two arrivals at one city have different futures. The pair of city and coupon flag keeps both."}
```

```quiz
{"id": "sp-rev-stops", "q": "A cheapest route may use at most 3 flights. A cost of 7 reaches city c in 2 flights and a cost of 9 reaches it in 1 flight. Which arrival may matter?", "options": ["Only the cost of 7", "Both, because the costlier arrival leaves one more flight to use", "Only the cost of 9", "Neither"], "answer": 1, "explain": "The cheaper arrival has 1 flight left and the costlier arrival has 2 flights left. The costlier arrival can reach cities that the cheaper one cannot, so a single cost per city loses it."}
```

```quiz
{"id": "sp-rev-colors", "q": "A red edge enters node x first, and later a blue edge enters x. What happens if the search marks x visited once?", "options": ["Nothing, both arrivals are equal", "The blue arrival is dropped, and the edges that need a blue arrival never run", "The search stops", "The distance doubles"], "answer": 1, "explain": "The red arrival allows only blue edges next, and the blue arrival allows only red edges next. Dropping one removes a whole set of continuations."}
```

```quiz
{"id": "sp-rev-deque", "q": "An edge costs 0 and improves the cost of vertex v. Which end of the deque receives v?", "options": ["The back, with other new vertices", "The front, because v has the same cost as the vertex being expanded", "Neither, because costs of 0 are skipped", "The middle"], "answer": 1, "explain": "The deque holds costs in nondecreasing order. A vertex with the current cost belongs before every entry that costs one more."}
```

```quiz
{"id": "sp-rev-heap-score", "q": "A search must find the route whose largest single edge is smallest. What changes in the heap method?", "options": ["Nothing changes", "The proposed cost becomes the larger of the route's cost so far and the edge, and the rest stays", "The heap becomes a stack", "Every edge cost becomes 1"], "answer": 1, "explain": "Extending a path never lowers its largest edge, so the finishing rule still holds. Only the combining step changes, from the sum of the route's cost and the edge to their maximum."}
```

```quiz
{"id": "sp-rev-grid", "q": "A grid search charges 1 for entering a cell with value 1. What does the start cell with value 1 cost?", "options": ["1, like every cell", "0, because the path never enters the start cell", "2", "It depends on the goal"], "answer": 1, "explain": "The path begins on the start cell and pays only for cells it enters afterward."}
```
