<!-- lesson-kind: combination -->
<!-- lesson-id: several-indexes-in-step -->
## Keep Several Indexes In Step

<!-- stage: context -->
### A Warehouse Report That Disagrees With Itself

A warehouse service keeps its stock in one table of items. Each item has a code, an aisle and a count. Two screens read that table. One screen shows the total count per aisle, and a second screen lists the item with the fewest units, so a clerk knows what to reorder first. On Monday a clerk moves an item from aisle 1 to aisle 2. The item table shows aisle 2, the least-stocked screen is correct, and the aisle report still counts the item in aisle 1.

Nothing crashed, and no single number looks absurd. Aisle 1 reports too much stock and aisle 2 reports too little, and the totals only drift further apart with every move. The move call updated the table and forgot one of the summaries.

This lesson asks how to build a class whose calls change one stored record and several summaries at once, so that every summary agrees with the record after every call. The same question appears in games that keep line counters, in transit systems that keep route averages, in feeds with visibility rules and in matching services with waiting queues.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

#### Counters Beside A Board

The lesson Move Pieces On A Board supplied the idea that a count kept per line replaces a scan of the whole board. It also supplied the order of legality checks: reject the move first, then write. This lesson keeps both rules and asks what happens to the counters when a move is taken back.

#### One Complete Before And After

The lesson Apply Transactions Without Partial Changes supplied the rule that a failed call changes nothing and that an open journey is state like any other record. This lesson uses that rule to separate a plan from a commit, and it adds a derived ranking of routes that the commit must repair.

#### Visibility Before The Cut

The lesson Merge Feeds From Many Sources supplied the merge of several newest-first lists and the rule that filtering happens before the output limit. This lesson keeps the merge and adds sources whose visibility changes between calls.

#### Status As The Only Truth

The lesson Track Status And Pick The Next Task supplied the rule that a lifecycle status is authoritative and that a queue shows only live entities. This lesson adds a second index over the same entities, so one status change must repair two structures.

#### The Choice This Lesson Adds

The new work is the single path that writes. Earlier lessons repaired indexes inside each method. Here every public call builds the old and the new version of a record and hands both to one method, and that method repairs every summary.

<!-- stage: naive -->
### Each Method Repairs What It Remembers

The direct design stores items in a map, keeps a map of totals per aisle and keeps a sorted set for the least-stocked screen. Each public method updates the structures that its author had in mind.

```java
final class NaiveShelf {
    record Item(String sku, String aisle, int qty) {}
    private final java.util.Map<String, Item> items = new java.util.HashMap<>();
    private final java.util.Map<String, Integer> aisleTotal = new java.util.HashMap<>();
    private final java.util.TreeSet<Item> lowest = new java.util.TreeSet<>(
            java.util.Comparator.comparingInt(Item::qty).thenComparing(Item::sku));

    void receive(String sku, String aisle, int n) {
        Item old = items.get(sku);
        Item next = new Item(sku, aisle, (old == null ? 0 : old.qty()) + n);
        if (old != null) lowest.remove(old);
        items.put(sku, next);
        lowest.add(next);
        aisleTotal.merge(aisle, n, Integer::sum);
    }

    void transfer(String sku, String aisle) {
        Item old = items.get(sku);
        Item next = new Item(sku, aisle, old.qty());
        lowest.remove(old);
        items.put(sku, next);                    // the aisle totals stay as they were
        lowest.add(next);
    }
}
```

After `receive("a", "A1", 5)` and `transfer("a", "A2")`, the total of A1 is still 5 and the total of A2 is 0.

```predict
Which structure does transfer forget, and what does the aisle report show for a call to total("A1") and total("A2") after one transfer of five units?

The transfer forgets the map of aisle totals. A1 still reports 5 units, which are no longer there, and A2 reports 0 units, which it now holds. Each later move widens the gap, and nothing in the item table reveals it.
```

<!-- stage: bottleneck -->
### Every Method Repeats The Same Repairs

The naive design is fast. Each call runs a constant number of hash and tree operations, so the cost is O(log n) per call. The weakness is correctness, and it grows with every new method.

A class with k public methods and m summaries has k times m repair decisions, and the author makes each decision again in each method. Receive remembers the sorted set. Transfer remembers the sorted set and forgets the totals. A ship method written later may remember neither. A single missed decision leaves a summary that disagrees with the record, and no call ever corrects it.

Rebuilding the summaries from the record on every query repairs the disagreement. That costs O(n) per query, and a service with 10^5 items and 10^5 queries then needs 10^10 steps. The class needs a way to keep every summary correct after every write at the price of O(log n).

<!-- stage: insight -->
### One Writer Updates Every Summary

Split the stored data into two kinds. The **authoritative state** is the one map from key to record, and a call may never contradict it. A **derived index** is any other structure that can be rebuilt from that map, such as a total per group, a sorted set or a counter per line.

Give the class one **single writer**, a private method that takes the old record, or none, and the new record, or none. It reads both versions, removes the old version from every derived index and inserts the new version. Receive, ship and transfer each decide what the new record is and then call the writer. No public method touches a derived index.

#### Why Old And New Both Go In

A total per group changes by the difference between the new and the old count, and the new group may differ from the old group. A sorted set must find the old entry by its old fields before the new entry exists. The writer sees both versions, so it applies both repairs without guessing what the caller meant.

#### Why Checks Come First

The writer never rejects a call. Every public method validates its preconditions, builds the new record and only then calls the writer. A rejected call returns before the first write, so no summary is half repaired.

The invariant is that the map and every derived index describe the same records after each call, and only the writer writes them.

<!-- names: authoritative state, derived index, single writer -->

<!-- stage: variables -->
### Three Structures And One Method

The shelf class stores one map, two derived structures and one writer.

- **items** maps each sku to its immutable record of sku, aisle and count, and is the authoritative state.
- **aisleTotal** maps each aisle to the sum of the counts of its items. An aisle whose sum reaches zero is deleted.
- **lowest** is a tree set of all records, ordered by smaller count and then smaller sku.
- **replace** is the only method that writes the three structures.

Records are immutable. A change builds a new record, so a record never changes while it sits in the tree set.

<!-- stage: trace -->
### Following Calls Through Every View

#### A Move And A Shipment

The first trace receives stock in two aisles, moves an item and ships the rest of another. The pointer `call` marks the call that just ran. The variable `lowest` lists the records in set order, and `totals` lists the sum per aisle.

```trace
{"cells":["receive(a,A1,5)","receive(b,A1,2)","receive(c,A2,4)","transfer(b,A2)","ship(b,2)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"lowest":"a:5","totals":"A1=5","result":"true"},"note":"Call 0: replace inserts the new record a with 5 units into A1."},{"at":{"call":1},"vars":{"lowest":"b:2 a:5","totals":"A1=7","result":"true"},"note":"Call 1: replace inserts the new record b with 2 units into A1."},{"at":{"call":2},"vars":{"lowest":"b:2 c:4 a:5","totals":"A1=7 A2=4","result":"true"},"note":"Call 2: replace inserts the new record c with 4 units into A2."},{"at":{"call":3},"vars":{"lowest":"b:2 c:4 a:5","totals":"A1=5 A2=6","result":"true"},"note":"Call 3: replace moves 2 units of b from A1 to A2 in the table, the set and the totals."},{"at":{"call":4},"vars":{"lowest":"c:4 a:5","totals":"A1=5 A2=4","result":"true"},"note":"Call 4: all 2 units leave, so replace removes b from every structure."}]}
```

The transfer at call 3 moves the two units of b from A1 to A2. The totals change in the same step as the item table, so the report never disagrees with the record.

#### Rejected Calls Change Nothing

The second trace shows calls that fail validation. Each rejected call returns `false` and leaves all three structures as they were.

```trace
{"cells":["receive(x,A1,3)","receive(y,A1,3)","ship(x,5)","ship(x,3)","transfer(y,A1)","transfer(z,A2)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"lowest":"x:3","totals":"A1=3","result":"true"},"note":"Call 0: replace inserts the new record x with 3 units into A1."},{"at":{"call":1},"vars":{"lowest":"x:3 y:3","totals":"A1=6","result":"true"},"note":"Call 1: replace inserts the new record y with 3 units into A1."},{"at":{"call":2},"vars":{"lowest":"x:3 y:3","totals":"A1=6","result":"false"},"note":"Call 2: the check fails before any write, so all three structures stay as they were."},{"at":{"call":3},"vars":{"lowest":"y:3","totals":"A1=3","result":"true"},"note":"Call 3: all 3 units leave, so replace removes x from every structure."},{"at":{"call":4},"vars":{"lowest":"y:3","totals":"A1=3","result":"false"},"note":"Call 4: the check fails before any write, so all three structures stay as they were."},{"at":{"call":5},"vars":{"lowest":"y:3","totals":"A1=3","result":"false"},"note":"Call 5: the check fails before any write, so all three structures stay as they were."}]}
```

The shipment of five units at call 2 fails because x holds three. The later shipment of three units empties x, so `replace` receives a new record of none and removes x from the sorted set, and the total of A1 drops to the three units of y.

<!-- stage: code -->
### The Shelf In Java

The class routes every write through `replace`, and each public method checks its preconditions before it builds the new record.

```java
final class Shelf {
    private record Item(String sku, String aisle, int qty) {}
    private final java.util.Map<String, Item> items = new java.util.HashMap<>();
    private final java.util.Map<String, Integer> aisleTotal = new java.util.HashMap<>();
    private final java.util.TreeSet<Item> lowest = new java.util.TreeSet<>(
            java.util.Comparator.comparingInt(Item::qty).thenComparing(Item::sku));

    private void replace(Item old, Item next) {
        if (old != null) {
            items.remove(old.sku());
            lowest.remove(old);                               // the old fields find the old entry
            if (aisleTotal.merge(old.aisle(), -old.qty(), Integer::sum) == 0) aisleTotal.remove(old.aisle());
        }
        if (next != null) {
            items.put(next.sku(), next);
            lowest.add(next);
            aisleTotal.merge(next.aisle(), next.qty(), Integer::sum);
        }
    }

    boolean ship(String sku, int n) {
        Item old = items.get(sku);
        if (old == null || n <= 0 || old.qty() < n) return false;   // validate before any write
        replace(old, old.qty() == n ? null : new Item(sku, old.aisle(), old.qty() - n));
        return true;
    }
}
```

Each call runs a fixed number of hash and tree operations, so the time is O(log n). The space is O(n), because every item appears in the map and in the sorted set, and every aisle appears once.

<!-- stage: applicability -->
### Spotting A Class With Many Views

#### List The Writes And The Views

Write down every public call that creates, changes or removes a record. Beside each call, list every summary it must repair. If a summary appears in the list of two calls, those calls need a shared writer. The invariant is that the record and every derived index describe the same data after each call, including calls that undo or cancel.

#### Undo Is Another Writer Call

A call that takes back an earlier change does not need special code when the writer takes an old and a new record. Undo passes the current record as the old one and the logged record as the new one. A log of old records is the only extra state.

#### False Friends And Limits

Recomputing a summary from the record on demand looks like a false friend when queries are rare, since it needs no writer. It costs O(n) per query, so it fails when queries are frequent. A lazy heap with stale entries is a valid alternative for a single ranking, but it fails for totals and counters, because those need exact decrements. Skip a summary when no call reads it, because it costs memory and one repair per write.

<!-- stage: exercises -->
### Exercises

#### [Build] Tic-Tac-Toe With Undo (LeetCode 348)
<!-- id: sv-ix-board-undo -->

**Prerequisites.** The shelf class above and its single writer.

**Problem.** Design a class `UndoBoard` for an `n` by `n` grid and players 1 and 2. The call `move(row, col, player)` places a mark and returns 0 if no player has won, returns `player` if that move completes a full row, column, main diagonal or anti-diagonal of one player, and returns -1 if the call is rejected. A call is rejected if the cell is occupied or if a player has already won. The call `undo()` removes the latest accepted move, returns `true`, and returns `false` if no accepted move exists. The call `winner()` returns the winning player or 0.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 1000`, and **players** are 1 or 2, in any order.
- **Cells** satisfy `0 <= row, col < n`.
- **Calls** number at most `10^5`.
- **Rejected** calls change nothing, and an undo of a winning move clears the winner.

**Example 1.** Input `n = 3` and the calls `move(0,0,1)`, `move(1,1,1)`, `move(0,0,2)`, `move(2,2,1)`, `move(0,1,2)`, `undo()`, `move(0,1,2)`, output 0, 0, -1, 1, -1, `true`, 0.

**Example 2.** Input `n = 2` and the calls `undo()`, `move(0,0,2)`, `move(0,1,2)`, `winner()`, `undo()`, `winner()`, output `false`, 0, 2, 2, `true`, 0.

**Hint.** Which counters must a move add to, and which numbers must an undo subtract from?

**Changed decision.** The call adds an undo and a move log, so every counter, the grid and the winner must return to the state before the move.

#### [Vary] Underground System With Cancel (LeetCode 1396)
<!-- id: sv-ix-underground-slow -->

**Prerequisites.** The first exercise above and the rule that checks run before writes.

**Problem.** Design a class `Metro` for stations named by lowercase strings. The call `checkIn(card, station, t)` opens a trip and returns `true`, and returns `false` if the card already has an open trip. The call `checkOut(card, station, t)` closes the open trip, records its duration `t - startTime` for the route from the check-in station to this station, and returns `true`. It returns `false`, and leaves the trip open, if the card has no open trip or if `t` is less than the check-in time. The call `cancel(card)` discards an open trip without recording a duration and returns `true`, or returns `false` if none is open. The call `average(start, end)` returns the mean duration of recorded trips on that route, or -1.0 if none. The call `slowest()` returns the route written `start>end` with the largest mean duration, with the smaller route string winning ties, or the empty string if no trip is recorded.

**Constraints.** The limits are:
- **Calls** number at most `10^5`, and times satisfy `0 <= t <= 10^6`.
- **Stations** are non-empty lowercase strings, and a route may start and end at the same station.
- **Cards** are integers.
- **Return** of `average` is a `double`, and `slowest` compares means exactly, without rounding.

**Example 1.** Input the calls `checkIn(7,a,3)`, `checkIn(7,b,4)`, `checkOut(7,c,13)`, `checkIn(8,a,0)`, `checkOut(8,b,5)`, `slowest()`, `average(a,b)`, output `true`, `false`, `true`, `true`, `true`, `a>c`, 5.0.

**Example 2.** Input the calls `checkIn(1,x,10)`, `checkOut(1,y,9)`, `cancel(1)`, `cancel(1)`, `slowest()`, `average(x,y)`, output `true`, `false`, `true`, `false`, the empty string, -1.0.

**Hint.** The mean of a route changes at every checkout, so which entry of a sorted set must leave before it changes?

**Changed decision.** A cancel call is a second exit for an open trip, and the slowest-route report adds a sorted index that every recorded trip must repair.

#### [Boundary] Twitter With Mute And Delete (LeetCode 355)
<!-- id: sv-ix-feed-sources -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `FeedDesk`. The call `post(user, tweet)` publishes a tweet with a distinct id, and recency is the order of the post calls. The calls `follow(a, b)` and `unfollow(a, b)` change who a follows, and the calls `mute(viewer, author)` and `unmute(viewer, author)` change which followed authors the viewer hides. The call `delete(tweet)` hides a tweet for everyone and returns `true`, or returns `false` if it is unknown or already deleted. The call `feed(user, k)` returns a `Feed` of the tweet ids and a source count. The ids are the `k` newest tweets that the user can see, newest first. A tweet is visible if its author is the user, or if the user follows the author and has not muted the author, and the tweet is not deleted. The source count is the number of distinct authors among the returned ids.

**Constraints.** The limits are:
- **Users** and **tweet ids** are integers, and tweet ids are distinct.
- **Calls** number at most `10^5`, and `1 <= k <= 20`.
- **Self** follow and mute calls are ignored.
- **Return** of `feed` has at most `k` ids and a source count from 0 to `k`.

**Example 1.** Input the calls `post(1,10)`, `post(2,20)`, `post(2,21)`, `post(3,30)`, `follow(1,2)`, `follow(1,3)`, `feed(1,3)`, `mute(1,3)`, `feed(1,3)`, `delete(21)`, `feed(1,3)`, output ids 30, 21, 20 with 2 sources, then ids 21, 20, 10 with 2 sources, then `true` and ids 20, 10 with 2 sources.

**Example 2.** Input the calls `post(5,50)`, `follow(4,5)`, `unfollow(4,5)`, `feed(4,2)`, `follow(4,4)`, `post(4,40)`, `feed(4,2)`, `delete(99)`, output no ids with 0 sources, then ids 40 with 1 source, then `false`.

**Hint.** Where in the merge must a muted author and a deleted tweet disappear, so that the output still holds `k` tweets when enough exist?

**Changed decision.** Visibility has two new rules, mute and delete, and the result carries a source count, so a filter that runs after the cut returns too few tweets.

#### [Recognize] Ride Sharing With Nearest Driver (LeetCode 3829)
<!-- id: sv-ix-ride-match -->

**Prerequisites.** All three exercises above.

**Problem.** This chapter states the contract below itself, and it can differ in detail from LeetCode. Design a class `RideDesk` on a line of integer positions. The call `addDriver(id, pos)` registers a free driver and returns `true`, or returns `false` if the id was used before. The call `goOffline(id)` retires a free driver for good and returns `true`, or returns `false` otherwise. The call `request(rider, pos, dest)` adds a waiting rider and returns `true`, or returns `false` if the id was used before. The call `cancel(rider)` ends a waiting rider and returns `true`, or returns `false` otherwise. The call `match()` takes the longest-waiting rider and the free driver with the smallest distance to the rider's position, with the smaller driver id winning ties, marks both as riding, and returns the array `{rider, driver}`. It returns an empty array and changes nothing if no rider waits or no driver is free. The call `finish(rider)` ends a riding trip, frees the driver at the rider's destination and returns `true`, or returns `false` if the rider is not riding.

**Constraints.** The limits are:
- **Positions** and **destinations** satisfy `0 <= x <= 10^9`.
- **Ids** of drivers and riders are separate integer spaces.
- **Calls** number at most `2 * 10^5`.
- **Return** of `match` is an `int[]` of length 2 or 0.

**Example 1.** Input the calls `addDriver(1,10)`, `addDriver(2,20)`, `request(100,15,40)`, `request(101,30,5)`, `match()`, `match()`, `match()`, `finish(100)`, output `true`, `true`, `true`, `true`, then 100 with driver 1, 101 with driver 2, an empty array, and `true`.

**Example 2.** Input the calls `request(7,5,9)`, `match()`, `addDriver(3,100)`, `cancel(7)`, `cancel(7)`, `match()`, `finish(7)`, output `true`, an empty array, `true`, `true`, `false`, an empty array, `false`.

**Hint.** Which index finds the nearest free driver, and which two structures must a finished trip repair?

**Changed decision.** The match policy is nearest driver with the smaller id on ties, and a finished trip moves the driver to a new position, so the free-driver index replaces an entry instead of only removing one.
