# Chapter map (generated; do not edit, edit the source spec)



## Lesson order

01. Windowed Streams  ->  01-windowed-streams.md
02. Expiring State  ->  02-expiring-state.md
03. Online Prefixes  ->  03-online-prefixes.md
04. Stream Order Statistics  ->  04-stream-order-statistics.md
05. Frequency Streams  ->  05-frequency-streams.md
06. Temporal Indexes  ->  06-temporal-indexes.md
07. Randomized Evolution  ->  07-randomized-evolution.md

# Chapter 38: Streaming and temporal state

**Status:** Authored curriculum specification; PDF generation remains pending.

## Purpose

Teach online APIs whose answers evolve as values or timestamped events arrive. The learner must state what can be forgotten, what must remain queryable, and when stale state is removed.

## Entry Contract

Queues, sliding windows, prefix state, heaps, ordered sets, hashing, probability, and binary search are prerequisites.

## Mastery Scope

The required LeetCode anchors are LC 933, LC 1797, LC 1352, and LC 2034. LC 2671 and LC 1825 are transfer problems. Other numbered problems in this specification are taxonomy examples or prerequisite reviews; they are not assigned work and do not receive complete solutions in the PDF.

## Independent Micro-Patterns

| Required lesson | Authoring obligation |
| --- | --- |
| fixed-window streams | Maintain only the portion still contributing to the answer. |
| expiring event state | Remove or ignore entries whose validity interval has ended. |
| online prefix recurrences | Turn append-only queries into prefix division, difference, or recurrence state. |
| order statistics on streams | Maintain median, trimmed mean, or rank under updates and corrections. |
| online frequency and uniqueness | Keep counts synchronized with the candidates they validate. |
| temporal indexes and buckets | Group events by timestamp and answer time-range queries. |
| randomized evolving state | Preserve the requested distribution as the represented set changes. |



## Released Combination Lessons

### Queue Time Window

- **Build - LC 346 Moving Average from Data Stream.** Bound by count.
- **Vary - LC 933 Number of Recent Calls.** Bound by timestamp.
- **Boundary - LC 362 Design Hit Counter.** Define the exact inclusive window.
- **Recognize - LC 1797 Design Authentication Manager.** Generalize expiry to keyed renewable state.

### Ordered Stream State

- **Build - LC 703 Kth Largest Element in a Stream.** Keep a bounded heap.
- **Vary - LC 295 Find Median from Data Stream.** Balance two ordered halves.
- **Boundary - LC 2034 Stock Price Fluctuation.** Repair corrected timestamps with lazy validation.
- **Recognize - LC 1825 Finding MK Average.** Maintain three ordered regions plus expiry.

## Practice Contract

Every lesson must state whether the stream is append-only, correctable, or expiring before choosing its data structure. Use short timestamp traces and focused state-update drills for the early staircase roles. Fully expand the four required anchors; present the two transfer problems as interview prompts with hints and review notes rather than complete code.

## Java Integrity Focus

- Use `long` for sums, products, timestamps, and count aggregation when needed.
- Avoid `PriorityQueue.remove(Object)` in hot paths; use ordered multisets or lazy deletion.
- Inject or parameterize time in author exercises where deterministic testing matters.

## Unlocked Combinations Preview

| Outcome | Combination | Review requirement |
| --- | --- | --- |
| Teach now | Queue + Time Window | Expiry and inclusivity are part of the API contract. |
| Teach now | Ordered Structures + Stream | Every active value belongs to one validated ordered region. |
| Already covered | Reservoir and weighted sampling | Chapter 35 owns probability proofs. |

## Composition Audit

All queue, sliding-window, prefix, heap, ordered-set, and randomization prerequisites are complete.

## Publication Gate

- Test equal timestamps, expired boundaries, corrections, duplicates, zeros, and numeric width.
- Compare append-only, correction-capable, and expiring variants explicitly.
- Render and validate the final PDF.

## Research Baseline

- [LeetCode Design problem list](https://leetcode.com/problem-list/design/).
- [Design-tag crosswalk](../design-tag-crosswalk.md).
- Oracle Java queue, heap, and navigable collection documentation.
