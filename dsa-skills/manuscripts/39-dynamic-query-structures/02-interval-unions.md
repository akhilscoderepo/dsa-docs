<!-- lesson-kind: standard -->
<!-- lesson-id: interval-unions -->
## Interval Unions

<!-- stage: context -->
### Answering Coverage Questions After Every Update

A firewall service receives rules all day. Some rules open a block of port numbers, and some close part of a block that an earlier rule opened. Between rules, callers ask whether ports 8000 through 8099 are all open, or how many ports are open in total. The service cannot sort the rules once and finish, because the next rule changes the answer to every later question.

The same shape appears in calendar booking, in disk block allocation and in a stream that reports which values it has seen so far. Each public method either adds a range, removes a range or asks about coverage. The question is how to store the ranges so that each call stays fast after thousands of earlier calls, without rereading the whole history.

<!-- stage: naive -->
### Keeping Every Added Range In A List

The direct design stores each call exactly as it arrives. An add appends a pair to a list. A query scans the list and checks the pairs.

```java
final class ListCoverage {
    private final List<long[]> added = new ArrayList<>();

    void add(long l, long r) {
        added.add(new long[] {l, r});
    }

    boolean covers(long l, long r) {
        // Walk the coordinates one by one and test each against every stored pair.
        for (long x = l; x < r; x++) {
            boolean hit = false;
            for (long[] p : added) if (p[0] <= x && x < p[1]) hit = true;
            if (!hit) return false;
        }
        return true;
    }
}
```

Adding is cheap, and the code is easy to trust. Removal does not fit at all, because a removal must cancel parts of earlier pairs that the list keeps as separate records.

<!-- stage: bottleneck -->
### Each Query Rereads The Whole History

```predict
A caller adds 100,000 ranges and then asks whether one range of width 1,000 is covered. Roughly how many pair checks does `covers` run?

Up to about 100 million checks, because each of the 1,000 coordinates is compared with all 100,000 stored pairs. Wider query ranges and longer histories multiply the cost further.
```

The list grows with every call, and nothing inside it ever shrinks. With `k` stored pairs and a query of width `w`, `covers` costs O(w * k) time. Port numbers or timestamps reach 10^9, so a wide query makes the width factor unusable. Even a smarter scan that checks pairs and not coordinates still costs O(k) per query.

Counting the covered coordinates is worse. Two stored pairs may overlap, so adding their lengths counts some coordinates twice. The service must find the union of all pairs before it can report a total. Redoing that union on every call turns a long workload of `m` calls into O(m^2) work or worse. The list stores the history of calls, while the questions ask about the current coverage. The coverage itself needs a smaller representation that updates in place.

<!-- stage: insight -->
### Store Merged Ranges In A Sorted Map

#### Merge Everything Into Disjoint Pieces

Coverage is a set of coordinates, and a set of coordinates that forms runs needs only one record per run. Two stored ranges that overlap or touch describe one run, so the structure merges them at insertion time. After every call, the stored ranges are disjoint, which means no coordinate belongs to two of them, and they stay sorted by start. Sorted and disjoint ranges also have sorted ends, so a single binary search by start finds the only range that can contain a given coordinate.

#### Fix One Half-Open Convention

A **half-open interval** `[start, end)` contains `start` and every coordinate up to but excluding `end`. Its length is `end - start`, and an empty range has `start == end`. Two ranges `[1,3)` and `[3,5)` touch when one end equals the other start. The test is `end >= start`, with no `+ 1` or `- 1`. Closed pairs force those adjustments into every comparison. A closed API such as "add the single value `v`" translates once at the boundary into `[v, v + 1)`. The output translates back by printing `end - 1`.

#### Name The Stored Form And Its Lookup

The ranges live in a `TreeMap` from start to end. Because the ranges are disjoint and merged, this map has exactly one **canonical form** for each coverage set. The same covered coordinates always produce the same entries, whatever order the calls arrive in. Equal coverage sets give equal maps, which makes the structure easy to test against a brute-force oracle.

The lookup tool is the **floor entry**, the entry with the greatest start that is at most a given key. `TreeMap.floorEntry` returns it in O(log n) time. Add uses the floor entry of `l` to find a range that reaches back into the new one. Then it walks forward over the entries whose starts are at most `r`, removing each one it absorbs. Remove uses the same floor entry to find a range that must be cut, and query reads one floor entry and compares its end.

<!-- names: half-open interval, canonical form, floor entry -->

#### Pay For Merges Only Once

Each add creates at most one entry, and the structure deletes each absorbed entry once. The total number of deletions never exceeds the total number of creations. The walk over absorbed entries absorbs O(1) entries per call on average, so each call costs amortized O(log n) including its tree lookups. Remove can split one range into two, which creates one extra entry and keeps the same argument valid.

<!-- stage: variables -->
### Fields The Structure Keeps

The structure keeps one map and one running sum. The sum follows from the map.

- **ends** is a `TreeMap<Long, Long>` that maps each stored start to its end under the `[start, end)` convention.
- **total** is a `long` that always equals the sum of `end - start` over all entries.
- **l and r** are the call arguments, with `l < r` for a non-empty range, and every comparison uses these half-open meanings.

The values stay `long` because a coordinate near 10^9 plus one, or a sum of many lengths, can exceed the `int` range.

<!-- stage: trace -->
### Tracing Merges And Splits

#### A Stream Of Single Points

The first trace feeds the values 1, 3, 2, 7, 6, 5 and 4 to a stream that stores closed points. Each value `v` becomes the range `[v, v + 1)`, so the pointer `l` marks `v` and the pointer `r` marks `v + 1`. The variable `stored` lists the map after the call.

The first two values create separate entries `[1,2)` and `[3,4)`. The value 2 arrives between them. The floor entry `[1,2)` ends exactly at 2, and the entry `[3,4)` starts exactly at 3, so one call fuses all three into `[1,4)`. The values 7, 6 and 5 then grow a second run backward, because each new range ends where the next entry starts. The last value 4 touches both runs and joins them into `[1,8)`. No call scans more than the entries it absorbs.

```trace
{"cells":["0","1","2","3","4","5","6","7","8","9"],"pointers":["l","r"],"steps":[{"at":{"l":1,"r":2},"vars":{"stored":"[1,2)"},"note":"add [1,2). The floor entry does not reach 1, so the start stays 1. No later entry starts inside the new range. The map stores [1,2)."},{"at":{"l":3,"r":4},"vars":{"stored":"[1,2) [3,4)"},"note":"add [3,4). The floor entry does not reach 3, so the start stays 3. No later entry starts inside the new range. The map stores [3,4)."},{"at":{"l":2,"r":3},"vars":{"stored":"[1,4)"},"note":"add [2,3). The floor entry [1,2) reaches 2, so it merges and the start becomes 1. The entry [3,4) starts at 3, which is at most 3, so it merges. The map stores [1,4)."},{"at":{"l":7,"r":8},"vars":{"stored":"[1,4) [7,8)"},"note":"add [7,8). The floor entry does not reach 7, so the start stays 7. No later entry starts inside the new range. The map stores [7,8)."},{"at":{"l":6,"r":7},"vars":{"stored":"[1,4) [6,8)"},"note":"add [6,7). The floor entry does not reach 6, so the start stays 6. The entry [7,8) starts at 7, which is at most 7, so it merges. The map stores [6,8)."},{"at":{"l":5,"r":6},"vars":{"stored":"[1,4) [5,8)"},"note":"add [5,6). The floor entry does not reach 5, so the start stays 5. The entry [6,8) starts at 6, which is at most 6, so it merges. The map stores [5,8)."},{"at":{"l":4,"r":5},"vars":{"stored":"[1,8)"},"note":"add [4,5). The floor entry [1,4) reaches 4, so it merges and the start becomes 1. The entry [5,8) starts at 5, which is at most 5, so it merges. The map stores [1,8)."}]}
```

#### Adds Removes And Queries

The second trace uses the half-open calls of a range module over coordinates 0 to 11. The pointers `l` and `r` mark the call arguments, and `result` appears on queries only.

Adding `[2,6)` and `[8,11)` creates two entries, and adding `[6,8)` bridges the gap between them. The map holds a single entry `[2,11)`. Removing `[4,7)` finds that entry as the floor entry, cuts it out and puts back the two remaining pieces `[2,4)` and `[7,11)`. The query `[3,5)` reads the floor entry `[2,4)`, whose end 4 falls short of 5, so the answer is false. The query `[7,10)` succeeds because the entry starting at 7 ends at 11. The query `[2,4)` succeeds because the end 4 equals the query end, which half-open ranges allow.

```trace
{"cells":["0","1","2","3","4","5","6","7","8","9","10","11"],"pointers":["l","r"],"steps":[{"at":{"l":2,"r":6},"vars":{"stored":"[2,6)"},"note":"add [2,6). The floor entry does not reach 2, so the start stays 2. No later entry starts inside the new range. The map stores [2,6)."},{"at":{"l":8,"r":11},"vars":{"stored":"[2,6) [8,11)"},"note":"add [8,11). The floor entry does not reach 8, so the start stays 8. No later entry starts inside the new range. The map stores [8,11)."},{"at":{"l":6,"r":8},"vars":{"stored":"[2,11)"},"note":"add [6,8). The floor entry [2,6) reaches 6, so it merges and the start becomes 2. The entry [8,11) starts at 8, which is at most 8, so it merges. The map stores [2,11)."},{"at":{"l":4,"r":7},"vars":{"stored":"[2,4) [7,11)"},"note":"remove [4,7). The entry [2,11) overlaps, so it is cut and keeps [2,4) and [7,11)."},{"at":{"l":3,"r":5},"vars":{"stored":"[2,4) [7,11)","result":"false"},"note":"query [3,5). The floor entry [2,4) does not reach up to 5, so the answer is false."},{"at":{"l":7,"r":10},"vars":{"stored":"[2,4) [7,11)","result":"true"},"note":"query [7,10). The floor entry [7,11) covers up to 10, so the answer is true."},{"at":{"l":2,"r":4},"vars":{"stored":"[2,4) [7,11)","result":"true"},"note":"query [2,4). The floor entry [2,4) covers up to 4, so the answer is true."}]}
```

<!-- stage: code -->
### Writing Add, Remove And Query Methods

```java
final class IntervalSet {
    // Half-open ranges [start, end), keyed by start, always disjoint and merged.
    private final TreeMap<Long, Long> ends = new TreeMap<>();
    private long total;

    void add(long l, long r) {
        if (l >= r) return;
        Map.Entry<Long, Long> left = ends.floorEntry(l);
        if (left != null && left.getValue() >= l) {
            drop(left);
            l = left.getKey();
            r = Math.max(r, left.getValue());
        }
        Map.Entry<Long, Long> next;
        while ((next = ends.ceilingEntry(l)) != null && next.getKey() <= r) {
            drop(next);
            r = Math.max(r, next.getValue());
        }
        ends.put(l, r);
        total += r - l;
    }

    void remove(long l, long r) {
        if (l >= r) return;
        Map.Entry<Long, Long> left = ends.floorEntry(l);
        if (left != null && left.getValue() > l) cut(left, l, r);
        Map.Entry<Long, Long> next;
        while ((next = ends.ceilingEntry(l)) != null && next.getKey() < r) cut(next, l, r);
    }

    boolean covers(long l, long r) {
        if (l >= r) return true; // an empty range holds no integer, so every integer in it is covered
        Map.Entry<Long, Long> e = ends.floorEntry(l);
        return e != null && e.getValue() >= r;
    }

    long covered() {
        return total;
    }

    private void drop(Map.Entry<Long, Long> e) {
        ends.remove(e.getKey());
        total -= e.getValue() - e.getKey();
    }

    private void cut(Map.Entry<Long, Long> e, long l, long r) {
        drop(e);
        if (e.getKey() < l) { ends.put(e.getKey(), l); total += l - e.getKey(); }
        if (e.getValue() > r) { ends.put(r, e.getValue()); total += e.getValue() - r; }
    }
}
```

Add absorbs everything that overlaps or touches `[l, r)`, and remove cuts everything that overlaps it. The helper `drop` keeps `total` in step with the map, and `cut` reinserts the pieces that survive on each side. A query on an empty range returns true before any lookup, because it holds no integer. A query on a non-empty range needs only the floor entry of `l`, because disjoint sorted entries leave no other candidate. The number of maximal runs of covered integers equals `ends.size()`, because each entry is one run and touching runs are already merged.

<!-- stage: applicability -->
### Check The Endpoint Convention First

#### Spot The Pattern In A Problem Statement

Reach for a sorted map of merged ranges when public methods add ranges, remove ranges or ask about coverage over time. The coordinate space must be too large for an array. The invariant to protect is that stored ranges stay disjoint, sorted and merged under one endpoint convention after every call. Every method may assume the invariant on entry and must restore it before it returns.

The workload decides the cost. With many updates and few queries, the amortized merge work dominates and stays cheap. With a small coordinate domain such as 0 to 10^5, a plain boolean array or a segment tree with lazy assignment also works. Before choosing, read the update and query counts, and check whether calls arrive online or are known in advance.

#### Avoid The Closed Interval Trap

Closed pairs look simpler, yet they are a false friend here. A closed range `[1,3]` and a closed range `[4,6]` touch even though `3 < 4`. Every comparison then needs a plus one or minus one, which is easy to forget on one side. Translate once at the boundary to half-open ranges and keep every internal comparison free of adjustments.

#### Know Where The Pattern Stops

Touching ranges merge in a range module, but a booking calendar often must keep them apart because two back-to-back reservations are different bookings. Decide whether touching ranges merge before writing the first comparison. If callers need each original range back, this structure loses that information. The same holds when ranges carry different labels. Those designs need a different record.

<!-- stage: exercises -->
### Exercises

#### [Build] Data Stream as Disjoint Intervals (LeetCode 352)
<!-- id: dq39-stream-intervals -->

**Prerequisites.** The sorted map of merged half-open ranges from this lesson.

**Problem.** Design a class `SummaryRanges` with two methods. `addNum(v)` records the integer `v` as seen, and recording a value twice has no further effect. `getIntervals()` returns the seen values as the shortest list of closed pairs `[a, b]`, sorted by `a`. Each pair stands for all integers from `a` to `b` inclusive. Two pairs `[a, b]` and `[c, d]` stay separate only when `c > b + 1`. Store each value `v` internally as the half-open range `[v, v + 1)` and convert an end back by subtracting 1.

**Constraints.** The limits are:
- **`v`** is an `int` with `0 <= v <= 10^9`.
- **Calls** number at most `2 * 10^5`, and they arrive online, so the sequence is not known in advance.
- **Update/query ratio** is about 10 to 1, because `getIntervals` is rare compared with `addNum`.
- **Return value** of `getIntervals` is a new `int[][]`, and the caller may modify it.
- **Empty stream** returns an empty array.

**Example 1.** Input `addNum(1)`, `addNum(3)`, `addNum(7)`, then `getIntervals()`, output `[[1,1],[3,3],[7,7]]`. After `addNum(2)`, the next `getIntervals()` output is `[[1,3],[7,7]]`.

**Example 2.** Input `addNum(5)`, `addNum(5)`, `addNum(4)`, then `getIntervals()`, output `[[4,5]]`, so the repeated value changes nothing.

**Hint.** Which stored entries can a new point touch? How many neighbors does a single point have in a sorted map?

**Changed decision.** Baseline case: inputs are single points, so a new value has at most one left neighbor and one right neighbor to merge.

#### [Vary] Range Module (LeetCode 715)
<!-- id: dq39-range-module -->

**Prerequisites.** The stream exercise above.

**Problem.** Design a class `RangeModule` over the integers, with half-open ranges `[left, right)`. `addRange(left, right)` makes every integer in the range tracked. `removeRange(left, right)` makes every integer in the range untracked. `queryRange(left, right)` returns `true` exactly when every integer in the range is tracked. Ranges that touch or overlap behave as one tracked run.

**Constraints.** The limits are:
- **`left` and `right`** are `int` values with `1 <= left < right <= 10^9`.
- **Calls** number at most `10^5`, and they arrive online.
- **Update/query ratio** is about 1 to 1, so adds, removes and queries all appear in volume.
- **Return value** is `true` or `false` for a query, and the other two methods return nothing.

**Example 1.** Input `addRange(10,20)`, `removeRange(14,16)`, then three queries. Output: `queryRange(10,14)` is true, `queryRange(13,15)` is false and `queryRange(16,17)` is true.

**Example 2.** Input `addRange(5,8)`, `addRange(8,10)`, `queryRange(5,10)`, output true, because the touching ranges merge. After input `removeRange(8,9)`, the same query has output false.

**Hint.** A removal may split one stored entry into a left piece and a right piece. Which entries need cutting, and which need deleting?

**Changed decision.** Removal is added, so an entry can split in two and the structure must reinsert surviving pieces.

#### [Boundary] Touching And Empty Ranges (Author exercise)
<!-- id: dq39-touching-empty -->

**Prerequisites.** The range module exercise above.

**Problem.** A coverage set starts empty. A list of operations arrives, each with a type (`add` or `remove`) and a half-open range `[l, r)` with `l <= r`. An `add` makes the integers of the range covered, and a `remove` makes them uncovered. A range with `l == r` contains no integers and changes nothing. After each operation, report the number of maximal runs of consecutive covered integers. Two runs that touch, where one ends at the coordinate that the next starts at, count as one run.

**Constraints.** The limits are:
- **`l` and `r`** are `long` values with `0 <= l <= r <= 10^12`.
- **Operations** number at most `2 * 10^5`, and the whole list is known in advance.
- **Update/query ratio** is 1 to 1, because every operation also reports a count.
- **Empty range** has `l == r` and must never create or split an entry.
- **Return value** is a `long[]` with one run count per operation.

**Example 1.** Input operations `add [1,3)`, `add [5,7)`, `add [3,5)`, `remove [2,2)`, `remove [3,5)`, output run counts `[1,2,1,1,2]`.

**Example 2.** Input operations `add [0,4)`, `remove [0,4)`, `add [2,2)`, `remove [1,3)`, output run counts `[1,0,0,0]`.

**Hint.** After each operation, the run count is the number of map entries, `ends.size()`. What should the touching test compare for an add, and what should it compare for a remove? Why do these two tests differ by an equality?

**Changed decision.** Empty ranges and touching ends appear together, so add merges on equality while remove does not, and the empty range exits early.

#### [Recognize] Count Integers in Intervals (LeetCode 2276)
<!-- id: dq39-count-intervals -->

**Prerequisites.** The three exercises above.

**Problem.** Design a class `CountIntervals`. `add(left, right)` marks every integer from `left` to `right` inclusive as covered, where the pair is closed. `count()` returns how many distinct integers are covered by all calls so far. Marking an integer twice counts it once. Convert each closed pair into a half-open range internally and keep a running total, because the domain is too large for an array.

**Constraints.** The limits are:
- **`left` and `right`** are `int` values with `1 <= left <= right <= 10^9`.
- **Calls** number at most `10^5`, mixed between `add` and `count`, and they arrive online.
- **Update/query ratio** is about 1 to 1.
- **Return value** of `count` is a `long`.
- **Coordinate domain** is far too large for a boolean array.

**Example 1.** Input `add(2,3)`, `add(7,10)`, `count()`, output 6. After input `add(5,8)`, the covered integers are 2, 3 and 5 through 10, so the `count()` output is 8.

**Example 2.** Input `add(1,1000000000)`, `count()`, output 1,000,000,000. After input `add(1,3)`, which lies inside the covered range, the `count()` output is still 1,000,000,000.

**Hint.** Can `count` read a stored field instead of walking the map? What must each merge do to that field?

**Changed decision.** The query asks for total covered length, so a running sum is kept and every merge adjusts it. The domain size rules out an array.
