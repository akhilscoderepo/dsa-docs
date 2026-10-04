<!-- section: orientation -->
## Orientation

Two questions about links keep returning in different clothes. The first asks for an order that respects dependencies, so that everything a task needs is done before the task itself. The second asks which things belong together once links have been laid one after another. The first lives on directed graphs and is answered by removing tasks whose prerequisites are finished, or by finishing a walk and reading it backwards. The second is answered by giving every group a single representative that can be found quickly, which is the disjoint-set structure. The chapter develops both, and ends with a spanning-tree method that needs the second to run at all.

### What To Bring

You need the queue and the mark from Chapter 21, the three-colour walk from the cycle lesson there, and the habit of writing down the contract of an input. Sorting with a comparator from Chapter 05 is used once, for ordering edges by cost. Arrays that mirror each other, such as a parent array and a size array, appear throughout, and they must be kept in step.

### The Eight Lessons

The first lesson orders tasks by counting unresolved prerequisites and removing those at zero. The second reaches the same goal by finishing a walk and reading the finishing order backwards, with three colours that say what an edge may mean. The third returns to undirected graphs and asks when a visited neighbour really closes a loop, and when a graph is a tree. The fourth introduces the representative and the search for it, together with the rewriting of a searched path. The fifth keeps the trees shallow by choosing which root goes under which. The sixth uses the structure online, answering questions between merges. The seventh builds a cheapest spanning tree by accepting edges in cost order. The eighth is the released combination, where graph edges are events and every component has one representative.

### How To Work Through A Lesson

Read the scene and guess what the slow method repeats. Before an insight, name what the structure must remember between steps. In each trace, say what every array holds at that moment. For an exercise, settle three questions first: which way does an edge point, may an edge repeat or loop onto its own vertex, and may the input be changed. Each solution file checks the fast method against an independent slow one on random inputs, and the traps in the lessons are asserted, not merely described.

### Leaving The Chapter

You should be able to explain what an indegree counter stands for, why only a grey neighbour proves a directed loop, what the parent check hides in an undirected graph, why a representative changes nothing about membership, why the smaller root goes under the larger one, and why Kruskal's accepted edges are safe. The review section poses these as short scenarios.
