# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Node Invariants  ->  01-node-invariants.md
02. Reverse  ->  02-reverse.md
03. Partial And K-Group Reversal  ->  03-partial-and-k-group-reversal.md
04. Merge  ->  04-merge.md
05. Dummy Heads  ->  05-dummy-heads.md
06. Cycle Entry  ->  06-cycle-entry.md
07. Intersection  ->  07-intersection.md
08. Middle Nodes  ->  08-middle-nodes.md
09. Fixed-Gap Kth From End  ->  09-fixed-gap-kth-from-end.md
10. Multilevel Flattening  ->  10-multilevel-flattening.md

# Chapter 14: Linked lists

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| node invariants | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| reverse | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| partial/k-group reversal | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| merge | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| dummy heads | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| cycle entry | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| intersection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| middle nodes | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| fixed-gap kth-from-end | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| multilevel flattening | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Linked List Map

The linked list supplies node identity and outgoing references; the map records which clone corresponds to each original node. Values alone cannot reconstruct arbitrary `random` edges, and pointer traversal alone cannot find a clone by original identity in constant time.

- **Build - Author exercise: Original-To-Clone Map.** Create one clone for every original node and store the identity mapping.
- **Vary - LC 138 Copy List with Random Pointer.** Use a second pass to wire `next` and `random` through the map.
- **Boundary - Author exercise: Null, Self, And Shared Random Targets.** Preserve all three reference cases without cloning a target twice.
- **Recognize - Author exercise: Two Arbitrary References.** Clone nodes containing `next`, `randomA`, and `randomB` by reusing the same identity-map invariant.

### Deferred: LRU Cache Composition

An LRU cache needs a map for direct lookup plus a doubly linked recency list with strict ownership around sentinels. Chapter 33 introduces the design API and owns that combination staircase.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use a dummy node only when its ownership simplifies the returned head contract.
- Guard pointer rewiring order so the unreached suffix is never lost.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Linked List + Hash Map | Original-to-clone identity mapping; representative: LC 138 |
| Deferred | Hash Map + Linked List Cache | Chapter 33 adds API and recency-list ownership |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** cache design and multi-list design structures beyond the released random-pointer copy.

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
