# Chapter 08: Two pointers

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| opposite-end sorted-pair scans | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| same-direction read/write scans | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| partitioning | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| Dutch-national-flag three-way partition | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| duplicate skipping | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| 3Sum/k-sum foundations | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| index-as-storage plus Floyd fast/slow cycle detection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0013 | Two pointers from both ends | Valid Palindrome | Direct concept | Simple symmetric two-end elimination. |
| P0014 | Two pointers on sorted array | Two Sum II - Input Array Is Sorted | Immediate application | Uses ordering to decide which pointer moves. |
| P0015 | Two pointers on sorted array | 3Sum | Small extension | Fixes one value and reuses the two-pointer invariant. |
| P0016 | Two pointers on sorted array | 4Sum | Immediate application | Extends the same reduction to one additional fixed dimension. |
| P0017 | Opposing pointers / optimization | Container With Most Water | New variation | Uses a proof-like pointer movement rather than target matching. |
| Bundle 1-1 | Sorted + Two Pointers | Two Sum II - Input Array Is Sorted | Learn | — |
| Bundle 1-2 | Sorted + Two Pointers | 3Sum | Extend | — |
| Bundle 1-3 | Sorted + Two Pointers | Container With Most Water | Twist | — |
| Bundle 1-1 | Opposite Direction | Valid Palindrome | Learn | — |
| Bundle 1-2 | Opposite Direction | Two Sum II - Input Array Is Sorted | Extend | — |
| Bundle 1-3 | Opposite Direction | Container With Most Water | Twist | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Maintain regions | Need divide array into regions around a pivot/category | Every processed element is placed into a final region | https://leetcode.com/problems/sort-colors/ | Core |
| Eliminate one side | Sorted data + pair target | Sortedness proves the discarded side cannot contain a better matching pair | https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/ | Core |
| Skip equal values after consuming one candidate | Need all unique k-sum combinations | Equal choices produce identical result branches | https://leetcode.com/problems/3sum/ | Core |
| Move the side whose information is resolved | Need compare both ends | Every movement permanently eliminates candidates | https://leetcode.com/problems/container-with-most-water/ | Core |
| Consume smaller current head | Need merge two sorted sequences | The smaller head cannot be beaten by later values in its own sorted sequence | https://leetcode.com/problems/merge-sorted-array/ | Core |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Sorting + Two Pointers | LC 167 Two Sum II | LC 15 3Sum | LC 16 3Sum Closest | LC 18 4Sum |
| Strings + Two Pointers | LC 125 Valid Palindrome | LC 344 Reverse String | LC 680 Valid Palindrome II | LC 392 Is Subsequence |
| Index-as-Storage + Fast/Slow Pointers | Author drill: follow value-as-next-index links | LC 287 Find the Duplicate Number | LC 287 all-same-cycle boundary trace | LC 287 explain phase-two entry proof |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Opposite Ends

**Recognition cue.** Ordered input lets one comparison eliminate every pair using one endpoint. **Invariant.** Any valid pair not yet ruled out lies between `left` and `right`. **False friend.** Without order or another monotone property, moving an endpoint is a guess.

- **Build - LC 167 Two Sum II.** Move left when the sum is too small and right when it is too large.
- **Vary - Author exercise: Closest Pair Sum.** Preserve the best distance while the same elimination rule shrinks the interval.
- **Boundary - Author exercise: Two Values.** Trace one comparison with equal values and an absent target.
- **Recognize - LC 11 Container With Most Water.** Move the shorter wall because moving the taller wall cannot improve the limiting height.

### Read And Write

**Recognition cue.** One pointer reads unresolved input while another marks the next output position or retained boundary. **Invariant.** The written prefix already satisfies the final contract. **False friend.** A sliding window’s left boundary removes state from a range; a write pointer constructs output.

- **Build - LC 27 Remove Element.** Revisit stable compaction as explicit read/write pointer movement.
- **Vary - LC 283 Move Zeroes.** Write stable nonzero values, then repair the suffix.
- **Boundary - LC 26 Remove Duplicates from Sorted Array.** Handle empty input and one-element runs.
- **Recognize - LC 80 Remove Duplicates from Sorted Array II.** The read pointer advances normally; the admission rule consults the kept prefix.

### Two-Way Partition

**Recognition cue.** Output needs two regions and relative order is not required. **Invariant.** Values before the boundary satisfy one category; unresolved values remain outside final regions. **False friend.** Stable compaction preserves order and may perform more writes.

- **Build - LC 905 Sort Array By Parity.** Swap misplaced values from opposite regions.
- **Vary - Author exercise: Partition Around Pivot.** Place values `< pivot` before values `>= pivot` without promising internal order.
- **Boundary - Author exercise: One Empty Region.** Test all-even and all-odd arrays.
- **Recognize - LC 922 Sort Array By Parity II.** Pointer positions encode even and odd destination classes.

### Three-Way Partition

**Recognition cue.** Values belong to low, middle, or high regions. **Invariant.** `[0,low)` is low, `[low,mid)` is middle, `[mid,high]` unresolved, and `(high,n)` high. This is the Dutch national flag partition.

- **Build - Author exercise: Partition 0,1,2.** Implement the four-region invariant on a short array.
- **Vary - LC 75 Sort Colors.** Apply the same category meanings to the formal problem.
- **Boundary - Author exercise: Reinspect Swapped High.** After swapping with `high`, do not advance `mid`; the incoming value is unresolved.
- **Recognize - Author exercise: Three-Way Pivot Partition.** Replace colors with `< pivot`, `== pivot`, and `> pivot`.

### Duplicate Skipping

**Recognition cue.** Sorted candidates can produce the same value combination repeatedly. **Invariant.** Skip equal choices only after one representative branch or pair has been fully processed. **False friend.** Skipping before evaluating the first representative can discard a valid answer.

- **Build - Author exercise: Unique Pairs.** Return distinct sorted pairs summing to a target.
- **Vary - LC 15 3Sum.** Skip repeated fixed values and repeated left/right values after recording a triplet.
- **Boundary - Author exercise: All Equal.** `[0,0,0,0]` produces exactly one triplet.
- **Recognize - LC 18 4Sum.** Duplicate policy applies at every fixed recursion/loop depth and at the final pair scan.

### K-Sum Reduction

**Recognition cue.** The array can be sorted, several leading values can be fixed, and the remaining two-value target is monotone. **State.** Each fixed choice reduces both `k` and the remaining target. **Java hazard.** Use `long` for sums when several integers can overflow.

- **Build - LC 15 3Sum.** Fix one value and solve a two-sum target on the suffix.
- **Vary - LC 16 3Sum Closest.** Preserve the closest total instead of collecting exact unique triples.
- **Boundary - Author exercise: Overflowing Sum.** Evaluate extreme integer inputs using `long` arithmetic.
- **Recognize - LC 18 4Sum.** Fix two values, then reuse the pair invariant and duplicate policy.

### Array Cycle State

**Recognition cue.** Every array value is a legal next index, producing a functional graph, and the contract implies a cycle whose entry represents the duplicate. **Invariant.** Floyd’s fast/slow phase finds a meeting inside the cycle; resetting one pointer and moving both one step finds the entry. **False friend.** Sign marking and cyclic placement mutate the array; this method follows links without modification.

- **Build - Author exercise: Follow Links.** Starting at index zero, repeatedly move to `nums[index]` under a proven in-range contract.
- **Vary - LC 287 Find the Duplicate Number.** Interpret values as next indices and return the cycle entry.
- **Boundary - Author exercise: Immediate Cycle.** Trace the smallest legal input and prove every dereference remains in range.
- **Recognize - LC 287 Proof Exercise.** Explain why phase two’s equal-speed pointers meet at the entry, not merely somewhere in the cycle.

## Released Combination Lessons

### Sorting And Two Pointers

Sorting creates the monotone sum relation; pointer movement exploits it. Sorting alone still scans too many pairs, while pointers on unsorted data have no safe movement proof.

- **Build - LC 167 Two Sum II.** Sorted pair elimination.
- **Vary - LC 15 3Sum.** Fix one value and reuse pair search.
- **Boundary - LC 16 3Sum Closest.** Preserve a best candidate when no exact target exists.
- **Recognize - LC 18 4Sum.** Add another fixed dimension with `long` sums and duplicate control.

### Strings And Two Pointers

String normalization/indexing supplies comparable characters; pointers supply symmetric or same-direction movement.

- **Build - LC 125 Valid Palindrome.** Skip non-alphanumeric characters and compare normalized endpoints.
- **Vary - LC 344 Reverse String.** Swap endpoints in a mutable `char[]`.
- **Boundary - LC 680 Valid Palindrome II.** At the first mismatch, test exactly one skipped endpoint.
- **Recognize - LC 392 Is Subsequence.** Both pointers now move left-to-right at different rates; this is not palindrome movement.

### Index State And Floyd

The array’s bounded values create next links; Floyd’s algorithm supplies cycle entry detection. Neither prerequisite alone explains LC 287.

- **Build - Author exercise: Value-As-Next-Index.** Validate the representation and trace one path.
- **Vary - LC 287 Find the Duplicate Number.** Run meeting and entry phases.
- **Boundary - Author exercise: Duplicate Near Start.** Trace a short tail and cycle without mutating the array.
- **Recognize - Author exercise: Compare Alternatives.** Explain when cyclic placement or sign marking would violate the no-mutation contract.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Document whether input mutation through sorting or partitioning is allowed.
- Explain duplicate-skipping order before moving either pointer.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Sorting + Two Pointers | Ordered sum search and duplicate policy; staircase: pair sum → 3Sum → 3Sum Closest |
| Teach now | Strings + Two Pointers | Opposite-end validation; representative: LC 125 Valid Palindrome |
| Teach now | Index-as-Storage + Fast/Slow Pointers | LC 287 after the array-value-as-next-index contract is restated |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Array-valued Floyd cycle detection:** add the released composition `index-as-storage + fast/slow pointers` for LC 287. Teach the required value domain first: each value names the next index. Phase one proves entry into a cycle; phase two resets one pointer to the start and advances both one step to find the entry/duplicate.
- **Do not mix with linked-list cycle mechanics:** the pointer motion is shared, but array-value-to-index representation and its bounds contract are Chapter 01 prerequisites.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** sliding window, greedy, linked-list pointer techniques.

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

