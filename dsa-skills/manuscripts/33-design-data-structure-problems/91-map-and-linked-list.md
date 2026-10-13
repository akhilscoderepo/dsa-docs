<!-- lesson-kind: combination -->
<!-- lesson-id: map-and-linked-list -->
## Locate By Key And Order By Recency

<!-- stage: context -->
### Why A Busy Cache Slows Down

A web service keeps the 10,000 most recently used user profiles in memory. Each request asks for one profile by its user id. A hit must return the profile and mark it as the freshest entry. A miss loads the profile from the database and, when the cache is full, drops the entry nobody has touched for the longest time.

The first version works in testing. Under production traffic, the cache itself becomes the slowest part of the request, and the profile at the database is not the cause. Each hit walks through thousands of entries before it returns. The question of this lesson is how one structure can answer "where is this key" and "which entry is oldest" at the same time, both in constant time.

<!-- stage: contributions -->
### What Each Earlier Lesson Contributes

Three earlier lessons of this chapter supply the parts. The lesson One Method Repairs Each Link taught that a single private method owns every pointer change, so no public operation touches a link by hand. The lesson Pair A Map With Ordered Storage taught that a hash map finds an entry by key while a second structure keeps the order. The lesson Evict The Least Recent Entry taught that the entry at the cold end of the order is the one to remove when the capacity is full.

This lesson joins the three. The map finds a node in O(1) average time. The doubly linked list removes that node and puts it at the hot end in O(1) time, because each node knows both of its neighbours. The new idea is that both structures hold the very same node objects.

<!-- stage: naive -->
### Keeping Recency In A Plain List

The direct design stores the entries in one `ArrayList`, with the freshest entry at index 0. A lookup scans for the key. When it finds the entry, it removes the entry and inserts it again at index 0.

```java
static int getNaive(java.util.ArrayList<int[]> entries, int key) {
    for (int i = 0; i < entries.size(); i++) {
        // Each entry is {key, value}; the scan stops at the first matching key.
        if (entries.get(i)[0] == key) {
            int[] hit = entries.remove(i);   // shifts every later entry one slot left
            entries.add(0, hit);             // shifts every entry one slot right
            return hit[1];
        }
    }
    return -1;
}
```

With entries `{7,70}, {3,30}, {9,90}` in that order, `getNaive(entries, 9)` returns 90 and leaves the list as `{9,90}, {7,70}, {3,30}`. The result is correct. Each call also touches every entry that sits in front of the match.

```predict
A cache holds n entries and receives n requests, each for the oldest key. How many entries does the plain list touch for the whole run, and what does adding a HashMap from key to index change?

Each request scans n entries and then shifts n entries twice, so the run costs O(n^2). A HashMap from key to index removes the scan only. Every removal and reinsertion shifts the indexes of the entries behind it, so the stored indexes become wrong and the shifts still cost O(n).
```

<!-- stage: bottleneck -->
### Two Questions That Need Two Structures

The plain list answers "which entry is oldest" in O(1), because the oldest entry sits at the end. It answers "where is this key" in O(n), because it must scan. Moving the hit to the front adds another O(n) for the shifts. A cache with 100,000 entries and a million requests performs on the order of 10^11 element moves, and the cost grows with the cache size.

A hash map alone has the opposite weakness. It finds a key in O(1) average time, yet it stores no order, so finding the oldest entry means visiting all n entries in O(n). A singly linked list also fails. Removing a node from the middle needs the node before it, and finding that node by walking from the head costs O(n). Each single structure answers one question quickly and the other slowly. The design needs both answers at once, and neither structure supplies both alone.

<!-- stage: insight -->
### One Node Shared By Two Structures

#### Sharing Node Identity

The fix is to keep two structures over the same objects. The map goes from each key to a node object, and the doubly linked list is made of those same node objects. The map does not store a copy of the node, and it does not store an index into a list. Because of this shared **node identity**, a map lookup returns the exact node that sits inside the list. That node already holds `prev` and `next`, so removing it needs no search, only four pointer writes.

Moving a node to the hot end is a detach followed by an insert. The detach connects the old neighbours to each other. The insert connects the node to the head and to the old first node.

#### Placing Sentinel Nodes

Two **sentinel nodes** make those writes uniform. A sentinel is a dummy node that never holds data. One sentinel marks the hot end and one marks the cold end. Every real node then has a real `prev` and a real `next`, even when the list holds one entry, so the detach and insert code has no null check and no special case for the first or last node.

#### Stating The Combined Invariant

The **combined invariant** says three things at once. The key set of the map equals the set of real nodes in the list. The list length equals the map size. A forward walk from the head sentinel and a backward walk from the tail sentinel visit the same nodes in opposite orders. Every operation ends by restoring this invariant, and the tests in this chapter check it after each call.

<!-- names: node identity, sentinel nodes, combined invariant -->

<!-- stage: variables -->
### State Held By The Combined Cache

The class holds five pieces of state. The first four are reachable from the public operations, and the last one is private to the repair methods.

- **index** is a `HashMap<Integer, Node>` that maps each key to its node.
- **head** is the sentinel before the hottest node, so `head.next` is the freshest entry.
- **tail** is the sentinel after the coldest node, so `tail.prev` is the next entry to evict.
- **capacity** is the largest number of entries the cache may hold.
- **Node** is a private class holding `key`, `value`, `prev` and `next`.

The node stores its own `key` for one reason. When the cache evicts `tail.prev`, the code must delete that entry from the map, and the map needs the key. Without the stored key, eviction would search the map for the value and cost O(n).

<!-- stage: trace -->
### Tracing Hits, Misses And Eviction

#### Capacity Two With One Eviction

The first trace runs a cache of capacity 2 on the five requests listed in the cells. The requests are `put 1`, `put 2`, `get 1`, `put 3` and `get 2`. The note on each step names the list as it reads from the hot end to the cold end.

The two puts leave the list as 2, then 1. The `get 1` finds node 1 through the map, detaches it and inserts it at the hot end, so the list reads 1, 2. The `put 3` finds the cache full, so it evicts the cold node 2, removes key 2 from the map and inserts node 3 at the hot end. The final `get 2` misses and returns -1.

```trace
{"cells":[1,2,1,3,2],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"list":"[]","mapKeys":"{}"},"note":"Start: capacity 2, an empty list and an empty map."},{"at":{"op":0},"vars":{"list":"[1]","mapKeys":"[1]"},"note":"put 1: the key is new. Node 1 joins the hot end. The list reads [1] from hot to cold."},{"at":{"op":1},"vars":{"list":"[2,1]","mapKeys":"[1,2]"},"note":"put 2: the key is new. Node 2 joins the hot end. The list reads [2, 1] from hot to cold."},{"at":{"op":2},"vars":{"list":"[1,2]","mapKeys":"[1,2]"},"note":"get 1: the map finds node 1, which is detached and inserted at the hot end. The list reads [1, 2] from hot to cold."},{"at":{"op":3},"vars":{"list":"[3,1]","mapKeys":"[1,3]"},"note":"put 3: the key is new. The cache is full, so cold node 2 is detached and removed from the map. Node 3 joins the hot end. The list reads [3, 1] from hot to cold."},{"at":{"op":4},"vars":{"list":"[3,1]","mapKeys":"[1,3]"},"note":"get 2: the map has no such key, so the call returns -1 and the list is unchanged. The list reads [3, 1] from hot to cold."}]}
```

#### Capacity Three With Repeated Gets

The second trace uses capacity 3 and calls `get 1` twice in a row. The first call moves node 1 to the hot end. The second call detaches that node and inserts it again at the same place, and the list stays correct. Then `put 4` evicts key 2, because node 2 is the coldest node once key 1 is hot again.

```trace
{"cells":[1,2,3,1,1,4],"pointers":["op"],"steps":[{"at":{"op":-1},"vars":{"list":"[]","mapKeys":"{}"},"note":"Start: capacity 3, an empty list and an empty map."},{"at":{"op":0},"vars":{"list":"[1]","mapKeys":"[1]"},"note":"put 1: the key is new. Node 1 joins the hot end. The list reads [1] from hot to cold."},{"at":{"op":1},"vars":{"list":"[2,1]","mapKeys":"[1,2]"},"note":"put 2: the key is new. Node 2 joins the hot end. The list reads [2, 1] from hot to cold."},{"at":{"op":2},"vars":{"list":"[3,2,1]","mapKeys":"[1,2,3]"},"note":"put 3: the key is new. Node 3 joins the hot end. The list reads [3, 2, 1] from hot to cold."},{"at":{"op":3},"vars":{"list":"[1,3,2]","mapKeys":"[1,2,3]"},"note":"get 1: the map finds node 1, which is detached and inserted at the hot end. The list reads [1, 3, 2] from hot to cold."},{"at":{"op":4},"vars":{"list":"[1,3,2]","mapKeys":"[1,2,3]"},"note":"get 1: the map finds node 1, which is detached and inserted at the hot end. The list reads [1, 3, 2] from hot to cold."},{"at":{"op":5},"vars":{"list":"[4,1,3]","mapKeys":"[1,3,4]"},"note":"put 4: the key is new. The cache is full, so cold node 2 is detached and removed from the map. Node 4 joins the hot end. The list reads [4, 1, 3] from hot to cold."}]}
```

<!-- stage: code -->
### Implementing The Cache With Four Pointer Writes

```java
final class LruCache {
    private static final class Node {
        final int key;
        int value;
        Node prev, next;
        Node(int key, int value) { this.key = key; this.value = value; }
    }

    private final java.util.Map<Integer, Node> index = new java.util.HashMap<>();
    private final Node head = new Node(0, 0);   // sentinel on the hot side
    private final Node tail = new Node(0, 0);   // sentinel on the cold side
    private final int capacity;

    LruCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    // Repair method one: removes n from its position; n keeps stale links until reinserted.
    private void detach(Node n) {
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }

    // Repair method two: places n directly after the head sentinel.
    private void insertFront(Node n) {
        n.prev = head;
        n.next = head.next;
        head.next.prev = n;
        head.next = n;
    }

    int get(int key) {
        Node n = index.get(key);
        if (n == null) return -1;
        detach(n);          // the map gave the exact node, so no search is needed
        insertFront(n);
        return n.value;
    }

    void put(int key, int value) {
        Node n = index.get(key);
        if (n != null) {            // update counts as a use
            n.value = value;
            detach(n);
            insertFront(n);
            return;
        }
        if (index.size() == capacity) {
            Node cold = tail.prev;   // coldest real node
            detach(cold);
            index.remove(cold.key);  // the stored key makes this removal O(1)
        }
        n = new Node(key, value);
        index.put(key, n);
        insertFront(n);
    }
}
```

The `get` and `put` operations each run in O(1) average time, because the map lookup is O(1) average and the pointer writes are O(1). The space is O(capacity) for the nodes plus the map. The two private methods are the only code that changes `prev` and `next`, which is the rule from One Method Repairs Each Link.

<!-- stage: applicability -->
### Recognizing When A Map Needs A List

#### Spotting The Cue

Use this pair when a problem asks for lookup by key and also for removal or reordering by position, with both in constant time. The cue words are "least recently used", "most recently used", "move to front" and "evict the oldest". An invariant is a fact that every operation must restore before it returns. Here the invariant is the combined one: the map keys and the list nodes are the same set, and the list length equals the map size.

#### Avoiding The False Friends

A false friend is a design that looks like it fits the cue and breaks a promise of the contract. Four designs qualify.

An `ArrayDeque` with `remove(Object)` keeps order, yet each removal scans the deque and costs O(n). A `PriorityQueue` ordered by timestamp costs O(log n) per touch, and an entry that is touched again leaves a stale copy behind. A singly linked list loses the O(1) detach because it has no `prev`. A second map from key to timestamp finds the key and still needs an O(n) scan for the minimum.

#### Handling Java Details

The class `LinkedHashMap` built with `accessOrder` set to true implements this same pair. Production code should prefer it, and an interview asks you to build the pair by hand. In your own build, keep the key inside the node, delete from the map before the node object is lost, and never let a public operation touch a link directly. A stale `Node` reference that stays in the map after eviction corrupts every later lookup. The same pair extends to frequency order when the list is replaced by one list per frequency, which the last exercise uses.

<!-- stage: exercises -->
### Exercises

#### [Build] Detach And Reinsert (Author exercise)
<!-- id: ds-detach-reinsert -->

**Prerequisites.** The `detach` and `insertFront` methods in this lesson.

**Problem.** A doubly linked list stores distinct integer keys between a head sentinel and a tail sentinel. Given the keys in order from head to tail and one key `k` that is present, move the node of `k` directly after the head sentinel using one detach and one insert. Return the keys in head-to-tail order after the move. The method must keep all four neighbour links correct: the old predecessor's `next`, the old successor's `prev`, and the moved node's own `prev` and `next`. Verify the result with a forward walk from the head and a backward walk from the tail, and require the backward walk to be the reverse of the forward walk.

**Constraints.** The limits are:
- **Length** is `1 <= keys.length <= 1000`.
- **Keys** are distinct `int` values.
- **Key k** is present in `keys`.
- **Mutation** is allowed on the list nodes, and `keys` is read only.
- **Return value** is a new `int[]` of the same length.

**Example 1.** Input `keys = [4,7,1,9]` and `k = 1`, output `[1,4,7,9]`.

**Example 2.** Input `keys = [4,7,1,9]` and `k = 9`, the cold-end node, output `[9,4,7,1]`.

**Hint.** After the detach, the old predecessor and the old successor must point at each other. Which sentinel does the old successor equal when the moved node is the last real node?

**Changed decision.** First exercise in the sequence: the move is one detach and one insert, and a two-direction walk proves every link.

#### [Vary] LRU Cache With Resize (LeetCode 146)
<!-- id: ds-lru-resize -->

**Prerequisites.** The cache in this lesson and the Detach And Reinsert exercise above.

**Problem.** Design a cache with three operations. `get(key)` returns the value for the key, or -1 when absent, and marks the key as most recently used. `put(key, value)` inserts or updates the key, marks it most recently used, and evicts the least recently used key when the size would exceed the capacity. `resize(newCapacity)` sets the capacity to `newCapacity` and evicts from the least recent end until the size is at most `newCapacity`. It returns the evicted keys as an `int[]` in eviction order. When `newCapacity` is 0, the cache stores nothing and every `put` does nothing.

**Constraints.** The limits are:
- **Initial capacity** is `1 <= capacity <= 1000`.
- **New capacity** is `0 <= newCapacity <= 1000`.
- **Keys and values** are `int` values.
- **Eviction by put** is silent and is not part of any returned array.
- **Cost** of get and put is O(1) average, and resize costs O(evicted + 1).

**Example 1.** Input capacity 3, then `put(1,10)`, `put(2,20)`, `put(3,30)`, `get(1)`, `resize(1)`. Output 10 for the get and `[2,3]` for the resize.

**Example 2.** Input capacity 2, then `put(5,50)`, `put(6,60)`, `get(5)`, `resize(0)`, `get(5)`. Output 50, then `[6,5]`, then -1.

**Hint.** The cold end is `tail.prev`. A loop that repeats the same eviction step as `put` already gives eviction order.

**Changed decision.** The capacity becomes mutable, so eviction moves from one step inside `put` to a loop whose removed keys are reported.

#### [Boundary] Repeated Get And Capacity One (Author exercise)
<!-- id: ds-repeated-get-capacity-one -->

**Prerequisites.** The two exercises above.

**Problem.** Run a script of cache operations on the cache from the previous exercise. Each operation is an `int[]`: `{0,key}` is a get, `{1,key,value}` is a put, and `{2,newCapacity}` is a resize. After every operation, walk the list forward from the head sentinel and backward from the tail sentinel. Every node must appear exactly once in each walk, the backward walk must be the reverse of the forward walk, and the walk length must equal the cache size. Return the keys of the final forward walk, hottest first.

**Constraints.** The limits are:
- **Initial capacity** is `1 <= capacity <= 20`.
- **Operations** number at most 200.
- **Keys** are in the range `0..9`.
- **Repeated get** on the same key must leave the list unchanged after the first call.
- **Resize to 0** leaves an empty list and an empty map.

**Example 1.** Input capacity 1, then `put(1,10)`, `get(1)` three times, and `put(2,20)`. Output `[2]`. A following `resize(0)` gives the output `[]`.

**Example 2.** Input capacity 3, then `put` for keys 1, 2 and 3, then `get(1)` three times. Output `[1,3,2]`.

**Hint.** A detach followed by an insert at the same place must still leave the node linked once. With one entry, which sentinel does `head.next` equal?

**Changed decision.** The tests check a structural fact, one appearance per node in both directions, instead of only checking returned values.

#### [Recognize] LFU Cache With Eviction Log (LeetCode 460)
<!-- id: ds-lfu-evicted-sequence -->

**Prerequisites.** All three exercises above.

**Problem.** Design a cache with fixed capacity and two operations. `get(key)` returns the value or -1, and counts as one use of the key. `put(key, value)` inserts or updates the key, and an update counts as one use. A new key starts with use count 1. When a new key arrives and the cache is full, the cache evicts the key with the lowest use count. Among keys with equal use counts, it evicts the least recently used one. Each eviction appends the evicted key to a log. Run a script of operations and return the log as an `int[]`.

**Constraints.** The limits are:
- **Capacity** is `1 <= capacity <= 1000` and never changes.
- **Operations** are `{0,key}` for get and `{1,key,value}` for put.
- **Script length** is at most 10,000 operations.
- **Log order** is eviction order.
- **Cost** of each operation is O(1) average.

**Example 1.** Input capacity 2, then `put(1,1)`, `put(2,2)`, `get(1)`, `put(3,3)`, `get(3)`, `put(4,4)`. Output `[2,1]`.

**Example 2.** Input capacity 2, then `put(1,1)`, `put(2,2)`, `put(1,5)`, `put(3,3)`. Output `[2]`, because the update raised the use count of key 1.

**Hint.** Keep one recency list for each use count, and remember the smallest use count that still has a node. Which list does a touched node leave, and which one does it join?

**Changed decision.** The single recency list becomes a family of lists indexed by use count, while the map still holds the shared nodes.
