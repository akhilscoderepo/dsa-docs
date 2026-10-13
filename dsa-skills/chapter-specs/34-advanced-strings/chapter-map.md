# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Rolling Hash  ->  01-rolling-hash.md
02. Prefix Matching  ->  02-prefix-matching.md
03. Palindrome Radii  ->  03-palindrome-radii.md
04. Suffix Structures  ->  04-suffix-structures.md
05. Aho Corasick  ->  05-aho-corasick.md

# Chapter 34: Advanced strings

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| rolling hash | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| KMP/Z algorithm | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| palindrome radii | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| suffix arrays/automata | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Aho-Corasick multi-pattern matching | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Stream Matching With Failure Links

Trie nodes encode prefixes; failure transitions make that prefix state reusable after mismatches and across a stream.

- **Build - LC 28 Find the Index of the First Occurrence in a String.** Establish reusable prefix fallback with KMP.
- **Vary - LC 459 Repeated Substring Pattern.** Interpret prefix structure as repeated period length.
- **Boundary - LC 1392 Longest Happy Prefix.** Require a proper prefix and suffix rather than the whole string.
- **Recognize - LC 1032 Stream of Characters.** Preserve multi-pattern automaton state between API calls.

### Deferred: Specialized String DP

Problem-specific string/DP compositions remain with their owning recurrence rather than being duplicated here.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use a collision policy for rolling hash and make alphabet/encoding assumptions explicit.
- Avoid substring allocation in repeated pattern checks when indexes suffice.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Prefix Automata + Stream State | KMP/Z prefix state and trie failure links summarize active matches; representative: LC 1032 |
| Deferred | Strings + DP/Trie compositions | Release only with the owning DP or trie invariant |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** trie/DP/string compositions.

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
