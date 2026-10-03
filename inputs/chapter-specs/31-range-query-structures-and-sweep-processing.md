# Chapter 31: Range-query structures and sweep processing

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| Fenwick tree | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| segment tree | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| lazy propagation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| coordinate compression | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sweep-line event state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Sweep + Ordered State | LC 1094 Car Pooling | LC 218 The Skyline Problem | Author exercise: equal-coordinate event ties | LC 732 My Calendar III |
| Coordinate Compression + Fenwick Tree | Author exercise: compress sparse coordinates | LC 307 Range Sum Query - Mutable | Author exercise: negative/extreme coordinates | LC 1649 Create Sorted Array through Instructions |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Fenwick Trees

**Recognition cue.** Point updates and prefix/range sums must both be logarithmic. **Invariant.** Tree index `i` stores the block ending at `i` whose length is `i & -i`; implementation uses one-based indexing.

- **Build - Author exercise: Prefix Query.** Repeatedly subtract the low bit.
- **Vary - Author exercise: Point Update.** Add a delta while repeatedly adding the low bit.
- **Boundary - Author exercise: Index Conversion.** Map external zero-based positions to internal one-based positions.
- **Recognize - LC 307 Range Sum Query - Mutable.** Compute range sums as two prefixes and update by delta.

### Segment Trees

**Recognition cue.** Associative range queries and point updates need more flexible state than prefix subtraction. **Invariant.** Every node stores the aggregate for one exact interval, combined from its children.

- **Build - Author exercise: Build Range Sums.** Recursively split and combine one array.
- **Vary - Author exercise: Point Assignment.** Update one leaf and recompute ancestors.
- **Boundary - Author exercise: No Overlap And Full Cover.** Return the operator identity or the stored node aggregate.
- **Recognize - LC 307 Range Sum Query - Mutable.** Implement mutable range sum with a segment tree.

### Lazy Propagation

**Recognition cue.** Updates affect whole ranges and immediate descent would be too expensive. **Invariant.** A lazy tag records an update already applied to the node aggregate but not yet pushed to children.

- **Build - Author exercise: Range Add One Node.** Update aggregate by overlap length and store a pending delta.
- **Vary - Author exercise: Push Before Descent.** Transfer the tag to both children exactly once.
- **Boundary - Author exercise: Assignment Versus Addition Tags.** State composition order; they are not interchangeable.
- **Recognize - Author exercise: Range Add Range Sum.** Support both operations in logarithmic time.

### Coordinate Compression

**Recognition cue.** Values are sparse or huge, but only relative order and equality matter. **Invariant.** Each distinct value maps to a dense rank preserving order.

- **Build - Author exercise: Compress Distinct Values.** Sort, deduplicate, and map ranks.
- **Vary - Author exercise: Preserve Equal Ranks.** Give duplicates the same coordinate.
- **Boundary - Author exercise: Negative And Extreme Values.** Compare safely and do not use values as raw array indices.
- **Recognize - LC 1649 Create Sorted Array through Instructions.** Query counts below and above each compressed rank with a Fenwick tree.

### Sweep Events

**Recognition cue.** State changes only at sorted coordinates or times. **Invariant.** After applying events under the stated tie policy, active state represents exactly the interval between this coordinate and the next.

- **Build - LC 1094 Car Pooling.** Add passenger deltas at pickup and drop-off coordinates.
- **Vary - Author exercise: Group Equal Coordinates.** Apply all same-position deltas before evaluating the next span.
- **Boundary - Author exercise: Start-End Tie.** Choose event order from closed or half-open semantics.
- **Recognize - LC 218 The Skyline Problem.** Maintain active heights while sweeping building boundaries.

## Released Combination Lessons

### Sweep And Ordered State

Event sorting determines when state changes; ordered structures summarize active values or compressed prefixes between events.

- **Build - LC 1094 Car Pooling.** Sweep capacity deltas in coordinate order.
- **Vary - LC 218 The Skyline Problem.** Maintain the greatest active height with explicit tie rules.
- **Boundary - Author exercise: Equal-Coordinate Events.** Group or order starts and ends according to the interval contract.
- **Recognize - LC 732 My Calendar III.** Maintain booking deltas and compute the maximum active overlap.

### Compression And Fenwick

Coordinate compression preserves order while replacing sparse values with dense ranks; the Fenwick tree maintains prefix aggregates over those ranks.

- **Build - Author exercise: Compress Sparse Coordinates.** Sort distinct values and map each to one-based rank.
- **Vary - LC 307 Range Sum Query - Mutable.** Maintain prefix sums with point-update deltas.
- **Boundary - Author exercise: Negative And Extreme Coordinates.** Compare safely and keep equal values on one rank.
- **Recognize - LC 1649 Create Sorted Array through Instructions.** Query counts strictly below and above each inserted value.

### Deferred: Specialized Range Applications

Persistent trees and multidimensional range structures require separate update/query contracts and remain outside the active core.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Choose `long` tree sums when update/query totals demand it.
- Explain one-based versus zero-based indexing in Fenwick and segment-tree arrays.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Sweep + Ordered State | Events are processed in coordinate order; representative: line sweep and coordinate compression |
| Teach now | Coordinate Compression + Fenwick Tree | Sparse values become ordered ranks supporting prefix-count updates and queries |
| Deferred | Persistent/multidimensional range structures | Release only when the version or dimensional query contract is explicit |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** persistent and multidimensional range structures.

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

