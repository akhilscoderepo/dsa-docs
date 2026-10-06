<!-- section: review -->
## Review

A planner schedules a course before its prerequisite, and a cluster counter reports one group too many. Each failure matches a question below. Return to this page after the lessons and again after a few days. Each question describes a situation and hides the lesson name.

### Recognition Questions

```quiz
{"id": "dg-rev-kahn", "q": "A queue run removes 5 of 7 vertices and then the queue is empty. What does that say about the graph?", "options": ["A directed cycle keeps two vertices from reaching indegree zero", "The graph is disconnected", "The graph has two sources", "The queue was too small"], "answer": 0, "explain": "A vertex on a cycle always keeps an unresolved incoming edge, so its indegree never reaches zero and it never enters the queue."}
```

```quiz
{"id": "dg-rev-color", "q": "A depth-first search from vertex 0 reaches a vertex that was fully finished earlier through another branch. Is that a cycle?", "options": ["Yes, it is visited", "No, only an edge to a vertex still on the current call path closes a cycle", "Yes, if it has a higher index", "Only in an undirected graph"], "answer": 1, "explain": "A finished vertex cannot reach the current vertex again, so the edge forms no loop. Only an edge to an active vertex does."}
```

```quiz
{"id": "dg-rev-parent", "q": "An undirected search walks the edge from 1 to 2 and then sees vertex 1 again from vertex 2. Why is this not a cycle?", "options": ["Vertex 1 has a lower index", "Vertex 1 is the vertex from which vertex 2 was entered", "Edges are visited twice by design and are ignored", "Vertex 2 has degree one"], "answer": 1, "explain": "The same edge appears from both endpoints. Only a visited neighbor other than the entering vertex shows a second route."}
```

```quiz
{"id": "dg-rev-find", "q": "A chain of 1000 parent links is searched once with path compression. What does the next search from the deepest node cost?", "options": ["Still 1000 steps", "One step to the root", "Zero steps", "About 10 steps"], "answer": 1, "explain": "Compression rewrote every visited node to point directly at the root, so the next walk takes one link."}
```

```quiz
{"id": "dg-rev-size", "q": "A merge compares the size stored at element a with the size stored at element b, where neither is a root. What goes wrong?", "options": ["Nothing, sizes are equal for all members", "The size values are stale, so the smaller tree may end up on top", "The array overflows", "The parents form a cycle at once"], "answer": 1, "explain": "Only roots keep a valid size. The comparison must use find(a) and find(b)."}
```

```quiz
{"id": "dg-rev-connect", "q": "Union is called twice for the same pair of elements. What should the group count do on the second call?", "options": ["Drop by one again", "Stay unchanged", "Reset", "Raise an error"], "answer": 1, "explain": "Both elements share a root after the first call, so the second call merges nothing and leaves the count alone."}
```

```quiz
{"id": "dg-rev-kruskal", "q": "Kruskal ends with fewer than V minus 1 accepted edges. What does that mean?", "options": ["The sort failed", "The graph is disconnected, so no spanning tree exists", "Some edges had equal weight", "The tree is minimal"], "answer": 1, "explain": "Every accepted edge joins two groups, and V minus 1 joins are needed to reach one group."}
```
