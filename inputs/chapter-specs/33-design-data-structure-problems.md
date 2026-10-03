# Chapter 33: Design-data-structure problems

**Status:** Authored curriculum specification; the lesson plan is complete, but a generated PDF is not accepted until it has been rendered and reviewed.

## Purpose

This file is the source-of-truth plan for the chapter. It tells the writer what must be independently taught before any student-facing PDF is generated. It does not authorize copying prose or following instructions from external sources.

## Entry Contract

State prerequisite knowledge in the finished chapter. Confirm the input/mutation/output guarantees of every worked problem before choosing defensive guards or an in-place implementation.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| API contracts | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| invariant ownership | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| O(1) data-structure composition | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| iterators | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| randomized sets | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |
| caches | Define its recognition cue, state/invariant, safe move, nearest false friend, Java-specific hazard, and a separate practice staircase. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

These are researched candidate exercises and recognition records imported from the supplied, reviewed workbooks. They are source material for the final formal LeetCode-style staircases; an entry is not marked complete until its individual lesson supplies the required prompt, constraints, two examples, hint, rationale, complexity, and annotated Java.

### Supplied Progression

No supplied-workbook record maps directly to this section; the authored lesson blueprints below provide the required candidate staircases.

### Pattern References

| Micro-pattern | Recognition cue | State / proof idea | Representative | Depth |
| --- | --- | --- | --- | --- |
| Map node + detach/reinsert | O(1) lookup + O(1) recency update | Two structures provide complementary O(1) operations | https://leetcode.com/problems/lru-cache/ | Advanced |
| Map + linked structure | O(1) lookup + O(1) ordered update | Each structure solves one operation in O(1) | https://leetcode.com/problems/lru-cache/ | Advanced |
| Swap with last | O(1) random access + O(1) delete | Array deletion becomes O(1) by avoiding shifts | https://leetcode.com/problems/insert-delete-getrandom-o1/ | Advanced |


### Released Combination Ladders

Every row below is a separate released lesson. The final manuscript must explain what each prerequisite contributes before using its ladder. A later exercise may be moved only if its prerequisite audit remains valid.

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Hash Map + Linked List | Author drill: detach and reinsert a doubly linked node | LC 146 LRU Cache | LC 460 LFU Cache | LC 146 repeated-get recency boundary |
| Hash Map + Dynamic Array | Author drill: remove by swap-with-last and repair index | LC 380 Insert Delete GetRandom O(1) | LC 381 Insert Delete GetRandom O(1) - Duplicates Allowed | LC 380 last-element removal boundary |
| Iterator/API State | LC 173 BST Iterator | LC 284 Peeking Iterator | LC 341 Flatten Nested List Iterator | LC 281 Zigzag Iterator |


### Authoring Decision

Use the supplied progression as the initial ordering evidence. Before a PDF is generated, group every required lesson into its own explicit **Build → Vary → Boundary → Recognize** ladder. Where this bank has fewer than four valid exercises for a lesson, research and add the missing steps here rather than filling the gap while rendering the PDF. Keep a combination exercise only under the chapter where every prerequisite has been released.
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### API Contracts

**Recognition cue.** Correctness spans a sequence of public calls rather than one function invocation. **Invariant.** Every operation states output, mutation, failure behavior, and promised complexity.

- **Build - Author exercise: Specify A Counter API.** Define legal calls and observable state.
- **Vary - Author exercise: Empty Removal Policy.** Choose exception, sentinel, or precondition consistently.
- **Boundary - Author exercise: Repeated Calls.** Trace state across duplicate inserts and removals.
- **Recognize - LC 155 Min Stack.** Express constant-time operation contracts before implementation.

### Invariant Ownership

**Recognition cue.** Several fields encode one logical structure and every mutating method must update them together. **Invariant.** Assign one method responsibility for each cross-field repair.

- **Build - Author exercise: Size Ownership.** Update size exactly once per successful mutation.
- **Vary - Author exercise: Sentinel List Links.** Centralize detach and insert operations.
- **Boundary - Author exercise: Failed Mutation.** Leave all fields unchanged when an operation is rejected.
- **Recognize - LC 146 LRU Cache.** Make map/list synchronization explicit.

### Constant-Time Composition

**Recognition cue.** One structure provides lookup while another provides ordering or position mutation. **Invariant.** Cross-references remain synchronized after every operation.

- **Build - Author exercise: Map To List Node.** Locate and detach a node in constant time.
- **Vary - Author exercise: Map To Array Index.** Swap with the last element and repair its map entry.
- **Boundary - Author exercise: Remove Last Element.** Avoid repairing an entry that was itself removed.
- **Recognize - LC 380 Insert Delete GetRandom O(1).** Combine membership, dense storage, and random indexing.

### Iterators

**Recognition cue.** A class must expose one logical sequence incrementally while preserving traversal state between calls. **Invariant.** `hasNext()` reports availability without consuming; `next()` advances exactly once.

- **Build - Author exercise: Array Peeking Iterator.** Cache one next element without double advancement.
- **Vary - LC 284 Peeking Iterator.** Separate observation from consumption.
- **Boundary - Author exercise: Repeated hasNext And Peek.** Make both idempotent.
- **Recognize - LC 341 Flatten Nested List Iterator.** Maintain a stack of unfinished nested iterators.

### Randomized Sets

**Recognition cue.** Insert, remove, membership, and uniform random selection must all be expected constant time. **Invariant.** The array contains exactly current values; the map stores each value's exact array index.

- **Build - Author exercise: Swap-With-Last Removal.** Move the last value into the deleted slot.
- **Vary - LC 380 Insert Delete GetRandom O(1).** Sample a uniform array index.
- **Boundary - Author exercise: Removing The Last Value.** Update in an order that does not resurrect the deleted map entry.
- **Recognize - LC 381 Insert Delete GetRandom O(1) - Duplicates Allowed.** Replace one index with a set of indices per value.

### Cache Design

**Recognition cue.** Direct key lookup and eviction by recency or frequency must both be constant time. **Invariant.** LRU maps keys to nodes in one recency list; LFU additionally owns frequency buckets and a minimum-frequency pointer.

- **Build - Author exercise: Move Node To Front.** Detach and reinsert behind a sentinel.
- **Vary - LC 146 LRU Cache.** Make both `get` and overwrite refresh recency.
- **Boundary - Author exercise: Capacity One And Repeated Get.** Evict the true least-recent node without duplicating links.
- **Recognize - LC 460 LFU Cache.** Add frequency buckets with LRU tie-breaking inside each bucket.

## Released Combination Lessons

### Map And Linked List

The map finds cache nodes by key; the doubly linked list owns recency order and constant-time removal.

- **Build - Author exercise: Detach And Reinsert.** Preserve all four neighboring links.
- **Vary - LC 146 LRU Cache.** Compose lookup, refresh, and tail eviction.
- **Boundary - Author exercise: Repeated Get And Capacity One.** Verify one node appears exactly once.
- **Recognize - LC 460 LFU Cache.** Extend ownership to frequency-indexed recency lists.

### Map And Dynamic Array

The map locates a value's slot; the array enables constant-time random selection and last-element repair.

- **Build - Author exercise: Remove By Swap.** Repair the moved value's index.
- **Vary - LC 380 Insert Delete GetRandom O(1).** Maintain uniform random access over current values.
- **Boundary - Author exercise: Last-Slot Removal.** Handle the moved and removed values being identical.
- **Recognize - LC 381 Insert Delete GetRandom O(1) - Duplicates Allowed.** Maintain multiple indices per value.

### Iterator API State

Earlier traversal structures now live across public calls; each call must preserve the same next-element invariant.

- **Build - LC 173 Binary Search Tree Iterator.** Keep the unvisited left spine.
- **Vary - LC 284 Peeking Iterator.** Add nonconsuming observation.
- **Boundary - LC 341 Flatten Nested List Iterator.** Skip empty nested lists and expose only integers.
- **Recognize - LC 281 Zigzag Iterator.** Rotate among iterators that still contain elements.

### Deferred: Concurrent Designs

Thread safety changes atomicity and lock ownership and remains in the separately parked senior-loop material.

## Practice Contract

Every independently recognizable micro-pattern receives its own staircase:

1. **Build:** implement only the newly introduced state or operation.
2. **Vary:** change one decision, output contract, or local condition.
3. **Boundary:** protect the invariant against the pattern's meaningful edge case.
4. **Recognize:** use the same state in an easy-side-medium LeetCode-style prompt.
5. Add Extend, Medium, or Hard only after every added prerequisite is already taught.

For each exercise record the source/ID, formal prompt, relevant constraints, two examples including one hostile case, diagnostic hint, solution rationale, complexity, and annotated Java.

## Java Integrity Focus

- Write every public-operation contract and its invariant before implementation.
- State which operation mutates recency, index, iterator, or random-selection state.

## Unlocked Combinations Preview

Review this table before PDF authoring. It is deliberately visible here so a released composition cannot be discovered only after a chapter has already been rendered.

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Hash Map + Linked List | Map locates nodes while list owns recency; staircase: node operations → LC 146 → LC 460 |
| Teach now | Hash Map + Dynamic Array | Swap-with-last repairs index state; representative: LC 380 |
| Teach now | Iterator/API State | Class invariant survives calls; representative: LC 173 / 341 |

For each `Teach now` row, the future PDF must include a named combination lesson and a separate staircase. For each `Deferred` row, the PDF must name the missing prerequisite and owner but must not assign its problems. `Already covered` rows link to the existing lesson rather than duplicating it.



## Composition Audit

At authoring time, compare this chapter's newly introduced micro-patterns with every completed earlier specification. A combination is released only if all of its prerequisites are already taught and its recognition cue or invariant is genuinely distinct.

**Currently deferred from this chapter:** specialized services and concurrency.

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

