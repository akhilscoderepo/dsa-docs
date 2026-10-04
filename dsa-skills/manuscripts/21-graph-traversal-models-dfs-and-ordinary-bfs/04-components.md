<!-- lesson-kind: standard -->
<!-- lesson-id: components -->
## Components

<!-- stage: context -->
### The Phone Trees Of Alder Court

Alder Court is a block of flats where news travels by telephone. Each resident has the numbers of a few neighbors and rings them when something happens, whether the lift is broken or the baker has sold out. Nobody keeps a list of the whole block. Last winter the caretaker, Mrs. Okafor, wanted to post a notice and asked herself a plain question: how many separate circles of gossip are there in this building? If she told one person in every circle, the whole block would know by evening.

She has a notebook of seven or eight hundred pairs of residents who ring each other. Some circles are large, with a dozen flats chatting through the same grapevine. Some are a lone tenant who never picks up the phone. She cannot tell by looking which flats are linked through a long chain of friends, and she does not want to ring a stranger and ask.

<!-- stage: naive -->
### Ask About Every Pair Of Flats

The direct method answers one small question at a time: can news starting at flat a ever reach flat b? It builds the neighbor lists once, runs a fresh search from a for every question, and then counts the flats that are the first of their circle. A flat is the first of its circle when no lower-numbered flat can reach it.

```java
static boolean reaches(List<List<Integer>> adj, int a, int b) {
    boolean[] seen = new boolean[adj.size()];
    Deque<Integer> stack = new ArrayDeque<>();
    stack.push(a);
    seen[a] = true;
    while (!stack.isEmpty()) {
        int v = stack.pop();
        if (v == b) return true;
        for (int w : adj.get(v)) {
            if (!seen[w]) { seen[w] = true; stack.push(w); }
        }
    }
    return false;
}

static int countCircles(List<List<Integer>> adj) {
    int firsts = 0;
    for (int b = 0; b < adj.size(); b++) {
        boolean first = true;
        for (int a = 0; a < b && first; a++) {
            if (reaches(adj, a, b)) first = false;
        }
        if (first) firsts++;
    }
    return firsts;
}
```

The method is easy to trust, because each question is answered from scratch and nothing is remembered between questions. It is correct for any building, including one where every tenant is alone or where everyone is linked.

<!-- stage: bottleneck -->
### Every Question Starts The Search Over

One call of `reaches` costs O(V + E), since in the worst case it visits every flat and every neighbor entry. The counting loop asks it for up to V * (V - 1) / 2 pairs, so the total is O(V^2 * (V + E)). For a block of a thousand flats and eight hundred pairs that is about five hundred thousand searches, each rereading most of a circle that an earlier search already walked completely.

The waste is that the answer to one search says a lot more than the single yes or no that was asked. A search from flat a that finishes has visited every flat of a's whole circle, so it already knows which flats are linked with a. A better method should keep what a search has learned and never start a second search inside a circle that has been walked once.

<!-- stage: insight -->
### One Search Per Unvisited Flat

Keep a single array of visited marks for the whole run, and never clear it between searches. Then walk the flats in order in an **outer loop**. When the loop meets a flat that is still unmarked, no earlier search reached it, so it must belong to a circle nobody has seen yet. Run one search from it that marks every flat it can reach, and add one to the tally. When the loop meets a flat that is already marked, it belongs to a circle already counted, so it does nothing.

Each such circle is one **component**: a maximal group of vertices in which every vertex can reach every other one through edges, and which no further edge joins to anything outside. The searches never overlap, because a search stops at marked flats, so the total work is one visit per vertex and one look per edge end, which is O(V + E) for the whole building instead of one search per pair.

The visited marks are the only memory the method needs, and they are the reason it stays linear. The same loop also gives more than a count for free. The number of flats a single search marks is the size of that circle, so recording it before the next start gives the sizes in the order the circles were found.

The invariant is that every outer-loop start on an unmarked vertex discovers exactly one new component, and after it finishes every vertex of that component is marked.

<!-- names: outer loop, component, visited marks -->

<!-- stage: variables -->
### Marks, Starts And Tallies

The count `n` fixes the flats as the numbers 0 to n - 1, and `adj` holds the neighbor list of each. The array `seen` is the visited marks, created once before the loop and shared by every search. The loop variable `s` is the start being considered. The counter `components` is how many unmarked starts have been found so far, and `size` counts the vertices marked by the search currently running, which is stored at the moment that search ends. A stack holds the vertices that are marked but whose neighbors have not yet been looked at.

<!-- stage: trace -->
### Two Runs Over Seven Flats

The first trace counts the circles of a building with seven flats and the pairs 0-1, 1-2 and 3-4. The pointer `s` is the start the outer loop is looking at, `components` is the tally so far, and `seen` is how many flats are marked. Flats 0, 3, 5 and 6 each begin a new circle, while 1, 2 and 4 are skipped because an earlier search already marked them. The final tally is 4.

```trace
{"cells":["0","1","2","3","4","5","6"],"pointers":["s"],"steps":[{"at":{"s":0},"vars":{"components":1,"seen":3},"note":"Vertex 0 is unmarked, so a new search starts here, reaches 3 vertices, and the tally becomes 1."},{"at":{"s":1},"vars":{"components":1,"seen":3},"note":"Vertex 1 is already marked by an earlier search, so the loop skips it and the tally stays 1."},{"at":{"s":2},"vars":{"components":1,"seen":3},"note":"Vertex 2 is already marked by an earlier search, so the loop skips it and the tally stays 1."},{"at":{"s":3},"vars":{"components":2,"seen":5},"note":"Vertex 3 is unmarked, so a new search starts here, reaches 2 vertices, and the tally becomes 2."},{"at":{"s":4},"vars":{"components":2,"seen":5},"note":"Vertex 4 is already marked by an earlier search, so the loop skips it and the tally stays 2."},{"at":{"s":5},"vars":{"components":3,"seen":6},"note":"Vertex 5 is unmarked, so a new search starts here, reaches 1 vertices, and the tally becomes 3."},{"at":{"s":6},"vars":{"components":4,"seen":7},"note":"Vertex 6 is unmarked, so a new search starts here, reaches 1 vertices, and the tally becomes 4."}]}
```

The second trace uses six flats with the pairs 0-3, 3-5 and 1-4, and it records the size of each circle. The variable `size` is the number of vertices the search from the current start marked, or 0 when the start was skipped. The sizes found, in order, are 3, 2 and 1, and they add up to 6, so every flat was counted in exactly one circle.

```trace
{"cells":["0","1","2","3","4","5"],"pointers":["s"],"steps":[{"at":{"s":0},"vars":{"size":3,"sizes":"3"},"note":"Vertex 0 is unmarked, so its search marks 3 vertices and 3 is added to the sizes."},{"at":{"s":1},"vars":{"size":2,"sizes":"3,2"},"note":"Vertex 1 is unmarked, so its search marks 2 vertices and 2 is added to the sizes."},{"at":{"s":2},"vars":{"size":1,"sizes":"3,2,1"},"note":"Vertex 2 is unmarked, so its search marks 1 vertices and 1 is added to the sizes."},{"at":{"s":3},"vars":{"size":0,"sizes":"3,2,1"},"note":"Vertex 3 is already marked, so no search runs and the size is 0."},{"at":{"s":4},"vars":{"size":0,"sizes":"3,2,1"},"note":"Vertex 4 is already marked, so no search runs and the size is 0."},{"at":{"s":5},"vars":{"size":0,"sizes":"3,2,1"},"note":"Vertex 5 is already marked, so no search runs and the size is 0."}]}
```

<!-- stage: code -->
### Counting And Measuring Circles

```java
static List<Integer> circleSizes(int n, List<List<Integer>> adj) {
    boolean[] seen = new boolean[n];
    List<Integer> sizes = new ArrayList<>();
    for (int s = 0; s < n; s++) {
        if (seen[s]) continue;
        int size = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(s);
        seen[s] = true;
        while (!stack.isEmpty()) {
            int v = stack.pop();
            size++;
            for (int w : adj.get(v)) {
                if (!seen[w]) { seen[w] = true; stack.push(w); }
            }
        }
        sizes.add(size);
    }
    return sizes;
}
```

The count of components is `sizes.size()`. A vertex is marked when it is pushed, not when it is popped, so it can never be pushed twice. The loop runs in O(n + E) time and uses O(n) extra space for the marks and the stack.

<!-- stage: applicability -->
### Counting Groups In A Split Graph

Use this loop when the graph may be split into several pieces and the answer counts or summarizes the maximal reachable groups: the number of friend circles, the size of the largest island, whether a network is fully connected, or how many wires must be added to join everything. Hold on to the invariant that an unmarked start always begins a group nobody has seen, and a finished search leaves its whole group marked.

The nearest false friend is a single search from vertex zero. It looks like a complete traversal, yet it only reaches the group of vertex zero and silently misses every other group, so a count based on it is wrong whenever the graph is not connected. A second false friend is counting vertices with no edges, which finds only the lone ones and ignores groups of two or more.

There is no use for this loop when the graph is known to be connected, or when the question depends on distances or on the order of discovery rather than on which group a vertex is in. In Java, a recursive depth-first search on a long chain of vertices needs one call frame per vertex of the chain, and that can overflow the call stack on large inputs. The loop above keeps its own stack on the heap instead, which is the safer alternative when the input may be a long path.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Components (Author exercise)
<!-- id: gt-count-components -->

**Prerequisites.** The adjacency list rung and a search that marks everything it reaches.

**Problem.** A network has `n` vertices labeled from `0` up to `n - 1`, and each entry of `edges` is an undirected link between two of them. Return the number of connected components, where a vertex with no edge is a component of its own.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 5000, with no repeated pair and no pair joining a vertex to itself.

**Example 1.** Input `n = 7, edges = [[0,1],[1,2],[3,4]]`, output `4`.

**Example 2.** Input `n = 6, edges = [[0,5],[2,3],[3,4]]`, output `3`.

**Hint.** What does it mean when the outer loop reaches a vertex that is not yet marked, and what must the search do before the loop moves on?

**Changed decision.** The visited marks are shared across all starts, so one search runs per component rather than one per vertex.

#### [Vary] Component Sizes (Author exercise)
<!-- id: gt-component-sizes -->

**Prerequisites.** The Count Components rung.

**Problem.** With the same input, return an array holding the number of vertices reached by each start that the outer loop launches. Starts are tried in increasing vertex order, so the array lists the components in order of their smallest vertex.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 5000, with no repeated pair and no self pair.

**Example 1.** Input `n = 7, edges = [[0,1],[1,2],[3,4]]`, output `[3,2,1,1]`.

**Example 2.** Input `n = 6, edges = [[0,5],[2,3],[3,4]]`, output `[2,1,3]`.

**Hint.** Where does a counter have to be reset, and when is its value written down?

**Changed decision.** The answer records the size of each search, so a counter restarts at every launched start and is stored when that search ends.

#### [Boundary] No Edges And One Component (Author exercise)
<!-- id: gt-no-edges-one -->

**Prerequisites.** The Component Sizes rung.

**Problem.** Return an array of two numbers: the count of components and the size of the largest one. The inputs of interest are the extremes, a graph with no edges at all, where every vertex stands alone, and a graph in which every pair of vertices is joined, where a single start reaches everything.

**Constraints.** 1 <= n <= 300, 0 <= edges.length <= 5000, with no repeated pair and no self pair.

**Example 1.** Input `n = 4, edges = []`, output `[4,1]`.

**Example 2.** Input `n = 4, edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]`, output `[1,4]`.

**Hint.** What does the outer loop do when no vertex has a neighbor, and how many starts does it launch when the first search reaches everyone?

**Changed decision.** Empty neighbor lists must exist for every vertex, so isolated vertices are counted, and a dense graph still launches only one search.

#### [Recognize] Number Of Provinces (LeetCode 547)
<!-- id: gt-provinces -->

**Prerequisites.** The Count Components rung and the adjacency matrix from graph representation.

**Problem.** There are `n` cities. The input is an `n` by `n` matrix `isConnected` in which `isConnected[i][j]` is `1` when city `i` and city `j` are directly connected and `0` otherwise, and a city is always connected to itself. A province is a group of cities connected directly or through other cities, with no link to any city outside it. Return the number of provinces.

**Constraints.** 1 <= n <= 200, every entry is 0 or 1, the matrix is symmetric, and the diagonal is all ones.

**Example 1.** Input `isConnected = [[1,1,0,0],[1,1,0,0],[0,0,1,0],[0,0,0,1]]`, output `3`.

**Example 2.** Input `isConnected = [[1,0,1],[0,1,0],[1,0,1]]`, output `2`.

**Hint.** The matrix is already the graph, so which cells of a row give the neighbors of a city?

**Changed decision.** Neighbors are read from a matrix row instead of a list, so each search costs O(n * n) in total and no lists are built.
