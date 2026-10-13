<!-- lesson-kind: standard -->
<!-- lesson-id: constant-time-composition -->
## Pair A Map With Ordered Storage

<!-- stage: context -->
### Why Disconnects Slow A Sampling Service

A gateway tracks the id of every open connection. A health monitor asks for the connection at position `i` so it can sample one at random. A disconnect handler removes the id of a closed connection. With 200,000 open connections and thousands of disconnects per second, the handler becomes the busiest code in the process. Profiling shows that nearly all of its time sits in one call that removes an id from a list.

The list answers the sampling question well, because reading position `i` takes one step. It answers the removal question badly, because the handler must find the id first and then close the gap. This lesson asks how one class can answer both questions in constant time, and what it must keep true between calls.

<!-- stage: naive -->
### Keeping Only A List

The tempting design stores the ids in one `ArrayList` and nothing else. Insertion appends to the end. Sampling reads a position. Removal searches for the id and deletes it.

```java
import java.util.ArrayList;
import java.util.List;

final class ListOnlyIds {
    private final List<Integer> ids = new ArrayList<>();

    boolean insert(int id) {
        if (ids.contains(id)) return false;   // a linear scan on every insert
        ids.add(id);
        return true;
    }

    boolean remove(int id) {
        return ids.remove(Integer.valueOf(id));   // a linear scan, then a shift of the tail
    }

    int getAt(int i) {
        return ids.get(i);
    }
}
```

The class is correct. With ids `[40, 17, 93, 52, 8]`, calling `remove(17)` leaves `[40, 93, 52, 8]`, and `getAt(1)` returns 93.

```predict
Which operations of ListOnlyIds cost O(1) with 200,000 ids, and which cost O(n)?

Only getAt costs O(1), because it reads one position. insert must scan for a duplicate, and remove must scan for the id and then shift every later element left, so both cost O(n).
```

<!-- stage: bottleneck -->
### Two Linear Scans Hide In One Class

The list gives position access in O(1) but gives no way to ask where an id sits. The method `contains` compares the id against elements one by one, so it takes O(n) time. The method `remove(Object)` does the same scan and then shifts the elements after the gap, so a removal near the front moves almost n elements. With n equal to 200,000 and thousands of calls per second, the scans dominate the whole service.

A `HashSet` fixes the lookup, because membership takes O(1) on average. A `HashSet` has no positions, so it cannot answer `getAt(i)`. Keeping both a set and a list fails differently. The removal from the list still scans and shifts, and the two collections can disagree about which ids exist. The class needs one structure whose strength is lookup, one whose strength is position, and a rule that connects them.

<!-- stage: insight -->
### Letting Each Structure Answer One Question

#### Dividing The Work

A `HashMap` from id to slot answers "where is this id" in O(1) on average. An `ArrayList` of ids answers "which id is at slot `i`" in O(1) and appends in amortized O(1). Neither structure alone answers both questions. Together they do, as long as every entry of the map points at the slot that really holds that id. Each stored fact is a **cross-reference**, a fact stored in one structure that names a location in the other.

The **invariant** of the class is that for every id in the list, `slotOf.get(id)` equals the position of that id in the list, and the map holds no other entries. Insertion keeps it by appending the id and recording its slot. A removal must break it for a moment and then restore it before the operation returns.

#### Closing The Gap Without Shifting

Deleting from the middle of a list shifts every later element, which costs O(n). The standard remedy is **swap with last**. Copy the final element into the freed slot, then delete the final slot, which costs O(1) because nothing sits after it. The order of the ids changes, since one id jumped to a new slot. The contract must say so, and this lesson makes the jump visible by returning the id that moved.

#### Restoring The Moved Entry

The id that jumped now sits at a different position, so its map entry is wrong. The **repair** is one `put` that rewrites that entry to the freed slot. The id being removed also needs its entry deleted. When the removed id was itself the final element, nothing jumps. The repair must then not run in a way that writes the removed id back into the map. Placing the delete of the removed entry after the repair of the moved entry makes both cases correct.

<!-- names: cross-reference, swap with last, repair -->

<!-- stage: variables -->
### Variables Of The Paired Class

The class holds two fields, and each operation touches both. These entities need names before the trace.

- **values** is the `ArrayList<Integer>` that owns the order and answers `getAt(i)`.
- **slotOf** is the `HashMap<Integer, Integer>` from a value to its position in `values`.
- **slot** is the position of the value being removed, read from `slotOf`.
- **last** is the value at the final position of `values`, which is the one that moves. The trace marks its position with the pointer `lastSlot`.
- **moved** is the returned result: `last` when it changed position, or `-1` when no value moved.

Values are non-negative, so `-1` never collides with a real value.

<!-- stage: trace -->
### Tracing Two Removals

#### Removing A Value From The Middle

Start with values `[40, 17, 93, 52, 8]`. The call `remove(17)` first reads `slotOf.get(17)`, which gives slot 1. The final value is 8. The class copies 8 into slot 1, so the list reads `[40, 8, 93, 52, 8]` for one moment, with 8 stored twice. Then it writes `slotOf.put(8, 1)`, which is the repair. It deletes the entry for 17 and shrinks the list. The result is `[40, 8, 93, 52]`, and the call returns 8.

```trace
{"cells":[40,17,93,52,8],"pointers":["slot","lastSlot"],"steps":[{"at":{"slot":-1,"lastSlot":-1},"vars":{"values":"[40,17,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:4"},"note":"Start. The list holds [40, 17, 93, 52, 8] and slotOf maps each value to its position. The call is remove(17)."},{"at":{"slot":1,"lastSlot":4},"vars":{"values":"[40,17,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:4","slot":1,"last":8},"note":"slotOf.get(17) gives slot 1. The final value is 8, stored at position 4."},{"at":{"slot":1,"lastSlot":4},"vars":{"values":"[40,8,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:4","slot":1,"last":8},"note":"Copy 8 into slot 1. The list now reads [40, 8, 93, 52, 8], so 8 is stored twice for a moment."},{"at":{"slot":1,"lastSlot":4},"vars":{"values":"[40,8,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:1","slot":1,"last":8},"note":"Repair: slotOf.put(8, 1). The entry for 8 now names slot 1."},{"at":{"slot":1,"lastSlot":4},"vars":{"values":"[40,8,93,52,8]","slotOf":"40:0,93:2,52:3,8:1"},"note":"Delete the entry for 17. Only the entry for 17 is removed."},{"at":{"slot":1,"lastSlot":3},"vars":{"values":"[40,8,93,52]","slotOf":"40:0,93:2,52:3,8:1","moved":8},"note":"Drop the final position. The list reads [40, 8, 93, 52] and the call returns 8."}]}
```

#### Removing The Final Value

The second case removes the value that is itself last. The call `remove(8)` reads slot 4, and the final value is also 8. The copy writes 8 into slot 4, which changes nothing. The repair writes `slotOf.put(8, 4)`, and the next step deletes the entry for 8, so the stale write disappears. The list shrinks to `[40, 17, 93, 52]`, and the call returns -1 because no value moved.

```trace
{"cells":[40,17,93,52,8],"pointers":["slot","lastSlot"],"steps":[{"at":{"slot":-1,"lastSlot":-1},"vars":{"values":"[40,17,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:4"},"note":"Start. The list holds [40, 17, 93, 52, 8] and slotOf maps each value to its position. The call is remove(8)."},{"at":{"slot":4,"lastSlot":4},"vars":{"values":"[40,17,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:4","slot":4,"last":8},"note":"slotOf.get(8) gives slot 4. The final value is 8, stored at position 4."},{"at":{"slot":4,"lastSlot":4},"vars":{"values":"[40,17,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:4","slot":4,"last":8},"note":"Copy 8 into slot 4. The final value is the removed value, so the copy writes it onto itself and the list still reads [40, 17, 93, 52, 8]."},{"at":{"slot":4,"lastSlot":4},"vars":{"values":"[40,17,93,52,8]","slotOf":"40:0,17:1,93:2,52:3,8:4","slot":4,"last":8},"note":"Repair: slotOf.put(8, 4). The entry for 8 now names slot 4."},{"at":{"slot":4,"lastSlot":4},"vars":{"values":"[40,17,93,52,8]","slotOf":"40:0,17:1,93:2,52:3"},"note":"Delete the entry for 8. It was also the final value, so the repair write disappears with it."},{"at":{"slot":4,"lastSlot":3},"vars":{"values":"[40,17,93,52]","slotOf":"40:0,17:1,93:2,52:3","moved":-1},"note":"Drop the final position. The list reads [40, 17, 93, 52] and the call returns -1."}]}
```

If the delete ran before the repair, the repair would put the entry for 8 back into the map. The map would then name a slot that no longer exists.

<!-- stage: code -->
### Implementing The Paired Class

```java
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

final class PairedIds {
    private final List<Integer> values = new ArrayList<>();
    private final Map<Integer, Integer> slotOf = new HashMap<>();

    boolean insert(int v) {
        if (slotOf.containsKey(v)) return false;
        slotOf.put(v, values.size());   // record the slot before the append changes size
        values.add(v);
        return true;
    }

    int remove(int v) {
        Integer slot = slotOf.get(v);
        if (slot == null) return -1;                 // absent: nothing changes, nothing moves
        int last = values.get(values.size() - 1);
        values.set(slot, last);                      // swap with last: close the gap in O(1)
        slotOf.put(last, slot);                      // repair the moved entry first
        slotOf.remove(v);                            // then delete the removed entry
        values.remove(values.size() - 1);            // index form: drops the final slot
        return last == v ? -1 : last;
    }

    int getAt(int i) {
        if (i < 0 || i >= values.size()) throw new IndexOutOfBoundsException("slot " + i);
        return values.get(i);
    }
}
```

Every operation runs in O(1) on average. The `values.remove(values.size() - 1)` call uses an `int` argument, so Java treats it as a position and not as an element to find.

<!-- stage: applicability -->
### Recognizing A Paired Design

#### Spotting The Cue

Look for a contract that asks for lookup by key and also for a position, an order or a neighbor, each in constant time. Hash-based sets and maps give the first and have no order to read by position. Arrays and linked lists give the second and cannot find a key quickly. When both questions appear in one contract, pair the two structures and write down which one answers which question.

An **invariant** is a fact about the state that holds before and after every operation. For a pair, the invariant says that every cross-reference names the right location. Check it at every exit of every operation, including the early returns and the empty and single-element cases. A linked list works the same way. The map holds the node instead of a slot, and a detach rewrites two neighbor links, `prev.next` and `next.prev`, instead of one entry.

#### Naming The False Friends

A **false friend** is a tool that looks like a fit and breaks the contract. `LinkedHashSet` gives O(1) lookup and O(1) removal, but it offers no way to read the element at position `i` in O(1), so it fails a contract with `getAt`. An `ArrayList` plus a `HashSet` with no slot map still scans to remove. Keeping slots in a map without repairing them after a swap returns the wrong value from `getAt` later, long after the faulty call.

Two Java hazards belong here. Comparing two `Integer` objects with `==` is true for small values and false for others, so compare slots with `equals` or unbox them first. Removing entries from the map while a loop iterates over its keys throws `ConcurrentModificationException`, so copy the keys before the loop. Lesson 05 reuses this design for randomized sets, and lesson 06 uses a linked list for caches.

<!-- stage: exercises -->
### Exercises

#### [Build] Map To List Node (Author exercise)
<!-- id: ds-map-list-node -->

**Prerequisites.** The paired class in this lesson and a doubly linked list.

**Problem.** Implement `OrderedKeys`, a doubly linked list of distinct non-negative integer keys with a `HashMap` from each key to its node. The operation `append(key)` adds the key at the tail and returns `false` when the key already exists. The operation `detach(key)` unlinks the node of the key in O(1) and returns the key that followed it, or `-1` when the detached node was the tail. The operation `order()` returns the keys from head to tail. The operation `detach` of an absent key throws `IllegalArgumentException`.

**Constraints.** The limits are:
- **Keys** are `int` values in the range `0` to `10^9`.
- **Calls** number at most `10^5`.
- **Cost** of `append` and `detach` is O(1) on average.
- **Empty list** is allowed, and `order()` returns an empty array.

**Example 1.** Input: append 5, 9, 2, 7 in order, then call `detach(9)`. Output: the call returns 2, and `order()` is `[5, 2, 7]`.

**Example 2.** Input: append 4 to an empty list, then call `detach(4)` and `append(6)`. Output: `detach(4)` returns -1, `order()` is empty after it, and `order()` is `[6]` at the end.

**Hint.** Which two neighbors point at the node you remove? What must the list's head and tail become when the node has no previous or no next neighbor?

**Changed decision.** First exercise in the sequence: the second structure is a linked list, so the map stores a node and the repair rewrites links.

#### [Vary] Map To Array Index (Author exercise)
<!-- id: ds-map-array-index -->

**Prerequisites.** The first exercise above.

**Problem.** Implement `IndexedKeys`, an array-backed list of distinct non-negative integer keys with a `HashMap` from each key to its position. The operation `add(key)` appends the key and returns `false` when it exists. The operation `removeAt(i)` deletes the key stored at position `i` by moving the final key into position `i`. It returns the key that moved, or `-1` when no key moved. The operation `slotOf(key)` returns the position of the key, or `-1` when it is absent. The operation `removeAt(i)` throws `IndexOutOfBoundsException` for a position outside `0` to `size - 1`.

**Constraints.** The limits are:
- **Keys** are `int` values in the range `0` to `10^9`.
- **Calls** number at most `10^5`.
- **Cost** of every operation is O(1) on average.
- **Positions** after a removal keep every untouched key at its old position.

**Example 1.** Input: add 30, 11, 64, 25, then call `removeAt(1)`. Output: the call returns 25, the keys read `[30, 25, 64]`, and `slotOf(25)` is 1.

**Example 2.** Input: add 30, then call `removeAt(0)` and `add(30)`. Output: `removeAt(0)` returns -1 and leaves the structure empty, and `add(30)` returns `true`.

**Hint.** The caller names a position and not a key. Which key must you read from the array to find out whose map entry changes?

**Changed decision.** The removal request changes from a key to a position, so the map is needed only to repair the entry of the key that moves.

#### [Boundary] Remove Last Element (Author exercise)
<!-- id: ds-remove-last-slot -->

**Prerequisites.** The two exercises above.

**Problem.** Implement `IndexedKeys` with the operation `removeKey(key)`, which deletes the key by moving the final key into its slot. The operation returns `true` when the key existed and `false` otherwise. After every call, `mapSize()` must equal `size()`, and `slotOf(k)` must equal the position of `k` for every stored key. The case under test is a removal of the key stored at the final position.

**Constraints.** The limits are:
- **Keys** are `int` values in the range `0` to `10^9`.
- **Calls** number at most `10^5`.
- **Cost** of every operation is O(1) on average.
- **Absent key** returns `false` and leaves both structures unchanged.

**Example 1.** Input: add 8, 3, 6, then call `removeKey(6)`. Output: the call returns `true`, the keys read `[8, 3]`, `slotOf(6)` is -1 and `mapSize()` is 2.

**Example 2.** Input: add 8, 3, 6, then call `removeKey(3)` and `removeKey(9)`. Output: the keys read `[8, 6]`, `slotOf(6)` is 1, `mapSize()` is 2, and `removeKey(9)` returns `false`.

**Hint.** When the removed key is the final key, the move copies it onto itself. Which of the two map updates must run last so the removed key stays out of the map?

**Changed decision.** The removed key and the moved key can be the same key, so the order of the repair and the delete decides whether a stale entry survives.

#### [Recognize] Insert Delete GetRandom O(1) With Positions (LeetCode 380)
<!-- id: ds-indexed-set-contract -->

**Prerequisites.** All three exercises above.

**Problem.** Design `IndexedSet`, a set of distinct non-negative integers, in the style of LeetCode 380 with a changed contract. The operation `insert(v)` returns `true` when `v` was added and `false` when it was present. The operation `remove(v)` deletes `v` and returns the value that moved into the freed position, or `-1` when no value moved or `v` was absent. The operation `getAt(i)` returns the value at position `i`. The operation `size()` returns the count of values. New values take the next free position, and a removal moves the final value into the freed position.

**Constraints.** The limits are:
- **Values** are `int` values in the range `0` to `10^9`, so `-1` is never a value.
- **Calls** number at most `10^5`.
- **Cost** of every operation is O(1) on average.
- **Positions** for `getAt` run from `0` to `size() - 1`, and any other position throws `IndexOutOfBoundsException`.

**Example 1.** Input: insert 12, 5, 30, 9, then call `remove(5)`. Output: the call returns 9, `getAt(1)` is 9 and `size()` is 3.

**Example 2.** Input: insert 7, 2, 7, then call `remove(2)` and `remove(99)`. Output: the second `insert(7)` returns `false`, both removals return -1 because 2 was last and 99 is absent, `getAt(0)` is 7 and `size()` is 1.

**Hint.** The return value of `remove` exposes the order of the repair. Which entry is wrong right after the move, and what happens when you compare two boxed slots with `==` for values above 127?

**Changed decision.** The prompt asks for position reads and for the moved value as output, so the repair order and the slot map are both observable.
