<!-- lesson-kind: standard -->
<!-- lesson-id: search-from-both-ends -->
## Search From Both Ends

<!-- stage: context -->
### Finding A Chain Of Word Edits

A word puzzle app must turn "cold" into "warm" by changing one letter at a time. Every intermediate word must appear in the dictionary. The app shows the shortest chain, and the user counts the words to check it. With 100 000 words in the dictionary, a search that fans out from "cold" through all neighbors becomes slow on a phone when the chain is long.

Model each word as a **state**, which is one situation the search can stand on, and each one-letter change as a **move**, which turns one state into another. A move can be undone by a move in the opposite direction, so the moves are reversible. The **branching factor** `b` is the number of moves available from one state. The **distance** `d` is the fewest moves between the start and the target.

This lesson asks how to find `d` without visiting every state within distance `d` of the start.

<!-- stage: naive -->
### Searching From The Start Only

The breadth-first search of the previous chapter already finds `d`. It begins at the start state, visits states in order of distance, and stops when it reaches the target.

```java
static int distanceFromStart(List<List<Integer>> adj, int start, int target) {
    int[] dist = new int[adj.size()];
    Arrays.fill(dist, -1);
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    dist[start] = 0;
    queue.add(start);
    while (!queue.isEmpty()) {
        int cur = queue.poll();
        if (cur == target) return dist[cur];
        for (int next : adj.get(cur)) {
            if (dist[next] != -1) continue;
            dist[next] = dist[cur] + 1;
            queue.add(next);
        }
    }
    return -1;
}
```

Take a state space where every state has 10 moves and the target is 6 moves from the start.

```predict
About how many states can this search discover before it reaches the target?

Up to about 1.1 million. Distance 0 holds 1 state, distance 1 holds 10, distance 2 holds 100, and so on. The sum of the levels up to distance 6 is 1 111 111. The search cannot skip a level, because it removes states in order of distance.
```

<!-- stage: bottleneck -->
### Counting States Inside One Radius

With branching factor `b`, at most `b^k` states have distance `k`. The search finishes every level below `d` before it reaches the target, and it often discovers part of level `d` as well. The time is therefore O(b^d), and the queue plus the distance array take O(b^d) memory in the same worst case. For `b = 10` and `d = 6` the search stores about one million states, and for `d = 8` about one hundred million.

The start is not the only fixed point. The target is known as well, and every move is reversible, so a search can also begin at the target and follow the moves backward. Each search then only needs depth about `d / 2`. Two searches of depth 3 with `b = 10` discover about 1 111 states each. That is 2 222 states in total, against 1 111 111 for one search of depth 6. The time falls from O(b^d) to O(b^(d/2)). The next stage names the parts that make this safe.

<!-- stage: insight -->
### Growing Two Searches Toward Each Other

One search starts at the start state, and a second search starts at the target and uses the same moves backward. Each search stops long before it reaches the far end. The answer is the sum of the two distances at the state where they connect.

#### Two Searches With Two Maps

Each search keeps its own map from a state to the distance from its own origin. The map `distStart` holds distances from the start and the map `distTarget` holds distances from the target. The two maps stay separate, because a state can appear in both with different values.

The **frontier** of a search is the list of its newest states, all at the largest distance the search has reached and not yet expanded. Initially `frontierStart` holds the start and `frontierTarget` holds the target.

<!-- names: frontier, layer, crossing -->

#### Expanding One Whole Layer

A **layer** is the set of all states at one distance from the origin of a search. A round picks the side whose frontier has fewer states and expands every state of that frontier. The new states form the next frontier, which is the next layer of that side. Choosing the smaller frontier keeps the work of a round small, because the cost of a round is about the frontier size times `b`.

#### Testing Neighbors When They Appear

The search tests a state at the moment a move generates it. For each generated `next`, it looks `next` up in the map of the opposite side. When the lookup succeeds, the two searches have **crossing** paths, and the answer is `own[cur] + 1 + other[next]`.

The test must happen here and not later. Suppose the start is 0 and the target is 1, with one move between them. Before the first expansion, `distStart` holds only 0 and `distTarget` holds only 1, so no state sits in both maps.

A test that waits for one state in both maps still answers correctly. The first expansion writes state 1 into `distStart`, and the test then sees it. That answer comes one expansion later than the generation test, so it does extra work.

A test that compares queue fronts fails. When each side removes one state per turn, the start side removes 0 and queues 1, while the target side removes 1 and queues 0. The two queues never hold the same state at the same time.

The generated neighbor of 0 is 1, which the opposite map already holds, so the generation test returns 0 + 1 + 0 = 1 at once. Every odd distance has such a crossing edge between a state of one map and a state of the other.

#### Why Whole Layers Keep Sums Exact

The invariant is that before a round starts with depths `dS` and `dT`, no path of length `dS + dT` or less exists between the start and the target. The opposite map holds complete layers up to depth `dT`.

A match at a smaller depth would give a path of length `dS + dT` or less, which the invariant excludes, so every match has depth `dT`. A match found while expanding side `S` therefore gives the length `dS + 1 + dT`, and the first match is the answer.

Expanding a single state breaks this. Take the edges 0-1, 0-4, 1-3, 2-3, 2-4 and 2-5, with start 0 and target 5. The table shows four turns that expand one state each.

| Turn | Side | State expanded | What the turn finds |
| --- | --- | --- | --- |
| 1 | start | 0 | `distStart` gets 1 and 4 at distance 1 |
| 2 | target | 5 | `distTarget` gets 2 at distance 1 |
| 3 | start | 1 | `distStart` gets 3 at distance 2 |
| 4 | target | 2 | neighbor 3 is in `distStart`, so the sum is 1 + 1 + 2 = 4 |

The sum 4 is too large. State 4 also lies in `distStart` at distance 1, and the generation test would have returned 1 + 1 + 1 = 3. Turn 4 reached state 3 first only because the start side stopped in the middle of its layer.

A search that expands whole layers differs at turn 3. After turn 2 the start frontier holds 1 and 4, and the target frontier holds 2. The target side holds the smaller frontier, so it expands state 2 next. Its neighbor 3 is not in `distStart`, but its neighbor 4 is, at distance 1, so the sum is 1 + 1 + 1 = 3.

<!-- stage: variables -->
### What Each Search Keeps

The method keeps two maps and two frontiers. Each round also uses five local names: `fromStart`, `frontier`, `own`, `other` and `nextFrontier`. Each name has a fixed starting value.

- **distStart** is a map from state to distance from the start; it begins with the start at 0.
- **distTarget** is a map from state to distance from the target; it begins with the target at 0.
- **frontierStart** is the list of newest states of the first search; it begins with the start.
- **frontierTarget** is the list of newest states of the second search; it begins with the target.
- **fromStart** is a boolean that is true when the start side holds the smaller frontier.
- **frontier** is the list that the current round expands.
- **own** and **other** point to the map of the side being expanded and the map of the opposite side.
- **nextFrontier** is a new list that collects the generated states of one round.

<!-- stage: trace -->
### Following Two Searches On A Graph

The graph for both traces has the edges 0-1, 0-2, 1-3, 2-3, 3-4, 4-5, 4-6, 5-7 and 6-7. The cells are the vertex ids and the pointer `cur` shows the state being expanded. The values `distStart` and `distTarget` list the distance for each vertex in order, and -1 means that the vertex is not in that map yet.

#### Distance Five With A Crossing Edge

The start is 0 and the target is 7. Both frontiers hold one state, so the search expands the start side first, and it adds 1 and 2. The target side is smaller now, so it expands 7 and adds 5 and 6. Both frontiers hold two states, which means the start side expands again: states 1 and 2 add state 3, and state 3 adds state 4. When the search expands 4, its neighbor 5 is already in `distTarget` at distance 1. The generated neighbor is the match, and the answer is 3 + 1 + 1 = 5. No state appears in both maps at that moment, because the connection is the edge from 4 to 5.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"distStart":"0,1,1,-1,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,-1,-1,-1,0"},"note":"The start side expands 0 and adds 1 and 2."},{"at":{"cur":7},"vars":{"distStart":"0,1,1,-1,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,-1,1,1,0"},"note":"The target side expands 7 and adds 5 and 6."},{"at":{"cur":1},"vars":{"distStart":"0,1,1,2,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,-1,1,1,0"},"note":"The start side expands 1 and adds 3."},{"at":{"cur":2},"vars":{"distStart":"0,1,1,2,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,-1,1,1,0"},"note":"The start side expands 2 and adds nothing new."},{"at":{"cur":3},"vars":{"distStart":"0,1,1,2,3,-1,-1,-1","distTarget":"-1,-1,-1,-1,-1,1,1,0"},"note":"The start side expands 3 and adds 4."},{"at":{"cur":4},"vars":{"distStart":"0,1,1,2,3,-1,-1,-1","distTarget":"-1,-1,-1,-1,-1,1,1,0"},"note":"The start side expands 4. Its neighbor 5 is already in the opposite map at distance 1, so the answer is 3 + 1 + 1 = 5."}]}
```

#### Distance Four With A Larger Target Side

The start is 0 and the target is 5. The start side expands 0 and adds 1 and 2. The target side holds the smaller frontier, so it expands 5 and adds 4 and 7. Both frontiers hold two states, so the start side runs again. Expanding 1 adds 3, and expanding 2 finds 3 already known. The start frontier now holds one state against two on the target side, so the start side expands 3. Its neighbor 4 is in `distTarget` at distance 1, and the answer is 2 + 1 + 1 = 4.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"distStart":"0,1,1,-1,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,-1,0,-1,-1"},"note":"The start side expands 0 and adds 1 and 2."},{"at":{"cur":5},"vars":{"distStart":"0,1,1,-1,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,1,0,-1,1"},"note":"The target side expands 5 and adds 4 and 7."},{"at":{"cur":1},"vars":{"distStart":"0,1,1,2,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,1,0,-1,1"},"note":"The start side expands 1 and adds 3."},{"at":{"cur":2},"vars":{"distStart":"0,1,1,2,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,1,0,-1,1"},"note":"The start side expands 2 and adds nothing new."},{"at":{"cur":3},"vars":{"distStart":"0,1,1,2,-1,-1,-1,-1","distTarget":"-1,-1,-1,-1,1,0,-1,1"},"note":"The start side expands 3. Its neighbor 4 is already in the opposite map at distance 1, so the answer is 2 + 1 + 1 = 4."}]}
```

<!-- stage: code -->
### Computing Distance From Both Sides

The method returns the minimum number of moves, or -1 when the target is unreachable.

```java
static int bothEnds(List<List<Integer>> adj, int start, int target) {
    if (start == target) return 0;
    Map<Integer, Integer> distStart = new HashMap<>();
    Map<Integer, Integer> distTarget = new HashMap<>();
    distStart.put(start, 0);
    distTarget.put(target, 0);
    List<Integer> frontierStart = List.of(start);
    List<Integer> frontierTarget = List.of(target);
    while (!frontierStart.isEmpty() && !frontierTarget.isEmpty()) {
        boolean fromStart = frontierStart.size() <= frontierTarget.size();
        List<Integer> frontier = fromStart ? frontierStart : frontierTarget;
        Map<Integer, Integer> own = fromStart ? distStart : distTarget;
        Map<Integer, Integer> other = fromStart ? distTarget : distStart;
        List<Integer> nextFrontier = new ArrayList<>();
        for (int cur : frontier) {
            for (int next : adj.get(cur)) {
                Integer far = other.get(next);
                if (far != null) return own.get(cur) + 1 + far;
                if (own.containsKey(next)) continue;
                own.put(next, own.get(cur) + 1);
                nextFrontier.add(next);
            }
        }
        if (fromStart) frontierStart = nextFrontier; else frontierTarget = nextFrontier;
    }
    return -1;
}
```

The equal case returns before the loop, because both maps would otherwise hold the same state from the first step. The method stores `far` as an `Integer`, since `Map.get` returns `null` for a missing key. The loop ends when either frontier is empty, because that search has no state left to expand. With `b` moves per state, each search discovers about `b^(d/2)` states, so the time and the space are O(b^(d/2)).

<!-- stage: applicability -->
### Recognizing Two-Ended Searches

#### Reading The Cue

Use two searches when the start and the target are both known, every move costs the same, and every move has a reverse move. The state space must also branch heavily, since a chain of states with two neighbors each gains almost nothing. Typical statements ask for the minimum number of edits, turns or transformations between two given values.

#### Checking The Invariant

The invariant is that the two maps hold exact distances from their own origins, and that no path of length `dS + dT` or less exists, where `dS` and `dT` are the two current depths. It holds only when each round expands a whole layer and tests each generated state against the opposite map. The invariant breaks when edges have different costs, since a state's first discovery then no longer gives its distance. It also breaks when a move has no reverse, because the target side cannot follow the move backward.

#### Avoiding The False Friend

The false friend is to declare the meeting only when both queue fronts hold the same state. That rule misses the crossing edge of every odd distance, and the search then runs until a side is empty. A rule that waits for one state in both maps still finds the answer, but one expansion later than the generation test. A second false friend is to expand one state per turn and take the first match, which can return a sum that is too large, as the insight stage showed. A weighted graph needs a different method, which a later chapter teaches.

<!-- stage: exercises -->
### Exercises

#### [Build] Two-Ended Integer Search (Author exercise)
<!-- id: bv3-two-ended-integer -->

**Prerequisites.** The two-sided search of this lesson.

**Problem.** Given integers `start`, `target` and `limit`, a move changes the current value `x` to one of `x + 1`, `x - 1` and `2 * x`. It also allows `x / 2` when `x` is even. Every value that appears must lie in `1..limit`. Each move is reversible, because `x + 1` and `x - 1` undo each other, and so do `2 * x` and `x / 2`. Return the minimum number of moves that turn `start` into `target`.

**Constraints.** The limits are:
- **Limit** satisfies `1 <= limit <= 10^6`.
- **Start and target** are integers in `1..limit`, and they may be equal.
- **Result** is one `int`; the answer always exists, because `x + 1` and `x - 1` connect every pair.

**Example 1.** Input `start = 3`, `target = 29`, `limit = 40`, output `5`.

**Example 2.** Input `start = 1`, `target = 1000`, `limit = 1000`, output `12`.

**Hint.** Write a helper `static int[] neighbors(int x, int limit)` that returns the values one move away, and call it for both sides. Which of the two maps does a generated value consult before it is stored?

**Changed decision.** Each round expands the whole frontier of the smaller side and tests every generated value against the opposite map.

#### [Vary] Detect A Crossing Neighbor (Author exercise)
<!-- id: bv3-crossing-neighbor -->

**Prerequisites.** The first exercise above.

**Problem.** A grid `grid` has `rows` rows and `cols` columns, where 0 marks a free cell and 1 marks a wall. A move goes from a cell to a free cell directly above, below, left or right of it. Given a free start cell and a free target cell, return the minimum number of moves between them, or `-1` when no sequence of moves connects them.

**Constraints.** The limits are:
- **Grid size** satisfies `1 <= rows, cols <= 300`.
- **Cells** are 0 or 1, and the start and the target are 0.
- **Start and target** may be the same cell, and then the answer is 0.
- **Result** is one `int`.

**Example 1.** Input `grid = [[0,0,0,0],[1,1,0,1],[0,0,0,0]]`, `start = (0,0)`, `target = (2,3)`, output `5`.

**Example 2.** Input `grid = [[0,1,0],[1,0,1],[0,1,0]]`, `start = (0,0)`, `target = (1,1)`, output `-1`.

**Hint.** When the distance is odd, the two searches never share a cell. Where does the connection show up?

**Changed decision.** The search tests the neighbor cell at generation time, before it writes the cell into its own distance array.

#### [Boundary] Start Equals Target (Author exercise)
<!-- id: bv3-start-equals-target -->

**Prerequisites.** The two exercises above.

**Problem.** An undirected graph has vertices `0` to `n - 1` and an edge list `edges`, where `[a, b]` joins `a` and `b` in both directions. For a pair `start` and `target`, return the minimum number of edges on a path between them. Return `0` when `start` equals `target`, and return `-1` when no path exists.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no duplicate edge and no self loop.
- **Start and target** are vertices in `0..n-1`.
- **Result** is one `int`.

**Example 1.** Input `n = 3`, `edges = [[0,1]]`, `start = 2`, `target = 2`, output `0`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,2],[3,4]]`, `start = 0`, `target = 4`, output `-1`.

**Hint.** If start equals target, both maps hold that state before the first expansion. What should the method return, and at which point?

**Changed decision.** The method returns 0 before any search starts, and it keeps one distance array for each side.

#### [Recognize] Word Ladder (LeetCode 127)
<!-- id: bv3-word-ladder -->

**Prerequisites.** All three exercises above.

**Problem.** Given `beginWord`, `endWord` and a list `wordList`, a transformation sequence is a list of words that starts with `beginWord` and ends with `endWord`. Consecutive words differ in exactly one letter, and every word except `beginWord` belongs to `wordList`. Return the number of words in the shortest transformation sequence, or `0` when no sequence exists.

**Constraints.** The limits are:
- **Word length** satisfies `1 <= length <= 10`, and all words have the same length.
- **List size** satisfies `1 <= wordList.length <= 5000`, with distinct words.
- **Letters** are lowercase English letters.
- **Words** satisfy `beginWord != endWord`, and `endWord` may be missing from the list.

**Example 1.** Input `beginWord = "cold"`, `endWord = "warm"`, `wordList = ["cord","card","ward","warm","word","wood","worm"]`, output `5`.

**Example 2.** Input `beginWord = "cat"`, `endWord = "dog"`, `wordList = ["cot","cog","dot","dig"]`, output `0`.

**Hint.** Each word has at most `26 * length` neighbors; which side should expand when the lists have different sizes?

**Changed decision.** The search expands the smaller word frontier by a whole layer, and the answer counts words and not moves.
