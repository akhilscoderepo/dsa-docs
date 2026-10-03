# Chapter 20: Greedy

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| local choice | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| interval scheduling | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| reachability/farthest frontier | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| exchange reasoning in interviews | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| task selection | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

| Source ID | Family | Problem | Supplied role | Why this follows |
| --- | --- | --- | --- | --- |
| P0116 | Local choice | Assign Cookies | Direct concept | Sorts both sides and makes the smallest useful assignment. |
| P0117 | Interval scheduling | Minimum Number of Arrows to Burst Balloons | Immediate application | Reuses endpoint-based greedy selection. |
| P0118 | Reachability | Jump Game | New subtopic | Maintains the furthest reachable position. |
| P0119 | Reachability | Jump Game II | Immediate application | Turns reachability into minimum number of jumps. |
| P0120 | Greedy + ordering | Partition Labels | New variation | Uses last occurrences to determine safe partition boundaries. |
| Bundle 1-1 | Reachability | Jump Game | Learn | — |
| Bundle 1-2 | Reachability | Jump Game II | Extend | — |
| Bundle 1-3 | Gas/Capacity | Gas Station | Twist | — |

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Commit locally | Local choice can be proven to dominate alternatives | Proof, not intuition, establishes global optimality | https://leetcode.com/problems/non-overlapping-intervals/ | Core |
| Keep farthest reach | Need furthest reachable position | Only the furthest state dominates weaker reachable states | https://leetcode.com/problems/jump-game/ | Core |
| Current boundary + next farthest | Need minimum number of jumps/layers | All positions in a layer cost the same additional jump | https://leetcode.com/problems/jump-game-ii/ | Core |
| Take earliest ending compatible interval | Need select non-overlapping intervals | Earliest finish leaves maximal remaining room | https://leetcode.com/problems/non-overlapping-intervals/ | Core |
| Place resource at best boundary | Need minimum arrows/resources to cover intervals | One placement covers the maximum future overlap possible | https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/ | Core |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Greedy + Ordering | LC 455 Assign Cookies | LC 435 Non-overlapping Intervals | LC 452 Minimum Number of Arrows to Burst Balloons | LC 763 Partition Labels |
| Greedy + Heap | LC 1642 Furthest Building You Can Reach | LC 871 Minimum Number of Refueling Stops | LC 630 Course Schedule III | LC 502 IPO |
| Greedy + Monotonic Stack | LC 402 Remove K Digits | LC 316 Remove Duplicate Letters | LC 1081 Smallest Subsequence of Distinct Characters | LC 1673 Find the Most Competitive Subsequence |
| Greedy + Two Pointers | LC 455 Assign Cookies | LC 881 Boats to Save People | Author exercise: exact-capacity and singleton boundary | LC 948 Bag of Tokens |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Local Choice

**Recognition cue.** A decision must be committed now, and a proof shows that replacing any optimal solution's first conflicting decision with this choice cannot make the remainder worse. **Invariant.** After each commitment, an optimal completion still exists for the unresolved suffix. **False friend.** Choosing the locally largest reward is not greedy correctness without a dominance or exchange proof.

- **Build - Author exercise: Smallest Sufficient Match.** Assign the smallest resource that satisfies the smallest remaining demand.
- **Vary - LC 455 Assign Cookies.** Sort both sides and commit only useful assignments.
- **Boundary - Author exercise: Unusable Resources.** Advance the resource pointer without consuming a demand it cannot satisfy.
- **Recognize - LC 860 Lemonade Change.** Preserve scarce five-dollar bills by selecting a safe change combination.

### Interval Scheduling

**Recognition cue.** The objective selects the largest compatible set or uses the fewest points to cover overlapping intervals. **Invariant.** Keeping the earliest possible finishing boundary leaves at least as much room for all future choices. **False friend.** Sorting by start is natural for merging but does not prove maximum compatible selection.

- **Build - Author exercise: Choose Compatible Meetings.** Sort by end and accept the next nonoverlapping interval.
- **Vary - LC 435 Non-overlapping Intervals.** Count rejected intervals while retaining the earlier finishing one.
- **Boundary - Author exercise: Touching Endpoint Contract.** Decide compatibility using the declared closed or half-open model.
- **Recognize - LC 452 Minimum Number of Arrows to Burst Balloons.** Place one arrow at the current overlap group's earliest end.

### Farthest Frontier

**Recognition cue.** Many paths reach positions in a linear sequence, but only the farthest reachable boundary matters. **Invariant.** Every index up to `farthest` is reachable; encountering an index beyond it proves failure. **False friend.** Backtracking explores exponentially many jump sequences that the frontier already dominates.

- **Build - Author exercise: Update Reachable Prefix.** Scan only indices already inside the frontier.
- **Vary - LC 55 Jump Game.** Return whether the frontier reaches the last index.
- **Boundary - Author exercise: Zero Before The Frontier.** A zero is harmless when an earlier jump already crosses it.
- **Recognize - LC 45 Jump Game II.** Treat the current reachable boundary as one BFS-like jump layer and track the next frontier.

### Exchange Reasoning

**Recognition cue.** An interviewer asks why a local rule is globally safe. **Invariant.** Transform an arbitrary optimal solution to use the greedy choice without worsening its objective; repeat on the remaining problem. **False friend.** Examples support intuition but do not prove all inputs.

- **Build - Author exercise: Exchange Two Assignments.** Replace a larger resource used on a small demand with the smallest sufficient one.
- **Vary - Author exercise: Swap To Earlier Finish.** Replace an optimal schedule's first interval with an earlier-finishing compatible interval.
- **Boundary - Author exercise: Find A Counterexample.** Disprove the rule “always take the shortest interval” for maximum scheduling.
- **Recognize - Author exercise: Present A Greedy Proof.** State the choice, exchange transformation, preserved feasibility, and reduced subproblem for a supplied rule.

### Task Selection

**Recognition cue.** Tasks have capacities, deadlines, rewards, or costs, and the algorithm must decide which subset or order to keep. **Invariant.** The retained tasks are feasible under the processed constraint and are best according to the proven replacement rule. **False friend.** Sorting once is insufficient when feasibility can require ejecting an earlier choice.

- **Build - LC 1710 Maximum Units on a Truck.** Take available box types in descending unit value until capacity is filled.
- **Vary - Author exercise: Deadline-Compatible Unit Tasks.** Sort deadlines and take a task whenever one slot remains feasible.
- **Boundary - Author exercise: Equal Reward And Capacity Limit.** State a deterministic tie rule and use `long` for accumulated reward when required.
- **Recognize - LC 630 Course Schedule III.** Sort by deadline, retain durations, and eject the longest task when total time becomes infeasible.

## Released Combination Lessons

### Greedy And Ordering

Ordering makes the next locally dominant choice visible; the greedy proof explains why committing to it preserves an optimal completion. Sorting without the proof is only a heuristic.

- **Build - LC 455 Assign Cookies.** Match sorted demands with the smallest sufficient resources.
- **Vary - LC 435 Non-overlapping Intervals.** Order by end to maximize room for future intervals.
- **Boundary - LC 452 Minimum Number of Arrows to Burst Balloons.** Apply the closed-endpoint overlap rule at equal coordinates.
- **Recognize - LC 763 Partition Labels.** Use last-occurrence order to close a partition only when every included character ends inside it.

### Greedy And Heap

Greedy reasoning identifies which past option should be committed or discarded; the heap exposes that option dynamically. Heap priority alone does not prove the choice is safe.

- **Build - LC 1642 Furthest Building You Can Reach.** Use ladders for the largest climbs by ejecting smaller assignments to bricks.
- **Vary - LC 871 Minimum Number of Refueling Stops.** When fuel is insufficient, choose the largest station already passed.
- **Boundary - LC 630 Course Schedule III.** Remove the longest retained duration whenever a deadline becomes infeasible.
- **Recognize - LC 502 IPO.** Add projects as capital makes them eligible and select the largest available profit.

### Greedy And Monotonic Stack

The greedy proof permits removing a worse earlier choice while removals remain; the stack exposes the nearest such choice and preserves output order. A normal monotonic stack has no removal budget or final-length contract.

- **Build - LC 402 Remove K Digits.** Pop a larger previous digit while a removal remains.
- **Vary - LC 316 Remove Duplicate Letters.** Pop only when the removed character appears again later.
- **Boundary - LC 1081 Smallest Subsequence of Distinct Characters.** Preserve uniqueness, future availability, and leading-order decisions together.
- **Recognize - LC 1673 Find the Most Competitive Subsequence.** Use the remaining-length requirement as the pop budget.

### Greedy And Two Pointers

Sorting creates monotone candidate order; two pointers expose the cheapest feasible pairing, and greedy reasoning proves which endpoint can be committed. Pointer motion without that proof is guesswork.

- **Build - LC 455 Assign Cookies.** Advance through the smallest remaining demand and resource.
- **Vary - LC 881 Boats to Save People.** Pair the heaviest person with the lightest only when feasible.
- **Boundary - Author exercise: Exact Capacity And One Remaining Person.** Treat equality as feasible and count the final singleton once.
- **Recognize - LC 948 Bag of Tokens.** Spend the cheapest token for score and, when necessary, sell the most expensive to regain power.

### Deferred: Greedy And Dynamic Programming

Some problems look locally optimizable but require comparing reusable future states. Chapters 26–29 provide the state-value framework needed to distinguish those cases from genuinely safe greedy choices.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- State the comparator or ordering relation that makes a local choice safe.
- Use `long` where accumulated value or feasibility arithmetic can overflow.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Greedy + Ordering | Exchange argument validates a visible ordered choice; staircase: assignment → intervals → partition boundaries |
| Teach now | Greedy + Heap | Heap mechanics arrived in Chapter 17; greedy proof now releases deferred selection problems |
| Teach now | Greedy + Monotonic Stack | Chapter 12 supplied ordered stack state; this chapter supplies the safe-pop proof |
| Teach now | Greedy + Two Pointers | Chapter 8 supplied pointer elimination; this chapter proves endpoint commitment |
| Deferred | Greedy + Dynamic Programming | Chapters 26–29 supply explicit future-state comparison |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** dynamic-programming comparisons.

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

