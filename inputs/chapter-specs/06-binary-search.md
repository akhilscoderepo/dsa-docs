# Chapter 06: Binary search

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| exact search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| first/last occurrence | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| lower/upper bounds | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| first-true predicate search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| peak/mountain search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| rotated minimum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| rotated-array target search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| integer answer-space feasibility search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| continuous answer-space feasibility search | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0023 | Exact search | Binary Search | Direct concept | Learn the basic sorted-search invariant. |
| P0024 | Exact search | Search Insert Position | Immediate application | Turns exact search into finding an insertion boundary. |
| P0025 | Boundaries | Find First and Last Position of Element in Sorted Array | Small extension | Continue after finding a match to locate both boundaries. |
| P0026 | Boundaries | Find Smallest Letter Greater Than Target | Immediate application | Reuses boundary search with a wraparound condition. |
| P0027 | Rotated sorted arrays | Search in Rotated Sorted Array | New concept | Identify which half remains sorted. |
| P0028 | Rotated sorted arrays | Find Minimum in Rotated Sorted Array | Immediate application | Uses the same ordering observation to find the rotation point. |
| P0029 | Rotated sorted arrays | Search in Rotated Sorted Array II | Small variation | Handles duplicates that weaken the sorted-half decision. |
| P0030 | Peaks and boundaries | Find Peak Element | New variation | Uses a local ordering relationship to discard half the search space. |
| P0031 | Binary search over possible answer | Koko Eating Bananas | New concept | Searches numerical answers using a monotonic feasibility test. |
| P0032 | Binary search over possible answer | Capacity To Ship Packages Within D Days | Immediate application | Adds greedy allocation to the feasibility check. |
| P0033 | Binary search over possible answer | Minimum Number of Days to Make m Bouquets | Small extension | Uses a different monotonic feasibility function. |
| P0034 | Binary search over possible answer | Split Array Largest Sum | Combination | Combines answer-space search with a harder partitioning argument. |
| P0035 | Matrix search | Search a 2D Matrix | New variation | Treats ordered matrix positions as one search space. |
| P0036 | Advanced recognition | Find K-th Smallest Pair Distance | Recognition | Binary searches a value space while counting feasible pairs. |
| Bundle 1-1 | Rotated Binary Search | Search in Rotated Sorted Array | Learn | — |
| Bundle 1-2 | Rotated Binary Search | Find Minimum in Rotated Sorted Array | Extend | — |
| Bundle 1-3 | Rotated Binary Search | Search in Rotated Sorted Array II | Twist | — |
| Bundle 1-1 | Basic | Binary Search | Learn | — |
| Bundle 1-2 | Boundary | Search Insert Position | Extend | — |
| Bundle 1-3 | Boundary | Find First and Last Position of Element in Sorted Array | Twist | — |
| Bundle 1-1 | Answer Space | Koko Eating Bananas | Learn | — |
| Bundle 1-2 | Answer Space | Capacity To Ship Packages Within D Days | Extend | — |
| Bundle 1-3 | Answer Space | Split Array Largest Sum | Twist | — |
| Bundle 2-3 | Answer Space | Koko Eating Bananas | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Discard half | Exact lookup in sorted data | Sortedness makes half impossible | https://leetcode.com/problems/binary-search/ | Core |
| Save answer, search left | First valid/first occurrence | You are locating the transition boundary | https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/ | Core |
| Save answer, search right | Last valid/last occurrence | You are locating the final feasible boundary | https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/ | Core |
| Optimization -> monotone feasibility | Need minimum/maximum answer and can test candidate | If x is feasible, all more permissive answers remain feasible (or reverse for maximum) | https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/ | Core |
| Identify ordered half | Rotated sorted array | At least one half retains sorted order | https://leetcode.com/problems/search-in-rotated-sorted-array/ | Core |
| Binary-search partition in smaller array | Two sorted arrays; need median/partition without merging | A valid partition has every left element <= every right element | https://leetcode.com/problems/median-of-two-sorted-arrays/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Hash Map + Binary Search | Author drill: binary-search timestamps for one key | LC 981 Time Based Key-Value Store | LC 1146 Snapshot Array | LC 911 Online Election |
| Matrix + Binary Search | LC 74 Search a 2D Matrix | Author exercise: return first matching coordinates | Author exercise: empty matrix shape | LC 240 Search a 2D Matrix II |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

All integer searches use an explicitly stated interval convention and the overflow-safe midpoint `lo + (hi - lo) / 2`.

### Exact Search

**Recognition cue.** The array is sorted and the question asks whether or where one exact target occurs. **Invariant.** If the target exists, it remains inside the current search interval. **False friend.** Unsorted input has no safe half to discard.

- **Build - LC 704 Binary Search.** Return the target index or `-1`. `[-1,0,3,5,9,12], 9 -> 4`; `[5], 2 -> -1`.
- **Vary - Author exercise: Descending Search.** Reverse the comparison-to-movement rule under a descending-order contract.
- **Boundary - Author exercise: Two Elements.** Trace `[1,3]` for targets `1`, `3`, and `2`; prove the interval shrinks after every comparison.
- **Recognize - LC 74 Search a 2D Matrix.** Treat a globally row-major sorted matrix as one virtual sorted array; the full combination lesson appears below.

### First And Last

**Recognition cue.** Duplicates exist and the output asks for an extreme occurrence. **Invariant.** A found target is a candidate, not permission to stop; continue toward the requested boundary.

- **Build - Author exercise: First Occurrence.** Return the smallest index equal to `target`.
- **Vary - Author exercise: Last Occurrence.** Preserve a candidate and continue right.
- **Boundary - LC 34 Find First and Last Position.** Return `[-1,-1]` when absent and handle all-equal arrays.
- **Recognize - LC 278 First Bad Version.** The first true position is the same boundary shape without explicit duplicates.

### Lower And Upper Bounds

**Recognition cue.** The output is an insertion boundary: first value `>= target` or first value `> target`. **Invariant.** One side is known to fail the predicate and the other contains the first possible success. **False friend.** Exact search may stop on equality; bounds may not.

- **Build - LC 35 Search Insert Position.** Find the first position whose value is at least `target`.
- **Vary - Author exercise: Upper Bound.** Find the first position whose value is strictly greater than `target`.
- **Boundary - Author exercise: Outside Range.** Test a target smaller than every value and larger than every value; insertion positions may be `0` or `n`.
- **Recognize - LC 744 Find Smallest Letter Greater Than Target.** Apply upper-bound logic plus the stated wraparound contract.

### First True

**Recognition cue.** A monotone predicate changes once from false to true. **Invariant.** `hi` remains a possible first true answer while discarded positions are proved false or cannot improve it. **False friend.** A non-monotone predicate cannot justify discarding half.

- **Build - Author exercise: First True Boolean.** Find the first `true` in `[false,false,true,true]`.
- **Vary - LC 278 First Bad Version.** Replace stored booleans with an oracle call.
- **Boundary - Author exercise: No True Value.** Define and return sentinel `n` when the contract permits all false.
- **Recognize - LC 1539 Kth Missing Positive Number.** The count of missing values by index is monotone and becomes a searchable predicate.

### Peak Search

**Recognition cue.** Local slope determines which side must contain a peak. **Invariant.** Comparing `nums[mid]` with `nums[mid+1]` preserves at least one peak in the remaining interval. **False friend.** This is not target search; equality and direction mean something different.

- **Build - LC 852 Peak Index in a Mountain Array.** Use the guaranteed rise-then-fall shape.
- **Vary - LC 162 Find Peak Element.** Preserve any peak without a unique mountain guarantee.
- **Boundary - Author exercise: Endpoint Peak.** Trace strictly increasing and strictly decreasing arrays.
- **Recognize - LC 1095 Find in Mountain Array.** Peak discovery precedes two ordered searches; API-call cost becomes part of the contract.

### Rotated Minimum

**Recognition cue.** A strictly increasing array was rotated and only the pivot/minimum is needed. **Invariant.** Comparison with the right endpoint identifies which side contains the discontinuity.

- **Build - LC 153 Find Minimum in Rotated Sorted Array.** `[3,4,5,1,2] -> 1`; `[1,2,3] -> 1`.
- **Vary - Author exercise: Rotation Count.** Return the minimum’s index.
- **Boundary - Author exercise: Two Values.** Trace `[2,1]` and `[1,2]`.
- **Recognize - LC 154 Find Minimum in Rotated Sorted Array II.** Duplicates can destroy the strict comparison; shrinking equality may degrade to linear time.

### Rotated Target

**Recognition cue.** A target must be found in a rotated array. **Invariant.** At least one half is normally sorted; determine it before asking whether the target belongs there. **False friend.** Finding the minimum alone does not finish target lookup.

- **Build - LC 33 Search in Rotated Sorted Array.** Identify the sorted half and discard only a half proved unable to contain the target.
- **Vary - Author exercise: Pivot Then Search.** Find the rotation index, then binary-search the appropriate sorted segment.
- **Boundary - LC 81 Search in Rotated Sorted Array II.** When left, mid, and right are equal, sorted-half identity is ambiguous.
- **Recognize - Author exercise: Explain Both Strategies.** Compare one-pass sorted-half search with pivot-plus-search; state complexity and proof obligations.

### Integer Answers

**Recognition cue.** The answer is an integer value in a numeric range, and feasibility is monotone. **Invariant.** Every discarded candidate is proved infeasible or no better than an already feasible boundary. **False friend.** Binary search applies to the ordered answer space, not because the input happens to be an array.

- **Build - LC 875 Koko Eating Bananas.** Search the minimum eating speed that finishes on time.
- **Vary - LC 1011 Capacity To Ship Packages Within D Days.** Change the feasibility simulation while retaining minimum-feasible search.
- **Boundary - LC 1482 Minimum Number of Days to Make m Bouquets.** Detect impossible total demand before searching.
- **Recognize - LC 410 Split Array Largest Sum.** Search a maximum allowed part sum and greedily count required partitions.

### Continuous Answers

**Recognition cue.** Feasibility is monotone over real values and the problem accepts bounded numeric error. **State.** Maintain a real interval containing the answer and a documented convergence policy. **Java hazard.** A fixed iteration count bounds work; an epsilon loop must still make progress under `double` precision.

- **Build - Author exercise: Square Root.** Approximate `sqrt(x)` within the stated absolute error.
- **Vary - Author exercise: Maximum Minimum Distance.** Search a real separation value under a monotone placement check.
- **Boundary - Author exercise: Scale-Aware Error.** Compare absolute and relative error for very small and very large answers.
- **Recognize - Author exercise: Fixed Iterations.** Explain why 80 bisections are a convergence policy, not a claim of universal maximal precision.

## Released Combination Lessons

### Time Indexed Lookup

**Contributions.** A `HashMap` selects the history for one key; an ordered timestamp list makes binary search valid. A map alone cannot choose the latest timestamp `<= queryTime` without scanning that history.

- **Build - Author exercise: One Key History.** Binary-search the latest timestamp not exceeding a query.
- **Vary - LC 981 Time Based Key-Value Store.** Add independent histories per string key.
- **Boundary - LC 981 Early Query.** Return the specified empty value when every timestamp is later than the query.
- **Recognize - LC 1146 Snapshot Array.** Each index owns an ordered history searched by snapshot ID.

### Matrix Search

**Contributions.** Matrix shape maps a virtual one-dimensional index to `(row, col)`; binary search discards ordered ranges.

- **Build - LC 74 Search a 2D Matrix.** Use `row = mid / cols`, `col = mid % cols` under global row-major ordering.
- **Vary - Author exercise: First Matrix Position.** Return coordinates instead of a boolean.
- **Boundary - Author exercise: Empty Shape.** Guard zero rows before computing `cols` or a final virtual index.
- **Recognize - LC 240 Search a 2D Matrix II.** Rows and columns are sorted independently; use staircase elimination, not virtual-array binary search.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `lo + (hi - lo) / 2` for an overflow-safe midpoint.
- Make the chosen interval convention and post-loop return contract explicit.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Hash Map + Binary Search | Timestamp lookup; representative: LC 981 Time Based Key-Value Store |
| Teach now | Matrix + Binary Search | Row-major index mapping supports LC 74; independently sorted rows/columns require staircase elimination in LC 240 |
| Deferred | Sorting + Binary Search | Sorting-specific search applications stay with later owner where needed |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Continuous binary search:** add an advanced answer-space variant for real-valued monotone predicates. State the numeric interval and desired absolute/relative error. A fixed iteration count is a bounded convergence policy; `hi - lo > epsilon` is valid only when epsilon has a meaningful scale and the interval still changes under `double` arithmetic.
- **Precision boundary:** do not promise that any fixed count gives maximal precision for every scale. Return an endpoint or midpoint according to the problem's error contract.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** two-pointers, heaps, dynamic programming.

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

