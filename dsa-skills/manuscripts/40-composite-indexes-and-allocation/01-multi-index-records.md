<!-- lesson-kind: standard -->
<!-- lesson-id: multi-index-records -->
## Multi-Index Records

<!-- stage: context -->
### One Update That Reaches Only One View

An online store keeps one record per product. Support staff look a product up by its id, and the category page lists the cheapest products first. A developer stores the records in a hash map for the id lookups and keeps a second sorted collection for the category page. One night a price drops from 40 to 25. The hash map shows 25, but the category page still lists the product at 40, and a second copy appears at 25 after the next refresh.

Both views are correct about something. Each one is wrong about the other. The bug sits in the update, which touched one structure and forgot the other.

This lesson asks how to store one record in several structures so that every public call leaves all of them telling the same story.

<!-- stage: naive -->
### Two Collections That Update Separately

The direct design keeps a map from each index to its number. A separate list of pairs answers the ordered question of which index is smallest for a number. The class below stores the pairs in a list and scans it.

```java
final class NaiveContainers {
    private final java.util.Map<Integer, Integer> numberAt = new java.util.HashMap<>();
    private final java.util.List<int[]> pairs = new java.util.ArrayList<>(); // {index, number}

    void change(int index, int number) {
        numberAt.put(index, number);
        pairs.add(new int[] {index, number});      // forgets the old pair for this index
    }

    int find(int number) {
        int best = -1;
        for (int[] p : pairs) {
            if (p[1] == number && (best == -1 || p[0] < best)) best = p[0];
        }
        return best;
    }
}
```

After `change(1, 10)` and then `change(1, 20)`, the call `find(10)` still returns 1, although index 1 now holds 20.

```predict
The class passes a test that changes each index only once. What breaks when an index is changed twice, and how much work does each find call do after n changes?

The list keeps the old pair for the index, so find reports an index for a number that the index no longer holds. Each find scans every pair ever added, so it costs O(n) and the list also grows with every change instead of with the number of live indexes.
```

<!-- stage: bottleneck -->
### Stale Pairs And Full Scans

Two separate costs hide in the naive class. The first is correctness. The map answers "what does index 1 hold now?" correctly, while the list still holds the history of every earlier value. A call that reads the list sees values that no longer exist.

The second cost is time. A find call scans the whole list, which costs O(n) for n changes made so far, and the list never shrinks.

Fixing only the speed does not help. A sorted set per number answers find in O(log n), yet it still returns a dead entry when the old pair stays inside it. The sorted set needs the exact old pair removed at the moment the record changes. That removal needs the old value, and only the map can supply it.

<!-- stage: insight -->
### Keeping Every View Equal To The Record

The map from index to number is the **source of truth**. It holds exactly one current value per index, and no other structure may disagree with it.

#### Views Built From The Record

A **secondary index** is any other structure that answers a question faster than a scan of the map. Here the secondary index maps each number to a sorted set of the indexes that hold it. A secondary index stores no new facts. It stores the same facts in another order.

#### Repairing After Every Change

Each public call finishes with a **repair step**. The step reads the old value from the source of truth. It removes the old entry from each secondary index and writes the new value. It then inserts the new entry into each secondary index. The removal must come first. A sorted set locates an entry by its fields, so the entry must still hold the old fields when the removal runs.

The invariant has two parts. Every live record appears in every secondary index exactly once. No secondary index holds an entry for a record that no longer exists or no longer has those fields.

<!-- names: source of truth, secondary index, repair step -->

<!-- stage: variables -->
### What Each Piece Of State Means

Three pieces of state carry the lesson, and each changes at a known moment.

- **numberAt** maps each index to its current number and changes in every change call.
- **indexesOf** maps each number to a sorted set of indexes and changes in step with numberAt.
- **old** is the number that numberAt held before the call, or absent for a new index, and it exists only inside the call.

The call removes an empty set from indexesOf. A find call then treats a missing key as the answer -1.

<!-- stage: trace -->
### Following Calls Through Both Maps

#### Changing An Index Twice

The first trace uses five calls. The pointer `call` points at the call that just ran. Each step shows both maps after that call, with the map from index to number first.

```trace
{"cells":["change(2,10)","change(1,10)","change(1,20)","find(10)","find(20)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"numberAt":"2:10","indexesOf":"10:{2}","result":"null"},"note":"Call 0: index 2 is new, so there is no old entry to remove, and number 10 gains index 2."},{"at":{"call":1},"vars":{"numberAt":"1:10,2:10","indexesOf":"10:{1,2}","result":"null"},"note":"Call 1: index 1 is new, so there is no old entry to remove, and number 10 gains index 1."},{"at":{"call":2},"vars":{"numberAt":"1:20,2:10","indexesOf":"10:{2} 20:{1}","result":"null"},"note":"Call 2: index 1 holds 20 now. The old number 10 loses index 1."},{"at":{"call":3},"vars":{"numberAt":"1:20,2:10","indexesOf":"10:{2} 20:{1}","result":"2"},"note":"Call 3: find(10) reads the set for 10 and returns 2."},{"at":{"call":4},"vars":{"numberAt":"1:20,2:10","indexesOf":"10:{2} 20:{1}","result":"1"},"note":"Call 4: find(20) reads the set for 20 and returns 1."}]}
```

The third call is the one that the naive class gets wrong. It reads the old number 10 from the source of truth, removes index 1 from the set for 10, and only then inserts index 1 into the set for 20. The set for 10 keeps index 2, so find still answers 2.

#### Writing The Same Value Again

The second trace changes index 3 to 5 twice, then to 7. The repeated call finds that the old number equals the new number, so it leaves both maps alone.

```trace
{"cells":["change(3,5)","change(3,5)","change(3,7)","find(5)"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"numberAt":"3:5","indexesOf":"5:{3}","result":"null"},"note":"Call 0: index 3 is new, so there is no old entry to remove, and number 5 gains index 3."},{"at":{"call":1},"vars":{"numberAt":"3:5","indexesOf":"5:{3}","result":"null"},"note":"Call 1: index 3 already holds 5, so the call changes neither map."},{"at":{"call":2},"vars":{"numberAt":"3:7","indexesOf":"7:{3}","result":"null"},"note":"Call 2: index 3 holds 7 now. The old number 5 loses index 3. The set for 5 is empty, so its key disappears."},{"at":{"call":3},"vars":{"numberAt":"3:7","indexesOf":"7:{3}","result":"-1"},"note":"Call 3: find(5) reads the set for 5 and returns -1."}]}
```

The set for 5 empties after the move to 7, so the repair step deletes the key. The last find returns -1 because the key is gone.

<!-- stage: code -->
### The Repair Step In Java

The class below keeps one map as the source of truth and one map of sorted sets as the secondary index.

```java
final class NumberContainers {
    private final java.util.Map<Integer, Integer> numberAt = new java.util.HashMap<>();
    private final java.util.Map<Integer, java.util.TreeSet<Integer>> indexesOf = new java.util.HashMap<>();

    void change(int index, int number) {
        Integer old = numberAt.put(index, number);          // source of truth first; returns the old value
        if (old != null && old == number) return;           // same value: both maps already agree
        if (old != null) {
            java.util.TreeSet<Integer> set = indexesOf.get(old);
            set.remove(index);                               // remove the exact old entry
            if (set.isEmpty()) indexesOf.remove(old);        // drop empty sets so memory follows live data
        }
        indexesOf.computeIfAbsent(number, k -> new java.util.TreeSet<>()).add(index);
    }

    int find(int number) {
        java.util.TreeSet<Integer> set = indexesOf.get(number);
        return set == null ? -1 : set.first();               // smallest index in O(log n)
    }
}
```

A change call costs O(log n), because one hash lookup and at most two tree operations run. A find call costs O(log n) as well, and the first element of a tree set needs no scan. The space is O(n), one entry per index in each map.

<!-- stage: applicability -->
### When Several Indexes Share One Record

#### Spotting The Pattern

Look for one entity that callers reach by an id and also through an order, such as smallest index, cheapest price or best rating. If a call changes a field that an index sorts by, the call must repair that index. The invariant is that the source of truth and every secondary index describe the same live records.

#### Fields That Order A Tree

Java tree sets and tree maps find entries by comparing fields. Mutating a field of an object that already sits inside a tree set leaves the object in the wrong place, and later removals miss it. Store immutable entries, or remove the entry before the field changes. Compare fields with `Integer.compare` and never by subtraction, because subtraction overflows.

#### A False Friend And A Boundary

A cache that stores each value twice under two keys looks like a multi-index record. It is a false friend when the two copies never need to agree after a change. A second false friend is a derived value that costs almost nothing to recompute on every read. Such a value needs no index. Skip this design when a single sorted structure already contains the id, because then the id lookup is one of the views and nothing needs repair.

<!-- stage: exercises -->
### Exercises

#### [Build] Number Container System (LeetCode 2349)
<!-- id: ci40-number-container -->

**Prerequisites.** Hash maps and tree sets from earlier chapters.

**Problem.** Design a class `NumberContainers` with an unbounded array of slots indexed by non-negative integers, where every slot starts empty. The call `change(index, number)` stores `number` in slot `index` and replaces any earlier value. The call `find(number)` returns the smallest index whose slot holds `number`, or -1 if no slot holds it.

**Constraints.** The limits are:
- **Calls** number at most 10^5 in total.
- **Index** satisfies `0 <= index <= 10^9`, and **number** satisfies `1 <= number <= 10^9`.
- **Return** is a single `int`.
- **Mutation** happens only in `change`.

**Example 1.** Input calls `find(10)`, `change(2,10)`, `change(1,10)`, `find(10)`, output -1 for the first find and 1 for the second.

**Example 2.** Input calls `change(1,10)`, `change(1,20)`, `find(10)`, `find(20)`, output -1 for `find(10)` and 1 for `find(20)`.

**Hint.** Which structure holds the current number for an index, and which structure answers the smallest-index question?

**Changed decision.** The class stores both maps and removes the old pair on every change.

#### [Vary] Food Rating System (LeetCode 2353)
<!-- id: ci40-food-rating -->

**Prerequisites.** The number container exercise above.

**Problem.** Design a class `FoodRatings` built from arrays `foods`, `cuisines` and `ratings` of equal length, where `foods[i]` belongs to cuisine `cuisines[i]` and starts with rating `ratings[i]`. The call `changeRating(food, newRating)` sets the rating of one food. The call `highestRated(cuisine)` returns the food of that cuisine with the highest rating. Among equal ratings, return the name that is smallest in lexicographic order.

**Constraints.** The limits are:
- **Foods** are distinct lowercase strings, and the arrays hold `1` to `2 * 10^4` entries.
- **Ratings** satisfy `1 <= rating <= 10^8`.
- **Calls** number at most `2 * 10^4`, and every queried cuisine exists.
- **Return** is the food name.

**Example 1.** Input foods `a`, `b`, `c` in cuisine `x` with ratings 5, 9, 9 and the call `highestRated(x)`, output `b`, because `b` beats `c` by name.

**Example 2.** Input the call `changeRating(b, 1)` and then `highestRated(x)` on the same data, output `c`.

**Hint.** What must the tree set compare, and what must hold true about the entry at the moment of removal?

**Changed decision.** Ratings now change, so the entry in each cuisine set must leave before its rating changes.

#### [Boundary] Update To Same Value (Author exercise)
<!-- id: ci40-same-value -->

**Prerequisites.** The two exercises above.

**Problem.** Design a class `Roster` of players. The call `setTeam(player, team)` assigns a player to a team and returns `true` if the stored team changed, or `false` if the player already belongs to that team. The call `size(team)` returns the number of players on a team, kept as a counter. The call `members(team)` returns the players on a team in increasing order.

**Constraints.** The limits are:
- **Players** and **teams** are integers from 1 to 10^5.
- **Calls** number at most 10^5.
- **Counter** must equal the length of `members(team)` after every call.
- **Return** of `setTeam` is a `boolean`.

**Example 1.** Input calls `setTeam(7,1)`, `setTeam(7,1)`, `size(1)`, output `true`, `false` and 1.

**Example 2.** Input calls `setTeam(7,1)`, `setTeam(7,2)`, `size(1)`, `size(2)`, output `true`, `true`, 0 and 1.

**Hint.** What happens to the counter when the code raises it before comparing the old team with the new team?

**Changed decision.** An update that does not change the value must change nothing else either.

#### [Recognize] Movie Rental System (LeetCode 1912)
<!-- id: ci40-movie-rental -->

**Prerequisites.** All three exercises above.

**Problem.** A chain has `n` shops, and each shop owns at most one copy of each movie at a fixed price. Design a class `MovieRental` built from entries `{shop, movie, price}`. The call `search(movie)` returns up to 5 shops that hold an unrented copy, ordered by price and then shop number. The call `rent(shop, movie)` marks that copy rented. The call `drop(shop, movie)` marks it unrented. The call `report()` returns up to 5 rented copies as `{shop, movie}`, ordered by price, then shop, then movie.

**Constraints.** The limits are:
- **Shops** are numbered 0 to `n - 1`, with `1 <= n <= 3 * 10^5`.
- **Entries** number at most `10^5`, each `{shop, movie}` pair appears once.
- **Calls** number at most `10^5`, and `rent` and `drop` use existing and valid copies.
- **Price** is an `int` from 1 to 10^4.

**Example 1.** Input entries `{0,1,5}`, `{0,2,6}`, `{1,1,4}` and the call `search(1)`, output shops 1 and 0.

**Example 2.** Input the call `rent(1,1)` on the same entries, then `search(1)` and `report()`, output shop 0 and the pair `{1,1}`.

**Hint.** Which two questions need an order, and which record move touches both of them?

**Changed decision.** One call moves a copy between two views, so it removes from one index and inserts into the other.
