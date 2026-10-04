<!-- lesson-kind: standard -->
<!-- lesson-id: path-enumeration -->
## Path Enumeration

<!-- stage: context -->
### The Laminated Cards At Kestrel Huts

High in the Kestrel range, five mountain huts are joined by signed trails. After a rockfall closed the old loop, the park service made every trail one way and always downhill, so a walker who leaves a hut can never climb back to it. Ines, the head warden, is printing a laminated card for every distinct route a trekker can take from the Windgap hut at the top to the Tarn hut by the lake. Each card lists the huts in the order they are passed, and trekkers pick one at the desk.

Ines has a sheet that says which huts each hut's trails lead to, and nothing more. Two routes can share a middle hut and still be different cards, so she cannot just ask which huts are reachable. She needs every route written out in full, for any network the park service draws next season.

<!-- stage: naive -->
### Guess Every Sequence Of Huts

The plainest method treats a card as a guess. Start from the Windgap hut and grow sequences of huts one position at a time, trying every hut in every position, whether or not a trail exists. Whenever a sequence ends at the Tarn hut, walk along it and confirm that each hut really has a trail to the next one. Keep the sequence only if every step is a real trail.

```java
static List<List<Integer>> routesByGuessing(int[][] trails, int from, int to) {
    List<List<Integer>> found = new ArrayList<>();
    guess(trails, List.of(from), to, found);
    return found;
}

static void guess(int[][] trails, List<Integer> seq, int to, List<List<Integer>> found) {
    int n = trails.length;
    if (seq.get(seq.size() - 1) == to && allStepsAreTrails(trails, seq)) found.add(seq);
    if (seq.size() == n) return;
    for (int hut = 0; hut < n; hut++) {
        List<Integer> longer = new ArrayList<>(seq);
        longer.add(hut);
        guess(trails, longer, to, found);
    }
}

static boolean allStepsAreTrails(int[][] trails, List<Integer> seq) {
    for (int i = 0; i + 1 < seq.size(); i++) {
        boolean ok = false;
        for (int next : trails[seq.get(i)]) if (next == seq.get(i + 1)) ok = true;
        if (!ok) return false;
    }
    return true;
}
```

This is correct. Because trails only go downhill, no walk can visit more than n huts, so sequences of length n cover every possible route, and the final check lets nothing invalid through.

<!-- stage: bottleneck -->
### Most Guesses Break At Step One

With n huts there are n choices at each of the n - 1 positions after the start, so the method builds about n^(n-1) sequences and checks each in O(n) more. That is O(n^n) work. At twelve huts the count is above seven hundred billion, for a map that may hold a few dozen real routes.

The waste has a clear source. The trail check happens only at the very end, so a sequence whose first step is not a trail still grows into every possible extension, and every one of those extensions is doomed. Each growth step also copies the whole sequence into a new list. A better method should refuse a bad step the moment it is taken, extend only along trails that exist, and spend its copying only on sequences that turn out to be complete cards.

<!-- stage: insight -->
### One Working List That Grows And Shrinks

Keep a single list, the **working path**, holding the huts on the walk in progress. It is not a candidate that gets checked later. It is exactly the chain of calls currently open: the hut at the end is the one being explored, and the huts before it are its ancestors in the recursion. Taking a trail means appending the next hut and calling the method on it. When that call returns, the **undo step** removes the hut just added, so the list is again what it was before the loop tried that neighbor, and the next trail starts from a clean state.

When the walk arrives at the target, the working path is a finished card, but it cannot be stored as it is. The list will keep being changed as the recursion unwinds, and a stored reference would end up showing whatever the list holds at the end, which is only the starting hut. Store a **snapshot**, a fresh list copied from the working path at that moment. Copying costs time proportional to the card length, and it is paid only once per real route.

A hut that is a dead end, with no trails out, simply returns and leaves nothing behind. In a downhill network there is no visited set at all. A hut reached through two different upper huts has to appear in two different cards, so marking it forbidden after the first card would silently erase the second.

The invariant is that the working path equals the chain of open calls, and each call leaves it exactly as it found it.

<!-- names: working path, undo step, snapshot -->

<!-- stage: variables -->
### Trails, Path And Found Cards

The array `trails` holds, for each hut number, the list of huts its trails lead to, and `from` and `to` are the Windgap and Tarn huts. The list `path` is the working path and starts holding only `from`. The list `found` collects the finished cards, and each of its entries is a separate copy. The integer `hut` is the end of the walk in the current call, and `next` is the trail being tried from it. The size of `path` is also the depth of the recursion.

<!-- stage: trace -->
### Two Walks Over The Same Map

Both traces use the map with five huts: hut 0 leads to 1 and 2, hut 1 leads to 3, hut 2 leads to 3 and 4, and huts 3 and 4 lead nowhere. The target is hut 3, and hut 4 is a dead end. The cells list the huts in order and the pointer `hut` marks the end of the working path. In the first trace a step is shown whenever a hut is entered and whenever a call returns and the undo step runs, so the vars show the list growing and shrinking, and hut 3 is reached twice, once from hut 1 and once from hut 2.

```trace
{"cells":[0,1,2,3,4],"pointers":["hut"],"steps":[{"at":{"hut":0},"vars":{"path":"0","found":0,"cards":"none"},"note":"The walk starts at hut 0 with the working path holding only that hut."},{"at":{"hut":3},"vars":{"path":"0>1>3","found":1,"cards":"0>1>3"},"note":"Hut 3 is the target, so a copy of the working path 0>1>3 is stored as card 1."},{"at":{"hut":1},"vars":{"path":"0>1","found":1,"cards":"0>1>3"},"note":"Back at hut 1, the undo step removes hut 3, leaving the working path 0>1."},{"at":{"hut":0},"vars":{"path":"0","found":1,"cards":"0>1>3"},"note":"Back at hut 0, the undo step removes hut 1, leaving the working path 0."},{"at":{"hut":3},"vars":{"path":"0>2>3","found":2,"cards":"0>1>3 | 0>2>3"},"note":"Hut 3 is the target, so a copy of the working path 0>2>3 is stored as card 2."},{"at":{"hut":2},"vars":{"path":"0>2","found":2,"cards":"0>1>3 | 0>2>3"},"note":"Back at hut 2, the undo step removes hut 3, leaving the working path 0>2."},{"at":{"hut":4},"vars":{"path":"0>2>4","found":2,"cards":"0>1>3 | 0>2>3"},"note":"Hut 4 has no trails and is not the target, so the call returns with nothing stored."},{"at":{"hut":2},"vars":{"path":"0>2","found":2,"cards":"0>1>3 | 0>2>3"},"note":"Back at hut 2, the undo step removes hut 4, leaving the working path 0>2."},{"at":{"hut":0},"vars":{"path":"0","found":2,"cards":"0>1>3 | 0>2>3"},"note":"Back at hut 0, the undo step removes hut 2, leaving the working path 0."}]}
```

The second trace runs the same map with the false friend added, a single set of huts that are marked used the first time they are entered and never released. The walk reaches hut 3 through hut 1 and records one card. When it later goes down from hut 2, hut 3 is already marked, so the trail is skipped and the second card never appears. The answer is one card instead of two, with no error raised.

```trace
{"cells":[0,1,2,3,4],"pointers":["hut"],"steps":[{"at":{"hut":0},"vars":{"path":"0","found":0,"used":"0"},"note":"Hut 0 is entered and marked used."},{"at":{"hut":1},"vars":{"path":"0>1","found":0,"used":"0,1"},"note":"Hut 1 is entered and marked used."},{"at":{"hut":3},"vars":{"path":"0>1>3","found":1,"used":"0,1,3"},"note":"Hut 3 is the target and is marked used, and card 1 is stored as 0>1>3."},{"at":{"hut":2},"vars":{"path":"0>2","found":1,"used":"0,1,2,3"},"note":"Hut 2 is entered and marked used."},{"at":{"hut":2},"vars":{"path":"0>2","found":1,"used":"0,1,2,3"},"note":"At hut 2, the trail to hut 3 is skipped because hut 3 is already marked used, so a valid route is lost."},{"at":{"hut":4},"vars":{"path":"0>2>4","found":1,"used":"0,1,2,3,4"},"note":"Hut 4 is entered and marked used."},{"at":{"hut":-1},"vars":{"path":"0","found":1,"used":"0,1,2,3,4"},"note":"The walk ends with 1 card, while the correct answer from the first trace is 2."}]}
```

<!-- stage: code -->
### Append, Recurse, Remove

```java
static List<List<Integer>> allRoutes(int[][] trails, int from, int to) {
    List<List<Integer>> found = new ArrayList<>();
    List<Integer> path = new ArrayList<>();
    path.add(from);
    walk(trails, from, to, path, found);
    return found;
}

static void walk(int[][] trails, int hut, int to, List<Integer> path, List<List<Integer>> found) {
    if (hut == to) {
        found.add(new ArrayList<>(path));
        return;
    }
    for (int next : trails[hut]) {
        path.add(next);
        walk(trails, next, to, path, found);
        path.remove(path.size() - 1);
    }
}
```

The target check comes before the loop, so the walk stops there, and a dead end falls through an empty loop and returns with nothing recorded. The work is bounded by the walks the recursion makes, each costing a copy of at most n huts when it succeeds, so the total is O(P * n) for P cards plus the steps spent in dead branches. Space beyond the output is O(n) for the list and the call stack.

<!-- stage: applicability -->
### When Every Route Must Be Listed

Use this model when the answer is the routes themselves: all ways through a maze of one-way corridors, every dependency chain between two build steps, every sequence of connecting flights. The cue is a request for each path, not a yes or a count. What has to hold in every variant is the invariant that the working list equals the chain of open calls, which is why each append is paired with one removal on every exit from the loop.

The false friend is the visited set from earlier lessons. It answers "have I been here" and is right when each vertex needs handling once, but in a one-way network it throws away routes that share a hut. Also keep the output in mind: a chain of k diamonds has 2^k routes, so enumeration is the wrong tool when the question needs only a count or a reachability answer, since those can be had without listing anything. In Java, never add `path` itself to the result, and never call `path.remove(v)` with an `int` vertex, because on a `List<Integer>` that removes the entry at index v, not the hut v.

<!-- stage: exercises -->
### Exercises

#### [Build] Paths In A Tiny DAG (Author exercise)
<!-- id: gt-tiny-dag-paths -->

**Prerequisites.** The append, recurse and undo pattern from this lesson.

**Problem.** The `graph` is an array where `graph[v]` lists the vertices that vertex `v` has a one-way edge to, and the graph has no cycles. Given vertices `from` and `to`, return every path from `from` to `to`, each written as its vertices joined by single spaces, such as `"1 0 2 3"`. The routes come in the order the search finds them, trying the neighbors of each vertex in the order they are listed. The input is not modified.

**Constraints.** The graph has 2 to 8 vertices numbered from 0, there are no repeated edges, and `from` differs from `to`.

**Example 1.** Input `graph = [[1,2],[3],[3],[]], from = 0, to = 3`, output `["0 1 3", "0 2 3"]`.

**Example 2.** Input `graph = [[2],[0,2],[3],[]], from = 1, to = 3`, output `["1 0 2 3", "1 2 3"]`.

**Hint.** What must be true of the working list at the moment the loop moves on to the next neighbor?

**Changed decision.** The paths are recorded as finished strings in search order, so the order of the neighbor lists decides the order of the output.

#### [Vary] All Paths From Source To Target (LeetCode 797)
<!-- id: gt-all-paths-source-target -->

**Prerequisites.** The Paths In A Tiny DAG rung.

**Problem.** The `graph` is an adjacency array of a directed graph with no cycles on vertices `0` to `n - 1`. Return every path from vertex `0` to vertex `n - 1` as a list of vertices, in any order. The contract is that each returned list is independent, so changing one never changes another.

**Constraints.** 2 <= n <= 12 and edges point only to other vertices, with no repeated edges and no self loops.

**Example 1.** Input `graph = [[1,2,3],[3],[1,3],[]]`, output `[[0,1,3],[0,2,1,3],[0,2,3],[0,3]]` in any order.

**Example 2.** Input `graph = [[1],[2],[3],[4],[]]`, output `[[0,1,2,3,4]]`.

**Hint.** What goes wrong later if the result keeps a reference to the working list instead of a copy?

**Changed decision.** The lists are stored as copies taken at the target, so the contract of independent results replaces the string output of the previous rung.

#### [Boundary] Dead End And Direct Edge (Author exercise)
<!-- id: gt-dead-end-direct-edge -->

**Prerequisites.** The All Paths From Source To Target rung.

**Problem.** The `graph` is an adjacency array with no cycles, and `from` and `to` are vertices that may be equal. Return every path from `from` to `to` as a list of vertices, in any order. When the two are equal the only path is the single vertex. When `to` cannot be reached the answer is an empty list. Only complete paths ending at `to` are recorded, so a vertex with no outgoing edge that is not `to` contributes nothing.

**Constraints.** The graph has 1 to 8 vertices numbered from 0 and no repeated edges, and the input is not modified.

**Example 1.** Input `graph = [[1,3],[2],[],[]], from = 0, to = 3`, output `[[0,3]]`.

**Example 2.** Input `graph = [[1],[],[1]], from = 0, to = 2`, output `[]`.

**Hint.** Is reaching a vertex with an empty neighbor list the same event as reaching the target?

**Changed decision.** A path is recorded when the current vertex is the target, never because the vertex has no neighbors, and a start equal to the target is recorded immediately.

#### [Recognize] Enumerate Simple Paths (Author exercise)
<!-- id: gt-simple-paths -->

**Prerequisites.** The Dead End And Direct Edge rung.

**Problem.** The `graph` is an adjacency array of a directed graph that may contain cycles, including pairs of vertices that point at each other and self loops. Given `from` and `to`, return every simple path from `from` to `to`, meaning a path in which no vertex appears twice, as lists of vertices in any order. The input is not modified.

**Constraints.** The graph has 2 to 8 vertices numbered from 0, no edge is listed twice, and `from` differs from `to`.

**Example 1.** Input `graph = [[1,2],[0,2,3],[1,3],[]], from = 0, to = 3`, output `[[0,1,2,3],[0,1,3],[0,2,1,3],[0,2,3]]` in any order.

**Example 2.** Input `graph = [[1],[2,0],[1,3],[]], from = 0, to = 3`, output `[[0,1,2,3]]`.

**Hint.** With cycles present, which vertices are forbidden at a given moment, and when does a vertex stop being forbidden?

**Changed decision.** A vertex is marked when the walk enters it and unmarked when the call leaves it, so the marks describe the current path and never a past one.
