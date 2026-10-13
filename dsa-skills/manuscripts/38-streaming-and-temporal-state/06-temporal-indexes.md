<!-- lesson-kind: standard -->
<!-- lesson-id: temporal-indexes -->
## Temporal Indexes

<!-- stage: context -->
### Why A Date Search Misses A Day

A support engineer opens the log viewer and searches for errors from `2024-03-01` to `2024-03-05`. The viewer stores each line with a full timestamp such as `2024-03-05 14:02:11`. It compares the stored text with the two search strings. The text `2024-03-05 14:02:11` sorts after `2024-03-05`, so every line from the last day falls outside the answer. The engineer sees four days of errors and closes the ticket while the incident is still running.

A second tool from the same team draws a chart of requests per second. It allocates one counter for every second between the two chart ends. A one-year chart needs about 31 million counters for every series, and the service runs out of memory when ten series are open. Both failures have one cause. The events had no agreed rule for where a query range ends, and no way to jump to the matching events. This lesson asks how to store each event once and answer questions about time ranges, granularity and empty stretches of time.

The stream in this lesson is append-only. Events arrive with non-decreasing timestamps, and nothing is corrected or expires afterward. Later parts mention what changes when arrivals come in any order.

<!-- stage: naive -->
### Scanning Every Event For Every Query

The direct design keeps all event times in an array and answers each question with a full scan. A query for a time range counts the events that lie between two times. A query for counts per interval allocates one counter for every interval of fixed length between the two ends and adds each event to its counter.

```java
final class NaiveEventLog {
    private long[] times = new long[16];
    private int n;

    void append(long t) {
        if (n == times.length) times = java.util.Arrays.copyOf(times, n * 2);
        times[n++] = t;
    }

    int countBetween(long from, long to) {          // both ends inclusive
        int c = 0;
        for (int i = 0; i < n; i++)                 // visits every stored event
            if (times[i] >= from && times[i] <= to) c++;
        return c;
    }

    int[] countsPerInterval(long from, long to, long size) {
        int[] counts = new int[(int) ((to - from) / size + 1)];   // one counter for every interval
        for (int i = 0; i < n; i++)                 // visits every stored event again
            if (times[i] >= from && times[i] <= to)
                counts[(int) ((times[i] - from) / size)]++;
        return counts;
    }
}
```

With events at times 2, 2, 9, 31, 33 and 58, the call `countsPerInterval(0, 59, 10)` returns `{3, 0, 0, 2, 0, 1}`, and `countBetween(9, 33)` returns 4. Both answers are correct.

```predict
A caller appends 3 events and then calls countsPerInterval(0, 1000000000000L, 1). What happens, and which counters hold a nonzero value?

The cast of 10^12 + 1 to int produces a negative number, so the array allocation throws NegativeArraySizeException. If the span were smaller, such as 3 * 10^9 intervals, the cast would still be wrong, and a span of 10^9 would ask for 4 GB of counters. At most 3 counters could ever be nonzero. The method spends all of its memory on counters that stay at zero.
```

<!-- stage: bottleneck -->
### Cost That Ignores The Query

#### Work Per Call Depends On The Whole Stream

Each query visits all `n` stored events, even when the matching events are a handful. With `q` queries the total cost is O(n * q). A dashboard that refreshes 50 panels every second over a log of 10^8 events performs 5 * 10^9 comparisons per second to read a few thousand events. The events are already in time order. Every event before the range and every event after it can be ruled out without a comparison.

#### Memory Depends On The Span Of Time

The counters array has one entry for each interval between the two ends. If the span is `S` and the interval length is `w`, the method uses O(S / w) memory and O(S / w + n) time, whatever the number of events. A quiet week at one-second resolution needs 604800 counters for a few hundred events. A sparse series can hold 3 events and still span 10^12 time units.

#### What A Correct Design Needs

A better design must satisfy three conditions. It must jump to the first matching event in O(log n) time and stop at the first event after the range. It must group events into intervals while it walks only over events, so empty intervals cost nothing. It must define, in one place, whether a range includes its ends, because that single choice decided the missing day in the log viewer.

<!-- stage: insight -->
### Order Plus A Fixed Boundary Rule

#### Events Live In A Sorted Index

<!-- names: sorted index, prefix key, bucket, half-open range -->

A **sorted index** is a structure that keeps the stored events in timestamp order and can find the first event at or after any time by binary search. For an append-only stream with non-decreasing arrivals, a plain growable array is a sorted index, because each append goes at the end and keeps the order. The search costs O(log n). Everything between two search results is a contiguous run of the array, so a range count is a subtraction of two positions.

When events arrive in any order, an array can no longer append in O(1). A balanced tree map keeps the same search cost at O(log n) per insert, and its range view plays the role of the array slice.

#### A Half-Open Range Settles The Ends

A **half-open range** `[a, b)` includes `a` and excludes `b`. Two such ranges that share an end never share an event, and the length of `[a, b)` is exactly `b - a`. The search for the first event at or after `a` and the search for the first event at or after `b` mark the two ends of the answer. A query with an inclusive end `[a, b]` converts to `[a, b + 1)` for integer timestamps. The conversion happens once, at the entry of the method. This conversion is the fix for the missing day in the log viewer.

#### Buckets And Prefix Keys Group Events

A **bucket** is the set of timestamps that map to the same integer `(t - from) / size` for a query that starts at `from` with interval length `size`. Bucket `b` covers the half-open range `[from + b * size, from + (b + 1) * size)`. Because the index is sorted, all events of one bucket sit next to each other. The walk counts one bucket and then moves to the next event with a larger bucket number. Buckets with no events are never visited, so a gap in time costs nothing.

A **prefix key** is the leading part of a fixed-width timestamp text, such as the first 10 characters of `2021:05:07:09:30:15`, which name the day. When every field has a fixed number of digits, text order equals time order. Cutting both query ends to the same prefix length selects a granularity, and an inclusive comparison of prefixes then matches every event inside the chosen day, hour or minute.

The invariant of a temporal index is that timestamp order and bucket meaning agree with one stated boundary rule. Every event then belongs to exactly one bucket and one search position.

<!-- stage: variables -->
### State Of The Index And The Query

The index and one query share these quantities, and the traces below follow them.

- **times** is the `long` array of event timestamps in non-decreasing order.
- **n** is the number of stored events, so valid positions run from 0 to `n - 1`.
- **lo** and **hi** are the ends of the binary-search window, and the answer position lies between them.
- **from**, **to** and **size** are the query ends and the bucket width, with `from <= to` and `size >= 1`.
- **b** is the bucket number of the event under the pointer, computed as `(times[i] - from) / size`.
- **i** is the position of the event the walk is looking at, from `lowerBound(from)` up to `n`.

The invariant for the search is that every position below `lo` holds a time smaller than the target. Every position at or after `hi` holds a time at least as large.

<!-- stage: trace -->
### Tracing A Search And A Bucket Walk

#### Two Binary Searches Mark A Range

The first trace stores the times 3, 3, 8, 14, 15, 15, 27 and 40, and asks for the events in `[8, 28)`. The search for 8 starts with the window `[0, 8)`. The middle position 4 holds 15, which is at least 8, so `hi` moves to 4. Position 2 holds 8, so `hi` moves to 2. Position 1 holds 3, which is below 8, so `lo` moves to 2 and the window closes at position 2. The second search, for 28, closes at position 7, because 27 sits at position 6 and 40 sits at position 7. The count is 7 minus 2, which is 5. The pointer `mid` shows which position each step compares, and the value -1 means that no comparison is running.

```trace
{"cells":[3,3,8,14,15,15,27,40],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":8,"mid":-1},"vars":{"target":8,"result":"open"},"note":"Start of query [8, 28): search the first index whose time is at least 8. The window is [0, 8)."},{"at":{"lo":0,"hi":4,"mid":4},"vars":{"target":8,"result":"open"},"note":"a[4] is 15, at least 8, so hi moves to 4."},{"at":{"lo":0,"hi":2,"mid":2},"vars":{"target":8,"result":"open"},"note":"a[2] is 8, at least 8, so hi moves to 2."},{"at":{"lo":2,"hi":2,"mid":1},"vars":{"target":8,"result":"first = 2"},"note":"a[1] is 3, below 8, so lo moves to 2."},{"at":{"lo":0,"hi":8,"mid":-1},"vars":{"target":28,"result":"open"},"note":"End of query [8, 28): search the first index whose time is at least 28. The window is [0, 8)."},{"at":{"lo":5,"hi":8,"mid":4},"vars":{"target":28,"result":"open"},"note":"a[4] is 15, below 28, so lo moves to 5."},{"at":{"lo":7,"hi":8,"mid":6},"vars":{"target":28,"result":"open"},"note":"a[6] is 27, below 28, so lo moves to 7."},{"at":{"lo":7,"hi":7,"mid":7},"vars":{"target":28,"result":"stop = 7"},"note":"a[7] is 40, at least 28, so hi moves to 7."},{"at":{"lo":2,"hi":7,"mid":-1},"vars":{"target":"none","result":"count = 5"},"note":"The events at indexes 2 through 6 lie inside [8, 28), so the count is 7 minus 2, which is 5."}]}
```

#### A Walk Skips Empty Buckets

The second trace stores the times 2, 2, 9, 31, 33 and 58, and asks for counts with width 10 over the inclusive range 0 to 59. That range holds 6 buckets. One search finds the first event at or after 0. The walk then takes the events 2, 2 and 9, which all have bucket number 0, and records the pair of bucket start 0 and count 3. The next event, 31, has bucket number 3, so the walk jumps over buckets 1 and 2 without touching them. Events 31 and 33 form the pair 30 and 2. The event 58 forms the pair 50 and 1. The result lists only three pairs, and the three missing buckets have count 0 by definition.

```trace
{"cells":[2,2,9,31,33,58],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"bucket":"none","nonEmpty":"[]"},"note":"Binary search places i on the first event at or after time 0. The query has 6 buckets of width 10."},{"at":{"i":3},"vars":{"bucket":0,"nonEmpty":"[0:3]"},"note":"Events 0 through 2 share bucket 0, which starts at 0. The walk records 3 and jumps to index 3."},{"at":{"i":5},"vars":{"bucket":3,"nonEmpty":"[0:3,30:2]"},"note":"Events 3 through 4 share bucket 3, which starts at 30. The walk records 2 and jumps to index 5."},{"at":{"i":6},"vars":{"bucket":5,"nonEmpty":"[0:3,30:2,50:1]"},"note":"Events 5 through 5 share bucket 5, which starts at 50. The walk records 1 and jumps to index 6."},{"at":{"i":6},"vars":{"bucket":"none","nonEmpty":"[0:3,30:2,50:1]"},"note":"The walk touched 3 buckets and no empty one. Buckets 1, 2 and 4 are absent from the list, so each of them has count 0."}]}
```

<!-- stage: code -->
### A Sorted Array With A Boundary Rule

#### The Index And Its Search

The class keeps the array and the size. The search method returns the first position whose time is at least the target, and the range count uses two such positions. The method `countBetween` takes an inclusive end and converts it once.

```java
final class TimeIndex {
    private long[] times = new long[16];
    private int n;

    void append(long t) {
        if (n > 0 && t < times[n - 1]) throw new IllegalArgumentException("arrivals must not go backward");  // keeps the array sorted
        if (n == times.length) times = java.util.Arrays.copyOf(times, n * 2);                                 // amortized O(1) growth
        times[n++] = t;
    }

    private int lowerBound(long target) {
        int lo = 0, hi = n;                          // window [lo, hi) holds the answer position
        while (lo < hi) {                            // each pass halves the window, O(log n) passes
            int mid = (lo + hi) >>> 1;
            if (times[mid] < target) lo = mid + 1;   // everything up to mid is too early
            else hi = mid;                           // mid could be the answer
        }
        return lo;
    }

    int countBetween(long from, long to) {           // inclusive ends, to < Long.MAX_VALUE
        return lowerBound(to + 1) - lowerBound(from);   // half-open [from, to + 1), a subtraction of two positions
    }
}
```

#### The Bucket Walk

The walk starts at the first event of the query. It reads the bucket number of the current event, advances over every event with the same number, and records one pair. Pairs are stored as the bucket start and the count, and only nonempty buckets appear. The method takes the sorted array and its length, so it repeats the same binary search inline.

```java
final class BucketWalk {
    static java.util.List<long[]> nonEmpty(long[] times, int n, long from, long to, long size) {
        java.util.List<long[]> out = new java.util.ArrayList<>();
        int lo = 0, hi = n;                                         // binary search for the first event at or after from
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (times[mid] < from) lo = mid + 1; else hi = mid;
        }
        int i = lo;                                                 // first event inside the query
        while (i < n && times[i] <= to) {                           // stops at the first event after the query
            long b = (times[i] - from) / size;                      // bucket number of this event
            int start = i;
            while (i < n && times[i] <= to && (times[i] - from) / size == b) i++;   // same bucket, same pair
            out.add(new long[]{from + b * size, i - start});        // bucket start and its count
        }
        return out;                                                 // empty buckets are absent, so their count is 0
    }
}
```

#### Cutting A Timestamp To A Granularity

For fixed-width text, the granularity is a prefix length. The two query ends are cut to the same length and compared inclusively with each stored text cut to that length.

```java
final class PrefixKeys {
    static String prefixKey(String timestamp, int digits) {
        return timestamp.substring(0, digits);       // fixed width, so text order equals time order
    }
}
```

#### Cost

- **append** costs O(1) amortized time and O(1) extra space per event.
- **countBetween** costs O(log n) time and O(1) extra space.
- **nonEmptyBuckets** costs O(log n + m) time, where `m` is the number of events inside the query, and O(k) space for the `k` nonempty buckets it returns.

<!-- stage: applicability -->
### When To Index By Time

#### Recognizing The Pattern

Use a temporal index when events are stored once and later read by a time range, a granularity or an interval grid. Phrases such as "between two times", "per minute", "every hour" and "inclusive" in a requirement point to it. Before coding, state whether the stream is append-only, correctable or expiring, and write the one boundary rule in a comment next to the entry method. The invariant to protect is that timestamp order and bucket meaning agree with that rule, so a range query and a bucket query on the same data never disagree.

#### A False Friend

A hash map keyed by the raw timestamp is a false friend of the sorted index. It answers "how many events at exactly time 90" in O(1). It cannot answer a range, because a hash has no order and a range scan visits every key. A fixed array with one counter for every possible interval is a second false friend. It passes small tests and fails on a sparse series that spans a long time.

#### When The Method Does Not Apply

If events expire, change or disappear, a plain sorted array no longer shows the current state. The earlier lessons of this chapter on expiring state and on corrected values apply first. If timestamp text has variable width, such as `2021:5:7` next to `2021:05:07`, text order and time order differ, and the text must be parsed into numbers before it is indexed. If the interval length changes from query to query and the query ends are always the stream ends, a running prefix total may be simpler than any index.

<!-- stage: exercises -->
### Exercises

#### [Build] Log Storage System (LeetCode 635)
<!-- id: st38-log-storage-system -->

**Prerequisites.** The prefix key and the sorted index from this lesson. This exercise reads the granularity from a text argument and selects events by a prefix comparison.

**Problem.** Design the class `LogStore`. The method `store(id, timestamp)` saves a log with an integer id and a timestamp text of the form `YYYY:MM:DD:hh:mm:ss`. The method `retrieve(start, end, unit)` takes two timestamp texts and a unit, which is one of `Year`, `Month`, `Day`, `Hour`, `Minute` or `Second`. It returns the ids of all stored logs whose timestamp, cut to the unit, lies between `start` and `end` cut to the unit, both ends included. The ids come back in ascending order.

**Constraints.** The limits are:
- **Calls** number at most 500 per object.
- **Ids** are distinct integers from 1 to 500.
- **Timestamps** have fixed width, with years from 2000 to 2099, and may repeat across logs.
- **Order** of `start` and `end` is guaranteed so that `start` is not later than `end`.

**Example 1.** Input calls `["LogStore","store","store","store","store","retrieve","retrieve"]` with arguments `[[],[1,"2021:05:07:09:30:15"],[2,"2021:05:07:23:59:59"],[3,"2021:05:08:00:00:00"],[4,"2021:06:01:12:00:00"],["2021:05:07:12:00:00","2021:05:08:00:00:00","Day"],["2021:05:07:12:00:00","2021:05:08:00:00:00","Hour"]]`, output `[null,null,null,null,null,[1,2,3],[2,3]]`.

**Example 2.** Input calls `["LogStore","store","store","store","retrieve","retrieve"]` with arguments `[[],[7,"2019:12:31:23:59:59"],[8,"2020:01:01:00:00:00"],[9,"2020:01:01:00:00:01"],["2019:01:01:00:00:00","2020:01:01:00:00:00","Year"],["2020:01:01:00:00:00","2020:01:01:00:00:00","Second"]]`, output `[null,null,null,null,[7,8,9],[8]]`.

**Hint.** What does the pair of cut texts `2021:05:07` and `2021:05:08` select, and why does the original start text `2021:05:07:12:00:00` not matter for the unit `Day`?

**Changed decision.** The query end is no longer a time but a prefix. Both ends are cut to the unit first, and then the comparison is inclusive on the cut texts, which is the rule that fixes the log viewer failure.

#### [Vary] Tweet Counts Per Frequency (LeetCode 1348)
<!-- id: st38-count-per-interval -->

**Prerequisites.** The Log Storage System exercise above. This exercise keeps one sorted index for each key and turns a time range into a list of bucket counts.

**Problem.** Design the class `ReadingCounter`. The method `record(sensor, time)` stores one reading of a named sensor at an integer second `time`. The method `counts(sensor, unit, from, to)` takes `unit` equal to `minute`, `hour` or `day`, with widths 60, 3600 and 86400 seconds. It returns a list in which entry `b` counts the readings of that sensor with time in `[from + b * width, from + (b + 1) * width)`. The last bucket ends at `to` and may be shorter. The list has exactly `(to - from) / width + 1` entries.

**Constraints.** The limits are:
- **Calls** number at most 10^4 per object.
- **Times** are `long` values from 0 to 10^12, and readings may arrive in any order.
- **Range** satisfies `from <= to` and `to - from <= 10^7`.
- **Sensor** names have 1 to 10 lowercase letters, and an unknown sensor gives a list of zeros.

**Example 1.** Input calls `["ReadingCounter","record","record","record","record","record","record","counts","counts"]` with arguments `[[],["a",10],["a",70],["a",75],["a",130],["a",3700],["a",3700],["a","minute",10,200],["a","hour",0,7200]]`, output `[null,null,null,null,null,null,null,[1,2,1,0],[4,2,0]]`.

**Example 2.** Input calls `["ReadingCounter","record","record","record","counts","counts","counts"]` with arguments `[[],["b",5],["b",5],["b",120],["b","minute",0,119],["b","minute",0,120],["c","day",0,0]]`, output `[null,null,null,null,[2,0],[2,0,1],[0]]`.

**Hint.** Which tree view returns the readings of one sensor inside a time range, and how does the bucket number of each reading find its slot in the answer list?

**Changed decision.** Arrivals come in any order, so the array becomes a sorted map from time to count. The answer list is dense and has one entry for every bucket, and its length is limited by the constraint on the range.

#### [Boundary] Sparse Empty Buckets (Author exercise)
<!-- id: st38-sparse-empty-buckets -->

**Prerequisites.** The Tweet Counts Per Frequency exercise above. This exercise changes the output so that empty buckets are never listed, and the range can be too long to list.

**Problem.** Design the class `SparseSeries`. The method `record(time)` appends one event, and times never decrease from call to call. Bucket `b` of the inclusive range `[from, to]` starts at `from + b * size`. The method `nonEmpty(from, to, size)` returns a pair `{start, count}` for each bucket that holds an event, in ascending order of `start`. The method `countAt(from, to, size, index)` returns the count of bucket `index` counted from 0, and it returns 0 for an empty bucket. It returns -1 when `index` is not a bucket of the range. The last bucket ends at `to`.

**Constraints.** The limits are:
- **Calls** number at most 10^4 per object.
- **Times and ends** are `long` values from 0 to 10^15, with `from <= to`.
- **Size** is a `long` from 1 to 10^15.
- **Index** is a `long` from 0 to 10^15.
- **Memory** must not depend on the number of buckets in the range.

**Example 1.** Input calls `["SparseSeries","record","record","record","record","record","record","nonEmpty","countAt","countAt","countAt"]` with arguments `[[],[2],[2],[9],[31],[33],[58],[0,59,10],[0,59,10,1],[0,59,10,5],[0,59,10,6]]`, output `[null,null,null,null,null,null,null,[[0,3],[30,2],[50,1]],0,1,-1]`.

**Example 2.** Input calls `["SparseSeries","record","record","nonEmpty","countAt","countAt"]` with arguments `[[],[0],[1000000000000000],[0,1000000000000000,7],[0,1000000000000000,7,142857142857142],[0,1000000000000000,7,142857142857143]]`, output `[null,null,null,[[0,1],[999999999999994,1]],1,-1]`. The last bucket starts at 999999999999994 and holds the event at 10^15.

**Hint.** How many buckets does the second example have, and which type holds that number? Which two binary searches count the events of one bucket?

**Changed decision.** The answer is no longer a dense list. The walk visits events and never buckets, and every number that involves a bucket count, an index or a start uses `long` arithmetic.

#### [Recognize] Design Exam Scores Tracker (LeetCode 3709)
<!-- id: st38-exam-scores-tracker -->

**Prerequisites.** The Sparse Empty Buckets exercise above. Here every query is a time range, and a running total replaces the walk.

**Problem.** Design the class `ScoreLedger`. The method `add(time, score)` stores one exam result, and the times of successive calls strictly increase. The method `total(from, to)` returns the sum of the scores with a time in the inclusive range `[from, to]`. It returns 0 when `from > to` or when no result lies inside the range.

**Constraints.** The limits are:
- **Calls** number at most 10^5 per object.
- **Times** are `long` values from 1 to 10^9, strictly increasing across `add` calls.
- **Scores** are `int` values from 1 to 10^9.
- **Sums** can exceed `Integer.MAX_VALUE`, so the return type is `long`.

**Example 1.** Input calls `["ScoreLedger","add","add","add","total","total","total"]` with arguments `[[],[5,900000000],[8,800000000],[20,700000000],[5,20],[6,19],[9,10]]`, output `[null,null,null,null,2400000000,800000000,0]`.

**Example 2.** Input calls `["ScoreLedger","add","add","total","total","total"]` with arguments `[[],[3,10],[4,20],[4,3],[1,1000000000],[3,3]]`, output `[null,null,null,0,30,10]`.

**Hint.** Which array holds the sum of all scores up to each position, and which two positions does a range need?

**Changed decision.** Each result carries a value, so a count by subtraction of positions becomes a sum by subtraction of running totals. The index is still a sorted array, but the second array of `long` totals answers every range in O(log n).
