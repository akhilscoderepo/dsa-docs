# Chapter map (generated; do not edit, edit the source spec)

All integer searches use an explicitly stated interval convention and the overflow-safe midpoint `lo + (hi - lo) / 2`.

## Lesson order

01. Exact Search  ->  01-exact-search.md
02. First And Last  ->  02-first-and-last.md
03. Lower And Upper Bounds  ->  03-lower-and-upper-bounds.md
04. First True  ->  04-first-true.md
05. Peak Search  ->  05-peak-search.md
06. Rotated Minimum  ->  06-rotated-minimum.md
07. Rotated Target  ->  07-rotated-target.md
08. Integer Answers  ->  08-integer-answers.md
09. Continuous Answers  ->  09-continuous-answers.md

# Chapter 06: Binary search

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| exact search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| first/last occurrence | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| lower/upper bounds | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| first-true predicate search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| peak/mountain search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| rotated minimum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| rotated-array target search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| integer answer-space feasibility search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| continuous answer-space feasibility search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Time Indexed Lookup

**Contributions.** A `HashMap` selects the history for one key; an ordered timestamp list makes binary search valid. A map alone cannot choose the latest timestamp `<= queryTime` without scanning that history.

- **Build - Author exercise: One Key History.** Binary-search the latest timestamp not exceeding a query.
- **Vary - LC 981 Time Based Key-Value Store.** Add independent histories per string key.
- **Boundary - LC 981 Early Query.** Return the specified empty value when every timestamp is later than the query.
- **Recognize - LC 1146 Snapshot Array.** Each index owns an ordered history searched by snapshot ID.

### Matrix Search

**Contributions.** Matrix shape maps a virtual one-dimensional index to `(row, col)`; binary search discards ordered ranges.

- **Build - LC 74 Search a 2D Matrix.** Use `row = mid / cols`, `col = mid % cols` under global row-major ordering.
- **Vary - Author exercise: First Matrix Position.** Return coordinates instead of a boolean.
- **Boundary - Author exercise: Empty Shape.** Guard zero rows before computing `cols` or a final virtual index.
- **Recognize - LC 240 Search a 2D Matrix II.** Rows and columns are sorted independently; use staircase elimination, not virtual-array binary search.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `lo + (hi - lo) / 2` for an overflow-safe midpoint.
- Make the chosen interval convention and post-loop return contract explicit.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Hash Map + Binary Search | Timestamp lookup; representative: LC 981 Time Based Key-Value Store |
| Teach now | Matrix + Binary Search | Row-major index mapping supports LC 74; independently sorted rows/columns require staircase elimination in LC 240 |
| Deferred | Sorting + Binary Search | Sorting-specific search applications stay with later owner where needed |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Continuous binary search:** add an advanced answer-space variant for real-valued monotone predicates. State the numeric interval and desired absolute/relative error. A fixed iteration count is a bounded convergence policy; `hi - lo > epsilon` is valid only when epsilon has a meaningful scale and the interval still changes under `double` arithmetic.
- **Precision boundary:** do not promise that any fixed count gives maximal precision for every scale. Return an endpoint or midpoint according to the problem's error contract.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** two-pointers, heaps, dynamic programming.

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
