# Chapter map (generated; do not edit, edit the source spec)

This chapter teaches the language used to reason about every later problem. Its exercises are deliberately small: the learner should practice reading a contract, predicting a cost, and constructing a hostile test before a named algorithm competes for attention.

## Lesson order

01. Reading Input Limits Before Choosing An Algorithm  ->  01-constraint-signals.md
02. Whether A Method May Modify Its Input  ->  02-mutation-contracts.md
03. Subarrays, Subsequences And Subsets Compared  ->  03-sequence-language.md
04. Input Preconditions And Edge Cases  ->  04-input-guarantees.md
05. Comparing Time And Space Complexity Trade-Offs  ->  05-complexity-tradeoffs.md
06. Amortized Time Complexity  ->  06-amortized-cost.md
07. Writing Edge-Case Tests  ->  07-hostile-dry-runs.md
08. Time Complexity Of Common Java Methods  ->  08-java-cost-habits.md

# Chapter 00: Problem contracts, complexity, and sequence language

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| constraints as algorithm signals | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| mutation/space contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| subarray versus subsequence | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| input guarantees | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| complexity tradeoffs | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| amortized analysis (accounting/potential intuition) | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| adversarial dry-runs | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Java API/code-quality habits | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Foundation Exit Check

Before Chapter 01, the learner should be able to read a prompt and state: the meaningful input guarantees; whether mutation is allowed; what output portion is valid; the sequence relationship being requested; the plausible time/space budget; one adversarial test; and any Java API operation that changes the claimed complexity. No new algorithm is unlocked here, but every later lesson assumes this language.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- State the input and mutation contract before writing guards.
- Name asymptotic costs of the Java operation actually used.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| No teach-now combination | Foundations only | Specific structures and algorithms |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** specific data structures and algorithms.

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
