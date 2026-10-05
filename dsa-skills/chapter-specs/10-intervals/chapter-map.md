# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Choose How To Sort Intervals  ->  01-endpoint-ordering-contracts.md
02. Decide When Touching Intervals Overlap  ->  02-touching-boundary-semantics.md
03. Merge Intervals And Insert A New One  ->  03-merge-and-insert.md
04. Intersect Two Lists Of Intervals  ->  04-two-list-intersection.md
05. Keep The Most Intervals Without Overlap  ->  05-overlap-and-coverage.md
06. Count Active Intervals With Events  ->  06-event-sweep-ties.md

# Chapter 10: Intervals

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| endpoint ordering contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| touching-boundary semantics | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| merge/insert | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| two-list intersection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| overlap removal/coverage decisions | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sweep events with explicit tie policy | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Sort Intervals Then Scan Once

Sorting exposes intervals in an order where one local state—the active end or last selected end—summarizes all processed input. Interval semantics supply the overlap predicate. Sorting alone does not determine whether the task wants union, insertion, or maximum compatible selection.

- **Build - LC 56 Merge Intervals.** Sort by start and maintain one active union.
- **Vary - LC 57 Insert Interval.** Exploit an already sorted, disjoint input and process before/overlap/after regions.
- **Boundary - LC 435 Non-overlapping Intervals.** Change to end order and preserve the interval that finishes earliest.
- **Recognize - LC 452 Minimum Number of Arrows to Burst Balloons.** Recognize compatible overlap groups through their common rightmost feasible point.

### Deferred: Heap And Intervals

Meeting Rooms II and similar allocation problems need a heap whose minimum end time identifies the next reusable resource. Chapter 17 teaches that heap invariant and owns the full combination staircase.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use safe endpoint comparison and state whether intervals are closed, open, or half-open.
- Return dynamic interval results through an explicit `List<int[]>` to `int[][]` conversion.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Sorting + Intervals | Endpoint order creates a local overlap decision; staircase: merge → insert → erase overlap |
| Deferred | Heap + Intervals | Chapter 17 supplies resource-release heap state |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Endpoint tie policy:** add an event-sweep lesson. The order of a start and end at the same coordinate follows the interval contract: closed intervals may count touching endpoints as overlap, while half-open `[start, end)` intervals free an end before a same-time start. State and test that policy before sorting events.
- **Output conversion:** `List<int[]>` to `int[][]` is an explicit API/output step, not an asymptotic optimization; show `list.toArray(new int[list.size()][])` when that is the required return type.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** greedy scheduling, heap rooms.

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
