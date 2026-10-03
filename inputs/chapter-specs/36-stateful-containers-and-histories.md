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

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

### Supplied Progression

The live Design-tag crosswalk assigns 19 problems to this chapter. Public problems anchor the staircases; premium problems may appear as described variants with equivalent author exercises.

### Pattern References

| Micro-pattern | Recognition cue | Representative progression |
| --- | --- | --- |
| Operation trace | Constructor followed by interdependent calls | LC 1603, LC 1656 |
| Direct-address store | Bounded integer keys or explicit buckets | LC 705, LC 706, LC 707 |
| Circular buffer | Fixed capacity with wraparound | LC 622, LC 641, LC 3508 |
| Split container | Front, middle, and back must remain cheap | LC 1670, LC 1172 |
| Cursor history | Back/forward or insertion around a cursor | LC 1472, LC 2296 |
| Resource pool | Allocate smallest/free identifier and return it | LC 379, LC 2336, LC 2502 |
| Deferred bulk update | Apply one operation to a logical prefix/range | LC 1381, LC 2166 |

### Released Combination Ladders

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Containers + API State | Author bounded queue | LC 622 | LC 641 | LC 3508 |
| Multiple Collections + Ownership | Author reusable-ID pool | LC 2336 | LC 379 | LC 1172 |
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Operation Traces

**Recognition cue.** The input is a constructor plus a chronological list of method calls. **Invariant.** Each completed call leaves a legal state for every possible next call.

- **Build - Author exercise: Bounded Counter API.** Specify constructor, increment, reset, and query behavior.
- **Vary - LC 1603 Design Parking System.** Keep independent capacity state per car type.
- **Boundary - Author exercise: Rejected Calls.** Prove failed operations leave all fields unchanged.
- **Recognize - LC 1656 Design an Ordered Stream.** Return exactly the newly contiguous suffix released by one insertion.

### Direct Stores

**Recognition cue.** The prompt forbids a library map/set or provides a bounded key domain. **Invariant.** Each key has one deterministic bucket or direct slot, and update/remove preserve bucket ownership.

- **Build - Author exercise: Boolean Direct Set.** Use a bounded key domain.
- **Vary - LC 705 Design HashSet.** Replace direct addressing with bucketed collision handling.
- **Boundary - LC 706 Design HashMap.** Distinguish absent keys from stored values and update in place.
- **Recognize - LC 707 Design Linked List.** Preserve head/tail/size ownership across indexed mutation.

### Circular Buffers

**Recognition cue.** A fixed-capacity FIFO or deque must reuse array positions. **Invariant.** `head`, `size`, and modular index arithmetic identify every live slot exactly once.

- **Build - Author exercise: Ring Buffer.** Implement enqueue/dequeue with `head` and `size`.
- **Vary - LC 622 Design Circular Queue.** Expose front, rear, full, and empty without ambiguous indices.
- **Boundary - LC 641 Design Circular Deque.** Support mutation at both ends when capacity is one.
- **Recognize - LC 3508 Implement Router.** Combine bounded FIFO expiry with packet identity and destination queries.

### Split Containers

**Recognition cue.** Operations target several logical positions that one ordinary deque cannot expose cheaply. **Invariant.** Two containers differ in size by at most one and their boundary defines the logical middle.

- **Build - Author exercise: Balanced Two-Deque Sequence.** Rebalance after end insertion.
- **Vary - LC 1670 Design Front Middle Back Queue.** Define which middle is removed when size is even.
- **Boundary - Author exercise: Oscillating Empty Halves.** Preserve balance through repeated middle removal.
- **Recognize - LC 1172 Dinner Plate Stacks.** Maintain multiple bounded stacks plus the next writable location.

### Cursor Histories

**Recognition cue.** The class supports navigation through past state while new writes invalidate part of the future. **Invariant.** Stored elements and the current cursor jointly define the visible state.

- **Build - Author exercise: Undoable String Cursor.** Move backward and append after undo.
- **Vary - LC 1472 Design Browser History.** Truncate forward history after visiting a new page.
- **Boundary - Author exercise: Oversized Navigation.** Clamp movement without corrupting history.
- **Recognize - LC 2296 Design a Text Editor.** Combine cursor-local insertion/deletion with bounded context output.

### Resource Pools

**Recognition cue.** Identifiers or memory segments move between free and allocated states. **Invariant.** No resource is simultaneously free and allocated, and reuse follows the promised ordering rule.

- **Build - Author exercise: Reusable ID Pool.** Allocate and return identifiers exactly once.
- **Vary - LC 2336 Smallest Number in Infinite Set.** Combine an increasing frontier with returned smaller values.
- **Boundary - LC 379 Design Phone Directory.** Reject duplicate release and exhausted allocation.
- **Recognize - LC 2502 Design Memory Allocator.** Track contiguous free runs and release all blocks owned by one ID.

### Deferred Updates

**Recognition cue.** One operation changes many logical values, but eager rewriting would violate the target complexity. **Invariant.** Deferred metadata is applied exactly once when an element crosses the boundary where its final value becomes known.

- **Build - Author exercise: Prefix Increment Stack.** Store pending increments at prefix endpoints.
- **Vary - LC 1381 Design a Stack With Increment Operation.** Propagate deferred increments during pop.
- **Boundary - LC 2166 Design Bitset.** Keep global flip state consistent with count and string output.
- **Recognize - LC 1476 Subrectangle Queries.** Compare eager updates with an append-only overlay under different call ratios.

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

