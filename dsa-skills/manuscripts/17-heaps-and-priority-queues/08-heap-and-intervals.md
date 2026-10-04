<!-- lesson-kind: combination -->
<!-- lesson-id: heap-and-intervals -->
## Heap And Intervals

<!-- stage: context -->
### How Many Stages Does The Festival Need

A town festival schedules performances in a park, and each performance has a start time and an end time. A performance needs a whole stage while it runs, with its own sound gear and crew, and two performances can share a stage only if one finishes before the other begins. The organisers have the full programme on a sheet, in no particular order, and the rental company asks a simple question before the weekend: how many stages must be hired so that every performance has one?

Counting by eye works for a dozen acts. The programme for the big weekend lists tens of thousands of short performances, most of them overlapping with a few neighbours and none of them with the whole sheet. The organisers also want the answer for a variant of the programme in which an act that ends at the exact minute another begins is still counted as running, because the crews need that minute to swap cables.

<!-- stage: contributions -->
### What Each Technique Brings

Sorting brings the order of events. Once the performances are arranged by start time, the loop meets each performance at the moment it begins, and everything that has not begun is still ahead and cannot affect the stages in use. The earlier chapter on intervals supplied this idea, and sorting also gives a clear contract for what overlap means at the shared endpoint.

The heap brings the answer to the only question the loop keeps asking: among the stages in use, which one becomes free first. Its root exposes that stage in constant time and updates the standing of the stages in logarithmic time. Sorting alone cannot answer it, since the end times of the stages in use form a set that changes with every start. The recognition cue for the combination is a count or an assignment of resources over intervals, where a new interval can reuse the resource that frees up earliest.

<!-- stage: naive -->
### Scan The Stages For A Free One

The direct method handles performances in start order and keeps a list with the end time of the last act on each stage. For every new act it scans the list for a stage whose last act has already ended, reuses it if there is one, and adds a new stage otherwise.

```java
static int stagesByScan(int[][] acts) {                  // each act is {start, end}, end exclusive
    int[][] byStart = acts.clone();
    java.util.Arrays.sort(byStart, (x, y) -> Integer.compare(x[0], y[0]));
    java.util.ArrayList<Integer> lastEnd = new java.util.ArrayList<>();
    for (int[] act : byStart) {
        int free = -1;
        for (int s = 0; s < lastEnd.size(); s++) {
            if (lastEnd.get(s) <= act[0]) { free = s; break; }
        }
        if (free < 0) lastEnd.add(act[1]); else lastEnd.set(free, act[1]);
    }
    return lastEnd.size();
}
```

It is correct. For the acts `[1, 4], [2, 6], [4, 7]` it returns 2.

<!-- stage: bottleneck -->
### Every Act Looks At Every Stage

An act examines up to all the stages in use, and with `n` acts and `s` stages the cost is O(n * s), which approaches O(n^2) when the programme is crowded and many stages are in use at once. The scan also settles for the first free stage that it meets, which is fine for counting but does nothing to show which stage will become free next, so every act repeats the whole search. A check of every pair of acts for overlap is slower still, at O(n^2) pairs, and does not directly yield a count of stages.

What the loop needs is smaller than a list of stage end times. It needs the earliest of them, because if even the earliest-finishing stage is still busy when an act begins, then every stage is busy, and a new one is required, and if it is free, the act can take it. A structure that gives the minimum of a changing collection at a logarithmic cost is exactly what the earlier lessons of this chapter built, and the sorted order of starts supplies the moments at which the question is asked.

<!-- stage: insight -->
### Reuse The Earliest Ending Stage

The **start sweep** visits the acts in order of start time. The **end heap** is a min-heap that holds one end time for every stage opened so far, namely the end of the last act placed on that stage, so its root is the earliest time at which any stage becomes free. For each act, apply the **reuse test**: if the end heap is not empty and its root is at most the act's start, the earliest stage is free, so poll that end time and give the act to that stage. Otherwise every stage is busy and a new one is opened. In both cases, offer the act's end time to the heap.

Reusing the earliest-ending stage is safe, because if any stage can take the act, the one that frees first can, and taking it leaves the other stages' end times unchanged and as late as possible. The heap never loses an element when a stage is opened and keeps its size when one is reused, so its final size is the number of stages that the programme requires, and equals the largest number of acts running at once.

<!-- names: start sweep, end heap, reuse test -->

The sort costs O(n log n) and each act causes at most one poll and one offer on a heap of size at most the answer, so the whole procedure costs O(n log n) time with O(s) extra memory for `s` stages. The comparison in the reuse test encodes the contract for the shared endpoint. With half-open intervals, an act that starts exactly when another ends does not overlap it, so the test uses at most. With closed intervals, the two acts share the minute and overlap, so the test uses strictly less than.

<!-- stage: variables -->
### Sorted Acts, End Times And Tie Rule

The sorted array of acts is read once, left to right, and never changes. The end heap holds integers, one per stage, and its size changes only when the reuse test fails, which opens a stage. The root is the quantity under test, and it is compared with the start of the current act. The tie rule is a single choice between `<=` and `<`, and it is fixed by the statement of the problem before any code is written. Times that can reach 10^9 fit in an `int`, but sums such as a start plus a duration need a `long`, and the comparison itself must not subtract. When two acts have the same start, their order in the sorted array does not change the count, since each takes the earliest stage that is free.

<!-- stage: trace -->
### Stages Opened And Reused

The first run uses half-open acts `[1, 4], [2, 6], [4, 7], [5, 9], [8, 10]`. The first act opens a stage that frees at 4. The act starting at 2 finds the root 4 above its start and opens a second stage, and the heap holds 4 and 6. The act starting at 4 meets the root 4, which is not greater than its start, so it reuses that stage and replaces the 4 by 7. The act starting at 5 finds the root 6 above its start and opens a third stage. The act starting at 8 sees the root 6, reuses that stage, and the heap ends with three end times, so three stages suffice.

The second run uses the closed acts `[1, 3], [3, 6], [4, 8], [6, 9]`. The act starting at 3 meets the root 3, but under the closed rule the root must be strictly smaller, so it opens a second stage. The act starting at 4 reuses the stage that ended at 3, and the act starting at 6 meets the root 6 and again must open a stage, so the answer is three. The same acts under the half-open rule would need two. The step to study is the act starting at 3, where the answer depends on nothing but the tie rule.

```trace
{"cells":[1,2,4,5,8],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"ends":"[4]","stages":1},"note":"Act [1,4] starts at 1. No stage exists yet, so one is opened with end 4."},{"at":{"i":1},"vars":{"ends":"[4,6]","stages":2},"note":"Act [2,6] starts at 2. The root 4 is above the start, so every stage is busy and a new stage is opened with end 6."},{"at":{"i":2},"vars":{"ends":"[6,7]","stages":2},"note":"Act [4,7] starts at 4. The root 4 is not above the start, so that stage is reused and its end 4 is replaced by 7."},{"at":{"i":3},"vars":{"ends":"[6,7,9]","stages":3},"note":"Act [5,9] starts at 5. The root 6 is above the start, so every stage is busy and a new stage is opened with end 9."},{"at":{"i":4},"vars":{"ends":"[7,9,10]","stages":3},"note":"Act [8,10] starts at 8. The root 6 is not above the start, so that stage is reused and its end 6 is replaced by 10."}]}
```

```trace
{"cells":[1,3,4,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"ends":"[3]","stages":1},"note":"Act [1,3] starts at 1. No stage exists yet, so one is opened with end 3."},{"at":{"i":1},"vars":{"ends":"[3,6]","stages":2},"note":"Act [3,6] starts at 3. The root 3 is not below the start, so every stage is busy and a new stage is opened with end 6."},{"at":{"i":2},"vars":{"ends":"[6,8]","stages":2},"note":"Act [4,8] starts at 4. The root 3 is strictly below the start, so that stage is reused and its end 3 is replaced by 8."},{"at":{"i":3},"vars":{"ends":"[6,8,9]","stages":3},"note":"Act [6,9] starts at 6. The root 6 is not below the start, so every stage is busy and a new stage is opened with end 9."}]}
```

<!-- stage: code -->
### Counting Stages With An End Heap

```java
static int stagesNeeded(int[][] acts, boolean closed) {
    int[][] byStart = acts.clone();
    java.util.Arrays.sort(byStart, (x, y) -> Integer.compare(x[0], y[0]));
    java.util.PriorityQueue<Integer> ends = new java.util.PriorityQueue<>();
    for (int[] act : byStart) {
        boolean free = !ends.isEmpty() && (closed ? ends.peek() < act[0] : ends.peek() <= act[0]);
        if (free) ends.poll();                      // reuse the stage that frees first
        ends.offer(act[1]);
    }
    return ends.size();
}
```

The sort costs O(n log n), and the loop does one offer and at most one poll per act, so the method as a whole is O(n log n) time with the heap holding at most one entry per stage. The test reads `ends.peek()` only after checking `isEmpty()`, since `peek` returns `null` on an empty heap, and unboxing that value would throw. The comparison operators are applied to unboxed `int` values, and no subtraction is used, so large times cannot overflow. Sorting with `Integer.compare` leaves acts with equal starts in an arbitrary but harmless order.

<!-- stage: applicability -->
### When Intervals Compete For Resources

Use a sorted sweep with an end heap when intervals compete for identical resources such as rooms, stages, machines or lanes, and the question is how many resources are needed, or which one a new interval can reuse. The invariant is that, after each act is processed, the heap holds one end time per resource opened so far, namely the end of the last interval placed on it, so the root says when the next resource frees. Store a resource identifier next to the end time when the answer must name the resource.

The false friend is the merging of overlapping intervals from the interval chapter. Merging turns a crowd of overlapping intervals into a single block, which answers where time is covered and not how many things happen at once, so a merged schedule would report one stage for any amount of overlap. Another false friend is a check of adjacent intervals after sorting, which finds whether any overlap exists, but not how deep the overlap goes.

Do not use it when the resources are different from one another, since reusing the earliest-ending one may then break a constraint that depends on which resource it is. Do not use it when the tie rule has not been settled, because the wrong comparison changes the answer on touching endpoints. If only the count is needed and the endpoints are small integers, a difference array is simpler. In Java, sort with `Integer.compare`, test emptiness before `peek`, and decide between `<` and `<=` from the wording of the problem.

<!-- stage: exercises -->
### Exercises

#### [Build] Meeting Rooms (LeetCode 252)
<!-- id: hi-meeting-rooms -->

**Prerequisites.** The sorted start order and the half-open overlap contract of this lesson.

**Problem.** Given an array of meeting time intervals `[start, end)`, decide whether one person could attend all of them. A meeting that starts exactly when another ends does not conflict with it.

**Constraints.** 0 <= intervals.length <= 10^4 and 0 <= start < end <= 10^9.

**Example 1.** Input `intervals = [[0, 5], [5, 9], [12, 14]]`, output `true`.

**Example 2.** Input `intervals = [[1, 6], [5, 8]]`, output `false`.

**Hint.** After sorting by start, which single neighbour of an interval can reveal a conflict? Which comparison operator reflects the contract about the shared endpoint?

**Changed decision.** First rung: sort by start and settle the endpoint rule, before the heap is introduced.

#### [Vary] Meeting Rooms II (LeetCode 253)
<!-- id: hi-meeting-rooms-two -->

**Prerequisites.** Meeting Rooms above.

**Problem.** Given an array of meeting intervals `[start, end)`, return the minimum number of rooms required so that every meeting has a room for its whole duration. A meeting may begin in a room in the same minute that another one leaves it.

**Constraints.** 1 <= intervals.length <= 10^4 and 0 <= start < end <= 10^6.

**Example 1.** Input `intervals = [[2, 7], [7, 9], [3, 8], [9, 12]]`, output 2.

**Example 2.** Input `intervals = [[1, 2]]`, output 1.

**Hint.** What does the earliest finishing room tell you about every other room? What should happen to the heap when a room is reused and when it is not?

**Changed decision.** The question changes from existence of a conflict to a count of resources, so a heap of end times replaces the neighbour check.

#### [Boundary] Divide Intervals Into Minimum Number of Groups (LeetCode 2406)
<!-- id: hi-min-groups-closed -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array of closed intervals `[left, right]`, divide them into the smallest number of groups so that no two intervals in the same group intersect. Two closed intervals that share even one endpoint intersect. Return the number of groups.

**Constraints.** 1 <= intervals.length <= 10^5 and 1 <= left <= right <= 10^6.

**Example 1.** Input `intervals = [[2, 5], [5, 8], [1, 2], [8, 9]]`, output 2.

**Example 2.** Input `intervals = [[1, 1], [1, 1]]`, output 2.

**Hint.** Which comparison in the reuse test changes when the intervals are closed? What happens to a one-point interval?

**Changed decision.** The tie rule flips, so touching endpoints now conflict, and the root must be strictly smaller than the new start before it can be reused.

#### [Recognize] Minimum Interval to Include Each Query (LeetCode 1851)
<!-- id: hi-min-interval-queries -->

**Prerequisites.** All three exercises above.

**Problem.** Each interval `[left, right]` is closed, and its size is `right - left + 1`. For each query value `q`, return the size of the smallest interval that contains `q`, or -1 if none does. The answers are returned in the order of the queries.

**Constraints.** 1 <= intervals.length, queries.length <= 10^5 and 1 <= left <= right, q <= 10^7.

**Example 1.** Input `intervals = [[2, 5], [1, 3], [6, 9], [3, 3]]`, `queries = [3, 1, 6, 10, 4]`, output `[1, 3, 4, -1, 4]`.

**Example 2.** Input `intervals = [[4, 4]]`, `queries = [4, 5]`, output `[1, -1]`.

**Hint.** If the queries are handled in increasing order, which intervals can still matter? By which key should the heap be ordered, and when is an entry at the root useless?

**Changed decision.** The heap is ordered by interval size and not by end time, and entries expire at the root when their end falls below the query, so two sorted streams drive one heap.
