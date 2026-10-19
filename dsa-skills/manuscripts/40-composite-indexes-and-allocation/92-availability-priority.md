<!-- lesson-kind: combination -->
<!-- lesson-id: availability-priority -->
## Pick The Best Free Resource

<!-- stage: context -->
### Too Many Seats To List

An online exam service assigns seats in a long virtual row of one billion positions. Each arriving student must sit as far as possible from every student already seated. Students also leave, and their seats open up again. A developer lists all free seats in a set at start-up, and the service runs out of memory before the first student sits down.

A second developer keeps only the occupied seats and scans every pair of neighbors to find the widest gap. That works for 100 students. With 100,000 students in the room, each new arrival scans 100,000 pairs, and each arrival costs 100,000 steps, a cost that grows with every student.

Both designs answer the same question. The first stores too much, and the second recomputes too much. This lesson asks how to store only what exists, how to find the best option without a scan, and how to make sure that an option computed earlier still describes the room now.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

#### Free And Held Items In One Partition

The lesson Resource Allocation supplied the rule that every resource is free or held and never both. This lesson keeps that rule for seats whose numbers are too large to list, and the first exercise adds the held-side check that the code below leaves out.

#### Candidates That Are Checked Later

The lesson Validated Priority supplied the heap of candidates, the record that decides, and the habit of checking a candidate when it reaches the top instead of searching for it earlier. This lesson reuses the habit with a harder check.

#### Where The Record Lives

The lesson Multi-Index Records supplied the method of reading the old state before writing the new state. Here the old state includes the two neighbors of a seat.

#### The Choice This Lesson Adds

The new work is the source of priority. In the earlier lessons a candidate carried its own priority, such as a rating or a number. A gap between two seated students derives its priority from two other records, so a candidate is valid only if both of those records still describe the same pair.

<!-- stage: naive -->
### Listing Every Free Seat

The direct design stores every free seat in a sorted set and picks the seat that is farthest from the nearest occupied seat.

```java
final class NaiveRoom {
    private final java.util.TreeSet<Integer> free = new java.util.TreeSet<>();
    private final java.util.TreeSet<Integer> seated = new java.util.TreeSet<>();

    NaiveRoom(int n) { for (int s = 0; s < n; s++) free.add(s); }   // n entries up front

    int seat() {
        int best = -1, bestDist = -1;
        for (int s : free) {                                       // checks every free seat
            Integer lo = seated.floor(s), hi = seated.ceiling(s);
            int d = Math.min(lo == null ? Integer.MAX_VALUE : s - lo, hi == null ? Integer.MAX_VALUE : hi - s);
            if (d > bestDist) { bestDist = d; best = s; }
        }
        free.remove(best);
        seated.add(best);
        return best;
    }
}
```

The class gives right answers for a small room. Its memory and its time both grow with the number of seats, not with the number of students.

```predict
The room has one billion seats. About how much memory does the free set need before the first student arrives, and how many seats does one seat call check when 100 students are seated?

A tree set entry takes roughly 40 bytes, so one billion entries need about 40 gigabytes before any student arrives. With 100 students seated, one call still checks all 999,999,900 free seats, so no useful call finishes.
```

<!-- stage: bottleneck -->
### Cost That Tracks Seats Not Students

Let `n` be the number of seats and `k` the number of seated students. The free set costs O(n) memory, and a seat call costs O(n log k). Both depend on the size of the room.

Only `k` seats are interesting. The best new seat is either seat 0, seat `n - 1`, or the middle of a gap between two neighbors. A room with `k` students has at most `k + 1` gaps, so the choice has at most `k + 1` candidates.

Keeping candidates in a heap cuts the cost to O(log k) per call. The heap holds each gap computed at some earlier time. A gap changes whenever a student sits inside it or leaves one end of it. A heap entry for the old gap does not change, and it looks as good as before.

<!-- stage: insight -->
### Candidates That Check Their Own Neighbors

Store the room as the occupied seats only. A **next-unused counter** covers the case where seats have no structure beyond their numbers. It names the smallest seat that has never been handed out, so a room of a billion seats needs one integer. Released seats go into a min-heap, and the smallest free seat is the smaller of the heap top and the counter.

#### Gaps As Candidates

For a room where distance matters, each pair of neighbors defines a **gap candidate**. The candidate holds the two neighbors, and its priority is computed from them. A gap between neighbors `a` and `b` offers the seat in the middle at distance `(b - a) / 2`. The two ends of the row offer seat 0 and seat `n - 1`.

#### The Neighbor Check

A candidate in the heap is current only if its two seats are still neighbors. The **neighbor check** asks whether both seats are occupied and no occupied seat lies between them. A linked structure over the occupied seats answers that in O(1): the successor of the left seat must be the right seat. When the check fails, the call drops the candidate and looks at the next one.

The invariant is that every current gap has a candidate in the heap, and a candidate leaves the loop only if both neighbors still match.

<!-- names: next-unused counter, gap candidate, neighbor check -->

<!-- stage: variables -->
### Counters, Links And Heaps

Two small designs share one idea. The first holds two pieces of state, and the second holds three.

- **next** is the next-unused counter, and it only grows.
- **released** is a min-heap of seats that were handed out and returned, and a release call adds to it.
- **nextOf** and **prevOf** map each occupied seat to its neighbors, and a seat or leave call rewires them.
- **heap** holds gap candidates ordered by larger distance and then smaller seat, and every call that creates a gap adds one.

A candidate holds only its two end seats, and the sentinel values `-1` and `n` stand for the two ends of the row. The left-end candidate `(-1, b)` offers seat 0 at distance `b`. The right-end candidate `(a, n)` offers seat `n - 1` at distance `n - 1 - a`. In the trace, `(a,b)` reads as left seat then right seat.

<!-- stage: trace -->
### Following Candidates Through A Room

#### A Counter And A Heap Of Released Seats

The first trace hands out seats from a room of six seats. The pointer `call` marks the call just run. Each step shows the counter and the released heap.

```trace
{"cells":["reserve","reserve","reserve","unreserve(2)","reserve","reserve"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"next":2,"released":"{}","result":"1"},"note":"Call 0: the released heap is empty, so the call returns the counter value 1 and raises the counter to 2."},{"at":{"call":1},"vars":{"next":3,"released":"{}","result":"2"},"note":"Call 1: the released heap is empty, so the call returns the counter value 2 and raises the counter to 3."},{"at":{"call":2},"vars":{"next":4,"released":"{}","result":"3"},"note":"Call 2: the released heap is empty, so the call returns the counter value 3 and raises the counter to 4."},{"at":{"call":3},"vars":{"next":4,"released":"{2}","result":"null"},"note":"Call 3: seat 2 goes into the released heap, and the counter stays at 4."},{"at":{"call":4},"vars":{"next":4,"released":"{}","result":"2"},"note":"Call 4: the released heap holds a seat, so the call returns the smallest one, 2."},{"at":{"call":5},"vars":{"next":5,"released":"{}","result":"4"},"note":"Call 5: the released heap is empty, so the call returns the counter value 4 and raises the counter to 5."}]}
```

The fifth call returns seat 2, because the released heap holds 2 and the counter holds 4. The sixth call returns 4, the counter, because the heap is empty.

#### Gaps That Go Stale

The second trace seats students in a row of eight seats. Two leave calls then merge gaps, and older gaps in the heap stop being current.

```trace
{"cells":["seat","seat","seat","seat","leave(3)","leave(5)","seat","seat"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"occupied":"{0}","heapSize":1,"result":"0"},"note":"Call 0: the room is empty, so the first student takes seat 0 and the candidate (0,8) enters the heap."},{"at":{"call":1},"vars":{"occupied":"{0,7}","heapSize":1,"result":"7"},"note":"Call 1: the current candidate (0,8) gives seat 7. Its halves (0,7) and (7,8) enter the heap, except a half with no free seat."},{"at":{"call":2},"vars":{"occupied":"{0,3,7}","heapSize":2,"result":"3"},"note":"Call 2: the current candidate (0,7) gives seat 3. Its halves (0,3) and (3,7) enter the heap, except a half with no free seat."},{"at":{"call":3},"vars":{"occupied":"{0,3,5,7}","heapSize":3,"result":"5"},"note":"Call 3: the current candidate (3,7) gives seat 5. Its halves (3,5) and (5,7) enter the heap, except a half with no free seat."},{"at":{"call":4},"vars":{"occupied":"{0,5,7}","heapSize":4,"result":"null"},"note":"Call 4: seat 3 leaves, so its neighbors 0 and 5 form the new candidate (0,5). The old candidates that name seat 3 stay in the heap."},{"at":{"call":5},"vars":{"occupied":"{0,7}","heapSize":5,"result":"null"},"note":"Call 5: seat 5 leaves, so its neighbors 0 and 7 form the new candidate (0,7). The old candidates that name seat 5 stay in the heap."},{"at":{"call":6},"vars":{"occupied":"{0,3,7}","heapSize":6,"result":"3"},"note":"Call 6: the current candidate (0,7) gives seat 3. Its halves (0,3) and (3,7) enter the heap, except a half with no free seat."},{"at":{"call":7},"vars":{"occupied":"{0,3,5,7}","heapSize":6,"result":"5"},"note":"Call 7: the call drops 1 stale candidate, then the current candidate (3,7) gives seat 5. Its halves (3,5) and (5,7) enter the heap, except a half with no free seat."}]}
```

The last call drops one candidate before it finds a current one. The dropped candidate (0,5) names seat 5, which left the room, so the two seats are no longer neighbors.

<!-- stage: code -->
### A Counter With A Heap In Java

The class below covers a room of any size, because it stores only what was handed out.

```java
final class SeatCounter {
    private int next = 1;                                          // smallest seat never handed out
    private final java.util.PriorityQueue<Integer> released = new java.util.PriorityQueue<>();

    int reserve() {
        if (!released.isEmpty()) return released.poll();           // a returned seat is always below next
        return next++;
    }

    void unreserve(int seat) { released.add(seat); }
}
```

A call costs O(log k) for k returned seats, and the space is O(k). The code assumes that callers return only seats that they hold, and the first exercise adds the check that removes the assumption.

<!-- stage: applicability -->
### Free Resources Under A Derived Priority

#### Checking The Pattern

Look for a request for the best free resource where the number of resources is far larger than the number of callers. List what the priority depends on. If it depends only on the resource itself, a counter and a heap are enough. If it depends on neighbors, store candidates for the neighbor pairs and check both ends when a candidate reaches the top. The invariant is that every current option has a candidate and no stale candidate is ever returned.

#### What Else Can Go Stale

An end of the row is a special case. The gap before the first seat and the gap after the last seat have only one real neighbor, so the check uses the first and last occupied seat instead of a successor. A seat that leaves and returns to the same place makes an old candidate current again, and that is correct, because the room matches the candidate once more.

#### False Friends

A sorted set of free seats is a false friend when the room is huge, because it stores seats that no caller will ever name. A queue of released seats is a false friend when the rule asks for the smallest seat. Skip candidates when the number of callers is small, because a scan of `k` neighbors costs less than the code for the checks.

<!-- stage: exercises -->
### Exercises

#### [Build] Seat Counter With Validation (LeetCode 1845)
<!-- id: ci40-seat-counter -->

**Prerequisites.** Heaps and the resource allocation lesson.

**Problem.** Design a class `SeatCounter` for seats numbered from 1 to `n`, all free at the start. The call `reserve()` holds the free seat with the smallest number and returns it. The call `unreserve(seat)` frees a held seat and returns `true`, or returns `false` and changes nothing if the seat is not currently held.

**Constraints.** The limits are:
- **Seats** satisfy `1 <= n <= 10^9`, so no structure may list every seat.
- **Calls** number at most `10^5`.
- **Reserve** is called only while a free seat exists.
- **Seat** in `unreserve` is any `int`.

**Example 1.** Input `n = 1000000000` and calls `reserve()`, `reserve()`, `unreserve(1)`, `unreserve(1)`, `reserve()`, `reserve()`, output 1, 2, `true`, `false`, 1 and 3.

**Example 2.** Input the calls `unreserve(5)`, `reserve()` on a new counter, output `false` and 1.

**Hint.** Which collection answers whether a seat is held, and which two sources give the smallest free seat?

**Changed decision.** A huge seat range replaces the full set with a counter and a heap, and a held set takes over the duplicate check.

#### [Vary] Exam Room With A Gap Heap (LeetCode 855)
<!-- id: ci40-exam-room-heap -->

**Prerequisites.** The first exercise above and the validated priority lesson.

**Problem.** A row has `n` seats numbered 0 to `n - 1`. Design a class `GapRoom`. The call `seat()` seats a student at the free seat that maximizes the distance to the nearest seated student and returns it. Equal distances go to the smaller seat, and the first student sits at seat 0. The call `leave(p)` frees seat `p`.

**Constraints.** The limits are:
- **Seats** satisfy `2 <= n <= 10^9`.
- **Calls** number at most `10^5`, so a scan of all seated students per call is too slow.
- **Seat** is called only while a free seat exists, and `leave` names a seated student.
- **Return** of `seat` is an `int`.

**Example 1.** Input `n = 8` and four `seat()` calls, output 0, 7, 3 and 5.

**Example 2.** Input the same calls, then `leave(3)` and `seat()`, output 2.

**Hint.** What must be true of the two seats in a gap entry when it reaches the top of the heap?

**Changed decision.** Candidate gaps replace the scan, and each pop checks that the two end seats are still neighbors.

#### [Boundary] Stale Gap Candidate (Author exercise)
<!-- id: ci40-stale-gap -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `GapBook` of occupied positions on a line. The call `occupy(seat)` marks a free position occupied. The call `vacate(seat)` marks an occupied position free. The call `widestGap()` returns `[left, right]` for the pair of consecutive occupied positions with the largest difference `right - left`, breaking ties by the smaller `left`. It returns an empty array when fewer than two positions are occupied.

**Constraints.** The limits are:
- **Positions** are integers from 0 to 10^9.
- **Calls** number at most `10^5`, and `occupy` and `vacate` name positions in the right state.
- **Consecutive** means no occupied position lies strictly between the two.
- **Return** of `widestGap` is an array of length 2 or length 0.

**Example 1.** Input calls `occupy(2)`, `occupy(10)`, `occupy(6)`, `widestGap()`, `vacate(6)`, `widestGap()`, output `[2,6]` and then `[2,10]`.

**Example 2.** Input calls `occupy(1)`, `widestGap()`, `occupy(9)`, `occupy(4)`, `widestGap()`, `vacate(9)`, `widestGap()`, output an empty array, `[4,9]` and then `[1,4]`.

**Hint.** Is it enough to check that the left position is still occupied? What can happen between the two positions?

**Changed decision.** A candidate needs both ends occupied and no occupied position between them, and checking one end accepts wrong answers.

#### [Recognize] Booking Hall With Cancellations (LeetCode 2286)
<!-- id: ci40-hall-cancel -->

**Prerequisites.** All three exercises above and the segment tree from the range-query chapter.

**Problem.** A hall has `n` rows of `m` seats. Seats in a row are booked from the left, so a row with `b` bookings has its first `b` seats booked. Design a class `CancelHall`. The call `gather(k, maxRow)` books `k` seats in the smallest row `r <= maxRow` that has `k` free seats, and returns `[r, firstSeat]`, or an empty array if no such row exists. The call `scatter(k, maxRow)` books `k` seats over rows 0 to `maxRow`, lowest rows first, and returns `true`, or returns `false` and changes nothing if the free seats there total fewer than `k`. The call `cancel(row, k)` frees the last `k` booked seats of the row and returns `true`, or returns `false` if the row holds fewer than `k` bookings.

**Constraints.** The limits are:
- **Rows** satisfy `1 <= n <= 5 * 10^4`, and **m** satisfies `1 <= m <= 10^9`.
- **k** satisfies `1 <= k <= m`, and `maxRow` and `row` satisfy `0 <= value < n`.
- **Calls** number at most `5 * 10^4`.
- **Totals** of free seats need a `long`.

**Example 1.** Input `n = 3`, `m = 4` and calls `scatter(5,2)`, `cancel(0,2)`, `gather(2,0)`, output `true`, `true` and `[0,2]`.

**Example 2.** Input the same hall and calls `scatter(5,2)`, `cancel(2,1)`, `gather(4,2)`, output `true`, `false` and `[2,0]`.

**Hint.** After a cancellation, which row is the first one with free seats, and can a pointer that only moves forward still find it?

**Changed decision.** Cancellation makes the first open row move backward, so each call finds it by a tree descent and not by a pointer.
