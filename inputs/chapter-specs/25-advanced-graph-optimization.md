# Chapter 25: Advanced graph optimization

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| Bellman-Ford | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Floyd-Warshall | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Prim | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Kruskal | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Eulerian trails/Hierholzer | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| strongly connected components | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| bridges/articulation points | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| minimum spanning-tree decisions | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0111 | Weighted shortest path | Path With Minimum Effort | Combination | Combines graph modeling with a nonstandard path cost. |
| P0112 | Minimum spanning tree | Min Cost to Connect All Points | New subtopic | Introduces MST reasoning with Prim/Kruskal. |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Edge-count relaxation layers | Negative edges or a bounded number of transitions | After pass i, paths using at most i edges are represented | https://leetcode.com/problems/cheapest-flights-within-k-stops/ | Intermediate |
| Intermediate-vertex DP | Need all-pairs distances on a small graph | State k permits only vertices 0 through k as intermediates | https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/ | Advanced |
| Cheapest safe crossing edge | Need a minimum spanning tree | The cut property justifies Prim or Kruskal choices | https://leetcode.com/problems/min-cost-to-connect-all-points/ | Intermediate |
| Consume every edge once | Need an Eulerian trail | Postorder after edge exhaustion produces the trail in reverse | https://leetcode.com/problems/reconstruct-itinerary/ | Advanced |
| Mutual-reachability components | Need strongly connected regions | SCC condensation produces a directed acyclic graph | Author exercise: condensation DAG | Advanced |
| Discovery and low-link times | Need bridges or articulation points | A subtree with no earlier back edge depends on its parent connection | https://leetcode.com/problems/critical-connections-in-a-network/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Graph Optimization + Union-Find/Heap | LC 1584 Min Cost to Connect All Points | LC 1192 Critical Connections in a Network | LC 1334 Find the City With the Smallest Number of Neighbors | LC 332 Reconstruct Itinerary |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Bellman Ford

**Recognition cue.** Weighted edges may be negative, or the number of usable edges is bounded. **Invariant.** After pass `i`, distances cover paths using at most `i` edges. **False friend.** Dijkstra is unsafe with negative edges.

- **Build - Author exercise: One Relaxation Pass.** Read previous distances and write improvements without accidental same-pass chaining.
- **Vary - LC 787 Cheapest Flights Within K Stops.** Run exactly the permitted number of edge layers.
- **Boundary - Author exercise: Unreachable And Negative Cycle.** Guard infinity before addition and explain the extra detection pass.
- **Recognize - Author exercise: Negative-Edge Shortest Paths.** Compute distances where no reachable negative cycle exists.

### Floyd Warshall

**Recognition cue.** A small dense graph needs distances between every pair. **Invariant.** After intermediate `k`, `dist[i][j]` is best using only intermediates `0..k`. **False friend.** Reordering the `k` loop breaks the recurrence.

- **Build - Author exercise: Allow One Intermediate.** Compare the direct route with `i -> k -> j`.
- **Vary - Author exercise: All-Pairs Table.** Add intermediates one by one.
- **Boundary - Author exercise: Infinity Arithmetic.** Never add an unreachable sentinel and use safe numeric width.
- **Recognize - LC 1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance.** Compute all-pairs distances and apply the tie rule.

### Prim

**Recognition cue.** A weighted undirected graph needs a minimum-cost spanning tree and adjacency expansion is convenient. **Invariant.** The heap contains edges crossing from the built tree to unvisited vertices; the cheapest crossing edge is safe.

- **Build - Author exercise: Grow One Tree Edge.** Accept the cheapest edge reaching an unvisited vertex.
- **Vary - Author exercise: Skip Stale Heap Edges.** Ignore edges whose destination already joined the tree.
- **Boundary - Author exercise: Disconnected Graph.** Detect when the heap empties before all vertices join.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Apply Prim to Manhattan-distance edges.

### Kruskal

**Recognition cue.** All weighted edges can be sorted and union-find is available. **Invariant.** Accepted edges form an acyclic forest; the next cheapest edge joining two components is safe.

- **Build - Author exercise: Sorted Safe Edges.** Union endpoints only when their roots differ.
- **Vary - Author exercise: Stop At V Minus One.** Finish when the forest becomes one tree.
- **Boundary - Author exercise: Equal Weights And Disconnection.** Allow any safe tie and report failure when components remain.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Implement the Kruskal alternative and compare its edge-storage cost with Prim.

### Hierholzer Trails

**Recognition cue.** Every edge must be consumed exactly once in an Eulerian trail. **Invariant.** Remove edges while walking; append a vertex only when it has no unused outgoing edge, producing reverse trail order.

- **Build - Author exercise: Eulerian Cycle.** Consume each directed edge once and reverse the postorder output.
- **Vary - Author exercise: Eulerian Path.** Start at the vertex required by degree imbalance.
- **Boundary - Author exercise: Parallel Edges.** Represent edge multiplicity rather than neighbor membership.
- **Recognize - LC 332 Reconstruct Itinerary.** Combine Hierholzer's algorithm with lexical edge selection.

### Strong Components

**Recognition cue.** Directed vertices must be grouped when each can reach every other. **Invariant.** Kosaraju processes the reversed graph in decreasing original finish order, or Tarjan uses discovery and low-link state.

- **Build - Author exercise: Finish Order.** Record vertices after outgoing DFS completes.
- **Vary - Author exercise: Reverse-Graph Components.** Traverse in reverse finish order.
- **Boundary - Author exercise: Singleton And One-Way Edge.** Keep vertices separate without mutual reachability.
- **Recognize - Author exercise: Condensation DAG.** Collapse SCCs and verify the resulting graph is acyclic.

### Low Links

**Recognition cue.** Removing one undirected edge or vertex may disconnect the graph. **Invariant.** `low[u]` is the earliest discovery time reachable from `u`'s DFS subtree without using its parent edge.

- **Build - Author exercise: Discovery And Low Values.** Update low links from child returns and back edges.
- **Vary - Author exercise: Bridge Test.** Mark `(u,v)` when `low[v] > disc[u]`.
- **Boundary - Author exercise: Root Articulation Rule.** Treat a DFS root by child count rather than the nonroot formula.
- **Recognize - LC 1192 Critical Connections in a Network.** Return all bridges in one DFS.

### MST Decisions

**Recognition cue.** The task needs minimum total connectivity, not shortest routes from one source. **Invariant.** The cut property makes the lightest safe crossing edge compatible with some MST.

- **Build - Author exercise: Distinguish MST From Shortest Paths.** Compare objectives on the same graph.
- **Vary - Author exercise: Cut-Safe Choice.** Identify the lightest edge crossing a supplied cut.
- **Boundary - Author exercise: Multiple Valid MSTs.** Explain why equal weights can yield different optimal trees.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Choose Prim or Kruskal from graph density and representation.

## Released Combination Lessons

### Graph Optimization State

Earlier graph, heap, and union-find mechanics now support separate global optimization invariants; one structure does not solve every objective.

- **Build - LC 1584 Min Cost to Connect All Points.** Connect components with safe minimum-cost edges.
- **Vary - LC 1192 Critical Connections in a Network.** Replace cost selection with low-link structural analysis.
- **Boundary - LC 1334 Find the City With the Smallest Number of Neighbors.** Use all-pairs distances and explicit tie ownership.
- **Recognize - LC 332 Reconstruct Itinerary.** Consume every edge through lexical Eulerian traversal.

### Deferred: Flow And Matching

Residual-capacity and augmenting-path invariants are outside the active core and receive no premature exercises.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- State sentinel values for unreachable distances and overflow behavior.
- Keep graph-edge and union-find representations separate when both appear.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Graph Optimization + Union-Find/Heap | MST and low-link problems release distinct graph invariants; separate ladders per family |
| Deferred | Flow and Matching | Outside active core unless explicitly added |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** flow, matching, and specialized contest algorithms.

For every released combination, create a dedicated lesson that states each prerequisite's contribution, the combined state/invariant, a false friend, implementation, and its own Build → Vary → Boundary → Recognize staircase. Deferred combinations receive an explanation and a future owner only—never premature exercises.

## Publication Gate

- Crosswalk every required micro-pattern to a named lesson and practice ladder.
- Run the composition audit and record released/deferred outcomes.
- Run the Java integrity focus against every code example.
- Verify exact problem wording, examples, complexity, and prerequisite ownership.
- Render and inspect the PDF; then perform text extraction checks.

## Research Baseline

- [LeetCode Study Plans](https://leetcode.com/studyplan/) for problem discovery and current interview-style prompts.
- [NeetCode Roadmap](https://neetcode.io/roadmap) for a cross-check of prerequisite order and representative pattern families.
- [Tech Interview Handbook study cheatsheets](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) for topic-specific corner cases, complexity review, and interview habits.
- [Oracle Java Collections documentation](https://docs.oracle.com/javase/tutorial/collections/implementations/index.html) for Java collection semantics. Prefer the installed JDK documentation for version-specific details when a chapter relies on a newer API.
- Supplied reference books: *Cracking the Coding Interview*, *Grokking Algorithms*, and *Elements of Programming Interviews in Java*. They guide explanation quality and problem selection; they are not copied verbatim.

