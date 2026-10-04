<!-- lesson-kind: standard -->
<!-- lesson-id: multi-source-bfs -->
## Multi-Source BFS

<!-- stage: context -->
### Fire Stations In Pellam Ridge

Pellam Ridge is a hill town of crooked lanes, and the volunteer brigade keeps a fire engine in four different places: the old mill, the school gate, the quarry road and the chapel. Dispatcher Ines Okafor has a wall map of the town with every lane junction numbered and every lane drawn between two junctions. When a call comes in she needs one number at once, the count of lane segments between the caller's junction and the closest engine, so that she can tell the family how long to wait.

Until now she has counted by eye, and on a bad night she miscounts. The council has asked for a printed table with one row per junction and the distance to its closest station. Junctions that no lane connects to any station must be marked so that nobody trusts them. The table has to be produced for any map and any set of stations, in a form that a small program can follow.

<!-- stage: naive -->
### One Search Per Station

The direct plan treats each station as its own problem. Stand at the mill, count outward lane by lane with an ordinary queue, and write down the distance to every junction. Do the same from the school gate, then the quarry road, then the chapel. For each junction, the answer is the smallest of the four numbers written for it.

```java
static int[] bestOfSeparateRuns(int[][] adj, int[] stations) {
    int n = adj.length;
    int[] best = new int[n];
    Arrays.fill(best, -1);
    for (int station : stations) {
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        dist[station] = 0;
        queue.add(station);
        while (!queue.isEmpty()) {
            int v = queue.poll();
            for (int w : adj[v]) {
                if (dist[w] != -1) continue;
                dist[w] = dist[v] + 1;
                queue.add(w);
            }
        }
        for (int v = 0; v < n; v++) {
            if (dist[v] != -1 && (best[v] == -1 || dist[v] < best[v])) best[v] = dist[v];
        }
    }
    return best;
}
```

Every run is a plain breadth-first count, so each run is right about its own station, and taking the minimum over all runs is right about the closest one. A junction that no run reaches keeps the value -1, and the input arrays are only read.

<!-- stage: bottleneck -->
### Every Run Repeats Most Of The Map

One run costs O(V + E) for V junctions and E lanes, since it may touch every junction and every lane. With S stations the plan costs O(S * (V + E)), plus O(S * V) more for folding the tables together. For Pellam Ridge that is four passes and nobody notices. A county with ten thousand junctions and a station on every second one is five thousand passes over ten thousand junctions each, around fifty million junction visits to answer a question about ten thousand junctions.

Worse, the runs mostly redo each other. A junction beside the chapel is also reached by the mill run, the school run and the quarry run, and three of those three visits are thrown away when the minimum is taken. Only the closest station could ever matter for a junction, yet the plan computes every distance from every station and discards the losers. A better method should let the stations compete during the search, so that each junction is settled once by whichever station gets there first.

<!-- stage: insight -->
### All Stations Start The Count Together

Put every station into one queue before anything is dequeued. That queue is the **shared frontier**: it holds the junctions whose neighbors still have to be examined, and it does not care which station each junction came from. The stations form the **starting layer**, all at distance 0. Ordinary breadth-first search then proceeds exactly as before, giving each newly found junction the distance of the entry that found it, plus one.

Why does that give the right table? A queue releases junctions in non-decreasing distance order, so the first time any station's wave touches a junction, no other station can be closer, because a closer one would have touched it earlier. That first touch is the **nearest-source distance**. Marking happens at that moment, which means a junction is never enqueued twice and every later arrival from a different station is simply refused. One pass of cost O(V + E) replaces S passes.

In Java the marking array doubles as the distance table. Fill it with -1 for unreached, because a fresh `int[]` is full of zeros and 0 is a real distance. When the station list is built carelessly it may name the same junction twice, so a station must also be checked against the table before it joins the queue.

The invariant is that every queued junction already holds its final distance, and the queue's distances never decrease from front to back.

<!-- names: shared frontier, starting layer, nearest-source distance -->

<!-- stage: variables -->
### Adjacency, Stations And Distances

The array `adj` holds, for each junction number, the junctions joined to it by one lane, and `stations` lists the junctions that hold an engine. The array `dist` has one slot per junction: -1 means not reached yet, and any other value is the final lane count to the closest station. The queue `frontier` holds junction numbers, `v` is the one just removed, and `w` is a neighbor being tried. No separate visited array is needed, since `dist[w] != -1` already says seen.

<!-- stage: trace -->
### Two Stations Then A Walled Grid

The first trace uses a map of eight junctions, labelled by their numbers, with stations at junctions 0 and 5. The pointer `cur` is the junction just removed from the queue, and the vars show its distance and the queue after its neighbors were added. Both stations sit in the queue before the first step, so the stations are processed first and the junctions between them are settled by whichever side arrives first. Junction 3 is three lanes from station 0 and two from station 5, and it receives the smaller number without ever being compared.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":0,"queue":"5,1"},"note":"Junction 0 is removed at distance 0, and it adds 1 junction (1) at distance 1."},{"at":{"cur":5},"vars":{"dist":0,"queue":"1,4,7"},"note":"Junction 5 is removed at distance 0, and it adds 2 junctions (4,7) at distance 1."},{"at":{"cur":1},"vars":{"dist":1,"queue":"4,7,2,6"},"note":"Junction 1 is removed at distance 1, and it adds 2 junctions (2,6) at distance 2."},{"at":{"cur":4},"vars":{"dist":1,"queue":"7,2,6,3"},"note":"Junction 4 is removed at distance 1, and it adds 1 junction (3) at distance 2."},{"at":{"cur":7},"vars":{"dist":1,"queue":"2,6,3"},"note":"Junction 7 is removed at distance 1, and it adds nothing, because every neighbor already has a distance."},{"at":{"cur":2},"vars":{"dist":2,"queue":"6,3"},"note":"Junction 2 is removed at distance 2, and it adds nothing, because every neighbor already has a distance."},{"at":{"cur":6},"vars":{"dist":2,"queue":"3"},"note":"Junction 6 is removed at distance 2, and it adds nothing, because every neighbor already has a distance."},{"at":{"cur":3},"vars":{"dist":2,"queue":"empty"},"note":"Junction 3 is removed at distance 2, and it adds nothing, because every neighbor already has a distance."}]}
```

The second trace is a flat grid of three rows and four columns, where `S` is a station, `.` is an open square and `#` is a wall, so the pointer `cur` is a flat index and square (1, 1) is index 5. Walls are never entered. The vars show the distance of the removed square and the largest distance given out so far, which is the time until the last open square is reached. The last step is notable: after the final square is removed there is nothing left to enqueue, and the time stays at the largest label instead of growing by one for the empty round.

```trace
{"cells":["S",".","#",".",".","#",".",".",".",".","S","#"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":0,"max_dist":0,"queue":"10,4,1"},"note":"Square 0 at row 0, column 0 is removed at distance 0, and it adds 2 squares (4,1)."},{"at":{"cur":10},"vars":{"dist":0,"max_dist":0,"queue":"4,1,6,9"},"note":"Square 10 at row 2, column 2 is removed at distance 0, and it adds 2 squares (6,9)."},{"at":{"cur":4},"vars":{"dist":1,"max_dist":1,"queue":"1,6,9,8"},"note":"Square 4 at row 1, column 0 is removed at distance 1, and it adds 1 square (8)."},{"at":{"cur":1},"vars":{"dist":1,"max_dist":1,"queue":"6,9,8"},"note":"Square 1 at row 0, column 1 is removed at distance 1, and it adds nothing, so no later round begins from here."},{"at":{"cur":6},"vars":{"dist":1,"max_dist":1,"queue":"9,8,7"},"note":"Square 6 at row 1, column 2 is removed at distance 1, and it adds 1 square (7)."},{"at":{"cur":9},"vars":{"dist":1,"max_dist":1,"queue":"8,7"},"note":"Square 9 at row 2, column 1 is removed at distance 1, and it adds nothing, so no later round begins from here."},{"at":{"cur":8},"vars":{"dist":2,"max_dist":2,"queue":"7"},"note":"Square 8 at row 2, column 0 is removed at distance 2, and it adds nothing, so no later round begins from here."},{"at":{"cur":7},"vars":{"dist":2,"max_dist":2,"queue":"3"},"note":"Square 7 at row 1, column 3 is removed at distance 2, and it adds 1 square (3)."},{"at":{"cur":3},"vars":{"dist":3,"max_dist":3,"queue":"empty"},"note":"Square 3 at row 0, column 3 is removed at distance 3, and it adds nothing, so no later round begins from here."}]}
```

<!-- stage: code -->
### Seeding The Queue With Every Station

```java
final class Depots {
    static int[] nearestStation(int[][] adj, int[] stations) {
        int[] dist = new int[adj.length];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        for (int s : stations) {
            if (dist[s] != -1) continue;
            dist[s] = 0;
            frontier.add(s);
        }
        while (!frontier.isEmpty()) {
            int v = frontier.poll();
            for (int w : adj[v]) {
                if (dist[w] != -1) continue;
                dist[w] = dist[v] + 1;
                frontier.add(w);
            }
        }
        return dist;
    }
}
```

The seeding loop is the only new line of thought compared with a single search. Time is O(V + E + S), because each junction is queued once, each lane is read twice and each station is looked at once. Space is O(V) for the table and the queue.

<!-- stage: applicability -->
### Waves From Many Places At Once

Look for this shape whenever several starting points act together and the question is how far each place is from its closest start, or how long until everything is covered: engines and hydrants, wifi routers and rooms, infection spreading from several carriers, or fire creeping from several ignition points through a grid. The invariant to defend is that all starting points sit at distance zero in one queue before the first removal, so the first arrival at any cell is also the closest one.

The nearest false friend is running a separate search from every start and taking minimums. It returns the right numbers, which makes it tempting, but it repeats most of the work S times over. A second false friend is counting minutes by the number of rounds executed: if the last round discovers nothing, the count is one too large, and with no unreached cells at all it reports 1 instead of 0.

Do not use the shared queue when the starts are not equal. If one station begins after a delay, or lanes have different lengths, the queue no longer releases junctions in distance order, and a weighted method is needed instead. In Java, remember that a new `int[]` holds zeros, so a distance table that is never filled with a sentinel treats every unreached junction as sitting at a station.

<!-- stage: exercises -->
### Exercises

#### [Build] Nearest Source Distances (Author exercise)
<!-- id: bv-nearest-source-distances -->

**Prerequisites.** The distance table with -1 for unreached, and the seeding loop from this lesson.

**Problem.** There are `n` vertices numbered 0 to n - 1 and an undirected graph given as the edge list `edges`, where each entry `[a, b]` joins two vertices. The array `sources` names the marked vertices. Return an array `dist` where `dist[v]` is the smallest number of edges on a path from `v` to any marked vertex, or -1 if no marked vertex can be reached from `v`. The inputs are not modified.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 5000, 1 <= sources.length <= n, the entries of `sources` are distinct, and the graph has no self loops.

**Example 1.** Input `n = 7, edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6]], sources = [0,6]`, output `[0,1,2,3,2,1,0]`.

**Example 2.** Input `n = 6, edges = [[0,1],[1,2],[3,4]], sources = [2]`, output `[2,1,0,-1,-1,-1]`.

**Hint.** What must already be in the queue before the first vertex is removed, and what value says a vertex has not been reached?

**Changed decision.** Instead of starting one search from a single vertex, the queue starts with every marked vertex at distance 0.

#### [Vary] 01 Matrix (LeetCode 542)
<!-- id: bv-zero-one-matrix -->

**Prerequisites.** The Build rung, and the direction deltas of a grid.

**Problem.** The `mat` is a rectangular `int[][]` holding only 0 and 1. Return a matrix of the same shape in which each cell holds the number of up, down, left or right steps to the nearest cell containing 0. A new matrix is returned and `mat` is not modified.

**Constraints.** 1 <= rows, cols <= 50, every entry is 0 or 1, and at least one entry is 0.

**Example 1.** Input `mat = [[0,0,0],[0,1,0],[1,1,1]]`, output `[[0,0,0],[0,1,0],[1,2,1]]`.

**Example 2.** Input `mat = [[1,1,1],[1,1,1],[1,1,0]]`, output `[[4,3,2],[3,2,1],[2,1,0]]`.

**Hint.** Which cells are the sources here, and which cells should the search spend its effort on?

**Changed decision.** The sources are discovered by scanning the grid for zeros, and every cell, not only the open ones, receives a distance.

#### [Boundary] No Source Or All Sources (Author exercise)
<!-- id: bv-no-or-all-sources -->

**Prerequisites.** The Build rung.

**Problem.** The graph is given as in the Build exercise, but the question is a time. Starting with only the vertices in `sources` marked, each minute every unmarked vertex that shares an edge with a marked vertex becomes marked. Return the number of minutes until every vertex is marked, or -1 if that never happens. The list `sources` may be empty, and it may name the same vertex more than once. When every vertex is marked at the start, the answer is 0.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 5000, 0 <= sources.length <= 3000, and the graph has no self loops.

**Example 1.** Input `n = 3, edges = [[0,1],[1,2]], sources = [2,0,1,1]`, output `0`.

**Example 2.** Input `n = 2, edges = [[0,1]], sources = []`, output `-1`.

**Hint.** If the answer is the largest label ever assigned, what does an empty source list leave unlabelled, and what would a loop that counts rounds report when nothing is ever discovered?

**Changed decision.** The answer is the largest distance given out, with a separate count of marked vertices deciding between that value and -1, instead of a list of distances.

#### [Recognize] Rotting Oranges (LeetCode 994)
<!-- id: bv-rotting-oranges -->

**Prerequisites.** The Vary rung and the Boundary rung.

**Problem.** The `grid` is a rectangular `int[][]` in which 0 is an empty cell, 1 is a fresh orange and 2 is a rotten orange. Every minute, each fresh orange that has a rotten orange directly above, below, left or right becomes rotten. Return the number of minutes that must pass until no fresh orange is left, or -1 if some fresh orange can never rot. The grid is not modified.

**Constraints.** 1 <= rows, cols <= 10, and every entry is 0, 1 or 2. The grid may hold no fresh oranges.

**Example 1.** Input `grid = [[2,1,1],[1,1,0],[0,1,1]]`, output `4`.

**Example 2.** Input `grid = [[2,1,0,1],[1,1,0,1]]`, output `-1`.

**Hint.** Which cells start in the queue, what does one batch of the queue stand for, and how can you tell afterwards whether a fresh orange was missed?

**Changed decision.** One layer of the queue is one minute, and the final answer is the number of layers that rotted at least one orange, with a fresh-orange counter to detect the unreachable case.
