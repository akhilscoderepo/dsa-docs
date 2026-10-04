<!-- lesson-kind: standard -->
<!-- lesson-id: bidirectional-frontiers -->
## Bidirectional Frontiers

<!-- stage: context -->
### Two Crews Under Corrie Pass

Corrie Pass is riddled with old mine workings: hundreds of numbered chambers, each joined to about ten neighbours by short galleries that miners cut a century ago. The water board wants a drain tunnel from chamber 0, high on the western slope, to the pump house at a chamber on the eastern slope. Each gallery that has to be cleared and shored costs the same, so the cheapest tunnel is the one that opens the fewest galleries.

Two crews are available, and they set off at once. Hale's crew works inward from the eastern portal, Marrow's from the western one. At the end of every shift each crew radios the chambers it has reached and how many galleries it took to get there. The foreman, Ines Okoro, wants a rule for when to call a halt and what number to quote the board, and she does not want to send either crew into the whole mountain to find out.

<!-- stage: naive -->
### One Crew Digs Out From The West

The direct method uses a single crew. Start at chamber 0, reach every chamber one gallery away, then every chamber two galleries away, and keep going ring by ring until the pump house shows up. The ring number at that moment is the answer, and it is the true minimum because rings are completed in order.

```java
static int galleriesFromWest(int[][] adj, int west, int pump) {
    int[] dist = new int[adj.length];
    java.util.Arrays.fill(dist, -1);
    java.util.ArrayDeque<Integer> line = new java.util.ArrayDeque<>();
    dist[west] = 0;
    line.add(west);
    while (!line.isEmpty()) {
        int cur = line.poll();
        if (cur == pump) return dist[cur];
        for (int next : adj[cur]) {
            if (dist[next] >= 0) continue;
            dist[next] = dist[cur] + 1;
            line.add(next);
        }
    }
    return -1;
}
```

The method is right for any mountain: it never revisits a chamber, and it answers -1 when the pump house cannot be reached at all. Every chamber it reaches is touched a constant number of times.

<!-- stage: bottleneck -->
### The Rings Grow Like Powers

A single crew pays for every chamber inside a ring of the answer's radius. If each chamber has b onward galleries and the pump house is d galleries away, ring k holds roughly b to the power k new chambers, so the work is O(b^d). With b = 10 and d = 6 that is about a million chambers examined for one tunnel. Tunnels, word puzzles and puzzle boards all look like this, with a fan-out of ten or more and an answer a handful of steps away.

Most of that effort is spent in the outer rings, which are the widest, and those rings are explored in every direction even though the target lies in only one. A better method should stop the rings while they are still small. The only lever is where the search starts: if both ends searched at the same time, each would need to reach only half of the distance, and a ring of radius three is a thousand chambers, not a million.

<!-- stage: insight -->
### Digging From Both Ends At Once

Let both crews dig. Each keeps its own distance table, and the two tables together are the **paired maps**: one maps every chamber the western crew has reached to its distance from the west, the other does the same from the east. The tables are never merged, because a chamber's distance from one end means nothing about the other end, and a single shared table cannot tell a chamber the crew itself already reached from one the other crew reached.

Each crew also owns a layer of chambers that it has reached but not yet explored from. At every turn, grow the **smaller frontier**: take the crew whose current layer holds fewer chambers and expand that whole layer by one gallery. Choosing the thinner side keeps the total number of chambers touched near the cheaper of the two growth patterns, which matters when one end sits in a dense cluster and the other in a sparse one.

The meeting is found by the **crossing check**. While generating a neighbour of the layer being expanded, ask whether that neighbour already sits in the opposite table. If it does, the answer is the distance of the chamber being expanded, plus one gallery, plus the neighbour's distance in the other table, and it can be returned on the spot. Waiting until both crews hold the same chamber at the front of their layers is not enough, since a tunnel of odd length is completed by a gallery that links two different chambers, one from each side.

The invariant is that, before every expansion, no chamber is in both tables, which proves the pump house is at least the two depths plus one gallery away, so the first crossing found is exactly the shortest tunnel.

<!-- names: paired maps, smaller frontier, crossing check -->

<!-- stage: variables -->
### Tables, Layers And The Meeting

The array `adj` lists, for each chamber, its neighbours, and `west` and `pump` are the two end chambers. Two arrays `fromWest` and `fromPump`, one entry per chamber, hold the distance from that end, with -1 meaning not reached. The lists `layerW` and `layerP` hold the chambers each side has reached but not yet expanded. The flag `growWest` says which side takes this turn. The integer `cur` is a chamber being expanded and `next` a neighbour being tried.

<!-- stage: trace -->
### Two Searches On Small Maps

The first trace uses eight chambers with joins 0-1, 0-2, 0-3, 1-4, 2-4, 3-5, 4-6, 5-6 and 6-7, searching from 0 to 7. The cells are the chamber numbers and the pointer `cur` is the chamber being expanded. The vars show which side is growing, how many chambers each table holds after the step, and the answer once found. Watch the sides: after the first expansion the western layer holds three chambers and the eastern one holds a single chamber, so the east takes every remaining turn.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"side":"W","west_reached":4,"pump_reached":1,"answer":"none"},"note":"Chamber 0 is expanded for the west side, and it reaches 3 new chambers (1,2,3)."},{"at":{"cur":7},"vars":{"side":"P","west_reached":4,"pump_reached":2,"answer":"none"},"note":"Chamber 7 is expanded for the pump side, and it reaches 1 new chamber (6)."},{"at":{"cur":6},"vars":{"side":"P","west_reached":4,"pump_reached":4,"answer":"none"},"note":"Chamber 6 is expanded for the pump side, and it reaches 2 new chambers (4,5)."},{"at":{"cur":4},"vars":{"side":"P","west_reached":4,"pump_reached":4,"answer":4},"note":"Chamber 4 is expanded for the pump side, and its neighbour 1 is already in the other table at distance 1, so the answer is 2 + 1 + 1 = 4."}]}
```

The second trace uses five chambers with joins 0-1, 1-2, 2-3 and 0-4, searching from 0 to 3. A leaf at chamber 4 makes the western layer larger, so the eastern crew gets a turn, and the two crews end up one gallery apart, holding chambers 1 and 2 that are different. The pointer `cur` and the vars are as before, and the last step is the crossing check firing while the neighbour is generated.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"side":"W","west_reached":3,"pump_reached":1,"answer":"none"},"note":"Chamber 0 is expanded for the west side, and it reaches 2 new chambers (1,4)."},{"at":{"cur":3},"vars":{"side":"P","west_reached":3,"pump_reached":2,"answer":"none"},"note":"Chamber 3 is expanded for the pump side, and it reaches 1 new chamber (2)."},{"at":{"cur":2},"vars":{"side":"P","west_reached":3,"pump_reached":2,"answer":3},"note":"Chamber 2 is expanded for the pump side, and its neighbour 1 is already in the other table at distance 1, so the answer is 1 + 1 + 1 = 3."}]}
```

<!-- stage: code -->
### Growing The Thinner Side

```java
static int tunnelLength(int[][] adj, int west, int pump) {
    if (west == pump) return 0;
    int n = adj.length;
    int[] fromWest = new int[n], fromPump = new int[n];
    java.util.Arrays.fill(fromWest, -1);
    java.util.Arrays.fill(fromPump, -1);
    fromWest[west] = 0;
    fromPump[pump] = 0;
    java.util.List<Integer> layerW = new java.util.ArrayList<>(java.util.List.of(west));
    java.util.List<Integer> layerP = new java.util.ArrayList<>(java.util.List.of(pump));
    while (!layerW.isEmpty() && !layerP.isEmpty()) {
        boolean growWest = layerW.size() <= layerP.size();
        java.util.List<Integer> layer = growWest ? layerW : layerP;
        int[] mine = growWest ? fromWest : fromPump;
        int[] other = growWest ? fromPump : fromWest;
        java.util.List<Integer> fresh = new java.util.ArrayList<>();
        for (int cur : layer) {
            for (int next : adj[cur]) {
                if (other[next] >= 0) return mine[cur] + 1 + other[next];
                if (mine[next] >= 0) continue;
                mine[next] = mine[cur] + 1;
                fresh.add(next);
            }
        }
        if (growWest) layerW = fresh; else layerP = fresh;
    }
    return -1;
}
```

The crossing check comes before the own-table check, so a neighbour that both sides know is reported and not skipped. A whole layer is expanded before sides are compared again, which keeps every distance in a table exact. Work is about twice the cost of one search to half the depth, and an empty layer on either side means that side is walled in, so the answer is -1.

<!-- stage: applicability -->
### Reversible Moves And A Known Target

Use two-ended search when there is one start, one known target, equal-cost moves that can be undone, and a fan-out large enough that rings of half the radius are far smaller than rings of the full radius. Puzzle boards, word chains, integer rewrite games and huge implicit graphs all qualify. The invariant to defend is that the two tables never share a chamber before a crossing is reported, and that every table entry is a true distance from its own end. If that holds, the first crossing found is optimal without any extra comparison.

The nearest false friend is declaring the meeting only when the two sides hold the very same chamber at the front of their queues. Whenever the shortest path has an odd number of galleries, the sides finish one gallery apart, linked by an edge, and that rule never fires. A second false friend is merging the two tables into one shared visited array, because a chamber's own self-loop or an old entry of the same side then looks like a meeting.

Do not use the method when the moves have different costs, since the layer-by-layer distance argument fails, when the target is not a single known state, or when the moves cannot be reversed so the backward side has no way to generate its neighbours. The gain also vanishes when the fan-out is one or two, since a path is a path. In Java, doubling a value with `2 * x` overflows `int` silently to a negative number once x passes about 1.07 billion, so test `x <= cap / 2` before doubling in integer searches.

<!-- stage: exercises -->
### Exercises

#### [Build] Two-Ended Integer Search (Author exercise)
<!-- id: bv-two-ended-integer -->

**Prerequisites.** The paired tables, the thinner-side rule and the crossing check from this lesson.

**Problem.** The values are integers from 1 to `cap`. From a value x you may move to x + 1, to x - 1, to 2 * x, and, when x is even, to x / 2, but every value visited must stay between 1 and `cap`. Return the fewest moves that turn `start` into `target`, or -1 when no sequence exists. The moves can be undone, so both searches use the same four moves.

**Constraints.** 1 <= start, target <= cap <= 1000000.

**Example 1.** Input `start = 3, target = 11, cap = 11`, output `4`.

**Example 2.** Input `start = 1, target = 37, cap = 37`, output `7`.

**Hint.** Which side's layer should be expanded next, and what must be true of a generated value for the answer to be ready?

**Changed decision.** The graph is never stored: each side generates neighbors from the four moves, and the thinner layer is grown a whole step at a time.

#### [Vary] Detect A Crossing Neighbor (Author exercise)
<!-- id: bv-crossing-neighbor -->

**Prerequisites.** The Two-Ended Integer Search rung.

**Problem.** A directed network has `n` nodes numbered 0 to n - 1 and arcs given as pairs `[u, v]`, each meaning one move from u to v. Return the fewest arcs on a route from `source` to `sink`, or -1 when there is none. The search from the sink may only follow arcs backwards, so it needs its own reversed adjacency, and the meeting is tested at the moment a next node is generated.

**Constraints.** 1 <= n <= 2000, 0 <= arcs <= 10000, and nodes can repeat among arcs, including self-loops and parallel arcs.

**Example 1.** Input `n = 5, arcs = [[0,1],[1,2],[2,3],[0,4]], source = 0, sink = 3`, output `3`.

**Example 2.** Input `n = 4, arcs = [[1,0],[1,2],[2,3]], source = 0, sink = 3`, output `-1`.

**Hint.** Which adjacency does the sink side walk, and what is added to the two distances when a neighbor is found in the other table?

**Changed decision.** The backward side walks reversed arcs, so the two sides no longer share one adjacency, while the crossing test still happens during generation.

#### [Boundary] Start Equals Target (Author exercise)
<!-- id: bv-start-equals-target -->

**Prerequisites.** The Detect A Crossing Neighbor rung.

**Problem.** An undirected network of `n` nodes is given as an edge list in which self-loops and repeated edges may appear. Return the fewest edges between `a` and `b`, or -1 if they are not connected. The two ends may be the same node, in which case the answer is 0 at once, and the two distance tables must stay logically separate.

**Constraints.** 1 <= n <= 2000 and 0 <= edges <= 10000, with every endpoint in range.

**Example 1.** Input `n = 3, edges = [[2,2]], a = 2, b = 2`, output `0`.

**Example 2.** Input `n = 3, edges = [[0,0],[0,1],[0,1]], a = 0, b = 2`, output `-1`.

**Hint.** What does the method return before it allocates anything, and why would a self-loop fool a single shared visited array?

**Changed decision.** The method returns 0 before any search when the ends coincide, and the tables stay separate so a node's own loop is never read as a meeting.

#### [Recognize] Word Ladder (LeetCode 127)
<!-- id: bv-word-ladder -->

**Prerequisites.** The Start Equals Target rung.

**Problem.** Given `beginWord`, `endWord` and a list `wordList` of distinct words that all have the same length, a transformation changes exactly one letter at a time, and every word after the first must be in `wordList`. Return the number of words in the shortest sequence from `beginWord` to `endWord`, counting both, or 0 when there is none. The `beginWord` need not be in the list, and it differs from `endWord`.

**Constraints.** 1 <= word length <= 10, 1 <= wordList.length <= 5000, and all words use lowercase English letters.

**Example 1.** Input `beginWord = "cold", endWord = "warm", wordList = ["cord","card","ward","warm","word","wold"]`, output `5`.

**Example 2.** Input `beginWord = "cold", endWord = "warm", wordList = ["cord","card","ward","word","wold"]`, output `0`.

**Hint.** How are the neighbors of a word produced without comparing it with every list word, and which side should be expanded next?

**Changed decision.** The implicit graph is searched from both words at once, growing whichever word layer is smaller until a generated word is known to the other side.
