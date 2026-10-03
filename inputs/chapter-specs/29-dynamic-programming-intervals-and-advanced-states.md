# Chapter 29: Dynamic programming: intervals and advanced states

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| matrix-chain-style interval state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| palindrome table/partition state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| tree DP and rerooting | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| bitmask assignment/grid-profile DP | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| submask/SOS aggregation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| digit DP (tight/started state) | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| problem-specific optimizations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0136 | Interval DP | Burst Balloons | Advanced application | Chooses the last operation inside an interval. |

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| DP + Interval/Advanced State | LC 516 Longest Palindromic Subsequence | LC 132 Palindrome Partitioning II | LC 312 Burst Balloons | LC 698 Partition to K Equal Sum Subsets |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Interval DP

**Recognition cue.** The answer for a contiguous interval depends on choosing a split or final operation inside it. **Invariant.** `dp[left][right]` owns exactly that interval and reads only shorter completed intervals.

- **Build - Author exercise: Best Split Of A Short Interval.** Combine left and right subinterval values around each split.
- **Vary - Author exercise: Matrix Chain Cost.** Minimize multiplication cost across split positions.
- **Boundary - Author exercise: Empty And Singleton Intervals.** Define neutral base values explicitly.
- **Recognize - LC 312 Burst Balloons.** Choose the last balloon removed inside each interval.

### Palindrome Partitions

**Recognition cue.** Partition cost depends on whether each substring is a palindrome. **Invariant.** A precomputed palindrome table answers validity while a prefix DP minimizes cuts.

- **Build - Author exercise: Palindrome Table.** Fill equal endpoints after the inner interval is known.
- **Vary - Author exercise: Minimum Valid Prefix Pieces.** Transition from every earlier cut whose suffix is valid.
- **Boundary - Author exercise: Empty Prefix And Whole Palindrome.** Avoid an off-by-one extra cut.
- **Recognize - LC 132 Palindrome Partitioning II.** Combine substring validity with minimum partition cuts.

### Tree DP

**Recognition cue.** Each subtree returns several values because the parent decision changes what children may do. **Invariant.** Returned state summarizes the subtree completely for every parent-relevant mode.

- **Build - Author exercise: Take Or Skip Node.** Return two values from each subtree.
- **Vary - LC 337 House Robber III.** Taking a node forces both children into skip states.
- **Boundary - Author exercise: Null And Negative Values.** Define neutral returns and the empty-choice contract.
- **Recognize - Author exercise: Rerooted Distance Sums.** Use one subtree pass and one parent-contribution pass.

### Bitmask Assignment

**Recognition cue.** A small set of used items must be part of the state. **Invariant.** Bit `i` records whether item `i` is already assigned; popcount often determines the next position. This lesson includes the needed mask primer because Chapter 30 is numbered later.

- **Build - Author exercise: Set Test And Clear Bits.** Represent a small used set in one integer.
- **Vary - Author exercise: Minimum Assignment Cost.** Add one unused item to the mask.
- **Boundary - Author exercise: Full Mask And State Count.** Stop at `(1 << n) - 1` and budget `2^n` memory.
- **Recognize - LC 698 Partition to K Equal Sum Subsets.** Use a mask and current-bucket state for small input.

### Submask Aggregation

**Recognition cue.** A transition or query ranges over every subset of a mask. **Invariant.** `(sub - 1) & mask` enumerates each nonempty submask exactly once.

- **Build - Author exercise: Enumerate Submasks.** List all nonempty subsets of one mask.
- **Vary - Author exercise: Partition A Mask.** Combine `dp[sub]` with `dp[mask ^ sub]`.
- **Boundary - Author exercise: Include Empty Submask Deliberately.** Prevent an infinite unsigned-style loop.
- **Recognize - Author exercise: SOS Subset Sums.** Aggregate values from every submask using bit dimensions.

### Digit DP

**Recognition cue.** Count numbers up to a bound under digit constraints without enumerating every number. **Invariant.** State includes position, whether the prefix is tight to the bound, and whether a nonleading digit has started the number.

- **Build - Author exercise: Count Fixed-Length Digit Strings.** Start without tightness.
- **Vary - Author exercise: Add Tight State.** Restrict the next digit by the bound prefix.
- **Boundary - Author exercise: Leading Zero And Number Zero.** Define when the constructed number has started.
- **Recognize - LC 902 Numbers At Most N Given Digit Set.** Count valid numbers under a decimal upper bound.

### Optimization Proofs

**Recognition cue.** A correct DP is too slow or large, and structure may reduce transitions or memory. **Invariant.** The optimization must preserve every dependency and candidate needed by the original recurrence.

- **Build - Author exercise: Roll One Dimension.** Prove only the previous layer is read.
- **Vary - Author exercise: Prefix-Minimum Transition.** Replace a repeated range scan with a maintained aggregate.
- **Boundary - Author exercise: In-Place Direction Counterexample.** Show how wrong order changes reuse semantics.
- **Recognize - Author exercise: Optimization Audit.** State original recurrence, dependency set, replacement structure, and resulting complexity.

## Released Combination Lessons

### DP With Advanced State

The DP recurrence supplies value reuse; interval, tree, digit, or mask encoding defines which subproblem is being reused.

- **Build - LC 516 Longest Palindromic Subsequence.** Use interval state with endpoint choices.
- **Vary - LC 132 Palindrome Partitioning II.** Combine a validity table with prefix optimization.
- **Boundary - LC 312 Burst Balloons.** Choose the last interval operation and handle virtual boundaries.
- **Recognize - LC 698 Partition to K Equal Sum Subsets.** Encode used elements with a mask and prevent symmetric bucket work.

### Deferred: Specialized Optimization

Knuth, divide-and-conquer, and convex-hull optimizations require recurrence-specific proofs and remain outside the active core.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Budget memory before materializing high-dimensional DP tables.
- Use an explicit encoding for bitmask or digit-DP state and document its bounds.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | DP + Interval/Advanced State | Subproblems are intervals or encoded masks; separate ladders by state representation |
| Deferred | Advanced optimization | Only release with a proof and a focused ownership decision |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** advanced optimizations.

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

