# Chapter 23: Directed graphs and union-find

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| Kahn indegree topological order | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| DFS postorder and three-color directed-cycle detection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| parent-aware undirected cycle detection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| disjoint-set find/path compression | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| union by size | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| connectivity | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Kruskal foundations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0106 | Topological sort | Course Schedule II | Immediate application | Turns dependency feasibility into an ordering. |
| P0113 | Union Find | Number of Provinces | New subtopic | Builds dynamic connectivity with disjoint sets. |
| P0114 | Union Find | Redundant Connection | Immediate application | Detects an edge joining already-connected components. |
| Bundle 1-1 | Topological Sort | Course Schedule | Learn | — |
| Bundle 1-2 | Topological Sort | Course Schedule II | Extend | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Root + union | Edges/components dynamically merge | Component identity is maintained without traversing entire component | https://leetcode.com/problems/redundant-connection/ | Core |
| Union all entities using same key | Need merge entities sharing identifiers | Shared identifier implies same connected component | https://leetcode.com/problems/accounts-merge/ | Intermediate |
| Relax edges in topological order | Need shortest path in DAG | All predecessors of a node are finalized before it | https://leetcode.com/problems/parallel-courses-iii/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Graph + Union-Find | LC 547 Number of Provinces | LC 684 Redundant Connection | LC 721 Accounts Merge | LC 1584 Min Cost to Connect All Points |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Kahn Topological Order

**Recognition cue.** Directed prerequisites require an order in which every predecessor appears first. **Invariant.** Indegree counts unresolved incoming prerequisites; the queue contains exactly currently available zero-indegree vertices. **False friend.** Sorting labels cannot satisfy arbitrary dependencies.

- **Build - Author exercise: Compute Indegrees.** Count every directed incoming edge.
- **Vary - LC 207 Course Schedule.** Process zero-indegree courses and test whether all vertices are removed.
- **Boundary - Author exercise: Several Initial Sources.** Enqueue every zero-indegree vertex, including isolated ones.
- **Recognize - LC 210 Course Schedule II.** Return the removal order or an empty result when a cycle remains.

### DFS Topological State

**Recognition cue.** Directed cycle detection and topological order can be produced through recursive completion. **Invariant.** White is unvisited, gray is active, and black is complete; only an edge to gray proves a cycle. Postorder reversal yields an order when no cycle exists.

- **Build - Author exercise: Three-Color Trace.** Mark entry gray and exit black.
- **Vary - Author exercise: Postorder Topological List.** Append only after every outgoing neighbor completes.
- **Boundary - Author exercise: Cross Edge To Black.** Accept it because it does not return to an active ancestor.
- **Recognize - LC 210 Course Schedule II.** Produce an order with DFS or reject a gray back edge.

### Undirected Parent State

**Recognition cue.** An undirected traversal sees every tree edge from both endpoints. **Invariant.** A visited neighbor is a cycle only when it is not the vertex from which the current node was entered. **False friend.** Directed three-color logic is unnecessary for ordinary undirected cycle detection.

- **Build - Author exercise: DFS With Parent.** Pass the previous vertex into each call.
- **Vary - Author exercise: Detect A Triangle.** Find the non-parent visited neighbor.
- **Boundary - Author exercise: Single Edge And Parallel Edges.** State the graph's parallel-edge contract before judging a cycle.
- **Recognize - LC 261 Graph Valid Tree.** Require both no cycle and exactly one connected component.

### Find Compression

**Recognition cue.** Repeated operations ask which dynamically merged component contains an element. **Invariant.** Parent links lead to one representative root; path compression rewrites searched paths without changing membership. **False friend.** Union-find does not enumerate paths or support arbitrary edge deletion.

- **Build - Author exercise: Follow Parents To Root.** Implement `find` without compression.
- **Vary - Author exercise: Compress A Chain.** Point every visited node directly to the root.
- **Boundary - Author exercise: Singleton Components.** A node initially represents itself.
- **Recognize - LC 547 Number of Provinces.** Union connected cities and count remaining representatives.

### Union By Size

**Recognition cue.** Two representatives must merge while keeping parent trees shallow. **Invariant.** Attach the smaller root under the larger root and update size only at the surviving root. **False friend.** Comparing original elements rather than roots corrupts size accounting.

- **Build - Author exercise: Merge Two Roots.** Find both representatives before writing parent links.
- **Vary - Author exercise: Repeated Unequal Merges.** Update the receiving root's size.
- **Boundary - Author exercise: Already Connected.** Return without double-counting size or reducing component count.
- **Recognize - LC 684 Redundant Connection.** The first edge whose endpoints already share a root closes a cycle.

### Dynamic Connectivity

**Recognition cue.** Edges arrive or shared identifiers merge groups, and queries need component identity. **Invariant.** Two elements are connected exactly when their finds return the same representative. **False friend.** A static DFS can answer one snapshot but does not naturally maintain repeated merges.

- **Build - Author exercise: Online Connect And Query.** Alternate union and same-component operations.
- **Vary - LC 547 Number of Provinces.** Build connectivity from a matrix.
- **Boundary - Author exercise: Duplicate Union.** Preserve counts when an edge repeats.
- **Recognize - LC 721 Accounts Merge.** Union accounts sharing an email and group data by representative.

### Kruskal Foundations

**Recognition cue.** The graph must connect all vertices with minimum total edge cost. **Invariant.** Edges are considered by increasing weight; accept an edge only when it joins different components. The cut property makes that edge safe. **False friend.** Choosing the cheapest edges without cycle checks may not form a tree.

- **Build - Author exercise: Cheapest Safe Edge.** Sort edges and skip one whose endpoints already connect.
- **Vary - Author exercise: Stop After V Minus One.** End once the spanning tree has enough edges.
- **Boundary - Author exercise: Disconnected Weighted Graph.** Report that no spanning tree exists.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Generate weighted edges and apply Kruskal with union-find.

## Released Combination Lessons

### Merge Groups As Edges Arrive

Graph edges define connectivity events; union-find compresses each evolving component to one representative.

- **Build - LC 547 Number of Provinces.** Merge endpoints and count components.
- **Vary - LC 684 Redundant Connection.** Detect an edge inside an existing component.
- **Boundary - LC 721 Accounts Merge.** Merge repeated shared identifiers and group by final root.
- **Recognize - LC 1584 Min Cost to Connect All Points.** Add sorted safe edges to form a minimum spanning tree.

### Deferred: Weighted Paths

Connectivity representatives do not store route cost. Chapter 24 introduces distance relaxation for weighted shortest paths.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Keep disjoint-set parent and size/rank arrays synchronized.
- For graph direction, explain the adjacency representation and indegree mutation contract.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Graph + Union-Find | Connectivity state is component representative; staircase: components → redundant edge → Kruskal foundation |
| Deferred | Weighted Shortest Path | Chapter 24 supplies distance relaxation |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** weighted shortest paths and advanced graph state.

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

