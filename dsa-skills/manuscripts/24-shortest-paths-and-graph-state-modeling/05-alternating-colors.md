<!-- lesson-kind: standard -->
<!-- lesson-id: alternating-colors -->
## Alternate Edge Colors

<!-- stage: context -->
### Routes That Must Switch Link Types

#### A Search That Misses A Route

A routing tool for a company network has two kinds of links, and policy says that a packet may never use two links of the same kind in a row. The tool must report the fewest links from the gateway to each machine under that rule. A plain breadth-first search reports no route to machine 2, although a legal route with two links exists. Operators then open a ticket for a healthy machine. The search is correct for ordinary graphs, so the fault lies in what it remembers.

#### Task And Question

Model the machines as nodes `0` to `n - 1` and each link as a directed edge. Every edge is red or blue, and the input may contain parallel edges and self loops. A walk is a sequence of edges in which each edge starts where the previous one ends, and it alternates when no two neighbors in the sequence share a color. The task is to return, for each node, the number of edges in the shortest alternating walk from node 0, or -1 when none exists. An earlier lesson in this chapter introduced Dijkstra's method for weighted edges. Here every edge costs 1, so a queue is enough, but the rule about colors changes what the search must store.

This lesson asks what a breadth-first search has to remember about a node when the next legal edge depends on how the search arrived.

<!-- stage: naive -->
### Marking Each Node As Visited

The first attempt is the usual breadth-first search. A `boolean[]` marks each node on its first arrival. The queue stores the node together with the color of its arriving edge. The next edge must differ from that color.

```java
static int[] visitedPerNode(int n, int[][] red, int[][] blue) {
    int[] dist = new int[n];
    Arrays.fill(dist, -1);
    boolean[] seen = new boolean[n];
    ArrayDeque<int[]> queue = new ArrayDeque<>();
    seen[0] = true;
    dist[0] = 0;
    queue.add(new int[] {0, -1});
    while (!queue.isEmpty()) {
        int[] cur = queue.poll();
        for (int color = 0; color < 2; color++) {
            if (color == cur[1]) continue;
            for (int[] e : color == 0 ? red : blue) {
                if (e[0] == cur[0] && !seen[e[1]]) {
                    seen[e[1]] = true;
                    dist[e[1]] = dist[cur[0]] + 1;
                    queue.add(new int[] {e[1], color});
                }
            }
        }
    }
    return dist;
}
```

The method never uses two edges of one color in a row, because it skips the color that brought the search to the current node. Every distance it returns belongs to a real alternating walk. The question is whether it returns every node that such a walk can reach.

```predict
Take n = 3, red edges 0 to 1 and 1 to 2, and blue edge 0 to 1. What does visitedPerNode return, and what is the correct answer?

It returns [0, 1, -1], and the correct answer is [0, 1, 2]. The search scans red edges first, so it reaches node 1 over the red edge and marks node 1. The blue edge from 0 to 1 then finds a marked node and is dropped. From node 1 the search arrived by red, so the red edge to node 2 is forbidden. The dropped blue arrival would have allowed that edge, so node 2 is lost.
```

<!-- stage: bottleneck -->
### One Mark Hides A Second Arrival

#### What The Mark Loses

The method scans each edge a bounded number of times, so its cost is O(V + E) and speed is not the problem. The answer is the problem. One alternating walk can end at a node with a red edge, and another can end there with a blue edge. These two arrivals look the same to a boolean mark, but they allow different next edges. After a red arrival only blue edges may follow, and after a blue arrival only red edges may follow.

#### Why Order Matters

The failing input above is small, yet the same pattern appears in every network that has two link kinds between the same machines. Whichever arrival the scan order meets first wins, and the other one disappears. The result then depends on the order of the edge lists, which a correct method must not allow. Swapping the two lists in the example changes which arrival survives and changes the output, so the method is wrong and not merely unlucky.

#### What A Repair Needs

A repair has to keep one record for each way of arriving, and it has to keep the total work near O(V + E). The next stage names the record and shows why a single queue still gives the shortest walks.

<!-- stage: insight -->
### Search Over Pairs Of Node And Color

Each position in the search is a node plus the kind of edge that arrived there. Treating that pair as the unit turns the problem into an ordinary shortest path on a larger graph.

<!-- names: state pair, opposite, seed -->

#### The State Pair

A **state pair** `(v, c)` stands for an alternating walk that ends at node `v` with its last edge of color `c`, where 0 means red and 1 means blue. A graph with `n` nodes has `2n` state pairs. The array `dist[v][c]` stores the fewest edges of any such walk, with -1 for a pair that no walk reaches. The pairs `(v, 0)` and `(v, 1)` are different entries, so reaching one never hides the other.

#### Moving To The Opposite Color

From the pair `(v, c)` the search may follow only edges of the **opposite** color `1 - c`. An edge of color `1 - c` from `v` to `w` leads to the pair `(w, 1 - c)`. No other transition exists. Only the pair `(v, 1 - k)` reads an edge of color `k` from `v`. Every edge is therefore read at most once, and the pair graph has at most `E` transitions.

#### Choosing The Seed

The walk of length zero has no last edge, so the first edge may have either color. The method places both `(0, 0)` and `(0, 1)` in the queue with distance 0 as the **seed**. Each pair then permits exactly the edges of the other color, and together the two pairs permit every first edge. A start that must begin with red needs only the pair `(0, 1)`, because that pair permits red edges alone.

#### Why One Queue Is Enough

Every transition adds one edge, so all weights in the pair graph equal 1. The queue then leaves pairs in order of nondecreasing distance, and the first arrival at a pair is its shortest one. The invariant is that `dist[v][c]` is final when the pair is first set. The answer for node `v` is the smaller of `dist[v][0]` and `dist[v][1]` among those that are not -1, and it is -1 when both are -1.

<!-- stage: variables -->
### What The Search Keeps

The method reads the node count `n` and the two edge lists, and it changes none of them. It builds one adjacency list for each color, and the list for color `c` and node `v` holds the targets of the edges of that color from `v`. Three structures hold the search state.

- **dist** is an `int[n][2]` table, where `dist[v][c]` is the edge count of the shortest walk that ends at `v` with color `c`, or -1.
- **queue** is an `ArrayDeque<Integer>` that holds the encoded pair `2 * v + c`, so the queue needs no wrapper object.
- **cur** is the pair that was just removed from the queue, and its distance is `dist` of that pair.

The table doubles as the visited record. A value other than -1 means that the search queued the pair already.

<!-- stage: trace -->
### Expanding Pairs On Two Small Graphs

#### Both Colors Allowed At The Start

The first graph has 5 nodes, red edges 0 to 1, 1 to 2 and 3 to 4, and blue edges 0 to 1 and 2 to 3. The cells list all ten pairs, each as a node followed by `r` or `b`. The pointer `cur` marks the pair that the search expands. The variable `dist` is the distance of that pair, `queue` lists the pairs that wait after the expansion, and `found` counts the pairs that have a distance so far. The search expands the two seeds first. Step 3 is the one that matters: pair `1b` leads over the red edge to node 2, which is the route that the single mark of the first attempt lost. Pair `1r` at step 4 has no blue edge to follow, and that is a dead end that costs nothing.

```trace
{"cells":["0r","0b","1r","1b","2r","2b","3r","3b","4r","4b"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":0,"queue":"0b-1b","found":3},"note":"Pair 0r has distance 0, so only blue edges may leave node 0. They add 1b with distance 1."},{"at":{"cur":1},"vars":{"dist":0,"queue":"1b-1r","found":4},"note":"Pair 0b has distance 0, so only red edges may leave node 0. They add 1r with distance 1."},{"at":{"cur":3},"vars":{"dist":1,"queue":"1r-2r","found":5},"note":"Pair 1b has distance 1, so only red edges may leave node 1. They add 2r with distance 2."},{"at":{"cur":2},"vars":{"dist":1,"queue":"2r","found":5},"note":"Pair 1r has distance 1, so only blue edges may leave node 1. No such edge reaches a new pair."},{"at":{"cur":4},"vars":{"dist":2,"queue":"3b","found":6},"note":"Pair 2r has distance 2, so only blue edges may leave node 2. They add 3b with distance 3."},{"at":{"cur":7},"vars":{"dist":3,"queue":"4r","found":7},"note":"Pair 3b has distance 3, so only red edges may leave node 3. They add 4r with distance 4."},{"at":{"cur":8},"vars":{"dist":4,"queue":"empty","found":7},"note":"Pair 4r has distance 4, so only blue edges may leave node 4. No such edge reaches a new pair."}]}
```

#### Red Edge Required First

The second graph has 3 nodes, red edges 0 to 1, 1 to 1 and 1 to 2, and blue edges 1 to 1 and 2 to 0. The search must start with a red edge, so the seed is the pair `0b` alone. The self loops are plain transitions. The red loop at node 1 leaves pair `1b` and returns to pair `1r`, which is already set, so the search drops it. Pair `2r` follows the blue edge to node 0, which leads to pair `0b`, and that pair also has a distance already.

```trace
{"cells":["0r","0b","1r","1b","2r","2b"],"pointers":["cur"],"steps":[{"at":{"cur":1},"vars":{"dist":0,"queue":"1r","found":2},"note":"Pair 0b has distance 0, so only red edges may leave node 0. They add 1r with distance 1."},{"at":{"cur":2},"vars":{"dist":1,"queue":"1b","found":3},"note":"Pair 1r has distance 1, so only blue edges may leave node 1. They add 1b with distance 2."},{"at":{"cur":3},"vars":{"dist":2,"queue":"2r","found":4},"note":"Pair 1b has distance 2, so only red edges may leave node 1. They add 2r with distance 3. The edge to 1r meets a pair that already has a distance, so the search drops it."},{"at":{"cur":4},"vars":{"dist":3,"queue":"empty","found":4},"note":"Pair 2r has distance 3, so only blue edges may leave node 2. No such edge reaches a new pair. The edge to 0b meets a pair that already has a distance, so the search drops it."}]}
```

<!-- stage: code -->
### Breadth-First Search Over Node And Color

The method builds the two adjacency lists in one array of lists, which uses the index `color * n + node`. It seeds both pairs, runs the queue loop and then reduces each row of `dist` to one answer.

```java
static int[] alternatingDistances(int n, int[][] red, int[][] blue) {
    List<List<Integer>> next = new ArrayList<>();
    for (int i = 0; i < 2 * n; i++) next.add(new ArrayList<>());
    for (int[] e : red) next.get(e[0]).add(e[1]);
    for (int[] e : blue) next.get(n + e[0]).add(e[1]);
    int[][] dist = new int[n][2];
    for (int[] row : dist) Arrays.fill(row, -1);
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    dist[0][0] = 0;
    dist[0][1] = 0;
    queue.add(0);
    queue.add(1);
    while (!queue.isEmpty()) {
        int pair = queue.poll();
        int v = pair / 2, c = pair % 2;
        int other = 1 - c;
        for (int w : next.get(other * n + v)) {
            if (dist[w][other] != -1) continue;
            dist[w][other] = dist[v][c] + 1;
            queue.add(2 * w + other);
        }
    }
    int[] answer = new int[n];
    for (int v = 0; v < n; v++) {
        int a = dist[v][0], b = dist[v][1];
        answer[v] = a == -1 ? b : b == -1 ? a : Math.min(a, b);
    }
    return answer;
}
```

Parallel edges and self loops need no special case, because every transition goes through the same check of `dist`. The method runs in O(V + E) time and uses O(V + E) memory. The method fills each row in a loop, because `Arrays.fill` does not accept a two-dimensional array. Writing `Arrays.fill(dist, new int[] {-1, -1})` would make every row the same object, and one write would change all nodes. Distances stay far below the `int` limit, because a walk over `2n` pairs has fewer than `2n` edges.

<!-- stage: applicability -->
### Recognizing Searches Over Node And Last Color

#### Reading The Cue

Use a pair of node and last color when the statement restricts the next edge. The restriction must depend on one property of the previous edge only. Typical cases are alternating link types, a turn that must change direction, or a rule that bans two toll roads in a row. The cue is a shortest path request together with a rule about consecutive edges. Check that the property has a small set of values, because the pair count is the node count times that set.

#### Checking The Invariant

The invariant is that `dist[v][c]` holds the fewest edges of an alternating walk that ends at `v` with color `c`, and the pair is set once and never changed. The invariant needs the seed to match the allowed first edges. Seeding only one pair silently forbids one color at the start. Test an input in which node 0 has a self loop, and test a node that has edges of both colors to the same target.

#### Avoiding The False Friend

The false friend is the visited array indexed by node alone. It looks right, since breadth-first search on a plain graph marks each node once, and it passes many small tests. The input with one red and one blue edge between the same two nodes, followed by a red edge, breaks it. A second false friend is a Dijkstra heap. Weights are all 1 here, so a heap adds a logarithm and gains nothing. Weighted edges with a color rule need the heap over the same pairs.

<!-- stage: exercises -->
### Exercises

#### [Build] Alternate Red And Blue (Author exercise)
<!-- id: sp-alternate-red-blue -->

**Prerequisites.** The state pair of this lesson.

**Problem.** Consider a directed graph on the nodes `0` to `n - 1`. The lists `red` and `blue` hold edges `[a, b]` from `a` to `b` of that color. A walk alternates when no two consecutive edges have the same color. Consider the alternating walks from node 0 that start with a red edge, where the empty walk also counts. Return an `int[]` of length `n` where entry `v` is the fewest edges of such a walk that ends at `v`, or -1 when none exists. The empty walk gives entry 0 the value 0.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 100`.
- **Edges** satisfy `0 <= red.length, blue.length <= 400`, with ends in `0..n-1`.
- **Repeats** and self loops may occur in either list.
- **Result** has length `n` and uses -1 for unreachable nodes.

**Example 1.** Input `n = 3`, `red = [[0,1],[1,2]]`, `blue = [[0,1]]`, output `[0,1,-1]`.

**Example 2.** Input `n = 4`, `red = [[0,1],[2,3]]`, `blue = [[1,2],[1,1]]`, output `[0,1,2,3]`.

**Hint.** Which one pair starts at distance 0 when the first edge has to be red?

**Changed decision.** The method queues only the pair that permits red edges, and every later move takes an edge of the color that differs from the last one.

#### [Vary] Two Start Modes (Author exercise)
<!-- id: sp-two-start-modes -->

**Prerequisites.** The exercise above.

**Problem.** The graph, the lists `red` and `blue` and the walks are as in the previous exercise, but the first edge may have either color. Return an `int[][]` with `n` rows. Entry `[v][0]` is the fewest edges of an alternating walk from node 0 that ends at `v` with a red edge, and `[v][1]` is the same for a blue edge. Use -1 when no such walk exists. The empty walk counts for both colors, so both entries of node 0 start at 0.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 100`.
- **Edges** satisfy `0 <= red.length, blue.length <= 400`, with ends in `0..n-1`.
- **Repeats** and self loops may occur in either list.
- **Result** has `n` rows of 2 values each, and the two entries of node 0 are 0.

**Example 1.** Input `n = 3`, `red = [[0,1],[1,2]]`, `blue = [[0,1]]`, output `[[0,0],[1,1],[2,-1]]`.

**Example 2.** Input `n = 4`, `red = [[0,1],[2,3]]`, `blue = [[1,2],[1,1]]`, output `[[0,0],[1,2],[-1,2],[3,-1]]`.

**Hint.** Which two pairs wait in the queue before the first expansion, and what does each permit?

**Changed decision.** The method queues both pairs of node 0 with distance 0, and it returns the whole table without reducing a row to one value.

#### [Boundary] Self-Loop And Parallel Colors (Author exercise)
<!-- id: sp-self-loop-parallel -->

**Prerequisites.** The two exercises above.

**Problem.** The graph and the lists `red` and `blue` are as before. Consider alternating walks from node 0 that contain at least one edge, with a first edge of either color. Return an `int[]` of length `n`. Entry `v` holds the edge count of the shortest such walk that ends at `v`, and -1 when no such walk exists. Entry 0 is therefore the length of the shortest alternating walk that returns to node 0, and it is not 0 by default.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 100`.
- **Edges** satisfy `0 <= red.length, blue.length <= 400`, with ends in `0..n-1`.
- **Self loops** and parallel edges of both colors may occur.
- **Result** entry 0 is -1 when no alternating walk of one edge or more ends at node 0.

**Example 1.** Input `n = 3`, `red = [[0,0],[0,1],[1,2]]`, `blue = [[0,1],[1,0]]`, output `[1,1,2]`.

**Example 2.** Input `n = 2`, `red = [[0,1]]`, `blue = [[1,1]]`, output `[-1,1]`.

**Hint.** Why can the pairs of node 0 not start with distance 0 for this task?

**Changed decision.** The method queues the targets of the edges that leave node 0 at distance 1 and sets no distance for the empty walk. It treats the two pairs of a node as independent entries.

#### [Recognize] Shortest Path with Alternating Colors (LeetCode 1129)
<!-- id: sp-alternating-colors-lc1129 -->

**Prerequisites.** All three exercises above.

**Problem.** A directed graph has `n` nodes labeled `0` to `n - 1`. The lists `redEdges` and `blueEdges` hold edges `[a, b]` from `a` to `b` of that color. Return an `int[]` `answer` of length `n`. Entry `answer[x]` is the fewest edges of a walk from node 0 to `x` whose consecutive edges differ in color. It is -1 when no such walk exists. The empty walk gives `answer[0] = 0`.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 100`.
- **Edges** satisfy `0 <= redEdges.length, blueEdges.length <= 400`.
- **Repeats** and self loops may occur in either list.
- **Result** has length `n`.

**Example 1.** Input `n = 3`, `redEdges = [[0,1],[0,2]]`, `blueEdges = [[1,0]]`, output `[0,1,1]`.

**Example 2.** Input `n = 5`, `redEdges = [[0,1],[1,2],[2,3],[3,4]]`, `blueEdges = [[1,2],[2,3],[3,1],[1,4]]`, output `[0,1,2,3,2]`.

**Hint.** Which of the two table entries of a node does the answer use, when one of them is -1?

**Changed decision.** The method seeds both pairs of node 0, expands only opposite-color edges, and reports the smaller defined entry of each row.
