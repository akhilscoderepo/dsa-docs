<!-- section: orientation -->
## Orientation

A route planner reports that a city is unreachable, but a friend drives there every week. A photo editor recolors a patch that is not connected to the one the user clicked. A copy of a social network ends up with every user pointing back at the original accounts. A prerequisite checker accepts a course plan in which two courses wait for each other. Each program treats a set of connected things as a plain list, and each failure comes from forgetting which things were already seen. This chapter teaches how to store connections, walk them once, and answer questions about the walk.

### Prerequisites

You should know recursion, queues and hash maps. Chapter 15 taught depth-first search on trees, which lessons 02, 03, 04, 06 and 09 extend to graphs that can contain cycles. Chapter 16 taught breadth-first search by levels, which lessons 03, 05, 07 and 08 reuse. Chapter 19 taught recursion with undo, which lesson 06 needs. Chapter 04 taught `HashMap`, which lesson 02 uses for the identity map. Code samples assume `import java.util.*;` and a recent JDK.

### The Nine Lessons

Each lesson adds one piece of state to a graph walk.

- **Graph Representation** stores edges as adjacency lists or as a matrix and states the cost of each.
- **Graph Cloning** copies a cyclic graph with a map from each original vertex to its copy.
- **Visited State** marks each vertex once, and compares marking on entry with marking on removal from a queue.
- **Components** starts a walk from every unvisited vertex and counts the groups.
- **Grid Graphs** treats cells as vertices and the four moves as edges.
- **Path Enumeration** lists every route and removes the last vertex after each branch.
- **Unweighted Shortest Paths** uses a queue so the first discovery of a vertex is the shortest.
- **Bipartite Coloring** gives each vertex one of two colors so that the ends of every edge differ, and reports the first conflict.
- **Cycle Detection** separates the edge back to the parent from a real cycle, and a finished vertex from one that is still being visited.

### The Combination Lesson

One lesson joins two ideas from this chapter.

- **Walk A Grid As A Graph** joins the grid neighbors of lesson 05 with the map from original to copy of lesson 02, and changes the question asked of the walk in four ways.

### How To Work Through Each Lesson

A lesson opens with a program that fails on a realistic input. It then shows the first version and asks you to predict its result. The next parts name the rule, list the state, follow two traces, show the code and mark where the rule stops working. The exercises climb from a basic version to a pattern recognition problem, labeled Build, Vary, Boundary or Recognize. Read the hint only after a real attempt.

### What You Can Do After This Chapter

You can choose between a list and a matrix from the edge count. You can say at which moment a vertex is marked and why. You can count components, find a shortest route by edges, color a graph with two colors and detect a cycle in either kind of graph. You can list the edge cases before coding: no edges, isolated vertices, self-loops, repeated edges and a source that equals the target.

### What Later Chapters Reuse

Three ideas carry forward.

- **Mark a vertex when it is scheduled** returns in every search with a queue, including the variations of chapter 22.
- **Treat an implicit structure as a graph** returns whenever a state has legal moves, such as a word, a key set or a board.
- **Separate vertices being visited from finished ones** returns in the topological order of chapter 23.
