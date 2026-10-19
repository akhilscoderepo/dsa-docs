# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Mutable Range Queries  ->  01-mutable-range-queries.md
02. Interval Unions  ->  02-interval-unions.md
03. Ordered Structures  ->  03-ordered-structures.md
04. Query Planning  ->  04-query-planning.md
05. Dynamic Graph Queries  ->  05-dynamic-graph-queries.md

# Chapter 39: Dynamic query structures

**Status:** Authored curriculum specification; PDF generation remains pending.

## Purpose

Teach design APIs that interleave updates with range, order, connectivity, or shortest-path queries. Earlier chapters taught the underlying algorithms; this chapter teaches how to preserve their invariants across public calls.

## Entry Contract

Prefix sums, Fenwick and segment trees, ordered sets, intervals, binary lifting, union-find, and shortest paths are prerequisites.

## Mastery Scope

The required LeetCode anchors are LC 352, LC 715, LC 1622, and LC 2642. LC 1206 and LC 2276 are transfer problems. Other numbered problems in this specification are taxonomy examples or prerequisite reviews; they are not assigned work and do not receive complete solutions in the PDF.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| immutable-to-mutable query upgrades | Explain why preprocessing alone fails after updates. |
| dynamic interval unions | Maintain canonical disjoint coverage under additions/removals. |
| explicit ordered structures | Implement or reason about ordered search when library structures are unavailable. |
| deferred algebraic transforms | Compose range-wide operations without replaying the whole history. |
| static versus online query planning | Choose offline sorting, preprocessing, or a mutable index from the call contract. |
| dynamic tree and graph query APIs | Recompute or incrementally maintain expensive graph/tree answers under updates. |



## Released Combination Lessons

### Ordered Interval State

- **Build - LC 352 Data Stream as Disjoint Intervals.** Canonicalize point insertions.
- **Vary - LC 715 Range Module.** Add deletion and half-open queries.
- **Boundary - LC 2276 Count Integers in Intervals.** Preserve covered length through multi-interval merges.
- **Recognize - Author exercise: Dynamic Coverage API.** Select ordered-map or segment-tree state from the coordinate domain.

### Preprocessed Query APIs

- **Build - LC 1483 Kth Ancestor of a Tree Node.** Expose binary lifting through an object.
- **Vary - LC 2080 Range Frequency Queries.** Expose position indexes.
- **Boundary - LC 1724 Checking Existence of Edge Length Limited Paths II.** Respect online versus offline constraints.
- **Recognize - LC 2642 Design Graph With Shortest Path Calculator.** Choose update/query tradeoffs explicitly.

## Practice Contract

Every problem must state the update/query ratio and whether calls are known in advance; those facts are algorithmic inputs. Use interval traces and focused update/query comparisons for the early staircase roles. Fully expand the four required anchors; present the two transfer problems as interview prompts with hints and review notes rather than complete code.

## Java Integrity Focus

- Use `long` for covered lengths and path sums.
- State half-open versus closed intervals before writing comparisons.
- Avoid comparator subtraction and unbounded stale heap growth.

## Unlocked Combinations Preview

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Ordered Set + Intervals | Canonical disjoint state and endpoint semantics remain visible. |
| Teach now | Graph/Tree Preprocessing + API | Constructor/update/query ratios justify the maintained index. |
| Already covered | Fenwick and segment trees | Chapter 31 owns the base structures. |

## Composition Audit

All algorithmic prerequisites are complete; this chapter adds persistent API ownership and workload-based selection.

## Publication Gate

- Include update/query-ratio comparisons in every design choice.
- Test touching intervals, repeated assignment, duplicate keys, and graph corrections.
- Render and validate the final PDF.

## Research Baseline

- [LeetCode Design problem list](https://leetcode.com/problem-list/design/).
- [Design-tag crosswalk](../design-tag-crosswalk.md).
- Oracle navigable collections and priority queue documentation.
