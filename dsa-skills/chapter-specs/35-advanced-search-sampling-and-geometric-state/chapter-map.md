# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Meet In Middle  ->  01-meet-in-middle.md
02. A Star Search  ->  02-a-star-search.md
03. Reservoir Sampling  ->  03-reservoir-sampling.md
04. Weighted Selection  ->  04-weighted-selection.md
05. Rejection Sampling  ->  05-rejection-sampling.md
06. Randomized Partitioning  ->  06-randomized-partitioning.md

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
