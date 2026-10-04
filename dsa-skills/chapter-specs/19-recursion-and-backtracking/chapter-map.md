# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Call State  ->  01-call-state.md
02. Choose Explore Unchoose  ->  02-choose-explore-unchoose.md
03. Subsets  ->  03-subsets.md
04. Permutations  ->  04-permutations.md
05. Increasing-Start Combinations  ->  05-increasing-start-combinations.md
06. Reusable Candidates  ->  06-reusable-candidates.md
07. Duplicate Control  ->  07-duplicate-control.md
08. Proof-Based Pruning  ->  08-proof-based-pruning.md
09. Partition Generation  ->  09-partition-generation.md
10. Board Constraints  ->  10-board-constraints.md

# Chapter 19: Recursion and backtracking

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| call state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| choose/explore/unchoose | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| subsets | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| permutations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| increasing-start combinations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| reusable-candidate combination sum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| duplicate control | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| proof-based pruning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| partition generation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| board constraints | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Trie And Backtracking

Backtracking owns the current board path and restores visited cells; the trie represents every dictionary prefix still compatible with that path. A trie without path search cannot move across the board, while independent word searches repeat the same prefixes.

- **Build - Author exercise: Trie-Guided Row Search.** Walk adjacent cells on one row while advancing a trie node and emitting terminal words.
- **Vary - Author exercise: Stop On Missing Trie Edge.** Replace one target index with a trie node and prune impossible prefixes.
- **Boundary - Author exercise: Shared Prefix And Duplicate Discovery.** Emit one word once even when several paths reach its terminal node.
- **Recognize - LC 212 Word Search II.** Search all words simultaneously through trie-guided board backtracking.

### Deferred: Backtracking And Memoization

Memoization is safe only after equivalent call states and their return meaning are defined precisely. Chapter 26 introduces that dynamic-programming contract and owns the combination.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Make choose/explore/unchoose mutation order visible.
- Copy a completed path before storing it when later backtracking will mutate the working list.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Trie + Backtracking | Trie prunes board search; representative: LC 212 Word Search II |
| Deferred | Backtracking + Memoization | Chapter 26 supplies DP state definition |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** memoized pruning.

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
