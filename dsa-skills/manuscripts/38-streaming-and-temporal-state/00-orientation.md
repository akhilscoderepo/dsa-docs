<!-- section: orientation -->
## Orientation

A rate limiter counts requests in the last sixty seconds. It works in testing, then lets a burst through at exactly second sixty, because one request sits on the boundary and the code disagrees with the spec about whether that second still counts. This chapter teaches APIs whose answers change as values or timestamped events arrive. Each lesson asks what the object may forget, what it must keep queryable, and when stale state disappears.

### Prerequisites

You should know queues, sliding windows, prefix sums, heaps, ordered sets, hash maps and binary search. A **stream** is a sequence of values that arrive one call at a time. A stream is **append-only** when old values never change, **correctable** when a call can replace an earlier value, and **expiring** when old values stop counting after a duration. A **window** is the part of the stream that still contributes to the answer. A **timestamp** is the time of an event, and every lesson here passes time into the methods so tests stay deterministic.

### What Each Lesson Protects

One fact that every call must keep true is named in each lesson.

- **Windowed Streams** keeps exactly the active window and its running total, so each call does constant amortized work.
- **Expiring State** never shows a record past its deadline, even when cleanup is lazy.
- **Online Prefixes** turns a question about the newest k values into one relation between stored prefixes.
- **Stream Order Statistics** keeps every active value in exactly one ordered region, so the median or extreme stays readable.
- **Frequency Streams** keeps counts and the containers built on them in agreement.
- **Temporal Indexes** makes bucket boundaries and query boundaries mean the same instants.
- **Randomized Evolution** keeps the promised probability as the collection changes.
- **Queue Time Window** joins count limits, time limits, corrections and keyed expiry in one queue.
- **Ordered Stream State** joins ranks, windows and corrections with heaps and ordered maps.

### Reading Order

Every lesson opens with a class that passes short tests but is slow, wrong or unsafe on longer ones. The reasoning appears only after you predict the failure. Two traces follow the fields call by call. Next come the code in Java and a note on where the idea stops fitting. The four exercises start with a basic build, move to a variation and an edge case, and end with a recognition problem. A **false friend** is a design that looks like the pattern but breaks its precondition. Each solution compares its class with a brute-force **oracle**, a slow but obviously correct version, on random inputs.

### What You Can Do After This Chapter

You can state for any stream API whether it is append-only, correctable or expiring before you choose a structure. You can say whether the boundary instant is inside or outside the window and keep that rule on every path. Reservoir sampling proofs belong to chapter 35, and caches belong to chapter 33.
