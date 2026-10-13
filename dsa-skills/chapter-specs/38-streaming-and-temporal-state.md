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

<!-- BEGIN VERIFIED-CANDIDATE-BANK -->
## Verified Candidate Bank

### Supplied Progression

The crosswalk assigns 18 previously unowned Design-tag problems here and links existing stream foundations from Chapters 09, 17, 33, and 35.

### Pattern References

| Micro-pattern | Recognition cue | Representative progression |
| --- | --- | --- |
| Fixed window | Only recent values/events contribute | LC 346, LC 933, LC 362 |
| Expiry | Validity ends at a timestamp | LC 359, LC 1797 |
| Online prefix | Query concerns the last `k` appends | LC 1352, LC 901 |
| Order statistics | Median/rank/trimmed average changes online | LC 295, LC 1825, LC 2034 |
| Frequency state | Answer depends on current multiplicity | LC 1429, LC 2671, LC 2526 |
| Temporal buckets | Queries aggregate named time ranges | LC 635, LC 1348, LC 3709 |
| Randomized state | Output distribution is part of correctness | LC 384 and Chapter 35 sampling |

### Released Combination Ladders

| Released combination | Build | Vary | Boundary | Recognize |
| --- | --- | --- | --- | --- |
| Queue + Time Window | LC 346 | LC 933 | LC 362 | LC 1797 |
| Ordered Structures + Stream | LC 703 | LC 295 | LC 2034 | LC 1825 |
<!-- END VERIFIED-CANDIDATE-BANK -->

## Lesson Blueprints

### Windowed Streams

**Recognition cue.** Values arrive one at a time and only the last `k` items or recent duration matters. **Invariant.** Stored state contains exactly the active window and its aggregate.

- **Build - LC 346 Moving Average from Data Stream.** Maintain a bounded queue and running sum.
- **Vary - LC 933 Number of Recent Calls.** Expire timestamps outside the time window.
- **Boundary - Author exercise: Large Sum Window.** Use `long` and define inclusive time boundaries.
- **Recognize - LC 362 Design Hit Counter.** Compare event queue and fixed-bucket implementations.

### Expiring State

**Recognition cue.** Entries remain valid until a deadline and methods may renew or count them. **Invariant.** A query never exposes expired state, even if physical cleanup is lazy.

- **Build - LC 359 Logger Rate Limiter.** Store the next allowed time per message.
- **Vary - LC 1797 Design Authentication Manager.** Renew live tokens and count unexpired tokens.
- **Boundary - Author exercise: Renew At Expiry.** Define whether equality is expired before mutation.
- **Recognize - Author exercise: Expiring Key Store.** Compare lazy validation with heap-driven cleanup.

### Online Prefixes

**Recognition cue.** Appends are permanent and each query asks about a suffix or accumulated recurrence. **Invariant.** Prefix state converts a suffix query into a constant-time relation unless a reset value breaks invertibility.

- **Build - Author exercise: Product Prefix Stream.** Append positive values and query the last `k` product.
- **Vary - LC 1352 Product of the Last K Numbers.** Reset prefix history after zero.
- **Boundary - Author exercise: Overflow Contract.** Match numeric width to stated constraints.
- **Recognize - LC 901 Online Stock Span.** Replace arithmetic prefixes with a monotonic compressed history.

### Stream Order Statistics

**Recognition cue.** Inserts, corrections, or removals must preserve a median, rank, or trimmed aggregate. **Invariant.** Ordered partitions cover every active value exactly once and satisfy their size/order relation.

- **Build - LC 295 Find Median from Data Stream.** Balance lower and upper heaps.
- **Vary - LC 2034 Stock Price Fluctuation.** Correct old timestamps while min/max remain queryable.
- **Boundary - Author exercise: Duplicate And Stale Heap Roots.** Validate heap entries before use.
- **Recognize - LC 1825 Finding MK Average.** Maintain low, middle, and high multisets over a sliding window.

### Frequency Streams

**Recognition cue.** Each update changes multiplicity, uniqueness, or whether a run condition has been met. **Invariant.** Candidate containers may contain stale values only when a count check filters them before exposure.

- **Build - LC 170 Two Sum III - Data structure design.** Store frequencies and answer complement queries.
- **Vary - LC 1429 First Unique Number.** Couple counts with a queue of possible unique values.
- **Boundary - LC 2671 Frequency Tracker.** Keep value counts and count-of-counts synchronized at zero.
- **Recognize - LC 2526 Find Consecutive Integers from a Data Stream.** Track the current suffix run instead of retaining the stream.

### Temporal Indexes

**Recognition cue.** Events are stored once and later queried by time, granularity, or interval. **Invariant.** Timestamp order and bucket semantics agree with inclusive query boundaries.

- **Build - LC 635 Design Log Storage System.** Normalize timestamp prefixes by requested granularity.
- **Vary - LC 1348 Tweet Counts Per Frequency.** Bucket event counts across a requested range.
- **Boundary - Author exercise: Sparse Empty Buckets.** Return zeros without materializing all time.
- **Recognize - LC 3709 Design Exam Scores Tracker.** Maintain cumulative scores for time/sequence queries.

### Randomized Evolution

**Recognition cue.** Public calls mutate a collection and later return randomized output. **Invariant.** Each valid arrangement or element has the promised probability under the current state.

- **Build - Author exercise: Fisher-Yates One Step.** Choose uniformly from the remaining suffix.
- **Vary - LC 384 Shuffle an Array.** Produce a uniform permutation and preserve reset state.
- **Boundary - Author exercise: Repeated Reset And Shuffle.** Avoid aliasing the original array.
- **Recognize - Author exercise: Streaming Sample Review.** Connect evolving state to Chapter 35 reservoir sampling.

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

