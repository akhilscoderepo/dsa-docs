<!-- lesson-kind: standard -->
<!-- lesson-id: overlap-and-coverage -->
## Overlap And Coverage

<!-- stage: context -->
### The Market Square Booking Desk

A town square hosts a weekend market, and the booking desk receives requests from stallholders who each want the square for one block of time, such as from hour 9 to hour 12. Two stallholders cannot use the square at once, but one may start at the very hour another leaves. The desk has no wish to refuse anyone without cause, yet the square is small, so the clerk must decide which requests to turn down so that the accepted ones never clash and as many stallholders as possible get a slot.

A second question arrives from the town council. Some requests are wasteful because a larger request already contains them: a stall that wants hours 10 to 11 is pointless to list when another stall holds hours 9 to 13. The council wants to know how many requests would remain if every contained request were struck from the list, and the clerk must answer without losing track of which requests were struck.

<!-- stage: naive -->
### Try Every Set Of Requests

The direct approach is to consider every subset of the requests, check whether the chosen ones are free of clashes, and remember the largest subset that passes.

```java
static int mostCompatible(int[][] requests) {
    int n = requests.length, best = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        boolean ok = true;
        for (int a = 0; a < n && ok; a++) {
            if ((mask >> a & 1) == 0) continue;
            for (int b = a + 1; b < n && ok; b++) {
                if ((mask >> b & 1) == 0) continue;
                if (requests[a][0] < requests[b][1] && requests[b][0] < requests[a][1]) ok = false;
            }
        }
        if (ok) best = Math.max(best, Integer.bitCount(mask));
    }
    return best;
}
```

It is correct because every possible set of accepted requests is examined, so the best one cannot be overlooked.

<!-- stage: bottleneck -->
### The Subsets Double Per Request

With n requests there are 2^n subsets, and each one needs a pairwise clash check, so the work is O(2^n n^2). Thirty requests already mean over a billion subsets, and a weekend market easily has hundreds. The search wastes nearly all of its effort, because most subsets are doomed by a single clash between two members, and the code still builds, checks and discards each of them in full.

The waste comes from treating every request as an equal candidate at all times. Once the requests are sorted, the choice at each step is not between two huge families of subsets but between two single requests, and one of them can be shown never to be worse than the other. A rule that settles each clash locally would reduce the search to one sorted pass, costing O(n log n) for the sort plus O(n) for the walk.

<!-- stage: insight -->
### Keep Whoever Leaves The Room Soonest

Sort the requests by their end time and walk through them once. Keep a request when it starts at or after the end of the last kept request, and reject it otherwise. The reasoning is an exchange argument. Among all requests that could come next, the one with the **earliest finish** leaves the most remaining time for everything after it, so replacing any other choice by it can never make the final count smaller. Picking by earliest start or by shortest length does not carry that guarantee, because a request that starts early can still block the square for most of the day.

The invariant is that the kept set is as large as any compatible set of the requests processed so far, and among such sets its last end is as small as possible. Each new request either fits after that end, which grows the set by one with the smallest possible new end, or it does not fit, and then no set that uses it can beat the current one, because the current set already ends no later.

Coverage questions use a second summary. Sort by start, and break ties by the larger end first. A running **reach** records the greatest end seen so far, and a request whose end does not pass the reach lies inside an earlier **container**. The tie order matters, since a shorter request with the same start must come after the longer one so that the container is already counted when the shorter one arrives.

<!-- names: earliest finish, reach, container -->

Merging the requests into blocks answers neither question. A merge replaces several requests by one union, and the union no longer says which original request should be refused or struck.

<!-- stage: variables -->
### One Last End, One Running Reach

For selection, `lastEnd` is the end of the most recently kept request, `kept` counts the accepted requests, and the answer for removals is the total minus `kept`. For coverage, `reach` is the largest end among earlier requests in the sorted order and `visible` counts requests that stick out past it. A request that ties the reach exactly is hidden, since its end does not pass it. Sorting uses a cloned array, so the caller's list keeps its original order.

<!-- stage: trace -->
### Two Passes Over Sorted Requests

The first trace selects among the half-open requests 0 to 6, 1 to 3, 2 to 4, 3 to 5, 5 to 7 and 6 to 8, listed here in order of end time. The cells hold that sorted order, `i` points at the request being judged, and `kept` points at the last accepted request. Look at the second step: the request 2 to 4 starts at 2, before the last end 3, so it is rejected and the kept pointer stays put.

```trace
{"cells":["1-3","2-4","3-5","0-6","5-7","6-8"],"pointers":["i","kept"],"steps":[{"at":{"i":0,"kept":0},"vars":{"lastEnd":3,"kept":1},"note":"The request 1 to 3 is the first one, so it is kept and the last end becomes 3."},{"at":{"i":1,"kept":0},"vars":{"lastEnd":3,"kept":1},"note":"The request 2 to 4 starts at 2, before the last end 3, so it is rejected and the kept pointer stays put."},{"at":{"i":2,"kept":2},"vars":{"lastEnd":5,"kept":2},"note":"The request 3 to 5 starts at 3, at or after the last end, so it is kept and the last end becomes 5."},{"at":{"i":3,"kept":2},"vars":{"lastEnd":5,"kept":2},"note":"The request 0 to 6 starts at 0, before the last end 5, so it is rejected and the kept pointer stays put."},{"at":{"i":4,"kept":4},"vars":{"lastEnd":7,"kept":3},"note":"The request 5 to 7 starts at 5, at or after the last end, so it is kept and the last end becomes 7."},{"at":{"i":5,"kept":4},"vars":{"lastEnd":7,"kept":3},"note":"The request 6 to 8 starts at 6, before the last end 7, so it is rejected and the kept pointer stays put."}]}
```

The second trace answers the council question for the requests 1 to 4, 3 to 6, 2 to 8, 2 to 5, 8 to 9 and 7 to 8, sorted by start with the longer end first when starts tie. The pointer `owner` marks the request that set the current reach. The request 2 to 5 comes after 2 to 8, so the larger container is already in place and the shorter one is hidden.

```trace
{"cells":["1-4","2-8","2-5","3-6","7-8","8-9"],"pointers":["i","owner"],"steps":[{"at":{"i":0,"owner":0},"vars":{"reach":4,"visible":1},"note":"The request 1 to 4 is the first one, so it is visible and sets the reach to 4."},{"at":{"i":1,"owner":1},"vars":{"reach":8,"visible":2},"note":"The request 2 to 8 ends past the reach, so it is visible and now sets the reach to 8."},{"at":{"i":2,"owner":1},"vars":{"reach":8,"visible":2},"note":"The request 2 to 5 ends at 5, which does not pass the reach 8, so it is covered and hidden."},{"at":{"i":3,"owner":1},"vars":{"reach":8,"visible":2},"note":"The request 3 to 6 ends at 6, which does not pass the reach 8, so it is covered and hidden."},{"at":{"i":4,"owner":1},"vars":{"reach":8,"visible":2},"note":"The request 7 to 8 ends at 8, which does not pass the reach 8, so it is covered and hidden."},{"at":{"i":5,"owner":5},"vars":{"reach":9,"visible":3},"note":"The request 8 to 9 ends past the reach, so it is visible and now sets the reach to 9."}]}
```

<!-- stage: code -->
### Select By End, Count By Reach

```java
static int removalsForCompatibility(int[][] requests) {
    int[][] sorted = new int[requests.length][];
    for (int i = 0; i < sorted.length; i++) sorted[i] = requests[i].clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
    int kept = 0;
    long lastEnd = Long.MIN_VALUE;
    for (int[] r : sorted) {
        if (r[0] >= lastEnd) { kept++; lastEnd = r[1]; }
    }
    return requests.length - kept;
}

static int visibleAfterCoverage(int[][] requests) {
    int[][] sorted = new int[requests.length][];
    for (int i = 0; i < sorted.length; i++) sorted[i] = requests[i].clone();
    Arrays.sort(sorted, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(b[1], a[1]));
    int visible = 0;
    long reach = Long.MIN_VALUE;
    for (int[] r : sorted) {
        if (r[1] > reach) { visible++; reach = r[1]; }
    }
    return visible;
}
```

Each function is dominated by its sort, so it costs O(n log n) time and O(n) space for the copy, and the scan after the sort is linear.

<!-- stage: applicability -->
### When To Prefer, Remove, Or Cover

Use this when the goal is to keep as many compatible intervals as possible, to count how many must be dropped, or to find which ones sit wholly inside another. The invariant for selection is that the last kept end is the smallest possible among processed choices, and for coverage that the reach summarizes every earlier container.

A false friend is the merge from the earlier lesson, which fuses overlapping intervals and so forgets which originals were removed. A second false friend is sorting by start and keeping greedily, which fails on a long early request that blocks several short ones. A third is sorting coverage input by start alone, which lets a short request with an equal start hide its own container.

In Java, order the pair with `Integer.compare` and never with `a[1] - b[1]`, because subtracting extreme coordinates overflows and flips the sign. Decide from the contract whether a request that starts exactly at the last end is compatible, since that choice changes `>=` into `>`. Sort a clone when the caller's order must survive.

<!-- stage: exercises -->
### Exercises

#### [Build] Keep Earlier Finishing Interval (Author exercise)
<!-- id: iv-keep-earlier-finish -->

**Prerequisites.** The endpoint contracts and touching-boundary lessons.

**Problem.** Given two half-open intervals that overlap, return 0 when the first should be kept and 1 when the second should be kept, where the kept one is whichever leaves more room for later choices. Return 0 when both end at the same value.

**Constraints.** -1000000000 <= start < end <= 1000000000, and the two intervals overlap.

**Example 1.** Input `a = [1, 9], b = [3, 5]`, output `1`.

**Example 2.** Input `a = [2, 6], b = [4, 6]`, output `0`.

**Hint.** Which of the two frees the square sooner? What does the tie mean for the future?

**Changed decision.** First rung: the choice is made by the end value alone, and the start never enters the comparison.

#### [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: iv-non-overlapping-intervals -->

**Prerequisites.** Keep Earlier Finishing Interval.

**Problem.** Given an array of half-open intervals, return the fewest intervals to remove so that the rest do not overlap. Intervals that meet only at an endpoint do not overlap. Sort by end and keep an interval when it starts at or after the last kept end.

**Constraints.** 1 <= intervals.length <= 100000 and -2147483648 <= start < end <= 2147483647.

**Example 1.** Input `intervals = [[0, 6], [1, 3], [2, 4], [3, 5], [5, 7], [6, 8]]`, output `3`.

**Example 2.** Input `intervals = [[4, 5], [4, 5], [4, 5]]`, output `2`.

**Hint.** Which end order makes the first kept interval safe? What does an equal start and end of the previous keep mean?

**Changed decision.** The sort key moves from the start to the end, so the invariant concerns the smallest last end rather than the earliest start.

#### [Boundary] Remove Covered Intervals (LeetCode 1288)
<!-- id: iv-remove-covered-intervals -->

**Prerequisites.** Non-overlapping Intervals.

**Problem.** Given an array of intervals, remove every interval that lies inside another one, and return how many remain. An interval lies inside another when the other starts no later and ends no earlier. Equal duplicates count as covered except for one copy.

**Constraints.** 1 <= intervals.length <= 100000 and 0 <= start < end <= 1000000000.

**Example 1.** Input `intervals = [[1, 4], [3, 6], [2, 8], [2, 5], [8, 9], [7, 8]]`, output `3`.

**Example 2.** Input `intervals = [[5, 7], [5, 7], [5, 7]]`, output `1`.

**Hint.** If two intervals share a start, which one must be seen first? What does an end equal to the reach mean?

**Changed decision.** Equal starts are ordered by descending end, so a shorter interval can never be counted before its container.

#### [Recognize] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: iv-minimum-arrows -->

**Prerequisites.** Remove Covered Intervals.

**Problem.** Each balloon is a closed horizontal span, and an arrow shot straight up at one coordinate bursts every balloon whose span contains it. Return the fewest arrows needed to burst all balloons. Sort by end and shoot at the end of the first unburst balloon.

**Constraints.** 1 <= points.length <= 100000 and -2147483648 <= start <= end <= 2147483647.

**Example 1.** Input `points = [[10, 16], [2, 8], [1, 6], [7, 12]]`, output `2`.

**Example 2.** Input `points = [[1, 2], [2, 3], [3, 4], [4, 5]]`, output `2`.

**Hint.** Where should one arrow be placed to reach as many later balloons as possible? When does a balloon fall outside that shot?

**Changed decision.** The span is closed, so a balloon that starts exactly at the shot coordinate is still burst, and the comparison is strict.
