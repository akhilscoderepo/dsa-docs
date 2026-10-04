<!-- lesson-kind: standard -->
<!-- lesson-id: cycle-detection -->
## Cycle Detection

<!-- stage: context -->
### The Recipe Rail At Marrow Lane

Marrow Lane Bakery keeps its recipes on paper cards clipped to a steel rail above the proofing racks. Every card carries a short line at the bottom: "needs first", followed by the cards whose products must be ready before this one can start. The seeded loaf needs the rye levain, the levain needs a feed of the house starter, and so on down to flour and water. A new head baker, Imre, wants to plan the 4 a.m. shift by laying the cards out in an order where nothing is begun before its needs are done.

On his second morning he gets stuck. He follows the seeded loaf to the levain, the levain to a starter feed, and the feed to a note that says "use yesterday's seeded loaf crumbs". He is standing at the same card he began with. No order can ever satisfy a rail like that, and he would like a procedure that says so for any rail, before anyone lights an oven.

<!-- stage: naive -->
### Chase Every Card Around Its Own Loop

The plain approach tests one card at a time. Start from a card and ask which cards can be reached in one step, then in two steps, then in three, and keep going. If the starting card ever turns up in one of those sets, the rail loops through it. A route that has not returned within n steps, with n the number of cards, never will, because a longer walk must have repeated a card already.

```java
static boolean loopsByChasing(List<List<Integer>> needs) {
    int n = needs.size();
    for (int start = 0; start < n; start++) {
        boolean[] here = new boolean[n];
        here[start] = true;
        for (int step = 1; step <= n; step++) {
            boolean[] after = new boolean[n];
            for (int card = 0; card < n; card++) {
                if (!here[card]) continue;
                for (int need : needs.get(card)) after[need] = true;
            }
            if (after[start]) return true;
            here = after;
        }
    }
    return false;
}
```

This is correct for any rail, including one with a card that lists itself. Each start gets its own fresh tables, so earlier starts cannot disturb later ones, and the answer is true as soon as any single card finds its way home.

<!-- stage: bottleneck -->
### Every Start Repeats The Same Walks

One round of chasing touches every card and every "needs" line, which costs O(n + m) for n cards and m lines. A start runs up to n rounds, and all n cards are tried as starts, so the total is O(n^2 * (n + m)). For a catalogue of ten thousand cards and fifty thousand lines that is about six times ten to the thirteenth steps, far beyond any shift.

The waste is plain to see. Chasing from the levain walks the same corridor to flour that chasing from the seeded loaf has already walked, and a corridor that dead-ends at flour is rechecked from every card above it. Once a card is known to lead only to dead ends, nobody should walk its corridor again. A better method should walk each card once, remember what it learned there, and notice a loop at the moment a walk steps onto something it is still in the middle of.

<!-- stage: insight -->
### Marks For Cards In Progress

Walk depth first and give every card one of **three colors**: 0 for never reached, 1 for a card on the route being walked right now, and 2 for a card whose entire corridor has been explored and found loop-free. A card turns 1 when the walk enters it and 2 when the walk leaves it for good. In a directed graph, an edge that lands on a color-1 card is the **back edge** that closes a loop, because the route from that card down to the current one, plus this edge, is a circle. An edge landing on a color-2 card proves nothing. That card cannot lead back here, since its whole corridor was already searched. Two routes that merely meet at a shared card, a diamond, are fine.

An undirected graph is simpler, with one trap. Every edge is stored twice, once from each end, so the walk down an edge always sees the same edge again from the far side. That reflection is the **parent edge**, and it must be skipped. Skip it by the edge's own number, not by the neighbor's identity, so that a second, parallel edge between the same two cards still counts as a loop. Any other edge to an already reached card then closes a cycle, and no third color is needed.

The invariant is that the color-1 cards always form one unbroken route from the current walk's starting card down to the card being expanded.

<!-- names: three colors, back edge, parent edge -->

<!-- stage: variables -->
### Marks, Routes And Edge Numbers

The array `mark` holds one of 0, 1 or 2 per card, and `v` is the card being expanded with `w` as the neighbor tried from it. In the undirected form `seen` is a plain boolean per vertex, and each adjacency entry carries a pair `{w, id}`, where `id` is the position of that edge in the input list. The number `from` is the id of the edge the walk used to arrive at `v`, with -1 for a start. The route is the chain of color-1 cards, reported in the trace as text.

<!-- stage: trace -->
### A Rail Without And With Loops

The first trace is a directed rail of five cards with lines 0 to 1, 0 to 2, 1 to 3, 2 to 3 and 3 to 4, where an arrow u to v means u needs v. The pointer `cur` is the card being handled, and the vars show the marks of cards 0 to 4 as a string, so the route is the cards currently marked 1. Card 3 is reached twice, first through card 1 and later through card 2. The second arrival finds it already marked 2, which is why a diamond is not a loop.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"marks":"1 0 0 0 0"},"note":"Card 0 is entered as a start and marked 1."},{"at":{"cur":1},"vars":{"marks":"1 1 0 0 0"},"note":"Card 1 is entered from card 0 and marked 1."},{"at":{"cur":3},"vars":{"marks":"1 1 0 1 0"},"note":"Card 3 is entered from card 1 and marked 1."},{"at":{"cur":4},"vars":{"marks":"1 1 0 1 1"},"note":"Card 4 is entered from card 3 and marked 1."},{"at":{"cur":4},"vars":{"marks":"1 1 0 1 2"},"note":"Card 4 has no more needs, so it leaves the route and is marked 2."},{"at":{"cur":3},"vars":{"marks":"1 1 0 2 2"},"note":"Card 3 has no more needs, so it leaves the route and is marked 2."},{"at":{"cur":1},"vars":{"marks":"1 2 0 2 2"},"note":"Card 1 has no more needs, so it leaves the route and is marked 2."},{"at":{"cur":2},"vars":{"marks":"1 2 1 2 2"},"note":"Card 2 is entered from card 0 and marked 1."},{"at":{"cur":2},"vars":{"marks":"1 2 1 2 2"},"note":"Card 2 looks at card 3, which is marked 2, so the edge is harmless and is not followed."},{"at":{"cur":2},"vars":{"marks":"1 2 2 2 2"},"note":"Card 2 has no more needs, so it leaves the route and is marked 2."},{"at":{"cur":0},"vars":{"marks":"2 2 2 2 2"},"note":"Card 0 has no more needs, so it leaves the route and is marked 2."}]}
```

The second trace is an undirected graph on five vertices with edges numbered 0 to 4: 0-1, 1-2, 2-3, 3-1 and 3-4. The vars list the route and the edge id used to arrive. Each vertex first skips the edge that brought the walk to it, and the walk stops the moment an edge other than that one leads to a vertex still on the route. Vertex 4 is never visited, because the answer is already known by then.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"route":"0","arrived_by":-1},"note":"Vertex 0 is entered as a start."},{"at":{"cur":1},"vars":{"route":"0>1","arrived_by":0},"note":"Vertex 1 is entered by edge 0."},{"at":{"cur":1},"vars":{"route":"0>1","arrived_by":0},"note":"Edge 0 to vertex 0 is the edge the walk arrived by, so it is skipped."},{"at":{"cur":2},"vars":{"route":"0>1>2","arrived_by":1},"note":"Vertex 2 is entered by edge 1."},{"at":{"cur":2},"vars":{"route":"0>1>2","arrived_by":1},"note":"Edge 1 to vertex 1 is the edge the walk arrived by, so it is skipped."},{"at":{"cur":3},"vars":{"route":"0>1>2>3","arrived_by":2},"note":"Vertex 3 is entered by edge 2."},{"at":{"cur":3},"vars":{"route":"0>1>2>3","arrived_by":2},"note":"Edge 2 to vertex 2 is the edge the walk arrived by, so it is skipped."},{"at":{"cur":3},"vars":{"route":"0>1>2>3","arrived_by":2},"note":"Edge 3 reaches vertex 1, already on the route, so the answer is true."}]}
```

<!-- stage: code -->
### Two Walks With Their Guards

```java
final class RouteCheck {
    static boolean directedCycle(List<List<Integer>> out) {
        int[] mark = new int[out.size()];
        for (int s = 0; s < out.size(); s++) {
            if (mark[s] == 0 && enter(out, mark, s)) return true;
        }
        return false;
    }

    private static boolean enter(List<List<Integer>> out, int[] mark, int v) {
        mark[v] = 1;
        for (int w : out.get(v)) {
            if (mark[w] == 1) return true;
            if (mark[w] == 0 && enter(out, mark, w)) return true;
        }
        mark[v] = 2;
        return false;
    }

    static boolean undirectedCycle(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int id = 0; id < edges.length; id++) {
            adj.get(edges[id][0]).add(new int[] {edges[id][1], id});
            adj.get(edges[id][1]).add(new int[] {edges[id][0], id});
        }
        boolean[] seen = new boolean[n];
        for (int s = 0; s < n; s++) {
            if (!seen[s] && reach(adj, seen, s, -1)) return true;
        }
        return false;
    }

    private static boolean reach(List<List<int[]>> adj, boolean[] seen, int v, int from) {
        seen[v] = true;
        for (int[] e : adj.get(v)) {
            if (e[1] == from) continue;
            if (seen[e[0]] || reach(adj, seen, e[0], e[1])) return true;
        }
        return false;
    }
}
```

Both walks cost O(n + m) time, since every card is entered once and every line is looked at once or twice, and use O(n) space for the marks and the recursion. The directed walk checks mark 1 before mark 0 on purpose, and the undirected walk compares edge ids, never vertex numbers.

<!-- stage: applicability -->
### Loops In Plans And Dependencies

Look for this model when the input is a set of "must come before" or "is linked to" relations and the question is whether a route can return to a place it has not left yet: build orders, course prerequisites, spreadsheet formulas that refer to each other, import chains between source files, and redundant links in a cable network. The invariant to defend is the unbroken route of color-1 vertices in the directed form, and the rule that only the edge number identifies the parent in the undirected form.

The nearest false friend is the belief that any already reached neighbor means a directed cycle. A diamond refutes it at once: two prerequisites that share a prerequisite are perfectly schedulable. A second false friend is the parent vertex check judged from the descendant's side, such as the directed marks reused with a skip of the parent card: the child skips both copies of a doubled edge because the neighbor is the parent both times, and the ancestor later sees only a finished card.

Do not use this walk when the task needs the shortest loop, the number of loops, or the loop itself listed in full. It reports only whether one exists, and a breadth-first search from each vertex fits better for shortest length. In Java, the recursion goes as deep as the longest route, so a chain of a few hundred thousand cards overflows the default thread stack with a `StackOverflowError`. An explicit stack of vertex and next-neighbor positions avoids that.

<!-- stage: exercises -->
### Exercises

#### [Build] Undirected Parent Check (Author exercise)
<!-- id: gt-parent-check -->

**Prerequisites.** The undirected walk and the visited table from the Visited State lesson.

**Problem.** An undirected graph on `n` vertices, labelled 0 to n - 1, arrives as an edge list. Return `true` when the graph contains a cycle and `false` when it is a forest. The contract is that the input is a simple graph: there are no self loops, and no pair of vertices appears twice, in either order. A neighbor that was already reached and is not the vertex you came from closes a cycle.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 4000, and every edge has two different endpoints in range. The graph may be disconnected.

**Example 1.** Input `n = 6, edges = [[0,1],[1,2],[2,0],[3,4]]`, output `true`.

**Example 2.** Input `n = 6, edges = [[0,1],[1,2],[1,3],[4,5]]`, output `false`.

**Hint.** When the walk is expanding a vertex and its neighbor is the one it just came from, what has the walk actually seen?

**Changed decision.** The walk carries the vertex it arrived from, and a reached neighbor other than that vertex ends the search with true.

#### [Vary] Directed Three Colors (Author exercise)
<!-- id: gt-three-colors -->

**Prerequisites.** The Undirected Parent Check rung.

**Problem.** A directed graph on `n` vertices, labelled 0 to n - 1, arrives as pairs `[from, to]`. Return `true` when it contains a directed cycle, where a self loop `[v, v]` counts as a cycle of length 1, and `false` otherwise. Use three states per vertex: unreached, on the current route, and done.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 6000, and endpoints are in range. A pair may repeat.

**Example 1.** Input `n = 5, edges = [[0,1],[0,2],[1,3],[2,3],[3,4]]`, output `false`.

**Example 2.** Input `n = 4, edges = [[0,1],[1,2],[2,3],[3,1]]`, output `true`.

**Hint.** If the edge lands on a vertex that is already reached, which of the two later states decides the answer?

**Changed decision.** A reached neighbor is no longer enough. Only a neighbor still on the current route reports a cycle, and a vertex is marked done when its walk ends.

#### [Boundary] Two-Way Undirected Edge (Author exercise)
<!-- id: gt-two-way-edge -->

**Prerequisites.** The Directed Three Colors rung.

**Problem.** The Undirected Parent Check problem again, with the simple-graph promise removed. An edge `[u, v]` listed once is a single edge. The same pair listed twice, in either order, is a parallel edge, and two parallel edges between two vertices form a cycle of length 2, so the answer is `true`. Self loops are still excluded.

**Constraints.** 1 <= n <= 2000, 0 <= edges.length <= 4000, and every edge has two different endpoints in range.

**Example 1.** Input `n = 3, edges = [[0,1],[1,2]]`, output `false`.

**Example 2.** Input `n = 4, edges = [[0,1],[2,3],[3,2]]`, output `true`.

**Hint.** If the walk skips the neighbor it came from, what happens to the second copy of the same edge?

**Changed decision.** The walk skips the specific edge number it arrived by, not every edge leading to the parent vertex.

#### [Recognize] Course Schedule (LeetCode 207)
<!-- id: gt-course-schedule -->

**Prerequisites.** The Directed Three Colors rung.

**Problem.** There are `numCourses` courses numbered from 0 to numCourses - 1. Each pair `[a, b]` in `prerequisites` means course b must be taken before course a. Return `true` when all courses can be finished in some order, and `false` otherwise.

**Constraints.** 1 <= numCourses <= 2000, 0 <= prerequisites.length <= 5000, and every number is in range. A course is never listed as its own prerequisite.

**Example 1.** Input `numCourses = 4, prerequisites = [[1,0],[2,1],[3,2]]`, output `true`.

**Example 2.** Input `numCourses = 3, prerequisites = [[0,2],[2,1],[1,0]]`, output `false`.

**Hint.** Which way should each edge point, and what does a loop among courses say about the order?

**Changed decision.** The answer is the opposite of cycle detection: the courses can be finished exactly when the directed graph has no cycle.
