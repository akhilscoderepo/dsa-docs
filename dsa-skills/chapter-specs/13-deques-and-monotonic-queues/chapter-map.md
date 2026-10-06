# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Use ArrayDeque From Both Ends  ->  01-arraydeque-mechanics.md
02. Give Each End One Job  ->  02-front-and-back-invariants.md
03. Remove Weaker Values From The Back  ->  03-dominated-back-eviction.md
04. Remove Old Indices From The Front  ->  04-expired-front-eviction.md
05. Find The Maximum Of Every Window  ->  05-sliding-maximum.md
06. Find The Minimum Of Every Window  ->  06-sliding-minimum.md
07. Allow Only Recent Positions  ->  07-index-expiry.md
08. Find The Shortest Subarray With Negatives  ->  08-shortest-subarray-deque-state.md

# Chapter 13: Deques and monotonic queues

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| `ArrayDeque` | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| front/back invariants | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| dominated-back eviction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| expired-front eviction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sliding maximum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sliding minimum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| index expiry | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| shortest-subarray deque state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Deque And Sliding Window

The sliding window supplies changing eligibility boundaries; the monotonic deque keeps only candidates that could still answer an extreme-value query. The combined state must enforce chronology, expiry, and value order.

- **Build - Author exercise: Fixed-Window Maximum Trace.** Separate front expiry from back domination on a short array.
- **Vary - LC 239 Sliding Window Maximum.** Produce every fixed-window maximum in linear time.
- **Boundary - LC 1438 Longest Continuous Subarray With Absolute Difference Less Than or Equal to Limit.** Coordinate maximum and minimum deques while `left` may move repeatedly.
- **Recognize - LC 862 Shortest Subarray with Sum at Least K.** Recognize prefix indices as the moving candidates even though the original array contains negatives.

### Deferred: Deque And Graph BFS

Zero-one BFS uses a deque to prioritize zero-cost transitions ahead of one-cost transitions. Graph state and shortest-path correctness are not available yet; Chapters 21 and 24 own that composition.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `ArrayDeque` and state which end owns insertion and removal.
- Expire indices before using a front value outside the current window.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Deque + Sliding Window | Index expiry and monotone value state; staircase: fixed max → LC 239 → LC 862 |
| Deferred | Deque + Graph BFS | Chapter 21/24 owns graph state and 0-1 BFS |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Bidirectional deque maintenance:** make the two jobs explicit: pop stale indices from the front before reading an answer, and pop dominated values from the back before appending the new index. The deque stores indices so chronology and values can both be checked.
- **Expiry contract:** for a size-`k` window ending at `right`, an index `<= right - k` is expired. Test repeated equal values and a jump beyond one expired index.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** graph BFS and dynamic-programming optimizations beyond the introductory recent-state example.

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
