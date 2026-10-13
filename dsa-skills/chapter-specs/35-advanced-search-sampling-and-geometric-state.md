# Chapter 35: Advanced search, sampling, and geometric state

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| meet-in-the-middle | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| A* search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| reservoir sampling | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| weighted random selection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| rejection sampling | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| randomized partitioning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Split choices into two halves | Full subset enumeration is too large near n=40 | Two half-enumerations reduce work from `2^n` to roughly `2^(n/2)` | https://leetcode.com/problems/closest-subsequence-sum/ | Advanced |
| Prioritize `g + h` | Shortest path has an admissible goal heuristic | A lower-bound heuristic preserves optimality while focusing expansion | Author exercise: A-star grid path | Advanced |
| Replace with probability `k/i` | Uniform sample from unknown-length stream | Every seen item retains equal inclusion probability | https://leetcode.com/problems/linked-list-random-node/ | Intermediate |
| Prefix-weight ticket | Probability is proportional to positive weight | Prefix intervals have lengths equal to weights | https://leetcode.com/problems/random-pick-with-weight/ | Intermediate |
| Reject outside target domain | Uniform proposal is easy in a bounding region | Conditioning a uniform proposal on acceptance preserves uniformity | https://leetcode.com/problems/generate-random-point-in-a-circle/ | Intermediate |
| Random pivot before partition | Adversarial input threatens deterministic partition balance | Pivot randomness yields expected linear selection time | https://leetcode.com/problems/kth-largest-element-in-an-array/ | Intermediate |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Randomized State + Sampling Structure | LC 398 Random Pick Index | LC 382 Linked List Random Node | LC 528 Random Pick with Weight | LC 478 Generate Random Point in a Circle |
| Graph + A-Star Heuristic | Author exercise: Dijkstra with zero heuristic | Author exercise: Manhattan grid heuristic | Author exercise: inadmissible-heuristic counterexample | Author exercise: A-star grid path |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Meet In Middle

**Recognition cue.** Exponential search has roughly 30–44 choices—too many for `2^n`, but two `2^(n/2)` enumerations are practical. **Invariant.** Every full choice splits uniquely into one subset from each half.

- **Build - Author exercise: Half Subset Sums.** Enumerate sums independently.
- **Vary - Author exercise: Closest Pair Of Half Sums.** Sort one side and binary-search complements.
- **Boundary - Author exercise: Duplicates And Long Sums.** Preserve multiplicity when counting and use `long`.
- **Recognize - LC 1755 Closest Subsequence Sum.** Minimize distance to a target with two half-sum sets.

### A Star Search

**Recognition cue.** A shortest-path search has a heuristic lower bound toward the goal. **Invariant.** Priority is `g + h`; an admissible heuristic never overestimates remaining cost, and consistency supports safe closed-state handling.

- **Build - Author exercise: Dijkstra With Zero Heuristic.** Show A* reducing to Dijkstra.
- **Vary - Author exercise: Manhattan Grid Heuristic.** Prioritize states by traveled cost plus Manhattan distance.
- **Boundary - Author exercise: Overestimating Heuristic.** Construct a case where optimality fails.
- **Recognize - Author exercise: A-Star Grid Path.** State admissibility and stale-entry handling before implementation.

### Reservoir Sampling

**Recognition cue.** A stream length is unknown and items cannot all be stored, but each must have equal inclusion probability. **Invariant.** After seeing `i` items, each has probability `k/i` of residing in a size-`k` reservoir.

- **Build - Author exercise: Sample One Item.** Replace the sample with probability `1/i`.
- **Vary - LC 382 Linked List Random Node.** Traverse once with constant extra space.
- **Boundary - Author exercise: First K Items And Short Stream.** Initialize the reservoir from available elements.
- **Recognize - LC 398 Random Pick Index.** Uniformly select among occurrences without storing their indices.

### Weighted Selection

**Recognition cue.** Item probability is proportional to a positive weight. **Invariant.** Prefix sums partition `[1,totalWeight]` into intervals whose lengths equal weights.

- **Build - Author exercise: Prefix Weight Intervals.** Map a random ticket to one item.
- **Vary - LC 528 Random Pick with Weight.** Binary-search the first prefix reaching the ticket.
- **Boundary - Author exercise: Large Total And Zero Weight Policy.** Use `long` and state whether zero weights are legal.
- **Recognize - Author exercise: Mutable Weight Discussion.** Explain why updates would require a Fenwick tree rather than static prefixes.

### Rejection Sampling

**Recognition cue.** Uniform samples are easy in a bounding domain, and rejecting outside points leaves the desired uniform conditional distribution. **Invariant.** Every accepted point comes from the same uniform proposal density.

- **Build - Author exercise: Point In Unit Circle.** Sample a square and reject points outside the circle.
- **Vary - LC 478 Generate Random Point in a Circle.** Translate and scale accepted points.
- **Boundary - Author exercise: Boundary And Expected Trials.** State inclusion policy and analyze acceptance probability.
- **Recognize - LC 470 Implement Rand10() Using Rand7().** Reject biased overflow outcomes from a uniform larger range.

### Randomized Partitioning

**Recognition cue.** Partition-based selection risks adversarial pivots. **Invariant.** A uniformly random pivot makes expected partition balance independent of input order while correctness remains deterministic after pivot choice.

- **Build - Author exercise: Uniform Pivot Index.** Sample within the active inclusive range.
- **Vary - Author exercise: Randomized Quickselect.** Partition and retain only the target side.
- **Boundary - Author exercise: Equal Values.** Use three-way partitioning to avoid repeated near-identical work.
- **Recognize - LC 215 Kth Largest Element in an Array.** Explain expected linear time and worst-case quadratic time.

## Released Combination Lessons

### Randomized Sampling State

The data structure controls which items are eligible; the probability invariant proves that the selection is uniform or correctly weighted.

- **Build - LC 398 Random Pick Index.** Reservoir-sample uniformly among matching indices.
- **Vary - LC 382 Linked List Random Node.** Sample from an unknown-length traversal.
- **Boundary - LC 528 Random Pick with Weight.** Use safe-width prefix totals and exact ticket boundaries.
- **Recognize - LC 478 Generate Random Point in a Circle.** Preserve geometric uniformity through rejection sampling.

### A-Star Heuristics

Graph shortest-path mechanics are already available. This chapter supplies the admissible-heuristic proof; A* is therefore taught here rather than left deferred.

- **Build - Author exercise: Zero-Heuristic Search.** Recover Dijkstra's processing order.
- **Vary - Author exercise: Manhattan Grid Search.** Add an admissible lower bound to the heap priority.
- **Boundary - Author exercise: Inadmissible Counterexample.** Show how overestimation can finalize a nonoptimal goal.
- **Recognize - Author exercise: A-Star Grid Path.** Combine `g`, `h`, predecessor state, and stale-entry rejection.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `long` for random-range arithmetic and weighted prefixes.
- Make randomness, seed assumptions, and probability invariants explicit.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Randomized State + Sampling Structure | Probability invariant is part of correctness; staircase: random index → reservoir sample → weighted choice |
| Teach now | Graph + A-Star Heuristic | Chapter 24 supplied shortest-path state; this chapter supplies admissible-heuristic proof |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** no additional core combination.

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

