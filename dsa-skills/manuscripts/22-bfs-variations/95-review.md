<!-- section: review -->
## Review

Return here after the lessons and again after some days. The scenarios do not name the technique, so decide what the vertices are, what the first queue holds and what one round stands for before you read the options. These questions test prediction and recognition, which the guided exercises do not.

### Recognition Questions

```quiz
{"id": "bv-rev-one-queue", "q": "Eight fire stations spread help across a town grid, and each cell needs the distance to its nearest station. Which plan is both correct and cheapest?", "options": ["Run a separate search from each station and keep the minimum per cell.", "Put all stations in one queue at distance zero and run a single search.", "Search from every cell until a station is found, each time from scratch.", "Run a depth-first search from the first station."], "answer": 1, "explain": "With all sources in one queue, the first time a cell is reached is its nearest station. Separate searches repeat most of the work."}
```

```quiz
{"id": "bv-rev-time-per-node", "q": "A spread process is simulated with a queue, and the minute counter is raised once for every vertex taken from the queue. What is wrong?", "options": ["Nothing, a vertex is a minute.", "The queue should be a stack.", "Vertices that spread at the same time are counted as separate minutes.", "The counter should start at one."], "answer": 2, "explain": "A round holds every vertex that acts simultaneously, so the counter belongs to the whole round, taken from the queue size captured at its start."}
```

```quiz
{"id": "bv-rev-empty-frontier", "q": "A board has no fresh item, so nothing ever needs to spread. A student's loop adds one to the minute counter after each round, including a last round that creates nothing. What does the result show?", "options": ["Zero, as expected.", "One too many unless the counter counts only rounds that create something new.", "An infinite loop.", "Minus one."], "answer": 1, "explain": "A round that discovers nothing is not a minute of spread. The counter must count only productive rounds, and an initially complete state answers zero before any round runs."}
```

```quiz
{"id": "bv-rev-meeting-rule", "q": "Two searches expand toward each other on an unweighted graph. When is it safe to conclude the shortest length?", "options": ["When the two queue fronts are the same vertex.", "As soon as a generated neighbour already appears in the other side's table, combining both distances, and after finishing that whole layer's check.", "After one layer from each side.", "When both searches have the same size."], "answer": 1, "explain": "A crossing can happen on an edge between two vertices that are never at the two fronts together. The test belongs at neighbour generation, and the layer is completed before the best total is trusted."}
```

```quiz
{"id": "bv-rev-smaller-side", "q": "Why does a bidirectional search expand the smaller frontier?", "options": ["It keeps the two distances equal.", "It is required for correctness.", "A branching graph grows fast with depth, so growing the smaller side keeps the total number of states small.", "It avoids the need for visited marks."], "answer": 2, "explain": "Both sides remain correct whichever is expanded. Choosing the smaller one is a cost decision that limits how large the frontiers become."}
```

```quiz
{"id": "bv-rev-state-encoding", "q": "A courier walks a grid and may pick up a key that opens a door. The visited array is indexed only by position. What can go wrong?", "options": ["Nothing, a position is a vertex.", "A position reached once without the key blocks a later visit that holds the key.", "The queue overflows.", "Distances become negative."], "answer": 1, "explain": "The key changes which moves are legal, so position alone is not a complete state. The mark must cover position and key together."}
```

```quiz
{"id": "bv-rev-dead-start", "q": "A lock puzzle lists dead combinations. The starting combination is itself on that list. What should the search answer?", "options": ["Zero, since start equals start.", "The shortest path avoiding the start.", "Minus one, because the contract forbids standing on a dead state and the check happens before anything is queued.", "It depends on the target."], "answer": 2, "explain": "The dead-state rule applies to the start as well. Checking it before enqueueing keeps the contract from leaking into the search."}
```

```quiz
{"id": "bv-rev-dominance", "q": "A search tracks position and remaining breaks. When may a state at the same cell be discarded as dominated?", "options": ["When another state reached the cell earlier with fewer breaks left.", "When another state reached the cell with at least as many breaks left and no more moves used.", "Whenever the cell was seen before.", "Never, dominance does not exist."], "answer": 1, "explain": "A state with no more moves used and no fewer breaks left can do everything the other one can. A longer route that keeps more breaks may still be needed, so earlier arrival alone proves nothing."}
```

```quiz
{"id": "bv-rev-word-ladder-count", "q": "Counting the shortest ladders instead of measuring one needs which change to the plain layered search?", "options": ["Nothing, the first discovery already counts routes.", "A depth-first search with a global visited set.", "A larger queue.", "Remember every parent that reaches a state at the same layer, instead of only the first."], "answer": 3, "explain": "Equal-length routes enter a state from several parents in the same layer. Keeping only the first parent loses the others, so counts must add over all of them."}
```
