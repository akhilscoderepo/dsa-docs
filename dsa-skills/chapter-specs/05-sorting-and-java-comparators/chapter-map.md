# Chapter map (generated; do not edit, edit the source spec)

Sorting is not the answer by itself. It is a transformation that makes a later local decision valid; every lesson names the order and the decision it unlocks.

## Lesson order

01. Ordering Contracts  ->  01-ordering-contracts.md
02. Arrays Sort  ->  02-arrays-sort.md
03. Comparator Contracts  ->  03-comparator-contracts.md
04. Object Ordering  ->  04-object-ordering.md
05. Stability And Ties  ->  05-stability-and-ties.md
06. Sort And Sweep  ->  06-sort-and-sweep.md
07. Sort And Deduplicate  ->  07-sort-and-deduplicate.md
08. Sort Then Scan  ->  08-sort-then-scan.md

# Chapter 05: Sorting and Java comparators

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| ordering contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| `Arrays.sort` | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| `Comparator` | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| custom objects | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| stability guarantees and tie ownership | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sort-and-sweep | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sort-and-deduplicate | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sort-then-scan | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Strings, Maps, And Sorting

**What each part contributes.** String traversal supplies characters; sorting produces a canonical sequence; the map uses that sequence as a grouping key. **Recognition cue.** Different strings belong together when their character multisets agree. **False friend.** A frequency-array signature is valid only under a stated alphabet contract; it is a variation, not the reason sorted signatures work.

- **Build - LC 242 Valid Anagram.** Sort both character arrays and compare the canonical forms.
- **Vary - LC 49 Group Anagrams.** Use each sorted string as a `HashMap` key whose value is the group list.
- **Boundary - LC 451 Sort Characters by Frequency.** Separate the canonical-key decision from output ordering by frequency.
- **Recognize - LC 1657 Determine if Two Strings Are Close.** Compare the two character sets and their frequency multisets; a raw sorted string is insufficient.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `Integer.compare` or `Long.compare`; comparator subtraction can overflow.
- A custom comparator applies to object arrays, not `int[]`.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Already covered | Arrays + Sorting | Sort-and-sweep and sorted-run lessons own the relation |
| Teach now | Strings + Maps + Sorting | Canonical signature groups; staircase: LC 49 → count signature → multiplicity boundary → LC 1657 |
| Deferred | Sorting + Two Pointers | Chapter 08 supplies safe pointer movement and duplicate policy |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Stability contract:** add a stability decision. `Arrays.sort(Object[])` promises a stable sort, while primitive-array sorting offers no stability guarantee the algorithm may rely on. If equal values need original-position tie order, retain index/object state and make that order part of the comparator or use a stable object sort.
- **Do not teach implementation folklore as an invariant:** the useful interview rule is the API guarantee and the required tie behavior, not memorizing a specific internal sort implementation.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** intervals, greedy, binary-search-on-sorted-input, quickselect.

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
