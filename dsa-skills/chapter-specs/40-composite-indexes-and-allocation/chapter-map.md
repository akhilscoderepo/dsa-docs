# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Multi-Index Records  ->  01-multi-index-records.md
02. Dynamic Rankings  ->  02-dynamic-rankings.md
03. Resource Allocation  ->  03-resource-allocation.md
04. Frequency Buckets  ->  04-frequency-buckets.md
05. Validated Priority  ->  05-validated-priority.md
06. Transaction Lifecycles  ->  06-transaction-lifecycles.md

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
