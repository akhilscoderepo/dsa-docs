<!-- section: orientation -->
## Orientation

A graph is the shape of any problem whose pieces are linked in arbitrary ways: roads between towns, keys that open rooms, prerequisites between courses, tiles that touch. This chapter teaches how to write such a problem down, how to walk it without going in circles, and which questions a single walk can answer. Reachability, the number of separate groups, a shortest hop count, a two-way split and the presence of a loop all come from the same few moves, and each lesson isolates one of them.

### What To Bring

Arrays, lists and the queue and stack of Chapter 11 are assumed, as is recursion over a tree from Chapter 15, where the shape could never loop back on itself. Grids come from Chapter 02 and the hash map of Chapter 04 appears as an identity table in the cloning lesson. Union-find, weighted paths and multi-source search are not assumed because later chapters own them.

### The Ten Lessons

The first lesson files the edges into piles and weighs a list against a table. The second copies a tangle of linked objects without merging look-alikes. The third introduces the visited mark and the exact moment at which it must be set. The fourth counts separate groups with an outer loop, and the fifth lets the cells of a board stand in for vertices. The sixth lists every route in a graph that has no loops, the seventh finds the fewest hops, the eighth splits vertices into two sides, and the ninth tells a harmless second look at a vertex from a genuine loop. The tenth is the released combination of boards and graphs, where one visited array and one scan serve both worlds.

### How To Work Through A Lesson

Start each lesson by reading the scene and predicting what a patient clerk would do slowly. Before an insight, name the work that is done twice. In a trace, say aloud what each mark means and why a vertex is allowed to enter the frontier only once. Before writing code for an exercise, settle three contract questions: are the links one-way, may a link repeat or return to its own start, and is the input allowed to change. Each solution file runs the fast method against a slow oracle on random graphs, so a disagreement is a signal to trace by hand.

### Leaving The Chapter

You should be able to choose a list or a table and defend it, say when a mark belongs on entry and when on removal from a queue, and explain why one start vertex is not enough on a scattered graph. You should also be able to say why a shared mark breaks route listing, why a queue gives fewest hops and a stack does not, what fails when only one group is two-coloured, and which mark states a directed loop needs. The review section poses these as scenarios.
