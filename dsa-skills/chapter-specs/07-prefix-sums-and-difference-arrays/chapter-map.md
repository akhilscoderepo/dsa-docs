# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Prefix Construction  ->  01-prefix-construction.md
02. Range Queries  ->  02-range-queries.md
03. Exclusion State  ->  03-exclusion-state.md
04. Prefix Counts  ->  04-prefix-counts.md
05. Earliest Balance  ->  05-earliest-balance.md
06. Remainder Classes  ->  06-remainder-classes.md
07. Prefix XOR  ->  07-prefix-xor.md
08. Difference Arrays  ->  08-difference-arrays.md
09. Two-Dimensional Prefix  ->  09-two-dimensional-prefix.md
10. Two-Dimensional Difference  ->  10-two-dimensional-difference.md

# Chapter 07: Prefix sums and difference arrays

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| one-dimensional prefix | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| range query | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| prefix/suffix exclusion state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| prefix-count maps | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| earliest-index/balance maps | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| remainder-class maps | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| prefix XOR | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| difference/range updates | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 2D prefix | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 2D difference rectangle updates | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Prefix State And Maps

Prefix state turns every earlier position into a meaningful key; the map supplies either frequency or earliest-index memory. A map alone does not explain what its keys mean.

- **Build - LC 560 Subarray Sum Equals K.** Given an integer array `nums` and integer `k`, return the number of contiguous subarrays whose sum equals `k`. Store how many earlier boundaries have each raw prefix sum.
- **Vary - LC 525 Contiguous Array.** Given a binary array, return the maximum length of a contiguous subarray containing the same number of zeroes and ones. Transform zero into `-1` and preserve the earliest index of each balance.
- **Boundary - LC 974 Subarray Sums Divisible by K.** Count the non-empty contiguous subarrays whose sum is divisible by `k`. Normalize negative prefix remainders with `Math.floorMod` before using them as keys.
- **Recognize - LC 523 Continuous Subarray Sum.** Determine whether a length-at-least-two contiguous subarray has a sum divisible by `k`. Store the earliest index for each remainder so the length contract can be checked.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `long` prefix state where totals can exceed `int`.
- Reserve and explain any sentinel slot used by a difference array.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Prefix State + Hash Map | Prefix counts / earliest index / remainder state; staircase: LC 560 → LC 525 → LC 974 → LC 523 |
| Deferred | Prefix + Sliding Window | Chapter 09 supplies moving-boundary comparison |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **2D difference arrays:** add rectangular range updates as a separate micro-pattern. A rectangle update writes four signed corner deltas; a two-dimensional prefix reconstruction materializes final cells. Allocate a sentinel border or guard the `r2 + 1` and `c2 + 1` writes explicitly.
- **Keep it separate from 2D prefix queries:** one preprocesses point values for range queries; the other batches range updates before materialization.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** sliding window, segment tree/Fenwick tree.

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
