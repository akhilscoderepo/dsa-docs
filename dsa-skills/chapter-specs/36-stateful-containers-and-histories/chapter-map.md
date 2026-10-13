# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Operation Traces  ->  01-operation-traces.md
02. Direct Stores  ->  02-direct-stores.md
03. Circular Buffers  ->  03-circular-buffers.md
04. Split Containers  ->  04-split-containers.md
05. Cursor Histories  ->  05-cursor-histories.md
06. Resource Pools  ->  06-resource-pools.md

# Chapter 36: Stateful containers and histories

**Status:** Authored curriculum specification; PDF generation remains pending.

## Purpose

Teach class-shaped problems whose difficulty comes from preserving a container invariant across a sequence of public calls. All ordinary arrays, lists, stacks, queues, maps, and deques are prerequisites.

## Entry Contract

The learner has completed Chapters 00-35. Every lesson begins with the constructor contract, legal operation sequence, failure behavior, complexity promise, and fields that jointly represent one logical state.

## Mastery Scope

The required LeetCode anchors are LC 622, LC 1472, LC 2336, and LC 1381. LC 1670 and LC 2502 are transfer problems. Other numbered problems in this specification are examples available to the author; they are not assigned work and do not receive complete solutions in the PDF.

**PDF exercise roles:** 28. This is seven four-step staircases containing four required anchors and two transfer prompts; research-only examples are excluded.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| operation-trace contracts | Define observable behavior across calls and distinguish API correctness from one-function correctness. |
| direct-address stores | Compare bounded-key arrays, bucketed hashing, and node ownership. |
| circular buffers | Teach head, tail, size, wraparound, full, and empty invariants. |
| split containers | Maintain two physical halves that expose front, middle, and back operations. |
| cursor and history state | Separate stored history from the current logical cursor and truncate invalid futures. |
| reusable resource pools | Track free, allocated, and returned identifiers without duplication. |
| deferred bulk mutation | Record a range-wide logical update without eagerly rewriting every element. |



## Released Combination Lessons

### Containers And API State

**Recognition cue.** A bounded queue-like API must preserve front/back behavior across full, empty, wraparound, and rejected calls. **Invariant.** Container indices identify each live element exactly once, and a public call restores that representation before returning. **False friend.** Knowing how to call a queue is not the same as designing the array state that implements one.

- **Build - Author exercise: Bounded Queue Contract.** Name full/empty behavior and state fields.
- **Vary - LC 622 Design Circular Queue.** Add modular storage.
- **Boundary - LC 641 Design Circular Deque.** Add symmetric end operations.
- **Recognize - LC 3508 Implement Router.** Add identity, expiry, and query indexes.

### Multiple Collections Ownership

**Recognition cue.** One collection chooses the next resource efficiently while another must answer whether that resource is already represented. **Invariant.** Every resource belongs to exactly one of the never-issued, allocated, or returned states, and all indexes agree about that ownership. **False friend.** A priority queue supplies order but cannot by itself prevent duplicate returned entries.

- **Build - Author exercise: Reusable-ID Pool.** Separate the never-issued frontier from returned IDs.
- **Vary - LC 2336 Smallest Number in Infinite Set.** Order reusable values.
- **Boundary - LC 379 Design Phone Directory.** Make release idempotence explicit.
- **Recognize - LC 1172 Dinner Plate Stacks.** Coordinate container state with writable/nonempty indexes.

## Practice Contract

Every lesson still has Build, Vary, Boundary, and Recognize roles, but those roles do not imply four full LeetCode solutions. Use short operation traces and focused implementation drills for Build and Boundary. Fully expand the four required anchors; present the two transfer problems as interview prompts with hints and review notes rather than complete code.

## Java Integrity Focus

- Prefer explicit `size` over using equal head/tail indices to represent both full and empty.
- Use `ArrayDeque`, `TreeSet`, or `PriorityQueue` only after stating the ordering and stale-entry policy.
- Keep helper methods as the sole owners of cross-field mutation.

## Unlocked Combinations Preview

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Containers + API State | Constructor and every method preserve one operation-sequence invariant. |
| Teach now | Multiple Collections + Ownership | Each logical resource appears in one state and every index agrees. |
| Already covered | Cache composition | Chapter 33 owns LRU/LFU and randomized-set composition. |

## Composition Audit

All required containers, hashing, linked lists, heaps, ordered sets, and amortized analysis were released earlier. Concurrency remains deferred to the separate senior curriculum.

## Publication Gate

- Crosswalk every lesson to the Design-tag inventory.
- Verify every staircase changes one meaningful design decision.
- Audit Java mutation order, modular arithmetic, and stale-index cleanup.
- Render, visually inspect, and text-validate the PDF.

## Research Baseline

- [LeetCode Design problem list](https://leetcode.com/problem-list/design/) and the dated local metadata snapshot.
- [Design-tag crosswalk](../design-tag-crosswalk.md).
- Oracle Java Collections documentation for container semantics and complexity.
