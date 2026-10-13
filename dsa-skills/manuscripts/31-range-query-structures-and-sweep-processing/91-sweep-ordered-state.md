<!-- lesson-kind: combination -->
<!-- lesson-id: sweep-ordered-state -->
## Sweep And Ordered State

<!-- stage: context -->
### Finding The First Moment Of Overload

A licence server allows at most 4 simultaneous sessions. Its log holds one record per session with a user count, a start time and an end time. The times are integers up to one billion. An operator asks for the first time at which the licence limit is exceeded.

Checking every possible time is impossible, because one billion times is too many. Checking only the start times is possible, but each check must add up every session that is active at that time. A log with 100,000 sessions makes that repeated addition slow.

A second report asks for the tallest stack of overlapping jobs, and a third asks how many bookings overlap at the busiest moment. Each report has the same shape. The answer depends only on the instants at which something starts or ends.

Formally, the input is a list of half-open intervals `[start, end)` with weights. The task is to report a maximum, or the first point where a sum passes a limit. This lesson asks how to read the instants in sorted order and keep just enough state to answer without rescanning.

<!-- stage: contributions -->
### What Earlier Lessons Contribute

#### Event Sweeps Supply The Order

The sweep-events lesson turned each interval into two events, a coordinate paired with a change. It sorted the events by coordinate and applied them one after another. The state between two neighbouring coordinates is constant, so one evaluation per coordinate is enough. This lesson reuses that order and adds a data structure to hold the state.

#### Compression Supplies Only The Needed Coordinates

The compression lesson replaced sparse values with dense ranks, because only the relative order of the coordinates matters. A sweep has the same property. Only coordinates where an event occurs can change the answer, so a billion possible times shrink to at most 2n relevant ones. An ordered map keeps those coordinates sorted without a separate rank table.

#### Tree Structures Answer Interleaved Queries

The Fenwick and segment tree lessons answered range questions while values changed at fixed positions. They are the right tool when queries ask about arbitrary ranges between updates. A sweep asks one fixed question at each coordinate in order. A sorted map then suffices, and the applicability part names the case where a tree is needed instead.

#### The Ordered Map

A `TreeMap` is the Java sorted map. It keeps its keys in increasing order and inserts, finds and removes a key in O(log n) time. It also offers `firstKey`, `lastKey` and iteration in key order. The combination of sorted events and a sorted map is the whole subject of this lesson.

<!-- stage: naive -->
### Adding Up Every Session At Every Start

The direct approach collects all coordinates, sorts them and recomputes the load at each one by testing every trip. The routine below returns the first coordinate where the load passes the capacity.

```java
static int firstOverloadByScan(int[][] trips, int capacity) {
    int[] stops = new int[trips.length];
    for (int i = 0; i < trips.length; i++) stops[i] = trips[i][1];
    java.util.Arrays.sort(stops);
    for (int x : stops) {
        long load = 0;
        for (int[] t : trips) if (t[1] <= x && x < t[2]) load += t[0];
        if (load > capacity) return x;
    }
    return -1;
}
```

The routine is correct. The load can only rise at a start, so checking each start is enough. The inner loop reads all n trips for each of n starts. That is the cost to reduce.

<!-- stage: bottleneck -->
### Rescanning Trips Costs Too Much

```predict
A log holds 100,000 sessions. The routine above tests every session at each of the 100,000 start times. About how many interval tests does it run?

About 10^10 tests, which is O(n^2). Each start re-reads every session, although moving from one start to the next changes the active set by only a few sessions.
```

#### Count The Repeated Work

The scan performs n tests for each of n starts, so it runs in O(n^2) time. For `n = 100,000` that is 10^10 tests, far beyond a one-second limit. The work is repeated, because two neighbouring starts share almost the same active sessions. The scan throws that sharing away and recomputes the load from nothing.

#### Count The Cost Of Removal

Reading the maximum of an active set is also hard. Take the skyline task, where each building has a height and the answer at each coordinate is the greatest active height. A single variable `maxHeight` works while heights only arrive. When the tallest building ends, the variable cannot say which height is next. An unsorted list of active heights fixes that but costs O(n) to search and O(n) to delete from. The target is O(log n) per event, which gives O(n log n) for the whole sweep.

<!-- stage: insight -->
### Keep Net Changes In A Sorted Map

#### Store Net Changes In A Delta Map

Keep a **delta map**, which is a `TreeMap` from coordinate to the net change in weight at that coordinate. A trip adds its passengers at its start key and subtracts them at its end key. Adding to an existing key merges the two changes into one value. Reading the map in key order and keeping a running sum gives the load on every span, with no sorting step of its own.

<!-- names: delta map, active multiset, tie policy -->

#### Store Active Values In An Active Multiset

Some answers need the extreme of the currently active values and not their sum. For that, keep an **active multiset**, which is a `TreeMap` from value to the number of active items with that value. Java has no multiset class, so the count plays that role. Inserting a height increments its count. Removing one decrements the count and deletes the key at zero. `lastKey` then returns the greatest active height in O(log n) time, even after the tallest building ends.

#### Fix A Tie Policy

Events at one coordinate need a **tie policy**, which is the rule for the order in which they are applied and when the state is read. For half-open intervals `[start, end)`, all changes at coordinate `x` apply before the state is read, so an ending interval and a starting interval at `x` never overlap. For closed intervals `[start, end]`, an interval that ends at `x` still counts at `x`, so the starts at `x` apply first and the state is read before the ends apply. A delta map merges all changes at one key, so it fits only the half-open rule. A closed integer interval fits it after the end moves to `end + 1`. The tie policy follows from the interval contract and is chosen before any code.

Under the half-open rule the invariant is the same for both structures. After all events at coordinate `x` are applied, the state describes exactly the span from `x` up to the next event coordinate.

<!-- stage: variables -->
### Quantities To Track During The Sweep

Track these seven quantities across the sweeps in this lesson.

- **delta map** holds the net change in weight at each event coordinate, in sorted order.
- **load** is the running sum of the deltas applied so far, kept as a `long`.
- **active multiset** maps each active height to the number of active buildings with it.
- **height** is the greatest key of the active multiset after a coordinate, or 0 when it is empty.
- **best height** is the greatest height seen so far.
- **best x** is the coordinate where the best height first appeared.
- **end x** is the first later coordinate whose height is lower than the best height, and it stays -1 while the stretch is open.

In the code, the delta map is the variable `change`, and the active multiset is the variable `active`. In the second trace, `bestH`, `bestX` and `endX` are best height, best x and end x. The names differ only because the code and trace use short identifiers.

<!-- stage: trace -->
### Two Sweeps Step By Step

#### Overload Check With Merged Changes

Take capacity 4 and four trips written as passengers, from, to: (2, 1, 4), (1, 2, 6), (2, 4, 8) and (3, 6, 9). The delta map holds +2 at 1, +1 at 2, 0 at 4, +2 at 6, -2 at 8 and -3 at 9.

The value at key 4 is zero, because the first trip ends there and the third trip starts there. That merge is the half-open tie policy at work. The load stays 3 across coordinate 4, and no false drop or spike appears.

The sweep adds +2 to reach 2, adds +1 to reach 3, keeps 3 at key 4 and adds +2 to reach 5 at key 6. Since 5 exceeds 4, the sweep returns coordinate 6 and stops.

```trace
{"cells":[1,2,4,6,8,9],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"load":0,"change":0},"note":"Nothing is applied yet. The load is 0."},{"at":{"i":0},"vars":{"load":2,"change":2},"note":"Coordinate 1 carries the merged change +2. The load becomes 2."},{"at":{"i":1},"vars":{"load":3,"change":1},"note":"Coordinate 2 carries the merged change +1. The load becomes 3."},{"at":{"i":2},"vars":{"load":3,"change":0},"note":"Coordinate 4 carries the merged change +0. The load becomes 3."},{"at":{"i":3},"vars":{"load":5,"change":2},"note":"Coordinate 6 carries the merged change +2. The load becomes 5. That exceeds the capacity 4, so the sweep returns 6 and stops."}]}
```

#### Tallest Stretch With Touching Buildings

Take four buildings written as left, right, height: (1, 6, 3), (4, 9, 5), (6, 8, 2) and (8, 11, 5). The event coordinates are 1, 4, 6, 8, 9 and 11.

At coordinate 4 the height 5 appears for the first time, so best height is 5 and best x is 4. At coordinate 6 the height 3 ends and the height 2 starts, and the greatest key stays 5. At coordinate 8 the height 2 ends and a second height 5 starts, so the count for key 5 becomes 2.

At coordinate 9 the first height 5 ends. The count for key 5 drops from 2 to 1, so the key stays and the height is still 5. Without counts, the key would vanish and the sweep would report a false drop. At coordinate 11 the last building ends, the map is empty, and the stretch closes with end x equal to 11.

```trace
{"cells":[1,4,6,8,9,11],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"height":0,"bestH":0,"bestX":-1,"endX":-1},"note":"No event is applied yet. The active multiset is empty."},{"at":{"i":0},"vars":{"height":3,"bestH":3,"bestX":1,"endX":-1},"note":"After the events at 1, the active heights are {3: 1} and the height is 3. This is a new best, so best x is 1."},{"at":{"i":1},"vars":{"height":5,"bestH":5,"bestX":4,"endX":-1},"note":"After the events at 4, the active heights are {3: 1, 5: 1} and the height is 5. This is a new best, so best x is 4."},{"at":{"i":2},"vars":{"height":5,"bestH":5,"bestX":4,"endX":-1},"note":"After the events at 6, the active heights are {2: 1, 5: 1} and the height is 5."},{"at":{"i":3},"vars":{"height":5,"bestH":5,"bestX":4,"endX":-1},"note":"After the events at 8, the active heights are {5: 2} and the height is 5."},{"at":{"i":4},"vars":{"height":5,"bestH":5,"bestX":4,"endX":-1},"note":"After the events at 9, the active heights are {5: 1} and the height is 5."},{"at":{"i":5},"vars":{"height":0,"bestH":5,"bestX":4,"endX":11},"note":"After the events at 11, the active heights are {} and the height is 0. The height is below the best, so end x is 11."}]}
```

<!-- stage: code -->
### Two Sweep Methods With TreeMap

```java
static long peakLoad(int[][] trips) {
    java.util.TreeMap<Integer, Long> change = new java.util.TreeMap<>();
    for (int[] t : trips) {
        change.merge(t[1], (long) t[0], Long::sum);
        change.merge(t[2], -(long) t[0], Long::sum);
    }
    long load = 0, peak = 0;
    for (long delta : change.values()) {
        load += delta;
        peak = Math.max(peak, load);
    }
    return peak;
}

static int firstOverload(int[][] trips, int capacity) {
    java.util.TreeMap<Integer, Long> change = new java.util.TreeMap<>();
    for (int[] t : trips) {
        change.merge(t[1], (long) t[0], Long::sum);
        change.merge(t[2], -(long) t[0], Long::sum);
    }
    long load = 0;
    for (var entry : change.entrySet()) {
        load += entry.getValue();                  // the merged change is applied as one step
        if (load > capacity) return entry.getKey();   // the load holds until the next key
    }
    return -1;
}

static void addHeight(java.util.TreeMap<Integer, Integer> active, int h) {
    active.merge(h, 1, Integer::sum);
}

static void removeHeight(java.util.TreeMap<Integer, Integer> active, int h) {
    if (active.merge(h, -1, Integer::sum) == 0) active.remove(h);
}

static int greatestHeight(java.util.TreeMap<Integer, Integer> active) {
    return active.isEmpty() ? 0 : active.lastKey();
}

static int[] tallestStretch(int[][] buildings) {
    java.util.TreeMap<Integer, java.util.List<int[]>> at = new java.util.TreeMap<>();
    for (int[] b : buildings) {
        at.computeIfAbsent(b[0], k -> new java.util.ArrayList<>()).add(new int[]{b[2], 1});
        at.computeIfAbsent(b[1], k -> new java.util.ArrayList<>()).add(new int[]{b[2], -1});
    }
    java.util.TreeMap<Integer, Integer> active = new java.util.TreeMap<>();
    int bestH = 0, bestX = -1, endX = -1;
    for (var group : at.entrySet()) {
        for (int[] ev : group.getValue()) {          // apply the whole group before reading
            if (ev[1] == 1) addHeight(active, ev[0]); else removeHeight(active, ev[0]);
        }
        int height = greatestHeight(active);
        if (height > bestH) { bestH = height; bestX = group.getKey(); endX = -1; }   // a new best opens a stretch
        else if (height < bestH && endX == -1) endX = group.getKey();           // the first lower height closes it
    }
    return new int[]{bestH, bestX, endX};
}
```

The method `peakLoad` needs only the values of the delta map, because the keys matter for order and not for arithmetic. The method `firstOverload` also reads the keys, because it returns the coordinate where the load first passes the capacity. The three helpers wrap the multiset operations, and `removeHeight` is the single place where a key disappears, when its count reaches zero. The method `tallestStretch` applies every event at one coordinate before it reads `greatestHeight`. Each map operation costs O(log n), so a sweep over 2n events costs O(n log n) in total.

<!-- stage: applicability -->
### When To Sweep With Ordered State

#### Recognize The Pattern

Reach for this combination when each item is an interval with a weight or a value. The question asks for a maximum, a total or a first violation over all points. The answer then changes only at interval boundaries. Car loads, overlapping bookings and skylines share that cue.

The invariant is that the state after each coordinate describes the span up to the next coordinate. If the question instead asks about an arbitrary query range between updates, the answer depends on the query and a Fenwick or segment tree is the better fit.

#### Choose The Tie Policy From The Contract

Read whether the end coordinate belongs to the interval. Half-open ends apply with starts at one coordinate before the state is read. Closed ends need starts first and the state read before the ends apply. A skipped decision here produces off-by-one answers that pass most random tests and fail on touching intervals.

#### Avoid The False Friend

A single running maximum is a false friend of the active multiset. It looks like enough state, but it cannot recover the next value when the current maximum leaves. A `PriorityQueue` is a related trap, because its `remove(Object)` call costs O(n) in Java. A `TreeMap` of counts removes in O(log n).

One Java hazard remains. Sums of weights can pass `int` range, so use `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] First Overloaded Stop (LeetCode 1094)
<!-- id: rq31-first-overload-stop -->

**Prerequisites.** The delta map and the half-open tie policy from this lesson.

**Problem.** A vehicle has `capacity` seats. Each trip is `[passengers, from, to]`. The riders of a trip occupy seats at every integer coordinate `x` with `from <= x < to`. The load at `x` is the sum of `passengers` over all trips that occupy `x`. Return the smallest integer coordinate whose load is greater than `capacity`. Return -1 if no coordinate has such a load.

**Constraints.** The limits are:
- **Trips** number between 1 and 100,000, and the order is arbitrary.
- **`passengers`** is an `int` from 1 to 100.
- **Coordinates** satisfy `0 <= from < to <= 1,000,000,000`.
- **`capacity`** is an `int` from 1 to 1,000,000,000.
- **Input** is not modified.

**Example 1.** Input capacity 4 and trips `[[2,1,5],[3,3,7],[4,5,9]]`, output 3, because the load at coordinate 3 is 2 + 3 = 5.

**Example 2.** Input capacity 3 and trips `[[3,1,4],[3,4,7]]`, output -1, because the first trip frees its seats at coordinate 4 before the second trip fills them.

**Hint.** Where can the load change? What happens to a drop-off and a pickup at the same coordinate?

**Changed decision.** The original asks whether the capacity is ever exceeded. This version returns the first coordinate where it is exceeded.

#### [Vary] Tallest Stretch Of A Skyline (LeetCode 218)
<!-- id: rq31-skyline-tallest -->

**Prerequisites.** The active multiset and the first exercise.

**Problem.** Each building is `[left, right, height]` and covers every integer coordinate `x` with `left <= x < right`. The skyline height at `x` is the greatest height among the buildings that cover `x`, or 0 if none covers it. Let `M` be the greatest skyline height over all `x`. Return `[M, a, b]`, where `a` is the smallest coordinate with skyline height `M` and `b` is the smallest coordinate greater than `a` with skyline height below `M`.

**Constraints.** The limits are:
- **Buildings** number between 1 and 100,000, and the order is arbitrary.
- **Coordinates** satisfy `0 <= left < right <= 1,000,000,000`.
- **`height`** is an `int` from 1 to 1,000,000,000.
- **Equal heights** may occur, and buildings may touch at an endpoint.
- **Input** is not modified.

**Example 1.** Input `[[1,5,7],[2,4,9],[3,8,9],[6,10,4]]`, output `[9,2,8]`, because the two buildings of height 9 overlap on [3,4) and together cover [2,8).

**Example 2.** Input `[[1,4,6],[2,3,6]]`, output `[6,1,4]`, because one building of height 6 still covers coordinate 3 after the other ends.

**Hint.** What must the active structure remember when two buildings share a height? When is the skyline height read at a coordinate?

**Changed decision.** The original lists every point where the skyline changes. This version reports only the first stretch at the greatest height, which makes equal heights and touching ends decisive.

#### [Boundary] Equal-Coordinate Events (Author exercise)
<!-- id: rq31-equal-coordinate-events -->

**Prerequisites.** The tie policy from this lesson.

**Problem.** Given integer intervals `[start, end]` and a flag `closed`, return the largest number of intervals that contain one common integer coordinate, and the smallest coordinate where that number occurs. When `closed` is true, an interval contains every `x` with `start <= x <= end`. When `closed` is false, it contains every `x` with `start <= x < end`, so an interval with `start == end` contains nothing.

**Constraints.** The limits are:
- **Intervals** number between 1 and 100,000, and the order is arbitrary.
- **Coordinates** satisfy `0 <= start <= end <= 1,000,000,000`.
- **`closed`** is a `boolean` that applies to every interval.
- **Result** is an `int[]` of the form `{count, coordinate}`, and `{0, -1}` is possible when `closed` is false and all intervals are empty.

**Example 1.** Input `[[1,3],[3,5]]`, output `{1, 1}` when `closed` is false and `{2, 3}` when `closed` is true.

**Example 2.** Input `[[2,6],[6,9],[4,6],[6,6]]`, output `{2, 4}` when `closed` is false and `{4, 6}` when `closed` is true.

**Hint.** At one coordinate, should a start or an end come first? When does the running load first reach its maximum?

**Changed decision.** The interval contract changes between the two calls, and the result also names the first coordinate of the maximum, so the event order at equal coordinates must change with it and the load must be read at the right moment.

#### [Recognize] Busiest Moment After Each Booking (LeetCode 732)
<!-- id: rq31-calendar-busiest -->

**Prerequisites.** The delta map and all three exercises above.

**Problem.** Design a class with a method `int[] book(int start, int end)`. Each call adds the booking `[start, end)`. It returns `[k, x]`, where `k` is the largest number of bookings so far that cover one integer coordinate, and `x` is the smallest coordinate covered by `k` bookings.

**Constraints.** The limits are:
- **Calls** number at most 400.
- **Coordinates** satisfy `0 <= start < end <= 1,000,000,000`.
- **Bookings** stay stored, and none is ever removed.
- **Touching** bookings, where one `end` equals another `start`, do not overlap.

**Example 1.** Input the calls `book(4,8)`, `book(8,12)`, `book(6,10)`, `book(1,5)`, output `[1,4]`, `[1,4]`, `[2,6]`, `[2,4]`.

**Example 2.** Input the calls `book(3,9)`, `book(9,14)`, `book(1,3)`, output `[1,3]`, `[1,3]`, `[1,1]`, because touching bookings never overlap.

**Hint.** What does a booking add to the map? How is the leftmost coordinate of the maximum kept during the pass?

**Changed decision.** The original returns only the maximum. This version also returns the leftmost coordinate that reaches it.
