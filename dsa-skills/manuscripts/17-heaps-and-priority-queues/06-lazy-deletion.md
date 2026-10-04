<!-- lesson-kind: standard -->
<!-- lesson-id: lazy-deletion -->
## Lazy Deletion

<!-- stage: context -->
### The Parcel Board With Revisions

A courier depot keeps a board of parcels waiting for a van, and each parcel carries an urgency score. Whenever a van is free, the dispatcher takes the most urgent parcel that is still waiting. Through the day the board is edited: a customer upgrades the delivery of a parcel and its score changes, another customer cancels and the parcel must leave the board without ever being sent, and a third parcel is returned to the shelf by mistake and then put back.

The dispatcher used to rebuild the board by hand after every edit, and during the afternoon rush that left vans waiting while she re-sorted the cards. The depot manager would like her to be able to apply an edit in the time it takes to write one line, and to be sure that a cancelled or revised parcel is never sent under its old score.

<!-- stage: naive -->
### Pull The Old Card Out

The obvious repair uses the queue's own removal. To revise a parcel, remove its old entry from the `PriorityQueue` and offer the new one. To cancel, remove the entry and stop.

```java
static void revise(java.util.PriorityQueue<int[]> board, int[] oldCard, int newScore) {
    board.remove(oldCard);                                  // find and delete the old entry
    board.offer(new int[]{newScore, oldCard[1]});           // {score, parcel id}
}
```

With a board of a few dozen cards this behaves correctly, and a revised parcel is dispatched under its new score only.

<!-- stage: bottleneck -->
### Finding A Card Means Reading The Board

A heap does not know where an arbitrary entry is. `remove(Object)` has to walk the array from the front until it finds an entry that is equal to the argument, which is O(n) for a board of `n` cards, and then it repairs the heap around the hole. A day with `n` edits therefore costs O(n^2), and for a hundred thousand parcels that is again billions of steps. The call `contains` has the same linear cost, so even checking whether a parcel is still on the board is expensive.

The waste comes from insisting that the heap must always hold only live entries. The dispatcher never looks at a card in the middle of the board. She looks at the top one, and she needs the top one to be right. Entries that are out of date but buried under better ones do no harm at the moment they are buried. If outdated entries could simply be left in place and recognised when they surface, an edit would cost one insertion, and the only repair needed would happen at the top, where it is cheap.

<!-- stage: insight -->
### Delete When It Surfaces

**Lazy deletion** means that an edit never touches the old entry. To revise, insert a new entry. To cancel, insert nothing. In both cases the change is written to **companion state**, a small side table that says what is currently true: a map from parcel id to its latest version, or a map from a value to the number of its copies that are logically removed. Edits cost O(1) for the table and O(log n) for the insertion.

Before the root is used, in a peek or a poll, run the **root cleanup**: while the heap is not empty and its root disagrees with the companion state, poll it and drop it, and update the table if the discard consumed a pending removal. Only when the root is valid is it returned. The invariant is that after the cleanup the root is either a live entry or the heap is empty, while entries below the root are allowed to be stale.

<!-- names: lazy deletion, companion state, root cleanup -->

Each entry is inserted once and discarded at most once, so the cleanup work over a whole run is paid for by the insertions, and every operation is O(log n) amortised. The price is memory and bookkeeping. Stale entries stay in the heap until they surface, so the heap's own `size()` is larger than the number of live items, and the true count must be kept in the companion state. Where equal values may have several copies, the table has to count them, because a single flag could not say that two out of three copies of a value are gone.

<!-- stage: variables -->
### Entries, Versions And Pending Counts

There are two common shapes of companion state. For priorities that change, each id has a version counter. Every heap entry stores `{priority, id, version}`, the table stores the current version of each id, and an entry is stale when its version differs from the table's, or when the id has been removed. For plain removals of values, the table maps each value to a pending count. An entry whose value has a positive pending count is stale, and discarding it lowers the count by one. A separate `live` counter is updated at the time of the edit, not at the time of the discard, since it describes the logical contents. The heap's size, by contrast, counts every entry that has not yet surfaced.

<!-- stage: trace -->
### Removed Values Wait Under The Root

The first run applies the operations `5, 3, 8, -3, 0, -5, 0`, where a positive number adds that value, a negative number removes one copy of its absolute value, and 0 asks for the current minimum. Three values enter the heap. Removing 3 only writes a pending count of one, and the 3 stays at the root. The first query runs the cleanup, finds that the root 3 is pending, discards it, and then reports the next root, which is 5. Removing 5 repeats the pattern, and the second query discards the 5 and reports 8.

The second run uses the operations `4, 4, 6, -4, 0, -4, 0` and has two copies of one value. The first removal makes one of the two 4s stale, and the query discards exactly one of them and still reports 4, because the other copy is live. The second removal marks the remaining 4, and the second query discards it and reports 6. The step to study is the first query of the second run, where a pending count of one cleans only one of two equal entries.

```trace
{"cells":[5,3,8,-3,0,-5,0],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"heap":"[5]","pending":"{}","output":"[]"},"note":"Add 5. It is inserted into the heap and nothing else changes."},{"at":{"i":1},"vars":{"heap":"[3,5]","pending":"{}","output":"[]"},"note":"Add 3. It is inserted into the heap and nothing else changes."},{"at":{"i":2},"vars":{"heap":"[3,5,8]","pending":"{}","output":"[]"},"note":"Add 8. It is inserted into the heap and nothing else changes."},{"at":{"i":3},"vars":{"heap":"[3,5,8]","pending":"{3:1}","output":"[]"},"note":"Remove 3. Only the pending count of 3 rises to 1, and the heap is not touched."},{"at":{"i":4},"vars":{"heap":"[5,8]","pending":"{}","output":"[5]"},"note":"Query. The cleanup discards the stale root 3 and then finds a live root, so the minimum is 5."},{"at":{"i":5},"vars":{"heap":"[5,8]","pending":"{5:1}","output":"[5]"},"note":"Remove 5. Only the pending count of 5 rises to 1, and the heap is not touched."},{"at":{"i":6},"vars":{"heap":"[8]","pending":"{}","output":"[5,8]"},"note":"Query. The cleanup discards the stale root 5 and then finds a live root, so the minimum is 8."}]}
```

```trace
{"cells":[4,4,6,-4,0,-4,0],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"heap":"[4]","pending":"{}","output":"[]"},"note":"Add 4. It is inserted into the heap and nothing else changes."},{"at":{"i":1},"vars":{"heap":"[4,4]","pending":"{}","output":"[]"},"note":"Add 4. It is inserted into the heap and nothing else changes."},{"at":{"i":2},"vars":{"heap":"[4,4,6]","pending":"{}","output":"[]"},"note":"Add 6. It is inserted into the heap and nothing else changes."},{"at":{"i":3},"vars":{"heap":"[4,4,6]","pending":"{4:1}","output":"[]"},"note":"Remove 4. Only the pending count of 4 rises to 1, and the heap is not touched."},{"at":{"i":4},"vars":{"heap":"[4,6]","pending":"{}","output":"[4]"},"note":"Query. The cleanup discards the stale root 4 and then finds a live root, so the minimum is 4."},{"at":{"i":5},"vars":{"heap":"[4,6]","pending":"{4:1}","output":"[4]"},"note":"Remove 4. Only the pending count of 4 rises to 1, and the heap is not touched."},{"at":{"i":6},"vars":{"heap":"[6]","pending":"{}","output":"[4,6]"},"note":"Query. The cleanup discards the stale root 4 and then finds a live root, so the minimum is 6."}]}
```

<!-- stage: code -->
### A Min Bag With Delayed Removal

```java
final class LazyMinBag {
    private final java.util.PriorityQueue<Integer> heap = new java.util.PriorityQueue<>();
    private final java.util.HashMap<Integer, Integer> pending = new java.util.HashMap<>();
    private int live;                                   // logical size

    void add(int v) { heap.offer(v); live++; }
    void remove(int v) { pending.merge(v, 1, Integer::sum); live--; }   // caller guarantees v is present
    int size() { return live; }
    Integer min() { cleanRoot(); return heap.peek(); }

    private void cleanRoot() {
        while (!heap.isEmpty()) {
            Integer top = heap.peek();
            Integer count = pending.get(top);
            if (count == null) return;                  // root is live
            if (count == 1) pending.remove(top); else pending.put(top, count - 1);
            heap.poll();                                // discard one stale copy
        }
    }
}
```

Adding and removing cost O(log n) and O(1) respectively. The cleanup is a loop, and its iterations are paid for by earlier additions, so any sequence of `m` operations runs in O(m log m) time. The `Integer` objects are compared with `count == 1` by unboxing, and `pending.get(top)` returns `null` for a value with no pending removals, which is the signal that the root is live. The heap may hold more entries than `size()` reports, and that is intended.

<!-- stage: applicability -->
### When Updates Outnumber Surfacing

Use lazy deletion when a heap is the right structure for the extreme item, but items must be cancelled, replaced, expired or counted down in the middle of its life. The invariant is that, before the root is trusted, stale roots have been discarded, and the companion state alone defines what is live. Keep the logical size in that state, and never infer it from the heap.

The false friend is the pair of library calls `remove(Object)` and `contains`. They look like the natural way to delete and to test membership, and they work on small examples, but each one scans the array and costs O(n). On entries stored as arrays they have a second hazard, since they compare by `equals`, which for an array is identity, so an equal-looking array may not be found at all. Another false friend is a `TreeMap` or `TreeSet`: it removes any item in O(log n) and is the right tool when neighbours or ranks are needed, but it is heavier than a heap when only the extreme item is read.

Do not use it when stale entries could pile up without ever reaching the root, as in a long run in which the root is rarely read, because memory then grows with the number of edits and not with the number of live items. Do not forget that a pending removal must refer to an item that is actually present. In Java, count stale items in a map, never in the heap's `size()`, and test the root in a loop and not with a single `if`.

<!-- stage: exercises -->
### Exercises

#### [Build] Versioned Priorities (Author exercise)
<!-- id: hp-versioned-priorities -->

**Prerequisites.** The version table and the root cleanup of this lesson.

**Problem.** Maintain a set of ids with priorities, and process the operations in `ops`. The operation `{0, id, priority}` sets the priority of an id, adding it if it is not present. The operation `{1}` pops the id with the smallest priority, using the smaller id among equal priorities, removes that id from the set, and records it. A pop on an empty set records -1. Return the recorded values. Do not call `remove(Object)` or `contains` on the heap.

**Constraints.** 1 <= ops.length <= 10^5, 0 <= id <= 10^5, and 1 <= priority <= 10^9.

**Example 1.** Input `ops = [[0, 1, 5], [0, 2, 3], [0, 1, 1], [1], [1], [1]]`, output `[1, 2, -1]`.

**Example 2.** Input `ops = [[0, 7, 4], [0, 7, 9], [0, 3, 6], [1], [1]]`, output `[3, 7]`.

**Hint.** When an id is set again, what do you insert, and how does an old entry for the same id recognise that it is outdated?

**Changed decision.** First rung: a changed priority inserts a new entry and leaves the old one in place, with a version number to tell them apart.

#### [Vary] Delayed Removal Counts (Author exercise)
<!-- id: hp-delayed-removal-counts -->

**Prerequisites.** Versioned Priorities above.

**Problem.** Maintain a multiset of positive integers. In `ops`, a positive number `x` adds `x`, a negative number `-x` removes one copy of `x`, which is guaranteed to be present, and 0 asks for the current minimum without removing it. Return the answer to each query, or -1 if the multiset is empty.

**Constraints.** 1 <= ops.length <= 10^5 and each value has absolute value at most 10^9.

**Example 1.** Input `ops = [5, 3, 8, -3, 0, -5, 0, 0]`, output `[5, 8, 8]`.

**Example 2.** Input `ops = [2, -2, 0]`, output `[-1]`.

**Hint.** What does the table store when equal values can repeat? What must a query do before it reads the root?

**Changed decision.** No ids exist, so the companion state is a count per value, and the cleanup consumes one count for every stale root.

#### [Boundary] Several Stale Roots (Author exercise)
<!-- id: hp-several-stale-roots -->

**Prerequisites.** The two exercises above.

**Problem.** Use the same operations as in the previous exercise. Return `[discarded, physical, live]`: the number of stale entries that the queries have discarded, the number of entries left in the heap at the end, and the number of live values at the end.

**Constraints.** 1 <= ops.length <= 10^5 and each value has absolute value at most 10^9.

**Example 1.** Input `ops = [4, 4, 4, -4, -4, 0]`, output `[2, 1, 1]`.

**Example 2.** Input `ops = [1, 2, 3, -2, -3, 0, 0]`, output `[0, 3, 1]`.

**Hint.** Is one `if` enough when several removed entries sit at the top together? Which stale entries can never be discarded by a query?

**Changed decision.** Several stale entries may share the top of the heap, so the cleanup becomes a loop, and the report exposes stale entries that remain buried.

#### [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-sliding-window-median -->

**Prerequisites.** The three exercises above. The two-heap layout is previewed in the hint and developed in the next lesson.

**Problem.** Given an integer array `nums` and a window length `k`, return the median of every window of `k` consecutive values, as `double` values. For an even `k` the median is the average of the two middle values.

**Constraints.** 1 <= k <= nums.length <= 10^5 and every value is any `int`, including `-2147483648` and `2147483647`.

**Example 1.** Input `nums = [3, 9, 1, 7, 5, 2]`, `k = 3`, output `[3.0, 7.0, 5.0, 5.0]`.

**Example 2.** Input `nums = [4, 6, 2, 8]`, `k = 2`, output `[5.0, 4.0, 5.0]`.

**Hint.** Keep the smaller half of the window in a max-heap and the larger half in a min-heap, with sizes that differ by at most one. When a value leaves the window, which half owned it, and how do you delete it without searching?

**Changed decision.** Values now expire by age, so each departure is a lazy deletion in one of two heaps, and the sizes of the halves must be counted logically.
