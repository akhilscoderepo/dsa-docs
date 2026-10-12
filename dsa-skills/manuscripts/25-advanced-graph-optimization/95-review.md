<!-- section: review -->
## Review

A refund price comes out wrong because one fee was a credit. A cable plan costs more than the cheapest plan. A support tool needs an hour to find the links that matter. Each failure matches a question below. Return to this page after the lessons and again after a few days. Each question describes a situation and hides the lesson name.

### Recognition Questions

```quiz
{"id": "ga-rev-bellman-ford", "q": "A pass over all edges reads and writes the same distance array, so one pass can chain two edges. What does that change?", "options": ["Nothing, the answer is the same", "The pass can cover more than the allowed number of edges, which breaks a limit on edges", "The graph becomes undirected", "The array overflows"], "answer": 1, "explain": "After pass i the distances must cover routes of at most i edges. Reading new values inside the same pass lets a route use extra edges, so a limit on the number of edges no longer holds."}
```

```quiz
{"id": "ga-rev-floyd-warshall", "q": "In the table method, which loop must be the outermost one?", "options": ["The loop over the start vertex", "The loop over the end vertex", "The loop over the intermediate vertex", "Any of them, since the three loops are symmetric"], "answer": 2, "explain": "The round for k admits vertex k as an intermediate for every pair. Putting another loop outside the round breaks the claim that all intermediates up to k are already allowed."}
```

```quiz
{"id": "ga-rev-prim", "q": "A vertex is already in the tree, and the heap returns an edge that leads to it. What does the method do with that edge?", "options": ["Adds it, because it is the cheapest", "Removes the other endpoint from the tree", "Stops the search", "Skips it, because it no longer crosses from the tree to an outside vertex"], "answer": 3, "explain": "The edge was a crossing edge when it entered the heap, yet its target joined the tree through a cheaper edge. Accepting it would close a cycle."}
```

```quiz
{"id": "ga-rev-kruskal", "q": "A sorted edge joins two vertices that already have the same root. What happens?", "options": ["The method buys the cheaper one", "The method merges the two groups again", "The method skips the edge, because it would close a cycle", "The method reorders the list"], "answer": 2, "explain": "Equal roots show that a chain of bought edges already joins the endpoints. A further edge between them adds cost and no new connection."}
```

```quiz
{"id": "ga-rev-hierholzer", "q": "In the trail walk, when does a vertex go into the output list?", "options": ["When the walk first reaches it", "When it has been visited twice", "When it has the most unused edges", "When no unused edge leaves it"], "answer": 3, "explain": "A vertex with no unused outgoing edge is a dead end of the open walk. Writing it then, and reading the list backward, yields a trail that uses every edge once."}
```

```quiz
{"id": "ga-rev-strong-components", "q": "A directed graph has an edge from A to B and no path from B back to A. What follows for the components?", "options": ["A and B belong to different components", "A and B belong to one component", "The graph has a negative cycle", "B is a bridge"], "answer": 0, "explain": "Vertices share a strongly connected component only when each reaches the other. A one-way connection keeps them in separate components."}
```

```quiz
{"id": "ga-rev-low-links", "q": "A child v of vertex u has low[v] greater than disc[u]. What does this show about the tree edge from u to v?", "options": ["It lies on a cycle", "It is the only connection between the subtree of v and the rest, so it is a bridge", "It has the smallest weight", "u is the root"], "answer": 1, "explain": "No edge from the subtree of v reaches u or any earlier vertex except the tree edge itself. Removing that edge cuts the subtree off."}
```

```quiz
{"id": "ga-rev-mst-decisions", "q": "A shortest path tree from vertex 0 and a minimum spanning tree are built on the same weighted graph. Why can their total weights differ?", "options": ["Only one of them is a tree", "A minimum spanning tree ignores edge weights", "One minimizes each route from vertex 0 and the other minimizes the sum of all chosen edges", "They never differ"], "answer": 2, "explain": "A shortest path tree fixes the cost of every route from the source. A minimum spanning tree has the smallest total weight and may use longer routes from the source."}
```

```quiz
{"id": "ga-rev-choose-method", "q": "A statement asks for the links whose failure splits a network. Why does a shortest path search from one site fail to answer it?", "options": ["It cannot read undirected links", "It needs a sorted edge list", "It reports distances from a source, and a bridge is not a distance", "It always runs too long on small graphs"], "answer": 2, "explain": "The goal names a structural property, so the method must keep a fact about discovery times and low links. Distances from a source do not carry that fact."}
```
