<!-- lesson-kind: standard -->
<!-- lesson-id: interval-scheduling -->
## Interval Scheduling

<!-- stage: context -->
### Why A Booking System Rejects Short Requests

A conference room accepts booking requests that each name a start time and an end time. One request asks for the room from 0 to 10. Three other requests ask for 1 to 2, 3 to 4 and 5 to 6. The room can hold only one meeting at a time.

A system that accepts the first request it sees books the long meeting and rejects the other three. A system that rejects the long meeting books three meetings in the same hours. The question of this lesson is which request a program should accept next, so that the number of accepted meetings is as large as possible.

<!-- stage: naive -->
### Accepting Requests By Start Time

The direct plan sorts the requests by start time. It walks them in that order and accepts a request whenever it does not overlap the last accepted one. Each request is a half-open interval `[start, end)`, so a request that starts exactly when the last one ends does not overlap it.

```java
static int acceptByStart(int[][] meetings) {
    int[][] byStart = meetings.clone();
    Arrays.sort(byStart, (a, b) -> Integer.compare(a[0], b[0]));
    int accepted = 0;
    int lastEnd = Integer.MIN_VALUE;
    for (int[] m : byStart) {
        if (m[0] >= lastEnd) {          // no overlap with the last accepted request
            accepted++;
            lastEnd = m[1];
        }
    }
    return accepted;
}
```

```predict
Run the method on the requests `[0,10)`, `[1,2)`, `[3,4)` and `[5,6)`. What does it return, and is that the most meetings the room can hold?

It returns 1. The request `[0,10)` starts first, so the method accepts it, and the other three all start before time 10, so each overlaps it. The room can hold 3 meetings if it books `[1,2)`, `[3,4)` and `[5,6)`.
```

<!-- stage: bottleneck -->
### Counting What Early Starts Cost

The method sorts once and scans once, so it runs in O(n log n) time. The cost is fine. The answer is wrong, because the order it uses does not track the quantity that limits later choices.

A request that starts early can still end very late. Accepting it moves the end of the last accepted request to a late time, and every later request that starts before that time is lost. The count of lost requests can grow as large as `n - 1`, as the example shows. The program needs an order in which accepting the next request costs the least possible room for the requests that follow.

<!-- stage: insight -->
### Keeping The Room Free Early

#### Sorting By End Time

The **earliest end rule** sorts the requests by end time, and the algorithm accepts a request whenever it does not overlap the last accepted one. After each acceptance the room is busy only until that end time. A smaller end time leaves a larger part of the day open.

#### Why The Rule Is Safe

Compare any two requests that do not overlap the last accepted one. Let `a` end no later than `b`. Take a best schedule that begins with `b`. Replace `b` with `a`. Request `a` ends no later than `b`, so every request that followed `b` in the schedule still starts after `a` ends. The replacement keeps the schedule valid and keeps its size.

Applied again to the rest of the day, this swap shows that the request with the earliest end is the first member of some best schedule. The accepted requests form a **compatible set**, a group in which no two requests overlap. The argument shows that the set built by the rule is as large as any other compatible set.

#### Free Time After A Choice

The quantity that the rule protects is the **free time after** the last accepted request. A schedule that ends earlier has at least as much free time, because every later request that fits after the later end also fits after the earlier end. Start times do not measure this quantity. Only the end of the last accepted request does.

<!-- names: earliest end rule, compatible set, free time after -->

<!-- stage: variables -->
### What The Scan Tracks

After the sort, the scan needs one number and one count. Four items describe the state.

- **meetings** is the array of intervals `[start, end)`, sorted by end time.
- **lastEnd** is the end of the most recently accepted interval, and it starts below every start.
- **accepted** is the number of accepted intervals.
- **i** is the index of the interval under test, and the scan accepts it when its start is at least `lastEnd`.

The comparison uses `>=` because the model is half-open. A different model changes this one operator, and the Boundary exercise below tests that.

<!-- stage: trace -->
### Two Scans In End Order

#### A Scan With Rejections

The first trace sorts five requests by end time: `[1,3)`, `[2,4)`, `[3,6)`, `[5,7)` and `[6,8)`. The pointer `i` marks the request under test.

The scan accepts `[1,3)` and sets `lastEnd` to 3. It rejects `[2,4)`, because 2 is below 3. It accepts `[3,6)`, because 3 equals `lastEnd`, and then rejects `[5,7)`. It accepts `[6,8)`. The scan accepts three requests.

```trace
{"cells":["1-3","2-4","3-6","5-7","6-8"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"lastEnd":3,"accepted":1},"note":"The request [1,3) starts at 1, which is not below lastEnd, so the scan accepts it and sets lastEnd to 3."},{"at":{"i":1},"vars":{"lastEnd":3,"accepted":1},"note":"The request [2,4) starts at 2, which is below lastEnd = 3, so the scan rejects it."},{"at":{"i":2},"vars":{"lastEnd":6,"accepted":2},"note":"The request [3,6) starts at 3, which is not below lastEnd, so the scan accepts it and sets lastEnd to 6."},{"at":{"i":3},"vars":{"lastEnd":6,"accepted":2},"note":"The request [5,7) starts at 5, which is below lastEnd = 6, so the scan rejects it."},{"at":{"i":4},"vars":{"lastEnd":8,"accepted":3},"note":"The request [6,8) starts at 6, which is not below lastEnd, so the scan accepts it and sets lastEnd to 8."}]}
```

#### The Long Request From The Start

The second trace uses the four requests from the opening: `[1,2)`, `[3,4)`, `[5,6)` and `[0,10)` in end order. The three short requests are accepted in turn, and the long request is rejected last because it starts at 0, before `lastEnd = 6`. The scan accepts three requests where the start-order method accepted one.

```trace
{"cells":["1-2","3-4","5-6","0-10"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"lastEnd":2,"accepted":1},"note":"The request [1,2) starts at 1, which is not below lastEnd, so the scan accepts it and sets lastEnd to 2."},{"at":{"i":1},"vars":{"lastEnd":4,"accepted":2},"note":"The request [3,4) starts at 3, which is not below lastEnd, so the scan accepts it and sets lastEnd to 4."},{"at":{"i":2},"vars":{"lastEnd":6,"accepted":3},"note":"The request [5,6) starts at 5, which is not below lastEnd, so the scan accepts it and sets lastEnd to 6."},{"at":{"i":3},"vars":{"lastEnd":6,"accepted":3},"note":"The request [0,10) starts at 0, which is below lastEnd = 6, so the scan rejects it."}]}
```

<!-- stage: code -->
### Counting Accepted Requests After Sorting By End

```java
static int maxMeetings(int[][] meetings) {
    int[][] byEnd = meetings.clone();
    Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));
    int accepted = 0;
    long lastEnd = Long.MIN_VALUE;
    for (int[] m : byEnd) {
        if (m[0] >= lastEnd) {
            accepted++;
            lastEnd = m[1];
        }
    }
    return accepted;
}
```

The method differs from the start-order version in one line, the comparator. The comparator uses `Integer.compare` and never subtracts, so extreme values do not overflow. The variable `lastEnd` is a `long` that starts at the smallest value, so the first interval is always accepted. The method clones the outer array so the caller keeps its order.

- **Time** is O(n log n) for the sort, and the scan adds O(n).
- **Space** is O(n) for the sorted copy of the references.

<!-- stage: applicability -->
### Recognizing Selection By Room Left

#### Applying The Invariant

Reach for this method when the goal is the largest set of items that cannot overlap, or the fewest points that touch every item. The invariant is that, after each acceptance, no other choice leaves more free time for the requests that remain. State the invariant first, then pick the sort key that makes it true.

#### Finding Cases That Break The Precondition

A false friend is sorting by start time. Start order suits merging, because a merge needs neighbors, and it fails here. Sorting by shortest length is a second false friend, and a later lesson of this chapter builds a counterexample. The method also assumes every request is worth the same. When requests carry different values, the question changes, and later chapters on dynamic programming handle it.

#### Avoiding Java Pitfalls

State the overlap model before coding. Half-open intervals use `m[0] >= lastEnd`, and closed intervals use `m[0] > lastEnd`. Compare with `Integer.compare`. Do not sort `int[][]` by `a[1] - b[1]`, because the subtraction overflows for large values.

<!-- stage: exercises -->
### Exercises

#### [Build] Choose Compatible Meetings (Author exercise)
<!-- id: gr-choose-compatible-meetings -->

**Prerequisites.** The end-order scan of this lesson.

**Problem.** Each meeting is a half-open interval `[start, end)` with `start < end`. Two meetings overlap when they share a moment, so `[1,2)` and `[2,3)` do not overlap. Return the largest number of meetings that no two overlap.

**Constraints.** The limits are:
- **Count** is `0 <= meetings.length <= 10^5`.
- **Values** are integers in `0 <= start < end <= 10^9`.
- **Ties** in end time may appear in any order.
- **Mutation** of the input is allowed.

**Example 1.** Input `meetings = [[1,3],[2,4],[3,6],[5,7],[6,8]]`, output 3.

**Example 2.** Input `meetings = [[0,10],[1,2],[3,4],[5,6]]`, output 3.

**Hint.** Which request leaves the most free time after it ends?

**Changed decision.** The method sorts by end time and counts accepted meetings.

#### [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gr-non-overlapping-intervals -->

**Prerequisites.** The previous exercise.

**Problem.** Each interval is half-open, `[start, end)`. Choose a largest set of intervals that no two overlap. Order the intervals by end time, and break ties by smaller position in the input. Keep an interval when it does not overlap the last kept one. Return the positions of the intervals that are not kept, in increasing order.

**Constraints.** The limits are:
- **Count** is `0 <= intervals.length <= 10^5`.
- **Values** are integers in `-5 * 10^4 <= start < end <= 5 * 10^4`.
- **Positions** start at 0 in the input order.
- **Mutation** does not occur; the input keeps its order.

**Example 1.** Input `intervals = [[1,2],[2,3],[3,4],[1,3]]`, output `[3]`.

**Example 2.** Input `intervals = [[1,2],[1,2],[1,2]]`, output `[1,2]`.

**Hint.** Sort positions, not intervals, so each removed interval keeps its original index.

**Changed decision.** The method returns the removed positions, not a count.

#### [Boundary] Touching Endpoint Contract (Author exercise)
<!-- id: gr-touching-endpoint-contract -->

**Prerequisites.** The first exercise.

**Problem.** Each interval is `[start, end]` in a model chosen by the flag `closed`. When `closed` is true, an interval includes both ends, so two intervals that share an endpoint overlap. When `closed` is false, an interval includes `start` and excludes `end`, so intervals that share an endpoint do not overlap. Return the largest number of intervals that no two overlap in the chosen model.

**Constraints.** The limits are:
- **Count** is `0 <= intervals.length <= 10^5`.
- **Values** are integers in `0 <= start <= end <= 10^9`, with `start < end` when `closed` is false.
- **Point intervals** with `start == end` appear only when `closed` is true.
- **Flag** `closed` is a boolean.

**Example 1.** Input `intervals = [[1,2],[2,3]]` and `closed = true`, output 1.

**Example 2.** Input `intervals = [[1,2],[2,3]]` and `closed = false`, output 2.

**Hint.** Which comparison operator changes between the two models?

**Changed decision.** The overlap test depends on a flag.

#### [Recognize] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gr-balloon-group-sizes -->

**Prerequisites.** The end-order scan and the closed model.

**Problem.** Each balloon spans the closed range `[start, end]`. An arrow at coordinate `x` bursts every unburst balloon with `start <= x <= end`. Place arrows one at a time. Each arrow goes at the smallest end among the unburst balloons. Return an array whose entry `k` is the number of balloons that the arrow number `k` bursts.

**Constraints.** The limits are:
- **Count** is `0 <= points.length <= 10^5`.
- **Values** are integers in `-2^31 <= start <= end <= 2^31 - 1`.
- **Order** of the input is arbitrary.
- **Return** is an empty array for empty input.

**Example 1.** Input `points = [[10,16],[2,8],[1,6],[7,12]]`, output `[2,2]`.

**Example 2.** Input `points = [[1,2],[3,4],[5,6]]`, output `[1,1,1]`.

**Hint.** After sorting by end, when does the current arrow stop reaching the next balloon?

**Changed decision.** The method reports group sizes, not the arrow count.
