# Chapter 21: Graph traversal: models, DFS, and ordinary BFS

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| adjacency lists/matrices | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| graph cloning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| visited state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| components | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| grid graphs | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| path enumeration | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| unweighted shortest paths | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| bipartite check | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| directed/undirected cycle detection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0100 | Graph representation | Find Center of Star Graph | Direct concept | Simple graph structure recognition. |
| P0101 | DFS | Number of Islands | Direct concept | Treats a grid as connected components. |
| P0102 | BFS | Clone Graph | Immediate application | Traverses graph nodes while maintaining a mapping. |
| P0103 | Connected components | Number of Connected Components in an Undirected Graph | Immediate application | Generalizes component counting beyond grids. |
| P0104 | Cycle detection — undirected | Graph Valid Tree | New subtopic | Combines connectivity with cycle detection. |
| P0105 | Cycle detection — directed | Course Schedule | New subtopic | Models prerequisites as a directed graph and detects cycles. |
| P0107 | Bipartite graphs | Is Graph Bipartite? | New subtopic | Uses two-coloring during traversal. |
| P0115 | Advanced graph | Reconstruct Itinerary | Advanced application | Requires graph traversal with edge-consumption constraints. |
| Bundle 1-1 | Grid Components | Number of Islands | Learn | — |
| Bundle 1-2 | Grid Components | Max Area of Island | Extend | — |
| Bundle 1-3 | Multi-source BFS | Rotting Oranges | Twist | — |
| Bundle 1-1 | Connectivity | Number of Provinces | Learn | — |
| Bundle 1-2 | Connectivity | Redundant Connection | Extend | — |
| Bundle 1-3 | Merging | Accounts Merge | Twist | — |
| Bundle 2-8 | Grid | Pacific Atlantic Water Flow | Mixed | — |
| Bundle 2-9 | Connectivity | Redundant Connection | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Visited on entry | Need visit connected component | Each state is processed once | https://leetcode.com/problems/number-of-islands/ | Core |
| Frontier by distance | Need shortest unweighted path | First discovery has minimum number of edges | https://leetcode.com/problems/word-ladder/ | Core |
| Start from target/boundary | Need reachability from many cells to a boundary | Reversing the perspective avoids repeating source searches | https://leetcode.com/problems/pacific-atlantic-water-flow/ | Intermediate |
| Original-to-clone identity map | Need copy a cyclic object graph | One clone is created before any recursive revisit | https://leetcode.com/problems/clone-graph/ | Core |
| Opposite colors across edges | Need detect bipartiteness | A conflict proves no two-part partition exists | https://leetcode.com/problems/is-graph-bipartite/ | Core |
| Parent edge versus back edge | Need undirected cycle detection | A visited non-parent neighbor closes a cycle | https://leetcode.com/problems/graph-valid-tree/ | Core |
| Visiting versus completed | Need directed cycle detection | Only an edge to an active recursion ancestor proves a cycle | https://leetcode.com/problems/course-schedule/ | Core |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Grid + Graph Traversal | LC 733 Flood Fill | LC 200 Number of Islands | LC 695 Max Area of Island | LC 133 Clone Graph |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Graph Representation

**Recognition cue.** Relationships are arbitrary edges rather than one parent or next pointer. **Invariant.** An adjacency list enumerates exactly each vertex's outgoing neighbors; a matrix answers edge existence directly. **False friend.** A matrix costs `O(V^2)` even for sparse graphs.

- **Build - Author exercise: Undirected Adjacency Lists.** Add both directions for every undirected edge.
- **Vary - Author exercise: Directed Adjacency Lists.** Add only the stated direction and preserve isolated vertices.
- **Boundary - Author exercise: Parallel And Self Edges.** State whether the input permits them before deduplicating.
- **Recognize - LC 1791 Find Center of Star Graph.** Use the graph contract to identify the shared endpoint.

### Graph Cloning

**Recognition cue.** A reachable object graph must be copied while preserving identity and cycles. **Invariant.** The map holds exactly one clone for each discovered original node. **False friend.** Cloning by value merges distinct nodes with equal labels.

- **Build - Author exercise: Clone One Edge.** Create both clones before wiring the copied edge.
- **Vary - Author exercise: Clone A Cycle.** Insert the mapping before traversing neighbors.
- **Boundary - Author exercise: Null And Self-Loop.** Preserve both absence and an edge back to the same identity.
- **Recognize - LC 133 Clone Graph.** Traverse every reachable node and wire clone neighbors through the identity map.

### Visited State

**Recognition cue.** Multiple paths may reach the same vertex. **Invariant.** Each vertex is scheduled once; BFS normally marks at enqueue time and DFS at entry. **False friend.** Marking BFS only when dequeued permits duplicate queue entries.

- **Build - Author exercise: Reachable Vertices.** Traverse from one source with a Boolean visited array.
- **Vary - Author exercise: Iterative DFS.** Mark before pushing or otherwise prove duplicates are harmless.
- **Boundary - Author exercise: Cycle And Disconnected Vertex.** Terminate the cycle without claiming unreachable vertices were visited.
- **Recognize - LC 841 Keys and Rooms.** Treat keys as directed edges and test complete reachability.

### Components

**Recognition cue.** The graph may be disconnected and the answer counts or summarizes maximal reachable groups. **Invariant.** Every outer-loop start on an unvisited vertex discovers exactly one new component. **False friend.** One traversal from vertex zero misses other components.

- **Build - Author exercise: Count Components.** Start DFS from every unvisited vertex.
- **Vary - Author exercise: Component Sizes.** Return the number of vertices reached by each start.
- **Boundary - Author exercise: No Edges And One Component.** Test all isolated vertices and a fully connected graph.
- **Recognize - LC 547 Number of Provinces.** Count components represented by an adjacency matrix.

### Grid Graphs

**Recognition cue.** Cells are vertices and legal moves define implicit edges. **Invariant.** Every queued or recursive coordinate is in bounds, eligible, and not previously visited. **False friend.** Diagonal movement is not implied by a two-dimensional array.

- **Build - LC 733 Flood Fill.** Traverse same-color four-direction neighbors.
- **Vary - LC 200 Number of Islands.** Start one traversal per unvisited land component.
- **Boundary - Author exercise: Original Color Equals New Color.** Avoid endlessly rediscovering unchanged cells.
- **Recognize - LC 695 Max Area of Island.** Return a component size from the grid traversal.

### Path Enumeration

**Recognition cue.** The output needs every source-to-target path, not only reachability. **Invariant.** The working path contains exactly the current recursion chain and is restored after each neighbor. **False friend.** Global visited state can incorrectly forbid a vertex appearing in different valid paths of a DAG.

- **Build - Author exercise: Paths In A Tiny DAG.** Append a neighbor, recurse, then remove it.
- **Vary - LC 797 All Paths From Source to Target.** Copy the path whenever the target is reached.
- **Boundary - Author exercise: Dead End And Direct Edge.** Record only complete target paths.
- **Recognize - Author exercise: Enumerate Simple Paths.** Add path-local visited state when cycles are permitted.

### Unweighted Shortest Paths

**Recognition cue.** Every transition has equal cost and the task asks for minimum edges or moves. **Invariant.** BFS dequeues vertices in nondecreasing distance, so first discovery is shortest. **False friend.** DFS may find a path first but not the shortest one.

- **Build - Author exercise: Distance From One Source.** Assign `distance[next] = distance[current] + 1` at discovery.
- **Vary - Author exercise: Restore One Shortest Path.** Store a predecessor for each first discovery.
- **Boundary - Author exercise: Source Equals Target And Unreachable Target.** Return zero or the stated failure value.
- **Recognize - LC 1091 Shortest Path in Binary Matrix.** Apply BFS distance to an implicit eight-direction grid graph.

### Bipartite Coloring

**Recognition cue.** Vertices must split into two groups with every edge crossing groups. **Invariant.** Each colored edge endpoint must receive opposite colors; every component needs its own start. **False friend.** Checking only one connected component is incomplete.

- **Build - Author exercise: Color One Component.** Assign opposite colors during BFS.
- **Vary - Author exercise: Process Disconnected Components.** Start coloring from every uncolored vertex.
- **Boundary - Author exercise: Self-Loop And Odd Cycle.** Reject both because they force a color conflict.
- **Recognize - LC 785 Is Graph Bipartite?.** Validate two-colorability across the entire graph.

### Cycle Detection

**Recognition cue.** The task asks whether edges return to an already active route. **Invariant.** Undirected DFS ignores the edge back to its parent; directed DFS distinguishes visiting from fully processed nodes. **False friend.** Any visited neighbor indicates a directed cycle only when that neighbor is still active.

- **Build - Author exercise: Undirected Parent Check.** Reject a visited neighbor other than the traversal parent.
- **Vary - Author exercise: Directed Three Colors.** Detect an edge to a visiting node.
- **Boundary - Author exercise: Two-Way Undirected Edge.** Do not mistake the parent edge for a cycle.
- **Recognize - LC 207 Course Schedule.** Detect a directed prerequisite cycle with three-color DFS.

## Released Combination Lessons

### Walk A Grid As A Graph

The matrix supplies implicit vertices and neighbors; graph traversal supplies visited ownership and component discovery.

- **Build - LC 733 Flood Fill.** Traverse one eligible cell component.
- **Vary - LC 200 Number of Islands.** Repeat traversal for every unvisited land component.
- **Boundary - LC 695 Max Area of Island.** Accumulate size while preserving boundary and visited checks.
- **Recognize - LC 133 Clone Graph.** Transfer the same discovery invariant from coordinates to object identities.

### Deferred: Advanced BFS

Multi-source and bidirectional BFS require different frontier initialization and termination proofs. Chapter 22 owns those variations.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `ArrayDeque` for the BFS frontier and mark visited at the point that prevents duplicate enqueues.
- Encode grid coordinates without unnecessary allocation when hot-loop pressure matters.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Grid + Graph Traversal | Coordinates become vertices and visited state prevents repeated work; staircase: flood fill → islands → clone graph |
| Deferred | Multi-source / Bidirectional BFS | Chapter 22 supplies distinct frontier initialization |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** multi-source/bidirectional search, weighted paths, union-find.

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

