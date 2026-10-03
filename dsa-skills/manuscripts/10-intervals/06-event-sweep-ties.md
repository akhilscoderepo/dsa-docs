<!-- lesson-kind: standard -->
<!-- lesson-id: event-sweep-ties -->
## Event Sweep Ties

<!-- stage: context -->
### How Many Kettles At Once

A tea festival lends electric kettles to its stalls, and every stall books a kettle for a block of time, such as from minute 10 to minute 40. The festival electrician is worried about the wiring, because the fuse board can supply only so many kettles at the same moment. She does not care which stalls clash or how the blocks merge into longer ones. She needs one number: the most kettles that are ever running together.

The bookings come in a messy pile and some of them touch. One stall returns its kettle at minute 40 and the next collects one at minute 40. Whether those two count as overlapping decides whether the board is overloaded at that exact minute, so the electrician must know how the festival defines a booking before she can trust any number.

<!-- stage: naive -->
### Count Kettles At Each Start

The direct approach is to take the start of every booking as a candidate minute, count how many bookings are running at that minute, and keep the largest count.

```java
static int mostKettlesAtOnce(int[][] bookings) {
    int best = 0;
    for (int[] probe : bookings) {
        int minute = probe[0];
        int running = 0;
        for (int[] b : bookings) {
            if (b[0] <= minute && minute < b[1]) running++;
        }
        best = Math.max(best, running);
    }
    return best;
}
```

It is correct because the busiest moment always falls on the start of some booking, so one of the probes lands on it.

<!-- stage: bottleneck -->
### Each Probe Rescans Every Booking

With n bookings the outer loop picks n probe minutes and the inner loop reads all n bookings for each, so the cost is O(n^2). A festival with a hundred thousand bookings needs ten billion checks, and most of them re-ask a question whose answer barely changed from the previous probe. Moving from one probe minute to the next adds a few bookings that just began and removes a few that just ended, yet the inner loop throws that knowledge away and counts from nothing.

The wasted effort comes from asking "how many are running now" as an independent question each time. The number only changes at the instants when a booking begins or ends, and it changes by exactly one each time. If those instants are visited in time order, the count can be updated in constant time per instant, and the whole answer costs O(n log n) for the sort and one linear walk after it.

<!-- stage: insight -->
### Turn Bookings Into Signed Moments

Replace each interval by two entries in an **event stream**: a start entry worth plus one at the start coordinate, and an end entry worth minus one at the end coordinate. Sort the whole stream by coordinate and walk it, adding each entry's value to a counter. After each entry the counter holds the number of intervals active at that point of the walk, and the answer is the largest value the counter ever reached.

The only delicate part is what happens when several entries share a coordinate. The sorted order inside such a group is the **tie order**, and it is a decision taken from the endpoint contract, not an accident of the sort. For half-open intervals a booking that ends at a coordinate is already gone when another one starts there, so end entries come first. For closed intervals both bookings are alive at the shared coordinate, so start entries come first, and the counter is allowed to reach the higher value for an instant.

The invariant is that the **running count** equals the number of intervals active after all entries before the current position, in tie order, have been applied. Ordering by coordinate guarantees that no entry from the future has been applied, and the tie order decides which same-coordinate entries count as already applied. A different input order can then never change the answer, because the sort fixes the order completely.

<!-- names: event stream, tie order, running count -->

Sorting the start values and the end values as two separate lists can also find the maximum, but it hides the tie policy inside a comparison, and it cannot carry weights or several kinds of entry.

<!-- stage: variables -->
### One Counter Over Sorted Entries

Each entry is a pair `{coordinate, delta}` with `delta` equal to plus one or minus one, and `active` is the counter. The answer `peak` is the maximum of `active` after any entry. Entries are ordered by coordinate first and by delta second, ascending for half-open intervals so that minus one comes before plus one, and descending for closed intervals. When a task needs the first coordinate where the counter reaches a limit, `active` is tested only after the last entry of a coordinate group, so a transient value inside the group is never reported.

<!-- stage: trace -->
### Sweeping The Sorted Entries

Both traces use the bookings 1 to 4, 2 to 5, 4 to 7 and 5 to 8. The first trace treats them as half-open. The cells show each entry as its coordinate and a sign, in tie order, and `e` points at the entry being applied. Look at the entries at coordinate 4: the end comes first, so the counter drops to one before the new start lifts it back to two.

```trace
{"cells":["1+","2+","4-","4+","5-","5+","7-","8-"],"pointers":["e"],"steps":[{"at":{"e":0},"vars":{"active":1,"peak":1},"note":"The start entry at coordinate 1 moves the counter to 1, and the peak so far is 1."},{"at":{"e":1},"vars":{"active":2,"peak":2},"note":"The start entry at coordinate 2 moves the counter to 2, and the peak so far is 2."},{"at":{"e":2},"vars":{"active":1,"peak":2},"note":"The end entry at coordinate 4 comes first and moves the counter down to 1, and the peak so far is 2."},{"at":{"e":3},"vars":{"active":2,"peak":2},"note":"The start entry at coordinate 4 moves the counter to 2, and the peak so far is 2."},{"at":{"e":4},"vars":{"active":1,"peak":2},"note":"The end entry at coordinate 5 moves the counter to 1, and the peak so far is 2."},{"at":{"e":5},"vars":{"active":2,"peak":2},"note":"The start entry at coordinate 5 moves the counter to 2, and the peak so far is 2."},{"at":{"e":6},"vars":{"active":1,"peak":2},"note":"The end entry at coordinate 7 moves the counter to 1, and the peak so far is 2."},{"at":{"e":7},"vars":{"active":0,"peak":2},"note":"The end entry at coordinate 8 moves the counter to 0, and the peak so far is 2."}]}
```

The second trace uses the same bookings as closed ranges, so the starts go first within each coordinate. The cells now show a plus before a minus at coordinates 4 and 5. Because the bookings 1 to 4 and 4 to 7 share the value 4, the counter reaches three there, which the half-open sweep never reached, and this one extra overlap is the entire difference between the two contracts.

```trace
{"cells":["1+","2+","4+","4-","5+","5-","7-","8-"],"pointers":["e"],"steps":[{"at":{"e":0},"vars":{"active":1,"peak":1},"note":"The start entry at coordinate 1 moves the counter to 1, and the peak so far is 1."},{"at":{"e":1},"vars":{"active":2,"peak":2},"note":"The start entry at coordinate 2 moves the counter to 2, and the peak so far is 2."},{"at":{"e":2},"vars":{"active":3,"peak":3},"note":"The start entry at coordinate 4 moves the counter to 3, and the peak so far is 3."},{"at":{"e":3},"vars":{"active":2,"peak":3},"note":"The end entry at coordinate 4 moves the counter to 2, and the peak so far is 3."},{"at":{"e":4},"vars":{"active":3,"peak":3},"note":"The start entry at coordinate 5 moves the counter to 3, and the peak so far is 3."},{"at":{"e":5},"vars":{"active":2,"peak":3},"note":"The end entry at coordinate 5 moves the counter to 2, and the peak so far is 3."},{"at":{"e":6},"vars":{"active":1,"peak":3},"note":"The end entry at coordinate 7 moves the counter to 1, and the peak so far is 3."},{"at":{"e":7},"vars":{"active":0,"peak":3},"note":"The end entry at coordinate 8 moves the counter to 0, and the peak so far is 3."}]}
```

<!-- stage: code -->
### Build Entries And Sweep Them

```java
static int[][] entriesFor(int[][] intervals, boolean closed) {
    int[][] entries = new int[intervals.length * 2][];
    for (int i = 0; i < intervals.length; i++) {
        entries[2 * i] = new int[] {intervals[i][0], +1};
        entries[2 * i + 1] = new int[] {intervals[i][1], -1};
    }
    Arrays.sort(entries, (a, b) -> a[0] != b[0]
            ? Integer.compare(a[0], b[0])
            : (closed ? Integer.compare(b[1], a[1]) : Integer.compare(a[1], b[1])));
    return entries;
}

static int peakConcurrency(int[][] intervals, boolean closed) {
    int active = 0, peak = 0;
    for (int[] e : entriesFor(intervals, closed)) {
        active += e[1];
        peak = Math.max(peak, active);
    }
    return peak;
}
```

Building and sorting the stream dominates the cost, so the method runs in O(n log n) time with O(n) space for the 2n entries, and the sweep itself is a single linear pass.

<!-- stage: applicability -->
### When Counts Beat Geometry

Use a sweep when the answer depends on how many intervals are active at each coordinate, such as peak load, the first moment of overload, or the number of rooms in use, and not on the shape of any merged block. The invariant is that the counter equals the number of active intervals once every entry before the current position in tie order has been applied.

A false friend is the merge from the third lesson, which reports blocks of coverage and loses how deep the stacking is inside a block. A second false friend is sorting starts and ends separately and walking two pointers, which works for a plain maximum but gives no place to attach weights, groups, or a separate rule for equal coordinates. A third is leaving the tie order to the default array sort, which compares only the first element when told to and so lets ties fall in whatever order the input arrived.

In Java, write the comparator with `Integer.compare` on both keys so that extreme coordinates cannot overflow, and set the delta direction from the contract in a single visible place. Keep the counter in an `int` only when n is bounded, and sort a freshly built entry array so the caller's intervals stay untouched.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Concurrent Half-Open Intervals (Author exercise)
<!-- id: iv-max-concurrent-half-open -->

**Prerequisites.** The endpoint contracts and the touching-boundary lessons.

**Problem.** Given half-open intervals `[start, end)`, return the largest number of intervals that contain one common coordinate. Emit a plus one at each start and a minus one at each end, and process an end before a start at the same coordinate.

**Constraints.** 0 <= intervals.length <= 100000 and -1000000000 <= start < end <= 1000000000.

**Example 1.** Input `intervals = [[1, 4], [2, 5], [4, 7], [5, 8]]`, output `2`.

**Example 2.** Input `intervals = [[1, 3], [3, 5], [5, 7]]`, output `1`.

**Hint.** What does the counter hold after an end entry that shares a coordinate with a start? Which order keeps touching intervals apart?

**Changed decision.** First rung: the answer is produced by a counter over sorted signed entries, and the tie order puts ends before starts.

#### [Vary] Maximum Concurrent Closed Intervals (Author exercise)
<!-- id: iv-max-concurrent-closed -->

**Prerequisites.** Maximum Concurrent Half-Open Intervals.

**Problem.** Given closed intervals `[start, end]`, return the largest number of intervals that share one coordinate. Two intervals that meet at a single value do overlap, so a start must be applied before an end at the same coordinate.

**Constraints.** 0 <= intervals.length <= 100000 and -1000000000 <= start <= end <= 1000000000.

**Example 1.** Input `intervals = [[1, 4], [2, 5], [4, 7], [5, 8]]`, output `3`.

**Example 2.** Input `intervals = [[1, 3], [3, 5], [5, 7]]`, output `2`.

**Hint.** Which same-coordinate entry must the counter see first so that touching intervals are both alive? Is a zero-length interval still counted?

**Changed decision.** The tie order is reversed, so starts come before ends and a shared endpoint raises the peak.

#### [Boundary] Many Events At One Coordinate (Author exercise)
<!-- id: iv-many-events-one-coordinate -->

**Prerequisites.** Maximum Concurrent Closed Intervals.

**Problem.** Given entries `[coordinate, delta]` in any order, where delta may be any nonzero integer, return the largest counter value measured after all entries of a coordinate have been applied. The total of all deltas is zero and the counter never goes below zero when the entries are applied in coordinate order. Shuffling the input must never change the result.

**Constraints.** 0 <= entries.length <= 100000, -1000000000 <= coordinate <= 1000000000 and -1000 <= delta <= 1000.

**Example 1.** Input `entries = [[5, -2], [5, 3], [1, 2], [9, -3]]`, output `3`.

**Example 2.** Input `entries = [[2, 1], [2, -1], [2, 1], [2, -1]]`, output `0`.

**Hint.** What value should be recorded when several entries share a coordinate? Can an intermediate value inside the group be the answer?

**Changed decision.** Entries at one coordinate are grouped and applied together, so only the value after the group counts and the input order cannot matter.

#### [Recognize] First Coordinate Reaching Capacity (Author exercise)
<!-- id: iv-first-coordinate-capacity -->

**Prerequisites.** Many Events At One Coordinate.

**Problem.** Given half-open intervals and a positive limit `k`, return the smallest coordinate at which at least `k` intervals are active, or -1 when that never happens. Sweep the entries and test the counter after the last entry of each coordinate.

**Constraints.** 0 <= intervals.length <= 100000, 1 <= k <= 100000 and -1000000000 <= start < end <= 1000000000.

**Example 1.** Input `intervals = [[1, 5], [2, 6], [3, 4]], k = 3`, output `3`.

**Example 2.** Input `intervals = [[1, 3], [3, 5]], k = 2`, output `-1`.

**Hint.** At which point of a coordinate group does the counter describe the intervals active at that coordinate? Why can a test inside the group return a wrong answer?

**Changed decision.** The sweep stops early with a coordinate instead of reporting a maximum, and the test happens only after a whole group.
