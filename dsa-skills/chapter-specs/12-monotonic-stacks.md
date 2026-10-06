# Chapter 12: Monotonic stacks

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| next greater/smaller | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| circular next-greater | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| stock span | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| boundary discovery | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| duplicate-attribution policy | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| contribution counting | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| histogram rectangles | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| Bundle 1-1 | Monotonic Stack | Daily Temperatures | Learn | — |
| Bundle 1-2 | Monotonic Stack | Next Greater Element I | Extend | — |
| Bundle 1-3 | Monotonic Stack | Largest Rectangle in Histogram | Twist | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Use surviving top as nearest boundary | Nearest smaller/greater boundaries | Dominated candidates are farther/no better | https://leetcode.com/problems/online-stock-span/ | Core |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Stack + Contribution Counting | LC 496 Next Greater Element I | LC 739 Daily Temperatures | LC 84 Largest Rectangle in Histogram | LC 907 Sum of Subarray Minimums |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Find The Next Greater Value

**Recognition cue.** Each position needs the first later value that crosses a greater/smaller threshold. **Invariant.** The stack stores unresolved indices in monotonic value order; the current value resolves every top it dominates. **False friend.** A globally greater value is not necessarily the next greater value. **Java hazard.** Store indices when the answer is a distance or position.

- **Build - Author exercise: Next Greater Value.** Scan left to right and fill an answer whenever the current value exceeds the unresolved stack top.
- **Vary - LC 739 Daily Temperatures.** Store indices and return the distance to the resolving warmer day.
- **Boundary - Author exercise: Equal Values Stay Unresolved.** Use strict comparison so an equal value is not mistaken for a greater one.
- **Recognize - LC 496 Next Greater Element I.** Precompute next-greater values for the reference array and answer lookups for the subset.

### Find The Next Greater In A Circle

**Recognition cue.** Successors wrap from the end of the array to the beginning, but each answer still needs the first greater value in circular order. **Invariant.** A virtual scan of at most `2n` positions exposes every possible successor; indices are pushed only during the first pass so each position is represented once. **False friend.** Physically duplicating the array is unnecessary.

- **Build - Author exercise: Circular Successor Indices.** Enumerate `(i + 1) % n` order for one starting position.
- **Vary - Author exercise: Virtual Double Scan.** Read `nums[i % n]` across two passes without allocating a copy.
- **Boundary - Author exercise: All Equal Circular Array.** Leave every answer at `-1` and avoid resolving on equality.
- **Recognize - LC 503 Next Greater Element II.** Combine virtual traversal with the unresolved-index stack.

### Compute The Stock Span

**Recognition cue.** For each new value, count the consecutive suffix ending here whose earlier values do not exceed it. **Invariant.** The stack stores decreasing price candidates paired with the span each candidate already summarizes. **False friend.** This asks for the full dominated run, not merely the nearest greater value.

- **Build - Author exercise: Span From Previous-Greater Index.** Compute `i - previousGreaterIndex` for an offline array.
- **Vary - Author exercise: Compressed Price-Span Pairs.** Pop dominated pairs and add their stored spans.
- **Boundary - Author exercise: Equal Prices.** Pop equality because equal earlier days belong to the current `<= price` span.
- **Recognize - LC 901 Online Stock Span.** Maintain the compressed monotonic state across successive API calls.

### Find Both Boundaries Of A Value

**Recognition cue.** Each element's valid region ends at the nearest smaller or greater element on both sides. **Invariant.** One scan determines a nearest boundary when an index is popped; a reverse scan or surviving top supplies the other boundary under the chosen comparison. **False friend.** The boundary value alone is insufficient when width or number of choices depends on distance.

- **Build - Author exercise: Previous Smaller Index.** Store indices in increasing value order and report the surviving top.
- **Vary - Author exercise: Next Smaller Index.** Resolve indices when a smaller current value arrives.
- **Boundary - Author exercise: No Boundary.** Use sentinels `-1` and `n` consistently when no smaller element exists.
- **Recognize - Author exercise: Widest Region Where Each Value Is Minimum.** Combine left and right boundaries into width `right - left - 1`.

### Break Ties Between Equal Values

**Recognition cue.** Equal values could claim the same subarray when nearest boundaries are used for counting. **Invariant.** Make one side strict and the other non-strict so every subarray with tied minima has exactly one owner. **False friend.** Using strict comparisons on both sides can double-count; non-strict on both can leave gaps. The chosen asymmetric side is a convention, not a universal direction.

- **Build - Author exercise: Two Equal Minima Ownership.** List subarrays of `[2,2]` and assign each to exactly one index.
- **Vary - Author exercise: Strict Left, Non-Strict Right.** Compute boundaries and verify the ownership partition.
- **Boundary - Author exercise: All Equal Array.** Confirm the total number of owned subarrays is `n(n+1)/2`.
- **Recognize - LC 907 Sum of Subarray Minimums.** Explain the tie convention before translating distances into contributions.

### Count Subarrays By Their Minimum

**Recognition cue.** The result is a sum over all subarrays, but each element can be counted as the minimum or maximum for a number of boundary choices. **Invariant.** If index `i` owns subarrays between its selected left and right boundaries, its count is `(i - left) * (right - i)`. **False friend.** This multiplication is valid only after duplicate ownership is proved. **Java hazard.** Multiply with `long` before applying the modulus.

- **Build - Author exercise: Count Subarrays Owned By One Index.** Enumerate left-start and right-end choices from supplied boundaries.
- **Vary - Author exercise: Sum Owned Minimum Contributions.** Multiply each value by its number of owned subarrays.
- **Boundary - Author exercise: Negative And Repeated Values.** Separate arithmetic/modulus handling from the equality ownership proof.
- **Recognize - LC 907 Sum of Subarray Minimums.** Discover boundaries with a monotonic stack and accumulate each index's contribution.

### Find The Largest Rectangle

**Recognition cue.** Every bar may be the limiting height of a rectangle extending until the first smaller bar on either side. **Invariant.** Increasing stack indices await a right boundary; when a shorter bar arrives, the popped bar's right boundary is current and its left boundary is the new stack top. **False friend.** Next-smaller distance on only one side cannot determine rectangle width.

- **Build - Author exercise: Rectangle From Supplied Boundaries.** Compute `height * (right - left - 1)`.
- **Vary - Author exercise: Resolve On A Shorter Bar.** Pop bars and calculate widths during one left-to-right scan.
- **Boundary - Author exercise: Flush Increasing Heights.** Append a conceptual zero-height sentinel so every remaining bar is resolved.
- **Recognize - LC 84 Largest Rectangle in Histogram.** Maintain increasing indices and maximize each popped height's full width.

## Released Combination Lessons

### Count Subarrays From Stack Boundaries

An ordinary stack preserves unresolved positions. Monotonic ordering proves that dominated positions can be resolved, while boundary distances convert the result into widths or numbers of subarrays. Contribution counting additionally needs an explicit equality ownership rule.

- **Build - LC 496 Next Greater Element I.** Learn resolution on pop without counting regions.
- **Vary - LC 739 Daily Temperatures.** Convert the resolving index into a distance.
- **Boundary - LC 84 Largest Rectangle in Histogram.** Use both boundaries and flush unresolved bars at the end.
- **Recognize - LC 907 Sum of Subarray Minimums.** Count left/right choices with asymmetric duplicate handling.

### Deferred: Greedy And Monotonic Stack

Problems such as Remove K Digits pop a worse earlier choice because a limited-removal greedy proof shows that choice can never help. The ordered stack alone does not establish that exchange argument. Chapter 20 owns this composition and its exercises.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Store indices when equal-value boundary policy matters.
- Explain whether equality pops, remains, or requires an explicit tie rule.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Stack + Contribution Counting | Nearest boundaries determine an element's contribution; staircase: next greater → histogram → LC 907 |
| Deferred | Greedy + Monotonic Stack | Chapter 20 supplies greedy safety proof |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Duplicate attribution:** contribution-counting with equal values must choose one strict and one non-strict boundary so each subarray is owned exactly once. The side that accepts equality depends on the chosen convention; teach the proof rather than one universal `>`/`>=` recipe.
- **Practice boundary:** include all-equal arrays and verify that their contributions are neither dropped nor double-counted.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** greedy stack and DP stack variants.

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

