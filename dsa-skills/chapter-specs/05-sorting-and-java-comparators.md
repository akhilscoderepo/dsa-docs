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

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0037 | Sorting as preprocessing | Sort an Array | Direct concept | Establishes sorting as a deliberate preprocessing step and complexity tradeoff. |
| P0038 | Sorting + scanning | Merge Intervals | Immediate application | Sort order makes overlap detection sequential. |
| P0039 | Sorting + scanning | Insert Interval | Small extension | Uses ordered intervals to limit where merging is necessary. |
| P0040 | Custom comparator | Largest Number | New variation | Shows that the desired order may require a nonstandard comparator. |
| P0041 | Frequency / bucket ordering | Sort Characters By Frequency | New variation | Combines frequency counting with ordering. |
| P0042 | Sorting + greedy | Non-overlapping Intervals | New variation | Uses sort order to support an optimal interval choice. |
| P0043 | Cyclic / index placement | First Missing Positive | Combination | Uses in-place indexing rather than comparison sorting. |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Order by decisive coordinate | Need local interval relationships | Sorting converts global relationships into local comparisons | https://leetcode.com/problems/merge-intervals/ | Core |
| Quickselect or bounded heap | Need kth without full ordering | Everything beyond kth boundary is irrelevant | https://leetcode.com/problems/kth-largest-element-in-an-array/ | Intermediate |
| Count cross-half inversions | Need count inversions / quantify out-of-order pairs | Both halves are sorted, so all remaining left elements are greater than right[j] | https://leetcode.com/problems/count-of-smaller-numbers-after-self/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Strings + Maps + Sorting | LC 242 Valid Anagram (sort-key baseline) | LC 49 Group Anagrams | LC 451 Sort Characters By Frequency | LC 1657 Determine if Two Strings Are Close |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

Sorting is not the answer by itself. It is a transformation that makes a later local decision valid; every lesson names the order and the decision it unlocks.

### Compare Two Values Safely

**Recognition cue.** A problem asks for a deterministic order before any scan can make a local decision. **Java hazard.** Use `Integer.compare(a, b)` or `Long.compare(a, b)`; subtraction can overflow. **False friend.** Sorting primitive values cannot preserve custom-object tie behavior by accident.

- **Build - LC 912 Sort an Array.** Sort integers; state the required output order.
- **Vary - Author exercise: Sort Boxed Integers in Descending Order.** Sort an `Integer[]` with a safe reverse comparator, and explain why the same comparator overload does not accept `int[]`.
- **Boundary - Author exercise: Extreme Comparator.** Order `Integer.MIN_VALUE`, `0`, and `Integer.MAX_VALUE` without subtraction.
- **Recognize - LC 179 Largest Number.** The decisive comparator is concatenation order, not numeric order.

### Sort A Primitive Array

**Recognition cue.** Primitive values need a complete natural ordering and mutation of the input is permitted. **Invariant.** After `Arrays.sort(nums)`, every adjacent pair is nondecreasing and equal values form contiguous runs. **False friend.** `Arrays.sort(int[])` cannot accept a custom comparator.

- **Build - Author exercise: Sort A Primitive Copy.** Preserve the caller's array by copying before sorting.
- **Vary - Author exercise: Sort A Subrange.** State the inclusive/exclusive bounds used by the Java API.
- **Boundary - Author exercise: Empty, Singleton, And Extreme Values.** Verify natural ordering without comparator subtraction.
- **Recognize - LC 217 Contains Duplicate.** Sort, then detect equal adjacent values.

### Write A Valid Comparator

**Recognition cue.** Objects or boxed values require an order different from their natural order. **Invariant.** The comparator is antisymmetric, transitive, and returns zero only when elements are interchangeable for the required ordering.

- **Build - Author exercise: Safe Integer Comparator.** Use `Integer.compare` instead of subtraction.
- **Vary - Author exercise: Chained Keys.** Compare a primary field, then a deterministic secondary field.
- **Boundary - Author exercise: Equal Keys And Extreme Values.** Test comparator consistency and overflow safety.
- **Recognize - LC 179 Largest Number.** Order strings by `b+a` versus `a+b` to maximize concatenation.

### Sort Objects By Several Fields

**Recognition cue.** The thing being ordered has several fields and a stated priority. **State.** The comparator encodes the contract, including tie ownership. **Java hazard.** `Comparator` applies to objects such as `int[][]`, not `int[]` elements directly.

- **Build - Author exercise: Sort Scores.** Sort `Student(name, score)` by score, then name.
- **Vary - LC 937 Reorder Data in Log Files.** Compare identifier only after content ties.
- **Boundary - Author exercise: Equal Primary Keys.** State the secondary tie rule rather than relying on current order.
- **Recognize - LC 406 Queue Reconstruction by Height.** The first sort key makes insertion-by-position meaningful.

### Keep Equal Items In Order

**Recognition cue.** Equal primary keys must retain or explicitly replace original order. **State.** The tie rule is part of correctness, not a cosmetic comparator detail. **Java hazard.** `Arrays.sort(Object[])` is stable; do not rely on primitive-array stability.

- **Build - Author exercise: Stable Score Sort.** Preserve arrival order for equal scores.
- **Vary - Author exercise: Explicit Index Tie.** Attach original index and sort by it when the API cannot promise the required stability.
- **Boundary - Author exercise: Comparator Equality.** Verify comparator returns zero only for interchangeable output positions.
- **Recognize - LC 1356 Sort Integers by The Number of 1 Bits.** The numeric tie rule must be explicit.

### Sweep A Sorted Array

**Recognition cue.** After sorting, only neighboring or frontier items can affect the next decision. **State.** A sweep summary owns everything still relevant from earlier items. **False friend.** Intervals add endpoint semantics and receive their full chapter later.

- **Build - LC 977 Squares of a Sorted Array.** Sorting supplies order, though Chapter 08 later gives the optimal two-pointer version.
- **Vary - LC 406 Queue Reconstruction by Height.** Process a sorted order and preserve the partial output invariant.
- **Boundary - Author exercise: A Long Run of Equal Values.** After sorting, compute the increments needed to make every value unique; use `long` for the accumulated cost and test a large duplicate run.
- **Recognize - LC 945 Minimum Increment to Make Array Unique.** After sorting, raise each value to at least one more than the previous finalized value.

### Remove Duplicates After Sorting

**Recognition cue.** Equal values become adjacent after sorting, and output needs one representative or a count per run. **State.** The current run is the only unresolved duplicate group. **False friend.** Sorted in-place deduplication from Arrays assumes the input was already sorted.

- **Build - LC 217 Contains Duplicate.** Sort a copy, then compare neighbors.
- **Vary - LC 349 Intersection of Two Arrays.** Emit each common run once.
- **Boundary - Author exercise: All Equal.** Verify one emitted representative from `[4,4,4]`.
- **Recognize - LC 720 Longest Word in Dictionary.** A sorted word order can make deterministic tie choice explicit.

### Scan The Sorted Array

**Recognition cue.** Sorting exposes a simple adjacent relation but does not itself compute the answer. **State.** A scan retains the best local candidate under the new order. **False friend.** Binary search needs a monotone query contract, not merely sorted input.

- **Build - LC 414 Third Maximum Number.** Sort then select under duplicate rules.
- **Vary - LC 506 Relative Ranks.** Preserve original positions while scanning sorted values.
- **Boundary - Author exercise: Fewer Than k Distinct Values.** Return the stated fallback rather than indexing past the deduplicated run count.
- **Recognize - LC 268 Missing Number.** Sort the values, then return the first index whose value differs from the expected value; return `n` if every earlier position matches.

## Released Combination Lessons

### Group Strings By Sorted Letters

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

