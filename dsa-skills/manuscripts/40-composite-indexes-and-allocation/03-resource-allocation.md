<!-- lesson-kind: standard -->
<!-- lesson-id: resource-allocation -->
## Resource Allocation

<!-- stage: context -->
### Two Customers Hold The Same Seat

A ticket service sells numbered seats for a small theater. A customer asks for any seat, and the service must hand out the lowest-numbered seat that nobody holds. Customers also cancel, and the service must hand a cancelled seat out again. One evening two customers receive seat 12, because the service handled one cancellation twice. Each customer arrives at the door with a valid ticket for the same chair.

The failure is a bookkeeping error, not a slow query. The service lost track of which seats customers hold. The same problem appears in port allocators, ID generators, meeting-room booking and license pools. Each caller asks for the best free item under some rule, and each caller can return an item later.

This lesson asks how to store free and held items so that the best free item comes out quickly. It also asks how to stop a repeated return of one item from creating a second copy.

<!-- stage: naive -->
### Scanning Flags For The First Free Seat

The direct design keeps an array of flags. A reserve call scans from seat 1 for the first flag that says free. A cancel call sets the flag back.

```java
final class NaiveSeats {
    private final boolean[] held;                       // held[s] is true while seat s belongs to a customer

    NaiveSeats(int n) { held = new boolean[n + 1]; }

    int reserve() {
        for (int s = 1; s < held.length; s++) {
            if (!held[s]) { held[s] = true; return s; }
        }
        return -1;
    }

    void unreserve(int s) { held[s] = false; }
}
```

The class is correct. A cancel call is idempotent, because setting a flag to false twice leaves the same state.

```predict
A theater has 100,000 seats and the first 99,999 are held. How many flags does one reserve call read, and what changes if the class keeps released seats in a min-heap instead of scanning?

The scan reads 99,999 flags before it finds the last free seat, so each call costs O(n). A min-heap of released seats reads one entry, but releasing seat 12 twice pushes it twice, and two later reserve calls both return seat 12.
```

<!-- stage: bottleneck -->
### Scans And Duplicates In The Free List

The array pays O(n) for every reserve when the low seats are all held, and the cost repeats for every call. A heap or sorted list of free seats removes the scan. It also removes the flag that told the class whether a customer holds a seat. Without that fact, a repeated release adds the seat to the free structure a second time.

A fast structure without a held record gives duplicates. A held record without a fast structure gives scans. The two facts about each seat have to live together and stay consistent.

Each seat has one status at any moment. A call that changes the status must change every structure that stores it. A call that does not change the status must change nothing.

<!-- stage: insight -->
### Every Resource Sits In Exactly One Set

Split the resources into two groups. The **free set** holds every resource that no caller owns, in sorted order, so the best free resource is the first element. The **taken set** records every resource that a caller owns, in a form that answers membership in O(1).

#### A Partition Of The Resources

The two sets form a **partition** of all resources. Every resource belongs to one set, and no resource belongs to both. The sum of the two sizes equals the total number of resources. This statement is the invariant, and every call must keep it true.

#### Moving One Resource At A Time

A reserve call removes the first element of the free set and marks it taken. A release call first checks the taken record. If the resource is not taken, the call stops, because a second release would put the resource into the free set twice. Otherwise the call unmarks the resource and inserts it into the free set. Each call moves at most one resource, and it removes the resource from its old set before it inserts it into the new one.

<!-- names: free set, taken set, partition -->

<!-- stage: variables -->
### What Each Structure Records

Two structures and one rule carry the state.

- **free** is a sorted set of the seat numbers that no customer holds, and its first element is the answer to a reserve call.
- **taken** is a boolean array indexed by seat number, and it is true exactly for the seats that a customer holds.
- **Release rule** says that a seat leaves `taken` and enters `free` only when `taken` is true for that seat.

The counts satisfy `free.size() + (number of true flags) = n` after every call.

<!-- stage: trace -->
### Following Seats And Gaps

#### Reserving And Releasing Seats

The first trace uses four seats. The pointer `call` sits on the call that just finished. Each step lists the free set and the taken seats.

```trace
{"cells":["reserve()","reserve()","release(1)","reserve()","reserve()"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"free":"{2,3,4}","taken":"{1}","result":"1"},"note":"Call 0: the first free seat is 1. It leaves the free set and enters the taken seats."},{"at":{"call":1},"vars":{"free":"{3,4}","taken":"{1,2}","result":"2"},"note":"Call 1: the first free seat is 2. It leaves the free set and enters the taken seats."},{"at":{"call":2},"vars":{"free":"{1,3,4}","taken":"{2}","result":"true"},"note":"Call 2: seat 1 is taken, so it leaves the taken seats and enters the free set."},{"at":{"call":3},"vars":{"free":"{3,4}","taken":"{1,2}","result":"1"},"note":"Call 3: the first free seat is 1. It leaves the free set and enters the taken seats."},{"at":{"call":4},"vars":{"free":"{4}","taken":"{1,2,3}","result":"3"},"note":"Call 4: the first free seat is 3. It leaves the free set and enters the taken seats."}]}
```

The fourth call returns seat 1 and not seat 3. The release in the third call put seat 1 back into the free set, and the first element of that set is the smallest free seat.

#### Choosing A Seat By Distance

The second trace changes the rule. A room has seats 0 to 9, and each seat call picks the seat farthest from every occupied seat, with the smallest number winning ties.

```trace
{"cells":["seat","seat","seat","seat","leave 4","seat"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"occupied":"{0}","result":"0"},"note":"Call 0: The room is empty, so the first student sits at seat 0."},{"at":{"call":1},"vars":{"occupied":"{0,9}","result":"9"},"note":"Call 1: The best candidate sits at seat 9, at distance 9 from its nearest occupied seat."},{"at":{"call":2},"vars":{"occupied":"{0,4,9}","result":"4"},"note":"Call 2: The best candidate sits at seat 4, at distance 4 from its nearest occupied seat."},{"at":{"call":3},"vars":{"occupied":"{0,2,4,9}","result":"2"},"note":"Call 3: The best candidate sits at seat 2, at distance 2 from its nearest occupied seat."},{"at":{"call":4},"vars":{"occupied":"{0,2,9}","result":"null"},"note":"Call 4: seat 4 leaves the occupied set, so its two neighboring gaps merge."},{"at":{"call":5},"vars":{"occupied":"{0,2,5,9}","result":"5"},"note":"Call 5: The best candidate sits at seat 5, at distance 3 from its nearest occupied seat."}]}
```

This room needs a different structure. The useful structure is the sorted set of occupied seats. Each pair of neighbors defines a gap, and the middle of the gap is a candidate seat.

<!-- stage: code -->
### A Seat Manager In Java

The class keeps the free set as a tree set and the taken record as a boolean array.

```java
final class SeatManager {
    private final java.util.TreeSet<Integer> free = new java.util.TreeSet<>();
    private final boolean[] taken;

    SeatManager(int n) {
        taken = new boolean[n + 1];
        for (int s = 1; s <= n; s++) free.add(s);          // every seat starts free
    }

    int reserve() {
        if (free.isEmpty()) return -1;
        int s = free.pollFirst();                          // leave the free set first
        taken[s] = true;                                   // then enter the taken record
        return s;
    }

    boolean release(int s) {
        if (s < 1 || s >= taken.length || !taken[s]) return false;  // a second release stops here
        taken[s] = false;
        free.add(s);
        return true;
    }
}
```

A reserve call costs O(log n) and a release call costs O(log n). The constructor costs O(n log n). The space is O(n) for the set and the array.

<!-- stage: applicability -->
### Allocators With A Sorted Free Set

#### Recognizing The Pattern

Look for calls that take the best available resource under a stated rule and return it later. State the rule first, such as smallest number, nearest to a target or farthest from the others. The invariant is that every resource sits in exactly one of the two sets, and every call moves at most one resource.

#### Sorted Set Or Counter

A resource pool that grows without bound and never receives repeated returns needs less. A counter for the next unused number plus a heap of returned numbers is enough, and the lesson Pick The Best Free Resource later in this chapter shows it. A fixed pool of at most about 10^5 resources fits the sorted set above.

#### False Friends And Limits

A queue of free seats looks like an allocator, but it is a false friend when the rule asks for the smallest number and not the oldest release. A free list that skips the taken record is a false friend as well, because repeated releases create copies. Skip the pre-filled set when n reaches 10^9. The set would need a billion entries. The allocator has to derive free seats from the few seats that customers hold.

<!-- stage: exercises -->
### Exercises

#### [Build] Seat Reservation Manager (LeetCode 1845)
<!-- id: ci40-seat-manager -->

**Prerequisites.** Tree sets and the multi-index lesson.

**Problem.** Design a class `SeatManager` for seats numbered 1 to `n`, all free at the start. The call `reserve()` marks the free seat with the smallest number as held and returns that number. The call `unreserve(seatNumber)` marks a held seat as free again. Callers only unreserve seats that they hold.

**Constraints.** The limits are:
- **Seats** satisfy `1 <= n <= 10^5`.
- **Calls** number at most `10^5` in total.
- **Reserve** is called only while a free seat exists.
- **Unreserve** names a held seat, so no seat is released twice.

**Example 1.** Input `n = 3` and calls `reserve()`, `reserve()`, `unreserve(1)`, `reserve()`, output 1, 2 and 1.

**Example 2.** Input `n = 2` and calls `reserve()`, `reserve()`, output 1 and 2.

**Hint.** Which structure returns the smallest free seat without a scan?

**Changed decision.** A cancelled seat returns to the free set, so the next reserve may return a lower number than before.

#### [Vary] Exam Room (LeetCode 855)
<!-- id: ci40-exam-room -->

**Prerequisites.** The seat manager exercise above.

**Problem.** A room has `n` seats numbered 0 to `n - 1` in a row. Design a class `ExamRoom`. The call `seat()` seats a student at the free seat that maximizes the distance to the nearest occupied seat, and returns that seat. Equal distances go to the smallest seat number, and the first student sits at seat 0. The call `leave(p)` frees seat `p`.

**Constraints.** The limits are:
- **Seats** satisfy `1 <= n <= 10^9`.
- **Calls** number at most `10^4`.
- **Seat** is called only while a free seat exists.
- **Leave** names an occupied seat.

**Example 1.** Input `n = 10` and four `seat()` calls, output 0, 9, 4 and 2.

**Example 2.** Input the same calls, then `leave(4)` and `seat()`, output 5.

**Hint.** Which seats can ever be optimal: the two ends of the row, or the middle of a gap between neighbors?

**Changed decision.** The best seat depends on the gaps between occupied seats, so the sorted set holds occupied seats and a scan of neighbors picks the seat.

#### [Boundary] Duplicate Release (Author exercise)
<!-- id: ci40-duplicate-release -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `SeatBook` for seats 1 to `n`. The call `reserve()` returns the smallest free seat and marks it held, or returns -1 when every seat is held. The call `release(seat)` returns `true` and frees the seat if the seat is held. It returns `false` and changes nothing if the seat number is out of range or the seat is already free. The call `available()` returns the number of free seats.

**Constraints.** The limits are:
- **Seats** satisfy `1 <= n <= 10^5`.
- **Calls** number at most `10^5`, and `release` accepts any integer.
- **Seat** numbers passed to `release` fit in an `int`.
- **Available** equals `n` minus the number of held seats after every call.

**Example 1.** Input `n = 2` and calls `reserve()`, `reserve()`, `release(2)`, `release(2)`, `reserve()`, output 1, 2, `true`, `false` and 2.

**Example 2.** Input `n = 3` and calls `release(0)`, `release(3)`, `available()`, output `false`, `false` and 3.

**Hint.** Which record answers whether a customer holds seat 3, without touching the free set?

**Changed decision.** A rejected release must leave both structures untouched, so the check comes before any change.

#### [Recognize] Booking Concert Tickets In Groups (LeetCode 2286)
<!-- id: ci40-concert-tickets -->

**Prerequisites.** All three exercises above, and the segment tree from the range-query chapter.

**Problem.** A hall has `n` rows of `m` seats, numbered from 0 in each row. Seats in a row fill from the left, so row `r` with `u` held seats has seats `0` to `u - 1` held. Design a class `Hall`. The call `gather(k, maxRow)` finds the smallest row `r <= maxRow` with at least `k` free seats, holds `k` seats there from the leftmost free seat, and returns `[r, firstSeat]`. It returns an empty array if no such row exists. The call `scatter(k, maxRow)` holds `k` seats in rows 0 to `maxRow`, filling the lowest rows first, and returns `true`. It returns `false` and changes nothing if those rows hold fewer than `k` free seats in total.

**Constraints.** The limits are:
- **Rows** satisfy `1 <= n <= 5 * 10^4`, and **m** satisfies `1 <= m <= 10^9`.
- **k** satisfies `1 <= k <= m`, and `maxRow` satisfies `0 <= maxRow < n`.
- **Calls** number at most `5 * 10^4`.
- **Totals** of free seats can reach `5 * 10^13`, so use `long`.

**Example 1.** Input `n = 2`, `m = 5` and calls `gather(4,0)`, `gather(2,0)`, output `[0,0]` and an empty array.

**Example 2.** Input `n = 2`, `m = 5` and calls `scatter(5,1)`, `gather(5,1)`, output `true` and `[1,0]`.

**Hint.** A gather call needs the leftmost row with a large enough maximum, and a scatter call needs a sum over a prefix of rows. What does one tree node store?

**Changed decision.** One call needs a local fit in one row and the other needs total capacity over many rows, so each node stores both a maximum and a sum.
