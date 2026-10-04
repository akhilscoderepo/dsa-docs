<!-- lesson-kind: standard -->
<!-- lesson-id: bipartite-coloring -->
## Bipartite Coloring

<!-- stage: context -->
### Two Tables At Hartwell Grange

Mirela is the caterer for a family reunion at Hartwell Grange, and the hall has room for exactly two long tables. The hosts hand her a sheet of names with one awkward note: certain pairs of guests have not spoken since a disputed will, a borrowed tractor, or a wedding toast that went wrong, and those pairs must never share a table. Everyone else may sit anywhere.

Mirela can tell at a glance that a few guests are easy, such as an aunt who quarrels with one cousin only. She cannot tell whether the whole sheet can be satisfied at all. Her question is exact. Is there some way to put every guest at table one or table two so that no feuding pair ends up together, and if there is, which table does each guest get?

<!-- stage: naive -->
### Try Every Seating Plan

The plain approach is to settle the question by exhaustion. Give each of the n guests a table, one or two, which makes 2^n complete plans. Test each plan against the sheet, and stop at the first plan in which no feuding pair sits together. If every plan fails, the sheet cannot be satisfied.

```java
static int[] seatByTrying(int n, int[][] feuds) {
    for (int plan = 0; plan < (1 << n); plan++) {
        boolean ok = true;
        for (int[] pair : feuds) {
            int a = (plan >> pair[0]) & 1, b = (plan >> pair[1]) & 1;
            if (a == b) { ok = false; break; }
        }
        if (ok) {
            int[] table = new int[n];
            for (int g = 0; g < n; g++) table[g] = (plan >> g) & 1;
            return table;
        }
    }
    return new int[0];
}
```

This is correct for any sheet small enough for an int bit mask, since it looks at every possible plan, and a plan that survives the test is a valid seating by definition. An empty array reports that no plan works.

<!-- stage: bottleneck -->
### Plans Double With Every Guest

With n guests there are 2^n plans, and each is checked against all m feuding pairs, so the worst case costs O(2^n * m). A sheet of 30 guests already means a billion plans, and a reunion of 60 means more plans than anyone could check in a lifetime. The trouble gets worse in the very case that matters most, a sheet with no valid seating, because then every plan has to be tried and rejected.

The waste is plain once you look at what a plan really decides. Suppose guest 0 is placed at table one. Every guest who feuds with guest 0 is then forced to table two, and everyone who feuds with those guests is forced back to table one, and so on outward. Inside a group of linked quarrels there is never a free choice after the first guest. Plans that disagree with a forced seat are rejected by the same single pair, again and again, across billions of plans.

<!-- stage: insight -->
### Alternate Colors Along Every Edge

Treat guests as vertices and each feuding pair as an edge, and call the two tables **parity colors**, 0 and 1. Walk outward from one guest with a queue, exactly as ordinary BFS does. The first guest is given color 0. Each time a guest is taken off the queue, every neighbor that has no color yet receives the opposite color, 1 minus the current one, and joins the queue. Nothing is guessed, so each guest is colored exactly once and the work is a single pass over the edges.

The test happens on the other branch. When a neighbor already has a color, nothing is assigned. Instead the colors of the two ends are compared. Different colors are what the sheet asks for, so the edge is fine. Equal colors mean that two feuding guests are forced onto the same table, and the answer is no, since every color so far was forced by the start. Such a **conflict edge** is not an accident of the order in which guests are visited. It only exists when the graph holds an **odd cycle**, a ring of feuds with an odd number of guests, because colors alternate around a ring and an odd ring cannot close up with the first color matching the last. A graph has a valid two-table seating exactly when it has no odd cycle.

One start only covers the guests linked to it by feuds. A guest with no feud at all, or a second group of quarrels cut off from the first, is never reached, so the outer loop must try every guest and begin a fresh search at each one that is still uncolored.

The invariant is that every colored vertex has a color different from that of the neighbor that colored it, and the vertices already compared against their neighbors have shown no equal pair.

<!-- names: parity colors, conflict edge, odd cycle -->

<!-- stage: variables -->
### Colors, Queue And Start

The array `adj` lists the feuding neighbors of each guest, and `color` holds one entry per guest, with `-1` for not yet seated, and 0 or 1 for a table. The loop variable `start` walks every guest and launches a search at each one that is still `-1`. The queue `line` holds colored guests whose neighbors have not been looked at, `u` is the guest just taken from it, and `v` is a neighbor being tried. Reading `color[u]` tells what the neighbor should not have, and `1 - color[u]` is what an unseated neighbor receives.

<!-- stage: trace -->
### One Clean Run And One Clash

The first trace colors a connected graph of six guests, stored as the color array itself, where `-1` means unseated. The edges are 0-1, 0-2, 1-3, 2-3, 2-5 and 3-4, which form a single four-ring of guests 0, 1, 3 and 2 with two tails. The pointer `cur` is the guest just taken from the queue. The vars show the queue after that guest is expanded, and the note records whether a neighbor was newly colored or merely compared. Guest 3 meets guest 2 already colored, and the two colors differ, so the edge passes the test.

```trace
{"cells":[0,1,1,0,1,0],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"queue":"1,2","seated":3},"note":"Guest 0 with color 0 is taken from the queue and colors guest 1 with 1, guest 2 with 1."},{"at":{"cur":1},"vars":{"queue":"2,3","seated":4},"note":"Guest 1 with color 1 is taken from the queue and colors guest 3 with 0 and compares guest 0 (colors differ)."},{"at":{"cur":2},"vars":{"queue":"3,5","seated":5},"note":"Guest 2 with color 1 is taken from the queue and colors guest 5 with 0 and compares guest 0 (colors differ), guest 3 (colors differ)."},{"at":{"cur":3},"vars":{"queue":"5,4","seated":6},"note":"Guest 3 with color 0 is taken from the queue and colors guest 4 with 1 and compares guest 1 (colors differ), guest 2 (colors differ)."},{"at":{"cur":5},"vars":{"queue":"4","seated":6},"note":"Guest 5 with color 0 is taken from the queue and compares guest 2 (colors differ)."},{"at":{"cur":4},"vars":{"queue":"empty","seated":6},"note":"Guest 4 with color 1 is taken from the queue and compares guest 3 (colors differ)."}]}
```

The second trace runs the outer loop on seven guests with edges 0-1, 1-2, 3-4, 4-5 and 5-3. The first component is a path and the second is a ring of three, so the second has an odd cycle. The pointer `cur` again marks the guest taken from the queue, and the vars include the number of searches begun. Search 1 ends after guest 2, the scan skips every guest that is already colored, and search 2 starts at guest 3, which is where the first search could never have gone. The run stops when the ring of three forces guests 4 and 5 to share color 1.

```trace
{"cells":[0,1,0,0,1,1,-1],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"searches":1,"queue":"1"},"note":"Search 1: guest 0 with color 0 is expanded and colors guest 1 with 1."},{"at":{"cur":1},"vars":{"searches":1,"queue":"2"},"note":"Search 1: guest 1 with color 1 is expanded and colors guest 2 with 0."},{"at":{"cur":2},"vars":{"searches":1,"queue":"empty"},"note":"Search 1: guest 2 with color 0 is expanded with nothing new to color."},{"at":{"cur":3},"vars":{"searches":2,"queue":"4,5"},"note":"Search 2: guest 3 with color 0 is expanded and colors guest 4 with 1, guest 5 with 1."},{"at":{"cur":4},"vars":{"searches":2,"queue":"5"},"note":"Guest 4 with color 1 meets guest 5, which also has color 1, so the answer is false."}]}
```

<!-- stage: code -->
### Seating With A Queue

```java
final class Banquet {
    static boolean canSeat(int[][] adj) {
        int n = adj.length;
        int[] color = new int[n];
        Arrays.fill(color, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        for (int start = 0; start < n; start++) {
            if (color[start] != -1) continue;
            color[start] = 0;
            line.add(start);
            while (!line.isEmpty()) {
                int u = line.poll();
                for (int v : adj[u]) {
                    if (color[v] == -1) {
                        color[v] = 1 - color[u];
                        line.add(v);
                    } else if (color[v] == color[u]) {
                        return false;
                    }
                }
            }
        }
        return true;
    }
}
```

The check `color[v] == color[u]` also fires for a vertex that lists itself as a neighbor, since a guest cannot differ from itself. Each vertex joins the queue once and each adjacency entry is read once, so the time is O(V + E), and the color array plus the queue take O(V) space.

<!-- stage: applicability -->
### Splits, Teams And Rivalries

Look for this model when a set of items must be divided into exactly two groups and certain pairs may not stay together: rival teams, reviewers and authors who must not overlap, jobs that need two machines with no clash, or a dodgeball class split so that no two people on the same side are feuding. The same question appears with other words, such as whether a graph can be drawn with every edge crossing between two sides. The invariant to defend is that no colored vertex ever shares a color with the neighbor that colored it, and that every neighbor met a second time is compared before it is forgotten.

The most tempting false friend is checking a single connected component. A run from vertex 0 that ends cleanly says nothing about the guests it never reached, and a triangle in a far corner of the sheet will then be accepted by mistake. A second false friend is the idea that any cycle breaks the split: even rings are harmless, and only the odd ones do. A third is the belief that a conflict found late means the algorithm chose badly. It does not, because every color was forced.

The model does not fit when there are three or more groups, since k-coloring for three or more colors has no known fast method and a two-color check cannot answer it. In Java, remember that `new int[n]` is filled with 0, which is a real color here. If the color array is left at its defaults, every guest looks already seated at table one, so fill it with -1 before the first search.

<!-- stage: exercises -->
### Exercises

#### [Build] Color One Component (Author exercise)
<!-- id: gt-color-one-component -->

**Prerequisites.** The queue, the `color` array and the equal-color test from this lesson.

**Problem.** The input `adj` is the adjacency list of a connected undirected graph on vertices `0..n-1`, with no self-loops and no repeated edges. Run a breadth-first search from vertex 0, give vertex 0 the color 0, and give each newly reached vertex the opposite of the color of the vertex that reached it. Return the `int[]` of colors, or an empty array if some edge joins two vertices of the same color.

**Constraints.** 1 <= n <= 1000, the graph is connected, and every edge appears in both lists.

**Example 1.** Input `adj = [[1,2],[0,3],[0],[1]]`, output `[0,1,1,0]`.

**Example 2.** Input `adj = [[1,2],[0,2],[0,1]]`, output `[]`.

**Hint.** What does a neighbor that already has a color tell you, and what must you do with that color before moving on?

**Changed decision.** A colored neighbor is compared instead of skipped, so the traversal doubles as the validity test.

#### [Vary] Process Disconnected Components (Author exercise)
<!-- id: gt-disconnected-components -->

**Prerequisites.** The Color One Component rung and the components lesson.

**Problem.** The input is `n` and an edge list `edges` of pairs `[u, v]` for an undirected graph on vertices `0..n-1`, which may have several connected pieces and isolated vertices. Return the number of connected components if every component can be split into two groups with no edge inside a group, or -1 if any component has an odd cycle.

**Constraints.** 1 <= n <= 1000, no self-loops and no repeated edges, and 0 <= u, v < n.

**Example 1.** Input `n = 6, edges = [[0,1],[1,2],[3,4]]`, output `3`.

**Example 2.** Input `n = 5, edges = [[0,1],[2,3],[3,4],[4,2]]`, output `-1`.

**Hint.** Where is a new search launched, and what does the number of launches equal when no conflict appears?

**Changed decision.** The search is started from every uncolored vertex and counted, instead of once from vertex 0.

#### [Boundary] Self-Loop And Odd Cycle (Author exercise)
<!-- id: gt-self-loop-odd-cycle -->

**Prerequisites.** The Process Disconnected Components rung.

**Problem.** The input is `n` and an edge list `edges` of pairs `[u, v]`, now allowing `u == v` and repeated pairs. Return `true` if the vertices can be colored with two colors so that every edge has different colors at its ends, and `false` otherwise. A self-loop and any cycle with an odd number of vertices must both be rejected, and repeated pairs must not change the answer.

**Constraints.** 1 <= n <= 1000, 0 <= m <= 3000 edges, and 0 <= u, v < n.

**Example 1.** Input `n = 3, edges = [[0,1],[1,1]]`, output `false`.

**Example 2.** Input `n = 4, edges = [[0,1],[1,2],[2,3],[3,0],[0,1]]`, output `true`.

**Hint.** When a vertex is its own neighbor, what are the two colors being compared?

**Changed decision.** No new branch is added for a self-loop, because the equal-color test already fails when a vertex meets itself.

#### [Recognize] Is Graph Bipartite (LeetCode 785)
<!-- id: gt-is-graph-bipartite -->

**Prerequisites.** The Process Disconnected Components rung.

**Problem.** The input `graph` is an array of arrays where `graph[u]` lists the neighbors of vertex `u` in an undirected graph, so `v` is in `graph[u]` exactly when `u` is in `graph[v]`. Return `true` if the vertices can be divided into two sets so that every edge joins a vertex of one set to a vertex of the other, and `false` otherwise. The graph may be disconnected.

**Constraints.** 1 <= n <= 100, no self-loops and no repeated neighbors, and the lists are symmetric.

**Example 1.** Input `graph = [[2,3],[3],[0],[0,1],[]]`, output `true`.

**Example 2.** Input `graph = [[1],[0],[3,4],[2,4],[2,3]]`, output `false`.

**Hint.** If the search from vertex 0 finishes without a clash, can you stop, and what does Example 2 show?

**Changed decision.** The question is stated as splitting into two sets, so you must recognize it as two-coloring and run the search from every uncolored vertex.
