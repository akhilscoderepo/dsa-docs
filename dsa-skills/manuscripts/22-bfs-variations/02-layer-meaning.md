<!-- lesson-kind: standard -->
<!-- lesson-id: layer-meaning -->
## Layer Meaning

<!-- stage: context -->
### The Bells Of Tern Hill School

Tern Hill School is an old building of twelve rooms joined by a tangle of doors and short passages. Every room has a small brass handbell on a hook by the door. On the first day of term the caretaker rings the bell in the main hall, and the custom is that any room whose door is next to a ringing room answers with its own bell as soon as it hears one, exactly one count of ten later. Rooms that hear a bell at the same moment answer together, with a single clang.

The headteacher wants two numbers for any starting room. One is how many counts of ten pass before the very last reachable room has rung, and the other is which count the art room rings on. Some wings are cut off by a locked door, and those never ring at all. She does not want a guess from walking the corridors. She wants a procedure that gives the same answer for any plan of rooms and doors.

<!-- stage: naive -->
### Replay The Whole School Each Count

The direct method acts out the custom. Keep a table with the count on which each room rang, filled with -1 for rooms that have not rung. The starting room rings on count 0. Then run rounds: in round t, walk through every room in the school, and any silent room that has a door to a room that rang on count t - 1 rings now, on count t. Stop at the first round in which nobody new rings.

```java
static int[] ringCountsByRounds(int[][] doors, int start) {
    int rooms = doors.length;
    int[] rang = new int[rooms];
    java.util.Arrays.fill(rang, -1);
    rang[start] = 0;
    for (int t = 1; ; t++) {
        boolean anyone = false;
        for (int room = 0; room < rooms; room++) {
            if (rang[room] != -1) continue;
            for (int next : doors[room]) {
                if (rang[next] == t - 1) { rang[room] = t; anyone = true; break; }
            }
        }
        if (!anyone) return rang;
    }
}
```

This is correct for any plan. A room rings on count t only if some neighbor rang on count t - 1, and a room is never overwritten once it has rung. The plan itself is not changed, and a room behind a locked door keeps its -1.

<!-- stage: bottleneck -->
### Every Round Visits Every Room

Each round walks all V rooms and their doors, which costs O(V + E) however few rooms rang in the previous count. The number of rounds equals the largest count, and on a long chain of rooms that is nearly V. So the total is O(V * (V + E)) in the worst case, which for a school-sized plan is nothing but for a map of a hundred thousand rooms in a line is on the order of ten billion door checks, to produce one number per room.

The waste is plain. In round t only the rooms that rang on count t - 1 can possibly cause anything new, and there may be two of them or two thousand, yet the method rescans every silent room and every sleeping bell on the plan. A better method should keep the freshly rung rooms in hand, look only at their doors, and know exactly where one count ends and the next begins, without rereading the whole table to find out.

<!-- stage: insight -->
### One Layer Per Tick Of The Clock

A queue already holds exactly the rooms we want, as long as we are careful about where the cuts fall. Group the rooms by the count on which they ring. Everything that rings on count 0 is one **layer**, everything on count 1 is the next layer, and so on. The queue is ordered by layer, so at the start of any pass of the outer loop it contains one complete layer and nothing else, because the earlier layer has been fully removed and no room from two layers ahead has been found yet.

That gives the key move. Before touching the queue in a pass, read `queue.size()` into a local variable, the **captured size**. Remove exactly that many rooms, and give every one of them the same label. Rooms discovered during those removals join the back of the queue and belong to the next layer, so they are not part of this pass. Then add 1 to the clock once, after the whole layer is finished, not once per room. Reading the size again on each step would be wrong, because removals shrink the queue while discoveries grow it, so the pass would end in the wrong place and mix two layers.

One more detail matters whenever the question is about elapsed time rather than labels. The last layer taken from the queue discovers nobody, so advancing the clock after it counts a tick in which nothing happened. Only a **productive layer**, one whose processing found at least one new room, moves the answer forward. Either advance the clock when you actually queue something, or subtract the final empty pass.

The invariant is that at the top of each pass the queue holds precisely the rooms of one layer, all with the same label, and every unseen neighbor of them belongs to the next layer.

<!-- names: layer, captured size, productive layer -->

<!-- stage: variables -->
### Clock, Queue And Captured Size

The integer `n` is the number of rooms, the array `doors` lists the neighbors of each room, and `start` is the room of the first bell. The array `rang` has one entry per room, holding the count on which it rang, with -1 for rooms not reached. The queue `line` holds rooms that have rung but whose doors have not been looked at. The integer `clock` is the number of full layers completed, `size` is the captured size for the current pass, `room` is the one just removed, and `next` is the neighbor being tried through one of its doors.

<!-- stage: trace -->
### Two Clocks On Two Plans

The first trace runs on seven rooms numbered 0 to 6, with the pointer `cur` on the room just removed from the queue. The doors are 0-1, 0-2, 1-3, 2-3, 2-4, 3-5, 4-5 and 5-6, and the starting room is 0. The vars show the pass number in `layer`, the number of rooms of this layer still waiting in `left`, and the queue after the room is expanded. Notice that rooms 1 and 2 are removed in the same pass, and that room 3 is discovered during the removal of room 1 but is not touched until the next pass.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"layer":0,"left":0,"queue":"1,2"},"note":"Room 0 is removed in pass 0 and rings the new rooms 1,2."},{"at":{"cur":1},"vars":{"layer":1,"left":1,"queue":"2,3"},"note":"Room 1 is removed in pass 1 and rings the new room 3."},{"at":{"cur":2},"vars":{"layer":1,"left":0,"queue":"3,4"},"note":"Room 2 is removed in pass 1 and rings the new room 4."},{"at":{"cur":3},"vars":{"layer":2,"left":1,"queue":"4,5"},"note":"Room 3 is removed in pass 2 and rings the new room 5."},{"at":{"cur":4},"vars":{"layer":2,"left":0,"queue":"5"},"note":"Room 4 is removed in pass 2 and finds no new room."},{"at":{"cur":5},"vars":{"layer":3,"left":0,"queue":"6"},"note":"Room 5 is removed in pass 3 and rings the new room 6."},{"at":{"cur":6},"vars":{"layer":4,"left":0,"queue":"empty"},"note":"Room 6 is removed in pass 4 and finds no new room."}]}
```

The second trace is a small orchard crate problem written as a flat grid of three rows and four columns. A 2 is a rotten orange, a 1 is a fresh one and a 0 is an empty slot, and each minute every rotten orange spoils the fresh ones directly above, below, left and right. The pointer `cur` is the flat index of the orange being removed. The vars show `minutes`, which advances once per productive layer, and `per_orange`, the number you would get by adding one for every removal, which is the false friend. The cells show the grid at the start, and the queue column shows the oranges that are rotten but not yet expanded.

```trace
{"cells":[2,1,0,1,1,1,1,2,0,1,1,0],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"minutes":1,"per_orange":1,"queue":"7,4,1"},"note":"Orange 0 is removed during minute 1 and spoils 4,1."},{"at":{"cur":7},"vars":{"minutes":1,"per_orange":2,"queue":"4,1,3,6"},"note":"Orange 7 is removed during minute 1 and spoils 3,6."},{"at":{"cur":4},"vars":{"minutes":2,"per_orange":3,"queue":"1,3,6,5"},"note":"Orange 4 is removed during minute 2 and spoils 5."},{"at":{"cur":1},"vars":{"minutes":2,"per_orange":4,"queue":"3,6,5"},"note":"Orange 1 is removed during minute 2 and spoils nothing new."},{"at":{"cur":3},"vars":{"minutes":2,"per_orange":5,"queue":"6,5"},"note":"Orange 3 is removed during minute 2 and spoils nothing new."},{"at":{"cur":6},"vars":{"minutes":2,"per_orange":6,"queue":"5,10"},"note":"Orange 6 is removed during minute 2 and spoils 10."},{"at":{"cur":5},"vars":{"minutes":3,"per_orange":7,"queue":"10,9"},"note":"Orange 5 is removed during minute 3 and spoils 9."},{"at":{"cur":10},"vars":{"minutes":3,"per_orange":8,"queue":"9"},"note":"Orange 10 is removed during minute 3 and spoils nothing new."},{"at":{"cur":9},"vars":{"minutes":3,"per_orange":9,"queue":"empty"},"note":"Orange 9 is removed during minute 4 and spoils nothing new."}]}
```

<!-- stage: code -->
### Draining One Layer At A Time

```java
final class Bells {
    static int[] ringCounts(int[][] doors, int start) {
        int[] rang = new int[doors.length];
        java.util.Arrays.fill(rang, -1);
        java.util.ArrayDeque<Integer> line = new java.util.ArrayDeque<>();
        rang[start] = 0;
        line.add(start);
        int clock = 0;
        while (!line.isEmpty()) {
            int size = line.size();
            for (int i = 0; i < size; i++) {
                int room = line.poll();
                rang[room] = clock;
                for (int next : doors[room]) {
                    if (rang[next] != -1) continue;
                    rang[next] = clock + 1;
                    line.add(next);
                }
            }
            clock++;
        }
        return rang;
    }
}
```

The write `rang[next] = clock + 1` marks a room the moment it is queued, so no room can be queued twice, and the later write at removal repeats the same value harmlessly. The total time is O(V + E), because each room is removed once and each door is read twice, and the extra space is O(V) for the table and queue. After the loop `clock` is one more than the largest label, since the last pass found nobody.

<!-- stage: applicability -->
### Clocks, Waves And Rounds Of Work

Use a captured size whenever the answer is a number of simultaneous steps: minutes until a rumour or rot has spread, rounds of a game, days until every office has the update, or the grouping of states by distance. The invariant to defend is that each pass of the outer loop owns one complete layer, so every state removed in that pass gets one shared label and every new discovery gets that label plus one. Decide at the start whether the answer is the number of layers visited or the number of productive layers, and whether the target counts when it is queued or when it is removed.

The nearest false friend is a clock that ticks once per removed state. It looks natural, since each removal feels like work, but states of one layer act at the same instant, so ten rotten oranges next to ten fresh ones take one minute and not ten. A second false friend is reading `queue.size()` in the loop condition, `for (int i = 0; i < line.size(); i++)`, which compiles and runs yet moves with every removal and every discovery, so the pass ends in the wrong place and mixes layers.

This is the wrong tool when steps have different costs, because a layer then no longer means one unit of time, and a weighted method is required. It is also unnecessary when only reachability is wanted, since a plain traversal needs no clock. In Java, remember that `ArrayDeque.size()` is a live count, so the captured size must be copied into an `int` before the first removal, and that a collection holding `Integer` values should be drained with `poll()` into an `int`, not compared with `==`.

<!-- stage: exercises -->
### Exercises

#### [Build] Label BFS Layers (Author exercise)
<!-- id: bv-layer-lists -->

**Prerequisites.** The captured size and the shared label from this lesson.

**Problem.** An undirected graph has vertices 0 to n - 1 and an edge list `edges`, where each entry is a pair of endpoints, and `source` is a vertex. Return an `int[][]` in which row k holds, in ascending order, every vertex at distance exactly k from `source`. Vertices that cannot be reached appear in no row. The contract is that the inputs are not modified.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 3000, no self-loops, and repeated edges are allowed. The graph may be disconnected.

**Example 1.** Input `n = 7, edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[5,6]], source = 0`, output `[[0],[1,2],[3],[4]]`.

**Example 2.** Input `n = 6, edges = [[0,1],[1,2],[2,0],[2,3],[3,4]], source = 3`, output `[[3],[2,4],[0,1]]`.

**Hint.** What must be read before the inner loop starts so that the pass collects exactly one layer, and where does each finished batch go?

**Changed decision.** Instead of writing a distance into a table, every pass captures the queue size and copies its removed vertices into one row.

#### [Vary] Stop At First Target Layer (Author exercise)
<!-- id: bv-first-target-layer -->

**Prerequisites.** The Build rung with its layer rows.

**Problem.** The graph is as above, and `targets` is an array of distinct vertices. Return `[k, c]`, where k is the smallest distance from `source` to any target and c is how many targets lie at exactly distance k. Return `[-1, 0]` when no target is reachable. The contract is that the search stops after the first layer that contains a target and reads no later layer.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 3000, no self-loops, 1 <= targets.length <= n, and the targets are distinct.

**Example 1.** Input `n = 7, edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[4,5],[2,6]], source = 0, targets = [3,6,5]`, output `[2,2]`.

**Example 2.** Input `n = 7, edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[4,5],[2,6]], source = 0, targets = [0,4]`, output `[0,1]`.

**Hint.** If you stop at the first target you meet, can you still say how many other targets share its distance?

**Changed decision.** The search may not end when a target is first discovered, because the count needs the whole layer, so it ends after the layer in which one was found.

#### [Boundary] Initially Complete State (Author exercise)
<!-- id: bv-already-complete -->

**Prerequisites.** The Vary rung with its stop rule.

**Problem.** An undirected graph has n vertices and an edge list. Every vertex in `lit` starts lit, and each minute every dark vertex that shares an edge with a lit vertex becomes lit. Return the number of minutes until all n vertices are lit, `0` when they are lit from the start, and `-1` when some vertex can never be lit. The array `lit` may list a vertex more than once, and the inputs are not modified.

**Constraints.** 1 <= n <= 1000, 0 <= edges.length <= 3000, no self-loops, and 0 <= lit.length <= 2000 with every entry a valid vertex.

**Example 1.** Input `n = 4, edges = [[0,1],[1,2],[2,3]], lit = [3,2,1,0]`, output `0`.

**Example 2.** Input `n = 4, edges = [[0,1],[1,2],[2,3]], lit = [0,3,0,3]`, output `1`.

**Hint.** When there are no dark vertices to begin with, should the first pass run at all, and what does a repeated entry in `lit` do to a plain count of lit vertices?

**Changed decision.** The method tests for completeness before processing any layer and counts distinct lit vertices, so the finished start returns 0 instead of 1.

#### [Recognize] Rotting Oranges (LeetCode 994)
<!-- id: bv-rotting-final-minute -->

**Prerequisites.** The Boundary rung and the productive layer rule.

**Problem.** The `grid` is a rectangular `int[][]` where 0 is an empty slot, 1 is a fresh orange and 2 is a rotten orange. Each minute every fresh orange that is directly above, below, left or right of a rotten one becomes rotten. Return `[m, c]`, where m is the number of minutes until the last orange that can ever rot has rotted, and c is how many oranges rotted during minute m. Fresh oranges that no rotten orange can reach are ignored and stay fresh. Return `[0, 0]` when nothing ever rots. The contract is that `grid` is not modified.

**Constraints.** 1 <= rows, cols <= 10, and every entry is 0, 1 or 2.

**Example 1.** Input `grid = [[1,1,0,1],[1,2,1,1],[0,1,0,2]]`, output `[2,2]`.

**Example 2.** Input `grid = [[2,0,1]]`, output `[0,0]`.

**Hint.** Which layer is the final productive one, and how many oranges did it add to the queue?

**Changed decision.** The answer pairs the minutes with the size of the last productive layer, and unreachable fresh oranges no longer force a result of -1.
