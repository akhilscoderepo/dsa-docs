<!-- section: review -->
## Review

Come back to this section after the lessons and again after some days. The scenarios avoid naming the technique, so decide first what a vertex stands for, what the structure remembers and which way things point, then read the options. These questions test prediction and recognition, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "ug-rev-sorting-labels", "q": "Tasks are labelled 0 to 9 and arrows say which task must come before which. A student sorts the labels and calls it a schedule. What is the flaw?", "options": ["Sorting is too slow.", "Arrows may point from a larger label to a smaller one, so label order can break a dependency.", "Labels cannot be sorted.", "Nothing, ascending order always works."], "answer": 1, "explain": "An arrow from 7 to 2 demands 7 before 2, which ascending order violates. The order must be derived from the arrows."}
```

```quiz
{"id": "ug-rev-leftover-vertices", "q": "A zero-indegree removal process stops with some vertices never removed. What does that prove?", "options": ["The input has an isolated vertex.", "Those vertices lie on or behind a directed cycle, so no valid order exists.", "The queue was too small.", "The graph is disconnected."], "answer": 1, "explain": "A vertex on a cycle always keeps an unresolved prerequisite from the cycle itself, so its indegree never reaches zero."}
```

```quiz
{"id": "ug-rev-grey-edge", "q": "In a directed walk, an arrow leads to a vertex whose colour is black. What does it mean?", "options": ["A cycle exists.", "The walk must restart.", "The target is complete and cannot lead back to an open vertex, so there is no loop through this arrow.", "The graph is undirected."], "answer": 2, "explain": "Only an arrow to a grey vertex returns to something still open. Black means finished, and a finished vertex has no open route above it."}
```

```quiz
{"id": "ug-rev-postorder", "q": "Which list gives a valid dependency order when the directed graph has no cycle?", "options": ["Vertices in the order they are first entered.", "Vertices sorted by out-degree.", "The finishing order of a depth-first walk, reversed.", "Vertices in label order."], "answer": 2, "explain": "A vertex finishes only after everything it points to has finished, so in the reversed finishing order every vertex comes before its targets."}
```

```quiz
{"id": "ug-rev-tree-check", "q": "A graph on n vertices has exactly n - 1 edges. Is it necessarily a tree?", "options": ["Yes.", "No, it might be disconnected with a cycle somewhere, so connectivity or acyclicity must still be checked.", "Only if n is even.", "Only if it is directed."], "answer": 1, "explain": "A cycle in one part can be paid for by a missing connection in another. The count is a necessary condition, not a sufficient one."}
```

```quiz
{"id": "ug-rev-path-compression", "q": "After a find call rewrites every visited vertex to point at the root, what has changed about group membership?", "options": ["Nothing, only the shape of the paths changed.", "The smaller group joined the larger.", "The root is now a different vertex.", "Members of the group were removed."], "answer": 0, "explain": "Compression leaves the root and the membership alone. It only shortens future searches."}
```

```quiz
{"id": "ug-rev-size-update", "q": "Two groups with roots a and b are merged and b's root ends up under a's. Where is the size updated?", "options": ["At b, the vertex that moved.", "At every member of the merged group.", "At a, the surviving root, and nowhere else.", "In neither, sizes are never stored."], "answer": 2, "explain": "Only the root's size is ever read, so only the surviving root receives the added count."}
```

```quiz
{"id": "ug-rev-redundant", "q": "While edges are merged one by one, an edge arrives whose endpoints already have the same representative. What is it?", "options": ["A bridge between two groups.", "A redundant edge, which closes a cycle in the graph read so far.", "A new group.", "A mistake in the input."], "answer": 1, "explain": "The endpoints were already connected, so this edge adds a second route between them."}
```

```quiz
{"id": "ug-rev-online-queries", "q": "Links are added and connectivity questions are asked in alternation, thousands of times. Which approach scales?", "options": ["Rerun a depth-first search from scratch for every question.", "Keep a disjoint-set structure and compare representatives.", "Rebuild an adjacency matrix after every link.", "Sort the links after every question."], "answer": 1, "explain": "A fresh walk costs a pass over every link each time, while the structure answers in nearly constant time after each merge."}
```

```quiz
{"id": "ug-rev-kruskal-safe", "q": "Why may Kruskal accept the cheapest edge that joins two different groups?", "options": ["Because the group count is small.", "Because no cheaper edge can leave that cut, so some cheapest spanning tree contains it.", "Because sorting makes every edge safe.", "Because a cycle is impossible after sorting."], "answer": 1, "explain": "The edge is the cheapest across the cut separating its group from the rest, which is exactly the situation in which including it never hurts."}
```
