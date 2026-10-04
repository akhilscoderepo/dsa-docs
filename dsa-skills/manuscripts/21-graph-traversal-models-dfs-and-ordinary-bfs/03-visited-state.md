<!-- lesson-kind: standard -->
<!-- lesson-id: visited-state -->
## Visited State

<!-- stage: context -->
### A Rumor In Pebblewick

Pebblewick is a hill village of forty houses, and everyone in it has a short list of neighbors they trust. On Tuesday morning Ines the baker learns that the ford will be closed for repairs, and she cannot keep it to herself. She tells every neighbor on her list, and each of them tells every neighbor on theirs. The trouble is that trust runs in loops. Odo the miller trusts Ines, Ines trusts Odo, and two other families trust both of them, so the same news arrives at the same door again and again, each time as if it were fresh.

By noon the schoolteacher has heard the closure five times and has told her whole list five times over. Ines would like to know two things: which houses will eventually hear the news, and how to stop the village from whispering in circles.

<!-- stage: naive -->
### Retell To Everyone You Trust

The direct method follows the rumor exactly as the villagers do. A queue holds the people who have just heard and still have to pass it on. Take the next person off the queue, count one telling, and put each neighbor on that person's list at the back of the queue. Nothing remembers who has already heard, so the method needs no extra state at all. To keep a test run from going on forever, the method gives up when the number of tellings passes a budget.

```java
static int tellings(List<List<Integer>> adj, int source, int budget) {
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.add(source);
    int told = 0;
    while (!queue.isEmpty()) {
        int person = queue.poll();
        if (++told > budget) return -1;
        for (int next : adj.get(person)) queue.add(next);
    }
    return told;
}
```

On a village with no loops and no shared neighbors, the method ends with one telling per person, and it is correct. Whenever the answer is a number rather than -1, it has counted every person who can hear the news, and some of them more than once.

<!-- stage: bottleneck -->
### One Telling Per Path, Not Per Person

Without memory, a person is handled once for every distinct way the news can reach them. Put a pair of lanes between each two junction houses, so that the news splits in two and joins again, and chain k such pairs together. The count of tellings then roughly quadruples with every extra pair, which is exponential in the number of vertices, and a village of thirty houses already needs about four thousand tellings to inform thirty people. Any loop makes it worse, because a person who can hear the news from someone they told earlier is reached again forever, so the work is not merely large but unbounded.

What the task needed was O(V + E): each person handled once and each trusted link read once. The method wastes work because it asks the question "who do I tell?" again for a person whose answer cannot change. A better arrangement would remember who is already in the story and refuse to schedule them a second time.

<!-- stage: insight -->
### Remember Who Is Already Scheduled

Keep one boolean per vertex, the **visited array**. A vertex is marked the first time anything decides it will be processed, and from then on no edge may schedule it again. Every vertex enters the work list at most once, so every vertex is handled at most once and each edge is read at most once, which brings the cost to O(V + E). Cycles stop for the same reason: the edge that closes a loop leads to a vertex that is already marked, so the news dies there.

The decision that people get wrong is when to mark. With **mark at enqueue**, the flag is set at the instant the vertex is put in the queue, before anyone else can reach it. With **mark at dequeue**, the flag is set only when the vertex comes off the front, and that leaves a gap. Take the diamond where vertex 0 trusts 1 and 2, and both trust 3. Vertex 1 is processed and puts 3 in the queue. Vertex 2 is processed next, finds 3 still unmarked, and puts a second 3 behind the first. The queue now holds two entries for the same vertex, and the second one must be recognized and skipped when it comes up. The answer is still right, but the queue is bounded by E instead of V, and the check at the front is no longer optional.

The same idea runs in depth-first search with a stack. If a vertex is marked as it is pushed, the stack never holds it twice. If it is marked only when popped, duplicates sit in the stack and the pop must skip them.

The invariant is that a marked vertex is either already processed or sitting in the work list exactly once, and an unmarked vertex has not been seen by any edge yet.

<!-- names: visited array, mark at enqueue, mark at dequeue -->

<!-- stage: variables -->
### Flags, Queue And Counters

The count `n` fixes the vertices as 0 to n - 1. The array `seen` has one boolean per vertex, all false at the start, and a true value means the vertex was scheduled at some point. The `queue` holds vertices that are marked but not yet expanded, and `v` is the one just taken from its front. The loop variable `w` runs over the neighbors of `v`. The counter `inserted` counts every addition to the queue over the whole run, and comparing it with the number of true flags exposes duplicates. For the stack version, `top` is the number of live entries in an int array of n cells.

<!-- stage: trace -->
### Two Ways To Mark The Diamond

Both traces run on one village of six houses. Vertex 0 trusts 1 and 2, both of those trust 3, vertex 3 trusts 0 again and also 4, and vertex 5 trusts 0 but nobody trusts 5. The pointer `v` marks the vertex taken from the front of the queue. The first trace marks at enqueue, so `inserted` ends at 5, equal to the number of vertices that can hear the news, and vertex 5 is never touched.

```trace
{"cells":["0","1","2","3","4","5"],"pointers":["v"],"steps":[{"at":{"v":0},"vars":{"inserted":3,"marked":3,"queue":"1,2"},"note":"Vertex 0 comes off the queue and adds 1,2 after marking it. Queue entries so far: 3."},{"at":{"v":1},"vars":{"inserted":4,"marked":4,"queue":"2,3"},"note":"Vertex 1 comes off the queue and adds 3 after marking it. Queue entries so far: 4."},{"at":{"v":2},"vars":{"inserted":4,"marked":4,"queue":"3"},"note":"Vertex 2 comes off the queue and finds no unmarked neighbor, so nothing is added. Queue entries so far: 4."},{"at":{"v":3},"vars":{"inserted":5,"marked":5,"queue":"4"},"note":"Vertex 3 comes off the queue and adds 4 after marking it. Queue entries so far: 5."},{"at":{"v":4},"vars":{"inserted":5,"marked":5,"queue":""},"note":"Vertex 4 comes off the queue and finds no unmarked neighbor, so nothing is added. Queue entries so far: 5."}]}
```

The second trace marks at dequeue on the same village and skips a vertex that comes off the queue already marked. The answer is the same five vertices, but the queue receives 7 entries, because 3 was added by both 1 and 2 and the edge from 3 back to 0 added 0 a second time. Two of the pops are wasted skips.

```trace
{"cells":["0","1","2","3","4","5"],"pointers":["v"],"steps":[{"at":{"v":0},"vars":{"inserted":3,"marked":1,"queue":"1,2"},"note":"Vertex 0 is marked now and every neighbor is added, marked or not. Queue entries so far: 3."},{"at":{"v":1},"vars":{"inserted":4,"marked":2,"queue":"2,3"},"note":"Vertex 1 is marked now and every neighbor is added, marked or not. Queue entries so far: 4."},{"at":{"v":2},"vars":{"inserted":5,"marked":3,"queue":"3,3"},"note":"Vertex 2 is marked now and every neighbor is added, marked or not. Queue entries so far: 5."},{"at":{"v":3},"vars":{"inserted":7,"marked":4,"queue":"3,0,4"},"note":"Vertex 3 is marked now and every neighbor is added, marked or not. Queue entries so far: 7."},{"at":{"v":3},"vars":{"inserted":7,"marked":4,"queue":"0,4"},"note":"Vertex 3 comes off the queue already marked, so this entry is a duplicate and is skipped."},{"at":{"v":0},"vars":{"inserted":7,"marked":4,"queue":"4"},"note":"Vertex 0 comes off the queue already marked, so this entry is a duplicate and is skipped."},{"at":{"v":4},"vars":{"inserted":7,"marked":5,"queue":""},"note":"Vertex 4 is marked now and every neighbor is added, marked or not. Queue entries so far: 7."}]}
```

<!-- stage: code -->
### Breadth First And Depth First

```java
static boolean[] bfs(List<List<Integer>> adj, int source) {
    boolean[] seen = new boolean[adj.size()];
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    seen[source] = true;
    queue.add(source);
    while (!queue.isEmpty()) {
        int v = queue.poll();
        for (int w : adj.get(v)) {
            if (!seen[w]) {
                seen[w] = true;
                queue.add(w);
            }
        }
    }
    return seen;
}

static boolean[] dfs(List<List<Integer>> adj, int source) {
    boolean[] seen = new boolean[adj.size()];
    int[] stack = new int[adj.size()];
    int top = 0;
    seen[source] = true;
    stack[top++] = source;
    while (top > 0) {
        int v = stack[--top];
        for (int w : adj.get(v)) {
            if (!seen[w]) {
                seen[w] = true;
                stack[top++] = w;
            }
        }
    }
    return seen;
}
```

The test and the assignment sit side by side, and the assignment comes before the insertion in both methods. That order is the whole lesson. Each vertex is inserted once, so the stack array of n cells can never overflow and the total work is O(n + E).

<!-- stage: applicability -->
### Any Walk That Can Return

Use visited state whenever a search can reach the same vertex by more than one route: any graph with a cycle, any undirected edge, any shared neighbor, and any grid walked in four directions. The invariant to keep in sight is that a vertex is marked at the moment it is scheduled, never later, and the traversal handles only marked vertices. The recognition cue is the question whether this vertex could be reached again from somewhere I have not looked yet, and a yes means a flag is needed.

The false friend is mark at dequeue in breadth first search. It looks natural because the flag sits next to the place where the vertex is processed, and on a tree it behaves perfectly. On a graph it lets duplicate entries into the queue, and any version that also forgets to skip a marked vertex when it comes off the front processes it twice. Two further false friends are a visited set that is cleared between sources, which silently repeats old work, and a flag array shared by two searches that were meant to be independent.

There is no need for any flag when the structure is known to be a tree walked away from its root, since a second route cannot exist. In Java, `ArrayDeque` refuses null elements, so a sentinel for an empty slot must be a number such as -1. A recursive depth first search on a long path of a hundred thousand vertices can overflow the call stack with `StackOverflowError`, so an explicit stack is the safe form there.

<!-- stage: exercises -->
### Exercises

#### [Build] Reachable Vertices (Author exercise)
<!-- id: gt-reachable-vertices -->

**Prerequisites.** Adjacency lists and the queue from the earlier lesson.

**Problem.** There are `n` vertices numbered `0` to `n - 1`, and `edges` lists directed edges as pairs `[from, to]`. Starting at `source`, return a boolean array of length `n` in which entry `v` is true exactly when a path of zero or more edges leads from `source` to `v`.

**Constraints.** 1 <= n <= 100, 0 <= edges.length <= 300, no pair repeats, and cycles are allowed.

**Example 1.** Input `n = 6, edges = [[0,1],[1,2],[3,2],[4,5]], source = 0`, output `[true,true,true,false,false,false]`.

**Example 2.** Input `n = 4, edges = [[2,1],[1,0],[0,3]], source = 2`, output `[true,true,true,true]`.

**Hint.** When is the flag of a neighbor set, and what does that do to a neighbor that two vertices both point at?

**Changed decision.** A vertex is flagged at the moment it enters the queue, so no vertex enters twice and the loop ends on every finite graph.

#### [Vary] Iterative DFS (Author exercise)
<!-- id: gt-iterative-dfs-stack -->

**Prerequisites.** The Reachable Vertices rung.

**Problem.** Solve the same reachability task with depth first search and an explicit stack, and return the reachable vertices as a list in ascending order. The stack must be an `int` array of exactly `n` cells, so the method must never hold a vertex on the stack twice at the same time.

**Constraints.** 1 <= n <= 100, 0 <= edges.length <= 300, no pair repeats, and cycles are allowed.

**Example 1.** Input `n = 5, edges = [[0,1],[0,2],[1,3],[2,3],[3,1]], source = 0`, output `[0,1,2,3]`.

**Example 2.** Input `n = 4, edges = [[2,0],[2,3],[1,2]], source = 2`, output `[0,2,3]`.

**Hint.** If a vertex is marked only when it is popped, how many copies can sit on the stack, and does n cells still suffice?

**Changed decision.** The mark moves from the pop to the push, which trades a skip check at the top of the loop for a bounded stack.

#### [Boundary] Cycle And Disconnected Vertex (Author exercise)
<!-- id: gt-cycle-and-disconnected -->

**Prerequisites.** The Iterative DFS rung.

**Problem.** Given a directed graph and a `source`, return the vertices that cannot be reached from `source`, in ascending order. The graph may contain cycles, self loops, vertices with no edges, and vertices that have an edge pointing into the reachable part without being reachable themselves.

**Constraints.** 1 <= n <= 100, 0 <= edges.length <= 300, pairs may join a vertex to itself.

**Example 1.** Input `n = 5, edges = [[0,1],[1,2],[2,0],[3,0]], source = 0`, output `[3,4]`.

**Example 2.** Input `n = 4, edges = [[1,1],[2,1]], source = 1`, output `[0,2,3]`.

**Hint.** What happens at the edge that closes a loop, and does an edge pointing into the reached area ever add its tail?

**Changed decision.** Edges are followed only from marked vertices toward their heads, so a loop ends at a marked head and an incoming edge never marks its tail.

#### [Recognize] Keys And Rooms (LeetCode 841)
<!-- id: gt-keys-and-rooms -->

**Prerequisites.** The Cycle And Disconnected Vertex rung.

**Problem.** There are `n` rooms numbered `0` to `n - 1`, and every room is locked except room `0`. The entry `rooms[i]` lists the keys found in room `i`, where key `k` opens room `k`. Starting in room 0 with no keys, return true when every room can be entered.

**Constraints.** 2 <= n <= 100, the total number of keys is at most 300, and keys may repeat or open a room that is already open.

**Example 1.** Input `rooms = [[2],[],[1,3],[0]]`, output `true`.

**Example 2.** Input `rooms = [[1],[0],[3],[2]]`, output `false`.

**Hint.** What is the edge here, and what must be counted at the end for the answer?

**Changed decision.** Keys become directed edges from room to room, and the answer is whether the count of marked rooms equals n.
