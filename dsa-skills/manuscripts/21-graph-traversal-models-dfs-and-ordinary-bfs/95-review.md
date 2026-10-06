<!-- section: review -->
## Review

A course scheduler accepts two courses that wait for each other, and a map counter reports three islands for one connected landmass. Each failure matches a question below. Return to this page after the lessons, and again after a few days. Each question describes a situation and hides the lesson name. Choose an answer before you read the explanation.

### Recognition Questions

```quiz
{"id": "gt-rev-matrix-cost", "q": "A graph has 100000 vertices and 150000 edges. Which storage fits in memory, and why?", "options": ["An adjacency matrix, because lookups are constant time", "An adjacency list, because it stores about V + E entries and a matrix needs V squared cells", "Either one, because both store the edges once", "Neither, because the graph is too large"], "answer": 1, "explain": "A matrix of 100000 by 100000 cells holds ten billion entries. An adjacency list holds one entry per edge end plus one list per vertex."}
```

```quiz
{"id": "gt-rev-clone-map", "q": "A copy of a cyclic graph never finishes. Which step is missing?", "options": ["Sorting the neighbors", "Storing the copy in the map before visiting the neighbors", "Copying the labels", "Using recursion instead of a queue"], "answer": 1, "explain": "When the copy is stored first, an edge that returns to the same vertex finds the copy in the map and stops. Without it, the walk creates a new copy at every return."}
```

```quiz
{"id": "gt-rev-mark-time", "q": "A queue-based walk marks a vertex only when it leaves the queue. What can happen on a graph where two vertices share a neighbor?", "options": ["The walk skips the neighbor", "The neighbor enters the queue twice", "The walk stops at once", "Nothing, the result is identical"], "answer": 1, "explain": "Both vertices see the neighbor unmarked and both enqueue it. Marking at enqueue time prevents the second entry."}
```

```quiz
{"id": "gt-rev-components", "q": "A program reports 1 cluster after one search from vertex 0, but that search reached only 4 of the 9 vertices. How does the program get the true cluster count?", "options": ["Nothing changes, because the graph has one component", "A second search from vertex 0", "Start a new search from each vertex still unvisited, and count the starts", "A sort of the vertices"], "answer": 2, "explain": "Every start on an unvisited vertex reaches one whole new component. Counting the starts counts the components."}
```

```quiz
{"id": "gt-rev-grid-diagonal", "q": "A grid walk uses four moves. Two land cells touch only at a corner. What does the walk decide?", "options": ["They belong to one island", "They belong to different islands, unless the problem lists diagonal moves", "The grid is invalid", "The walk fails"], "answer": 1, "explain": "The array does not imply diagonals. The moves written in the walk define the edges."}
```

```quiz
{"id": "gt-rev-path-undo", "q": "A path enumerator uses one global visited array and misses valid paths in a DAG. What repairs it?", "options": ["Sorting the edges", "Removing the vertex from the path after each branch returns", "Using a queue", "Marking at enqueue time"], "answer": 1, "explain": "Two different paths may share a vertex. The path-local state must hold only the current chain, so the vertex is removed when its call returns."}
```

```quiz
{"id": "gt-rev-bfs-distance", "q": "A breadth-first walk from vertex 0 first discovers vertex 5 at distance 3. What does this prove?", "options": ["Some route of 3 edges exists, and no route has fewer edges", "A route of 3 edges exists, and shorter routes may exist", "Vertex 5 has three neighbors", "Every route has 3 edges"], "answer": 0, "explain": "The queue removes vertices in nondecreasing distance, so the first discovery uses the fewest edges."}
```

```quiz
{"id": "gt-rev-odd-cycle", "q": "Which graph cannot be colored with two colors?", "options": ["A path of four vertices", "A cycle of five vertices", "A cycle of four vertices", "Two separate edges"], "answer": 1, "explain": "Colors alternate around a cycle, so an odd cycle forces two neighbors to share a color."}
```

```quiz
{"id": "gt-rev-parent-edge", "q": "An undirected walk reaches vertex B from A and sees A again as a neighbor. Is that a cycle?", "options": ["Yes, A is visited", "No, the edge is the one the walk arrived by", "Yes, but only in directed graphs", "Only if A has other neighbors"], "answer": 1, "explain": "The edge A-B is stored in both directions, so the walk sees A from B. Only a visited neighbor other than the parent closes a cycle."}
```

```quiz
{"id": "gt-rev-directed-finished", "q": "A directed walk reaches a neighbor that is already finished. What does it conclude?", "options": ["A cycle exists", "No cycle passes through that edge", "The graph is undirected", "The walk must restart"], "answer": 1, "explain": "A finished vertex has no route back to the active chain. Only an edge to an active vertex closes a directed cycle."}
```

```quiz
{"id": "gt-rev-clone-shared-vertex", "q": "A cloned graph has a vertex whose neighbor list holds an original vertex and not a copy. Which step caused it?", "options": ["The clone sorted the neighbor list", "The clone added a neighbor without looking up its copy in the map", "The clone used a queue", "The clone copied the label twice"], "answer": 1, "explain": "Every neighbor of a copy must be the copy of the original neighbor. The map from originals to copies supplies it, and a direct add leaves a pointer into the original graph."}
```

```quiz
{"id": "gt-rev-grid-walk-answer", "q": "A flood over a grid uses the same neighbors and the same marking rule for two tasks, counting islands and measuring the largest island. What differs between the two?", "options": ["The grid neighbors", "The moment of marking", "The value the walk returns for each start", "The number of directions"], "answer": 2, "explain": "The grid supplies the vertices and edges, and the marking rule keeps each cell scheduled once. Only the question asked of each walk changes, a count of starts or the size of one walk."}
```
