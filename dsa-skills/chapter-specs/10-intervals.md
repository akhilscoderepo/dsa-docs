# Chapter 10: Intervals

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| endpoint ordering contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| touching-boundary semantics | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| merge/insert | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| two-list intersection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| overlap removal/coverage decisions | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| sweep events with explicit tie policy | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0145 | Basic overlap | Meeting Rooms | Direct concept | Sorts starts and detects overlap. |
| P0146 | Resource allocation | Meeting Rooms II | Combination | Uses interval ordering plus a min-heap of resource end times. |
| P0147 | Coverage | Remove Covered Intervals | New variation | Uses ordering to detect complete containment. |
| Bundle 1-1 | Merge | Merge Intervals | Learn | — |
| Bundle 1-2 | Insert | Insert Interval | Extend | — |
| Bundle 1-3 | Scheduling | Meeting Rooms II | Twist | — |
| Bundle 2-5 | Scheduling | Meeting Rooms II | Mixed | — |
| Bundle 2-6 | Selection | Non-overlapping Intervals | Mixed | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Extend active end | Need merge overlaps | After sorting, only current merged interval can overlap next | https://leetcode.com/problems/merge-intervals/ | Core |
| Before / overlap / after | Need insert into sorted disjoint intervals | Only overlapping region needs mutation | https://leetcode.com/problems/insert-interval/ | Core |
| Intersect then advance smaller end | Need intersection of two sorted interval lists | That interval cannot intersect anything after its end | https://leetcode.com/problems/interval-list-intersections/ | Intermediate |
| Starts +1, ends -1 | Need max simultaneous overlap | Active count is exactly number of simultaneous intervals | https://leetcode.com/problems/my-calendar-iii/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Sorting + Intervals | LC 56 Merge Intervals | LC 57 Insert Interval | LC 435 Non-overlapping Intervals | LC 452 Minimum Number of Arrows to Burst Balloons |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Endpoint Ordering Contracts

**Recognition cue.** Each record describes a range and the algorithm needs a reliable order before making local overlap decisions. **Invariant.** Intervals already processed precede every unresolved interval under the stated comparator. **False friend.** Sorting by end supports selection problems, but it does not replace sorting by start for ordinary merging. **Java hazard.** Use `Integer.compare(a[0], b[0])`, not subtraction that can overflow.

- **Build - Author exercise: Order By Start Then End.** Sort intervals lexicographically and explain the tie rule.
- **Vary - Author exercise: Order By End Then Start.** Change the comparator for a scheduling objective and state what decision it enables.
- **Boundary - Author exercise: Equal And Extreme Endpoints.** Test equal starts and integer extremes with safe comparisons.
- **Recognize - LC 56 Merge Intervals.** Choose start order because only the current merged interval can overlap the next one.

### Touching-Boundary Semantics

**Recognition cue.** Correctness changes when one interval ends exactly where another begins. **Invariant.** The overlap predicate follows the declared model: closed `[a,b]`, open, or half-open `[a,b)`. **False friend.** Memorizing `<=` or `<` without the contract produces plausible but inconsistent answers.

- **Build - Author exercise: Closed Interval Overlap.** Decide whether `[1,3]` and `[3,5]` overlap when both endpoints are included.
- **Vary - Author exercise: Half-Open Reservations.** Decide whether `[1,3)` and `[3,5)` require the same resource.
- **Boundary - Author exercise: Zero-Length Range.** State whether `[x,x]` is one point and whether `[x,x)` is empty.
- **Recognize - Author exercise: Merge Under A Supplied Contract.** Implement the same scan twice with only the overlap predicate changed.

### Merge And Insert

**Recognition cue.** Overlapping ranges should become their union, or one new range must be added to an already sorted disjoint list. **Invariant.** The output contains finalized disjoint intervals plus at most one active interval that may still grow. **False friend.** Insert does not require re-sorting when the input contract already supplies order and disjointness.

- **Build - LC 56 Merge Intervals.** Sort by start and extend the active end while overlap continues.
- **Vary - Author exercise: Merge Already-Sorted Intervals.** Remove the sorting step under an explicit ordered-input contract.
- **Boundary - Author exercise: One Interval Covers Many.** Let one long range absorb several following ranges and touching endpoints.
- **Recognize - LC 57 Insert Interval.** Emit intervals before the new range, merge its overlap block, then emit intervals after it.

### Two-List Intersection

**Recognition cue.** Two lists are individually sorted and disjoint, and the output needs all pairwise overlaps. **Invariant.** The current pair is the only unresolved cross-list pair involving both current intervals; after emitting their intersection, the interval with the smaller end cannot meet a later interval in the other list. **False friend.** Merging the lists computes a union, not intersections.

- **Build - Author exercise: Intersect One Pair.** Return `[max(start), min(end)]` only when it is nonempty under the endpoint contract.
- **Vary - Author exercise: One Interval Against A Sorted List.** Advance past intervals that end before the fixed interval begins.
- **Boundary - Author exercise: Touching Intersections.** Compare the closed and half-open answers at equal endpoints.
- **Recognize - LC 986 Interval List Intersections.** Emit an overlap and advance the interval with the smaller end.

### Overlap And Coverage

**Recognition cue.** The objective is to keep many compatible intervals, remove overlaps, or detect intervals fully covered by another. **Invariant.** For non-overlap selection, the kept interval has the smallest possible end among processed choices; for coverage, the greatest reachable end summarizes prior containers. **False friend.** Merging changes intervals and loses which original intervals should be removed.

- **Build - Author exercise: Keep Earlier Finishing Interval.** Given two overlapping intervals, identify which one leaves more room for future choices.
- **Vary - LC 435 Non-overlapping Intervals.** Sort by end and count intervals rejected by the greedy compatibility rule.
- **Boundary - LC 1288 Remove Covered Intervals.** Sort equal starts by descending end so a shorter interval cannot hide its container.
- **Recognize - LC 452 Minimum Number of Arrows to Burst Balloons.** Treat each arrow as a point kept inside the current intersection of compatible balloons.

### Event Sweep Ties

**Recognition cue.** The answer depends on how many intervals are active at each coordinate rather than on their merged geometry. **Invariant.** The running count equals the number of active intervals after all events at the current coordinate have been processed in contract-defined order. **False friend.** Sorting starts and ends independently can find a maximum count, but an explicit event stream is clearer when ties or multiple event types matter.

- **Build - Author exercise: Maximum Concurrent Half-Open Intervals.** Emit `+1` at starts and `-1` at ends, processing an end before a same-time start.
- **Vary - Author exercise: Maximum Concurrent Closed Intervals.** Reverse the equal-coordinate priority because touching closed intervals overlap.
- **Boundary - Author exercise: Many Events At One Coordinate.** Group or order ties so the running count cannot depend on input order.
- **Recognize - Author exercise: First Coordinate Reaching Capacity.** Sweep events and return the earliest point where active count reaches a supplied limit.

## Released Combination Lessons

### Sorting And Intervals

Sorting exposes intervals in an order where one local state—the active end or last selected end—summarizes all processed input. Interval semantics supply the overlap predicate. Sorting alone does not determine whether the task wants union, insertion, or maximum compatible selection.

- **Build - LC 56 Merge Intervals.** Sort by start and maintain one active union.
- **Vary - LC 57 Insert Interval.** Exploit an already sorted, disjoint input and process before/overlap/after regions.
- **Boundary - LC 435 Non-overlapping Intervals.** Change to end order and preserve the interval that finishes earliest.
- **Recognize - LC 452 Minimum Number of Arrows to Burst Balloons.** Recognize compatible overlap groups through their common rightmost feasible point.

### Deferred: Heap And Intervals

Meeting Rooms II and similar allocation problems need a heap whose minimum end time identifies the next reusable resource. Chapter 17 teaches that heap invariant and owns the full combination staircase.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Use safe endpoint comparison and state whether intervals are closed, open, or half-open.
- Return dynamic interval results through an explicit `List<int[]>` to `int[][]` conversion.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Sorting + Intervals | Endpoint order creates a local overlap decision; staircase: merge → insert → erase overlap |
| Deferred | Heap + Intervals | Chapter 17 supplies resource-release heap state |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.


## Technical Review Additions

These are vetted requirements from the Chapters 04–13 architecture review. They expand the source plan; they are not copied student-facing prose.

- **Endpoint tie policy:** add an event-sweep lesson. The order of a start and end at the same coordinate follows the interval contract: closed intervals may count touching endpoints as overlap, while half-open `[start, end)` intervals free an end before a same-time start. State and test that policy before sorting events.
- **Output conversion:** `List<int[]>` to `int[][]` is an explicit API/output step, not an asymptotic optimization; show `list.toArray(new int[list.size()][])` when that is the required return type.


## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** greedy scheduling, heap rooms.

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

