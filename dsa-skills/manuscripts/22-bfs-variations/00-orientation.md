<!-- section: orientation -->
## Orientation

Ordinary breadth-first search starts from one vertex and spreads outward one step at a time. Many real questions bend that picture a little: the spreading begins in several places at once, the answer is a count of rounds rather than a distance, the search is launched from both ends, the vertices are not written down anywhere, or each vertex carries something the traveller spends along the way. This chapter takes each bend in turn and keeps the same engine underneath, a queue, a mark and a careful idea of what one round means.

### What To Bring

You need the queue discipline and the mark-on-entry rule from Chapter 21, and the habit of writing a contract for an input before coding. Grids are used again as implicit graphs, and strings appear as states. Nothing here uses weights, so a cheapest route that depends on edge costs is outside the chapter.

### The Six Lessons

The first lesson puts every source into the queue before the first round and shows why one search per source repeats work. The second asks what a round stands for and why time must advance once per whole round and never once per vertex. The third searches from both ends and settles when the two searches may be declared joined. The fourth builds vertices out of strings and moves, so that the state has to carry every fact that decides future moves. The fifth adds a spendable budget and examines when one state may be thrown away in favour of another. The sixth is the released combination, where several starts, rounds as time and a compound state meet in four re-asked problems.

### How To Work Through A Lesson

Read the scene, then guess what the slow method repeats. In every trace, say what a round holds and what is in the queue at the moment the round is closed. For an exercise, write down first what a vertex is, what makes two vertices the same, and what the round counter counts. Each solution file races the fast search against an independent oracle on small random inputs, so a mismatch deserves a hand trace.

### Leaving The Chapter

You should be able to say why all sources share one queue, when a counter may be incremented, how two searches decide that they have met, how to choose a state encoding, and what must be proved before a state is dropped as dominated. The review section gives these as short scenarios.
