# Chapter 13: Deques and monotonic queues

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| `ArrayDeque` | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| front/back invariants | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| dominated-back eviction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| expired-front eviction | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sliding maximum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sliding minimum | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| index expiry | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| shortest-subarray deque state | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Back=domination; front=expiration | Maximum/minimum over fixed moving window | Only non-dominated, in-window candidates can become the answer | https://leetcode.com/problems/sliding-window-maximum/ | Core |
| Expire + dominate | DP depends on best prior state in last K positions | Any worse state in same legal range is permanently dominated | https://leetcode.com/problems/jump-game-vi/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Deque + Sliding Window | LC 239 Sliding Window Maximum | LC 1438 Longest Continuous Subarray With Absolute Difference | LC 862 Shortest Subarray with Sum at Least K | LC 239 equal-value expiry boundary trace |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Use ArrayDeque From Both Ends

**Recognition cue.** The algorithm must inspect or remove candidates at both ends in constant time. **Invariant.** The front and back have fixed roles throughout the method. **False friend.** `LinkedList` can implement a deque, but `ArrayDeque` is the ordinary Java choice when null elements and indexed access are unnecessary. **Java hazard.** `ArrayDeque` rejects `null`.

- **Build - Author exercise: Two-Ended Buffer.** Add and remove integers at both ends using explicit `First` and `Last` methods.
- **Vary - Author exercise: Bounded Recent History.** Append at the back and evict the oldest front item once capacity is exceeded.
- **Boundary - Author exercise: Empty Deque Contract.** Choose deliberately between exception-throwing and sentinel-returning access methods.
- **Recognize - Author exercise: Candidate Deque API.** Identify the operations needed for front expiry and back domination without writing the algorithm yet.

### Give Each End One Job

**Recognition cue.** One end answers the current query while the other end admits a new candidate and removes weaker ones. **Invariant.** The front is the best surviving candidate; order toward the back follows the stated monotonic rule. **False friend.** Treating both ends as interchangeable destroys the proof.

- **Build - Author exercise: Decreasing Candidate Values.** Maintain a deque whose values decrease from front to back.
- **Vary - Author exercise: Increasing Candidate Values.** Reverse the comparison to support minima.
- **Boundary - Author exercise: Equal Candidate Policy.** Decide whether the newer equal value replaces the older one and explain how indices affect expiry.
- **Recognize - Author exercise: Name Each End.** Given a moving-range trace, identify whether each removal is expiration or domination.

### Remove Weaker Values From The Back

**Recognition cue.** A newly arrived value is at least as good as older candidates and will remain eligible longer. **Invariant.** Every stored index can still become the optimum of a future window; anything popped from the back cannot. **False friend.** Removing a smaller value is unsafe when the query asks for a minimum.

- **Build - Author exercise: Insert Maximum Candidate.** Pop smaller back values before appending a new index.
- **Vary - Author exercise: Insert Minimum Candidate.** Pop larger values for a monotonic increasing deque.
- **Boundary - Author exercise: Repeated Equal Values.** Compare keeping all equals with keeping only the newest and preserve a consistent expiry rule.
- **Recognize - Author exercise: Online Suffix Maximum Candidates.** Return the front after every insertion when no expiry is required.

### Remove Old Indices From The Front

**Recognition cue.** Candidate indices may be optimal by value but no longer lie in the active range. **Invariant.** Before reading the answer for a window ending at `right`, every stored index is greater than `right - k`. **False friend.** Value ordering cannot reveal whether a candidate is stale.

- **Build - Author exercise: Expire One Window.** Remove a front index when it falls left of a supplied boundary.
- **Vary - Author exercise: Jumping Boundary.** Use a loop because one boundary change may expire several stored indices.
- **Boundary - Author exercise: Exact Expiry Point.** For length `k`, verify that index `right - k` is outside the new window.
- **Recognize - Author exercise: Chronological Candidate Queue.** Preserve increasing indices while values remain monotonic.

### Find The Maximum Of Every Window

**Recognition cue.** Every fixed-size contiguous window needs its maximum in linear total time. **Invariant.** The deque contains in-window indices in chronological order and decreasing value order; its front is the current maximum. **False friend.** A heap can work but needs lazy stale-entry removal and costs `O(n log k)`.

- **Build - Author exercise: Maximum Of One Moving Window.** Perform expiry, domination, append, then read the front.
- **Vary - Author exercise: Return Maximum Indices.** Expose why the deque stores positions rather than values alone.
- **Boundary - Author exercise: Increasing, Decreasing, And Equal Arrays.** Trace the three shapes that stress opposite ends of the deque.
- **Recognize - LC 239 Sliding Window Maximum.** Produce all maxima in `O(n)` time and `O(k)` space.

### Find The Minimum Of Every Window

**Recognition cue.** Every fixed-size range needs its minimum and the same chronological expiry rule applies. **Invariant.** Values increase from front to back, so the front is the minimum among surviving indices. **False friend.** Copying maximum-window code without reversing every domination comparison silently returns maxima.

- **Build - Author exercise: Minimum Of Every K-Window.** Reverse the value comparison used by the maximum deque.
- **Vary - Author exercise: Window Range.** Maintain a maximum deque and minimum deque, then return `max - min` for each fixed window.
- **Boundary - Author exercise: Duplicate Minima Expire.** Ensure a later equal minimum survives after the earlier index leaves.
- **Recognize - LC 1438 Longest Continuous Subarray With Absolute Difference Less Than or Equal to Limit.** Use both deques while a variable window restores its range constraint.

### Allow Only Recent Positions

**Recognition cue.** Eligibility depends on age, distance, or an index interval as well as candidate quality. **Invariant.** Indices are appended in increasing order and the front is removed as soon as it crosses the legal left boundary. **False friend.** Storing only values loses identity when duplicates expire at different times.

- **Build - Author exercise: Best Of Last K Scores.** Maintain the maximum score among indices `[i-k, i-1]`.
- **Vary - Author exercise: Variable Legal Left Bound.** Expire against a supplied boundary array rather than constant `k`.
- **Boundary - Author exercise: Duplicate Values, Different Ages.** Prove expiry removes the correct occurrence.
- **Recognize - LC 1696 Jump Game VI.** Combine recent-index eligibility with the best previous dynamic-programming score.

### Find The Shortest Subarray With Negatives

**Recognition cue.** Negative values prevent an ordinary sum window, but prefix sums let the task ask for the shortest pair of indices whose difference is at least `k`. **Invariant.** Prefix-sum indices increase from front to back and their prefix values also strictly increase; the front supplies the earliest profitable start. **False friend.** A standard positive-number sliding window fails when extending can decrease the sum.

- **Build - Author exercise: Prefix-Pair Difference.** Given prefix sums, compute a subarray sum as `prefix[right] - prefix[left]`.
- **Vary - Author exercise: Remove Dominated Prefixes.** Discard a later-or-equal prefix value because the newer index is never a better start.
- **Boundary - Author exercise: Negative Values And Long Sums.** Use `long` prefix sums and trace a case where the window sum falls after expansion.
- **Recognize - LC 862 Shortest Subarray with Sum at Least K.** Pop valid starts from the front and dominated prefixes from the back.

## Released Combination Lessons

### Slide A Window With Two Deques

The sliding window supplies changing eligibility boundaries; the monotonic deque keeps only candidates that could still answer an extreme-value query. The combined state must enforce chronology, expiry, and value order.

- **Build - Author exercise: Fixed-Window Maximum Trace.** Separate front expiry from back domination on a short array.
- **Vary - LC 239 Sliding Window Maximum.** Produce every fixed-window maximum in linear time.
- **Boundary - LC 1438 Longest Continuous Subarray With Absolute Difference Less Than or Equal to Limit.** Coordinate maximum and minimum deques while `left` may move repeatedly.
- **Recognize - LC 862 Shortest Subarray with Sum at Least K.** Recognize prefix indices as the moving candidates even though the original array contains negatives.

### Deferred: Deque And Graph BFS

Zero-one BFS uses a deque to prioritize zero-cost transitions ahead of one-cost transitions. Graph state and shortest-path correctness are not available yet; Chapters 21 and 24 own that composition.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use `ArrayDeque` and state which end owns insertion and removal.
- Expire indices before using a front value outside the current window.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Deque + Sliding Window | Index expiry and monotone value state; staircase: fixed max → LC 239 → LC 862 |
| Deferred | Deque + Graph BFS | Chapter 21/24 owns graph state and 0-1 BFS |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Bidirectional deque maintenance:** make the two jobs explicit: pop stale indices from the front before reading an answer, and pop dominated values from the back before appending the new index. The deque stores indices so chronology and values can both be checked.
- **Expiry contract:** for a size-`k` window ending at `right`, an index `<= right - k` is expired. Test repeated equal values and a jump beyond one expired index.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** graph BFS and dynamic-programming optimizations beyond the introductory recent-state example.

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

