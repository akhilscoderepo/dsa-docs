# Chapter 22: BFS variations

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| multi-source initialization | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| layered-state meaning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| bidirectional frontiers | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| implicit/state-space BFS | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| resource-state dominance | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0108 | Multi-source BFS | Rotting Oranges | New subtopic | Models simultaneous spread from multiple sources. |

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Graph BFS + State Modeling | LC 994 Rotting Oranges | LC 542 01 Matrix | LC 1091 Shortest Path in Binary Matrix | LC 127 Word Ladder |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Multi-Source BFS

**Recognition cue.** Several sources spread simultaneously and the answer is distance to the nearest source or total spread time. **Invariant.** Every source begins at distance zero in the same queue; first discovery gives minimum distance to any source. **False friend.** Running one BFS per source repeats most work.

- **Build - Author exercise: Nearest Source Distances.** Enqueue all marked sources before processing.
- **Vary - LC 542 01 Matrix.** Start from every zero and fill distances outward.
- **Boundary - Author exercise: No Source Or All Sources.** Follow the input contract and avoid a false time increment.
- **Recognize - LC 994 Rotting Oranges.** Interpret one BFS layer as one minute of simultaneous spread.

### Layer Meaning

**Recognition cue.** Distance, time, or operation count advances once per entire frontier. **Invariant.** All states in the captured queue size share one distance; their unseen neighbors belong to the next layer. **False friend.** Incrementing time per node overcounts simultaneous work.

- **Build - Author exercise: Label BFS Layers.** Capture the queue size and label every state in one batch equally.
- **Vary - Author exercise: Stop At First Target Layer.** Return when the target is first discovered or dequeued under the chosen invariant.
- **Boundary - Author exercise: Initially Complete State.** Return zero before processing any layer.
- **Recognize - LC 994 Rotting Oranges.** Count only transitions between nonempty layers that create new rotten oranges.

### Bidirectional Frontiers

**Recognition cue.** One unweighted start and target have reversible transitions and the search space branches heavily. **Invariant.** Two visited-distance maps represent shortest discovery from each side; when a generated state exists in the opposite map, the distances combine. **False friend.** Meeting only when queue fronts are equal can miss crossing edges.

- **Build - Author exercise: Two-Ended Integer Search.** Expand one layer from the smaller frontier.
- **Vary - Author exercise: Detect A Crossing Neighbor.** Test intersection while generating next states.
- **Boundary - Author exercise: Start Equals Target.** Return immediately and keep the two visited maps logically distinct.
- **Recognize - LC 127 Word Ladder.** Expand the smaller word frontier until the searches connect.

### State-Space BFS

**Recognition cue.** Vertices are not listed explicitly; legal operations generate neighboring states. **Invariant.** The state encoding contains every fact that affects future moves, and visited uses that complete encoding. **False friend.** Marking only a visible location is wrong when inventory, mask, or mode changes future options.

- **Build - Author exercise: Combination-Lock States.** Generate one-wheel turns from a string state.
- **Vary - LC 752 Open the Lock.** Avoid deadends and return minimum turns.
- **Boundary - Author exercise: Forbidden Start And Target.** Apply the problem's dead-state contract before enqueueing.
- **Recognize - LC 1091 Shortest Path in Binary Matrix.** Recognize coordinates as an implicit state space with uniform moves.

### Resource Dominance

**Recognition cue.** Search state includes a consumable resource, but multiple states at the same node may dominate one another. **Invariant.** At equal or smaller distance, reaching a node with more remaining resource dominates a state with less; discard only when that relation is proved. **False friend.** A Boolean visited array by node loses useful resource states.

- **Build - Author exercise: Position And Remaining Breaks.** Encode both fields in the queue state.
- **Vary - Author exercise: Best Resource Per Cell.** Keep the greatest remaining budget seen at an equal-or-better layer.
- **Boundary - Author exercise: Longer Path With More Resource.** Do not apply dominance across distances without checking its proof.
- **Recognize - LC 1293 Shortest Path in a Grid with Obstacles Elimination.** BFS over `(row, col, remainingEliminations)` with safe dominance.

## Released Combination Lessons

### BFS State Modeling

Graph BFS supplies shortest-layer processing; state modeling decides what constitutes one distinct vertex and what visited must remember.

- **Build - LC 994 Rotting Oranges.** Initialize several sources and interpret layers as minutes.
- **Vary - LC 542 01 Matrix.** Compute nearest-source distances for every cell.
- **Boundary - LC 1091 Shortest Path in Binary Matrix.** Handle blocked endpoints and eight-direction movement.
- **Recognize - LC 127 Word Ladder.** Generate implicit word states and optionally meet from both ends.

### Deferred: Weighted Frontiers

Heap-ordered and deque-ordered frontiers require weighted relaxation rather than ordinary BFS discovery. Chapter 24 owns both.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- State what one BFS layer means before incrementing distance or time.
- Represent compound search state explicitly rather than hiding it in mutable global fields.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Graph BFS + State Modeling | Layered state and multiple starts change what visited means; staircase: rotting oranges → word ladder → state-space BFS |
| Deferred | Graph + Heap | Chapter 24 supplies weighted transitions |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** Dijkstra and weighted state transitions.

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

