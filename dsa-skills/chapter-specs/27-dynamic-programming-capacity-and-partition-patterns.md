# Chapter 27: Dynamic programming: capacity and partition patterns

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| unbounded coin change | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| unbounded knapsack | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 0/1 knapsack | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| subset/partition state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| target sum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| order-irrelevant combination counts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| order-sensitive permutation counts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0127 | Subset / knapsack | Partition Equal Subset Sum | New subtopic | Reframes partitioning as a subset-sum state. |
| P0128 | Subset / knapsack | Target Sum | Immediate application | Transforms signed choices into a subset-counting formulation. |
| Bundle 1-1 | Knapsack | Partition Equal Subset Sum | Learn | — |
| Bundle 1-2 | Knapsack | Coin Change | Extend | — |
| Bundle 1-3 | Knapsack | Coin Change II | Twist | — |

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| DP + Capacity State | LC 322 Coin Change | LC 518 Coin Change II | LC 416 Partition Equal Subset Sum | LC 494 Target Sum |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Unbounded Coin Change

**Recognition cue.** Each positive denomination may be reused and the objective minimizes item count. **Invariant.** `dp[a]` is the minimum coins for amount `a`; increasing amounts permit reuse of the current coin.

- **Build - Author exercise: One Denomination.** Mark reachable multiples and impossible amounts.
- **Vary - LC 322 Coin Change.** Minimize across all last-coin choices.
- **Boundary - Author exercise: Amount Zero And Impossible Target.** Return zero or the specified failure value.
- **Recognize - Author exercise: Reconstruct One Minimum Set.** Store the chosen final coin with each improvement.

### Unbounded Knapsack

**Recognition cue.** Items have weight and value, capacity is limited, and an item may be reused. **Invariant.** Increasing capacity order allows the current item to contribute again.

- **Build - Author exercise: One Reusable Item.** Fill every feasible capacity multiple.
- **Vary - Author exercise: Maximum Value With Reuse.** Compare skipping with taking from a smaller current-row capacity.
- **Boundary - Author exercise: Zero Capacity.** Prevent zero-weight positive-value items unless the contract excludes them.
- **Recognize - LC 279 Perfect Squares.** Treat square numbers as reusable item weights minimizing count.

### Zero-One Knapsack

**Recognition cue.** Each item can be used at most once. **Invariant.** Descending one-dimensional capacity order ensures the current item is not read from a state it just created.

- **Build - Author exercise: One-Use Items.** Fill a two-dimensional item/capacity table.
- **Vary - Author exercise: Descending Compression.** Compress capacity without enabling reuse.
- **Boundary - Author exercise: Ascending-Loop Counterexample.** Show one item being counted twice.
- **Recognize - LC 416 Partition Equal Subset Sum.** Use each number once to reach half the total.

### Partition State

**Recognition cue.** Values must split into groups with equal or constrained sums. **Invariant.** Reachable sums summarize all one-use choices processed so far.

- **Build - Author exercise: Reachable Subset Sums.** Update Boolean capacity states descending.
- **Vary - LC 416 Partition Equal Subset Sum.** Reduce equal partition to target `total/2`.
- **Boundary - Author exercise: Odd Total And Large Target.** Reject parity immediately and budget memory by target.
- **Recognize - LC 1049 Last Stone Weight II.** Find the reachable sum closest to half.

### Target Sum

**Recognition cue.** Each nonnegative value receives `+` or `-`, and assignments must reach a target. **Invariant.** Algebra converts sign assignments to selecting a subset with derived sum `(total + target)/2` when parity and range permit it.

- **Build - Author exercise: Derive The Subset Equation.** Separate positive and negative groups.
- **Vary - Author exercise: Count Derived Subsets.** Count one-use subsets reaching the derived target.
- **Boundary - Author exercise: Zero Values And Parity.** Zero doubles assignment counts; invalid parity returns zero.
- **Recognize - LC 494 Target Sum.** Apply the reduction with counting DP.

### Combination Counts

**Recognition cue.** Reusable values form a sum and order does not distinguish results. **Invariant.** Iterate candidates outside and amounts inside so each multiset is formed in one canonical candidate order.

- **Build - Author exercise: Count With One Coin.** Initialize `dp[0] = 1`.
- **Vary - LC 518 Coin Change II.** Add ways coin by coin.
- **Boundary - Author exercise: Empty Combination.** Amount zero has one construction even with no selected coins.
- **Recognize - Author exercise: Explain Loop Order.** Show why swapping loops counts sequences instead.

### Permutation Counts

**Recognition cue.** Reusable values form a target and different orders count separately. **Invariant.** Iterate totals outside and candidates inside so each final choice extends all smaller ordered sequences.

- **Build - Author exercise: Ordered Sums To Four.** Enumerate sequences from values `1` and `2`.
- **Vary - LC 377 Combination Sum IV.** Count ordered constructions for every total.
- **Boundary - Author exercise: Overflow And Nonpositive Values.** State numeric bounds and exclude transitions that do not shrink the target.
- **Recognize - Author exercise: Compare With Coin Change II.** Same recurrence ingredients, different loop ownership and meaning.

## Released Combination Lessons

### DP And Capacity

DP supplies reusable state; capacity and loop direction decide whether an item is reusable, one-use, and whether order distinguishes solutions.

- **Build - LC 322 Coin Change.** Minimize reusable item count.
- **Vary - LC 518 Coin Change II.** Count order-independent reusable combinations.
- **Boundary - LC 416 Partition Equal Subset Sum.** Reverse capacity order for one-use items.
- **Recognize - LC 494 Target Sum.** Algebraically reduce signs to subset-count state.

### Deferred: State Machines

Temporal holding and transaction states arrive in Chapter 28.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- State loop direction because it controls whether an item is reusable.
- Use `long` if counts of combinations can exceed `int`.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | DP + Capacity State | Loop direction controls reuse; staircase: coin change → 0/1 knapsack → partition |
| Deferred | DP + State Machine | Chapter 28 supplies temporal state transitions |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** state-machine and interval DP.

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

