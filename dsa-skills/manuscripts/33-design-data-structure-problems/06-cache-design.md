<!-- lesson-kind: standard -->
<!-- lesson-id: cache-design -->
## Evict The Least Recent Entry

<!-- stage: context -->
### Why Scanning For A Victim Is Slow

A profile service keeps recent user records in memory so that most requests skip the database. The cache holds 10,000 records. When record 10,001 arrives, the service must drop one, and the best candidate is the record that nobody has asked for the longest time. The first version finds that record by scanning a timestamp stored on every entry.

Under load, every miss touches ten thousand entries, and the latency of the whole service follows the scan. The cache exists to save time, and its own bookkeeping spends the savings. This lesson answers one question. How can a lookup, a refresh and an eviction each finish in constant time, both when the rule is "least recently used" and when the rule is "least frequently used"?

<!-- stage: naive -->
### Keeping Usage Order In An Array List

The simplest design stores values in a hash map and keeps the keys in an `ArrayList` ordered from least recent to most recent. Every use of a key removes it from the list and appends it at the end. An eviction removes index 0.

```java
import java.util.*;

final class ListCache {
    private final int capacity;
    private final Map<Integer, Integer> values = new HashMap<>();
    private final List<Integer> order = new ArrayList<>();   // index 0 is the least recently used key

    ListCache(int capacity) { this.capacity = capacity; }

    int get(int key) {
        if (!values.containsKey(key)) return -1;
        order.remove(Integer.valueOf(key));   // scans the list to find the key
        order.add(key);
        return values.get(key);
    }

    void put(int key, int value) {
        if (values.containsKey(key)) order.remove(Integer.valueOf(key));
        else if (values.size() == capacity) values.remove(order.remove(0));   // shifts every later key left
        values.put(key, value);
        order.add(key);
    }
}
```

The behavior is correct. After `put(1, 10)`, `put(2, 20)` and `get(1)` on a cache of capacity 2, the list reads `[2, 1]`, so a third key evicts key 2.

```predict
A cache of capacity 10,000 is full and receives a get for a key that was used a moment ago. How many list slots does the get touch, and does it matter that the hash map answers in constant time?

The get scans up to 10,000 list slots to find the key and then shifts later slots to close the gap. The hash map's constant lookup does not help, because the list update dominates the cost.
```

<!-- stage: bottleneck -->
### Where The List Spends Its Time

The hash map finds a value in O(1) expected time, but the list cannot find a key without a search. The call `order.remove(Integer.valueOf(key))` scans from the front, which costs O(n) for a cache of n entries. The call `order.remove(0)` is also O(n), because an array-backed list shifts every later element one slot to the left.

So `get`, `put` and eviction each cost O(n), even though the cache was built to answer in constant time. A cache of 10,000 entries wastes up to ten thousand steps on every hit, and hits are the common case. The data itself is fine. The order is stored in a shape that cannot move one element without visiting its neighbors. The fix has to let the cache move a known entry in constant time, which requires a way to reach that entry directly and a shape that does not shift others when it leaves.

<!-- stage: insight -->
### Pair A Map With Linked Nodes

#### Using One Map And One Recency List

The least recent use order needs a structure where removing a known element is O(1). A doubly linked list gives that, because a node knows both neighbors and can unlink itself by rewriting two links. The list is not searched, because the hash map takes the key straight to its node.

A **recency list** is a doubly linked list ordered from most recently used at the front to least recently used at the back. A use of key `k` finds the node through the map, detaches it and reinserts it at the front. An eviction detaches the node at the back and deletes its key from the map.

A **sentinel** is a dummy node at each end of the list that never holds a key. With a sentinel at the front and one at the back, every real node always has a previous and a next node. Insertion and removal then follow one code path with no null checks, including when the list has one node or none.

#### Adding Counts For Frequency Eviction

<!-- names: recency list, sentinel, frequency bucket -->

The least frequently used rule evicts the key with the fewest uses. Among keys with the same count, it evicts the one used longest ago. A **frequency bucket** is the set of all keys that currently share one use count, ordered from least recent at its start to most recent at its end. A map goes from each count to its bucket.

A use of key `k` with count `f` moves the key from bucket `f` to the end of bucket `f + 1`. An integer called the minimum frequency names the smallest count that has a non-empty bucket. Eviction takes the first key of that bucket. When bucket `f` empties and `f` was the minimum, the moved node is now in bucket `f + 1`, so the minimum becomes `f + 1`. A brand-new key sets the minimum to 1.

<!-- stage: variables -->
### State The Two Caches Keep

Each design keeps a small set of fields, and the operations must restore the same facts after every call.

- **byKey** is the map from a key to its node, so no operation searches a list.
- **first** and **last** are the two sentinels, and `first.after` is the most recent node.
- **capacity** is the fixed maximum number of keys, and eviction runs only when a new key arrives at that size.
- **countOf** is the LFU map from a key to its use count.
- **bucketOf** is the LFU map from a use count to its bucket of keys.
- **smallest** is the minimum frequency, the smallest count that has a non-empty bucket.

The invariant for the LRU cache is that the map and the list hold exactly the same keys, each once. For the LFU cache, each key also sits in exactly one bucket, the bucket of its count.

The traces use shorter labels. The label `order` shows the LRU list from `first.after` toward `last`, and the label `counts` shows `countOf`.

<!-- stage: trace -->
### Tracing An LRU And An LFU Cache

#### Stepping Through The LRU Cache

The first trace uses an LRU cache with capacity 2 and the keys `[1, 2, 1, 3, 2, 4]`. The first two keys are puts of values 10 and 20, and the third is a `get(1)`. The fourth is `put(3, 30)`, the fifth is `get(2)` and the sixth is `put(4, 40)`. The note on each step shows the order from most recent to least recent.

When key 3 arrives, the cache is full and key 2 is at the back, so key 2 leaves. The later `get(2)` is a miss and changes nothing. The final put evicts key 1, which has been at the back since key 3 arrived.

```trace
{"cells":[1,2,1,3,2,4],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"order":"[1]","size":1},"note":"put(1, 10) adds key 1 at the front. Order is [1]."},{"at":{"op":1},"vars":{"order":"[2,1]","size":2},"note":"put(2, 20) adds key 2 at the front. Order is [2, 1]."},{"at":{"op":2},"vars":{"order":"[1,2]","size":2},"note":"get(1) returns 10 and moves key 1 to the front. Order is [1, 2]."},{"at":{"op":3},"vars":{"order":"[3,1]","size":2},"note":"put(3, 30) finds the cache full, so key 2 leaves from the back. Order is [3, 1]."},{"at":{"op":4},"vars":{"order":"[3,1]","size":2},"note":"get(2) is a miss and changes nothing. Order is [3, 1]."},{"at":{"op":5},"vars":{"order":"[4,3]","size":2},"note":"put(4, 40) finds the cache full, so key 1 leaves from the back. Order is [4, 3]."}]}
```

#### Stepping Through The LFU Cache

The second trace uses an LFU cache with capacity 2 and the keys `[1, 2, 2, 1, 3, 4]`. Steps one and two put keys 1 and 2. Step three is `get(2)` and step four is `get(1)`, so both keys reach count 2, and key 2 reached it first. Step five puts key 3 and step six puts key 4.

When key 3 arrives, both keys sit in bucket 2, and the first key of that bucket is key 2, so key 2 leaves and key 3 enters bucket 1. The minimum becomes 1. When key 4 arrives, bucket 1 holds only key 3, so key 3 leaves.

```trace
{"cells":[1,2,2,1,3,4],"pointers":["op"],"steps":[{"at":{"op":0},"vars":{"counts":"{1:1}","smallest":1},"note":"put(1) adds key 1 with count 1. The minimum frequency is 1."},{"at":{"op":1},"vars":{"counts":"{1:1,2:1}","smallest":1},"note":"put(2) adds key 2 with count 1. The minimum frequency is 1."},{"at":{"op":2},"vars":{"counts":"{1:1,2:2}","smallest":1},"note":"get(2) raises its count to 2. The minimum frequency is 1."},{"at":{"op":3},"vars":{"counts":"{1:2,2:2}","smallest":2},"note":"get(1) raises its count to 2. The minimum frequency is 2."},{"at":{"op":4},"vars":{"counts":"{1:2,3:1}","smallest":1},"note":"put(3) finds the cache full, so key 2 with count 2 leaves from the start of its bucket, then key 3 enters with count 1. The minimum frequency is 1."},{"at":{"op":5},"vars":{"counts":"{1:2,4:1}","smallest":1},"note":"put(4) finds the cache full, so key 3 with count 1 leaves from the start of its bucket, then key 4 enters with count 1. The minimum frequency is 1."}]}
```

<!-- stage: code -->
### Implementing The Cache Moves

The LRU cache needs three private moves: cut a node out, push a node to the front, and evict the oldest node. All three are constant-time link rewrites. The LFU cache adds a fourth move, `bump`, after the first code block.

```java
import java.util.*;

final class LruCore {
    private static final class Entry { int key, value; Entry before, after; }
    private final Entry first = new Entry(), last = new Entry();   // sentinels that never hold data
    private final Map<Integer, Entry> byKey = new HashMap<>();

    LruCore() { first.after = last; last.before = first; }

    private void cut(Entry e) { e.before.after = e.after; e.after.before = e.before; }

    private void pushFront(Entry e) {
        e.before = first; e.after = first.after;
        first.after.before = e; first.after = e;
    }

    private Entry evictOldest() {
        Entry victim = last.before;   // the node next to the back sentinel is the least recent one
        cut(victim);
        byKey.remove(victim.key);
        return victim;
    }
}
```

The LFU cache adds one more move. It takes a key out of its current bucket, adds one to the count, and appends the key to the next bucket.

```java
import java.util.*;

final class LfuCore {
    private final Map<Integer, Integer> countOf = new HashMap<>();
    private final Map<Integer, LinkedHashSet<Integer>> bucketOf = new HashMap<>();
    private int smallest;   // the minimum frequency

    void bump(int key) {
        int c = countOf.get(key);
        LinkedHashSet<Integer> from = bucketOf.get(c);
        from.remove(key);
        if (from.isEmpty()) { bucketOf.remove(c); if (smallest == c) smallest = c + 1; }
        countOf.put(key, c + 1);
        bucketOf.computeIfAbsent(c + 1, x -> new LinkedHashSet<>()).add(key);   // end of the set is the most recent
    }
}
```

All four moves cost O(1) expected, and none of them searches a list.

<!-- stage: applicability -->
### Recognizing When A Cache Fits

#### Spotting The Pattern

Use this design when a lookup by key and an eviction by usage must both be constant time. The invariant is a fact that every operation must restore before it returns. Here it states that the map and the list hold the same keys once each, the list order matches the order of use, and the minimum frequency, when present, matches a non-empty bucket.

A false friend is a technique that seems right for the job but breaks one promise of the contract. A `TreeMap` from timestamp to key finds the oldest entry, but each refresh costs O(log n) and two uses in the same tick collide. A priority queue keyed by count makes ties arbitrary and cannot remove an arbitrary key in constant time.

#### Checking The Java Library Shortcut

The class `LinkedHashMap` with access order enabled and an overridden `removeEldestEntry` implements an LRU cache in a few lines. Its contract is narrower than the design above. A `get` counts as a structural change, so a `get` inside a loop over its keys throws `ConcurrentModificationException`. The call `containsKey` does not refresh the order, and there is no read that skips the refresh, so a `peek` operation needs another design.

Keys also need correct `equals` and `hashCode`. A key class that overrides neither is compared by identity, so a lookup with an equal-looking new object misses. A key that changes after insertion lands in the wrong bucket. Use `record` keys or immutable fields.

The use count is an `int`. It overflows past 2147483647, and a cache that serves that many uses of one key needs a `long`. The exercises below cap the operation count far below that.

<!-- stage: exercises -->
### Exercises

#### [Build] Move Node To Front (Author exercise)
<!-- id: ds-move-to-front -->

**Prerequisites.** The sentinel list and the node moves in this lesson.

**Problem.** Implement a class `FrontList` that stores distinct `int` keys in a doubly linked list with a front sentinel and a back sentinel. The operation `addFront(key)` inserts a new node at the front and returns the node. The operation `moveToFront(node)` detaches a node that is in the list and reinserts it at the front. The operation `removeLast()` removes the node at the back and returns its key. The operations `frontToBack()` and `backToFront()` return the keys as lists in each direction.

**Constraints.** The limits are:
- **Keys** are distinct `int` values, and each key is added once.
- **Node** passed to `moveToFront` belongs to this list.
- **Empty list** makes `removeLast` throw `NoSuchElementException`.
- **First node** may be passed to `moveToFront`, and the list stays unchanged.
- **Cost** is O(1) per operation, except the two walking operations.

**Example 1.** Input: add keys 1, 2, 3, then call `moveToFront` on the node of key 1 and `removeLast()`. Output: `frontToBack()` was `[3, 2, 1]` before the move and is `[1, 3, 2]` after it, and `removeLast()` returns 2.

**Example 2.** Input: the list `[1, 3]` and a call of `moveToFront` on the node of key 1, which is already first. Output: `frontToBack()` stays `[1, 3]` and `backToFront()` is `[3, 1]`.

**Hint.** Which two links change when a node leaves, and which four change when it enters? Does the order of the two steps matter when the node is already first?

**Changed decision.** First exercise in the sequence: introduces the sentinel list and the detach-then-insert move without any map.

#### [Vary] LRU Cache With Peek (LeetCode 146)
<!-- id: ds-lru-peek-contract -->

**Prerequisites.** The move-to-front exercise above.

**Problem.** Implement a class `RecencyCache` with a fixed capacity. The operation `get(key)` returns the value or -1 and refreshes the key. The operation `put(key, value)` stores the value, refreshes the key, and evicts the least recent key first when a new key arrives at capacity. The operation `peek(key)` returns the value or -1 and does not refresh. The operation `keysByRecency()` returns the stored keys with the most recent first.

**Constraints.** The limits are:
- **Capacity** is an `int` with `1 <= capacity <= 10^4`.
- **Keys** and **values** are `int`, with values in the range `0` to `10^9`, so -1 means absent.
- **Overwrite** of a stored key refreshes it and never evicts.
- **Cost** is O(1) expected for `get`, `put` and `peek`.

**Example 1.** Input: capacity 2 and the calls `put(1, 10)`, `put(2, 20)`, `get(1)` and `put(3, 30)`. Output: `get(1)` returns 10, `keysByRecency()` is `[3, 1]` and `peek(2)` is -1.

**Example 2.** Input: capacity 2 and the calls `put(1, 10)`, `put(2, 20)`, `peek(1)` and `put(3, 30)`. Output: `peek(1)` returns 10 and `keysByRecency()` is `[3, 2]`, so key 1 was evicted, because `peek` did not refresh it.

**Hint.** Which of the three read and write operations touch the links? Which one must leave them alone?

**Changed decision.** Adds an operation that reads without refreshing, so order becomes observable and the refresh moves from every read to only `get` and overwrite.

#### [Boundary] Capacity One And Repeated Get (Author exercise)
<!-- id: ds-capacity-one-repeated-get -->

**Prerequisites.** The two exercises above.

**Problem.** Implement a class `SlotCache` that stores its list links in `int` arrays indexed by slot number, with a head slot and a tail slot as sentinels. The operations `get` and `put` follow the least recently used rule. The operations `forwardCount()` and `backwardCount()` return the number of data slots reached by walking from each sentinel to the other. Both must equal the number of stored keys after every operation, including capacity one and repeated `get` calls on the same key.

**Constraints.** The limits are:
- **Capacity** is an `int` with `1 <= capacity <= 100`.
- **Keys** and **values** are `int`, and a miss returns -1.
- **Walk** fails with an exception when it visits more than `capacity` data slots, because a legal walk from one sentinel to the other crosses at most `capacity + 1` links.
- **Overwrite** of the stored key keeps the size and never evicts.

**Example 1.** Input: capacity 1 and the calls `put(5, 50)`, `get(5)` twice, and `put(6, 60)`. Output: the later `get(5)` is -1, `get(6)` is 60, and both counts are 1.

**Example 2.** Input: capacity 1 and the calls `put(5, 50)` and `put(5, 51)`. Output: `get(5)` is 51 and both counts are 1.

**Hint.** What would happen to a slot's links if a refresh only inserted and never detached? At capacity one, which slot is both the first and the last?

**Changed decision.** The cache shrinks to the smallest legal size, where the front node and back node are the same, and the check moves from values to the link structure.

#### [Recognize] LFU Cache With Frequency Query (LeetCode 460)
<!-- id: ds-lfu-frequency-ties -->

**Prerequisites.** All three exercises above.

**Problem.** Implement a class `FrequencyCache` with a fixed capacity. The operations `get(key)` and `put(key, value)` each count one use of the key when it is present, and a new key starts at count 1. When a new key arrives at capacity, the cache evicts the key with the smallest count, and ties go to the least recently used key among them. The operation `frequency(key)` returns the count or 0, and it counts no use.

**Constraints.** The limits are:
- **Capacity** is an `int` with `0 <= capacity <= 10^4`, and capacity 0 accepts every operation and stores nothing.
- **Keys** and **values** are `int`, with values in `0` to `10^9`; a miss returns -1.
- **Operations** number at most 200000, so no count can overflow an `int`.
- **Cost** is O(1) expected per operation.

**Example 1.** Input: capacity 2 and the calls `put(1, 10)`, `put(2, 20)`, `get(1)` and `put(3, 30)`. Output: `frequency(1)` is 2, `frequency(2)` is 0 and `frequency(3)` is 1.

**Example 2.** Input: capacity 2 and the calls `put(1, 10)`, `put(2, 20)`, `get(2)`, `get(1)` and `put(3, 30)`. Output: both old keys have count 2 and key 2 was used first, so a later `get(2)` is -1 and `get(1)` is 10.

**Hint.** When the list of keys with the smallest count empties, which count becomes the smallest? Which key sits at the start of its bucket after several uses?

**Changed decision.** Eviction depends on use counts first and recency second, so one list becomes one list per count plus a pointer to the smallest count.
