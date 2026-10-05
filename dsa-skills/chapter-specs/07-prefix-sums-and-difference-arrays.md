# Chapter 07: Prefix sums and difference arrays

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| one-dimensional prefix | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| range query | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| prefix/suffix exclusion state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| prefix-count maps | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| earliest-index/balance maps | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| remainder-class maps | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| prefix XOR | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| difference/range updates | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 2D prefix | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 2D difference rectangle updates | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0002 | Array traversal and running state | Find Pivot Index | Immediate application | Reuses cumulative information to compare both sides. |
| P0007 | Prefix sum | Range Sum Query - Immutable | Direct concept | Makes repeated range queries constant time after preprocessing. |
| P0008 | Prefix sum + hash map | Subarray Sum Equals K | Combination | Combines cumulative state with frequency lookup. |
| P0011 | Subarray state | Maximum Subarray | New variation | Introduces Kadane-style best-ending-here state. |
| P0012 | Prefix/suffix state | Product of Array Except Self | New variation | Builds reusable left/right information without division. |
| Bundle 1-1 | Prefix Sum | Running Sum of 1d Array | Learn | — |
| Bundle 1-2 | Prefix Sum | Range Sum Query - Immutable | Extend | — |
| Bundle 1-3 | Prefix/Suffix | Find Pivot Index | Twist | — |
| Bundle 1-1 | Subarray + Prefix Hashing | Subarray Sum Equals K | Learn | — |
| Bundle 1-2 | Subarray + Prefix Hashing | Subarray Sums Divisible by K | Extend | — |
| Bundle 1-3 | Subarray + Prefix Hashing | Contiguous Array | Twist | — |
| Bundle 1-1 | 2D Prefix Sum | Matrix Block Sum | Learn | — |
| Bundle 1-2 | 2D Prefix Sum | Range Sum Query 2D - Immutable | Extend | — |
| Bundle 2-1 | Subarray + Prefix Hashing | Subarray Sum Equals K | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Prefix/suffix state | Need left/right aggregate at each index | Each position gets information from all earlier/later positions without rescanning | https://leetcode.com/problems/product-of-array-except-self/ | Core |
| Boundary marking | Many interval updates, final array needed | An interval's effect starts at l and stops after r | https://leetcode.com/problems/corporate-flight-bookings/ | Core |
| Look up prefix-target | Need count subarrays satisfying additive relation | Subarray sum equals difference between two prefix states | https://leetcode.com/problems/subarray-sum-equals-k/ | Core |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Prefix State + Hash Map | LC 560 Subarray Sum Equals K | LC 525 Contiguous Array | LC 974 Subarray Sums Divisible by K | LC 523 Continuous Subarray Sum |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Build Running Totals

**Recognition cue.** Later work repeatedly needs the aggregate of everything before a position. **State.** With a sentinel convention, `prefix[i]` is the sum of the first `i` values. **Java hazard.** Use `long` when the maximum possible total exceeds `int`.

- **Build - LC 1480 Running Sum of 1d Array.** Construct cumulative sums from left to right.
- **Vary - LC 724 Find Pivot Index.** Compare `prefix before i` with `total - prefix through i`.
- **Boundary - Author exercise: Empty Prefix.** Define `prefix[0] = 0`; verify an empty range contributes zero.
- **Recognize - Author exercise: Prefix Averages.** Reuse cumulative totals while dividing by the correct number of values.

### Answer Range Sum Queries

**Recognition cue.** The input is unchanged and many contiguous range sums are requested. **Invariant.** `sum(left..right) = prefix[right+1] - prefix[left]` under the sentinel convention. **False friend.** A sliding window answers one moving family of ranges; it does not provide arbitrary query lookup.

- **Build - LC 303 Range Sum Query - Immutable.** Preprocess once and answer each query in `O(1)`.
- **Vary - Author exercise: Half-Open Query.** Accept `[left,right)` and derive the corresponding formula.
- **Boundary - Author exercise: Whole Array.** Query `[0,n-1]` without reading before index zero.
- **Recognize - LC 1310 XOR Queries of a Subarray.** Replace addition/subtraction with XOR cancellation; the dedicated XOR lesson follows.

### Combine Totals From Both Sides

**Recognition cue.** Every output position needs an aggregate of all elements except itself. **State.** A left pass stores the aggregate before `i`; a right pass folds the aggregate after `i`. **False friend.** Division may be forbidden or invalid around zeros.

- **Build - Author exercise: Sum Except Self.** Return total-minus-current using `long` under an additive contract.
- **Vary - LC 238 Product of Array Except Self.** Build left products, then multiply by a rolling right product without division.
- **Boundary - LC 238 With Zeros.** Verify one zero and multiple zeros without special division cases.
- **Recognize - Author exercise: Prefix And Suffix Maximums.** Give every index the best value strictly to its left and right.

### Count Subarrays With A Target Sum

**Recognition cue.** Count subarrays whose additive relation can be written as `currentPrefix - earlierPrefix = target`. **State.** A frequency map records how many earlier prefixes have each value. **Invariant.** Seed prefix zero once so subarrays beginning at index zero are counted.

- **Build - LC 560 Subarray Sum Equals K.** Look up `prefix - k` before recording the current prefix.
- **Vary - LC 930 Binary Subarrays With Sum.** Apply the same count state to a binary domain.
- **Boundary - Author exercise: Zero Target.** Repeated equal prefixes create multiple zero-sum subarrays; a set would undercount them.
- **Recognize - LC 1248 Count Number of Nice Subarrays.** Convert odd values to one and count target-sum subarrays.

### Find The Longest Balanced Span

**Recognition cue.** The goal is the longest span between two equal balance states. **State.** Store the earliest index for each balance because the earliest occurrence creates the longest later span. **False friend.** Frequency counts answer how many spans; earliest indices answer the longest span.

- **Build - LC 525 Contiguous Array.** Treat `0` as `-1`; equal balances enclose equal counts.
- **Vary - Author exercise: Equal A And B.** Add `+1` for `A`, `-1` for `B`, and `0` for irrelevant values.
- **Boundary - Author exercise: Prefix From Zero.** Seed balance zero at index `-1` so a valid span can start at index zero.
- **Recognize - LC 1371 Find the Longest Substring Containing Vowels in Even Counts.** The repeated state is a parity mask rather than one integer balance.

### Group Prefixes By Remainder

**Recognition cue.** Divisibility of a range depends on two prefixes having the same normalized remainder. **State.** Store counts or earliest indices by `Math.floorMod(prefix, k)`. **Java hazard.** Java `%` may be negative.

- **Build - LC 974 Subarray Sums Divisible by K.** Count equal normalized remainder pairs.
- **Vary - LC 523 Continuous Subarray Sum.** Store earliest remainder indices and enforce length at least two.
- **Boundary - Author exercise: Negative Values.** Normalize negative prefix remainders with `Math.floorMod`.
- **Recognize - Author exercise: Longest Divisible Span.** Switch map meaning from count to earliest index.

### Use XOR As A Running Total

**Recognition cue.** A range XOR can be recovered because `x ^ x = 0`. **State.** `prefixXor[i]` summarizes values before `i`, so a range is the XOR of two prefix states.

- **Build - LC 1310 XOR Queries of a Subarray.** Answer immutable range XOR queries.
- **Vary - Author exercise: Count XOR K.** Use a frequency map and look up `prefixXor ^ k`.
- **Boundary - Author exercise: Empty Prefix.** Seed XOR zero for ranges starting at index zero.
- **Recognize - LC 1442 Count Triplets That Can Form Two Arrays of Equal XOR.** Repeated prefix XOR states identify zero-XOR ranges.

### Add To Ranges In Constant Time

**Recognition cue.** Many range additions are applied, and only the final materialized array is needed. **State.** A delta starts at `left` and is canceled immediately after `right`; one prefix reconstruction applies all updates. **False friend.** Prefix sums preprocess queries; difference arrays batch updates.

- **Build - Author exercise: One Range Add.** Add `value` to `[left,right]` using two delta writes.
- **Vary - LC 1109 Corporate Flight Bookings.** Accumulate many inclusive bookings.
- **Boundary - Author exercise: Final Endpoint.** Use a sentinel slot or guard `right + 1` when the update reaches the final index.
- **Recognize - LC 1094 Car Pooling.** Treat passenger changes as ordered coordinate deltas under the bounded-coordinate contract.

### Sum A Rectangle In Constant Time

**Recognition cue.** Many immutable rectangle-sum queries target a matrix. **State.** `prefix[r+1][c+1]` stores the rectangle from the origin through `(r,c)`; inclusion-exclusion removes two outside strips and restores their overlap.

- **Build - LC 304 Range Sum Query 2D - Immutable.** Precompute a sentinel-bordered prefix matrix.
- **Vary - LC 1314 Matrix Block Sum.** Query a clipped rectangle around every cell.
- **Boundary - Author exercise: Single Cell Rectangle.** Verify inclusion-exclusion returns exactly one cell.
- **Recognize - Author exercise: Whole Matrix Query.** Confirm sentinel coordinates avoid negative indices.

### Add To Rectangles In Constant Time

**Recognition cue.** Many rectangle additions precede one final matrix materialization. **State.** Four signed corner updates encode each rectangle; two-dimensional prefix reconstruction spreads their effects. **False friend.** A 2D prefix-query table reads fixed values; it does not batch writes.

- **Build - Author exercise: One Rectangle Add.** Apply four corner deltas to an interior rectangle.
- **Vary - LC 2536 Increment Submatrices by One.** Batch all rectangle increments before reconstruction.
- **Boundary - Author exercise: Bottom-Right Edge.** Allocate a sentinel border or explicitly guard `r2+1` and `c2+1`.
- **Recognize - Author exercise: Weighted Rectangle Updates.** Generalize increment-by-one to signed `long` weights.

## Released Combination Lessons

### Count And Measure Spans With Maps

Prefix state turns every earlier position into a meaningful key; the map supplies either frequency or earliest-index memory. A map alone does not explain what its keys mean.

- **Build - LC 560 Subarray Sum Equals K.** Given an integer array `nums` and integer `k`, return the number of contiguous subarrays whose sum equals `k`. Store how many earlier boundaries have each raw prefix sum.
- **Vary - LC 525 Contiguous Array.** Given a binary array, return the maximum length of a contiguous subarray containing the same number of zeroes and ones. Transform zero into `-1` and preserve the earliest index of each balance.
- **Boundary - LC 974 Subarray Sums Divisible by K.** Count the non-empty contiguous subarrays whose sum is divisible by `k`. Normalize negative prefix remainders with `Math.floorMod` before using them as keys.
- **Recognize - LC 523 Continuous Subarray Sum.** Determine whether a length-at-least-two contiguous subarray has a sum divisible by `k`. Store the earliest index for each remainder so the length contract can be checked.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `long` prefix state where totals can exceed `int`.
- Reserve and explain any sentinel slot used by a difference array.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Prefix State + Hash Map | Prefix counts / earliest index / remainder state; staircase: LC 560 → LC 525 → LC 974 → LC 523 |
| Deferred | Prefix + Sliding Window | Chapter 09 supplies moving-boundary comparison |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **2D difference arrays:** add rectangular range updates as a separate micro-pattern. A rectangle update writes four signed corner deltas; a two-dimensional prefix reconstruction materializes final cells. Allocate a sentinel border or guard the `r2 + 1` and `c2 + 1` writes explicitly.
- **Keep it separate from 2D prefix queries:** one preprocesses point values for range queries; the other batches range updates before materialization.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** sliding window, segment tree/Fenwick tree.

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

