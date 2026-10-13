<!-- lesson-kind: combination -->
<!-- lesson-id: map-and-dynamic-array -->
## Find A Slot And Pick From Array

<!-- stage: context -->
### Why A Random Pick Gets Slower

A video platform keeps a pool of live streaming servers. Servers join the pool when traffic grows and leave when they fail a health check. Every incoming request asks for one server chosen uniformly at random from the pool. In the morning the pool holds 20 servers and nothing is noticeable. By the evening the pool holds 50,000 servers, joins and removals arrive thousands of times per second, and the routing code shows up first in every profile.

The pool must answer three questions quickly. Is this server already in the pool? Can the pool drop this server right now? Which server is the uniform random choice for the next request? One standard collection answers each question well, and no single standard collection answers all three. This lesson asks how to combine two collections so that insert, remove and random pick each cost constant time on average.

<!-- stage: contributions -->
### What The Map And Array Each Add

The lesson Pair A Map With Ordered Storage showed that a hash map can point into ordered storage, and the lesson Pick A Random Value In Constant Time showed that a dense array turns one random integer into one uniform element. Both ideas are needed here, and each covers what the other cannot.

The hash map answers membership and location. Given a server identifier, the map returns the array position that holds it, in constant expected time. An array cannot do that without scanning. The dynamic array answers selection and cheap removal at its end. Any position from 0 to size minus 1 is equally likely to be drawn, and removing the last element moves nothing. A map cannot do either, because its iteration order is not a numbered sequence. Together, the map supplies the address of a value and the array supplies a dense numbering of all values.

<!-- stage: naive -->
### Keeping The Pool In One List

The direct plan keeps the servers in a single `ArrayList`. Insert scans the list to reject duplicates. Remove searches for the value and deletes it. The random pick draws an index.

```java
final class ListPool {
    private final java.util.ArrayList<Integer> servers = new java.util.ArrayList<>();
    private final java.util.Random rng = new java.util.Random(7);

    boolean insert(int id) {
        if (servers.contains(id)) return false;     // linear scan for a duplicate
        servers.add(id);
        return true;
    }

    boolean remove(int id) {
        return servers.remove(Integer.valueOf(id)); // linear search, then shift the tail left
    }

    int getRandom() {
        return servers.get(rng.nextInt(servers.size())); // one draw, one read
    }
}
```

On a pool of 50,000 servers, a removal near the front searches a few positions and then shifts almost 50,000 elements one place left. A removal of a missing server scans all 50,000 and finds nothing. Only the random pick is fast.

```predict
A pool holds 50,000 servers in an ArrayList. Which of insert, remove and getRandom has a cost that grows with the pool size, and what part of each call causes it?

Insert and remove both grow, at O(n) per call. Insert pays for the duplicate scan with contains. Remove pays for the search and then for shifting every later element one place left. Only getRandom stays at O(1), because it reads one index.
```

<!-- stage: bottleneck -->
### Counting Where The List Spends Its Time

Two separate costs hide in the list version, and both are O(n). The first cost is finding a value. The `contains` call and the search inside `remove(Object)` compare the argument with elements one after another, and a missing value costs the whole list. The second cost is closing the gap. `ArrayList.remove` keeps the elements contiguous by moving every later element one position left. That shift costs O(n) for a removal near the front and O(1) only for a removal at the very end.

A pool with 50,000 servers and 5,000 removals per second performs about 250 million element moves per second on the shifting alone. Replacing the list with a `HashSet` fixes the first cost and breaks the third operation, because a set has no numbered positions. Drawing a random element from a set means iterating to the k-th element, which is O(n) again. The bottleneck is that one structure supplies either fast lookup or numbered positions, never both.

<!-- stage: insight -->
### Keep Each Value's Slot In The Map

#### Giving Every Value A Slot

Store the values in a dense array and store, for every value, the index where it lives. That index is the value's **slot**. A hash map from value to slot gives constant expected lookup. The array gives a uniform random pick, because every index from 0 to size minus 1 is a real value with no holes.

#### Removing By Swap-With-Last

Removal is the only hard part, because deleting from the middle leaves a hole. Avoid the hole by choosing which element leaves the array. Copy the last element into the removed element's slot, then shrink the array by one. That move is called **swap-with-last**. It costs O(1) because it touches one slot and the end of the array, and the array stays dense.

<!-- names: slot, swap-with-last, agreement -->

#### Repairing What The Move Broke

Swap-with-last moves one value to a new position, so the map entry of the moved value is now stale. The operation must rewrite that entry to the removed slot, and then delete the removed value's own entry. The fact that must hold after every public call is **agreement** between the two structures. Every index `i` below the size satisfies `slotOf.get(items[i]) == i`, and the map holds exactly `size` entries. A single missed repair breaks agreement, and the next lookup silently points at the wrong element.

<!-- stage: variables -->
### State The Pool Keeps

The pool owns four fields, and the invariant ties them together. No caller reads these fields directly, so every operation can restore the invariant before it returns.

- **items** is the int array of current values, and positions `0..size-1` are meaningful.
- **size** is the count of current values and the first unused index.
- **slotOf** is the hash map from a value to the index where `items` holds it.
- **rng** is the `Random` that supplies the index for a pick.

The invariant is the agreement from the insight: `slotOf.get(items[i]) == i` for every `i < size`, and `slotOf.size() == size`. An insert appends at `size` and records that index. A remove performs swap-with-last and repairs one entry. A pick reads only `items`, so it changes nothing.

<!-- stage: trace -->
### Tracing Two Removals From The Pool

#### Removing A Value From The Middle

Start with the pool `[5, 8, 2, 9]`, whose map holds 5 at slot 0, 8 at slot 1, 2 at slot 2 and 9 at slot 3. Remove 8. The map answers that 8 sits at slot 1, and the last element is 9 at slot 3.

The operation copies 9 into slot 1, so the array reads `[5, 9, 2, 9]` for a moment. The map entry for 9 still says slot 3, so the operation rewrites it to slot 1. The operation then deletes the key 8 and lowers `size` to 3. The meaningful part of the array is `[5, 9, 2]`, and the old 9 at slot 3 is a stale leftover that no lookup can reach.

```trace
{"cells":[5,8,2,9],"pointers":["removed","last"],"steps":[{"at":{"removed":1,"last":3},"vars":{"items":"[5,8,2,9]","size":4},"note":"remove(8): the map says 8 sits at slot 1, and the last slot is 3 holding 9."},{"at":{"removed":1,"last":3},"vars":{"items":"[5,9,2,9]","size":4},"note":"Copy 9 from slot 3 into slot 1."},{"at":{"removed":1,"last":3},"vars":{"items":"[5,9,2,9]","size":4,"slotOf[9]":1},"note":"Repair the map: 9 now lives at slot 1."},{"at":{"removed":1,"last":3},"vars":{"items":"[5,9,2]","size":3},"note":"Delete the key 8 and lower size to 3. The meaningful array is [5,9,2]."}]}
```

#### Removing The Last Element

Start with the pool `[4, 7, 1]` and remove 1. The map answers slot 2, and the last slot is also 2. The removed value and the moved value are the same element.

The copy would write 1 onto itself, which changes nothing. The map repair would set the entry for 1 to slot 2, and the delete that follows removes the key anyway. Everything depends on the order. If the delete ran first and the repair second, the repair would add the key 1 back, and the map would hold one entry too many.

```trace
{"cells":[4,7,1],"pointers":["removed","last"],"steps":[{"at":{"removed":2,"last":2},"vars":{"items":"[4,7,1]","size":3},"note":"remove(1): the map says 1 sits at slot 2, and the last slot is 2 holding 1."},{"at":{"removed":2,"last":2},"vars":{"items":"[4,7,1]","size":3},"note":"Copy 1 from slot 2 into slot 2. The copy writes the value onto itself."},{"at":{"removed":2,"last":2},"vars":{"items":"[4,7,1]","size":3,"slotOf[1]":2},"note":"Repair the map: 1 now lives at slot 2."},{"at":{"removed":2,"last":2},"vars":{"items":"[4,7]","size":2},"note":"Delete the key 1 and lower size to 2. The meaningful array is [4,7]."}]}
```

<!-- stage: code -->
### Implementing The Pool With Swap-With-Last

```java
final class IndexedPool {
    private int[] items = new int[4];
    private int size = 0;
    private final java.util.HashMap<Integer, Integer> slotOf = new java.util.HashMap<>();
    private final java.util.Random rng;

    IndexedPool(long seed) { rng = new java.util.Random(seed); }

    /** Appends id when absent. Time O(1) amortized, Space O(1) extra. Invariant: agreement holds on exit. */
    boolean insert(int id) {
        if (slotOf.containsKey(id)) return false;           // reject duplicates in O(1)
        if (size == items.length) items = java.util.Arrays.copyOf(items, size * 2); // doubling gives amortized O(1)
        items[size] = id;                                   // the new value takes the first unused slot
        slotOf.put(id, size);                               // record where it lives
        size++;
        return true;
    }

    /** Removes id by swap-with-last. Time O(1) expected, Space O(1). Invariant: agreement holds on exit. */
    boolean remove(int id) {
        Integer slot = slotOf.get(id);                      // locate the value in O(1)
        if (slot == null) return false;                     // absent values change nothing
        int last = items[size - 1];                         // the value that will fill the hole
        items[slot] = last;                                 // overwrite the removed value
        slotOf.put(last, slot);                             // repair the moved value's slot first
        slotOf.remove(id);                                  // then delete the removed key, so a self-move stays deleted
        size--;                                             // the old last index is no longer meaningful
        return true;
    }

    /** Returns a uniform current value. Time O(1), Space O(1). Requires size > 0. */
    int getRandom() {
        return items[rng.nextInt(size)];                    // every index below size holds a real value
    }
}
```

The cost of each operation is constant on average. The hash map lookup is O(1) expected, the array write is O(1), and the array doubling is O(1) amortized over many inserts. The space is O(n) for the array and the map together. The order of `put` before `remove` in `remove` is deliberate and matters only for the case where the removed value is the last element.

<!-- stage: applicability -->
### When A Map And Array Fit

#### Recognizing The Pattern

Reach for this pair when a problem asks for membership checks, deletion and uniform random selection in the same data structure, all at constant expected cost. The cue is the combination of "random element" with "remove by value". Either request alone has a simpler structure.

An **invariant** is a fact that every public operation must restore before it returns, and here the invariant is agreement between the map and the array. Write the invariant first and let it dictate the order of the steps inside `remove`.

#### Finding The False Friend

A **false friend** is a structure that looks like it solves the problem and fails on one required operation. Two qualify here. A `HashSet` gives constant lookup and removal, yet it has no numbered positions, so a uniform pick costs O(n). An `ArrayList` gives a constant random pick, yet `remove(int)` shifts the tail and `remove(Object)` also searches, so removal costs O(n).

#### Avoiding Java Hazards

The overloads `remove(int index)` and `remove(Object o)` on a list are easy to confuse when the values are integers. Comparing two `Integer` objects with `==` works only for small cached values, so compare with `equals` or unbox first. The structure fits poorly when the order of elements matters or when removals need ordering by age. Chapter 33 handles recency order with the map and linked list pair instead.

<!-- stage: exercises -->
### Exercises

#### [Build] Remove By Swap (Author exercise)
<!-- id: ds-remove-by-swap -->

**Prerequisites.** The `IndexedPool` fields and the agreement invariant in this lesson.

**Problem.** A pool stores distinct `int` values in a dense list `items` and a map `slotOf` from each value to its index in `items`. Agreement holds when `slotOf.get(items.get(i)) == i` for every index `i` and `slotOf.size() == items.size()`. Implement `boolean remove(int value)` that returns `false` and changes nothing when `value` is absent. Otherwise it removes `value` in O(1) expected time by moving the last element into the vacated index, repairing the moved value's entry in `slotOf`, and shrinking the list. After every call to `insert` or `remove`, a check method `agrees()` must return `true`.

**Constraints.** The limits are:
- **Values** are distinct `int` values in the range `0..10^9`.
- **Size** is at most `10^5`.
- **Mutation** is allowed on `items` and `slotOf` only.
- **Order** of the remaining elements is unspecified after a removal.
- **Cost** of each operation is O(1) expected.

**Example 1.** Input is the inserts 5, 8, 2, 9 in that order, then `remove(8)`. The output is `true`, `items = [5,9,2]` and the map sends 5 to 0, 9 to 1 and 2 to 2.

**Example 2.** Input is `remove(7)` and then `remove(5)` on that state. The output is `false` with nothing changed, then `true` with `items = [2,9]`.

**Hint.** Which single map entry describes an element whose index just changed? Does the removed value's own entry still describe a real element?

**Changed decision.** First exercise on the pair: the removal now repairs a second structure, and a check method proves agreement after each call.

#### [Vary] Insert Delete GetRandom O(1) With A Different Pick (LeetCode 380)
<!-- id: ds-random-excluding -->

**Prerequisites.** The Remove By Swap exercise above.

**Problem.** Extend the pool with `int getRandomExcluding(int value)`. It returns a current value chosen uniformly among all current values that differ from `value`. It returns `-1` when no such value exists. The given `value` may be absent from the pool, and then every current value qualifies. The operation draws exactly one random integer and uses O(1) worst-case time, so it must not redraw in a loop.

**Constraints.** The limits are:
- **Values** are distinct `int` values in the range `0..10^9`, so `-1` never collides with a stored value.
- **Size** is between 0 and `10^5`.
- **Mutation** is none; the operation reads state only.
- **Randomness** comes from the one `java.util.Random` that the pool owns, created from a seed in the constructor.
- **Cost** is O(1) worst case after the map lookup.

**Example 1.** Input is the pool 3, 6, 9 and the call `getRandomExcluding(6)`. The output is 3 or 9, each with probability 1/2.

**Example 2.** Input is the pool holding only 4 and the call `getRandomExcluding(4)`. The output is `-1`.

**Hint.** When `value` is present, draw an index from a range one shorter than `size`. If the draw hits the slot of `value`, which other index has not yet been offered? When `value` is absent, every current value qualifies, so draw from the full range.

**Changed decision.** The output contract changes from any current value to any value except one, so the random index range shrinks and one index is redirected.

#### [Boundary] Last-Slot Removal (Author exercise)
<!-- id: ds-last-slot-removal -->

**Prerequisites.** The Remove By Swap exercise above.

**Problem.** In a pool using swap-with-last, the removed value occupies the last index when the vacated index equals `size - 1`. Then the moved value and the removed value are the same element. Implement `remove` so that this case leaves the map without the removed key and without any extra entry. Show what goes wrong when the map repair runs after the key deletion. Include the case of a pool with exactly one element.

**Constraints.** The limits are:
- **Values** are distinct `int` values in the range `0..10^9`.
- **Size** before the call is at least 1.
- **Repair** is one `put` for the moved value and one `remove` for the deleted key.
- **Result** keeps `slotOf.size() == items.size()`.

**Example 1.** Input is the pool `[4,7,1]` and `remove(1)`. The output is `true`, `items = [4,7]`, and the map holds only 4 and 7.

**Example 2.** Input is the pool `[6]` and `remove(6)`. The output is `true`, `items = []`, and the map is empty.

**Hint.** When the removed index and the last index are equal, which of the two map updates should win?

**Changed decision.** The moved value and the removed value become the same element, so the order of the two map updates decides whether a deleted key survives.

#### [Recognize] Duplicate Values Pool (LeetCode 381)
<!-- id: ds-duplicate-values -->

**Prerequisites.** All three exercises above.

**Problem.** A multiset pool accepts repeated values. The array `items` holds one entry per occurrence. For each value the map keeps an int array of the indices where that value occurs, and the array grows by doubling. Implement `boolean insert(int value)` that returns `true` when the value was absent before, `boolean remove(int value)` that removes one occurrence and returns `true` when one existed, `int countOf(int value)` that returns the multiplicity, and `int getRandom()` that returns a value with probability equal to its multiplicity divided by `size`. All operations cost O(1) expected, with doubling amortized.

**Constraints.** The limits are:
- **Values** are `int` values in the range `0..10^9`.
- **Size** is at most `10^5` occurrences.
- **Index lists** are plain `int[]` arrays with a count, with no set classes.
- **getRandom** is called only when `size > 0`.
- **Cost** is O(1) expected per operation.

**Example 1.** Input is the inserts 3, 3, 8. The output is `countOf(3) = 2`, and `getRandom()` returns 3 with probability 2/3 and 8 with probability 1/3.

**Example 2.** Input is `remove(3)` then `remove(5)` on that state. The output is `true` with `countOf(3) = 1`, then `false`.

**Hint.** An array slot that moves must update one entry in its value's index list. What extra number per array slot lets you find that entry in O(1)?

**Changed decision.** One value now owns several slots, so the map stores a growing list per value and every array slot remembers its position in that list.
