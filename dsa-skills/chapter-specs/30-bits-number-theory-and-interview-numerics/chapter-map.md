# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Bit Masks  ->  01-bit-masks.md
02. Shifts  ->  02-shifts.md
03. Low Bit  ->  03-low-bit.md
04. XOR Cancellation  ->  04-xor-cancellation.md
05. Subset Masks  ->  05-subset-masks.md
06. Overflow  ->  06-overflow.md
07. Binary Arithmetic  ->  07-binary-arithmetic.md
08. GCD And Power  ->  08-gcd-and-power.md
09. Sieve  ->  09-sieve.md
10. Modular Arithmetic  ->  10-modular-arithmetic.md

# Chapter 30: Bits, number theory, and interview numerics

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| masks | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| shifts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| low-bit operations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| XOR | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| subset masks | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| overflow | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| binary arithmetic | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| gcd/fast power | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sieve | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| modular arithmetic | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Bits With Search State

A mask compresses subset membership; DP or graph search stores a distinct answer for each structural state plus that mask.

- **Build - LC 78 Subsets.** Interpret every mask as one subset.
- **Vary - LC 187 Repeated DNA Sequences.** Encode a fixed-width character window in bits.
- **Boundary - LC 318 Maximum Product of Word Lengths.** Test disjointness and protect product width.
- **Recognize - LC 847 Shortest Path Visiting All Nodes.** BFS over `(node, visitedMask)` until the full mask is reached.

### Deferred: Bitmask DP Ownership

Full assignment/profile DP is authored in Chapter 29, whose lesson includes a self-contained mask primer. This chapter consolidates and broadens those bit mechanics, so the numbered order no longer creates an unstated prerequisite.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use parentheses around shifts and document signed versus unsigned behavior.
- Use `long` masks when bit positions can exceed the `int` range.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Bits + DP/Search State | A mask encodes subset membership; representative: subset iteration and bitmask DP foundations |
| Already covered | Bitmask DP | Chapter 29 owns full assignment/profile state and includes its own mask primer; this chapter consolidates the general bit mechanics |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** no additional bitmask composition; Chapter 29 owns the full assignment/profile DP after this chapter's mask prerequisite.

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
