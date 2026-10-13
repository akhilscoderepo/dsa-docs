# Chapter 32: Selection and ordered-data techniques

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| quickselect | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| partition invariants | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| ordered maps/sets | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| merge-based counting | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

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
| Partition + Selection | LC 215 Kth Largest Element in an Array | LC 973 K Closest Points to Origin | LC 315 Count of Smaller Numbers After Self | LC 493 Reverse Pairs |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Quickselect

**Recognition cue.** Only one rank is needed, not a fully sorted array. **Invariant.** Partition places the pivot at its final rank and proves which side can contain the target.

- **Build - Author exercise: Select Kth Smallest.** Partition and recurse only toward the target rank.
- **Vary - LC 215 Kth Largest Element in an Array.** Convert kth-largest to a zero-based target index.
- **Boundary - Author exercise: Duplicates And Extreme K.** Preserve progress when many values equal the pivot.
- **Recognize - LC 973 K Closest Points to Origin.** Select by squared distance without sorting every point.

### Partition Invariants

**Recognition cue.** Values must be divided around a pivot in-place. **Invariant.** Each pointer delimits finalized less/equal/greater and unresolved regions.

- **Build - Author exercise: Lomuto Partition.** Maintain a prefix strictly below the pivot.
- **Vary - Author exercise: Three-Way Partition.** Group values below, equal, and above the pivot.
- **Boundary - Author exercise: All Equal Values.** Guarantee pointer progress and correct equal region.
- **Recognize - LC 215 Kth Largest Element in an Array.** Use pivot rank to discard one partition.

### Ordered Maps And Sets

**Recognition cue.** Queries need predecessor, successor, floor, ceiling, or ordered iteration under updates. **Invariant.** `TreeMap`/`TreeSet` comparator equality defines key identity and navigation order.

- **Build - Author exercise: Floor And Ceiling.** Query nearest keys around a target.
- **Vary - Author exercise: Ordered Frequency Map.** Update counts while preserving key order.
- **Boundary - Author exercise: Missing Neighbor And Comparator Equality.** Handle null results and consistent comparison.
- **Recognize - LC 729 My Calendar I.** Use neighboring starts to reject interval overlap.

### Merge Counting

**Recognition cue.** Count cross-pairs satisfying an order relation faster than all-pairs comparison. **Invariant.** Recursive halves are sorted; a monotone pointer counts an entire valid suffix or prefix at once before merge.

- **Build - Author exercise: Count Inversions.** Count left values greater than right values during merge.
- **Vary - LC 315 Count of Smaller Numbers After Self.** Preserve original indices while merging.
- **Boundary - Author exercise: Equal Values.** Match strict versus non-strict comparison to the contract.
- **Recognize - LC 493 Reverse Pairs.** Count `nums[i] > 2 * nums[j]` with `long` arithmetic before merging.

## Released Combination Lessons

### Partition And Selection

Partition supplies a final pivot rank; selection uses that proof to ignore one entire side instead of sorting it.

- **Build - LC 215 Kth Largest Element in an Array.** Select one rank by quickselect.
- **Vary - LC 973 K Closest Points to Origin.** Partition records by a derived key.
- **Boundary - LC 315 Count of Smaller Numbers After Self.** Contrast pivot selection with merge-based per-index counting.
- **Recognize - LC 493 Reverse Pairs.** Recognize when ordered cross-pair counting, not selection, is the required divide-and-conquer state.

### Deferred: Streaming Selection

Continuously updated order statistics require a stream contract and balanced-state design; heaps cover the common top-k form.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Define partition boundaries before swapping.
- Do not copy subarrays merely to pass recursion state; pass index bounds.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Partition + Selection | Partition places a pivot relative to a target rank; staircase: partition → quickselect → merge counting |
| Deferred | Streaming order statistics | Needs a stream/update contract |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** streaming and range-query compositions.

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

