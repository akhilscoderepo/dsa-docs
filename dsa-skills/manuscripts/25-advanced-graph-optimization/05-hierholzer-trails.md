<!-- lesson-kind: standard -->
<!-- lesson-id: hierholzer-trails -->
## Walk Every Edge Once With Hierholzer

<!-- stage: context -->
### One Probe Per Link

A network tester must check every one-way link between servers. It sends one probe packet along each link. The probes travel in one continuous route, so each probe starts on the server where the previous probe ended. A link probed twice wastes time, and a link never probed stays untested. The tester has five links to cover: 0 to 1, 1 to 2, 2 to 0, 1 to 3 and 3 to 1. The route 0, 1, 3, 1, 2, 0 covers each of them exactly once.

Model the servers as vertices numbered `0` to `n - 1`. Model each link as a directed edge from one vertex to another. A **route** is a sequence of vertices in which every adjacent pair is a link. The task is to find a route that starts at a given vertex and uses every link exactly once. The method must also report when no such route exists. This lesson assumes a directed graph, a link list `links` of pairs `[from, to]`, and an input that the method never changes.

The first question is how to build the route so that the work grows with the number of links. The second question is how to detect that no route exists without trying every order.

<!-- stage: naive -->
### Following Any Unused Link

The first attempt is a greedy walk. It starts at the given vertex and follows the first unused link out of the current vertex. It repeats until the current vertex has no unused link, and then it returns the vertices it visited.

```java
static List<Integer> greedyWalk(int[][] links, int start) {
    boolean[] used = new boolean[links.length];
    List<Integer> route = new ArrayList<>();
    route.add(start);
    int cur = start;
    boolean moved = true;
    while (moved) {
        moved = false;
        for (int i = 0; i < links.length; i++) {
            if (!used[i] && links[i][0] == cur) {
                used[i] = true;
                cur = links[i][1];
                route.add(cur);
                moved = true;
                break;
            }
        }
    }
    return route;
}
```

The method never uses a link twice, because it marks each link in `used`. It stops when the current vertex has no unused link. The question is whether every link has been used at that point.

```predict
Use the five links 0 to 1, 1 to 2, 2 to 0, 1 to 3 and 3 to 1, and start at vertex 0. What route does greedyWalk return, and how many links stay unused?

It returns 0, 1, 2, 0 and leaves two links unused. The walk leaves vertex 1 through the link to 2, because that link is listed first. It returns to vertex 0, and vertex 0 has no unused link. The links 1 to 3 and 3 to 1 are never visited. A valid route exists, but the greedy walk committed to the wrong order at vertex 1 and cannot go back.
```

<!-- stage: bottleneck -->
### A Stuck Walk Cannot Resume

The greedy walk stops at the first vertex without an unused link. Unused links can remain at vertices that the walk passed earlier. The method has no way to return to such a vertex, because it keeps only the current vertex and the list of visited vertices.

One repair is to try every order of the links and keep the first order that works. A graph with E links has up to E! orders, which is O(E!) work. A second repair splices extra loops into the route. After each stuck walk, the method scans the route for a vertex with an unused link, walks a loop from there, and inserts the loop into the route. Each scan costs O(E), and a graph can need a new scan for each loop, so the total grows toward O(E^2). The greedy walk also pays O(E) for each step, because it scans the whole link list to find the next unused link.

A better method must find the next unused link of a vertex in constant time. It must also resume from an earlier vertex without scanning the route. Then each link is touched a constant number of times, and the total work is linear in the number of links.

<!-- stage: insight -->
### Recording Vertices After Their Links

The method walks until it is stuck, writes the stuck vertex to an output list, steps back one vertex, and continues from there. It reverses the output list at the end.

<!-- names: trail, postorder, balanced -->

#### Counting Degrees Before Walking

A **trail** is a route that uses each link at most once. An **Eulerian trail** uses every link exactly once, and an **Eulerian cycle** is an Eulerian trail that ends where it starts. The out-degree of a vertex counts the links that leave it, and the in-degree counts the links that enter it. A vertex is **balanced** when its out-degree equals its in-degree.

An Eulerian cycle needs every vertex to be balanced, because each visit enters through one link and leaves through another. An Eulerian trail that ends elsewhere needs the same condition at every vertex except two. The start has one more outgoing link than incoming links, and the end has one more incoming link than outgoing links. The method counts `out - in` for each vertex and rejects any other pattern before it walks.

#### Walking Until A Vertex Is Stuck

The method keeps a stack of vertices, which holds the walk that is still open. It starts with the start vertex on the stack. While the vertex on top of the stack has an unused outgoing link, the method consumes that link and pushes its target. Consuming a link means that the method moves a per-vertex index past it, and the link is never offered again. The input list is not changed.

#### Recording A Vertex After Its Links

When the vertex on top of the stack has no unused outgoing link, the method pops it and appends it to the output list. This order is called **postorder**, because a vertex is recorded only after all of its outgoing links are consumed. A popped vertex can never gain a new link, so its place in the output is final. After the pop, the new top may still have unused links. The method then walks a fresh loop from it, and the loop is recorded before the vertex below it. This is the splice that the greedy walk could not do.

#### Reversing The Recorded Order

Read the output list from its last entry to its first entry. Each vertex was recorded after every vertex that follows it on the trail, so the reversed list is the trail in travel order. The recorded order is right for a further reason. In a balanced graph, every vertex has as many unused outgoing links as incoming ones, so a stuck walk can only end at the vertex where it began. The stuck walk is therefore a closed loop. The method records it first and then returns to the vertex below, which is the place where the loop is spliced in. The invariant is that the output list, read backward, is a valid tail of the trail and uses only consumed links. The method finishes when the stack is empty. The trail is complete when the output holds `E + 1` vertices. A shorter output means that some links were not reachable from the start.

<!-- stage: variables -->
### Stack, Cursors And Output

The method reads `n`, the list `links` of pairs `[from, to]`, and the vertex `start`. It changes none of them. It builds an adjacency list from `links` and keeps these structures.

- **adj** is a list of `n` lists; `adj.get(v)` holds the targets of the links that leave `v`, in the order of `links`.
- **balance** is an `int[]` of length `n`; entry `v` is the out-degree minus the in-degree of `v`.
- **cursor** is an `int[]` of length `n`; entry `v` is the index of the next unused link in `adj.get(v)`.
- **stack** is an `int[]` of length `E + 1` with a count `top`; it holds the open walk.
- **out** is an `int[]` of length `E + 1` with a count `size`; it holds the recorded vertices.

The empty array is the answer when no trail exists. A vertex that has no links is valid input, and a graph with no links returns the array that holds only `start`.

<!-- stage: trace -->
### Two Runs Of The Walk

#### A Walk That Returns Too Early

The first run uses the five links 0 to 1, 1 to 2, 2 to 0, 1 to 3 and 3 to 1, with start vertex 0. Each cell is one event, in the order that events happen. A cell named take shows the vertex that the method pushes after it consumes a link. A cell named emit shows the vertex that the method pops and appends to the output. The pointer `ev` marks the current event. The variable `stack` is the number of vertices on the stack after the event, `unused` is the number of links not yet consumed, and `emitted` is the length of the output. The walk takes the links 0 to 1, 1 to 2 and 2 to 0 and gets stuck at vertex 0. Vertex 0 is emitted, and vertex 2 is emitted next. Vertex 1 is now on top and still owns the link 1 to 3. The method takes that link and the link 3 to 1, emits vertex 1, emits vertex 3, and emits vertex 1 and vertex 0 as the stack empties. The output is 0, 2, 1, 3, 1, 0. The reversed output 0, 1, 3, 1, 2, 0 uses all five links.

```trace
{"cells":["take 1","take 2","take 0","emit 0","emit 2","take 3","take 1","emit 1","emit 3","emit 1","emit 0"],"pointers":["ev"],"steps":[{"at":{"ev":0},"vars":{"stack":2,"unused":4,"emitted":0},"note":"The method consumes the link 0 to 1 and pushes vertex 1."},{"at":{"ev":1},"vars":{"stack":3,"unused":3,"emitted":0},"note":"The method consumes the link 1 to 2 and pushes vertex 2."},{"at":{"ev":2},"vars":{"stack":4,"unused":2,"emitted":0},"note":"The method consumes the link 2 to 0 and pushes vertex 0."},{"at":{"ev":3},"vars":{"stack":3,"unused":2,"emitted":1},"note":"Vertex 0 has no unused link, so the method pops it and appends it to the output. Vertex 2 is on top now. The first loop has ended at the start, and one vertex below still owns links."},{"at":{"ev":4},"vars":{"stack":2,"unused":2,"emitted":2},"note":"Vertex 2 has no unused link, so the method pops it and appends it to the output. Vertex 1 is on top now. Vertex 1 still owns the link 1 to 3."},{"at":{"ev":5},"vars":{"stack":3,"unused":1,"emitted":2},"note":"The method consumes the link 1 to 3 and pushes vertex 3."},{"at":{"ev":6},"vars":{"stack":4,"unused":0,"emitted":2},"note":"The method consumes the link 3 to 1 and pushes vertex 1."},{"at":{"ev":7},"vars":{"stack":3,"unused":0,"emitted":3},"note":"Vertex 1 has no unused link, so the method pops it and appends it to the output. Vertex 3 is on top now."},{"at":{"ev":8},"vars":{"stack":2,"unused":0,"emitted":4},"note":"Vertex 3 has no unused link, so the method pops it and appends it to the output. Vertex 1 is on top now."},{"at":{"ev":9},"vars":{"stack":1,"unused":0,"emitted":5},"note":"Vertex 1 has no unused link, so the method pops it and appends it to the output. Vertex 0 is on top now."},{"at":{"ev":10},"vars":{"stack":0,"unused":0,"emitted":6},"note":"Vertex 0 has no unused link, so the method pops it and appends it to the output. The stack is empty."}]}
```

#### A First Link To A Dead End

The second run uses the four links 0 to 1, 0 to 2, 2 to 3 and 3 to 0, with start vertex 0. Vertex 0 has one more outgoing link than incoming links, and vertex 1 has one more incoming link than outgoing links, so the trail must end at vertex 1. The first link out of vertex 0 leads straight to vertex 1, and vertex 1 has no outgoing link. A method that prints vertices in the order that it visits them returns 0, 1 and leaves three links unused. This method emits vertex 1 first, so vertex 1 lands last after the reversal. It then continues from vertex 0 through vertices 2, 3 and back to 0. The output is 1, 0, 3, 2, 0. The reversed output 0, 2, 3, 0, 1 uses all four links.

```trace
{"cells":["take 1","emit 1","take 2","take 3","take 0","emit 0","emit 3","emit 2","emit 0"],"pointers":["ev"],"steps":[{"at":{"ev":0},"vars":{"stack":2,"unused":3,"emitted":0},"note":"The method consumes the link 0 to 1 and pushes vertex 1."},{"at":{"ev":1},"vars":{"stack":1,"unused":3,"emitted":1},"note":"Vertex 1 has no unused link, so the method pops it and appends it to the output. Vertex 0 is on top now. The walk would print only 0, 1 here, and this vertex lands last after the reversal."},{"at":{"ev":2},"vars":{"stack":2,"unused":2,"emitted":1},"note":"The method consumes the link 0 to 2 and pushes vertex 2."},{"at":{"ev":3},"vars":{"stack":3,"unused":1,"emitted":1},"note":"The method consumes the link 2 to 3 and pushes vertex 3."},{"at":{"ev":4},"vars":{"stack":4,"unused":0,"emitted":1},"note":"The method consumes the link 3 to 0 and pushes vertex 0."},{"at":{"ev":5},"vars":{"stack":3,"unused":0,"emitted":2},"note":"Vertex 0 has no unused link, so the method pops it and appends it to the output. Vertex 3 is on top now."},{"at":{"ev":6},"vars":{"stack":2,"unused":0,"emitted":3},"note":"Vertex 3 has no unused link, so the method pops it and appends it to the output. Vertex 2 is on top now."},{"at":{"ev":7},"vars":{"stack":1,"unused":0,"emitted":4},"note":"Vertex 2 has no unused link, so the method pops it and appends it to the output. Vertex 0 is on top now."},{"at":{"ev":8},"vars":{"stack":0,"unused":0,"emitted":5},"note":"Vertex 0 has no unused link, so the method pops it and appends it to the output. The stack is empty."}]}
```

<!-- stage: code -->
### Hierholzer With An Explicit Stack

The method returns the vertices of the trail in travel order, or an empty array when no trail starts at `start` and uses every link. It keeps the stack in an `int[]`, because a recursive version needs one call frame per link and can raise `StackOverflowError` on a long trail. The sums here count links, so `int` is enough.

```java
static int[] hierholzer(int n, int[][] links, int start) {
    int m = links.length;
    List<List<Integer>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    int[] balance = new int[n];
    for (int[] e : links) {
        adj.get(e[0]).add(e[1]);
        balance[e[0]]++;
        balance[e[1]]--;
    }
    for (int v = 0; v < n; v++) {
        if (balance[v] > 1 || balance[v] < -1) return new int[0];
        if (balance[v] == 1 && v != start) return new int[0];
    }
    int[] cursor = new int[n];
    int[] stack = new int[m + 1];
    int[] out = new int[m + 1];
    int top = 0, size = 0;
    stack[top++] = start;
    while (top > 0) {
        int v = stack[top - 1];
        if (cursor[v] < adj.get(v).size()) {
            stack[top++] = adj.get(v).get(cursor[v]++);
        } else {
            out[size++] = v;
            top--;
        }
    }
    if (size != m + 1) return new int[0];
    for (int i = 0, j = size - 1; i < j; i++, j--) {
        int t = out[i]; out[i] = out[j]; out[j] = t;
    }
    return out;
}
```

The degree check runs first and rejects every pattern except a balanced graph or a start with one extra outgoing link. The loop pushes a target after it advances `cursor[v]`, so each link is consumed once. The final length test catches links that the walk never reached. The method runs in O(V + E) time, because each link is pushed once and each push is matched by one pop. It uses O(V + E) memory for the adjacency list, the cursors, the stack and the output.

<!-- stage: applicability -->
### Recognizing Every-Edge-Once Problems

#### Reading The Cue

Use this method when the statement asks for a route that uses every edge exactly once. Reconstructing a trip from a pile of one-way tickets has this shape. Testing every link of a network once and drawing every segment of a figure without lifting the pen have it too. The answer is usually the route itself, a yes or no answer, or the count of edges. A statement that asks to visit every vertex once is a different problem.

#### Checking The Invariant

The invariant is that the method consumes each link once while it walks, and it appends a vertex to the output only when that vertex has no unused outgoing link. The output then lists the trail in reverse. Two conditions in the code protect it. The degree check must run before the walk, and the output length must equal `E + 1` after it. Test a graph with no links, a self loop, two parallel links, and a graph whose links split into two parts that the start cannot reach.

#### Avoiding The False Friend

A false friend is a method that looks correct for the problem and gives a wrong answer on some inputs. Here it is an ordinary depth-first search that records each vertex when it first visits it. That order is a valid route only when the search never gets stuck early, and the second run of this lesson shows the failure. A second false friend is the degree check alone. Balanced degrees do not prove that every link is reachable from the start, so the length test is also required.

<!-- stage: exercises -->
### Exercises

#### [Build] Eulerian Cycle (Author exercise)
<!-- id: ga-hier-euler-cycle -->

**Prerequisites.** The code stage of this lesson.

**Problem.** A directed graph is given on `n` vertices numbered from zero and has a list `links` of pairs `[a, b]`, each a link from `a` to `b`. An Eulerian cycle is a route that starts and ends at vertex `0` and uses every link exactly once. At each vertex the method consumes the unused link that appears earliest in `links`. Return the cycle as an `int[]` of vertices. Return an empty array when no Eulerian cycle through vertex `0` exists. A graph with no links returns `[0]`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Links** satisfy `0 <= links.length <= 5000`.
- **Repeats** do not occur, and no link joins a vertex to itself.
- **Mutation** of `links` is not allowed.

**Example 1.** Input `n = 5`, `links = [[0,1],[1,2],[2,0],[1,3],[3,1],[1,4],[4,1]]`, output `[0,1,3,1,4,1,2,0]`.

**Example 2.** Input `n = 4`, `links = [[0,1],[1,2],[2,0],[2,3]]`, output `[]`.

**Hint.** Which vertices must be balanced, and what does the length of the recorded output reveal about unreachable links?

**Changed decision.** The method returns the reversed postorder and not the order of first visits, and it returns an empty array when the cycle cannot exist.

#### [Vary] Eulerian Path (Author exercise)
<!-- id: ga-hier-euler-path -->

**Prerequisites.** The exercise above.

**Problem.** A directed graph has the vertex labels `0` to `n - 1` and has a list `links` of pairs `[a, b]`. An Eulerian path is a route that uses every link exactly once and may end at a different vertex than it starts. The start vertex is the one whose out-degree is one more than its in-degree. When every vertex is balanced, the start is the smallest vertex that has an outgoing link. The method always takes the earliest listed unused link out of the current vertex. Return the path as an `int[]`, or an empty array when none exists. A graph with no links returns `[0]`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Links** satisfy `0 <= links.length <= 5000`.
- **Repeats** do not occur, and no link joins a vertex to itself.
- **Mutation** of `links` is not allowed.

**Example 1.** Input `n = 5`, `links = [[2,0],[0,1],[1,2],[2,3],[3,4]]`, output `[2,0,1,2,3,4]`.

**Example 2.** Input `n = 4`, `links = [[1,2],[2,3],[1,3]]`, output `[]`.

**Hint.** Which degree pattern names the start vertex, and what happens to the start when all vertices are balanced?

**Changed decision.** The method chooses the start from the degree counts and does not take it as input.

#### [Boundary] Parallel Edges (Author exercise)
<!-- id: ga-hier-parallel-edges -->

**Prerequisites.** The two exercises above.

**Problem.** A directed multigraph uses vertex labels `0` through `n - 1`. The matrix `count` has size `n` by `n`, and `count[u][v]` is the number of links from `u` to `v`. Self loops are allowed, so `count[u][u]` may be positive. Find an Eulerian cycle that starts and ends at vertex `0` and uses every link exactly once. At each vertex the method takes the link to the smallest target that still has an unused link. Return the cycle as an `int[]`, or an empty array when none exists. A graph with no links returns `[0]`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 100`.
- **Counts** satisfy `0 <= count[u][v] <= 50`.
- **Total** number of links is at most `10^6`.
- **Mutation** of `count` is not allowed.

**Example 1.** Input `count = [[1,2],[2,0]]`, output `[0,0,1,0,1,0]`.

**Example 2.** Input `count = [[1,0,0],[0,0,1],[0,1,0]]`, output `[]`.

**Hint.** What does the method need to store for a pair of vertices when one link can appear several times?

**Changed decision.** The method stores how many links remain between two vertices, and a yes or no entry for each pair would lose the repeats.

#### [Recognize] Reconstruct Itinerary (LeetCode 332)
<!-- id: ga-hier-itinerary -->

**Prerequisites.** All three exercises above.

**Problem.** A list `tickets` holds pairs `[from, to]` of airport codes, and each pair is one flight. The trip starts at `JFK` and uses every ticket exactly once. Among all valid itineraries, return the one that is lexically largest when compared airport by airport. Return an empty list when no valid itinerary exists. Equal tickets may appear several times.

**Constraints.** The limits are:
- **Tickets** satisfy `1 <= tickets.length <= 300`.
- **Codes** are strings of three uppercase letters.
- **Repeats** and self loops may occur.
- **Mutation** of `tickets` is not allowed.

**Example 1.** Input `tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]`, output `["JFK","SFO","ATL","JFK","ATL","SFO"]`.

**Example 2.** Input `tickets = [["JFK","ATL"],["JFK","SFO"]]`, output `[]`.

**Hint.** Which order of the outgoing tickets gives the largest result, and how does the method notice that no itinerary exists?

**Changed decision.** The method prefers the largest destination and not the smallest, and it must report a missing itinerary because the input does not guarantee one.
