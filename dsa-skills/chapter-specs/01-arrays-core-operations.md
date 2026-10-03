# Chapter 01: Arrays: Core operations

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| direct scans and result contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| aggregation | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| stable write-index compaction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sorted in-place deduplication | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| bounded-domain frequency arrays | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| cyclic placement | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| in-place sign marking | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Kadane maximum/minimum state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| maximum-product max/min state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| circular-subarray reasoning after ordinary Kadane | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0001 | Array traversal and running state | Running Sum of 1d Array | Direct concept | Establish single-pass state maintenance. |
| P0009 | In-place array manipulation | Move Zeroes | Direct concept | Introduces stable in-place compaction. |
| P0010 | In-place array manipulation | Remove Duplicates from Sorted Array | Immediate application | Same write-pointer idea with sorted-input information. |
| Bundle 1-1 | Kadane | Maximum Subarray | Learn | — |
| Bundle 1-2 | Kadane | Best Time to Buy and Sell Stock | Extend | — |
| Bundle 1-3 | Kadane | Maximum Sum Circular Subarray | Twist | — |
| Bundle 1-1 | Index Placement | Missing Number | Learn | — |
| Bundle 1-2 | Index Placement | Find All Numbers Disappeared in an Array | Extend | — |
| Bundle 1-3 | Index Placement | Find All Duplicates in an Array | Twist | — |
| Bundle 1-1 | In-place Partition | Move Zeroes | Learn | — |
| Bundle 1-2 | In-place Partition | Sort Array By Parity | Extend | — |
| Bundle 1-3 | In-place Partition | Sort Colors | Twist | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Fast/slow write | Need remove/compact in-place | Only accepted elements need final placement | https://leetcode.com/problems/remove-element/ | Core |
| Mark/check by value-derived index | Value range maps directly to array indices | The array itself supplies O(1) auxiliary storage | https://leetcode.com/problems/find-all-duplicates-in-an-array/ | Core |
| Best ending here | Need maximum contiguous contribution | Any optimal subarray ending at i either starts at i or extends the best ending at i-1 | https://leetcode.com/problems/maximum-subarray/ | Core |
| Wrap = total - minimum | Need circular maximum contiguous contribution | A wrapping subarray excludes one contiguous middle segment | https://leetcode.com/problems/maximum-sum-circular-subarray/ | Intermediate |


### Released Combination Ladders

No combination is released by this chapter's current prerequisite boundary. The visible deferred entries below remain ownership notes, not premature exercises.


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

The following records replace a flat array problem list. Each is a separate lesson in the eventual PDF; a later problem must not silently borrow a different array pattern.

### Direct Scans

**Recognition cue.** The input is unsorted, every element may matter, and the answer is determined by inspecting one element at a time. **State.** The loop index marks the next unexamined position; the answer records the result required by the contract. **False friend.** Do not sort just to make search look easier: sorting changes index semantics and costs more than one scan.

- **Build — Author exercise: First Match.** Given an integer array `nums` and integer `target`, return the first index containing `target`, or `-1` when it does not occur. `[7, 4, 7], 7 → 0`; `[], 3 → -1`. Hint: ask what reaching the end proves.
- **Vary — Author exercise: Last Match.** Keep scanning after a match and return the last matching index. `[7, 4, 7], 7 → 2`; `[1], 9 → -1`. The changed decision is whether a match permits early return.
- **Boundary — Author exercise: Target Absent.** Given an unsorted array and a target that may not occur, return `-1` after a complete scan. `[3,2,2,3], 5 → -1`; `[], 3 → -1`.
- **Recognize — LC 1920 Build Array from Permutation.** Given a valid permutation `nums`, return `ans[i] = nums[nums[i]]`. The direct indexed-read contract, not a search, selects the method.

### Aggregation

**Recognition cue.** The answer can be summarized by a fixed-size value after each element. **Invariant.** Before processing `nums[i]`, the accumulator describes exactly `nums[0..i-1]`. **False friend.** Pair or subarray relationships need more than one scalar summary.

- **Build — Author exercise: Maximum.** Given a non-empty array, return its largest value. `[-3, 8, 1] → 8`; `[-5] → -5`. Initialize from the input, not zero.
- **Vary — LC 1295 Find Numbers with Even Number of Digits.** The state changes from an extremum to a count; `[12,345,2,6,7896] → 2`; `[] → 0`.
- **Boundary — LC 485 Max Consecutive Ones.** Reset the current run at zero while preserving the best completed run. `[1,1,0,1] → 2`; `[0,0] → 0`.
- **Recognize — LC 1491 Average Salary Excluding the Minimum and Maximum Salary.** One pass keeps the sum, the minimum and the maximum together; three scalars summarize everything the final formula needs.

### Running Extremum And Best Gain

**Recognition cue.** The answer is the best difference between two positions where the earlier one must come first, and the chosen positions need not be adjacent. **State.** `lowestSoFar` is the smallest value among positions already read; `bestGain` is the largest `value - lowestSoFar` seen at any position. **Invariant.** Before reading `nums[i]`, `lowestSoFar` is the minimum of `nums[0..i-1]`. **False friend.** Kadane's algorithm chooses one contiguous block, which this scan does not; the best gain pairs two positions and ignores everything between them. Added by the coverage audit addendum; LC 121 moved here from Aggregation.

- **Build — LC 121 Best Time to Buy and Sell Stock.** `[7,1,5,3,6,4] → 5`; `[7,6,4,3,1] → 0`.
- **Vary — Author exercise: Largest Drop.** Return the largest `earlier - later` over pairs where the earlier value comes first. The changed decision is that the running extremum becomes a maximum.
- **Boundary — Author exercise: No Profitable Pair.** For strictly decreasing prices the contract answer is `0`, not a negative number and not `-1`. State the contract before writing the initial value.
- **Recognize — LC 122 Best Time to Buy and Sell Stock II.** Multiple transactions are now allowed; state the transaction contract first. The state changes from a running minimum to day-to-day differences, so this is a false friend of the lesson's own pattern.

### Stable Compaction

**Recognition cue.** Keep selected values in original order while reusing the input array. **Invariant.** `nums[0..write-1]` contains exactly the accepted values already read, in order. **Java contract.** Return `write`; never claim the suffix was removed.

- **Build — LC 27 Remove Element.** Filter a value with one read index and one write index.
- **Vary — LC 283 Move Zeroes.** Keep non-zero values stable, then fill the remaining suffix with zeroes. `[0,1,0,3,12] → [1,3,12,0,0]`; `[0] → [0]`.
- **Boundary — Author exercise: Keep Evens.** Given `nums`, overwrite its prefix with its even values and return `k`. `[-2,3,4] → [-2,4], k=2`; `[1,3] → k=0`.
- **Recognize — Author exercise: Filter Positives.** Given `nums`, overwrite its prefix with positive values in their original order and return `k`. The test changes, but the read/write invariant does not.

### Sorted Deduplication

**Recognition cue.** Equal values occur in adjacent runs because the input is sorted. **Invariant.** The written prefix contains one representative of every completed value run. **False friend.** This is not general duplicate removal from unsorted data; sorting or a set would be a different prerequisite.

- **Build — LC 26 Remove Duplicates from Sorted Array.** `[1,1,2] → k=2, [1,2]`; `[] → k=0`.
- **Vary — LC 80 Remove Duplicates from Sorted Array II.** Permit two representatives, so the admission check reads `nums[write-2]`.
- **Boundary — Author exercise: Keep One Per Run.** Verify all-equal `[5,5,5] → k=1` and already-unique `[1,2,3] → k=3`.
- **Recognize — LC 443 String Compression.** The representation changes to `char[]`, but each completed run still owns one write decision.

### Frequency Arrays

**Recognition cue.** Values lie in a small, explicitly stated integer domain. **State.** `count[v]` is the number of processed occurrences of `v`. **False friend.** Do not allocate an array indexed by arbitrary IDs; Chapter 04 owns general hash maps.

- **Build — Author exercise: Digit Counts.** Given digits `0..9`, return ten counts. `[2,0,2] → [1,0,2,0,0,0,0,0,0,0]`; `[] → ten zeroes`.
- **Vary — LC 1365 How Many Numbers Are Smaller Than the Current Number.** Turn counts into accumulated smaller-value totals.
- **Boundary — Author exercise: Dice Validation.** Reject a value outside `1..6` before indexing; test `[1,6,0]`.
- **Recognize — LC 1051 Height Checker.** A compact known range makes counting sort preferable to comparison sorting.

### Majority Vote

**Recognition cue.** One value may occur more than half the time, and constant extra space is requested. **State.** `candidate` and `votes`; a different value cancels one vote, and the same value adds one. **Invariant.** After reading a prefix, every value other than `candidate` that was cancelled was cancelled against a distinct occurrence, so a true majority of the whole array cannot be eliminated. **Verification requirement.** The survivor is only a candidate unless the contract guarantees a majority; a second counting pass confirms it. **False friend.** It is not a frequency map and not ordinary counting. Added by the coverage audit addendum (Boyer-Moore majority vote).

- **Build — LC 169 Majority Element.** `[2,2,1,1,2] → 2`; `[3] → 3`. A majority is guaranteed.
- **Vary — Author exercise: Verify The Candidate.** No majority is guaranteed. Run the vote, then count the survivor in a second pass and return it only when it occurs more than `n/2` times, otherwise `-1`.
- **Boundary — Author exercise: No Majority.** `[1,2,3]` leaves a survivor that is not a majority; show why verification is mandatory. Also trace `[1,2]`, where the votes cancel to zero.
- **Recognize — Author exercise: Dominant Product Id.** A stream of order lines each carry a product id; decide whether any single id accounts for more than half the lines, using O(1) extra space.
- **Extend — LC 229 Majority Element II.** Elements occurring more than `n/3` times: two candidates and two vote counters, with a mandatory verification pass.

### Cyclic Placement

**Recognition cue.** Each positive value has one intended slot, and mutation is allowed. **Invariant.** A value `v` belonging to `1..n` is either already at `v-1` or is swapped toward that slot. **False friend.** Sign marking records visits but does not put values into their final locations.

- **Build — Author exercise: Place 1..n.** Reorder a permutation of `1..n` so that `v` occupies index `v-1`.
- **Vary — LC 268 Missing Number.** Use the `0..n` placement/range contract and identify the unmatched index.
- **Boundary — Author exercise: Duplicate Slot.** Stop swapping when `nums[i] == nums[nums[i] - 1]`; this avoids an infinite duplicate cycle.
- **Recognize — LC 41 First Missing Positive.** Ignore values outside `1..n`; cyclic placement makes the first misplaced positive identify the answer.

### In-Place Sign Marking

**Recognition cue.** Values are in `1..n`, the input may be mutated, and the question asks which values have appeared rather than where every value belongs. **Invariant.** The sign of slot `v-1` records whether value `v` has been observed; use `abs(nums[i])` because a previously visited slot may already be negative. **False friend.** Cyclic placement uses swaps to restore locations; sign marking only records membership.

- **Build — LC 448 Find All Numbers Disappeared in an Array.** Mark `abs(value)-1` negative and collect still-positive slots.
- **Vary — LC 442 Find All Duplicates in an Array.** If the target slot is already negative, the value is a duplicate; otherwise mark it.
- **Boundary — Author exercise: Re-read a Marked Value.** Explain why indexing with a negative value is invalid and why `Math.abs` is required.
- **Recognize — LC 645 Set Mismatch.** Use sign marking to identify the repeated value, then find the position that remains positive to recover the missing value.

### Kadane State

**Recognition cue.** The objective is the best contiguous sum with no fixed length. **State.** `bestEndingHere` is the best sum of a subarray forced to end at the current position; `bestOverall` is the best seen anywhere. This recurrence is **Kadane's algorithm**. **False friend.** Running minimum plus stock gain chooses two positions, not one contiguous subarray.

- **Build — LC 53 Maximum Subarray.** `[-2,1,-3,4,-1,2,1,-5,4] → 6`; `[-3] → -3`.
- **Vary — Author exercise: Minimum Subarray Sum.** Replace the maximum recurrence with the minimum recurrence; all-positive input must still return its smallest element.
- **Boundary — Author exercise: All Negative.** Return the largest value, not zero, for `[-8,-3,-6] → -3`; this protects the non-empty subarray contract.
- **Recognize — LC 1749 Maximum Absolute Sum of Any Subarray.** Track both maximum and minimum ending states because either can produce the largest magnitude.

### Product State

**Recognition cue.** The objective is a contiguous product and negative values can reverse the useful order. **State.** Keep both the maximum and minimum product ending at the current index; a negative swaps their roles. **False friend.** Sum Kadane needs one ending state because addition does not reverse order.

- **Build — LC 152 Maximum Product Subarray.** `[2,3,-2,4] → 6`; `[-2,0,-1] → 0`.
- **Vary — Author exercise: Product Ending Here.** Return the best product forced to include the final item; this removes `bestOverall` but retains max/min state.
- **Boundary — LC 152 zero-and-negative trace.** Dry-run `[-2,3,-4] → 24` and `[0,-2] → 0`.
- **Recognize — LC 1567 Maximum Length of Subarray With Positive Product.** The representation changes from products to sign/length state, but a negative still swaps the favorable and unfavorable histories.

### Circular Kadane

**Recognition cue.** A contiguous answer may wrap from the final index back to the first. **Invariant.** A wrapping maximum equals `totalSum - minimumOrdinarySubarray`; compare it with ordinary Kadane and forbid the empty remainder. **False friend.** A fixed-length circular window has a different state.

- **Build — LC 918 Maximum Sum Circular Subarray.** `[1,-2,3,-2] → 3`; `[5,-3,5] → 10`.
- **Vary — Author exercise: Circular Minimum.** Compute the smallest non-empty circular subarray using the symmetric maximum-exclusion argument.
- **Boundary — Author exercise: All Negative.** `[-3,-2,-3] → -2`; explain why the wrap candidate is invalid.
- **Recognize — LC 918 with a proof prompt.** State why every wrapping choice excludes exactly one ordinary contiguous middle segment.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `long` for sums or products when constraints can exceed `int`.
- State which in-place prefix is meaningful after compaction.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Deferred | Arrays + Hash Maps | Chapter 04 supplies key-to-state lookup |
| Deferred | Arrays + Two Pointers | Chapter 08 supplies two-boundary movement |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** opposite-end/three-way partition pointers, prefix sums, binary search, sorting.

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

