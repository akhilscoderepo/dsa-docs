# Chapter 40: Composite indexes and allocation

**Status:** Authored curriculum specification; PDF generation remains pending.

## Purpose

Teach hard Design problems in which the same logical record appears in several indexes: direct lookup, ranking, availability, frequency, price, or recency. Correctness depends on atomic cross-index repair.

## Entry Contract

Chapter 33 cache composition, heaps, ordered maps/sets, linked lists, lazy deletion, and interval/resource reasoning are prerequisites.

## Mastery Scope

The required LeetCode anchors are LC 2349, LC 2353, LC 1845, and LC 432. LC 1912 and LC 2286 are transfer problems. Other numbered problems in this specification are taxonomy examples or prerequisite reviews; they are not assigned work and do not receive complete solutions in the PDF.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| multi-index consistency | Define one source of truth and repair every secondary index. |
| dynamic rank views | Maintain top/bottom queries under score changes and ties. |
| availability allocation | Separate available resources from allocated ownership. |
| frequency bucket structures | Move keys/items between ordered frequency groups in constant or logarithmic time. |
| priority with stale entries | Validate heap candidates against authoritative current state. |
| transactional state transitions | Make multi-step rent, return, reserve, cancel, or purchase operations atomic. |

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

### Supplied Progression

The crosswalk assigns 16 problems here, while LRU, LFU, randomized sets, and ordinary heap scheduling remain owned by Chapters 17 and 33.

### Pattern References

| Micro-pattern | Recognition cue | Representative progression |
| --- | --- | --- |
| Multi-index record | Lookup and ordered views share mutable records | LC 2349, LC 2353, LC 1912 |
| Dynamic rank | Query highest/lowest after updates | LC 1244, LC 2102, LC 3408 |
| Allocation | Reserve smallest/best available resource | LC 855, LC 1845, LC 2286 |
| Frequency buckets | O(1) or logarithmic frequency movement | LC 432, LC 895, LC 460 |
| Stale priority | Heap entries outlive corrected state | LC 2034 review, LC 1912 |
| Transaction lifecycle | Operations move entities through legal states | LC 2241, LC 3815, LC 3822, LC 3885 |

### Released Combination Ladders

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Map + Ordered Index | LC 2349 | LC 2353 | LC 1912 | LC 3408 |
| Availability + Priority | LC 1845 | LC 855 | LC 2286 | Author allocation service |
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Multi-Index Records

**Recognition cue.** The same entity must support lookup by ID and ordered/filter views by mutable attributes. **Invariant.** Authoritative record state and every secondary index describe exactly the same live entities.

- **Build - LC 2349 Design a Number Container System.** Map index to number and number to ordered indices.
- **Vary - LC 2353 Design a Food Rating System.** Order by rating with deterministic name tie-breaking.
- **Boundary - Author exercise: Update To Same Value.** Avoid duplicate index entries and unnecessary removal.
- **Recognize - LC 1912 Design Movie Rental System.** Maintain available and rented views over shared records.

### Dynamic Rankings

**Recognition cue.** Scores change while queries request the next, top, or lowest ranked entity. **Invariant.** Comparator order is total, tie policy is explicit, and updates remove the exact old key before inserting the new key.

- **Build - LC 1244 Design A Leaderboard.** Maintain scores and top-`k` totals.
- **Vary - LC 2102 Sequentially Ordinal Rank Tracker.** Partition returned and not-yet-returned ranks.
- **Boundary - Author exercise: Equal Scores And Renames.** Use a comparator consistent with identity.
- **Recognize - LC 3408 Design Task Manager.** Update priority and execute the global best task.

### Resource Allocation

**Recognition cue.** Calls reserve and release resources under a smallest, nearest, or contiguous-fit rule. **Invariant.** Availability and ownership form a partition of the resource set.

- **Build - LC 1845 Seat Reservation Manager.** Reserve the smallest free seat.
- **Vary - LC 855 Exam Room.** Choose the seat maximizing distance with deterministic ties.
- **Boundary - Author exercise: Duplicate Release.** Reject or define repeated unreserve explicitly.
- **Recognize - LC 2286 Booking Concert Tickets in Groups.** Combine contiguous capacity and prefix availability queries.

### Frequency Buckets

**Recognition cue.** Operations update counts and must expose min, max, or most-frequent elements efficiently. **Invariant.** Every live key belongs to exactly one frequency group and group order matches the count.

- **Build - Author exercise: Key Frequency Buckets.** Move keys between adjacent count groups.
- **Vary - LC 432 All O`one Data Structure.** Return any min/max key in constant time.
- **Boundary - Author exercise: Empty Bucket Removal.** Repair neighbors and min/max ownership.
- **Recognize - LC 895 Maximum Frequency Stack.** Break frequency ties by recency.

### Validated Priority

**Recognition cue.** Fast updates make direct arbitrary heap removal expensive. **Invariant.** The map/record is authoritative; a heap root is exposed only if it still matches current state.

- **Build - Author exercise: Versioned Heap Entry.** Reject stale roots by version.
- **Vary - LC 1912 Design Movie Rental System.** Maintain ordered availability and rental reports.
- **Boundary - Author exercise: Repeated Corrections.** Prevent stale entries from changing observable results.
- **Recognize - LC 3815 Design Auction System.** Select the current winning bid under updates and withdrawals.

### Transaction Lifecycles

**Recognition cue.** One public call moves an entity through a lifecycle and touches multiple balances or indexes. **Invariant.** Either every required state change occurs or none becomes visible.

- **Build - LC 2241 Design an ATM Machine.** Dispense under denomination and inventory constraints.
- **Vary - LC 3822 Design Order Management System.** Track legal order transitions and indexed retrieval.
- **Boundary - Author exercise: Failed Transition Rollback.** Leave balances and indexes unchanged.
- **Recognize - LC 3885 Design Event Manager.** Coordinate event identity, schedule, and lifecycle views.

## Released Combination Lessons

### Map Ordered Index

- **Build - LC 2349 Design a Number Container System.** Synchronize direct and ordered lookup.
- **Vary - LC 2353 Design a Food Rating System.** Add mutable scores and ties.
- **Boundary - LC 1912 Design Movie Rental System.** Move records between availability states.
- **Recognize - LC 3408 Design Task Manager.** Execute and remove the globally best live record.

### Availability Priority

- **Build - LC 1845 Seat Reservation Manager.** Choose the smallest available resource.
- **Vary - LC 855 Exam Room.** Derive priority from gaps rather than resource IDs.
- **Boundary - Author exercise: Stale Gap Candidate.** Validate both neighboring occupied seats.
- **Recognize - LC 2286 Booking Concert Tickets in Groups.** Combine local contiguous space with global capacity.

## Practice Contract

Every exercise must list all indexes modified by each public operation before presenting code. Use cross-index mutation traces and failure-repair drills for the early staircase roles. Fully expand the four required anchors; present the two transfer problems as interview prompts with hints and review notes rather than complete code.

## Java Integrity Focus

- Use immutable composite keys or remove-before-mutate when fields participate in `TreeSet` ordering.
- Use `Integer.compare`/`Long.compare`; never subtract comparator fields.
- Define atomic mutation helpers so failures cannot leave half-repaired indexes.

## Unlocked Combinations Preview

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Map + Ordered Index | Direct and ordered views agree after every update. |
| Teach now | Availability + Priority | Candidate priority is validated against current ownership. |
| Already covered | Map + linked-list cache | Chapter 33 owns LRU/LFU foundations. |

## Composition Audit

All map, heap, ordered-set, interval, and cache prerequisites are complete. This chapter owns their multi-index consistency combinations.

## Publication Gate

- Draw the authoritative record and every derived index for each lesson.
- Trace update-to-same-value, ties, cancellation, stale entries, and failed transitions.
- Render and validate the final PDF.

## Research Baseline

- [LeetCode Design problem list](https://leetcode.com/problem-list/design/).
- [Design-tag crosswalk](../design-tag-crosswalk.md).
- Oracle Java `TreeMap`, `TreeSet`, and `PriorityQueue` documentation.

