# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. PriorityQueue Mechanics  ->  01-priorityqueue-mechanics.md
02. Heap Orientation  ->  02-heap-orientation.md
03. Top K  ->  03-top-k.md
04. K-Way Merge  ->  04-k-way-merge.md
05. Heap Scheduling  ->  05-heap-scheduling.md
06. Lazy Deletion  ->  06-lazy-deletion.md
07. Running Median  ->  07-running-median.md

# Chapter 17: Heaps and priority queues

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| Java `PriorityQueue` | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| min/max heap orientation and comparators | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| top-k | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| k-way merge | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| scheduling | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| lazy deletion/stale entries | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| running median and dual-heap balancing | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Heap And Intervals

Interval sorting reveals start times; the heap exposes the active interval that finishes first. Together they decide whether a resource can be reused or a new resource is required.

- **Build - LC 252 Meeting Rooms.** Establish the overlap contract after sorting by start.
- **Vary - LC 253 Meeting Rooms II.** Reuse the room with the earliest finishing active meeting.
- **Boundary - LC 2406 Divide Intervals Into Minimum Number of Groups.** Apply the closed-interval tie rule where touching endpoints still overlap.
- **Recognize - LC 1851 Minimum Interval to Include Each Query.** Add eligible intervals by start, expire by end, and select minimum size.

### Deferred: Graph And Heap

Dijkstra-style search also uses the smallest heap entry, but correctness depends on graph relaxation and stale-distance state. Chapter 24 owns that composition.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- `PriorityQueue` is a min-heap by default; write the comparator direction explicitly.
- Do not treat `contains` or `remove(Object)` as logarithmic; use lazy deletion or companion state when needed.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Heap + Intervals | Earliest release time controls room reuse; representative: LC 253 |
| Deferred | Graph + Heap | Chapter 24 supplies distance and stale-entry invariants |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** graph shortest paths.

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
