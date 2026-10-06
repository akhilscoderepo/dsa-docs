<!-- section: orientation -->
## Orientation

A build system reports that all packages can be built, yet one package waits on itself through three others. A course planner prints an order that places a course before its prerequisite. A network tool counts four clusters when the machines form two. A social app asks "are these two users in one group?" and reruns a full traversal for every question. Each program uses a graph correctly and still fails, because it ignores one rule: a directed edge has an order, and a merged group needs one stored name. This chapter teaches those two rules and the spanning tree that follows from them.

### Prerequisites

You should know adjacency lists and the depth-first and breadth-first traversals of chapter 21, including a visited array and the queue. Sorting with a comparator comes from chapter 05, and heaps are not needed. Code samples assume `import java.util.*;` and a recent JDK.

### The Seven Lessons

Each lesson adds one piece of state to a graph algorithm.

- **Kahn Topological Order** keeps an indegree count per vertex and a queue of vertices with count zero.
- **DFS Topological State** marks each vertex unvisited, active or complete, and treats an edge to an active vertex as a cycle.
- **Undirected Parent State** remembers the vertex a call came from, so the same edge does not count as a cycle.
- **Find Compression** follows parent links to a root and rewrites the links it walked.
- **Union By Size** hangs the smaller tree under the larger root and updates the size at the surviving root.
- **Dynamic Connectivity** answers same-group questions while unions arrive one at a time.
- **Kruskal Foundations** sorts edges by weight and accepts an edge only when it joins two different groups.

### The Combination Lesson

- **Merge Groups As Edges Arrive** uses edges as merge events and shows how each of the earlier lessons contributes to one group-merging state.

### How To Work Through Each Lesson

A lesson opens with a program that fails on a realistic input. It then shows a first version and asks you to predict what that version does. The next parts name the rule, list the state, follow two traces, show the code and mark where the rule stops working. The exercises climb through Build, Vary, Boundary and Recognize. Read a hint only after a real attempt.

### What You Can Do After This Chapter

You can order tasks by prerequisites and say when no order exists. You can tell a directed cycle from an undirected one and say why the checks differ. You can keep groups in a parent array, merge them in near constant time and read the group count. You can build a minimum spanning tree and report when the graph is disconnected.

### What Later Chapters Reuse

Chapter 24 adds edge weights to shortest paths and contrasts them with the spanning tree built here. The parent array and the size update return whenever a later chapter merges groups.
