# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Find The Next Greater Value  ->  01-next-greater-or-smaller.md
02. Find The Next Greater In A Circle  ->  02-circular-next-greater.md
03. Compute The Stock Span  ->  03-stock-span.md
04. Find Both Boundaries Of A Value  ->  04-boundary-discovery.md
05. Break Ties Between Equal Values  ->  05-duplicate-attribution-policy.md
06. Count Subarrays By Their Minimum  ->  06-contribution-counting.md
07. Find The Largest Rectangle  ->  07-histogram-rectangles.md

# Chapter 12: Monotonic stacks

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| next greater/smaller | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| circular next-greater | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| stock span | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| boundary discovery | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| duplicate-attribution policy | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| contribution counting | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| histogram rectangles | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Stack And Contribution Counting

An ordinary stack preserves unresolved positions. Monotonic ordering proves that dominated positions can be resolved, while boundary distances convert the result into widths or numbers of subarrays. Contribution counting additionally needs an explicit equality ownership rule.

- **Build - LC 496 Next Greater Element I.** Learn resolution on pop without counting regions.
- **Vary - LC 739 Daily Temperatures.** Convert the resolving index into a distance.
- **Boundary - LC 84 Largest Rectangle in Histogram.** Use both boundaries and flush unresolved bars at the end.
- **Recognize - LC 907 Sum of Subarray Minimums.** Count left/right choices with asymmetric duplicate handling.

### Deferred: Greedy And Monotonic Stack

Problems such as Remove K Digits pop a worse earlier choice because a limited-removal greedy proof shows that choice can never help. The ordered stack alone does not establish that exchange argument. Chapter 20 owns this composition and its exercises.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Store indices when equal-value boundary policy matters.
- Explain whether equality pops, remains, or requires an explicit tie rule.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Stack + Contribution Counting | Nearest boundaries determine an element's contribution; staircase: next greater → histogram → LC 907 |
| Deferred | Greedy + Monotonic Stack | Chapter 20 supplies greedy safety proof |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Duplicate attribution:** contribution-counting with equal values must choose one strict and one non-strict boundary so each subarray is owned exactly once. The side that accepts equality depends on the chosen convention; teach the proof rather than one universal `>`/`>=` recipe.
- **Practice boundary:** include all-equal arrays and verify that their contributions are neither dropped nor double-counted.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** greedy stack and DP stack variants.

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
