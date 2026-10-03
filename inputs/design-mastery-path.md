# Design Problems: Mastery Path

This is the learner-facing problem set for Chapters 36-41. The Design tag snapshot contains 134 problems, but the curriculum does **not** require solving all 134. The snapshot is a research inventory used to detect missing state models; it is not a checklist.

The required path contains 24 anchor problems. Each anchor was chosen because it makes a reusable state model visible. Twelve transfer problems then test whether the same reasoning survives a changed API, ordering rule, or update/query balance. The other 98 tagged problems are reference-only variants. They may be used for extra practice, but they do not receive full lessons and are not required before moving to LLD or machine coding.

## How To Use It

For each subtopic, first work through the chapter's small implementation and operation trace. Then solve the required anchor without copying the implementation. Use a transfer problem only after you can state the anchor's fields, invariant, mutation order, and per-operation complexity from memory.

You are ready to leave a family when you can do four things:

1. Turn the public methods into an explicit behavioral contract.
2. Name the smallest state that makes every operation possible.
3. State which fields or indexes must agree after every successful call.
4. Recognize the same state model when the surface story changes.

## Required Anchors

| Chapter | Required problems | What they establish |
| --- | --- | --- |
| 36 Stateful containers and histories | LC 622 Circular Queue; LC 1472 Browser History; LC 2336 Smallest Number in Infinite Set; LC 1381 Stack With Increment | circular ownership, cursor history, reusable resources, deferred updates |
| 37 Iterators, encodings, and versioned state | LC 900 RLE Iterator; LC 1286 Combination Iterator; LC 1146 Snapshot Array; LC 2080 Range Frequency Queries | persistent cursors, generated iteration, sparse versions, constructor-time indexing |
| 38 Streaming and temporal state | LC 933 Recent Calls; LC 1797 Authentication Manager; LC 1352 Product of the Last K Numbers; LC 2034 Stock Price Fluctuation | expiry, temporal validity, online prefixes, corrected stream state |
| 39 Dynamic query structures | LC 352 Data Stream as Disjoint Intervals; LC 715 Range Module; LC 1622 Fancy Sequence; LC 2642 Design Graph | canonical interval state, add/remove/query, deferred transforms, update/query tradeoffs |
| 40 Composite indexes and allocation | LC 2349 Number Container System; LC 2353 Food Rating System; LC 1845 Seat Reservation Manager; LC 432 All O(1) Data Structure | synchronized indexes, mutable ranking, allocation, frequency buckets |
| 41 Algorithmic services and simulations | LC 348 Tic-Tac-Toe or the supplied equivalent; LC 355 Design Twitter; LC 1396 Underground System; LC 677 Map Sum Pairs | maintained summaries, feed aggregation, lifecycle ledgers, prefix aggregates |

## Transfer Set

| Chapter | Transfer problems | Changed decision |
| --- | --- | --- |
| 36 | LC 1670 Front Middle Back Queue; LC 2502 Memory Allocator | balance two physical halves; allocate and release contiguous resources |
| 37 | LC 449 Serialize and Deserialize BST; LC 1993 Operations on Tree | exploit structural ordering; preserve rules spanning ancestors and descendants |
| 38 | LC 2671 Frequency Tracker; LC 1825 Finding MK Average | synchronize count-of-counts; combine expiry with three ordered regions |
| 39 | LC 1206 Design Skiplist; LC 2276 Count Integers in Intervals | implement an ordered structure; maintain aggregate coverage during merges |
| 40 | LC 1912 Movie Rental System; LC 2286 Booking Concert Tickets in Groups | move records between ordered views; combine local and global capacity |
| 41 | LC 588 In-Memory File System or the supplied equivalent; LC 642 Autocomplete System or the supplied equivalent | hierarchical namespaces; combine prefix lookup with mutable ranking |

## Reference Inventory

The remaining Design-tag problems stay in [the crosswalk](design-tag-crosswalk.md) only so authors can check that a supposedly new problem is actually a variant of a taught family. They are not scheduled exercises. If a reference problem introduces a genuinely different invariant in the future, it may replace a weaker anchor; it should not simply be added to the learner's workload.
