# Chapter 09: Sliding window

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| fixed-size aggregate windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| fixed-size frequency/permutation windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| longest-valid windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| minimum-cover/deficit windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| at-most-K distinct windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| exactly-K-by-subtraction windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| replacement-budget windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| count-all-valid-subarrays windows | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| repeated-shrink versus non-shrinking policy | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0018 | Fixed sliding window | Maximum Average Subarray I | Direct concept | Introduces a fixed-size contiguous window. |
| P0019 | Variable sliding window | Longest Substring Without Repeating Characters | Direct concept | Introduces expand/shrink windows with a maintained condition. |
| P0020 | Variable sliding window | Longest Repeating Character Replacement | Small extension | Maintains a frequency-based validity condition. |
| P0021 | Variable sliding window | Permutation in String | Small extension | Applies fixed-window frequency matching. |
| P0022 | Advanced variable window | Minimum Window Substring | Deeper variation | Maintains a richer validity condition while shrinking aggressively. |
| Bundle 1-1 | Variable | Minimum Size Subarray Sum | Learn | — |
| Bundle 1-2 | Variable | Max Consecutive Ones III | Extend | — |
| Bundle 1-3 | Variable | Subarray Product Less Than K | Twist | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Enter one/remove one | Contiguous range + exact fixed size | Adjacent windows differ by only entering/leaving elements | https://leetcode.com/problems/sliding-window-maximum/ | Core |
| Expand; shrink only when invalid | Need longest valid range | For each right, the smallest valid left yields the longest valid range | https://leetcode.com/problems/longest-substring-without-repeating-characters/ | Core |
| Expand until valid; shrink while valid | Need shortest valid range | Every unnecessary left element can be discarded while preserving validity | https://leetcode.com/problems/minimum-window-substring/ | Core |
| Maintain violation counter | At most K violations/distinct values | Window is valid exactly when the budget invariant holds | https://leetcode.com/problems/longest-repeating-character-replacement/ | Core |
| Count atMost(K)-atMost(K-1) | Exactly K distinct / exact property | Exact count is the difference between two monotone counts | https://leetcode.com/problems/subarrays-with-k-different-integers/ | Intermediate |
| Matched requirements | Find every permutation/anagram | Window validity can be updated locally | https://leetcode.com/problems/find-all-anagrams-in-a-string/ | Core |
| Dominated + expired candidates | Need max/min for every window | Dominated candidates can never become future extrema; expired candidates are outside the window | https://leetcode.com/problems/sliding-window-maximum/ | Intermediate |
| Add number of valid starts | Need count of all valid subarrays with monotone validity | Every start after the boundary is valid | https://leetcode.com/problems/subarrays-with-k-different-integers/ | Intermediate |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Sliding Window + Frequency State | LC 567 Permutation in String | LC 3 Longest Substring Without Repeating Characters | LC 424 Longest Repeating Character Replacement | LC 76 Minimum Window Substring |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Fixed-Size Aggregate Windows

**Recognition cue.** The problem asks for every contiguous block of exactly `k` elements and the block can be updated when one value leaves and one enters. **Invariant.** Before recording a result, the maintained aggregate equals the contents of `nums[left..right]`, whose length is `k`. **False friend.** A prefix sum is often better when many unrelated range queries follow; a window is natural for one left-to-right pass.

- **Build - Author exercise: Sums of Every K-Block.** Return the sum of each length-`k` subarray by adding the entering value and removing the leaving value.
- **Vary - LC 643 Maximum Average Subarray I.** Track the maximum fixed-window sum and divide only once at the end.
- **Boundary - Author exercise: Whole-Array Window.** Handle `k == nums.length` and state the contract for illegal `k` rather than silently inventing a result.
- **Recognize - LC 1456 Maximum Number of Vowels in a Substring of Given Length.** Replace numeric sum with a Boolean contribution per character.

### Fixed Frequency Windows

**Recognition cue.** Every candidate has a fixed length, but validity depends on its multiset rather than its aggregate. **Invariant.** The frequency state describes exactly the current length-`k` window. **False friend.** Sorting every window destroys linear time. **Java hazard.** A small count array is valid only when the character domain is stated.

- **Build - Author exercise: Binary Window Counts.** For every length-`k` block, report its number of ones.
- **Vary - LC 438 Find All Anagrams in a String.** Record every start whose counts match the pattern.
- **Boundary - Author exercise: Repeated Required Character.** Test a pattern such as `aab`; set membership cannot represent multiplicity.
- **Recognize - LC 567 Permutation in String.** Return whether any fixed window has the pattern's frequency signature.

### Longest-Valid Windows

**Recognition cue.** The answer is the longest contiguous range satisfying a condition that can be restored by moving `left` forward. **Invariant.** After the shrink loop, the current window is valid; every discarded start is known to be unusable for the current `right`. **False friend.** A minimum-cover problem shrinks while valid and records before validity is lost.

- **Build - Author exercise: Longest Binary Run With One Zero.** Maintain the number of zeroes and shrink while it exceeds one.
- **Vary - LC 3 Longest Substring Without Repeating Characters.** Maintain character multiplicities and remove from the left until the duplicate is gone.
- **Boundary - Author exercise: Violation At Both Ends.** Trace repeated violations and verify the loop may remove several elements for one `right`.
- **Recognize - LC 1004 Max Consecutive Ones III.** Treat zeroes as violations with a budget of `k`.

### Minimum-Cover And Deficit Windows

**Recognition cue.** The range must cover required values or counts, and the objective is the shortest valid range. **Invariant.** A deficit ledger says whether every requirement is met; while valid, removing the leftmost item tests whether the range can be improved. **False friend.** Equality with a fixed signature is not coverage: a cover may contain surplus characters.

- **Build - Author exercise: Shortest Segment Containing A And B.** Expand until both required symbols appear, then shrink surplus symbols.
- **Vary - Author exercise: Required Multiplicities.** Require two copies of one symbol and track fulfilled counts rather than distinct membership.
- **Boundary - Author exercise: No Cover Exists.** Return the specified empty result without constructing invalid substrings.
- **Recognize - LC 76 Minimum Window Substring.** Maintain deficits, remember the best boundaries, and create the substring once.

### At-Most-K Distinct Windows

**Recognition cue.** Validity is monotone under removing elements and is expressed as no more than `k` distinct values. **Invariant.** The map contains positive counts for exactly the values in the current window. **Java hazard.** Remove a key when its count reaches zero or `map.size()` stops representing distinct values.

- **Build - Author exercise: Longest Segment With One Distinct Value.** Maintain one active key and its count.
- **Vary - LC 904 Fruit Into Baskets.** Find the longest subarray containing at most two distinct values.
- **Boundary - Author exercise: K Is Zero.** Return zero without allowing a negative count or an invalid left boundary.
- **Recognize - Author exercise: Longest Substring With At Most K Distinct Characters.** Transfer the same invariant from integers to characters.

### Exactly-K By Subtraction

**Recognition cue.** The task counts subarrays with exactly `k` occurrences or categories, while an at-most condition is monotone and easy to count. **Invariant.** `exactly(k) = atMost(k) - atMost(k - 1)` partitions all subarrays by property count. **False friend.** A direct exactly-`k` window does not usually give one stable boundary because removing a redundant left value can preserve exactness.

- **Build - Author exercise: Exactly One Odd Number.** Compute `atMost(1) - atMost(0)`.
- **Vary - LC 1248 Count Number of Nice Subarrays.** Count subarrays containing exactly `k` odd values.
- **Boundary - Author exercise: Empty At-Most Budget.** Define `atMost(-1)` as zero so the subtraction remains safe.
- **Recognize - LC 992 Subarrays with K Different Integers.** Apply the identity to distinct-value counts maintained by a map.

### Replacement-Budget Windows

**Recognition cue.** A range can be made uniform by changing at most `k` values. **Invariant.** The required replacements are `windowLength - maxFrequency`; the window is usable when that value is at most `k`. **False friend.** Recomputing the maximum frequency on every move is unnecessary for the standard longest-length formulation.

- **Build - Author exercise: Replacement Cost Of One Window.** Given fixed boundaries, compute length minus its largest frequency.
- **Vary - Author exercise: Longest Binary Uniform Window.** Permit at most `k` flips and maintain the dominant count.
- **Boundary - Author exercise: Stale Maximum Trace.** Show why a historical `maxFrequency` may remain high without causing an impossible best length to be reported.
- **Recognize - LC 424 Longest Repeating Character Replacement.** Use the replacement budget to maintain the best achievable length.

### Count-All-Valid-Subarrays Windows

**Recognition cue.** The problem asks for the number of contiguous ranges and, once the left boundary is restored, every suffix ending at `right` is valid. **Invariant.** After shrinking, starts `left..right` produce exactly `right - left + 1` valid subarrays ending at `right`. **False friend.** This addition is invalid when validity is not monotone under removing a prefix. **Java hazard.** Use `long` when the number of subarrays can exceed `int`.

- **Build - Author exercise: Count Subarrays With At Most One Zero.** Add the number of valid starts for each right endpoint.
- **Vary - Author exercise: Count Subarrays With Sum Below K For Positive Values.** Use positivity to justify that removing from the left cannot increase the sum.
- **Boundary - Author exercise: K At The Minimum.** Verify that a window may shrink to empty and contributes zero.
- **Recognize - LC 713 Subarray Product Less Than K.** Maintain a positive-product window and count all valid suffixes.

### Repeated-Shrink Versus Non-Shrinking Policy

**Recognition cue.** A normal window must restore validity before its state is used; a one-removal formulation is safe only when a separate proof shows that retaining a window of the current best length cannot hide a better answer. **Invariant.** State explicitly whether the maintained window is valid or merely represents a candidate length. **False friend.** Replacing every `while` with `if` is not an optimization rule.

- **Build - Author exercise: Restore Before Record.** Implement a duplicate-free window with a `while` loop and assert validity before measuring it.
- **Vary - Author exercise: One-Removal Maximum-Length Trace.** Trace a proved non-shrinking replacement-budget formulation and identify what its window length represents.
- **Boundary - Author exercise: Multiple Left Removals Needed.** Use an input where one removal leaves the ordinary window invalid.
- **Recognize - LC 424 Longest Repeating Character Replacement.** Compare the always-valid and proved non-shrinking forms, including the invariant required by each.

## Released Combination Lessons

### Window Frequency State

Window boundaries identify the active contiguous range; frequency state records the multiset, deficits, or violations inside it. Neither component is sufficient by itself. The combined invariant must say both which indices are active and what every stored count means.

- **Build - LC 567 Permutation in String.** Maintain exact counts in a fixed-length window.
- **Vary - LC 3 Longest Substring Without Repeating Characters.** Let the length vary and shrink until all counts are at most one.
- **Boundary - LC 424 Longest Repeating Character Replacement.** Convert frequencies into a replacement budget and justify the maximum-frequency policy.
- **Recognize - LC 76 Minimum Window Substring.** Track required multiplicities, expand to validity, and shrink to a minimal cover.

### Deferred: Sliding Window And Deque

A deque can retain the best candidate for each moving window, but its ordered-candidate and index-expiry invariants have not been taught. Chapter 13 owns Sliding Window Maximum and related exercises; this chapter only names the future composition.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Avoid creating substrings in the moving-window loop; retain boundaries and construct output once.
- Use primitive count arrays only when the character-domain contract permits them.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Sliding Window + Frequency State | Moving boundaries plus counts/deficits; staircase: LC 567 → LC 3 → LC 76 |
| Deferred | Sliding Window + Deque | Chapter 13 supplies the monotone-deque and index-expiry invariant |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Shrink-policy classification:** distinguish a repeatedly shrinking window, which restores validity before continuing, from a non-shrinking maximum-length formulation, which advances `left` at most once per `right` under a separately proved monotonic condition. Do not present the one-removal form as a universal longest-window rule.
- **Practice split:** give the two policies separate recognition cues and staircases; minimum-cover and replacement-budget windows should not share one vague shrink explanation.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** prefix-sum alternatives, heap/window combinations.

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

