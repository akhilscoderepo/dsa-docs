<!-- lesson-kind: standard -->
<!-- lesson-id: bfs-queue-state -->
## Find Shortest Steps With A Queue

<!-- stage: context -->
### An Elevator That Takes The Long Way

An elevator controller has two buttons. One moves the car up 3 floors and one moves it down 2 floors. The building has floors 0 to 20, and a button that would leave that range does nothing. A test asks for the fewest presses that take the car from floor 1 to floor 10. The controller search uses a stack, and it reports 8 presses. A short manual check shows that three presses work: up to 4, up to 7, up to 10.

The search visits every floor it can reach, so it does find floor 10. It simply does not find the shortest route first. What kind of container makes the first time the search reaches the target also the cheapest time?

<!-- stage: naive -->
### Search Deep, Stop At First Hit

The usual first attempt follows one route as far as possible. It keeps a stack of floors with their press counts. It pops the newest entry, tries the down button first, and stops when the popped floor is the target.

```java
static int firstFound(int start, int target, int top) {
    java.util.ArrayDeque<int[]> stack = new java.util.ArrayDeque<>();
    boolean[] seen = new boolean[top + 1];
    stack.push(new int[] {start, 0});
    seen[start] = true;
    while (!stack.isEmpty()) {
        int[] cur = stack.pop();
        if (cur[0] == target) return cur[1];
        int up = cur[0] + 3, down = cur[0] - 2;
        if (up <= top && !seen[up]) { seen[up] = true; stack.push(new int[] {up, cur[1] + 1}); }
        if (down >= 0 && !seen[down]) { seen[down] = true; stack.push(new int[] {down, cur[1] + 1}); }
    }
    return -1;
}
```

The `seen` array stops the search from revisiting a floor. For start 1, target 10 and top 20, the method returns 8.

<!-- stage: bottleneck -->
### The First Route Is Not Shortest

```predict
The stack search above tries the down button first and returns the press count of the first route that reaches floor 10. The shortest route needs 3 presses. Does the stack search return 3, a number slightly larger than 3, or a much larger number?

It returns 8. The stack follows one long route of mixed up and down presses before it backs up, and floor 10 first appears on that long route. The popped entry is the newest one, so a route with 3 presses waits under the entries above it.
```

The stack gives every route one chance in newest-first order. The order has no relation to press count, so the first hit can carry any number up to the size of the board. The search does visit each of the 21 floors at most once, so its work is O(B) for B floors. The answer is still wrong.

Trying every route to compare their lengths repairs the answer but costs O(2^d) for routes of d presses, because each floor offers two buttons. The search needs a visiting order that stays at O(B) and makes the first hit the shortest. A container that serves the oldest entry first gives such an order.

<!-- stage: insight -->
### Serve The Oldest Entry First

Replace the stack with a queue. The search then takes entries in the order it stored them. Routes with fewer presses are stored before routes with more presses, so the front of the queue always has the fewest presses among entries not yet served.

#### The Frontier Holds Unfinished Floors

The queue holds the **frontier**. The frontier is every floor the search has found but whose buttons it has not yet tried. Each floor stores its press count when it enters the frontier. Front to back, those counts never decrease, and the back count exceeds the front count by at most 1.

<!-- names: frontier, discovered, level -->

#### A Floor Is Discovered Once

A floor is **discovered** when the search first puts it into the queue. The search marks the floor at that moment, and not later when it leaves the queue. A floor reachable by two routes then enters the queue once, and the first route is the shorter one because of the queue order. Marking later would let one floor enter several times before its first removal.

#### Levels Are Press Counts

All floors with the same press count form a **level**. The search serves the whole level with count `k` before any floor with count `k + 1`, because new floors always join behind the floors already waiting. So the first time the target leaves the queue, its stored count is the fewest presses. The cost is O(B + E) for B floors and E button moves, which here is at most 2B.

<!-- stage: variables -->
### What The Search Keeps

The search keeps three pieces of state.

- **queue** holds the frontier, and the next floor to serve is at its front.
- **dist** stores the press count of each discovered floor, with -1 for undiscovered floors.
- **top** is the highest allowed floor, and the search ignores any move outside 0 to top.

The array `dist` plays two roles. A value other than -1 means the floor is marked as discovered, so a separate `seen` array is not needed. The same value is the press count that the answer returns. The queue changes on every step, and `dist` changes only when a floor is discovered.

<!-- stage: trace -->
### Serving The Frontier Step By Step

#### From Floor 1 To Floor 10

The first trace starts at floor 1 with target 10 and top 20. The cells are the floors 0 to 20, and the pointer `cur` marks the floor just removed from the queue. Each step lists the queue after the removal and the new floors that the removal adds.

Floor 1 is served first, and only its up button is valid, so floor 4 enters the queue with count 1. Floor 4 adds floors 7 and 2 with count 2. Floor 7 adds floors 10 and 5 with count 3, and floor 2 adds floor 0. Floor 10 then leaves the queue, and the search returns its count.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],"pointers":["cur"],"steps":[{"at":{"cur":1},"vars":{"queue":"[4:1]","new":"4:1"},"note":"Floor 1 leaves the queue with count 0. It adds 1 new floor(s)."},{"at":{"cur":4},"vars":{"queue":"[7:2, 2:2]","new":"7:2, 2:2"},"note":"Floor 4 leaves the queue with count 1. It adds 2 new floor(s)."},{"at":{"cur":7},"vars":{"queue":"[2:2, 10:3, 5:3]","new":"10:3, 5:3"},"note":"Floor 7 leaves the queue with count 2. It adds 2 new floor(s)."},{"at":{"cur":2},"vars":{"queue":"[10:3, 5:3, 0:3]","new":"0:3"},"note":"Floor 2 leaves the queue with count 2. It adds 1 new floor(s)."},{"at":{"cur":10},"vars":{"queue":"[5:3, 0:3]","count":3},"note":"Floor 10 leaves the queue and is the target. The answer is 3."}]}
```

#### From Floor 18 To Floor 13

The second trace starts at floor 18 with target 13. It shows that a floor already discovered is skipped, and that the search stops at the first time the target leaves the queue. Floors near the top lose their up button because the move would leave the board.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],"pointers":["cur"],"steps":[{"at":{"cur":18},"vars":{"queue":"[16:1]","new":"16:1"},"note":"Floor 18 leaves the queue with count 0. It adds 1 new floor(s)."},{"at":{"cur":16},"vars":{"queue":"[19:2, 14:2]","new":"19:2, 14:2"},"note":"Floor 16 leaves the queue with count 1. It adds 2 new floor(s)."},{"at":{"cur":19},"vars":{"queue":"[14:2, 17:3]","new":"17:3"},"note":"Floor 19 leaves the queue with count 2. It adds 1 new floor(s)."},{"at":{"cur":14},"vars":{"queue":"[17:3, 12:3]","new":"12:3"},"note":"Floor 14 leaves the queue with count 2. It adds 1 new floor(s)."},{"at":{"cur":17},"vars":{"queue":"[12:3, 20:4, 15:4]","new":"20:4, 15:4"},"note":"Floor 17 leaves the queue with count 3. It adds 2 new floor(s)."},{"at":{"cur":12},"vars":{"queue":"[20:4, 15:4, 10:4]","new":"10:4"},"note":"Floor 12 leaves the queue with count 3. It adds 1 new floor(s)."},{"at":{"cur":20},"vars":{"queue":"[15:4, 10:4]","new":"none"},"note":"Floor 20 leaves the queue with count 4. It adds 0 new floor(s)."},{"at":{"cur":15},"vars":{"queue":"[10:4, 13:5]","new":"13:5"},"note":"Floor 15 leaves the queue with count 4. It adds 1 new floor(s)."},{"at":{"cur":10},"vars":{"queue":"[13:5, 8:5]","new":"8:5"},"note":"Floor 10 leaves the queue with count 4. It adds 1 new floor(s)."},{"at":{"cur":13},"vars":{"queue":"[8:5]","count":5},"note":"Floor 13 leaves the queue and is the target. The answer is 5."}]}
```

<!-- stage: code -->
### Writing The Queue Search

#### The Method

The method uses `dist` as the discovery mark. It checks the target when a floor is removed, which is the first moment the stored count is final.

```java
static int fewestPresses(int start, int target, int top) {
    int[] dist = new int[top + 1];
    java.util.Arrays.fill(dist, -1);
    java.util.ArrayDeque<Integer> queue = new java.util.ArrayDeque<>();
    dist[start] = 0;
    queue.addLast(start);
    int[] step = {3, -2};
    while (!queue.isEmpty()) {
        int cur = queue.removeFirst();
        if (cur == target) return dist[cur];
        for (int s : step) {
            int next = cur + s;
            if (next < 0 || next > top || dist[next] != -1) continue;
            dist[next] = dist[cur] + 1;
            queue.addLast(next);
        }
    }
    return -1;
}
```

#### The Cost

Each floor enters the queue at most once, because `dist[next] != -1` blocks later entries. Each removed floor tries two buttons. The time is O(B) for B floors, and the space is O(B) for `dist` and the queue. The queue never holds `null`, because it stores `Integer` floors. A null divider between levels would fail in `ArrayDeque`, which is why the code stores counts in `dist` instead.

<!-- stage: applicability -->
### Deciding When A Queue Search Applies

#### Recognizing The Problem

The cue is a start state, moves that each cost one step, and a question about the fewest steps to a target. The invariant is that the queue holds discovered floors not yet served, with press counts that never decrease from front to back, and each state is marked when it enters the queue. Check the marking line first in any review, because a missing mark makes the queue grow without bound.

#### False Friend And Limits

A stack search is the false friend here. It uses the same loop shape with the container swapped, it visits the same states, and it passes a test that asks only whether the target is reachable. It fails any test that asks for the fewest steps, as the result of 8 against 3 in the opening problem showed. The queue search also assumes every move costs exactly one step. When moves have different costs, the queue order no longer follows total cost, and a different method is needed.

Do not use this search when the question is only whether a target is reachable and memory is tight. A stack search needs less memory on long narrow routes. Building the state space from raw input, as in grids and general graphs, is the topic of a later chapter. This lesson takes the moves as given.

<!-- stage: exercises -->
### Exercises

#### [Build] Process A Supplied Frontier (Author exercise)
<!-- id: sq-supplied-frontier -->

**Prerequisites.** The queue, the mark set at discovery, and the frontier in this lesson.

**Problem.** A directed graph has nodes numbered `0` to `n - 1`. The array `adj` gives, for each node, its successors in a fixed order. A queue starts with the node `start`, which is marked. Repeat until the queue is empty: remove the front node and record it, then append each successor that is not yet marked, in the listed order, and mark it when it is appended. Return the recorded nodes in order.

**Constraints.** The limits are:
- **Nodes** number `1 <= n <= 1000`.
- **Edges** may include self-loops and repeated successors.
- **Start** satisfies `0 <= start < n`.
- **Return** is an `int[]` with each reachable node exactly once.

**Example 1.** Input `adj = [[2,1],[3],[3,4],[1],[]]` and `start = 0`, output `[0,2,1,3,4]`.

**Example 2.** Input `adj = [[1],[2],[0,3],[]]` and `start = 2`, output `[2,0,3,1]`.

**Hint.** When does a node get its mark? What happens to a node that appears in two lists before the first one is removed?

**Changed decision.** The graph is supplied, so the work is the queue and the mark, with no graph construction.

#### [Vary] Minimum Add-One Or Double Steps (Author exercise)
<!-- id: sq-add-one-or-double -->

**Prerequisites.** The exercise above.

**Problem.** A counter shows an integer. One move adds 1 to it, and another move doubles it. A shown value above `bound` is not allowed. Given `start`, `target` and `bound`, return the fewest moves that turn `start` into `target`, or -1 if no sequence of allowed moves does.

**Constraints.** The limits are:
- **Bound** satisfies `1 <= bound <= 10^5`.
- **Values** satisfy `1 <= start, target <= bound`.
- **Return** is an `int`, with -1 when unreachable.
- **Moves** that would exceed `bound` are skipped.

**Example 1.** Input `start = 3`, `target = 10`, `bound = 20`, output 3.

**Example 2.** Input `start = 5`, `target = 3`, `bound = 20`, output -1.

**Hint.** What plays the role of the floors from the lesson? How large can the set of states be?

**Changed decision.** The moves change from fixed offsets to an add and a double, and the bound limits the states.

#### [Boundary] Start Is Target (Author exercise)
<!-- id: sq-start-is-target -->

**Prerequisites.** The two exercises above.

**Problem.** A token sits on a value between `0` and `bound`. One move subtracts 1 and another adds 4, and the token must stay within `0` to `bound`. Given `start`, `target` and `bound`, return the fewest moves from `start` to `target`, or -1 if none exists. A search that starts at the target must return 0 before it generates any move.

**Constraints.** The limits are:
- **Bound** satisfies `0 <= bound <= 10^5`.
- **Values** satisfy `0 <= start, target <= bound`.
- **Return** is an `int`, with -1 when unreachable and 0 when `start == target`.
- **Marking** applies when a value enters the queue, so no value enters twice.

**Example 1.** Input `start = 7`, `target = 7`, `bound = 10`, output 0.

**Example 2.** Input `start = 0`, `target = 3`, `bound = 10`, output 2.

**Hint.** Is the start marked before the loop? What would happen if marking waited until a value left the queue?

**Changed decision.** The start is the target, and marking at insertion keeps the queue free of duplicates.

#### [Recognize] Shortest Word Transform From Supplied Neighbors (Author exercise)
<!-- id: sq-word-transform-neighbors -->

**Prerequisites.** All three exercises above.

**Problem.** An array `words` has distinct words. The array `neighbors` lists, for each word index, the indices of the words that differ from it in exactly one letter. A transform sequence starts at word `begin`, ends at word `end`, and each step moves to a listed neighbor. Return the number of words in the shortest sequence, counting both ends, or 0 if no sequence exists.

**Constraints.** The limits are:
- **Words** number `1 <= words.length <= 2000`.
- **Neighbors** lists are symmetric and contain no self index.
- **Indices** satisfy `0 <= begin, end < words.length`.
- **Return** is an `int`, with 1 when `begin == end`.

**Example 1.** Input `words = [cat, cot, cog, dog, dot, bat]`, `neighbors = [[1,5],[0,2,4],[1,3],[2,4],[1,3],[0]]`, `begin = 0`, `end = 3`, output 4.

**Example 2.** Input `words = [red, rod, rid, bid, mud]`, `neighbors = [[1,2],[0,2],[0,1,3],[2],[]]`, `begin = 0`, `end = 4`, output 0.

**Hint.** Which quantity in the lesson counts presses? How does it relate to the number of words in the sequence?

**Changed decision.** The states are word indices and the moves come from lists, so the queue search runs on given neighbors.
