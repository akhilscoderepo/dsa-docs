<!-- lesson-kind: standard -->
<!-- lesson-id: direct-stores -->
## Store Keys In Direct Slots

<!-- stage: context -->
### Why Membership Checks Slow Down

A port scanner probes all 65 536 TCP ports of a host and records which ones answered. The first version keeps the answers in an `ArrayList<Integer>` and calls `contains` before every insert, to avoid duplicates. On a host that answers on 60 000 ports, the last probes each scan tens of thousands of stored numbers just to learn that the port is new. The scan that should take milliseconds takes seconds.

The same shape appears whenever a program must remember a set of small integers, a table from ids to values, or an ordered list that supports changes in the middle. Interview prompts often add a rule: no library `HashSet` or `HashMap` is allowed. This lesson asks one question. How can a class decide where a key belongs by looking at the key alone, so that every later call checks only that one place?

<!-- stage: naive -->
### Searching A List For Each Key

The simple store keeps every key in one growing list. To add a key, the method searches the list and appends the key only when the search finds nothing. To test or remove a key, it searches the same list from the front.

```java
final class ListSet {
    private final java.util.List<Integer> keys = new java.util.ArrayList<>();

    boolean add(int key) {
        if (keys.contains(key)) return false;
        keys.add(key);
        return true;
    }

    boolean contains(int key) { return keys.contains(key); }

    boolean remove(int key) { return keys.remove((Integer) key); }
}
```

The class is correct. After adding 40, 7 and 19, a call to `contains(19)` compares 19 with 40, then 7, then 19 and answers true. The cast in `remove` matters, because `remove(int)` on a list deletes by index while `remove(Object)` deletes by value.

<!-- stage: bottleneck -->
### Counting The Searches

```predict
A set holds 50 000 distinct keys in the list-based class. About how many comparisons does one more `add` of a new key make, and how many does `add` make for 50 000 new keys in total?

One `add` of a new key compares it with all 50 000 stored keys before it appends, so it costs about 50 000 comparisons. Adding 50 000 new keys in total costs about 1.25 billion comparisons, because the list length grows from 0 to 50 000 and the costs add up to roughly n squared over 2.
```

Each call searches the whole list, so one operation costs O(n) for a store holding n keys, and n operations cost O(n^2). The cost grows with the number of stored keys, although the answer to a single question depends on one key only.

The waste has a precise form. The search reads keys that cannot equal the query, such as 40 when the query is 19. Nothing in the store tells the search which stored keys are worth reading. The store keeps keys in arrival order, and arrival order carries no information about a key's value. A better store must place each key by its value. Then a later query computes the same place from the same value and reads only that place.

<!-- stage: insight -->
### Giving Every Key One Fixed Place

#### Direct Slots For A Small Domain

Suppose every key is an integer from 0 to `D - 1` for a known `D`. The store allocates a `boolean[D]` array. Array position `k` is the **direct slot** of key `k`, because the key is its own index. The slot holds `true` when the set contains `k` and `false` otherwise.

<!-- names: direct slot, bucket, hash function -->

An add writes `true` to slot `k`, a remove writes `false`, and a contains reads the slot. Each call touches one array position, so the cost is O(1). The store owns each key in exactly one place, and that place never changes. We call this the **ownership rule**: a call may change only the place that belongs to its key.

#### Buckets For A Large Domain

A domain of all `int` values, or of 10^6 keys with only a few hundred stored, makes the direct array too large or too empty. The store then uses a smaller array of `B` **buckets**. A bucket is one array position that owns a short chain of nodes, and each node holds one key. A **hash function** maps a key to a bucket index. For non-negative keys, the function `key % B` is enough.

Two different keys can share one bucket, such as 6 and 10 when `B = 4`. The chain in that bucket holds both nodes. A lookup computes the bucket index, then walks only that chain and compares keys by value. Because the hash function is deterministic, the key always returns to the same bucket, and no other bucket can contain it.

#### Updates And Removals Keep Ownership

A map stores a value next to each key. A put on a key that already has a node changes the value in that node and creates no second node. A get that finds no node returns an explicit absent result, which differs from a stored value such as 0. A remove unlinks the node from its own chain and touches no other bucket.

The same ownership rule governs an indexed list. Its head field owns the first node, its tail field owns the last node, and its size field counts the chain. Every insert and delete must update all three fields before the call returns. A chain bucket and a linked list therefore share one habit: each mutation changes exactly the fields that own the affected nodes.

With a good hash function and `B` close to the number of stored keys `n`, a chain holds O(1) nodes on average. The cost per call is O(1 + n / B) in expectation and O(n) in the worst case, when every key falls in one bucket.

<!-- stage: variables -->
### Fields That Describe One Store

Each store keeps a few fields that together describe one logical state, and every public call must leave them in agreement.

- **present** is the `boolean[]` array in the direct set, where `present[k]` is true exactly when key `k` is stored.
- **buckets** is the array of chain heads, where `buckets[b]` is the first node of bucket `b` or `null` when the bucket is empty.
- **B** is the number of buckets, and `key % B` is the bucket index of a non-negative key.
- **node** is one chain element with a key, a value in the map, and a `next` reference.
- **head**, **tail** and **size** are the linked list fields: the first node, the last node, and the number of nodes.

The invariant is that every stored key appears in exactly one place, which is the slot or the chain that its hash function selects, and that the counts and end references agree with the chains after every call.

<!-- stage: trace -->
### Tracing Slots And Chains

#### Direct Slots For Keys Up To 7

The first trace uses a direct set with domain 8, so the cells are the slot indexes 0 to 7. The pointer `key` marks the slot that the current call reads or writes. The calls run in order: add 3, add 5, add 3 again, remove 5, contains 5, contains 3.

The first add writes slot 3, and the second add writes slot 5. The repeated add of 3 finds the slot already true, so it changes nothing and reports that the key was present. The remove of 5 clears only slot 5, and the following contains of 5 reads that slot and finds false. The last call finds slot 3 still true. No call ever reads a slot other than the one numbered by its key, which is the reason each call costs one step.

```trace
{"cells":["0","1","2","3","4","5","6","7"],"pointers":["key"],"steps":[{"at":{"key":3},"vars":{"stored":"3"},"note":"add 3: slot 3 was false, so the call writes true there and reports a new key."},{"at":{"key":5},"vars":{"stored":"3,5"},"note":"add 5: slot 5 was false, so the call writes true there and reports a new key."},{"at":{"key":3},"vars":{"stored":"3,5"},"note":"add 3: slot 3 is already true, so nothing changes and the call reports that the key was present."},{"at":{"key":5},"vars":{"stored":"3"},"note":"remove 5: slot 5 was true, so the call writes false there and no other slot changes."},{"at":{"key":5},"vars":{"stored":"3"},"note":"contains 5: the call reads slot 5 and finds false."},{"at":{"key":3},"vars":{"stored":"3"},"note":"contains 3: the call reads slot 3 and finds true."}]}
```

#### Buckets For Four Chains

The second trace uses four buckets, so the cells are the bucket indexes 0 to 3. The pointer `b` marks the bucket chosen by `key % 4`. The calls run in order: add 6, add 10, add 3, add 10 again, remove 6, contains 10.

Keys 6 and 10 both map to bucket 2, so the second add walks the one-node chain, finds no equal key and links a new node at the chain head. The key 3 maps to bucket 3 and leaves bucket 2 untouched. The repeated add of 10 finds 10 at the head of bucket 2 and stops because the keys are equal. The remove of 6 walks past the head node 10 and unlinks the last node, and key 10 stays reachable from the bucket head. The final contains computes bucket 2 again and finds 10 after one comparison. Each step reads the one bucket that the key selects, and the other three buckets are never visited.

```trace
{"cells":["0","1","2","3"],"pointers":["b"],"steps":[{"at":{"b":2},"vars":{"chains":"0:- | 1:- | 2:6 | 3:-"},"note":"add 6: 6 % 4 = 2. The chain of bucket 2 has no equal key, so a new node becomes its head."},{"at":{"b":2},"vars":{"chains":"0:- | 1:- | 2:10,6 | 3:-"},"note":"add 10: 10 % 4 = 2. The chain of bucket 2 has no equal key, so a new node becomes its head."},{"at":{"b":3},"vars":{"chains":"0:- | 1:- | 2:10,6 | 3:3"},"note":"add 3: 3 % 4 = 3. The chain of bucket 3 has no equal key, so a new node becomes its head."},{"at":{"b":2},"vars":{"chains":"0:- | 1:- | 2:10,6 | 3:3"},"note":"add 10: bucket 2 holds 10 already, so the walk compares and stops without a new node."},{"at":{"b":2},"vars":{"chains":"0:- | 1:- | 2:10 | 3:3"},"note":"remove 6: 6 % 4 = 2. The walk finds the node and unlinks it, and the other buckets stay untouched."},{"at":{"b":2},"vars":{"chains":"0:- | 1:- | 2:10 | 3:3"},"note":"contains 10: 10 % 4 = 2. The walk of bucket 2 reaches key 10 and answers true."}]}
```

<!-- stage: code -->
### Direct Set And Chained Set

#### Two Containers

The two classes below use the same three method names. The direct set indexes an array by the key. The chained set indexes an array of chain heads by `key % buckets.length`. Both assume non-negative keys.

```java
final class Stores {
    static final class DirectSet {
        private final boolean[] present;

        DirectSet(int domain) { present = new boolean[domain]; }

        boolean add(int key) {
            if (present[key]) return false;
            present[key] = true;
            return true;
        }

        boolean contains(int key) { return present[key]; }

        boolean remove(int key) {
            if (!present[key]) return false;
            present[key] = false;
            return true;
        }
    }

    static final class ChainedSet {
        private static final class Node {
            final int key;
            Node next;
            Node(int key, Node next) { this.key = key; this.next = next; }
        }

        private final Node[] buckets;

        ChainedSet(int bucketCount) { buckets = new Node[bucketCount]; }

        private int bucketOf(int key) { return key % buckets.length; }

        boolean contains(int key) {
            for (Node n = buckets[bucketOf(key)]; n != null; n = n.next) if (n.key == key) return true;
            return false;
        }

        boolean add(int key) {
            if (contains(key)) return false;
            int b = bucketOf(key);
            buckets[b] = new Node(key, buckets[b]);
            return true;
        }

        boolean remove(int key) {
            int b = bucketOf(key);
            Node prev = null;
            for (Node n = buckets[b]; n != null; prev = n, n = n.next) {
                if (n.key != key) continue;
                if (prev == null) buckets[b] = n.next; else prev.next = n.next;
                return true;
            }
            return false;
        }
    }
}
```

#### Cost And Java Details

- **DirectSet** costs O(1) time per call and O(D) space for the domain size `D`.
- **ChainedSet** costs O(1 + n / B) expected time per call and O(B + n) space.

The remove method keeps a `prev` reference because a singly linked chain cannot step backward. When the removed node is the chain head, the bucket array entry itself changes. Java arrays of references start with `null` entries, which is why an empty bucket needs no setup. The expression `key % buckets.length` is non-negative only for non-negative keys, because the Java remainder keeps the sign of the dividend.

<!-- stage: applicability -->
### When Direct Placement Applies

#### Recognizing The Shape

Reach for this design when the prompt forbids a library map or set, or when it states a small key range such as 0 to 10^6. A request to implement `put`, `get` and `remove` from scratch, or a list with head, tail and index operations, has the same shape. Before coding, state the invariant that each key has one deterministic place, and that each update or removal changes only the fields that own that place.

#### Choosing Between The Layouts

Use a direct array when the whole domain fits in memory and the keys are dense enough to justify it. A domain of 10^6 booleans takes about one megabyte, which is acceptable. Use chains when the domain is huge or unknown, and choose `B` as a prime near the expected number of keys so that keys spread evenly. Use a head, tail and size triple when the order of elements matters and the key is a position, not a value.

#### Two False Friends

A false friend of the map is the sentinel return. A `get` that returns 0 for a missing key cannot be told apart from a stored 0, so the contract must name a separate absent result or check for the node. A second false friend is the list's tail reference. A delete that unlinks the last node but leaves `tail` pointing at it breaks the next append silently, because the fields no longer describe the same list.

Do not use a chained table when the problem needs keys in sorted order, since chains hold no order across buckets. A balanced tree or a sorted array serves that case.

<!-- stage: exercises -->
### Exercises

#### [Build] Boolean Direct Set (Author exercise)
<!-- id: sc-direct-boolean-set -->

**Prerequisites.** The direct slot and the ownership rule from this lesson.

**Problem.** Design a class `DirectSet` with a constructor `DirectSet(int domain)` that creates an empty set of integer keys drawn from `0..domain-1`. The method `add(key)` inserts the key and returns `true` when the key was absent, or `false` when it was already present. The method `remove(key)` deletes the key and returns `true` when the key was present, or `false` otherwise. The method `contains(key)` returns `true` exactly when the key is stored. A key outside `0..domain-1` makes any of the three methods throw `IllegalArgumentException`.

**Constraints.** The limits are:
- **Domain** is `1 <= domain <= 10^6`.
- **Keys** are `int` values, and values outside the domain throw.
- **Calls** number at most 10^5, and each call must cost O(1).
- **Library** classes `HashSet`, `HashMap` and `List` are not allowed.

**Example 1.** Input `domain = 10` and the calls `add(4)`, `add(4)`, `contains(4)`, `remove(4)`, `remove(4)`, `contains(4)`, output `true, false, true, true, false, false`.

**Example 2.** Input `domain = 3` and the calls `add(0)`, `contains(2)`, `add(2)`, `remove(0)`, `contains(0)`, output `true, false, true, true, false`. A later `add(3)` throws.

**Hint.** Which array index can hold the answer for key `k` without any search, and what must a repeated add report?

**Changed decision.** Basic case: the key is the array index, so no search and no collision exist.

#### [Vary] Design HashSet (LeetCode 705)
<!-- id: sc-bucketed-hash-set -->

**Prerequisites.** The Boolean Direct Set exercise above and the chained set from the code stage.

**Problem.** Design a class `MyHashSet` with `add(key)`, `remove(key)` and `contains(key)` over integer keys. The set holds no duplicates, `add` of a stored key changes nothing, and `remove` of an absent key changes nothing. Use no built-in hash table. The memory used must not depend on the key range, so a direct array over all keys is not allowed.

**Constraints.** The limits are:
- **Keys** satisfy `0 <= key <= 10^6`.
- **Calls** number at most 10^4 in total.
- **Memory** must stay proportional to the number of stored keys plus the bucket count.
- **Return** values: `add` and `remove` return nothing, and `contains` returns a `boolean`.

**Example 1.** Input the calls `add(5)`, `add(9)`, `contains(5)`, `contains(6)`, `remove(5)`, `contains(5)`, output `true, false, false` for the three `contains` calls.

**Example 2.** Input 769 buckets and the calls `add(3)`, `add(772)`, `remove(3)`, `contains(772)`, `contains(3)`, output `true, false`. Keys 3 and 772 share a bucket.

**Hint.** Which bucket must a key reach on every call, and what must `remove` do when the key sits behind another node?

**Changed decision.** The direct array becomes an array of chains, so two keys can share a place and each call must compare keys by value.

#### [Boundary] Design HashMap (LeetCode 706)
<!-- id: sc-map-absent-update -->

**Prerequisites.** The Design HashSet exercise above.

**Problem.** Design a class `MyHashMap` with `put(key, value)`, `get(key)` and `remove(key)` over integer keys and non-negative integer values. The call `put` inserts the pair, or replaces the value when the key already exists. The call `get` returns the stored value, or `-1` when the key is absent. The call `remove` deletes the pair when it exists. Use no built-in hash table.

**Constraints.** The limits are:
- **Keys** satisfy `0 <= key <= 10^6`.
- **Values** satisfy `0 <= value <= 10^6`, so `0` is a legal stored value and `-1` is never stored.
- **Calls** number at most 10^4 in total.
- **Update** of an existing key must reuse its node and must not add a second pair.

**Example 1.** Input the calls `put(2, 0)`, `get(2)`, `get(5)`, `put(2, 7)`, `get(2)`, `remove(2)`, `get(2)`, output `0, -1, 7, -1` for the four `get` calls.

**Example 2.** Input 769 buckets and the calls `put(1, 1)`, `put(770, 5)`, `put(1, 9)`, `get(770)`, `get(1)`, `remove(1)`, `get(770)`, output `5, 9, 5`. Keys 1 and 770 share a bucket.

**Hint.** What distinguishes a stored 0 from a missing key, and where must the second `put` of the same key write?

**Changed decision.** The node now carries a value, so a lookup must separate "no node found" from "node found with value 0", and a repeated key must change the node in place.

#### [Recognize] Design Linked List (LeetCode 707)
<!-- id: sc-list-head-tail-size -->

**Prerequisites.** The Design HashMap exercise above.

**Problem.** Design a class `MyLinkedList` that stores integers in a singly linked chain with zero-based positions. The call `get(index)` returns the value at the position, or `-1` when the position does not exist. The calls `addAtHead(val)` and `addAtTail(val)` insert at the ends. The call `addAtIndex(index, val)` inserts the value so that it occupies the position `index`, appends when `index` equals the current size, and does nothing when `index` is greater than the size or negative. The call `deleteAtIndex(index)` removes the node at the position and does nothing for an invalid position.

**Constraints.** The limits are:
- **Values** satisfy `0 <= val <= 1000`.
- **Indexes** are `int` values, and invalid ones leave the list unchanged.
- **Calls** number at most 2000 in total.
- **Library** list classes are not allowed, so the class stores its own nodes.

**Example 1.** Input the calls `addAtHead(4)`, `addAtTail(8)`, `addAtIndex(1, 6)`, `get(1)`, `deleteAtIndex(2)`, `addAtTail(3)`, `get(2)`, output `6, 3`. The list is `4, 6, 8` after the third call and `4, 6, 3` at the end.

**Example 2.** Input on an empty list the calls `addAtIndex(1, 5)`, `get(0)`, `addAtIndex(0, 5)`, `deleteAtIndex(0)`, `addAtTail(2)`, `get(0)`, output `-1, 2`. The first call is ignored because 1 exceeds the size 0.

**Hint.** After any delete, which of `head`, `tail` and `size` can still point at a node that no longer belongs to the chain?

**Changed decision.** The key is now a position, so a chain walk replaces the hash function, and three fields must agree after every call.
