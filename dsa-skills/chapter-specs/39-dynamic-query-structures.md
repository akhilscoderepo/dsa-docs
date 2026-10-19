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

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

### Supplied Progression

The crosswalk assigns 10 problems here and reuses Chapters 23, 24, 29, 31, and 32 as algorithmic prerequisites.

### Pattern References

| Micro-pattern | Recognition cue | Representative progression |
| --- | --- | --- |
| Mutable range query | Point/range updates interleave with queries | LC 307, LC 308 |
| Interval union | Add/remove/query covered coordinates | LC 352, LC 715, LC 2276 |
| Ordered structure | Search/insert/erase expected logarithmic | LC 1206 |
| Deferred transform | Append plus global affine update | LC 1622 |
| Query planning | Static data permits specialized preprocessing | LC 1157, LC 2080, LC 1724 |
| Dynamic graph service | Add edges then answer shortest path | LC 2642 |

### Released Combination Ladders

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Ordered Set + Intervals | LC 352 | LC 715 | LC 2276 | Author dynamic coverage API |
| Graph/Tree Preprocessing + API | LC 1483 review | LC 2080 | LC 1724 | LC 2642 |
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Mutable Range Queries

**Recognition cue.** Queries are no longer separated from updates. **Invariant.** Every tree node or Fenwick entry summarizes exactly its owned range after each mutation.

- **Build - LC 307 Range Sum Query - Mutable.** Upgrade prefix sums to point updates.
- **Vary - LC 308 Range Sum Query 2D - Mutable.** Extend ownership to two dimensions.
- **Boundary - Author exercise: Repeated Assignment.** Apply delta from the old value rather than adding the new value twice.
- **Recognize - Author exercise: Mutable Range Minimum.** Explain when a segment tree replaces a Fenwick tree.

### Interval Unions

**Recognition cue.** Public methods add, remove, or count covered coordinates over time. **Invariant.** Stored intervals remain disjoint, ordered, and use one explicit endpoint convention.

- **Build - LC 352 Data Stream as Disjoint Intervals.** Insert one point and merge adjacent runs.
- **Vary - LC 715 Range Module.** Add removal and coverage queries over half-open ranges.
- **Boundary - Author exercise: Touching And Empty Ranges.** Apply endpoint semantics consistently.
- **Recognize - LC 2276 Count Integers in Intervals.** Maintain total covered length while merging.

### Ordered Structures

**Recognition cue.** The design needs predecessor/successor search and cannot rely on a built-in ordered set. **Invariant.** Search levels or rotations preserve sorted order and reachability.

- **Build - Author exercise: Layered Linked Search.** Search through promoted levels.
- **Vary - LC 1206 Design Skiplist.** Add randomized promotion, insertion, and erase.
- **Boundary - Author exercise: Duplicate Key Policy.** State whether nodes or multiplicities represent duplicates.
- **Recognize - Author exercise: Ordered Multiset API.** Add counts and predecessor queries.

### Deferred Transforms

**Recognition cue.** Appended values coexist with operations affecting every existing value. **Invariant.** Lazy algebra composes operations in order and can translate new values into the current coordinate system.

- **Build - Author exercise: Global Add Sequence.** Store one additive offset.
- **Vary - LC 1622 Fancy Sequence.** Compose multiplication and addition modulo `M`.
- **Boundary - Author exercise: Zero Multiplier.** Explain why modular inverse-based normalization needs special handling.
- **Recognize - Author exercise: Affine Lazy Segment Tree.** Move from whole-sequence to range transforms.

### Query Planning

**Recognition cue.** A constructor is followed by many queries whose constraints may justify preprocessing or offline ordering. **Invariant.** The chosen summary is sufficient for every query without rebuilding original work.

- **Build - LC 2080 Range Frequency Queries.** Store sorted positions per value.
- **Vary - LC 1157 Online Majority Element In Subarray.** Combine candidate selection with occurrence verification.
- **Boundary - Author exercise: No Majority Exists.** Verification must reject plausible but insufficient candidates.
- **Recognize - LC 1724 Checking Existence of Edge Length Limited Paths II.** Contrast online API requirements with offline sorted-query DSU.

### Dynamic Graph Queries

**Recognition cue.** Graph mutations and path queries share one object. **Invariant.** Every returned distance reflects all accepted edges and the chosen recomputation/incremental strategy.

- **Build - Author exercise: Static Shortest-Path Calculator.** Preprocess or run Dijkstra per query.
- **Vary - LC 2642 Design Graph With Shortest Path Calculator.** Add edges between later queries.
- **Boundary - Author exercise: Duplicate And Dominated Edges.** Preserve the minimum useful cost.
- **Recognize - Author exercise: Update-Frequency Tradeoff.** Choose Floyd-Warshall, repeated Dijkstra, or incremental relaxation from constraints.

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

