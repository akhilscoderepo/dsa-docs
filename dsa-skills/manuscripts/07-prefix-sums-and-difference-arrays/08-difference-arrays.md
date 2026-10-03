<!-- lesson-kind: standard -->
<!-- lesson-id: difference-arrays -->
## Difference Arrays

<!-- stage: context -->
### A Gardener's Sprinkler Schedule

A garden has a long row of plots, numbered from zero, and a gardener who works from a list of watering jobs. Each job says: give every plot from this one to that one this many liters. The jobs overlap, so a plot in the middle may be watered by several of them, and the amounts add up. There are thousands of jobs, and nobody needs to know the amount until every job has been listed. Only then does the gardener want a final sheet showing the total water for each plot.

Walking along the plots of each job and adding the amount to every one is slow when the jobs are long. The gardener wonders whether a note could be made at the start and the end of each job, with the walk along the plots happening once at the end instead of once per job.

<!-- stage: naive -->
### Water Every Plot Of Every Job

The direct approach is to apply each job by adding its amount to each plot in its stretch.

```java
static long[] finalWater(int plots, int[][] jobs) {
    long[] water = new long[plots];
    for (int[] job : jobs) {
        int first = job[0], last = job[1], liters = job[2];
        for (int p = first; p <= last; p++) {
            water[p] += liters;
        }
    }
    return water;
}
```

Both ends of a job are included, and the totals are the sum of the amounts of all the jobs that cover each plot.

<!-- stage: bottleneck -->
### Long Jobs Are Walked Again And Again

A job covering m plots costs O(m), so q jobs on n plots can take O(q n) time: a hundred thousand long jobs on a hundred thousand plots is ten billion additions. Most of that work is the same instruction repeated across a stretch where nothing changes from one plot to the next.

Look at what a single job does to the sheet of totals. Going from left to right, the amount rises by the job's liters at the first plot and falls back at the plot after the last one, and stays flat everywhere else. Only two places in the sheet change their step from the previous plot, so a job needs two notes, not m. If the notes of all the jobs are collected first and the sheet is read once, from left to right, with a running sum, the total cost is O(q + n).

<!-- stage: insight -->
### Record The Steps, Rebuild The Totals

A **difference array** stores, at each position, how much the total changes when moving from the previous position to this one. A job from `first` to `last` with amount `v` adds `v` to the entry at `first`, because the total steps up there, and subtracts `v` from the entry at `last + 1`, because the total steps back down just after the job ends. Each entry is a **delta**, a change relative to the left neighbor and not a total. Adding many jobs is adding many deltas into the same array, and the order in which jobs arrive does not matter.

To read the totals, **materialize** the array: scan from left to right keeping a running sum of the deltas, and the running sum at each position is that position's total. This works because the total at position `p` is the sum of every delta at positions up to `p`, and a job contributes `+v` for positions from its start and `-v` from just after its end, so the contribution is `v` exactly inside the job and zero outside it. This is the reverse of the prefix sum: the prefix sum of the difference array is the totals, and the neighbor differences of the totals are the difference array.

<!-- names: difference array, delta, materialize -->

The entry for `last + 1` raises one detail: a job that reaches the final plot has no plot after it. The usual solution is a **sentinel** slot, one extra entry at the end of the array, so that the write is always valid and is simply never read when materializing. The invariant is that the array has `n + 1` slots, every job touches exactly two of them, and materializing the first `n` slots gives the correct totals.

<!-- stage: variables -->
### Deltas, Running Sum And The Extra Slot

`diff` has `n + 1` entries, all zero at first, where slot `n` is the extra slot for jobs that end at the last plot. A job `(first, last, v)` performs `diff[first] += v` and `diff[last + 1] -= v`. During materialization, `running` is the sum of the deltas read so far, and `out[p]` is set to `running` after adding `diff[p]`. Totals can be large, so the types of `diff`, `running` and `out` are chosen from the bounds, and `long` is the safe default.

<!-- stage: trace -->
### Two Notes Per Job, One Scan

The first trace records three jobs on six plots: five liters for plots 1 to 3, two liters for plots 2 to 5, and four liters for plots 4 to 5. The row of cells is the difference array with its extra slot, and the variables list the two slots written. See the third job: its end is plot 5, so the cancelling note goes to slot 6, the extra slot, and the array ends as 0, 5, 2, 0, -1, 0, -6.

```trace
{"cells":["0","5","2","0","-1","0","-6"],"pointers":["start","cancel"],"steps":[{"at":{"start":1,"cancel":4},"vars":{"amount":5,"slotStart":5,"slotCancel":-5},"note":"Job 1 adds 5 to plots 1 to 3. Add 5 to slot 1, which becomes 5, and subtract 5 from slot 4, which becomes -5."},{"at":{"start":2,"cancel":6},"vars":{"amount":2,"slotStart":2,"slotCancel":-2},"note":"Job 2 adds 2 to plots 2 to 5. Add 2 to slot 2, which becomes 2, and subtract 2 from slot 6, which becomes -2."},{"at":{"start":4,"cancel":6},"vars":{"amount":4,"slotStart":-1,"slotCancel":-6},"note":"Job 3 adds 4 to plots 4 to 5. Add 4 to slot 4, which becomes -1, and subtract 4 from slot 6, which becomes -6."}]}
```

The second trace materializes that array with a running sum. Each step adds one delta and sets the total of one plot. Notice the fourth step: the delta is 0, so the total stays 7, which shows that a flat stretch needs no entries between its two notes.

```trace
{"cells":["0","5","2","0","-1","0","-6"],"pointers":["p"],"steps":[{"at":{"p":0},"vars":{"delta":0,"total":0},"note":"Add the delta 0 to the running sum, which becomes 0, so plot 0 receives 0 liters."},{"at":{"p":1},"vars":{"delta":5,"total":5},"note":"Add the delta 5 to the running sum, which becomes 5, so plot 1 receives 5 liters."},{"at":{"p":2},"vars":{"delta":2,"total":7},"note":"Add the delta 2 to the running sum, which becomes 7, so plot 2 receives 7 liters."},{"at":{"p":3},"vars":{"delta":0,"total":7},"note":"Add the delta 0 to the running sum, which becomes 7, so plot 3 receives 7 liters."},{"at":{"p":4},"vars":{"delta":-1,"total":6},"note":"Add the delta -1 to the running sum, which becomes 6, so plot 4 receives 6 liters."},{"at":{"p":5},"vars":{"delta":0,"total":6},"note":"Add the delta 0 to the running sum, which becomes 6, so plot 5 receives 6 liters."}]}
```

<!-- stage: code -->
### Write Two Slots, Scan Once

```java
static long[] applyRangeAdds(int n, int[][] adds) {
    long[] diff = new long[n + 1];
    for (int[] a : adds) {
        diff[a[0]] += a[2];
        diff[a[1] + 1] -= a[2];
    }
    long[] out = new long[n];
    long running = 0;
    for (int p = 0; p < n; p++) {
        running += diff[p];
        out[p] = running;
    }
    return out;
}

static int[] corporateBookings(int[][] bookings, int n) {
    int[] diff = new int[n + 1];
    for (int[] b : bookings) {
        diff[b[0] - 1] += b[2];
        diff[b[1]] -= b[2];
    }
    int[] seats = new int[n];
    int running = 0;
    for (int i = 0; i < n; i++) {
        running += diff[i];
        seats[i] = running;
    }
    return seats;
}

static boolean carPooling(int[][] trips, int capacity) {
    int[] diff = new int[1002];
    for (int[] t : trips) {
        diff[t[1]] += t[0];
        diff[t[2]] -= t[0];
    }
    int onBoard = 0;
    for (int d : diff) {
        onBoard += d;
        if (onBoard > capacity) return false;
    }
    return true;
}
```

Writing a job takes O(1) and materializing takes O(n), so q jobs on n plots cost O(q + n), with n + 1 slots of space. The bookings function shifts the one-based flight numbers into zero-based slots, and the car pool uses the end coordinate as the point where passengers leave.

<!-- stage: applicability -->
### When Updates Come Before Questions

Use a difference array when many range updates are applied and the whole array is read afterwards, or when one pass over the coordinates is enough to answer a question about the totals. The invariant is that every update touches two slots, the start gets the amount and the cell after the end gets the opposite, and the totals are the running sum of the slots.

A false friend is the prefix sum from the earlier lessons: it prepares an array for many questions about ranges, while a difference array prepares for many updates over ranges, and a solution that mixes them will do work in the wrong direction. Another false friend is reading the array between updates. The deltas are not totals, and reading them before materializing gives numbers that mean nothing. A third is the missing end slot: writing at `last + 1` without an extra slot fails when a job ends at the last plot.

In Java, allocate `n + 1` slots and explain the extra one in a comment. Use `long` for the array when amounts times counts can pass the range of `int`. Match the convention of the problem: an inclusive end writes at `last + 1`, an exclusive end writes at `end`, and a one-based index shifts by one before the write.

<!-- stage: exercises -->
### Exercises

#### [Build] One Range Add (Author exercise)
<!-- id: ps-one-range-add -->

**Prerequisites.** The prefix construction lesson, since materializing is a running sum.

**Problem.** Given a length `n`, a stretch `[left, right]` with both ends included, and an amount, return the array of length `n` that starts as zeros and has the amount added to every position of the stretch. Do it with two writes in a difference array and one scan.

**Constraints.** 1 <= n <= 100000, 0 <= left <= right < n, and -1000000000 <= amount <= 1000000000.

**Example 1.** Input `n = 5, left = 0, right = 2, amount = 3`, output `[3, 3, 3, 0, 0]`.

**Example 2.** Input `n = 6, left = 1, right = 3, amount = 5`, output `[0, 5, 5, 5, 0, 0]`.

**Hint.** Where does the total step up? Where does it step back down?

**Changed decision.** First rung: a single update touches two slots, and the totals are rebuilt by a running sum.

#### [Vary] Corporate Flight Bookings (LeetCode 1109)
<!-- id: ps-flight-bookings -->

**Prerequisites.** The One Range Add exercise above.

**Problem.** There are `n` flights numbered from 1 to `n`. Each booking `[first, last, seats]` reserves that number of seats on every flight from `first` through `last`, both included. Return an array with the total seats reserved on each flight.

**Constraints.** 1 <= n <= 20000, 1 <= bookings.length <= 20000, 1 <= first <= last <= n, and 1 <= seats <= 10000.

**Example 1.** Input `bookings = [[1, 3, 5], [2, 4, 3], [3, 5, 2]], n = 5`, output `[5, 8, 10, 5, 2]`.

**Example 2.** Input `bookings = [[1, 1, 7]], n = 2`, output `[7, 0]`.

**Hint.** Flights are numbered from one but the array is indexed from zero. Which slot receives the cancelling note?

**Changed decision.** Many updates are batched before one scan, and the flight numbers are one-based, so the writes are shifted.

#### [Boundary] Final Endpoint (Author exercise)
<!-- id: ps-final-endpoint -->

**Prerequisites.** The two exercises above.

**Problem.** Handle updates that end at the last position. Show that a difference array of length `n` throws when the cancelling write goes to index `n`, and that an array of length `n + 1`, or an explicit guard, fixes it. Also check an array of length one.

**Constraints.** 1 <= n <= 100000 and each update is `[left, right, amount]` with 0 <= left <= right < n, including `right == n - 1`.

**Example 1.** Input `n = 3`, one update `[0, 2, 2]`, output `[2, 2, 2]`.

**Example 2.** Input `n = 1`, one update `[0, 0, 9]`, output `[9]`.

**Hint.** Which index receives the cancelling note when the stretch ends at position `n - 1`? Is that slot ever read?

**Changed decision.** The cancelling write may land one past the end, so either the array gets an extra slot or the write is skipped.

#### [Recognize] Car Pooling (LeetCode 1094)
<!-- id: ps-car-pooling -->

**Prerequisites.** All three exercises above.

**Problem.** A vehicle has a given capacity and only drives forward. Each trip `[passengers, from, to]` picks up that number of people at position `from` and drops them at position `to`. People who leave at a position make room for those who board at the same position. Return true if the vehicle can complete all trips without ever exceeding its capacity.

**Constraints.** 1 <= trips.length <= 1000, 1 <= passengers <= 100, 0 <= from < to <= 1000, and 1 <= capacity <= 100000.

**Example 1.** Input `trips = [[2, 1, 5], [3, 3, 7]], capacity = 4`, output false.

**Example 2.** Input `trips = [[4, 0, 3], [4, 3, 6]], capacity = 4`, output true.

**Hint.** At which coordinates does the number of passengers change? What happens to people who leave at a coordinate where others board?

**Changed decision.** The array is indexed by coordinates and the question is a maximum along the scan, so the running sum is compared with the capacity as it goes.
