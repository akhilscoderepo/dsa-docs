<!-- section: orientation -->
## Orientation

A delivery app quotes a route through three cities as the cheapest, yet a direct road costs less. A flight search returns a route with five stops after the traveler asked for at most one. A map program counts blocks and ignores that some roads are toll roads. Each program found a path and used the wrong idea of cost. This chapter teaches how a program finds the cheapest path when edges carry costs, and how to keep extra facts such as stops used or the last edge color.

### Prerequisites

You should know adjacency lists and breadth-first search from chapter 21, and the `PriorityQueue` from chapter 17. The deque from chapter 13 is needed in the last two lessons. Code samples assume `import java.util.*;` and a recent JDK.

### The Six Lessons

Each lesson adds one idea to a shortest-path search.

- **Find Cheapest Routes With Dijkstra** keeps a best known cost per vertex and always expands the cheapest unfinished vertex.
- **Skip Outdated Heap Entries** lets a vertex sit in the heap several times and ignores every entry that no longer matches its best cost.
- **Search Over Place And State** indexes the best cost by the pair of vertex and extra fact.
- **Limit A Route By Stops** counts the edges used, so a costlier route with fewer stops stays alive.
- **Alternate Edge Colors** stores the color of the last edge and allows only the opposite color next.
- **Search With Zero And One Costs** replaces the heap with a deque when every edge costs 0 or 1.

### The Combination Lessons

- **Shortest Paths With A Heap** joins the first four lessons into one heap search with several path scores.
- **Shortest Paths With A Deque** joins the zero-one search with grid problems whose cost comes from the cell contents.

### How To Work Through Each Lesson

A lesson opens with a program that returns a wrong answer on a realistic input. It then shows a first version and asks you to predict its result. The next parts name the rule, list the state, follow two traces, show the code and mark where the rule stops working. The exercises climb through Build, Vary, Boundary and Recognize. Read a hint only after a real attempt.

### What You Can Do After This Chapter

You can find the cheapest route when every edge cost is nonnegative, and you can say why a negative edge breaks the method. You can extend the state of a search with stops, colors or coupons. You can pick a queue, a heap or a deque from the set of edge costs.

### What Later Chapters Reuse

Chapter 25 continues with harder graph optimization and reuses the heap search. Chapter 26 treats a table of best values by state as a dynamic programming table.
