<!-- lesson-kind: standard -->
<!-- lesson-id: unweighted-shortest-paths -->
## Unweighted Shortest Paths

<!-- stage: context -->
### Night Shift On The Kestrel Line

The Kestrel Line is a small metro with seven stations, and each pair of neighbouring stations is joined by a single stretch of track. At two in the morning a cleaning crew is dropped at Ferndale, the depot station, and the duty manager has to get them to the station where a flooded stairwell was reported. Every ride between neighbouring stations costs the same, one stop, and walking between platforms costs nothing. The manager cares about one number only, the fewest stops the crew must ride.

The manager's wall map is a tangle of branching lines and a loop at the harbour end, so the shortest way is not obvious by eye. A route that looks natural, straight down the main line, may be twice as long as a branch that cuts across. The manager wants a procedure that, for Ferndale and any other station, reports the fewest stops, says so plainly when no route exists, and can then name the stations along one such route.

<!-- stage: naive -->
### Try Every Route And Keep The Best

The direct method tries every way to get there. Start at the depot and ride to each neighbouring station in turn. From each one keep riding, never revisiting a station already on the current route, until the goal is reached or the route has nowhere to go. Every complete route reports its stop count, and the answer is the smallest count seen.

```java
static int fewestStopsByDfs(List<List<Integer>> adj, int at, int goal, boolean[] onRoute) {
    if (at == goal) return 0;
    onRoute[at] = true;
    int best = Integer.MAX_VALUE;
    for (int next : adj.get(at)) {
        if (onRoute[next]) continue;
        int rest = fewestStopsByDfs(adj, next, goal, onRoute);
        if (rest != Integer.MAX_VALUE) best = Math.min(best, rest + 1);
    }
    onRoute[at] = false;
    return best;
}
```

This is correct for any map, because every simple route is tried and compared, and the station is released from the route on the way back so that other routes may use it. A result of `Integer.MAX_VALUE` means that no route reaches the goal.

<!-- stage: bottleneck -->
### The Routes Multiply Faster Than Stations

The number of simple routes is the problem. On a map where stations form layers, with every station in one layer joined to every station in the next, each added layer of width k multiplies the route count by k. Dense maps are worse, since a complete map of n stations has about (n - 1)! simple routes from one station to another, so the time is O(n!) in the worst case and is hopeless beyond about a dozen stations. Even a sparse map with a few loops can hold thousands of routes between two nearby stations.

The waste is plain. The method rediscovers the same station again and again by different roads, and it fully explores long detours that were already beaten by a shorter ride found elsewhere. A better method should reach each station once and be able to state, at that moment, that no cheaper ride to it can exist. That calls for a different order of exploring, not a cleverer way of pruning the old one.

<!-- stage: insight -->
### Rings Of Stations Around The Depot

Picture the stations in rings around the depot. The depot is ring 0, the stations one stop away form ring 1, those two stops away form ring 2, and so on. A queue explores these rings strictly in order, which is called **level order**: every station of ring k leaves the queue before any station of ring k + 1, and the stations of ring k + 1 are exactly the new ones that ring k's members can reach in one more ride.

That order has a strong consequence. The **first discovery** of a station is always by a station from the closest possible ring, so the moment a station is first marked it has its final answer, and nobody will ever improve it. The code can therefore write `dist[next] = dist[cur] + 1` at that single moment and never touch the entry again. A table filled this way doubles as the visited check, as long as unreached entries hold -1 and not 0, because 0 is the legal distance of the depot itself.

Remember who discovered each station, too. The **predecessor** array stores, at the instant of first discovery, the station that was being expanded. To name a route, start at the goal and follow predecessors back to the depot, then reverse what was collected. The route has exactly `dist[goal]` rides, since each predecessor sits one ring nearer the depot.

The invariant is that the queue always holds stations of at most two adjacent distances, in non-decreasing order, and every station has its final distance when it is first marked.

<!-- names: level order, first discovery, predecessor -->

<!-- stage: variables -->
### Distance Table And Parent Links

The integer `n` is the number of stations, numbered 0 to n - 1, and `adj` holds for each station the list of its neighbours. The station `source` is where the crew starts. The array `dist` has one entry per station, filled with -1 for unreached, and `parent` has one entry per station for the station that discovered it, also -1 at first. The queue `line` holds discovered stations whose neighbours have not yet been looked at, `cur` is the one just taken from it, and `next` is the neighbour being tried.

<!-- stage: trace -->
### Two Runs On The Kestrel Map

The first trace runs the search from station 0 on a map with seven stations and these tracks: 0-1, 1-2, 2-3, 3-4, 0-5, 5-4 and 5-6. The cells are the stations, the pointer `cur` is the station taken from the queue, and the vars show the distance table after that station is expanded, with a dash for unreached stations, and the queue contents. Notice that stations leave the queue in the order 0, 1, 5, 2, 4, 6, 3, and the distances along that order never fall. Station 4 gets distance 2 through the branch at 5, though the main line 0-1-2-3-4 would have made it 4.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":"0 1 - - - 1 -","queue":"1,5"},"note":"Station 0 is taken from the queue at distance 0, and it discovers 2 new stations (1,5) at distance 1."},{"at":{"cur":1},"vars":{"dist":"0 1 2 - - 1 -","queue":"5,2"},"note":"Station 1 is taken from the queue at distance 1, and it discovers 1 new station (2) at distance 2."},{"at":{"cur":5},"vars":{"dist":"0 1 2 - 2 1 2","queue":"2,4,6"},"note":"Station 5 is taken from the queue at distance 1, and it discovers 2 new stations (4,6) at distance 2."},{"at":{"cur":2},"vars":{"dist":"0 1 2 3 2 1 2","queue":"4,6,3"},"note":"Station 2 is taken from the queue at distance 2, and it discovers 1 new station (3) at distance 3."},{"at":{"cur":4},"vars":{"dist":"0 1 2 3 2 1 2","queue":"6,3"},"note":"Station 4 is taken from the queue at distance 2, and it discovers nothing new, since every neighbour already has a distance."},{"at":{"cur":6},"vars":{"dist":"0 1 2 3 2 1 2","queue":"3"},"note":"Station 6 is taken from the queue at distance 2, and it discovers nothing new, since every neighbour already has a distance."},{"at":{"cur":3},"vars":{"dist":"0 1 2 3 2 1 2","queue":"empty"},"note":"Station 3 is taken from the queue at distance 3, and it discovers nothing new, since every neighbour already has a distance."}]}
```

The second trace restores a route to station 3 on the same map, using the parent links the first run left behind. The pointer `v` walks from the goal back to the depot, and the vars show the route collected so far in walking order. The collected stations read 3, 2, 1, 0, so the route is that list reversed, and its length of 3 rides matches the distance table.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["v"],"steps":[{"at":{"v":3},"vars":{"route":"3"},"note":"Station 3 joins the route and its predecessor is 2, so the walk moves there."},{"at":{"v":2},"vars":{"route":"3,2"},"note":"Station 2 joins the route and its predecessor is 1, so the walk moves there."},{"at":{"v":1},"vars":{"route":"3,2,1"},"note":"Station 1 joins the route and its predecessor is 0, so the walk moves there."},{"at":{"v":0},"vars":{"route":"3,2,1,0"},"note":"Station 0 joins the route, and it has no predecessor, so it is the depot and the walk ends."}]}
```

<!-- stage: code -->
### Distances And Parents In One Pass

```java
final class Kestrel {
    static int[][] explore(List<List<Integer>> adj, int source) {
        int n = adj.size();
        int[] dist = new int[n];
        int[] parent = new int[n];
        Arrays.fill(dist, -1);
        Arrays.fill(parent, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        dist[source] = 0;
        line.add(source);
        while (!line.isEmpty()) {
            int cur = line.poll();
            for (int next : adj.get(cur)) {
                if (dist[next] != -1) continue;
                dist[next] = dist[cur] + 1;
                parent[next] = cur;
                line.add(next);
            }
        }
        return new int[][] {dist, parent};
    }

    static List<Integer> routeTo(int[] parent, int goal) {
        LinkedList<Integer> route = new LinkedList<>();
        for (int v = goal; v != -1; v = parent[v]) route.addFirst(v);
        return route;
    }
}
```

Time is O(V + E), because each station is queued once and each track is looked at from both ends, and space is O(V) for the two tables and the queue. The route builder is only meaningful for a goal that was reached, since an unreached goal has parent -1 and would come back as a route of one station.

<!-- stage: applicability -->
### When Equal Cost Means Count The Rides

Use this model when every move costs the same and the question asks for the fewest moves: stops on a transit map, hops in a relay of messengers, edits in a word ladder, turns of a sliding puzzle, steps of a robot on a grid with eight-way motion. The invariant to protect is the one about the queue, that stations leave in non-decreasing distance, since the whole claim that a first mark is final rests on it. Anything that breaks the order, such as pushing a station to the front of a deque or reusing the queue for two different sources at different times, breaks the answer silently.

The false friend is depth-first search. It will find a route first, and sometimes a very long one, and the first route it finds says nothing about being the shortest. On the Kestrel map above, a search that tries station 1 before station 5 reaches station 4 by the main line, four rides, when two were enough. Taking the minimum over all routes repairs the answer only at the cost of the factorial blow-up from before.

There is no use for this model when rides have different costs, for instance when a tunnel takes five minutes and a transfer takes one. A queue then no longer yields stations in order of true cost, and a weighted method is needed. In Java, `new int[n]` is filled with 0, and 0 is a real distance, so a table that is not first filled with -1 treats the depot as unreached and queues it a second time.

<!-- stage: exercises -->
### Exercises

#### [Build] Distance From One Source (Author exercise)
<!-- id: gt-distance-from-source -->

**Prerequisites.** The queue and the visited check from the earlier lessons of this chapter.

**Problem.** There are `n` vertices numbered 0 to n - 1 and an undirected graph given by `edges`, where each entry `[u, v]` is one edge. Return an `int[]` of length `n` whose entry v is the fewest edges on any path from `source` to v, or -1 when v cannot be reached. Entry `source` is 0.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 5000, no self-loops, and repeated edges are possible.

**Example 1.** Input `n = 7, edges = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,4],[5,6]], source = 0`, output `[0,1,2,3,2,1,2]`.

**Example 2.** Input `n = 4, edges = [[0,1],[2,3]], source = 2`, output `[-1,-1,0,1]`.

**Hint.** What value marks a vertex as unreached, and at which moment is a distance written?

**Changed decision.** The distance table replaces a separate visited array, and each entry is written once, when its vertex is first discovered.

#### [Vary] Restore One Shortest Path (Author exercise)
<!-- id: gt-restore-shortest-path -->

**Prerequisites.** The Distance From One Source rung.

**Problem.** The graph and its encoding are as in the previous rung. Return the vertices of one shortest path from `source` to `target`, in order, as an `int[]`, or an empty array when the target is unreachable. To make the answer unique, build every adjacency list in ascending vertex order, run the search with neighbours scanned in that order, record each vertex's predecessor at its first discovery, and return the path that the predecessors give.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 5000, no self-loops, and the adjacency lists are sorted ascending with repeated edges removed or harmless.

**Example 1.** Input `n = 7, edges = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,4],[5,6]], source = 0, target = 3`, output `[0,1,2,3]`.

**Example 2.** Input `n = 5, edges = [[0,1],[0,2],[1,3],[2,3],[3,4]], source = 0, target = 4`, output `[0,1,3,4]`.

**Hint.** In which direction do the predecessors lead, and what must be done to the collected list before it is returned?

**Changed decision.** Besides the distance, each discovery also records who made it, and the answer is rebuilt from the target by following those records backward.

#### [Boundary] Source Equals Target And Unreachable Target (Author exercise)
<!-- id: gt-source-target-edges -->

**Prerequisites.** The Restore One Shortest Path rung.

**Problem.** Given the same kind of undirected graph, return the fewest edges on a path from `source` to `target`. Return 0 when the two are the same vertex, even if that vertex has no edges, and return -1 when no path exists. The search should stop as soon as the target is discovered.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 5000, no self-loops, and vertices are numbered 0 to n - 1.

**Example 1.** Input `n = 7, edges = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,4],[5,6]], source = 2, target = 2`, output `0`.

**Example 2.** Input `n = 6, edges = [[0,1],[1,2],[0,3],[3,2],[4,5]], source = 0, target = 4`, output `-1`.

**Hint.** Is there a ride to make when the crew already stands at the goal, and what does an emptied queue tell you?

**Changed decision.** Two answers are decided before or after the loop, zero when the ends coincide and the failure value when the queue runs dry, instead of a distance read from the table.

#### [Recognize] Shortest Path In Binary Matrix (LeetCode 1091)
<!-- id: gt-binary-matrix-path -->

**Prerequisites.** The Grid Graphs lesson and the Distance From One Source rung.

**Problem.** The `grid` is an n by n `int[][]` of 0 (open) and 1 (blocked). A move goes to any of the eight surrounding cells, diagonals included, and only onto an open cell. Return the number of cells on the shortest path from the top-left cell to the bottom-right cell, counting both ends, or -1 when no path exists. If either end cell is blocked, the answer is -1.

**Constraints.** 1 <= n <= 100, and every entry is 0 or 1.

**Example 1.** Input `grid = [[0,0,1],[1,0,0],[1,1,0]]`, output `3`.

**Example 2.** Input `grid = [[0,1,0,0],[0,1,0,1],[0,0,1,0],[1,0,0,0]]`, output `5`.

**Hint.** Which cells does the answer count, and what must be checked about the two end cells before any queue is built?

**Changed decision.** The graph is implicit with eight direction deltas instead of four, and the distance counts cells, so the start cell has distance 1.
