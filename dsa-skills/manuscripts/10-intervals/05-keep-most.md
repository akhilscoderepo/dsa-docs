<!-- lesson-kind: standard -->
<!-- lesson-id: keep-most -->
## Keep The Most Intervals Without Overlap

<!-- stage: context -->
### Four Requests, One Accepted

A conference room accepts requests in the order they arrive. The requests are the half-open time slots `[1,10)`, `[2,3)`, `[4,5)` and `[6,7)`. The first request holds the room from hour 1 to hour 10. The system accepts it and rejects the other three, because each of them falls inside it. The room hosts one event. The three short requests share no hour with each other, so the room could host three events by accepting those and rejecting the long one.

The arrival order gave the wrong answer. A different rule can give the right one, but the rule is not obvious. Choosing the request that starts first would again pick `[1,10)`. This lesson answers one question: which request should the room keep when two requests clash, so that the room hosts as many events as possible?

<!-- stage: naive -->
### Try Every Set Of Requests

A method that cannot fail tries every subset of the requests. For each subset it checks that no two chosen requests share an hour, and it remembers the largest such subset.

```java
static int maxEvents(int[][] slots) {
    int n = slots.length, best = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        boolean ok = true;
        int size = 0;
        for (int i = 0; i < n && ok; i++) {
            if ((mask >> i & 1) == 0) continue;
            size++;
            for (int j = i + 1; j < n; j++) {
                if ((mask >> j & 1) == 1 && Math.max(slots[i][0], slots[j][0]) < Math.min(slots[i][1], slots[j][1])) {
                    ok = false;
                    break;
                }
            }
        }
        if (ok) best = Math.max(best, size);
    }
    return best;
}
```

For the four requests above the method returns 3, which is the correct answer. It has no rule to get wrong, because it examines every possible choice.

<!-- stage: bottleneck -->
### Counting The Subsets

```predict
Two requests overlap, and the room can keep only one of them. Which one leaves more room for the requests that have not been decided, and why?

The one that ends first. Any later request that fits after the longer one also fits after the earlier-ending one, because it starts at or after the later end. Keeping the earlier end can only help.
```

A list of `n` requests has `2^n` subsets, and each check costs up to `n^2` pair tests. The method therefore costs O(2^n * n^2). For `n = 30` that is about a billion subsets, and for `n = 100` no machine can finish. Real booking lists hold thousands of requests.

The method repeats a decision that has a local answer. Every subset that holds a long request and a short request inside it contains a clash. The method rediscovers that clash in each of them. The prediction above says that the clash has a best resolution, and applying it one request at a time removes the search.

<!-- stage: insight -->
### Keep The Request That Ends First

Two requests are **compatible** when they share no hour, so under the half-open model the second starts at or after the end of the first. The goal is the largest set of pairwise compatible requests.

#### Sort By End And Keep When It Fits

Sort the requests by end, using the end order from the first lesson. Scan them while keeping `lastEnd`, the end of the last request that was kept. A request whose start is at least `lastEnd` fits, so keep it and set `lastEnd` to its end. A request that starts earlier clashes with the kept request, so skip it. The number of skipped requests is the number to remove.

<!-- names: compatible, earliest finish, exchange argument -->

#### Why The Earliest Finish Is Safe

The request with the **earliest finish** is the first one in end order. An **exchange argument** shows that some best set contains it. Take any best set, and let `f` be its request with the smallest end. Replace `f` by the earliest-finishing request `g`. The end of `g` is at most the end of `f`. Every other request in the set starts at or after the end of `f`, so it also starts at or after the end of `g`. The new set is still compatible and has the same size. After keeping `g`, the same argument applies to the requests that start at or after its end.

#### Coverage Needs Start Order Instead

A different decision asks which requests lie fully inside another request. Sort by start ascending and, when starts tie, by end descending. The container then comes before the request it holds. A running maximum end over the earlier requests summarizes all earlier containers. A request whose end is at most that maximum is covered.

<!-- stage: variables -->
### What The Two Scans Keep

Each scan needs one running value and one counter.

- **sorted** is a copy of the input in the order that the decision needs, and the original array stays as given.
- **lastEnd** is the end of the last kept request in the selection scan.
- **maxEnd** is the largest end among the earlier requests in the coverage scan.
- **count** is the number of requests that were kept, or the number that are not covered.

<!-- stage: trace -->
### Tracing Selection And Coverage

#### Selecting By End

Take the requests `[1,10)`, `[2,3)`, `[4,5)`, `[6,7)` and `[5,9)`. In end order they are `[2,3)`, `[4,5)`, `[6,7)`, `[5,9)`, `[1,10)`. Each cell of the trace holds one end in that order, and the pointer `i` marks the request under test.

The first three requests fit one after another, because each starts at or after `lastEnd`. The request `[5,9)` starts at 5, before `lastEnd = 7`, so it clashes and is skipped. The request `[1,10)` clashes too. The scan keeps 3 requests and removes 2.

```trace
{"cells":[3,5,7,9,10],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"lastEnd":"none","kept":0},"note":"The requests are sorted by end. Nothing is kept yet."},{"at":{"i":0},"vars":{"lastEnd":3,"kept":1},"note":"The start 2 is at least lastEnd, or nothing is kept yet, so [2,3) is kept and lastEnd becomes 3."},{"at":{"i":1},"vars":{"lastEnd":5,"kept":2},"note":"The start 4 is at least lastEnd, or nothing is kept yet, so [4,5) is kept and lastEnd becomes 5."},{"at":{"i":2},"vars":{"lastEnd":7,"kept":3},"note":"The start 6 is at least lastEnd, or nothing is kept yet, so [6,7) is kept and lastEnd becomes 7."},{"at":{"i":3},"vars":{"lastEnd":7,"kept":3},"note":"The start 5 is before lastEnd 7, so [5,9) clashes and is skipped."},{"at":{"i":4},"vars":{"lastEnd":7,"kept":3},"note":"The start 1 is before lastEnd 7, so [1,10) clashes and is skipped."}]}
```

#### Finding Covered Requests

Now take `[1,4)`, `[3,6)`, `[2,8)`, `[1,2)` and `[8,9)`. In start order, with ties by descending end, they are `[1,4)`, `[1,2)`, `[2,8)`, `[3,6)`, `[8,9)`. The cells are the starts in that order. The request `[1,2)` shares its start with `[1,4)`, and the descending end puts the larger request first, so `[1,2)` is recognised as covered.

```trace
{"cells":[1,1,2,3,8],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"maxEnd":"none","notCovered":0},"note":"The requests are sorted by start, with ties by larger end first."},{"at":{"i":0},"vars":{"maxEnd":4,"notCovered":1},"note":"The end 4 is larger than every earlier end, so [1,4) is not covered and maxEnd becomes 4."},{"at":{"i":1},"vars":{"maxEnd":4,"notCovered":1},"note":"The end 2 is at most maxEnd 4, so an earlier request covers [1,2)."},{"at":{"i":2},"vars":{"maxEnd":8,"notCovered":2},"note":"The end 8 is larger than every earlier end, so [2,8) is not covered and maxEnd becomes 8."},{"at":{"i":3},"vars":{"maxEnd":8,"notCovered":2},"note":"The end 6 is at most maxEnd 8, so an earlier request covers [3,6)."},{"at":{"i":4},"vars":{"maxEnd":9,"notCovered":3},"note":"The end 9 is larger than every earlier end, so [8,9) is not covered and maxEnd becomes 9."}]}
```

<!-- stage: code -->
### Writing The Scans In Java

#### Selection By End

The method returns the number of requests to remove so the rest are compatible. The end comparison uses `Integer.compare`, never subtraction.

```java
static int removalsForNoOverlap(int[][] slots) {
    int[][] sorted = slots.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[1], b[1]));
    int kept = 0;
    long lastEnd = Long.MIN_VALUE;
    for (int[] s : sorted) {
        if (s[0] >= lastEnd) {
            kept++;
            lastEnd = s[1];
        }
    }
    return slots.length - kept;
}
```

#### Coverage By Start With Descending Ends

The comparator breaks a start tie by the larger end first.

```java
static int countNotCovered(int[][] slots) {
    int[][] sorted = slots.clone();
    Arrays.sort(sorted, (a, b) -> a[0] != b[0]
            ? Integer.compare(a[0], b[0])
            : Integer.compare(b[1], a[1]));
    int notCovered = 0;
    long maxEnd = Long.MIN_VALUE;
    for (int[] s : sorted) {
        if (s[1] > maxEnd) {
            notCovered++;
            maxEnd = s[1];
        }
    }
    return notCovered;
}
```

Sorting dominates both methods at O(n log n) time, and the clone takes O(n) space. Each scan afterwards adds only O(n) time and O(1) space. The `long` initial values are below every `int`, so the first request is always kept.

<!-- stage: applicability -->
### When The Greedy Choice Applies

#### State The Objective Before Sorting

The invariant of the selection scan is about `lastEnd`. After each request, it is the smallest end that any largest compatible set of the processed requests can have. Use end order when the objective is to keep the most requests, remove the fewest, or place the fewest points. Use start order with descending ends when the question is about requests inside other requests. The two scans differ in sort key, and each key follows from its objective.

#### Other Greedy Rules Fail

The rule "keep the request that starts first" is a false friend, and the opening example shows why. Another false friend is "keep the shortest request". Take `[1,6)`, `[5,7)` and `[6,12)`. The shortest request is `[5,7)`, which clashes with both others, so the rule keeps 1 request. The requests `[1,6)` and `[6,12)` give 2. Merging the requests, as in the earlier lesson, is also a false friend here. A merge replaces the original requests with unions and loses which original request should be removed.

#### Limits Of The Method

The greedy rule maximizes the count only. When requests carry weights, such as profit, keeping the earliest end can lose value, and a later chapter on dynamic programming solves that case. When the question is how many rooms are needed at once, the answer is a different quantity, and Chapter 17 teaches it with a heap.

<!-- stage: exercises -->
### Exercises

#### [Build] Keep Earlier Finishing Interval (Author exercise)
<!-- id: iv-keep-earlier-finish -->

**Prerequisites.** The half-open model and the end order from the earlier lessons.

**Problem.** Two half-open intervals `[start, end)` overlap. Return 0 if keeping the first interval leaves at least as much room for later intervals as keeping the second, and return 1 otherwise. An interval leaves more room when its end is smaller. Any interval that starts at or after the larger end also starts at or after the smaller end. When the two ends are equal, return 0.

**Constraints.** The limits are:
- **Values** are `int` values with `start < end` in each interval.
- **Overlap** is guaranteed: the larger start is below the smaller end.
- **Return** is the `int` 0 or 1.
- **Mutation** is not allowed; neither interval changes.

**Example 1.** Input `[1,10)` and `[2,3)`, output 1.

**Example 2.** Input `[1,4)` and `[2,4)`, output 0, because the ends tie.

**Hint.** Which end limits where the next interval may start? Which choice moves that limit less to the right?

**Changed decision.** Basic case: the end, and not the start or the length, decides which interval to keep.

#### [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: iv-non-overlapping -->

**Prerequisites.** The exercise above.

**Problem.** Given half-open intervals `[start, end)`, return the smallest number of intervals to remove so that no two remaining intervals overlap. Two intervals that only touch, as `[1,2)` and `[2,3)` do, do not overlap.

**Constraints.** The limits are:
- **Length** is `0 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start < end`.
- **Return** is a single `int`, which is 0 for an empty input.
- **Mutation** is not allowed; the input keeps its order.

**Example 1.** Input `[[1,4],[2,3],[3,6],[5,7]]`, output 2.

**Example 2.** Input `[[0,2],[0,2],[2,5]]`, output 1.

**Hint.** Sort by end. Keep a request when its start is at least the end of the last kept request.

**Changed decision.** The scan sorts by end and counts rejected requests, where a merge would have changed them.

#### [Boundary] Remove Covered Intervals (LeetCode 1288)
<!-- id: iv-remove-covered -->

**Prerequisites.** The two exercises above.

**Problem.** Given half-open intervals `[start, end)`, an interval `[a, b)` is covered by `[c, d)` when `c <= a` and `b <= d`. Return the number of intervals that are not covered by any other interval in the list. Two equal intervals cover each other, so exactly one copy of them counts as not covered when no other interval covers them.

**Constraints.** The limits are:
- **Length** is `1 <= intervals.length <= 10^5`.
- **Values** are `int` values with `start < end`.
- **Equal starts** are legal, and so are duplicates.
- **Return** is a single `int`.

**Example 1.** Input `[[1,5],[1,3],[2,5],[4,9],[6,9]]`, output 2.

**Example 2.** Input `[[2,6],[2,4],[2,6]]`, output 1.

**Hint.** For equal starts, which interval must the scan see first so that the shorter one looks covered?

**Changed decision.** The sort breaks start ties by larger end first, so a container always comes before what it holds.

#### [Recognize] Minimum Number Of Arrows (LeetCode 452)
<!-- id: iv-min-arrows -->

**Prerequisites.** All three exercises above.

**Problem.** Each balloon spans the closed range `[start, end]` on a line. An arrow shot at coordinate `x` bursts every balloon with `start <= x <= end`. Return the smallest number of arrows that burst all balloons.

**Constraints.** The limits are:
- **Length** is `0 <= balloons.length <= 10^5`.
- **Values** are any `int` values with `start <= end`, including both extremes.
- **Touching** balloons that share one coordinate are burst by one arrow at that coordinate.
- **Return** is a single `int`, and the input is not modified.

**Example 1.** Input `[[1,4],[3,8],[7,9],[10,12]]`, output 3.

**Example 2.** Input `[[-2147483648,2147483647],[2147483647,2147483647]]`, output 1.

**Hint.** Sort by end and shoot at the first end. Which later balloons does that arrow burst? Compare the extremes without subtraction.

**Changed decision.** An arrow is placed at the smallest end of a group, which keeps the group's common range as large as possible.
