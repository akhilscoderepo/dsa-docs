<!-- lesson-kind: combination -->
<!-- lesson-id: queue-time-window -->
## Queue Time Window

<!-- stage: context -->
### Why The Alert Fires Minutes Late

A monitoring service pages the on-call engineer when the alert score of the last 60 seconds exceeds 500. Each failure adds a weight to the score, which is 1 for an ordinary failure and larger for a severe one. A developer implements the check in the obvious way. Every failure is appended to a list with its timestamp and weight, and the check runs after each failure and adds up the entries from the last minute. In the first week of testing, the alert fires within a second of the real spike. In production, traffic runs at 20,000 failures per second during an incident. After an hour the list holds 72 million entries, and the process spends more time summing than the next failure takes to arrive. The check falls behind its input, and the page reaches the engineer several minutes after the outage began. The heap also grows until the garbage collector stalls the whole service.

Nothing in the logic is wrong, because every score is correct. The cost grows with the age of the process and not with the length of the window. This lesson asks how to keep exactly the entries of the last `span` time units, and how to say precisely which entry on the border belongs to the window.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

The lesson Windowed Streams supplied the count window, where a queue holds the latest `k` values and a running sum changes by one addition and one subtraction per arrival. It also supplied the habit of keeping the sum in a `long`, so that a long stream of large values cannot wrap around. This lesson keeps that machinery and replaces the question that decides when the front leaves.

The lesson Expiring State supplied the vocabulary of a deadline and of live and ended entries, and it supplied the rule that equality at the deadline needs one documented answer. Entries that leave in the order they arrived can be removed from the front of one sequence without a search. This lesson uses that property for a stream where every entry has the same lifetime.

The new work is the combination. A count window decides by position, so the queue alone is enough. A time window decides by the clock, so each entry must carry its timestamp, and a rule must say which clock value is the current time. The lesson shows that the queue, the running sum and a half-open border together answer every question about the last `span` time units in constant amortized time.

<!-- stage: naive -->
### Keeping Every Event In A List

The direct design stores every event for the life of the process and scans the whole list on each query. Each entry holds a timestamp and a weight, where a weight counts how severe the event is. The score at time `now` is the sum of the weights of the entries whose timestamp lies inside the last `span` time units.

```java
final class NaiveScore {
    private final java.util.ArrayList<long[]> events = new java.util.ArrayList<>(); // {time, weight}
    private final long span;

    NaiveScore(long span) { this.span = span; }

    void add(long now, long weight) { events.add(new long[] {now, weight}); }

    long score(long now) {
        long limit = now - span;                    // events at or before this time are too old
        long sum = 0;
        for (long[] e : events) {                   // visits every event ever added
            if (e[0] > limit) sum += e[1];
        }
        return sum;
    }
}
```

With `span = 10`, the calls `add(2, 5)`, `add(4, 3)` and `add(9, 2)` followed by `score(11)` return 10, and `score(13)` returns 5, because the event at time 2 is then 11 units old and the other two are younger than 10. The class is correct on every small test.

```predict
The service receives 20000 events per second, the span is 60 seconds, and score is called once per event. After one hour of running, how many entries does one call to score visit, how many of them can still count, and how much memory does the list hold?

The list holds every event of the hour, which is 72 million entries. Each call visits all of them, although at most 1.2 million lie inside the last 60 seconds, so about 98 percent of the visits touch entries that can never count again. Every entry is an array object with two longs plus a reference, roughly 40 bytes, so the list needs close to 3 GB. Both the time per call and the memory grow without limit as the process keeps running.
```

<!-- stage: bottleneck -->
### Work That Grows With The Process Age

Let `n` be the number of events added so far and `w` the number that lie inside the window. One call to `score` costs O(n) time, and the list costs O(n) memory. The useful work is only O(w). For a service that runs for weeks, `n` is many orders of magnitude larger than `w`, and the gap widens with every event.

The repeated work has a clear shape. An event that falls out of the window at time `t` stays out for every later query, because time never moves backward. The naive scan tests the same expired entry again on every call and rejects it again. Deleting expired entries from the list would stop the memory growth, but `ArrayList.remove(0)` shifts every remaining element, so each removal costs O(w) and the call is still slow.

A correct design meets three requirements. An expired event must be dropped once and never examined again. The sum must update without a rescan. The border must have one exact definition, because an event that sits exactly `span` units old is either counted or not counted, and two parts of a program that disagree on this produce an off-by-one error that appears only on the tick where timestamps align.

<!-- stage: insight -->
### Remove From The Front By Age

#### The Stream Is Expiring

Before choosing a structure, state the kind of stream. Events here are appended in non-decreasing time order, and they are never corrected. Each event expires after the same `span`, so the stream is expiring and not correctable, and the oldest event is always the next to expire.

#### Three Parts That Move Together

<!-- names: arrival queue, cutoff, running sum -->

The **arrival queue** holds the live events in the order they arrived, each with its timestamp and weight. Because arrival order equals age order, the oldest live event is at the front, and a new event joins at the back. The **cutoff** is the time `now - span`. An event is live when its timestamp is strictly greater than the cutoff, so the window is the half-open range from the cutoff, excluded, to `now`, included. The **running sum** is the total weight of the arrival queue, kept as a `long` and adjusted by one addition for each arrival and one subtraction for each removal.

Every operation that receives a time first computes the cutoff. It then removes events from the front while the oldest timestamp is at or before the cutoff, and it subtracts each removed weight from the running sum. The score is then the running sum, with no further scan, because the queue holds exactly the live events. An `add` performs the same removal first and then appends the new event. The removal on `add` is what keeps memory bounded even when nobody asks for a score.

#### Why Equality Is Settled By The Cutoff

The rule "at or before the cutoff leaves" is one comparison, and both operations use it through the same code. An event at time 4 with `span = 10` is live at time 13, because 4 is greater than 3. It is gone at time 14, because 4 is not greater than 4. The window therefore always spans exactly `span` distinct integer times. A program that tested the border in two places, with `<` in one and `<=` in another, would count an event in `add` that `score` has already rejected. Time arrives as an argument, so a test can drive the clock to the exact border value.

<!-- stage: variables -->
### Fields Of The Alert Score

The score object stores four fields besides the argument `now` that each call receives. The caller supplies `now`, so no method reads the system clock, and a test can choose every timestamp.

- **span** is the window length, a `long` fixed at construction, with a value of at least 1.
- **queue** is the arrival queue of `{time, weight}` pairs, oldest first, and it contains only live events after any call.
- **sum** is the running sum of the weights in `queue`, as a `long`.
- **last** is the latest time passed to any call, used to reject a time that moves backward.

In the traces, the pointer `head` marks the index of the oldest live event among the cells, and `tail` marks the index of the newest event added. The queue holds `tail - head + 1` events, and an empty queue has `head` equal to `tail + 1`.

The invariant is that after every call, `queue` holds exactly the events with a timestamp greater than `last - span`, in non-decreasing time order, and `sum` equals the sum of their weights.

<!-- stage: trace -->
### Tracing Adds And Scores

#### Eviction On Each Call

The span is 10. Six events arrive over time, and the cells below list them in arrival order. The pointer `head` marks the index of the oldest live event, and the pointer `tail` marks the newest event added so far. When the queue is empty, `head` equals `tail + 1`. The first three adds all fit inside the window, so `head` stays at the first cell and the running sum grows to 10. A score at time 11 has the cutoff 1, so nothing leaves. The add at time 12 has the cutoff 2, and the event at time 2 is at or before it, so it leaves before the new event joins. Later calls repeat the pattern. A score at time 20 removes the event at time 9 without any add, and the last add removes the event at time 12.

```trace
{"cells":["t2 w5","t4 w3","t9 w2","t12 w4","t14 w1","t22 w6"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":-1},"vars":{"call":"new(span=10)","result":"none","queue":"[]","sum":0},"note":"Start: the queue is empty, the sum is 0, and no event has arrived."},{"at":{"head":0,"tail":0},"vars":{"call":"add(2,5)","result":"none","queue":"[t2]","sum":5},"note":"The first event joins the empty queue. The sum becomes 5."},{"at":{"head":0,"tail":1},"vars":{"call":"add(4,3)","result":"none","queue":"[t2,t4]","sum":8},"note":"The cutoff is -6, so nothing leaves. The event joins the back and the sum becomes 8."},{"at":{"head":0,"tail":2},"vars":{"call":"add(9,2)","result":"none","queue":"[t2,t4,t9]","sum":10},"note":"The cutoff is -1, so the queue is unchanged. The sum becomes 10."},{"at":{"head":0,"tail":2},"vars":{"call":"score(11)","result":10,"queue":"[t2,t4,t9]","sum":10},"note":"The cutoff is 1. The oldest event has time 2, which is greater, so nothing leaves and the score is the stored sum."},{"at":{"head":1,"tail":3},"vars":{"call":"add(12,4)","result":"none","queue":"[t4,t9,t12]","sum":9},"note":"The cutoff is 2. The event at time 2 is at or before it and leaves first, so the sum drops by 5. Then the new event joins."},{"at":{"head":2,"tail":4},"vars":{"call":"add(14,1)","result":"none","queue":"[t9,t12,t14]","sum":7},"note":"The cutoff is 4. The event at time 4 is on the border and leaves. The new event joins."},{"at":{"head":3,"tail":4},"vars":{"call":"score(20)","result":5,"queue":"[t12,t14]","sum":5},"note":"The cutoff is 10. The event at time 9 leaves, and the events at times 12 and 14 stay."},{"at":{"head":4,"tail":5},"vars":{"call":"add(22,6)","result":"none","queue":"[t14,t22]","sum":7},"note":"The cutoff is 12. The event at time 12 is on the border and leaves, so the queue holds the events at times 14 and 22."}]}
```

#### Border, Equal Times And Bad Input

The second trace uses the span 5. Two events arrive at the same time 3, which the queue stores as separate entries. A score at time 8 has the cutoff 3, so both entries at time 3 are at or before it and leave together. This is the exact border: the events are five units old, and the half-open range excludes them. A late score finds the queue empty, and the sum is 0. An add with a time smaller than the latest time is rejected, and it changes neither the queue nor the sum.

```trace
{"cells":["t3 w4","t3 w6","t8 w1","t21 w7"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":-1},"vars":{"call":"new(span=5)","result":"none","queue":"[]","sum":0},"note":"Start: the queue is empty, the sum is 0, and no event has arrived."},{"at":{"head":0,"tail":0},"vars":{"call":"add(3,4)","result":"none","queue":"[t3]","sum":4},"note":"The first event at time 3 joins the queue."},{"at":{"head":0,"tail":1},"vars":{"call":"add(3,6)","result":"none","queue":"[t3,t3]","sum":10},"note":"An equal time is allowed. The second event at time 3 joins the back, and the sum is 10."},{"at":{"head":2,"tail":1},"vars":{"call":"score(8)","result":0,"queue":"[]","sum":0},"note":"The cutoff is 3. Both events at time 3 are at or before it, so both leave and the sum is 0."},{"at":{"head":2,"tail":2},"vars":{"call":"add(8,1)","result":"none","queue":"[t8]","sum":1},"note":"The queue is empty, so nothing leaves. The event at time 8 joins and the sum is 1."},{"at":{"head":3,"tail":2},"vars":{"call":"score(20)","result":0,"queue":"[]","sum":0},"note":"The cutoff is 15. The event at time 8 leaves, the queue is empty and the score is 0."},{"at":{"head":3,"tail":2},"vars":{"call":"add(10,9)","result":"throws","queue":"[]","sum":0},"note":"Time 10 is smaller than the latest time 20, so the call throws. The queue and the sum do not change."},{"at":{"head":3,"tail":3},"vars":{"call":"add(21,7)","result":"none","queue":"[t21]","sum":7},"note":"The queue is empty. The event at time 21 joins and the sum is 7."}]}
```

<!-- stage: code -->
### The Alert Score With Injected Time

#### The Class

The class `AlertScore` stores each event as a two-element array of time and weight, and it takes the time as an argument. Both public methods call the private method `evict`, so the border rule exists in one place. The method `add` rejects a backward time before it changes anything.

An ordinary failure passes weight 1, so the running sum counts failures and the alert fires when `score` exceeds 500. A severe failure passes a larger weight and moves the score faster. The invariant is that the queue is sorted by time and holds exactly the events inside the half-open window, and that the sum matches it after every call.

```java
final class AlertScore {
    private final long span;
    private final java.util.ArrayDeque<long[]> queue = new java.util.ArrayDeque<>();
    private long sum;
    private long last = Long.MIN_VALUE;

    AlertScore(long span) {
        if (span < 1) throw new IllegalArgumentException("span must be at least 1");
        this.span = span;
    }

    private void evict(long now) {
        if (now < last) throw new IllegalArgumentException("time moved backward");   // checked before any change
        last = now;
        long cutoff = now - span;                                  // an event at or before this time is too old
        while (!queue.isEmpty() && queue.peekFirst()[0] <= cutoff) {
            sum -= queue.pollFirst()[1];                           // each event leaves once
        }
    }

    void add(long now, long weight) {
        evict(now);                                                // drop expired events first
        queue.addLast(new long[] {now, weight});                   // the newest event is the youngest
        sum += weight;
    }

    long score(long now) {
        evict(now);                                                // a quiet stream still expires
        return sum;
    }
}
```

#### Array With A Head Index

The Counts Over Several Window Lengths exercise needs a binary search over the live events. An `ArrayDeque` has no indexed access, so that exercise keeps an array and a head index. The live events sit in positions `head` to `tail - 1`, and eviction only moves `head` forward.

```java
final class IndexedWindow {
    private long[] times = new long[16];
    private int head, tail;                              // live events occupy [head, tail)

    void record(long now, long maxSpan) {
        while (head < tail && times[head] <= now - maxSpan) head++;   // evict by the widest border
        if (tail == times.length) {                                   // compact the live part to the front
            times = java.util.Arrays.copyOfRange(times, head, head + Math.max(16, 2 * (tail - head)));
            tail -= head; head = 0;
        }
        times[tail++] = now;
    }

    int count(long now, long span) {
        int lo = head, hi = tail;                        // search the first live event newer than now - span
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (times[mid] <= now - span) lo = mid + 1; else hi = mid;
        }
        return tail - lo;                                // a narrower window is a suffix of the live part
    }
}
```

#### Cost

- **add** costs O(1) amortized time, because each event is appended once and removed once.
- **score** costs O(1) amortized time, and a single call that removes many events pays for them all at once.
- **Memory** is O(w) for the `w` events inside the window, and it does not depend on the age of the process.

<!-- stage: applicability -->
### When A Queue Fits A Time Window

#### Recognizing The Pattern

Use this method when every event has the same lifetime, events arrive in non-decreasing time order, and the answer is a sum, a count or an average over the live events. Check three points before coding. State whether the border is inclusive or exclusive, and write it once in the code. Decide where time comes from, and pass it as an argument. Decide what happens to an entry when the stream is corrected. If the lifetimes differ by entry, or an entry can renew, the expiry order no longer matches the arrival order, and the exercises below show how to keep a second order for it. The invariant to protect in all variants is that the structure holds exactly the live entries and the running aggregate matches them.

#### False Friends

A cleanup task that runs every second looks like eviction, and it is a false friend. Between two runs, a score still includes events that expired, so the answer depends on when the task last ran. A second false friend is a window by event count used for a time question. The last 100 events cover one second at peak traffic and an hour at night, so the count cannot tell how recent they are.

#### When The Method Does Not Apply

If events can arrive out of time order, the front of the queue is no longer the oldest event, and the method gives wrong counts. The input then needs a buffer that waits for stragglers, or a sorted structure keyed by time. If the question asks for the maximum or the median of the live events, a sum cannot be adjusted by subtraction, and a monotonic deque or two ordered halves is needed instead.

<!-- stage: exercises -->
### Exercises

#### [Build] Smoothed Reading With Two Limits (LeetCode 346)
<!-- id: st38c-count-and-age-cap -->

**Prerequisites.** The count window from the lesson Windowed Streams and the cutoff from this lesson. This exercise changes the contract of LeetCode 346: the average also drops readings that are too old.

**Problem.** Design the class `CappedAverage` with a constructor that receives an `int` called `maxCount` and a `long` called `span`. The method `next(time, value)` records one reading and returns a `double`. The returned number is the average of the readings that are among the latest `maxCount` readings and also have a timestamp greater than `time - span`. The new reading always counts. The stream is expiring, and a reading leaves the window by either rule.

**Constraints.** The limits are:
- **maxCount** is an `int` from 1 to 100000, and **span** is a `long` from 1 to 10^12.
- **time** is a `long` from 0 to 10^15 that does not decrease, and equal times are allowed.
- **value** is an `int` from -10^9 to 10^9, and calls number at most 100000.
- **Decreasing time** throws `IllegalArgumentException` and changes nothing.

**Example 1.** Input: with `maxCount = 3` and `span = 10`, calls `next(1,4)`, `next(3,8)`, `next(5,6)`, `next(6,10)`, `next(20,2)`, `next(21,7)`; output `[4.0, 6.0, 6.0, 8.0, 2.0, 4.5]`.

**Example 2.** Input: with `maxCount = 2` and `span = 5`, calls `next(4,1000000000)`, `next(4,1000000000)`, `next(4,7)`, `next(9,3)`, `next(9,5)`; output `[1000000000.0, 1000000000.0, 500000003.5, 3.0, 4.0]`.

**Hint.** Which end of the queue does each of the two limits remove from, and can one loop test both conditions?

**Changed decision.** The single size condition of a count window becomes two conditions in one eviction loop. The sum must be a `long`, because 10^5 values of 10^9 exceed the `int` range.

#### [Vary] Counts Over Several Window Lengths (LeetCode 933)
<!-- id: st38c-many-spans-one-queue -->

**Prerequisites.** The Smoothed Reading exercise above. This exercise changes the contract of LeetCode 933: each query chooses its own window length, so the eviction border and the query border differ.

**Problem.** Design the class `MultiSpanCounter` with a constructor that receives a `long` called `maxSpan`. The method `record(time)` stores one event. The method `count(time, span)` returns the number of recorded events with a timestamp greater than `time - span`, for a `span` from 1 to `maxSpan`. Every call carries the current time, and the times of all calls do not decrease.

**Constraints.** The limits are:
- **maxSpan** is a `long` from 1 to 10^9, and **span** is a `long` from 1 to `maxSpan`.
- **time** is a `long` from 0 to 10^15, and calls number at most 100000.
- **Invalid input** means a span outside its range or a time that decreases throws `IllegalArgumentException`.
- **Memory** must depend on the events inside the widest window, not on the history.

**Example 1.** Input: with `maxSpan = 10`, calls `record(1)`, `record(2)`, `record(5)`, `record(5)`, `count(6,3)`, `count(6,10)`, `record(9)`, `count(12,4)`, `count(12,10)`, `count(20,10)`; output `[null, null, null, null, 2, 4, null, 1, 3, 0]`.

**Example 2.** Input: with `maxSpan = 4`, calls `count(3,4)`, `record(3)`, `record(3)`, `count(3,1)`, `count(7,4)`, `count(7,1)`; output `[0, null, null, 2, 0, 0]`.

**Hint.** Which cutoff may the structure use to drop events for good, and how can a narrower query find its first live event without scanning? Binary search needs indexed access, so keep an array and a head index.

**Changed decision.** Eviction uses the widest cutoff and never a query's cutoff, because a later query may be wider than an earlier one. A narrower query counts a suffix of the live events, found by binary search.

#### [Boundary] Correct The Newest Reading (LeetCode 362)
<!-- id: st38c-amend-latest-entry -->

**Prerequisites.** The Counts Over Several Window Lengths exercise above. The stream is now correctable at its newest entry, and the exact border decides whether a correction is allowed. This exercise changes the contract of LeetCode 362: events carry a weight, and the newest one can be replaced.

**Problem.** Design the class `ByteMeter` with a constructor that receives a `long` called `span`. The method `add(time, bytes)` appends an entry. The method `total(time)` returns the sum of `bytes` over the entries with a timestamp greater than `time - span`. The method `amend(bytes)` replaces the byte count of the most recently added entry. It throws `IllegalStateException` when no entry was added, or when that entry is outside the window at the latest time given to `add` or `total`.

**Constraints.** The limits are:
- **span** is a `long` from 1 to 10^12, and **bytes** is a `long` from 0 to 10^12.
- **time** is a `long` from 0 to 10^15 that does not decrease across `add` and `total`, with equal times allowed.
- **Calls** number at most 100000, and totals can exceed the `int` range.
- **amend** takes no time and does not move the clock.

**Example 1.** Input: with `span = 5`, calls `amend(1)`, `add(3,10)`, `total(7)`, `amend(4)`, `total(8)`, `amend(9)`, `add(8,2)`, `add(8,0)`, `amend(5)`, `total(8)`; output `["IllegalStateException", null, 10, null, 0, "IllegalStateException", null, null, null, 7]`.

**Example 2.** Input: with `span = 10`, calls `add(2,50)`, `add(6,30)`, `total(8)`, `amend(45)`, `total(8)`, `total(12)`, `amend(99)`, `total(16)`, `amend(1)`; output `[null, null, 80, null, 95, 45, null, 0, "IllegalStateException"]`.

**Hint.** Which element of the queue holds the newest entry, and what does an empty queue say about whether that entry is still live?

**Changed decision.** The queue gains one more operation, a replacement at the back, and the running sum changes by the difference. The border now decides a correction as well as a count.

#### [Recognize] Sessions With Idle And Hard Expiry (LeetCode 1797)
<!-- id: st38c-idle-and-hard-expiry -->

**Prerequisites.** The Correct The Newest Reading exercise above and the expiring entries from the lesson Expiring State. A renewal moves an entry in one order and leaves it in another. This exercise changes the contract of LeetCode 1797: a session ends by idleness or by a maximum age, whichever comes first.

**Problem.** Design the class `SessionStore` with a constructor that receives two `long` values, `idle` and `maxLife`. The method `open(key, time)` starts a session for a `String` key and replaces any earlier session of that key. The method `renew(key, time)` returns `true` and records the touch if the session is live, and returns `false` and changes nothing otherwise. The method `liveCount(time)` returns the number of live sessions. A session started at `s` and last touched at `l` is live at `time` when `time - l < idle` and `time - s < maxLife`.

**Constraints.** The limits are:
- **idle** and **maxLife** are `long` values from 1 to 10^12.
- **time** is a `long` from 0 to 10^15 that does not decrease across all calls.
- **key** is a nonempty `String`, and calls number at most 100000.
- **Renewal** changes the last touch and never the start.

**Example 1.** Input: with `idle = 5` and `maxLife = 12`, calls `open("a",0)`, `open("b",2)`, `renew("a",4)`, `liveCount(4)`, `renew("a",8)`, `renew("b",8)`, `liveCount(8)`, `renew("a",12)`, `liveCount(12)`, `renew("a",12)`; output `[null, null, true, 2, true, false, 1, false, 0, false]`.

**Example 2.** Input: with `idle = 3` and `maxLife = 3`, calls `open("x",1)`, `renew("x",3)`, `liveCount(3)`, `renew("x",4)`, `open("x",4)`, `liveCount(6)`, `liveCount(7)`; output `[null, true, 1, false, null, 1, 0]`.

**Hint.** A renewal changes the order of expiry by idleness. Which second order keeps the expiry by age sorted? Two insertion-ordered maps over the same keys give one order by last touch and one by start.

**Changed decision.** One queue becomes two ordered collections over the same keys, one by last touch and one by start. A key that fails either rule leaves both.
