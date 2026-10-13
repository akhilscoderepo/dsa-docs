<!-- lesson-kind: standard -->
<!-- lesson-id: frequency-streams -->
## Frequency Streams

<!-- stage: context -->
### Why A Dashboard Lags Behind Its Data

A support team watches a dashboard that shows the first error code that has appeared exactly once since the last deploy. Each incoming log line carries one code. The dashboard service stores every code in a list and rescans the whole list whenever someone opens the page. During a quiet hour this is instant. During an outage the list grows by thousands of lines per second, and the page that should help the team takes longer to load than the outage takes to change. The numbers on screen describe the system as it was a minute ago.

A second service has the opposite flaw. It tracks how many users have performed exactly three failed logins, so it can flag them. It keeps a map from each user to a login count and a separate figure for how many users have three. When a user's record is deleted, the map shrinks but the separate figure does not, and the page flags a user who no longer exists. Both services answer questions about multiplicity. How many times has a value appeared? Is any value present exactly `f` times? Which value is still unique? Were the last `k` inputs all the same? This lesson asks how to answer such questions after every update without rereading the stream and without letting two pieces of bookkeeping disagree.

The stream matters before the structure does. A stream is **append-only** when values only arrive, **correctable** when earlier arrivals can be withdrawn, and **expiring** when values leave on their own after a time. The first three problems in this lesson are append-only. The tracker in the third is correctable. No problem here expires, because expiry is the topic of other lessons in this chapter.

<!-- stage: naive -->
### Keep Every Value And Recount

The direct design stores each arriving value in a list. A query rebuilds the multiplicities from scratch with a hash map and then answers from the result. The class below supports `add`, a check whether any value occurs exactly `f` times, and a lookup of the first value that occurs once.

```java
final class RecountingLog {
    private final java.util.ArrayList<Integer> seen = new java.util.ArrayList<>();

    void add(int v) { seen.add(v); }

    boolean hasFrequency(int f) {
        java.util.HashMap<Integer, Integer> counts = new java.util.HashMap<>();
        for (int v : seen) counts.merge(v, 1, Integer::sum);     // recounts the whole history
        for (int c : counts.values()) if (c == f) return true;   // scans every distinct value
        return false;
    }

    int firstOnce() {
        java.util.HashMap<Integer, Integer> counts = new java.util.HashMap<>();
        for (int v : seen) counts.merge(v, 1, Integer::sum);     // recounts again
        for (int v : seen) if (counts.get(v) == 1) return v;     // walks in arrival order
        return -1;                                               // nothing is unique
    }
}
```

After the values `4, 7, 4`, the call `hasFrequency(2)` returns `true` and `firstOnce()` returns 7. Both answers are correct, and for a short stream the class is fast enough.

```predict
A monitor adds 100000 values to this log and calls hasFrequency after every single add. Roughly how many hash-map insertions happen in total, and what changes if the caller asks only once at the end?

The call after the k-th add rebuilds a map from k stored values, so the total is 1 + 2 + ... + 100000, which is about 5 * 10^9 insertions. The program spends almost all of its time repeating work it already did on the previous call. If the caller asks once at the end, the cost is only 100000 insertions and the design is fine. The cost depends on how often the question is asked, and an online interface asks after every update.
```

<!-- stage: bottleneck -->
### Every Query Repeats The Whole Count

Each query of the log costs O(n) time for a history of `n` values, and it also keeps O(n) memory for the list. A stream of `n` updates with a query after each one therefore costs O(n^2) time. For `n` near 10^5 this is about 5 * 10^9 hash-map operations, which is far beyond a time limit. The memory grows without bound too, since the list keeps every value even after the answer no longer depends on its position.

The repeated work is visible in the code. The multiplicity of one value changes by exactly 1 when one update arrives, yet the query rebuilds the multiplicity of every value. The set of answers changes by at most two entries per update: one value leaves its old frequency and enters a new one. A design that stores the counts and moves only those two entries answers each update in constant time.

A second cost hides in the first-unique query. The scan walks the list from the front each time, so a front that has stayed non-unique for a long time is rechecked on every call. A correct design needs three properties. Each update touches a bounded number of entries. Every stored summary agrees with the counts after every update, including the update that brings a count to zero. Anything that the design keeps without a guarantee is checked before it is shown to the caller.

<!-- stage: insight -->
### Counts Plus A Second Map

#### One Map Is The Source Of Truth

<!-- names: tally, candidate, stale, streak -->

A map from value to its current count is the only place that stores how often a value occurs. Every other structure either summarizes it or is checked against it. When the map says a value has count 0, the entry is removed, so the key set of the map equals the set of values that are present.

#### A Tally Summarizes The Counts

Questions of the form "is any value present exactly `f` times" ask about counts and not about values. A **tally** is a second map from a count `c` to the number of values whose count is `c`. When a value moves from count `c` to count `c + 1`, the update subtracts 1 from `tally[c]` and adds 1 to `tally[c + 1]`. The query then reads `tally[f] > 0` in constant time. The two maps agree when every update changes both, and the zero count is the case that breaks agreement. A value whose count is 0 is not present, so no `tally[0]` entry exists. The update skips the increment when the new count is 0 and skips the decrement when the old count is 0.

#### A Queue May Hold Stale Entries

For first-unique queries the design keeps a queue of values in arrival order, a **candidate** being any value in the queue that could be the answer. A value enters the queue once, when its count first becomes 1. Later arrivals of the same value raise its count and leave the queue alone, so the queue now holds a **stale** entry, a value whose count is no longer 1. Removing that entry from the middle of the queue would cost O(n). The design leaves it there. Before the query exposes the front, it compares the front's count with 1 and pops while the front is stale. Each entry is popped at most once, so the pops are paid for by the pushes.

#### A Streak Replaces The Stream

Some questions need no history. "Are the last `k` values all equal to a target" depends only on the **streak**, the number of consecutive target values at the end of the stream. A matching value adds 1 to the streak and any other value sets it to 0. One integer replaces a window of `k` values.

The invariant of this lesson is that a container may hold stale values only when a count check filters them before the caller sees them. The maps never hold stale data, the queue may, and the streak is always exact.

<!-- stage: variables -->
### State Kept By Each Structure

The lesson builds one tracker class and one run recognizer. The trace follows the state of the first and the queue of the second.

- **counts** maps a value to its current number of occurrences, and it holds no entry with count 0.
- **tally** maps a count to the number of values that currently have it, and it holds no entry for count 0.
- **order** is the queue of values in the order their count first reached 1.
- **target** and **k** are the fixed value and the length that the run recognizer compares against.
- **streak** is the number of consecutive target values at the end of the input, and it is a `long` because the stream can be long.

The invariant is that `tally[c]` equals the number of values with `counts[v] == c` for every `c >= 1`, and every value whose count is 1 appears in `order`.

<!-- stage: trace -->
### Tracing Updates And Queries

#### The Tracker With Corrections

The first trace applies nine operations to the counts and the tally. The pointer `op` marks the operation just applied. After `add 4`, `add 7` and `add 4`, the map holds `4:2` and `7:1`, so the tally holds `1:1` and `2:1`. The query `has 2` reads `tally[2]`, finds 1 and answers `true`. The operation `del 4` lowers the count of 4 from 2 to 1, so the tally moves one entry from 2 to 1 and `tally[2]` disappears. The next `has 2` answers `false`. The operation `del 7` takes the count of 7 from 1 to 0, so the map removes the key. The tally loses its entry for 1 and gains no entry for 0. The second `del 7` finds no key and changes nothing. The final `has 1` answers `true` because the value 4 still has count 1.

```trace
{"cells":["add 4","add 7","add 4","has 2","del 4","has 2","del 7","del 7","has 1"],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"counts":"empty","tally":"empty","answer":"none"},"note":"Start: both maps are empty."},{"at":{"op":0},"vars":{"counts":"4:1","tally":"1:1","answer":"none"},"note":"add 4 moves its count from 0 to 1 in both maps."},{"at":{"op":1},"vars":{"counts":"4:1 7:1","tally":"1:2","answer":"none"},"note":"add 7 moves its count from 0 to 1 in both maps."},{"at":{"op":2},"vars":{"counts":"4:2 7:1","tally":"1:1 2:1","answer":"none"},"note":"add 4 moves its count from 1 to 2 in both maps."},{"at":{"op":3},"vars":{"counts":"4:2 7:1","tally":"1:1 2:1","answer":"true"},"note":"has 2 reads tally[2], which is 1, so the answer is true."},{"at":{"op":4},"vars":{"counts":"4:1 7:1","tally":"1:2","answer":"none"},"note":"del 4 moves its count from 2 to 1 in both maps."},{"at":{"op":5},"vars":{"counts":"4:1 7:1","tally":"1:2","answer":"false"},"note":"has 2 reads tally[2], which is 0, so the answer is false."},{"at":{"op":6},"vars":{"counts":"4:1","tally":"1:1","answer":"none"},"note":"del 7 moves its count from 1 to 0 and removes the key, with no tally entry for 0."},{"at":{"op":7},"vars":{"counts":"4:1","tally":"1:1","answer":"none"},"note":"del 7 finds no key, so nothing changes."},{"at":{"op":8},"vars":{"counts":"4:1","tally":"1:1","answer":"true"},"note":"has 1 reads tally[1], which is 1, so the answer is true."}]}
```

#### First Unique With A Lazy Queue

The second trace feeds values to the queue `order`. The pointer `op` marks the operation just applied. Adding 5 and 3 pushes both. The second `add 5` raises the count of 5 to 2 and pushes nothing, so the front of the queue, 5, is now stale. The query `first` sees count 2 at the front, pops 5, then sees count 1 at 3 and returns it. After `add 2` and `add 3`, the front 3 is stale again, and the next `first` pops it and returns 2. When `add 2` follows, the query pops 2 and finds an empty queue, so the answer is -1. Every pop happens inside a query, and no entry is ever searched for in the middle of the queue.

```trace
{"cells":["add 5","add 3","add 5","first","add 2","add 3","first","add 2","first","add 7","first"],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"order":"empty","answer":"none"},"note":"Start: the queue is empty."},{"at":{"op":0},"vars":{"order":"5","answer":"none"},"note":"add 5 gives count 1, so 5 enters the queue."},{"at":{"op":1},"vars":{"order":"5 3","answer":"none"},"note":"add 3 gives count 1, so 3 enters the queue."},{"at":{"op":2},"vars":{"order":"5 3","answer":"none"},"note":"add 5 raises its count to 2 and pushes nothing, so 5 in the queue is now stale."},{"at":{"op":3},"vars":{"order":"3","answer":"3"},"note":"first pops stale 5 and returns 3."},{"at":{"op":4},"vars":{"order":"3 2","answer":"none"},"note":"add 2 gives count 1, so 2 enters the queue."},{"at":{"op":5},"vars":{"order":"3 2","answer":"none"},"note":"add 3 raises its count to 2 and pushes nothing, so 3 in the queue is now stale."},{"at":{"op":6},"vars":{"order":"2","answer":"2"},"note":"first pops stale 3 and returns 2."},{"at":{"op":7},"vars":{"order":"2","answer":"none"},"note":"add 2 raises its count to 2 and pushes nothing, so 2 in the queue is now stale."},{"at":{"op":8},"vars":{"order":"empty","answer":"-1"},"note":"first pops stale 2, finds an empty queue and returns -1."},{"at":{"op":9},"vars":{"order":"7","answer":"none"},"note":"add 7 gives count 1, so 7 enters the queue."},{"at":{"op":10},"vars":{"order":"7","answer":"7"},"note":"first finds the front 7 with count 1 and returns it."}]}
```

<!-- stage: code -->
### Three Small Classes With Defined Updates

#### The Tracker With Counts And Tally

The `shift` method is the only place that changes a count, so the two maps cannot disagree. It receives the old and new count of one value.

```java
final class FrequencyBook {
    private final java.util.HashMap<Long, Integer> counts = new java.util.HashMap<>();
    private final java.util.HashMap<Integer, Integer> tally = new java.util.HashMap<>();

    private void shift(long v, int from, int to) {
        if (from > 0 && tally.merge(from, -1, Integer::sum) == 0)
            tally.remove(from);                                // the value leaves its old count, an empty bucket is dropped
        if (to > 0) tally.merge(to, 1, Integer::sum);          // the value joins its new count
        if (to == 0) counts.remove(v); else counts.put(v, to); // zero means absent
    }

    void add(long v) { int c = counts.getOrDefault(v, 0); shift(v, c, c + 1); }

    void removeOne(long v) { int c = counts.getOrDefault(v, 0); if (c > 0) shift(v, c, c - 1); }

    boolean hasFrequency(int f) { return tally.getOrDefault(f, 0) > 0; }   // constant-time read
}
```

#### The First Unique Reader

The reader pushes a value only when its count first becomes 1, and the query removes stale entries from the front.

```java
final class UniqueReader {
    private final java.util.HashMap<Integer, Integer> counts = new java.util.HashMap<>();
    private final java.util.ArrayDeque<Integer> order = new java.util.ArrayDeque<>();

    void add(int v) {
        int c = counts.merge(v, 1, Integer::sum);   // authoritative count
        if (c == 1) order.addLast(v);               // enters the queue once
    }

    int first() {
        while (!order.isEmpty() && counts.get(order.peekFirst()) != 1)
            order.pollFirst();                      // each stale front is popped once
        return order.isEmpty() ? -1 : order.peekFirst();
    }
}
```

#### The Suffix Run Counter

The counter stores no values, only the length of the current matching suffix.

```java
final class RunCounter {
    private final int target;
    private final long k;
    private long streak;

    RunCounter(int target, long k) { this.target = target; this.k = k; }

    boolean push(int x) {
        streak = (x == target) ? streak + 1 : 0;   // one comparison decides the whole state
        return streak >= k;                        // true when the last k are all target
    }
}
```

#### Cost

- **FrequencyBook** costs O(1) expected time per call and O(d) space for `d` distinct values.
- **UniqueReader** costs O(1) amortized time per call, because each value is pushed once and popped at most once, and O(d) space.
- **RunCounter** costs O(1) time per call and O(1) space.

<!-- stage: applicability -->
### When To Track Counts Online

#### Recognizing The Pattern

Use this method when each update changes the multiplicity of one value and the queries ask about multiplicities, uniqueness or a run of equal values. Before choosing structures, write whether the stream is append-only, correctable or expiring. A correctable stream needs the tally to move in both directions. An append-only stream may skip the downward move. Name the summary of every count you keep, and decide what each update does at count 0. The invariant to keep is that a stale container entry is rejected by a count check before the caller sees it.

#### A False Friend

A frequency map alone is a false friend of "is any value present exactly `f` times". It answers how often one value occurs but forces a scan of all values to answer the question about `f`. A second false friend is a sorted structure of counts, which looks natural for ranking questions and costs O(log d) per update when a constant-time map suffices. A third is a queue that removes a duplicate from the middle on every arrival, which turns an amortized O(1) design into O(n).

#### When The Method Does Not Apply

If values expire after a time, a count that only rises or falls by explicit updates is wrong, because counts must also fall when time passes. Use the time-based methods of the neighboring lessons. If the query asks for the k-th most frequent value or for a rank, a tally of counts is not enough and an ordered structure is required. If the queue of candidates would need removal from the middle for correctness and not only for speed, the lazy check is also not enough.

<!-- stage: exercises -->
### Exercises

#### [Build] Pair Sum Lookup (LeetCode 170)
<!-- id: st38-pair-sum-lookup -->

**Prerequisites.** The count map and the append-only definition from this lesson.

**Problem.** Design the class `PairSumStore`. The method `add(x)` appends the integer `x` to a multiset. The method `find(target)` returns `true` when two different stored elements, counted by position of arrival, have the sum `target`. An element may not pair with itself, but two equal values stored at different positions may pair.

**Constraints.** The limits are:
- **Values** are `int` values from -10^9 to 10^9.
- **Target** is a `long` value from -4 * 10^9 to 4 * 10^9.
- **Calls** number at most 10^4 per object, and `find` may be called on an empty store.
- **Stream** is append-only, so no call removes a stored value.

**Example 1.** Input calls `["PairSumStore","add","add","add","find","find","find","find"]` with arguments `[[],[3],[7],[3],[6],[10],[14],[9]]`, output `[null,null,null,null,true,true,false,false]`.

**Example 2.** Input calls `["PairSumStore","add","find","add","find","add","find"]` with arguments `[[],[-5],[-10],[-5],[-10],[2000000000],[1999999995]]`, output `[null,null,false,null,true,null,true]`.

**Hint.** When the partner of `x` equals `x` itself, which extra fact about the count of `x` must hold?

**Changed decision.** Basic case: the map stores counts and not positions, and the target is a `long` so that the partner `target - x` never overflows.

#### [Vary] First Unique Reader (LeetCode 1429)
<!-- id: st38-first-unique-reader -->

**Prerequisites.** The Pair Sum Lookup exercise above. This exercise changes the question from a pair to the arrival order of values that occur once.

**Problem.** Design the class `UniqueReader` with a constructor that receives an initial `int[]`. The method `append(v)` adds `v` to the end of the stream. The method `first()` returns the earliest-arriving value that occurs exactly once in the whole stream so far, or -1 when none exists. The method `uniqueCount()` returns the number of values that currently occur exactly once.

**Constraints.** The limits are:
- **Values** are `int` values from 0 to 10^9, so -1 is never a stream value.
- **Initial** length is from 0 to 10^5.
- **Calls** number at most 10^5 per object.
- **Cost** per call must not depend on the length of the stream.

**Example 1.** Input calls `["UniqueReader","first","append","first","append","first","uniqueCount","append","first"]` with arguments `[[[7,7,4]],[],[4],[],[9],[],[],[9],[]]`, output `[null,4,null,-1,null,9,1,null,-1]`.

**Example 2.** Input calls `["UniqueReader","first","append","uniqueCount","append","uniqueCount","first"]` with arguments `[[[]],[],[6],[],[6],[],[]]`, output `[null,-1,null,1,null,0,-1]`.

**Hint.** What does the queue hold after a value arrives a second time, and who removes that entry?

**Changed decision.** The queue gains entries on first arrival only and loses them lazily at the front. A new counter, `uniqueCount`, moves when a value goes from 1 to 2.

#### [Boundary] Count Of Counts (LeetCode 2671)
<!-- id: st38-count-of-counts -->

**Prerequisites.** The Pair Sum Lookup and First Unique Reader exercises above. This exercise is a transfer prompt: the stream is correctable, so the tally must also move downward.

**Problem.** Design the class `FrequencyTracker`. The method `add(x)` stores one more copy of `x`. The method `removeOne(x)` removes one copy of `x` and does nothing when `x` is absent. The method `removeAll(x)` removes every copy of `x`. The method `hasFrequency(f)` returns `true` when some value is stored exactly `f` times.

**Constraints.** The limits are:
- **Values** are `int` values from 0 to 10^9.
- **Frequency** `f` satisfies `1 <= f <= 10^5`, so no query asks about count 0.
- **Calls** number at most 10^5 per object.
- **Removal** of an absent value changes no state.

**Example 1.** Input calls `["FrequencyTracker","add","add","add","hasFrequency","removeOne","hasFrequency","hasFrequency","removeAll","hasFrequency","hasFrequency"]` with arguments `[[],[5],[5],[8],[2],[5],[2],[1],[8],[1],[2]]`, output `[null,null,null,null,true,null,false,true,null,true,false]`.

**Example 2.** Input calls `["FrequencyTracker","removeOne","hasFrequency","add","add","add","removeAll","hasFrequency","hasFrequency"]` with arguments `[[],[4],[1],[4],[4],[4],[4],[3],[1]]`, output `[null,null,false,null,null,null,null,false,false]`.

**Hint.** When a count reaches 0, which of the two maps must lose an entry and which must receive none?

**Changed decision.** A count of zero is the boundary. The tally entry for the old count shrinks and no entry for count 0 appears. The new `removeAll` moves a value across many counts in one call.

#### [Recognize] Suffix Run Counter (LeetCode 2526)
<!-- id: st38-suffix-run-counter -->

**Prerequisites.** The state list of this lesson. This exercise is a transfer prompt: the stream needs one integer, not a stored window.

**Problem.** Design the class `SuffixRun` with a constructor that receives an `int` named `target` and a `long` named `k`. The method `push(x)` appends `x` to the stream and returns `true` when at least `k` values have been pushed and the last `k` are all equal to `target`. The method `currentRun()` returns the number of consecutive values equal to `target` at the end of the stream.

**Constraints.** The limits are:
- **Values** and `target` are `int` values from 0 to 10^9.
- **Length** `k` is a `long` from 1 to 10^12.
- **Calls** number at most 10^5 per object.
- **Memory** must not depend on `k` or on the number of calls.

**Example 1.** Input calls `["SuffixRun","push","push","push","push","push","push","push"]` with arguments `[[6,3],[6],[6],[2],[6],[6],[6],[6]]`, output `[null,false,false,false,false,false,true,true]`.

**Example 2.** Input calls `["SuffixRun","push","push","push","currentRun"]` with arguments `[[0,1],[0],[5],[0],[]]`, output `[null,true,false,true,1]`.

**Hint.** Which single number must change when a non-matching value arrives, and does it ever need to know the earlier values?

**Changed decision.** The summary of the stream is one integer that either grows by 1 or resets to 0. Memory is O(1) whatever `k` is.
