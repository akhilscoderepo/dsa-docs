# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Dijkstra  ->  01-dijkstra.md
02. Stale Heap Entries  ->  02-stale-heap-entries.md
03. Node-State Search  ->  03-node-state-search.md
04. Constrained Flights  ->  04-constrained-flights.md
05. Alternating Colors  ->  05-alternating-colors.md
06. Zero-One BFS  ->  06-zero-one-bfs.md

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



## Released Combination Lessons

### Graph And Heap

Graph relaxation creates improved tentative distances; the heap exposes the smallest candidate, and stale-entry rejection replaces decrease-key.

- **Build - LC 743 Network Delay Time.** Apply ordinary nonnegative shortest paths.
- **Vary - LC 1631 Path With Minimum Effort.** Change path aggregation from sum to maximum edge effort.
- **Boundary - LC 787 Cheapest Flights Within K Stops.** Add stop count to state so one node distance is not over-pruned.
- **Recognize - LC 1514 Path with Maximum Probability.** Reverse heap priority and maximize multiplicative path score.

### Graph And Deque

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
