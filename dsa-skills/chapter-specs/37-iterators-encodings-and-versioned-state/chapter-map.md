# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Iterator Protocols  ->  01-iterator-protocols.md
02. Nested Iteration  ->  02-nested-iteration.md
03. Structural Codecs  ->  03-structural-codecs.md
04. Version Histories  ->  04-version-histories.md
05. Query Objects  ->  05-query-objects.md
06. Incremental Trees  ->  06-incremental-trees.md

# Chapter 37: Iterators, encodings, and versioned state

**Status:** Authored curriculum specification; PDF generation remains pending.

## Purpose

Teach APIs that expose a large or structured value incrementally, encode it for later reconstruction, or answer queries against a historical version.

## Entry Contract

Stacks, queues, trees, tries, prefix sums, binary lifting, and ordinary iterator state are prerequisites. The chapter distinguishes materialized output from resumable state.

## Mastery Scope

The required LeetCode anchors are LC 900, LC 1286, LC 1146, and LC 2080. LC 449 and LC 1993 are transfer problems. Other numbered problems in this specification are taxonomy examples or prerequisite reviews; they are not assigned work and do not receive complete solutions in the PDF.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| iterator protocol state | Separate observation, availability, consumption, and exhaustion. |
| nested and multi-source iteration | Preserve unfinished traversal state without flattening the entire input. |
| structural codecs | Make encoding unambiguous and decoding consume exactly one representation. |
| versioned snapshots | Separate logical versions from physical copies through change histories. |
| preprocessed query objects | Spend constructor work to make repeated queries cheaper. |
| incremental tree APIs | Maintain traversal or hierarchy state as the represented tree changes. |



## Released Combination Lessons

### Iterator Traversal State

- **Build - LC 284 Peeking Iterator.** Separate cached observation from source advancement.
- **Vary - LC 900 RLE Iterator.** Advance by a logical count.
- **Boundary - LC 341 Flatten Nested List Iterator.** Skip empty nested containers.
- **Recognize - LC 1586 Binary Search Tree Iterator II.** Preserve reversible traversal history.

### Codec Structural Traversal

- **Build - Author exercise: Length-Prefixed String Codec.** Make token boundaries explicit.
- **Vary - LC 297 Serialize and Deserialize Binary Tree.** Preserve null structure.
- **Boundary - LC 431 Encode N-ary Tree to Binary Tree.** Preserve ordered child ownership.
- **Recognize - LC 449 Serialize and Deserialize BST.** Exploit ordering without losing reconstructability.

## Practice Contract

Each independent protocol retains a Build-to-Recognize staircase, but the early roles may be cursor traces, encoding drills, or invariant checks rather than full LeetCode solutions. Fully expand the four required anchors; present the two transfer problems as interview prompts with hints and review notes rather than complete code.

## Java Integrity Focus

- State whether exhausted `next()` is forbidden or throws.
- Avoid recursive eager flattening when the contract requires lazy iteration.
- Use `long` for version/timestamp arithmetic when constraints require it.

## Unlocked Combinations Preview

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Iterator + Traversal State | Stack/cursor state must survive arbitrary call sequences. |
| Teach now | Codec + Structural Traversal | Encoding and decoding share one grammar and shape contract. |
| Already covered | Binary lifting | Chapter 29/30 foundations support LC 1483 as advanced review. |

## Composition Audit

The chapter releases iterator/tree, string/codec, and binary-search/history combinations because all participating techniques are already taught.

## Publication Gate

- Trace repeated `hasNext`, `peek`, exhaustion, and malformed-boundary cases.
- Verify every codec is injective over the stated input domain.
- Check historical queries at versions before the first and after the last update.
- Render and validate the final PDF.

## Research Baseline

- [LeetCode Design problem list](https://leetcode.com/problem-list/design/).
- [Design-tag crosswalk](../design-tag-crosswalk.md).
- Oracle Iterator and Collections documentation.
