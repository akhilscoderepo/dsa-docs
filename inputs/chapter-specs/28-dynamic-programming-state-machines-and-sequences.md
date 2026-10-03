# Chapter 28: Dynamic programming: state machines and sequences

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| stock buy/sell states | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| cooldown/fee/transaction-count transitions | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| LIS O(n^2) and patience/binary-search O(n log n) | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| LCS | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| edit distance | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| palindromic sequence state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0131 | Sequence DP | Longest Increasing Subsequence | New subtopic | Tracks the best subsequence ending at each position. |
| P0132 | Sequence DP | Longest Common Subsequence | New variation | Uses two-prefix state and a match/mismatch transition. |
| P0134 | State machine | Best Time to Buy and Sell Stock with Cooldown | New subtopic | Models multiple states and transitions. |
| Bundle 1-1 | Subsequence | Longest Increasing Subsequence | Learn | — |
| Bundle 1-2 | Subsequence | Number of Longest Increasing Subsequence | Extend | — |
| Bundle 1-3 | Subsequence | Longest Common Subsequence | Twist | — |
| Bundle 2-2 | LIS | Longest Increasing Subsequence | Mixed | — |

### Pattern References

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| DP + State Machine | LC 121 Best Time to Buy and Sell Stock | LC 309 Best Time to Buy and Sell Stock with Cooldown | LC 714 Best Time to Buy and Sell Stock with Transaction Fee | LC 123 Best Time to Buy and Sell Stock III |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Stock States

**Recognition cue.** Each day ends in a small mode such as holding or not holding. **Invariant.** `hold` and `cash` are the best values after processing the current prefix under their exact ownership states.

- **Build - LC 121 Best Time to Buy and Sell Stock.** Track one buy followed by one sell.
- **Vary - LC 122 Best Time to Buy and Sell Stock II.** Transition between hold and cash repeatedly.
- **Boundary - Author exercise: One Day And Falling Prices.** Respect the no-transaction result.
- **Recognize - Author exercise: State Diagram.** Derive transitions before compressing them to scalars.

### Transaction Variants

**Recognition cue.** Cooldown, fee, or transaction count changes which transitions are legal. **Invariant.** Every state represents both possession and the restriction needed for the next action.

- **Build - LC 309 Best Time to Buy and Sell Stock with Cooldown.** Add a state that prevents immediate rebuy.
- **Vary - LC 714 Best Time to Buy and Sell Stock with Transaction Fee.** Charge the fee on exactly one transition.
- **Boundary - Author exercise: Update Aliasing.** Compute new states from old states, not partially overwritten values.
- **Recognize - LC 123 Best Time to Buy and Sell Stock III.** Add transaction-count state for at most two completed sales.

### Increasing Subsequences

**Recognition cue.** The answer is a longest strictly increasing subsequence, not necessarily contiguous. **Invariant.** Quadratic DP ends at each index; patience sorting keeps the smallest possible tail for every length.

- **Build - Author exercise: LIS Ending At I.** Extend from earlier smaller values.
- **Vary - LC 300 Longest Increasing Subsequence.** Compute the quadratic recurrence.
- **Boundary - Author exercise: Duplicates.** Use lower bound so equal values do not increase strict length.
- **Recognize - LC 300 O(n log n).** Maintain minimal tails with binary search and explain why tails are not the actual LIS.

### Common Subsequences

**Recognition cue.** Two sequences may skip characters while preserving relative order. **Invariant.** `dp[i][j]` is the best result for stated prefixes or suffixes; equal characters match, otherwise one side is skipped.

- **Build - Author exercise: LCS Of Short Prefixes.** Fill match and mismatch transitions.
- **Vary - LC 1143 Longest Common Subsequence.** Build the full table.
- **Boundary - Author exercise: Empty Prefix.** Initialize zero row and column.
- **Recognize - LC 583 Delete Operation for Two Strings.** Express deletions through LCS length.

### Edit Distance

**Recognition cue.** One string becomes another through insert, delete, and replace operations. **Invariant.** `dp[i][j]` is minimum edits between fixed prefixes; each operation moves to its corresponding smaller state.

- **Build - Author exercise: Insert Or Delete Only.** Model two operations first.
- **Vary - LC 72 Edit Distance.** Add replacement and matching-character transitions.
- **Boundary - Author exercise: Empty String.** Distance equals the other prefix length.
- **Recognize - Author exercise: Reconstruct Operations.** Backtrack a valid optimal edit script.

### Palindromic Sequences

**Recognition cue.** The state is a substring interval, but characters may be skipped. **Invariant.** `dp[left][right]` is the best palindromic subsequence within that closed interval.

- **Build - Author exercise: Length One And Two.** Establish interval base cases.
- **Vary - LC 516 Longest Palindromic Subsequence.** Match equal endpoints or skip one endpoint.
- **Boundary - Author exercise: Fill By Increasing Length.** Ensure inner intervals are ready first.
- **Recognize - LC 1312 Minimum Insertion Steps to Make a String Palindrome.** Relate insertions to the longest palindromic subsequence.

## Released Combination Lessons

### DP State Machines

DP stores prefix-optimal values; a state machine names the legal modes and transitions that prevent invalid action sequences.

- **Build - LC 121 Best Time to Buy and Sell Stock.** Establish cash and hold meaning.
- **Vary - LC 309 Best Time to Buy and Sell Stock with Cooldown.** Add temporal restriction state.
- **Boundary - LC 714 Best Time to Buy and Sell Stock with Transaction Fee.** Charge once and protect update order.
- **Recognize - LC 123 Best Time to Buy and Sell Stock III.** Add bounded transaction count.

### Deferred: Advanced States

Interval, tree, digit, and bitmask state spaces arrive in Chapter 29.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Name every state dimension and the meaning of a sentinel impossible state.
- Avoid accidental aliasing when rolling arrays or updating stock states.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | DP + State Machine | Hold/cash or sequence state captures legal transitions; staircase: stock → cooldown/fee → bounded transactions |
| Deferred | Interval and Bitmask DP | Chapter 29 supplies those state spaces |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** interval/partition DP and bitmask DP.

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

