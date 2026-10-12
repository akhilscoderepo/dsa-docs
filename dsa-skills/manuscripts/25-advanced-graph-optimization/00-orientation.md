<!-- section: orientation -->
## Orientation

A payments system routes a refund through three accounts, and one transfer carries a credit instead of a fee. The route finder from the last chapter then reports a price that a cheaper route beats. A network team buys a cable plan that follows the shortest routes from one office and pays more than a cheaper plan. A support tool deletes one link at a time to find out which links matter, and it needs an hour per map. Each tool applied a correct method to the wrong question. This chapter teaches the methods for questions that shortest paths from one source cannot answer, and it teaches how to tell the questions apart.

### Prerequisites

You should know adjacency lists and depth-first search from chapter 21. You should know directed graphs and union-find from chapter 23, and the heap loop for shortest paths from chapter 24. The `PriorityQueue` comes from chapter 17. Code samples assume `import java.util.*;` and a recent JDK.

### The Eight Lessons

Each lesson keeps one fact true while a loop runs.

- **Find Shortest Paths With Negative Edges** repeats passes over all edges, and after pass `i` the distances cover routes of at most `i` edges.
- **Find All Distances With Floyd Warshall** fills a table of every pair by admitting one more intermediate vertex per round.
- **Grow A Spanning Tree With Prim** adds the cheapest edge that leaves the tree built so far.
- **Build A Spanning Tree With Kruskal** adds sorted edges whose ends lie in different union-find groups.
- **Walk Every Edge Once With Hierholzer** consumes edges and writes a vertex when no unused edge leaves it.
- **Find Strongly Connected Components** groups directed vertices that reach each other, using finish order and the reversed graph.
- **Find Bridges With Low Links** compares discovery times to find edges that disconnect an undirected graph.
- **Choose Edges For A Minimum Spanning Tree** explains why the cheapest edge across a cut is safe, and separates spanning trees from shortest paths.

### The Combination Lesson

- **Choose A Method For Each Graph Goal** reads the goal of a statement first, and then picks the spanning tree, low link, distance table or trail method that matches it.

### How To Work Through Each Lesson

A lesson opens with a program that gives a wrong or slow answer on a realistic input. It then shows a first version and asks you to predict its result. The next parts name the rule, list the variables, follow two traces, show the code and say when the rule stops fitting. Four exercises close each lesson, and they climb through Build, Vary, Boundary and Recognize. Read a hint only after a real attempt.

### What You Can Do After This Chapter

You can compute distances when an edge is negative, and you can say when a negative cycle makes the answer undefined. You can build a minimum spanning tree with either of two methods and say which one fits a given input. You can list the bridges of a network, group a directed graph into components, and print a trail that uses every edge once.

### What Later Chapters Reuse

Chapter 26 starts dynamic programming and reuses the idea of a table whose entries are final after an ordered sequence of rounds, which the distance table shows first. The union-find structure and the heap return in later design chapters. Flow and matching problems are not part of this chapter.
