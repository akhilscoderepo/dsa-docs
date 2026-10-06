# Chapter 24: Shortest paths and graph state modeling

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| Dijkstra | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| stale heap entries | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| `(node, state)` search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| constrained flights | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| alternating colors | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 0-1 BFS | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0109 | Unweighted shortest path | Shortest Path in Binary Matrix | Immediate application | Uses BFS distance to find a shortest route. |
| P0110 | Weighted shortest path | Network Delay Time | New subtopic | Introduces Dijkstra for nonnegative weighted edges. |
| Bundle 1-3 | Shortest Path | Network Delay Time | Twist | — |

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Graph + Heap | LC 743 Network Delay Time | LC 1631 Path With Minimum Effort | LC 787 Cheapest Flights Within K Stops | LC 1514 Path with Maximum Probability |
| Graph + Deque | Author drill: push zero-cost moves to the front | LC 1368 Minimum Cost to Make at Least One Valid Path | LC 2290 Minimum Obstacle Removal to Reach Corner | Author exercise: minimum toll on a zero/one weighted graph |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Find Cheapest Routes With Dijkstra

**Recognition cue.** Edges have nonnegative weights and the task asks for minimum total cost from a source. **Invariant.** When the smallest nonstale tentative distance is removed from the heap, no later path can improve it; relaxing an edge proposes `dist[u] + weight`. **False friend.** Ordinary BFS is correct only when transition costs are equal.

- **Build - Author exercise: Relax One Edge.** Update a neighbor only when the proposed distance is smaller.
- **Vary - Author exercise: Small Weighted Graph.** Repeatedly process the smallest tentative distance.
- **Boundary - Author exercise: Unreachable Vertex And Large Sum.** Preserve infinity and use `long` when path sums may overflow.
- **Recognize - LC 743 Network Delay Time.** Run Dijkstra from the source and return the largest finite finalized distance.

### Skip Outdated Heap Entries

**Recognition cue.** Java's heap has no decrease-key operation, so a vertex may have several queued distances. **Invariant.** `dist[node]` is the best known value; discard a popped entry when its stored distance differs from that value. **False friend.** Removing the old heap object with `remove(Object)` is linear.

- **Build - Author exercise: Two Entries For One Node.** Insert an improved distance and identify the old entry as stale.
- **Vary - Author exercise: Skip Before Expansion.** Reject stale entries before relaxing outgoing edges.
- **Boundary - Author exercise: Equal-Cost Alternatives.** Keep the distance contract consistent when a proposal ties the current best.
- **Recognize - LC 743 Network Delay Time.** Use duplicate insertion plus stale rejection instead of decrease-key.

### Search Over Place And State

**Recognition cue.** Future transitions depend on both location and another fact such as stops used, keys held, or last edge color. **Invariant.** Distance and visited state are indexed by the complete pair `(node, state)`; two states at one node are distinct unless dominance is proved. **False friend.** One distance per node discards potentially necessary routes.

- **Build - Author exercise: Node And Coupon Flag.** Track whether a one-use discount has been consumed.
- **Vary - Author exercise: Distance By State.** Store separate distances for every node-mode pair.
- **Boundary - Author exercise: Same Node, Different Future.** Show why a costlier arrival with an unused resource may remain useful.
- **Recognize - LC 1129 Shortest Path with Alternating Colors.** Include the last edge color in BFS state.

### Limit A Route By Stops

**Recognition cue.** A cheapest route is limited by stops or edges, so cost alone does not dominate every arrival. **Invariant.** State includes node and edges used; relaxations never exceed the allowed count. **False friend.** Plain Dijkstra with one `dist[node]` can discard a more expensive arrival that uses fewer stops.

- **Build - Author exercise: At Most Two Edges.** Compute costs layer by layer without reusing same-layer updates.
- **Vary - Author exercise: Cost By Stops Used.** Store one best cost for each node and allowed edge count.
- **Boundary - Author exercise: Direct Flight And K Zero.** Translate `k` intermediate stops into at most `k + 1` edges.
- **Recognize - LC 787 Cheapest Flights Within K Stops.** Use bounded Bellman-Ford layers or an explicit heap state with correct dominance.

### Alternate Edge Colors

**Recognition cue.** Edge type constrains which edge type may be used next. **Invariant.** Visited is indexed by node and last color; neighbors must use the opposite color. **False friend.** Marking the node once can suppress a necessary arrival with the other last color.

- **Build - Author exercise: Alternate Red And Blue.** Generate only opposite-color transitions.
- **Vary - Author exercise: Two Start Modes.** Seed both possible previous colors at distance zero.
- **Boundary - Author exercise: Self-Loop And Parallel Colors.** Treat color-state pairs independently.
- **Recognize - LC 1129 Shortest Path with Alternating Colors.** BFS over `(node, lastColor)` and take the smaller state distance.

### Search With Zero And One Costs

**Recognition cue.** Every edge weight is exactly zero or one. **Invariant.** The deque processes tentative distances in nondecreasing order by pushing zero-cost improvements to the front and one-cost improvements to the back. **False friend.** Ordinary BFS counts edges, while Dijkstra works but pays an unnecessary heap cost.

- **Build - Author exercise: Choose Deque End By Weight.** Push a relaxed zero edge first and a one edge last.
- **Vary - Author exercise: Reject Nonimproving Relaxations.** Maintain a distance array exactly as in weighted search.
- **Boundary - Author exercise: Zero-Cost Cycle.** Terminate through distance improvement checks rather than Boolean discovery alone.
- **Recognize - LC 1368 Minimum Cost to Make at Least One Valid Path in a Grid.** Model following an arrow as zero and changing direction as one.

## Released Combination Lessons

### Shortest Paths With A Heap

Graph relaxation creates improved tentative distances; the heap exposes the smallest candidate, and stale-entry rejection replaces decrease-key.

- **Build - LC 743 Network Delay Time.** Apply ordinary nonnegative shortest paths.
- **Vary - LC 1631 Path With Minimum Effort.** Change path aggregation from sum to maximum edge effort.
- **Boundary - LC 787 Cheapest Flights Within K Stops.** Add stop count to state so one node distance is not over-pruned.
- **Recognize - LC 1514 Path with Maximum Probability.** Reverse heap priority and maximize multiplicative path score.

### Shortest Paths With A Deque

The graph supplies zero/one weighted transitions; the deque preserves distance order without a heap by choosing the insertion end from edge weight.

- **Build - Author exercise: Zero-One Relaxation.** Push zero-cost improvements front and one-cost improvements back.
- **Vary - LC 1368 Minimum Cost to Make at Least One Valid Path in a Grid.** Derive edge cost from agreement with the cell arrow.
- **Boundary - LC 2290 Minimum Obstacle Removal to Reach Corner.** Charge the destination cell consistently and handle a zero-cost start.
- **Recognize - Author exercise: Minimum Zero-One Toll.** Find the minimum cost in an explicit graph whose edges cost only zero or one.

### Deferred: Negative Weights

Dijkstra and 0-1 BFS depend on restricted nonnegative weights. Bellman-Ford and all-pairs algorithms require separate relaxation schedules and remain outside this chapter's core staircase.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `long` distances when additions may overflow `int`.
- Handle stale priority-queue entries explicitly instead of attempting in-place key decrease.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Graph + Heap | Dijkstra uses relaxation and stale-entry rejection; staircase: network delay → minimum effort → constrained flights |
| Teach now | Graph + Deque | 0-1 BFS uses edge weight to choose deque end |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** negative-weight paths and all-pairs algorithms.

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

