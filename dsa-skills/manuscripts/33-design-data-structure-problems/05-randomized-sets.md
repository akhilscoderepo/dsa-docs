<!-- lesson-kind: standard -->
<!-- lesson-id: randomized-sets -->
## Pick A Random Value In Constant Time

<!-- stage: context -->
### Why A Random Pick Gets Slow

A load balancer keeps the addresses of healthy backend servers. Health checks add a server when it recovers and remove it when it fails. Every incoming request must pick one healthy server at random, with every server equally likely. The balancer handles tens of thousands of requests per second. The pool changes a few times per second.

A first version works in testing with ten servers. In production the pool holds tens of thousands of entries, and the pick shows up at the top of the profile. Insert, remove and membership checks are all fast. Only the random pick is slow. This lesson asks how one structure can support insert, remove, membership and a random pick, each in constant expected time.

<!-- stage: naive -->
### Copying The Set On Every Pick

The tempting design stores the values in a `HashSet<Integer>`. Insert, remove and membership are O(1) expected. A set has no position to draw, so the pick first copies the values into a list.

```java
static int pickFrom(java.util.HashSet<Integer> pool, java.util.Random rng) {
    java.util.List<Integer> copy = new java.util.ArrayList<>(pool);
    return copy.get(rng.nextInt(copy.size()));
}
```

The copy visits every element in the set's internal iteration order. That order depends on hash buckets, not on insertion order, and the set promises no order at all. The pick is still correct, because every copy position holds one value. It is slow because the copy is rebuilt for each pick.

<!-- stage: bottleneck -->
### The Cost Of Copying Per Pick

```predict
A pool holds 50,000 values and receives 20,000 picks per second. About how many element copies per second does the copying design perform, and which operation is responsible?

About one billion element copies per second, because each pick copies all 50,000 values. The pick is responsible. Insert and remove stay cheap.
```

Each pick costs O(n) time and O(n) extra space for the copy, where n is the number of current values. Over m picks the total is O(m * n). For 20,000 picks on 50,000 values that is one billion copies per second, which no single core sustains.

Keeping the copy between picks does not fix this. Every insert or remove makes the copy stale, so the next pick must rebuild it. A pool that changes between nearly every pick pays the full cost each time. The fast random pick needs a structure that already has stable positions, so a random number can name a position directly. An array has that property. An array alone fails the other direction, because finding a value to remove scans O(n) slots.

<!-- stage: insight -->
### Keeping Values In An Array

#### Removing By Swapping With The Last Slot

Store the current values in a dynamic array, in any order. Insert appends to the end in O(1) amortized time. Removing from the middle would shift every later element, which costs O(n). The **swap-with-last** move avoids the shift. Copy the last value into the slot of the removed value, then delete the last slot. Order is not part of the contract, so the move is allowed, and it takes O(1) time.

<!-- names: swap-with-last, index map, uniform -->

#### Tracking Where Each Value Sits

Removal needs to find the slot of the value. A hash map from value to array index answers that in O(1) expected time. Call it the **index map**. Insert writes the new value into the array and records its slot in the index map. Remove reads the slot from the index map, performs the swap-with-last move and then repairs the index map. The value that moved now sits in a new slot, so its entry must change. The removed value must lose its entry.

#### Why A Random Index Is A Fair Pick

The array holds exactly the current values, one per slot. A random pick draws an index from `0` to `size - 1`, and each index has probability `1 / size`. That draw is **uniform**: every current value is equally likely. The value follows from the index, because each slot holds exactly one value and no value holds two slots. If the array held a stale or duplicate slot, the pick would favor that value. So the correctness of the pick depends on the invariant that the array and the index map always describe the same set of values.

<!-- stage: variables -->
### State The Set Keeps

The class needs two fields. The contract also fixes who supplies the random source, which is a parameter and not a field.

- **values** is the dynamic array holding exactly the current values, with no gaps and no stale slots.
- **index** is the map from each current value to its slot in `values`.
- **rng** is a `java.util.Random` that the caller passes into `getRandom`, so a test can seed it. The class does not store it.

The invariant ties the fields together. For every slot `i` in `0..values.size() - 1`, `index.get(values.get(i))` equals `i`. The map holds no other key. Every operation must restore this fact before it returns.

<!-- stage: trace -->
### Tracing Two Removals

#### Removing A Middle Value

Start with the array `[10, 20, 30, 40]` and the index map `10 -> 0, 20 -> 1, 30 -> 2, 40 -> 3`. Remove 20.

The index map says 20 sits in slot 1, and the last slot is 3 and holds 40. The operation copies 40 into slot 1, so the array reads `[10, 40, 30, 40]`. It then records that 40 now sits in slot 1. Next it drops the last slot, which leaves `[10, 40, 30]`. Finally it deletes the entry for 20. The map now agrees with the array again.

```trace
{"cells":[10,20,30,40],"pointers":["slot","last"],"steps":[{"at":{"slot":-1,"last":3},"vars":{"array":"[10, 20, 30, 40]","map":"10->0, 20->1, 30->2, 40->3"},"note":"Start: remove 20. The array is [10, 20, 30, 40] and the last slot is 3."},{"at":{"slot":1,"last":3},"vars":{"array":"[10, 20, 30, 40]","map":"10->0, 20->1, 30->2, 40->3"},"note":"The map gives slot 1 for 20. The last slot 3 holds 40."},{"at":{"slot":1,"last":3},"vars":{"array":"[10, 40, 30, 40]","map":"10->0, 20->1, 30->2, 40->3"},"note":"Copy 40 into slot 1. The array reads [10, 40, 30, 40]."},{"at":{"slot":1,"last":3},"vars":{"array":"[10, 40, 30, 40]","map":"10->0, 20->1, 30->2, 40->1"},"note":"Record slot 1 for 40 in the map."},{"at":{"slot":1,"last":3},"vars":{"array":"[10, 40, 30]","map":"10->0, 20->1, 30->2, 40->1"},"note":"Drop the last slot. The array reads [10, 40, 30]."},{"at":{"slot":1,"last":3},"vars":{"array":"[10, 40, 30]","map":"10->0, 30->2, 40->1"},"note":"Delete the entry for 20 as the final step. The map agrees with the array again."}]}
```

#### Removing The Last Value

Start with the array `[10, 20, 40]` and remove 40, which sits in the last slot. Here the removed slot and the last slot are the same slot.

The copy step writes 40 into the slot that already holds 40. The repair step records slot 2 for 40, which rewrites the entry with the value it already has. That entry is the one the operation is about to delete. The operation then drops the last slot. Only the final step, which deletes the entry for 40, makes the map correct. The order of those steps matters, as the second trace shows.

```trace
{"cells":[10,20,40],"pointers":["slot","last"],"steps":[{"at":{"slot":-1,"last":2},"vars":{"array":"[10, 20, 40]","map":"10->0, 20->1, 40->2"},"note":"Start: remove 40. The array is [10, 20, 40] and the last slot is 2."},{"at":{"slot":2,"last":2},"vars":{"array":"[10, 20, 40]","map":"10->0, 20->1, 40->2"},"note":"The map gives slot 2 for 40. The last slot 2 holds 40."},{"at":{"slot":2,"last":2},"vars":{"array":"[10, 20, 40]","map":"10->0, 20->1, 40->2"},"note":"Copy 40 into slot 2. The array reads [10, 20, 40]."},{"at":{"slot":2,"last":2},"vars":{"array":"[10, 20, 40]","map":"10->0, 20->1, 40->2"},"note":"Record slot 2 for 40 in the map."},{"at":{"slot":2,"last":2},"vars":{"array":"[10, 20]","map":"10->0, 20->1, 40->2"},"note":"Drop the last slot. The array reads [10, 20]."},{"at":{"slot":2,"last":2},"vars":{"array":"[10, 20]","map":"10->0, 20->1"},"note":"Delete the entry for 40 as the final step. The map agrees with the array again."}]}
```

<!-- stage: code -->
### Implementing The Set With Injected Random

```java
final class RandomPool {
    private final java.util.ArrayList<Integer> values = new java.util.ArrayList<>();
    private final java.util.HashMap<Integer, Integer> index = new java.util.HashMap<>();

    // Contract: true when val was absent and is now stored; false when it was already present.
    boolean insert(int val) {
        if (index.containsKey(val)) return false;    // the value is present, so state is unchanged
        index.put(val, values.size());                // the new value will occupy the next free slot
        values.add(val);                              // append in O(1) amortized time
        return true;
    }

    // Contract: true when val was present and is now gone; false when it was absent.
    boolean remove(int val) {
        Integer slot = index.get(val);                // O(1) lookup of the slot
        if (slot == null) return false;               // absent, so nothing to change
        int last = values.get(values.size() - 1);     // the value that fills the hole
        values.set(slot, last);                       // overwrite the removed value
        index.put(last, slot);                        // repair the moved value first
        values.remove(values.size() - 1);             // int argument, so this removes by position
        index.remove(val);                            // delete the removed value last
        return true;
    }

    // Contract: every current value has probability 1/size; the caller supplies rng.
    int getRandom(java.util.Random rng) {
        if (values.isEmpty()) throw new IllegalStateException("empty");   // nextInt(0) would throw a less clear error
        return values.get(rng.nextInt(values.size()));                    // uniform index, so uniform value
    }
}
```

Every operation costs O(1) expected time. The class uses O(n) space for the array and the map. The `insert` operation checks the map before it writes anything, so a repeated value leaves the state unchanged. The `remove` operation writes the map entry of the moved value before it deletes the entry of the removed value. The `getRandom` operation reads the size once and never allocates.

<!-- stage: applicability -->
### Deciding When This Structure Fits

#### Recognizing The Pattern

Reach for this structure when one structure must support insert, remove, membership and a random pick, all in constant expected time. An invariant is a fact about the state that every operation must restore before it returns. Here the invariant says that the array holds exactly the current values and that the index map gives each value's exact slot. The recognition cue is the pair of demands "remove by value" and "pick by position".

#### Spotting The False Friends

A false friend is a structure that looks like the right tool and fails one demand. A `HashSet` fails the pick, because it has no positions. An `ArrayList` alone fails the removal, because `indexOf` scans O(n) slots. A `LinkedHashSet` keeps insertion order but still offers no index. A `TreeSet` picks a random rank only in O(log n) with extra bookkeeping, so it breaks the constant-time demand.

#### Watching The Java Hazards

Three Java details cause real bugs here. First, `Random.nextInt(bound)` throws `IllegalArgumentException` when the bound is 0, so an empty set needs its own check. Second, `HashSet<Integer>` iterates in bucket order, which is not insertion order, so no design may rely on "the first element". Third, on an `ArrayList<Integer>`, the call `remove(int)` removes by position and `remove(Object)` removes by value. Passing a plain `int` selects the first form, which is what the array tail needs. A test that seeds the random source turns the pick into an exact, repeatable check.

<!-- stage: exercises -->
### Exercises

#### [Build] Swap-With-Last Removal (Author exercise)
<!-- id: ds-swap-last-removal -->

**Prerequisites.** The array plus index map structure in this lesson.

**Problem.** Implement a class `IntPool` with three operations. `insert(val)` stores `val` when it is absent and returns `true`, and it returns `false` without any change when `val` is present. `remove(val)` deletes `val` when present and returns `true`, and it returns `false` without any change when `val` is absent. `contains(val)` returns whether `val` is present. Store the values in an array and keep a map from each value to its slot. After `remove`, the last value must fill the slot of the removed value.

**Constraints.** The limits are:
- **Values** are `int` and may be negative.
- **Cost** of each operation is O(1) expected time.
- **Slots** hold no gaps, so slot indexes run from 0 to size - 1.
- **Order** of the values in the array is not part of the contract.
- **Empty pool** is allowed, and `remove` on it returns `false`.

**Example 1.** Input `insert(5)`, `insert(8)`, `insert(2)`, `insert(9)`, then `remove(8)`, output `true` for the removal, the array `[5, 9, 2]` and the map `5 -> 0, 9 -> 1, 2 -> 2`.

**Example 2.** Input the same pool and `remove(4)`, output `false`, with the array `[5, 8, 2, 9]` unchanged.

**Hint.** Which value moves when slot 1 is removed from a four-slot array? After it moves, which map entry is now wrong?

**Changed decision.** First exercise in the sequence: the array removal replaces the shift of later elements with a copy of the last value.

#### [Vary] Insert Delete GetRandom O(1) (LeetCode 380)
<!-- id: ds-random-pick-injected -->

**Prerequisites.** The swap-with-last exercise above.

**Problem.** Implement `RandomizedSet` with `insert(val)`, `remove(val)` and `getRandom(Random rng)`. Both `insert` and `remove` return a `boolean`: `true` when the call changed the set. The operation `getRandom` takes a caller-supplied `java.util.Random` and returns one current value, each with probability `1 / size`. It must draw exactly one index with `rng.nextInt(size)`. It throws `IllegalStateException` when the set is empty. Lesson 03 built the same structure with `getAt` and a moved-value return. This version replaces both: the pick takes an injected random source, and the removal returns only a boolean.

**Constraints.** The limits are:
- **Values** are `int`.
- **Cost** of each operation is O(1) expected time.
- **Random source** is the argument `rng`; the class never creates its own.
- **Empty set** makes `getRandom` throw `IllegalStateException`.
- **Tests** may pass a seeded `Random` or a subclass that scripts `nextInt`.

**Example 1.** Input `insert(4)`, `insert(4)`, `insert(7)`, `insert(9)`, output `true`, `false`, `true`, `true`, and a script that makes `nextInt` return 1 makes `getRandom` return 7 after being asked for a bound of 3.

**Example 2.** Input the values 1 to 5 and 10,000 picks from `new Random(42)`, output five counts whose chi-square statistic stays below 18.47, the 0.1% critical value for four degrees of freedom.

**Hint.** If `nextInt(size)` is uniform over the indexes, why does the array make it uniform over the values? What breaks if a removed value stays in the array?

**Changed decision.** The random source moves from the class to the caller, so a test can enumerate the exact index and seed a statistical check.

#### [Boundary] Removing The Last Value (Author exercise)
<!-- id: ds-remove-last-value -->

**Prerequisites.** Both exercises above.

**Problem.** In the swap-with-last removal, the value to remove can already be the last one. Then the moved value and the removed value are identical. Implement `remove(val)` so that the deleted map entry is never restored. Include the case where the set holds only one value. State the order of the four state updates and explain why a different order resurrects the entry.

**Constraints.** The limits are:
- **Case** covers a removed value that sits in the last slot, and that includes a set of size 1.
- **Result** after removing the only value is an empty array and an empty map.
- **Membership** of the removed value is `false` afterward.
- **Reinsertion** of the same value works and appends it again.
- **Cost** is O(1) expected time.

**Example 1.** Input a pool holding only 6, then `remove(6)`, `contains(6)`, `insert(6)`, output `true`, `false`, `true`, and the final array is `[6]`.

**Example 2.** Input the array `[3, 6]`, then `remove(6)`, output the array `[3]` and the map `3 -> 0`. Then `remove(3)` on the original array `[3, 6]` outputs the array `[6]` and the map `6 -> 0`.

**Hint.** When the slot equals the last slot, which map entry does the repair step write? Which step must run after it?

**Changed decision.** The edge case changes the order of the updates, not the algorithm: the entry for the removed value must be deleted after the moved value's entry is written.

#### [Recognize] Duplicates Allowed (LeetCode 381)
<!-- id: ds-random-duplicates -->

**Prerequisites.** All three exercises above.

**Problem.** Implement `RandomizedCollection` that accepts repeated values. `insert(val)` always stores one more occurrence and returns `true` only when `val` had no occurrence before. `remove(val)` removes the occurrence with the greatest array index and returns the number of occurrences of `val` that remain. It returns `-1` when `val` has no occurrence. `getRandom(Random rng)` draws one array index with `rng.nextInt(size)`, so a value is returned with probability proportional to its count. Store a map from each value to the set of its indexes.

**Constraints.** The limits are:
- **Values** are `int`.
- **Index set** per value must support finding the greatest index.
- **Removal** returns the remaining count, which is 0 when the last occurrence goes, and `-1` when the value is absent.
- **Cost** is O(log k) for `insert` and `remove`, where k is the count of that value, and O(1) for `getRandom`.
- **Empty collection** makes `getRandom` throw `IllegalStateException`.

**Example 1.** Input `insert(4)`, `insert(4)`, `insert(6)`, `insert(4)`, then `remove(4)`, output `true`, `false`, `true`, `false`, and `2`, with the array `[4, 4, 6]`.

**Example 2.** Input the collection that Example 1 leaves, which holds the array `[4, 4, 6]`, then `remove(4)`, `remove(9)`, output `1` and `-1`, with the array `[4, 6]`.

**Hint.** Which index leaves the array when the greatest index of the value is removed? When is that index equal to the last slot, and what does that say about the moved value?

**Changed decision.** One index per value becomes a set of indexes per value, and the removal rule becomes "greatest index first", which also decides when the moved value and the removed value coincide.
