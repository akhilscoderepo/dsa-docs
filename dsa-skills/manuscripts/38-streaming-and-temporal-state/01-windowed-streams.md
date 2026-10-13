<!-- lesson-kind: standard -->
<!-- lesson-id: windowed-streams -->
## Windowed Streams

<!-- stage: context -->
### Why A Rate Limiter Slows Down

An API gateway allows each client 100 requests per minute. Its rate limiter appends the timestamp of every request to a list. To decide whether a new request passes, the limiter scans the list and counts the timestamps from the last 60 seconds. The code is correct and the tests pass. Then a customer script sends 5000 requests per second for an hour. The list grows by millions of entries, each check scans all of them, and the gateway stops answering within minutes. Memory fills with timestamps that can never change an answer again.

A second service shows the same shape with a count in place of a clock. A dashboard reports the average latency of the last 100 requests, and it copies the whole latency history before it averages. Both programs keep everything and look at a small tail. This lesson asks which part of an endless stream a program must keep, and how it forgets the rest without losing the answer.

<!-- stage: naive -->
### Store Everything And Scan

The direct design stores every value and recomputes the answer from the stored list. The class below answers "how many pings arrived in the last `span` time units" by keeping all timestamps. A second method averages the last `k` numbers by summing the tail of a list.

```java
final class NaiveStreams {
    private final java.util.ArrayList<Long> times = new java.util.ArrayList<>();
    private final java.util.ArrayList<Integer> values = new java.util.ArrayList<>();

    int ping(long t, long span) {
        times.add(t);                              // keeps every timestamp forever
        int count = 0;
        for (long u : times)                       // scans the whole history on every call
            if (u > t - span) count++;
        return count;
    }

    double average(int v, int k) {
        values.add(v);
        long sum = 0;
        int from = Math.max(0, values.size() - k);
        for (int i = from; i < values.size(); i++) sum += values.get(i);   // re-adds k numbers on every call
        return (double) sum / (values.size() - from);
    }
}
```

With `span = 5`, the pings at times 1, 3, 3, 8 return 1, 2, 3 and 1. With `k = 2`, the values 4, 6, 10 average to 4.0, 5.0 and 8.0. Every answer is correct.

```predict
A client sends one million pings, one per time unit, with span = 100. Roughly how many timestamps does the class hold at the end, and roughly how many comparisons does the last call to ping perform? What does the total number of comparisons look like for all one million calls?

The class holds all one million timestamps, although at most 100 of them can matter. The last call compares against all one million entries. The total is about 1 + 2 + ... + 10^6, close to 5 * 10^11 comparisons, so the program slows down in proportion to the square of the stream length while its memory grows with every call.
```

<!-- stage: bottleneck -->
### Cost Grows With The Whole Stream

After `n` calls the naive class stores `n` timestamps and scans `n` entries on the next call. A single call costs O(n) time, a run of `n` calls costs O(n^2) time in total, and the memory is O(n). The average method scans only the last `k` entries, so a call costs O(k) time. That cost still repeats work, because two neighboring calls add up almost the same `k` numbers. Only one number leaves and one number enters between them.

Both methods also keep entries that are certain to be useless. Once the clock passes `t + span`, a timestamp `t` can never count again, because later calls only move the clock forward. Once more than `k` values arrive after a value, that value can never enter an average again. The program holds on to data whose future effect is zero.

A better design must meet three needs. It must store only the entries that can still change an answer, so memory depends on the window and not on `n`. It must update the answer from the change between two calls, and not from a fresh scan. It must remove an entry at the moment it stops counting, and the moment must come from a written rule.

<!-- stage: insight -->
### Keep The Window, Update The Sum

#### Decide What Kind Of Stream It Is

<!-- names: active window, running sum, eviction, boundary -->

Before choosing a structure, classify the stream. An **append-only** stream never revises a value after it arrives. A **correctable** stream can replace a value that arrived earlier. An **expiring** stream drops a value when its age or its position passes a limit. The streams in this lesson are append-only, and their values expire. Arrivals come in order, no call changes an older value, and the only removal is expiry from the old end. A correctable stream needs a different structure, which later lessons build.

#### The Window Is A Queue With A Sum

The **active window** is the set of stored values that can still change the next answer. For a count rule, it holds the last `k` values. For a time rule with length `span`, it holds the events whose timestamp lies in a stated range that ends at the current time. Arrivals enter at the new end and expiry leaves from the old end, so a queue stores the window in arrival order.

The **running sum** is the total of the values in the window, stored in one `long` field. A new value adds its amount to the field. An expired value subtracts the same amount. Each call changes the field by a constant number of operations, so the cost does not depend on `k` or on `n`. For a pure count of events, the size of the queue replaces the sum.

#### Eviction Needs A Written Rule

**Eviction** is the removal of expired entries from the old end of the queue. It runs inside the call that needs the new answer, as a loop that stops at the first entry that is still inside the window. Each entry enters once and leaves once, so the loops add up to O(1) amortized time per call.

The **boundary** is the exact timestamp that separates an expired event from a live one. A rule such as "events from the last 5 seconds" does not say whether the event exactly 5 seconds old counts. The contract must state it. The trace uses one convention. An event with timestamp `u` counts at time `t` when `t - span < u <= t`. Eviction therefore removes every entry with `u <= t - span`. The exercises use other conventions on purpose.

The invariant is that the queue holds exactly the entries inside the window at the latest call, and the running sum equals their total.

<!-- stage: variables -->
### Queue, Sum, And Clock

The two classes in this lesson share the same few pieces of state.

- **window** is the queue of entries in arrival order, with the oldest at the front.
- **sum** is the `long` total of the values in `window`, and it equals 0 when `window` is empty.
- **k** is the largest number of values the count rule keeps.
- **span** is the length of the time rule, in the same unit as the timestamps.
- **now** is the timestamp of the current call, passed in by the caller and never read from a system clock.

Timestamps never decrease from one call to the next. Equal timestamps are allowed, and each one is a separate event. In the traces, the pointer `head` marks the oldest entry still in the window and `tail` marks the newest entry that has arrived. The window size is `tail - head + 1`.

<!-- stage: trace -->
### Tracing Both Window Rules

#### A Window Of The Last Three Values

The first trace uses the count rule with `k = 3` and the values 4, 1, 7, 2, 9 and 5. Before any call, `head` is 0 and `tail` is -1, so the window is empty. The first three values enter without eviction, and the sum grows to 12. The fourth value, 2, makes the window size 4, which exceeds `k`. The loop evicts the oldest value, 4, so the sum becomes 12 + 2 - 4 = 10, and `head` moves to 1. The fifth value, 9, evicts 1 and gives 10 + 9 - 1 = 18. The sixth value, 5, evicts 7 and gives 18 + 5 - 7 = 16. At every step the sum is the total of the cells from `head` to `tail`, and the average is that sum divided by the window size.

```trace
{"cells":["4","1","7","2","9","5"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":-1},"vars":{"event":"start","sum":0,"size":0,"average":"none"},"note":"Start: the window is empty, so head is 0 and tail is -1."},{"at":{"head":0,"tail":0},"vars":{"event":"add 4","sum":4,"size":1,"average":"4.00"},"note":"4 enters; the window holds 1 value and the sum is 4."},{"at":{"head":0,"tail":1},"vars":{"event":"add 1","sum":5,"size":2,"average":"2.50"},"note":"1 enters; the window holds 2 values and the sum is 5."},{"at":{"head":0,"tail":2},"vars":{"event":"add 7","sum":12,"size":3,"average":"4.00"},"note":"7 enters; the window holds 3 values, which equals k, so nothing leaves."},{"at":{"head":1,"tail":3},"vars":{"event":"add 2","sum":10,"size":3,"average":"3.33"},"note":"2 enters and the size 4 exceeds k, so 4 leaves; head moves to 1 and the sum is 10."},{"at":{"head":2,"tail":4},"vars":{"event":"add 9","sum":18,"size":3,"average":"6.00"},"note":"9 enters and 1 leaves; head moves to 2 and the sum is 18."},{"at":{"head":3,"tail":5},"vars":{"event":"add 5","sum":16,"size":3,"average":"5.33"},"note":"5 enters and 7 leaves; head moves to 3 and the sum is 16."}]}
```

#### A Window Of The Last Five Time Units

The second trace uses the time rule with `span = 5` and the pings at times 1, 3, 3, 8, 9 and 13. The rule keeps a ping when `t - 5 < u`. At time 3, nothing expires, because 3 - 5 is negative, so the count is 3 and includes both pings at time 3. At time 8, the cutoff is 3, so the loop evicts the pings at times 1, 3 and 3 and stops at the first entry that is newer. Only the ping at time 8 remains. At time 9, the cutoff is 4 and nothing leaves, so the count is 2. At time 13, the cutoff is 8, so the ping at time 8 leaves and the count is 2 again. The pointer `head` only moves right, and it moves right at most once per ping in total.

```trace
{"cells":["1","3","3","8","9","13"],"pointers":["head","tail"],"steps":[{"at":{"head":0,"tail":-1},"vars":{"event":"start","cutoff":"none","count":0},"note":"Start: no pings yet, so head is 0 and tail is -1."},{"at":{"head":0,"tail":0},"vars":{"event":"ping 1","cutoff":-4,"count":1},"note":"The cutoff is -4, so nothing expires and the count is 1."},{"at":{"head":0,"tail":1},"vars":{"event":"ping 3","cutoff":-2,"count":2},"note":"The cutoff is -2, so nothing expires and the count is 2."},{"at":{"head":0,"tail":2},"vars":{"event":"ping 3","cutoff":-2,"count":3},"note":"A second ping at time 3 is a separate event; the cutoff is -2 and the count is 3."},{"at":{"head":3,"tail":3},"vars":{"event":"ping 8","cutoff":3,"count":1},"note":"The cutoff is 3, so the pings at times 1, 3 and 3 expire; head moves to 3 and the count is 1."},{"at":{"head":3,"tail":4},"vars":{"event":"ping 9","cutoff":4,"count":2},"note":"The cutoff is 4 and the oldest ping is 8, so nothing leaves and the count is 2."},{"at":{"head":4,"tail":5},"vars":{"event":"ping 13","cutoff":8,"count":2},"note":"The cutoff is 8, so the ping at time 8 expires; head moves to 4 and the count is 2."}]}
```

<!-- stage: code -->
### Two Windows With Injected Time

#### The Count Window

The count window keeps a queue of at most `k` values and a `long` sum. Adding a value adds it to the sum, and one eviction subtracts the oldest value when the queue is too long.

```java
final class CountWindow {
    private final int k;
    private final java.util.ArrayDeque<Integer> window = new java.util.ArrayDeque<>();
    private long sum;                       // long, because k values of 10^9 overflow an int

    CountWindow(int k) { this.k = k; }

    double add(int v) {
        window.addLast(v);                  // the new value enters at the new end
        sum += v;                           // the sum changes by this value only
        if (window.size() > k) sum -= window.pollFirst();   // at most one value leaves per arrival
        return (double) sum / window.size();   // size is at least 1 here
    }
}
```

#### The Time Window

The time window stores timestamps and takes the current time as an argument, so a test controls the clock. The eviction loop uses the convention `u <= now - span`.

```java
final class TimeWindow {
    private final long span;
    private final java.util.ArrayDeque<Long> window = new java.util.ArrayDeque<>();

    TimeWindow(long span) { this.span = span; }

    int ping(long now) {
        window.addLast(now);                                          // the event enters at the new end
        while (!window.isEmpty() && window.peekFirst() <= now - span)   // stops at the first live entry
            window.pollFirst();                                       // each timestamp leaves once
        return window.size();                                         // the size is the count of live events
    }
}
```

#### Cost

- **CountWindow** costs O(1) time per call and O(k) space.
- **TimeWindow** spends O(1) time per call when averaged over the stream, since every timestamp is removed once, and uses O(w) space, where `w` is the largest number of events inside one window.

<!-- stage: applicability -->
### When A Window Fits

#### Recognizing The Pattern

Use this method when values arrive in order and the answer depends only on the last `k` values or on the events of a recent time range. The aggregate must be one that a removal can undo, such as a count or a sum. Before coding, state the stream kind, write the boundary rule as an inequality, and choose the unit of the clock. The invariant to keep is that the queue holds exactly the entries inside the window and the sum matches them. Evict before reading the answer, and never after.

A fixed-bucket array is a second way to hold a time window. It keeps one slot per time unit, and each slot stores the second it belongs to and a count. Its memory depends on `span` and not on the number of events. That helps when many events share one timestamp.

#### A False Friend

A running maximum looks like a running sum, and it is a false friend. When the oldest value leaves, the old maximum and the departing value do not give the new maximum. The second largest value was never stored. The same holds for a median. These aggregates need a different structure, such as a monotonic deque or a pair of heaps.

#### When The Method Does Not Apply

If timestamps can arrive out of order, the front of the queue is not the oldest entry and eviction stops too early. If the stream is correctable, the queue cannot find the old value to subtract. If a query asks about an arbitrary past time and not the latest time, one forward-moving window is not enough, and the entries need an index by time.

<!-- stage: exercises -->
### Exercises

#### [Build] Rolling Average Of Readings (LeetCode 346)
<!-- id: st38-moving-average -->

**Prerequisites.** The count window and the running sum from this lesson.

**Problem.** Design the class `MovingAverage` with a constructor that receives an integer `size`. The method `next(val)` appends `val` to the stream and returns the arithmetic mean of the last `size` values, or of all values when fewer than `size` have arrived. The class stores at most `size` values.

**Constraints.** The limits are:
- **Size** is from 1 to 10^4.
- **Values** are `int` values from -10^5 to 10^5.
- **Calls** number at most 10^4 per object.
- **Result** is the exact sum divided by the count, as a `double`.

**Example 1.** Input calls `["MovingAverage","next","next","next","next"]` with arguments `[[3],[5],[8],[2],[11]]`, output `[null,5.0,6.5,5.0,7.0]`.

**Example 2.** Input calls `["MovingAverage","next","next","next"]` with arguments `[[1],[4],[-2],[0]]`, output `[null,4.0,-2.0,0.0]`.

**Hint.** Which value leaves when the 4th value arrives, and what happens to the stored total when it leaves?

**Changed decision.** Basic case: the window length is a count, one `long` total replaces a re-sum of the tail, and a size of 1 makes every call replace the whole window.

#### [Vary] Recent Pings Within A Span (LeetCode 933)
<!-- id: st38-recent-calls -->

**Prerequisites.** The Rolling Average exercise above. This exercise changes the bound from a count of values to a length of time.

**Problem.** Design the class `RecentCounter` with a constructor that receives an integer `span`. The method `ping(t)` records a ping at time `t` and returns how many recorded pings have a time `u` with `t - span <= u <= t`. The count includes the new ping. The time `t` of each call is at least the time of the previous call.

**Constraints.** The limits are:
- **Span** is from 0 to 10^9.
- **Times** are `int` values from 0 to 10^9, and equal times are allowed.
- **Calls** number at most 10^4 per object.
- **Memory** holds only pings that can still count at the latest time.

**Example 1.** Input calls `["RecentCounter","ping","ping","ping","ping","ping","ping"]` with arguments `[[4],[1],[3],[5],[5],[9],[10]]`, output `[null,1,2,3,4,3,2]`.

**Example 2.** Input calls `["RecentCounter","ping","ping","ping"]` with arguments `[[0],[2],[2],[3]]`, output `[null,1,2,1]`.

**Hint.** Which comparison decides that the oldest ping has expired when both ends of the range count?

**Changed decision.** The bound is now time, so the number of pings inside the window varies. Eviction becomes a loop, and the inclusive range changes the comparison to `u < t - span`.

#### [Boundary] Large Sum Window (Author exercise)
<!-- id: st38-large-sum-window -->

**Prerequisites.** The Recent Pings exercise above. This exercise changes the aggregate from a count to a sum and enlarges the number range.

**Problem.** Design the class `TimedSum` with a constructor that receives a `long` named `span`. The method `record(time, value)` stores an event. The method `total(now)` returns the sum of the values of recorded events with `now - span <= time <= now`. Both ends of the range count. The `time` and `now` arguments of all calls, taken together in call order, never decrease.

**Constraints.** The limits are:
- **Span and times** are `long` values from 0 to 4 * 10^18.
- **Values** are `long` values from -10^12 to 10^12, and 0 is allowed.
- **Calls** number at most 10^5 per object.
- **Clock** is always an argument, and the class never reads a system clock.

**Example 1.** Input calls `["TimedSum","record","record","total","total"]` with arguments `[[10],[5,100],[15,-30],[15],[16]]`, output `[null,null,null,70,-30]`.

**Example 2.** Input calls `["TimedSum","record","record","total","total"]` with arguments `[[4000000000000000000],[0,5000000000000],[4000000000000000000,5000000000000],[4000000000000000000],[4000000000000000001]]`, output `[null,null,null,10000000000000,5000000000000]`.

**Hint.** Which side of the comparison can overflow if the program writes `time + span`, and which rewriting avoids it?

**Changed decision.** Both ends are inclusive, a query alone can expire entries, the total needs `long`, and the cutoff `now - span` is computed instead of `time + span`.

#### [Recognize] Hit Counter With Two Designs (LeetCode 362)
<!-- id: st38-hit-counter -->

**Prerequisites.** The Large Sum Window exercise above. This exercise has the lesson's half-open range and asks for two designs.

**Problem.** Design the class `HitCounter` with a constructor that receives an integer `span`. The method `hit(t)` records one hit at second `t`. The method `count(t)` returns the number of recorded hits with `t - span < u <= t`. Implement the class twice, once with a queue of hit entries and once with a fixed array of `span` slots, and show that both give equal answers.

**Constraints.** The limits are:
- **Span** is from 1 to 3600.
- **Times** are `int` values from 1 to 10^9 and never decrease across calls.
- **Hits** may share one second, and up to 10^5 hits may arrive in one second.
- **Calls** number at most 10^5 per object.

**Example 1.** Input calls `["HitCounter","hit","hit","hit","count","hit","count","count","count"]` with arguments `[[5],[1],[2],[2],[4],[7],[7],[11],[12]]`, output `[null,null,null,null,3,null,1,1,0]`.

**Example 2.** Input calls `["HitCounter","hit","count","count","count","hit","hit","count","count"]` with arguments `[[3],[4],[4],[6],[7],[7],[7],[9],[10]]`, output `[null,null,1,1,0,null,null,2,0]`.

**Hint.** In the slot design, how does a slot know that its stored count belongs to an old second and must be ignored?

**Changed decision.** The range is half-open, many hits can share one second, and the design choice changes memory from the number of live hits to the number of time units.
