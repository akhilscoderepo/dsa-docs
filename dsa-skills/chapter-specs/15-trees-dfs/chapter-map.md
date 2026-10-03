# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Tree Representation  ->  01-tree-representation.md
02. Recursive Traversal Orders  ->  02-recursive-traversal-orders.md
03. Iterative DFS  ->  03-iterative-dfs.md
04. Depth And Path State  ->  04-depth-and-path-state.md
05. Diameter And Subtree Returns  ->  05-diameter-and-subtree-returns.md
06. Balance Sentinels  ->  06-balance-sentinels.md
07. Traversal Reconstruction  ->  07-traversal-reconstruction.md
08. Morris Traversal  ->  08-morris-traversal.md
09. Quadtree Construction  ->  09-quadtree-construction.md

# Chapter 15: Trees: DFS

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| binary/N-ary tree representation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| preorder/inorder/postorder recursion | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| iterative DFS | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| depth/height/path state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| diameter and subtree return values | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| balance sentinels | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| tree reconstruction from traversals | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Morris traversal | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| quadtree construction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |



## Released Combination Lessons

### Tree DFS Returns

The tree supplies recursive subproblems; DFS return state compresses each completed subtree into the fact its parent needs. The central design decision is separating the value returned upward from any complete answer formed at the current node.

- **Build - LC 104 Maximum Depth of Binary Tree.** Return one height from two completed child heights.
- **Vary - LC 543 Diameter of Binary Tree.** Return one branch but evaluate a two-branch answer locally.
- **Boundary - LC 110 Balanced Binary Tree.** Propagate a failure sentinel without recomputing heights.
- **Recognize - LC 124 Binary Tree Maximum Path Sum.** Separate upward gain from a path that may turn through the current node.

### Deferred: Tree And BFS

DFS does not preserve distance layers. Chapter 16 adds the level-sized queue frontier and owns level order, zigzag output, and tree views.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Return recursion state rather than relying on mutable globals when possible.
- Define the `null`-node base case as part of the traversal contract.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Tree + DFS Return State | Subtree facts returned to parent; staircase: depth → diameter → balanced tree |
| Deferred | Tree + BFS | Chapter 16 supplies level-frontier state |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** BFS, BST-specific ordering.

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
