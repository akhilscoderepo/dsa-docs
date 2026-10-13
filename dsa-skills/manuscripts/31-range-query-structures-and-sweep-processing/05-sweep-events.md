<!-- lesson-kind: standard -->
<!-- lesson-id: sweep-events -->
## Sweep Events

<!-- stage: context -->
### Why Per-Position Checks Fail On Long Ranges

A shuttle service accepts trips. Each trip carries some passengers from a pickup marker to a drop-off marker on a road, and the bus has a fixed number of seats. Before accepting a batch, the service must answer one question: does the number of passengers on board ever exceed the seat count?

Markers can be as large as one billion, and a trip can span almost all of them. A check that visits every marker inside every trip does work proportional to the road length. That cost is far beyond a time limit, even when only a handful of trips exist.

The same failure appears when a calendar looks for double-booked rooms and when a map renderer draws building outlines. The load changes at a few known coordinates and stays constant everywhere between them. The question this lesson answers is how to look only at the coordinates where something changes.

<!-- stage: naive -->
### Add Each Trip To Every Position

The direct approach keeps one load counter per marker. For each trip, it adds the passenger count to every marker from the pickup up to, but not including, the drop-off. It stops as soon as one counter exceeds the capacity.

```java
static boolean carPoolingNaive(int[][] trips, int capacity, int maxMarker) {
    int[] load = new int[maxMarker + 1];       // one counter for every marker on the road
    for (int[] trip : trips) {
        for (int x = trip[1]; x < trip[2]; x++) {
            load[x] += trip[0];                // the trip occupies seats at x
            if (load[x] > capacity) return false;
        }
    }
    return true;
}
```

The method is correct, and it works well when the road has a few hundred markers. The answer depends only on the trips, but the cost depends on how long each trip is.

<!-- stage: bottleneck -->
### Cost Follows Trip Length, Not Trip Count

```predict
There are 1,000 trips, and each one runs from marker 0 to marker 1,000,000,000. About how many counter updates does the direct approach perform, and how many coordinates actually change the load?

About 10^12 updates, because each trip updates one billion counters. Only 2 distinct coordinates change the load, 0 and 1,000,000,000, although they hold 2,000 events, namely 1,000 pickups and 1,000 drop-offs. Everywhere else the load stays the same as at the previous coordinate.
```

#### Count The Work

With `n` trips and a longest trip of length `L`, the loop performs O(n * L) updates. The counter array also needs O(maxMarker) memory, which is a gigabyte-scale allocation for a billion markers. Both costs track the size of the coordinate range and ignore the size of the input.

#### Find The Wasted Work

Between two neighboring pickup or drop-off coordinates, no trip starts or ends. Every position in that gap has the same load, so the inner loop recomputes one number millions of times. The load at a position equals the load at the previous change coordinate plus the changes that happen exactly there. Only the change coordinates, at most 2n of them, carry information, so the work should be O(n log n) for sorting them and not O(n * L).

<!-- stage: insight -->
### Process Changes In Coordinate Order

#### Turn Each Trip Into Two Events

An **event** is a pair of a coordinate and a signed change in the active state. A trip of `p` passengers from `a` to `b` yields the event `{a, +p}` and the event `{b, -p}`. The drop-off is the exclusive end of the half-open range `[a, b)`, so the seats free up at `b`.

#### Sort Then Move Along The Line

A **sweep line** visits the events in ascending coordinate order and keeps the active state up to date. For car pooling, the state is one number, the current load. Add each delta to the load, and the load after an event is the load on the span up to the next event coordinate. Checking the load against the capacity at each step covers every position with at most 2n steps.

<!-- names: sweep line, event, tie policy -->

#### Fix A Tie Policy For Equal Coordinates

Several events can share one coordinate, for example a drop-off and a pickup at the same marker. The **tie policy** is the rule for those events. For half-open ranges, the policy applies every delta at the coordinate and only then reads the state. Ordering the deltas with decreases first and reading after each one gives the same maximum. For closed ranges, a range that ends at the coordinate still counts there, so the policy orders increases first and reads the state before the decreases apply. Without a stated policy, the load can show a peak that no position ever had.

The invariant is this. With the half-open tie policy, after the events at a coordinate are applied, the active state describes exactly the positions from this coordinate up to the next one. Every sweep line algorithm preserves that sentence, and only the kind of state changes. A counter handles a load, and a structure that reports a maximum handles heights.

<!-- stage: variables -->
### Quantities To Track While Sweeping

Track these items for the two sweeps in the code stage.

- **events** holds the pairs `{coordinate, delta}`, two per trip, sorted by coordinate and then by delta.
- **load** is the sum of all deltas applied so far, which equals the passengers on board.
- **capacity** is the fixed seat limit that `load` must never exceed.
- **e** is the event being applied, and it is the pointer in the first trace.
- **heap** holds the heights of started buildings with the greatest on top, and it starts with the ground height 0.
- **pending** counts each ended height whose value still sits inside `heap`.
- **previous** is the height of the last outline point, so a new point appears only when the top differs.

The sorted order by delta puts drop-offs, which are negative, before pickups at the same coordinate. That order is the tie policy used here. The skyline sweep sorts its events by coordinate only and applies every event at one coordinate before it reads the state. In the skyline trace, `maxHeight` is the code variable `top`, which is the top of `heap` after the discards. The trace value `pendingRemovals` is the number of ended heights still waiting in `pending`.

<!-- stage: trace -->
### Follow The Load Across Sorted Events

#### Trips With A Shared Stop

Take capacity 4 and three trips: 2 passengers from 1 to 5, 1 passenger from 3 to 6, and 3 passengers from 5 to 8. The sorted events are `{1,+2}`, `{3,+1}`, `{5,-2}`, `{5,+3}`, `{6,-1}` and `{8,-3}`.

The first two events raise the load to 2 and then 3. The two events at coordinate 5 form the tie. The drop-off of 2 runs first, so the load falls to 1, and the pickup of 3 then raises it to 4. The load equals the capacity and does not exceed it.

The remaining events lower the load to 3 and then to 0, so every trip fits. The hardest step is coordinate 5. If the pickup ran first, the load would reach 6 for a moment that no position ever has, and the answer would be wrong.

```trace
{"cells":[1,3,5,5,6,8],"pointers":["e"],"steps":[{"at":{"e":-1},"vars":{"load":0,"capacity":4},"note":"No event is applied yet, so the load is 0 and the capacity is 4."},{"at":{"e":0},"vars":{"load":2,"capacity":4},"note":"Coordinate 1 applies a pickup of 2. The load is now 2, which is at most 4."},{"at":{"e":1},"vars":{"load":3,"capacity":4},"note":"Coordinate 3 applies a pickup of 1. The load is now 3, which is at most 4."},{"at":{"e":2},"vars":{"load":1,"capacity":4},"note":"Coordinate 5 applies a drop-off of 2. The load is now 1, which is at most 4. Another event waits at the same coordinate, and this decrease runs first."},{"at":{"e":3},"vars":{"load":4,"capacity":4},"note":"Coordinate 5 applies a pickup of 3. The load is now 4, which is at most 4. This event shares its coordinate with the previous one, and the decrease ran first."},{"at":{"e":4},"vars":{"load":3,"capacity":4},"note":"Coordinate 6 applies a drop-off of 1. The load is now 3, which is at most 4."},{"at":{"e":5},"vars":{"load":0,"capacity":4},"note":"Coordinate 8 applies a drop-off of 3. The load is now 0, which is at most 4."}]}
```

#### Buildings With Shared Edges

A skyline problem gives buildings `[left, right)` with a height. The outline lists a key point `(x, height)` wherever the greatest active height changes, and the last key point has height 0. The state of this sweep is the maximum of the active heights, so it must forget a height when its building ends. A max-heap gives the maximum, but removing an arbitrary value costs O(n). Lazy deletion avoids that: an ended height is only counted as a pending removal and leaves the heap when it reaches the top. Take buildings `[2,6)` of height 3, `[4,6)` of height 5 and `[6,9)` of height 2.

At coordinate 2 the maximum rises from 0 to 3, so the outline gets a key point `(2,3)`. At coordinate 4 it rises to 5, giving `(4,5)`. At coordinate 6 two buildings end and one starts, and all three events are applied before the maximum is read. The maximum becomes 2, giving `(6,2)`. At coordinate 9 the last building ends and the outline returns to height 0.

The ended heights 5 and 3 are not deleted from the heap at once. They are recorded as pending removals and discarded when they reach the top, which the trace shows at coordinate 6.

```trace
{"cells":[2,4,6,9],"pointers":["x"],"steps":[{"at":{"x":-1},"vars":{"maxHeight":0,"pendingRemovals":0},"note":"The heap holds only the ground height 0, and no removal is pending."},{"at":{"x":0},"vars":{"maxHeight":3,"pendingRemovals":0},"note":"Coordinate 2 adds heights [3] and ends heights none. The maximum is 3, so the outline gets the key point (2,3)."},{"at":{"x":1},"vars":{"maxHeight":5,"pendingRemovals":0},"note":"Coordinate 4 adds heights [5] and ends heights none. The maximum is 5, so the outline gets the key point (4,5)."},{"at":{"x":2},"vars":{"maxHeight":2,"pendingRemovals":0},"note":"Coordinate 6 adds heights [2] and ends heights [3, 5]. The top values [5, 3] are pending removals, so they leave the heap. The maximum is 2, so the outline gets the key point (6,2)."},{"at":{"x":3},"vars":{"maxHeight":0,"pendingRemovals":0},"note":"Coordinate 9 adds heights none and ends heights [2]. The top values [2] are pending removals, so they leave the heap. The maximum is 0, so the outline gets the key point (9,0)."}]}
```

<!-- stage: code -->
### Sweep Trips And Buildings In Java

```java
static boolean carPooling(int[][] trips, int capacity) {
    int[][] events = new int[trips.length * 2][];
    int k = 0;
    for (int[] t : trips) {
        events[k++] = new int[]{t[1], t[0]};      // pickup adds passengers
        events[k++] = new int[]{t[2], -t[0]};     // drop-off removes them at the exclusive end
    }
    // Integer.compare states the order directly and cannot overflow.
    Arrays.sort(events, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(p[1], q[1]));
    long load = 0;
    for (int[] e : events) {
        load += e[1];                              // apply one delta under the decreases-first policy
        if (load > capacity) return false;
    }
    return true;
}

static List<int[]> skyline(int[][] buildings) {
    int[][] events = new int[buildings.length * 2][];
    int k = 0;
    for (int[] b : buildings) {
        events[k++] = new int[]{b[0], b[2]};      // positive height means the building starts
        events[k++] = new int[]{b[1], -b[2]};     // negative height means the building ends
    }
    Arrays.sort(events, (p, q) -> Integer.compare(p[0], q[0]));
    PriorityQueue<Integer> heap = new PriorityQueue<>(Comparator.reverseOrder());
    Map<Integer, Integer> pending = new HashMap<>();   // heights ended but still inside the heap
    heap.add(0);                                       // ground level is always active
    List<int[]> outline = new ArrayList<>();
    int previous = 0, i = 0;
    while (i < events.length) {
        int x = events[i][0];
        while (i < events.length && events[i][0] == x) {   // apply every event at this coordinate first
            int h = events[i++][1];
            if (h > 0) heap.add(h);
            else pending.merge(-h, 1, Integer::sum);
        }
        while (pending.getOrDefault(heap.peek(), 0) > 0)   // discard ended heights that reached the top
            pending.merge(heap.poll(), -1, Integer::sum);
        int top = heap.peek();
        if (top != previous) { outline.add(new int[]{x, top}); previous = top; }
    }
    return outline;
}
```

The first method reads the state after each delta, so its tie policy is the sort order. The second method applies a whole group of equal coordinates before it reads the state, so its tie policy is grouping. The `PriorityQueue` removes its top in O(log n) time, but removing an arbitrary value needs a linear search. Lazy deletion avoids that search. It counts each ended height in `pending` and removes a heap value only when that value is at the top and its count is positive. Each height enters and leaves the heap once, so the total heap work is O(n log n).

<!-- stage: applicability -->
### When A Sweep Line Applies

#### Recognize The Pattern

Use a sweep line when the state changes only at known coordinates or times. The question must also concern the state between those coordinates, such as a maximum load, a covered length or an outline. Typical cases are overlapping intervals, meeting room counts, capacity limits and skyline outlines.

The invariant to carry through the code is that the state always describes the span from the current coordinate to the next one. State it before choosing the structure. A counter is enough when only a total matters. A heap with lazy deletion, or a `TreeMap` of height counts, is needed when the maximum matters.

#### Avoid The False Friend

A difference array looks like a close relative, because both add a delta at the start and subtract it at the end. That false friend works only when coordinates are small and dense, because it allocates one cell per coordinate. It fails for markers near a billion. Coordinate compression, from the previous lesson, shrinks the coordinates and makes an array usable again, while the sweep line needs no array at all.

#### Watch The Java Hazards

Sorting with a comparator such as `p[0] - q[0]` overflows when coordinates have opposite signs and large magnitude, so use `Integer.compare`. The coordinates here stay between 0 and 10^9, where subtraction would still fit, but negative inputs make the habit necessary. A tie policy that disagrees with the range convention gives wrong answers on touching intervals, and no test with distinct coordinates reveals it. Test every sweep with two events at one coordinate.

<!-- stage: exercises -->
### Exercises

#### [Build] Car Pooling (LeetCode 1094)
<!-- id: rq31-car-pooling -->

**Prerequisites.** The events, load and tie policy from this lesson.

**Problem.** A vehicle has `capacity` seats. A list of trips is given, where trip `i` is `[passengers, from, to]`. The passengers occupy seats on the half-open range `[from, to)`, so they leave at `to` before any passenger who boards at `to`. Return `true` if the number of occupied seats never exceeds `capacity` at any position, and `false` otherwise.

**Constraints.** The limits are:
- **Trips** number between 1 and 10^4.
- **Passengers** per trip are an `int` between 1 and 100.
- **Positions** satisfy `0 <= from < to <= 10^9`.
- **Capacity** is an `int` between 1 and 10^5.
- **Input** arrays are read only, and the return value is a `boolean`.

**Example 1.** Input trips [[2,1,5],[3,3,7]] and capacity 4, output `false`, because positions 3 and 4 carry 2 + 3 = 5 passengers.

**Example 2.** Input trips [[2,1,5],[3,5,7]] and capacity 3, output `true`, because the 2 passengers leave at 5 as the 3 passengers board.

**Hint.** What are the two events of a trip, and which one runs first when two share a coordinate?

**Changed decision.** Baseline case: replaces the per-position load array with two signed events per trip.

#### [Vary] Group Equal Coordinates (Author exercise)
<!-- id: rq31-group-equal-coordinates -->

**Prerequisites.** The Car Pooling exercise above.

**Problem.** Given half-open intervals `[start, end)`, return the maximal covered spans in ascending order. A span `[a, b)` is maximal when every position in it lies inside at least one interval and no position just before `a` or at `b` does. Intervals that touch at a coordinate belong to one span.

**Constraints.** The limits are:
- **Intervals** number between 0 and 10^5.
- **Coordinates** are `int` values with `-10^9 <= start < end <= 10^9`.
- **Output** is a list of `[a, b]` pairs, empty when there are no intervals.
- **Input** may be unsorted and may contain duplicates.

**Example 1.** Input [[1,3],[3,5],[7,9]], output [[1,5],[7,9]], because `[1,3)` and `[3,5)` touch at 3 and form one span.

**Example 2.** Input [[4,6],[1,2],[3,4]], output [[1,2],[3,6]], because position 2 is uncovered and separates the first two spans.

**Hint.** What is the coverage count after all events at one coordinate have run, and when does it change between zero and positive?

**Changed decision.** The state is a count that is read once per distinct coordinate, so all deltas at a coordinate are applied before the read.

#### [Boundary] Start-End Tie (Author exercise)
<!-- id: rq31-start-end-tie -->

**Prerequisites.** The two exercises above.

**Problem.** Given intervals `[start, end]` with integer endpoints and a flag `closed`, return the largest number of intervals that are active at the same integer position. If `closed` is true, an interval contains both endpoints. If `closed` is false, it contains `start` and excludes `end`.

**Constraints.** The limits are:
- **Intervals** number between 1 and 10^5.
- **Endpoints** are `int` values with `-10^9 <= start < end <= 10^9`.
- **Flag** `closed` selects the endpoint convention for every interval.
- **Return** value is an `int`.

**Example 1.** Input [[1,3],[3,5]], output 2 when `closed` is true and 1 when `closed` is false, because position 3 belongs to both intervals only in the closed case.

**Example 2.** Input [[1,4],[2,6],[4,8]], output 3 when `closed` is true and 2 when `closed` is false, because the first interval contains position 4 only in the closed case.

**Hint.** At one coordinate, should the interval that starts or the interval that ends run first for each convention?

**Changed decision.** Only the endpoint convention changes, and it reverses the order of increases and decreases at equal coordinates.

#### [Recognize] The Skyline Problem (LeetCode 218)
<!-- id: rq31-skyline -->

**Prerequisites.** All three exercises above.

**Problem.** Each building is `[left, right, height]` and covers the half-open range `[left, right)`. Return the outline as a list of key points `[x, height]` in ascending `x`. A key point is the left end of a horizontal segment, and it appears only where the maximum height changes. The last key point has height 0.

**Constraints.** The limits are:
- **Buildings** number between 0 and 10^4.
- **Coordinates** satisfy `0 <= left < right <= 10^9`.
- **Heights** are `int` values between 1 and 10^9.
- **Output** has no two consecutive key points with the same height.

**Example 1.** Input [[2,6,3],[4,6,5],[6,9,2]], output [[2,3],[4,5],[6,2],[9,0]], because the shared edge at 6 changes the maximum from 5 to 2.

**Example 2.** Input [[0,3,4],[2,5,4]], output [[0,4],[5,0]], because the two buildings of height 4 overlap and produce no key point at 3.

**Hint.** Which structure reports the largest active height, and how can it forget a building that has ended?

**Changed decision.** The state is the maximum of a changing set and not a counter, so removing an ended height needs lazy deletion.
