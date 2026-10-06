<!-- lesson-kind: combination -->
<!-- lesson-id: reuse-meeting-rooms -->
## Reuse Meeting Rooms With A Heap

<!-- stage: context -->
### Why The Booking Tool Counts Extra Rooms

A booking tool for an office receives a day of meeting requests and must report how many rooms the office needs. The first version counts every pair of requests whose times overlap and adds one room for each overlapping pair. Take the requests 1 to 10, 2 to 3 and 4 to 5. Two pairs overlap, so the tool reports three rooms. The office can host all three meetings in two rooms, because the short meetings share the second room one after the other.

The tool also treats a meeting that ends at 3 and a meeting that starts at 3 inconsistently. Some reports call them a conflict, and others do not. This lesson asks how a program decides which room each meeting uses, and how it settles what a shared endpoint means.

<!-- stage: contributions -->
### What Sorting And The Queue Each Add

Two earlier ideas combine here. Sorting by start time, from the intervals chapter, supplies the order. Meetings reach the program one by one, and every meeting that could have blocked a room has already arrived. After sorting, a program never needs to look ahead for a meeting that starts earlier than the current one.

The priority queue from this chapter supplies the question that sorting cannot answer. Among all rooms in use, which one becomes free first? The queue holds one end time for each room in use, and its root is the earliest end time. Sorting alone gives no cheap way to find that room, and the queue alone has no order of arrival. Together they decide, for each meeting, whether an existing room is free or a new room is needed.

<!-- stage: naive -->
### Scanning Every Room For Each Meeting

The direct plan sorts the meetings by start time and keeps a list with the end time of the last meeting in each room. For each meeting, it scans the list for a room whose last meeting has ended.

```java
static int roomsByScan(int[][] meetings) {
    int[][] sorted = meetings.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    List<Integer> roomEnd = new ArrayList<>();              // end time of the last meeting in each room
    for (int[] m : sorted) {
        int free = -1;
        for (int r = 0; r < roomEnd.size(); r++) {
            if (roomEnd.get(r) <= m[0]) { free = r; break; } // the first room that has ended before this start
        }
        if (free == -1) roomEnd.add(m[1]);                   // no room is free, so open a new one
        else roomEnd.set(free, m[1]);
    }
    return roomEnd.size();
}
```

The method returns the correct room count for half-open meetings, where a meeting ending at 4 and a meeting starting at 4 can share a room.

<!-- stage: bottleneck -->
### Counting Room Checks

```predict
A day has n = 100,000 meetings that all overlap one another, so each needs its own room. How many room checks does the scan method make?

The i-th meeting scans all i - 1 existing rooms and finds none free, so the total is about n * n / 2 = 5 * 10^9 checks. That is O(n^2), and each scan rereads rooms whose end times did not change.
```

The scan costs O(n) per meeting in the worst case, so the whole day costs O(n^2). The scan also answers a question that is too large. The program needs to know only whether the room that frees up first has already ended. If the earliest-ending room has not ended, no other room has either. If it has ended, the program may use it, and it does not matter which ended room it is.

The program needs the smallest end time among the rooms in use, and it needs to replace that end time with a new one. That is exactly what a queue provides.

<!-- stage: insight -->
### Keeping The Earliest Finish At The Root

The program sorts the meetings by start time. It keeps a `PriorityQueue<Integer>` of end times, one for each **active meeting**, which is a meeting that holds a room at the current start time. The root holds the **earliest finish**, the smallest end time among the rooms in use.

#### Deciding Between Reuse And A New Room

For each meeting `[s, e]`, the program compares `s` with the earliest finish. If that end time is at most `s`, the room is free. The program removes that end time, so the meeting takes over the room. Otherwise every room is busy, and the program leaves the queue unchanged. In both cases the program then offers `e`.

The test `earliest finish <= s` is the **reuse rule** for half-open meetings, which include the start and exclude the end. A meeting that ends at 4 and one that starts at 4 share a room. For closed meetings, where both endpoints belong to the meeting, the rule changes to `earliest finish < s`, because a shared endpoint is a conflict.

#### Reading The Answer

A reuse step removes one end time and adds one, so the queue size stays the same. A new room adds one end time and grows the size. The queue size at the end therefore equals the largest number of meetings that were active at once, which is the number of rooms. The program costs O(n log n), with the sort and the queue operations each costing O(n log n) in total.

<!-- names: earliest finish, active meeting, reuse rule -->

<!-- stage: variables -->
### The State Of The Room Planner

The planner keeps three pieces of state.

- **Sorted meetings** are the requests ordered by start time, and the loop reads them once from left to right.
- **End times queue** holds one end time per room in use, and its size is the number of rooms opened so far.
- **Touching flag** says whether a shared endpoint is a conflict, and it decides between the test `<=` and the test `<`.

The queue size only grows when no room is free. It never shrinks during the scan, so the final size is the answer.

<!-- stage: trace -->
### Planning Rooms For Two Days

#### Sharing A Room At A Shared Endpoint

Take the half-open meetings 1 to 4, 2 to 5, 4 to 6 and 5 to 7. In the first trace the cells hold the start times, and the pointer `next` marks the meeting just placed. The variable `ends` lists the end times in the queue.

The first meeting opens a room with end time 4. The second meeting starts at 2, before the earliest finish 4, so it opens a second room. The third meeting starts at 4, and the earliest finish is 4, so it reuses that room, and the queue becomes 5 and 6. The fourth meeting starts at 5 and reuses the room that ends at 5. The planner needs two rooms in total.

#### Treating Shared Endpoints As Conflicts

The second trace uses the closed intervals 1 to 3, 3 to 5 and 6 to 8. The interval 3 to 5 shares the point 3 with 1 to 3. The earliest finish 3 is not smaller than the start 3, so the room is not reused. The interval 6 to 8 starts after both ends 3 and 5, and it reuses the room of the earliest finish 3. The answer is two groups.

#### Stepping Through Both Plans

```trace
{"cells":[1,2,4,5],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"ends":"[4]","rooms":1},"note":"No room exists, so the program opens the first room. The end times are [4]."},{"at":{"next":1},"vars":{"ends":"[4, 5]","rooms":2},"note":"The earliest finish 4 is after the start 2, so every room is busy and the program opens a new room. The end times are [4, 5]."},{"at":{"next":2},"vars":{"ends":"[5, 6]","rooms":2},"note":"The earliest finish 4 is at most the start 4, so the meeting takes over that room. The end times are [5, 6]."},{"at":{"next":3},"vars":{"ends":"[6, 7]","rooms":2},"note":"The earliest finish 5 is at most the start 5, so the meeting takes over that room. The end times are [6, 7]."}]}
```

```trace
{"cells":[1,3,6],"pointers":["next"],"steps":[{"at":{"next":0},"vars":{"ends":"[3]","rooms":1},"note":"No room exists, so the program opens the first room. The end times are [3]."},{"at":{"next":1},"vars":{"ends":"[3, 5]","rooms":2},"note":"The earliest finish 3 is not smaller than the start 3, so every room is busy and the program opens a new room. The end times are [3, 5]."},{"at":{"next":2},"vars":{"ends":"[5, 8]","rooms":2},"note":"The earliest finish 3 is smaller than the start 6, so the meeting takes over that room. The end times are [5, 8]."}]}
```

<!-- stage: code -->
### Planning Rooms In Java

#### One Method For Both Endpoint Rules

The parameter `touchingOverlaps` selects the strict test for closed meetings.

```java
static int roomsNeeded(int[][] meetings, boolean touchingOverlaps) {
    int[][] sorted = meetings.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));      // order by start time
    PriorityQueue<Integer> ends = new PriorityQueue<>();             // end time of each room in use
    for (int[] m : sorted) {
        boolean reusable = !ends.isEmpty()
            && (touchingOverlaps ? ends.peek() < m[0] : ends.peek() <= m[0]);  // the reuse rule
        if (reusable) ends.poll();                                   // the meeting takes over that room
        ends.offer(m[1]);                                            // this room is busy until the new end time
    }
    return ends.size();                                              // rooms opened equals the peak of active meetings
}
```

#### Cost Of The Planner

The sort costs O(n log n). The loop makes one poll at most and one offer for each meeting, so it costs O(n log n) too. The queue holds at most one end time per room, so the memory is O(n) in the worst case.

<!-- stage: applicability -->
### Recognizing A Room Reuse Question

#### Spotting The Pattern

The cue is intervals that compete for a limited resource, with a question about how many resources are needed or whether one is free. The invariant is that each active meeting owns one end time in the queue, so the root tells whether any room is free. After that comparison the program never rescans the rooms.

#### Finding The False Friend

The false friend is the pairwise check. After sorting by start time, comparing each meeting only with its neighbor answers whether any two meetings overlap, which is enough for a yes or no question. It does not count rooms. A long meeting can overlap several later meetings that do not overlap one another.

Counting overlapping pairs fails for the same reason, as the opening example showed.

#### Recognizing The No-Go Cases

The heap is not needed when the question only asks whether a conflict exists. A sort and a neighbor check cost O(n log n) with no queue. The room count also has a second route. Sorting the starts and the ends separately and walking both lists gives the same count without a queue. That route does not say which room each meeting uses.

<!-- stage: exercises -->
### Exercises

#### [Build] Meeting Rooms (LeetCode 252)
<!-- id: hp-meeting-rooms -->

**Prerequisites.** The sorting rule of this lesson and the half-open meaning of an interval.

**Problem.** Given an array `intervals`, each `[start, end]` is a half-open meeting that includes `start` and excludes `end`. Return true when one person can attend every meeting. Two meetings conflict when their time ranges share a point. A meeting that ends at 4 and one that starts at 4 do not conflict.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Endpoints** satisfy `0 <= start < end <= 10^9`.
- **Mutation** does not occur; `intervals` keeps its order.

**Example 1.** Input `intervals = [[8,10],[2,4],[4,8]]`, output true.

**Example 2.** Input `intervals = [[1,5],[4,6]]`, output false.

**Hint.** After sorting by start, which pair of meetings is enough to compare? What does an end time equal to the next start mean here?

**Changed decision.** The check compares only sorted neighbors, and a shared endpoint is allowed.

#### [Vary] Meeting Rooms II (LeetCode 253)
<!-- id: hp-meeting-rooms-two -->

**Prerequisites.** The previous exercise and the earliest finish from this lesson.

**Problem.** Given an array `intervals` of half-open meetings `[start, end)`, return the minimum number of rooms. Two meetings that share a point must use different rooms. A meeting that ends at 4 and one that starts at 4 may share a room.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Endpoints** satisfy `0 <= start < end <= 10^9`.
- **Mutation** does not occur; `intervals` keeps its order.

**Example 1.** Input `intervals = [[1,4],[2,5],[4,6],[5,7]]`, output 2.

**Example 2.** Input `intervals = [[3,9]]`, output 1.

**Hint.** Which end time does the program compare with each new start? What happens to the queue size when a room is reused?

**Changed decision.** The queue replaces the earliest finish when a room is reused and grows when none is free.

#### [Boundary] Divide Intervals Into Minimum Number of Groups (LeetCode 2406)
<!-- id: hp-divide-intervals-groups -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `intervals` of closed intervals `[left, right]`, divide them into groups. No two intervals in one group may share a point. Minimize the number of groups. Two closed intervals that share an endpoint share a point. Return the minimum number of groups.

**Constraints.** The limits are:
- **Length** is `1 <= intervals.length <= 10^5`.
- **Endpoints** satisfy `1 <= left <= right <= 10^6`.
- **Closed** means both endpoints belong to the interval.
- **Mutation** does not occur; `intervals` keeps its order.

**Example 1.** Input `intervals = [[1,3],[3,5],[6,8]]`, output 2.

**Example 2.** Input `intervals = [[2,2]]`, output 1.

**Hint.** Which test, `<` or `<=`, decides that a group is free for a closed interval? What changes if two intervals touch at one point?

**Changed decision.** The reuse rule becomes strict, so an end time equal to the next start does not free the group.

#### [Recognize] Minimum Interval to Include Each Query (LeetCode 1851)
<!-- id: hp-minimum-interval-query -->

**Prerequisites.** All three exercises above and the delayed deletion lesson.

**Problem.** Given closed intervals `[left, right]` with size `right - left + 1`, and an array `queries`, return one answer per query `q`. The answer is the size of the smallest interval with `left <= q <= right`, or -1 when no interval contains `q`. Answer the queries in increasing order of value, add intervals by start, and expire them by end.

**Constraints.** The limits are:
- **Intervals** number `1 <= intervals.length <= 10^5`, with `1 <= left <= right <= 10^7`.
- **Queries** number `1 <= queries.length <= 10^5`, with `1 <= queries[j] <= 10^7`.
- **Answer** has one entry per query in the original query order.

**Example 1.** Input `intervals = [[2,5],[3,4],[7,9]]` and `queries = [3,5,8,10]`, output `[2,4,3,-1]`.

**Example 2.** Input `intervals = [[1,1]]` and `queries = [1,2]`, output `[1,-1]`.

**Hint.** Which intervals can contain the current query? What must the program discard from the root before it reads the smallest size?

**Changed decision.** The queue orders intervals by size, and entries whose right end lies before the query leave when they reach the root.
