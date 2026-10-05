<!-- lesson-kind: standard -->
<!-- lesson-id: difference-arrays -->
## Add To Ranges In Constant Time

<!-- stage: context -->
### Bookings That Slow With Every Request

An airline sells seats on a chain of 50,000 consecutive flight legs. Each booking request adds a number of seats to every leg between two stops. The system handles 20,000 requests and then prints the total number of booked seats on every leg once. A request that spans the whole chain touches all 50,000 legs, and 20,000 such requests perform a billion additions.

Nobody reads the totals until all requests have arrived. The system updates a range for each request and reads every leg once. This lesson asks how a program can apply each range update in constant time and still produce all final totals.

<!-- stage: naive -->
### Looping Over Every Leg Of Each Update

The direct method loops over the range of each request and adds the value to every element.

```java
static long[] applyAll(int n, int[][] updates) {
    long[] total = new long[n];
    for (int[] u : updates) {
        for (int i = u[0]; i <= u[1]; i++) total[i] += u[2];
    }
    return total;
}
```

Each update is a triple `{left, right, value}` with both ends inside the range. For `n = 5` and the single update `{1, 3, 7}`, the method returns `[0, 7, 7, 7, 0]`.

```predict
There are 50,000 legs and 20,000 updates that each cover all legs. How many additions does `applyAll` perform?

It performs 20,000 times 50,000 additions, which is 1,000,000,000. Each update costs the length of its range, so the cost is O(n) per update and O(n * m) for m updates.
```

<!-- stage: bottleneck -->
### Each Update Pays For Its Whole Range

An update over a range of length `w` costs `w` additions, which is O(n) for a wide range. With `m` updates the method costs O(n * m). The program pays for every leg inside every range, although it needs the totals only once, at the end.

All the elements of a range receive the same value. Writing that value `w` times records one fact `w` times. A shorter record would say that the value starts at `left` and stops after `right`. A single pass over the array can then spread those facts into totals.

<!-- stage: insight -->
### Record Where A Value Starts And Stops

A **delta** is a change that applies from a given index onward. A **difference array** `diff` stores one delta per index. The total at index `i` is the sum of all deltas at indexes 0 through `i`.

#### Two Writes For One Update

To add `v` to the range from `left` through `right`, the program writes `diff[left] += v` and `diff[right + 1] -= v`. The first write makes every total from `left` onward larger by `v`. The second write cancels that effect from `right + 1` onward. Only the indexes `left` through `right` keep the extra `v`. Each update costs O(1), whatever the length of its range.

#### One Pass To Read The Totals

After all updates, one pass computes the **running sum** of `diff`. The total at index `i` equals the total at index `i - 1` plus `diff[i]`. The pass costs O(n), so `m` updates and one read cost O(n + m) in total.

<!-- names: difference array, delta, running sum -->

#### The Extra Slot At The End

An update that reaches the last index writes to `diff[right + 1]`, which is `diff[n]`. The array therefore has length `n + 1`, and the slot `n` absorbs that write. The slot is never read as a total. Without it, the write throws an `ArrayIndexOutOfBoundsException`. A guard `if (right + 1 < n)` on every update would avoid the error, and the extra slot makes the guard unnecessary.

<!-- stage: variables -->
### Five Names And Their Roles

Five entries describe the method. The code reads `left`, `right` and `value` as `u[0]`, `u[1]` and `u[2]` of each update triple.

- **diff** is the `long` array of length `n + 1` that holds the deltas, and its last slot absorbs writes past the end.
- **left** and **right** are the first and last index of an update, and both belong to the range.
- **value** is the amount that the update adds to each index in the range.
- **total** is the result array of length `n`, and entry `i` is the running sum of `diff[0..i]`.
- **cur** is the running sum while the final pass walks the array.

Between the updates and the final pass, `diff` is the only array that changes. The final pass reads `diff[0]` through `diff[n - 1]` and ignores the extra slot.

<!-- stage: trace -->
### Reading Totals From The Deltas

#### Two Overlapping Updates

The length is 6, and the updates are `{1, 3, +2}` and `{2, 4, +3}`. The first update writes +2 at index 1 and -2 at index 4. The second writes +3 at index 2 and -3 at index 5. The array below shows the six deltas and the extra slot. The pass walks from index 0 and adds each delta to `cur`, and the totals are `[0, 2, 5, 5, 3, 0]`.

```trace
{"cells":[0,2,3,0,-2,-3,0],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"cur":"0"},"note":"The deltas are written. The pass starts with cur = 0 before index 0."},{"at":{"i":0},"vars":{"diff[i]":"0","cur":"0","total":"[0]"},"note":"Add the delta 0 to cur, which gives the total 0 for index 0."},{"at":{"i":1},"vars":{"diff[i]":"2","cur":"2","total":"[0, 2]"},"note":"Add the delta 2 to cur, which gives the total 2 for index 1."},{"at":{"i":2},"vars":{"diff[i]":"3","cur":"5","total":"[0, 2, 5]"},"note":"Add the delta 3 to cur, which gives the total 5 for index 2."},{"at":{"i":3},"vars":{"diff[i]":"0","cur":"5","total":"[0, 2, 5, 5]"},"note":"Add the delta 0 to cur, which gives the total 5 for index 3."},{"at":{"i":4},"vars":{"diff[i]":"-2","cur":"3","total":"[0, 2, 5, 5, 3]"},"note":"Add the delta -2 to cur, which gives the total 3 for index 4."},{"at":{"i":5},"vars":{"diff[i]":"-3","cur":"0","total":"[0, 2, 5, 5, 3, 0]"},"note":"Add the delta -3 to cur, which gives the total 0 for index 5."},{"at":{"i":6},"vars":{"diff[n]":"0"},"note":"Index 6 is the extra slot. It holds 0 and the pass never reads it."}]}
```

#### An Update That Reaches The End

The length is 6, and the update is `{3, 5, +4}`. The write for the end goes to index 6, which is the extra slot, and it stores -4. The pass reads indexes 0 through 5, so the slot never enters a total. The totals are `[0, 0, 0, 4, 4, 4]`.

```trace
{"cells":[0,0,0,4,0,0,-4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"cur":"0"},"note":"The deltas are written. The pass starts with cur = 0 before index 0."},{"at":{"i":0},"vars":{"diff[i]":"0","cur":"0","total":"[0]"},"note":"Add the delta 0 to cur, which gives the total 0 for index 0."},{"at":{"i":1},"vars":{"diff[i]":"0","cur":"0","total":"[0, 0]"},"note":"Add the delta 0 to cur, which gives the total 0 for index 1."},{"at":{"i":2},"vars":{"diff[i]":"0","cur":"0","total":"[0, 0, 0]"},"note":"Add the delta 0 to cur, which gives the total 0 for index 2."},{"at":{"i":3},"vars":{"diff[i]":"4","cur":"4","total":"[0, 0, 0, 4]"},"note":"Add the delta 4 to cur, which gives the total 4 for index 3."},{"at":{"i":4},"vars":{"diff[i]":"0","cur":"4","total":"[0, 0, 0, 4, 4]"},"note":"Add the delta 0 to cur, which gives the total 4 for index 4."},{"at":{"i":5},"vars":{"diff[i]":"0","cur":"4","total":"[0, 0, 0, 4, 4, 4]"},"note":"Add the delta 0 to cur, which gives the total 4 for index 5."},{"at":{"i":6},"vars":{"diff[n]":"-4"},"note":"Index 6 is the extra slot. It holds -4 and the pass never reads it."}]}
```

<!-- stage: code -->
### Updates And Final Pass In Java

```java
static long[] applyAll(int n, int[][] updates) {
    long[] diff = new long[n + 1];
    for (int[] u : updates) {
        diff[u[0]] += u[2];
        diff[u[1] + 1] -= u[2];
    }
    long[] total = new long[n];
    long cur = 0;
    for (int i = 0; i < n; i++) {
        cur += diff[i];
        total[i] = cur;
    }
    return total;
}
```

The array has `n + 1` entries, so `u[1] + 1` is always a valid index when `u[1] <= n - 1`. The type `long` protects the deltas and the totals from overflow when many large values overlap. The loop uses `+=` and `-=` and not `=`, because several updates can write to the same index.

<!-- stage: applicability -->
### When Deltas Replace Range Loops

#### The Invariant

The invariant is that the total at index `i` equals the sum of `diff[0]` through `diff[i]`. That sum equals the sum of the values of all updates whose range contains `i`. An update with `left <= i <= right` adds `v` through `diff[left]` and has not yet been cancelled by `diff[right + 1]`. An update that ends before `i` adds `v` and then subtracts `v`.

#### The False Friend

The prefix array of the earlier lessons is the false friend. Both structures use running sums, and they solve opposite problems. A prefix array preprocesses fixed values so that many queries read a range fast. A difference array batches many range writes and reads the values once. A prefix array cannot absorb writes, and a difference array cannot answer a total in the middle of the updates.

#### Conditions That Break The Fit

The method needs all updates before the first read. A read between two updates costs a full pass. It also needs updates that apply the same value to a whole range, such as an addition. A range assignment does not combine by addition, and it needs another method.

<!-- stage: exercises -->
### Exercises

#### [Build] One Range Add (Author exercise)
<!-- id: ps-one-range-add -->

**Prerequisites.** The two writes and the final pass of this lesson.

**Problem.** Given an array length `n`, two indexes `left <= right` inside `0..n-1`, and an integer `value`, return the array of length `n` that holds `value` at the indexes `left` through `right` and 0 elsewhere. Use two writes to a difference array.

**Constraints.** The limits are:
- **Length** is `1 <= n <= 10^5`.
- **Indexes** satisfy `0 <= left <= right <= n - 1`.
- **Value** is an `int` with `|value| <= 10^9`.
- **Return type** is `long[]` of length `n`.

**Example 1.** Input `n = 5`, `left = 1`, `right = 3` and `value = 7`, output `[0,7,7,7,0]`.

**Example 2.** Input `n = 3`, `left = 0`, `right = 2` and `value = -4`, output `[-4,-4,-4]`.

**Hint.** Which index receives `+value`, and which receives `-value`? What length must the delta array have?

**Changed decision.** Basic case: one range costs two writes, and a pass spreads them into values.

#### [Vary] Corporate Flight Bookings (LeetCode 1109)
<!-- id: ps-flight-bookings-1109 -->

**Prerequisites.** The first exercise above.

**Problem.** There are `n` flights, numbered from 1 to `n`. A booking `[first, last, seats]` adds `seats` reserved seats to every flight from `first` through `last`, and both ends belong to the range. Return an array `answer` of length `n` where `answer[i]` is the number of seats reserved on flight `i + 1`.

**Constraints.** The limits are:
- **Flights** satisfy `1 <= n <= 2 * 10^4`.
- **Bookings** number at most `2 * 10^4`, with `1 <= first <= last <= n`.
- **Seats** satisfy `1 <= seats <= 10^4`.
- **Numbering** of flights starts at 1, and the array index starts at 0.

**Example 1.** Input `n = 4` and `bookings = [[1,3,5],[2,4,7],[3,3,1]]`, output `[5,12,13,7]`.

**Example 2.** Input `n = 1` and `bookings = [[1,1,9]]`, output `[9]`.

**Hint.** Convert the flight number to an index before the writes. Which index gets the cancelling write?

**Changed decision.** Many updates overlap, and the shift from 1-based flights to a 0-based array must stay consistent.

#### [Boundary] Final Endpoint (Author exercise)
<!-- id: ps-final-endpoint -->

**Prerequisites.** The first exercise above and the second trace of this lesson.

**Problem.** Given an array length `n` and a list of updates `[left, right, value]`, return the array of totals after all updates. Every update is valid even when `right` equals `n - 1`. The difference array must hold the cancelling write of such an update without any guard.

**Constraints.** The limits are:
- **Length** is `1 <= n <= 10^5`.
- **Updates** number at most `10^5`, with `0 <= left <= right <= n - 1`.
- **Value** is an `int` with `|value| <= 10^9`.
- **Return type** is `long[]` of length `n`.

**Example 1.** Input `n = 4` and updates `[[1,3,4]]`, output `[0,4,4,4]`.

**Example 2.** Input `n = 4` and updates `[[0,0,3],[0,3,2]]`, output `[5,2,2,2]`.

**Hint.** The cancelling write goes to index `right + 1`. How many slots does the delta array need so that this index exists for `right = n - 1`?

**Changed decision.** The range can end at the last index, so the delta array reserves one slot beyond the result.

#### [Recognize] Car Pooling (LeetCode 1094)
<!-- id: ps-car-pooling-1094 -->

**Prerequisites.** All exercises above.

**Problem.** A car has `capacity` empty seats. A trip `[passengers, from, to]` picks up `passengers` people at position `from` and drops them at position `to`. Positions lie on one line, and the car only drives forward. Return `true` when the car can complete all trips without ever carrying more than `capacity` people. A drop at a position happens before a pickup at the same position.

**Constraints.** The limits are:
- **Trips** number `1 <= trips.length <= 1000`.
- **Passengers** satisfy `1 <= passengers <= 100`.
- **Positions** satisfy `0 <= from < to <= 1000`.
- **Capacity** satisfies `1 <= capacity <= 10^5`.

**Example 1.** Input `trips = [[2,1,5],[3,3,7]]` and `capacity = 4`, output `false`.

**Example 2.** Input `trips = [[3,2,4],[3,4,6]]` and `capacity = 3`, output `true`.

**Hint.** Add `+passengers` at `from` and `-passengers` at `to`. After the running sum, the value at each position is the number of people in the car. Why does the same position combine a drop and a pickup into one delta?

**Changed decision.** The range is half-open, because passengers leave at `to`, so the cancelling write lands exactly at `to`.
