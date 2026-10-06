# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Read A Tree Level By Level  ->  01-levels-zigzag-and-views.md
02. Carry Value Limits Down A Search Tree  ->  02-bst-invariant-and-bounds.md
03. Search And Insert With One Path  ->  03-validate-search-and-insert.md
04. Find The Next And Previous Key  ->  04-successor-and-predecessor.md
05. Answer Rank And Range Questions  ->  05-kth-and-range-queries.md
06. Find The Lowest Common Ancestor  ->  06-general-and-bst-lca.md
07. Walk A Tree One Key At A Time  ->  07-iterator-foundations.md
08. Turn A Tree Into Text And Back  ->  08-serialization-and-deserialization.md
09. Keep A Search Tree Short  ->  09-balanced-tree-concepts.md

# Chapter 16: Trees: BFS and BSTs

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| queue levels and zigzag/views | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| BST invariant/bounds | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| validate/search/insert | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| successor/predecessor | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| kth/range queries | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| general-tree and BST lowest common ancestor | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| iterator foundations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| serialization/deserialization | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| balanced-tree concepts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Group Nodes By Depth With A Queue

The tree supplies children; the FIFO queue preserves discovery by depth. Capturing the current queue size turns ordinary queue processing into an exact level boundary.

- **Build - LC 102 Binary Tree Level Order Traversal.** Produce one output list per frontier.
- **Vary - LC 103 Binary Tree Zigzag Level Order Traversal.** Reverse output direction without changing enqueue order.
- **Boundary - LC 199 Binary Tree Right Side View.** Select exactly the last node of each captured level.
- **Recognize - LC 429 N-ary Tree Level Order Traversal.** Generalize child expansion from two references to a child collection.

### Search And Validate A Search Tree

BST ordering narrows the legal range inherited by each descendant. Bounds make the global property explicit; local parent-child checks alone cannot validate the structure.

- **Build - LC 700 Search in a Binary Search Tree.** Use one comparison to discard one subtree.
- **Vary - LC 98 Validate Binary Search Tree.** Carry strict ancestor bounds through every recursive call.
- **Boundary - LC 230 Kth Smallest Element in a BST.** Use inorder order rather than numeric bounds to answer a rank query.
- **Recognize - LC 450 Delete Node in a BST.** Preserve ordering while reconnecting children after deletion.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `ArrayDeque` for level queues and record queue-level size before consuming that level.
- State duplicate/equality policy in BST bounds.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Tree + BFS | Level-sized queue state; staircase: levels → zigzag → right view |
| Teach now | BST + Bounds | Ancestor bounds, not local child comparison, prove validity; representative: LC 98 |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** heap traversal.

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
