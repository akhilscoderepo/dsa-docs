<!-- lesson-kind: standard -->
<!-- lesson-id: graph-representation -->
## Graph Representation

<!-- stage: context -->
### The Route Slips Of Harbor Street

The ferry office on Harbor Street keeps its timetable as a shoebox of route slips. Each slip names two landings that one boat connects, such as Quay and Lighthouse, and nothing else. Passengers come to the window with questions that sound simple. Which landings can I reach in one hop from the Lighthouse? Is there a direct boat between the Mill and the Quay? How many boats call at the Fish Market?

The clerk answers every question by turning over slips. On a quiet day with twenty slips this is fine. On the day the regional ferry merges with the island company, the shoebox holds eight thousand slips, a queue stands at the window, and the clerk starts to wish that the slips had been sorted by landing, so that all the boats of one landing sat in one small pile.

<!-- stage: naive -->
### Scan The Whole Shoebox

The direct method keeps the slips exactly as they arrive, as a list of pairs, and answers each question by reading them all. To list the hops from one landing, it walks the pairs and collects the other end of every pair that mentions the landing.

```java
static List<Integer> hopsFrom(int[][] slips, int landing) {
    List<Integer> out = new ArrayList<>();
    for (int[] s : slips) {
        if (s[0] == landing) out.add(s[1]);
        else if (s[1] == landing) out.add(s[0]);
    }
    return out;
}
```

The method is correct for any slips, whatever their order, and it needs no preparation. It also handles the unlucky slip that names the same landing twice, because the first test already matches it, and the answer then contains that landing as a hop to itself.

<!-- stage: bottleneck -->
### Every Question Rereads Every Slip

One question costs O(E) for E slips, however few boats call at the landing, since the scan cannot know where the useful slips are. A search that visits every landing and asks for its hops at each one pays O(V * E) in total, which for a thousand landings and eight thousand slips is eight million slip reads for a task that only needed to touch each slip twice. The repeated work is the rereading of slips that were already read for another landing.

The flat list also hides a decision that the search cannot avoid. A slip names two landings, yet it is not said whether a boat sails both ways. The scan above silently assumes it does, and a one-way ferry would be reported as a hop in the wrong direction. A better arrangement should fix the question of direction once, when the slips are filed, and then answer each question by looking only at what belongs to the landing.

<!-- stage: insight -->
### File Each Slip Under Its Landing

Give every vertex its own pile and file each edge into the piles of the vertices it leaves. That arrangement is the **adjacency list**: an array of lists where position v holds exactly the neighbors reachable from v in one step. Asking for the hops of a landing is then the length of one pile, and a whole traversal reads each pile once, so the work is O(V + E) instead of O(V * E). An undirected edge is filed twice, once under each end, and a directed edge is filed once, under its tail only.

The other arrangement is the **adjacency matrix**: a square table in which the entry at row u and column v says whether an edge leads from u to v. It answers the question whether the Mill and the Quay are directly linked in one probe, which a list cannot do without searching a pile. The price is a table of V * V entries whatever the number of edges, and listing the hops of one landing means reading a full row of V cells, even when the landing has two boats.

A third quantity ties the two together. The **degree** of a vertex is the number of edge ends attached to it, which is the length of its pile in an undirected list. Summing all degrees counts every undirected edge twice, and that sum is the quickest sanity check that every edge was filed under both ends.

The invariant is that the pile of a vertex holds exactly the neighbors one step away from it, in the direction the input states, and holds a neighbor once per input edge unless the contract says edges may not repeat.

<!-- names: adjacency list, adjacency matrix, degree -->

<!-- stage: variables -->
### Piles, Rows And Degrees

The count `n` fixes the vertices as the numbers 0 to n - 1, which matters because a vertex with no edge still needs an empty pile. The array `adj` has one list per vertex and is filled in a single pass over the slips. The loop variable `e` is the slip being filed, with ends `u` and `v`. For a directed contract only `adj[u]` receives `v`, and for an undirected contract both `adj[u]` and `adj[v]` are updated. When a matrix is used instead, `has[u][v]` is a boolean that is set the same way, and `deg[v]` is a counter that rises once for each pile that receives an entry.

<!-- stage: trace -->
### Filing Three Slips

The first trace files an undirected network of four landings. The pointer `e` marks the slip being filed, and `total` is the number of entries now held across all piles. After the last slip the total is 6, which is twice the number of slips, so each undirected edge really was filed under both ends.

```trace
{"cells":["0-1","1-2","1-3"],"pointers":["e"],"steps":[{"at":{"e":0},"vars":{"total":2,"pile_u":"1","pile_v":"0"},"note":"The slip 0-1 is filed twice: vertex 1 joins the pile of 0 and vertex 0 joins the pile of 1, so 2 entries are held in all."},{"at":{"e":1},"vars":{"total":4,"pile_u":"0,2","pile_v":"1"},"note":"The slip 1-2 is filed twice: vertex 2 joins the pile of 1 and vertex 1 joins the pile of 2, so 4 entries are held in all."},{"at":{"e":2},"vars":{"total":6,"pile_u":"0,2,3","pile_v":"1"},"note":"The slip 1-3 is filed twice: vertex 3 joins the pile of 1 and vertex 1 joins the pile of 3, so 6 entries are held in all."}]}
```

The second trace files three one-way boats on four landings into a matrix. Here the count `ones` is the number of true cells, and it matches the number of slips because each directed slip sets one cell. Landing 3 has no slip at all, and its row stays empty without any special case.

```trace
{"cells":["0>1","2>1","1>3"],"pointers":["e"],"steps":[{"at":{"e":0},"vars":{"ones":1,"row_u":"0100"},"note":"The one-way slip 0>1 sets only the cell in row 0 and column 1, so row 0 now reads 0100 and 1 cells are true."},{"at":{"e":1},"vars":{"ones":2,"row_u":"0100"},"note":"The one-way slip 2>1 sets only the cell in row 2 and column 1, so row 2 now reads 0100 and 2 cells are true."},{"at":{"e":2},"vars":{"ones":3,"row_u":"0001"},"note":"The one-way slip 1>3 sets only the cell in row 1 and column 3, so row 1 now reads 0001 and 3 cells are true."}]}
```

<!-- stage: code -->
### Building The Piles

```java
final class Network {
    static List<List<Integer>> undirected(int n, int[][] slips) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : slips) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        return adj;
    }

    static boolean[][] matrix(int n, int[][] slips) {
        boolean[][] has = new boolean[n][n];
        for (int[] e : slips) has[e[0]][e[1]] = true;
        return has;
    }
}
```

Creating the piles first, one per vertex, is what keeps isolated vertices alive. Filing is O(n + E), and the matrix needs O(n * n) cells even when E is tiny. A self edge `[v, v]` is filed twice into the same pile by the undirected method, which is why the degree rule for it has to be written down.

<!-- stage: applicability -->
### Arbitrary Links Between Things

Reach for a graph when relationships are arbitrary links rather than a single parent or a single next pointer: road maps, friendship lists, course prerequisites, dependency files, and the cells of a board once they are treated as vertices. The first decision is always the contract. State whether edges are directed, whether vertices are numbered from zero, and whether an edge may repeat or point at its own tail, because every later traversal inherits that choice. The invariant to keep in sight is that each pile contains one entry per stated edge end.

The nearest false friend is the adjacency matrix for a sparse network. A road map with a hundred thousand junctions and two hundred thousand roads fits in a list of a few hundred thousand entries, while a matrix would need ten billion cells and cannot even be allocated. A second false friend is a list of pairs sorted by first end, which looks filed yet still needs a search for the second end of an undirected edge.

There is no gain from a list when the question is a heavy stream of edge existence probes on a small dense graph, where the matrix is the better choice. In Java, prefer `List<Integer>[]` or `ArrayList<List<Integer>>` filled in a loop, and never create the piles with `Collections.nCopies`, which would place one shared list at every position.

<!-- stage: exercises -->
### Exercises

#### [Build] Undirected Adjacency Lists (Author exercise)
<!-- id: gt-undirected-lists -->

**Prerequisites.** The idea of a pile of neighbors per vertex.

**Problem.** The network has `n` landings labelled `0` through `n - 1`, and `edges` lists undirected edges as pairs. Return the adjacency lists as a list of `n` lists, where each list holds the neighbors of its vertex in the order that the edges arrived. Every edge appears in the lists of both of its ends.

**Constraints.** 1 <= n <= 100, 0 <= edges.length <= 300, no edge repeats and no edge joins a vertex to itself.

**Example 1.** Input `n = 4, edges = [[0,1],[1,2],[1,3]]`, output `[[1],[0,2,3],[1],[1]]`.

**Example 2.** Input `n = 3, edges = [[2,0],[1,2]]`, output `[[2],[2],[0,1]]`.

**Hint.** How many lists receive a new entry for one input edge, and when are the lists created?

**Changed decision.** Both ends of every edge receive an entry, so the entries across all lists equal twice the number of edges.

#### [Vary] Directed Adjacency Lists (Author exercise)
<!-- id: gt-directed-lists -->

**Prerequisites.** The Undirected Adjacency Lists rung.

**Problem.** The same input describes directed edges, where the pair `[u, v]` is a one-way link from `u` to `v`. Return the adjacency lists in the order the edges arrived, and keep an empty list for every vertex with no outgoing edge, including a vertex that appears in no edge at all.

**Constraints.** 1 <= n <= 100, 0 <= edges.length <= 300, no pair repeats.

**Example 1.** Input `n = 4, edges = [[0,1],[2,1],[1,3]]`, output `[[1],[3],[1],[]]`.

**Example 2.** Input `n = 5, edges = [[3,0],[3,4]]`, output `[[],[],[],[0,4],[]]`.

**Hint.** Which end of a pair owns the entry, and what must a vertex that never starts an edge still own?

**Changed decision.** Only the tail of a directed edge receives an entry, and the list for every vertex exists before any edge is read.

#### [Boundary] Parallel And Self Edges (Author exercise)
<!-- id: gt-parallel-and-self -->

**Prerequisites.** The Directed Adjacency Lists rung.

**Problem.** The input is an undirected network in which the same pair may be listed several times in either order and an edge may join a vertex to itself. The contract treats the network as simple, so repeated edges count once and a self edge is ignored. Return an array with the number of distinct neighbors of each vertex.

**Constraints.** 1 <= n <= 60, 0 <= edges.length <= 400, vertices are numbers from 0 to n - 1.

**Example 1.** Input `n = 3, edges = [[0,1],[1,0],[2,2]]`, output `[1,1,0]`.

**Example 2.** Input `n = 4, edges = [[0,1],[0,1],[0,2],[3,3],[3,0]]`, output `[3,1,1,1]`.

**Hint.** What identifies a repeated edge when it may arrive as `[1,0]` after `[0,1]`, and what does a self edge add to a set of neighbors?

**Changed decision.** The contract is read before filing, so a set of neighbors replaces the list and a self edge is skipped instead of being filed.

#### [Recognize] Find Center Of Star Graph (LeetCode 1791)
<!-- id: gt-star-center -->

**Prerequisites.** The Parallel And Self Edges rung and the idea of degree.

**Problem.** An undirected star graph has one center joined to every other vertex and has no other edges. The vertices are labeled `1` to `n`, and the input lists the `n - 1` edges. Return the label of the center.

**Constraints.** 3 <= n <= 1000, and the edges form a valid star, in any order and with either end first.

**Example 1.** Input `edges = [[1,2],[2,3],[4,2]]`, output `2`.

**Example 2.** Input `edges = [[5,1],[5,2],[3,5],[5,4]]`, output `5`.

**Hint.** Which vertex has degree n - 1, and which vertex must two different edges of a star share?

**Changed decision.** A full list or matrix is not needed, because the contract guarantees a star and the shared end of any two edges is the answer.
