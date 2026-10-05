<!-- lesson-kind: standard -->
<!-- lesson-id: event-sweep -->
## Count Active Intervals With Events

<!-- stage: context -->
### Peak Logins That Never Happened

A capacity report needs the peak number of users logged in at one moment. Each login session is a half-open time range, so session `[1,4)` ends before time 4 begins. The log holds `[1,4)` and `[4,6)`. A user leaves at time 4 and the next user arrives at time 4, so at no moment are two users logged in. The report says the peak is 2 and asks for another server.

The report is wrong because of how the code handled time 4. Two changes happen at the same coordinate, one departure and one arrival, and the code applied the arrival first. The numbers in the log are fine, and the order of two changes at one coordinate produced the error. The goal of this lesson is one answer. How does a scan count active intervals when several changes land on the same coordinate?

<!-- stage: naive -->
### Count The Sessions Around Every Start

The peak number of sessions occurs at some start time, because the count can only rise when a session begins. So the direct method visits each start time and counts the sessions that hold it, meaning the sessions with `start <= t < end`. It keeps the largest count.

```java
static int peakByCounting(int[][] sessions) {
    int best = 0;
    for (int[] a : sessions) {
        int t = a[0];
        int count = 0;
        for (int[] b : sessions) {
            if (b[0] <= t && t < b[1]) count++;
        }
        best = Math.max(best, count);
    }
    return best;
}
```

On `[1,4)` and `[4,6)` the method returns 1, which is correct. It reads the half-open rule directly in its condition, so it has no tie to get wrong.

<!-- stage: bottleneck -->
### Counting Pairs Again

```predict
Suppose you record only the times at which the count of active sessions changes, as a plus 1 for a start and a minus 1 for an end. What does the count do between two neighbouring change times, and where can the peak occur?

The count stays constant between changes, so the peak occurs right after some change. Sorting the 2n change times and adding up the changes in order gives every count in O(n log n) time.
```

The direct method tests every session against every start, which is `n * n` tests and so O(n^2). For `n = 100,000` that is 10 billion tests. The method counts again from scratch at each start. Yet the count at one start differs from the previous count by only a few starts and ends.

The change times carry all the information. A list of the `2n` changes, ordered by coordinate, lets one pass keep the count and update it by one at each change. The single difficulty is the order of changes that share a coordinate, which the opening report got wrong.

<!-- stage: insight -->
### Turn Intervals Into Ordered Events

An **event** is a pair of a coordinate and a change. A start is the event `(start, +1)` and an end is the event `(end, -1)`. Sorting the events by coordinate lets one pass keep the **running count**, the number of intervals that are active after the events processed so far.

#### Ties Follow The Contract

When events share a coordinate, the **tie policy** is the rule that orders them. It comes from the model for ends in the second lesson. A half-open interval `[a, b)` no longer holds `b`, so at coordinate `b` the end frees a place before a start at `b` takes one. The tie policy processes minus 1 before plus 1. A closed interval `[a, b]` still holds `b`, so a start at `b` meets the interval that ends at `b`. The tie policy processes plus 1 before minus 1.

<!-- names: event, running count, tie policy -->

#### Where The Peak Is Read

The peak is the largest running count after a start event. Under the half-open policy, all ends at a coordinate run first. The count after the last start at that coordinate is then the true number of active intervals there. Under the closed policy, all starts run first. The count after the last start still includes the intervals that end at that coordinate, as the closed model requires.

#### Empty Intervals Need A Guard

A half-open interval with `start == end` holds no coordinate. Its end event runs before its start event under the half-open policy, so the running count would dip below zero. The pass must skip such intervals, which is the same decision as treating `[x, x)` as empty in the second lesson.

<!-- stage: variables -->
### What The Sweep Keeps

The sweep keeps four pieces of state.

- **events** is an array of pairs `{coordinate, change}` with `2n` entries, sorted by coordinate and then by the tie policy.
- **active** is the running count, which equals the number of intervals that hold the current coordinate.
- **best** is the largest value of `active` seen after any start event.
- **e** is the index of the next event to process.

<!-- stage: trace -->
### Sweeping Under Two Tie Policies

#### Half-Open Intervals

Take the intervals `[1,4)`, `[4,6)`, `[2,5)` and `[5,7)`. The sorted events under the half-open policy are `(1,+1)`, `(2,+1)`, `(4,-1)`, `(4,+1)`, `(5,-1)`, `(5,+1)`, `(6,-1)` and `(7,-1)`. The cells of the trace are the coordinates of these events, and the pointer `e` marks the event being applied.

At coordinate 4 the end of `[1,4)` runs first and the start of `[4,6)` runs second. The count goes from 2 to 1 and back to 2. The peak is 2.

```trace
{"cells":[1,2,4,4,5,5,6,7],"pointers":["e"],"steps":[{"at":{"e":-1},"vars":{"active":0,"best":0},"note":"The events are sorted. The running count starts at 0."},{"at":{"e":0},"vars":{"change":"+1","active":1,"best":1},"note":"The start event at coordinate 1 changes the count by +1, so the count becomes 1."},{"at":{"e":1},"vars":{"change":"+1","active":2,"best":2},"note":"The start event at coordinate 2 changes the count by +1, so the count becomes 2."},{"at":{"e":2},"vars":{"change":"-1","active":1,"best":2},"note":"The end event at coordinate 4 changes the count by -1, so the count becomes 1."},{"at":{"e":3},"vars":{"change":"+1","active":2,"best":2},"note":"The start event at coordinate 4 changes the count by +1, so the count becomes 2."},{"at":{"e":4},"vars":{"change":"-1","active":1,"best":2},"note":"The end event at coordinate 5 changes the count by -1, so the count becomes 1."},{"at":{"e":5},"vars":{"change":"+1","active":2,"best":2},"note":"The start event at coordinate 5 changes the count by +1, so the count becomes 2."},{"at":{"e":6},"vars":{"change":"-1","active":1,"best":2},"note":"The end event at coordinate 6 changes the count by -1, so the count becomes 1."},{"at":{"e":7},"vars":{"change":"-1","active":0,"best":2},"note":"The end event at coordinate 7 changes the count by -1, so the count becomes 0."}]}
```

#### Closed Intervals

Now take the same four ranges as closed intervals `[1,4]`, `[4,6]`, `[2,5]` and `[5,7]`. Under the closed policy, the starts at a coordinate run before the ends. At coordinate 4 the start of `[4,6]` runs first, so the count rises to 3 before the end of `[1,4]` lowers it. Coordinate 4 truly lies in three closed intervals, so the peak is 3.

```trace
{"cells":[1,2,4,4,5,5,6,7],"pointers":["e"],"steps":[{"at":{"e":-1},"vars":{"active":0,"best":0},"note":"The events are sorted. The running count starts at 0."},{"at":{"e":0},"vars":{"change":"+1","active":1,"best":1},"note":"The start event at coordinate 1 changes the count by +1, so the count becomes 1."},{"at":{"e":1},"vars":{"change":"+1","active":2,"best":2},"note":"The start event at coordinate 2 changes the count by +1, so the count becomes 2."},{"at":{"e":2},"vars":{"change":"+1","active":3,"best":3},"note":"The start event at coordinate 4 changes the count by +1, so the count becomes 3."},{"at":{"e":3},"vars":{"change":"-1","active":2,"best":3},"note":"The end event at coordinate 4 changes the count by -1, so the count becomes 2."},{"at":{"e":4},"vars":{"change":"+1","active":3,"best":3},"note":"The start event at coordinate 5 changes the count by +1, so the count becomes 3."},{"at":{"e":5},"vars":{"change":"-1","active":2,"best":3},"note":"The end event at coordinate 5 changes the count by -1, so the count becomes 2."},{"at":{"e":6},"vars":{"change":"-1","active":1,"best":3},"note":"The end event at coordinate 6 changes the count by -1, so the count becomes 1."},{"at":{"e":7},"vars":{"change":"-1","active":0,"best":3},"note":"The end event at coordinate 7 changes the count by -1, so the count becomes 0."}]}
```

<!-- stage: code -->
### Writing The Sweep In Java

#### Build And Sort The Events

The method takes a flag for the model. The comparator sorts by coordinate. It then orders the changes by the tie policy, which is ascending change for half-open and descending change for closed.

```java
static int peakConcurrent(int[][] intervals, boolean closed) {
    List<int[]> events = new ArrayList<>();
    for (int[] iv : intervals) {
        if (!closed && iv[0] == iv[1]) continue;
        events.add(new int[] {iv[0], +1});
        events.add(new int[] {iv[1], -1});
    }
    events.sort((a, b) -> a[0] != b[0]
            ? Integer.compare(a[0], b[0])
            : (closed ? Integer.compare(b[1], a[1]) : Integer.compare(a[1], b[1])));
    int active = 0, best = 0;
    for (int[] e : events) {
        active += e[1];
        best = Math.max(best, active);
    }
    return best;
}
```

The method costs O(n log n) time for sorting `2n` events and O(n) space for the events. The maximum is read after every event, not only after starts. The two readings agree, because an end never raises the count.

<!-- stage: applicability -->
### When A Sweep Is The Right Tool

#### Count Versus Shape

The invariant of the sweep concerns `active`. Once all events at a coordinate have run in the order of the tie policy, `active` equals the number of intervals holding that coordinate. Use a sweep when the answer depends on how many intervals are active. Peak load, the first time a limit is reached and the coordinates where the count changes are examples. A sweep gives no merged geometry, so use the merge scan when the answer is the covered ranges.

#### Sorting Starts And Ends Apart Is A False Friend

Sorting the starts and the ends in two separate arrays, then walking both with two cursors, also finds a peak. It is a false friend for problems with several kinds of events or explicit ties. The order of a start and an end at one coordinate stays hidden in the cursor comparison. An explicit event list shows the tie policy in the comparator, where a reader can check it.

#### What The Sweep Cannot Answer

The sweep reports how many intervals are active, not which ones. A problem that asks which room or machine each interval uses needs the identity of the interval that ends next. Chapter 17 teaches the heap that provides it. A sweep also needs the model for ends before it starts. A wrong tie policy changes the answer at every touching pair.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Concurrent Half-Open Intervals (Author exercise)
<!-- id: iv-peak-half-open -->

**Prerequisites.** The half-open model from the second lesson.

**Problem.** Each session is a half-open interval `[start, end)` holding every integer time `t` with `start <= t < end`. Return the largest number of sessions that hold one common integer time. Process the end event before a start event at the same coordinate.

**Constraints.** The limits are:
- **Length** is `0 <= sessions.length <= 10^5`.
- **Values** are `int` values with `start < end`.
- **Return** is a single `int`, which is 0 for an empty input.
- **Mutation** is not allowed; the input array keeps its values.

**Example 1.** Input `[[1,4],[4,6],[2,5],[5,7]]`, output 2.

**Example 2.** Input `[[3,5],[5,8],[8,9]]`, output 1.

**Hint.** Write each session as a start event and an end event. What does the order of the two events at coordinate 4 decide?

**Changed decision.** Basic case: the end event runs before a start event at the same coordinate.

#### [Vary] Maximum Concurrent Closed Intervals (Author exercise)
<!-- id: iv-peak-closed -->

**Prerequisites.** The exercise above.

**Problem.** Each session is a closed interval `[start, end]` holding every integer time `t` with `start <= t <= end`. Find the largest number of sessions that share one integer time, and return that number. Intervals that touch at one coordinate hold that coordinate together.

**Constraints.** The limits are:
- **Length** is `0 <= sessions.length <= 10^5`.
- **Values** are `int` values with `start <= end`.
- **Return** is a single `int`.
- **Mutation** is not allowed; the input array keeps its values.

**Example 1.** Input `[[1,4],[4,6],[2,5],[5,7]]`, output 3.

**Example 2.** Input `[[3,5],[5,8],[8,9]]`, output 2.

**Hint.** The end coordinate is still held. Which event must run first at a shared coordinate so that both intervals count?

**Changed decision.** The tie policy reverses, and the start event runs before the end event at one coordinate.

#### [Boundary] Many Events At One Coordinate (Author exercise)
<!-- id: iv-events-one-coordinate -->

**Prerequisites.** The two exercises above.

**Problem.** Each session is a half-open interval `[start, end)`, and an interval with `start == end` is empty and holds no time. Return, for every coordinate where at least one event of a non-empty interval occurs, a pair `[coordinate, active]`. The value `active` is the number of intervals holding that coordinate once all events at that coordinate ran. List the pairs by increasing coordinate. The result must not depend on the order of the input.

**Constraints.** The limits are:
- **Length** is `0 <= sessions.length <= 10^5`.
- **Values** are `int` values with `start <= end`.
- **Ties** can involve up to `10^5` events at one coordinate.
- **Return** is an `int[][]`, empty when no interval is non-empty.

**Example 1.** Input `[[1,4],[4,6],[4,9]]`, output `[[1,1],[4,2],[6,1],[9,0]]`.

**Example 2.** Input `[[5,5],[5,8]]`, output `[[5,1],[8,0]]`.

**Hint.** What would the count do at coordinate 5 if the empty interval's end ran before its own start? How does skipping it fix that?

**Changed decision.** The scan reports a value only after the whole group at a coordinate ran, and empty intervals are skipped.

#### [Recognize] First Coordinate Reaching Capacity (Author exercise)
<!-- id: iv-first-capacity -->

**Prerequisites.** All three exercises above.

**Problem.** Each session is a half-open interval `[start, end)`. Given a capacity `k`, return the smallest integer coordinate at which at least `k` sessions hold it, or -1 if no coordinate has `k` sessions.

**Constraints.** The limits are:
- **Length** is `0 <= sessions.length <= 10^5`.
- **Values** are `int` values with `0 <= start < end <= 10^9`.
- **Capacity** satisfies `1 <= k <= 10^5`.
- **Return** is a single `int`, and the input is not modified.

**Example 1.** Input `[[1,5],[2,6],[4,8]]` and `k = 3`, output 4.

**Example 2.** Input `[[1,3],[3,5]]` and `k = 2`, output -1.

**Hint.** The count first reaches `k` right after some start event. Which coordinate does that event carry?

**Changed decision.** The sweep stops at the first event that makes the count reach `k`, and no peak is stored.
