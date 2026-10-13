# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. API Contracts  ->  01-api-contracts.md
02. Invariant Ownership  ->  02-invariant-ownership.md
03. Pair A Map With Ordered Storage  ->  03-constant-time-composition.md
04. Iterators  ->  04-iterators.md
05. Randomized Sets  ->  05-randomized-sets.md
06. Cache Design  ->  06-cache-design.md

# Chapter 33: Design-data-structure problems

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| API contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| invariant ownership | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| O(1) data-structure composition | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| iterators | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| randomized sets | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| caches | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Map And Linked List

The map finds cache nodes by key; the doubly linked list owns recency order and constant-time removal.

- **Build - Author exercise: Detach And Reinsert.** Preserve all four neighboring links.
- **Vary - LC 146 LRU Cache.** Compose lookup, refresh, and tail eviction.
- **Boundary - Author exercise: Repeated Get And Capacity One.** Verify one node appears exactly once.
- **Recognize - LC 460 LFU Cache.** Extend ownership to frequency-indexed recency lists.

### Map And Dynamic Array

The map locates a value's slot; the array enables constant-time random selection and last-element repair.

- **Build - Author exercise: Remove By Swap.** Repair the moved value's index.
- **Vary - LC 380 Insert Delete GetRandom O(1).** Maintain uniform random access over current values.
- **Boundary - Author exercise: Last-Slot Removal.** Handle the moved and removed values being identical.
- **Recognize - LC 381 Insert Delete GetRandom O(1) - Duplicates Allowed.** Maintain multiple indices per value.

### Iterator API State

Earlier traversal structures now live across public calls; each call must preserve the same next-element invariant.

- **Build - LC 173 Binary Search Tree Iterator.** Keep the unvisited left spine.
- **Vary - LC 284 Peeking Iterator.** Add nonconsuming observation.
- **Boundary - LC 341 Flatten Nested List Iterator.** Skip empty nested lists and expose only integers.
- **Recognize - LC 281 Zigzag Iterator.** Rotate among iterators that still contain elements.

### Deferred: Concurrent Designs

Thread safety changes atomicity and lock ownership and remains in the separately parked senior-loop material.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Write every public-operation contract and its invariant before implementation.
- State which operation mutates recency, index, iterator, or random-selection state.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Hash Map + Linked List | Map locates nodes while list owns recency; staircase: node operations → LC 146 → LC 460 |
| Teach now | Hash Map + Dynamic Array | Swap-with-last repairs index state; representative: LC 380 |
| Teach now | Iterator/API State | Class invariant survives calls; representative: LC 173 / 341 |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** specialized services and concurrency.

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
