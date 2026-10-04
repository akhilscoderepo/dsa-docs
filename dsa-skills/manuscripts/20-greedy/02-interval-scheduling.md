<!-- lesson-kind: standard -->
<!-- lesson-id: interval-scheduling -->
## Interval Scheduling

<!-- stage: context -->
### The Booking Desk Of Linden Hall

Linden Hall has one big room and a booking desk that receives requests for it, each with a start time and an end time. Two events cannot share the room at the same moment, and the hall's manager wants to hold as many events as the calendar allows. Requests differ wildly in length. A choir wants the whole day, a book club wants an hour, and a wedding wants the evening.

The clerk has a pile of requests in no particular order. She can accept any of them, but each acceptance knocks out every request that overlaps it, so one wrong yes can cost several later events. She wants a rule for walking through the pile that she can trust without rewriting the calendar.

<!-- stage: naive -->
### Try Each Request In Or Out

The direct method lists the requests by start time and, for each one, branches into two worlds, one where the request is held and one where it is declined. It remembers the time at which the room last became empty, and a request can be held only if it begins at or after that time.

```java
static int mostEvents(int[][] req, int i, int roomEmptyAt) {
    if (i == req.length) return 0;
    int best = mostEvents(req, i + 1, roomEmptyAt);                 // decline request i
    if (req[i][0] >= roomEmptyAt)                                   // request i fits
        best = Math.max(best, 1 + mostEvents(req, i + 1, req[i][1]));
    return best;
}
```

The call assumes the requests are sorted by start, and it answers correctly for every input because both worlds are explored. With ten requests it finishes at once.

<!-- stage: bottleneck -->
### Two Branches At Every Request

Each request opens two branches, so the search makes up to O(2^n) calls. Fifty requests already produce more calls than anyone can wait for. Most of the work is redundant. Hundreds of branches arrive at the same request with the same time for the room becoming empty, and each of them solves the remaining list again from scratch.

A closer look shows what really matters in a branch. The only fact about the past that affects the future is the time at which the room becomes empty. A smaller time can never hurt, because every request that fits after a later time also fits after an earlier one. So among the plans that have held the same number of events, the plan whose last event ends sooner is simply better, and the search keeps expanding the worse ones.

<!-- stage: insight -->
### Always Take The One That Ends First

Call the set of events held so far a **compatible set**, meaning no two of them overlap. The room becomes empty at the end of the last held event, and that moment is the **free boundary**. Among all requests that begin at or after the free boundary, take the one with the **earliest finish**. Then repeat from its end.

The reason is an exchange. Take any best calendar, and look at its first event. Suppose the request with the earliest finish among all requests is different from it. The earliest-finishing request ends no later than the first event of the best calendar ends. Replace that first event with the earliest-finishing request. Every other event in the best calendar begins at or after the end of the replaced one, so it also begins at or after the end of its replacement. The calendar is still conflict-free and holds the same number of events. So some best calendar starts with the earliest finish, and the same argument applies to what remains.

<!-- names: compatible set, free boundary, earliest finish -->

The rule needs a sorted order only to find that request quickly. Sort the requests by end time, then walk them once. A request that begins before the free boundary is rejected, and one that begins at or after it is accepted, and its end becomes the new free boundary. The count of rejected requests is the minimum number of removals that leaves no overlap, since the accepted ones are the largest compatible set.

A second reading of the same rule covers a problem where overlapping requests are grouped and one stroke serves a whole group. A group is a run of requests that all contain a single point. The group is closed at the earliest end among its members, because a stroke placed there still touches every member, and any later point would miss the member that ends first.

<!-- stage: variables -->
### The Free Boundary And The Counters

After sorting by end, the cursor `i` is the next request to judge. The variable `freeAt` is the end of the last accepted request, which is the moment the room is empty, and it starts below every possible start. The counter `kept` is the size of the compatible set so far, and the number rejected is `i - kept` at any moment. Only `freeAt` can change the verdict for a request, and it changes only on an acceptance, to a value that is never smaller than before. For the group reading, `groupEnd` plays the same role: it is the smallest end seen in the current group of overlapping requests.

<!-- stage: trace -->
### One Calendar And One Group Of Arrows

The first trace takes seven requests sorted by end, with half-open spans, so a request that begins exactly when another ends is allowed. The request one to three is accepted because nothing is held. Two to five begins at two, before the boundary three, so it is rejected. Four to six begins after three and is accepted, and the boundary moves to six. Three to eight is rejected. Six to nine begins exactly at the boundary six and is accepted, which is the touching case. Eight to ten is rejected, and nine to twelve is accepted, giving four events held and three rejected.

The second trace is the group reading. Balloons are closed spans sorted by start, and one arrow serves every balloon that contains its point. The first balloon opens a group whose end is six. Balloons two to eight and five to six join, because they begin at or before six, and the group end stays at six. Seven to twelve begins after six, so the arrow fires at six and a new group begins with end twelve. Ten to sixteen joins, and fourteen to eighteen starts after twelve, so a third arrow is needed.

```trace
{"cells":["1-3","2-5","4-6","3-8","6-9","8-10","9-12"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"freeAt":3,"kept":1,"rejected":0},"note":"The span 1 to 3 is first in end order and nothing is held, so it is accepted and the free boundary becomes 3."},{"at":{"i":1},"vars":{"freeAt":3,"kept":1,"rejected":1},"note":"The span 2 to 5 begins at 2, before the boundary 3, so it is rejected and the boundary stays."},{"at":{"i":2},"vars":{"freeAt":6,"kept":2,"rejected":1},"note":"The span 4 to 6 begins at 4, not before the boundary, so it is accepted and the boundary moves to 6."},{"at":{"i":3},"vars":{"freeAt":6,"kept":2,"rejected":2},"note":"The span 3 to 8 begins at 3, before the boundary 6, so it is rejected and the boundary stays."},{"at":{"i":4},"vars":{"freeAt":9,"kept":3,"rejected":2},"note":"The span 6 to 9 begins at 6, not before the boundary, so it is accepted and the boundary moves to 9. It begins exactly at the boundary, which half-open spans allow."},{"at":{"i":5},"vars":{"freeAt":9,"kept":3,"rejected":3},"note":"The span 8 to 10 begins at 8, before the boundary 9, so it is rejected and the boundary stays."},{"at":{"i":6},"vars":{"freeAt":12,"kept":4,"rejected":3},"note":"The span 9 to 12 begins at 9, not before the boundary, so it is accepted and the boundary moves to 12. It begins exactly at the boundary, which half-open spans allow."}]}
```

```trace
{"cells":["1-6","2-8","5-6","7-12","10-16","14-18"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"groupEnd":6,"arrows":1},"note":"The balloon 1 to 6 opens the first group, so arrow number 1 is owed and the group end is 6."},{"at":{"i":1},"vars":{"groupEnd":6,"arrows":1},"note":"The balloon 2 to 8 starts at 2, within reach of the group end 6, so it joins and the group end becomes 6."},{"at":{"i":2},"vars":{"groupEnd":6,"arrows":1},"note":"The balloon 5 to 6 starts at 5, within reach of the group end 6, so it joins and the group end becomes 6."},{"at":{"i":3},"vars":{"groupEnd":12,"arrows":2},"note":"The balloon 7 to 12 starts at 7, past the group end 6, so the earlier group is closed at 6 and arrow number 2 is owed with group end 12."},{"at":{"i":4},"vars":{"groupEnd":12,"arrows":2},"note":"The balloon 10 to 16 starts at 10, within reach of the group end 12, so it joins and the group end becomes 12."},{"at":{"i":5},"vars":{"groupEnd":18,"arrows":3},"note":"The balloon 14 to 18 starts at 14, past the group end 12, so the earlier group is closed at 12 and arrow number 3 is owed with group end 18."}]}
```

<!-- stage: code -->
### Sort By End, Then One Sweep

```java
static int mostCompatible(int[][] req) {
    int[][] sorted = req.clone();                                    // shallow copy of the rows
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
    int kept = 0, freeAt = Integer.MIN_VALUE;
    for (int[] r : sorted) {
        if (r[0] >= freeAt) { kept++; freeAt = r[1]; }
    }
    return kept;
}

static int arrows(int[][] balloons) {
    int[][] sorted = balloons.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
    int shots = 0;
    long groupEnd = Long.MIN_VALUE;                                  // no open group yet
    for (int[] b : sorted) {
        if (shots == 0 || b[0] > groupEnd) { shots++; groupEnd = b[1]; }
        else groupEnd = Math.min(groupEnd, b[1]);
    }
    return shots;
}
```

The comparators use `Integer.compare` instead of subtraction, because a difference of two ints near opposite limits wraps around and misorders the rows. The sweeps are linear after the sort, so the total is dominated by the sort at O(n log n). The first loop uses `>=` for half-open spans, and the second uses `>` because closed spans touch at a shared endpoint.

<!-- stage: applicability -->
### When Ending Early Wins

Use this pattern when the objective is the biggest set of pairwise compatible intervals, the fewest removals that leave no overlap, or the fewest points that touch every interval. The invariant is that the accepted set always has the smallest possible free boundary for its size. Decide before sorting what the endpoints mean, because the test is `>=` for half-open spans and `>` for closed ones.

The false friend is sorting by start, which is the right order for merging intervals but is wrong for choosing. With requests from 0 to 10, 1 to 2 and 3 to 4, start order accepts the long one first and ends with a single event, while the end order holds two. The pattern also stops applying when events carry weights, since a heavy long event can beat several short ones, and that needs dynamic programming from Chapters 26 to 29. A shortest-first rule fails too, and Lesson 04 builds the counterexample.

In Java, copy the outer array before sorting rows, and compare with `Integer.compare` or `Long.compare`. Keep the free boundary in a type wide enough for the smallest possible endpoint.

<!-- stage: exercises -->
### Exercises

#### [Build] Choose Compatible Meetings (Author exercise)
<!-- id: gr-compatible-meetings -->

**Prerequisites.** Sorting rows with a comparator from Chapter 05; the interval notation of Chapter 10.

**Problem.** Each meeting is a half-open span `[start, end)`, so a meeting may begin exactly when another ends. The room holds one meeting at a time. Return the largest number of meetings that can be held without any two overlapping.

**Constraints.** 0 <= meetings.length <= 20 and 0 <= start < end <= 10000. The input rows must not be reordered.

**Example 1.** Input `meetings = [[9, 11], [9, 10], [10, 12], [11, 13], [12, 14]]`, output 3.

**Example 2.** Input `meetings = [[1, 2], [1, 2], [1, 2]]`, output 1, since identical spans overlap each other.

**Hint.** Which meeting leaves the room empty soonest? After accepting it, which meetings can still be considered?

**Changed decision.** First rung: sort by end and accept a meeting whenever it begins at or after the free boundary.

#### [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gr-non-overlapping-removals -->

**Prerequisites.** The meeting-selection exercise above.

**Problem.** Given half-open spans with `long` endpoints, return the smallest number of spans to remove so that no two remaining spans overlap. Spans that merely touch do not overlap.

**Constraints.** 0 <= intervals.length <= 100000, each span has `start < end`, and all endpoints lie anywhere in the `long` range. Do not compute a difference of two endpoints.

**Example 1.** Input `intervals = [[1, 3], [2, 5], [4, 6], [3, 8], [6, 9]]`, output 2.

**Example 2.** Input `intervals = [[-8000000000000000000, 8000000000000000000], [-9000000000000000000, -8500000000000000000], [7000000000000000000, 9000000000000000000]]`, output 1.

**Hint.** What is the relation between the number kept and the number removed? Which comparison between two `long` values is safe at the extremes?

**Changed decision.** The answer is the complement of the kept count, and the endpoints are wide enough to make a subtracting comparator wrong.

#### [Boundary] Touching Endpoint Contract (Author exercise)
<!-- id: gr-touching-endpoint-contract -->

**Prerequisites.** The two exercises above.

**Problem.** Spans are given with a flag. If `closed` is true, each span is `[a, b]` with `a <= b`, and two spans overlap when they share any point, including a single endpoint. If `closed` is false, each span is `[a, b)` with `a < b`, and touching spans do not overlap. Return the largest number of pairwise non-overlapping spans.

**Constraints.** 0 <= spans.length <= 15 and 0 <= a, b <= 1000. A closed span may have `a == b`.

**Example 1.** Input `spans = [[1, 3], [3, 5], [5, 7]]`, `closed = true`, output 2, and with `closed = false` the same spans give 3.

**Example 2.** Input `spans = [[4, 4], [4, 4], [5, 5]]`, `closed = true`, output 2.

**Hint.** Which comparison of the next start with the free boundary changes between the two models? What does a point span do to the boundary?

**Changed decision.** Only the acceptance test changes between the models, and the exercise checks that the test matches the declared contract.

#### [Recognize] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gr-arrows-by-group -->

**Prerequisites.** All three exercises above.

**Problem.** Each balloon is a closed span `[xStart, xEnd]` on a line. An arrow shot at a point bursts every balloon whose span contains that point. Return the fewest arrows that burst every balloon. Solve it by sorting by start and tracking the smallest end of the current group.

**Constraints.** 0 <= points.length <= 100000 and endpoints are `int` values that may reach both `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.

**Example 1.** Input `points = [[10, 16], [2, 8], [1, 6], [7, 12]]`, output 2.

**Example 2.** Input `points = [[-2147483648, 0], [0, 2147483647]]`, output 1, since the shared point zero lies in both balloons.

**Hint.** What one number summarises the group that the next balloon is tested against? How does that number change when a balloon joins?

**Changed decision.** The state is the shrinking overlap of a group, with the strict comparison that closed spans need.
